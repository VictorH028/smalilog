package com.deadnote;

import android.content.Context;
import android.util.Log;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class CatchError implements Thread.UncaughtExceptionHandler {

    private static final String TAG = "APK_CRASH_CATCHER";
    private final Thread.UncaughtExceptionHandler defaultHandler;
    private final Context context;

    // Constructor privado
    private CatchError(Context context, Thread.UncaughtExceptionHandler defaultHandler) {
        this.context = context.getApplicationContext();
        this.defaultHandler = defaultHandler;
    }

    /**
     * Método estático sencillo para llamar directamente desde Smali
     */
    public static void init(Context context) {
        if (context == null) return;
        
        Thread.UncaughtExceptionHandler currentHandler = Thread.getDefaultUncaughtExceptionHandler();
        
        // Evitar doble inicialización
        if (!(currentHandler instanceof CatchError)) {
            CatchError customLogger = new CatchError(context, currentHandler);
            Thread.setDefaultUncaughtExceptionHandler(customLogger);
            RemoteLogger.d(TAG, "CatchError registrado correctamente.");
        }
    }

    @Override
    public void uncaughtException(Thread thread, Throwable throwable) {
        try {
            // 1. Convertir la excepción a String (Stacktrace)
            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            throwable.printStackTrace(pw);
            String stackTrace = sw.toString();

            // 2. Formatear el reporte de error
            String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss", Locale.US).format(new Date());
            String logMessage = "=== CRASH DETECTADO ===\n" +
                    "Fecha: " + timestamp + "\n" +
                    "Hilo: " + thread.getName() + " (ID: " + thread.getId() + ")\n" +
                    "Excepción: " + throwable.getClass().getName() + "\n" +
                    "Mensaje: " + throwable.getMessage() + "\n" +
                    "Stacktrace:\n" + stackTrace + "\n";

            // 3. Imprimir directamente en Logcat (Nivel ERROR)
            android.util.Log.e(TAG, logMessage);

            // 4. Guardar archivo en /data/data/<package_name>/files/crash_logs/
            saveToFile(timestamp, logMessage);

        } catch (Exception e) {
            RemoteLogger.d(TAG, "Error al guardar el crash log" );// +  e.toString() );
        } finally {
            // 5. Delegar al manejador original de Android para terminar el proceso de forma limpia
            if (defaultHandler != null) {
                defaultHandler.uncaughtException(thread, throwable);
            }
        }
    }

    private void saveToFile(String timestamp, String content) {
        try {
            File logDir = new File(context.getFilesDir(), "crash_logs");
            if (!logDir.exists()) {
                logDir.mkdirs();
            }
            File logFile = new File(logDir, "crash_" + timestamp + ".txt");
            FileWriter writer = new FileWriter(logFile);
            writer.write(content);
            writer.close();
            RemoteLogger.d(TAG, "Log guardado en: " + logFile.getAbsolutePath());
        } catch (Exception e) {
            RemoteLogger.d(TAG, "No se pudo escribir el archivo de log");  //, e);
        }
    }
}

