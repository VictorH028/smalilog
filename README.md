<div align="center">

```
██████╗ ███╗   ███╗██████╗ ██╗     ██╗██╗      ██████╗  ██████╗
██╔════╝ ████╗ ████║██╔══██╗██║     ██║██║     ██╔═══██╗██╔════╝
╚█████╗  ██╔████╔██║██████╔╝██║     ██║██║     ██║   ██║██║  ███╗
╚═══██╗ ██║╚██╔╝██║██╔═══╝ ██║     ██║██║     ██║   ██║██║   ██║
██████╔╝ ██║ ╚═╝ ██║██║     ███████╗██║███████╗╚██████╔╝╚██████╔╝
╚═════╝  ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝╚══════╝ ╚═════╝  ╚═════╝
```

### ⚡ [ SYSTEM STATUS: EXPERIMENTAL LOGGING FRAMEWORK ] ⚡

> Herramienta CLI para analizar e instrumentar código **Smali** y recibir logs HTTP durante pruebas de la aplicacion Android. Está pensada para flujos de reverse engineering, depuración en Termux/Linux.

--- 

![Estado](https://img.shields.io/badge/SYSTEM_STATUS-EXPERIMENTAL-ff0055?style=for-the-badge&logo=android&logoColor=white)
![Plataforma](https://img.shields.io/badge/TARGET_OS-ANDROID_%2B_TERMUX-00f0ff?style=for-the-badge&logo=android&logoColor=black)
![Arquitectura](https://img.shields.io/badge/ARCH-ARM64_%2F_AArch64-7000ff?style=for-the-badge&logo=cpu&logoColor=white)
![Python](https://img.shields.io/badge/ENGINE-PYTHON_3.10%2B-39ff14?style=for-the-badge&logo=python&logoColor=black)
![Licencia](https://img.shields.io/badge/LICENSE-AUTHORIZED_USE_ONLY-ffe600?style=for-the-badge&logo=shield&logoColor=black)

---

</div>


<a id="index"></a>
## [00] INDEX // TABLA DE CONTENIDOS

- [◈ 01. Estructura](#estructura)
- [◈ 02. Instalación](#instalacion)
- [◈ 03. Documentación](#documentación)

---

## Estructura

```text
smalilog/
├── src/smalilog/
│   ├── main.py              # CLI principal
│   ├── __main__.py          # python -m smalilog
│   ├── config.py            # configuración común
│   ├── injector/            # parser/orquestador y CLI de hooks
│   ├── manifest/            # análisis y parcheo de AndroidManifest.xml
│   ├── smali/               # modelo, parser, análisis y codegen
│   ├── emit/                # instrucciones Dalvik/Smali
│   ├── server/              # receptor HTTP /log
│   ├── ui/                  # salida de terminal
│   ├── renef/               # puente Lua->Smali, agente y runtime
│   └── lms/                 # consultas/memoria experimental opcional
├── tests/
├── docs/
└── Makefile
```

## Instalación

```bash
python -m pip install -e .
```

## Documentación

- [Guía rápida para nuevos usuarios](docs/guia-rapida.md)
- [Índice completo de documentación](docs/README.md)
- [Referencia de la CLI](docs/cli.md)
- [Puente Renef → Smali](docs/renef.md)
- [Manual del agente embebido](docs/agente.md)

## CLI

```bash
smalilog --help
smalilog server --help
smalilog manifest --help
smalilog hook --help
```

### Servidor

```bash
smalilog server
smalilog server --host 0.0.0.0 --port 9999 --log-file app_logs.txt
```

El endpoint de recepción es `POST /log` con JSON, por ejemplo:

```json
{"level":"INFO","tag":"APP","message":"hola"}
```

### Manifiesto

Antes de instrumentar, prepara el manifiesto y localiza los puntos de entrada:

```bash
smalilog manifest info app_dir/AndroidManifest.xml --smali-dir app_dir
smalilog manifest fix app_dir/AndroidManifest.xml
```

`manifest fix` agrega `INTERNET` y `usesCleartextTraffic` (necesario para HTTP
local en Android 9+). `entrypoints` lista el launcher, actividades, servicios,
receivers y providers.

### Hooks Smali

```bash
smalilog hook list app.smali
smalilog hook show app.smali -m onCreate
smalilog hook analyze app.smali -m onCreate
smalilog hook enter app.smali -m onCreate
smalilog hook exit app.smali -m onCreate
smalilog hook both app.smali -m onCreate
smalilog hook info app.smali -m onCreate --tag APP --message "hola"
smalilog hook lifecycle Application.smali -m onCreate
```

Los niveles de log disponibles son `debug`, `info`, `warn` y `error`
(equivalen a `RemoteLog->d/i/w/e`).

`--help` es la fuente práctica de opciones de cada comando.

### Renef sin root

`smalilog renef` traduce un subconjunto de los scripts Lua de
[Renef](https://renef.io) (hooks Java con `args.skip`/`return` constante y
observación) a instrumentación Smali estática. Los hooks nativos y las APIs de
runtime (`Module`, `Memory`, `Syscall`, `Java.use`) se reportan como no
traducibles porque requieren el agente dinámico de Renef.

```bash
smalilog renef presets
smalilog renef parse --preset ssl
smalilog renef apply --preset ssl --smali-dir ./apk --dry-run
smalilog renef apply --preset root --smali-dir ./apk
```

Detalles, matriz de compatibilidad y flujo con `apkeditor`: [`docs/renef.md`](docs/renef.md).
Hay un ejemplo listo para instalar en `build_payloads/renef_demo.lua`.

### Agente embebido instalable (sin root)

Para ejecutar Lua en una APK ya descompilada, `smalilog renef install` copia
`libagent.so`, añade el puente Smali (`com.smalilog.agent`), parchea el
manifiesto (receptor exportado, `INTERNET`, tráfico HTTP en claro) y
opcionalmente compila y firma:

```bash
apkeditor d -i app.apk -o ./apk
smalilog renef install ./apk --dry-run
smalilog renef install ./apk --build -o app-instrumentada.apk
```

Con la app ya instalada y abierta, arranca el servidor en otra terminal y
contrólala por broadcast **sin root**:

```bash
# Terminal 1
smalilog server --host 127.0.0.1 --port 9999 --log-level DEBUG

# Terminal 2
smalilog renef runtime ping --apk-dir ./apk
smalilog renef runtime status --apk-dir ./apk
smalilog renef runtime exec --code 'print("hola")' --apk-dir ./apk
smalilog renef runtime push hook.lua --apk-dir ./apk
smalilog renef runtime unhook --apk-dir ./apk
```

Los resultados no vuelven por la terminal: llegan a `app_logs.txt`. El agente
admite scripts de hasta 256 KB. Solo incluye `arm64-v8a`; el receptor exportado
no tiene permiso propio, así que úsalo solo en apps propias o de laboratorio.
Si la APK original tiene otra firma, desinstálala antes o firma con tu propia
clave. El flujo completo está en [`docs/agente.md`](docs/agente.md).

`build_payloads` también incluye `libagent.so`, así que la app de prueba puede
ejecutar Lua en runtime. Con la app en ejecución se envía un script por
broadcast (`LUA`, `LUA_CODE`/`LUA_B64` o `LUA_PUSH`) y se limpian con
`LUA_UNHOOK`; ver [`docs/renef.md` §7c](docs/renef.md). APK de trabajo:
`build_payloads/build/renef_runtime.apk` (copia instalable en
`/storage/emulated/0/Download/renef_runtime.apk`). Para ver `[RenefDemo]` inicia
el servidor con `--log-level DEBUG`.

## LMS experimental

El subcomando `smalilog lms` se carga de forma diferida y no participa en el arranque de `server` ni `hook`. Sus funciones dependen del entorno MCP configurado.

## Desarrollo

```bash
make install   # requerido antes de los tests (instala el paquete en editable)
make compile
make test
make check
make native    # compila liblogger.so en build_payloads/lib/arm64-v8a/
```

El proyecto evita incluir caches, bases de datos, logs y artefactos generados en el repositorio.
