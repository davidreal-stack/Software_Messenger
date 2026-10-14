"""Small shared helpers for domain timestamps."""

from datetime import UTC, datetime


def now_utc() -> datetime:
    return datetime.now(UTC)


def require_utc(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None or value.utcoffset().total_seconds() != 0:
        raise ValueError(f"{field_name} must be a timezone-aware UTC timestamp")
