.class Lcom/smalilog/agent/AgentReceiver$1;
.super Ljava/lang/Object;
.source "AgentReceiver.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/smalilog/agent/AgentReceiver;->onReceive(Landroid/content/Context;Landroid/content/Intent;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/smalilog/agent/AgentReceiver;

.field final synthetic val$app:Landroid/content/Context;

.field final synthetic val$b64:Ljava/lang/String;

.field final synthetic val$name:Ljava/lang/String;

.field final synthetic val$op:Ljava/lang/String;

.field final synthetic val$pending:Landroid/content/BroadcastReceiver$PendingResult;


# direct methods
.method constructor <init>(Lcom/smalilog/agent/AgentReceiver;Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Landroid/content/BroadcastReceiver$PendingResult;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010,
            0x1010,
            0x1010,
            0x1010,
            0x1010
        }
        names = {
            null,
            null,
            null,
            null,
            null,
            null
        }
    .end annotation
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 41
    iput-object p1, p0, Lcom/smalilog/agent/AgentReceiver$1;->this$0:Lcom/smalilog/agent/AgentReceiver;

    iput-object p2, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$app:Landroid/content/Context;

    iput-object p3, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$op:Ljava/lang/String;

    iput-object p4, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$b64:Ljava/lang/String;

    iput-object p5, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$name:Ljava/lang/String;

    iput-object p6, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$pending:Landroid/content/BroadcastReceiver$PendingResult;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 4

    .line 45
    :try_start_0
    iget-object v0, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$app:Landroid/content/Context;

    iget-object v1, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$op:Ljava/lang/String;

    iget-object v2, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$b64:Ljava/lang/String;

    iget-object v3, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$name:Ljava/lang/String;

    invoke-static {v0, v1, v2, v3}, Lcom/smalilog/agent/AgentReceiver;->access$000(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    .line 49
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :goto_0
    iget-object v0, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$pending:Landroid/content/BroadcastReceiver$PendingResult;

    invoke-virtual {v0}, Landroid/content/BroadcastReceiver$PendingResult;->finish()V

    .line 50
    goto :goto_1

    .line 46
    :catchall_0
    move-exception v0

    .line 47
    :try_start_1
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Error en receptor: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/smalilog/agent/AgentLog;->e(Ljava/lang/String;)V

    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    goto :goto_0

    .line 51
    :goto_1
    return-void

    .line 49
    :catchall_1
    move-exception v0

    iget-object v1, p0, Lcom/smalilog/agent/AgentReceiver$1;->val$pending:Landroid/content/BroadcastReceiver$PendingResult;

    invoke-virtual {v1}, Landroid/content/BroadcastReceiver$PendingResult;->finish()V

    .line 50
    throw v0
.end method
