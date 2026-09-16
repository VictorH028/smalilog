# Descripción General

*native_logger.c* es un módulo JNI (Java Native Interface) escrito en C que permite enviar logs desde una aplicación Java/Android hacia un servidor HTTP local escuchando en 127.0.0.1:9999.

El envío se realiza de forma asíncrona mediante un hilo POSIX (pthread), de modo que la llamada desde Java no bloquea el hilo principal de la aplicación.

# Constantes
Constante Valor Descripción
- LOGGER_HOST "127.0.0.1" Host del servidor de logs
- LOGGER_PORT 9999 Puerto del servidor
- MAX_LOG_FIELD 16384 Tamaño máximo por campo (level/tag/message)
- MAX_JSON_SIZE 65536 Tamaño máximo del JSON
- MAX_REQUEST_SIZE 73728 Tamaño máximo de la petición HTTP completa

--- 

# Estructuras y Tipos

> struct LogData

Contenedor que transporta los datos del log hacia el hilo.

```c
struct LogData {
    char *level;
    char *tag;
    char *message;
};
```

Cada campo es una copia propia del string (no apunta a memoria gestionada por la JVM).

--- 

# Petición HTTP generada:

```http
POST /log HTTP/1.1
Host: 127.0.0.1
Content-Type: application/json
Content-Length: <n>
Connection: close

{"level":"INFO","tag":"MainActivity","message":"Hola \"mundo\""}
```

# Función JNI Pública 

`Java_com_deadnote_RemoteLogger_nativeSendLog`

```c
JNIEXPORT void JNICALL
Java_com_deadnote_RemoteLogger_nativeSendLog(
    JNIEnv *env,
    jclass clazz,
    jstring jlevel,
    jstring jtag,
    jstring jmessage
);
```

Firma en Java

```java
package com.deadnote;

public class RemoteLogger {
    static {
        System.loadLibrary("native_logger");
    }

    public static native void nativeSendLog(
        String level,
        String tag,
        String message
    );
}
```

[RemoteLogger](url) 

> [!WARNING]
> El nombre debe coincidir exactamente: paquete com.deadnote, clase RemoteLogger, método nativeSendLog.
