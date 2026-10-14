# System Architecture

SMS Messenger is a modular layered application. The implemented foundation contains domain dataclasses, Pydantic boundary contracts, and initial persistence infrastructure under `app/infrastructure/persistence/`. The persistence package configures PostgreSQL with SQLAlchemy 2.x and Psycopg 3, maps separate ORM models to the domain dataclasses, and provides explicit schema creation for development/tests.

The domain does not depend on SQLAlchemy or PostgreSQL. Services and repositories remain unimplemented; when added, repositories will use the persistence infrastructure and services will coordinate use cases without direct SQL. Provider adapters, API routes, UI, queues, and SMS delivery also remain unimplemented. Production schema migrations are not selected by MISSION-004.
