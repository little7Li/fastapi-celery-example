# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Fastapi celery example."""
import os
import random
import time

import uvicorn
from celery import Celery
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

app = FastAPI()


if not bool(os.getenv("DOCKER")):  # running example without docker
    celery_app = Celery(
        "worker",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/1",
    )
else:  # running example with docker
    celery_app = Celery(
        "worker",
        broker="redis://redis:6379/0",
        backend="redis://redis:6379/1",
    )


@celery_app.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
    adjective = ["master", "radiant", "silent", "harmonic", "fast"]
    noun = ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"]
    message = ""
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = f"{random.choice(verb)} {random.choice(adjective)} " \
                f"{random.choice(noun)}"
        self.update_state(state="PROGRESS",
                          meta={
                              "current": i,
                              "total": total,
                              "status": message,
                          })
        time.sleep(1)
    return {
        "current": 100,
        "total": 100,
        "status": "Task completed!",
        "result": 42,
    }


@app.get("/")
def index():
    """Entry of the service."""
    return HTMLResponse(open("index.html", "r", encoding="utf8").read())


@app.post("/longtask", status_code=202)
def longtask(request: Request, response: Response):
    """Accept long running task."""
    task = long_task.apply_async()
    response.headers["location"] = request.url_for(
        "taskstatus", **{"task_id": task.id})
    return {}


@app.get("/status/{task_id}")
def taskstatus(task_id):
    """Query tasks status."""
    task = long_task.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
