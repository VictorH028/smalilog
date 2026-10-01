.class public final Lokio/Options;
.super Ljava/util/AbstractList;
.source "Options.java"

# interfaces
.implements Ljava/util/RandomAccess;


# annotations
.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/util/AbstractList<",
        "Lokio/ByteString;",
        ">;",
        "Ljava/util/RandomAccess;"
    }
.end annotation


# instance fields
.field final byteStrings:[Lokio/ByteString;

.field final trie:[I


# direct methods
.method private constructor <init>([Lokio/ByteString;[I)V
    .locals 0
    .param p1, "byteStrings"    # [Lokio/ByteString;
    .param p2, "trie"    # [I

    .line 30
    invoke-direct {p0}, Ljava/util/AbstractList;-><init>()V

    .line 31
    iput-object p1, p0, Lokio/Options;->byteStrings:[Lokio/ByteString;

    .line 32
    iput-object p2, p0, Lokio/Options;->trie:[I

    .line 33
    return-void
.end method

.method private static buildTrieRecursive(JLokio/Buffer;ILjava/util/List;IILjava/util/List;)V
    .locals 23
    .param p0, "nodeOffset"    # J
    .param p2, "node"    # Lokio/Buffer;
    .param p3, "byteStringOffset"    # I
    .param p5, "fromIndex"    # I
    .param p6, "toIndex"    # I
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(J",
            "Lokio/Buffer;",
            "I",
            "Ljava/util/List<",
            "Lokio/ByteString;",
            ">;II",
            "Ljava/util/List<",
            "Ljava/lang/Integer;",
            ">;)V"
        }
    .end annotation

    .line 123
    .local p4, "byteStrings":Ljava/util/List;, "Ljava/util/List<Lokio/ByteString;>;"
    .local p7, "indexes":Ljava/util/List;, "Ljava/util/List<Ljava/lang/Integer;>;"
    move-object/from16 v0, p2

    move/from16 v1, p3

    move-object/from16 v6, p4

    move/from16 v2, p5

    move/from16 v10, p6

    move-object/from16 v9, p7

    if-ge v2, v10, :cond_11

    .line 124
    move/from16 v3, p5

    .local v3, "i":I
    :goto_0
    if-ge v3, v10, :cond_1

    .line 125
    invoke-interface {v6, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Lokio/ByteString;

    invoke-virtual {v4}, Lokio/ByteString;->size()I

    move-result v4

    if-lt v4, v1, :cond_0

    .line 124
    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    .line 125
    :cond_0
    new-instance v4, Ljava/lang/AssertionError;

    invoke-direct {v4}, Ljava/lang/AssertionError;-><init>()V

    throw v4

    .line 128
    .end local v3
    :cond_1
    invoke-interface/range {p4 .. p5}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Lokio/ByteString;

    .line 129
    .local v3, "from":Lokio/ByteString;
    add-int/lit8 v4, v10, -0x1

    invoke-interface {v6, v4}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v4

    move-object v11, v4

    check-cast v11, Lokio/ByteString;

    .line 130
    .local v11, "to":Lokio/ByteString;
    const/4 v4, -0x1

    .line 133
    .local v4, "prefixIndex":I
    invoke-virtual {v3}, Lokio/ByteString;->size()I

    move-result v5

    if-ne v1, v5, :cond_2

    .line 134
    invoke-interface {v9, v2}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Ljava/lang/Integer;

    invoke-virtual {v5}, Ljava/lang/Integer;->intValue()I

    move-result v4

    .line 135
    add-int/lit8 v2, v2, 0x1

    .line 136
    .end local p5
    .local v2, "fromIndex":I
    invoke-interface {v6, v2}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v5

    move-object v3, v5

    check-cast v3, Lokio/ByteString;

    move v12, v2

    move-object v13, v3

    move v14, v4

    goto :goto_1

    .line 133
    .end local v2
    .restart local p5
    :cond_2
    move v12, v2

    move-object v13, v3

    move v14, v4

    .line 139
    .end local v3
    .end local v4
    .end local p5
    .local v12, "fromIndex":I
    .local v13, "from":Lokio/ByteString;
    .local v14, "prefixIndex":I
    :goto_1
    invoke-virtual {v13, v1}, Lokio/ByteString;->getByte(I)B

    move-result v2

    invoke-virtual {v11, v1}, Lokio/ByteString;->getByte(I)B

    move-result v3

    const-wide/16 v4, 0x2

    if-eq v2, v3, :cond_c

    .line 141
    const/4 v2, 0x1

    .line 142
    .local v2, "selectChoiceCount":I
    add-int/lit8 v3, v12, 0x1

    .local v3, "i":I
    :goto_2
    if-ge v3, v10, :cond_4

    .line 143
    add-int/lit8 v7, v3, -0x1

    invoke-interface {v6, v7}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v7

    check-cast v7, Lokio/ByteString;

    invoke-virtual {v7, v1}, Lokio/ByteString;->getByte(I)B

    move-result v7

    .line 144
    invoke-interface {v6, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v8

    check-cast v8, Lokio/ByteString;

    invoke-virtual {v8, v1}, Lokio/ByteString;->getByte(I)B

    move-result v8

    if-eq v7, v8, :cond_3

    .line 145
    add-int/lit8 v2, v2, 0x1

    .line 142
    :cond_3
    add-int/lit8 v3, v3, 0x1

    goto :goto_2

    .line 150
    .end local v3
    :cond_4
    invoke-static {v0}, Lokio/Options;->intCount(Lokio/Buffer;)I

    move-result v3

    int-to-long v7, v3

    add-long v7, p0, v7

    add-long/2addr v7, v4

    mul-int/lit8 v3, v2, 0x2

    int-to-long v3, v3

    add-long/2addr v7, v3

    .line 152
    .local v7, "childNodesOffset":J
    invoke-virtual {v0, v2}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 153
    invoke-virtual {v0, v14}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 155
    move v3, v12

    .restart local v3
    :goto_3
    if-ge v3, v10, :cond_7

    .line 156
    invoke-interface {v6, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Lokio/ByteString;

    invoke-virtual {v4, v1}, Lokio/ByteString;->getByte(I)B

    move-result v4

    .line 157
    .local v4, "rangeByte":B
    if-eq v3, v12, :cond_5

    add-int/lit8 v5, v3, -0x1

    invoke-interface {v6, v5}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Lokio/ByteString;

    invoke-virtual {v5, v1}, Lokio/ByteString;->getByte(I)B

    move-result v5

    if-eq v4, v5, :cond_6

    .line 158
    :cond_5
    and-int/lit16 v5, v4, 0xff

    invoke-virtual {v0, v5}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 155
    .end local v4
    :cond_6
    add-int/lit8 v3, v3, 0x1

    goto :goto_3

    .line 162
    .end local v3
    :cond_7
    new-instance v4, Lokio/Buffer;

    invoke-direct {v4}, Lokio/Buffer;-><init>()V

    .line 163
    .local v4, "childNodes":Lokio/Buffer;
    move v3, v12

    .line 164
    .local v3, "rangeStart":I
    :goto_4
    if-ge v3, v10, :cond_b

    .line 165
    invoke-interface {v6, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Lokio/ByteString;

    invoke-virtual {v5, v1}, Lokio/ByteString;->getByte(I)B

    move-result v5

    .line 166
    .local v5, "rangeByte":B
    move/from16 v17, p6

    .line 167
    .local v17, "rangeEnd":I
    add-int/lit8 v18, v3, 0x1

    move/from16 v15, v18

    const-wide/16 v19, -0x1

    .local v15, "i":I
    :goto_5
    if-ge v15, v10, :cond_9

    .line 168
    invoke-interface {v6, v15}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v16

    move/from16 p5, v2

    .end local v2
    .local p5, "selectChoiceCount":I
    move-object/from16 v2, v16

    check-cast v2, Lokio/ByteString;

    invoke-virtual {v2, v1}, Lokio/ByteString;->getByte(I)B

    move-result v2

    if-eq v5, v2, :cond_8

    .line 169
    move/from16 v17, v15

    .line 170
    move/from16 v2, v17

    goto :goto_6

    .line 167
    :cond_8
    add-int/lit8 v15, v15, 0x1

    move/from16 v2, p5

    goto :goto_5

    .end local p5
    .restart local v2
    :cond_9
    move/from16 p5, v2

    .end local v2
    .restart local p5
    move/from16 v2, v17

    .line 174
    .end local v15
    .end local v17
    .local v2, "rangeEnd":I
    :goto_6
    add-int/lit8 v15, v3, 0x1

    if-ne v15, v2, :cond_a

    add-int/lit8 v15, v1, 0x1

    .line 175
    invoke-interface {v6, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v16

    check-cast v16, Lokio/ByteString;

    invoke-virtual/range {v16 .. v16}, Lokio/ByteString;->size()I

    move-result v1

    if-ne v15, v1, :cond_a

    .line 177
    invoke-interface {v9, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/lang/Integer;

    invoke-virtual {v1}, Ljava/lang/Integer;->intValue()I

    move-result v1

    invoke-virtual {v0, v1}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    move/from16 v1, p5

    move v15, v5

    move-wide/from16 v21, v7

    move v8, v2

    move v7, v3

    move-wide/from16 v2, v21

    goto :goto_7

    .line 180
    :cond_a
    invoke-static {v4}, Lokio/Options;->intCount(Lokio/Buffer;)I

    move-result v1

    move v15, v2

    .end local v2
    .local v15, "rangeEnd":I
    int-to-long v1, v1

    add-long/2addr v1, v7

    mul-long v1, v1, v19

    long-to-int v2, v1

    invoke-virtual {v0, v2}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 181
    move v1, v5

    .end local v5
    .local v1, "rangeByte":B
    add-int/lit8 v5, p3, 0x1

    move-wide/from16 v21, v7

    move v7, v3

    move-wide/from16 v2, v21

    move v8, v15

    move v15, v1

    move/from16 v1, p5

    .end local v3
    .end local p5
    .local v1, "selectChoiceCount":I
    .local v2, "childNodesOffset":J
    .local v7, "rangeStart":I
    .local v8, "rangeEnd":I
    .local v15, "rangeByte":B
    invoke-static/range {v2 .. v9}, Lokio/Options;->buildTrieRecursive(JLokio/Buffer;ILjava/util/List;IILjava/util/List;)V

    .line 191
    :goto_7
    nop

    .line 192
    .end local v7
    .end local v15
    .local v8, "rangeStart":I
    move-wide/from16 v21, v2

    move v3, v8

    move-wide/from16 v7, v21

    move v2, v1

    move/from16 v1, p3

    goto/16 :goto_4

    .line 194
    .end local v1
    .end local v8
    .local v2, "selectChoiceCount":I
    .restart local v3
    .local v7, "childNodesOffset":J
    :cond_b
    move v1, v2

    move-wide/from16 v21, v7

    move v7, v3

    move-wide/from16 v2, v21

    .end local v3
    .restart local v1
    .local v2, "childNodesOffset":J
    .local v7, "rangeStart":I
    move/from16 p5, v1

    move-wide v15, v2

    .end local v1
    .end local v2
    .local v15, "childNodesOffset":J
    .restart local p5
    invoke-virtual {v4}, Lokio/Buffer;->size()J

    move-result-wide v1

    invoke-virtual {v0, v4, v1, v2}, Lokio/Buffer;->write(Lokio/Buffer;J)V

    .line 196
    .end local v4
    .end local v7
    .end local v15
    .end local p5
    move v7, v12

    goto/16 :goto_a

    .line 198
    :cond_c
    const-wide/16 v19, -0x1

    const/4 v1, 0x0

    .line 199
    .local v1, "scanByteCount":I
    move/from16 v2, p3

    .local v2, "i":I
    invoke-virtual {v13}, Lokio/ByteString;->size()I

    move-result v3

    invoke-virtual {v11}, Lokio/ByteString;->size()I

    move-result v7

    invoke-static {v3, v7}, Ljava/lang/Math;->min(II)I

    move-result v3

    .local v3, "max":I
    :goto_8
    if-ge v2, v3, :cond_d

    .line 200
    invoke-virtual {v13, v2}, Lokio/ByteString;->getByte(I)B

    move-result v7

    invoke-virtual {v11, v2}, Lokio/ByteString;->getByte(I)B

    move-result v8

    if-ne v7, v8, :cond_d

    .line 201
    add-int/lit8 v1, v1, 0x1

    .line 199
    add-int/lit8 v2, v2, 0x1

    goto :goto_8

    .line 208
    .end local v2
    .end local v3
    :cond_d
    invoke-static {v0}, Lokio/Options;->intCount(Lokio/Buffer;)I

    move-result v2

    int-to-long v2, v2

    add-long v2, p0, v2

    add-long/2addr v2, v4

    int-to-long v4, v1

    add-long/2addr v2, v4

    const-wide/16 v4, 0x1

    add-long/2addr v2, v4

    .line 210
    .local v2, "childNodesOffset":J
    neg-int v4, v1

    invoke-virtual {v0, v4}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 211
    invoke-virtual {v0, v14}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 213
    move/from16 v4, p3

    .local v4, "i":I
    :goto_9
    add-int v5, p3, v1

    if-ge v4, v5, :cond_e

    .line 214
    invoke-virtual {v13, v4}, Lokio/ByteString;->getByte(I)B

    move-result v5

    and-int/lit16 v5, v5, 0xff

    invoke-virtual {v0, v5}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 213
    add-int/lit8 v4, v4, 0x1

    goto :goto_9

    .line 217
    .end local v4
    :cond_e
    add-int/lit8 v4, v12, 0x1

    if-ne v4, v10, :cond_10

    .line 219
    add-int v4, p3, v1

    invoke-interface {v6, v12}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Lokio/ByteString;

    invoke-virtual {v5}, Lokio/ByteString;->size()I

    move-result v5

    if-ne v4, v5, :cond_f

    .line 222
    invoke-interface {v9, v12}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Ljava/lang/Integer;

    invoke-virtual {v4}, Ljava/lang/Integer;->intValue()I

    move-result v4

    invoke-virtual {v0, v4}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    move v7, v12

    goto :goto_a

    .line 220
    :cond_f
    new-instance v4, Ljava/lang/AssertionError;

    invoke-direct {v4}, Ljava/lang/AssertionError;-><init>()V

    throw v4

    .line 225
    :cond_10
    new-instance v4, Lokio/Buffer;

    invoke-direct {v4}, Lokio/Buffer;-><init>()V

    .line 226
    .local v4, "childNodes":Lokio/Buffer;
    invoke-static {v4}, Lokio/Options;->intCount(Lokio/Buffer;)I

    move-result v5

    int-to-long v7, v5

    add-long/2addr v7, v2

    mul-long v7, v7, v19

    long-to-int v5, v7

    invoke-virtual {v0, v5}, Lokio/Buffer;->writeInt(I)Lokio/Buffer;

    .line 227
    add-int v5, p3, v1

    move v8, v10

    move v7, v12

    .end local v12
    .local v7, "fromIndex":I
    invoke-static/range {v2 .. v9}, Lokio/Options;->buildTrieRecursive(JLokio/Buffer;ILjava/util/List;IILjava/util/List;)V

    .line 235
    invoke-virtual {v4}, Lokio/Buffer;->size()J

    move-result-wide v5

    invoke-virtual {v0, v4, v5, v6}, Lokio/Buffer;->write(Lokio/Buffer;J)V

    .line 238
    .end local v1
    .end local v2
    .end local v4
    :goto_a
    return-void

    .line 123
    .end local v7
    .end local v11
    .end local v13
    .end local v14
    .local p5, "fromIndex":I
    :cond_11
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1}, Ljava/lang/AssertionError;-><init>()V

    goto :goto_c

    :goto_b
    throw v1

    :goto_c
    goto :goto_b
.end method

.method private static intCount(Lokio/Buffer;)I
    .locals 4
    .param p0, "trieBytes"    # Lokio/Buffer;

    .line 249
    invoke-virtual {p0}, Lokio/Buffer;->size()J

    move-result-wide v0

    const-wide/16 v2, 0x4

    div-long/2addr v0, v2

    long-to-int v1, v0

    return v1
.end method

.method public static varargs of([Lokio/ByteString;)Lokio/Options;
    .locals 12
    .param p0, "byteStrings"    # [Lokio/ByteString;

    .line 36
    array-length v0, p0

    const/4 v1, -0x1

    const/4 v2, 0x0

    if-nez v0, :cond_0

    .line 38
    new-instance v0, Lokio/Options;

    new-array v3, v2, [Lokio/ByteString;

    filled-new-array {v2, v1}, [I

    move-result-object v1

    invoke-direct {v0, v3, v1}, Lokio/Options;-><init>([Lokio/ByteString;[I)V

    return-object v0

    .line 43
    :cond_0
    new-instance v0, Ljava/util/ArrayList;

    invoke-static {p0}, Ljava/util/Arrays;->asList([Ljava/lang/Object;)Ljava/util/List;

    move-result-object v3

    invoke-direct {v0, v3}, Ljava/util/ArrayList;-><init>(Ljava/util/Collection;)V

    move-object v8, v0

    .line 44
    .local v8, "list":Ljava/util/List;, "Ljava/util/List<Lokio/ByteString;>;"
    invoke-static {v8}, Ljava/util/Collections;->sort(Ljava/util/List;)V

    .line 45
    new-instance v11, Ljava/util/ArrayList;

    invoke-direct {v11}, Ljava/util/ArrayList;-><init>()V

    .line 46
    .local v11, "indexes":Ljava/util/List;, "Ljava/util/List<Ljava/lang/Integer;>;"
    const/4 v0, 0x0

    .local v0, "i":I
    :goto_0
    invoke-interface {v8}, Ljava/util/List;->size()I

    move-result v3

    if-ge v0, v3, :cond_1

    .line 47
    invoke-static {v1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    invoke-interface {v11, v3}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 46
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    .line 49
    .end local v0
    :cond_1
    const/4 v0, 0x0

    .restart local v0
    :goto_1
    invoke-interface {v8}, Ljava/util/List;->size()I

    move-result v1

    if-ge v0, v1, :cond_2

    .line 50
    aget-object v1, p0, v0

    invoke-static {v8, v1}, Ljava/util/Collections;->binarySearch(Ljava/util/List;Ljava/lang/Object;)I

    move-result v1

    .line 51
    .local v1, "sortedIndex":I
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    invoke-interface {v11, v1, v3}, Ljava/util/List;->set(ILjava/lang/Object;)Ljava/lang/Object;

    .line 49
    .end local v1
    add-int/lit8 v0, v0, 0x1

    goto :goto_1

    .line 53
    .end local v0
    :cond_2
    invoke-interface {v8, v2}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lokio/ByteString;

    invoke-virtual {v0}, Lokio/ByteString;->size()I

    move-result v0

    if-eqz v0, :cond_a

    .line 60
    const/4 v0, 0x0

    .local v0, "a":I
    :goto_2
    invoke-interface {v8}, Ljava/util/List;->size()I

    move-result v1

    if-ge v0, v1, :cond_7

    .line 61
    invoke-interface {v8, v0}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lokio/ByteString;

    .line 62
    .local v1, "prefix":Lokio/ByteString;
    add-int/lit8 v2, v0, 0x1

    .local v2, "b":I
    :goto_3
    invoke-interface {v8}, Ljava/util/List;->size()I

    move-result v3

    if-ge v2, v3, :cond_6

    .line 63
    invoke-interface {v8, v2}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Lokio/ByteString;

    .line 64
    .local v3, "byteString":Lokio/ByteString;
    invoke-virtual {v3, v1}, Lokio/ByteString;->startsWith(Lokio/ByteString;)Z

    move-result v4

    if-nez v4, :cond_3

    goto :goto_5

    .line 65
    :cond_3
    invoke-virtual {v3}, Lokio/ByteString;->size()I

    move-result v4

    invoke-virtual {v1}, Lokio/ByteString;->size()I

    move-result v5

    if-eq v4, v5, :cond_5

    .line 68
    invoke-interface {v11, v2}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Ljava/lang/Integer;

    invoke-virtual {v4}, Ljava/lang/Integer;->intValue()I

    move-result v4

    invoke-interface {v11, v0}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Ljava/lang/Integer;

    invoke-virtual {v5}, Ljava/lang/Integer;->intValue()I

    move-result v5

    if-le v4, v5, :cond_4

    .line 69
    invoke-interface {v8, v2}, Ljava/util/List;->remove(I)Ljava/lang/Object;

    .line 70
    invoke-interface {v11, v2}, Ljava/util/List;->remove(I)Ljava/lang/Object;

    goto :goto_4

    .line 72
    :cond_4
    add-int/lit8 v2, v2, 0x1

    .line 74
    .end local v3
    :goto_4
    goto :goto_3

    .line 66
    .restart local v3
    :cond_5
    new-instance v4, Ljava/lang/IllegalArgumentException;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "duplicate option: "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-direct {v4, v5}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v4

    .line 60
    .end local v1
    .end local v2
    .end local v3
    :cond_6
    :goto_5
    add-int/lit8 v0, v0, 0x1

    goto :goto_2

    .line 77
    .end local v0
    :cond_7
    new-instance v6, Lokio/Buffer;

    invoke-direct {v6}, Lokio/Buffer;-><init>()V

    .line 78
    .local v6, "trieBytes":Lokio/Buffer;
    const/4 v9, 0x0

    invoke-interface {v8}, Ljava/util/List;->size()I

    move-result v10

    const-wide/16 v4, 0x0

    const/4 v7, 0x0

    invoke-static/range {v4 .. v11}, Lokio/Options;->buildTrieRecursive(JLokio/Buffer;ILjava/util/List;IILjava/util/List;)V

    .line 80
    invoke-static {v6}, Lokio/Options;->intCount(Lokio/Buffer;)I

    move-result v0

    new-array v0, v0, [I

    .line 81
    .local v0, "trie":[I
    const/4 v1, 0x0

    .local v1, "i":I
    :goto_6
    array-length v2, v0

    if-ge v1, v2, :cond_8

    .line 82
    invoke-virtual {v6}, Lokio/Buffer;->readInt()I

    move-result v2

    aput v2, v0, v1

    .line 81
    add-int/lit8 v1, v1, 0x1

    goto :goto_6

    .line 84
    .end local v1
    :cond_8
    invoke-virtual {v6}, Lokio/Buffer;->exhausted()Z

    move-result v1

    if-eqz v1, :cond_9

    .line 88
    new-instance v1, Lokio/Options;

    invoke-virtual {p0}, [Lokio/ByteString;->clone()Ljava/lang/Object;

    move-result-object v2

    check-cast v2, [Lokio/ByteString;

    invoke-direct {v1, v2, v0}, Lokio/Options;-><init>([Lokio/ByteString;[I)V

    return-object v1

    .line 85
    :cond_9
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1}, Ljava/lang/AssertionError;-><init>()V

    throw v1

    .line 54
    .end local v0
    .end local v6
    :cond_a
    new-instance v0, Ljava/lang/IllegalArgumentException;

    const-string v1, "the empty byte string is not a supported option"

    invoke-direct {v0, v1}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    goto :goto_8

    :goto_7
    throw v0

    :goto_8
    goto :goto_7
.end method


# virtual methods
.method public bridge synthetic get(I)Ljava/lang/Object;
    .locals 0

    .line 26
    invoke-virtual {p0, p1}, Lokio/Options;->get(I)Lokio/ByteString;

    move-result-object p1

    return-object p1
.end method

.method public get(I)Lokio/ByteString;
    .locals 1
    .param p1, "i"    # I

    .line 241
    iget-object v0, p0, Lokio/Options;->byteStrings:[Lokio/ByteString;

    aget-object v0, v0, p1

    return-object v0
.end method

.method public final size()I
    .locals 1

    .line 245
    iget-object v0, p0, Lokio/Options;->byteStrings:[Lokio/ByteString;

    array-length v0, v0

    return v0
.end method
