from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import tasks, auth

STATIC_DIR = Path(__file__).parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Task Manager API",
    description="Simple REST API for managing tasks.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def frontend():
    return FileResponse(STATIC_DIR / "index.html")
