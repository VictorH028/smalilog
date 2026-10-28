package com.deadnote;

import android.app.Activity;
import android.os.Bundle;

import java.io.File;
import android.content.Context;
import android.os.Environment;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.zip.GZIPOutputStream;

public final class Backup {

    private Backup() {
    }

    public static void init(Context context){
       try {
            File backup = Backup.create(context);

            RemoteLog.i(
                "DEADNOTE_BACKUP",
                "Backup creado: " + backup.getAbsolutePath()
        );

    } catch (java.io.IOException e) {

            RemoteLog.e("Error creando backup", "Error");

       } 
    }

    public static File create(Context context) throws IOException {

        // Sandbox completo de la aplicación.
        File dataDir = context.getDataDir();

        /*
         * Directorio accesible desde Termux:
         *
         * /storage/emulated/0/Download/DeadNote/
         */
        File backupDir = new File(
                Environment.getExternalStoragePublicDirectory(
                        Environment.DIRECTORY_DOWNLOADS
                ),
                "BackupDir"
        );

        if (!backupDir.exists() && !backupDir.mkdirs()) {
            throw new IOException(
                    "No se pudo crear: " + backupDir
            );
        }

        String timestamp =
                new SimpleDateFormat(
                        "yyyy-MM-dd_HH-mm-ss",
                        Locale.US
                ).format(new Date());

        File output = new File(
                backupDir,
                "sandbox-full-" +
                        timestamp +
                        ".tar.gz"
        );

        try (
                FileOutputStream fos =
                        new FileOutputStream(output);

                BufferedOutputStream bos =
                        new BufferedOutputStream(fos);

                GZIPOutputStream gzip =
                        new GZIPOutputStream(bos)
        ) {

            /*
             * Copiar TODO el contenido del sandbox.
             *
             * No hay lista de directorios.
             */
            File[] children = dataDir.listFiles();

            if (children != null) {

                for (File child : children) {

                    addFile(
                            child,
                            child.getName(),
                            gzip
                    );
                }
            }

            /*
             * Dos bloques TAR de cero indican EOF.
             */
            gzip.write(new byte[1024]);
        }

        return output;
    }

    private static void addFile(
            File file,
            String archivePath,
            GZIPOutputStream output)
            throws IOException {

        if (file.isDirectory()) {

            /*
             * Añadir entrada del directorio.
             */
            addDirectoryEntry(
                    archivePath,
                    file.lastModified() / 1000,
                    output
            );

            File[] children =
                    file.listFiles();

            if (children == null) {
                return;
            }

            for (File child : children) {

                addFile(
                        child,
                        archivePath +
                                "/" +
                                child.getName(),
                        output
                );
            }

            return;
        }

        if (file.isFile()) {

            addRegularFile(
                    file,
                    archivePath,
                    output
            );
        }
    }

    private static void addDirectoryEntry(
            String path,
            long modified,
            GZIPOutputStream output)
            throws IOException {

        byte[] header =
                createHeader(
                        path + "/",
                        0,
                        modified,
                        '5'
                );

        output.write(header);
    }

    private static void addRegularFile(
            File file,
            String path,
            GZIPOutputStream output)
            throws IOException {

        byte[] header =
                createHeader(
                        path,
                        file.length(),
                        file.lastModified() / 1000,
                        '0'
                );

        output.write(header);

        try (
                BufferedInputStream input =
                        new BufferedInputStream(
                                new FileInputStream(file)
                        )
        ) {

            byte[] buffer =
                    new byte[8192];

            int count;

            while ((count = input.read(buffer)) != -1) {
                output.write(
                        buffer,
                        0,
                        count
                );
            }
        }

        /*
         * TAR trabaja en bloques de 512 bytes.
         */
        long remainder =
                file.length() % 512;

        if (remainder != 0) {

            output.write(
                    new byte[
                            (int) (512 - remainder)
                    ]
            );
        }
    }

    private static byte[] createHeader(
            String path,
            long size,
            long modified,
            char type)
            throws IOException {

        byte[] header =
                new byte[512];

        byte[] name =
                path.getBytes(StandardCharsets.UTF_8);

        System.arraycopy(
                name,
                0,
                header,
                0,
                Math.min(
                        name.length,
                        100
                )
        );

        writeOctal(
                header,
                100,
                8,
                0644
        );

        writeOctal(
                header,
                108,
                8,
                0
        );

        writeOctal(
                header,
                116,
                8,
                0
        );

        writeOctal(
                header,
                124,
                12,
                size
        );

        writeOctal(
                header,
                136,
                12,
                modified
        );

        header[156] = (byte) type;

        byte[] magic =
                "ustar\0".getBytes(
                        StandardCharsets.US_ASCII
                );

        System.arraycopy(
                magic,
                0,
                header,
                257,
                magic.length
        );

        /*
         * Espacios reservados para checksum.
         */
        for (int i = 148; i < 156; i++) {
            header[i] = ' ';
        }

        long checksum = 0;

        for (byte b : header) {
            checksum += b & 0xff;
        }

        String checksumString =
                String.format(
                        Locale.US,
                        "%06o",
                        checksum
                );

        byte[] checksumBytes =
                checksumString.getBytes(
                        StandardCharsets.US_ASCII
                );

        System.arraycopy(
                checksumBytes,
                0,
                header,
                148,
                checksumBytes.length
        );
                
        header[154] = 0;
        header[155] = ' ';

        return header;
    }

    private static void writeOctal(
            byte[] buffer,
            int offset,
            int length,
            long value) {

        String octal =
                String.format(
                        Locale.US,
                        "%0" + (length - 1) + "o",
                        value
                );

        byte[] bytes =
                octal.getBytes(
                        StandardCharsets.US_ASCII
                );

        int start =
                offset +
                        length -
                        1 -
                        bytes.length;

        if (start < offset) {
            start = offset;
        }

        System.arraycopy(
                bytes,
                0,
                buffer,
                start,
                Math.min(
                        bytes.length,
                        length - 1
                )
        );

        buffer[
                offset + length - 1
        ] = 0;
    }
}
