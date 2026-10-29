.class public Lcom/smalilog/agent/AgentReceiver;
.super Landroid/content/BroadcastReceiver;
.source "AgentReceiver.java"


# static fields
.field public static final ACTION:Ljava/lang/String; = "com.smalilog.agent.ACTION"

.field private static final LOADED:Z

.field private static final LOAD_ERROR:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 16
    nop

    .line 17
    nop

    .line 19
    :try_start_0
    const-string v0, "agent"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    .line 20
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    nop

    .line 23
    const/4 v0, 0x0

    const/4 v1, 0x1

    goto :goto_0

    .line 21
    :catchall_0
    move-exception v0

    .line 22
    invoke-virtual {v0}, Ljava/lang/Throwable;->toString()Ljava/lang/String;

    move-result-object v0

    const/4 v1, 0x0

    .line 24
    :goto_0
    sput-boolean v1, Lcom/smalilog/agent/AgentReceiver;->LOADED:Z

    .line 25
    sput-object v0, Lcom/smalilog/agent/AgentReceiver;->LOAD_ERROR:Ljava/lang/String;

    .line 26
    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .line 8
    invoke-direct {p0}, Landroid/content/BroadcastReceiver;-><init>()V

    return-void
.end method

.method static synthetic access$000(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 0

    .line 8
    invoke-static {p0, p1, p2, p3}, Lcom/smalilog/agent/AgentReceiver;->handle(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method

.method private static handle(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 2

    .line 58
    if-nez p1, :cond_0

    .line 59
    const-string p0, "Broadcast sin op"

    invoke-static {p0}, Lcom/smalilog/agent/AgentLog;->w(Ljava/lang/String;)V

    .line 60
    return-void

    .line 62
    :cond_0
    sget-boolean v0, Lcom/smalilog/agent/AgentReceiver;->LOADED:Z

    if-nez v0, :cond_1

    .line 63
    new-instance p0, Ljava/lang/StringBuilder;

    invoke-direct {p0}, Ljava/lang/StringBuilder;-><init>()V

    const-string p1, "libagent.so no cargada: "

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    sget-object p1, Lcom/smalilog/agent/AgentReceiver;->LOAD_ERROR:Ljava/lang/String;

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/smalilog/agent/AgentLog;->e(Ljava/lang/String;)V

    .line 64
    return-void

    .line 67
    :cond_1
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "op="

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, " pid="

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-static {}, Landroid/os/Process;->myPid()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 69
    const-string v0, "PING"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2

    .line 70
    new-instance p0, Ljava/lang/StringBuilder;

    invoke-direct {p0}, Ljava/lang/StringBuilder;-><init>()V

    const-string p2, "OK: receptor activo (pid="

    invoke-virtual {p0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-static {}, Landroid/os/Process;->myPid()I

    move-result p2

    invoke-virtual {p0, p2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object p0

    const-string p2, ")"

    invoke-virtual {p0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    goto/16 :goto_4

    .line 71
    :cond_2
    const-string v0, "STATUS"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3

    .line 72
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->status()Ljava/lang/String;

    move-result-object p0

    goto/16 :goto_4

    .line 73
    :cond_3
    const-string v0, "EXEC"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_b

    const-string v0, "LUA_CODE"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_b

    const-string v0, "LUA_B64"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4

    goto :goto_3

    .line 75
    :cond_4
    const-string v0, "PUSH"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_a

    const-string v0, "LUA_PUSH"

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_5

    goto :goto_2

    .line 77
    :cond_5
    const-string p2, "UNHOOK"

    invoke-virtual {p2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p2

    if-nez p2, :cond_9

    const-string p2, "LUA_UNHOOK"

    invoke-virtual {p2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p2

    if-eqz p2, :cond_6

    goto :goto_1

    .line 79
    :cond_6
    const-string p2, "EXEC_FILE"

    invoke-virtual {p2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p2

    if-nez p2, :cond_8

    const-string p2, "LUA"

    invoke-virtual {p2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p2

    if-eqz p2, :cond_7

    goto :goto_0

    .line 82
    :cond_7
    new-instance p0, Ljava/lang/StringBuilder;

    invoke-direct {p0}, Ljava/lang/StringBuilder;-><init>()V

    const-string p2, "ERROR: operaci\u00f3n desconocida: "

    invoke-virtual {p0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    goto :goto_4

    .line 80
    :cond_8
    :goto_0
    invoke-static {p0, p3}, Lcom/smalilog/agent/AgentRuntime;->execLuaFile(Landroid/content/Context;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    goto :goto_4

    .line 78
    :cond_9
    :goto_1
    invoke-static {}, Lcom/smalilog/agent/AgentRuntime;->unhookAll()Ljava/lang/String;

    move-result-object p0

    goto :goto_4

    .line 76
    :cond_a
    :goto_2
    invoke-static {p0, p3, p2}, Lcom/smalilog/agent/AgentRuntime;->saveLuaAndExec(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    goto :goto_4

    .line 74
    :cond_b
    :goto_3
    invoke-static {p2}, Lcom/smalilog/agent/AgentRuntime;->execLuaBase64(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    .line 84
    :goto_4
    new-instance p2, Ljava/lang/StringBuilder;

    invoke-direct {p2}, Ljava/lang/StringBuilder;-><init>()V

    const-string p3, "resultado "

    invoke-virtual {p2, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p2

    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    const-string p2, ": "

    invoke-virtual {p1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p1

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/smalilog/agent/AgentLog;->i(Ljava/lang/String;)V

    .line 85
    return-void
.end method

.method private static parseInt(Ljava/lang/String;I)I
    .locals 0

    .line 88
    if-nez p0, :cond_0

    .line 89
    return p1

    .line 92
    :cond_0
    :try_start_0
    invoke-virtual {p0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p0

    :try_end_0
    .catch Ljava/lang/NumberFormatException; {:try_start_0 .. :try_end_0} :catch_0

    return p0

    .line 93
    :catch_0
    move-exception p0

    .line 94
    return p1
.end method


# virtual methods
.method public onReceive(Landroid/content/Context;Landroid/content/Intent;)V
    .locals 9

    .line 30
    if-eqz p2, :cond_1

    const-string v0, "com.smalilog.agent.ACTION"

    invoke-virtual {p2}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    goto :goto_0

    .line 34
    :cond_0
    const-string v0, "host"

    invoke-virtual {p2, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const-string v1, "port"

    invoke-virtual {p2, v1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    invoke-static {v1, v2}, Lcom/smalilog/agent/AgentReceiver;->parseInt(Ljava/lang/String;I)I

    move-result v1

    invoke-static {v0, v1}, Lcom/smalilog/agent/AgentLog;->configure(Ljava/lang/String;I)V

    .line 35
    invoke-virtual {p1}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    move-result-object v4

    .line 36
    const-string p1, "op"

    invoke-virtual {p2, p1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    .line 37
    const-string p1, "b64"

    invoke-virtual {p2, p1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    .line 38
    const-string p1, "name"

    invoke-virtual {p2, p1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v7

    .line 40
    invoke-virtual {p0}, Lcom/smalilog/agent/AgentReceiver;->goAsync()Landroid/content/BroadcastReceiver$PendingResult;

    move-result-object v8

    .line 41
    new-instance p1, Ljava/lang/Thread;

    new-instance v2, Lcom/smalilog/agent/AgentReceiver$1;

    move-object v3, p0

    invoke-direct/range {v2 .. v8}, Lcom/smalilog/agent/AgentReceiver$1;-><init>(Lcom/smalilog/agent/AgentReceiver;Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Landroid/content/BroadcastReceiver$PendingResult;)V

    const-string p2, "SmalilogAgentBroadcast"

    invoke-direct {p1, v2, p2}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    .line 53
    const/4 p2, 0x1

    invoke-virtual {p1, p2}, Ljava/lang/Thread;->setDaemon(Z)V

    .line 54
    invoke-virtual {p1}, Ljava/lang/Thread;->start()V

    .line 55
    return-void

    .line 31
    :cond_1
    :goto_0
    return-void
.end method
