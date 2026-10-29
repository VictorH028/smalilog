.class Lcom/smalilog/agent/AgentLog$2;
.super Ljava/lang/Object;
.source "AgentLog.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/smalilog/agent/AgentLog;->send(Ljava/lang/String;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic val$level:Ljava/lang/String;

.field final synthetic val$message:Ljava/lang/String;


# direct methods
.method constructor <init>(Ljava/lang/String;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 60
    iput-object p1, p0, Lcom/smalilog/agent/AgentLog$2;->val$level:Ljava/lang/String;

    iput-object p2, p0, Lcom/smalilog/agent/AgentLog$2;->val$message:Ljava/lang/String;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 2

    .line 63
    iget-object v0, p0, Lcom/smalilog/agent/AgentLog$2;->val$level:Ljava/lang/String;

    iget-object v1, p0, Lcom/smalilog/agent/AgentLog$2;->val$message:Ljava/lang/String;

    invoke-static {v0, v1}, Lcom/smalilog/agent/AgentLog;->access$000(Ljava/lang/String;Ljava/lang/String;)V

    .line 64
    return-void
.end method
