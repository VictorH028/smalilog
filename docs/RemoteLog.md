# RemoteLogger — Documentación Técnica

`RemoteLog` es un cliente de depuración **100 % Java** para Android que actúa como interfaz frente a la capa nativa JNI (`smalilog.so`). Permite instrumentar código en tiempo de ejecución, trazar entradas y salidas de funciones, y serializar estructuras de datos complejas sin bloquear el hilo principal (*UI Thread*) y garantizando tolerancia total a fallos.

---

## 🏗 Arquitectura y Diseño

El diseño se apoya en tres pilares:

1. **Reutilización de capa nativa**: Los métodos de trazado y colecciones procesan la información en Java y la canalizan a través de la función nativa existente `nativeSendLog(String level, String tag, String message)`. No requiere modificaciones en C/C++ ni cambios en las firmas JNI.
2. **Ejecución Asíncrona (*Fire-and-Forget*)**: Ninguna llamada a `RemoteLog` bloquea el hilo de ejecución de la aplicación. Los datos se formatean, se encolan en el búfer circular nativo (256 slots) y un hilo *worker* nativo procesa el envío mediante HTTP/JSON en lotes.
3. **Resiliencia Total (*Fail-Safe*)**: Todo el árbol de llamadas (serialización, reflexión, acceso a colecciones) está envuelto en bloques `try/catch (Throwable)`. Si la librería C no está cargada (`UnsatisfiedLinkError`), hay un error de memoria o una excepción al invocar `toString()`, el error se absorbe silenciosamente y la app continúa su ejecución sin interrupciones.



+-------------------------------------------------------------------+ | Hilo de Aplicación | | traceIn() / traceOut() / logList() / d() / i() / w() / e() | +-------------------------------------------------------------------+ | v Formatters Java & Guards (formatValue, quote, truncate) | v (JNI - nativeSendLog) +-------------------------------------------------------------------+ | Capa Nativa (C) | | Cola circular acotada (256) | +-------------------------------------------------------------------+ | v (Hilo Worker Nativo) Servidor smalilog (HTTP/JSON)
---

## 🛠 Referencia de la API Java

### 1. Configuración y Diagnóstico

| Método | Descripción |
| :--- | :--- |
| `configure(String host, int port)` | Establece la dirección IP y puerto del servidor `smalilog`. Llamar preferentemente en `Application.onCreate()`. |
| `shutdown()` | Notifica a la capa nativa que debe procesar el *flush* de los mensajes pendientes en cola y detener el hilo *worker*. |
| `droppedCount()` | Devuelve el total de mensajes descartados por saturación de cola o fallos de red. Devuelve `-1` si la librería nativa no está cargada. |

---

### 2. Trazado de Funciones (`traceIn` / `traceOut`)

Permite rastrear el flujo de ejecución capturando parámetros de entrada y valores de retorno o excepciones. 

#### Métodos disponibles

```java
// Entrada
public static long traceIn(String function, Object... params)

// Salida Normal
public static void traceOut(String function, Object result)
public static void traceOut(String function, long traceId, Object result)

// Salida Void
public static void traceOutVoid(String function)
public static void traceOutVoid(String function, long traceId)

// Salida por Excepción
public static void traceOutError(String function, Throwable error)
public static void traceOutError(String function, long traceId, Throwable error)
```

Id de Correlación

`traceIn` genera un identificador único incremental de tipo long (AtomicLong). Pasar este ID a las variantes de `traceOut` permite al servidor de logs emparejar llamadas concurrentes o recursivas mediante el prefijo #ID.

Ejemplo de integración

```java 
public User processOrder(String orderId, List<Item> items, double discount) throws OrderException {
    // 1. Entrada con captura de ID
    long traceId = RemoteLogger.traceIn("processOrder", orderId, items, discount);
    
    try {
        User result = storeService.checkout(orderId, items, discount);
        
        // 2. Salida exitosa correlacionada
        RemoteLogger.traceOut("processOrder", traceId, result);
        return result;
    } catch (OrderException e) {
        // 3. Salida por error correlacionada (Registrado como nivel ERROR)
        RemoteLogger.traceOutError("processOrder", traceId, e);
        throw e; // La excepción sigue su flujo normal
    }
}
```
---

**Formato impreso en servidor (tag: "TRACE")**
Transición
Formato del Mensaje
Nivel
*Entrada*
`#<id> -> <función>(<param1>, <param2>, ...)`
DEBUG
Salida
`#<id> <- <función> = <valor_retorno>`
DEBUG
Salida Void
`#<id> <- <función> = void`
DEBUG
Excepción
`#<id> <- <función> LANZÓ <ExceptionClass>(<mensaje>)`
ERROR

3. Registro de Colecciones (logList / logCollection)
Recorren estructuras lineales iterables e imprimen cada elemento como un registro independiente en el servidor. Esto facilita la inspección, ordenación y filtrado por índice.
public static void logList(String tag, List<?> items)
public static void logCollection(String tag, Collection<?> items)


Ejemplo de uso
List<Product> catalog = fetchCatalog();
RemoteLogger.logList("CatalogDebug", catalog);


Ejemplo de salida en el servidor
2026-10-02 11:44:00 - INFO - [CatalogDebug] [0] Product(id=101, name="Keyboard")
2026-10-02 11:44:00 - INFO - [CatalogDebug] [1] Product(id=102, name="Mouse")
2026-10-02 11:44:00 - INFO - [CatalogDebug] ... 18 elemento(s) omitidos


⚙️ Motor de Serialización Java (formatValue)
El método interno formatValue inspecciona dinámicamente los tipos de datos recibidos y los transforma a una representación en texto legible sin riesgo de desbordamiento de memoria ni bucles infinitos.
Mapeo de Tipos de Datos
Tipo de Dato Java
Regla de Formateo
Ejemplo de Salida
null
Cadena explícita
null
String
Comillas dobles con escapado de control (\n, \t, \", \\)
"Línea 1\nLínea 2"
Character
Comilla simple
'Z'
Number / Boolean
Invocación directa a toString()
1054.50, true
Throwable
Nombre de la clase + mensaje de la excepción
NullPointerException(address is null)
Array (Primitivos / Objetos)
Formato [...] mediante Array.get() sintético
[1, 2, 3]
Collection
Iteración incremental en formato [...]
["admin", "guest"]
Map
Pares clave=valor en formato {k=v}
{id=1001, type="admin"}
POJO / Objeto Genérico
Nombre simple de la clase + toString() envuelto
User(id=42, name="John")
Objeto con toString() defectuoso
Captura del fallo y reporte seguro
Order(<toString falló: NullPointerException>)

Constantes y Límites de Seguridad
Para prevenir el consumo masivo de memoria RAM o la saturación del ancho de banda, la serialización impone límites estrictos:
MAX_TEXT_LENGTH  = 4096; // Tamaño máximo en caracteres del mensaje enviando al nativeSendLog
MAX_VALUE_LENGTH = 512;  // Tamaño máximo de cualquier String individual recortado con "..."
MAX_DEPTH        = 4;    // Nivel máximo de anidamiento de estructuras de datos
MAX_ITEMS_SHOWN  = 16;   // Elementos visibles dentro de un Array/Collection/Map anidado
MAX_LIST_ITEMS   = 64;   // Elementos máximos procesados de forma independiente en logList


📋 Guía de Integración
1. Inicialización en el Ciclo de Vida
Configura el cliente en la clase Application o en el punto de entrada de la app, y asegúrate de invocar shutdown() al cerrar los componentes principales para vaciar los búferes.
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // En emulador Android usar "10.0.2.2", en dispositivo físico usar "127.0.0.1" con adb reverse
        RemoteLogger.configure("127.0.0.1", 9999);
        RemoteLogger.i("Lifecycle", "MainActivity creada");
    }

    @Override
    protected void onDestroy() {
        RemoteLogger.i("Lifecycle", "MainActivity destruida");
        RemoteLogger.shutdown(); // Flush de la cola de logs nativa
        super.onDestroy();
    }
}


2. Configuración de Red en Dispositivos Físicos
Para redirigir el tráfico desde un dispositivo Android físico hacia el servidor ejecutándose en tu equipo de desarrollo:
adb reverse tcp:9999 tcp:9999


⚠️ Consideraciones de Seguridad y Producción
Compilación Condicional: Esta librería no utiliza mecanismos de cifrado ni autenticación. Los logs se transmiten en texto plano. Se recomienda limitar su uso exclusivamente a builds de depuración:
if (BuildConfig.DEBUG) {
    RemoteLogger.configure("127.0.0.1", 9999);
}


Privacidad de Datos: La serialización automática de objetos POJO y colecciones enviará la representación completa generada por toString(). No pases objetos que contengan tokens de acceso, contraseñas, o información personal identificable (PII) a métodos de depuración.


