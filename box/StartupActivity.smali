.class public final Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;
.super Lmo0/g;
.source "StartupActivity.kt"

# interfaces
.implements Lmo0/d;
.implements Lmo0/y;


# static fields
.field public static final synthetic G:I


# instance fields
.field public final A:Lqv0/u;

.field public final B:Lmo0/s;

.field public final C:Lqv0/u;

.field public final D:Lqv0/u;

.field public final E:Lqv0/u;

.field public final F:I

.field public n:Lpb0/a;

.field public o:Lps/f;

.field public p:Lxi/a;

.field public q:Lyl/c;

.field public r:Lfm/a;

.field public s:Ljz/a;

.field public t:Lmz/n;

.field public u:Loo0/g;

.field public v:Lcom/ellation/crunchyroll/features/configs/z1;

.field public w:Lbg/d;

.field public x:Lfg/c;

.field public final y:Landroidx/lifecycle/q1;

.field public z:Landroid/view/ViewGroup;


# direct methods
.method public constructor <init>()V
    .registers 6

    .line 1
    invoke-direct {p0}, Lmo0/g;-><init>()V

    .line 4
    new-instance v0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$h;

    .line 6
    invoke-direct {v0, p0}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$h;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)V

    .line 9
    new-instance v1, Landroidx/lifecycle/q1;

    .line 11
    const-class v2, Lcom/ellation/crunchyroll/presentation/startup/b;

    .line 13
    invoke-static {v2}, Lkotlin/jvm/internal/f0;->a(Ljava/lang/Class;)Lkotlin/jvm/internal/e;

    .line 16
    move-result-object v2

    .line 17
    new-instance v3, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$i;

    .line 19
    invoke-direct {v3, p0}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$i;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)V

    .line 22
    new-instance v4, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$j;

    .line 24
    invoke-direct {v4, p0}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$j;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)V

    .line 27
    invoke-direct {v1, v2, v3, v0, v4}, Landroidx/lifecycle/q1;-><init>(Lkotlin/jvm/internal/e;Lfw0/a;Lfw0/a;Lfw0/a;)V

    .line 30
    iput-object v1, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->y:Landroidx/lifecycle/q1;

    .line 32
    new-instance v0, Landroidx/xr/compose/platform/b;

    .line 34
    const/4 v1, 0x2

    .line 35
    invoke-direct {v0, p0, v1}, Landroidx/xr/compose/platform/b;-><init>(Ljava/lang/Object;I)V

    .line 38
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 41
    move-result-object v0

    .line 42
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->A:Lqv0/u;

    .line 44
    sget-boolean v0, Lib0/l;->a:Z

    .line 46
    sget-object v0, Loa0/c;->a:Loa0/c;

    .line 48
    new-instance v0, Lmo0/s;

    .line 50
    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    .line 53
    new-instance v2, Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 55
    const/4 v3, 0x1

    .line 56
    invoke-direct {v2, v3}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>(Z)V

    .line 59
    iput-object v2, v0, Lmo0/s;->a:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 61
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->B:Lmo0/s;

    .line 63
    new-instance v0, Landroidx/xr/compose/platform/c;

    .line 65
    invoke-direct {v0, p0, v1}, Landroidx/xr/compose/platform/c;-><init>(Ljava/lang/Object;I)V

    .line 68
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 71
    move-result-object v0

    .line 72
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->C:Lqv0/u;

    .line 74
    new-instance v0, Landroidx/xr/compose/platform/d;

    .line 76
    invoke-direct {v0, p0, v1}, Landroidx/xr/compose/platform/d;-><init>(Ljava/lang/Object;I)V

    .line 79
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 82
    move-result-object v0

    .line 83
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->D:Lqv0/u;

    .line 85
    new-instance v0, Ldd/k1;

    .line 87
    invoke-direct {v0, p0, v1}, Ldd/k1;-><init>(Ljava/lang/Object;I)V

    .line 90
    invoke-static {v0}, Lqv0/k;->b(Lfw0/a;)Lqv0/u;

    .line 93
    move-result-object v0

    .line 94
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->E:Lqv0/u;

    .line 96
    const v0, 0x7f0e06af

    .line 99
    iput v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->F:I

    .line 101
    return-void
.end method

.method public static Rf(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)Lmo0/w;
    .registers 26

    .line 1
    move-object/from16 v1, p0

    .line 3
    iget-object v0, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->D:Lqv0/u;

    .line 5
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 8
    move-result-object v0

    .line 9
    move-object v2, v0

    .line 10
    check-cast v2, Lyn/y;

    .line 12
    iget-object v3, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->n:Lpb0/a;

    .line 14
    if-eqz v3, :cond_1a3

    .line 16
    sget-object v4, Lvg0/d;->a:Lvg0/d;

    .line 18
    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 21
    sget-object v4, Lvg0/d;->c:Ljq0/l;

    .line 23
    if-eqz v4, :cond_19b

    .line 25
    sget-object v5, Lob0/i;->b:Lob0/i;

    .line 27
    invoke-static {}, Lob0/i$b;->a()Lob0/i;

    .line 30
    move-result-object v5

    .line 31
    sget-object v6, Lup0/i$a;->a:Lup0/j;

    .line 33
    if-nez v6, :cond_29

    .line 35
    new-instance v6, Lup0/j;

    .line 37
    invoke-direct {v6, v5}, Lup0/j;-><init>(Landroid/content/Context;)V

    .line 40
    sput-object v6, Lup0/i$a;->a:Lup0/j;

    .line 42
    :cond_29
    sget-object v5, Lup0/i$a;->a:Lup0/j;

    .line 44
    invoke-static {v5}, Lkotlin/jvm/internal/l;->c(Ljava/lang/Object;)V

    .line 47
    iget-object v6, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->B:Lmo0/s;

    .line 49
    iget-object v7, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->C:Lqv0/u;

    .line 51
    invoke-virtual {v7}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 54
    move-result-object v7

    .line 55
    check-cast v7, Lyn/w;

    .line 57
    invoke-interface {v7}, Lyn/w;->a()Lyn/f;

    .line 60
    move-result-object v7

    .line 61
    const-class v8, Lmo0/t;

    .line 63
    invoke-static {v1, v8}, Lct0/c;->c(Landroid/content/Context;Ljava/lang/Class;)Ljava/lang/Object;

    .line 66
    move-result-object v9

    .line 67
    check-cast v9, Lmo0/t;

    .line 69
    invoke-interface {v9}, Lmo0/t;->c()Lz30/i;

    .line 72
    move-result-object v9

    .line 73
    invoke-interface {v9}, Lz30/i;->c()Lz30/c;

    .line 76
    move-result-object v9

    .line 77
    invoke-static {v1, v8}, Lct0/c;->c(Landroid/content/Context;Ljava/lang/Class;)Ljava/lang/Object;

    .line 80
    move-result-object v8

    .line 81
    check-cast v8, Lmo0/t;

    .line 83
    invoke-interface {v8}, Lmo0/t;->c()Lz30/i;

    .line 86
    move-result-object v8

    .line 87
    invoke-interface {v8, v1}, Lz30/i;->a(Landroid/content/Context;)Le40/d;

    .line 90
    move-result-object v8

    .line 91
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 94
    move-result-object v10

    .line 95
    check-cast v10, Lid0/g;

    .line 97
    invoke-virtual {v10}, Lid0/g;->h()Lcom/ellation/crunchyroll/api/etp/EtpNetworkModule;

    .line 100
    move-result-object v10

    .line 101
    invoke-interface {v10}, Lcom/ellation/crunchyroll/api/etp/EtpNetworkModule;->getUserTokenInteractor()Lrb0/d;

    .line 104
    move-result-object v13

    .line 105
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 108
    move-result-object v10

    .line 109
    check-cast v10, Lid0/g;

    .line 111
    invoke-virtual {v10}, Lid0/g;->d()Lob0/o0;

    .line 114
    move-result-object v14

    .line 115
    iget-object v15, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->p:Lxi/a;

    .line 117
    if-eqz v15, :cond_193

    .line 119
    sget v10, Landroid/os/Build$VERSION;->SDK_INT:I

    .line 121
    const/16 v11, 0x21

    .line 123
    if-lt v10, v11, :cond_8f

    .line 125
    invoke-virtual {v1}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 128
    move-result-object v10

    .line 129
    invoke-virtual {v1}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 132
    move-result-object v11

    .line 133
    const-wide/16 v16, 0x80

    .line 135
    invoke-static/range {v16 .. v17}, Landroid/content/pm/PackageManager$ApplicationInfoFlags;->of(J)Landroid/content/pm/PackageManager$ApplicationInfoFlags;

    .line 138
    move-result-object v12

    .line 139
    invoke-virtual {v10, v11, v12}, Landroid/content/pm/PackageManager;->getApplicationInfo(Ljava/lang/String;Landroid/content/pm/PackageManager$ApplicationInfoFlags;)Landroid/content/pm/ApplicationInfo;

    .line 142
    move-result-object v10

    .line 143
    goto :goto_9d

    .line 144
    :cond_8f
    invoke-virtual {v1}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 147
    move-result-object v10

    .line 148
    invoke-virtual {v1}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 151
    move-result-object v11

    .line 152
    const/16 v12, 0x80

    .line 154
    invoke-virtual {v10, v11, v12}, Landroid/content/pm/PackageManager;->getApplicationInfo(Ljava/lang/String;I)Landroid/content/pm/ApplicationInfo;

    .line 157
    move-result-object v10

    .line 158
    :goto_9d
    iget-object v10, v10, Landroid/content/pm/ApplicationInfo;->metaData:Landroid/os/Bundle;

    .line 160
    invoke-virtual {v10}, Landroid/os/BaseBundle;->keySet()Ljava/util/Set;

    .line 163
    move-result-object v10

    .line 164
    const-string v11, "keySet(...)"

    .line 166
    invoke-static {v10, v11}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 169
    new-instance v11, Lmo0/e;

    .line 171
    invoke-direct {v11, v10}, Lmo0/e;-><init>(Ljava/util/Set;)V

    .line 174
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 177
    move-result-object v10

    .line 178
    check-cast v10, Lid0/g;

    .line 180
    invoke-virtual {v10}, Lid0/g;->b()Lte0/a;

    .line 183
    move-result-object v10

    .line 184
    invoke-interface {v10}, Lte0/a;->getProfilesFeature()Lxz/e;

    .line 187
    move-result-object v10

    .line 188
    invoke-interface {v10, v1}, Lxz/e;->e(Le/k;)Lz00/i;

    .line 191
    move-result-object v16

    .line 192
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 195
    move-result-object v10

    .line 196
    check-cast v10, Lid0/g;

    .line 198
    invoke-virtual {v10}, Lid0/g;->a()Le50/f;

    .line 201
    move-result-object v17

    .line 202
    iget-object v10, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->q:Lyl/c;

    .line 204
    if-eqz v10, :cond_18b

    .line 206
    iget-object v12, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->r:Lfm/a;

    .line 208
    if-eqz v12, :cond_183

    .line 210
    const/16 v18, 0x0

    .line 212
    iget-object v0, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->u:Loo0/g;

    .line 214
    if-eqz v0, :cond_17b

    .line 216
    move-object/from16 v21, v0

    .line 218
    iget-object v0, v1, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->w:Lbg/d;

    .line 220
    move-object/from16 v19, v18

    .line 222
    if-eqz v0, :cond_175

    .line 224
    move-object/from16 v18, v10

    .line 226
    move-object v10, v11

    .line 227
    sget-object v11, Lib0/t$a;->a:Lib0/v;

    .line 229
    move-object/from16 v22, v0

    .line 231
    invoke-static {}, Lob0/i$b;->a()Lob0/i;

    .line 234
    move-result-object v0

    .line 235
    sget-object v1, Lob0/b;->a:Lob0/d;

    .line 237
    const-string v20, "instance"

    .line 239
    if-eqz v1, :cond_171

    .line 241
    iget-object v1, v1, Lob0/d;->a:Leb0/a;

    .line 243
    move-object/from16 v23, v3

    .line 245
    const-string v3, "terms_of_service"

    .line 247
    move-object/from16 v24, v4

    .line 249
    const-class v4, Lcom/ellation/crunchyroll/features/configs/g2;

    .line 251
    invoke-virtual {v1, v4, v3}, Leb0/a;->b(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Object;

    .line 254
    move-result-object v1

    .line 255
    if-eqz v1, :cond_169

    .line 257
    check-cast v1, Lcom/ellation/crunchyroll/features/configs/g2;

    .line 259
    invoke-static {v0, v1}, Lps/a$a;->a(Lob0/i;Lcom/ellation/crunchyroll/features/configs/g2;)Lps/b;

    .line 262
    move-result-object v0

    .line 263
    sget-object v1, Lob0/b;->a:Lob0/d;

    .line 265
    if-eqz v1, :cond_165

    .line 267
    iget-object v1, v1, Lob0/d;->a:Leb0/a;

    .line 269
    const-string v3, "price_change_consent"

    .line 271
    const-class v4, Lcom/ellation/crunchyroll/features/configs/m1;

    .line 273
    invoke-virtual {v1, v4, v3}, Leb0/a;->b(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Object;

    .line 276
    move-result-object v1

    .line 277
    if-eqz v1, :cond_15d

    .line 279
    move-object/from16 v19, v1

    .line 281
    check-cast v19, Lcom/ellation/crunchyroll/features/configs/m1;

    .line 283
    sget-object v1, Lxw0/x0;->a:Lex0/c;

    .line 285
    sget-object v1, Lex0/b;->b:Lex0/b;

    .line 287
    new-instance v3, Lec/q0;

    .line 289
    const/4 v4, 0x1

    .line 290
    invoke-direct {v3, v4}, Lec/q0;-><init>(I)V

    .line 293
    const-string v4, "deeplinkProvider"

    .line 295
    invoke-static {v2, v4}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 298
    const-string v4, "analytics"

    .line 300
    invoke-static {v6, v4}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 303
    const-string v4, "deepLinkAnalytics"

    .line 305
    invoke-static {v7, v4}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 308
    const-string v4, "ssoEvents"

    .line 310
    invoke-static {v9, v4}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 313
    const-string v4, "userTokenInteractor"

    .line 315
    invoke-static {v13, v4}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 318
    const-string v4, "userSessionAnalytics"

    .line 320
    invoke-static {v11, v4}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 323
    const-string v4, "ioDispatcher"

    .line 325
    invoke-static {v1, v4}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 328
    move-object/from16 v20, v12

    .line 330
    move-object v12, v0

    .line 331
    new-instance v0, Lmo0/w;

    .line 333
    move-object v4, v9

    .line 334
    move-object v9, v8

    .line 335
    move-object v8, v4

    .line 336
    move-object/from16 v4, v24

    .line 338
    move-object/from16 v24, v3

    .line 340
    move-object/from16 v3, v23

    .line 342
    move-object/from16 v23, v1

    .line 344
    move-object/from16 v1, p0

    .line 346
    invoke-direct/range {v0 .. v24}, Lmo0/w;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;Lyn/y;Lpb0/a;Ljq0/l;Lup0/i;Lmo0/s;Lyn/f;Lz30/h;Le40/c;Lmo0/e;Lib0/t;Lps/a;Lrb0/d;Lob0/o0;Lxi/a;Lz00/g;Le50/f;Lyl/c;Lcom/ellation/crunchyroll/features/configs/m1;Lfm/a;Loo0/g;Lbg/d;Lxw0/e0;Lfw0/a;)V

    .line 349
    return-object v0

    .line 350
    :cond_15d
    new-instance v0, Ljava/lang/NullPointerException;

    .line 352
    const-string v1, "null cannot be cast to non-null type com.ellation.crunchyroll.features.configs.PriceChangeConsentConfigImpl"

    .line 354
    invoke-direct {v0, v1}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    .line 357
    throw v0

    .line 358
    :cond_165
    invoke-static/range {v20 .. v20}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 361
    throw v19

    .line 362
    :cond_169
    new-instance v0, Ljava/lang/NullPointerException;

    .line 364
    const-string v1, "null cannot be cast to non-null type com.ellation.crunchyroll.features.configs.TermsOfServiceConfigImpl"

    .line 366
    invoke-direct {v0, v1}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    .line 369
    throw v0

    .line 370
    :cond_171
    invoke-static/range {v20 .. v20}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 373
    throw v19

    .line 374
    :cond_175
    const-string v0, "ageAssuranceOutcomeProvider"

    .line 376
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 379
    throw v19

    .line 380
    :cond_17b
    move-object/from16 v19, v18

    .line 382
    const-string v0, "getConsentUiModelUseCase"

    .line 384
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 387
    throw v19

    .line 388
    :cond_183
    const/16 v19, 0x0

    .line 390
    const-string v0, "consentStateHolder"

    .line 392
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 395
    throw v19

    .line 396
    :cond_18b
    const/16 v19, 0x0

    .line 398
    const-string v0, "consentUseCase"

    .line 400
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 403
    throw v19

    .line 404
    :cond_193
    const/16 v19, 0x0

    .line 406
    const-string v0, "accountStateProvider"

    .line 408
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 411
    throw v19

    .line 412
    :cond_19b
    const/16 v19, 0x0

    .line 414
    const-string v0, "translationsSynchronizer"

    .line 416
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 419
    throw v19

    .line 420
    :cond_1a3
    const/16 v19, 0x0

    .line 422
    const-string v0, "appInitializer"

    .line 424
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 427
    throw v19
.end method


# virtual methods
.method public final B8(Z)V
    .registers 3

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 3
    if-eqz v0, :cond_b

    .line 5
    invoke-virtual {v0, p1}, Landroid/view/View;->setEnabled(Z)V

    .line 8
    invoke-virtual {v0, p1}, Landroid/view/View;->setClickable(Z)V

    .line 11
    return-void

    .line 12
    :cond_b
    const-string p1, "container"

    .line 14
    invoke-static {p1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 17
    const/4 p1, 0x0

    .line 18
    throw p1
.end method

.method public final E6(Lfm/d;)V
    .registers 3

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->s:Ljz/a;

    .line 3
    if-eqz v0, :cond_8

    .line 5
    invoke-interface {v0, p1}, Ljz/a;->e(Lfm/d;)V

    .line 8
    return-void

    .line 9
    :cond_8
    const-string p1, "priceConsentFlowMonitor"

    .line 11
    invoke-static {p1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 14
    const/4 p1, 0x0

    .line 15
    throw p1
.end method

.method public final F()V
    .registers 3

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->v:Lcom/ellation/crunchyroll/features/configs/z1;

    .line 3
    if-eqz v0, :cond_23

    .line 5
    invoke-virtual {v0}, Lcom/ellation/crunchyroll/features/configs/z1;->isEnabled()Z

    .line 8
    move-result v0

    .line 9
    if-eqz v0, :cond_1a

    .line 11
    new-instance v0, Landroid/content/Intent;

    .line 13
    const-class v1, Lcom/ellation/crunchyroll/presentation/mainv2/MobileMainActivity;

    .line 15
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 18
    const/high16 v1, 0x24000000

    .line 20
    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 23
    invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V

    .line 26
    goto :goto_1f

    .line 27
    :cond_1a
    sget v0, Lcom/ellation/crunchyroll/presentation/main/home/HomeBottomBarActivity;->X:I

    .line 29
    invoke-static {p0}, Lcom/ellation/crunchyroll/presentation/main/home/HomeBottomBarActivity$a;->a(Landroid/content/Context;)V

    .line 32
    :goto_1f
    invoke-virtual {p0}, Landroid/app/Activity;->finish()V

    .line 35
    return-void

    .line 36
    :cond_23
    const-string v0, "singleActivityNavigationConfig"

    .line 38
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 41
    const/4 v0, 0x0

    .line 42
    throw v0
.end method

.method public final M1(Luu/a;)V
    .registers 4

    .line 1
    const-string v0, "mode"

    .line 3
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 9
    move-result-object v0

    .line 10
    check-cast v0, Lid0/g;

    .line 12
    invoke-virtual {v0}, Lid0/g;->b()Lte0/a;

    .line 15
    move-result-object v0

    .line 16
    invoke-interface {v0}, Lte0/a;->r()Luu/c;

    .line 19
    move-result-object v0

    .line 20
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 23
    new-instance v0, Landroid/content/Intent;

    .line 25
    const-class v1, Lcom/crunchyroll/onboarding/presentation/OnboardingV2Activity;

    .line 27
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 30
    const-string v1, "onboarding_start_mode"

    .line 32
    invoke-virtual {p1}, Ljava/lang/Enum;->name()Ljava/lang/String;

    .line 35
    move-result-object p1

    .line 36
    invoke-virtual {v0, v1, p1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 39
    invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V

    .line 42
    return-void
.end method

.method public final Mf()Ljava/lang/Integer;
    .registers 2

    .line 1
    iget v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->F:I

    .line 3
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    .line 6
    move-result-object v0

    .line 7
    return-object v0
.end method

.method public final Sf()Lmo0/u;
    .registers 2

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->E:Lqv0/u;

    .line 3
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 6
    move-result-object v0

    .line 7
    check-cast v0, Lmo0/u;

    .line 9
    return-object v0
.end method

.method public final Tf(Ljava/lang/String;)V
    .registers 5

    .line 1
    const-string v0, "uri"

    .line 3
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    new-instance v0, Landroid/content/Intent;

    .line 8
    const-string v1, "android.intent.action.VIEW"

    .line 10
    invoke-static {p1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    .line 13
    move-result-object v2

    .line 14
    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 17
    :try_start_10
    invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V
    :try_end_13
    .catch Landroid/content/ActivityNotFoundException; {:try_start_10 .. :try_end_13} :catch_14

    .line 20
    return-void

    .line 21
    :catch_14
    move-exception v0

    .line 22
    sget-object v1, Lgy0/a;->a:Lgy0/a$a;

    .line 24
    const-string v2, "StartupActivity"

    .line 26
    invoke-virtual {v1, v2}, Lgy0/a$a;->r(Ljava/lang/String;)V

    .line 29
    const-string v2, "Failed to open URI: "

    .line 31
    invoke-virtual {v2, p1}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    .line 34
    move-result-object p1

    .line 35
    const/4 v2, 0x0

    .line 36
    new-array v2, v2, [Ljava/lang/Object;

    .line 38
    invoke-virtual {v1, v0, p1, v2}, Lgy0/a$a;->f(Ljava/lang/Throwable;Ljava/lang/String;[Ljava/lang/Object;)V

    .line 41
    return-void
.end method

.method public final cc()V
    .registers 11

    .line 1
    new-instance v0, Lpo0/c;

    .line 3
    iget-object v1, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->o:Lps/f;

    .line 5
    if-eqz v1, :cond_ac

    .line 7
    invoke-direct {v0, p0, p0, v1}, Lpo0/c;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;Lps/f;)V

    .line 10
    new-instance v2, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$f;

    .line 12
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->Sf()Lmo0/u;

    .line 15
    move-result-object v4

    .line 16
    const-string v7, "onUserAcceptedUpdatedTerms()V"

    .line 18
    const/4 v8, 0x0

    .line 19
    const/4 v3, 0x0

    .line 20
    const-class v5, Lmo0/u;

    .line 22
    const-string v6, "onUserAcceptedUpdatedTerms"

    .line 24
    invoke-direct/range {v2 .. v8}, Lkotlin/jvm/internal/k;-><init>(ILjava/lang/Object;Ljava/lang/Class;Ljava/lang/String;Ljava/lang/String;I)V

    .line 27
    new-instance v3, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$g;

    .line 29
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->Sf()Lmo0/u;

    .line 32
    move-result-object v5

    .line 33
    const-string v8, "onTermsUpdatedDialogCancelledByUser()V"

    .line 35
    const/4 v9, 0x0

    .line 36
    const/4 v4, 0x0

    .line 37
    const-class v6, Lmo0/u;

    .line 39
    const-string v7, "onTermsUpdatedDialogCancelledByUser"

    .line 41
    invoke-direct/range {v3 .. v9}, Lkotlin/jvm/internal/k;-><init>(ILjava/lang/Object;Ljava/lang/Class;Ljava/lang/String;Ljava/lang/String;I)V

    .line 44
    const v1, 0x7f14088e

    .line 47
    invoke-virtual {p0, v1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 50
    move-result-object v4

    .line 51
    const v5, 0x7f14088d

    .line 54
    invoke-virtual {p0, v5}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 57
    move-result-object v6

    .line 58
    filled-new-array {v4, v6}, [Ljava/lang/Object;

    .line 61
    move-result-object v4

    .line 62
    const v6, 0x7f14088f

    .line 65
    invoke-virtual {p0, v6, v4}, Landroid/content/Context;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    .line 68
    move-result-object v4

    .line 69
    const-string v6, "getString(...)"

    .line 71
    invoke-static {v4, v6}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 74
    new-instance v7, Lse0/r;

    .line 76
    invoke-virtual {p0, v1}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 79
    move-result-object v1

    .line 80
    invoke-static {v1, v6}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 83
    new-instance v8, Loi/a;

    .line 85
    const/4 v9, 0x1

    .line 86
    invoke-direct {v8, v0, v9}, Loi/a;-><init>(Ljava/lang/Object;I)V

    .line 89
    invoke-direct {v7, v1, v8}, Lse0/r;-><init>(Ljava/lang/String;Lfw0/p;)V

    .line 92
    new-instance v1, Lse0/r;

    .line 94
    invoke-virtual {p0, v5}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    .line 97
    move-result-object v5

    .line 98
    invoke-static {v5, v6}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 101
    new-instance v6, Lor/p7;

    .line 103
    invoke-direct {v6, v0}, Lor/p7;-><init>(Lpo0/c;)V

    .line 106
    invoke-direct {v1, v5, v6}, Lse0/r;-><init>(Ljava/lang/String;Lfw0/p;)V

    .line 109
    filled-new-array {v7, v1}, [Lse0/r;

    .line 112
    move-result-object v0

    .line 113
    invoke-static {v4, v0}, Lse0/p0;->f(Ljava/lang/String;[Lse0/r;)Landroid/text/SpannableString;

    .line 116
    move-result-object v0

    .line 117
    new-instance v1, Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;

    .line 119
    invoke-direct {v1, p0}, Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;-><init>(Landroid/content/Context;)V

    .line 122
    const v4, 0x7f140890

    .line 125
    invoke-virtual {v1, v4}, Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;->setTitle(I)Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;

    .line 128
    move-result-object v1

    .line 129
    invoke-virtual {v1, v0}, Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;->setMessage(Ljava/lang/CharSequence;)Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;

    .line 132
    move-result-object v1

    .line 133
    new-instance v4, Lpo0/a;

    .line 135
    invoke-direct {v4, v2}, Lpo0/a;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$f;)V

    .line 138
    const v2, 0x7f140056

    .line 141
    invoke-virtual {v1, v2, v4}, Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;->setPositiveButton(ILandroid/content/DialogInterface$OnClickListener;)Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;

    .line 144
    move-result-object v1

    .line 145
    new-instance v2, Lpo0/b;

    .line 147
    invoke-direct {v2, v3}, Lpo0/b;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$g;)V

    .line 150
    invoke-virtual {v1, v2}, Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;->setOnCancelListener(Landroid/content/DialogInterface$OnCancelListener;)Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;

    .line 153
    move-result-object v1

    .line 154
    invoke-virtual {v1}, Landroidx/appcompat/app/g$a;->show()Landroidx/appcompat/app/g;

    .line 157
    move-result-object v1

    .line 158
    const v2, 0x102000b

    .line 161
    invoke-virtual {v1, v2}, Landroidx/appcompat/app/v;->findViewById(I)Landroid/view/View;

    .line 164
    move-result-object v1

    .line 165
    check-cast v1, Landroid/widget/TextView;

    .line 167
    if-eqz v1, :cond_ab

    .line 169
    invoke-static {v1, v0}, Lse0/s0;->b(Landroid/widget/TextView;Landroid/text/SpannableString;)V

    .line 172
    :cond_ab
    return-void

    .line 173
    :cond_ac
    const-string v0, "appLegalInfoRouter"

    .line 175
    invoke-static {v0}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 178
    const/4 v0, 0x0

    .line 179
    throw v0
.end method

.method public final k4(Lmo0/v;)V
    .registers 9

    .line 1
    sget-object v0, Lcom/ellation/crunchyroll/ui/animation/AnimationUtil;->INSTANCE:Lcom/ellation/crunchyroll/ui/animation/AnimationUtil;

    .line 3
    iget-object v1, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 5
    if-eqz v1, :cond_19

    .line 7
    new-instance v4, Landroid/view/animation/PathInterpolator;

    .line 9
    const/high16 v2, 0x3f000000  # 0.5f

    .line 11
    const/4 v3, 0x0

    .line 12
    const/high16 v5, 0x3e800000  # 0.25f

    .line 14
    const/high16 v6, 0x3f800000  # 1.0f

    .line 16
    invoke-direct {v4, v2, v3, v5, v6}, Landroid/view/animation/PathInterpolator;-><init>(FFFF)V

    .line 19
    const-wide/16 v2, 0xc8

    .line 21
    move-object v5, p1

    .line 22
    invoke-virtual/range {v0 .. v5}, Lcom/ellation/crunchyroll/ui/animation/AnimationUtil;->fadeOut(Landroid/view/View;JLandroid/animation/TimeInterpolator;Lfw0/a;)V

    .line 25
    return-void

    .line 26
    :cond_19
    const-string p1, "container"

    .line 28
    invoke-static {p1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 31
    const/4 p1, 0x0

    .line 32
    throw p1
.end method

.method public final kf()V
    .registers 7

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 3
    const-string v1, "container"

    .line 5
    const/4 v2, 0x0

    .line 6
    if-eqz v0, :cond_8e

    .line 8
    invoke-virtual {v0}, Landroid/view/View;->getRootView()Landroid/view/View;

    .line 11
    move-result-object v0

    .line 12
    const-string v3, "getRootView(...)"

    .line 14
    invoke-static {v0, v3}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 17
    new-instance v3, Lmo0/i;

    .line 19
    const/4 v4, 0x0

    .line 20
    invoke-direct {v3, v4}, Lmo0/i;-><init>(I)V

    .line 23
    invoke-static {v0, v3}, Lbx/m0;->b(Landroid/view/View;Lfw0/l;)V

    .line 26
    invoke-virtual {p0}, Landroid/app/Activity;->getLayoutInflater()Landroid/view/LayoutInflater;

    .line 29
    move-result-object v0

    .line 30
    const v3, 0x7f0e0326

    .line 33
    invoke-virtual {v0, v3, v2}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;)Landroid/view/View;

    .line 36
    move-result-object v0

    .line 37
    new-instance v3, Landroid/view/ViewGroup$LayoutParams;

    .line 39
    const/4 v4, -0x1

    .line 40
    invoke-direct {v3, v4, v4}, Landroid/view/ViewGroup$LayoutParams;-><init>(II)V

    .line 43
    invoke-virtual {v0, v3}, Landroid/view/View;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    .line 46
    iget-object v3, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 48
    if-eqz v3, :cond_8a

    .line 50
    invoke-virtual {v3}, Landroid/view/ViewGroup;->removeAllViews()V

    .line 53
    invoke-virtual {v3}, Landroid/view/View;->getContext()Landroid/content/Context;

    .line 56
    move-result-object v4

    .line 57
    const v5, 0x7f06002b

    .line 60
    invoke-static {v4, v5}, Lx3/a;->getColor(Landroid/content/Context;I)I

    .line 63
    move-result v4

    .line 64
    invoke-virtual {v3, v4}, Landroid/view/View;->setBackgroundColor(I)V

    .line 67
    invoke-virtual {v3, v0}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V

    .line 70
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 72
    if-eqz v0, :cond_86

    .line 74
    const v3, 0x7f0b0724

    .line 77
    invoke-virtual {v0, v3}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    .line 80
    move-result-object v0

    .line 81
    iput-object v0, p0, Ldq0/c;->d:Landroid/view/View;

    .line 83
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 85
    if-eqz v0, :cond_82

    .line 87
    const v3, 0x7f0b075b

    .line 90
    invoke-virtual {v0, v3}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    .line 93
    move-result-object v0

    .line 94
    new-instance v3, Lmo0/j;

    .line 96
    invoke-direct {v3, p0}, Lmo0/j;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)V

    .line 99
    invoke-virtual {v0, v3}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 102
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 104
    if-eqz v0, :cond_7e

    .line 106
    const v1, 0x7f0b0150

    .line 109
    invoke-virtual {v0, v1}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    .line 112
    move-result-object v0

    .line 113
    const-string v1, "findViewById(...)"

    .line 115
    invoke-static {v0, v1}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 118
    new-instance v1, Lmo0/k;

    .line 120
    invoke-direct {v1, p0}, Lmo0/k;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)V

    .line 123
    invoke-virtual {v0, v1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 126
    return-void

    .line 127
    :cond_7e
    invoke-static {v1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 130
    throw v2

    .line 131
    :cond_82
    invoke-static {v1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 134
    throw v2

    .line 135
    :cond_86
    invoke-static {v1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 138
    throw v2

    .line 139
    :cond_8a
    invoke-static {v1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 142
    throw v2

    .line 143
    :cond_8e
    invoke-static {v1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 146
    throw v2
.end method

.method public final m4()V
    .registers 2

    .line 1
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->Sf()Lmo0/u;

    .line 4
    move-result-object v0

    .line 5
    invoke-static {v0, p0}, Lih0/f;->a(Lch0/m;Landroidx/lifecycle/e0;)V

    .line 8
    return-void
.end method

.method public final onCreate(Landroid/os/Bundle;)V
    .registers 12
    # Log D inyectado - 2026-09-11T20:56:51.604192

    # ========== LOG D ==========
    const-string v0, "MainActivity"
    const-string v1, "onCreate iniciado"
    invoke-static {v0, v1}, Lcom/deadnote/RemoteLogger;->d(Ljava/lang/String;Ljava/lang/String;)V
    # ============================

    .line 1
    const v0, 0x7f1504db

    .line 4
    invoke-virtual {p0, v0}, Landroidx/appcompat/app/h;->setTheme(I)V

    .line 7
    invoke-super {p0, p1}, Lmo0/g;->onCreate(Landroid/os/Bundle;)V

    .line 10
    const/4 p1, 0x0

    .line 11
    invoke-static {p0, p1}, Lse0/b;->e(Landroidx/appcompat/app/h;Z)V

    .line 14
    new-instance v0, Landroid/content/Intent;

    .line 16
    sget-object v1, Llv/b;->FINISH_PIP_ACTIVITY:Llv/b;

    .line 18
    invoke-virtual {v1}, Llv/b;->getValue()Ljava/lang/String;

    .line 21
    move-result-object v1

    .line 22
    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 25
    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    .line 28
    move-result-object v1

    .line 29
    invoke-virtual {v0, v1}, Landroid/content/Intent;->setPackage(Ljava/lang/String;)Landroid/content/Intent;

    .line 32
    invoke-virtual {p0, v0}, Landroid/content/Context;->sendBroadcast(Landroid/content/Intent;)V

    .line 35
    const v0, 0x7f0b084d

    .line 38
    invoke-virtual {p0, v0}, Landroidx/appcompat/app/h;->findViewById(I)Landroid/view/View;

    .line 41
    move-result-object v0

    .line 42
    const-string v1, "findViewById(...)"

    .line 44
    invoke-static {v0, v1}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 47
    check-cast v0, Landroid/view/ViewGroup;

    .line 49
    iput-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 51
    invoke-virtual {p0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;

    .line 54
    move-result-object v0

    .line 55
    invoke-virtual {v0}, Landroid/content/Intent;->getExtras()Landroid/os/Bundle;

    .line 58
    move-result-object v0

    .line 59
    if-eqz v0, :cond_45

    .line 61
    sget-object v0, Lhb0/c;->a:Lhb0/b;

    .line 63
    :cond_45
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->z:Landroid/view/ViewGroup;

    .line 65
    const/4 v1, 0x0

    .line 66
    if-eqz v0, :cond_f8

    .line 68
    new-instance v2, Lmo0/h;

    .line 70
    invoke-direct {v2, p0, p1}, Lmo0/h;-><init>(Ljava/lang/Object;I)V

    .line 73
    invoke-virtual {v0, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 76
    invoke-virtual {p0}, Le/k;->getLifecycle()Landroidx/lifecycle/w;

    .line 79
    move-result-object p1

    .line 80
    invoke-static {p0, p1}, Lpl/l$a;->a(Landroid/content/Context;Landroidx/lifecycle/w;)Lpl/p;

    .line 83
    move-result-object p1

    .line 84
    invoke-virtual {p0}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->Sf()Lmo0/u;

    .line 87
    move-result-object v0

    .line 88
    invoke-virtual {p1, v0}, Lpl/p;->b(Lpl/a;)V

    .line 91
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 94
    move-result-object p1

    .line 95
    check-cast p1, Lid0/g;

    .line 97
    invoke-virtual {p1}, Lid0/g;->b()Lte0/a;

    .line 100
    move-result-object p1

    .line 101
    invoke-interface {p1}, Lte0/a;->p()Ln30/a;

    .line 104
    move-result-object p1

    .line 105
    invoke-virtual {p0}, Landroid/app/Activity;->getIntent()Landroid/content/Intent;

    .line 108
    move-result-object v0

    .line 109
    const-string v2, "getIntent(...)"

    .line 111
    invoke-static {v0, v2}, Lkotlin/jvm/internal/l;->e(Ljava/lang/Object;Ljava/lang/String;)V

    .line 114
    invoke-interface {p1, v0}, Ln30/a;->b(Landroid/content/Intent;)V

    .line 117
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 120
    move-result-object p1

    .line 121
    check-cast p1, Lid0/g;

    .line 123
    invoke-virtual {p1}, Lid0/g;->b()Lte0/a;

    .line 126
    move-result-object p1

    .line 127
    invoke-interface {p1}, Lte0/a;->p()Ln30/a;

    .line 130
    move-result-object p1

    .line 131
    invoke-interface {p1}, Ln30/a;->a()V

    .line 134
    invoke-static {}, Lob0/h;->b()Lid0/a;

    .line 137
    move-result-object p1

    .line 138
    check-cast p1, Lid0/g;

    .line 140
    invoke-virtual {p1}, Lid0/g;->b()Lte0/a;

    .line 143
    move-result-object p1

    .line 144
    invoke-interface {p1}, Lte0/a;->f()Ldi/c;

    .line 147
    move-result-object p1

    .line 148
    invoke-interface {p1}, Ldi/c;->a()Ldi/e;

    .line 151
    move-result-object p1

    .line 152
    iget-object p1, p1, Ldi/e;->b:Lei/e;

    .line 154
    invoke-interface {p1}, Lei/e;->a()V

    .line 157
    const p1, 0x7f0b009b

    .line 160
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/h;->findViewById(I)Landroid/view/View;

    .line 163
    move-result-object p1

    .line 164
    check-cast p1, Landroidx/compose/ui/platform/ComposeView;

    .line 166
    const/4 v0, 0x1

    .line 167
    if-eqz p1, :cond_bf

    .line 169
    new-instance v2, Lmo0/o;

    .line 171
    invoke-direct {v2, p0}, Lmo0/o;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)V

    .line 174
    new-instance v3, Lh1/a;

    .line 176
    const v4, 0x2d7ce254

    .line 179
    invoke-direct {v3, v4, v2, v0}, Lh1/a;-><init>(ILjava/lang/Object;Z)V

    .line 182
    invoke-virtual {p1, v3}, Landroidx/compose/ui/platform/ComposeView;->setContent(Lfw0/p;)V

    .line 185
    :cond_bf
    const p1, 0x1020002

    .line 188
    invoke-virtual {p0, p1}, Landroidx/appcompat/app/h;->findViewById(I)Landroid/view/View;

    .line 191
    move-result-object p1

    .line 192
    check-cast p1, Landroid/view/ViewGroup;

    .line 194
    new-instance v2, Landroidx/compose/ui/platform/ComposeView;

    .line 196
    const/4 v3, 0x6

    .line 197
    invoke-direct {v2, p0, v1, v3}, Landroidx/compose/ui/platform/ComposeView;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V

    .line 200
    new-instance v3, Landroid/view/ViewGroup$LayoutParams;

    .line 202
    const/4 v4, -0x1

    .line 203
    invoke-direct {v3, v4, v4}, Landroid/view/ViewGroup$LayoutParams;-><init>(II)V

    .line 206
    invoke-virtual {v2, v3}, Landroid/view/View;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    .line 209
    new-instance v3, Landroidx/xr/compose/platform/a;

    .line 211
    invoke-direct {v3, p0, v0}, Landroidx/xr/compose/platform/a;-><init>(Ljava/lang/Object;I)V

    .line 214
    new-instance v4, Lh1/a;

    .line 216
    const v5, 0x6a5e996f

    .line 219
    invoke-direct {v4, v5, v3, v0}, Lh1/a;-><init>(ILjava/lang/Object;Z)V

    .line 222
    invoke-virtual {v2, v4}, Landroidx/compose/ui/platform/ComposeView;->setContent(Lfw0/p;)V

    .line 225
    invoke-virtual {p1, v2}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V

    .line 228
    invoke-static {p0}, Landroidx/lifecycle/f0;->e(Landroidx/lifecycle/e0;)Landroidx/lifecycle/z;

    .line 231
    move-result-object p1

    .line 232
    new-instance v0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$c;

    .line 234
    invoke-direct {v0, p0, v1}, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity$c;-><init>(Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;Luv0/e;)V

    .line 237
    const/4 v2, 0x3

    .line 238
    invoke-static {p1, v1, v1, v0, v2}, Lxw0/h;->c(Lxw0/g0;Luv0/g;Lxw0/i0;Lfw0/p;I)Lxw0/i2;

    .line 241
    return-void

    .line 242
    :cond_f8
    const-string p1, "container"

    .line 244
    invoke-static {p1}, Lkotlin/jvm/internal/l;->m(Ljava/lang/String;)V

    .line 247
    throw v1
.end method

.method public final p6()V
    .registers 3

    .line 1
    sget-object v0, Lcom/ellation/crunchyroll/presentation/downloads/activity/DownloadsActivity;->r:Lcom/ellation/crunchyroll/presentation/downloads/activity/DownloadsActivity$a;

    .line 3
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 6
    new-instance v0, Landroid/content/Intent;

    .line 8
    const-class v1, Lcom/ellation/crunchyroll/presentation/downloads/activity/DownloadsActivity;

    .line 10
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 13
    invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V

    .line 16
    return-void
.end method

.method public final setupPresenters()Ljava/util/Set;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/Set<",
            "Lmo0/a;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;->A:Lqv0/u;

    .line 3
    invoke-virtual {v0}, Lqv0/u;->getValue()Ljava/lang/Object;

    .line 6
    move-result-object v0

    .line 7
    check-cast v0, Lmo0/a;

    .line 9
    invoke-static {v0}, Lcx0/j;->h(Ljava/lang/Object;)Ljava/util/Set;

    .line 12
    move-result-object v0

    .line 13
    return-object v0
.end method

.method public final t9(Leg/e;)V
    .registers 6

    .line 1
    const-string v0, "outcome"

    .line 3
    invoke-static {p1, v0}, Lkotlin/jvm/internal/l;->f(Ljava/lang/Object;Ljava/lang/String;)V

    .line 6
    new-instance v0, Lmo0/m;

    .line 8
    invoke-direct {v0, p1, p0}, Lmo0/m;-><init>(Leg/e;Lcom/ellation/crunchyroll/presentation/startup/StartupActivity;)V

    .line 11
    new-instance p1, Lh1/a;

    .line 13
    const v1, 0x42aef216

    .line 16
    const/4 v2, 0x1

    .line 17
    invoke-direct {p1, v1, v0, v2}, Lh1/a;-><init>(ILjava/lang/Object;Z)V

    .line 20
    new-instance v0, Landroidx/compose/ui/platform/ComposeView;

    .line 22
    const/4 v1, 0x0

    .line 23
    const/4 v3, 0x6

    .line 24
    invoke-direct {v0, p0, v1, v3}, Landroidx/compose/ui/platform/ComposeView;-><init>(Landroid/content/Context;Landroid/util/AttributeSet;I)V

    .line 27
    new-instance v1, Landroid/view/ViewGroup$LayoutParams;

    .line 29
    const/4 v3, -0x1

    .line 30
    invoke-direct {v1, v3, v3}, Landroid/view/ViewGroup$LayoutParams;-><init>(II)V

    .line 33
    invoke-virtual {v0, v1}, Landroid/view/View;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    .line 36
    new-instance v1, Ley/w;

    .line 38
    const/4 v3, 0x1

    .line 39
    invoke-direct {v1, p1, v3}, Ley/w;-><init>(Ljava/lang/Object;I)V

    .line 42
    new-instance p1, Lh1/a;

    .line 44
    const v3, 0x6ad0648c

    .line 47
    invoke-direct {p1, v3, v1, v2}, Lh1/a;-><init>(ILjava/lang/Object;Z)V

    .line 50
    invoke-virtual {v0, p1}, Landroidx/compose/ui/platform/ComposeView;->setContent(Lfw0/p;)V

    .line 53
    invoke-virtual {p0, v0}, Ldq0/c;->setContentView(Landroid/view/View;)V

    .line 56
    return-void
.end method
