# Servidor de logs

`smalilog server` levanta un servidor HTTP mínimo para recibir los logs que envía
la app instrumentada. Por defecto escucha en `127.0.0.1:9999` y escribe en
`app_logs.txt`.

## Arranque

```bash
smalilog server
smalilog server --host 0.0.0.0 --port 9999 \
  --log-file app_logs.txt --log-level DEBUG
```

Opciones completas: [`cli.md`](cli.md#smalilog-server).

## Endpoint

```text
POST /log
Content-Type: application/json
```

Acepta un objeto o una lista de objetos:

```json
{"level":"INFO","tag":"APP","message":"hola"}
```

```json
[
  {"level":"DEBUG","tag":"APP","message":"inicio"},
  {"level":"ERROR","tag":"APP","message":"fallo"}
]
```

Niveles admitidos: `DEBUG`, `INFO`, `WARNING`, `ERROR`. El servidor filtra por
el nivel configurado: con el `INFO` por defecto, los `RemoteLog.d` no se
escriben.

## Prueba manual

```bash
curl -X POST http://127.0.0.1:9999/log \
  -H 'Content-Type: application/json' \
  -d '{"level":"INFO","tag":"APP","message":"hola"}'

tail -f app_logs.txt
```

Salida esperada:

```text
2026-01-01 12:00:00,000 - INFO - [APP] hola
```

## Desde la app

`RemoteLog` de `build_payloads` envía al host y puerto configurados (por defecto
`127.0.0.1:9999`). Si el servidor corre en otro equipo, cambia esa configuración
en la app y arranca el servidor con `--host 0.0.0.0`.

El tag `SMALILOG_ACTIVITY` se usa para las trazas de actividad; también puedes
inyectar logs propios:

```bash
smalilog hook info App.smali -m onCreate \
  --tag SMALILOG_ACTIVITY --message "onCreate"
```
