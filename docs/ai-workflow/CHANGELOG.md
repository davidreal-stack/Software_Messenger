# AI Workflow Changelog

## 2026-09-28 — MISSION-001 — Initialize AI Workflow v1

- Added the project context, current-state snapshot, architecture, decision log, business rules, operational rules, glossary, import glossary, roadmap, and mission registry.
- Added architecture reference documents and conceptual architecture, project-structure, and domain diagrams.
- Added `.codex/AGENTS.md` as the Codex operating contract.
- Created the initial `docs/` and `.codex/` structure in an empty workspace.
- Reason: establish persistent project context and agent guidance before implementation.
- No application code or dependencies were added.

## 2026-09-30 — MISSION-002 — Domain Foundation

- Added the `app.domain` package with Contact, Message, MessageAttempt, and Job entities and domain-only unit tests.
- Added documented decisions for UUID identifiers, minimal phone syntax, provider-independent message content, and initial lifecycle states.
- Updated the domain architecture, glossary, data model, project structure, mission registry, and current state to match implementation.
- Reason: implement the explicitly authorized first application layer while keeping it independent of database, API, and external services.
- No external dependencies were introduced. MISSION-001.5 Git/GitHub setup remains paused at the user's request.

## 2026-09-30 — MISSION-002.5 — Backend Learning Glossary

- Added five concise Spanish glossary pages covering Python syntax, dataclasses, datetime/UTC, regex, and UUID as used by the current domain code.
- Converted `IMPORT_GLOSSARY.md` into a short index and added an incremental backend-glossary rule to `.codex/AGENTS.md`.
- Updated the project structure map, mission registry, and current state.
- Reason: make intermediate backend constructs easier to learn from the project's actual code without creating a generic language manual.
- Documentation only; application code, tests, and dependencies were not changed.

## 2026-09-30 — MISSION-003 — Schemas / Contracts

- Recorded the owner-approved Pydantic decision and the explicit policy to reject unexpected schema fields.
- Added four transport-neutral data contracts under `app/schemas/`, eight schema tests, and the Pydantic v2 project dependency.
- Added a Spanish Pydantic glossary page and updated the dependency/glossary index, project structure, architecture notes, mission registry, and current state.
- Reason: validate, represent, and serialize boundary data while keeping domain entities and future infrastructure layers separate.
- No domain entities, services, repositories, database, providers, API routes, HTTP layer, recipient-limit rule, sending flow, Git, or GitHub were implemented.

## 2026-10-03 — MISSION-004 — Persistence / Database

- Added SQLAlchemy 2.x persistence models, explicit domain mappers, PostgreSQL engine/session configuration, and opt-in schema creation.
- Selected PostgreSQL for development, tests, and production with Psycopg 3; persisted status values as checked strings.
- Added structural, mapper, and database setup tests, including an isolated-schema PostgreSQL CRUD integration test activated by `TEST_DATABASE_URL`.
- Recorded the persistence boundary, database target, schema setup, and status storage decisions; updated architecture and learning documentation.
- Live PostgreSQL integration verification remains pending because the inspected environment has no PostgreSQL service or `TEST_DATABASE_URL`.
- No repositories, services, providers, API, SMS sending, recipient-limit enforcement, job processing, Git, or GitHub operations were introduced.
