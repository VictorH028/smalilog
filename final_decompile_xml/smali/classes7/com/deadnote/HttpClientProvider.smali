.class public final Lcom/deadnote/HttpClientProvider;
.super Ljava/lang/Object;
.source "HttpClientProvider.java"


# static fields
.field private static volatile INSTANCE:Lokhttp3/OkHttpClient;


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 12
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static build()Lokhttp3/OkHttpClient;
    .locals 5

    .line 26
    new-instance v0, Lokhttp3/logging/HttpLoggingInterceptor;

    new-instance v1, Lcom/deadnote/HttpClientProvider$0;

    invoke-direct {v1}, Lcom/deadnote/HttpClientProvider$0;-><init>()V

    invoke-direct {v0, v1}, Lokhttp3/logging/HttpLoggingInterceptor;-><init>(Lokhttp3/logging/HttpLoggingInterceptor$Logger;)V

    .line 29
    sget-object v1, Lokhttp3/logging/HttpLoggingInterceptor$Level;->BODY:Lokhttp3/logging/HttpLoggingInterceptor$Level;

    invoke-virtual {v0, v1}, Lokhttp3/logging/HttpLoggingInterceptor;->setLevel(Lokhttp3/logging/HttpLoggingInterceptor$Level;)Lokhttp3/logging/HttpLoggingInterceptor;

    .line 31
    new-instance v1, Lokhttp3/OkHttpClient$Builder;

    invoke-direct {v1}, Lokhttp3/OkHttpClient$Builder;-><init>()V

    sget-object v2, Ljava/util/concurrent/TimeUnit;->SECONDS:Ljava/util/concurrent/TimeUnit;

    .line 32
    const-wide/16 v3, 0x1e

    invoke-virtual {v1, v3, v4, v2}, Lokhttp3/OkHttpClient$Builder;->connectTimeout(JLjava/util/concurrent/TimeUnit;)Lokhttp3/OkHttpClient$Builder;

    move-result-object v1

    sget-object v2, Ljava/util/concurrent/TimeUnit;->SECONDS:Ljava/util/concurrent/TimeUnit;

    .line 33
    invoke-virtual {v1, v3, v4, v2}, Lokhttp3/OkHttpClient$Builder;->readTimeout(JLjava/util/concurrent/TimeUnit;)Lokhttp3/OkHttpClient$Builder;

    move-result-object v1

    sget-object v2, Ljava/util/concurrent/TimeUnit;->SECONDS:Ljava/util/concurrent/TimeUnit;

    .line 34
    invoke-virtual {v1, v3, v4, v2}, Lokhttp3/OkHttpClient$Builder;->writeTimeout(JLjava/util/concurrent/TimeUnit;)Lokhttp3/OkHttpClient$Builder;

    move-result-object v1

    .line 35
    invoke-virtual {v1, v0}, Lokhttp3/OkHttpClient$Builder;->addInterceptor(Lokhttp3/Interceptor;)Lokhttp3/OkHttpClient$Builder;

    move-result-object v0

    .line 36
    invoke-virtual {v0}, Lokhttp3/OkHttpClient$Builder;->build()Lokhttp3/OkHttpClient;

    move-result-object v0

    .line 31
    return-object v0
.end method

.method public static get()Lokhttp3/OkHttpClient;
    .locals 2

    .line 15
    sget-object v0, Lcom/deadnote/HttpClientProvider;->INSTANCE:Lokhttp3/OkHttpClient;

    if-nez v0, :cond_1

    .line 16
    const-class v0, Lcom/deadnote/HttpClientProvider;

    monitor-enter v0

    .line 17
    :try_start_0
    sget-object v1, Lcom/deadnote/HttpClientProvider;->INSTANCE:Lokhttp3/OkHttpClient;

    if-nez v1, :cond_0

    invoke-static {}, Lcom/deadnote/HttpClientProvider;->build()Lokhttp3/OkHttpClient;

    move-result-object v1

    sput-object v1, Lcom/deadnote/HttpClientProvider;->INSTANCE:Lokhttp3/OkHttpClient;

    .line 18
    :cond_0
    monitor-exit v0

    goto :goto_0

    :catchall_0
    move-exception v1

    monitor-exit v0

    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw v1

    .line 20
    :cond_1
    :goto_0
    sget-object v0, Lcom/deadnote/HttpClientProvider;->INSTANCE:Lokhttp3/OkHttpClient;

    return-object v0
.end method

.method static synthetic lambda$build$0(Ljava/lang/String;)V
    .locals 1

    .line 27
    const-string v0, "Traffic"

    invoke-static {v0, p0}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method
