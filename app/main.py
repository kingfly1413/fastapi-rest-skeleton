"""FastAPI application entrypoint: app instance, lifespan, routers, handlers."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config import get_settings
from app.core.exceptions import AppError, app_error_handler
from app.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev: create tables on startup. Replace with Alembic in production.
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_exception_handler(AppError, app_error_handler)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}
