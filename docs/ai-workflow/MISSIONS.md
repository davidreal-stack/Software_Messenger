# Mission Registry

## Standard mission structure

- Mission ID
- Objective
- Context
- Scope
- Allowed changes
- Forbidden changes
- Dependencies
- Acceptance criteria
- Tests
- Documentation requirements
- Result

## MISSION-001 — Initialize AI Workflow v1

- **Objective:** Establish persistent project documentation and Codex guidance.
- **Context:** The repository directory was empty at inspection time.
- **Scope:** Documentation and agent-guidance files required by the mission.
- **Allowed changes:** Create the requested workflow documents, architecture references, diagrams, and `.codex/AGENTS.md`.
- **Forbidden changes:** Application implementation, dependencies, real or fake SMS sending, provider connections, API/UI, database schema/models, queues/workers, bulk messaging, authentication, production infrastructure, and microservices.
- **Dependencies:** None introduced.
- **Acceptance criteria:** Required documentation exists and reflects the inspected repository; Git status is reported accurately.
- **Tests:** No application tests were applicable because no code or test suite existed. Structural/documentation checks were performed after creation.
- **Documentation requirements:** All required AI Workflow, architecture, diagram, and agent-guidance files; changelog and current-state update.
- **Result:** COMPLETED 2026-09-28. Documentation only. The directory was not a Git repository.

## MISSION-001.5 — Git + GitHub Infrastructure

- **Objective:** Initialize local Git controls and connect the existing GitHub repository.
- **Result:** BLOCKED / PAUSED at the user's request pending access to two-factor authentication. GitHub setup has not been completed; local Git initialization was not performed.

## MISSION-002 — Domain Foundation

- **Objective:** Implement the infrastructure-independent Contact, Message, MessageAttempt, and Job domain foundation.
- **Scope:** Domain entities, unit tests, and synchronized domain documentation only.
- **Dependencies:** None added; tests use standard-library `unittest`.
- **Result:** COMPLETED 2026-09-30. Twelve domain unit tests pass. No SQL, API, provider, SMS sending, queues, or workers were implemented.

## MISSION-002.5 — Backend Learning Glossary

- **Objective:** Create a concise, practical learning glossary tied to backend code already present.
- **Scope:** Documentation only: glossary entries, glossary index, agent guidance, current state, changelog, mission registry, and project structure map.
- **Forbidden changes:** Application code, tests, dependencies, Git/GitHub setup, or MISSION-003 implementation.
- **Result:** COMPLETED 2026-09-30. Added five backend glossary pages; MISSION-003 remains NOT STARTED.

## MISSION-003 — Schemas / Contracts

- **Objective:** Implement transport-neutral Pydantic contracts for MVP-relevant boundary data.
- **Scope:** Four data contracts, schema tests, the Pydantic dependency, and synchronized workflow/architecture/glossary documentation.
- **Dependencies:** `pydantic>=2.12,<3`, selected by owner decision DECISION-006.
- **Forbidden changes:** Changes to domain entities, database models, repositories, services, providers, API routes, HTTP endpoints, UI, recipient-limit enforcement, sending, preview/confirmation, Git, or GitHub.
- **Tests:** Eight schema tests and the full existing test suite passed with Python 3.14.5 and Pydantic 2.13.4.
- **Result:** COMPLETED 2026-09-30. Domain remains independent of Pydantic; no infrastructure or future mission was implemented.

## MISSION-004 — Persistence / Database

- **Objective:** Establish the initial PostgreSQL persistence infrastructure while keeping ORM models separate from domain dataclasses.
- **Scope:** SQLAlchemy 2.x engine/session configuration, Contact/Message/MessageAttempt/Job models, explicit mappers, controlled development/test schema creation, dependency and synchronized architecture documentation.
- **Decisions:** PostgreSQL is the target for development, tests, and production; Psycopg 3 is the driver. Status values are persisted as checked strings. Production migrations remain undecided.
- **Forbidden changes:** Repositories, services, providers, API, SMS, recipient maximum enforcement, job processing, Git/GitHub, or remote operations.
- **Tests:** Persistence structural tests, mapper round trips, database setup tests, and full suite. PostgreSQL CRUD integration is configured through `TEST_DATABASE_URL` and requires a dedicated PostgreSQL test database.
- **Result:** PARTIAL 2026-10-03. Persistence code, tests, decisions, and documentation were added. Live PostgreSQL persistence/retrieval verification was skipped because no local PostgreSQL service or `TEST_DATABASE_URL` was available. Domain remains independent of SQLAlchemy; no later mission was implemented.

## MISSION-005 — Repositories — NOT STARTED

Planned as the next separately authorized mission. No repository or interface is implemented by MISSION-004.
