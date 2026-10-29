.class public final Lcom/smalilog/agent/AgentRuntime;
.super Ljava/lang/Object;
.source "AgentRuntime.java"


# static fields
.field private static final CLOSE_LOCK:Ljava/lang/Object;

.field private static final COMMAND_TIMEOUT_MS:I = 0x3a98

.field private static final LOCK:Ljava/lang/Object;

.field private static final MAX_SCRIPT_BYTES:I = 0x40000

.field private static final RESPONSES:Ljava/util/concurrent/LinkedBlockingQueue;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/concurrent/LinkedBlockingQueue<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private static final WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

.field private static reader:Ljava/io/BufferedReader;

.field private static readerThread:Ljava/lang/Thread;

.field private static sessionKey:Ljava/lang/String;

.field private static socket:Landroid/net/LocalSocket;

.field private static writer:Ljava/io/OutputStream;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 29
    new-instance v0, Ljava/lang/Object;

    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->LOCK:Ljava/lang/Object;

    .line 30
    new-instance v0, Ljava/lang/Object;

    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->CLOSE_LOCK:Ljava/lang/Object;

    .line 31
    new-instance v0, Ljava/util/concurrent/LinkedBlockingQueue;

    invoke-direct {v0}, Ljava/util/concurrent/LinkedBlockingQueue;-><init>()V

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->RESPONSES:Ljava/util/concurrent/LinkedBlockingQueue;

    .line 32
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x0

    invoke-direct {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>(Z)V

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .line 40
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 41
    return-void
.end method

.method static synthetic access$000()V
    .locals 0

    .line 24
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->readLoop()V

    return-void
.end method

.method static synthetic access$100()Ljava/util/concurrent/atomic/AtomicBoolean;
    .locals 1

    .line 24
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-object v0
.end method

.method static synthetic access$200()V
    .locals 0

    .line 24
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->close()V

    return-void
.end method

.method private static armWatchdog()V
    .locals 3

    .line 252
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/smalilog/agent/AgentRuntime$2;

    invoke-direct {v1}, Lcom/smalilog/agent/AgentRuntime$2;-><init>()V

    const-string v2, "SmalilogAgent-watchdog"

    invoke-direct {v0, v1, v2}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 266
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/lang/Thread;->setDaemon(Z)V

    .line 267
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    .line 268
    return-void
.end method

.method private static close()V
    .locals 3

    .line 282
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->CLOSE_LOCK:Ljava/lang/Object;

    monitor-enter v0

    .line 283
    :try_start_0
    sget-object v1, Lcom/smalilog/agent/AgentRuntime;->WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v2, 0x0

    invoke-virtual {v1, v2}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 284
    sget-object v1, Lcom/smalilog/agent/AgentRuntime;->RESPONSES:Ljava/util/concurrent/LinkedBlockingQueue;

    invoke-virtual {v1}, Ljava/util/concurrent/LinkedBlockingQueue;->clear()V

    .line 285
    sget-object v1, Lcom/smalilog/agent/AgentRuntime;->socket:Landroid/net/LocalSocket;

    .line 286
    const/4 v2, 0x0

    sput-object v2, Lcom/smalilog/agent/AgentRuntime;->socket:Landroid/net/LocalSocket;

    .line 287
    sput-object v2, Lcom/smalilog/agent/AgentRuntime;->reader:Ljava/io/BufferedReader;

    .line 288
    sput-object v2, Lcom/smalilog/agent/AgentRuntime;->writer:Ljava/io/OutputStream;

    .line 289
    sput-object v2, Lcom/smalilog/agent/AgentRuntime;->sessionKey:Ljava/lang/String;

    .line 290
    sput-object v2, Lcom/smalilog/agent/AgentRuntime;->readerThread:Ljava/lang/Thread;

    .line 291
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v1, :cond_0

    .line 293
    :try_start_1
    invoke-virtual {v1}, Landroid/net/LocalSocket;->shutdownInput()V

    .line 295
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_0

    .line 294
    :catch_0
    move-exception v2

    .line 297
    :goto_0
    :try_start_2
    invoke-virtual {v1}, Landroid/net/LocalSocket;->shutdownOutput()V

    .line 299
    :try_end_2
    .catch Ljava/io/IOException; {:try_start_2 .. :try_end_2} :catch_1
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    goto :goto_1

    .line 298
    :catch_1
    move-exception v2

    .line 301
    :goto_1
    :try_start_3
    invoke-virtual {v1}, Landroid/net/LocalSocket;->close()V

    .line 303
    :try_end_3
    .catch Ljava/io/IOException; {:try_start_3 .. :try_end_3} :catch_2
    .catchall {:try_start_3 .. :try_end_3} :catchall_0

    goto :goto_2

    .line 302
    :catch_2
    move-exception v1

    .line 305
    :cond_0
    :goto_2
    :try_start_4
    monitor-exit v0

    .line 306
    return-void

    .line 305
    :catchall_0
    move-exception v1

    monitor-exit v0

    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_0

    throw v1
.end method

.method private static ensureConnected()V
    .locals 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 169
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->socket:Landroid/net/LocalSocket;

    if-eqz v0, :cond_0

    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->socket:Landroid/net/LocalSocket;

    invoke-virtual {v0}, Landroid/net/LocalSocket;->isConnected()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 170
    return-void

    .line 172
    :cond_0
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->close()V

    .line 174
    new-instance v0, Landroid/net/LocalSocketAddress;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "renef_pl_"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    .line 175
    invoke-static {}, Landroid/os/Process;->myPid()I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    sget-object v2, Landroid/net/LocalSocketAddress$Namespace;->ABSTRACT:Landroid/net/LocalSocketAddress$Namespace;

    invoke-direct {v0, v1, v2}, Landroid/net/LocalSocketAddress;-><init>(Ljava/lang/String;Landroid/net/LocalSocketAddress$Namespace;)V

    .line 178
    nop

    .line 179
    nop

    .line 180
    const/4 v1, 0x0

    const/4 v2, 0x0

    move-object v3, v1

    :goto_0
    const/16 v4, 0x28

    if-ge v2, v4, :cond_1

    .line 181
    new-instance v3, Landroid/net/LocalSocket;

    invoke-direct {v3}, Landroid/net/LocalSocket;-><init>()V

    .line 183
    :try_start_0
    invoke-virtual {v3, v0}, Landroid/net/LocalSocket;->connect(Landroid/net/LocalSocketAddress;)V

    .line 184
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    nop

    .line 185
    nop

    .line 186
    move-object v7, v3

    move-object v3, v1

    move-object v1, v7

    goto :goto_2

    .line 187
    :catch_0
    move-exception v4

    .line 188
    nop

    .line 190
    :try_start_1
    invoke-virtual {v3}, Landroid/net/LocalSocket;->close()V

    .line 192
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_1

    goto :goto_1

    .line 191
    :catch_1
    move-exception v3

    .line 194
    :goto_1
    const-wide/16 v5, 0x32

    :try_start_2
    invoke-static {v5, v6}, Ljava/lang/Thread;->sleep(J)V

    .line 198
    :try_end_2
    .catch Ljava/lang/InterruptedException; {:try_start_2 .. :try_end_2} :catch_2

    nop

    .line 180
    add-int/lit8 v2, v2, 0x1

    move-object v3, v4

    goto :goto_0

    .line 195
    :catch_2
    move-exception v0

    .line 196
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    .line 197
    move-object v3, v4

    .line 201
    :cond_1
    :goto_2
    if-nez v1, :cond_3

    .line 202
    if-eqz v3, :cond_2

    goto :goto_3

    :cond_2
    new-instance v3, Ljava/io/IOException;

    const-string v0, "no se pudo conectar al agente"

    invoke-direct {v3, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    :goto_3
    throw v3

    .line 205
    :cond_3
    sput-object v1, Lcom/smalilog/agent/AgentRuntime;->socket:Landroid/net/LocalSocket;

    .line 206
    invoke-virtual {v1}, Landroid/net/LocalSocket;->getOutputStream()Ljava/io/OutputStream;

    move-result-object v0

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->writer:Ljava/io/OutputStream;

    .line 207
    new-instance v0, Ljava/io/BufferedReader;

    new-instance v2, Ljava/io/InputStreamReader;

    .line 208
    invoke-virtual {v1}, Landroid/net/LocalSocket;->getInputStream()Ljava/io/InputStream;

    move-result-object v1

    sget-object v3, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-direct {v2, v1, v3}, Ljava/io/InputStreamReader;-><init>(Ljava/io/InputStream;Ljava/nio/charset/Charset;)V

    invoke-direct {v0, v2}, Ljava/io/BufferedReader;-><init>(Ljava/io/Reader;)V

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->reader:Ljava/io/BufferedReader;

    .line 209
    invoke-static {}, Ljava/util/UUID;->randomUUID()Ljava/util/UUID;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/UUID;->toString()Ljava/lang/String;

    move-result-object v0

    const-string v1, "-"

    const-string v2, ""

    invoke-virtual {v0, v1, v2}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;

    move-result-object v0

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->sessionKey:Ljava/lang/String;

    .line 211
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->writer:Ljava/io/OutputStream;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "con "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    sget-object v2, Lcom/smalilog/agent/AgentRuntime;->sessionKey:Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "\n"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    sget-object v2, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {v1, v2}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/io/OutputStream;->write([B)V

    .line 212
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->writer:Ljava/io/OutputStream;

    invoke-virtual {v0}, Ljava/io/OutputStream;->flush()V

    .line 215
    const-wide/16 v0, 0xc8

    :try_start_3
    invoke-static {v0, v1}, Ljava/lang/Thread;->sleep(J)V

    .line 218
    :try_end_3
    .catch Ljava/lang/InterruptedException; {:try_start_3 .. :try_end_3} :catch_3

    goto :goto_4

    .line 216
    :catch_3
    move-exception v0

    .line 217
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    .line 220
    :goto_4
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/smalilog/agent/AgentRuntime$1;

    invoke-direct {v1}, Lcom/smalilog/agent/AgentRuntime$1;-><init>()V

    const-string v2, "SmalilogAgent-reader"

    invoke-direct {v0, v1, v2}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    sput-object v0, Lcom/smalilog/agent/AgentRuntime;->readerThread:Ljava/lang/Thread;

    .line 226
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->readerThread:Ljava/lang/Thread;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/lang/Thread;->setDaemon(Z)V

    .line 227
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->readerThread:Ljava/lang/Thread;

    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    .line 229
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "Conectado al agente Renef @renef_pl_"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-static {}, Landroid/os/Process;->myPid()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 230
    return-void
.end method

.method public static execLua(Ljava/lang/String;)Ljava/lang/String;
    .locals 2

    .line 107
    if-eqz p0, :cond_2

    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_0

    goto :goto_0

    .line 110
    :cond_0
    sget-object v0, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p0, v0}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p0

    .line 111
    array-length v0, p0

    const/high16 v1, 0x40000

    if-le v0, v1, :cond_1

    .line 112
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "ERROR: script demasiado grande: "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    array-length p0, p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string v0, " bytes"

    invoke-virtual {p0, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0

    .line 114
    :cond_1
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "hexexec "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-static {p0}, Lcom/smalilog/agent/AgentRuntime;->toHex([B)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/smalilog/agent/AgentRuntime;->sendCommand(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    return-object p0

    .line 108
    :cond_2
    :goto_0
    const-string p0, "ERROR: c\u00f3digo Lua vac\u00edo"

    return-object p0
.end method

.method public static execLuaBase64(Ljava/lang/String;)Ljava/lang/String;
    .locals 2

    .line 94
    if-eqz p0, :cond_1

    invoke-virtual {p0}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_0

    goto :goto_0

    .line 98
    :cond_0
    const/4 v0, 0x0

    :try_start_0
    invoke-static {p0, v0}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object p0

    .line 99
    new-instance v0, Ljava/lang/String;

    sget-object v1, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-direct {v0, p0, v1}, Ljava/lang/String;-><init>([BLjava/nio/charset/Charset;)V

    invoke-static {v0}, Lcom/smalilog/agent/AgentRuntime;->execLua(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-object p0

    .line 100
    :catchall_0
    move-exception p0

    .line 101
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "Base64 inv\u00e1lido: "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/smalilog/agent/AgentLog;->e(Ljava/lang/String;)V

    .line 102
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "ERROR: "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0

    .line 95
    :cond_1
    :goto_0
    const-string p0, "ERROR: c\u00f3digo Lua vac\u00edo"

    return-object p0
.end method

.method public static execLuaFile(Landroid/content/Context;Ljava/lang/String;)Ljava/lang/String;
    .locals 3

    .line 44
    const-string v0, ": "

    invoke-static {p0, p1}, Lcom/smalilog/agent/AgentRuntime;->resolveFile(Landroid/content/Context;Ljava/lang/String;)Ljava/io/File;

    move-result-object p0

    .line 45
    if-nez p0, :cond_0

    .line 46
    const-string p0, "ERROR: ruta Lua vac\u00eda"

    return-object p0

    .line 48
    :cond_0
    invoke-virtual {p0}, Ljava/io/File;->isFile()Z

    move-result p1

    if-nez p1, :cond_1

    .line 49
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v0, "ERROR: no existe "

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0

    .line 52
    :cond_1
    :try_start_0
    invoke-static {p0}, Lcom/smalilog/agent/AgentRuntime;->readFile(Ljava/io/File;)Ljava/lang/String;

    move-result-object p1

    .line 53
    invoke-static {p1}, Lcom/smalilog/agent/AgentRuntime;->execLua(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    .line 54
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Lua "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 55
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-object p1

    .line 56
    :catchall_0
    move-exception p1

    .line 57
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Error leyendo "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/smalilog/agent/AgentLog;->e(Ljava/lang/String;)V

    .line 58
    new-instance p0, Ljava/lang/StringBuilder;

    invoke-direct {p0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v0, "ERROR: "

    invoke-virtual {p0, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method

.method private static isResponse(Ljava/lang/String;)Z
    .locals 1

    .line 271
    const-string v0, "OK"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 272
    const-string v0, "Removed "

    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 273
    const-string v0, "Hook "

    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 274
    const-string v0, "ERROR: Failed to remove hook"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 275
    const-string v0, "ERROR: Lua engine not initialized"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 276
    const-string v0, "ERROR: Lua execution failed"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 277
    const-string v0, "ERROR: hexexec requires hex-encoded Lua code"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 278
    const-string v0, "ERROR: malloc failed"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p0

    if-eqz p0, :cond_0

    goto :goto_0

    :cond_0
    const/4 p0, 0x0

    goto :goto_1

    :cond_1
    :goto_0
    const/4 p0, 0x1

    .line 271
    :goto_1
    return p0
.end method

.method private static readFile(Ljava/io/File;)Ljava/lang/String;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 338
    invoke-virtual {p0}, Ljava/io/File;->length()J

    move-result-wide v0

    const-wide/32 v2, 0x40000

    cmp-long v0, v0, v2

    if-gtz v0, :cond_1

    .line 341
    new-instance v0, Ljava/io/FileInputStream;

    invoke-direct {v0, p0}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    .line 342
    :try_start_0
    new-instance v1, Ljava/io/ByteArrayOutputStream;

    invoke-virtual {p0}, Ljava/io/File;->length()J

    move-result-wide v2

    long-to-int p0, v2

    invoke-direct {v1, p0}, Ljava/io/ByteArrayOutputStream;-><init>(I)V

    .line 343
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_2

    const/16 p0, 0x2000

    :try_start_1
    new-array p0, p0, [B

    .line 345
    :goto_0
    invoke-virtual {v0, p0}, Ljava/io/InputStream;->read([B)I

    move-result v2

    const/4 v3, -0x1

    if-eq v2, v3, :cond_0

    .line 346
    const/4 v3, 0x0

    invoke-virtual {v1, p0, v3, v2}, Ljava/io/ByteArrayOutputStream;->write([BII)V

    goto :goto_0

    .line 348
    :cond_0
    sget-object p0, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p0}, Ljava/nio/charset/Charset;->name()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/io/ByteArrayOutputStream;->toString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    .line 349
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    :try_start_2
    invoke-virtual {v1}, Ljava/io/ByteArrayOutputStream;->close()V

    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_2

    invoke-virtual {v0}, Ljava/io/InputStream;->close()V

    .line 348
    return-object p0

    .line 341
    :catchall_0
    move-exception p0

    :try_start_3
    invoke-virtual {v1}, Ljava/io/ByteArrayOutputStream;->close()V

    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_1

    goto :goto_1

    :catchall_1
    move-exception v1

    :try_start_4
    invoke-virtual {p0, v1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_1
    throw p0

    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_2

    :catchall_2
    move-exception p0

    :try_start_5
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V

    :try_end_5
    .catchall {:try_start_5 .. :try_end_5} :catchall_3

    goto :goto_2

    :catchall_3
    move-exception v0

    invoke-virtual {p0, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_2
    throw p0

    .line 339
    :cond_1
    new-instance v0, Ljava/io/IOException;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "script demasiado grande: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p0}, Ljava/io/File;->length()J

    move-result-wide v2

    invoke-virtual {v1, v2, v3}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string v1, " bytes"

    invoke-virtual {p0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method private static readLoop()V
    .locals 3

    .line 235
    nop

    :goto_0
    :try_start_0
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->reader:Ljava/io/BufferedReader;

    invoke-virtual {v0}, Ljava/io/BufferedReader;->readLine()Ljava/lang/String;

    move-result-object v0

    if-eqz v0, :cond_1

    .line 236
    sget-object v1, Lcom/smalilog/agent/AgentRuntime;->WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v1

    if-eqz v1, :cond_0

    invoke-static {v0}, Lcom/smalilog/agent/AgentRuntime;->isResponse(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 237
    sget-object v1, Lcom/smalilog/agent/AgentRuntime;->RESPONSES:Ljava/util/concurrent/LinkedBlockingQueue;

    invoke-virtual {v1, v0}, Ljava/util/concurrent/LinkedBlockingQueue;->offer(Ljava/lang/Object;)Z

    goto :goto_0

    .line 239
    :cond_0
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "RenefLua "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    goto :goto_0

    .line 247
    :cond_1
    :goto_1
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->close()V

    .line 248
    goto :goto_2

    .line 242
    :catchall_0
    move-exception v0

    .line 243
    :try_start_1
    sget-object v1, Lcom/smalilog/agent/AgentRuntime;->socket:Landroid/net/LocalSocket;

    if-eqz v1, :cond_1

    .line 244
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Lector Renef termin\u00f3: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/smalilog/agent/AgentLog;->w(Ljava/lang/String;)V

    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    goto :goto_1

    .line 249
    :goto_2
    return-void

    .line 247
    :catchall_1
    move-exception v0

    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->close()V

    .line 248
    throw v0
.end method

.method private static resolveFile(Landroid/content/Context;Ljava/lang/String;)Ljava/io/File;
    .locals 3

    .line 309
    const/4 v0, 0x0

    if-eqz p1, :cond_5

    invoke-virtual {p1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->isEmpty()Z

    move-result v1

    if-eqz v1, :cond_0

    goto :goto_0

    .line 312
    :cond_0
    invoke-virtual {p1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object p1

    .line 313
    const-string v1, "files/"

    invoke-virtual {p1, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_1

    .line 314
    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v1

    invoke-virtual {p1, v1}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p1

    .line 317
    :cond_1
    new-instance v1, Ljava/io/File;

    invoke-direct {v1, p1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 318
    invoke-virtual {v1}, Ljava/io/File;->isAbsolute()Z

    move-result v2

    if-eqz v2, :cond_2

    .line 319
    return-object v1

    .line 322
    :cond_2
    new-instance v1, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v2

    invoke-direct {v1, v2, p1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 323
    invoke-virtual {v1}, Ljava/io/File;->isFile()Z

    move-result v2

    if-eqz v2, :cond_3

    .line 324
    return-object v1

    .line 327
    :cond_3
    invoke-virtual {p0, v0}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    move-result-object p0

    .line 328
    if-eqz p0, :cond_4

    .line 329
    new-instance v0, Ljava/io/File;

    invoke-direct {v0, p0, p1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 330
    invoke-virtual {v0}, Ljava/io/File;->isFile()Z

    move-result p0

    if-eqz p0, :cond_4

    .line 331
    return-object v0

    .line 334
    :cond_4
    return-object v1

    .line 310
    :cond_5
    :goto_0
    return-object v0
.end method

.method public static saveLuaAndExec(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 3

    .line 63
    const-string v0, ".lua"

    if-eqz p2, :cond_6

    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result v1

    if-eqz v1, :cond_0

    goto/16 :goto_3

    .line 67
    :cond_0
    const/4 v1, 0x0

    :try_start_0
    invoke-static {p2, v1}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object p2

    .line 68
    new-instance v1, Ljava/io/File;

    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_2

    const-string v2, "runtime.lua"

    if-nez p1, :cond_1

    move-object p1, v2

    :cond_1
    :try_start_1
    invoke-direct {v1, p1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object p1

    .line 69
    invoke-virtual {p1}, Ljava/lang/String;->isEmpty()Z

    move-result v1

    if-eqz v1, :cond_2

    .line 70
    goto :goto_0

    .line 69
    :cond_2
    move-object v2, p1

    .line 72
    :goto_0
    invoke-virtual {v2, v0}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result p1

    if-nez p1, :cond_3

    .line 73
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {p1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    .line 75
    :cond_3
    new-instance p1, Ljava/io/File;

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object p0

    const-string v0, "smalilog"

    invoke-direct {p1, p0, v0}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 76
    invoke-virtual {p1}, Ljava/io/File;->isDirectory()Z

    move-result p0

    if-nez p0, :cond_5

    invoke-virtual {p1}, Ljava/io/File;->mkdirs()Z

    move-result p0

    if-eqz p0, :cond_4

    goto :goto_1

    .line 77
    :cond_4
    new-instance p0, Ljava/io/IOException;

    new-instance p2, Ljava/lang/StringBuilder;

    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v0, "no se pudo crear "

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p2

    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 79
    :cond_5
    :goto_1
    new-instance p0, Ljava/io/File;

    invoke-direct {p0, p1, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    .line 80
    new-instance p1, Ljava/io/FileOutputStream;

    invoke-direct {p1, p0}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    .line 81
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_2

    :try_start_2
    invoke-virtual {p1, p2}, Ljava/io/FileOutputStream;->write([B)V

    .line 82
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    :try_start_3
    invoke-virtual {p1}, Ljava/io/FileOutputStream;->close()V

    .line 83
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v0, "Lua guardado en "

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 84
    new-instance p1, Ljava/lang/String;

    sget-object v0, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-direct {p1, p2, v0}, Ljava/lang/String;-><init>([BLjava/nio/charset/Charset;)V

    invoke-static {p1}, Lcom/smalilog/agent/AgentRuntime;->execLua(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    .line 85
    new-instance p2, Ljava/lang/StringBuilder;

    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v0, "Lua "

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p2

    invoke-virtual {p0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {p2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string p2, ": "

    invoke-virtual {p0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 86
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_2

    return-object p1

    .line 80
    :catchall_0
    move-exception p0

    :try_start_4
    invoke-virtual {p1}, Ljava/io/FileOutputStream;->close()V

    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_1

    goto :goto_2

    :catchall_1
    move-exception p1

    :try_start_5
    invoke-virtual {p0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_2
    throw p0

    .line 87
    :try_end_5
    .catchall {:try_start_5 .. :try_end_5} :catchall_2

    :catchall_2
    move-exception p0

    .line 88
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1}, Ljava/lang/StringBuilder;-><init>()V

    const-string p2, "Error guardando Lua: "

    invoke-virtual {p1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/smalilog/agent/AgentLog;->e(Ljava/lang/String;)V

    .line 89
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1}, Ljava/lang/StringBuilder;-><init>()V

    const-string p2, "ERROR: "

    invoke-virtual {p1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0

    .line 64
    :cond_6
    :goto_3
    const-string p0, "ERROR: c\u00f3digo Lua vac\u00edo"

    return-object p0
.end method

.method private static sendCommand(Ljava/lang/String;)Ljava/lang/String;
    .locals 5

    .line 141
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->LOCK:Ljava/lang/Object;

    monitor-enter v0

    .line 143
    const/4 v1, 0x0

    :try_start_0
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->ensureConnected()V

    .line 144
    sget-object v2, Lcom/smalilog/agent/AgentRuntime;->RESPONSES:Ljava/util/concurrent/LinkedBlockingQueue;

    invoke-virtual {v2}, Ljava/util/concurrent/LinkedBlockingQueue;->clear()V

    .line 145
    sget-object v2, Lcom/smalilog/agent/AgentRuntime;->WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v3, 0x1

    invoke-virtual {v2, v3}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 146
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->armWatchdog()V

    .line 147
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v3, Lcom/smalilog/agent/AgentRuntime;->sessionKey:Ljava/lang/String;

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, " "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string v2, "\n"

    invoke-virtual {p0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    .line 148
    sget-object v2, Lcom/smalilog/agent/AgentRuntime;->writer:Ljava/io/OutputStream;

    sget-object v3, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p0, v3}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p0

    invoke-virtual {v2, p0}, Ljava/io/OutputStream;->write([B)V

    .line 149
    sget-object p0, Lcom/smalilog/agent/AgentRuntime;->writer:Ljava/io/OutputStream;

    invoke-virtual {p0}, Ljava/io/OutputStream;->flush()V

    .line 151
    sget-object p0, Lcom/smalilog/agent/AgentRuntime;->RESPONSES:Ljava/util/concurrent/LinkedBlockingQueue;

    sget-object v2, Ljava/util/concurrent/TimeUnit;->MILLISECONDS:Ljava/util/concurrent/TimeUnit;

    const-wide/16 v3, 0x3a98

    invoke-virtual {p0, v3, v4, v2}, Ljava/util/concurrent/LinkedBlockingQueue;->poll(JLjava/util/concurrent/TimeUnit;)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Ljava/lang/String;

    .line 152
    sget-object v2, Lcom/smalilog/agent/AgentRuntime;->WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v2, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 153
    if-nez p0, :cond_0

    .line 154
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->close()V

    .line 155
    const-string p0, "Timeout esperando al agente Renef"

    invoke-static {p0}, Lcom/smalilog/agent/AgentLog;->e(Ljava/lang/String;)V

    .line 156
    const-string p0, "ERROR: timeout"

    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :try_start_1
    monitor-exit v0

    return-object p0

    .line 158
    :cond_0
    monitor-exit v0

    return-object p0

    .line 159
    :catchall_0
    move-exception p0

    .line 160
    sget-object v2, Lcom/smalilog/agent/AgentRuntime;->WAITING_RESPONSE:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v2, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 161
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->close()V

    .line 162
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Error ejecutando comando Renef: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/smalilog/agent/AgentLog;->e(Ljava/lang/String;)V

    .line 163
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "ERROR: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    monitor-exit v0

    return-object p0

    .line 165
    :catchall_1
    move-exception p0

    monitor-exit v0

    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    throw p0
.end method

.method public static status()Ljava/lang/String;
    .locals 2

    .line 118
    const-string v0, "return true"

    invoke-static {v0}, Lcom/smalilog/agent/AgentRuntime;->execLua(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 119
    const-string v1, "ERROR"

    invoke-virtual {v0, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 120
    return-object v0

    .line 122
    :cond_0
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "OK: agente activo (pid="

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-static {}, Landroid/os/Process;->myPid()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, ")"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private static toHex([B)Ljava/lang/String;
    .locals 6

    .line 353
    const-string v0, "0123456789abcdef"

    invoke-virtual {v0}, Ljava/lang/String;->toCharArray()[C

    move-result-object v0

    .line 354
    array-length v1, p0

    mul-int/lit8 v1, v1, 0x2

    new-array v1, v1, [C

    .line 355
    const/4 v2, 0x0

    :goto_0
    array-length v3, p0

    if-ge v2, v3, :cond_0

    .line 356
    aget-byte v3, p0, v2

    and-int/lit16 v3, v3, 0xff

    .line 357
    mul-int/lit8 v4, v2, 0x2

    ushr-int/lit8 v5, v3, 0x4

    aget-char v5, v0, v5

    aput-char v5, v1, v4

    .line 358
    add-int/lit8 v4, v4, 0x1

    and-int/lit8 v3, v3, 0xf

    aget-char v3, v0, v3

    aput-char v3, v1, v4

    .line 355
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 360
    :cond_0
    new-instance p0, Ljava/lang/String;

    invoke-direct {p0, v1}, Ljava/lang/String;-><init>([C)V

    return-object p0
.end method

.method public static unhookAll()Ljava/lang/String;
    .locals 4

    .line 126
    sget-object v0, Lcom/smalilog/agent/AgentRuntime;->LOCK:Ljava/lang/Object;

    monitor-enter v0

    .line 127
    :try_start_0
    const-string v1, "unhook: reseteando guarda"

    invoke-static {v1}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 128
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "hexexec "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "_G.__smalilog_runtime_hook = nil"

    sget-object v3, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    .line 129
    invoke-virtual {v2, v3}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object v2

    .line 128
    invoke-static {v2}, Lcom/smalilog/agent/AgentRuntime;->toHex([B)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/smalilog/agent/AgentRuntime;->sendCommand(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 130
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "unhook: guarda="

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 131
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->close()V

    .line 132
    const-string v2, "unhook: conexi\u00f3n cerrada"

    invoke-static {v2}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 133
    const-string v2, "ERROR"

    invoke-virtual {v1, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_0

    .line 134
    monitor-exit v0

    return-object v1

    .line 136
    :cond_0
    const-string v1, "OK: hooks eliminados"

    monitor-exit v0

    return-object v1

    .line 137
    :catchall_0
    move-exception v1

    monitor-exit v0

    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw v1
.end method
