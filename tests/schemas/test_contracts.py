"""Tests for Pydantic's structural boundary contracts."""

from datetime import UTC, datetime
import unittest
from uuid import UUID

from pydantic import ValidationError

from app.domain.job import JobStatus
from app.domain.message_attempt import MessageAttemptStatus
from app.schemas import ContactContract, JobContract, MessageAttemptContract, MessageContract


class ContactContractTests(unittest.TestCase):
    def test_accepts_required_primitive_fields_without_domain_validation(self) -> None:
        contact = ContactContract(id=UUID(int=1), name=" ", phone="not normalized")

        self.assertEqual(contact.id, UUID(int=1))
        self.assertEqual(contact.phone, "not normalized")

    def test_requires_fields_and_rejects_wrong_primitive_types(self) -> None:
        with self.assertRaises(ValidationError):
            ContactContract(name="Alex", phone="+14155550123")  # type: ignore[call-arg]

        with self.assertRaises(ValidationError):
            ContactContract(id=UUID(int=1), name=42, phone="+14155550123")  # type: ignore[arg-type]

    def test_rejects_unexpected_fields(self) -> None:
        with self.assertRaises(ValidationError):
            ContactContract(id=UUID(int=1), name="Alex", phone="1234567", is_admin=True)  # type: ignore[call-arg]


class MessageContractTests(unittest.TestCase):
    def test_requires_id_and_content_but_does_not_apply_domain_invariants(self) -> None:
        message = MessageContract(id=UUID(int=2), content="  ")

        self.assertEqual(message.content, "  ")


class MessageAttemptContractTests(unittest.TestCase):
    def test_validates_enum_and_parses_uuid_datetime_strings(self) -> None:
        attempt = MessageAttemptContract.model_validate(
            {
                "id": "00000000-0000-0000-0000-000000000003",
                "message_id": "00000000-0000-0000-0000-000000000004",
                "recipient_contact_id": "00000000-0000-0000-0000-000000000005",
                "status": "sent",
                "provider_reference": "generic-ref",
                "created_at": "2026-09-30T10:00:00Z",
                "completed_at": "2026-09-30T10:00:02Z",
            }
        )

        self.assertEqual(attempt.status, MessageAttemptStatus.SENT)
        self.assertEqual(attempt.id, UUID(int=3))
        self.assertEqual(attempt.created_at, datetime(2026, 9, 30, 10, tzinfo=UTC))

    def test_rejects_unknown_enum_value(self) -> None:
        with self.assertRaises(ValidationError):
            MessageAttemptContract.model_validate(
                {
                    "id": UUID(int=3),
                    "message_id": UUID(int=4),
                    "recipient_contact_id": UUID(int=5),
                    "status": "delivered",
                    "created_at": datetime(2026, 9, 30, tzinfo=UTC),
                }
            )

    def test_serializes_to_json_compatible_data_and_round_trips(self) -> None:
        attempt = MessageAttemptContract(
            id=UUID(int=3),
            message_id=UUID(int=4),
            recipient_contact_id=UUID(int=5),
            status=MessageAttemptStatus.FAILED,
            error="provider rejected request",
            created_at=datetime(2026, 9, 30, 10, tzinfo=UTC),
            completed_at=datetime(2026, 9, 30, 10, 1, tzinfo=UTC),
        )

        serialized = attempt.model_dump(mode="json")
        restored = MessageAttemptContract.model_validate(serialized)

        self.assertEqual(serialized["id"], str(UUID(int=3)))
        self.assertEqual(serialized["status"], "failed")
        self.assertEqual(restored, attempt)


class JobContractTests(unittest.TestCase):
    def test_parses_status_and_defaults_optional_fields(self) -> None:
        job = JobContract.model_validate(
            {
                "id": UUID(int=6),
                "status": "pending",
                "created_at": datetime(2026, 9, 30, 10, tzinfo=UTC),
            }
        )

        self.assertEqual(job.status, JobStatus.PENDING)
        self.assertIsNone(job.started_at)
        self.assertIsNone(job.completed_at)
        self.assertIsNone(job.error)


if __name__ == "__main__":
    unittest.main()
