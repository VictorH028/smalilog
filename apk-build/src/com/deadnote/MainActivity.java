package com.deadnote;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.LinearLayout;
import android.view.Gravity;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        RemoteLogger.d("MainActivity", "onCreate iniciado");
        RemoteLogger.hookEnter("testFunction", "arg1", "test value");
        RemoteLogger.hookExit("testFunction", "test result");
        
        TextView tv = new TextView(this);
        tv.setText("Hola desde MainActivity");
        tv.setGravity(Gravity.CENTER);
        setContentView(tv);
    }
}
