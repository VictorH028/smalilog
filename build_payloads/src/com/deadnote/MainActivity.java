package com.deadnote;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.view.Gravity;

import java.util.Arrays;
import java.util.List;

public class MainActivity extends Activity {

    private String descifrarNombreClase() {
        // Nombre real de una clase tuya, ofuscado en Base64
        // "com.deadnote.Backup" en Base64:
        String cifrado = "Y29tLmRlYWRub3RlLkJhY2t1cA==";
        byte[] decoded = android.util.Base64.decode(cifrado, android.util.Base64.DEFAULT);
        return new String(decoded);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        LifecycleTracker.init(this);

        // Contenedor principal vertical
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        layout.setPadding(32, 32, 32, 32);

        // Texto informativo
        TextView tv = new TextView(this);
        tv.setText("Panel de Control");
        tv.setGravity(Gravity.CENTER);
        tv.setTextSize(18);

        // Botón de activación
        Button btnEnableService = new Button(this);
        btnEnableService.setText("Backup");
        btnEnableService.setOnClickListener(v -> backup());

        Button btnv1 = new Button(this);
        btnv1.setText("prueba1");
        btnv1.setOnClickListener(v -> prueba1());

        Button btnTestAgent = new Button(this);
        btnTestAgent.setText("Probar Agente");
        btnTestAgent.setOnClickListener(v -> probarAgente());
        layout.addView(btnTestAgent);

        // Agregar elementos al layout
        layout.addView(btnv1);
        layout.addView(btnEnableService);

        // Establecer el layout como vista principal
        setContentView(layout);

        RemoteLog.d("MainActivity", "onCreate iniciado");
    }

    private void backup() {
        RemoteLog.i("backup", "Backup");
        Backup.init(this);
    }

    private void prueba1() {
        RemoteLog.d("bot", "Prueba de botón pulsada");

        // Valores usados por el ejemplo de smalilog renef (docs/renef.md):
        // el script puede convertir el retorno en false / "parcheado".
        RemoteLog.d("RenefDemo", "demoRenefCheck=" + demoRenefCheck());
        RemoteLog.d("RenefDemo", "demoRenefLabel=" + demoRenefLabel());

        // Puedes probar trazas o listas para ver la serialización en acción:
        List<String> items = Arrays.asList("Elemento 1", "Elemento 2", "Elemento 3");
        RemoteLog.logList("TestList", items);
    }

    private boolean demoRenefCheck() {
        return true;
    }

    private String demoRenefLabel() {
        return "original";
    }

    private void probarAgente() {
        RemoteLog.d("MainActivity", "Botón 'Probar Agente' pulsado");
        try {
            // Caso real: cargar clase dinámica y trazar todo
            TracingClassLoader loader = new TracingClassLoader(getClassLoader());
            String nombre = descifrarNombreClase();
            Class<?> clazz = loader.loadClass(nombre);

            RemoteLog.i("MainActivity", "Clase real cargada: " + clazz.getName());
            RemoteLog.i("MainActivity", "Loader: " + clazz.getClassLoader());
            RemoteLog.i("MainActivity", "Métodos: " +
                    java.util.Arrays.toString(clazz.getDeclaredMethods()));

        } catch (Throwable t) {
            RemoteLog.e("MainActivity", "Error real: " + t);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        RemoteLog.d("Lifecycle", "onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        RemoteLog.d("Lifecycle", "onPause");
    }
}
