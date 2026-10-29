# Referencia de la CLI

`smalilog` tiene cuatro grupos principales: `server`, `manifest`, `hook` y
`renef`; `lms` es experimental y se carga aparte. La ayuda de cada subcomando
es la fuente más actualizada:

```bash
smalilog --help
smalilog server --help
smalilog manifest <cmd> --help
smalilog hook <cmd> --help
smalilog renef <cmd> --help
```

## Códigos de salida

| Código | Significado |
|---|---|
| `0` | Éxito. |
| `1` | Error de ejecución (archivo no encontrado, método no resuelto, etc.). |
| `2` | Error de uso o argumentos inválidos. |

## `smalilog server`

Arranca un servidor HTTP mínimo que acepta `POST /log` con JSON y escribe las
líneas en un archivo.

```bash
smalilog server [--host HOST] [-p PUERTO] [-f ARCHIVO]
                [-l {CRITICAL,DEBUG,ERROR,INFO,WARNING}]
                [--max-headers BYTES] [--max-body BYTES]
                [--no-blocking] [-v]
```

| Opción | Por defecto | Descripción |
|---|---|---|
| `--host` | `127.0.0.1` | Interfaz de escucha. Usa `0.0.0.0` para aceptar conexiones externas. |
| `-p`, `--port` | `9999` | Puerto TCP (0-65535). |
| `-f`, `--log-file` | `app_logs.txt` | Archivo de salida. |
| `-l`, `--log-level` | `INFO` | Nivel mínimo que se escribe. Para `RemoteLog.d` usa `DEBUG`. |
| `--max-headers` | `16384` | Tamaño máximo de cabeceras HTTP. |
| `--max-body` | `1048576` | Tamaño máximo del cuerpo HTTP. |
| `--no-blocking` | — | Arranca en un hilo aparte. |
| `-v`, `--verbose` | — | Muestra la configuración antes de arrancar. |

Ejemplo:

```bash
smalilog server --host 0.0.0.0 --port 9999 \
  --log-file app_logs.txt --log-level DEBUG
```

Petición de prueba:

```bash
curl -X POST http://127.0.0.1:9999/log \
  -H 'Content-Type: application/json' \
  -d '{"level":"INFO","tag":"APP","message":"hola"}'
```

## `smalilog manifest`

Analiza el `AndroidManifest.xml` ya descompilado y agrega lo mínimo para que
los logs HTTP funcionen: permiso `INTERNET` y tráfico en claro hacia
`127.0.0.1`. El manifiesto debe estar en texto; si es binario (AXML), primero
descompila la APK con `apkeditor`.

```bash
smalilog manifest info apk/AndroidManifest.xml
smalilog manifest entrypoints apk/AndroidManifest.xml --smali-dir apk
smalilog manifest permissions apk/AndroidManifest.xml
smalilog manifest fix apk/AndroidManifest.xml
```

### `manifest info`

Muestra paquete, versión, aplicación, `debuggable`, `usesCleartextTraffic`,
permisos, launcher, componentes y enlaces profundos. Con `--smali-dir` añade
las clases Smali que heredan directamente de `Application`, `Activity`, `Service`,
`BroadcastReceiver` o `ContentProvider`. Acepta `--json`.

### `manifest entrypoints`

Lista actividades, servicios, receivers, providers y `activity-alias`, con su
estado `exported`, permisos y `intent-filter`. Es la forma rápida de localizar
el launcher y los puntos de entrada que conviene instrumentar.

| Opción | Descripción |
|---|---|
| `--smali-dir RUTA` | Busca también clases de entrada en el árbol Smali. |
| `--json` | Salida JSON con componentes, launcher y clases Smali. |

### `manifest permissions`

Lista los permisos declarados. Con `--json` devuelve
`{"permissions": [...]}`.

### `manifest fix`

Agrega `android.permission.INTERNET` y
`android:usesCleartextTraffic="true"` si faltan. Es idempotente: ejecutarlo dos
veces no duplica nada. Crea `AndroidManifest.xml.bak` salvo que uses
`--no-backup` o `--output`.

| Opción | Descripción |
|---|---|
| `--permission PERMISO` | Añade un `<uses-permission>` adicional (repetible). |
| `--no-internet` | No agrega `INTERNET`. |
| `--no-cleartext` | No modifica `usesCleartextTraffic`. |
| `-o`, `--output` | Escribe en otro archivo y no toca el original. |
| `--dry-run` | Muestra los cambios sin escribir. |
| `--no-backup` | No crea `.bak`. |

`usesCleartextTraffic` es necesario en Android 9+ para que la app pueda enviar
HTTP a `127.0.0.1`. Si el manifiesto usa `android:networkSecurityConfig`, la
herramienta avisa: esa configuración puede tener prioridad y requerir una
excepción de red para `localhost`.

## `smalilog hook`

Inyecta llamadas de log en un archivo `.smali` concreto. No procesa una APK
completa: primero descompila con `apkeditor` y apunta al archivo de la clase.

```bash
smalilog hook <cmd> archivo.smali [opciones]
```

### Subcomandos

| Subcomando | Qué hace |
|---|---|
| `list` | Lista los métodos del archivo, sus firmas y número de registros. |
| `show` | Muestra el Smali de un método (`-m`) o todos los que tienen cuerpo (`--all`). |
| `analyze` | Muestra registros, parámetros y plan de inyección sin modificar. |
| `enter` | Inyecta un log al entrar al método. |
| `exit` | Inyecta un log al salir (incluye el valor de retorno). |
| `both` | Inyecta entrada y salida. |
| `debug` / `info` / `warn` / `error` | Inyecta un log de nivel fijo con `--tag` y `--message`. |
| `lifecycle` | Inyecta `LifecycleTracker.init(this)` en `Application.onCreate`. |

### Opciones comunes

Salvo en `list` (que solo acepta `archivo`), estos subcomandos comparten:

| Opción | Descripción |
|---|---|
| `-m`, `--method` | Nombre del método. Obligatorio salvo en `list` y `show --all`. |
| `--sig`, `--signature` | Subcadena de la firma para distinguir sobrecargas, p. ej. `"(I)V"`. |
| `--logger-class` | Descriptor Smali del logger. Por defecto `Lcom/deadnote/RemoteLog;`. |
| `-o`, `--output` | Escribe el resultado en otro archivo en vez de sobrescribir. |
| `--no-backup` | No crea el `.bak`. |
| `--no-color` | Desactiva el resaltado. |
| `--style` | Estilo de Pygments (por defecto `default`). |
| `-v`, `--verbose` | Muestra clase, registros y parámetros. |

En los subcomandos de nivel (`debug`/`info`/`warn`/`error`) se añaden:

| Opción | Por defecto | Descripción |
|---|---|---|
| `--tag` | `APP` | Tag que aparece en el log. |
| `--message`, `--msg` | vacío | Mensaje del log. |

### Ejemplos

```bash
smalilog hook list app_dir/smali/classes/com/ejemplo/MainActivity.smali
smalilog hook show app_dir/smali/classes/com/ejemplo/MainActivity.smali -m onCreate
smalilog hook analyze app_dir/smali/classes/com/ejemplo/MainActivity.smali -m onCreate
smalilog hook both app_dir/smali/classes/com/ejemplo/MainActivity.smali -m onCreate
smalilog hook info app_dir/smali/classes/com/ejemplo/MainActivity.smali \
  -m onCreate --tag APP --message "onCreate"
```

Notas:

- Los métodos `abstract` y `native` no tienen cuerpo y se omiten.
- Los stubs de retorno no se permiten en `<init>`/`<clinit>`.
- La inyección es idempotente para los hooks de observación: no duplica el
  mismo bloque si se ejecuta dos veces.
- `lifecycle` espera que el APK tenga `Lcom/deadnote/LifecycleTracker;`.

## `smalilog renef`

Traduce un subconjunto de scripts Lua de Renef a Smali. La referencia completa,
matriz de compatibilidad y ejemplos están en [`renef.md`](renef.md).

```bash
smalilog renef <cmd> [opciones]
```

### `renef parse`

```bash
smalilog renef parse [script.lua] [--preset {ssl,root}]
```

Analiza el script y muestra cada receta clasificada. No escribe archivos.

### `renef apply`

```bash
smalilog renef apply [script.lua] --smali-dir RUTA [opciones]
```

| Opción | Descripción |
|---|---|
| `--smali-dir RUTA` | Raíz del APK descompilado (con `smali*/`) o un `.smali` concreto. |
| `--preset {ssl,root}` | Usa un preset incluido en lugar de un script. |
| `--logger-class` | Descriptor del logger (por defecto `Lcom/deadnote/RemoteLog;`). |
| `--tag` | Tag de los logs de observación (por defecto `RENEF`). |
| `--only CLASE#MÉTODO` | Aplica solo recetas cuyo texto coincida. |
| `--dry-run` | Muestra el plan sin escribir. |
| `--no-backup` | No crea `.smali.bak`. |

### `renef presets`

```bash
smalilog renef presets
smalilog renef presets --show ssl
```

Lista o muestra los presets `ssl` y `root`.

### `renef install`

```bash
smalilog renef install APK_DESCOMPILADA [opciones]
```

Copia `libagent.so`, las clases Smali del puente y parchea el manifiesto con el
receptor exportado, `INTERNET` y `usesCleartextTraffic`. Pensado para el árbol
que produce `apkeditor d` (con `AndroidManifest.xml`, `smali/` y `root/lib/` o
`lib/`).

| Opción | Descripción |
|---|---|
| `--build` | Compila con `apkeditor b` y firma con `apksigner`. |
| `-o, --output APK` | Salida para `--build`; por defecto `<nombre>-smalilog.apk` junto al árbol. |
| `--agent-so RUTA` | Usa otro `libagent.so` (arm64-v8a). |
| `--payload-dir RUTA` | Payload alternativo; solo para pruebas del instalador. |
| `--permission PERMISO` | Añade un `<uses-permission>` adicional (repetible); no protege el receptor. |
| `--no-internet` | No agregar `android.permission.INTERNET`. |
| `--no-cleartext` | No habilitar `usesCleartextTraffic`. |
| `--force` | Reemplaza clases o `libagent.so` existentes. |
| `--no-backup` | No crear el respaldo externo `.<nombre>.smalilog-backup/`. |
| `--dry-run` | Muestra el plan sin escribir. |
| `--ks KEYSTORE` | Keystore para `--build` (por defecto el de Termux). |
| `--ks-pass CLAVE` | Clave del keystore, sin el prefijo `pass:` (por defecto `password`). |

`install` es idempotente y crea un respaldo externo
`.<nombre>.smalilog-backup/`; no deja `.bak` dentro de la APK. Usa `--force` si
ya existen clases o un `libagent.so` con otro contenido. Sin `--build` solo
parchea el árbol; compila y firma después.

### `renef runtime`

```bash
smalilog renef runtime <exec|push|status|ping|unhook> [opciones]
```

Envía una orden por `am broadcast` al receptor del agente. No necesita root.

| Opción | Descripción |
|---|---|
| `--package APP` | Package de la app instrumentada. |
| `--apk-dir DIR` | APK descompilada para leer el package (por defecto `.`). |
| `--manifest XML` | Manifiesto concreto. |
| `--adb` / `--serial SERIE` | Ejecuta el broadcast con `adb`; `--serial` implica `--adb`. |
| `--host IP` / `--port PUERTO` | Servidor de logs alternativo. |
| `--action` / `--receiver` | Action/clase del receptor (avanzado). |
| `--dry-run` | Imprime el comando sin ejecutarlo. |

`exec` acepta un archivo `.lua` o `--code '...'` (exactamente uno); `push` acepta
un archivo y opcionalmente `--name`, y lo guarda en `files/smalilog/` antes de
ejecutarlo. `status` comprueba el agente y `unhook` cierra la sesión para que el
agente restaure los hooks.

El comando `am` solo confirma el envío. El resultado real (`op=...`,
`resultado ...`, `RenefLua ...`) aparece en el servidor, por defecto
`app_logs.txt`. Se envía con `-f 0x20` para incluir paquetes detenidos; aun así,
abre la app al menos una vez. `--host`/`--port` quedan guardados en el proceso
de la app hasta que se cambien; si los omites después, se conserva el último
valor. El flujo completo está en [`agente.md`](agente.md).

## Rutas y archivos

- `smalilog hook` trabaja sobre un archivo Smali, no sobre la APK.
- `smalilog renef apply` busca archivos en `RUTA/smali*/` y también acepta un
  `.smali` directo.
- El servidor escribe en `app_logs.txt` por defecto, con rotación de 5 MB y
  3 respaldos.
