"""Application-level exceptions."""

from __future__ import annotations


class JobMarketError(Exception):
    """Base application error."""


class ResourceNotFoundError(JobMarketError):
    """Requested resource does not exist."""


class InvalidStateError(JobMarketError):
    """Application state does not support the requested operation."""
