"""Explicit PostgreSQL engine, session-factory, and schema setup."""

import os
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine, URL, make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL_ENV = "DATABASE_URL"
POSTGRESQL_DRIVER = "postgresql+psycopg"


class Base(DeclarativeBase):
    """Base metadata for persistence models."""


def create_database_engine(
    database_url: str | URL | None = None,
    **engine_options: Any,
) -> Engine:
    """Create a PostgreSQL engine using an explicit URL or ``DATABASE_URL``.

    The URL must select Psycopg 3 explicitly, for example
    ``postgresql+psycopg://user:password@localhost/database``.
    No connection or schema creation happens until the caller uses the engine.
    """
    configured_url = database_url if database_url is not None else os.getenv(DATABASE_URL_ENV)
    if configured_url is None or (isinstance(configured_url, str) and not configured_url.strip()):
        raise RuntimeError(f"Set {DATABASE_URL_ENV} or pass a PostgreSQL URL explicitly")

    url = make_url(configured_url)
    if url.drivername != POSTGRESQL_DRIVER:
        raise ValueError(f"Database URL must use the {POSTGRESQL_DRIVER} driver")

    return create_engine(url, **engine_options)


def create_session_factory(bind: Engine | Connection) -> sessionmaker[Session]:
    """Create sessions bound to a configured engine or connection."""
    return sessionmaker(bind=bind, expire_on_commit=False)


def create_schema(bind: Engine | Connection) -> None:
    """Create missing tables explicitly for development or tests.

    This is not a production migration mechanism. Callers opt in by invoking
    this function; importing persistence modules never creates database objects.
    """
    Base.metadata.create_all(bind=bind)
