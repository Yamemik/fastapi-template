FROM python:3.12-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && \
   apt install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

COPY . .