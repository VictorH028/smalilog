package com.deadnote;

import android.content.Context;
import com.deadnote.RemoteLogger;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/**
 * Clase de utilidad para gestionar el directorio de caché de la aplicación.
 * Permite obtener la ruta, listar su contenido y realizar copias de seguridad.
 */
public class CacheManager {

    private static final String TAG = "CACHE";

    private final Context context;

    public CacheManager(Context context) {
        this.context = context.getApplicationContext();
    }

    // =========================================================
    // 1️⃣ OBTENER LA RUTA DEL CACHÉ
    // =========================================================

    /**
     * Devuelve la ruta absoluta del directorio de caché interno.
     *
     * @return String con la ruta, o null si no se pudo obtener.
     */
    public String obtenerRutaCache() {
        File cacheDir = context.getCacheDir();
        if (cacheDir == null) {
            RemoteLogger.d(TAG, "No se pudo obtener el directorio de caché.");
            return null;
        }
        return cacheDir.getAbsolutePath();
    }

    /**
     * Devuelve el objeto File del directorio de caché.
     * Útil si necesitas trabajar directamente con él.
     */
    public File obtenerDirectorioCache() {
        return context.getCacheDir();
    }

    // =========================================================
    // 2️⃣ LISTAR EL CONTENIDO DEL CACHÉ
    // =========================================================

    /**
     * Devuelve una lista con los nombres de todos los archivos
     * que se encuentran directamente en el directorio de caché.
     *
     * @return List<String> con los nombres de archivo.
     */
    public List<String> listarContenidoCache() {
        List<String> nombres = new ArrayList<>();
        File cacheDir = context.getCacheDir();

        if (cacheDir == null || !cacheDir.exists()) {
            RemoteLogger.d(TAG, "El directorio de caché no existe.");
            return nombres;
        }

        File[] archivos = cacheDir.listFiles();
        if (archivos == null) return nombres;

        for (File archivo : archivos) {
            nombres.add(archivo.getName());
        }
        return nombres;
    }

    /**
     * Devuelve una lista detallada con información de cada archivo:
     * nombre, tamaño y si es carpeta o archivo.
     */
    public List<String> listarContenidoDetallado() {
        List<String> detalle = new ArrayList<>();
        File cacheDir = context.getCacheDir();

        if (cacheDir == null || !cacheDir.exists()) return detalle;

        File[] archivos = cacheDir.listFiles();
        if (archivos == null) return detalle;

        for (File archivo : archivos) {
            String tipo = archivo.isDirectory() ? "[DIR] " : "[FILE]";
            String info = tipo + " " + archivo.getName()
                    + " (" + archivo.length() + " bytes)";
            detalle.add(info);
        }
        return detalle;
    }

    // =========================================================
    // 3️⃣ HACER COPIA DE SEGURIDAD DEL CACHÉ       
    // =========================================================

    /**
     * Realiza una copia de seguridad completa del contenido del caché
     * en la carpeta de archivos internos de la app, dentro de
     * un subdirectorio llamado "backup_cache".
     *
     * @return La ruta de la carpeta de backup, o null si falló.
     */
    public String hacerCopiaDeSeguridad() {
        File cacheDir = context.getCacheDir();
        if (cacheDir == null || !cacheDir.exists()) {
            RemoteLogger.d(TAG, "No hay caché para respaldar.");
            return null;
        }

        // Carpeta destino: /data/data/<paquete>/files/backup_cache
        // En lugar de: context.getFilesDir()
        File backupDir = new File(context.getExternalFilesDir(null), "backup_cache");
        // File backupDir = new File(context.getFilesDir(), "backup_cache");
        if (!backupDir.exists() && !backupDir.mkdirs()) {
            RemoteLogger.d(TAG, "No se pudo crear la carpeta de backup.");
            return null;
        }

        try {
            copiarDirectorio(cacheDir, backupDir);
            RemoteLogger.d(TAG, "Copia de seguridad completada en: " + backupDir.getAbsolutePath());
            return backupDir.getAbsolutePath();
        } catch (IOException e) {
            RemoteLogger.d(TAG, "Error al copiar el caché: ");// + e.getMessage(), e);
            return null;
        }
    }

    /**
     * Realiza la copia de seguridad añadiendo un sufijo con la fecha/hora,
     * útil para mantener varias copias históricas.
     *
     * @return La ruta de la carpeta de backup, o null si falló.
     */
    public String hacerCopiaDeSeguridadConFecha() {
        File cacheDir = context.getCacheDir();
        if (cacheDir == null || !cacheDir.exists()) {
            RemoteLogger.d(TAG, "No hay caché para respaldar.");
            return null;
        }

        String marca = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault())
                .format(new Date());

        File backupDir = new File(context.getFilesDir(), "backup_cache_" + marca);
        if (!backupDir.exists() && !backupDir.mkdirs()) {
            RemoteLogger.d(TAG, "No se pudo crear la carpeta de backup.");
            return null;
        }

        try {
            copiarDirectorio(cacheDir, backupDir);
            RemoteLogger.d(TAG, "Backup con fecha creado en: " + backupDir.getAbsolutePath());
            return backupDir.getAbsolutePath();
        } catch (IOException e) {
            RemoteLogger.d(TAG, "Error al copiar el caché: " + e.getMessage()); //, e);
            return null;
        }
    }

    // =========================================================
    // MÉTODOS AUXILIARES
    // =========================================================

    /**
     * Copia recursivamente el contenido de un directorio a otro.
     */
    private void copiarDirectorio(File origen, File destino) throws IOException {
        if (origen.isDirectory()) {
            if (!destino.exists() && !destino.mkdirs()) {
                throw new IOException("No se pudo crear: " + destino.getAbsolutePath());
            }
            File[] hijos = origen.listFiles();
            if (hijos != null) {
                for (File hijo : hijos) {
                    copiarDirectorio(hijo, new File(destino, hijo.getName()));
                }
            }
        } else {
            copiarArchivo(origen, destino);
        }
    }

    /**
     * Copia un archivo byte a byte.
     */
    private void copiarArchivo(File origen, File destino) throws IOException {
        try (FileInputStream in = new FileInputStream(origen);
             FileOutputStream out = new FileOutputStream(destino)) {

            byte[] buffer = new byte[4096];
            int leidos;
            while ((leidos = in.read(buffer)) != -1) {
                out.write(buffer, 0, leidos);
            }
            out.flush();
        }
    
}

public static void CacheInfo(Context context) {
    CacheManager cacheManager = new CacheManager(context);

    // 1. Obtener la ruta
    String ruta = cacheManager.obtenerRutaCache();
    RemoteLogger.d("APP", "Caché en: " + ruta);

    // 2. Listar contenido
    List<String> archivos = cacheManager.listarContenidoCache();
    for (String a : archivos) {
        RemoteLogger.d("APP", "Archivo: " + a);
    }

    // 3. Hacer copia de seguridad (sobrescribiendo la anterior)
    String rutaBackup = cacheManager.hacerCopiaDeSeguridad();
    RemoteLogger.d("APP", "Backup en: " + rutaBackup);

    // 3b. Hacer copia con marca de tiempo
    String rutaBackupFecha = cacheManager.hacerCopiaDeSeguridadConFecha();

}}

