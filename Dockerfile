FROM python:3.11 as base
WORKDIR /app

FROM base as builder

RUN pip install --upgrade pip && \
    pip install poetry==1.6.1

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN mkdir app
RUN touch app/__init__.py

RUN poetry config virtualenvs.in-project true
RUN poetry install
RUN poetry build

FROM base as final

COPY --from=builder /app/.venv /opt/.venv
COPY --from=builder /app/dist .
RUN /opt/.venv/bin/pip install *.whl

ENV PATH="/opt/.venv/bin:$PATH"

COPY . .
