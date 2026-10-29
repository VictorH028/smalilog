package com.smalilog.agent;

import android.util.Log;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadFactory;

public final class AgentLog {

    private static final String TAG = "SmalilogAgent";
    private static final ExecutorService POOL = Executors.newSingleThreadExecutor(new ThreadFactory() {
        @Override
        public Thread newThread(Runnable runnable) {
            Thread thread = new Thread(runnable, "SmalilogAgentLog");
            thread.setDaemon(true);
            return thread;
        }
    });

    private static volatile String host = "127.0.0.1";
    private static volatile int port = 9999;

    private AgentLog() {
    }

    public static void configure(String newHost, int newPort) {
        if (newHost != null && !newHost.trim().isEmpty()) {
            host = newHost.trim();
        }
        if (newPort > 0 && newPort <= 65535) {
            port = newPort;
        }
    }

    public static void i(String message) {
        Log.i(TAG, message);
        send("INFO", message);
    }

    public static void w(String message) {
        Log.w(TAG, message);
        send("WARN", message);
    }

    public static void e(String message) {
        Log.e(TAG, message);
        send("ERROR", message);
    }

    private static void send(final String level, final String message) {
        if (message == null) {
            return;
        }
        try {
            POOL.execute(new Runnable() {
                @Override
                public void run() {
                    post(level, message);
                }
            });
        } catch (Throwable ignored) {
        }
    }

    private static void post(String level, String message) {
        HttpURLConnection connection = null;
        try {
            URL url = new URL("http://" + host + ":" + port + "/log");
            connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(1200);
            connection.setReadTimeout(1200);
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            byte[] body = ("{\"level\":" + quote(level)
                    + ",\"tag\":\"SmalilogAgent\",\"message\":" + quote(message) + "}")
                    .getBytes(StandardCharsets.UTF_8);
            connection.setFixedLengthStreamingMode(body.length);
            try (OutputStream out = connection.getOutputStream()) {
                out.write(body);
            }
            connection.getResponseCode();
        } catch (Throwable ignored) {
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

    private static String quote(String value) {
        StringBuilder out = new StringBuilder(value.length() + 2);
        out.append('"');
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            switch (c) {
                case '"':
                    out.append("\\\"");
                    break;
                case '\\':
                    out.append("\\\\");
                    break;
                case '\n':
                    out.append("\\n");
                    break;
                case '\r':
                    out.append("\\r");
                    break;
                case '\t':
                    out.append("\\t");
                    break;
                default:
                    if (c < 0x20) {
                        out.append(String.format("\\u%04x", (int) c));
                    } else {
                        out.append(c);
                    }
            }
        }
        out.append('"');
        return out.toString();
    }
}
