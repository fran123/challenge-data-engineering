FROM python:3.13-slim

RUN pip install poetry==2.1.1

WORKDIR /app

ENV HOST 0.0.0.0

COPY pyproject.toml poetry.lock .env ./
COPY app ./app

RUN touch README.md

RUN poetry install

ENTRYPOINT ["poetry", "run", "start"]
