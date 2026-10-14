"""Behavioral unit tests for the infrastructure-independent domain."""

from datetime import UTC, datetime, timedelta
import unittest
from uuid import UUID

from app.domain import (
    Contact,
    Job,
    JobStatus,
    Message,
    MessageAttempt,
    MessageAttemptStatus,
)


class ContactTests(unittest.TestCase):
    def test_creates_contact_and_normalizes_phone_formatting(self) -> None:
        contact = Contact("  Alex Rivera ", " +1 (415) 555-0123 ")

        self.assertEqual(contact.name, "Alex Rivera")
        self.assertEqual(contact.phone, "+14155550123")
        self.assertIsInstance(contact.id, UUID)

    def test_rejects_blank_name(self) -> None:
        with self.assertRaises(ValueError):
            Contact("  ", "14155550123")

    def test_rejects_invalid_phone(self) -> None:
        for phone in ("", "12345", "01234567", "+1+4155550123", "abc1234567"):
            with self.subTest(phone=phone), self.assertRaises(ValueError):
                Contact("Alex", phone)


class MessageTests(unittest.TestCase):
    def test_creates_message_without_changing_content(self) -> None:
        message = Message("  Hello there!  ")

        self.assertEqual(message.content, "  Hello there!  ")
        self.assertIsInstance(message.id, UUID)

    def test_rejects_empty_or_whitespace_content(self) -> None:
        for content in ("", " \n\t"):
            with self.subTest(content=content), self.assertRaises(ValueError):
                Message(content)


class MessageAttemptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.created_at = datetime(2026, 9, 30, 12, tzinfo=UTC)
        self.attempt = MessageAttempt(
            message_id=UUID(int=1),
            recipient_contact_id=UUID(int=2),
            created_at=self.created_at,
        )

    def test_starts_pending_and_sent_transition_preserves_original(self) -> None:
        sent_at = self.created_at + timedelta(seconds=2)

        sent = self.attempt.mark_sent("provider-ref-123", at=sent_at)

        self.assertEqual(self.attempt.status, MessageAttemptStatus.PENDING)
        self.assertEqual(sent.status, MessageAttemptStatus.SENT)
        self.assertEqual(sent.provider_reference, "provider-ref-123")
        self.assertEqual(sent.completed_at, sent_at)

    def test_failed_transition_requires_and_records_error(self) -> None:
        failed = self.attempt.mark_failed(
            "  recipient rejected  ",
            provider_reference="provider-ref-failed",
            at=self.created_at + timedelta(seconds=1),
        )

        self.assertEqual(failed.status, MessageAttemptStatus.FAILED)
        self.assertEqual(failed.provider_reference, "provider-ref-failed")
        self.assertEqual(failed.error, "recipient rejected")
        self.assertIsNotNone(failed.completed_at)

    def test_cannot_complete_attempt_twice(self) -> None:
        sent = self.attempt.mark_sent()

        with self.assertRaises(ValueError):
            sent.mark_failed("late failure")

    def test_failure_requires_nonblank_error(self) -> None:
        with self.assertRaises(ValueError):
            self.attempt.mark_failed("  ")


class JobTests(unittest.TestCase):
    def setUp(self) -> None:
        self.created_at = datetime(2026, 9, 30, 12, tzinfo=UTC)
        self.job = Job(created_at=self.created_at)

    def test_starts_pending_and_completes_through_running(self) -> None:
        running = self.job.start(at=self.created_at + timedelta(seconds=1))
        completed = running.complete(at=self.created_at + timedelta(seconds=2))

        self.assertEqual(self.job.status, JobStatus.PENDING)
        self.assertEqual(running.status, JobStatus.RUNNING)
        self.assertEqual(completed.status, JobStatus.COMPLETED)
        self.assertEqual(completed.started_at, self.created_at + timedelta(seconds=1))

    def test_pending_job_can_fail_without_starting(self) -> None:
        failed = self.job.fail("cancelled before start", at=self.created_at + timedelta(seconds=1))

        self.assertEqual(failed.status, JobStatus.FAILED)
        self.assertIsNone(failed.started_at)
        self.assertEqual(failed.error, "cancelled before start")

    def test_rejects_invalid_lifecycle_transition(self) -> None:
        with self.assertRaises(ValueError):
            self.job.complete()

        completed = self.job.start().complete()
        with self.assertRaises(ValueError):
            completed.fail("too late")


if __name__ == "__main__":
    unittest.main()
