# Instala el paquete localmente en modo editable
pip install -e .

# Verifica que el CLI reconoce los módulos
python -c "import smalilog; print(smalilog.__file__)"


invoke-static {p0}, Lcom/deadnote/LifecycleTracker;->init(Landroid/app/Application;)V

Puntos clave:
​Ubicación: Se coloca tras invoke-super {p0}, Ltc0/i;->onCreate()V para garantizar que el contexto base de la aplicación esté completamente inicializado por Hilt/Android.  
​Parámetro p0: p0 hace referencia a this (la instancia de CrunchyrollApplication), la cual hereda de android.app.Application y se pasa a LifecycleTracker.init().


# Ideas para agregar 

- DCL  -> Buscar 

> [!NOTE]
> No intalar desede pip3 da error sique los pasos de la wep 
- [androguard](https://androguard.github.io/androguard/contributing.html)

Se intala bien pero `cryptography` falla aunque se intale. 

Solucion usar la vercion de termux 
```
apt install python-cryptography
```

Verificar la ruta de el venv 

```
poetry env info --path
```
---
# Pendiente 
- Monitoreo de trafico (Chucker)
-  https://docs.oracle.com/en/java/javase/21/docs/specs/jni/invocation.html#jni_onload 
- Cambiar la logica que la aplicación sea el servidor 


Hacer que la .so carge configuracion informacion tomada del proyecto de frida 
```
    {
  "interaction": {
    "type": "listen",
    "address": "127.0.0.1",
    "port": 9999,
    "on_load": "wait"
  }
}
```

Qué significa:

· type: "listen": El Gadget se queda escuchando en un puerto TCP local.
· port: 27042: Puerto por defecto de Frida.
· on_load: "wait": Bloquea la app hasta que te conectes. Ideal para instrumentar antes de que corra el código.

- 
Esto es pra auto Backup manda la informacion a Google Drive 
> [!NOTE]
> Tener esto es cuenta para explotar 
```
<application
    android:allowBackup="true"
    android:fullBackupContent="@xml/backup_rules">
```


# Git revisar despues

- [document-api](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/document-api) 


# Mejoras 

Un `AccessibilityService` puede observar todos los clicks de la app sin tocar el código. Solo necesitas:

- Hay que activar el servisio en los ajustes 



```xml
<service
    android:name=".ClickAccessibilityService"
    android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">
    <intent-filter>
        <action android:name="android.accessibilityservice.AccessibilityService"/>
    </intent-filter>
    <meta-data
        android:name="android.accessibilityservice"
        android:resource="@xml/accessibility_config"/>
</service>
```

Archivo de configuracion (res/xml/accessibility_config.xml)

```
<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeViewClicked"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagDefault"
    android:canRetrieveWindowContent="true"
    android:notificationTimeout="100" />

```

```java
public class ClickAccessibilityService extends AccessibilityService {
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_VIEW_CLICKED) {
            CharSequence text = event.getText().isEmpty() ? "" : event.getText().get(0);
            String msg = "CLICK → " + event.getClassName()
                       + " | texto=" + text
                       + " | package=" + event.getPackageName();
            Log.d("ClickTracker", msg);
        }
    }
    @Override
    public void onInterrupt() {
        // Requerido por la clase abstracta AccessibilityService
    }
}
```


