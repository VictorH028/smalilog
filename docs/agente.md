# Manual del agente embebido (sin root)

Este manual explica el flujo completo para instrumentar una APK con el agente
`com.smalilog.agent`, ejecutar Lua dentro de la app y recibir los resultados en
el servidor de logs. No requiere root: el agente se carga dentro del proceso de
la aplicación y se controla con `am broadcast`.

> Uso permitido: solo apps propias o con autorización explícita. El receptor
> queda exportado y sin autenticación; no lo uses en apps de terceros ni en
> producción sin protegerlo. Ver [Seguridad](#10-seguridad).

## Contenido

- [1. Qué agente usar](#1-qué-agente-usar)
- [2. Requisitos y límites](#2-requisitos-y-límites)
- [3. Flujo mínimo](#3-flujo-mínimo)
- [4. Preparar la APK](#4-preparar-la-apk)
- [5. Servidor de logs](#5-servidor-de-logs)
- [6. Controlar la app](#6-controlar-la-app)
- [7. Scripts Lua](#7-scripts-lua)
- [8. Leer los logs](#8-leer-los-logs)
- [9. Problemas comunes](#9-problemas-comunes)
- [10. Seguridad](#10-seguridad)
- [11. Limpieza](#11-limpieza)
- [12. Lista de comprobación](#12-lista-de-comprobación)
- [13. Referencia interna](#13-referencia-interna)

## 1. Qué agente usar

| Puente | Paquete/action | Uso | Límite |
|---|---|---|---|
| Nuevo (este manual) | `com.smalilog.agent` / `com.smalilog.agent.ACTION` | Cualquier APK descompilada | 256 KB |
| Antiguo de prueba | `com.deadnote` / `com.deadnote.ACCION_DESDE_TERMUX` | Solo `build_payloads` | 30 KB |

El puente nuevo se instala con `smalilog renef install` y se controla con
`smalilog renef runtime`. El puente antiguo se documenta en
[`renef.md` §7c](renef.md);
no mezcles las órdenes ni los receptores de ambos.

No confundir con `smalilog renef apply`, que traduce Lua a Smali **antes** de
compilar. El agente de este manual ejecuta Lua **después**, con la app abierta.

## 2. Requisitos y límites

| Requisito | Detalle |
|---|---|
| Android | API 24 (Android 7.0) o superior. |
| ABI | `arm64-v8a`. El payload no incluye otras arquitecturas. |
| APK | Descompilada con `AndroidManifest.xml` en texto y árbol `smali/`. |
| Herramientas | `apkeditor`; `apksigner` si usas `--build`. |
| Servidor | `smalilog server`, por defecto en `127.0.0.1:9999`. |
| Dispositivo | Debe poder instalar la APK firmada; Termux solo prepara y controla. |

Límites prácticos:

- Script máximo: **256 KB** (antes de base64).
- Tiempo máximo por orden en el puente: **15 s**.
- El agente se ejecuta en el proceso principal de la app.
- Si la app se detiene o se fuerza su detención, hay que abrirla de nuevo.
- El `libagent.so` añade aproximadamente 9.2 MB a la APK.
- El receptor no tiene permiso propio: cualquier app podría enviarle órdenes.
- `usesCleartextTraffic` puede ser ignorado si la app usa
  `android:networkSecurityConfig`.
- Está pensado para una APK/base APK; los splits y los AAB no están probados.
- El receptor se ejecuta en el proceso que declara el manifiesto, normalmente
  el principal. En apps multiproceso, el agente no está en los demás procesos.
- Si actualizas o reinstalas la app desde otra fuente, pierdes la
  instrumentación y hay que volver a instalar el payload.

## 3. Flujo mínimo

```bash
# 1. Descompilar
apkeditor d -i app.apk -o ./app

# 2. Instalar el agente y generar una APK firmada
smalilog renef install ./app --build -o app-instrumentada.apk

# 3. Arrancar el servidor en otra terminal
smalilog server --log-level DEBUG

# 4. Instalar app-instrumentada.apk, abrir la app una vez y comprobar
smalilog renef runtime ping --apk-dir ./app
smalilog renef runtime status --apk-dir ./app

# 5. Ejecutar Lua y limpiar
smalilog renef runtime exec --code 'print("hola desde la app")' --apk-dir ./app
smalilog renef runtime push hook.lua --apk-dir ./app
smalilog renef runtime unhook --apk-dir ./app
```

El resultado de `ping`, `status`, `exec`, `push` y `unhook` **no se devuelve por
la terminal**: se envía al servidor y aparece en `app_logs.txt`. El comando
`am` solo confirma que el broadcast fue enviado.

## 4. Preparar la APK

### 4.1 Descompilar

```bash
apkeditor d -i app.apk -o ./app
ls ./app/AndroidManifest.xml ./app/smali
```

`apkeditor` puede generar `smali/classes/`, `smali/classes2/`, etc. El
instalador detecta el primer árbol válido y también acepta el layout
`smali/com/...` de apktool. Si el manifiesto sigue siendo binario, vuelve a
descompilar la APK.

### 4.2 Revisar el plan sin escribir

```bash
smalilog renef install ./app --dry-run
smalilog renef install ./app --dry-run --build -o /tmp/app-prueba.apk
```

`--dry-run` no escribe archivos ni compila. `--build` con `--dry-run` tampoco
compila; solo muestra el plan.

### 4.3 Instalar el payload

```bash
smalilog renef install ./app
```

El instalador:

1. Copia `libagent.so` en `root/lib/arm64-v8a/` o `lib/arm64-v8a/`.
2. Copia el Smali del puente en `smali/classes/com/smalilog/agent/` o
   `smali/com/smalilog/agent/`.
3. Inserta `com.smalilog.agent.AgentReceiver` en el manifiesto.
4. Añade `android.permission.INTERNET` y
   `android:usesCleartextTraffic="true"` si faltan.
5. Crea un respaldo externo `.<nombre-del-directorio>.smalilog-backup/` en el
   directorio padre. No mete `.bak` dentro de la APK. Si el respaldo ya existe,
   no lo sobrescribe: conserva la primera copia.

Opciones habituales:

```bash
# La app ya tenía otro libagent.so o las clases del puente
smalilog renef install ./app --force

# No tocar INTERNET o cleartext
smalilog renef install ./app --no-internet --no-cleartext

# Usar otro agente arm64-v8a
smalilog renef install ./app --agent-so ./libagent-personalizado.so

# Añadir un uses-permission adicional
smalilog renef install ./app --permission android.permission.ACCESS_NETWORK_STATE

# No crear respaldo externo
smalilog renef install ./app --no-backup
```

`--force` reemplaza únicamente archivos del payload que ya existan con otro
contenido. Sin `--force`, el instalador aborta para no pisar clases ajenas.

### 4.4 Compilar, firmar y verificar

La forma recomendada:

```bash
smalilog renef install ./app --build -o app-instrumentada.apk
```

`--build` ejecuta `apkeditor b` y `apksigner`. Genera:

- `app-instrumentada.apk`: APK firmada final.
- `app-instrumentada-unsigned.apk`: APK intermedia sin firmar.

Sin `-o`, el nombre por defecto es `<nombre-del-directorio>-smalilog.apk` en el
directorio padre del árbol. La firma usa por
defecto la clave de `termux-apk-make`; si esa clave no existe, deja la APK sin
firmar y avisa.

Puedes usar tu propia clave:

```bash
smalilog renef install ./app --build \
  -o app-instrumentada.apk \
  --ks mi-clave.jks --ks-pass 'mi-clave'
```

Verifica la firma:

```bash
"$PREFIX/lib/termux-apk-make/toolz/apksigner" verify --verbose app-instrumentada.apk
```

Si prefieres compilar a mano:

```bash
apkeditor b -i ./app -o app-unsigned.apk

bash "$PREFIX/lib/termux-apk-make/toolz/apksigner" sign \
  --ks "$PREFIX/lib/termux-apk-make/toolz/key.keystore" \
  --ks-pass pass:password \
  --min-sdk-version 24 \
  --out app-instrumentada.apk \
  app-unsigned.apk
```

Android no permite actualizar una app con una firma distinta. Si la APK
original usaba otra clave, desinstala la versión anterior o firma con la misma
clave.

Si `apksigner` falla con `/bin/bash: bad interpreter`:

```bash
termux-fix-shebang "$PREFIX/lib/termux-apk-make/toolz/apksigner"
```

### 4.5 Instalar en el dispositivo

Instala `app-instrumentada.apk` manualmente o con ADB:

```bash
adb install -r app-instrumentada.apk
```

Después abre la app al menos una vez. Aunque `runtime` envía
`FLAG_INCLUDE_STOPPED_PACKAGES` (`-f 0x20`), algunos fabricantes no entregan
broadcasts a apps detenidas o recién instaladas.

### 4.6 Actualizar una instrumentación existente

Vuelve a descompilar la APK original, no la ya instrumentada, y usa `--force`:

```bash
apkeditor d -i app.apk -o ./app
smalilog renef install ./app --force --build -o app-instrumentada.apk
```

Conserva una copia del APK original y de la carpeta
`.<nombre>.smalilog-backup/`. El respaldo replica las rutas relativas de los
archivos reemplazados; para restaurarlos antes de recompilar:

```bash
cp -a .app.smalilog-backup/. ./app/
```

El instalador no tiene un comando de desinstalación automática.

## 5. Servidor de logs

### 5.1 Arrancar

Para el mismo dispositivo:

```bash
smalilog server --host 127.0.0.1 --port 9999 \
  --log-file app_logs.txt --log-level DEBUG
```

Para aceptar conexiones desde otro equipo:

```bash
smalilog server --host 0.0.0.0 --port 9999 \
  --log-file app_logs.txt --log-level DEBUG
```

Si el servidor está en un PC y el dispositivo está conectado por USB, puedes
evitar la IP con:

```bash
adb reverse tcp:9999 tcp:9999
```

Así el agente puede seguir usando `127.0.0.1:9999` dentro del dispositivo.
El servidor rota `app_logs.txt` a 5 MB y conserva 3 respaldos.

`DEBUG` es necesario para ver logs de app enviados con `RemoteLog.d`, como
`[RenefDemo]` o `[bot]`. Los `print()` de Lua se registran como `INFO`.

En segundo plano:

```bash
nohup smalilog server --log-level DEBUG > servidor.out 2>&1 &
echo $! > servidor.pid
```

Detenerlo:

```bash
kill "$(cat servidor.pid)"
```

Android puede suspender procesos de Termux en segundo plano. Si el servidor deja
de responder, mantén la sesión abierta, desactiva la optimización de batería
para Termux o vuelve a arrancarlo.

### 5.2 Comprobar el endpoint

```bash
curl -X POST http://127.0.0.1:9999/log \
  -H 'Content-Type: application/json' \
  -d '{"level":"INFO","tag":"PRUEBA","message":"hola"}'

tail -f app_logs.txt
```

Debe aparecer `[PRUEBA] hola`. El servidor también escribe en su salida estándar.
Si usas otro host/puerto, pásalos al agente:

```bash
smalilog renef runtime status --apk-dir ./app \
  --host 192.168.1.50 --port 9999
```

El agente usa `127.0.0.1:9999` si no indicas `--host`/`--port`. El host y el
puerto se guardan mientras viva el proceso de la app: si primero usas
`--host 192.168.1.50`, una orden posterior sin `--host` seguirá usando esa IP.

## 6. Controlar la app

### 6.1 Elegir el package

El package se lee del manifiesto descompilado:

```bash
smalilog renef runtime status --apk-dir ./app
```

También puedes indicarlo directamente, sin depender del árbol:

```bash
smalilog renef runtime status --package com.mi.app
```

Si el manifiesto está en otra ruta:

```bash
smalilog renef runtime status --manifest ./app/AndroidManifest.xml
```

### 6.2 Órdenes

| Comando | Qué hace | Cuándo usarlo |
|---|---|---|
| `ping` | Comprueba que el receptor responde. | Tras instalar/abrir la app. |
| `status` | Conecta con el agente y ejecuta `return true`. | Para saber si Lua funciona. |
| `exec` | Ejecuta un archivo o `--code` sin guardarlo. | Pruebas rápidas. |
| `push` | Guarda el script en `files/smalilog/` y lo ejecuta. | Scripts que quieres conservar. |
| `unhook` | Cierra el socket, restaura hooks y resetea la guarda. | Antes de recargar o terminar. |

Ejemplos:

```bash
smalilog renef runtime ping --apk-dir ./app
smalilog renef runtime status --apk-dir ./app
smalilog renef runtime exec --code 'print("hola")' --apk-dir ./app
smalilog renef runtime exec hook.lua --apk-dir ./app
smalilog renef runtime push hook.lua --apk-dir ./app
smalilog renef runtime push hook.lua --name mi-hook.lua --apk-dir ./app
smalilog renef runtime unhook --apk-dir ./app
```

`exec` acepta un archivo `.lua` o `--code`, pero no ambos. `push` solo acepta
archivo; el nombre se sanea y se le añade `.lua` si falta.

### 6.3 Ver lo que se ejecutará

```bash
smalilog renef runtime status --package com.mi.app --dry-run
smalilog renef runtime exec --code 'print("hola")' \
  --package com.mi.app --dry-run
```

La salida es el comando `am broadcast` completo. No requiere que la app esté
abierta.

### 6.4 Dispositivo externo con ADB

```bash
adb devices
smalilog renef runtime status --package com.mi.app \
  --adb --serial emulator-5554
```

`--serial` implica `--adb`. Si no hay dispositivo, usa el broadcast local sin
`--adb`.

### 6.5 Qué significa la salida de `am`

```text
Broadcasting: Intent { act=com.smalilog.agent.ACTION ... }
Broadcast sent without waiting for result
```

Significa que Android aceptó el broadcast, **no** que el agente lo haya
ejecutado. La confirmación real está en `app_logs.txt`:

```text
[SmalilogAgent] op=STATUS
[SmalilogAgent] resultado STATUS: OK: agente activo (pid=...)
```

## 7. Scripts Lua

### 7.1 Prueba mínima

```bash
smalilog renef runtime exec \
  --code 'print("hola desde la app")' \
  --apk-dir ./app
```

Si el script imprime, el resultado aparece como `[RenefLua] ...` en el servidor.

### 7.2 Hooks de ejemplo

El repositorio incluye `build_payloads/runtime_hook.lua` para la app de prueba
`com.deadnote`. Instala hooks sobre `demoRenefCheck`, `demoRenefLabel` y
`prueba1`:

```bash
smalilog renef runtime push build_payloads/runtime_hook.lua \
  --package com.deadnote
```

Al pulsar **prueba1** en la app se espera:

```text
[bot] Prueba de botón pulsada
[RenefDemo] demoRenefCheck=false
[RenefLua] [runtime] prueba1 entra
[RenefLua] [runtime] demoRenefCheck -> false
[RenefDemo] demoRenefLabel=runtime-hook
[RenefLua] [runtime] prueba1 sale
```

En runtime, para modificar booleanos usa `JNI.boolean(false)`; un
`return false` directo de Lua no cambia el retorno. Para strings usa
`JNI.string("...")`.

### 7.3 Guarda contra hooks duplicados

El script de ejemplo usa:

```lua
if _G.__smalilog_runtime_hook then
    print("hooks ya instalados; usa unhook para recargar")
    return
end
_G.__smalilog_runtime_hook = true
```

Antes de recargar una versión distinta:

```bash
smalilog renef runtime unhook --apk-dir ./app
smalilog renef runtime push hook.lua --apk-dir ./app
```

`unhook` cierra el socket; el agente restaura los hooks nativos y Java y
resetea `_G.__smalilog_runtime_hook`.

### 7.4 Dónde se guarda un `push`

`push` escribe en el directorio privado de la app:

```text
/data/user/0/<package>/files/smalilog/<nombre>.lua
```

El script se ejecuta inmediatamente después de guardarlo. Si repites `push` con
el mismo nombre, se sobrescribe. Para volver a ejecutarlo sin reenviar el
código, usa la orden avanzada `EXEC_FILE`:

```bash
am broadcast -f 0x20 -a com.smalilog.agent.ACTION \
  -n com.mi.app/com.smalilog.agent.AgentReceiver \
  --es op EXEC_FILE --es name files/smalilog/hook.lua
```

La CLI no expone `EXEC_FILE`; para el uso normal vuelve a hacer `push`.

### 7.5 Límites del script

- 256 KB de código; por encima se rechaza antes de enviarlo.
- 15 s de espera por orden. Si Lua tarda más, la conexión se cierra y los hooks
  se restauran.
- El script se ejecuta dentro de la app, no en Termux. No uses rutas de Termux
  que la app no pueda leer.

## 8. Leer los logs

Etiquetas habituales:

| Etiqueta | Origen |
|---|---|
| `[SmalilogAgent]` | Receptor, conexión, resultado de la orden. |
| `[RenefLua]` | `print()` y mensajes del script. |
| `[RenefRuntime]` | Mensajes del puente de runtime antiguo. |
| `[RenefDemo]`, `[bot]` | Logs de la app de prueba. |

Ejemplo de sesión correcta:

```text
[SmalilogAgent] op=PING pid=16216
[SmalilogAgent] resultado PING: OK: receptor activo (pid=16216)
[SmalilogAgent] op=STATUS pid=16216
[SmalilogAgent] Conectado al agente Renef @renef_pl_16216
[SmalilogAgent] resultado STATUS: OK: agente activo (pid=16216)
[SmalilogAgent] op=PUSH pid=16216
[SmalilogAgent] RenefLua [runtime] hook demoRenefCheck instalado
[SmalilogAgent] resultado PUSH: OK
```

Si el servidor está apagado, el agente puede ejecutar la orden pero no podrás
ver el resultado en `app_logs.txt`. Arranca el servidor antes de controlar la
app.

## 9. Problemas comunes

| Síntoma | Causa / solución |
|---|---|
| `Broadcast sent without waiting for result` y no hay logs | Es normal que `am` no espere. Revisa que `smalilog server` esté activo, el puerto y `app_logs.txt`. |
| `Error: Activity not started, unable to resolve Intent` | Package/receptor incorrecto. Usa `--package` o revisa que la APK tenga el receptor. |
| `PING` responde pero `STATUS` falla | `libagent.so` no cargó. Comprueba ABI `arm64-v8a`, que la app sea API 24+ y reinstala con `--force`. |
| `java.lang.UnsatisfiedLinkError` | Falta `libagent.so` o la ABI no coincide. Reinstala el payload; el agente solo es arm64. |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Firma distinta. Desinstala la app o firma con la misma clave. |
| `PING` funciona pero no llegan logs | Revisa `INTERNET`, `usesCleartextTraffic` y `networkSecurityConfig`; el agente envía por HTTP. |
| No aparecen logs `[RenefDemo]` | Son `DEBUG`; arranca el servidor con `--log-level DEBUG`. |
| No aparece nada tras pulsar un botón | Los hooks no están instalados o se perdió la sesión. Revisa `PUSH`, vuelve a ejecutar y no cierres la app. |
| `ERROR: timeout` | El script tardó más de 15 s o el agente no responde. Haz `unhook`, reabre la app y reintenta. |
| `script demasiado grande` | Supera 256 KB. Divide el script o usa `push` con un archivo menor. |
| `Ya existe ... con otro contenido` | Usa `--force` al reinstalar el payload. |
| El manifiesto es binario | Descompila con `apkeditor d`; el instalador necesita XML de texto. |
| `apksigner: /bin/bash: bad interpreter` | `termux-fix-shebang "$PREFIX/lib/termux-apk-make/toolz/apksigner"`. |
| La app no recibe la orden tras force-stop | Ábrela manualmente; algunos fabricantes bloquean broadcasts a apps detenidas. |
| `--adb` no encuentra dispositivo | `adb devices`; sin dispositivo usa el broadcast local. |
| El servidor no recibe desde otro equipo | Usa `--host 0.0.0.0` y pasa la IP del servidor con `runtime --host`. |
| `usesCleartextTraffic` no basta | La app puede tener `networkSecurityConfig`; añade una excepción para `localhost`. |

## 10. Seguridad

El receptor se declara `exported="true"` y no tiene permiso propio. Cualquier
app del dispositivo podría:

- arrancar el proceso de la app;
- enviar órdenes `EXEC`/`PUSH` con Lua arbitrario;
- leer archivos accesibles por la app mediante las órdenes de archivo;
- cambiar el host/puerto de los logs.

Por eso:

- úsalo solo en apps propias o con autorización;
- no lo dejes instalado en un dispositivo compartido;
- no expongas `smalilog server` en `0.0.0.0` en redes no confiables;
- para producción, declara `android:permission` en el receptor con un permiso
  propio de nivel `signature`, valida un token o elimina el receptor antes de
  distribuir;
- protege los respaldos `.smalilog-backup/`, porque contienen manifiesto y
  archivos reemplazados.

## 11. Limpieza

```bash
# Restaurar hooks y cerrar la sesión del agente
smalilog renef runtime unhook --apk-dir ./app

# Detener el servidor si lo arrancaste en segundo plano
kill "$(cat servidor.pid)"

# Desinstalar la app instrumentada
adb uninstall com.mi.app

# Borrar el árbol descompilado y el respaldo
rm -rf ./app ./.app.smalilog-backup
```

Guarda el APK original antes de empezar. `install` no tiene un comando
`uninstall` que restaure automáticamente la APK; el respaldo externo solo
conserva los archivos que el instalador reemplazó.

## 12. Lista de comprobación

- [ ] Tengo permiso para instrumentar la app.
- [ ] La APK es arm64 y Android 24+.
- [ ] Guardé el APK original.
- [ ] Descompilé con `apkeditor` y el manifiesto es texto.
- [ ] Ejecuté `install --dry-run`.
- [ ] Instalé el payload con `--force` si era necesario.
- [ ] Compilé y firmé con `--build` o a mano.
- [ ] Verifiqué la firma con `apksigner verify`.
- [ ] Arranqué `smalilog server` antes de probar.
- [ ] Instalé y abrí la app.
- [ ] `ping` y `status` responden en `app_logs.txt`.
- [ ] Cargué el script y comprobé el efecto en la app.
- [ ] Hice `unhook` y detuve el servidor al terminar.

## 13. Referencia interna

- Payload versionado: `src/smalilog/renef/payload/`.
- Smali del puente: `src/smalilog/renef/payload/smali/com/smalilog/agent/`.
- Java fuente: `src/smalilog/renef/payload/java/com/smalilog/agent/`.
- Implementación del instalador: `src/smalilog/renef/_agent.py`.
- CLI: `src/smalilog/renef/_agent_cli.py`.
- Protocolo y puente antiguo: [`renef.md`](renef.md).
- Referencia de opciones: [`cli.md`](cli.md).
