# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Fastapi celery example."""
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from celery_app.tasks import long_task

app = FastAPI()


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
