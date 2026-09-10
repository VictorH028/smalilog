#include <jni.h>

#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <cstdlib>
#include <cstring>
#include <cstdio>

/* 1) Mejotar  escapes  en   joson  
 * 2)  send()  
 *
 *
 *
 *
 */


struct LogData {
    char* level;
    char* tag;
    char* message;
};

static char* copyString(const char* src) {
    if (src == nullptr) {
        return nullptr;
    }

    size_t len = strlen(src);

    char* dst = static_cast<char*>(malloc(len + 1));

    if (dst == nullptr) {
        return nullptr;
    }

    memcpy(dst, src, len + 1);

    return dst;
}

static void freeLogData(LogData* data) {
    if (data == nullptr) {
        return;
    }

    free(data->level);
    free(data->tag);
    free(data->message);
    free(data);
}

static void* sendLogThread(void* arg) {
    LogData* data = static_cast<LogData*>(arg);

    if (data == nullptr) {
        return nullptr;
    }

    int sock = socket(AF_INET, SOCK_STREAM, 0);

    if (sock < 0) {
        freeLogData(data);
        return nullptr;
    }

    struct sockaddr_in server {};

    server.sin_family = AF_INET;
    server.sin_port = htons(9999);

    if (inet_pton(AF_INET, "127.0.0.1", &server.sin_addr) != 1) {
        close(sock);
        freeLogData(data);
        return nullptr;
    }

    if (connect(
            sock,
            reinterpret_cast<struct sockaddr*>(&server),
            sizeof(server)
        ) < 0) {

        close(sock);
        freeLogData(data);
        return nullptr;
    }

    char json[4096];

    int jsonLen = snprintf(
        json,
        sizeof(json),
        "{\"level\":\"%s\",\"tag\":\"%s\",\"message\":\"%s\"}",
        data->level,
        data->tag,
        data->message
    );

    if (jsonLen < 0 || jsonLen >= static_cast<int>(sizeof(json))) {
        close(sock);
        freeLogData(data);
        return nullptr;
    }

    char request[8192];

    int requestLen = snprintf(
        request,
        sizeof(request),
        "POST /log HTTP/1.1\r\n"
        "Host: 127.0.0.1\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s",
        jsonLen,
        json
    );

    if (requestLen > 0 &&
        requestLen < static_cast<int>(sizeof(request))) {

        send(sock, request, requestLen, 0);
    }

    close(sock);

    freeLogData(data);

    return nullptr;
}

extern "C" {

JNIEXPORT void JNICALL
Java_com_deadnote_RemoteLogger_nativeSendLog(
    JNIEnv* env,
    jclass clazz,
    jstring jlevel,
    jstring jtag,
    jstring jmessage) {

    if (env == nullptr ||
        jlevel == nullptr ||
        jtag == nullptr ||
        jmessage == nullptr) {
        return;
    }

    const char* level =
        env->GetStringUTFChars(jlevel, nullptr);

    const char* tag =
        env->GetStringUTFChars(jtag, nullptr);

    const char* message =
        env->GetStringUTFChars(jmessage, nullptr);

    if (level == nullptr || tag == nullptr || message == nullptr) {

        if (level != nullptr) {
            env->ReleaseStringUTFChars(jlevel, level);
        }

        if (tag != nullptr) {
            env->ReleaseStringUTFChars(jtag, tag);
        }

        if (message != nullptr) {
            env->ReleaseStringUTFChars(jmessage, message);
        }

        return;
    }

    LogData* data = static_cast<LogData*>(malloc(sizeof(LogData)));

    if (data == nullptr) {
        env->ReleaseStringUTFChars(jlevel, level);
        env->ReleaseStringUTFChars(jtag, tag);
        env->ReleaseStringUTFChars(jmessage, message);
        return;
    }

    data->level = copyString(level);
    data->tag = copyString(tag);
    data->message = copyString(message);

    env->ReleaseStringUTFChars(jlevel, level);
    env->ReleaseStringUTFChars(jtag, tag);
    env->ReleaseStringUTFChars(jmessage, message);

    if (data->level == nullptr ||
        data->tag == nullptr ||
        data->message == nullptr) {

        freeLogData(data);
        return;
    }

    pthread_t thread;

    if (pthread_create(&thread, nullptr, sendLogThread, data) == 0) {
        pthread_detach(thread);
    } else {
        freeLogData(data);
    }
}

}
