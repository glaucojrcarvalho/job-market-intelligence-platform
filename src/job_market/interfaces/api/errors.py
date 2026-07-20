"""FastAPI error handling."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from job_market.shared.exceptions import JobMarketError, ResourceNotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ResourceNotFoundError)
    async def handle_not_found(_: Request, exc: ResourceNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": "not_found", "message": str(exc)},
        )

    @app.exception_handler(JobMarketError)
    async def handle_application_error(_: Request, exc: JobMarketError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": "application_error", "message": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": "validation_error", "details": exc.errors()},
        )
