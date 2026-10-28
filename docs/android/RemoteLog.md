# RemoteLog

Log remoto para Android con **envío asíncrono a un servidor `smalilog`**,
implementado como un wrapper Java sobre una librería nativa (`liblogger.so`).

Está diseñado para ser **completamente seguro para producción**: nunca lanza
excepciones, nunca bloquea el hilo llamador, trunca valores excesivamente
grandes y tolera objetos defectuosos (`toString()` roto, colecciones que
explotan al iterarse, `null`s por doquier). Si algo falla en el camino, el log
se pierde silenciosamente — **la aplicación sigue funcionando**.

> 📖 Servidor de recepción y protocolo HTTP: [`../server.md`](../server.md).
> Esta clase pertenece a la app de prueba `build_payloads`; no forma parte del
> paquete Python.

---

## ✨ Características

- 🚀 **No bloqueante** — el envío real ocurre en un hilo nativo.
- 🛡️ **A prueba de fallos** — cualquier `Throwable` interno se traga.
- 📊 **Serialización inteligente** de parámetros:
  - Primitivos, `String`, `Character`, `Boolean`, `Number`
  - Arrays (incluidos primitivos vía `Array.get`)
  - `Collection`, `Map`
  - `Throwable` (clase + mensaje)
  - POJOs (usa `toString()` protegido)
- 🔢 **Límites de seguridad** para no reventar el socket ni el servidor:
  - Mensaje final: **4096** caracteres
  - Strings individuales: **512** caracteres
  - Profundidad de anidamiento: **4** niveles
  - Elementos por colección/array/map: **16**
  - Elementos enviados por `logList`/`logCollection`: **64**
- 🔗 **Trazado correlacionado** de entrada/salida (`traceIn` / `traceOut`).
- 📉 **Métrica de descartes** (`droppedCount()`) para saber si el backend no da abasto.
- 🧵 **`AtomicLong`** para IDs de trace thread-safe.

---

## 📁 Estructura

```

com/deadnote/
└── RemoteLog.java     ← este archivo (API pública + serialización)

libs/
└── <abi>/liblogger.so ← librería nativa (una por ABI)

```

---

## ⚙️ Instalación

### 1. Copiar el código

Coloca `RemoteLog.java` en tu paquete (por defecto `com.deadnote`).

### 2. Incluir la librería nativa

Añade `liblogger.so` para cada ABI soportada:

```

jniLibs/
├── arm64-v8a/liblogger.so
├── armeabi-v7a/liblogger.so
├── x86/liblogger.so
└── x86_64/liblogger.so

```

La clase carga la librería en un bloque `static`:

```java
static {
    System.loadLibrary("logger");
}
```

## ⚠️ Si la librería no está presente en el dispositivo, el bloque static
lanzará UnsatisfiedLinkError. Envuélvela en un try/catch si quieres
que la app arranque sin logging remoto.

3. Configurar el servidor

Llámalo una sola vez, idealmente en Application.onCreate():

```java
RemoteLog.configure("logs.midominio.com", 9000);
```

---

## 🚀 Uso

Niveles básicos

```java
RemoteLog.d("Auth", "Token recibido");
RemoteLog.i("Sync",  "Sincronización completada en 342 ms");
RemoteLog.w("Cache", "Entrada expirada, recargando");
RemoteLog.e("Net",   "Timeout al conectar con el backend");
```

Trazado de funciones

```java
public int sumar(int a, int b) {
    long id = RemoteLog.traceIn("sumar", a, b);
    try {
        int result = a + b;
        RemoteLog.traceOut("sumar", id, result);
        return result;
    } catch (Throwable t) {
        RemoteLog.traceOutError("sumar", id, t);
        throw t;   // la excepción sigue su curso
    }
}
```

Para funciones void:

```java
public void limpiarCache() {
    long id = RemoteLog.traceIn("limpiarCache");
    // ...
    RemoteLog.traceOutVoid("limpiarCache", id);
}
```

Listas y colecciones

Cada elemento se envía como una entrada independiente ([i] valor),
facilitando el filtrado y la lectura en el servidor:

```java
List<String> urls = Arrays.asList("a.com", "b.com", "c.com");
RemoteLog.logList("Endpoints", urls);

// Salida en el servidor:
// INFO  [Endpoints] [0] "a.com"
// INFO  [Endpoints] [1] "b.com"
// INFO  [Endpoints] [2] "c.com"
```

Se envían como máximo 64 elementos; si la lista es más grande:

```
INFO [Endpoints] ... 27 elemento(s) omitidos
```

Diagnóstico y cierre

```java
long dropped = RemoteLog.droppedCount();
if (dropped > 0) {
    Log.w("App", "Se descartaron " + dropped + " logs remotos");
}

// Al cerrar la app (onTerminate, onDestroy del Application, etc.)
RemoteLog.shutdown();
```

droppedCount() devuelve:

· >= 0 → número real de logs descartados.
· -1   → la librería nativa no está disponible.

---

## 📐 Límites de serialización

Constante Valor Descripción
MAX_TEXT_LENGTH 4096 Longitud máxima del mensaje final
MAX_VALUE_LENGTH 512 Longitud máxima de cada string serializado
MAX_DEPTH 4 Profundidad máxima de anidamiento
MAX_ITEMS_SHOWN 16 Elementos mostrados por array/colección/map
MAX_LIST_ITEMS 64 Elementos enviados en logList/logCollection

Cuando se excede un límite:

· Strings largos → "texto truncado..."
· Colecciones grandes → [a, b, ..., ...(42 más)]
· Anidamiento profundo → ...

---

## 🧬 Formato de valores

Tipo Java Representación
null null
String "texto" (con \n, \t, \" escapados)
Character 'c'
Boolean/Number toString() directo
Throwable IllegalStateException(mensaje)
Array [1, 2, 3, ...(N más)]
Collection [a, b, c, ...(N más)]
Map {k1=v1, k2=v2, ...(N más)}
POJO NombreClase(toString())

---

## 🔒 Garantías de seguridad

1. Nunca lanza excepciones al llamador. Toda la API pública está envuelta
   en try/catch (Throwable) o delega en métodos que lo están.
2. Nunca bloquea — la serialización es CPU-bound y acotada; el envío es
   nativo y asíncrono.
3. Tolera objetos hostiles:
   · toString() que lanza → "<toString falló: X>"
   · Colecciones que revientan al iterarse → <colección defectuosa>
   · Valores no serializables → "<valor no serializable>"
4. Trunca antes de enviar, así que un mensaje enorme no puede tumbar
   el socket ni el servidor.

---

## 🧵 Concurrencia

· Los métodos d/i/w/e/trace*/log* son thread-safe por diseño: toda la
  sincronización ocurre en la capa nativa.
· TRACE_ID es un AtomicLong, por lo que los IDs de correlación son únicos
  incluso bajo uso concurrente intenso.
· No hay estado mutable compartido en Java.

---

## 🧩 API pública

```java
public final class RemoteLog {

    // Ciclo de vida
    public static void configure(String host, int port);
    public static void shutdown();

    // Niveles
    public static void d(String tag, String msg);
    public static void i(String tag, String msg);
    public static void w(String tag, String msg);
    public static void e(String tag, String msg);

    // Trazado
    public static long traceIn(String function, Object... params);
    public static void traceOut(String function, Object result);
    public static void traceOut(String function, long traceId, Object result);
    public static void traceOutVoid(String function);
    public static void traceOutVoid(String function, long traceId);
    public static void traceOutError(String function, Throwable error);
    public static void traceOutError(String function, long traceId, Throwable error);

    // Colecciones
    public static void logList(String tag, List<?> items);
    public static void logCollection(String tag, Collection<?> items);

    // Diagnóstico
    public static long droppedCount();
}
```

---

## 🧪 Ejemplo completo

```java
public final class App extends Application {

    @Override
    public void onCreate() {
        super.onCreate();

        RemoteLog.configure("logs.midominio.com", 9000);
        RemoteLog.i("App", "Arrancando versión " + BuildConfig.VERSION_NAME);

        probarTrazado();
    }

    private void probarTrazado() {
        List<String> urls = Arrays.asList(
            "https://a.com", "https://b.com", "https://c.com"
        );

        long id = RemoteLog.traceIn("fetchAll", urls, 3, true);
        try {
            Map<String, Integer> results = new HashMap<>();
            results.put("a", 200);
            results.put("b", 404);

            RemoteLog.logCollection("Results", results.entrySet());

            RemoteLog.traceOut("fetchAll", id, results);
        } catch (Throwable t) {
            RemoteLog.traceOutError("fetchAll", id, t);
        }
    }

    @Override
    public void onTerminate() {
        RemoteLog.i("App", "Cerrando, drops=" + RemoteLog.droppedCount());
        RemoteLog.shutdown();
        super.onTerminate();
    }
}
```

---

## 🛠️ Integración con Backup

Backup usa RemoteLog para reportar el resultado del respaldo:

```java
RemoteLog.i("DEADNOTE_BACKUP", "Backup creado: " + path);
RemoteLog.e("Error creando backup", "Error");
```

Ver Backup.java para más detalles.

---

## ⚠️ Limitaciones conocidas

## Limitación
1 Si liblogger.so no está presente, todas las llamadas son no-op silencioso.
2 droppedCount() devuelve -1 cuando la librería no está disponible.
3 No hay sampling ni rate limiting a nivel Java.
4 El remitente nativo (hilo, buffer, reintentos) no se configura aquí.
5 Sin TLS/autenticación a nivel Java; depende del backend nativo.
6 Los POJOs sin toString() útil se registran como Clase@hashcode.
7 No serializa enums de forma especial (cae en POJO).

---

## 🛡️ Recomendaciones

· 🔐 Asegurar el canal (TLS) y añadir un token de autenticación en configure.
· 📉 Implementar rate limiting en el lado nativo para no saturar la red.
· 🧪 Añadir un RemoteLog.NOOP para builds de release sin logging.
· 📦 Versionar liblogger.so y comprobar la ABI en tiempo de build.
· 📝 Emitir un w() la primera vez que un mensaje se trunca, para detectar
  problemas de formato en producción.

---

## 📄 Licencia



