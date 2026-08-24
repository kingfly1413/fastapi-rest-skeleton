"""Application-level error and its FastAPI handler."""

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Raised by services/repositories to map to a uniform HTTP error."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
