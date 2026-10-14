# Project Structure Map

Living map of the repository, updated through MISSION-004. The initial persistence implementation is present; its live PostgreSQL CRUD integration test still needs a configured test database.

```text
Software_Messenger/
├── .codex/
│   └── AGENTS.md
├── .vscode/
│   └── settings.json
├── app/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── _time.py
│   │   ├── contact.py
│   │   ├── job.py
│   │   ├── message.py
│   │   └── message_attempt.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   └── persistence/
│   │       ├── __init__.py
│   │       ├── database.py
│   │       ├── mappers.py
│   │       └── models.py
│   └── schemas/
│       ├── __init__.py
│       └── contracts.py
├── requirements.txt
├── docs/
│   ├── ai-workflow/
│   │   ├── ARCHITECTURE.md
│   │   ├── BUSINESS_RULES.md
│   │   ├── CHANGELOG.md
│   │   ├── CURRENT_STATE.md
│   │   ├── DECISIONS.md
│   │   ├── GLOSSARY.md
│   │   ├── IMPORT_GLOSSARY.md
│   │   ├── MISSIONS.md
│   │   ├── OPERATIONAL_RULES.md
│   │   ├── PROJECT_CONTEXT.md
│   │   └── ROADMAP.md
│   ├── architecture/
│   │   ├── database.md
│   │   ├── domain.md
│   │   └── system.md
│   ├── diagrams/
│   │   ├── architecture.md
│   │   ├── data_model.md
│   │   └── project_structure.md
│   └── glossary/
│       ├── dataclasses.md
│       ├── datetime.md
│       ├── python.md
│       ├── pydantic.md
│       ├── regex.md
│       ├── sqlalchemy.md
│       └── uuid.md
└── tests/
    ├── __init__.py
    ├── domain/
    │   ├── __init__.py
    │   └── test_entities.py
    ├── infrastructure/
    │   ├── __init__.py
    │   └── persistence/
    │       ├── __init__.py
    │       ├── test_database.py
    │       ├── test_mappers.py
    │       └── test_models.py
    └── schemas/
        ├── __init__.py
        └── test_contracts.py
```

The domain remains independent of SQLAlchemy. The tree contains no repositories, services, providers, API, frontend, SMS delivery, queues, or job processing. Git/GitHub remains paused and no remote operations were performed.
