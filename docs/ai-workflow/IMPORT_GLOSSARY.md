# Backend Learning Glossary

Índice incremental de construcciones que ya aparecen en el backend. Explica el código real en español; no anticipa tecnologías todavía ausentes.

```text
Python
├── Python general → docs/glossary/python.md
├── dataclasses → docs/glossary/dataclasses.md
├── datetime / UTC → docs/glossary/datetime.md
├── Pydantic → docs/glossary/pydantic.md
├── regex → docs/glossary/regex.md
├── SQLAlchemy → docs/glossary/sqlalchemy.md
└── UUID → docs/glossary/uuid.md
```

Los imports estándar se explican donde ayudan a entender una construcción. Las dependencias externas arquitectónicamente relevantes son:

| Paquete | Import | Propósito | Uso | Por qué existe | Misión |
| --- | --- | --- | --- | --- | --- |
| `pydantic>=2.12,<3` | `pydantic.BaseModel`, `pydantic.ConfigDict` | Validación y serialización de contratos | `app/schemas/contracts.py` | Tecnología aprobada para datos en límites de aplicación; no reemplaza las entidades de dominio | MISSION-003 |
| `SQLAlchemy>=2.0,<3` | `DeclarativeBase`, `Mapped`, `mapped_column`, `relationship`, `Enum`, `create_engine`, `sessionmaker` | ORM, estructura de tablas, relaciones, conexión y sesiones | `app/infrastructure/persistence/` | Implementa persistencia PostgreSQL fuera del dominio con modelos y mappers separados | MISSION-004 |
| `psycopg[binary]>=3.2,<4` | Driver `psycopg` | Conexión DB-API de SQLAlchemy con PostgreSQL mediante Psycopg 3 | Configurada por `postgresql+psycopg` en `app/infrastructure/persistence/database.py` | Usa el driver PostgreSQL seleccionado para desarrollo, pruebas y producción | MISSION-004 |
