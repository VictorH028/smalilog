package com.deadnote;

import android.content.Context;
import android.net.LocalSocket;
import android.net.LocalSocketAddress;
import android.os.Process;
import android.util.Base64;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.UUID;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Puente Java -> agente Renef embebido en libagent.so.
 *
 * El agente abre un socket UNIX abstracto llamado renef_pl_<pid>. Este puente
 * se conecta, hace el handshake "con <clave>" y envía comandos hexexec con
 * código Lua. La conexión se mantiene abierta: al cerrarla el agente elimina
 * todos los hooks instalados.
 */
public final class RenefRuntime {

    private static final String TAG = "RenefRuntime";
    private static final int COMMAND_TIMEOUT_MS = 8000;
    private static final int MAX_SCRIPT_BYTES = 30 * 1024;

    private static final Object LOCK = new Object();
    private static final Object CLOSE_LOCK = new Object();
    private static final LinkedBlockingQueue<String> RESPONSES = new LinkedBlockingQueue<>();
    private static final AtomicBoolean WAITING_RESPONSE = new AtomicBoolean(false);

    private static LocalSocket socket;
    private static BufferedReader reader;
    private static OutputStream writer;
    private static String sessionKey;
    private static Thread readerThread;

    static {
        System.loadLibrary("logger");
        System.loadLibrary("agent");
    }

    private RenefRuntime() {
    }

    public static String execLuaFile(Context context, String path) {
        File file = resolveFile(context, path);
        if (file == null) {
            return "ERROR: ruta Lua vacía";
        }
        if (!file.isFile()) {
            return "ERROR: no existe " + file.getAbsolutePath();
        }
        try {
            String code = readFile(file);
            String result = execLua(code);
            RemoteLog.i(TAG, "Lua " + file.getAbsolutePath() + ": " + result);
            return result;
        } catch (Throwable t) {
            RemoteLog.e(TAG, "Error leyendo " + file.getAbsolutePath() + ": " + t);
            return "ERROR: " + t;
        }
    }

    /**
     * Guarda un Lua en el directorio privado de la app y lo ejecuta.
     * Permite instalar scripts por broadcast sin run-as ni permisos de almacenamiento.
     */
    public static String saveLuaAndExec(Context context, String name, String base64) {
        if (base64 == null || base64.isEmpty()) {
            return "ERROR: código Lua vacío";
        }
        try {
            byte[] data = Base64.decode(base64, Base64.DEFAULT);
            String safeName = new File(name == null ? "runtime.lua" : name).getName();
            if (safeName.isEmpty()) {
                safeName = "runtime.lua";
            }
            if (!safeName.endsWith(".lua")) {
                safeName += ".lua";
            }
            File file = new File(context.getFilesDir(), safeName);
            try (FileOutputStream out = new FileOutputStream(file)) {
                out.write(data);
            }
            RemoteLog.i(TAG, "Lua guardado en " + file.getAbsolutePath());
            String result = execLua(new String(data, StandardCharsets.UTF_8));
            RemoteLog.i(TAG, "Lua " + file.getAbsolutePath() + ": " + result);
            return result;
        } catch (Throwable t) {
            RemoteLog.e(TAG, "Error guardando Lua: " + t);
            return "ERROR: " + t;
        }
    }

    public static String execLuaBase64(String base64) {
        if (base64 == null || base64.isEmpty()) {
            return "ERROR: código Lua vacío";
        }
        try {
            byte[] data = Base64.decode(base64, Base64.DEFAULT);
            return execLua(new String(data, StandardCharsets.UTF_8));
        } catch (Throwable t) {
            RemoteLog.e(TAG, "Base64 inválido: " + t);
            return "ERROR: " + t;
        }
    }

    public static String execLua(String code) {
        if (code == null || code.trim().isEmpty()) {
            return "ERROR: código Lua vacío";
        }
        byte[] data = code.getBytes(StandardCharsets.UTF_8);
        if (data.length > MAX_SCRIPT_BYTES) {
            return "ERROR: script demasiado grande: " + data.length + " bytes";
        }
        return sendCommand("hexexec " + toHex(data));
    }

    /**
     * Elimina todos los hooks (nativos y Java) cerrando la conexión: el agente
     * restaura todo al detectar el EOF. También resetea la guarda Lua para que
     * el próximo script pueda reinstalar sus hooks.
     */
    public static String unhookAll() {
        synchronized (LOCK) {
            RemoteLog.i(TAG, "unhook: reseteando guarda");
            String reset = sendCommand("hexexec " + toHex(
                    "_G.__smalilog_runtime_hook = nil".getBytes(StandardCharsets.UTF_8)));
            RemoteLog.i(TAG, "unhook: guarda=" + reset);
            close();
            RemoteLog.i(TAG, "unhook: conexión cerrada");
            if (reset.startsWith("ERROR")) {
                return reset;
            }
            return "OK: hooks eliminados";
        }
    }

    private static String sendCommand(String command) {
        synchronized (LOCK) {
            try {
                ensureConnected();
                RESPONSES.clear();
                WAITING_RESPONSE.set(true);
                armWatchdog();
                String payload = sessionKey + " " + command + "\n";
                writer.write(payload.getBytes(StandardCharsets.UTF_8));
                writer.flush();

                String response = RESPONSES.poll(COMMAND_TIMEOUT_MS, TimeUnit.MILLISECONDS);
                WAITING_RESPONSE.set(false);
                if (response == null) {
                    close();
                    RemoteLog.e(TAG, "Timeout esperando al agente Renef");
                    return "ERROR: timeout";
                }
                return response;
            } catch (Throwable t) {
                WAITING_RESPONSE.set(false);
                close();
                RemoteLog.e(TAG, "Error ejecutando comando Renef: " + t);
                return "ERROR: " + t;
            }
        }
    }

    private static void ensureConnected() throws IOException {
        if (socket != null && socket.isConnected()) {
            return;
        }
        close();

        LocalSocketAddress address = new LocalSocketAddress(
                "renef_pl_" + Process.myPid(),
                LocalSocketAddress.Namespace.ABSTRACT);

        LocalSocket connected = null;
        IOException last = null;
        for (int i = 0; i < 40; i++) {
            LocalSocket candidate = new LocalSocket();
            try {
                candidate.connect(address);
                connected = candidate;
                last = null;
                break;
            } catch (IOException e) {
                last = e;
                try {
                    candidate.close();
                } catch (IOException ignored) {
                }
                try {
                    Thread.sleep(50);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
        if (connected == null) {
            throw last != null ? last : new IOException("no se pudo conectar al agente");
        }

        socket = connected;
        writer = connected.getOutputStream();
        reader = new BufferedReader(
                new InputStreamReader(connected.getInputStream(), StandardCharsets.UTF_8));
        sessionKey = UUID.randomUUID().toString().replace("-", "");

        writer.write(("con " + sessionKey + "\n").getBytes(StandardCharsets.UTF_8));
        writer.flush();

        // El agente espera 50 ms tras el salto de línea para decidir si el
        // comando terminó. Si enviamos "con" y "hexexec" seguidos, los une en
        // el mismo buffer y pierde el segundo. Deja que procese el handshake.
        try {
            Thread.sleep(200);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        readerThread = new Thread(RenefRuntime::readLoop, "RenefRuntime-reader");
        readerThread.setDaemon(true);
        readerThread.start();

        RemoteLog.i(TAG, "Conectado al agente Renef @renef_pl_" + Process.myPid());
    }

    private static void readLoop() {
        try {
            String line;
            while ((line = reader.readLine()) != null) {
                if (WAITING_RESPONSE.get() && isResponse(line)) {
                    RESPONSES.offer(line);
                } else {
                    RemoteLog.i("RenefLua", line);
                }
            }
        } catch (Throwable t) {
            if (socket != null) {
                RemoteLog.w(TAG, "Lector Renef terminó: " + t);
            }
        } finally {
            close();
        }
    }

    private static void armWatchdog() {
        Thread watchdog = new Thread(() -> {
            try {
                Thread.sleep(COMMAND_TIMEOUT_MS + 2000L);
            } catch (InterruptedException e) {
                return;
            }
            if (WAITING_RESPONSE.get()) {
                RemoteLog.w(TAG, "Watchdog Renef: sin respuesta, cerrando conexión");
                close();
            }
        }, "RenefRuntime-watchdog");
        watchdog.setDaemon(true);
        watchdog.start();
    }

    private static boolean isResponse(String line) {
        return line.equals("OK")
                || line.startsWith("Removed ")
                || line.startsWith("Hook ")
                || line.equals("ERROR: Failed to remove hook")
                || line.equals("ERROR: Lua engine not initialized")
                || line.equals("ERROR: Lua execution failed")
                || line.equals("ERROR: hexexec requires hex-encoded Lua code")
                || line.equals("ERROR: malloc failed");
    }

    private static void close() {
        synchronized (CLOSE_LOCK) {
            WAITING_RESPONSE.set(false);
            RESPONSES.clear();
            LocalSocket s = socket;
            socket = null;
            reader = null;
            writer = null;
            sessionKey = null;
            readerThread = null;
            // No cerrar BufferedReader/OutputStream: su close() puede esperar
            // al readLine() en curso. shutdownInput() desbloquea al lector y
            // close() libera el descriptor.
            if (s != null) {
                try {
                    s.shutdownInput();
                } catch (IOException ignored) {
                }
                try {
                    s.shutdownOutput();
                } catch (IOException ignored) {
                }
                try {
                    s.close();
                } catch (IOException ignored) {
                }
            }
        }
    }

    private static File resolveFile(Context context, String path) {
        if (path == null || path.trim().isEmpty()) {
            return null;
        }
        String clean = path.trim();
        if (clean.startsWith("files/")) {
            clean = clean.substring("files/".length());
        }

        File file = new File(clean);
        if (file.isAbsolute()) {
            return file;
        }

        File internal = new File(context.getFilesDir(), clean);
        if (internal.isFile()) {
            return internal;
        }

        File externalDir = context.getExternalFilesDir(null);
        if (externalDir != null) {
            File external = new File(externalDir, clean);
            if (external.isFile()) {
                return external;
            }
        }
        return internal;
    }

    private static String readFile(File file) throws IOException {
        if (file.length() > MAX_SCRIPT_BYTES) {
            throw new IOException("script demasiado grande: " + file.length() + " bytes");
        }
        try (InputStream in = new FileInputStream(file);
             ByteArrayOutputStream out = new ByteArrayOutputStream((int) file.length())) {
            byte[] buffer = new byte[8192];
            int read;
            while ((read = in.read(buffer)) != -1) {
                out.write(buffer, 0, read);
            }
            return out.toString(StandardCharsets.UTF_8.name());
        }
    }

    private static String toHex(byte[] data) {
        char[] digits = "0123456789abcdef".toCharArray();
        char[] hex = new char[data.length * 2];
        for (int i = 0; i < data.length; i++) {
            int value = data[i] & 0xff;
            hex[i * 2] = digits[value >>> 4];
            hex[i * 2 + 1] = digits[value & 0x0f];
        }
        return new String(hex);
    }
}
