FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.2.2

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR  /src

COPY poetry.lock pyproject.toml /src/
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main --no-interaction --no-ansi

COPY . /src

CMD [ "uvicorn", "restaurant_menu_app.main:app" , "--host", "0.0.0.0"]