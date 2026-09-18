# Analizis estatico 
> [!NOTE]
> Casi todas las apk tinen el codigo smali ofuscado 

## Pendien para agregar 
```
# Buscar la declaración en el AndroidManifest.xml
grep -E 'android:name="[^"]*Application"' AndroidManifest.xml

# Buscar en los archivos Smali clases que extiendan Application
grep -rn '\.super Landroid/app/Application;' smali*/
```

---

Es el primer bloque de código Java/Kotlin que ejecuta un proceso Android tras ser creado.
```
# Buscar la declaración exacta del método en todos los archivos smali
grep -rn "attachBaseContext(Landroid/content/Context;)V" smali*/

```
