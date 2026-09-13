# classes3.dex

.class public final Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;
.super Lul0/b;
.source "UpgradeActivity.kt"

# interfaces
.implements Lul0/s;
.implements Lel0/c;


# static fields
.field public static final synthetic C:[Lmw0/i;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "[",
            "Lmw0/i<",
            "Ljava/lang/Object;",
            ">;"
        }
    .end annotation
.end field


# instance fields
.field public final A:Lkh0/a;

.field public final B:Lqv0/u;

.field public final n:Lqv0/u;

.field public o:Lbp0/e;

.field public p:Lkm0/f;

.field public q:Lwg/d;

.field public r:Lwg/c;

.field public s:Lwg/b;

.field public t:Lug/a;

.field public final u:Lse0/a;

.field public final v:Lqv0/u;

.field public final w:Lqv0/u;

.field public final x:Lqv0/u;

.field public final y:Lqv0/u;

.field public final z:Lkh0/a;


# direct methods
.method static constructor <clinit>()V
    .registers 6

    .line 1
    new-instance v0, Lkotlin/jvm/internal/w;

    .line 3
    const-class v1, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;

    .line 5
    const-string v2, "viewModel"

    .line 7
    const-string v3, "getViewModel()Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeViewModelImpl;"

    .line 9
    const/4 v4, 0x0

    .line 10
    invoke-direct {v0, v1, v2, v3, v4}, Lkotlin/jvm/internal/w;-><init>(Ljava/lang/Class;Ljava/lang/String;Ljava/lang/String;I)V

    .line 13
    sget-object v2, Lkotlin/jvm/internal/f0;->a:Lkotlin/jvm/internal/g0;

    .line 15
    const-string v3, "productsViewModel"

    .line 17
    const-string v5, "getProductsViewModel()Lcom/ellation/crunchyroll/presentation/multitiersubscription/subscription/viewmodel/CrPlusSubscriptionProductsViewModel;"

    .line 19
    invoke-static {v4, v1, v3, v5, v2}, Lnl/h;->b(ILjava/lang/Class;Ljava/lang/String;Ljava/lang/String;Lkotlin/jvm/internal/g0;)Lkotlin/jvm/internal/w;

    .line 22
    move-result-object v1

    .line 23
    const/4 v2, 0x2

    .line 24
    new-array v2, v2, [Lmw0/i;

    .line 26
    aput-object v0, v2, v4

    .line 28
    const/4 v0, 0x1

    .line 29
    aput-object v1, v2, v0

    .line 31
    sput-object v2, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->C:[Lmw0/i;

    .line 33
    return-void
.end method

.method public constructor <init>()V
    .registers 5

    .line 1
    invoke-direct {p0}, Lul0/b;-><init>()V

    .line 4
    new-instance v0, Lqj0/c;

    .line 6
    const/4 v1, 0x1

    .line 7
    invoke-direct {v0, p0, v1}, Lqj0/c;-><init>(Ljava/lang/Object;I)V

    .line 10
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 13
    move-result-object v0

    .line 14
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->n:Lqv0/u;

    .line 16
    new-instance v0, Lkm0/e0;

    .line 18
    const/4 v1, 0x2

    .line 19
    invoke-direct {v0, p0, v1}, Lkm0/e0;-><init>(Ljava/lang/Object;I)V

    .line 22
    invoke-static {p0, v0}, Lse0/b;->c(Landroid/app/Activity;Lfw0/l;)Lse0/a;

    .line 25
    move-result-object v0

    .line 26
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->u:Lse0/a;

    .line 28
    new-instance v0, Lgd/a;

    .line 30
    invoke-direct {v0, p0, v1}, Lgd/a;-><init>(Ljava/lang/Object;I)V

    .line 33
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 36
    move-result-object v0

    .line 37
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->v:Lqv0/u;

    .line 39
    new-instance v0, Landroidx/xr/scenecore/j0;

    .line 41
    const/4 v1, 0x4

    .line 42
    invoke-direct {v0, p0, v1}, Landroidx/xr/scenecore/j0;-><init>(Ljava/lang/Object;I)V

    .line 45
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 48
    move-result-object v0

    .line 49
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->w:Lqv0/u;

    .line 51
    new-instance v0, Lul0/g;

    .line 53
    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    .line 56
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 59
    move-result-object v0

    .line 60
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->x:Lqv0/u;

    .line 62
    new-instance v0, Led/h0;

    .line 64
    invoke-direct {v0, p0, v1}, Led/h0;-><init>(Ljava/lang/Object;I)V

    .line 67
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 70
    move-result-object v0

    .line 71
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->y:Lqv0/u;

    .line 73
    new-instance v0, Lhe0/r;

    .line 75
    const/4 v1, 0x2

    .line 76
    invoke-direct {v0, p0, v1}, Lhe0/r;-><init>(Ljava/lang/Object;I)V

    .line 79
    new-instance v1, Lkh0/a;

    .line 81
    new-instance v2, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity$b;

    .line 83
    invoke-direct {v2, p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity$b;-><init>(Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;)V

    .line 86
    const-class v3, Lul0/y;

    .line 88
    invoke-direct {v1, v3, v2, v0}, Lkh0/a;-><init>(Ljava/lang/Class;Lfw0/a;Lfw0/l;)V

    .line 91
    iput-object v1, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->z:Lkh0/a;

    .line 93
    new-instance v0, Lcom/ellation/crunchyroll/cast/expanded/u;

    .line 95
    const/4 v1, 0x2

    .line 96
    invoke-direct {v0, p0, v1}, Lcom/ellation/crunchyroll/cast/expanded/u;-><init>(Ljava/lang/Object;I)V

    .line 99
    new-instance v1, Lkh0/a;

    .line 101
    new-instance v2, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity$c;

    .line 103
    invoke-direct {v2, p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity$c;-><init>(Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;)V

    .line 106
    const-class v3, Ldm0/f;

    .line 108
    invoke-direct {v1, v3, v2, v0}, Lkh0/a;-><init>(Ljava/lang/Class;Lfw0/a;Lfw0/l;)V

    .line 111
    iput-object v1, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->A:Lkh0/a;

    .line 113
    new-instance v0, Lkm0/o;

    .line 115
    const/4 v1, 0x2

    .line 116
    invoke-direct {v0, p0, v1}, Lkm0/o;-><init>(Ljava/lang/Object;I)V

    .line 119
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 122
    move-result-object v0

    .line 123
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->B:Lqv0/u;

    .line 125
    return-void
.end method

.method public static Rf(Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;)Lmt/b;
    .registers 4

    .line 1
    invoke-virtual {p0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;

    .line 4
    move-result-object p0

    .line 5
    invoke-virtual {p0}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    .line 8
    move-result-object p0

    .line 9
    if-eqz p0, :cond_22

    .line 11
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 13
    const/16 v1, 0x21

    .line 15
    const-string v2, "UPGRADE_EXTRA_PRESELECTED_SKU"

    .line 17
    if-lt v0, v1, :cond_19

    .line 19
    const-class v0, Lmt/b;

    .line 21
    invoke-virtual {p0, v2, v0}, Landroid/os/Bundle;->getSerializable(Ljava/lang/String;Ljava/lang/Class;)Ljava/io/Serializable;

    .line 24
    move-result-object p0

    .line 25
    goto :goto_1f

    .line 26
    :cond_19
    invoke-virtual {p0, v2}, Landroid/os/Bundle;->getSerializable(Ljava/lang/String;)Ljava/io/Serializable;

    .line 29
    move-result-object p0

    .line 30
    check-cast p0, Lmt/b;

    .line 32
    :goto_1f
    check-cast p0, Lmt/b;

    .line 34
    return-object p0

    .line 35
    :cond_22
    const/4 p0, 0x0

    .line 36
    return-object p0
.end method

.method public static Sf(Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;)Lul0/q;
    .registers 11

    .line 1
    invoke-virtual {p0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;

    .line 4
    move-result-object v0

    .line 5
    invoke-virtual {v0}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    .line 8
    move-result-object v0

    .line 9
    if-eqz v0, :cond_23

    .line 11
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 13
    const/16 v2, 0x21

    .line 15
    const-string v3, "UPGRADE_EXTRA_SUCCESS_SCREEN_TYPE"

    .line 17
    if-lt v1, v2, :cond_19

    .line 19
    const-class v1, Lmt/a;

    .line 21
    invoke-virtual {v0, v3, v1}, Landroid/os/Bundle;->getSerializable(Ljava/lang/String;Ljava/lang/Class;)Ljava/io/Serializable;

    .line 24
    move-result-object v0

    .line 25
    goto :goto_1f

    .line 26
    :cond_19
    invoke-virtual {v0, v3}, Landroid/os/Bundle;->getSerializable(Ljava/lang/String;)Ljava/io/Serializable;

    .line 29
    move-result-object v0

    .line 30
    check-cast v0, Lmt/a;

    .line 32
    :goto_1f
    check-cast v0, Lmt/a;

    .line 34
    if-nez v0, :cond_25

    .line 36
    :cond_23
    sget-object v0, Lmt/a;->CR_PLUS:Lmt/a;

    .line 38
    :cond_25
    iget-object v1, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->z:Lkh0/a;

    .line 40
    sget-object v2, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->C:[Lmw0/i;

    .line 42
    const/4 v3, 0x0

    .line 43
    aget-object v2, v2, v3

    .line 45
    invoke-virtual {v1, p0, v2}, Lkh0/a;->a(Ljava/lang/Object;Lmw0/i;)Landroidx/lifecycle/o1;

    .line 48
    move-result-object v1

    .line 49
    move-object v4, v1

    .line 50
    check-cast v4, Lul0/y;

    .line 52
    invoke-static {p0}, Lzg0/b;->a(Landroid/content/Context;)Lzg0/a;

    .line 55
    move-result-object v1

    .line 56
    invoke-interface {v1}, Lzg0/a;->l()Lft/d;

    .line 59
    move-result-object v1

    .line 60
    invoke-interface {v1}, Lft/d;->w()Lic/d;

    .line 63
    move-result-object v1

    .line 64
    invoke-virtual {v1}, Lic/d;->invoke()Ljava/lang/Object;

    .line 67
    move-result-object v1

    .line 68
    check-cast v1, Lqe0/a;

    .line 70
    iget-object v2, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->y:Lqv0/u;

    .line 72
    invoke-virtual {v2}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 75
    move-result-object v2

    .line 76
    check-cast v2, Lmt/b;

    .line 78
    if-eqz v2, :cond_52

    .line 80
    iget-object v2, v2, Lmt/b;->d:Ljava/lang/String;

    .line 82
    goto :goto_53

    .line 83
    :cond_52
    const/4 v2, 0x0

    .line 84
    :goto_53
    const-string v3, "successScreenType"

    .line 86
    invoke-static {v0, v3}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 89
    sget-object v3, Lgm0/l$a$a;->a:[I

    .line 91
    invoke-virtual {v0}, Ljava/lang/Enum;->ordinal()I

    .line 94
    move-result v5

    .line 95
    aget v3, v3, v5

    .line 97
    const/4 v5, 0x1

    .line 98
    if-eq v3, v5, :cond_80

    .line 100
    const/4 v5, 0x2

    .line 101
    if-eq v3, v5, :cond_79

    .line 103
    const/4 v5, 0x3

    .line 104
    if-eq v3, v5, :cond_79

    .line 106
    const/4 v0, 0x4

    .line 107
    if-ne v3, v0, :cond_73

    .line 109
    new-instance v0, Lgm0/d;

    .line 111
    invoke-direct {v0, p0, v2}, Lgm0/d;-><init>(Landroid/content/Context;Ljava/lang/String;)V

    .line 114
    :goto_71
    move-object v5, v0

    .line 115
    goto :goto_86

    .line 116
    :cond_73
    new-instance p0, Lqv0/m;

    .line 118
    invoke-direct {p0}, Ljava/lang/RuntimeException;-><init>()V

    .line 121
    throw p0

    .line 122
    :cond_79
    new-instance v3, Lgm0/a;

    .line 124
    invoke-direct {v3, p0, v1, v0, v2}, Lgm0/a;-><init>(Landroid/content/Context;Lqe0/a;Lmt/a;Ljava/lang/String;)V

    .line 127
    move-object v5, v3

    .line 128
    goto :goto_86

    .line 129
    :cond_80
    new-instance v0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/success/a;

    .line 131
    invoke-direct {v0, p0, v1}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/success/a;-><init>(Landroid/content/Context;Lqe0/a;)V

    .line 134
    goto :goto_71

    .line 135
    :goto_86
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->v:Lqv0/u;

    .line 137
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 140
    move-result-object v0

    .line 141
    move-object v6, v0

    .line 142
    check-cast v6, Lfl0/f;

    .line 144
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->x:Lqv0/u;

    .line 146
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 149
    move-result-object v0

    .line 150
    move-object v7, v0

    .line 151
    check-cast v7, Lul0/i;

    .line 153
    invoke-static {p0}, Lzg0/b;->a(Landroid/content/Context;)Lzg0/a;

    .line 156
    move-result-object v0

    .line 157
    invoke-interface {v0}, Lzg0/a;->l()Lft/d;

    .line 160
    move-result-object v0

    .line 161
    invoke-interface {v0}, Lft/d;->d()Lub0/i;

    .line 164
    move-result-object v0

    .line 165
    invoke-virtual {v0}, Lub0/i;->getHasPremiumBenefit()Z

    .line 168
    move-result v8

    .line 169
    invoke-static {p0}, Lzg0/b;->a(Landroid/content/Context;)Lzg0/a;

    .line 172
    move-result-object v0

    .line 173
    invoke-interface {v0}, Lzg0/a;->l()Lft/d;

    .line 176
    move-result-object v0

    .line 177
    invoke-interface {v0}, Lft/d;->w()Lic/d;

    .line 180
    move-result-object v9

    .line 181
    const-string v0, "subscriptionAnalytics"

    .line 183
    invoke-static {v6, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 186
    const-string v0, "upgradeAnalytics"

    .line 188
    invoke-static {v7, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 191
    const-string v0, "availableTiersConfig"

    .line 193
    invoke-static {v9, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 196
    new-instance v2, Lul0/q;

    .line 198
    move-object v3, p0

    .line 199
    invoke-direct/range {v2 .. v9}, Lul0/q;-><init>(Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;Lul0/y;Lgm0/l;Lfl0/f;Lul0/i;ZLfw0/a;)V

    .line 202
    return-object v2
.end method

.method public static Tf(Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;)V
    .registers 6

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->B:Lqv0/u;

    .line 3
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 6
    move-result-object v0

    .line 7
    check-cast v0, Lul0/p;

    .line 9
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 12
    move-result-object v1

    .line 13
    iget-object v1, v1, Lpq0/e;->g:Lcom/ellation/crunchyroll/presentation/multitiersubscription/subscriptionbutton/CrPlusSubscriptionButton;

    .line 15
    invoke-virtual {v1}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/subscriptionbutton/CrPlusSubscriptionButton;->getButtonTextView()Lcom/google/android/material/button/MaterialButton;

    .line 18
    move-result-object v1

    .line 19
    const/4 v2, 0x0

    .line 20
    invoke-static {v1, v2}, Lra0/d;->a(Landroid/view/View;Ljava/lang/String;)Lra0/c;

    .line 23
    move-result-object v1

    .line 24
    invoke-virtual {p0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;

    .line 27
    move-result-object p0

    .line 28
    if-eqz p0, :cond_3b

    .line 30
    invoke-virtual {p0}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    .line 33
    move-result-object p0

    .line 34
    if-eqz p0, :cond_3b

    .line 36
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 38
    const/16 v3, 0x21

    .line 40
    const-string v4, "UPGRADE_EXTRA_EVENT_SOURCE_PROPERTY"

    .line 42
    if-lt v2, v3, :cond_32

    .line 44
    const-class v2, Lva0/m;

    .line 46
    invoke-virtual {p0, v4, v2}, Landroid/os/Bundle;->getSerializable(Ljava/lang/String;Ljava/lang/Class;)Ljava/io/Serializable;

    .line 49
    move-result-object p0

    .line 50
    goto :goto_38

    .line 51
    :cond_32
    invoke-virtual {p0, v4}, Landroid/os/Bundle;->getSerializable(Ljava/lang/String;)Ljava/io/Serializable;

    .line 54
    move-result-object p0

    .line 55
    check-cast p0, Lva0/m;

    .line 57
    :goto_38
    move-object v2, p0

    .line 58
    check-cast v2, Lva0/m;

    .line 60
    :cond_3b
    invoke-static {v2}, Lkotlin/jvm/internal/l;->c(Ljava/lang/Object;)V

    .line 63
    invoke-interface {v0, v1, v2}, Lul0/p;->t5(Lra0/c;Lva0/m;)V

    .line 66
    return-void
.end method


# virtual methods
.method public final C1(Lbm0/j;Lem0/a;Z)V
    .registers 12

    .line 1
    const-string v0, "product"

    .line 3
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    const-string v0, "ctaModel"

    .line 8
    invoke-static {p2, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 11
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 14
    move-result-object v0

    .line 15
    iget-object v1, v0, Lpq0/e;->d:Lcom/ellation/crunchyroll/presentation/multitiersubscription/disclaimer/CrPlusLegalDisclaimerTextView;

    .line 17
    iget p2, p2, Lem0/a;->b:I

    .line 19
    invoke-virtual {p0, p2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 22
    move-result-object p2

    .line 23
    const-string v0, "getString(...)"

    .line 25
    invoke-static {p2, v0}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 28
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    .line 31
    move-result-object v0

    .line 32
    const-string v2, "getDefault(...)"

    .line 34
    invoke-static {v0, v2}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 37
    invoke-virtual {p2, v0}, Ljava/lang/String;->toUpperCase(Ljava/util/Locale;)Ljava/lang/String;

    .line 40
    move-result-object v2

    .line 41
    const-string p2, "toUpperCase(...)"

    .line 43
    invoke-static {v2, p2}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 46
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 49
    move-result-object p2

    .line 50
    iget-object p2, p2, Lpq0/e;->d:Lcom/ellation/crunchyroll/presentation/multitiersubscription/disclaimer/CrPlusLegalDisclaimerTextView;

    .line 52
    sget-object v0, Lxa0/b;->PRODUCT_UPSELL_SUBSCRIPTION:Lxa0/b;

    .line 54
    invoke-static {p0, p2, v0}, Lps/i$a;->a(Ldq0/c;Lcom/ellation/crunchyroll/presentation/multitiersubscription/disclaimer/CrPlusLegalDisclaimerTextView;Lxa0/b;)Lps/j;

    .line 57
    move-result-object v4

    .line 58
    iget-object v5, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->o:Lbp0/e;

    .line 60
    if-eqz v5, :cond_46

    .line 62
    sget p2, Lcom/ellation/crunchyroll/presentation/multitiersubscription/disclaimer/CrPlusLegalDisclaimerTextView;->a:I

    .line 64
    const/4 v7, 0x0

    .line 65
    move-object v3, p1

    .line 66
    move v6, p3

    .line 67
    invoke-virtual/range {v1 .. v7}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/disclaimer/CrPlusLegalDisclaimerTextView;->v2(Ljava/lang/String;Lbm0/j;Lps/j;Lbp0/e;ZLjava/lang/String;)V

    .line 70
    return-void

    .line 71
    :cond_46
    const-string p1, "externalUriRouter"

    .line 73
    invoke-static {p1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 76
    const/4 p1, 0x0

    .line 77
    throw p1
.end method

.method public final U(Lem0/a;)V
    .registers 6

    .line 1
    const-string v0, "ctaButtonUiModel"

    .line 3
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 9
    move-result-object v0

    .line 10
    iget-object v0, v0, Lpq0/e;->g:Lcom/ellation/crunchyroll/presentation/multitiersubscription/subscriptionbutton/CrPlusSubscriptionButton;

    .line 12
    iget-object v1, v0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/subscriptionbutton/CrPlusSubscriptionButton;->a:Lyg0/a;

    .line 14
    iget-object v2, v1, Lyg0/a;->a:Lcom/google/android/material/button/MaterialButton;

    .line 16
    invoke-virtual {v0}, Landroid/view/View;->getContext()Landroid/content/Context;

    .line 19
    move-result-object v0

    .line 20
    iget v3, p1, Lem0/a;->a:I

    .line 22
    invoke-static {v0, v3}, Lx3/a;->getDrawable(Landroid/content/Context;I)Landroid/graphics/drawable/Drawable;

    .line 25
    move-result-object v0

    .line 26
    invoke-virtual {v2, v0}, Lcom/google/android/material/button/MaterialButton;->setIcon(Landroid/graphics/drawable/Drawable;)V

    .line 29
    iget-object v0, v1, Lyg0/a;->a:Lcom/google/android/material/button/MaterialButton;

    .line 31
    iget p1, p1, Lem0/a;->b:I

    .line 33
    invoke-virtual {v0, p1}, Landroid/widget/TextView;->setText(I)V

    .line 36
    return-void
.end method

.method public final Uf()Lpq0/e;
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->n:Lqv0/u;

    .line 3
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 6
    move-result-object v0

    .line 7
    check-cast v0, Lpq0/e;

    .line 9
    return-object v0
.end method

.method public final Vf()Lcl0/d;
    .registers 3

    .line 1
    const/4 v0, 0x0

    .line 2
    const/4 v1, 0x6

    .line 3
    invoke-static {p0, v0, v1}, Lcl0/d$a;->a(Landroid/content/Context;Lft/d;I)Lcl0/d;

    .line 6
    move-result-object v0

    .line 7
    return-object v0
.end method

.method public final a()V
    .registers 3

    .line 1
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 4
    move-result-object v0

    .line 5
    iget-object v0, v0, Lpq0/e;->e:Landroid/widget/FrameLayout;

    .line 7
    const-string v1, "progress"

    .line 9
    invoke-static {v0, v1}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 12
    const/4 v1, 0x0

    .line 13
    invoke-virtual {v0, v1}, Landroid/view/View;->setVisibility(I)V

    .line 16
    return-void
.end method

.method public final aa()V
    .registers 3

    .line 1
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 4
    move-result-object v0

    .line 5
    iget-object v0, v0, Lpq0/e;->k:Lcom/ellation/crunchyroll/presentation/multitiersubscription/alreadypremium/SubscriptionAlreadyPremiumLayout;

    .line 7
    const-string v1, "upgradeAlreadyPremiumLayout"

    .line 9
    invoke-static {v0, v1}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 12
    const/4 v1, 0x0

    .line 13
    invoke-virtual {v0, v1}, Landroid/view/View;->setVisibility(I)V

    .line 16
    return-void
.end method

.method public final c()V
    .registers 3

    .line 1
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 4
    move-result-object v0

    .line 5
    iget-object v0, v0, Lpq0/e;->e:Landroid/widget/FrameLayout;

    .line 7
    const-string v1, "progress"

    .line 9
    invoke-static {v0, v1}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 12
    const/16 v1, 0x8

    .line 14
    invoke-virtual {v0, v1}, Landroid/view/View;->setVisibility(I)V

    .line 17
    return-void
.end method

.method public final d1()V
    .registers 2

    .line 1
    const/4 v0, -0x1

    .line 2
    invoke-virtual {p0, v0}, Landroid/app/Activity;->setResult(I)V

    .line 5
    invoke-virtual {p0}, Landroid/app/Activity;->finish()V

    .line 8
    return-void
.end method

.method public final l9()V
    .registers 3

    .line 1
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 4
    move-result-object v0

    .line 5
    iget-object v0, v0, Lpq0/e;->l:Lpq0/p;

    .line 7
    iget-object v0, v0, Lpq0/p;->a:Landroidx/constraintlayout/widget/ConstraintLayout;

    .line 9
    const-string v1, "getRoot(...)"

    .line 11
    invoke-static {v0, v1}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 14
    const/4 v1, 0x0

    .line 15
    invoke-virtual {v0, v1}, Landroid/view/View;->setVisibility(I)V

    .line 18
    return-void
.end method

.method public final onCreate(Landroid/os/Bundle;)V
    .registers 6

    .line 1
    invoke-super {p0, p1}, Lul0/b;->onCreate(Landroid/os/Bundle;)V

    .line 4
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 7
    move-result-object p1

    .line 8
    iget-object p1, p1, Lpq0/e;->a:Landroidx/constraintlayout/widget/ConstraintLayout;

    .line 10
    invoke-virtual {p0, p1}, Ldq0/c;->setContentView(Landroid/view/View;)V

    .line 13
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 16
    move-result-object p1

    .line 17
    iget-object p1, p1, Lpq0/e;->a:Landroidx/constraintlayout/widget/ConstraintLayout;

    .line 19
    const-string v0, "getRoot(...)"

    .line 21
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 24
    new-instance v0, Lul0/c;

    .line 26
    const/4 v1, 0x0

    .line 27
    invoke-direct {v0, v1}, Lul0/c;-><init>(I)V

    .line 30
    invoke-static {p1, v0}, Lbx/m0;->b(Landroid/view/View;Lfw0/l;)V

    .line 33
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 36
    move-result-object p1

    .line 37
    iget-object p1, p1, Lpq0/e;->b:Landroid/widget/ImageView;

    .line 39
    new-instance v0, Lqj/f;

    .line 41
    const/4 v1, 0x1

    .line 42
    invoke-direct {v0, p0, v1}, Lqj/f;-><init>(Ljava/lang/Object;I)V

    .line 45
    invoke-virtual {p1, v0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 48
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 51
    move-result-object p1

    .line 52
    iget-object p1, p1, Lpq0/e;->g:Lcom/ellation/crunchyroll/presentation/multitiersubscription/subscriptionbutton/CrPlusSubscriptionButton;

    .line 54
    new-instance v0, Lul0/e;

    .line 56
    const/4 v1, 0x0

    .line 57
    invoke-direct {v0, p0, v1}, Lul0/e;-><init>(Ljava/lang/Object;I)V

    .line 60
    invoke-virtual {p1, v0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/subscriptionbutton/CrPlusSubscriptionButton;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 63
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 66
    move-result-object p1

    .line 67
    iget-object p1, p1, Lpq0/e;->i:Landroid/widget/ScrollView;

    .line 69
    new-instance v0, Lul0/f;

    .line 71
    invoke-direct {v0, p0}, Lul0/f;-><init>(Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;)V

    .line 74
    invoke-virtual {p1, v0}, Landroid/view/View;->setOnScrollChangeListener(Landroid/view/View$OnScrollChangeListener;)V

    .line 77
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 80
    move-result-object p1

    .line 81
    iget-object p1, p1, Lpq0/e;->h:Landroidx/compose/ui/platform/ComposeView;

    .line 83
    new-instance v0, Landroidx/xr/scenecore/f0;

    .line 85
    const/4 v1, 0x2

    .line 86
    invoke-direct {v0, p0, v1}, Landroidx/xr/scenecore/f0;-><init>(Ljava/lang/Object;I)V

    .line 89
    new-instance v1, Lh1/a;

    .line 91
    const v2, 0x1b652f7c

    .line 94
    const/4 v3, 0x1

    .line 95
    invoke-direct {v1, v2, v0, v3}, Lh1/a;-><init>(ILjava/lang/Object;Z)V

    .line 98
    invoke-virtual {p1, v1}, Landroidx/compose/ui/platform/ComposeView;->setContent(Lfw0/p;)V

    .line 101
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 104
    move-result-object p1

    .line 105
    iget-object p1, p1, Lpq0/e;->f:Lcom/ellation/crunchyroll/presentation/multitiersubscription/alternativeflow/SubscriptionAlternativeFlowLayout;

    .line 107
    sget-object v0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->C:[Lmw0/i;

    .line 109
    aget-object v0, v0, v3

    .line 111
    iget-object v1, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->A:Lkh0/a;

    .line 113
    invoke-virtual {v1, p0, v0}, Lkh0/a;->a(Ljava/lang/Object;Lmw0/i;)Landroidx/lifecycle/o1;

    .line 116
    move-result-object v0

    .line 117
    check-cast v0, Ldm0/d;

    .line 119
    invoke-virtual {p1, v0, p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/alternativeflow/SubscriptionAlternativeFlowLayout;->h4(Ldm0/d;Lel0/c;)V

    .line 122
    invoke-virtual {p0}, Le/k;->getOnBackPressedDispatcher()Le/h0;

    .line 125
    move-result-object p1

    .line 126
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->u:Lse0/a;

    .line 128
    invoke-virtual {p1, p0, v0}, Le/h0;->a(Landroidx/lifecycle/e0;Le/a0;)V

    .line 131
    return-void
.end method

.method public final setupPresenters()Ljava/util/Set;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Set<",
            "Lch0/m;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->B:Lqv0/u;

    .line 3
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 6
    move-result-object v0

    .line 7
    check-cast v0, Lul0/p;

    .line 9
    invoke-static {v0}, Lcx0/j;->h(Ljava/lang/Object;)Ljava/util/Set;

    .line 12
    move-result-object v0

    .line 13
    return-object v0
.end method

.method public final z(Lfw0/a;)V
    .registers 11
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lfw0/a<",
            "Lqv0/i0;",
            ">;)V"
        }
    .end annotation

    .line 1
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/multitiersubscription/extendedupgrade/UpgradeActivity;->Uf()Lpq0/e;

    .line 4
    move-result-object v0

    .line 5
    iget-object v1, v0, Lpq0/e;->c:Landroid/widget/FrameLayout;

    .line 7
    const-wide/16 v6, 0x0

    .line 9
    const/16 v8, 0xfe

    .line 11
    const/4 v3, 0x0

    .line 12
    const-wide/16 v4, 0x0

    .line 14
    move-object v2, p1

    .line 15
    invoke-static/range {v1 .. v8}, Lfq0/j;->d(Landroid/view/ViewGroup;Lfw0/a;Lfw0/a;JJI)V

    .line 18
    return-void
.end method
