package com.deadnote;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;
import android.os.Handler;
import android.os.Looper;

public class ReceptorTermux extends BroadcastReceiver {

    private static final String TAG = "ReceptorTermux";
    public static final String ACTION = "com.deadnote.ACCION_DESDE_TERMUX";

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent == null || !ACTION.equals(intent.getAction()))
            return;

        String orden = intent.getStringExtra("orden");
        String arg1 = intent.getStringExtra("arg1");
        String arg2 = intent.getStringExtra("arg2");

        RemoteLog.d(TAG, "Orden recibida: " + orden + " | arg1=" + arg1 + " | arg2=" + arg2);
        if (orden == null)
            return;

        switch (orden) {

            case "TOAST":
                mostrarToast(context, arg1 != null ? arg1 : "Hola desde Termux");
                break;

            case "ABRIR_APP":
                abrirMainActivity(context);
                break;

            case "CLICK_COORDENADAS":
                // arg1 = x, arg2 = y -> usa el AccessibilityService
                try {
                    int x = Integer.parseInt(arg1);
                    int y = Integer.parseInt(arg2);
                    ClickAccessibilityService.realizarClick(x, y);
                } catch (Exception e) {
                    RemoteLog.e(TAG, "Coordenadas inválidas" + e.getMessage());
                }
                break;

            case "VOLVER":
                ClickAccessibilityService.pulsarVolver();
                break;

            case "HOME":
                ClickAccessibilityService.pulsarHome();
                break;

            case "RECIENTES":
                ClickAccessibilityService.pulsarRecientes();
                break;

            case "ABRIR_URL":
                abrirUrl(context, arg1);
                break;

            case "GUARDAR_LOG":
                guardarLog(context, arg1);
                break;

            default:
                RemoteLog.w(TAG, "Orden desconocida: " + orden);
        }
    }

    // ---------- Funciones de ejemplo ----------

    private void mostrarToast(Context ctx, String texto) {
        new Handler(Looper.getMainLooper())
                .post(() -> Toast.makeText(ctx.getApplicationContext(), texto, Toast.LENGTH_SHORT).show());
    }

    private void abrirMainActivity(Context ctx) {
        Intent i = new Intent(ctx, MainActivity.class);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        ctx.startActivity(i);
    }

    private void abrirUrl(Context ctx, String url) {
        if (url == null)
            return;
        try {
            Intent i = new Intent(Intent.ACTION_VIEW, android.net.Uri.parse(url));
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            ctx.startActivity(i);
        } catch (Exception e) {
            RemoteLog.e(TAG, "No se pudo abrir URL" + e.getMessage());
        }
    }

    private void guardarLog(Context ctx, String texto) {
        if (texto == null)
            return;
        try {
            java.io.File f = new java.io.File(ctx.getFilesDir(), "ordenes.log");
            try (java.io.FileOutputStream fos = new java.io.FileOutputStream(f, true)) {
                fos.write((System.currentTimeMillis() + " -> " + texto + "\n").getBytes());
            }
            RemoteLog.d(TAG, "Log guardado en " + f.getAbsolutePath());
        } catch (Exception e) {
            RemoteLog.e(TAG, "Error guardando log" + e.getMessage());
        }
    }
}
