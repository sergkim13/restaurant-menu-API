FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.2.2

RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install "poetry==$POETRY_VERSION" --no-cache-dir && \
    poetry config virtualenvs.create false

WORKDIR  /src

COPY poetry.lock pyproject.toml /src/
RUN poetry install --no-root --only main --no-interaction --no-ansi --no-cache


COPY . /src