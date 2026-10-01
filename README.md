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

---

## Estructura

```text
smalilog/
├── src/smalilog/
│   ├── main.py              # CLI principal
│   ├── __main__.py          # python -m smalilog
│   ├── config.py            # configuración común
│   ├── injector/            # parser/orquestador y CLI de hooks
│   ├── smali/               # modelo, parser, análisis y codegen
│   ├── emit/                # instrucciones Dalvik/Smali
│   ├── server/              # receptor HTTP /log
│   ├── ui/                  # salida de terminal
│   └── lms/                 # consultas/memoria experimental opcional
├── tests/
├── docs/
└── Makefile
```

## Instalación

```bash
python -m pip install -e .
```

## CLI

```bash
smalilog --help
smalilog server --help
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

### Hooks Smali

```bash
smalilog hook list app.smali
smalilog hook show app.smali -m onCreate
smalilog hook analyze app.smali -m onCreate
smalilog hook enter app.smali -m onCreate
smalilog hook exit app.smali -m onCreate
smalilog hook both app.smali -m onCreate
smalilog hook log app.smali -m onCreate --tag APP --message "hola"
smalilog hook lifecycle Application.smali -m onCreate
```

`--help` es la fuente práctica de opciones de cada comando.

## LMS experimental

El subcomando `smalilog lms` se carga de forma diferida y no participa en el arranque de `server` ni `hook`. Sus funciones dependen del entorno MCP configurado.

## Desarrollo

```bash
make compile
make test
make check
```

El proyecto evita incluir caches, bases de datos, logs y artefactos generados en el repositorio.
