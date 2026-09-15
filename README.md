README.md — Remote Logger

<div align="center">

./.img/pre.png

Remote Logger

Sistema experimental de logging remoto para Android basado en JNI + Smali

https://img.shields.io/badge/estado-experimental-yellow?style=flat-square
https://img.shields.io/badge/plataforma-Android%20%2B%20Termux-green?style=flat-square
https://img.shields.io/badge/arquitectura-ARM64%20%2F%20AArch64-blue?style=flat-square
https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square
https://img.shields.io/badge/licencia-uso%20autorizado-lightgrey?style=flat-square

</div>

---

📖 Tabla de contenidos

· Descripción
· Arquitectura
· Estructura del proyecto
· API
  · Java
  · Tipos soportados
  · Smali
· Servidor de logs
· Inyector Smali (injector/)
· Compilación nativa
· Integración en una APK
· Pruebas
· Estado del proyecto
· Consideraciones
· Contribuir
· Documentación relacionada

---

📌 Descripción

Remote Logger es un sistema experimental de logging remoto para Android. Permite instrumentar aplicaciones (Java o Smali) para enviar trazas de ejecución —entradas de funciones, argumentos, valores de retorno y mensajes arbitrarios— hacia un servidor local mediante una biblioteca nativa JNI que se comunica por HTTP.

El proyecto está diseñado para ser usado en investigación, depuración y análisis de aplicaciones propias o autorizadas, con un enfoque práctico sobre Termux + ARM64.

⚠️ Estado: Experimental / WIP · Plataforma principal: Android + Termux · ABI objetivo: ARM64 / AArch64

---

🧭 Arquitectura

```text
        Smali (instrumentado)
                │
                ▼
        Java / RemoteLogger
                │
                ▼
              JNI
                │
                ▼
          liblogger.so
                │
                │  HTTP POST /log
                ▼
          log_server.py
                │
                ▼
          app_logs.txt
```

Flujo de una llamada típica:

```text
Android App
     │  RemoteLogger.hookEnter(...)
     ▼
   JNI Bridge
     │
     ▼
 liblogger.so
     │  POST /log (JSON)
     ▼
 log_server.py ──► app_logs.txt
```

---

📁 Estructura del proyecto

```text
.
├── README.md
├── MainActivity.java
├── RemoteLogger.java
├── native_logger.c
├── liblogger.so
├── log_server.py
├── dex-inj/
└── injector/
    ├── __init__.py
    ├── hooker.py              # Fachada pública + run_hooker (CLI entry)
    ├── _colors.py             # Colores ANSI y helpers log_*
    ├── _highlight.py          # Resaltado Smali (pygments + fallback)
    ├── _smali_types.py        # Tipos, parse_type_list, _type_size
    ├── _smali_model.py        # SmaliMethod, normalize_reg
    ├── _smali_parser.py       # parse_smali_file, parse_class_name
    ├── _register_planner.py   # plan_hook_registers
    ├── _emit.py               # Helpers de emisión Dalvik
    ├── _codegen.py            # Generadores hookEnter / hookExit / d
    ├── _injector.py           # HookInjector
    ├── _analyze.py            # analyze_method
    └── _cli.py                # build_hook_parser, run_hooker
```

Componentes principales

Archivo Función
RemoteLogger.java API Java expuesta a la aplicación
native_logger.c Capa JNI y comunicación nativa HTTP
liblogger.so Biblioteca nativa compilada (AArch64)
log_server.py Servidor HTTP que recibe y persiste los logs
MainActivity.java Ejemplo de integración y pruebas de tipos
dex-inj/ Recursos y utilidades para la instrumentación Smali
injector/ Inyector automático de hooks en archivos Smali

---

🔌 API

El componente Java expone tres operaciones principales:

```java
RemoteLogger.d(tag, message);
RemoteLogger.hookEnter(function, argumentName, value);
RemoteLogger.hookExit(function, result);
```

d(tag, message)

Logging simple para eventos independientes:

```java
RemoteLogger.d("MainActivity", "onCreate iniciado");
```

hookEnter(function, argumentName, value)

Registra la entrada a una función junto con uno de sus argumentos:

```java
RemoteLogger.hookEnter("miFuncion", "a", a);
```

hookExit(function, result)

Registra el valor de retorno al salir de una función:

```java
RemoteLogger.hookExit("miFuncion", resultado);
```

---

☕ Ejemplo Java

```java
public int miFuncion(String a) {

    RemoteLogger.hookEnter("miFuncion", "a", a);

    int resultado = /* ... */;

    RemoteLogger.hookExit("miFuncion", resultado);

    return resultado;
}
```

El MainActivity incluido contiene ejemplos con null, String, Boolean, Integer, Long, Double, Float, arrays, Object y Bundle.

---

🧩 Tipos soportados en las pruebas

```text
null      String     Boolean    Integer
Long      Double     Float      int[]
Object    Bundle
```

Ejemplos:

```java
RemoteLogger.hookEnter("testFunction", "argString",  "test value");
RemoteLogger.hookEnter("testFunction", "argBoolean", true);
RemoteLogger.hookEnter("testFunction", "argInteger", 42);
RemoteLogger.hookEnter("testFunction", "argLong",    123456789L);
RemoteLogger.hookEnter("testFunction", "argDouble",  3.14159);
RemoteLogger.hookEnter("testFunction", "argFloat",   2.5f);
RemoteLogger.hookEnter("testFunction", "argArray",   new int[]{1, 2, 3});
```

También se prueban retornos mediante hookExit(...).

---

🧬 Flujo JNI

```text
Android App
     │
     │ RemoteLogger.*
     ▼
    JNI
     │
     ▼
liblogger.so
     │
     │ HTTP POST /log
     ▼
log_server.py
     │
     ▼
app_logs.txt
```

El servidor espera un JSON como:

```json
{
    "level": "INFO",
    "tag": "MainActivity",
    "message": "onCreate iniciado"
}
```

Y aplica límites tanto a cabeceras (MAX_HEADERS = 16 KiB) como al cuerpo (MAX_BODY = 1 MiB).

---

🧱 Integración mediante Smali

Una vez disponible RemoteLogger, las llamadas pueden incorporarse directamente al Smali:

```smali
invoke-static {v0, v1, v2},
    Lcom/deadnote/RemoteLogger;->hookEnter(
        Ljava/lang/String;
        Ljava/lang/String;
        Ljava/lang/Object;
    )V
```

Nota: los registros utilizados deben coincidir con los tipos y valores reales de la función original.

📐 Reglas de registros Smali

· Rango seguro de temporales: si .registers sube de N_old a N_new, los temporales frescos son v[N_old] .. v[N_new - 1].
· Parámetros p:
  · En métodos de instancia: p0 es this; los argumentos reales comienzan en p1.
  · En métodos estáticos: los argumentos reales comienzan en p0.
· Alias p0, p1, … siguen funcionando tras aumentar .registers; el ensamblador recalcula sus posiciones.
· No basta con aumentar .registers: hay que verificar que las nuevas instrucciones no sobrescriban registros aún vivos.

Regla práctica:

```text
registros nuevos = registros originales + registros usados por los hooks
```

Ejemplo: .registers 2 puede convertirse en .registers 6 si se necesitan 4 registros adicionales.

---

🖥️ Servidor

Servidor HTTP minimalista en Python, implementado en log_server.py como la clase LogServer.

Configuración por defecto

```python
HOST = "127.0.0.1"
PORT = 9999
```

Parámetro Valor
Endpoint POST /log
Almacenamiento app_logs.txt
Niveles aceptados DEBUG, INFO, WARNING, ERROR
MAX_HEADERS 16 KiB
MAX_BODY 1 MiB

Ejecución

Desde Termux:

```bash
python3 log_server.py
```

Salida esperada:

```text
Servidor de logs en http://127.0.0.1:9999
```

Ejemplo de petición

```bash
curl -X POST http://127.0.0.1:9999/log \
     -H 'Content-Type: application/json' \
     -d '{"level":"INFO","tag":"APP","message":"hola"}'
```

---

🧪 Inyector Smali (injector/)

El subpaquete injector/ implementa un inyector automático de hooks sobre archivos Smali, con API programática y CLI tipo git subcommands.

Uso por CLI

```bash
smalilog hook list       app.smali
smalilog hook show       app.smali -m Sf
smalilog hook analyze    app.smali -m Sf --sig "(I)V"
smalilog hook enter      app.smali -m Sf
smalilog hook exit       app.smali -m Sf
smalilog hook log        app.smali -m Sf --tag APP --message "hola"
smalilog hook lifecycle  Application.smali -m onCreate
```

Uso programático

```python
from smalilog.injector.hooker import run_hooker

run_hooker(["app.smali", "-m", "Sf", "enter"])
```

Comportamiento

· Detecta sobrecargas y permite desambiguar con --signature.
· Planifica registros frescos con plan_hook_registers().
· Preserva los tipos wide (J, D) al mapear p → v.
· Respeta métodos static vs instance al resolver p0.
· Evita dobles inyecciones mediante marcadores (Hook ENTER inyectado, etc.).
· Resaltado opcional con Pygments (fallback propio si no está instalado).

📘 Documentación detallada del inyector en injector/README.md.

---

🔨 Compilación de la biblioteca nativa

Para AArch64:

```bash
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
```

Resultado esperado:

```text
liblogger.so
```

Comprobación de dependencias

```bash
readelf -d liblogger.so | grep NEEDED
```

Salida esperada:

```text
0x0000000000000001 (NEEDED) Shared library: [libdl.so]
0x0000000000000001 (NEEDED) Shared library: [libc.so]
```

Si aparecen dependencias adicionales, la compilación introdujo enlaces no deseados.

---

📦 Integración en una APK

```text
1. Preparar RemoteLogger
        │
        ▼
2. Preparar liblogger.so
        │
        ▼
3. Integrar archivos en la APK
        │
        ▼
4. Instrumentar Smali (manual o vía injector/)
        │
        ▼
5. Recompilar
        │
        ▼
6. Firmar APK
        │
        ▼
7. Instalar y probar
        │
        ▼
8. Ejecutar log_server.py
```

La biblioteca nativa debe ubicarse en la ruta ABI correspondiente:

```text
lib/arm64-v8a/liblogger.so
```

---

🧪 Pruebas

MainActivity funciona como aplicación de pruebas para verificar:

· Inicialización de RemoteLogger
· Logs simples (d)
· hookEnter / hookExit
· Diferentes tipos Java
· Ciclo de vida de una Activity
· Comunicación extremo a extremo con el servidor

Actualmente se emiten eventos durante:

```text
onCreate
onResume
onPause
```

---

📌 Estado del proyecto

```text
[████████░░] 80% — Experimental / WIP
```

✅ Implementado

· API Java (d, hookEnter, hookExit)
· Logging por niveles
· Puente JNI (native_logger.c)
· Biblioteca liblogger.so
· Servidor Python (LogServer)
· Recepción HTTP con validación básica
· Inyector Smali (injector/)
· Pruebas con múltiples tipos Java

🚧 En desarrollo

· Visualización web de logs
· Mejoras de protocolo y manejo de errores
· Instrumentación Smali completamente automatizada
· Sistema de filtros por tag y nivel
· Timestamps del lado del cliente
· Tests automatizados
· Documentación completa de la API Smali

---

⚠️ Consideraciones

Este proyecto está orientado a instrumentación, depuración y análisis de aplicaciones Android propias o autorizadas.

No debe utilizarse para interceptar información de aplicaciones, dispositivos o usuarios sin autorización explícita.

Además, el servidor escucha únicamente en 127.0.0.1 y no está diseñado como servidor de producción.

---

🤝 Contribuir

Las contribuciones son bienvenidas. Antes de enviar cambios:

1. Verifica las dependencias nativas:
   ```bash
   readelf -d liblogger.so | grep NEEDED
   ```
   Debe conservar únicamente libdl.so y libc.so.
2. Prueba el pipeline completo:
   ```text
   Java → Smali → JNI → liblogger.so → log_server.py
   ```
3. Si tocas el inyector, ejecuta las pruebas del subpaquete injector/.

---

📚 Documentación relacionada

· Documentación de Smali
· Documentación JNI (Oracle / Android NDK)
· Android Runtime (ART)
· Android Application Lifecycle
· ELF / readelf
· AArch64 ABI

---

<div align="center">

Hecho con ☕ y mucho readelf · Remote Logger · Experimental / WIP

</div>
