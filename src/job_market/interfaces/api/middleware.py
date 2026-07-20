"""FastAPI middleware for observability concerns."""

from __future__ import annotations

import logging
import time
import uuid

from fastapi import FastAPI, Request

from job_market.infrastructure.observability.metrics import MetricsRegistry
from job_market.shared.logging import request_id_var

logger = logging.getLogger(__name__)


def register_observability_middleware(app: FastAPI, metrics: MetricsRegistry) -> None:
    @app.middleware("http")
    async def observe_requests(request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        token = request_id_var.set(request_id)
        start = time.perf_counter()

        logger.info("request_started %s %s", request.method, request.url.path)
        try:
            response = await call_next(request)
        except Exception:
            latency_ms = (time.perf_counter() - start) * 1000
            metrics.record_request(request.url.path, latency_ms, 500)
            logger.exception("request_failed %s %s", request.method, request.url.path)
            request_id_var.reset(token)
            raise

        latency_ms = (time.perf_counter() - start) * 1000
        metrics.record_request(request.url.path, latency_ms, response.status_code)
        response.headers["x-request-id"] = request_id
        logger.info(
            "request_completed %s %s status=%s latency_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            latency_ms,
        )
        request_id_var.reset(token)
        return response
