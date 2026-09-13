.class public Lcom/deadnote/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"


# direct methods
.method public constructor <init>()V
    .registers 1

    .line 8
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .registers 10

    .line 12
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 17
    const-string v0, "MainActivity"

    const-string v1, "onCreate iniciado"

    invoke-static {v0, v1}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V

    .line 18
    const-string v0, "Lifecycle"

    const-string v1, "Actividad creada"

    invoke-static {v0, v1}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V

    .line 19
    const-string v0, "Construyendo TextView..."

    const-string v1, "UI"

    invoke-static {v1, v0}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V

    .line 26
    const-string v0, "testFunction"

    const-string v2, "argNull"

    const/4 v3, 0x0

    invoke-static {v0, v2, v3}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 29
    const-string v2, "argString"

    const-string v4, "test value"

    invoke-static {v0, v2, v4}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 32
    const/4 v2, 0x1

    invoke-static {v2}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v4

    const-string v5, "argBooleanTrue"

    invoke-static {v0, v5, v4}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 33
    const/4 v5, 0x0

    invoke-static {v5}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v5

    const-string v6, "argBooleanFalse"

    invoke-static {v0, v6, v5}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 36
    const/16 v6, 0x2a

    invoke-static {v6}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v6

    const-string v7, "argInteger"

    invoke-static {v0, v7, v6}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 37
    const-wide/32 v6, 0x75bcd15

    invoke-static {v6, v7}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v6

    const-string v7, "argLong"

    invoke-static {v0, v7, v6}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 38
    const-wide v6, 0x400921f9f01b866eL  # 3.14159

    invoke-static {v6, v7}, Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;

    move-result-object v6

    const-string v7, "argDouble"

    invoke-static {v0, v7, v6}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 39
    const/high16 v6, 0x40200000  # 2.5f

    invoke-static {v6}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v6

    const-string v7, "argFloat"

    invoke-static {v0, v7, v6}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 40
    const/4 v6, 0x2

    const/4 v7, 0x3

    filled-new-array {v2, v6, v7}, [I

    move-result-object v2

    const-string v6, "argArray"

    invoke-static {v0, v6, v2}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 41
    new-instance v2, Ljava/lang/Object;

    invoke-direct {v2}, Ljava/lang/Object;-><init>()V

    const-string v6, "argObject"

    invoke-static {v0, v6, v2}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 42
    const-string v2, "argBundle"

    invoke-static {v0, v2, p1}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 49
    invoke-static {v0, v3}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 52
    const-string p1, "test result"

    invoke-static {v0, p1}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 55
    invoke-static {v0, v4}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 56
    invoke-static {v0, v5}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 59
    const/16 p1, 0x63

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    invoke-static {v0, p1}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 60
    const-wide v2, 0x3ff9e353f7ced917L  # 1.618

    invoke-static {v2, v3}, Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;

    move-result-object p1

    invoke-static {v0, p1}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 61
    new-instance p1, Ljava/lang/StringBuilder;

    const-string v2, "resultado"

    invoke-direct {p1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {v0, p1}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 66
    new-instance p1, Landroid/widget/TextView;

    invoke-direct {p1, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V

    .line 67
    const-string v0, "Hola desde MainActivity"

    invoke-virtual {p1, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 68
    const/16 v0, 0x11

    invoke-virtual {p1, v0}, Landroid/widget/TextView;->setGravity(I)V

    .line 69
    invoke-virtual {p0, p1}, Lcom/deadnote/MainActivity;->setContentView(Landroid/view/View;)V

    .line 71
    const-string p1, "TextView mostrado en pantalla"

    invoke-static {v1, p1}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V

    .line 72
    return-void
.end method

.method protected onPause()V
    .registers 4

    .line 84
    const-string v0, "state"

    const-string v1, "paused"

    const-string v2, "onPause"

    invoke-static {v2, v0, v1}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 85
    const-string v0, "Lifecycle"

    invoke-static {v0, v2}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V

    .line 86
    invoke-super {p0}, Landroid/app/Activity;->onPause()V

    .line 87
    const/4 v0, 0x1

    invoke-static {v0}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v0

    invoke-static {v2, v0}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 88
    return-void
.end method

.method protected onResume()V
    .registers 4

    .line 76
    invoke-super {p0}, Landroid/app/Activity;->onResume()V

    .line 77
    const-string v0, "Lifecycle"

    const-string v1, "onResume"

    invoke-static {v0, v1}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V

    .line 78
    const-string v0, "state"

    const-string v2, "resumed"

    invoke-static {v1, v0, v2}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V

    .line 79
    const-string v0, "ok"

    invoke-static {v1, v0}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V

    .line 80
    return-void
.end method
