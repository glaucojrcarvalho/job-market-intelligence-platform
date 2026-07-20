"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI

from job_market import __version__
from job_market.config.settings import Settings
from job_market.infrastructure.observability.metrics import MetricsRegistry
from job_market.interfaces.api.errors import register_exception_handlers
from job_market.interfaces.api.middleware import register_observability_middleware
from job_market.interfaces.api.routes import router
from job_market.shared.logging import configure_logging


def create_app() -> FastAPI:
    settings = Settings.from_env()
    configure_logging(settings.log_level)
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Production-oriented API for job market intelligence and candidate matching.",
    )
    app.state.metrics = MetricsRegistry()
    app.include_router(router)
    register_exception_handlers(app)
    register_observability_middleware(app, app.state.metrics)
    return app
