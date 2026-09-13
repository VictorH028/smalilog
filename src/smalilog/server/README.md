Ejemplo de petición:

```
  curl -X POST http://127.0.0.1:9999/log \
       -H 'Content-Type: application/json' \
       -d '{"level":"INFO","tag":"APP","message":"hola"}'
```
