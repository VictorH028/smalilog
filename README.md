
# Todo echo desde termux 

1) - Pasar la libreria a la app objetivo 

2) - Pasar el ==dex== para poder cargar la linbreria y usar sus metodos 

Flujo 
Smali → Java → JNI → servidor.


Metodos 

- d(string,strin)
- e(string,strin)
- hookEnter()
- 

> [!NOTE]
> ..... 

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
aarch64-linux-android-clang -shared -fPIC -std=c++17 -O2 -fno-exceptions -fno-rtti -o liblogger.so native_logger.cpp -I/usr/lib/jvm/java-8-openjdk-amd64/include -I/usr/lib/jvm/java-8-openjdk-amd64/include/linux
```

# Comprobacion basica 

> Solo pueden estar estas 2 

```
readelf -d liblogger.so | grep NEEDED
  0x0000000000000001 (NEEDED)       Shared library: [libdl.so]
  0x0000000000000001 (NEEDED)       Shared library: [libc.so]
```
