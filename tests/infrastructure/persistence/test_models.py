"""Structural tests for persistence tables and relationships."""

import ast
from datetime import UTC, datetime
from pathlib import Path
import unittest
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, Enum, Text, Uuid, inspect

from app.domain import JobStatus, MessageAttemptStatus
from app.infrastructure.persistence import Base
from app.infrastructure.persistence.models import ContactModel, JobModel, MessageAttemptModel, MessageModel


class PersistenceModelTests(unittest.TestCase):
    def test_models_register_expected_tables_and_uuid_primary_keys(self) -> None:
        self.assertEqual(
            set(Base.metadata.tables),
            {"contacts", "messages", "message_attempts", "jobs"},
        )

        for model in (ContactModel, MessageModel, MessageAttemptModel, JobModel):
            with self.subTest(model=model.__name__):
                table = model.__table__
                self.assertEqual([column.name for column in table.primary_key.columns], ["id"])
                identifier = table.c.id
                self.assertIsInstance(identifier.type, Uuid)
                self.assertIs(identifier.type.as_uuid, True)
                self.assertFalse(identifier.nullable)

    def test_required_fields_and_optional_fields_have_expected_nullability(self) -> None:
        for column in (ContactModel.__table__.c.name, ContactModel.__table__.c.phone, MessageModel.__table__.c.content):
            with self.subTest(column=column):
                self.assertFalse(column.nullable)
                self.assertIsInstance(column.type, Text)

        attempt = MessageAttemptModel.__table__.c
        for name in ("message_id", "recipient_contact_id", "status", "created_at"):
            with self.subTest(field=name):
                self.assertFalse(attempt[name].nullable)
        for name in ("provider_reference", "error", "completed_at"):
            with self.subTest(field=name):
                self.assertTrue(attempt[name].nullable)

        job = JobModel.__table__.c
        for name in ("id", "status", "created_at"):
            with self.subTest(field=f"job.{name}"):
                self.assertFalse(job[name].nullable)
        for name in ("started_at", "completed_at", "error"):
            with self.subTest(field=f"job.{name}"):
                self.assertTrue(job[name].nullable)

    def test_attempt_foreign_keys_and_bidirectional_relationships(self) -> None:
        foreign_keys = {foreign_key.target_fullname for foreign_key in MessageAttemptModel.__table__.foreign_keys}
        self.assertEqual(foreign_keys, {"messages.id", "contacts.id"})

        contact_relationships = inspect(ContactModel).relationships
        message_relationships = inspect(MessageModel).relationships
        attempt_relationships = inspect(MessageAttemptModel).relationships
        self.assertEqual(set(contact_relationships.keys()), {"attempts"})
        self.assertEqual(set(message_relationships.keys()), {"attempts"})
        self.assertEqual(set(attempt_relationships.keys()), {"message", "recipient_contact"})
        self.assertIs(contact_relationships["attempts"].mapper.class_, MessageAttemptModel)
        self.assertIs(message_relationships["attempts"].mapper.class_, MessageAttemptModel)
        self.assertIs(attempt_relationships["message"].mapper.class_, MessageModel)
        self.assertIs(attempt_relationships["recipient_contact"].mapper.class_, ContactModel)

    def test_statuses_are_checked_string_values(self) -> None:
        expectations = (
            (MessageAttemptModel, MessageAttemptStatus, "message_attempt_status"),
            (JobModel, JobStatus, "job_status"),
        )
        for model, status_type, enum_name in expectations:
            with self.subTest(model=model.__name__):
                column_type = model.__table__.c.status.type
                self.assertIsInstance(column_type, Enum)
                self.assertFalse(column_type.native_enum)
                self.assertTrue(column_type.create_constraint)
                self.assertEqual(column_type.name, enum_name)
                self.assertEqual(column_type.enums, [status.value for status in status_type])
                check = next(item for item in model.__table__.constraints if isinstance(item, CheckConstraint))
                check_sql = str(check.sqltext.compile(compile_kwargs={"literal_binds": True}))
                for status in status_type:
                    self.assertIn(status.value, check_sql)

    def test_models_can_be_constructed_without_business_validation(self) -> None:
        contact = ContactModel(id=UUID(int=1), name=" ", phone="unvalidated")
        message = MessageModel(id=UUID(int=2), content=" ")
        attempt = MessageAttemptModel(
            id=UUID(int=3),
            message_id=message.id,
            recipient_contact_id=contact.id,
            status=MessageAttemptStatus.PENDING,
            created_at=datetime.now(UTC),
        )
        job = JobModel(
            id=UUID(int=4),
            status=JobStatus.PENDING,
            created_at=attempt.created_at,
        )

        self.assertEqual(contact.phone, "unvalidated")
        self.assertEqual(message.content, " ")
        self.assertEqual(attempt.status, MessageAttemptStatus.PENDING)
        self.assertEqual(job.status, JobStatus.PENDING)
        self.assertIsInstance(attempt.__table__.c.created_at.type, DateTime)
        self.assertTrue(attempt.__table__.c.created_at.type.timezone)

    def test_domain_source_does_not_import_sqlalchemy_or_infrastructure(self) -> None:
        domain_directory = Path(__file__).resolve().parents[3] / "app" / "domain"
        for source_path in domain_directory.glob("*.py"):
            tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    imported = [node.module]
                else:
                    continue
                with self.subTest(file=source_path.name, imports=imported):
                    self.assertFalse(any(name == "sqlalchemy" or name.startswith("sqlalchemy.") for name in imported))
                    self.assertFalse(any(name.startswith("app.infrastructure") for name in imported))


if __name__ == "__main__":
    unittest.main()
