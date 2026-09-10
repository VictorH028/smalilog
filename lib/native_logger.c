#include <jni.h>

#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>

#define LOGGER_HOST "127.0.0.1"
#define LOGGER_PORT 9999

#define MAX_LOG_FIELD 16384
#define MAX_JSON_SIZE 65536
#define MAX_REQUEST_SIZE 73728

struct LogData {
    char *level;
    char *tag;
    char *message;
};

static char *copy_string(const char *src) {
    size_t len;
    char *dst;

    if (src == NULL) {
        return NULL;
    }

    len = strlen(src);

    if (len > MAX_LOG_FIELD) {
        len = MAX_LOG_FIELD;
    }

    dst = (char *)malloc(len + 1);

    if (dst == NULL) {
        return NULL;
    }

    memcpy(dst, src, len);
    dst[len] = '\0';

    return dst;
}

static void free_log_data(struct LogData *data) {
    if (data == NULL) {
        return;
    }

    free(data->level);
    free(data->tag);
    free(data->message);
    free(data);
}

/*
 * Escapa caracteres especiales para JSON.
 *
 * Ejemplo:
 *   Hola "mundo"
 *
 * Se convierte en:
 *   Hola \"mundo\"
 */
static int json_escape(
    char *dst,
    size_t dst_size,
    const char *src
) {
    size_t i;
    size_t pos = 0;
    unsigned char c;

    if (dst == NULL || src == NULL || dst_size == 0) {
        return -1;
    }

    for (i = 0; src[i] != '\0'; i++) {
        c = (unsigned char)src[i];

        if (c == '"' || c == '\\') {
            if (pos + 2 >= dst_size) {
                return -1;
            }

            dst[pos++] = '\\';
            dst[pos++] = (char)c;
        }
        else if (c == '\n') {
            if (pos + 2 >= dst_size) {
                return -1;
            }

            dst[pos++] = '\\';
            dst[pos++] = 'n';
        }
        else if (c == '\r') {
            if (pos + 2 >= dst_size) {
                return -1;
            }

            dst[pos++] = '\\';
            dst[pos++] = 'r';
        }
        else if (c == '\t') {
            if (pos + 2 >= dst_size) {
                return -1;
            }

            dst[pos++] = '\\';
            dst[pos++] = 't';
        }
        else if (c < 0x20) {
            /*
             * Otros caracteres de control:
             * se descartan para evitar JSON inválido.
             */
            continue;
        }
        else {
            if (pos + 1 >= dst_size) {
                return -1;
            }

            dst[pos++] = (char)c;
        }
    }

    dst[pos] = '\0';

    return (int)pos;
}

/*
 * Envía todos los bytes.
 *
 * send() puede enviar menos bytes de los solicitados.
 */
static int send_all(
    int sock,
    const char *buffer,
    size_t length
) {
    size_t total = 0;

    while (total < length) {
        ssize_t sent = send(
            sock,
            buffer + total,
            length - total,
            0
        );

        if (sent <= 0) {
            return -1;
        }

        total += (size_t)sent;
    }

    return 0;
}

static void *send_log_thread(void *arg) {
    struct LogData *data;
    int sock = -1;

    char escaped_level[MAX_LOG_FIELD * 2 + 1];
    char escaped_tag[MAX_LOG_FIELD * 2 + 1];
    char escaped_message[MAX_LOG_FIELD * 2 + 1];

    char json[MAX_JSON_SIZE];
    char request[MAX_REQUEST_SIZE];

    int json_len;
    int request_len;

    data = (struct LogData *)arg;

    if (data == NULL) {
        return NULL;
    }

    /*
     * Escapar antes de construir el JSON.
     */
    if (json_escape(
            escaped_level,
            sizeof(escaped_level),
            data->level
        ) < 0 ||
        json_escape(
            escaped_tag,
            sizeof(escaped_tag),
            data->tag
        ) < 0 ||
        json_escape(
            escaped_message,
            sizeof(escaped_message),
            data->message
        ) < 0) {

        free_log_data(data);
        return NULL;
    }

    json_len = snprintf(
        json,
        sizeof(json),
        "{\"level\":\"%s\",\"tag\":\"%s\",\"message\":\"%s\"}",
        escaped_level,
        escaped_tag,
        escaped_message
    );

    if (json_len < 0 ||
        (size_t)json_len >= sizeof(json)) {

        free_log_data(data);
        return NULL;
    }

    sock = socket(AF_INET, SOCK_STREAM, 0);

    if (sock < 0) {
        free_log_data(data);
        return NULL;
    }

    {
        struct sockaddr_in server;

        memset(&server, 0, sizeof(server));

        server.sin_family = AF_INET;
        server.sin_port = htons(LOGGER_PORT);

        if (inet_pton(
                AF_INET,
                LOGGER_HOST,
                &server.sin_addr
            ) != 1) {

            close(sock);
            free_log_data(data);
            return NULL;
        }

        if (connect(
                sock,
                (struct sockaddr *)&server,
                sizeof(server)
            ) < 0) {

            close(sock);
            free_log_data(data);
            return NULL;
        }
    }

    request_len = snprintf(
        request,
        sizeof(request),
        "POST /log HTTP/1.1\r\n"
        "Host: " LOGGER_HOST "\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s",
        json_len,
        json
    );

    if (request_len < 0 ||
        (size_t)request_len >= sizeof(request)) {

        close(sock);
        free_log_data(data);
        return NULL;
    }

    /*
     * Enviar toda la petición.
     */
    send_all(
        sock,
        request,
        (size_t)request_len
    );

    close(sock);

    free_log_data(data);

    return NULL;
}

JNIEXPORT void JNICALL
Java_com_deadnote_RemoteLogger_nativeSendLog(
    JNIEnv *env,
    jclass clazz,
    jstring jlevel,
    jstring jtag,
    jstring jmessage
) {
    const char *level;
    const char *tag;
    const char *message;

    struct LogData *data;
    pthread_t thread;

    (void)clazz;

    if (env == NULL ||
        jlevel == NULL ||
        jtag == NULL ||
        jmessage == NULL) {
        return;
    }

    level = (*env)->GetStringUTFChars(
        env,
        jlevel,
        NULL
    );

    tag = (*env)->GetStringUTFChars(
        env,
        jtag,
        NULL
    );

    message = (*env)->GetStringUTFChars(
        env,
        jmessage,
        NULL
    );

    if (level == NULL ||
        tag == NULL ||
        message == NULL) {

        if (level != NULL) {
            (*env)->ReleaseStringUTFChars(
                env,
                jlevel,
                level
            );
        }

        if (tag != NULL) {
            (*env)->ReleaseStringUTFChars(
                env,
                jtag,
                tag
            );
        }

        if (message != NULL) {
            (*env)->ReleaseStringUTFChars(
                env,
                jmessage,
                message
            );
        }

        return;
    }

    data = (struct LogData *)malloc(sizeof(struct LogData));

    if (data == NULL) {
        goto cleanup;
    }

    data->level = copy_string(level);
    data->tag = copy_string(tag);
    data->message = copy_string(message);

    if (data->level == NULL ||
        data->tag == NULL ||
        data->message == NULL) {

        free_log_data(data);
        data = NULL;
        goto cleanup;
    }

    if (pthread_create(
            &thread,
            NULL,
            send_log_thread,
            data
        ) == 0) {

        pthread_detach(thread);
        data = NULL;
    }
    else {
        free_log_data(data);
        data = NULL;
    }

cleanup:

    (*env)->ReleaseStringUTFChars(
        env,
        jlevel,
        level
    );

    (*env)->ReleaseStringUTFChars(
        env,
        jtag,
        tag
    );

    (*env)->ReleaseStringUTFChars(
        env,
        jmessage,
        message
    );
}
