Using Celery with FastAPI
========

This repository implements the second example of [flask-celery-example](https://github.com/miguelgrinberg/flask-celery-example.git) with FastAPI.

Quick Start
-----------
1. Clone this repository.
2. Start a local Redis server.
3. Start a Celery worker:
    - on Linux OS:
    `celery -A main.celery_app worker --loglevel=info`
    - on windows OS:
    `celery -A main.celery_app worker --pool=solo --loglevel=info`
4. Start Celery Flower to monitor. `celery -A main.celery_app flower`
5. Start the Fastapi web server. `poetry run python main.py`
