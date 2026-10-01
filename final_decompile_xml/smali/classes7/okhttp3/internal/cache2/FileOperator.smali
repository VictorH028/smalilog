.class final Lokhttp3/internal/cache2/FileOperator;
.super Ljava/lang/Object;
.source "FileOperator.java"


# instance fields
.field private final fileChannel:Ljava/nio/channels/FileChannel;


# direct methods
.method constructor <init>(Ljava/nio/channels/FileChannel;)V
    .locals 0
    .param p1, "fileChannel"    # Ljava/nio/channels/FileChannel;

    .line 39
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 40
    iput-object p1, p0, Lokhttp3/internal/cache2/FileOperator;->fileChannel:Ljava/nio/channels/FileChannel;

    .line 41
    return-void
.end method


# virtual methods
.method public read(JLokio/Buffer;J)V
    .locals 9
    .param p1, "pos"    # J
    .param p3, "sink"    # Lokio/Buffer;
    .param p4, "byteCount"    # J
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 60
    const-wide/16 v0, 0x0

    cmp-long v2, p4, v0

    if-ltz v2, :cond_1

    move-wide v4, p1

    move-wide v6, p4

    .line 62
    .end local p1
    .end local p4
    .local v4, "pos":J
    .local v6, "byteCount":J
    :goto_0
    cmp-long p1, v6, v0

    if-lez p1, :cond_0

    .line 63
    iget-object v3, p0, Lokhttp3/internal/cache2/FileOperator;->fileChannel:Ljava/nio/channels/FileChannel;

    move-object v8, p3

    .end local p3
    .local v8, "sink":Lokio/Buffer;
    invoke-virtual/range {v3 .. v8}, Ljava/nio/channels/FileChannel;->transferTo(JJLjava/nio/channels/WritableByteChannel;)J

    move-result-wide p1

    .line 64
    .local p1, "bytesRead":J
    add-long/2addr v4, p1

    .line 65
    sub-long/2addr v6, p1

    .line 66
    .end local p1
    goto :goto_0

    .line 67
    .end local v8
    .restart local p3
    :cond_0
    return-void

    .line 60
    .end local v4
    .end local v6
    .local p1, "pos":J
    .restart local p4
    :cond_1
    move-object v8, p3

    .end local p3
    .restart local v8
    new-instance p3, Ljava/lang/IndexOutOfBoundsException;

    invoke-direct {p3}, Ljava/lang/IndexOutOfBoundsException;-><init>()V

    goto :goto_2

    :goto_1
    throw p3

    :goto_2
    goto :goto_1
.end method

.method public write(JLokio/Buffer;J)V
    .locals 11
    .param p1, "pos"    # J
    .param p3, "source"    # Lokio/Buffer;
    .param p4, "byteCount"    # J
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 45
    const-wide/16 v0, 0x0

    cmp-long v2, p4, v0

    if-ltz v2, :cond_1

    invoke-virtual {p3}, Lokio/Buffer;->size()J

    move-result-wide v2

    cmp-long v4, p4, v2

    if-gtz v4, :cond_1

    move-wide v7, p1

    move-wide v9, p4

    .line 47
    .end local p1
    .end local p4
    .local v7, "pos":J
    .local v9, "byteCount":J
    :goto_0
    cmp-long p1, v9, v0

    if-lez p1, :cond_0

    .line 48
    iget-object v5, p0, Lokhttp3/internal/cache2/FileOperator;->fileChannel:Ljava/nio/channels/FileChannel;

    move-object v6, p3

    invoke-virtual/range {v5 .. v10}, Ljava/nio/channels/FileChannel;->transferFrom(Ljava/nio/channels/ReadableByteChannel;JJ)J

    move-result-wide p1

    .line 49
    .local p1, "bytesWritten":J
    add-long/2addr v7, p1

    .line 50
    sub-long/2addr v9, p1

    .line 51
    .end local p1
    goto :goto_0

    .line 52
    :cond_0
    return-void

    .line 45
    .end local v7
    .end local v9
    .local p1, "pos":J
    .restart local p4
    :cond_1
    new-instance v0, Ljava/lang/IndexOutOfBoundsException;

    invoke-direct {v0}, Ljava/lang/IndexOutOfBoundsException;-><init>()V

    goto :goto_2

    :goto_1
    throw v0

    :goto_2
    goto :goto_1
.end method
