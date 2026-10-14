# Decision Log

Record decisions using this format:

- **ID and title**
- **Status and date**
- **Context**
- **Problem**
- **Alternatives considered**
- **Decision**
- **Reason**
- **Consequences**

## DECISION-001 — Separation of Services and Repositories

- **Status:** Approved; 2026-09-28
- **Context:** The application needs use cases that coordinate validation, persistence, and eventually SMS delivery.
- **Problem:** Combining application workflows with SQL access couples business operations to storage and makes isolated testing harder.
- **Alternatives considered:** Put persistence queries directly in services; separate persistence behind repositories; defer the boundary until later.
- **Decision:** Services coordinate application operations, while repositories abstract persistence and data access. Services must not contain direct SQL implementation.
- **Reason:** The split keeps application coordination independent of persistence details and supports modular testing.
- **Consequences:** Future persistence work must be accessed through repository abstractions; the boundary should be introduced only when authorized implementation work needs it.

## DECISION-002 — Domain identifiers use UUIDs

- **Status:** Approved; 2026-09-30
- **Context:** Domain entities need stable identifiers before a persistence layer exists.
- **Problem:** Database-generated IDs would couple the domain to infrastructure that this phase does not implement.
- **Alternatives considered:** Database-generated integers; caller-supplied strings; standard-library UUID4 identifiers.
- **Decision:** Each entity receives a UUID4 by default and accepts a UUID for deterministic construction or later rehydration.
- **Reason:** UUIDs are available in the Python standard library and need no database or package dependency.
- **Consequences:** Persistence and serialization missions must preserve UUID identity and decide their boundary representation.

## DECISION-003 — Minimal telephone syntax validation

- **Status:** Approved; 2026-09-30
- **Context:** BR-002 requires valid telephone information before sending, but no country-specific validation policy or telephone library is defined.
- **Problem:** The domain needs a useful syntax check without pretending to verify assignment, reachability, or country-specific validity.
- **Alternatives considered:** Accept any non-empty string; add a phone-number dependency; enforce a small E.164-like syntax rule without external metadata.
- **Decision:** Accept 7–15 digits, optionally prefixed by `+`, require the first digit to be 1–9, and remove spaces, parentheses, periods, and hyphens before storing. Reject other characters.
- **Reason:** This is a small provider-independent syntax guard and uses no external service or dependency.
- **Consequences:** It is not a guarantee that a number is assigned or reachable. Country-specific parsing and normalization remain future decisions.

## DECISION-004 — Message content has no provider-specific length limit

- **Status:** Approved; 2026-09-30
- **Context:** Message content must not be empty, but no project limit is documented and SMS limits depend on encoding and provider behavior.
- **Problem:** An arbitrary character cap would silently introduce transport policy into the logical domain message.
- **Alternatives considered:** Choose a generic character cap now; model encoding/segments; reject blank content and defer transport limits.
- **Decision:** Reject non-string, empty, or whitespace-only content, preserve nonblank content as supplied, and impose no length or encoding limit in the domain.
- **Reason:** It protects the basic invariant without implementing SMS segmentation or encoding policy.
- **Consequences:** A later authorized application/provider mission must handle any transport-specific constraints.

## DECISION-005 — Minimal domain lifecycle states

- **Status:** Approved; 2026-09-30
- **Context:** MessageAttempt and Job need explicit MVP-level status and transition behavior; the previous documentation named these concepts but did not define their states.
- **Problem:** The entities need valid initial and terminal states without prematurely modeling retries, queues, cancellation, or delivery receipts.
- **Alternatives considered:** Leave states unspecified; add a broad workflow; use minimal pending/sent/failed attempt states and pending/running/completed/failed job states.
- **Decision:** MessageAttempt starts pending and can complete once as sent or failed. It may retain a generic optional provider reference or a failure reason, and uses UTC timestamps. Job starts pending, may start, then complete, or fail while pending/running. Domain values are immutable; transitions return updated values.
- **Reason:** These states express the requested per-recipient result and simple future operation tracking without implementing a worker system.
- **Consequences:** `sent` records an attempt outcome and does not claim carrier delivery. Retry, cancellation, progress aggregation, and delivery receipts remain undecided and out of scope.

## DECISION-006 — Pydantic for Schemas / Contracts

- **Status:** Approved by project owner; 2026-09-30
- **Context:** MISSION-003 requires explicit boundary contracts for contact, message, attempt, and job data.
- **Problem:** The project needs structured validation and serialization at application boundaries without making domain entities depend on schema technology.
- **Alternatives considered:** Pydantic models in the boundary layer; Python dataclasses as schemas; replacing domain entities with validation models.
- **Decision:** Use Pydantic in `app/schemas/` for boundary data validation, structured contracts, and serialization/deserialization. Keep `app/domain/` independent of Pydantic and keep its entities as Python dataclasses; Pydantic models must not replace them. Database models, repositories, services, providers, and API routes remain separate concerns.
- **Reason:** This is the explicit project-owner approval supplied for MISSION-003 and preserves the existing layer boundaries.
- **Consequences:** Pydantic is a direct project dependency for schemas only. Future services may coordinate conversions when authorized; this mission adds no conversion or orchestration layer.

## DECISION-007 — Schema contracts reject unknown fields

- **Status:** Approved for MISSION-003; 2026-09-30
- **Context:** Contracts are intended to describe explicit, predictable data shapes, and MISSION-003 requires a defined policy for unexpected fields.
- **Problem:** Pydantic's default handling would silently ignore unrecognized fields, which can hide a mismatch between a boundary and its contract.
- **Alternatives considered:** Ignore extra input using the library default; preserve arbitrary extra data; reject fields not declared by a contract.
- **Decision:** Configure schema contracts with `extra="forbid"`.
- **Reason:** A closed shape makes structural mismatches explicit and testable without adding business validation.
- **Consequences:** A boundary payload with undeclared keys is rejected and must be deliberately reflected in a future contract change.

## DECISION-008 — SQLAlchemy Persistence Boundary

- **Status:** Approved by project owner; 2026-10-03
- **Context:** MISSION-004 adds database persistence after the domain dataclasses and Pydantic contracts are established.
- **Problem:** The project needs a concrete ORM layer without coupling domain entities to SQLAlchemy or database sessions.
- **Alternatives considered:** Map domain dataclasses directly with the ORM; keep separate persistence models and explicit mappers; defer the ORM boundary.
- **Decision:** Use SQLAlchemy 2.x in `app/infrastructure/persistence/`, with separate ORM models and explicit domain-to-persistence mappers. The domain may be imported by the mapping/infrastructure layer, but `app/domain/` must not import SQLAlchemy, sessions, engines, or persistence modules.
- **Reason:** This preserves the existing domain boundary while preparing a concrete persistence foundation for the later repository mission.
- **Consequences:** `ContactModel`, `MessageModel`, `MessageAttemptModel`, and `JobModel` are separate from domain dataclasses. Repositories, services, and database use cases remain later missions.

## DECISION-009 — PostgreSQL and Psycopg 3

- **Status:** Approved by project owner; 2026-10-03
- **Context:** The persistence implementation needs one target database for development, tests, and production.
- **Problem:** An unspecified or temporary database target could create implementation and deployment differences.
- **Alternatives considered:** Select SQLite for local convenience; leave the database configurable across several engines; use PostgreSQL consistently.
- **Decision:** PostgreSQL is the target engine for development, tests, and production, accessed with SQLAlchemy 2.x and the Psycopg 3 driver. Connection configuration uses `DATABASE_URL` and explicitly selects `postgresql+psycopg`.
- **Reason:** This is the project owner's explicit engine and driver decision and avoids creating a temporary SQLite persistence path.
- **Consequences:** Tests requiring live database behavior use a dedicated PostgreSQL `TEST_DATABASE_URL`; credentials remain outside source control. SQLAlchemy is used to keep connection and SQL mechanics out of the domain.

## DECISION-010 — Explicit Development and Test Schema Creation

- **Status:** Approved for MISSION-004; 2026-10-03
- **Context:** Initial persistence needs a repeatable way to create tables for development and tests.
- **Problem:** Automatic schema mutation on import or treating table creation as a production migration system would make lifecycle behavior implicit.
- **Alternatives considered:** Create tables during module import; expose explicit SQLAlchemy metadata creation; add a migration framework now.
- **Decision:** Expose an explicit `create_schema(...)` function backed by `Base.metadata.create_all(...)`. It is intended only for controlled development/test setup and is never called automatically. No production migration framework is selected in this mission.
- **Reason:** This supplies the current scoped setup mechanism without introducing Alembic or defining future production migration policy.
- **Consequences:** Callers must opt into schema creation. A later mission must select and implement production migration management before relying on schema evolution in production.

## DECISION-011 — Persist Lifecycle Statuses as Checked Strings

- **Status:** Approved for MISSION-004; 2026-10-03
- **Context:** `JobStatus` and `MessageAttemptStatus` are domain string enums whose values describe MVP lifecycle states.
- **Problem:** Persistence must prevent unknown status strings while retaining readable string values and avoiding PostgreSQL-specific native enum lifecycle coupling.
- **Alternatives considered:** Unchecked text; PostgreSQL native enum types; SQLAlchemy non-native enum types stored as strings with checks.
- **Decision:** Store status values as lowercase strings in `VARCHAR` columns using SQLAlchemy `Enum(..., native_enum=False, create_constraint=True, values_callable=...)`, which creates a check constraint for the allowed values.
- **Reason:** This provides controlled, readable string persistence without creating PostgreSQL native enum types or duplicating transition rules in the database.
- **Consequences:** Mappers preserve the domain enum value. Domain lifecycle validation remains in `app/domain/`; the database enforces only membership in the current status set.
