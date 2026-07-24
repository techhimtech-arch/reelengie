import sys
import os

# Ensure the backend package root is importable no matter how this file is
# launched (python app/main.py, uvicorn app.main:app, or via Electron).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

from fastapi.staticfiles import StaticFiles
from app.services.project_service import project_service
app.mount("/static", StaticFiles(directory=project_service.projects_dir), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8765)
