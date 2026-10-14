# Python en el backend

Referencia breve de construcciones presentes en `app/domain/`. No es un manual general de Python.

## Anotaciones de tipo

En [contact.py](../../app/domain/contact.py), `name: str` indica que se espera una cadena. En `message_attempt.py`, `provider_reference: str | None` significa que el valor puede ser una cadena o `None`; `|` expresa una unión de tipos.

`-> None` en métodos como `__post_init__` indica que no se espera un valor de retorno. Las anotaciones ayudan a leer y revisar el código, pero no validan por sí solas los valores en tiempo de ejecución.

## Decoradores

Un decorador como `@dataclass(...)` se coloca sobre una clase y ajusta su comportamiento al definirla. La entrada específica de dataclasses está en [dataclasses.md](dataclasses.md).

## Métodos especiales y tipos de retorno adelantados

`__post_init__` es un método especial de dataclass llamado después del inicializador generado. Aquí se usa para validar los datos al crear una entidad.

Anotaciones como `-> "MessageAttempt"` ponen el nombre de la propia clase entre comillas porque el método aparece dentro de su definición y devuelve otra instancia de ese tipo. Las comillas permiten referir al tipo antes de que la definición haya terminado.

## Imports relativos

`from ._time import now_utc` busca `_time.py` dentro del paquete actual (`app.domain`). Se usa para compartir la creación y validación de timestamps UTC entre las entidades, sin añadir una dependencia.

## Enum de estados

`class JobStatus(StrEnum)` define un conjunto cerrado de nombres (`PENDING`, `RUNNING`, etc.) cuyos valores también son cadenas. En el dominio, esto hace explícitos los estados permitidos y facilita compararlos y mostrarlos como texto.
