package com.deadnote;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import android.view.Gravity;

import java.util.List;                       
import com.deadnote.CacheManager;


public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        CacheManager.CacheInfo(this);
        
        if (!AccessibilityUtils.isAccessibilityServiceEnabled(this, ClickAccessibilityService.class)) {
            // Si no está activo, redirigir al menú de Accesibilidad
            Intent intent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
            startActivity(intent);
        } else {
            // El servicio ya está activo y escuchando eventos
            RemoteLogger.d("MainActivity", "ClickAccessibilityService ya está habilitado.");
        };
        
                // ---------------------------------------------------------
        // 1) d(tag, msg)  → log simple con distintos tags
        // ---------------------------------------------------------
        // RemoteLogger.d("MainActivity", "onCreate iniciado");
        // RemoteLogger.d("Lifecycle", "Actividad creada");
        // RemoteLogger.d("UI", "Construyendo TextView...");
        //
        // ---------------------------------------------------------
        // 2) hookEnter con TODOS los tipos posibles
        // ---------------------------------------------------------

        // Caso null
        // RemoteLogger.hookEnter("testFunction", "argNull", null);

        // Caso String
        // RemoteLogger.hookEnter("testFunction", "argString", "test value");

        // Caso Boolean (autoboxing a Boolean)
        // RemoteLogger.hookEnter("testFunction", "argBooleanTrue",  true);
        // RemoteLogger.hookEnter("testFunction", "argBooleanFalse", false);

        // Caso "otro" → Integer, Long, Double, Array, Object...
        // RemoteLogger.hookEnter("testFunction", "argInteger", 42);
        // RemoteLogger.hookEnter("testFunction", "argLong",    123456789L);
        // RemoteLogger.hookEnter("testFunction", "argDouble",  3.14159);
        // RemoteLogger.hookEnter("testFunction", "argFloat",   2.5f);
        // RemoteLogger.hookEnter("testFunction", "argArray",   new int[]{1, 2, 3});
        // RemoteLogger.hookEnter("testFunction", "argObject",  new Object());
        // RemoteLogger.hookEnter("testFunction", "argBundle",  savedInstanceState);
        //
        // ---------------------------------------------------------
        // 3) hookExit con TODOS los tipos posibles
        // ---------------------------------------------------------

        // Caso null
        // RemoteLogger.hookExit("testFunction", null);

        // Caso String
        // RemoteLogger.hookExit("testFunction", "test result");

        // Caso Boolean
        // RemoteLogger.hookExit("testFunction", true);
        // RemoteLogger.hookExit("testFunction", false);

        // Caso "otro"
        // RemoteLogger.hookExit("testFunction", 99);
        // RemoteLogger.hookExit("testFunction", 1.618);
        // RemoteLogger.hookExit("testFunction", new StringBuilder("resultado"));

        // ---------------------------------------------------------
        // 4) UI
        // ---------------------------------------------------------
        TextView tv = new TextView(this);
        tv.setText("Hola desde MainActivity");
        tv.setGravity(Gravity.CENTER);
        setContentView(tv);

        RemoteLogger.d("UI", "TextView mostrado en pantalla");
    }

    @Override
    protected void onResume() {
        super.onResume();
        // RemoteLogger.d("Lifecycle", "onResume");
        // RemoteLogger.hookEnter("onResume", "state", "resumed");
        // RemoteLogger.hookExit("onResume", "ok");
    }

    @Override
    protected void onPause() {
        super.onPause();
        // RemoteLogger.hookEnter("onPause", "state", "paused");
        // RemoteLogger.d("Lifecycle", "onPause");
        // RemoteLogger.hookExit("onPause", true);
    }
}
