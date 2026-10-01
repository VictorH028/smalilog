# Changelog

## 0.2.0-clean

- Unificada la entrada CLI en `smalilog.main`.
- Añadido `python -m smalilog`.
- Corregido el parser del subcomando `hook` y sus acciones.
- Corregida la detección de métodos `abstract`/`native` sin cuerpo instrumentable.
- Corregida la idempotencia de `hook exit` mediante marcador persistente.
- Corregida la configuración del servidor: `--log-file` y `--log-level` ahora se aplican realmente.
- Eliminada la configuración TOML con ruta absoluta específica del entorno.
- Separada la documentación en `docs/`.
- Eliminados caches y módulos experimentales sin referencias.
- Conservado `lms` como subsistema experimental cargado de forma diferida.
- Corregido el `pyproject.toml` para usar únicamente setuptools.
- Añadidos `Makefile`, `.gitignore` y pruebas reproducibles.
- Suite actual: 28 pruebas pasando.
