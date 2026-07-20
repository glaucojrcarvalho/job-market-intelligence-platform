"""Database engine and session factory helpers."""

from __future__ import annotations

from collections.abc import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SessionFactory = Callable[[], Session]


def session_factory_from_url(database_url: str) -> SessionFactory:
    engine = create_engine(database_url, future=True)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, class_=Session)
    return factory
