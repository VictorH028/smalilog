# Changelog

## Sin publicar

- Añadido `smalilog renef`: puente estático que traduce scripts Lua de Renef
  (hooks Java con `args.skip`/`return` constante y observación) a Smali, sin root.
- Nuevo módulo `src/smalilog/renef/` con lector Lua, clasificación de recetas,
  localizador de clases y CLI (`parse`, `apply`, `presets`).
- Nuevo `HookInjector.inject_stub()` para retornos constantes (`V`, primitivos,
  wide y referencias) con marcador persistente `Renef STUB inyectado`.
- Presets incluidos: `ssl` (unpinning Java) y `root` (RootBeer).
- Documentación nueva en `docs/renef.md` y sección en `README.md`.
- Ejemplo ejecutable `build_payloads/renef_demo.lua` y métodos de prueba en
  `MainActivity` para validar stubs boolean/string y observación en dispositivo.
- Runtime opcional en `build_payloads`: `RenefRuntime` conecta al socket del
  agente `libagent.so`, hace el handshake y ejecuta Lua con `hexexec`. Nuevas
  órdenes de broadcast `LUA` (archivo), `LUA_CODE`/`LUA_B64` (base64),
  `LUA_PUSH` (guarda en `files/` y ejecuta) y `LUA_UNHOOK` (cierra el socket,
  restaura hooks y resetea la guarda Lua), con script de ejemplo
  `build_payloads/runtime_hook.lua` y APK `build_payloads/build/renef_runtime.apk`.
- En runtime, los booleanos se modifican con `JNI.boolean(false)`; el agente
  ignora el `return false` directo de Lua. Límite de script: 30 KB. Los logs de
  broadcast ya no vuelcan el base64 completo.
- Reparado el shebang de `apksigner` de `termux-apk-make` en Termux
  (`termux-fix-shebang`), por lo que `termux-apk-make build_payloads` vuelve a
  firmar la APK sin pasos manuales.
- Documentación reorganizada: `docs/README.md` como índice,
  `docs/guia-rapida.md` para nuevos usuarios, `docs/cli.md` como referencia,
  `docs/android/` para clases de la app de prueba y `docs/legacy/` para notas
  históricas.
- Añadida la opción `--logger-class` a `smalilog hook` para APKs que no usan
  `Lcom/deadnote/RemoteLog;`.
- `pytest` limitado a `tests/` para no recolectar los tests del árbol `renef/`.
- Versión `0.3.0` en `pyproject.toml` y `config.VERSION`.
- Suite actual: 57 pruebas pasando.
- Alineada la inyección con la API real del payload (`RemoteLog`: `traceIn`/`traceOut`).
- Corregido el cálculo de temporales y el boxeo de primitivos en `_codegen.py`.
- Implementados `hook both` y los niveles `debug/info/warn/error`; eliminados subcomandos sin implementar.
- Escapado de literales de `const-string` (comillas, saltos de línea, etc.).
- `make native` y `bin/native_lib/Makefile` ya no dependen de `spin` ni del `CC`/`CFLAGS` de Termux.
- Tests actualizados a la API nueva (36 pasando).

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
