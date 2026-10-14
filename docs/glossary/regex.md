# Regex para el teléfono de Contact

En [`contact.py`](../../app/domain/contact.py) se usan dos expresiones regulares pequeñas para limpiar separadores y comprobar la sintaxis mínima definida en DECISION-003.

## Quitar formato visual

```python
_PHONE_FORMATTING = re.compile(r"[\s().-]")
normalized_phone = _PHONE_FORMATTING.sub("", self.phone)
```

- `re.compile(...)` prepara un patrón que se puede reutilizar.
- `r"..."` es una *raw string*: las barras invertidas llegan al patrón sin que Python las interprete primero como escapes de cadena.
- `[ ... ]` define una clase de caracteres; el patrón coincide con cualquiera de los caracteres indicados.
- `\s` significa un espacio en blanco, incluidos espacios y tabulaciones. Los demás caracteres de la clase son paréntesis, punto y guion; el guion al final se interpreta literalmente.
- `.sub("", texto)` reemplaza cada coincidencia por una cadena vacía. Aquí elimina únicamente esos separadores.

## Comprobar los dígitos

```python
_PHONE_DIGITS = re.compile(r"\+?[1-9][0-9]{6,14}\Z")
_PHONE_DIGITS.fullmatch(normalized_phone)
```

- `\+` representa un signo `+` literal, y `?` hace que sea opcional.
- `[1-9]` exige que el primer dígito sea del 1 al 9.
- `[0-9]{6,14}` exige entre 6 y 14 dígitos adicionales, para un total de 7 a 15.
- `\Z` marca el final del texto.
- `fullmatch(...)` requiere que el patrón coincida con toda la cadena, no solo con una parte.

La validación es sintáctica: no confirma país, asignación ni alcance del número.
