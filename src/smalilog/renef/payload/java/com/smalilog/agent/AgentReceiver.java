package com.smalilog.agent;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Process;

public class AgentReceiver extends BroadcastReceiver {

    public static final String ACTION = "com.smalilog.agent.ACTION";

    private static final boolean LOADED;
    private static final String LOAD_ERROR;

    static {
        boolean loaded = false;
        String error = null;
        try {
            System.loadLibrary("agent");
            loaded = true;
        } catch (Throwable t) {
            error = t.toString();
        }
        LOADED = loaded;
        LOAD_ERROR = error;
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent == null || !ACTION.equals(intent.getAction())) {
            return;
        }

        AgentLog.configure(intent.getStringExtra("host"), parseInt(intent.getStringExtra("port"), 0));
        final Context app = context.getApplicationContext();
        final String op = intent.getStringExtra("op");
        final String b64 = intent.getStringExtra("b64");
        final String name = intent.getStringExtra("name");

        final PendingResult pending = goAsync();
        Thread worker = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    handle(app, op, b64, name);
                } catch (Throwable t) {
                    AgentLog.e("Error en receptor: " + t);
                } finally {
                    pending.finish();
                }
            }
        }, "SmalilogAgentBroadcast");
        worker.setDaemon(true);
        worker.start();
    }

    private static void handle(Context context, String op, String b64, String name) {
        if (op == null) {
            AgentLog.w("Broadcast sin op");
            return;
        }
        if (!LOADED) {
            AgentLog.e("libagent.so no cargada: " + LOAD_ERROR);
            return;
        }

        AgentLog.i("op=" + op + " pid=" + Process.myPid());
        String result;
        if ("PING".equals(op)) {
            result = "OK: receptor activo (pid=" + Process.myPid() + ")";
        } else if ("STATUS".equals(op)) {
            result = AgentRuntime.status();
        } else if ("EXEC".equals(op) || "LUA_CODE".equals(op) || "LUA_B64".equals(op)) {
            result = AgentRuntime.execLuaBase64(b64);
        } else if ("PUSH".equals(op) || "LUA_PUSH".equals(op)) {
            result = AgentRuntime.saveLuaAndExec(context, name, b64);
        } else if ("UNHOOK".equals(op) || "LUA_UNHOOK".equals(op)) {
            result = AgentRuntime.unhookAll();
        } else if ("EXEC_FILE".equals(op) || "LUA".equals(op)) {
            result = AgentRuntime.execLuaFile(context, name);
        } else {
            result = "ERROR: operación desconocida: " + op;
        }
        AgentLog.i("resultado " + op + ": " + result);
    }

    private static int parseInt(String value, int fallback) {
        if (value == null) {
            return fallback;
        }
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            return fallback;
        }
    }
}
