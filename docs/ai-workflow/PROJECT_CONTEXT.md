# SMS Messenger — Project Context

SMS Messenger is a modular application for preparing and sending SMS messages to selected contacts. It addresses the need to send a clearly reviewed message to a small, explicitly selected group and retain an outcome for each recipient.

## MVP

The planned MVP will import contacts from SQL, allow selection of at most five contacts, validate telephone information, compose and preview a message, require explicit confirmation, send through an abstract provider, record a result for each recipient, and retain attempt history.

## Outside the MVP

Bulk messaging, queues and workers, production deployment/infrastructure, authentication, and any specific provider integration remain out of scope. MISSION-004 separately authorizes only the initial PostgreSQL persistence code; it does not provision production infrastructure. Real sending requires a later mission and explicit authorization.

## Approved direction

Use a modular layered architecture: Models, Schemas, Core, Services, Repositories, Database, Providers, API/UI, Tests, and Documentation. Services coordinate application operations; repositories abstract persistence; providers abstract external SMS integrations. Do not introduce microservices.

## Current phase

MISSION-001 established project and agent documentation. MISSION-002 added infrastructure-independent domain entities, MISSION-002.5 added a backend learning glossary, MISSION-003 added transport-neutral schema contracts, and MISSION-004 added initial PostgreSQL persistence infrastructure. MISSION-004's live database integration verification is still pending a dedicated PostgreSQL test database. Repositories remain for separately authorized MISSION-005 work.
