> Clase de la app de prueba `build_payloads`; no forma parte del paquete Python.

# 📱 Rastrear Ciclo de Vida de Pantallas (`LifecycleTracker.java`)

`LifecycleTracker` es una clase auxiliar que se engancha a las llamadas del ciclo de vida de Android (`ActivityLifecycleCallbacks`) para registrar automáticamente cuando una actividad pasa al primer plano, sin requerir cambios en cada pantalla de la app.

---

### API de `LifecycleTracker`

| Método | Descripción |
| :--- | :--- |
| `LifecycleTracker.init(Application app)` | Registra el tracker en la aplicación. Debe invocarse una sola vez en el `onCreate()` de la clase `Application`. |

---

### Ejemplo de Integración

```java
package com.deadnote;

import android.app.Application;

public class MyApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();

        // 1. Configurar servidor de logs
        RemoteLog.configure("127.0.0.1", 9999);

        // 2. Activar el seguimiento automático de actividades
        LifecycleTracker.init(this);
    }
}
```
**Garantías de Seguridad**
- Totalmente Fail-Safe: Si la referencia a la Activity es nula o la invocación a `getClass()` falla por cualquier inconsistencia del entorno Android, la excepción es absorbida en silencio.
- Protección contra nulos en `init()`: Si `LifecycleTracker.init(null)` es llamado por error, la llamada se ignora sin lanzar `NullPointerException`.
- Sin huella de memoria: Utiliza una única instancia interna en el registro de callbacks sin retener referencias fuertes a contextos de actividades (Context leaks).


