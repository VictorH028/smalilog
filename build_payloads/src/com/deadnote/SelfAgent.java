package com.deadnote;

import java.lang.instrument.Instrumentation;
import java.lang.instrument.ClassFileTransformer;
import java.security.ProtectionDomain;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class SelfAgent {

    public static void premain(String args, Instrumentation inst) {
        RemoteLog.i("[AGENT]", "Instrumentación activa con RemoteLog");
        RemoteLog.i("SelfAgent", "Agente Java cargado correctamente mediante premain");

        if (inst != null) {
            inst.addTransformer(new ClassFileTransformer() {
                @Override
                public byte[] transform(ClassLoader loader, String className,
                        Class<?> classBeingRedefined,
                        ProtectionDomain pd, byte[] classfileBuffer) {

                    if (className != null && className.contains("MiClaseOfuscada")) {
                        RemoteLog.i("[AGENT]", "Transformando clase objetivo: " + className);
                        RemoteLog.w("SelfAgent", "Clase detectada y lista para inyección: " + className);
                    }
                    return null;
                }
            });
        } else {
            RemoteLog.w("SelfAgent", "Instrumentation nula (ejecutándose en entorno Android estándar)");
        }
    }

}
