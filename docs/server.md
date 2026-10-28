Ejemplo de petición:

```
  curl -X POST http://127.0.0.1:9999/log \
       -H 'Content-Type: application/json' \
       -d '{"level":"INFO","tag":"APP","message":"hola"}'
``` 

Al usar como tag  SMALILOG_ACTIVITY llega la informacion como level INFO 

# Desde el móvil:
```
smalilog hook info App.smali -m onCreate --tag SMALILOG_ACTIVITY --message "onCreate"
```

