# Dataclasses

Las entidades [Contact](../../app/domain/contact.py), [Message](../../app/domain/message.py), [MessageAttempt](../../app/domain/message_attempt.py) y [Job](../../app/domain/job.py) usan dataclasses para representar valores del dominio con poco código repetitivo.

## Declaración de una entidad

```python
@dataclass(frozen=True, slots=True)
class Contact:
```

- `@dataclass` genera métodos habituales, como el inicializador, a partir de los atributos declarados.
- `frozen=True` impide reasignar normalmente un atributo después de crear la instancia. Por eso las transiciones de `MessageAttempt` y `Job` devuelven otra instancia.
- `slots=True` fija los atributos declarados y evita un `__dict__` convencional por instancia.

## Atributos generados

```python
id: UUID = field(default_factory=uuid4)
```

- `field(...)` configura un atributo de dataclass.
- `default_factory=uuid4` llama a `uuid4()` para cada instancia; no comparte un ID creado una sola vez.
- En `_time.py`, `field(default_factory=now_utc)` aplica el mismo patrón para obtener un timestamp nuevo al construir una entidad.

## Validación después de construir

```python
def __post_init__(self) -> None:
```

Dataclass llama a `__post_init__` después del `__init__` que generó. Las entidades lo usan para verificar invariantes. `Contact` normaliza el teléfono dentro de este método con `object.__setattr__`, que permite establecer ese valor inicial aun cuando la dataclass sea `frozen`.

## Transiciones inmutables

```python
replace(self, status=MessageAttemptStatus.SENT, completed_at=completed_at)
```

`dataclasses.replace(...)` crea una instancia nueva usando los valores actuales y sustituye los campos indicados. Aquí permite cambiar el estado sin mutar la entidad original; la instancia nueva vuelve a pasar por sus validaciones.
