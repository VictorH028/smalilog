package com.deadnote;

import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.ProviderInfo;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.os.ParcelFileDescriptor;
import android.provider.DocumentsContract;
import android.provider.DocumentsContract.Document;
import android.provider.DocumentsContract.Root;
import android.provider.DocumentsProvider;
import android.webkit.MimeTypeMap;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

public class TermuxDocumentsProviderRoot extends DocumentsProvider {

    public static final String AUTHORITY =
            "com.deadnote.documents";

    private static final String[] DEFAULT_ROOT_PROJECTION = {
            Root.COLUMN_ROOT_ID,
            Root.COLUMN_MIME_TYPES,
            Root.COLUMN_FLAGS,
            Root.COLUMN_ICON,
            Root.COLUMN_TITLE,
            Root.COLUMN_SUMMARY,
            Root.COLUMN_DOCUMENT_ID
    };

    private static final String[] DEFAULT_DOCUMENT_PROJECTION = {
            Document.COLUMN_DOCUMENT_ID,
            Document.COLUMN_MIME_TYPE,
            Document.COLUMN_DISPLAY_NAME,
            Document.COLUMN_LAST_MODIFIED,
            Document.COLUMN_FLAGS,
            Document.COLUMN_SIZE
    };

    private String packageName;
    private File dataDir;
    private String rootPath;

    @Override
    public void attachInfo(Context context, ProviderInfo info) {
        super.attachInfo(context, info);

        packageName = context.getPackageName();

        /*
         * Normalmente:
         *
         * /data/user/0/com.deadnote
         *
         * En algunos dispositivos puede resolverse como:
         *
         * /data/data/com.deadnote
         */
        dataDir = context.getDataDir();

        try {
            rootPath = dataDir.getCanonicalPath();
        } catch (IOException e) {
            rootPath = dataDir.getAbsolutePath();
        }
    }

    @Override
    public boolean onCreate() {
        return true;
    }

    /**
     * Convierte un Document ID en un archivo real.
     *
     * Root:
     *
     *     com.deadnote
     *
     * Archivo:
     *
     *     com.deadnote/files/test.txt
     */
    private File getFileForDocId(String documentId)
            throws FileNotFoundException {

        if (documentId == null) {
            throw new FileNotFoundException("null documentId");
        }

        if (documentId.equals(packageName)) {
            return dataDir;
        }

        String prefix = packageName + "/";

        if (!documentId.startsWith(prefix)) {
            throw new FileNotFoundException(
                    "Outside provider root: " + documentId
            );
        }

        String relativePath = documentId.substring(prefix.length());

        if (relativePath.isEmpty()) {
            return dataDir;
        }

        /*
         * Evitar:
         *
         * ../
         * ../../
         * etc.
         */
        File candidate = new File(dataDir, relativePath);

        try {
            String canonical = candidate.getCanonicalPath();

            if (!canonical.equals(rootPath)
                    && !canonical.startsWith(rootPath + File.separator)) {
                throw new FileNotFoundException(
                        "Path outside sandbox: " + documentId
                );
            }

            return candidate;

        } catch (IOException e) {
            throw new FileNotFoundException(
                    "Unable to resolve: " + documentId
            );
        }
    }

    private String getDocumentId(File file)
            throws IOException {

        String canonical = file.getCanonicalPath();

        if (canonical.equals(rootPath)) {
            return packageName;
        }

        if (!canonical.startsWith(rootPath + File.separator)) {
            throw new IOException("File outside sandbox");
        }

        String relative =
                canonical.substring(rootPath.length() + 1);

        return packageName + "/" + relative;
    }

    @Override
    public Cursor queryRoots(String[] projection) {

        ApplicationInfo app =
                getContext().getApplicationInfo();

        String title =
                app.loadLabel(
                        getContext().getPackageManager()
                ).toString();

        MatrixCursor result =
                new MatrixCursor(
                        projection != null
                                ? projection
                                : DEFAULT_ROOT_PROJECTION
                );

        MatrixCursor.RowBuilder row =
                result.newRow();

        row.add(
                Root.COLUMN_ROOT_ID,
                packageName
        );

        row.add(
                Root.COLUMN_DOCUMENT_ID,
                packageName
        );

        row.add(
                Root.COLUMN_TITLE,
                title
        );

        row.add(
                Root.COLUMN_SUMMARY,
                "Private app data"
        );

        row.add(
                Root.COLUMN_MIME_TYPES,
                "*/*"
        );

        row.add(
                Root.COLUMN_FLAGS,
                Root.FLAG_SUPPORTS_CREATE
                        | Root.FLAG_SUPPORTS_IS_CHILD
        );

        row.add(
                Root.COLUMN_ICON,
                app.icon
        );

        return result;
    }

    @Override
    public Cursor queryDocument(
            String documentId,
            String[] projection)
            throws FileNotFoundException {

        MatrixCursor result =
                new MatrixCursor(
                        projection != null
                                ? projection
                                : DEFAULT_DOCUMENT_PROJECTION
                );

        includeFile(result, documentId);

        return result;
    }

    @Override
    public Cursor queryChildDocuments(
            String parentDocumentId,
            String[] projection,
            String sortOrder)
            throws FileNotFoundException {

        MatrixCursor result =
                new MatrixCursor(
                        projection != null
                                ? projection
                                : DEFAULT_DOCUMENT_PROJECTION
                );

        File parent =
                getFileForDocId(parentDocumentId);

        if (!parent.isDirectory()) {
            return result;
        }

        File[] children = parent.listFiles();

        if (children == null) {
            return result;
        }

        for (File child : children) {

            try {
                String documentId =
                        getDocumentId(child);

                includeFile(
                        result,
                        documentId
                );

            } catch (IOException ignored) {
            }
        }

        return result;
    }

    private void includeFile(
            MatrixCursor result,
            String documentId)
            throws FileNotFoundException {

        File file =
                getFileForDocId(documentId);

        MatrixCursor.RowBuilder row =
                result.newRow();

        row.add(
                Document.COLUMN_DOCUMENT_ID,
                documentId
        );

        row.add(
                Document.COLUMN_DISPLAY_NAME,
                file.equals(dataDir)
                        ? packageName
                        : file.getName()
        );

        row.add(
                Document.COLUMN_MIME_TYPE,
                getMimeType(file)
        );

        row.add(
                Document.COLUMN_SIZE,
                file.isFile()
                        ? file.length()
                        : 0L
        );

        row.add(
                Document.COLUMN_LAST_MODIFIED,
                file.lastModified()
        );

        int flags = 0;

        if (file.isDirectory()) {

            if (file.canWrite()) {
                flags |=
                        Document.FLAG_DIR_SUPPORTS_CREATE;
            }

        } else if (file.canWrite()) {

            flags |=
                    Document.FLAG_SUPPORTS_WRITE;
        }

        if (!file.equals(dataDir)
                && file.getParentFile() != null
                && file.getParentFile().canWrite()) {

            flags |=
                    Document.FLAG_SUPPORTS_DELETE;

            flags |=
                    Document.FLAG_SUPPORTS_RENAME;
        }

        row.add(
                Document.COLUMN_FLAGS,
                flags
        );
    }

    @Override
    public ParcelFileDescriptor openDocument(
            String documentId,
            String mode,
            CancellationSignal signal)
            throws FileNotFoundException {

        File file =
                getFileForDocId(documentId);

        if (file.isDirectory()) {
            throw new FileNotFoundException(
                    "Cannot open directory"
            );
        }

        return ParcelFileDescriptor.open(
                file,
                parseFileMode(mode)
        );
    }

    private static int parseFileMode(String mode) {

        switch (mode) {

            case "r":
                return ParcelFileDescriptor.MODE_READ_ONLY;

            case "w":
            case "wt":
                return ParcelFileDescriptor.MODE_WRITE_ONLY
                        | ParcelFileDescriptor.MODE_CREATE
                        | ParcelFileDescriptor.MODE_TRUNCATE;

            case "wa":
                return ParcelFileDescriptor.MODE_WRITE_ONLY
                        | ParcelFileDescriptor.MODE_CREATE
                        | ParcelFileDescriptor.MODE_APPEND;

            case "rw":
                return ParcelFileDescriptor.MODE_READ_WRITE
                        | ParcelFileDescriptor.MODE_CREATE;

            case "rwt":
                return ParcelFileDescriptor.MODE_READ_WRITE
                        | ParcelFileDescriptor.MODE_CREATE
                        | ParcelFileDescriptor.MODE_TRUNCATE;

            default:
                throw new IllegalArgumentException(
                        "Invalid mode: " + mode
                );
        }
    }

    @Override
    public String createDocument(
            String parentDocumentId,
            String mimeType,
            String displayName)
            throws FileNotFoundException {

        File parent =
                getFileForDocId(parentDocumentId);

        if (!parent.isDirectory()
                || !parent.canWrite()) {

            throw new FileNotFoundException(
                    "Cannot write to " + parentDocumentId
            );
        }

        /*
         * Evitar nombres con rutas.
         */
        if (displayName == null
                || displayName.isEmpty()
                || displayName.contains("/")
                || displayName.equals(".")
                || displayName.equals("..")) {

            throw new FileNotFoundException(
                    "Invalid filename"
            );
        }

        File target =
                new File(parent, displayName);

        if (target.exists()) {

            int n = 2;

            String base = displayName;

            while (target.exists()) {
                target = new File(
                        parent,
                        base + " (" + n++ + ")"
                );
            }
        }

        try {

            boolean created;

            if (Document.MIME_TYPE_DIR.equals(mimeType)) {
                created = target.mkdir();
            } else {
                created = target.createNewFile();
            }

            if (!created) {
                throw new IOException(
                        "Creation failed"
                );
            }

            return getDocumentId(target);

        } catch (IOException e) {

            throw new FileNotFoundException(
                    "Failed to create " + displayName
            );
        }
    }

    @Override
    public void deleteDocument(
            String documentId)
            throws FileNotFoundException {

        File file =
                getFileForDocId(documentId);

        if (file.equals(dataDir)) {
            throw new FileNotFoundException(
                    "Cannot delete provider root"
            );
        }

        if (!deleteRecursively(file)) {
            throw new FileNotFoundException(
                    "Failed to delete " + documentId
            );
        }
    }

    private static boolean deleteRecursively(
            File file) {

        if (file.isDirectory()) {

            File[] children =
                    file.listFiles();

            if (children != null) {

                for (File child : children) {

                    if (!deleteRecursively(child)) {
                        return false;
                    }
                }
            }
        }

        return file.delete();
    }

    @Override
    public String renameDocument(
            String documentId,
            String displayName)
            throws FileNotFoundException {

        File source =
                getFileForDocId(documentId);

        if (source.equals(dataDir)) {
            throw new FileNotFoundException(
                    "Cannot rename provider root"
            );
        }

        if (displayName == null
                || displayName.isEmpty()
                || displayName.contains("/")
                || displayName.equals(".")
                || displayName.equals("..")) {

            throw new FileNotFoundException(
                    "Invalid filename"
            );
        }

        File target =
                new File(
                        source.getParentFile(),
                        displayName
                );

        if (target.exists()) {
            throw new FileNotFoundException(
                    "Target already exists"
            );
        }

        if (!source.renameTo(target)) {
            throw new FileNotFoundException(
                    "Rename failed"
            );
        }

        try {
            return getDocumentId(target);
        } catch (IOException e) {
            throw new FileNotFoundException(
                    "Unable to create document ID"
            );
        }
    }

    @Override
    public String moveDocument(
            String sourceDocumentId,
            String sourceParentDocumentId,
            String targetParentDocumentId)
            throws FileNotFoundException {

        File source =
                getFileForDocId(sourceDocumentId);

        File targetParent =
                getFileForDocId(targetParentDocumentId);

        if (!targetParent.isDirectory()
                || !targetParent.canWrite()) {

            throw new FileNotFoundException(
                    "Target is not writable"
            );
        }

        File target =
                new File(
                        targetParent,
                        source.getName()
                );

        if (target.exists()) {
            throw new FileNotFoundException(
                    "Target already exists"
            );
        }

        if (!source.renameTo(target)) {
            throw new FileNotFoundException(
                    "Move failed"
            );
        }

        try {
            return getDocumentId(target);
        } catch (IOException e) {
            throw new FileNotFoundException(
                    "Unable to create document ID"
            );
        }
    }

    @Override
    public String getDocumentType(
            String documentId)
            throws FileNotFoundException {

        return getMimeType(
                getFileForDocId(documentId)
        );
    }

    @Override
    public boolean isChildDocument(
            String parentDocumentId,
            String documentId) {

        if (parentDocumentId.equals(documentId)) {
            return false;
        }

        return documentId.startsWith(
                parentDocumentId + "/"
        );
    }

    private static String getMimeType(
            File file) {

        if (file.isDirectory()) {
            return Document.MIME_TYPE_DIR;
        }

        String name = file.getName();

        int dot =
                name.lastIndexOf('.');

        if (dot >= 0) {

            String extension =
                    name.substring(dot + 1)
                            .toLowerCase();

            String mime =
                    MimeTypeMap
                            .getSingleton()
                            .getMimeTypeFromExtension(
                                    extension
                            );

            if (mime != null) {
                return mime;
            }
        }

        return "application/octet-stream";
    }
}
