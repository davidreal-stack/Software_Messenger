# UUID en las entidades

Las entidades usan `UUID` y `uuid4` de la biblioteca estándar (`uuid`).

- `UUID` es el tipo que representa un identificador universal de 128 bits.
- `uuid4()` genera un identificador aleatorio para una nueva entidad.
- `field(default_factory=uuid4)` hace que cada instancia obtenga su propio UUID cuando no se entrega uno explícitamente.

Así el dominio puede asignar identidad antes de que exista una base de datos y evita depender de IDs generados por almacenamiento. Las entidades también aceptan un UUID explícito, útil al reconstruir un valor ya identificado.
