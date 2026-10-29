# Puente Renef → Smali (sin root)

> Estado: **experimental**. Traduce un subconjunto de scripts Lua de Renef a
> instrumentación Smali estática, pensada para Termux/Android sin root.

> Índice de documentación: [`README.md`](README.md).

## 1. Qué es y por qué

[Renef](https://renef.io) es un toolkit de instrumentación dinámica para
Android ARM64: inyecta un agente en el proceso, ejecuta scripts Lua y permite
hookear funciones nativas y Java, leer/escribir memoria, trazar syscalls, etc.

Smalilog hace lo contrario: modifica el **Smali** de una APK descompilada y la
vuelve a empaquetar. Esa diferencia es clave en Termux, donde **no hay root ni
permisos elevados**: un agente dinámico no se puede desplegar, pero sí se puede
instrumentar y reconstruir una APK.

Este puente combina ambos mundos:

1. Tomas tus scripts/recetas de Renef (o los presets incluidos).
2. Smalilog extrae las llamadas `hook`/`safe_hook` con argumentos literales.
3. Las traduce a parches Smali equivalentes cuando es posible.
4. Reporta con claridad lo que **solo** funciona con el agente Renef.

El puente estático no ejecuta Lua ni código del script: solo se leen sus
llamadas y literales. La sección **7c** describe el puente de runtime antiguo
de `build_payloads`; la sección **7d** y el
[manual del agente](agente.md) describen el puente nuevo instalable en
cualquier APK.

## 2. Módulos añadidos

```text
src/smalilog/renef/
├── __init__.py        # API pública
├── _lua.py            # lector de llamadas y literales Lua (sin intérprete)
├── _recipe.py         # clasificación de recetas (stub, log, nativo, ...)
├── _apply.py          # localización de clases Smali y aplicación
├── _cli.py            # smalilog renef ...
└── presets/
    ├── ssl_unpin.lua
    └── root_bypass.lua
```

Además, `HookInjector` incorpora `inject_stub()`, que emite un retorno
constante al inicio del método:

- `V` → `return-void`
- `Z`/`I`/... → `const` + `return`
- `J`/`D` → `const-wide` + `return-wide`
- referencias → `null` o `const-string` + `return-object`

El marcador persistente es `Renef STUB inyectado`, así que aplicar dos veces el
mismo script no duplica parches.

## 3. Comandos

```bash
# Presets incluidos
smalilog renef presets
smalilog renef presets --show ssl

# Analizar sin tocar nada
smalilog renef parse --preset ssl
smalilog renef parse mi_script.lua

# Aplicar sobre una APK descompilada
smalilog renef apply --preset ssl --smali-dir ./apk --dry-run
smalilog renef apply mi_script.lua --smali-dir ./apk/smali

# Filtrar y personalizar
smalilog renef apply --preset root --smali-dir ./apk --only RootBeer
smalilog renef apply mi_script.lua --smali-dir ./apk \
    --tag RENEF --logger-class Lcom/deadnote/RemoteLog;
```

Opciones de `apply`:

| Opción | Descripción |
|---|---|
| `--smali-dir RUTA` | Raíz de la APK descompilada (con `smali*/`) o un `.smali` concreto |
| `--preset {ssl,root}` | Usa un preset incluido en vez de un script |
| `--only TEXTO` | Aplica solo recetas cuyo `clase#método` contenga el texto |
| `--dry-run` | Analiza y muestra el plan sin escribir archivos |
| `--no-backup` | No genera `.smali.bak` |
| `--tag TAG` | Tag de los logs de observación (`RENEF` por defecto) |
| `--logger-class D` | Clase del logger Smali (`Lcom/deadnote/RemoteLog;` por defecto) |

Código de salida: `0` si se aplicó al menos una receta y no hubo errores;
`1` si no se aplicó nada o alguna inyección falló.

## 4. Formato reconocido

Se aceptan llamadas con literales de string:

```lua
-- Java: args.skip = true -> stub (retorno por defecto o indicado en onLeave)
hook("com/example/App", "isRooted", "()Z", {
    onLeave = function(retval) return false end
})

-- Java: observación de entrada y salida (usa traceIn/traceOutVoid/traceOut)
hook("com/example/App", "run", "()V", {
    onEnter = function(args) print("in") end,
    onLeave = function(retval) print("out") end
})
```

También se reconoce el alias `safe_hook(clase, método, firma, tabla, etiqueta)`
usado por los scripts de ejemplo de Renef.

Valores de retorno traducibles: enteros, `true`/`false`, strings y
`JNI.string("...")`. `return nil` y `return retval` significan "sin cambio" y se
tratan como observación, no como stub.

## 5. Matriz de compatibilidad

| Capacidad del script Renef | ¿Traducible sin root? | Resultado |
|---|---|---|
| Hook Java con `onLeave return <constante>` | Sí | `stub` con retorno constante |
| Hook Java void con `args.skip = true` | Sí | `return-void` al inicio |
| Hook Java con `args.skip` y `onLeave return X` | Sí | stub con `X` |
| Solo `print`/observación Java | Sí | log de entrada y/o salida |
| `hook("lib*.so", offset, ...)` | No | se reporta como `native` |
| `Memory.*`, `Module.*` | No | requiere agente Renef |
| `Syscall.*`, `Thread.*`, `KCov.*` | No | requiere agente Renef |
| `Java.use`, `Java.registerClass`, `Java.array` | No | requiere runtime |
| `args[n] = ...` (reescritura de argumentos) | No | se reporta como no soportado |
| Retorno no constante (`obj.raw`, variables) | No | se reporta como no soportado |
| Stubs en `<init>` / `<clinit>` | No | bloqueado por seguridad |

Los hooks nativos y de runtime **no se descartan en silencio**: aparecen en el
reporte con el motivo. Esto permite usar un mismo script en el puente estático y,
si algún día hay dispositivo con root/agente, ejecutarlo con Renef real.

## 6. Flujo completo sin root

```bash
# 1. Descompilar la APK (apkeditor)
apkeditor d -i app.apk -o apk

# 2. Analizar el script y ver qué se puede aplicar
smalilog renef parse --preset ssl

# 3. Aplicar los parches Smali
smalilog renef apply --preset ssl --smali-dir apk

# 4. Recompilar y firmar
apkeditor b -i apk -o app_patched.apk
apkeditor sign -i app_patched.apk

# 5. Instalar manualmente en el dispositivo
```

Para recibir los logs de observación, arranca el servidor antes de abrir la app:

```bash
smalilog server --host 0.0.0.0 --port 9999
```

Recuerda que en Termux **no se puede instalar ni ejecutar la APK**: la
validación de los parches es estática (tests + inspección del Smali). La prueba
en dispositivo ocurre fuera de este entorno.

## 7. Presets incluidos

| Preset | Qué hace | Naturaleza |
|---|---|---|
| `ssl` | Anula `checkServerTrusted`, `CertificatePinner`, `HostnameVerifier`, WebView SSL, Fabric/Appmattus/Flutter (lado Java) | Stubs estáticos |
| `root` | Devuelve `false` en las comprobaciones Java de RootBeer | Stubs estáticos |

Ambos son **listas de recetas**, no magia: si la app usa una librería con otro
nombre de clase o métodos ofuscados, la receta correspondiente se omite con
"clase no encontrada". Añade tus propias llamadas `hook(...)` al script.

No incluyen evasión nativa (por ejemplo `open`/`access`/`fopen` de `libc.so` o
`libflutter.so`) porque eso requiere el agente dinámico de Renef.

## 7b. Ejemplo ejecutable con `build_payloads`

El repo incluye un ejemplo listo para probar en dispositivo:

- `build_payloads/renef_demo.lua`: stubs de `demoRenefCheck()` y
  `demoRenefLabel()`, más observación de `prueba1()`.
- `build_payloads/src/com/deadnote/MainActivity.java`: el botón `prueba1`
  registra esos dos valores para que el efecto sea visible en los logs.

Flujo (Termux, sin root):

```bash
# 1. Compilar y firmar la app de prueba
termux-apk-make build_payloads

# Si apksigner falla con "/bin/bash: bad interpreter", repara su shebang:
termux-fix-shebang "$PREFIX/lib/termux-apk-make/toolz/apksigner"
# y reintenta. Como último recurso, firma a mano:
# bash $PREFIX/lib/termux-apk-make/toolz/apksigner sign \
#   --ks $PREFIX/lib/termux-apk-make/toolz/key.keystore \
#   --ks-pass pass:password --out build_payloads/build/final.apk \
#   build_payloads/build/aligned.apk

# 2. Descompilar
apkeditor d -i build_payloads/build/final.apk \
    -o build_payloads/build/decompiled

# 3. Aplicar el ejemplo Renef
smalilog renef apply build_payloads/renef_demo.lua \
    --smali-dir build_payloads/build/decompiled/smali/classes

# 4. Recompilar y firmar
apkeditor b -i build_payloads/build/decompiled \
    -o build_payloads/build/renef_demo_unsigned.apk
bash $PREFIX/lib/termux-apk-make/toolz/apksigner sign \
    --ks $PREFIX/lib/termux-apk-make/toolz/key.keystore \
    --ks-pass pass:password --out build_payloads/build/renef_demo.apk \
    build_payloads/build/renef_demo_unsigned.apk

# 5. Servidor de logs y luego instalar la APK manualmente
# [RenefDemo] usa RemoteLog.d, así que hace falta nivel DEBUG.
smalilog server --host 0.0.0.0 --port 9999 --log-level DEBUG
```

Al pulsar el botón **prueba1** se espera:

```text
[RenefDemo] demoRenefCheck=false
[RenefDemo] demoRenefLabel=parcheado
[TRACE] #N -> Lcom/deadnote/MainActivity;->prueba1()V(...)
[TRACE] #N <- Lcom/deadnote/MainActivity;->prueba1()V = void
```

Si aparece `demoRenefCheck=true` o `demoRenefLabel=original`, el parche no se
aplicó (revisa que hayas usado el árbol descompilado correcto y vuelve a
recompilar). Si no aparece nada, revisa que el servidor esté escuchando y que
la app tenga permiso `INTERNET`.

## 7c. Runtime antiguo de `build_payloads` por broadcast

Este apartado describe el puente `com.deadnote` que ya viene dentro de
`build_payloads`: action `com.deadnote.ACCION_DESDE_TERMUX`, receptor
`com.deadnote.ReceptorTermux` y órdenes `LUA_*`. Para instrumentar cualquier
otra APK usa el puente nuevo de §7d.

`build_payloads` ya incluye `lib/arm64-v8a/libagent.so`, el agente Renef con
motor Lua. La app lo carga desde `RemoteLog` y el agente abre un socket UNIX
abstracto `@renef_pl_<pid>`. `RenefRuntime` se conecta a ese socket, hace el
handshake y envía el script con `hexexec`, por lo que **no hace falta root ni
recompilar la APK para cambiar de hooks**.

La APK resultante está en `build_payloads/build/renef_runtime.apk` (copia
instalable en `/storage/emulated/0/Download/renef_runtime.apk`). `build/` no se
versiona; si falta, recompila con `termux-apk-make build_payloads` (firma incluida).

### Copiar el script a una ruta accesible por la app

La app es `debuggable`, así que Termux puede escribir en su directorio privado
con `run-as`:

```bash
cat build_payloads/runtime_hook.lua | \
  run-as com.deadnote sh -c 'mkdir -p files && cat > files/runtime_hook.lua'

# También sirve el directorio externo privado:
cat build_payloads/runtime_hook.lua | \
  run-as com.deadnote sh -c 'mkdir -p /storage/emulated/0/Android/data/com.deadnote/files && \
  cat > /storage/emulated/0/Android/data/com.deadnote/files/runtime_hook.lua'
```

### Enviar la orden mientras la app está en ejecución

```bash
# Script desde archivo (relativo a files/ o ruta absoluta)
am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
  -n com.deadnote/.ReceptorTermux \
  --es orden LUA \
  --es arg1 files/runtime_hook.lua

# Script embebido en base64 (útil para pruebas rápidas)
am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
  -n com.deadnote/.ReceptorTermux \
  --es orden LUA_CODE \
  --es arg1 "$(base64 -w0 build_payloads/runtime_hook.lua)"

# Si run-as falla por permisos: guardar el script en files/ y ejecutarlo
am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
  -n com.deadnote/.ReceptorTermux \
  --es orden LUA_PUSH \
  --es arg1 runtime_hook.lua \
  --es arg2 "$(base64 -w0 build_payloads/runtime_hook.lua)"

# Limpiar hooks y resetear la guarda antes de recargar otro script
am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
  -n com.deadnote/.ReceptorTermux \
  --es orden LUA_UNHOOK
```

`LUA_PUSH` no necesita `run-as`: la propia app decodifica el base64, escribe el
archivo en `getFilesDir()` y lo ejecuta. Después se puede recargar sin reenviar
el código:

```bash
am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
  -n com.deadnote/.ReceptorTermux \
  --es orden LUA --es arg1 runtime_hook.lua
```

Órdenes disponibles:

| `orden` | `arg1` | `arg2` | Efecto |
|---|---|---|---|
| `LUA` | ruta `.lua` | — | Lee el archivo y ejecuta su Lua en el agente |
| `LUA_CODE` / `LUA_B64` | base64 | — | Decodifica y ejecuta el Lua |
| `LUA_PUSH` | nombre `.lua` | base64 | Guarda en `files/` y ejecuta |
| `LUA_UNHOOK` | — | — | Cierra la conexión (el agente restaura los hooks) y resetea la guarda Lua |

El resultado se registra como `[RenefLua]` y `RenefRuntime` en el servidor de
logs. Si el script falla, también se muestra un Toast con el error.
Los logs `RemoteLog.d` (`[bot]`, `[RenefDemo]`) solo aparecen con
`smalilog server --log-level DEBUG`; los `print()` de Lua salen como INFO.

Notas de comportamiento:

- La conexión se mantiene abierta a propósito. Si se cierra, el agente Renef
  elimina todos los hooks instalados (nativos y Java). `LUA_UNHOOK` aprovecha
  ese comportamiento: resetea la guarda Lua y cierra el socket; el comando
  `unhook all` del agente solo cubre hooks nativos.
- Si la app se reinicia o se fuerza su detención, hay que volver a enviar la
  orden `LUA`/`LUA_PUSH`.
- `LUA_CODE`/`LUA_B64` y los scripts leídos de archivo tienen un límite de
  30 KB; el protocolo `hexexec` del agente no acepta más.
- Para recargar un script sin reiniciar, envía `LUA_UNHOOK` y después `LUA` o
  `LUA_PUSH`. `runtime_hook.lua` tiene una guarda que evita duplicar hooks si
  se reenvía sin limpiar; si cambias el script, haz `LUA_UNHOOK` primero.
- El script se ejecuta en el proceso de la app; los `print()` de Lua salen por
  el socket y se reenvían a `smalilog server` con el prefijo `[RenefLua]`.
- `runtime_hook.lua` instala hooks sobre `demoRenefCheck`, `demoRenefLabel` y
  `prueba1`. Al pulsar **prueba1** se espera `false`, `runtime-hook` y las
  trazas de entrada/salida.
- En runtime, para booleanos usa `return JNI.boolean(false)`; el agente no
  interpreta un `return false` de Lua como cambio de retorno. Los strings sí
  funcionan con `return JNI.string("...")`.
- `LUA` acepta rutas absolutas legibles por la app o rutas relativas a
  `getFilesDir()` / `getExternalFilesDir()`. En Android 13+ no uses
  `/sdcard/Download` sin permiso de almacenamiento; usa `run-as` como arriba.

## 7d. Instalación genérica del agente en una APK descompilada

`smalilog renef install` convierte cualquier APK descompilada en una app con el
agente embebido, sin depender de las clases de `build_payloads`. El flujo de uso
completo, con compilación, firma, control, logs y problemas comunes, está en el
[manual del agente](agente.md).

```bash
apkeditor d -i app.apk -o ./app
smalilog renef install ./app --build -o app-instrumentada.apk
```

El instalador:

1. Copia `payload/lib/arm64-v8a/libagent.so` a `root/lib/arm64-v8a/` (o
   `lib/arm64-v8a/`).
2. Añade las clases Smali del puente en `smali/classes/com/smalilog/agent/`.
3. Inserta en el manifiesto un receptor exportado
   `com.smalilog.agent.AgentReceiver` con la action
   `com.smalilog.agent.ACTION`.
4. Agrega `android.permission.INTERNET` y
   `android:usesCleartextTraffic="true"` (idempotente, con respaldo externo
   `.<nombre>.smalilog-backup/` para no incluirlo en la APK).

Con `--build`, reconstruye y firma con `apkeditor b` y `apksigner`. El payload
solo incluye `arm64-v8a` y el agente requiere Android 24+; si la APK es universal,
conserva sus otras ABIs.

`--build` firma con la clave de `termux-apk-make` por defecto. Si la app original
usa otra firma, Android rechazará la actualización: desinstala la original o
pasa `--ks`/`--ks-pass` con tu clave.

### Control sin root

```bash
smalilog renef runtime ping --apk-dir ./app
smalilog renef runtime status --apk-dir ./app
smalilog renef runtime exec hook.lua --apk-dir ./app
smalilog renef runtime push hook.lua --apk-dir ./app
smalilog renef runtime unhook --apk-dir ./app
```

Internamente se ejecuta:

```bash
am broadcast -f 0x20 -a com.smalilog.agent.ACTION \
  -n com.demo/com.smalilog.agent.AgentReceiver \
  --es op EXEC --es b64 <lua_base64>
```

`-f 0x20` incluye paquetes detenidos (`FLAG_INCLUDE_STOPPED_PACKAGES`); aun así,
abre la app al menos una vez tras instalarla.

Órdenes: `PING` (receptor vivo), `STATUS` (agente conectado), `EXEC` (Lua en
base64), `PUSH` (guarda en `files/smalilog/` y ejecuta) y `UNHOOK` (cierra la
sesión; el agente restaura los hooks). El resultado se envía a
`http://127.0.0.1:9999/log` por defecto; usa `--host`/`--port` si el servidor
está en otro equipo.

### Límites y seguridad

- Scripts de hasta **256 KB** (el límite de 30 KB es solo del puente antiguo de
  `build_payloads`).
- El receptor es `exported="true"` y no declara permiso propio: cualquier app
  podría enviarle órdenes. Es aceptable para laboratorio/apps propias; para
  producción protege el receptor con `android:permission` de nivel `signature`
  o valida un token.
- Si el manifiesto usa `android:networkSecurityConfig`, revisa que permita
  tráfico HTTP local; `usesCleartextTraffic` puede ser ignorado.
- El agente se ejecuta dentro del proceso de la app; si la app se detiene, hay
  que volver a enviar el script. Tras un `force-stop`, abre la app antes de
  intentar el broadcast: Android puede no entregar órdenes a paquetes detenidos.
- Usa `--force` al reinstalar el payload si el árbol ya tiene un `libagent.so`
  o clases del puente con otro contenido.
- El manual del agente incluye la lista de comprobación y la tabla de errores:
  [`agente.md`](agente.md).

## 8. Interpretación del reporte

Cada receta aparece con uno de estos estados:

- `[aplicado]`: el Smali se parcheó (o se habría parcheado en `--dry-run`).
- `[omitido]`: la clase/método no existe o la receta no es traducible.
- `[fallido]`: se encontró el método pero la inyección Smali no pudo completarse.

Al final se muestra `Aplicadas · omitidas · fallidas` y las APIs de runtime
detectadas. Un script con muchos hooks nativos puede tener `aplicadas: 0` y aun
así ser válido para Renef real.

## 9. Limitaciones y buenas prácticas

- **Ofuscación**: las recetas dependen de nombres de clase/método. En APKs
  ofuscadas hay que localizar antes los símbolos (por ejemplo con
  `smalilog lms` o inspección manual).
- **Sobrecargas**: la firma JNI del script debe coincidir con la del Smali. Si no,
  el método se omite.
- **Constructores**: no se permite convertir `<init>`/`<clinit>` en stub; puede
  romper la inicialización de la app.
- **Retornos de objeto**: solo se admite `null` o un string constante. Devolver
  objetos creados en runtime no es posible de forma estática.
- **Semántica**: un `stub` reemplaza el cuerpo efectivo del método (el código
  original queda inalcanzable). No es una intercepción con `onEnter` real.
- **Seguridad**: usa esto solo en apps propias o con autorización explícita.

## 10. Pruebas

```bash
pytest -q tests/renef_test.py
make check
```

Los tests cubren el lector Lua, la clasificación de recetas, los stubs de
retorno (boolean, `long`, string y void), la observación, la idempotencia, el
`--dry-run`, el filtro `--only` y la integración del CLI.

## 11. Referencias

- Renef: <https://renef.io>
- Catálogo de hooks: <https://hook.renef.io>
- API Lua de referencia: `renef/RENEF_AI_PROMPT.md` (copia upstream de consulta)
- Inyector Smali: [`docs/injector.md`](injector.md)
- Servidor de logs: [`docs/server.md`](server.md)
