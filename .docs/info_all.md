# Analizis estatico 
> [!NOTE]
> Casi todas las apk tinen el codigo smali ofuscado 

## Pendien para agregar 
```
# Buscar la declaración en el AndroidManifest.xml
grep -E 'android:name="[^"]*Application"' AndroidManifest.xml

# Buscar en los archivos Smali clases que extiendan Application
grep -rn '\.super Landroid/app/Application;' smali*/

# Buscar en clases que extiende Application ya que salen mucho y pueden ser del sistema  
grep -rn "\.super L.*Application;" smali*/ | cut -d: -f1 | xargs grep -rn "attachBaseContext"
```

---

Es el primer bloque de código Java/Kotlin que ejecuta un proceso Android tras ser creado.
```
# Buscar la declaración exacta del método en todos los archivos smali
grep -rn "attachBaseContext(Landroid/content/Context;)V" smali*/

```
--- 

# Detecciones

```
# Buscar carga de librerías nativas (.so) en onCreate
grep -rn "loadLibrary" smali*/

# Buscar comprobaciones de paquetes o archivos comunes de Root/Frida
grep -rn -E "su|magisk|frida|xposed" smali*/

```
*Buscar funciones definidas en las librias*
```
.method public static native
```
# Captuta de errorea 

[Code...](url) 
