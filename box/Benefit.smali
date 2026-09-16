# classes3.dex

.class public final Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;
.super Ljava/lang/Object;
.source "Benefit.kt"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit$Companion;
    }
.end annotation


# static fields
.field public static final $stable:I = 0x0

.field public static final BENTO_BENEFIT:Ljava/lang/String; = "cr_bento"

.field public static final Companion:Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit$Companion;

.field public static final MANGA_BENEFIT:Ljava/lang/String; = "cr_manga"

.field public static final OFFLINE_VIEWING_BENEFIT:Ljava/lang/String; = "offline_viewing"


# instance fields
.field private final benefit:Ljava/lang/String;
    .annotation runtime Lcom/google/gson/annotations/SerializedName;
        value = "benefit"
    .end annotation
.end field

.field private final source:Ljava/lang/String;
    .annotation runtime Lcom/google/gson/annotations/SerializedName;
        value = "source"
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .registers 2

    .line 1
    new-instance v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit$Companion;

    .line 3
    const/4 v1, 0x0

    .line 4
    invoke-direct {v0, v1}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit$Companion;-><init>(Lkotlin/jvm/internal/g;)V

    .line 7
    sput-object v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->Companion:Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit$Companion;

    .line 9
    return-void
.end method

.method public constructor <init>(Ljava/lang/String;Ljava/lang/String;)V
    .registers 4

    .line 1
    const-string v0, "benefit"

    .line 3
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 9
    iput-object p1, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 11
    iput-object p2, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 13
    return-void
.end method

.method public static synthetic copy$default(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;Ljava/lang/String;Ljava/lang/String;ILjava/lang/Object;)Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;
    .registers 5

    .line 1
    and-int/lit8 p4, p3, 0x1

    .line 3
    if-eqz p4, :cond_6

    .line 5
    iget-object p1, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 7
    :cond_6
    and-int/lit8 p3, p3, 0x2

    .line 9
    if-eqz p3, :cond_c

    .line 11
    iget-object p2, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 13
    :cond_c
    invoke-virtual {p0, p1, p2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->copy(Ljava/lang/String;Ljava/lang/String;)Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 16
    move-result-object p0

    .line 17
    return-object p0
.end method


# virtual methods
.method public final component1()Ljava/lang/String;
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 3
    return-object v0
.end method

.method public final component2()Ljava/lang/String;
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 3
    return-object v0
.end method

.method public final copy(Ljava/lang/String;Ljava/lang/String;)Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;
    .registers 4

    .line 1
    const-string v0, "benefit"

    .line 3
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    new-instance v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 8
    invoke-direct {v0, p1, p2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    .line 11
    return-object v0
.end method

.method public equals(Ljava/lang/Object;)Z
    .registers 6

    .line 1
    const/4 v0, 0x1

    .line 2
    if-ne p0, p1, :cond_4

    .line 4
    return v0

    .line 5
    :cond_4
    instance-of v1, p1, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 7
    const/4 v2, 0x0

    .line 8
    if-nez v1, :cond_a

    .line 10
    return v2

    .line 11
    :cond_a
    check-cast p1, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 13
    iget-object v1, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 15
    iget-object v3, p1, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 17
    invoke-static {v1, v3}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 20
    move-result v1

    .line 21
    if-nez v1, :cond_17

    .line 23
    return v2

    .line 24
    :cond_17
    iget-object v1, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 26
    iget-object p1, p1, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 28
    invoke-static {v1, p1}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 31
    move-result p1

    .line 32
    if-nez p1, :cond_22

    .line 34
    return v2

    .line 35
    :cond_22
    return v0
.end method

.method public final getBenefit()Ljava/lang/String;
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 3
    return-object v0
.end method

.method public final getSource()Ljava/lang/String;
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 3
    return-object v0
.end method

.method public hashCode()I
    .registers 3

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 3
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    .line 6
    move-result v0

    .line 7
    mul-int/lit8 v0, v0, 0x1f

    .line 9
    iget-object v1, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 11
    if-nez v1, :cond_e

    .line 13
    const/4 v1, 0x0

    .line 14
    goto :goto_12

    .line 15
    :cond_e
    invoke-virtual {v1}, Ljava/lang/String;->hashCode()I

    .line 18
    move-result v1

    .line 19
    :goto_12
    add-int/2addr v0, v1

    .line 20
    return v0
.end method

.method public toString()Ljava/lang/String;
    .registers 6

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->benefit:Ljava/lang/String;

    .line 3
    iget-object v1, p0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->source:Ljava/lang/String;

    .line 5
    const-string v2, ", source="

    .line 7
    const-string v3, ")"

    .line 9
    const-string v4, "Benefit(benefit="

    .line 11
    invoke-static {v4, v0, v2, v1, v3}, Lp6/x0;->b(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 14
    move-result-object v0

    .line 15
    return-object v0
.end method
