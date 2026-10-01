.class public final Lokio/GzipSource;
.super Ljava/lang/Object;
.source "GzipSource.java"

# interfaces
.implements Lokio/Source;


# static fields
.field private static final FCOMMENT:B = 0x4t

.field private static final FEXTRA:B = 0x2t

.field private static final FHCRC:B = 0x1t

.field private static final FNAME:B = 0x3t

.field private static final SECTION_BODY:B = 0x1t

.field private static final SECTION_DONE:B = 0x3t

.field private static final SECTION_HEADER:B = 0x0t

.field private static final SECTION_TRAILER:B = 0x2t


# instance fields
.field private final crc:Ljava/util/zip/CRC32;

.field private final inflater:Ljava/util/zip/Inflater;

.field private final inflaterSource:Lokio/InflaterSource;

.field private section:I

.field private final source:Lokio/BufferedSource;


# direct methods
.method public constructor <init>(Lokio/Source;)V
    .locals 3
    .param p1, "source"    # Lokio/Source;

    .line 60
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 39
    const/4 v0, 0x0

    iput v0, p0, Lokio/GzipSource;->section:I

    .line 58
    new-instance v0, Ljava/util/zip/CRC32;

    invoke-direct {v0}, Ljava/util/zip/CRC32;-><init>()V

    iput-object v0, p0, Lokio/GzipSource;->crc:Ljava/util/zip/CRC32;

    .line 61
    if-eqz p1, :cond_0

    .line 62
    new-instance v0, Ljava/util/zip/Inflater;

    const/4 v1, 0x1

    invoke-direct {v0, v1}, Ljava/util/zip/Inflater;-><init>(Z)V

    iput-object v0, p0, Lokio/GzipSource;->inflater:Ljava/util/zip/Inflater;

    .line 63
    invoke-static {p1}, Lokio/Okio;->buffer(Lokio/Source;)Lokio/BufferedSource;

    move-result-object v0

    iput-object v0, p0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    .line 64
    new-instance v0, Lokio/InflaterSource;

    iget-object v1, p0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    iget-object v2, p0, Lokio/GzipSource;->inflater:Ljava/util/zip/Inflater;

    invoke-direct {v0, v1, v2}, Lokio/InflaterSource;-><init>(Lokio/BufferedSource;Ljava/util/zip/Inflater;)V

    iput-object v0, p0, Lokio/GzipSource;->inflaterSource:Lokio/InflaterSource;

    .line 65
    return-void

    .line 61
    :cond_0
    new-instance v0, Ljava/lang/IllegalArgumentException;

    const-string v1, "source == null"

    invoke-direct {v0, v1}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method private checkEqual(Ljava/lang/String;II)V
    .locals 5
    .param p1, "name"    # Ljava/lang/String;
    .param p2, "expected"    # I
    .param p3, "actual"    # I
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 204
    if-ne p3, p2, :cond_0

    .line 208
    return-void

    .line 205
    :cond_0
    new-instance v0, Ljava/io/IOException;

    .line 206
    invoke-static {p3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    const/4 v3, 0x3

    new-array v3, v3, [Ljava/lang/Object;

    const/4 v4, 0x0

    aput-object p1, v3, v4

    const/4 v4, 0x1

    aput-object v1, v3, v4

    const/4 v1, 0x2

    aput-object v2, v3, v1

    .line 205
    const-string v1, "%s: actual 0x%08x != expected 0x%08x"

    invoke-static {v1, v3}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method private consumeHeader()V
    .locals 17
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 114
    move-object/from16 v0, p0

    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    const-wide/16 v2, 0xa

    invoke-interface {v1, v2, v3}, Lokio/BufferedSource;->require(J)V

    .line 115
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->buffer()Lokio/Buffer;

    move-result-object v1

    const-wide/16 v2, 0x3

    invoke-virtual {v1, v2, v3}, Lokio/Buffer;->getByte(J)B

    move-result v6

    .line 116
    .local v6, "flags":B
    shr-int/lit8 v1, v6, 0x1

    const/4 v7, 0x1

    and-int/2addr v1, v7

    const/4 v8, 0x0

    if-ne v1, v7, :cond_0

    const/4 v1, 0x1

    goto :goto_0

    :cond_0
    const/4 v1, 0x0

    :goto_0
    move v9, v1

    .line 117
    .local v9, "fhcrc":Z
    if-eqz v9, :cond_1

    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->buffer()Lokio/Buffer;

    move-result-object v1

    const-wide/16 v2, 0x0

    const-wide/16 v4, 0xa

    invoke-direct/range {v0 .. v5}, Lokio/GzipSource;->updateCrc(Lokio/Buffer;JJ)V

    .line 119
    :cond_1
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->readShort()S

    move-result v10

    .line 120
    .local v10, "id1id2":S
    const-string v1, "ID1ID2"

    const/16 v2, 0x1f8b

    invoke-direct {v0, v1, v2, v10}, Lokio/GzipSource;->checkEqual(Ljava/lang/String;II)V

    .line 121
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    const-wide/16 v2, 0x8

    invoke-interface {v1, v2, v3}, Lokio/BufferedSource;->skip(J)V

    .line 127
    shr-int/lit8 v1, v6, 0x2

    and-int/2addr v1, v7

    if-ne v1, v7, :cond_4

    .line 128
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    const-wide/16 v2, 0x2

    invoke-interface {v1, v2, v3}, Lokio/BufferedSource;->require(J)V

    .line 129
    if-eqz v9, :cond_2

    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->buffer()Lokio/Buffer;

    move-result-object v1

    const-wide/16 v2, 0x0

    const-wide/16 v4, 0x2

    invoke-direct/range {v0 .. v5}, Lokio/GzipSource;->updateCrc(Lokio/Buffer;JJ)V

    .line 130
    :cond_2
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->buffer()Lokio/Buffer;

    move-result-object v1

    invoke-virtual {v1}, Lokio/Buffer;->readShortLe()S

    move-result v11

    .line 131
    .local v11, "xlen":I
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    int-to-long v2, v11

    invoke-interface {v1, v2, v3}, Lokio/BufferedSource;->require(J)V

    .line 132
    if-eqz v9, :cond_3

    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->buffer()Lokio/Buffer;

    move-result-object v1

    const-wide/16 v2, 0x0

    int-to-long v4, v11

    invoke-direct/range {v0 .. v5}, Lokio/GzipSource;->updateCrc(Lokio/Buffer;JJ)V

    .line 133
    :cond_3
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    int-to-long v2, v11

    invoke-interface {v1, v2, v3}, Lokio/BufferedSource;->skip(J)V

    .line 140
    .end local v11
    :cond_4
    shr-int/lit8 v1, v6, 0x3

    and-int/2addr v1, v7

    const-wide/16 v11, -0x1

    const-wide/16 v13, 0x1

    if-ne v1, v7, :cond_7

    .line 141
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1, v8}, Lokio/BufferedSource;->indexOf(B)J

    move-result-wide v15

    .line 142
    .local v15, "index":J
    cmp-long v1, v15, v11

    if-eqz v1, :cond_6

    .line 143
    if-eqz v9, :cond_5

    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->buffer()Lokio/Buffer;

    move-result-object v1

    const-wide/16 v2, 0x0

    add-long v4, v15, v13

    invoke-direct/range {v0 .. v5}, Lokio/GzipSource;->updateCrc(Lokio/Buffer;JJ)V

    .line 144
    :cond_5
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    add-long v2, v15, v13

    invoke-interface {v1, v2, v3}, Lokio/BufferedSource;->skip(J)V

    goto :goto_1

    .line 142
    :cond_6
    new-instance v1, Ljava/io/EOFException;

    invoke-direct {v1}, Ljava/io/EOFException;-><init>()V

    throw v1

    .line 151
    .end local v15
    :cond_7
    :goto_1
    shr-int/lit8 v1, v6, 0x4

    and-int/2addr v1, v7

    if-ne v1, v7, :cond_a

    .line 152
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1, v8}, Lokio/BufferedSource;->indexOf(B)J

    move-result-wide v7

    .line 153
    .local v7, "index":J
    cmp-long v1, v7, v11

    if-eqz v1, :cond_9

    .line 154
    if-eqz v9, :cond_8

    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->buffer()Lokio/Buffer;

    move-result-object v1

    const-wide/16 v2, 0x0

    add-long v4, v7, v13

    invoke-direct/range {v0 .. v5}, Lokio/GzipSource;->updateCrc(Lokio/Buffer;JJ)V

    .line 155
    :cond_8
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    add-long/2addr v13, v7

    invoke-interface {v1, v13, v14}, Lokio/BufferedSource;->skip(J)V

    goto :goto_2

    .line 153
    :cond_9
    new-instance v1, Ljava/io/EOFException;

    invoke-direct {v1}, Ljava/io/EOFException;-><init>()V

    throw v1

    .line 162
    .end local v7
    :cond_a
    :goto_2
    if-eqz v9, :cond_b

    .line 163
    iget-object v1, v0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v1}, Lokio/BufferedSource;->readShortLe()S

    move-result v1

    iget-object v2, v0, Lokio/GzipSource;->crc:Ljava/util/zip/CRC32;

    invoke-virtual {v2}, Ljava/util/zip/CRC32;->getValue()J

    move-result-wide v2

    long-to-int v3, v2

    int-to-short v2, v3

    const-string v3, "FHCRC"

    invoke-direct {v0, v3, v1, v2}, Lokio/GzipSource;->checkEqual(Ljava/lang/String;II)V

    .line 164
    iget-object v1, v0, Lokio/GzipSource;->crc:Ljava/util/zip/CRC32;

    invoke-virtual {v1}, Ljava/util/zip/CRC32;->reset()V

    .line 166
    :cond_b
    return-void
.end method

.method private consumeTrailer()V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 173
    iget-object v0, p0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v0}, Lokio/BufferedSource;->readIntLe()I

    move-result v0

    iget-object v1, p0, Lokio/GzipSource;->crc:Ljava/util/zip/CRC32;

    invoke-virtual {v1}, Ljava/util/zip/CRC32;->getValue()J

    move-result-wide v1

    long-to-int v2, v1

    const-string v1, "CRC"

    invoke-direct {p0, v1, v0, v2}, Lokio/GzipSource;->checkEqual(Ljava/lang/String;II)V

    .line 174
    iget-object v0, p0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v0}, Lokio/BufferedSource;->readIntLe()I

    move-result v0

    iget-object v1, p0, Lokio/GzipSource;->inflater:Ljava/util/zip/Inflater;

    invoke-virtual {v1}, Ljava/util/zip/Inflater;->getBytesWritten()J

    move-result-wide v1

    long-to-int v2, v1

    const-string v1, "ISIZE"

    invoke-direct {p0, v1, v0, v2}, Lokio/GzipSource;->checkEqual(Ljava/lang/String;II)V

    .line 175
    return-void
.end method

.method private updateCrc(Lokio/Buffer;JJ)V
    .locals 5
    .param p1, "buffer"    # Lokio/Buffer;
    .param p2, "offset"    # J
    .param p4, "byteCount"    # J

    .line 188
    iget-object v0, p1, Lokio/Buffer;->head:Lokio/Segment;

    .line 189
    .local v0, "s":Lokio/Segment;
    :goto_0
    iget v1, v0, Lokio/Segment;->limit:I

    iget v2, v0, Lokio/Segment;->pos:I

    sub-int/2addr v1, v2

    int-to-long v1, v1

    cmp-long v3, p2, v1

    if-ltz v3, :cond_0

    .line 190
    iget v1, v0, Lokio/Segment;->limit:I

    iget v2, v0, Lokio/Segment;->pos:I

    sub-int/2addr v1, v2

    int-to-long v1, v1

    sub-long/2addr p2, v1

    .line 189
    iget-object v0, v0, Lokio/Segment;->next:Lokio/Segment;

    goto :goto_0

    .line 194
    :cond_0
    :goto_1
    const-wide/16 v1, 0x0

    cmp-long v3, p4, v1

    if-lez v3, :cond_1

    .line 195
    iget v1, v0, Lokio/Segment;->pos:I

    int-to-long v1, v1

    add-long/2addr v1, p2

    long-to-int v2, v1

    .line 196
    .local v2, "pos":I
    iget v1, v0, Lokio/Segment;->limit:I

    sub-int/2addr v1, v2

    int-to-long v3, v1

    invoke-static {v3, v4, p4, p5}, Ljava/lang/Math;->min(JJ)J

    move-result-wide v3

    long-to-int v1, v3

    .line 197
    .local v1, "toUpdate":I
    iget-object v3, p0, Lokio/GzipSource;->crc:Ljava/util/zip/CRC32;

    iget-object v4, v0, Lokio/Segment;->data:[B

    invoke-virtual {v3, v4, v2, v1}, Ljava/util/zip/CRC32;->update([BII)V

    .line 198
    int-to-long v3, v1

    sub-long/2addr p4, v3

    .line 199
    const-wide/16 p2, 0x0

    .line 194
    .end local v1
    .end local v2
    iget-object v0, v0, Lokio/Segment;->next:Lokio/Segment;

    goto :goto_1

    .line 201
    :cond_1
    return-void
.end method


# virtual methods
.method public close()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 182
    iget-object v0, p0, Lokio/GzipSource;->inflaterSource:Lokio/InflaterSource;

    invoke-virtual {v0}, Lokio/InflaterSource;->close()V

    .line 183
    return-void
.end method

.method public read(Lokio/Buffer;J)J
    .locals 11
    .param p1, "sink"    # Lokio/Buffer;
    .param p2, "byteCount"    # J
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 68
    const-wide/16 v0, 0x0

    cmp-long v2, p2, v0

    if-ltz v2, :cond_6

    .line 69
    cmp-long v2, p2, v0

    if-nez v2, :cond_0

    return-wide v0

    .line 72
    :cond_0
    iget v0, p0, Lokio/GzipSource;->section:I

    const/4 v1, 0x1

    if-nez v0, :cond_1

    .line 73
    invoke-direct {p0}, Lokio/GzipSource;->consumeHeader()V

    .line 74
    iput v1, p0, Lokio/GzipSource;->section:I

    .line 78
    :cond_1
    iget v0, p0, Lokio/GzipSource;->section:I

    const-wide/16 v2, -0x1

    const/4 v4, 0x2

    if-ne v0, v1, :cond_3

    .line 79
    iget-wide v7, p1, Lokio/Buffer;->size:J

    .line 80
    .local v7, "offset":J
    iget-object v0, p0, Lokio/GzipSource;->inflaterSource:Lokio/InflaterSource;

    invoke-virtual {v0, p1, p2, p3}, Lokio/InflaterSource;->read(Lokio/Buffer;J)J

    move-result-wide v9

    .line 81
    .local v9, "result":J
    cmp-long v0, v9, v2

    if-eqz v0, :cond_2

    .line 82
    move-object v5, p0

    move-object v6, p1

    .end local p1
    .local v6, "sink":Lokio/Buffer;
    invoke-direct/range {v5 .. v10}, Lokio/GzipSource;->updateCrc(Lokio/Buffer;JJ)V

    .line 83
    return-wide v9

    .line 85
    .end local v6
    .restart local p1
    :cond_2
    move-object v6, p1

    .end local p1
    .restart local v6
    iput v4, p0, Lokio/GzipSource;->section:I

    goto :goto_0

    .line 78
    .end local v6
    .end local v7
    .end local v9
    .restart local p1
    :cond_3
    move-object v6, p1

    .line 91
    .end local p1
    .restart local v6
    :goto_0
    iget p1, p0, Lokio/GzipSource;->section:I

    if-ne p1, v4, :cond_5

    .line 92
    invoke-direct {p0}, Lokio/GzipSource;->consumeTrailer()V

    .line 93
    const/4 p1, 0x3

    iput p1, p0, Lokio/GzipSource;->section:I

    .line 99
    iget-object p1, p0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {p1}, Lokio/BufferedSource;->exhausted()Z

    move-result p1

    if-eqz p1, :cond_4

    goto :goto_1

    .line 100
    :cond_4
    new-instance p1, Ljava/io/IOException;

    const-string v0, "gzip finished without exhausting source"

    invoke-direct {p1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 104
    :cond_5
    :goto_1
    return-wide v2

    .line 68
    .end local v6
    .restart local p1
    :cond_6
    move-object v6, p1

    .end local p1
    .restart local v6
    new-instance p1, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "byteCount < 0: "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p2, p3}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p1, v0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1
.end method

.method public timeout()Lokio/Timeout;
    .locals 1

    .line 178
    iget-object v0, p0, Lokio/GzipSource;->source:Lokio/BufferedSource;

    invoke-interface {v0}, Lokio/BufferedSource;->timeout()Lokio/Timeout;

    move-result-object v0

    return-object v0
.end method
