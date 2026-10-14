# SQLAlchemy en persistencia

La implementación está en [`app/infrastructure/persistence/`](../../app/infrastructure/persistence/). SQLAlchemy conecta esos modelos con PostgreSQL, pero las entidades del dominio siguen siendo dataclasses separadas.

## Modelo declarativo y columnas

```python
class ContactModel(Base):
    __tablename__ = "contacts"
    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
```

- `DeclarativeBase` aporta metadata compartida donde SQLAlchemy registra las tablas.
- `Mapped[T]` declara el tipo Python que la clase ORM expone.
- `mapped_column(...)` configura el tipo y las restricciones estructurales de una columna.
- `Uuid(as_uuid=True)` entrega UUID como objetos `uuid.UUID` en Python; PostgreSQL usa su tipo UUID.

## Relaciones y claves foráneas

`ForeignKey("messages.id")` y `ForeignKey("contacts.id")` hacen que cada intento refiera a un mensaje y un contacto existentes. `relationship(..., back_populates=...)` conecta los objetos ORM en ambos sentidos; no cambia las entidades de dominio ni ejecuta casos de uso.

## Estados como cadenas controladas

`Enum(..., native_enum=False, create_constraint=True, values_callable=...)` guarda los valores de las enumeraciones del dominio como texto de estado y crea una restricción `CHECK` con los valores permitidos. No crea tipos nativos de enumeración PostgreSQL.

## Engine y sesiones

- `create_engine(...)` configura la conexión usando una URL `postgresql+psycopg`; la contraseña se mantiene en la variable de entorno y no en el código.
- `sessionmaker(...)` crea sesiones ligadas a ese engine. Una sesión agrupa operaciones de persistencia y se usa como context manager para cerrar sus recursos.
- `Base.metadata.create_all(...)` crea las tablas ausentes cuando el código llama explícitamente a `create_schema(...)`. No se ejecuta al importar y no sustituye migraciones de producción.

El mapeo hacia/desde dataclasses vive en `mappers.py`, separado de las consultas y de la administración de sesiones.
