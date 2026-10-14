"""Pydantic contracts for data crossing application boundaries."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.job import JobStatus
from app.domain.message_attempt import MessageAttemptStatus


class _ContractBase(BaseModel):
    """Common policy for explicit, closed data contracts."""

    model_config = ConfigDict(extra="forbid")


class ContactContract(_ContractBase):
    """Contact data represented at an application boundary."""

    id: UUID
    name: str
    phone: str


class MessageContract(_ContractBase):
    """Logical message data, independent of any delivery provider."""

    id: UUID
    content: str


class MessageAttemptContract(_ContractBase):
    """One message's outcome for a specific recipient."""

    id: UUID
    message_id: UUID
    recipient_contact_id: UUID
    status: MessageAttemptStatus
    provider_reference: str | None = None
    error: str | None = None
    created_at: datetime
    completed_at: datetime | None = None


class JobContract(_ContractBase):
    """Minimal operation tracking data; this contract executes no work."""

    id: UUID
    status: JobStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None
