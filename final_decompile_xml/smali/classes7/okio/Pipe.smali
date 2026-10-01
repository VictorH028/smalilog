.class public final Lokio/Pipe;
.super Ljava/lang/Object;
.source "Pipe.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lokio/Pipe$PipeSource;,
        Lokio/Pipe$PipeSink;
    }
.end annotation


# instance fields
.field final buffer:Lokio/Buffer;

.field private foldedSink:Lokio/Sink;
    .annotation runtime Ljavax/annotation/Nullable;
    .end annotation
.end field

.field final maxBufferSize:J

.field private final sink:Lokio/Sink;

.field sinkClosed:Z

.field private final source:Lokio/Source;

.field sourceClosed:Z


# direct methods
.method public constructor <init>(J)V
    .locals 3
    .param p1, "maxBufferSize"    # J

    .line 46
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 39
    new-instance v0, Lokio/Buffer;

    invoke-direct {v0}, Lokio/Buffer;-><init>()V

    iput-object v0, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    .line 42
    new-instance v0, Lokio/Pipe$PipeSink;

    invoke-direct {v0, p0}, Lokio/Pipe$PipeSink;-><init>(Lokio/Pipe;)V

    iput-object v0, p0, Lokio/Pipe;->sink:Lokio/Sink;

    .line 43
    new-instance v0, Lokio/Pipe$PipeSource;

    invoke-direct {v0, p0}, Lokio/Pipe$PipeSource;-><init>(Lokio/Pipe;)V

    iput-object v0, p0, Lokio/Pipe;->source:Lokio/Source;

    .line 47
    const-wide/16 v0, 0x1

    cmp-long v2, p1, v0

    if-ltz v2, :cond_0

    .line 50
    iput-wide p1, p0, Lokio/Pipe;->maxBufferSize:J

    .line 51
    return-void

    .line 48
    :cond_0
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "maxBufferSize < 1: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1, p2}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method static synthetic access$000(Lokio/Pipe;)Lokio/Sink;
    .locals 1
    .param p0, "x0"    # Lokio/Pipe;

    .line 37
    iget-object v0, p0, Lokio/Pipe;->foldedSink:Lokio/Sink;

    return-object v0
.end method


# virtual methods
.method public fold(Lokio/Sink;)V
    .locals 7
    .param p1, "sink"    # Lokio/Sink;
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 71
    nop

    :goto_0
    const/4 v0, 0x0

    .line 73
    .local v0, "closed":Z
    iget-object v1, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    monitor-enter v1

    .line 74
    :try_start_0
    iget-object v2, p0, Lokio/Pipe;->foldedSink:Lokio/Sink;

    if-nez v2, :cond_4

    .line 76
    iget-object v2, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    invoke-virtual {v2}, Lokio/Buffer;->exhausted()Z

    move-result v2

    const/4 v3, 0x1

    if-eqz v2, :cond_0

    .line 77
    iput-boolean v3, p0, Lokio/Pipe;->sourceClosed:Z

    .line 78
    iput-object p1, p0, Lokio/Pipe;->foldedSink:Lokio/Sink;

    .line 79
    monitor-exit v1

    return-void

    .line 82
    :cond_0
    iget-boolean v2, p0, Lokio/Pipe;->sinkClosed:Z

    move v0, v2

    .line 83
    new-instance v2, Lokio/Buffer;

    invoke-direct {v2}, Lokio/Buffer;-><init>()V

    .line 84
    .local v2, "sinkBuffer":Lokio/Buffer;
    iget-object v4, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    iget-object v5, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    iget-wide v5, v5, Lokio/Buffer;->size:J

    invoke-virtual {v2, v4, v5, v6}, Lokio/Buffer;->write(Lokio/Buffer;J)V

    .line 85
    iget-object v4, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    invoke-virtual {v4}, Ljava/lang/Object;->notifyAll()V

    .line 86
    monitor-exit v1

    .line 88
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_3

    const/4 v1, 0x0

    .line 90
    .local v1, "success":Z
    :try_start_1
    iget-wide v4, v2, Lokio/Buffer;->size:J

    invoke-interface {p1, v2, v4, v5}, Lokio/Sink;->write(Lokio/Buffer;J)V

    .line 91
    if-eqz v0, :cond_1

    .line 92
    invoke-interface {p1}, Lokio/Sink;->close()V

    goto :goto_1

    .line 94
    :cond_1
    invoke-interface {p1}, Lokio/Sink;->flush()V

    .line 96
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    :goto_1
    const/4 v1, 0x1

    .line 98
    if-nez v1, :cond_2

    .line 99
    iget-object v4, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    monitor-enter v4

    .line 100
    :try_start_2
    iput-boolean v3, p0, Lokio/Pipe;->sourceClosed:Z

    .line 101
    iget-object v3, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    invoke-virtual {v3}, Ljava/lang/Object;->notifyAll()V

    .line 102
    monitor-exit v4

    goto :goto_2

    :catchall_0
    move-exception v3

    monitor-exit v4

    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    throw v3

    .line 105
    .end local v0
    .end local v1
    .end local v2
    :cond_2
    :goto_2
    goto :goto_0

    .line 98
    .restart local v0
    .restart local v1
    .restart local v2
    :catchall_1
    move-exception v4

    if-nez v1, :cond_3

    .line 99
    iget-object v5, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    monitor-enter v5

    .line 100
    :try_start_3
    iput-boolean v3, p0, Lokio/Pipe;->sourceClosed:Z

    .line 101
    iget-object v3, p0, Lokio/Pipe;->buffer:Lokio/Buffer;

    invoke-virtual {v3}, Ljava/lang/Object;->notifyAll()V

    .line 102
    monitor-exit v5

    goto :goto_3

    :catchall_2
    move-exception v3

    monitor-exit v5

    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_2

    throw v3

    :cond_3
    :goto_3
    throw v4

    .line 74
    .end local v1
    .end local v2
    :cond_4
    :try_start_4
    new-instance v2, Ljava/lang/IllegalStateException;

    const-string v3, "sink already folded"

    invoke-direct {v2, v3}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    .end local v0
    .end local p1
    throw v2

    .line 86
    .restart local v0
    .restart local p1
    :catchall_3
    move-exception v2

    monitor-exit v1

    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_3

    goto :goto_5

    :goto_4
    throw v2

    :goto_5
    goto :goto_4
.end method

.method public final sink()Lokio/Sink;
    .locals 1

    .line 58
    iget-object v0, p0, Lokio/Pipe;->sink:Lokio/Sink;

    return-object v0
.end method

.method public final source()Lokio/Source;
    .locals 1

    .line 54
    iget-object v0, p0, Lokio/Pipe;->source:Lokio/Source;

    return-object v0
.end method
