 package com.deadnote;

public final class RemoteLogger {
    private static boolean loaded = false;
    private static final String TAG_ACTIVITY = "SMALILOG_ACTIVITY";
    static {
        try {
            System.loadLibrary("logger");
            loaded = true;
        } catch (UnsatisfiedLinkError e) {
            loaded = false;
        }
    }

    public static void hookEnter(String function, String argName, Object arg) {
        if (!loaded) return;

        String value;
        if (arg == null) {
            value = "null";
        } else if (arg instanceof Boolean) {
            value = "Boolean: " + arg;
        } else if (arg instanceof String) {
            value = "String: " + arg;
        } else {
            value = arg.getClass().getSimpleName() + ": " + arg.toString();
        }

        nativeSendLog("DEBUG", "HOOK_ENTER", 
            function + " | " + argName + " | " + value);
    }

    public static void hookExit(String function, Object result) {
        if (!loaded) return;

        String value;
        if (result == null) {
            value = "null";
        } else if (result instanceof Boolean) {
            value = "Boolean: " + result;
        } else if (result instanceof String) {
            value = "String: " + result;
        } else {
            value = result.getClass().getSimpleName() + ": " + result.toString();
        }

        nativeSendLog("DEBUG", "HOOK_EXIT", 
            function + " | result | " + value);
    }

   
    public static void d(String tag, String msg) {
        if (!loaded) return;
        String level = TAG_ACTIVITY.equals(tag) ? "INFO" : "DEBUG";
        nativeSendLog(level, tag, msg);
    }

    private static native void nativeSendLog(String level, String tag, String msg);
}
