"""Tests for PostgreSQL configuration and explicit persistence setup."""

import os
import unittest
from unittest.mock import patch
from uuid import uuid4

from sqlalchemy import create_mock_engine, select
from sqlalchemy.schema import CreateSchema, DropSchema

from app.domain import Contact, Job, Message, MessageAttempt
from app.infrastructure.persistence import create_database_engine, create_schema, create_session_factory
from app.infrastructure.persistence.database import DATABASE_URL_ENV
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
from app.infrastructure.persistence.models import ContactModel, JobModel, MessageAttemptModel, MessageModel


TEST_DATABASE_URL_ENV = "TEST_DATABASE_URL"


class DatabaseConfigurationTests(unittest.TestCase):
    def test_engine_requires_a_configured_or_explicit_url(self) -> None:
        with patch.dict(os.environ, {DATABASE_URL_ENV: ""}):
            with self.assertRaisesRegex(RuntimeError, DATABASE_URL_ENV):
                create_database_engine()

    def test_engine_requires_the_approved_postgresql_driver(self) -> None:
        with self.assertRaisesRegex(ValueError, r"postgresql\+psycopg"):
            create_database_engine("sqlite://")

    def test_engine_uses_postgresql_and_psycopg_3(self) -> None:
        engine = create_database_engine("postgresql+psycopg://user:password@localhost/sms_messenger")
        try:
            self.assertEqual(engine.url.drivername, "postgresql+psycopg")
            self.assertEqual(engine.dialect.name, "postgresql")
            self.assertEqual(engine.url.database, "sms_messenger")
        finally:
            engine.dispose()

    def test_engine_reads_database_url_without_exposing_it(self) -> None:
        url = "postgresql+psycopg://user:password@localhost/sms_messenger"
        with patch.dict(os.environ, {DATABASE_URL_ENV: url}):
            engine = create_database_engine()
            try:
                self.assertEqual(engine.url.drivername, "postgresql+psycopg")
                self.assertEqual(engine.url.database, "sms_messenger")
            finally:
                engine.dispose()

    def test_session_factory_binds_sessions_without_connecting(self) -> None:
        engine = create_database_engine("postgresql+psycopg://user:password@localhost/sms_messenger")
        try:
            factory = create_session_factory(engine)
            with factory() as session:
                self.assertIs(session.bind, engine)
                self.assertTrue(session.expire_on_commit is False)
        finally:
            engine.dispose()

    def test_explicit_schema_creation_compiles_postgresql_tables(self) -> None:
        statements: list[str] = []
        engine = None

        def collect(statement, *multiparams, **params) -> None:
            statements.append(str(statement.compile(dialect=engine.dialect)))

        engine = create_mock_engine("postgresql+psycopg://", collect)
        create_schema(engine)
        sql = "\n".join(statements).lower()

        self.assertIn("create table contacts", sql)
        self.assertIn("create table messages", sql)
        self.assertIn("create table message_attempts", sql)
        self.assertIn("create table jobs", sql)
        self.assertIn("foreign key", sql)
        self.assertIn("check", sql)

    def test_postgresql_persistence_and_retrieval_in_an_isolated_schema(self) -> None:
        database_url = os.getenv(TEST_DATABASE_URL_ENV)
        if not database_url:
            self.skipTest(f"Set {TEST_DATABASE_URL_ENV} to a disposable PostgreSQL database to run this integration test")

        engine = create_database_engine(database_url)
        schema = f"test_persistence_{uuid4().hex}"
        schema_created = False
        try:
            with engine.begin() as connection:
                connection.execute(CreateSchema(schema))
            schema_created = True

            isolated_engine = engine.execution_options(schema_translate_map={None: schema})
            create_schema(isolated_engine)
            session_factory = create_session_factory(isolated_engine)

            created_at_contact = Contact(name="Alex Rivera", phone="+14155550123")
            created_at_message = Message(content="Persistence integration test")
            created_at_attempt = MessageAttempt(
                message_id=created_at_message.id,
                recipient_contact_id=created_at_contact.id,
            ).mark_sent("test-reference")
            created_at_job = Job()

            contact_model = contact_to_model(created_at_contact)
            message_model = message_to_model(created_at_message)
            attempt_model = message_attempt_to_model(created_at_attempt)
            attempt_model.message = message_model
            attempt_model.recipient_contact = contact_model
            job_model = job_to_model(created_at_job)

            with session_factory.begin() as session:
                session.add_all([contact_model, message_model, attempt_model, job_model])

            with session_factory() as session:
                loaded_contact = session.execute(
                    select(ContactModel).where(ContactModel.id == created_at_contact.id)
                ).scalar_one()
                loaded_message = session.execute(
                    select(MessageModel).where(MessageModel.id == created_at_message.id)
                ).scalar_one()
                loaded_attempt = session.execute(
                    select(MessageAttemptModel).where(MessageAttemptModel.id == created_at_attempt.id)
                ).scalar_one()
                loaded_job = session.execute(
                    select(JobModel).where(JobModel.id == created_at_job.id)
                ).scalar_one()

            self.assertEqual(contact_from_model(loaded_contact), created_at_contact)
            self.assertEqual(message_from_model(loaded_message), created_at_message)
            self.assertEqual(message_attempt_from_model(loaded_attempt), created_at_attempt)
            self.assertEqual(job_from_model(loaded_job), created_at_job)
        finally:
            if schema_created:
                with engine.begin() as connection:
                    connection.execute(DropSchema(schema, cascade=True))
            engine.dispose()


if __name__ == "__main__":
    unittest.main()
