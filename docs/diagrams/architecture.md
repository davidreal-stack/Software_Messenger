# Conceptual Architecture

```mermaid
flowchart TD
    User[User] --> Boundary[UI / Web / CLI<br/>planned]
    Boundary --> Services[Application Services<br/>planned]
    Services --> Repositories[Repositories<br/>planned]
    Repositories --> Persistence[Persistence infrastructure<br/>SQLAlchemy models + mappers + sessions]
    Persistence --> SQL[(PostgreSQL<br/>Psycopg 3)]
    Services --> Providers[Providers<br/>planned]
    Providers --> SMS[External SMS Provider]
```

The service, repository, provider, UI, and SMS nodes are planned only. MISSION-004 implements the persistence infrastructure and PostgreSQL target; it does not create repositories or connect to an SMS provider.
