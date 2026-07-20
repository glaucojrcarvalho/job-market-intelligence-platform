"""System-level response schemas."""

from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ReadinessResponse(BaseModel):
    status: str
    checks: dict[str, str]


class VersionResponse(BaseModel):
    app_name: str
    version: str
    environment: str


class MetricsResponse(BaseModel):
    requests_total: int
    errors_total: int
    routes: dict[str, dict[str, float | int]]
