# Architecture

The approved direction is a modular, layered application. The layers below describe responsibilities. The domain, transport-neutral schema/contracts, and initial PostgreSQL persistence infrastructure are implemented. Repositories and all application/service and transport layers remain planned.

| Component | Responsibility |
| --- | --- |
| Models | Represent domain concepts and behavior independent of transport and persistence details. |
| Schemas | Validate and shape data at boundaries such as API requests and responses. |
| Core | Hold shared configuration and foundational application concerns when introduced. |
| Services | Coordinate application use cases and enforce application-level rules, including rejecting more than five recipients. |
| Repositories | Abstract persistence and data access behind interfaces used by application operations. |
| Database / Persistence | Configure PostgreSQL, SQLAlchemy engine/sessions, ORM models, and explicit domain mappings. |
| Providers | Adapt external services, including SMS gateways, behind application-facing contracts. |
| API | Expose application operations through a transport boundary. |
| UI | Let a user select recipients, compose, preview, and confirm an operation. |

## Separation of services and repositories

Services coordinate a use case; repositories perform and abstract data access. Keeping these responsibilities separate prevents application workflows from containing direct SQL and makes them testable without binding business operations to one persistence implementation.

## Provider independence

Application logic depends on an abstract provider contract rather than a specific SMS vendor. Provider adapters can then change independently, and application behavior can be tested without contacting a real external service. No provider is implemented in the current repository.

## Dependency direction

Users interact through UI, web, or CLI boundaries. Those boundaries call application services. Services coordinate repositories and providers through abstractions. Repositories reach the SQL database; provider adapters reach external SMS services. This is a target design, not a description of existing code.

The approved schema technology is Pydantic in `app/schemas/` (DECISION-006). Domain entities remain independent Python dataclasses; schema and ORM models do not replace them. Schema contracts are transport-neutral and do not implement API routes.

MISSION-004 places SQLAlchemy models, mapping, PostgreSQL engine/session setup, and explicit development/test schema creation in `app/infrastructure/persistence/`. Domain code does not import SQLAlchemy. Repositories remain a separate, unimplemented layer for MISSION-005.
