README.md
# Backup

Módulo de respaldo (*backup*) del sandbox de la aplicación . Empaqueta
todo el contenido del directorio privado de la app en un archivo `.tar.gz`
sin dependencias externas, escribiendo el formato **POSIX ustar** a mano y
comprimiendo con `GZIPOutputStream` de la JDK.

- El archivo resultante queda en una ruta accesible desde **Termux** o cualquier
gestor de archivos, lo que facilita la inspección, extracción y automatización
del respaldo desde el shell.

---

## ✨ Características

- 📦 Respaldo **completo** del sandbox (`context.getDataDir()`).
- 🗜️ Formato **`.tar.gz`** estándar, extraíble con `tar -xzf`.
- 🧩 **Cero dependencias externas** — no usa Apache Commons Compress ni tar4j.
- 🕒 Nombres con **timestamp** (`yyyy-MM-dd_HH-mm-ss`) para no sobrescribir.
- 📂 Guardado en `Download/BackupDir/` accesible desde Termux.
- 🔁 Recorrido recursivo de directorios y archivos.
- 📝 Logging vía `RemoteLog` con tag `LOG_BACKUP`.

---

## 📁 Estructura del proyecto

```

build_payloads/
└── src/
└── com/
└── deadnote/
├── Backup.java          ← este módulo
└── RemoteLog.java       ← logger (dependencia interna)

```

---

## 🚀 Uso

### Desde código Java

```java
import com.deadnote.Backup;

public final class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Genera el backup y lo registra en RemoteLog
        Backup.init(this);
    }
}
```

Generación manual (con acceso al File)

```java
try {
    File backup = Backup.create(context);
    Log.i("Backup", "Ruta: " + backup.getAbsolutePath());
} catch (IOException e) {
    Log.e("Backup", "Fallo al crear el respaldo", e);
}
```

Resultado esperado

```
/storage/emulated/0/Download/BackupDir/sandbox-full-2025-01-15_14-30-22.tar.gz
```

Verificación desde Termux

```bash
cd /storage/emulated/0/Download/BackupDir

# Listar contenido
tar -tzf sandbox-full-2025-01-15_14-30-22.tar.gz | head

# Extraer en carpeta temporal
mkdir -p /tmp/deadnote-restore
tar -xzf sandbox-full-2025-01-15_14-30-22.tar.gz -C /tmp/deadnote-restore
```

---

## 🧠 Cómo funciona

```
create(Context)
   │
   ├─► context.getDataDir()                     ← sandbox de la app
   │
   ├─► Download/BackupDir/                      ← destino externo
   │      └─► sandbox-full-<timestamp>.tar.gz
   │
   ├─► FileOutputStream
   │     └─► BufferedOutputStream
   │           └─► GZIPOutputStream             ← compresión
   │
   ├─► addFile() recursivo
   │     ├─► addDirectoryEntry()  → header tipo '5'
   │     └─► addRegularFile()     → header tipo '0' + datos + padding
   │
   └─► write(new byte[1024])                    ← EOF TAR (2 bloques nulos)
```

Formato TAR (POSIX ustar)

Cada entrada consta de un header de 512 bytes:

Offset Tamaño Campo Valor
```
0 100 name Ruta UTF-8
100 8 mode 0644
108 8 uid 0
116 8 gid 0
124 12 size Tamaño en octal
136 12 mtime Unix timestamp en octal
148 8 chksum Checksum octal %06o\0 
156 1 typeflag '0' archivo · '5' directorio
257 6 magic "ustar\0"
```


El contenido de cada archivo se rellena con ceros hasta el siguiente múltiplo
de 512. El archivo se cierra con 1024 bytes en cero (dos bloques nulos)
indicando EOF según el estándar TAR.

---

## 🔐 Permisos (AndroidManifest.xml)

```xml
<uses-permission
    android:name="android.permission.WRITE_EXTERNAL_STORAGE"
    android:maxSdkVersion="28" />

<uses-permission
    android:name="android.permission.READ_EXTERNAL_STORAGE"
    android:maxSdkVersion="32" />
```

## ⚠️ En Android 10+ con scoped storage, getExternalStoragePublicDirectory
puede no ser escribible. En Android 11+ WRITE_EXTERNAL_STORAGE está
deprecado. Para producción se recomienda migrar a MediaStore o al
Storage Access Framework (SAF).

---

## ⚠️ Limitaciones conocidas

# Limitación
1 No soporta rutas > 100 bytes (sin extensión GNU ././@LongLink).
2 No soporta archivos > 8 GB (campo size octal de 12 bytes).
3 No maneja symlinks, hardlinks, sockets ni FIFOs.
4 No valida cambios de tamaño entre header y lectura.
5 Respalda todo el sandbox sin filtrar (tokens, cookies, DBs).
6 El backup no está cifrado y es legible por cualquier app.
7 Sin verificación de espacio libre en disco.
8 El campo version de ustar (offset 263) queda en ceros.

---

## 🛡️ Recomendaciones

· 🔒 Añadir cifrado AES-GCM con clave derivada de KeyStore.
· 🧹 Excluir directorios no críticos: cache/, code_cache/, no_backup/.
· 📱 Migrar a MediaStore.Downloads para Android 10+.
· 📏 Añadir soporte GNU LongLink para rutas largas.
· 📊 Exponer callback de progreso y cancelación.
· 🧪 Añadir tests de extracción con tar real en CI.
· 🐛 Mejorar el mensaje de error en RemoteLog.e(...) para incluir la causa.

---

## 📚 Referencias

· POSIX ustar — Wikipedia
· GNU Tar Manual
· Android — Data and file storage overview
· Android — Scoped Storage

---

## 📄 Licencia




