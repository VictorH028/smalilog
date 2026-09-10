package com.deadnote;

public final class RemoteLogger {

    private static boolean loaded = false;

    static {
        try {
            System.loadLibrary("logger");
            loaded = true;
        } catch (UnsatisfiedLinkError e) {
            // La app no debe cerrarse si la biblioteca no está disponible.
            loaded = false;
        }
    }

    private RemoteLogger() {
        // Evita crear instancias.
    }

    public static native void nativeSendLog(
            String level,
            String tag,
            String message
    );

    public static void d(String tag, String msg) {
        send("DEBUG", tag, msg);
    }

    public static void e(String tag, String msg) {
        send("ERROR", tag, msg);
    }

    private static void send(String level, String tag, String msg) {
        if (!loaded) {
            return;
        }

        try {
            nativeSendLog(level, tag, msg);
        } catch (Throwable ignored) {
            // El logger nunca debe tumbar la aplicación.
        }
    }
}
