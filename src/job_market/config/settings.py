"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "job-market-intelligence-platform"
    environment: str = "development"
    log_level: str = "INFO"
    api_version: str = "v1"
    database_url: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            environment=os.getenv("APP_ENV", cls.environment),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            api_version=os.getenv("API_VERSION", cls.api_version),
            database_url=os.getenv("DATABASE_URL"),
        )
