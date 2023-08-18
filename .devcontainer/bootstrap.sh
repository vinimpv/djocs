#!/bin/bash

set -o errexit

# create registry container unless it already exists
reg_name='kind-registry'
reg_port='5001'
if [ "$(docker inspect -f '{{.State.Running}}' "${reg_name}" 2>/dev/null || true)" != 'true' ]; then
    docker run \
        -d --restart=always -p "127.0.0.1:${reg_port}:5000" --name "${reg_name}" \
        registry:2
fi
# create a cluster with the local registry enabled in containerd

current_dir=$(dirname $0)
root_dir=$(dirname "$PWD")

cat <<EOF | kind create cluster --name local --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
    - |
      kind: InitConfiguration
      nodeRegistration:
        kubeletExtraArgs:
          node-labels: "ingress-ready=true"
  extraMounts:
    - hostPath: "$root_dir/app"
      containerPath: /projects
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
  - containerPort: 443
    hostPort: 443
  - containerPort: 4566
    hostPort: 4566
  - containerPort: 31432
    hostPort: 31432
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."localhost:${reg_port}"]
    endpoint = ["http://${reg_name}:5000"]
EOF


# connect the registry to the cluster network if not already connected
if [ "$(docker inspect -f='{{json .NetworkSettings.Networks.kind}}' "${reg_name}")" = 'null' ]; then
    docker network connect "kind" "${reg_name}"
fi

kubectl config use-context local
# Document the local registry
# https://github.com/kubernetes/enhancements/tree/master/keps/sig-cluster-lifecycle/generic/1755-communicating-a-local-registry
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:${reg_port}"
    help: "https://kind.sigs.k8s.io/docs/user/local-registry/"
EOF


kubectl apply -f "$current_dir/redis.yaml"
kubectl apply -f "$current_dir/localstack.yaml"
kubectl apply -f "$current_dir/postgresql.yaml"

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml



kubectl wait deployment --all --timeout=-60s --for=condition=Available -n default
kubectl wait deployment --all --timeout=-60s --for=condition=Available -n ingress-nginx

kubectl wait deployment --all --timeout=-240s --for=condition=Available -n ingress-nginx

echo "waiting for localstack to be ready"
kubectl wait deployment/localstack --timeout=-240s --for=condition=Available
kubectl exec deployment/localstack -- bash -c '
    #!/bin/bash
    set -e
    buckets=(
        "local-bucket"
    )
    for bucket in "${buckets[@]}"; do
      awslocal s3 mb s3://$bucket 2>&1 || true
    done
'

# try to create ingress until its available or fail after
echo "waiting for ingress to be ready"
for i in {1..10}; do
    echo "attempt to create ingress $i"
    kubectl apply -f "$current_dir/ingress.yaml" || sleep 10
done
