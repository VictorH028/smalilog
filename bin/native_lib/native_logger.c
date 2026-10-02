#include <jni.h>

#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <poll.h>
#include <pthread.h>
#include <sys/socket.h>
#include <unistd.h>

#include <errno.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DEFAULT_HOST "127.0.0.1"
#define DEFAULT_PORT 9999

#define MAX_LOG_FIELD 16384
#define QUEUE_CAPACITY 256
#define MAX_BATCH_ITEMS 32
#define MAX_BATCH_BYTES (128 * 1024)

#define CONNECT_TIMEOUT_MS 1500
#define IO_TIMEOUT_MS 2000

struct LogData {
  char *level;
  char *tag;
  char *message;
};

struct Buffer {
  char *data;
  size_t len;
  size_t cap;
};

/* -------- Estado global (protegido por g_mutex) -------- */

static pthread_mutex_t g_mutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t g_cond = PTHREAD_COND_INITIALIZER;

static pthread_t g_worker;
static int g_worker_running = 0;
static int g_shutdown = 0;

static char g_host[64] = DEFAULT_HOST;
static int g_port = DEFAULT_PORT;

static struct LogData *g_queue[QUEUE_CAPACITY];
static size_t g_head;
static size_t g_count;

static _Atomic long g_dropped; /* logs perdidos (cola llena o fallo de red) */

/* -------- Utilidades -------- */

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

static int buf_reserve(struct Buffer *b, size_t extra) {
  char *p;
  size_t newcap;

  if (b->len + extra + 1 <= b->cap) {
    return 0;
  }

  newcap = (b->cap > 0) ? b->cap : 512;
  while (newcap < b->len + extra + 1) {
    newcap *= 2;
  }

  p = (char *)realloc(b->data, newcap);
  if (p == NULL) {
    return -1;
  }

  b->data = p;
  b->cap = newcap;

  return 0;
}

static int buf_append(struct Buffer *b, const char *src, size_t n) {
  if (buf_reserve(b, n) != 0) {
    return -1;
  }

  memcpy(b->data + b->len, src, n);
  b->len += n;
  b->data[b->len] = '\0';

  return 0;
}

static int buf_append_str(struct Buffer *b, const char *src) {
  return buf_append(b, src, strlen(src));
}

/*
 * Escapa y añade un string como literal JSON ("...").
 * Buffer dinámico: nunca se pierde un log por falta de espacio.
 */
static int buf_append_json_string(struct Buffer *b, const char *src) {
  size_t i;

  if (buf_append(b, "\"", 1) != 0) {
    return -1;
  }

  for (i = 0; src[i] != '\0'; i++) {
    unsigned char c = (unsigned char)src[i];
    const char *esc = NULL;

    switch (c) {
    case '"':
      esc = "\\\"";
      break;
    case '\\':
      esc = "\\\\";
      break;
    case '\n':
      esc = "\\n";
      break;
    case '\r':
      esc = "\\r";
      break;
    case '\t':
      esc = "\\t";
      break;
    default:
      if (c < 0x20) {
        continue; /* otros caracteres de control: descartados */
      }
      if (buf_append(b, (const char *)&c, 1) != 0) {
        return -1;
      }
      continue;
    }

    if (buf_append(b, esc, 2) != 0) {
      return -1;
    }
  }

  return buf_append(b, "\"", 1);
}

/* -------- Red -------- */

static int connect_with_timeout(const char *host, int port) {
  struct sockaddr_in server;
  struct timeval tv;
  int sock;
  int flags;
  int rc;

  memset(&server, 0, sizeof(server));
  server.sin_family = AF_INET;
  server.sin_port = htons((uint16_t)port);

  if (inet_pton(AF_INET, host, &server.sin_addr) != 1) {
    return -1;
  }

  sock = socket(AF_INET, SOCK_STREAM, 0);
  if (sock < 0) {
    return -1;
  }

  /* Conexión no bloqueante + poll: nunca colgamos CONNECT_TIMEOUT_MS */
  flags = fcntl(sock, F_GETFL, 0);
  if (flags >= 0) {
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);
  }

  rc = connect(sock, (struct sockaddr *)&server, sizeof(server));

  if (rc != 0 && errno == EINPROGRESS) {
    struct pollfd pfd;
    int so_error;
    socklen_t optlen = sizeof(so_error);

    pfd.fd = sock;
    pfd.events = POLLOUT;

    rc = poll(&pfd, 1, CONNECT_TIMEOUT_MS);
    if (rc <= 0 ||
        getsockopt(sock, SOL_SOCKET, SO_ERROR, &so_error, &optlen) != 0 ||
        so_error != 0) {
      close(sock);
      return -1;
    }
  } else if (rc != 0) {
    close(sock);
    return -1;
  }

  /* Volver a modo bloqueante, con timeouts de E/S */
  if (flags >= 0) {
    fcntl(sock, F_SETFL, flags);
  }

  tv.tv_sec = IO_TIMEOUT_MS / 1000;
  tv.tv_usec = 0;
  setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));
  setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

  /* El lote sale de una pieza; sin Nagle */
  flags = 1;
  setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, &flags, sizeof(flags));

  return sock;
}

static int send_all(int sock, const char *buffer, size_t length) {
  size_t total = 0;

  while (total < length) {
    /* MSG_NOSIGNAL: que un RST del servidor no mate el proceso (SIGPIPE) */
    ssize_t sent = send(sock, buffer + total, length - total, MSG_NOSIGNAL);

    if (sent <= 0) {
      return -1;
    }

    total += (size_t)sent;
  }

  return 0;
}

/* -------- Construcción del lote -------- */

static int build_batch_json(struct LogData **items, size_t count,
                            struct Buffer *out) {
  size_t i;

  if (buf_append(out, "[", 1) != 0) {
    return -1;
  }

  for (i = 0; i < count; i++) {
    if (i > 0 && buf_append(out, ",", 1) != 0) {
      return -1;
    }

    if (buf_append(out, "{\"level\":", 9) != 0 ||
        buf_append_json_string(out, items[i]->level ? items[i]->level : "") !=
            0 ||
        buf_append(out, ",\"tag\":", 7) != 0 ||
        buf_append_json_string(out, items[i]->tag ? items[i]->tag : "") != 0 ||
        buf_append(out, ",\"message\":", 11) != 0 ||
        buf_append_json_string(out, items[i]->message ? items[i]->message
                                                      : "") != 0 ||
        buf_append(out, "}", 1) != 0) {
      return -1;
    }
  }

  return buf_append(out, "]", 1);
}

static int build_request(const char *host, const struct Buffer *json,
                         struct Buffer *out) {
  char content_length[32];

  snprintf(content_length, sizeof(content_length), "%zu", json->len);

  if (buf_append_str(out, "POST /log HTTP/1.1\r\n") != 0 ||
      buf_append_str(out, "Host: ") != 0 || buf_append_str(out, host) != 0 ||
      buf_append_str(out, "\r\n") != 0 ||
      buf_append_str(out, "Content-Type: application/json\r\n") != 0 ||
      buf_append_str(out, "Content-Length: ") != 0 ||
      buf_append_str(out, content_length) != 0 ||
      buf_append_str(out, "\r\nConnection: close\r\n\r\n") != 0) {
    return -1;
  }

  return buf_append(out, json->data, json->len);
}

/* -------- Worker único -------- */

static void *worker_main(void *arg) {
  struct LogData *batch[MAX_BATCH_ITEMS];
  struct Buffer json = {NULL, 0, 0};
  struct Buffer request = {NULL, 0, 0};

  (void)arg;

  for (;;) {
    size_t count = 0;
    size_t bytes = 0;
    size_t i;
    char host[64];
    int port;

    pthread_mutex_lock(&g_mutex);

    while (g_count == 0 && !g_shutdown) {
      pthread_cond_wait(&g_cond, &g_mutex);
    }

    if (g_count == 0 && g_shutdown) {
      pthread_mutex_unlock(&g_mutex);
      break; /* apagado con cola vacía: flush garantizado */
    }

    /* Snapshot de la configuración bajo el mutex */
    strncpy(host, g_host, sizeof(host) - 1);
    host[sizeof(host) - 1] = '\0';
    port = g_port;

    while (g_count > 0 && count < MAX_BATCH_ITEMS && bytes < MAX_BATCH_BYTES) {
      batch[count] = g_queue[g_head];
      g_queue[g_head] = NULL;
      g_head = (g_head + 1) % QUEUE_CAPACITY;
      g_count--;

      bytes += strlen(batch[count]->message) + 64;
      count++;
    }

    pthread_mutex_unlock(&g_mutex);

    if (build_batch_json(batch, count, &json) == 0 &&
        build_request(host, &json, &request) == 0) {

      int sock = connect_with_timeout(host, port);

      if (sock >= 0) {
        if (send_all(sock, request.data, request.len) != 0) {
          atomic_fetch_add(&g_dropped, (long)count);
        }
        close(sock);
      } else {
        atomic_fetch_add(&g_dropped, (long)count);
      }
    } else {
      atomic_fetch_add(&g_dropped, (long)count);
    }

    for (i = 0; i < count; i++) {
      free_log_data(batch[i]);
    }

    /* Los buffers se reutilizan entre iteraciones */
    json.len = 0;
    request.len = 0;
  }

  free(json.data);
  free(request.data);

  return NULL;
}

static void enqueue_log(struct LogData *data) {
  pthread_mutex_lock(&g_mutex);

  if (g_count >= QUEUE_CAPACITY) {
    /* Política: descartar el log nuevo; JAMÁS bloquear a la app */
    atomic_fetch_add(&g_dropped, 1);
    pthread_mutex_unlock(&g_mutex);
    free_log_data(data);
    return;
  }

  g_queue[(g_head + g_count) % QUEUE_CAPACITY] = data;
  g_count++;
  pthread_cond_signal(&g_cond);

  pthread_mutex_unlock(&g_mutex);
}

static void ensure_worker(void) {
  pthread_mutex_lock(&g_mutex);

  if (!g_worker_running && !g_shutdown) {
    if (pthread_create(&g_worker, NULL, worker_main, NULL) == 0) {
      g_worker_running = 1;
    }
    /* Si falla, la cola se llena y los drops se contabilizan */
  }

  pthread_mutex_unlock(&g_mutex);
}

/* -------- API JNI -------- */

JNIEXPORT void JNICALL Java_com_deadnote_RemoteLog_nativeConfigure(
    JNIEnv *env, jclass clazz, jstring jhost, jint jport) {
  const char *host;

  (void)clazz;

  if (env == NULL || jhost == NULL) {
    return;
  }

  host = (*env)->GetStringUTFChars(env, jhost, NULL);
  if (host == NULL) {
    return;
  }

  pthread_mutex_lock(&g_mutex);
  strncpy(g_host, host, sizeof(g_host) - 1);
  g_host[sizeof(g_host) - 1] = '\0';
  g_port = (int)jport;
  pthread_mutex_unlock(&g_mutex);

  (*env)->ReleaseStringUTFChars(env, jhost, host);
}

JNIEXPORT void JNICALL Java_com_deadnote_RemoteLog_nativeSendLog(
    JNIEnv *env, jclass clazz, jstring jlevel, jstring jtag, jstring jmessage) {
  const char *level;
  const char *tag;
  const char *message;
  struct LogData *data;

  (void)clazz;

  if (env == NULL || jlevel == NULL || jtag == NULL || jmessage == NULL) {
    return;
  }

  /* Salida temprana por llamada: más claro que el if triple del final */
  level = (*env)->GetStringUTFChars(env, jlevel, NULL);
  if (level == NULL) {
    return;
  }

  tag = (*env)->GetStringUTFChars(env, jtag, NULL);
  if (tag == NULL) {
    (*env)->ReleaseStringUTFChars(env, jlevel, level);
    return;
  }

  message = (*env)->GetStringUTFChars(env, jmessage, NULL);
  if (message == NULL) {
    (*env)->ReleaseStringUTFChars(env, jlevel, level);
    (*env)->ReleaseStringUTFChars(env, jtag, tag);
    return;
  }

  data = (struct LogData *)malloc(sizeof(struct LogData));

  if (data != NULL) {
    data->level = copy_string(level);
    data->tag = copy_string(tag);
    data->message = copy_string(message);

    if (data->level == NULL || data->tag == NULL || data->message == NULL) {
      free_log_data(data);
      data = NULL;
    }
  }

  (*env)->ReleaseStringUTFChars(env, jlevel, level);
  (*env)->ReleaseStringUTFChars(env, jtag, tag);
  (*env)->ReleaseStringUTFChars(env, jmessage, message);

  if (data == NULL) {
    return;
  }

  enqueue_log(data);
  ensure_worker();
}

JNIEXPORT jlong JNICALL
Java_com_deadnote_RemoteLog_nativeGetDroppedCount(JNIEnv *env, jclass clazz) {
  (void)env;
  (void)clazz;

  return (jlong)atomic_load(&g_dropped);
}

JNIEXPORT void JNICALL
Java_com_deadnote_RemoteLog_nativeShutdown(JNIEnv *env, jclass clazz) {
  pthread_t worker;
  int must_join = 0;

  (void)env;
  (void)clazz;

  pthread_mutex_lock(&g_mutex);

  if (g_worker_running && !g_shutdown) {
    g_shutdown = 1;
    worker = g_worker;
    must_join = 1;
    pthread_cond_broadcast(&g_cond);
  }

  pthread_mutex_unlock(&g_mutex);

  if (must_join) {
    /* Como mucho tarda ~CONNECT_TIMEOUT + IO_TIMEOUT (el worker vacía antes) */
    pthread_join(worker, NULL);

    pthread_mutex_lock(&g_mutex);
    g_worker_running = 0;
    g_shutdown = 0;
    pthread_mutex_unlock(&g_mutex);
  }
}
