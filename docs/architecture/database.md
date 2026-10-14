# Database and Persistence

## Approved target

PostgreSQL is the project's target database for development, tests, and production. SQLAlchemy 2.x provides the ORM and connection/session integration; Psycopg 3 is selected as its PostgreSQL driver. Configure connections with `DATABASE_URL` using the `postgresql+psycopg` scheme. Do not commit connection credentials.

## Implemented boundary

`app/infrastructure/persistence/` contains:

- `database.py`: SQLAlchemy declarative metadata, PostgreSQL engine configuration, session factory, and explicit schema creation.
- `models.py`: `ContactModel`, `MessageModel`, `MessageAttemptModel`, and `JobModel`.
- `mappers.py`: explicit conversion between each domain dataclass and its ORM model.

Domain objects remain plain dataclasses and do not import SQLAlchemy or database configuration. Message attempts have foreign keys to their message and recipient contact. Statuses are stored as checked `VARCHAR` strings using the domain enum values; this does not add database transition rules.

## Schema lifecycle

Call `create_schema(engine)` explicitly to create missing tables for controlled development or test setup. Importing modules does not connect to a database or create tables. This `metadata.create_all` mechanism is not the production migration strategy; selecting migration management remains future work. No migration package is currently used.

## Test database

`TEST_DATABASE_URL` may point to a dedicated PostgreSQL test database using `postgresql+psycopg`. The database integration test creates and removes a uniquely named schema so it does not clear or replace existing schemas. Run it only against a database intended for tests. Structural model and mapper tests do not need a running database.

Repositories remain the future abstraction through which application services will access persistence; no repository is implemented yet.
