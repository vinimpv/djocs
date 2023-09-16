FROM python:3.11-bullseye as base

WORKDIR /app


FROM base as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip
RUN pip install poetry==1.6.0
COPY pyproject.toml poetry.lock ./
RUN poetry export -o requirements.txt

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM base

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY /src .
COPY /scripts .

ENTRYPOINT ["./scripts/start.sh"]
