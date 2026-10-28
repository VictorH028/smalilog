package com.deadnote;

import java.util.Arrays;

public class TracingClassLoader extends ClassLoader {

    private static final String TAG = "TracingCL";

    public TracingClassLoader(ClassLoader parent) {
        super(parent);
    }

    @Override
    protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
        // Ignoramos clases del sistema para no inundar el log
        if (name.startsWith("java.") || name.startsWith("android.") || name.startsWith("kotlin.")) {
            return super.loadClass(name, resolve);
        }

        // Capturamos quién pide la clase en runtime
        StackTraceElement[] stack = new Throwable().getStackTrace();
        String caller = stack.length > 1 ? stack[1].toString() : "desconocido";

        RemoteLog.i(TAG, "loadClass: " + name + " | solicitado por: " + caller);

        try {
            Class<?> clazz = super.loadClass(name, resolve);
            RemoteLog.d(TAG, "Clase cargada OK: " + clazz.getName()
                    + " | loader=" + clazz.getClassLoader());
            return clazz;
        } catch (ClassNotFoundException e) {
            RemoteLog.e(TAG, "Fallo al cargar: " + name);
            throw e;
        }
    }
}
