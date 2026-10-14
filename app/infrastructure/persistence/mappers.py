"""Explicit conversion between domain dataclasses and SQLAlchemy models."""

from app.domain import Contact, Job, Message, MessageAttempt
from app.infrastructure.persistence.models import ContactModel, JobModel, MessageAttemptModel, MessageModel


def contact_to_model(contact: Contact) -> ContactModel:
    return ContactModel(id=contact.id, name=contact.name, phone=contact.phone)


def contact_from_model(model: ContactModel) -> Contact:
    return Contact(id=model.id, name=model.name, phone=model.phone)


def message_to_model(message: Message) -> MessageModel:
    return MessageModel(id=message.id, content=message.content)


def message_from_model(model: MessageModel) -> Message:
    return Message(id=model.id, content=model.content)


def message_attempt_to_model(attempt: MessageAttempt) -> MessageAttemptModel:
    return MessageAttemptModel(
        id=attempt.id,
        message_id=attempt.message_id,
        recipient_contact_id=attempt.recipient_contact_id,
        status=attempt.status,
        provider_reference=attempt.provider_reference,
        error=attempt.error,
        created_at=attempt.created_at,
        completed_at=attempt.completed_at,
    )


def message_attempt_from_model(model: MessageAttemptModel) -> MessageAttempt:
    return MessageAttempt(
        id=model.id,
        message_id=model.message_id,
        recipient_contact_id=model.recipient_contact_id,
        status=model.status,
        provider_reference=model.provider_reference,
        error=model.error,
        created_at=model.created_at,
        completed_at=model.completed_at,
    )


def job_to_model(job: Job) -> JobModel:
    return JobModel(
        id=job.id,
        status=job.status,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error=job.error,
    )


def job_from_model(model: JobModel) -> Job:
    return Job(
        id=model.id,
        status=model.status,
        created_at=model.created_at,
        started_at=model.started_at,
        completed_at=model.completed_at,
        error=model.error,
    )
