.class Lcom/smalilog/agent/AgentRuntime$1;
.super Ljava/lang/Object;
.source "AgentRuntime.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/smalilog/agent/AgentRuntime;->ensureConnected()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# direct methods
.method constructor <init>()V
    .locals 0

    .line 220
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 0

    .line 223
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->access$000()V

    .line 224
    return-void
.end method
