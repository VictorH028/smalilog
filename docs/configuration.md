# Configuración

La configuración de `lms` se lee de un `config.toml` opcional en el directorio
de trabajo y de variables de entorno con prefijo `SMALILOG_`. El servidor HTTP y
los hooks **no** usan este archivo: se configuran con sus propias opciones de
línea de comandos.

## `config.toml`

Usa [`config.example.toml`](config.example.toml) como plantilla:

```toml
server_cmd = "smali-lsp"
server_args = ["mcp"]
# workspace = "/ruta/al/apk/descompilado"
# db_path = "/ruta/a/memory.sqlite3"
```

| Clave | Por defecto | Descripción |
|---|---|---|
| `server_cmd` | `smali-lsp` | Comando del servidor MCP que usa `lms`. |
| `server_args` | `["mcp"]` | Argumentos de ese comando. |
| `workspace` | `null` | Directorio de trabajo del análisis. |
| `db_path` | `user_data_dir("smalilog")/memory.sqlite3` | Base SQLite de memoria. |

## Variables de entorno

Cualquier clave anterior se puede sobrescribir con `SMALILOG_` en mayúsculas:

```bash
export SMALILOG_WORKSPACE="$HOME/apk"
export SMALILOG_SERVER_CMD="smali-lsp"
export SMALILOG_DB_PATH="$HOME/smalilog.sqlite3"
```

## Servidor y hooks

El servidor se configura directamente:

```bash
smalilog server --host 0.0.0.0 --port 9999 \
  --log-file app_logs.txt --log-level DEBUG
```

Los límites HTTP (`--max-headers`, `--max-body`) también son opciones del
comando. Consulta [`cli.md`](cli.md) para la tabla completa.

## `lms`

`smalilog lms` es experimental, se carga de forma perezosa y depende del
servidor MCP configurado. No participa en `server` ni en `hook`.
