package com.deadnote;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.graphics.Path;
import android.view.accessibility.AccessibilityEvent;
import android.util.Log;

public class ClickAccessibilityService extends AccessibilityService {

    private static final String TAG = "ClickA11y";
    private static ClickAccessibilityService instancia;

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        instancia = this;
        Log.d(TAG, "Servicio de accesibilidad conectado");
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        /* no-op */ }

    @Override
    public void onInterrupt() {
        /* no-op */ }

    @Override
    public void onDestroy() {
        super.onDestroy();
        instancia = null;
    }

    // ---------- API estática usada por el receptor ----------

    public static void realizarClick(int x, int y) {
        if (instancia == null) {
            Log.w(TAG, "Servicio no activo");
            return;
        }

        Path path = new Path();
        path.moveTo(x, y);

        GestureDescription.StrokeDescription stroke = new GestureDescription.StrokeDescription(path, 0, 50);

        GestureDescription gesture = new GestureDescription.Builder()
                .addStroke(stroke)
                .build();

        instancia.dispatchGesture(gesture, null, null);
    }

    public static void pulsarVolver() {
        if (instancia != null)
            instancia.performGlobalAction(GLOBAL_ACTION_BACK);
    }

    public static void pulsarHome() {
        if (instancia != null)
            instancia.performGlobalAction(GLOBAL_ACTION_HOME);
    }

    public static void pulsarRecientes() {
        if (instancia != null)
            instancia.performGlobalAction(GLOBAL_ACTION_RECENTS);
    }
}
