
# Todo echo desde termux 

## Flujo 
Smali  → JNI → servidor.


### Archivos 

[RemoteLogger](url) contiene el codigo  java que se utiliza despues a nivel de smali 

*Metodos*  
- d(string,strin)
- hookEnter(...)
- hookExit(...) 

[log_server.py](url) Quien resive la conexión..

>> Pendiente
> [] - Crear una pagina 
> [] - Mejorar la conexión


[native_logger.os](url) Encargada de la comunicasion con el servidor

>> Pendiente
> 

# Uso

- lib 
- dex-inj

Pasar el contenido a la apk objetivo  

![alt text](path) 

![alt text](path) 

![alt text](path) 


Ejemolo es java

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

[Smali informacion]url) 

Tip:null 
Llamada Java: 
  RemoteLogger.hookEnter("testFunction", "argNull", null);
Llamada Smali:

-----------------------
Tipo: String
Llamada java: 
  RemoteLogger.hookEnter("testFunction", "argString", "test value");
Llamada Smali:

-----------------------
Tipo: Boolean
Llamada java: 
  RemoteLogger.hookEnter("testFunction", "argBooleanTrue",  true);
Llamada Smali:

-----------------------
Tipo: Integre 
Llamada java: 
  RemoteLogger.hookEnter("testFunction", "argInteger", 42);
Llamada Smali:

-----------------------
Tipo: Long
Llamada java: 
 RemoteLogger.hookEnter("testFunction", "argLong",    123456789L);
Llamada Smali:

-----------------------
Tipo: Boolean
Llamada java: 
  RemoteLogger.hookEnter("testFunction", "argDouble",  3.14159);
Llamada Smali:

-----------------------
Tipo: Float
Llamada java: 
  RemoteLogger.hookEnter("testFunction", "argFloat",   2.5f);
Llamada Smali:

-----------------------
Tipo: int[]: [I@xxxx
Llamada java: 
  RemoteLogger.hookEnter("testFunction", "argArray",   new int[]{1, 2, 3});
Llamada Smali:

-----------------------
Tipo: Object
Llamada java: 
 RemoteLogger.hookEnter("testFunction", "argObject",  new Object());
Llamada Smali:

-----------------------
Tipo: Bundle
java: 
 RemoteLogger.hookEnter("testFunction", "argBundle",  savedInstanceState);
Smali:

-----------------------


# Si deceas colaboral  

```bash 
aarch64-linux-android-clang -shared -fPIC -O2 -fno-exceptions -fno-rtti -o liblogger.so native_logger.c -I/usr/lib/jvm/java-8-openjdk-amd64/include -I/usr/lib/jvm/java-8-openjdk-amd64/include/linux
```

# Comprobacion basica 

> Solo pueden estar estas 2 

```bash 
readelf -d liblogger.so | grep NEEDED
  0x0000000000000001 (NEEDED)       Shared library: [libdl.so]
  0x0000000000000001 (NEEDED)       Shared library: [libc.so]
```
