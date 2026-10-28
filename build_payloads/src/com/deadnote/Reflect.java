package com.deadnote;

import java.lang.reflect.Method;
import java.util.Arrays;

public final class Reflect {

    private Reflect() {}

    public static Class<?> forName(String name) throws ClassNotFoundException {
        RemoteLog.i("Reflect", "Class.forName -> \"" + name + "\"");
        RemoteLog.i("Reflect", "Caller: " + Thread.currentThread().getStackTrace()[2]);
        return Class.forName(name);
    }

    public static Object invoke(Method m, Object target, Object... args) throws Exception {
        RemoteLog.i("Reflect", "Method.invoke -> "
                + m.getDeclaringClass().getName() + "." + m.getName()
                + " args=" + Arrays.toString(args));
        Object r = m.invoke(target, args);
        RemoteLog.i("Reflect", "invoke resultado: " + r);
        return r;
    }
}
