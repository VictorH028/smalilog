# Descripción General

==main.py== es el punto de entrada del CLI de smalilog, herramienta para instrumentar aplicaciones Android con log remoto mediante la combinación:

· Smali (inyección de hooks)
· JNI (envío nativo de logs, ver [...](url) )
· Servidor HTTP (recepción en 127.0.0.1:9999 por defecto)

El CLI expone dos subcomandos principales: server y hook.

--- 

# Estructura de Comandos

```
smalilog
├── server                         Arranca el servidor HTTP de logs
└── hook                           Inyecta hooks en archivos Smali
    ├── list                       Lista métodos del .smali
    ├── show                       Muestra el código smali de un método
    ├── analyze                    Analiza registros y plan de inyección
    ├── enter                      Hook de entrada
    ├── exit                       Hook de salida
    ├── both                       Hook de entrada + salida
    ├── log                        Log con tag/mensaje personalizado
    └── lifecycle                  LifecycleTracker en Application.onCreate
```

---

#  Constantes Globales

Constante Valor Descripción
EXIT_OK 0 Salida exitosa
EXIT_ERROR 1 Error de ejecución
EXIT_USAGE 2 Error de uso / argumentos inválidos
LOG_LEVELS dict Mapeo de niveles → constantes de logging

Niveles de log soportados

```python
LOG_LEVELS = {
    "DEBUG":    logging.DEBUG,
    "INFO":     logging.INFO,
    "WARNING":  logging.WARNING,
    "ERROR":    logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
```
---


