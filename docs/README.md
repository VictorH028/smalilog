# Documentación de smalilog

Smalilog instrumenta APKs Android sin root: inyecta hooks en Smali, recibe logs
por HTTP y permite traducir scripts Lua de Renef. Este índice separa la guía de
uso de la documentación interna y del material histórico.

## Empieza aquí

| Documento | Para qué |
|---|---|
| [Guía rápida](guia-rapida.md) | Instalación, primer servidor y flujo completo con una APK. |
| [Referencia CLI](cli.md) | Comandos, opciones, códigos de salida y ejemplos. |
| [Configuración](configuration.md) | `config.toml`, variables `SMALILOG_*` y límites del servidor. |

## Instrumentación Smali

| Documento | Contenido |
|---|---|
| [Inyector Smali](injector.md) | Estructura interna, plan de registros y helpers de la app de prueba. |
| [Llamadas Smali](smali-call.md) | Tipos, firmas, `invoke-*`, registros y `move-result`. |

## Renef

| Documento | Contenido |
|---|---|
| [Puente Renef → Smali](renef.md) | Comandos, compatibilidad, presets y runtime por broadcast (§7c). |

## Servidor y app de prueba

| Documento | Contenido |
|---|---|
| [Servidor de logs](server.md) | Endpoint `POST /log` y ejemplos de petición. |
| [RemoteLog](android/RemoteLog.md) | API del logger, serialización y límites. |
| [Backup](android/Backup.md) | Respaldo del sandbox de la app de prueba. |
| [LifecycleTracker](android/LifecycleTracker.md) | Registro automático de actividades. |
| [Reflect](android/Reflect.md) | Wrapper de reflexión de la app de prueba. |
| [TracingClassLoader](android/TracingClassLoader.md) | ClassLoader de trazado. |

## Material histórico

Estos documentos se conservan como referencia, pero **no son la guía actual**:

- [Notas sueltas](legacy/notes.md)
- [Notas del paquete](legacy/package-notes.md)
- [Análisis estático antiguo](legacy/architecture-old.md)
- [Investigación sobre reflexión](legacy/Revisar.md)
- [Índice del material histórico](legacy/README.md)

## Estado de la documentación

- **Guía rápida y CLI**: pensadas para usuarios nuevos.
- **Inyector y Renef**: referencia técnica; verificar contra el código si algo
  no coincide con `--help`.
- **App de prueba**: describe las clases de `build_payloads/`, no una API
  estable del paquete Python.
