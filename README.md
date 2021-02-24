Using Celery with FastAPI
========

This repository implements the second example of [flask-celery-example](https://github.com/miguelgrinberg/flask-celery-example.git) with FastAPI.

Quick Start
-----------
### Run with docker-compose
Just one-line command ```docker-compose up -d```to start up the redis, Fastapi server, flower and our worker.

Then just go to http://localhost:8000/ to try our application!

And monitor the execution of celery tasks by flower through http://localhost:5555 !
### Run without docker

1. Clone this repository.
2. Start a local Redis server.
3. Start a Celery worker:
    - on Linux OS:
    `celery -A celery_app worker --loglevel=info`
    - on windows OS:
    `celery -A celery_app worker --pool=solo --loglevel=info`
4. Start Celery Flower to monitor. `celery -A main.celery_app flower`
5. Start the Fastapi web server. `poetry run python main.py`
