.class Lcom/smalilog/agent/AgentLog$1;
.super Ljava/lang/Object;
.source "AgentLog.java"

# interfaces
.implements Ljava/util/concurrent/ThreadFactory;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/smalilog/agent/AgentLog;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# direct methods
.method constructor <init>()V
    .locals 0

    .line 16
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public newThread(Ljava/lang/Runnable;)Ljava/lang/Thread;
    .locals 2

    .line 19
    new-instance v0, Ljava/lang/Thread;

    const-string v1, "SmalilogAgentLog"

    invoke-direct {v0, p1, v1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 20
    const/4 p1, 0x1

    invoke-virtual {v0, p1}, Ljava/lang/Thread;->setDaemon(Z)V

    .line 21
    return-object v0
.end method
