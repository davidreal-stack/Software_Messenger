# Glossary

Definitions describe the approved project vocabulary. Contact, Message, MessageAttempt, and Job are implemented as infrastructure-independent domain entities by MISSION-002; application and infrastructure layers remain planned.

| Term | Project meaning |
| --- | --- |
| Model | A representation of data. The domain entities are plain Python domain objects; separate SQLAlchemy ORM models represent persisted rows. |
| ORM model | A SQLAlchemy class mapped to a database table. These classes live in `app/infrastructure/persistence/models.py` and do not replace domain dataclasses. |
| Mapper | A conversion function between a domain entity and its corresponding persistence model. It copies data and does not perform database access or use cases. |
| Schema | A boundary-oriented definition used to validate or serialize data. Project contracts are Pydantic models under `app/schemas/`, separate from domain dataclasses. |
| Service | An application-layer coordinator for a use case and its business rules. |
| Repository | An abstraction for persistence and data access. |
| Provider | An adapter for an external service, such as an SMS gateway. |
| Entity | A domain object with identity over its lifecycle; current entities use UUID identifiers. |
| Message | The provider-independent, nonblank logical content prepared for delivery. |
| MessageAttempt | A record for one message and one contact, with a pending/sent/failed outcome and optional generic provider reference or error. |
| Job | A minimal pending/running/completed/failed operation record; it does not execute work. |
| Batch | A group of recipients or message work processed together; bulk behavior is outside the current implementation phase. |
| Application Layer | The part of the system that coordinates use cases, represented by Services. |
| Infrastructure | Concrete technical integrations such as PostgreSQL access through SQLAlchemy and external provider adapters. |
