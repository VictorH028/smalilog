package com.deadnote;

import java.lang.reflect.Array;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Logger remoto para depuración. Envía entradas a un servidor smalilog
 * de forma asíncrona, sin bloquear y sin lanzar excepciones.
 *
 * Documentación completa: RemoteLogger.md
 */
public final class RemoteLog {

    static {
        System.loadLibrary("logger");
        System.loadLibrary("agent");
    }

    private RemoteLog() {
    }

    /* ---------------- Límites de serialización ---------------- */

    private static final int MAX_TEXT_LENGTH = 4096; /* mensaje final enviado */
    private static final int MAX_VALUE_LENGTH = 512; /* string individual */
    private static final int MAX_DEPTH = 4; /* anidamiento máximo */
    private static final int MAX_ITEMS_SHOWN = 16; /* elementos en colecciones */
    private static final int MAX_LIST_ITEMS = 64; /* elementos enviados logList */

    /** Id incremental para correlacionar traceIn/traceOut. */
    private static final AtomicLong TRACE_ID = new AtomicLong(0);

    /* ================= Ciclo de vida ================= */

    /** Configura el servidor destino. Llamar una vez, antes del primer log. */
    public static void configure(String host, int port) {
        try {
            nativeConfigure(host, port);
        } catch (Throwable ignored) {
        }
    }

    /* ================= Niveles básicos ================= */

    public static void d(String tag, String msg) {
        send("DEBUG", tag, msg);
    }

    public static void i(String tag, String msg) {
        send("INFO", tag, msg);
    }

    public static void w(String tag, String msg) {
        send("WARNING", tag, msg);
    }

    public static void e(String tag, String msg) {
        send("ERROR", tag, msg);
    }

    /* ================= Trazado de funciones ================= */

    /**
     * Registra la ENTRADA a una función junto con sus parámetros.
     * La ejecución continúa siempre: este método solo encola.
     *
     * @return id de correlación; pásalo a traceOut/traceOutError para
     *         que el servidor casé entrada y salida.
     */
    public static long traceIn(String function, Object... params) {
        long id = TRACE_ID.incrementAndGet();

        StringBuilder sb = new StringBuilder(64);
        sb.append('#').append(id).append(" -> ").append(function).append('(');
        if (params != null) {
            for (int i = 0; i < params.length; i++) {
                if (i > 0)
                    sb.append(", ");
                sb.append(formatValue(params[i], 0));
            }
        }
        sb.append(')');

        send("DEBUG", "TRACE", sb.toString());
        return id;
    }

    /** Salida normal de una función, con su valor de retorno. */
    public static void traceOut(String function, Object result) {
        send("DEBUG", "TRACE", "<- " + function + " = " + formatValue(result, 0));
    }

    /** Salida normal correlacionada con un traceIn previo. */
    public static void traceOut(String function, long traceId, Object result) {
        send("DEBUG", "TRACE",
                "#" + traceId + " <- " + function + " = " + formatValue(result, 0));
    }

    /** Salida de una función void (sin id de correlación). */
    public static void traceOutVoid(String function) {
        send("DEBUG", "TRACE", "<- " + function + " = void");
    }

    /** Salida de una función void, correlacionada. */
    public static void traceOutVoid(String function, long traceId) {
        send("DEBUG", "TRACE", "#" + traceId + " <- " + function + " = void");
    }

    /**
     * Salida por excepción: se registra a nivel ERROR. La excepción sigue su curso
     * normal.
     */
    public static void traceOutError(String function, Throwable error) {
        send("ERROR", "TRACE", "<- " + function + " LANZÓ " + formatValue(error, 0));
    }

    /** Salida por excepción, correlacionada. */
    public static void traceOutError(String function, long traceId, Throwable error) {
        send("ERROR", "TRACE",
                "#" + traceId + " <- " + function + " LANZÓ " + formatValue(error, 0));
    }

    /* ================= Listas y colecciones ================= */

    /**
     * Recorre la lista y envía cada elemento como una entrada independiente:
     * "[i] valor". Máximo MAX_LIST_ITEMS elementos; el resto se informa.
     */
    public static void logList(String tag, List<?> items) {
        logCollection(tag, items);
    }

    /** Igual que logList, para cualquier Collection. */
    public static void logCollection(String tag, Collection<?> items) {
        try {
            if (items == null) {
                send("INFO", tag, "<colección null>");
                return;
            }

            int size = items.size();
            if (size == 0) {
                send("INFO", tag, "<colección vacía>");
                return;
            }

            int sent = 0;
            Iterator<?> it = items.iterator();
            while (it.hasNext() && sent < MAX_LIST_ITEMS) {
                send("INFO", tag, "[" + sent + "] " + formatValue(it.next(), 1));
                sent++;
            }

            if (size > sent) {
                send("INFO", tag, "... " + (size - sent) + " elemento(s) omitidos");
            }
        } catch (Throwable ignored) {
            /* Una colección defectuosa no debe romper la aplicación. */
        }
    }

    /* ================= Apagado y diagnóstico ================= */

    /** Vacía la cola y detiene el hilo nativo. Úsalo al cerrar la app. */
    public static void shutdown() {
        try {
            nativeShutdown();
        } catch (Throwable ignored) {
        }
    }

    /**
     * Logs descartados desde el arranque (cola llena o fallo de red). -1 si la lib
     * no carga.
     */
    public static long droppedCount() {
        try {
            return nativeGetDroppedCount();
        } catch (Throwable t) {
            return -1;
        }
    }

    /* ================= Envío interno ================= */

    private static void send(String level, String tag, String msg) {
        try {
            nativeSendLog(level, tag, truncate(msg == null ? "null" : msg, MAX_TEXT_LENGTH));
        } catch (Throwable ignored) {
            /* La depuración nunca debe romper la aplicación. */
        }
    }

    /* ================= Serialización de valores ================= */

    /**
     * Representa un valor según su tipo de dato Java, con límites de
     * longitud, profundidad y elementos. Nunca lanza.
     */
    private static String formatValue(Object value, int depth) {
        if (depth > MAX_DEPTH) {
            return "...";
        }

        try {
            if (value == null) {
                return "null";
            }
            if (value instanceof String) {
                return quote((String) value);
            }
            if (value instanceof Character) {
                return "'" + value + "'";
            }
            if (value instanceof Boolean || value instanceof Number) {
                return value.toString();
            }
            if (value instanceof Throwable) {
                Throwable t = (Throwable) value;
                String msg = t.getMessage();
                return t.getClass().getSimpleName()
                        + "(" + (msg == null ? "sin mensaje" : msg) + ")";
            }
            if (value.getClass().isArray()) {
                return formatArray(value, depth);
            }
            if (value instanceof Collection) {
                return formatCollection((Collection<?>) value, depth);
            }
            if (value instanceof Map) {
                return formatMap((Map<?, ?>) value, depth);
            }

            /* POJO u otro objeto: NombreClase(toString()), protegido. */
            String s;
            try {
                s = value.toString();
            } catch (Throwable t) {
                s = "<toString falló: " + t.getClass().getSimpleName() + ">";
            }
            return value.getClass().getSimpleName() + "(" + s + ")";
        } catch (Throwable ignored) {
            return "<valor no serializable>";
        }
    }

    /*
     * Array.get() funciona con primitivos: devuelve el boxed (Integer, Double, ...)
     */
    private static String formatArray(Object array, int depth) {
        int len = Array.getLength(array);
        int shown = Math.min(len, MAX_ITEMS_SHOWN);

        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < shown; i++) {
            if (i > 0)
                sb.append(", ");
            sb.append(formatValue(Array.get(array, i), depth + 1));
        }
        if (len > shown) {
            sb.append(", ...(").append(len - shown).append(" más)");
        }
        return sb.append(']').toString();
    }

    private static String formatCollection(Collection<?> collection, int depth) {
        int size = collection.size();
        int shown = 0;

        StringBuilder sb = new StringBuilder("[");
        for (Object item : collection) {
            if (shown >= MAX_ITEMS_SHOWN) {
                break;
            }
            if (shown > 0)
                sb.append(", ");
            sb.append(formatValue(item, depth + 1));
            shown++;
        }
        if (size > shown) {
            sb.append(", ...(").append(size - shown).append(" más)");
        }
        return sb.append(']').toString();
    }

    private static String formatMap(Map<?, ?> map, int depth) {
        int size = map.size();
        int shown = 0;

        StringBuilder sb = new StringBuilder("{");
        for (Map.Entry<?, ?> entry : map.entrySet()) {
            if (shown >= MAX_ITEMS_SHOWN) {
                break;
            }
            if (shown > 0)
                sb.append(", ");
            sb.append(formatValue(entry.getKey(), depth + 1))
                    .append('=')
                    .append(formatValue(entry.getValue(), depth + 1));
            shown++;
        }
        if (size > shown) {
            sb.append(", ...(").append(size - shown).append(" más)");
        }
        return sb.append('}').toString();
    }

    private static String quote(String s) {
        String trimmed = truncate(s, MAX_VALUE_LENGTH);

        StringBuilder sb = new StringBuilder(trimmed.length() + 2);
        sb.append('"');
        for (int i = 0; i < trimmed.length(); i++) {
            char c = trimmed.charAt(i);
            switch (c) {
                case '"':
                    sb.append("\\\"");
                    break;
                case '\\':
                    sb.append("\\\\");
                    break;
                case '\n':
                    sb.append("\\n");
                    break;
                case '\r':
                    sb.append("\\r");
                    break;
                case '\t':
                    sb.append("\\t");
                    break;
                default:
                    sb.append(c);
                    break;
            }
        }
        return sb.append('"').toString();
    }

    private static String truncate(String s, int max) {
        if (s == null || s.length() <= max) {
            return s;
        }
        return s.substring(0, max - 3) + "...";
    }

    /* ================= Nativos (sin cambios respecto al .c) ================= */

    private static native void nativeConfigure(String host, int port);

    private static native void nativeSendLog(String level, String tag, String message);

    private static native void nativeShutdown();

    private static native long nativeGetDroppedCount();
}
