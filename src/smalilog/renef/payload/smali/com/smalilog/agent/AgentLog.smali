.class public final Lcom/smalilog/agent/AgentLog;
.super Ljava/lang/Object;
.source "AgentLog.java"


# static fields
.field private static final POOL:Ljava/util/concurrent/ExecutorService;

.field private static final TAG:Ljava/lang/String; = "SmalilogAgent"

.field private static volatile host:Ljava/lang/String;

.field private static volatile port:I


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .line 16
    new-instance v0, Lcom/smalilog/agent/AgentLog$1;

    invoke-direct {v0}, Lcom/smalilog/agent/AgentLog$1;-><init>()V

    invoke-static {v0}, Ljava/util/concurrent/Executors;->newSingleThreadExecutor(Ljava/util/concurrent/ThreadFactory;)Ljava/util/concurrent/ExecutorService;

    move-result-object v0

    sput-object v0, Lcom/smalilog/agent/AgentLog;->POOL:Ljava/util/concurrent/ExecutorService;

    .line 25
    const-string v0, "127.0.0.1"

    sput-object v0, Lcom/smalilog/agent/AgentLog;->host:Ljava/lang/String;

    .line 26
    const/16 v0, 0x270f

    sput v0, Lcom/smalilog/agent/AgentLog;->port:I

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .line 28
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 29
    return-void
.end method

.method static synthetic access$000(Ljava/lang/String;Ljava/lang/String;)V
    .locals 0

    .line 13
    invoke-static {p0, p1}, Lcom/smalilog/agent/AgentLog;->post(Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method

.method public static configure(Ljava/lang/String;I)V
    .locals 1

    .line 32
    if-eqz p0, :cond_0

    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_0

    .line 33
    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object p0

    sput-object p0, Lcom/smalilog/agent/AgentLog;->host:Ljava/lang/String;

    .line 35
    :cond_0
    if-lez p1, :cond_1

    const p0, 0xffff

    if-gt p1, p0, :cond_1

    .line 36
    sput p1, Lcom/smalilog/agent/AgentLog;->port:I

    .line 38
    :cond_1
    return-void
.end method

.method public static e(Ljava/lang/String;)V
    .locals 1

    .line 51
    const-string v0, "SmalilogAgent"

    invoke-static {v0, p0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 52
    const-string v0, "ERROR"

    invoke-static {v0, p0}, Lcom/smalilog/agent/AgentLog;->send(Ljava/lang/String;Ljava/lang/String;)V

    .line 53
    return-void
.end method

.method public static i(Ljava/lang/String;)V
    .locals 1

    .line 41
    const-string v0, "SmalilogAgent"

    invoke-static {v0, p0}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 42
    const-string v0, "INFO"

    invoke-static {v0, p0}, Lcom/smalilog/agent/AgentLog;->send(Ljava/lang/String;Ljava/lang/String;)V

    .line 43
    return-void
.end method

.method private static post(Ljava/lang/String;Ljava/lang/String;)V
    .locals 4

    .line 71
    nop

    .line 73
    const/4 v0, 0x0

    :try_start_0
    new-instance v1, Ljava/net/URL;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "http://"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    sget-object v3, Lcom/smalilog/agent/AgentLog;->host:Ljava/lang/String;

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, ":"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    sget v3, Lcom/smalilog/agent/AgentLog;->port:I

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, "/log"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-direct {v1, v2}, Ljava/net/URL;-><init>(Ljava/lang/String;)V

    .line 74
    invoke-virtual {v1}, Ljava/net/URL;->openConnection()Ljava/net/URLConnection;

    move-result-object v1

    check-cast v1, Ljava/net/HttpURLConnection;

    .line 75
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_3

    const/16 v0, 0x4b0

    :try_start_1
    invoke-virtual {v1, v0}, Ljava/net/HttpURLConnection;->setConnectTimeout(I)V

    .line 76
    invoke-virtual {v1, v0}, Ljava/net/HttpURLConnection;->setReadTimeout(I)V

    .line 77
    const-string v0, "POST"

    invoke-virtual {v1, v0}, Ljava/net/HttpURLConnection;->setRequestMethod(Ljava/lang/String;)V

    .line 78
    const/4 v0, 0x1

    invoke-virtual {v1, v0}, Ljava/net/HttpURLConnection;->setDoOutput(Z)V

    .line 79
    const-string v0, "Content-Type"

    const-string v2, "application/json; charset=utf-8"

    invoke-virtual {v1, v0, v2}, Ljava/net/HttpURLConnection;->setRequestProperty(Ljava/lang/String;Ljava/lang/String;)V

    .line 80
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "{\"level\":"

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-static {p0}, Lcom/smalilog/agent/AgentLog;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string v0, ",\"tag\":\"SmalilogAgent\",\"message\":"

    invoke-virtual {p0, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    .line 81
    invoke-static {p1}, Lcom/smalilog/agent/AgentLog;->quote(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string p1, "}"

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    sget-object p1, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    .line 82
    invoke-virtual {p0, p1}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p0

    .line 83
    array-length p1, p0

    invoke-virtual {v1, p1}, Ljava/net/HttpURLConnection;->setFixedLengthStreamingMode(I)V

    .line 84
    invoke-virtual {v1}, Ljava/net/HttpURLConnection;->getOutputStream()Ljava/io/OutputStream;

    move-result-object p1

    .line 85
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_2

    :try_start_2
    invoke-virtual {p1, p0}, Ljava/io/OutputStream;->write([B)V

    .line 86
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    if-eqz p1, :cond_0

    :try_start_3
    invoke-virtual {p1}, Ljava/io/OutputStream;->close()V

    .line 87
    :cond_0
    invoke-virtual {v1}, Ljava/net/HttpURLConnection;->getResponseCode()I

    .line 90
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_2

    if-eqz v1, :cond_2

    .line 91
    invoke-virtual {v1}, Ljava/net/HttpURLConnection;->disconnect()V

    goto :goto_2

    .line 84
    :catchall_0
    move-exception p0

    if-eqz p1, :cond_1

    :try_start_4
    invoke-virtual {p1}, Ljava/io/OutputStream;->close()V

    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_1

    goto :goto_0

    :catchall_1
    move-exception p1

    :try_start_5
    invoke-virtual {p0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_1
    :goto_0
    throw p0

    .line 88
    :try_end_5
    .catchall {:try_start_5 .. :try_end_5} :catchall_2

    :catchall_2
    move-exception p0

    move-object v0, v1

    goto :goto_1

    :catchall_3
    move-exception p0

    .line 90
    :goto_1
    if-eqz v0, :cond_2

    .line 91
    invoke-virtual {v0}, Ljava/net/HttpURLConnection;->disconnect()V

    .line 94
    :cond_2
    :goto_2
    return-void
.end method

.method private static quote(Ljava/lang/String;)Ljava/lang/String;
    .locals 5

    .line 97
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    add-int/lit8 v1, v1, 0x2

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(I)V

    .line 98
    const/16 v1, 0x22

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 99
    const/4 v2, 0x0

    :goto_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    if-ge v2, v3, :cond_1

    .line 100
    invoke-virtual {p0, v2}, Ljava/lang/String;->charAt(I)C

    move-result v3

    .line 101
    sparse-switch v3, :sswitch_data_0

    .line 118
    const/16 v4, 0x20

    if-ge v3, v4, :cond_0

    .line 119
    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    filled-new-array {v3}, [Ljava/lang/Object;

    move-result-object v3

    const-string v4, "\\u%04x"

    invoke-static {v4, v3}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_1

    .line 106
    :sswitch_0    # 0x5c
    const-string v3, "\\\\"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 107
    goto :goto_1

    .line 103
    :sswitch_1    # 0x22
    const-string v3, "\\\""

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 104
    goto :goto_1

    .line 112
    :sswitch_2    # 0xd
    const-string v3, "\\r"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 113
    goto :goto_1

    .line 109
    :sswitch_3    # 0xa
    const-string v3, "\\n"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 110
    goto :goto_1

    .line 115
    :sswitch_4    # 0x9
    const-string v3, "\\t"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 116
    goto :goto_1

    .line 121
    :cond_0
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 99
    :goto_1
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 125
    :cond_1
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 126
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0

    :sswitch_data_0
    .sparse-switch
        0x9 -> :sswitch_4
        0xa -> :sswitch_3
        0xd -> :sswitch_2
        0x22 -> :sswitch_1
        0x5c -> :sswitch_0

    .end sparse-switch
.end method

.method private static send(Ljava/lang/String;Ljava/lang/String;)V
    .locals 2

    .line 56
    if-nez p1, :cond_0

    .line 57
    return-void

    .line 60
    :cond_0
    :try_start_0
    sget-object v0, Lcom/smalilog/agent/AgentLog;->POOL:Ljava/util/concurrent/ExecutorService;

    new-instance v1, Lcom/smalilog/agent/AgentLog$2;

    invoke-direct {v1, p0, p1}, Lcom/smalilog/agent/AgentLog$2;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    invoke-interface {v0, v1}, Ljava/util/concurrent/ExecutorService;->execute(Ljava/lang/Runnable;)V

    .line 67
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    goto :goto_0

    .line 66
    :catchall_0
    move-exception p0

    .line 68
    :goto_0
    return-void
.end method

.method public static w(Ljava/lang/String;)V
    .locals 1

    .line 46
    const-string v0, "SmalilogAgent"

    invoke-static {v0, p0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I

    .line 47
    const-string v0, "WARN"

    invoke-static {v0, p0}, Lcom/smalilog/agent/AgentLog;->send(Ljava/lang/String;Ljava/lang/String;)V

    .line 48
    return-void
.end method
