# Pydantic en los contratos

En [contracts.py](../../app/schemas/contracts.py), Pydantic valida los datos que entran a contratos de frontera y los convierte a tipos Python declarados. Estos contratos describen datos; no son entidades de dominio ni ejecutan operaciones.

## `BaseModel`

```python
class ContactContract(_ContractBase):
    id: UUID
    name: str
    phone: str
```

`BaseModel` es la clase base de Pydantic. Al construir o validar una instancia, comprueba que los campos requeridos tengan tipos compatibles; también facilita convertir UUID, datetime y enums desde valores de entrada.

## `ConfigDict` y `model_config`

```python
class _ContractBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
```

`ConfigDict` expresa opciones de configuración. `model_config` aplica esas opciones al modelo y a sus derivados. Aquí `extra="forbid"` hace que un campo no declarado sea un error, evitando ignorar silenciosamente una diferencia de contrato.

## `model_validate(...)`

```python
attempt = MessageAttemptContract.model_validate(input_data)
```

Valida un objeto Python —en este proyecto, un diccionario con datos de frontera— y devuelve la instancia tipada. Puede interpretar UUID y fechas serializadas y rechaza campos ausentes, tipos incompatibles, enums desconocidos y campos extra.

## `model_dump(mode="json")`

```python
payload = attempt.model_dump(mode="json")
```

Devuelve los campos como un diccionario compatible con JSON: por ejemplo, UUID y datetime pasan a cadenas y los estados enum a sus valores. El método no envía HTTP ni guarda datos.

## `ValidationError`

Las pruebas capturan `pydantic.ValidationError` cuando un dato no satisface el contrato. La aplicación podrá decidir cómo manejarla en una misión de servicios o API posterior; este paquete no la transforma en respuesta HTTP.
