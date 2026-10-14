"""One recipient-specific delivery attempt and its outcome."""

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from ._time import now_utc, require_utc


class MessageAttemptStatus(StrEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class MessageAttempt:
    """An attempt to deliver one message to one contact."""

    message_id: UUID
    recipient_contact_id: UUID
    id: UUID = field(default_factory=uuid4)
    status: MessageAttemptStatus = MessageAttemptStatus.PENDING
    provider_reference: str | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=now_utc)
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not all(isinstance(value, UUID) for value in (self.id, self.message_id, self.recipient_contact_id)):
            raise ValueError("attempt, message, and recipient identifiers must be UUIDs")
        if not isinstance(self.status, MessageAttemptStatus):
            raise ValueError("status must be a MessageAttemptStatus")
        require_utc(self.created_at, "created_at")
        if self.completed_at is not None:
            require_utc(self.completed_at, "completed_at")
            if self.completed_at < self.created_at:
                raise ValueError("completed_at cannot precede created_at")

        if self.provider_reference is not None and not self.provider_reference.strip():
            raise ValueError("provider_reference must not be empty")
        if self.error is not None and not self.error.strip():
            raise ValueError("error must not be empty")

        if self.status is MessageAttemptStatus.PENDING:
            if self.completed_at is not None or self.error is not None or self.provider_reference is not None:
                raise ValueError("a pending attempt cannot have an outcome")
        elif self.status is MessageAttemptStatus.SENT:
            if self.completed_at is None or self.error is not None:
                raise ValueError("a sent attempt requires completed_at and cannot have an error")
        elif self.status is MessageAttemptStatus.FAILED:
            if self.completed_at is None or self.error is None:
                raise ValueError("a failed attempt requires completed_at and an error")
        else:
            raise ValueError("status must be a MessageAttemptStatus")

    def mark_sent(
        self,
        provider_reference: str | None = None,
        *,
        at: datetime | None = None,
    ) -> "MessageAttempt":
        """Return the sent outcome; attempts cannot be completed twice."""
        self._require_pending()
        completed_at = at or now_utc()
        require_utc(completed_at, "at")
        return replace(
            self,
            status=MessageAttemptStatus.SENT,
            provider_reference=provider_reference,
            completed_at=completed_at,
        )

    def mark_failed(
        self,
        error: str,
        *,
        provider_reference: str | None = None,
        at: datetime | None = None,
    ) -> "MessageAttempt":
        """Return the failed outcome with a non-empty reason."""
        self._require_pending()
        if not isinstance(error, str) or not error.strip():
            raise ValueError("error must not be empty")
        completed_at = at or now_utc()
        require_utc(completed_at, "at")
        return replace(
            self,
            status=MessageAttemptStatus.FAILED,
            provider_reference=provider_reference,
            error=error.strip(),
            completed_at=completed_at,
        )

    def _require_pending(self) -> None:
        if self.status is not MessageAttemptStatus.PENDING:
            raise ValueError("only a pending attempt can be completed")
