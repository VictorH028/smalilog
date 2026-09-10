
# Todo echo desde termux 

1) - Pasar la libreria a la app objetivo 

2) - Pasar el ==dex== para poder cargar la linbreria y usar sus metodos 

Flujo 
Smali → Java → JNI → servidor.


### Archivos 

[RemoteLogger](url) contiene el codigo  java que se utiliza despues a nivel de smali 

*Metodos*  
- d(string,strin)
- hookEnter()
- hookExit() 

[log_server.py](url) Quin resive la conexión desde la libreria

>> Pendiente
> [] - Mejorar la conexión

[native_logger](url) Encargada de la comunicasion con el servidor

>> Pendiente
> 

# Uso


- lib 
- dex-inj

Pasar el contenido a la apk objetivo  

```java
public int miFuncion(String a) {
    RemoteLogger.hookEnter("miFuncion", "a", a);
    int r = /* ... */;
    RemoteLogger.hookExit("miFuncion", r);
    return r;
}
```

Usar `d(...)` solo para log sueltos de depuracion 


### Representacion en smali 

> [!NOTE]
> Para evitar conflictos en el codigo hay que manipular bien los registros 

```smali
    const-string p1, "Network"

    const-string v0, "Conexión desde onCreat"

    invoke-static {p1, v0}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V
```


```smali
# ========== HOOK ENTER ==========
    const-string v0, "decodeBytesNative"    # function name
    const-string v1, "input"                # argument name
    move-object v2, p1                      # argument value (byte[])
    invoke-static {v0, v1, v2}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V
    # =================================
```

```smali 
    # ========== HOOK EXIT ==========
    const-string v0, "decodeBytesNative"    # function name
    move-object v1, v3                      # result
    invoke-static {v0, v1}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
    # ================================
```


# Compilacion de la lib 

```bash 
aarch64-linux-android-clang -shared -fPIC -O2 -fno-exceptions -fno-rtti -o liblogger.so native_logger.c -I/usr/lib/jvm/java-8-openjdk-amd64/include -I/usr/lib/jvm/java-8-openjdk-amd64/include/linux
```

# Comprobacion basica 

> Solo pueden estar estas 2 

```
readelf -d liblogger.so | grep NEEDED
  0x0000000000000001 (NEEDED)       Shared library: [libdl.so]
  0x0000000000000001 (NEEDED)       Shared library: [libc.so]
```
