FROM python:3.8-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV DOCKER=true

COPY . /celery_app/

ENTRYPOINT celery \
    -A celery_app \
    worker \
    --loglevel INFO