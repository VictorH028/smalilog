> Clase de la app de prueba `build_payloads`; no forma parte del paquete Python.

# Intesectar todas las clases de carga 

TracingClassLoader es una clase personalizada que extiende el ClassLoader estándar de Java. Su propósito principal es interceptar, auditar y registrar (loguear) la carga dinámica de clases en tiempo de ejecución (runtime), identificando exactamente qué componente o línea de código está solicitando cada clase.

# Uso

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
