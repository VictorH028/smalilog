package com.deadnote;

import android.app.Activity;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.TextView;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        new Thread(() -> {
            try {
                OkHttpClient client = HttpClientProvider.get();

                Request request = new Request.Builder()
                        .url("https://httpbin.org/ip")
                        .build();

                Response response = client.newCall(request).execute();
                String body = response.body().string();

                RemoteLogger.d("NetResult", "Respuesta: " + body);

            } catch (Exception e) {
                RemoteLogger.d("NetError", "Error: " + e);
            }
        }).start();

        TextView tv = new TextView(this);
        tv.setText("Tráfico vía SOCKS5 + RemoteLogger");
        tv.setGravity(Gravity.CENTER);
        setContentView(tv);
    }
}
