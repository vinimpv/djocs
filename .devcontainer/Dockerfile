FROM mcr.microsoft.com/devcontainers/base:ubuntu

ENV container=docker

ENV OPENFAAS_URL=http://localhost:8080

RUN sudo apt-get update > /dev/null \
	# Node.js
	&& wget -qO- https://deb.nodesource.com/setup_lts.x | sudo sh \
	# Common
	&& sudo apt-get install -y file nodejs \
	# Arkade
	&& curl -fsSL https://get.arkade.dev | sudo sh

COPY --chmod=755 ./bootstrap.sh ./bootstrap.sh

ENTRYPOINT ["./bootstrap.sh"]
