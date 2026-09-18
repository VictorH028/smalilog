# Instala el paquete localmente en modo editable
pip install -e .

# Verifica que el CLI reconoce los módulos
python -c "import smalilog; print(smalilog.__file__)"


invoke-static {p0}, Lcom/deadnote/LifecycleTracker;->init(Landroid/app/Application;)V

Puntos clave:
​Ubicación: Se coloca tras invoke-super {p0}, Ltc0/i;->onCreate()V para garantizar que el contexto base de la aplicación esté completamente inicializado por Hilt/Android.  
​Parámetro p0: p0 hace referencia a this (la instancia de CrunchyrollApplication), la cual hereda de android.app.Application y se pasa a LifecycleTracker.init().


# 

¿Qué es attachBaseContext()?

attachBaseContext() es un método del ciclo de vida de Android que se ejecuta antes que onCreate() tanto en Application como en Activity y Service. Su propósito es inyectar el Context base en el componente antes de que empiece a funcionar.

📌 Orden de ejecución

En una Application:

```
1. Constructor()                    ← se instancia la clase
2. attachBaseContext(Context)       ← se le asigna el Context base
3. onCreate()                       ← inicialización real
```

En una Activity:

```
1. Constructor()
2. attachBaseContext(Context)       ← se le asigna el Context base
3. onCreate()
4. onStart()
5. onResume()
```

attachBaseContext() siempre va primero. Es el primer método que recibe un Context válido.

🧠 ¿Para qué sirve?

El Context que recibe es el Context base de la aplicación (no el Context de la Activity, sino el global). A partir de él, el componente puede:

· Acceder a recursos (getResources(), getAssets()).
· Acceder a SharedPreferences.
· Acceder a servicios del sistema (getSystemService()).
· Crear otros Contexts derivados (createConfigurationContext(), etc.).

Sin attachBaseContext(), el componente no tiene Context y no puede hacer nada.


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

- 
