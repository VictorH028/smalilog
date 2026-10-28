> **Material histórico.** No es documentación vigente; consulta [../README.md](../README.md).

Sí, se puede hacer dentro de la propia aplicación Java, sin Frida ni herramientas externas. La técnica se llama auto-instrumentación (self-instrumentation) o auto-hooking, y funciona porque en Java puedes interceptar llamadas a métodos de reflexión antes de que ocurran, siempre que controles el punto de entrada.

La idea clave: no puedes "hookear" Class.forName directamente (es un método nativo estático), pero sí puedes:

1. Envolver las llamadas en tu propio wrapper y registrar los valores.
2. Usar un ClassLoader personalizado que registre cada clase cargada.
3. Usar Instrumentation (java.lang.instrument) con un premain o agentmain para transformar bytecode.
4. Usar un SecurityManager (obsoleto en Java 17+, pero funcional en versiones anteriores) para interceptar reflexión.

1. Wrapper propio (lo más simple y didáctico)

Si tú controlas el código donde se llama a la reflexión, envuelves las llamadas y registras todo:

```java
import java.lang.reflect.Method;
import java.util.Arrays;

public class ReflectiveTracer {

    public static Class<?> tracedForName(String name) throws ClassNotFoundException {
        System.out.println("[TRACE] Class.forName llamado con: \"" + name + "\"");
        // Aquí ves la cadena EN CLARO, sin importar cómo se cifró antes
        Class<?> clazz = Class.forName(name);
        System.out.println("[TRACE] Clase cargada: " + clazz.getName());
        return clazz;
    }

    public static Object tracedInvoke(Method method, Object target, Object... args) throws Exception {
        System.out.println("[TRACE] Method.invoke -> " + method.getDeclaringClass().getName()
                + "." + method.getName() + " args=" + Arrays.toString(args));
        Object result = method.invoke(target, args);
        System.out.println("[TRACE] Resultado: " + result);
        return result;
    }

    public static void main(String[] args) throws Exception {
        // Simula código ofuscado que construye la cadena en runtime
        String parte1 = "java.lang.";
        String parte2 = "Runtime";
        String clase = parte1 + parte2;

        Class<?> clazz = tracedForName(clase);
        Method m = clazz.getMethod("getRuntime");
        Object runtime = tracedInvoke(m, null);

        System.out.println("Runtime obtenido: " + runtime);
    }
}
```

Salida:

```
[TRACE] Class.forName llamado con: "java.lang.Runtime"
[TRACE] Clase cargada: java.lang.Runtime
[TRACE] Method.invoke -> java.lang.Runtime.getRuntime args=[]
[TRACE] Resultado: java.lang.Runtime@...
```

Ventaja: ves la cadena en claro en el punto exacto donde se usa, sin importar cuántas capas de cifrado haya antes.

Limitación: solo funciona si tú controlas el código que llama. Si el código malicioso/ofuscado llama directamente a Class.forName, tu wrapper no se ejecuta.

2. ClassLoader personalizado (intercepta toda carga de clases)

Aquí ya no necesitas modificar el código que llama. Solo cambias el ClassLoader de la aplicación:

```java
public class TracingClassLoader extends ClassLoader {

    public TracingClassLoader(ClassLoader parent) {
        super(parent);
    }

    @Override
    protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
        // Se registra cada clase que se intenta cargar en runtime
        System.out.println("[CL] loadClass: " + name
                + " | hilo=" + Thread.currentThread().getName()
                + " | stack=" + Arrays.toString(
                    Arrays.stream(new Throwable().getStackTrace())
                          .limit(3).toArray()));

        return super.loadClass(name, resolve);
    }
}
```

Uso:

```java
public class App {
    public static void main(String[] args) throws Exception {
        TracingClassLoader tcl = new TracingClassLoader(
                App.class.getClassLoader());

        // Cargar una clase usando el loader trazador
        Class<?> clazz = tcl.loadClass("java.util.ArrayList");
        System.out.println("Cargada: " + clazz);
    }
}
```

Lo potente: el stack trace te dice quién está pidiendo la clase, o sea, desde qué método ofuscado se origina la petición.

3. java.lang.instrument (el "hook" real, sin herramientas externas)

Esta es la forma más cercana a lo que haría Frida, pero dentro de la propia JVM. Se puede usar en modo agentmain para auto-adjuntarse o premain si controlas el arranque.

3.1 Agente con premain

```java
import java.lang.instrument.Instrumentation;
import java.lang.instrument.ClassFileTransformer;
import java.security.ProtectionDomain;

public class SelfAgent {
    public static void premain(String args, Instrumentation inst) {
        System.out.println("[AGENT] Instrumentación activa");
        inst.addTransformer(new ClassFileTransformer() {
            @Override
            public byte[] transform(ClassLoader loader, String className,
                                    Class<?> classBeingRedefined,
                                    ProtectionDomain pd, byte[] classfileBuffer) {
                if (className != null && className.contains("MiClaseOfuscada")) {
                    System.out.println("[AGENT] Transformando: " + className);
                    // Aquí podrías inyectar bytecode que registre los argumentos
                }
                return null; // null = no modificar
            }
        });
    }
}
```

Empaquetas esto en un JAR con MANIFEST.MF:

```
Premain-Class: SelfAgent
Can-Retransform-Classes: true
```

Y arrancas tu app:

```bash
java -javaagent:agent.jar -jar miApp.jar
```

3.2 Auto-adjuntarse con agentmain (sin reiniciar)

Si la app ya está corriendo, puedes cargar el agente desde dentro:

```java
import com.sun.tools.attach.VirtualMachine;

public class AutoAttach {
    public static void main(String[] args) throws Exception {
        String pid = String.valueOf(ProcessHandle.current().pid());
        VirtualMachine vm = VirtualMachine.attach(pid);
        vm.loadAgent("/ruta/a/agent.jar");
        vm.detach();
    }
}
```

Nota: requiere el módulo jdk.attach y permisos; en entornos restringidos puede estar bloqueado.

4. SecurityManager (Java ≤ 17)

Antes de Java 17, SecurityManager permitía interceptar reflexión:

```java
System.setSecurityManager(new SecurityManager() {
    @Override
    public void checkPermission(Permission perm) {
        if (perm instanceof ReflectPermission) {
            System.out.println("[SEC] Reflexión detectada: " + perm);
            // Aquí ves el stack trace que originó la llamada
            new Throwable().printStackTrace();
        }
    }
});
```

En Java 17+ está deprecado para remoción y ya no intercepta todo, así que solo sirve en proyectos antiguos.

5. Ejemplo completo: ver datos en runtime sin herramientas externas

Combina wrapper + ClassLoader para un caso realista:

```java
public class AppConTrazas {

    static class TracingLoader extends ClassLoader {
        TracingLoader(ClassLoader p) { super(p); }

        @Override
        protected Class<?> loadClass(String name, boolean resolve)
                throws ClassNotFoundException {
            System.out.println("[LOAD] " + name
                + " desde " + Thread.currentThread().getStackTrace()[2]);
            return super.loadClass(name, resolve);
        }
    }

    public static void main(String[] args) throws Exception {
        TracingLoader loader = new TracingLoader(AppConTrazas.class.getClassLoader());

        // Simula código ofuscado que descifra en runtime
        String cifrado = "amF2YS5sYW5nLlJ1bnRpbWU="; // Base64
        String clase = new String(java.util.Base64.getDecoder().decode(cifrado));
        System.out.println("[DECODE] Cadena descifrada: " + clase);

        Class<?> clazz = loader.loadClass(clase);
        Method m = clazz.getMethod("getRuntime");
        Object rt = m.invoke(null);
        System.out.println("[RESULT] " + rt);
    }
}
```

Salida:

```
[DECODE] Cadena descifrada: java.lang.Runtime
[LOAD] java.lang.Runtime desde AppConTrazas.main(AppConTrazas.java:25)
[RESULT] java.lang.Runtime@...
```

Aquí ves la cadena descifrada y quién la pidió, todo dentro de la misma app Java.

Resumen: ¿qué técnica usar según tu caso?

Objetivo Técnica ¿Sin herramientas externas?
Ver valores en el punto de uso Wrapper propio Sí, si controlas el código
Ver toda clase cargada en runtime ClassLoader personalizado Sí
Interceptar sin tocar el código java.lang.instrument (premain/agentmain) Sí, con restricciones
Interceptar reflexión en Java ≤17 SecurityManager Sí, pero deprecado
Instrumentación completa tipo Frida Agente + bytecode manipulation (ASM, ByteBuddy) Sí, pero requiere setup

La respuesta corta: sí, se puede. La forma más limpia y "nativa Java" es java.lang.instrument con premain, porque intercepta a nivel de JVM sin necesidad de wrappers ni de tocar el código ofuscado. La forma más simple y didáctica es el wrapper + ClassLoader personalizado, que además te muestra el stack trace de quién pide cada dato en runtime.

¿Quieres que te arme un ejemplo completo y compilable de un agente premain que registre todas las llamadas a Class.forName y Method.invoke de una app cualquiera?
