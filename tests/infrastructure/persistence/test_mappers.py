"""Round-trip tests for domain-to-persistence mapping."""

from datetime import UTC, datetime, timedelta
import unittest
from uuid import UUID

from app.domain import Contact, Job, Message, MessageAttempt
from app.infrastructure.persistence.mappers import (
    contact_from_model,
    contact_to_model,
    job_from_model,
    job_to_model,
    message_attempt_from_model,
    message_attempt_to_model,
    message_from_model,
    message_to_model,
)


class PersistenceMapperTests(unittest.TestCase):
    def test_contact_domain_model_round_trip(self) -> None:
        domain = Contact(id=UUID(int=1), name="Alex Rivera", phone="+14155550123")

        model = contact_to_model(domain)
        restored = contact_from_model(model)

        self.assertEqual((model.id, model.name, model.phone), (domain.id, domain.name, domain.phone))
        self.assertEqual(restored, domain)

    def test_message_domain_model_round_trip(self) -> None:
        domain = Message(id=UUID(int=2), content="A logical message with no transport limit.")

        model = message_to_model(domain)
        restored = message_from_model(model)

        self.assertEqual((model.id, model.content), (domain.id, domain.content))
        self.assertEqual(restored, domain)

    def test_message_attempt_domain_model_round_trip_preserves_status_and_outcome(self) -> None:
        created_at = datetime(2026, 10, 3, 12, tzinfo=UTC)
        domain = MessageAttempt(
            id=UUID(int=3),
            message_id=UUID(int=2),
            recipient_contact_id=UUID(int=1),
            created_at=created_at,
        ).mark_failed(
            "recipient rejected",
            provider_reference="generic-reference",
            at=created_at + timedelta(seconds=2),
        )

        model = message_attempt_to_model(domain)
        restored = message_attempt_from_model(model)

        self.assertEqual(model.status, domain.status)
        self.assertEqual(model.provider_reference, domain.provider_reference)
        self.assertEqual(model.error, domain.error)
        self.assertEqual(model.created_at, domain.created_at)
        self.assertEqual(model.completed_at, domain.completed_at)
        self.assertEqual(restored, domain)

    def test_job_domain_model_round_trip_preserves_lifecycle_fields(self) -> None:
        created_at = datetime(2026, 10, 3, 12, tzinfo=UTC)
        domain = Job(id=UUID(int=4), created_at=created_at).start(at=created_at + timedelta(seconds=1))
        domain = domain.complete(at=created_at + timedelta(seconds=3))

        model = job_to_model(domain)
        restored = job_from_model(model)

        self.assertEqual(model.status, domain.status)
        self.assertEqual(model.created_at, domain.created_at)
        self.assertEqual(model.started_at, domain.started_at)
        self.assertEqual(model.completed_at, domain.completed_at)
        self.assertEqual(restored, domain)


if __name__ == "__main__":
    unittest.main()
