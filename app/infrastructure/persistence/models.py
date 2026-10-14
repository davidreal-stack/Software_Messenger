"""SQLAlchemy models kept separate from the domain dataclasses."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.job import JobStatus
from app.domain.message_attempt import MessageAttemptStatus
from app.infrastructure.persistence.database import Base


def _status_type(enum_type: type[JobStatus] | type[MessageAttemptStatus], name: str) -> Enum:
    """Store domain status values as checked VARCHAR strings, not native enums."""
    return Enum(
        enum_type,
        name=name,
        native_enum=False,
        create_constraint=True,
        validate_strings=True,
        values_callable=lambda members: [member.value for member in members],
    )


class ContactModel(Base):
    """Persistent representation of a domain Contact."""

    __tablename__ = "contacts"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)

    attempts: Mapped[list["MessageAttemptModel"]] = relationship(
        back_populates="recipient_contact",
    )


class MessageModel(Base):
    """Persistent representation of a domain Message."""

    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    attempts: Mapped[list["MessageAttemptModel"]] = relationship(
        back_populates="message",
    )


class MessageAttemptModel(Base):
    """Persistent per-contact outcome with structural message/contact links."""

    __tablename__ = "message_attempts"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    message_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("messages.id"),
        nullable=False,
    )
    recipient_contact_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contacts.id"),
        nullable=False,
    )
    status: Mapped[MessageAttemptStatus] = mapped_column(
        _status_type(MessageAttemptStatus, "message_attempt_status"),
        nullable=False,
    )
    provider_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    message: Mapped[MessageModel] = relationship(back_populates="attempts")
    recipient_contact: Mapped[ContactModel] = relationship(back_populates="attempts")


class JobModel(Base):
    """Persistent lifecycle record; it does not execute or schedule work."""

    __tablename__ = "jobs"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    status: Mapped[JobStatus] = mapped_column(
        _status_type(JobStatus, "job_status"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
