.class Lcom/smalilog/agent/AgentRuntime$2;
.super Ljava/lang/Object;
.source "AgentRuntime.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/smalilog/agent/AgentRuntime;->armWatchdog()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# direct methods
.method constructor <init>()V
    .locals 0

    .line 252
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 2

    .line 256
    const-wide/16 v0, 0x4268

    :try_start_0
    invoke-static {v0, v1}, Ljava/lang/Thread;->sleep(J)V

    .line 259
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    nop

    .line 260
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->access$100()Ljava/util/concurrent/atomic/AtomicBoolean;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 261
    const-string v0, "Watchdog Renef: sin respuesta, cerrando conexi\u00f3n"

    invoke-static {v0}, Lcom/smalilog/agent/AgentLog;->w(Ljava/lang/String;)V

    .line 262
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->access$200()V

    .line 264
    :cond_0
    return-void

    .line 257
    :catch_0
    move-exception v0

    .line 258
    return-void
.end method
