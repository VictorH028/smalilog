# AGENTS.md

CLI para instrumentar apps Android vía inyección Smali + JNI y recibir logs HTTP. Python ≥3.10, src layout (`src/smalilog/`), setuptools con `where = ["src"]`. Se desarrolla en Termux/Android; sin CI, sin lint ni typecheck, sin pre-commit.

## Comandos

- `make install` → `pip install -e .`. **Requerido antes de pytest**: los tests importan `smalilog.*` y no hay `pythonpath` configurado para pytest.
- `make check` = `compileall src` + `pytest -q` (en ese orden). `make test` solo pytest; `make native` compila `liblogger.so` y lo instala en `build_payloads/lib/arm64-v8a/`.
- Termux exporta `CC=clang` y `CFLAGS` en el entorno: el Makefile nativo los ignora a propósito y fija `aarch64-linux-android-clang` + `-fPIC -shared`.
- Existen `tests/injector_test.py` (HookInjector), `tests/renef_test.py` (puente Renef→Smali), `tests/manifest_test.py` (manifiesto/entrypoints) y `tests/agent_test.py` (instalador/control del agente embebido). Prueba concreta: `pytest tests/injector_test.py -k <nombre>`.
- Ruff está configurado en `pyproject.toml` (docstrings Google, comillas dobles) pero no se ejecuta en ningún target — formatear a mano siguiendo ese estilo.
- `python -m smalilog` y el entry point `smalilog.main:cli` son equivalentes.
- `apkeditor` para compilar y desecompilar apk.
- `smalilog renef install ./apk --build -o app.apk` instala el agente embebido y firma; sin `--build` solo parchea el árbol descompilado.
- `smalilog renef runtime {ping,status,exec,push,unhook} --apk-dir ./apk` controla la app por `am broadcast` (o `--adb`) sin root. Usa `-f 0x20` para incluir paquetes detenidos; los resultados solo llegan al servidor, no a la terminal.
- `termux-apk-make build_payloads` compila y firma; si `apksigner` falla con `/bin/bash: bad interpreter`, ejecutar `termux-fix-shebang "$PREFIX/lib/termux-apk-make/toolz/apksigner"` y reintentar (el paquete puede sobrescribirlo al actualizarse).

## Arquitectura y trampas

- `smalilog/main.py::cli()` usa argparse, devuelve código de salida (int) y nunca lanza `SystemExit`.
- **`hook` no pasa por el parser de `main`**: `cli()` delega los args tras `hook` a `smalilog.injector._cli.run_hooker`, que tiene su propio parser (`--help` por subcomando es la fuente de verdad). `manifest` y `renef` funcionan igual, con parser propio en `smalilog/manifest/_cli.py` y `smalilog/renef/_cli.py`.
- **`lms` es experimental (Typer) y de carga perezosa**, no participa en `server`/`hook`. Su lista de subcomandos está escrita a mano en el menú de ayuda de `main.py` (~línea 310): añadir un subcomando exige tocar también `main.py`, no solo `lms/commands.py`.
- `renef install`/`runtime` viven en `renef/_agent.py` + `renef/_agent_cli.py`. El payload versionado está en `renef/payload/` (Smali del puente y `lib/arm64-v8a/libagent.so`, 9.2 MB): el `.so` solo es arm64 y el receptor queda `exported="true"` sin permiso propio. `install` exige un árbol con `smali/` (salida de `apkeditor d`); `--build` usa `apkeditor b` + `apksigner`, no `termux-apk-make`.
- El Java del puente está en `renef/payload/java/com/smalilog/agent/`; el Smali de `renef/payload/smali/` se genera con `javac`+`d8` y se decodifica con `apkeditor d`. Si cambias el Java, regenera ambos assets y vuelve a ejecutar `tests/agent_test.py`.
- El puente nuevo (`com.smalilog.agent`) usa la action `com.smalilog.agent.ACTION` y límite de 256 KB; su `libagent.so` se recompiló con `main_cmd` de 2 MB (el original truncaba a 64 KB). El puente antiguo de `build_payloads` (`com.deadnote`, `LUA_*`, 30 KB) sigue existiendo por compatibilidad. No confundir ambos en docs/tests.
- `smalilog manifest` trabaja sobre `AndroidManifest.xml` en texto (no AXML binario): `parse_manifest` extrae permisos/componentes y `patch_manifest` inserta `INTERNET` y `usesCleartextTraffic` por texto para no reformatear el XML; `scan_smali_entries` busca clases que heredan de Application/Activity/Service/Receiver/Provider. `fix` es idempotente y crea `.bak` salvo `--no-backup`/`--output`.
- Pipeline de hooks: `injector/_injector.py` (HookInjector) → `smali/_register_planner.py` (asigna registros temp) → `smali/_codegen.py` → `emit/`. La clase/logger de destino se pasa como descriptor (`Lcom/deadnote/RemoteLog;` por defecto) al construir `HookInjector`; el codegen usa `traceIn`/`traceOut`/`traceOutVoid` y los tests fijan los temps (2 sin args, 3 con referencia, 4 con primitivo) — al tocar codegen, ejecutar el suite.
- Métodos `abstract`/`native` no tienen cuerpo y no se instrumentan (skip, no error). La idempotencia de `hook exit` depende de marcadores persistentes en el archivo inyectado: no inventar un marcador distinto.
- Servidor: `server/logserver.py` con HTTPServer stdlib; por defecto `127.0.0.1:9999`, `POST /log` con JSON `{level, tag, message}` → `app_logs.txt`. Defaults/limites en `smalilog/config.py`. El agente embebido envía sus logs por HTTP a ese endpoint (`--host`/`--port` en runtime).
- Config para `lms`: pydantic-settings, `config.toml` en cwd + env `SMALILOG_*`; DB sqlite en `user_data_dir("smalilog")/memory.sqlite3`.
- En Termux no se puede instalar ni ejecutar la APK y no hay privilegios elevados; usa `$PREFIX/tmp` para archivos temporales.
## Payload Android (no es parte del paquete Python)

- **Entorno: solo Termux, sin privilegios.** No hay emulador, ni root/su, ni permisos elevados: la APK **no se puede instalar ni ejecutar** desde aquí. La validación de los hooks es estática (unit tests con smali sintético en `tests/` + el propio CLI); el flujo en un dispositivo real ocurre fuera de este repositorio.
- `build_payloads/` es la app de prueba Java `com.deadnote` usada para validar los hooks de punta a punta; incluye sources, resources y `lib/arm64-v8a/liblogger.so`. Su `build/` está ignorado (no versionado). Trátala como material de lectura/referencia: puedes generar smali e inyectar en sus archivos, no correrarla.
- `bin/native_lib/native_logger.c` es la librería JNI que envía logs async a `127.0.0.1:9999`; se compila con `aarch64-linux-android-clang` (`make native`, receta en `bin/README.md`). El nombre del símbolo JNI debe coincidir exactamente con `com.deadnote.RemoteLog.nativeSendLog`.
- Runtime Renef: `libagent.so` abre `@renef_pl_<pid>`; `RenefRuntime` mantiene el socket y ejecuta `hexexec`. Al cerrar el socket el agente restaura hooks nativos y Java; `LUA_UNHOOK` lo usa y resetea `_G.__smalilog_runtime_hook`. Conexión: handshake con pausa de 200 ms; el puente antiguo usa timeout 8 s y 30 KB, el nuevo (`com.smalilog.agent`) usa 15 s y 256 KB. En runtime los booleanos necesitan `JNI.boolean(...)`; `return false` directo se ignora.

## Convenciones

- Todo el texto (comentarios, salida CLI, docs, commits, tests) está en **español**.
- La versión está duplicada: `pyproject.toml` y `config.VERSION` — actualizar ambas.
- `docs/README.md` es el índice: `docs/guia-rapida.md` para usuarios nuevos, `docs/agente.md` para el flujo completo del agente embebido, `docs/cli.md` para referencia y `docs/legacy/` para material histórico. `docs/injector.md` y `docs/renef.md` son referencia técnica: verificar contra el código y `--help`; el `README.md` no es fuente exacta.
