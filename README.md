Aquí tienes una versión del README.md rediseñada con una estética Cyberpunk / High-Tech Futurista.
Se incorporaron tipografías estilizadas, glifos/íconos cibernéticos, bordes estructurados tipo interfaz terminal de ciencia ficción, badges neón con estilo for-the-badge, cuadros de alerta cyberpunk y diagramas Mermaid con paleta de colores Cyber-Neon (Cyan, Magenta y Matrix Green).
Puedes copiar y pegar el bloque completo directamente en tu archivo README.md:
<div align="center">


██████╗ ███╗   ███╗██████╗ ██╗     ██╗██╗      ██████╗  ██████╗
██╔════╝ ████╗ ████║██╔══██╗██║     ██║██║     ██╔═══██╗██╔════╝
╚█████╗  ██╔████╔██║██████╔╝██║     ██║██║     ██║   ██║██║  ███╗
╚═══██╗ ██║╚██╔╝██║██╔═══╝ ██║     ██║██║     ██║   ██║██║   ██║
██████╔╝ ██║ ╚═╝ ██║██║     ███████╗██║███████╗╚██████╔╝╚██████╔╝
╚═════╝  ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝╚══════╝ ╚═════╝  ╚═════╝

### ⚡ [ SYSTEM STATUS: EXPERIMENTAL LOGGING FRAMEWORK ] ⚡

*Instrumentación Smali de Bajo Nivel · Inyección JNI · Intercepción de Traza ARM64*

---

[![Estado](https://img.shields.io/badge/SYSTEM_STATUS-EXPERIMENTAL-ff0055?style=for-the-badge&logo=android&logoColor=white)](url)
[![Plataforma](https://img.shields.io/badge/TARGET_OS-ANDROID_%2B_TERMUX-00f0ff?style=for-the-badge&logo=android&logoColor=black)](url)
[![Arquitectura](https://img.shields.io/badge/ARCH-ARM64_%2F_AArch64-7000ff?style=for-the-badge&logo=cpu&logoColor=white)](url)
[![Python](https://img.shields.io/badge/ENGINE-PYTHON_3.10%2B-39ff14?style=for-the-badge&logo=python&logoColor=black)](url)
[![Licencia](https://img.shields.io/badge/LICENSE-AUTHORIZED_USE_ONLY-ffe600?style=for-the-badge&logo=shield&logoColor=black)](url)

---

</div>

<br/>


================================================================================
[00] INDEX // TABLA DE CONTENIDOS PROTOCOLIZADA

* [◈ 01. VISIÓN GENERAL](#-01-visión-general--descripción)
* [◈ 02. ARQUITECTURA DE DATOS](#-02-arquitectura-de-datos)
* [◈ 03. ESTRUCTURA DE REPOSITORIO](#-03-estructura-del-proyecto)
* [◈ 04. ESPECIFICACIONES DE API & TIPOS](#-04-especificaciones-de-api)
* [◈ 05. MOTOR JNI & MATRIZ SMALI](#-05-motor-jni--reglas-smali)
* [◈ 06. NÚCLEO DE ESCUCHA (SERVER)](#-06-servidor-de-logs)
* [◈ 07. INYECTOR AUTOMATIZADO](#-07-inyector-smali-injector)
* [◈ 08. COMPILACIÓN NATIVA AArch64](#-08-compilación-de-la-biblioteca-nativa)
* [◈ 09. DESPLIEGUE EN TARGET APK](#-09-integración-en-una-apk)
* [◈ 10. PROTOCOLO DE PRUEBAS](#-10-pruebas)
* [◈ 11. ROADMAP & ESTADO](#-11-estado-del-proyecto)
* [◈ 12. PROTOCOLO DE SEGURIDAD](#-12-consideraciones-de-seguridad)
* [◈ 13. NODO DE CONTRIBUCIÓN](#-13-contribuir)

<br/>


================================================================================
[01] OVERVIEW // VISIÓN GENERAL & DESCRIPCIÓN

`SMALILOG` es un sistema **experimental de telemetría y logging remoto de alto rendimiento** diseñado para entornos Android execution runtime (ART). Permite instrumentar binarios descompilados (`Smali`) para extraer trazas críticas en tiempo real —puntos de entrada/salida de funciones, inspección de argumentos, tipos de datos y mensajes de runtime— transmitiéndolos a través de una librería nativa escrita en **C/JNI** hacia un servidor local HTTP.

Diseñado específicamente para auditorías de seguridad, *reverse engineering*, depuración dinámica y análisis de código sobre entornos restrictivos **Termux + ARM64**.

> ⚠️ **TARGET ABI:** `ARM64 / AArch64`  
> ⚠️ **RUNTIME ENVIRONMENT:** `Android OS + Termux Environment`

<br/>


================================================================================
[02] SYSTEM ARCHITECTURE // ARQUITECTURA DE DATOS

```mermaid
flowchart TD
    classDef buildStyle fill:#0d0f18,stroke:#00f0ff,stroke-width:2px,color:#00f0ff;
    classDef runtimeStyle fill:#160926,stroke:#ff0055,stroke-width:2px,color:#ff0055;
    classDef serverStyle fill:#092615,stroke:#39ff14,stroke-width:2px,color:#39ff14;
    classDef nodeStyle fill:#05050a,stroke:#7000ff,color:#fff;

    subgraph BUILD[" 🏗️ STAGE 1: BUILD & INSTRUMENTATION "]
        S1[📄 Smali Original]:::nodeStyle --> S2[⚡ Injector Engine]:::nodeStyle
        S2 --> S3[📜 Smali Instrumentado]:::nodeStyle
        S3 --> S4[📦 Lib Injector Target]:::nodeStyle
    end

    subgraph RUNTIME[" ⚙️ STAGE 2: ANDROID RUNTIME CORE "]
        R1[🧊 Dex Memory]:::nodeStyle --> R2[🔗 JNI Bridge]:::nodeStyle
        R2 --> R3[⚡ liblogger.so]:::nodeStyle
    end

    subgraph SERVER[" 🖥️ STAGE 3: TELEMETRY RECEIVER "]
        V1[🛰️ Smalilog Server]:::nodeStyle --> V2[💾 Stream Log Output]:::nodeStyle
    end

    S3 -.->|Signed APK| R1
    R3 ==>|HTTP POST /log| V1

    class BUILD buildStyle;
    class RUNTIME runtimeStyle;
    class SERVER serverStyle;

================================================================================
  [03] FILE SYSTEM // ESTRUCTURA DEL PROYECTO
================================================================================

┌──[ROOT]
├── 📁 inyector/       ──> Engine de instrumentación y manipulación AST Smali
├── 📁 server/         ──> Servidor HTTP en Python para captura de eventos
└── 📁 cli/            ──> Consola de comandos para automatización CLI

================================================================================
  [04] DATA MATRIX // ESPECIFICACIONES DE API & TIPOS
================================================================================

El motor de serialización soporta la extracción y casteo dinámico de las siguientes estructuras de datos nativas de Java/Android:
┌─────────────────────────────────────────────────────────┐
│              SUPPORTED TYPES SPECS                      │
├────────────────────┬────────────────────┬───────────────┤
│  [Primitive/Null]  │  [Numeric Objects] │ [Complex Object]│
├────────────────────┼────────────────────┼───────────────┤
│  • null            │  • Integer         │ • Object      │
│  • String          │  • Long            │ • Bundle      │
│  • Boolean         │  • Double          │               │
│  │                 │  • Float           │               │
│  │                 │  • int[]           │               │
└────────────────────┴────────────────────┴───────────────┘

================================================================================
  [05] LOW LEVEL BRIDGING // MOTOR JNI & REGLAS SMALI
================================================================================

🧬 Flujo Execution Link JNI
flowchart LR
    A[📱 Android App] ==>|Dex Execution| B[🔗 JNI Interface]
    B ==>|Native Call| C[⚡ liblogger.so]
    C ==>|HTTP Request| D[🛰️ Smalilog Server]
    D ==>|Flush Log| E[📄 app_logs.txt]

    style A fill:#0c0d14,stroke:#00f0ff,color:#00f0ff
    style B fill:#0c0d14,stroke:#7000ff,color:#7000ff
    style C fill:#0c0d14,stroke:#ff0055,color:#ff0055
    style D fill:#0c0d14,stroke:#ffe600,color:#ffe600
    style E fill:#0c0d14,stroke:#39ff14,color:#39ff14

El servidor espera un payload estandarizado en formato JSON:
{
    "level": "INFO",
    "tag": "MainActivity",
    "message": "onCreate iniciado"
}

> 🛡️ POLÍTICA DE BUFFER Y LÍMITES:
> MAX HEADERS = 16 KiB | MAX BODY SIZE = 1 MiB
> 
🧱 Reglas de Inyección en Registros Smali
> [!IMPORTANT]
> Los registros utilizados deben alinearse estrictamente con los tipos y firmas reales de la función descompilada original.
> 
+-----------------------------------------------------------------------------+
| FORMULA DE CALCULO DE REGISTROS:                                            |
|                                                                             |
|   REGISTROS TOTALES = [REGISTROS ORIGINALES] + [REGISTROS EXTRA PARA HOOKS] |
|                                                                             |
| Ejemplo: .registers 2 ---> .registers 6 (cuando se reservan 4 slots libres) |
+-----------------------------------------------------------------------------+

 * ⚡ Rango Seguro Temp: Si .registers se incrementa de N_old a N_new, el espacio libre utilizable será v[N_old] .. v[N_new - 1].
 * ⚡ Mapeo de Parámetros (p):
   * Métodos de Instancia: p0 es reservado para this. Los argumentos de usuario inician en p1.
   * Métodos Estáticos: Los argumentos inician de forma directa en p0.
 * ⚡ Alias Mappings: Los alias p0, p1, ... conservan su lógica tras recalcular .registers (el ensamblador re-mapea sus offsets).
 * ⚡ Control de Destrucción: Incrementación masiva de registros debe validar la no-sobreescritura de datos vivos.
================================================================================
  [06] SERVER CORE // SERVIDOR DE LOGS
================================================================================

Servidor HTTP de ultra-bajo consumo desarrollado en Python.
🛠️ Configuración Core Network
HOST = "127.0.0.1"
PORT = 9999

> [!WARNING]
> La biblioteca binaria .so inyectada está compilada de forma rígida (hardcoded) para comunicarse exclusivamente con este socket loopback.
> 
🚀 Despliegue de servicio (Termux / Linux)
smalilog serve 

Salida de consola esperada:
[+] SERVER_LISTEN: [http://127.0.0.1:9999](http://127.0.0.1:9999) [READY]

🧪 Emulación de Petición Telemétrica (Test CLI)
curl -X POST [http://127.0.0.1:9999/log](http://127.0.0.1:9999/log) \
     -H 'Content-Type: application/json' \
     -d '{"level":"INFO","tag":"APP","message":"hola"}'

================================================================================
  [07] AUTOMATED INJECTOR // INYECTOR SMALI (injector/)
================================================================================

Herramienta para automatizar la inserción de Hooks sobre archivos .smali sin alteración manual del Bytecode.
💻 Comandos CLI
smalilog hook list       app.smali
smalilog hook show       app.smali -m Sf
smalilog hook analyze    app.smali -m Sf --sig "(I)V"
smalilog hook enter      app.smali -m Sf
smalilog hook exit       app.smali -m Sf
smalilog hook log        app.smali -m Sf --tag APP --message "hola"
smalilog hook lifecycle  Application.smali -m onCreate

🐍 Integración Programática (Python API)
from smalilog.injector.hooker import run_hooker

run_hooker(["app.smali", "-m", "Sf", "enter"])

┌──[ HIGHLIGHTS DE CAPACIDADES DEL INYECTOR ]
├── ⚡ Detección automática de sobrecargas (Resolución por --signature).
├── ⚡ Planificación dinámica de registros libres mediante plan_hook_registers().
├── ⚡ Preservación estricta de tipos de 64-bit Wide (J, D) al mapear p → v.
├── ⚡ Manejo adaptativo de contexto Static vs Instance (p0 context awareness).
├── ⚡ Previene inyecciones duplicadas aplicando marcadores idempotentes.
└── ⚡ Sombreado de sintaxis opcional vía Pygments (con fallback propio integrador).

================================================================================
  [08] NATIVE COMPILATION // COMPILACIÓN NATIVA
================================================================================

Para generar la librería compartida orientada a la arquitectura ARM64 (AArch64):
aarch64-linux-android-clang \
    -shared \
    -fPIC \
    -O2 \
    -fno-exceptions \
    -fno-rtti \
    -o liblogger.so \
    native_logger.c \
    -I/usr/lib/jvm/java-8-openjdk-amd64/include \
    -I/usr/lib/jvm/java-8-openjdk-amd64/include/linux

Artifact resultante: liblogger.so
🔍 Auditoría de Dependencias Dinámicas
readelf -d liblogger.so | grep NEEDED

Verificación de firmas limpia:
0x0000000000000001 (NEEDED) Shared library: [libdl.so]
0x0000000000000001 (NEEDED) Shared library: [libc.so]

> [!CAUTION]
> Si detectas librerías adicionales en la salida de readelf, la toolchain ha introducido enlaces no deseados que podrían romper la portabilidad en el APK.
> 
================================================================================
  [09] TARGET DEPLOYMENT // INTEGRACIÓN EN UNA APK
================================================================================

flowchart LR
    A[1. Inyectar Dex] --> B[2. Copiar liblogger.so]
    B --> C[3. Check Integración]
    C --> D[4. Instrumentar Smali]
    D --> E[5. Recompilar APK]
    E --> F[6. Firmar APK]
    F --> G[7. Install & Exec]
    G --> H[8. Listen Logs]

    style A fill:#0d0f18,stroke:#00f0ff,color:#00f0ff
    style H fill:#092615,stroke:#39ff14,color:#39ff14

La biblioteca nativa compilada debe alojarse obligatoriamente en la ruta ABI correspondiente:
📂 Target APK Base Structure
 └── 📁 lib/
      └── 📁 arm64-v8a/
           └── 📄 liblogger.so

================================================================================
  [10] TESTING & VERIFICATION // PRUEBAS DE CAMPO
================================================================================

Se provee un módulo MainActivity de pruebas para validar:
 * 🟢 Inicialización de componentes RemoteLogger
 * 🟢 Generación de trazado simple de depuración (d)
 * 🟢 Ejecución limpia de hookEnter / hookExit
 * 🟢 Extracción correcta de múltiples tipos Java
 * 🟢 Captura del Ciclo de Vida (Activity Lifecycle)
 * 🟢 Comunicación end-to-end con el Socket del Servidor
Puntos de emisión verificados por defecto:
  [+] Event Hook :: onCreate
  [+] Event Hook :: onResume
  [+] Event Hook :: onPause

================================================================================
  [11] ROADMAP & STATUS // ESTADO DEL PROYECTO
================================================================================

STATUS METRIC: [████████░░] 80% — Experimental / WIP

✅ MÓDULOS IMPLEMENTADOS
 * [x] API Java Nativa (d, hookEnter, hookExit)
 * [x] Motor Logging por Niveles (DEBUG, INFO, WARN, ERROR)
 * [x] Puente JNI de bajo nivel (native_logger.c)
 * [x] Binario dinámico liblogger.so (ARM64)
 * [x] Receiver Server en Python (LogServer)
 * [x] Parsing y validación básica HTTP Body/Headers
 * [x] Engine Automático de Inyección Smali (injector/)
 * [x] Soporte multi-tipo de estructuras Java
🚧 MÓDULOS EN DESARROLLO (WIP)
 * [ ] Interfaz Web Dashboard de monitoreo en tiempo real
 * [ ] Refactor de protocolo a WebSockets / TLS
 * [ ] Instrumentación Smali 100% Zero-Touch (Automatización Total)
 * [ ] Motor de filtros por TAG, expresiones regulares y severidad
 * [ ] Timestamps precisos sincronizados desde el cliente (Device Side)
 * [ ] Cobertura de tests unitarios e integración
 * [ ] Smali API Complete Reference Guide
================================================================================
  [12] SAFETY & SECURITY // CONSIDERACIONES DE SEGURIDAD
================================================================================

> [!WARNING]
> DECLARACIÓN DE USO ÉTICO Y LEGAL:
> Este framework ha sido diseñado únicamente para propósitos de investigación, auditorías de seguridad, depuración dinámica y análisis de software bajo expresa autorización.
> Queda estrictamente prohibido su uso para exfiltración no autorizada de datos, análisis malicioso o interceptación de información en dispositivos sin consentimiento previo.
> ÁMBITO DE RED: El servidor local escucha por defecto en el adaptador 127.0.0.1 (loopback) y no está acondicionado para entornos de producción.
> 
================================================================================
  [13] CONTRIBUTIONS // NODO DE CONTRIBUCIÓN
================================================================================

¿Quieres contribuir al desarrollo de SMALILOG? Las Pull Requests son bien recibidas. Revisa las tareas pendientes en el Roadmap antes de enviar propuestas.
<div align="center">
 ╔═════════════════════════════════════════════════════════════════════════╗
 ║  Coded with ☕ and low-level readelf analysis                           ║
 ║  REMOTE LOGGER FRAMEWORK // EXPERIMENTAL EDITION                        ║
 ╚═════════════════════════════════════════════════════════════════════════╝

</div>


