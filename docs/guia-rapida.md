# Guía rápida para nuevos usuarios

Esta guía va de cero a ver logs de una app Android con **smalilog**. No hace
falta root ni emulador: se instrumenta el Smali, se reconstruye la APK y se
prueba en un dispositivo real.

> Uso permitido: solo apps propias o con autorización explícita. No uses estas
> técnicas para saltar protecciones de terceros.

## 1. Qué piezas hay

| Pieza | Para qué sirve |
|---|---|
| `smalilog server` | Recibe logs JSON por HTTP y los escribe en un archivo. |
| `smalilog manifest ...` | Prepara permisos y busca puntos de entrada en el manifiesto. |
| `smalilog hook ...` | Inyecta llamadas de log en un archivo `.smali`. |
| `smalilog renef ...` | Traduce Lua a Smali, instala el agente y lo controla. |
| `build_payloads/` | App de prueba `com.deadnote` con `RemoteLog`, JNI y agente Renef. |
| `liblogger.so` | Librería JNI que envía los logs al servidor. |

La app de prueba ya trae las clases auxiliares (`RemoteLog`,
`LifecycleTracker`, `Backup`, etc.). Para otra APK necesitas esas clases dentro
del APK o adaptar el descriptor del logger (ver `--logger-class`).

## 2. Requisitos

- Python 3.10 o superior.
- Termux en Android o Linux.
- `apkeditor` para descompilar/recompilar APKs.
- `apksigner` (incluido en Termux con `termux-apk-make`).
- Un dispositivo Android para instalar la APK y probarla.

## 3. Instalación

Desde la raíz del repositorio:

```bash
make install
smalilog --version
```

`make install` ejecuta `pip install -e .`. Si no usas el Makefile:

```bash
python -m pip install -e .
```

## 4. Primer arranque del servidor

En una terminal:

```bash
smalilog server --host 0.0.0.0 --port 9999 --log-file app_logs.txt --log-level DEBUG
```

- `0.0.0.0` permite conexiones desde el dispositivo; si el servidor corre en el
  mismo móvil, `127.0.0.1` también sirve.
- `--log-level DEBUG` es necesario para ver logs `RemoteLog.d` como
  `[RenefDemo]` o `[bot]`. En `INFO` solo salen `i/w/e`.
- El archivo por defecto es `app_logs.txt` en el directorio actual.

Comprueba el endpoint en otra terminal:

```bash
curl -X POST http://127.0.0.1:9999/log \
  -H 'Content-Type: application/json' \
  -d '{"level":"INFO","tag":"PRUEBA","message":"hola"}'
tail -f app_logs.txt
```

Deberías ver una línea con `[PRUEBA] hola`.

## 5. Flujo A: instrumentar una APK

### 5.1 Descompilar

```bash
apkeditor d -i app.apk -o app_dir
find app_dir -maxdepth 3 -type d -name 'smali*'
```

Con `apkeditor` lo habitual es `smali/classes/` (y `smali/classes2/`, etc. para
multidex). Localiza el archivo de la clase que quieres observar:

```bash
SMALI=$(find app_dir/smali* -name 'MainActivity.smali' | head -n1)
echo "$SMALI"
```

### 5.2 Preparar el manifiesto y buscar puntos de entrada

Antes de inyectar, revisa qué componentes tiene la app y agrega los permisos que
necesita el logger HTTP:

```bash
smalilog manifest info app_dir/AndroidManifest.xml --smali-dir app_dir
smalilog manifest fix app_dir/AndroidManifest.xml
```

`manifest fix` agrega `android.permission.INTERNET` y
`android:usesCleartextTraffic="true"` si faltan, con copia `.bak`. Sin el
segundo, Android 9+ puede bloquear el HTTP a `127.0.0.1`.

`manifest entrypoints` lista el launcher y los componentes exportados; úsalo
para elegir qué método observar:

```bash
smalilog manifest entrypoints app_dir/AndroidManifest.xml --smali-dir app_dir
smalilog manifest entrypoints app_dir/AndroidManifest.xml --json
```

Si el manifiesto es binario, descompila primero con `apkeditor`; la herramienta
lo detecta y te lo indica.

### 5.3 Encontrar el método

```bash
smalilog hook list "$SMALI"
smalilog hook show "$SMALI" -m onCreate
```

Para ver el plan de registros antes de tocar nada:

```bash
smalilog hook analyze "$SMALI" -m onCreate
```

### 5.4 Inyectar

```bash
# Entrada y salida
smalilog hook both "$SMALI" -m onCreate

# Solo entrada
smalilog hook enter "$SMALI" -m onCreate

# Log de nivel con tag y mensaje
smalilog hook info "$SMALI" \
  -m onCreate --tag APP --message "onCreate"

# Usar otra clase logger (debe existir en el APK)
smalilog hook info "$SMALI" \
  -m onCreate --tag APP --message "onCreate" \
  --logger-class Lcom/ejemplo/RemoteLog;
```

El inyector crea un `.bak` salvo que uses `--no-backup`. Los métodos `abstract` y
`native` no se instrumentan; `<init>`/`<clinit>` están bloqueados para stubs.

### 5.5 Recompilar, firmar e instalar

```bash
apkeditor b -i app_dir -o app_unsigned.apk

bash "$PREFIX/lib/termux-apk-make/toolz/apksigner" sign \
  --ks "$PREFIX/lib/termux-apk-make/toolz/key.keystore" \
  --ks-pass pass:password \
  --out app_patched.apk app_unsigned.apk
```

Instala `app_patched.apk` manualmente en el dispositivo (el instalador de
Android pedirá confirmación). Desinstala la versión anterior si la firma cambia.

### 5.6 Ver los logs

Abre la app y mira la terminal del servidor o:

```bash
tail -f app_logs.txt
```

Los hooks `traceIn`/`traceOut` generan líneas como:

```text
[TRACE] #1 -> Lcom/ejemplo/MainActivity;->onCreate(Landroid/os/Bundle;)V(...)
[TRACE] #1 <- Lcom/ejemplo/MainActivity;->onCreate(Landroid/os/Bundle;)V = void
```

## 6. Flujo B: Renef sin root

Renef permite escribir hooks en Lua. Smalilog traduce un subconjunto a Smali:

```bash
smalilog renef presets
smalilog renef parse --preset ssl
smalilog renef apply --preset ssl --smali-dir app_dir --dry-run
smalilog renef apply --preset ssl --smali-dir app_dir
```

Opciones útiles de `apply`:

```bash
smalilog renef apply mi_script.lua --smali-dir app_dir \
  --tag RENEF --logger-class Lcom/deadnote/RemoteLog;
```

Los hooks nativos (`lib*.so`, `Memory.*`, `Syscall.*`, `Java.use`) no se pueden
traducir sin el agente dinámico; el reporte indica cuáles se omitieron y por qué.
La referencia completa está en [`renef.md`](renef.md).

## 6.1. Flujo B2: agente embebido en cualquier APK (sin root)

Para cargar Lua en runtime en una APK que no sea `build_payloads`, descompila,
instala el payload y reconstruye:

```bash
apkeditor d -i app.apk -o ./app
smalilog renef install ./app --dry-run
smalilog renef install ./app --build -o app-instrumentada.apk
```

`install` copia `libagent.so`, añade el puente Smali y parchea el manifiesto
(receptor exportado, `INTERNET` y `usesCleartextTraffic`). Usa `--force` si el
árbol ya tenía un `libagent.so` o las clases del puente. Si no usas `--build`,
compila y firma a mano:

```bash
apkeditor b -i ./app -o app-unsigned.apk

bash "$PREFIX/lib/termux-apk-make/toolz/apksigner" sign \
  --ks "$PREFIX/lib/termux-apk-make/toolz/key.keystore" \
  --ks-pass pass:password --min-sdk-version 24 \
  --out app-instrumentada.apk app-unsigned.apk
```

Si la app original tiene otra firma, desinstálala antes o firma con tu propia
clave (`--ks`/`--ks-pass`); Android no permite actualizar con una firma distinta.
Verifica la firma:

```bash
"$PREFIX/lib/termux-apk-make/toolz/apksigner" verify --verbose app-instrumentada.apk
```

Instala la APK, ábrela y arranca el servidor de logs en otra terminal antes de
controlar:

```bash
# Terminal 1
smalilog server --host 127.0.0.1 --port 9999 --log-level DEBUG

# Terminal 2
smalilog renef runtime ping --apk-dir ./app
smalilog renef runtime status --apk-dir ./app
smalilog renef runtime exec --code 'print("hola")' --apk-dir ./app
smalilog renef runtime push hook.lua --apk-dir ./app
smalilog renef runtime unhook --apk-dir ./app
```

El comando `am` solo confirma el envío; los resultados aparecen en
`app_logs.txt`. Los scripts admiten hasta 256 KB y se ejecutan dentro del
proceso de la app, sin root. Solo se incluye `arm64-v8a` y el agente requiere
Android 24+; el receptor exportado no tiene permiso propio, úsalo solo en
apps propias o de laboratorio.

El flujo detallado, incluyendo instalación con `--force`, ADB, `push`,
interpretación de logs y solución de problemas, está en
[`agente.md`](agente.md).

## 7. Flujo C: runtime Renef en la app de prueba

`build_payloads` incluye `libagent.so` y un receptor de broadcasts. Esto permite
cargar Lua **con la app ya abierta**, sin recompilar:

```bash
# 1. Compilar y firmar la app de prueba
termux-apk-make build_payloads

# 2. Instalar build_payloads/build/final.apk y abrirla

# 3. Enviar el script (la app debe seguir en ejecución)
B64=$(base64 -w0 build_payloads/runtime_hook.lua)
am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
  -n com.deadnote/.ReceptorTermux \
  --es orden LUA_PUSH --es arg1 runtime_hook.lua --es arg2 "$B64"

# 4. Pulsar el botón "prueba1" de la app y mirar app_logs.txt

# 5. Limpiar los hooks para recargar otro script
am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
  -n com.deadnote/.ReceptorTermux --es orden LUA_UNHOOK
```

Órdenes disponibles: `LUA` (archivo), `LUA_CODE`/`LUA_B64` (base64),
`LUA_PUSH` (guarda en `files/` y ejecuta) y `LUA_UNHOOK` (cierra el socket y
restaura los hooks). El detalle está en [`renef.md`](renef.md), sección 7c.

## 8. Problemas comunes

| Síntoma | Causa / solución |
|---|---|
| No aparece nada en `app_logs.txt` | Revisa host/puerto, ejecuta `smalilog manifest fix`, y usa `--log-level DEBUG` si esperas `RemoteLog.d`. |
| `apksigner: /bin/bash: bad interpreter` | `termux-fix-shebang "$PREFIX/lib/termux-apk-make/toolz/apksigner"` y reintenta. |
| `run-as: permission denied` | Usa `LUA_PUSH` en la app de prueba; no dependas de `run-as` en OEM restrictivos. |
| `Broadcast sent without waiting for result` y no hay logs | Es normal que `am` no espere. Comprueba que `smalilog server` esté activo, el host/puerto y `app_logs.txt`. |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | La firma cambió. Desinstala la app o firma con la misma clave. |
| `PING` responde pero `STATUS` falla | El agente no cargó: revisa ABI `arm64-v8a`, API 24+ y reinstala con `--force`. |
| Hooks duplicados en los logs | Fuerza la detención de la app o envía `LUA_UNHOOK` antes de recargar. |
| `NoClassDefFoundError: Lcom/deadnote/RemoteLog;` | La APK no incluye el logger. Añade `RemoteLog` + `liblogger.so` o usa `--logger-class` con una clase existente. |
| `No se pudo leer el AndroidManifest.xml` | Es AXML binario. Descompila con `apkeditor d` y usa el manifiesto en texto. |
| `hook lifecycle` falla | Solo funciona en `Application.onCreate` y espera `Lcom/deadnote/LifecycleTracker;`. |
| El método se omite | Es `abstract`/`native`, no existe con esa firma o es un constructor. |

## 9. Siguientes pasos

- [`README.md` de docs](README.md): índice completo.
- [`cli.md`](cli.md): referencia de todos los comandos y opciones.
- [`injector.md`](injector.md): cómo funciona la inyección Smali por dentro.
- [`renef.md`](renef.md): puente Lua → Smali y runtime por broadcast.
- [`agente.md`](agente.md): manual completo del agente embebido sin root.
- [`android/RemoteLog.md`](android/RemoteLog.md): API del logger y límites.
- [`legacy/`](legacy/README.md): notas históricas, no son guía de uso.
