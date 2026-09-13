# classes3.dex

.class public final Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;
.super Ljava/lang/Object;
.source "Benefit.kt"


# direct methods
.method public static final getStreamingBenefitsMax(Ljava/util/List;)I
    .registers 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Ljava/lang/String;",
            ">;)I"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    new-instance v0, Ljava/util/ArrayList;

    .line 10
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 13
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 16
    move-result-object p0

    .line 17
    :cond_10
    :goto_10
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 20
    move-result v1

    .line 21
    const/4 v2, 0x0

    .line 22
    if-eqz v1, :cond_3b

    .line 24
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 27
    move-result-object v1

    .line 28
    check-cast v1, Ljava/lang/String;

    .line 30
    const-string v3, "concurrent_streams"

    .line 32
    invoke-static {v1, v3, v2}, Lvx0/o;->z(Ljava/lang/String;Ljava/lang/String;Z)Z

    .line 35
    move-result v2

    .line 36
    if-eqz v2, :cond_34

    .line 38
    const-string v2, "."

    .line 40
    invoke-static {v1, v2, v1}, Lvx0/s;->b0(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 43
    move-result-object v1

    .line 44
    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    .line 47
    move-result v1

    .line 48
    invoke-static {v1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 51
    move-result-object v1

    .line 52
    goto :goto_35

    .line 53
    :cond_34
    const/4 v1, 0x0

    .line 54
    :goto_35
    if-eqz v1, :cond_10

    .line 56
    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 59
    goto :goto_10

    .line 60
    :cond_3b
    invoke-static {v0}, Lyw0/r;->V(Ljava/lang/Iterable;)Ljava/lang/Comparable;

    .line 63
    move-result-object p0

    .line 64
    check-cast p0, Ljava/lang/Integer;

    .line 66
    if-eqz p0, :cond_48

    .line 68
    invoke-virtual {p0}, Ljava/lang/Integer;->intValue()I

    .line 71
    move-result p0

    .line 72
    return p0

    .line 73
    :cond_48
    return v2
.end method

.method public static final hasBentoBenefit(Ljava/util/List;)Z
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    const/4 v1, 0x0

    .line 11
    if-eqz v0, :cond_16

    .line 13
    move-object v0, p0

    .line 14
    check-cast v0, Ljava/util/Collection;

    .line 16
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 19
    move-result v0

    .line 20
    if-eqz v0, :cond_16

    .line 22
    return v1

    .line 23
    :cond_16
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 26
    move-result-object p0

    .line 27
    :cond_1a
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 30
    move-result v0

    .line 31
    if-eqz v0, :cond_2e

    .line 33
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 36
    move-result-object v0

    .line 37
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 39
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isBentoBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 42
    move-result v0

    .line 43
    if-eqz v0, :cond_1a

    .line 45
    const/4 p0, 0x1

    .line 46
    return p0

    .line 47
    :cond_2e
    return v1
.end method

.method public static final hasMangaBenefit(Ljava/util/List;)Z
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    const/4 v1, 0x0

    .line 11
    if-eqz v0, :cond_16

    .line 13
    move-object v0, p0

    .line 14
    check-cast v0, Ljava/util/Collection;

    .line 16
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 19
    move-result v0

    .line 20
    if-eqz v0, :cond_16

    .line 22
    return v1

    .line 23
    :cond_16
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 26
    move-result-object p0

    .line 27
    :cond_1a
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 30
    move-result v0

    .line 31
    if-eqz v0, :cond_2e

    .line 33
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 36
    move-result-object v0

    .line 37
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 39
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isMangaBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 42
    move-result v0

    .line 43
    if-eqz v0, :cond_1a

    .line 45
    const/4 p0, 0x1

    .line 46
    return p0

    .line 47
    :cond_2e
    return v1
.end method

.method public static final hasOfflineViewingBenefit(Ljava/util/List;)Z
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    const/4 v1, 0x0

    .line 11
    if-eqz v0, :cond_16

    .line 13
    move-object v0, p0

    .line 14
    check-cast v0, Ljava/util/Collection;

    .line 16
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 19
    move-result v0

    .line 20
    if-eqz v0, :cond_16

    .line 22
    return v1

    .line 23
    :cond_16
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 26
    move-result-object p0

    .line 27
    :cond_1a
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 30
    move-result v0

    .line 31
    if-eqz v0, :cond_34

    .line 33
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 36
    move-result-object v0

    .line 37
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 39
    invoke-virtual {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 42
    move-result-object v0

    .line 43
    const-string v2, "offline_viewing"

    .line 45
    invoke-static {v0, v2}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 48
    move-result v0

    .line 49
    if-eqz v0, :cond_1a

    .line 51
    const/4 p0, 0x1

    .line 52
    return p0

    .line 53
    :cond_34
    return v1
.end method

.method public static final hasPremiumBenefit(Ljava/util/List;)Z
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    const/4 v1, 0x0

    .line 11
    if-eqz v0, :cond_16

    .line 13
    move-object v0, p0

    .line 14
    check-cast v0, Ljava/util/Collection;

    .line 16
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 19
    move-result v0

    .line 20
    if-eqz v0, :cond_16

    .line 22
    return v1

    .line 23
    :cond_16
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 26
    move-result-object p0

    .line 27
    :cond_1a
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 30
    move-result v0

    .line 31
    if-eqz v0, :cond_2e

    .line 33
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 36
    move-result-object v0

    .line 37
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 39
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isPremium(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 42
    move-result v0

    .line 43
    if-eqz v0, :cond_1a

    .line 45
    const/4 p0, 0x1

    .line 46
    return p0

    .line 47
    :cond_2e
    return v1
.end method

.method public static final hasStoreDiscountBenefit(Ljava/util/List;)Z
    .registers 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    const/4 v1, 0x0

    .line 11
    if-eqz v0, :cond_16

    .line 13
    move-object v0, p0

    .line 14
    check-cast v0, Ljava/util/Collection;

    .line 16
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 19
    move-result v0

    .line 20
    if-eqz v0, :cond_16

    .line 22
    return v1

    .line 23
    :cond_16
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 26
    move-result-object p0

    .line 27
    :cond_1a
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 30
    move-result v0

    .line 31
    if-eqz v0, :cond_64

    .line 33
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 36
    move-result-object v0

    .line 37
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 39
    invoke-virtual {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 42
    move-result-object v2

    .line 43
    const-string v3, "cr_store.member_offers_and_percent_off.10"

    .line 45
    invoke-static {v2, v3}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 48
    move-result v2

    .line 49
    if-nez v2, :cond_62

    .line 51
    invoke-virtual {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 54
    move-result-object v2

    .line 55
    const-string v3, "cr_store.member_offers_and_percent_off.20"

    .line 57
    invoke-static {v2, v3}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 60
    move-result v2

    .line 61
    if-nez v2, :cond_62

    .line 63
    invoke-virtual {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 66
    move-result-object v2

    .line 67
    const-string v3, "cr_store.member_offers_and_early_access_and_percent_off.5"

    .line 69
    invoke-static {v2, v3}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 72
    move-result v2

    .line 73
    if-nez v2, :cond_62

    .line 75
    invoke-virtual {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 78
    move-result-object v2

    .line 79
    const-string v3, "cr_store.member_offers_and_early_access_and_percent_off.10"

    .line 81
    invoke-static {v2, v3}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 84
    move-result v2

    .line 85
    if-nez v2, :cond_62

    .line 87
    invoke-virtual {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 90
    move-result-object v0

    .line 91
    const-string v2, "cr_store.member_offers_and_early_access_and_percent_off.15"

    .line 93
    invoke-static {v0, v2}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 96
    move-result v0

    .line 97
    if-eqz v0, :cond_1a

    .line 99
    :cond_62
    const/4 p0, 0x1

    .line 100
    return p0

    .line 101
    :cond_64
    return v1
.end method

.method public static final hasUltimateFanBenefit(Ljava/util/List;)Z
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    const/4 v1, 0x0

    .line 11
    if-eqz v0, :cond_16

    .line 13
    move-object v0, p0

    .line 14
    check-cast v0, Ljava/util/Collection;

    .line 16
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 19
    move-result v0

    .line 20
    if-eqz v0, :cond_16

    .line 22
    return v1

    .line 23
    :cond_16
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 26
    move-result-object p0

    .line 27
    :cond_1a
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 30
    move-result v0

    .line 31
    if-eqz v0, :cond_2e

    .line 33
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 36
    move-result-object v0

    .line 37
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 39
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isUltimateFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 42
    move-result v0

    .line 43
    if-eqz v0, :cond_1a

    .line 45
    const/4 p0, 0x1

    .line 46
    return p0

    .line 47
    :cond_2e
    return v1
.end method

.method public static final isAnnualDiscountBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 3

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    const-string v0, "annual_discount"

    .line 12
    const/4 v1, 0x0

    .line 13
    invoke-static {p0, v0, v1}, Lvx0/o;->z(Ljava/lang/String;Ljava/lang/String;Z)Z

    .line 16
    move-result p0

    .line 17
    return p0
.end method

.method public static final isAnnualMegaFunUser(Ljava/util/List;)Z
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    if-eqz v0, :cond_15

    .line 12
    move-object v1, p0

    .line 13
    check-cast v1, Ljava/util/Collection;

    .line 15
    invoke-interface {v1}, Ljava/util/Collection;->isEmpty()Z

    .line 18
    move-result v1

    .line 19
    if-eqz v1, :cond_15

    .line 21
    goto :goto_4f

    .line 22
    :cond_15
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 25
    move-result-object v1

    .line 26
    :cond_19
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 29
    move-result v2

    .line 30
    if-eqz v2, :cond_4f

    .line 32
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 35
    move-result-object v2

    .line 36
    check-cast v2, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 38
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isAnnualDiscountBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 41
    move-result v2

    .line 42
    if-eqz v2, :cond_19

    .line 44
    if-eqz v0, :cond_37

    .line 46
    move-object v0, p0

    .line 47
    check-cast v0, Ljava/util/Collection;

    .line 49
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 52
    move-result v0

    .line 53
    if-eqz v0, :cond_37

    .line 55
    goto :goto_4f

    .line 56
    :cond_37
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 59
    move-result-object p0

    .line 60
    :cond_3b
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 63
    move-result v0

    .line 64
    if-eqz v0, :cond_4f

    .line 66
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 69
    move-result-object v0

    .line 70
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 72
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 75
    move-result v0

    .line 76
    if-eqz v0, :cond_3b

    .line 78
    const/4 p0, 0x1

    .line 79
    return p0

    .line 80
    :cond_4f
    :goto_4f
    const/4 p0, 0x0

    .line 81
    return p0
.end method

.method public static final isAtLeastMegaFanUser(Ljava/util/List;)Z
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    if-eqz v0, :cond_15

    .line 12
    move-object v1, p0

    .line 13
    check-cast v1, Ljava/util/Collection;

    .line 15
    invoke-interface {v1}, Ljava/util/Collection;->isEmpty()Z

    .line 18
    move-result v1

    .line 19
    if-eqz v1, :cond_15

    .line 21
    goto :goto_4f

    .line 22
    :cond_15
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 25
    move-result-object v1

    .line 26
    :cond_19
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 29
    move-result v2

    .line 30
    if-eqz v2, :cond_4f

    .line 32
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 35
    move-result-object v2

    .line 36
    check-cast v2, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 38
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isPremium(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 41
    move-result v2

    .line 42
    if-eqz v2, :cond_19

    .line 44
    if-eqz v0, :cond_37

    .line 46
    move-object v0, p0

    .line 47
    check-cast v0, Ljava/util/Collection;

    .line 49
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 52
    move-result v0

    .line 53
    if-eqz v0, :cond_37

    .line 55
    goto :goto_4f

    .line 56
    :cond_37
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 59
    move-result-object p0

    .line 60
    :cond_3b
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 63
    move-result v0

    .line 64
    if-eqz v0, :cond_4f

    .line 66
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 69
    move-result-object v0

    .line 70
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 72
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 75
    move-result v0

    .line 76
    if-eqz v0, :cond_3b

    .line 78
    const/4 p0, 0x1

    .line 79
    return p0

    .line 80
    :cond_4f
    :goto_4f
    const/4 p0, 0x0

    .line 81
    return p0
.end method

.method public static final isBentoBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 2

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    const-string v0, "cr_bento"

    .line 12
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 15
    move-result p0

    .line 16
    return p0
.end method

.method public static final isCrBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 2

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getSource()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    const/4 v0, 0x1

    .line 11
    if-eqz p0, :cond_15

    .line 13
    invoke-interface {p0}, Ljava/lang/CharSequence;->length()I

    .line 16
    move-result p0

    .line 17
    if-nez p0, :cond_13

    .line 19
    return v0

    .line 20
    :cond_13
    const/4 p0, 0x0

    .line 21
    return p0

    .line 22
    :cond_15
    return v0
.end method

.method public static final isFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 2

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    const-string v0, "cr_fan_pack"

    .line 12
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 15
    move-result p0

    .line 16
    return p0
.end method

.method public static final isFunBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 3

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getSource()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    if-eqz p0, :cond_13

    .line 12
    const-string v0, "funimation_"

    .line 14
    const/4 v1, 0x1

    .line 15
    invoke-static {p0, v0, v1}, Lvx0/o;->z(Ljava/lang/String;Ljava/lang/String;Z)Z

    .line 18
    move-result p0

    .line 19
    return p0

    .line 20
    :cond_13
    const/4 p0, 0x0

    .line 21
    return p0
.end method

.method public static final isFunimationFanUser(Ljava/util/List;)Z
    .registers 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    if-eqz v0, :cond_15

    .line 12
    move-object v1, p0

    .line 13
    check-cast v1, Ljava/util/Collection;

    .line 15
    invoke-interface {v1}, Ljava/util/Collection;->isEmpty()Z

    .line 18
    move-result v1

    .line 19
    if-eqz v1, :cond_15

    .line 21
    goto :goto_5c

    .line 22
    :cond_15
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 25
    move-result-object v1

    .line 26
    :cond_19
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 29
    move-result v2

    .line 30
    if-eqz v2, :cond_5c

    .line 32
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 35
    move-result-object v2

    .line 36
    check-cast v2, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 38
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 41
    move-result v3

    .line 42
    if-eqz v3, :cond_19

    .line 44
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFunBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 47
    move-result v2

    .line 48
    if-eqz v2, :cond_19

    .line 50
    if-eqz v0, :cond_3d

    .line 52
    move-object v0, p0

    .line 53
    check-cast v0, Ljava/util/Collection;

    .line 55
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 58
    move-result v0

    .line 59
    if-eqz v0, :cond_3d

    .line 61
    goto :goto_5a

    .line 62
    :cond_3d
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 65
    move-result-object p0

    .line 66
    :cond_41
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 69
    move-result v0

    .line 70
    if-eqz v0, :cond_5a

    .line 72
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 75
    move-result-object v0

    .line 76
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 78
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 81
    move-result v1

    .line 82
    if-eqz v1, :cond_41

    .line 84
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isCrBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 87
    move-result v0

    .line 88
    if-eqz v0, :cond_41

    .line 90
    goto :goto_5c

    .line 91
    :cond_5a
    :goto_5a
    const/4 p0, 0x1

    .line 92
    return p0

    .line 93
    :cond_5c
    :goto_5c
    const/4 p0, 0x0

    .line 94
    return p0
.end method

.method public static final isFunimationPremiumUser(Ljava/util/List;)Z
    .registers 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    if-eqz v0, :cond_15

    .line 12
    move-object v1, p0

    .line 13
    check-cast v1, Ljava/util/Collection;

    .line 15
    invoke-interface {v1}, Ljava/util/Collection;->isEmpty()Z

    .line 18
    move-result v1

    .line 19
    if-eqz v1, :cond_15

    .line 21
    goto :goto_5c

    .line 22
    :cond_15
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 25
    move-result-object v1

    .line 26
    :cond_19
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 29
    move-result v2

    .line 30
    if-eqz v2, :cond_5c

    .line 32
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 35
    move-result-object v2

    .line 36
    check-cast v2, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 38
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isPremium(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 41
    move-result v3

    .line 42
    if-eqz v3, :cond_19

    .line 44
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFunBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 47
    move-result v2

    .line 48
    if-eqz v2, :cond_19

    .line 50
    if-eqz v0, :cond_3d

    .line 52
    move-object v0, p0

    .line 53
    check-cast v0, Ljava/util/Collection;

    .line 55
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 58
    move-result v0

    .line 59
    if-eqz v0, :cond_3d

    .line 61
    goto :goto_5a

    .line 62
    :cond_3d
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 65
    move-result-object p0

    .line 66
    :cond_41
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 69
    move-result v0

    .line 70
    if-eqz v0, :cond_5a

    .line 72
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 75
    move-result-object v0

    .line 76
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 78
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isPremium(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 81
    move-result v1

    .line 82
    if-eqz v1, :cond_41

    .line 84
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isCrBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 87
    move-result v0

    .line 88
    if-eqz v0, :cond_41

    .line 90
    goto :goto_5c

    .line 91
    :cond_5a
    :goto_5a
    const/4 p0, 0x1

    .line 92
    return p0

    .line 93
    :cond_5c
    :goto_5c
    const/4 p0, 0x0

    .line 94
    return p0
.end method

.method public static final isFunimationUltimateFanUser(Ljava/util/List;)Z
    .registers 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    if-eqz v0, :cond_15

    .line 12
    move-object v1, p0

    .line 13
    check-cast v1, Ljava/util/Collection;

    .line 15
    invoke-interface {v1}, Ljava/util/Collection;->isEmpty()Z

    .line 18
    move-result v1

    .line 19
    if-eqz v1, :cond_15

    .line 21
    goto :goto_5c

    .line 22
    :cond_15
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 25
    move-result-object v1

    .line 26
    :cond_19
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 29
    move-result v2

    .line 30
    if-eqz v2, :cond_5c

    .line 32
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 35
    move-result-object v2

    .line 36
    check-cast v2, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 38
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isUltimateFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 41
    move-result v3

    .line 42
    if-eqz v3, :cond_19

    .line 44
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFunBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 47
    move-result v2

    .line 48
    if-eqz v2, :cond_19

    .line 50
    if-eqz v0, :cond_3d

    .line 52
    move-object v0, p0

    .line 53
    check-cast v0, Ljava/util/Collection;

    .line 55
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 58
    move-result v0

    .line 59
    if-eqz v0, :cond_3d

    .line 61
    goto :goto_5a

    .line 62
    :cond_3d
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 65
    move-result-object p0

    .line 66
    :cond_41
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 69
    move-result v0

    .line 70
    if-eqz v0, :cond_5a

    .line 72
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 75
    move-result-object v0

    .line 76
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 78
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isUltimateFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 81
    move-result v1

    .line 82
    if-eqz v1, :cond_41

    .line 84
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isCrBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 87
    move-result v0

    .line 88
    if-eqz v0, :cond_41

    .line 90
    goto :goto_5c

    .line 91
    :cond_5a
    :goto_5a
    const/4 p0, 0x1

    .line 92
    return p0

    .line 93
    :cond_5c
    :goto_5c
    const/4 p0, 0x0

    .line 94
    return p0
.end method

.method public static final isMangaBenefit(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 2

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    const-string v0, "cr_manga"

    .line 12
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 15
    move-result p0

    .line 16
    return p0
.end method

.method public static final isPremium(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 2

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    const-string v0, "cr_premium"

    .line 12
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 15
    move-result p0

    .line 16
    return p0
.end method

.method public static final isUltimateFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z
    .registers 2

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;->getBenefit()Ljava/lang/String;

    .line 9
    move-result-object p0

    .line 10
    const-string v0, "cr_premium_plus"

    .line 12
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->a(Ljava/lang/Object;Ljava/lang/Object;)Z

    .line 15
    move-result p0

    .line 16
    return p0
.end method

.method public static final isUltimateFanUser(Ljava/util/List;)Z
    .registers 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/List<",
            "Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;",
            ">;)Z"
        }
    .end annotation

    .line 1
    const-string v0, "<this>"

    .line 3
    invoke-static {p0, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    check-cast p0, Ljava/lang/Iterable;

    .line 8
    instance-of v0, p0, Ljava/util/Collection;

    .line 10
    if-eqz v0, :cond_15

    .line 12
    move-object v1, p0

    .line 13
    check-cast v1, Ljava/util/Collection;

    .line 15
    invoke-interface {v1}, Ljava/util/Collection;->isEmpty()Z

    .line 18
    move-result v1

    .line 19
    if-eqz v1, :cond_15

    .line 21
    goto :goto_71

    .line 22
    :cond_15
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 25
    move-result-object v1

    .line 26
    :cond_19
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 29
    move-result v2

    .line 30
    if-eqz v2, :cond_71

    .line 32
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 35
    move-result-object v2

    .line 36
    check-cast v2, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 38
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isPremium(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 41
    move-result v2

    .line 42
    if-eqz v2, :cond_19

    .line 44
    if-eqz v0, :cond_37

    .line 46
    move-object v1, p0

    .line 47
    check-cast v1, Ljava/util/Collection;

    .line 49
    invoke-interface {v1}, Ljava/util/Collection;->isEmpty()Z

    .line 52
    move-result v1

    .line 53
    if-eqz v1, :cond_37

    .line 55
    goto :goto_71

    .line 56
    :cond_37
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 59
    move-result-object v1

    .line 60
    :cond_3b
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    .line 63
    move-result v2

    .line 64
    if-eqz v2, :cond_71

    .line 66
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 69
    move-result-object v2

    .line 70
    check-cast v2, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 72
    invoke-static {v2}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 75
    move-result v2

    .line 76
    if-eqz v2, :cond_3b

    .line 78
    if-eqz v0, :cond_59

    .line 80
    move-object v0, p0

    .line 81
    check-cast v0, Ljava/util/Collection;

    .line 83
    invoke-interface {v0}, Ljava/util/Collection;->isEmpty()Z

    .line 86
    move-result v0

    .line 87
    if-eqz v0, :cond_59

    .line 89
    goto :goto_71

    .line 90
    :cond_59
    invoke-interface {p0}, Ljava/lang/Iterable;->iterator()Ljava/util/Iterator;

    .line 93
    move-result-object p0

    .line 94
    :cond_5d
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    .line 97
    move-result v0

    .line 98
    if-eqz v0, :cond_71

    .line 100
    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    .line 103
    move-result-object v0

    .line 104
    check-cast v0, Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;

    .line 106
    invoke-static {v0}, Lcom/ellation/crunchyroll/api/etp/subscription/model/BenefitKt;->isUltimateFan(Lcom/ellation/crunchyroll/api/etp/subscription/model/Benefit;)Z

    .line 109
    move-result v0

    .line 110
    if-eqz v0, :cond_5d

    .line 112
    const/4 p0, 0x1

    .line 113
    return p0

    .line 114
    :cond_71
    :goto_71
    const/4 p0, 0x0

    .line 115
    return p0
.end method
