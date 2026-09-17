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

import com.deadnote.RemoteLogger;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Contenedor principal vertical
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        layout.setPadding(32, 32, 32, 32);

        // Texto informativo
        TextView tv = new TextView(this);
        tv.setText("Panel de Control Deadnote");
        tv.setGravity(Gravity.CENTER);
        tv.setTextSize(18);

        // Botón de activación
        Button btnEnableService = new Button(this);
        btnEnableService.setText("Prueba 1");
        btnEnableService.setOnClickListener(v -> prueba1());

        // Agregar elementos al layout
        layout.addView(tv);
        layout.addView(btnEnableService);

        // Establecer el layout como vista principal
        setContentView(layout);

        RemoteLogger.d("MainActivity", "onCreate iniciado");
    }

    private void prueba1() {
        RemoteLogger.d("Botton1", "Hola"); 
    }

    @Override
    protected void onResume() {
        super.onResume();
        RemoteLogger.d("Lifecycle", "onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        RemoteLogger.d("Lifecycle", "onPause");
    }
}

