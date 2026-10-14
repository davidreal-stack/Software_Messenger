# Datetime y UTC

La referencia de este proyecto está en [`_time.py`](../../app/domain/_time.py), `message_attempt.py` y `job.py`.

- `datetime` representa un instante con fecha y hora.
- `UTC` es la zona horaria universal definida por la biblioteca estándar.
- `datetime.now(UTC)` obtiene la hora actual con zona horaria UTC.
- Un timestamp **timezone-aware** tiene una zona horaria asociada. En Python, `tzinfo` contiene esa información; `None` indica una fecha/hora *naive*.
- `utcoffset()` devuelve la diferencia entre esa hora y UTC. El dominio comprueba que exista y que sea cero para aceptar únicamente instantes UTC.

Usar valores aware evita tratar accidentalmente una hora local sin zona como si fuera UTC. Los timestamps de creación, inicio y finalización del dominio se guardan con esta regla.
