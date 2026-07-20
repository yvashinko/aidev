import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from task_service.config import settings
from task_service.repository import init_db
from task_service.routers import tasks

logging.basicConfig(level=settings.log_level.upper())

app = FastAPI(title="Task Service")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
def generic_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "type": "about:blank",
            "title": "Internal Server Error",
            "status": 500,
            "detail": str(exc),
        },
    )


app.include_router(tasks.router)
