from fastapi import APIRouter

from app.api import health
from app.api.routers import projects, uploads

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])

