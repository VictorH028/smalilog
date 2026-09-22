package com.deadnote;

import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;

public final class HttpClientProvider {

    private static volatile OkHttpClient INSTANCE;

    private HttpClientProvider() {}

    public static OkHttpClient get() {
        if (INSTANCE == null) {
            synchronized (HttpClientProvider.class) {
                if (INSTANCE == null) INSTANCE = build();
            }
        }
        return INSTANCE;
    }

    private static OkHttpClient build() {

        // Loguea TODO: request + response + body completo
        HttpLoggingInterceptor logging = new HttpLoggingInterceptor(message ->
                RemoteLogger.d("Traffic", message)
        );
        logging.setLevel(HttpLoggingInterceptor.Level.BODY);

        return new OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .addInterceptor(logging)
                .build();
    }
}
