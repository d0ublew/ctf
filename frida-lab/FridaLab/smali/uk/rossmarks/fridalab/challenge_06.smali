.class public Luk/rossmarks/fridalab/challenge_06;
.super Ljava/lang/Object;
.source "challenge_06.java"


# static fields
.field static chall06:I

.field static timeStart:J


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .line 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static addChall06(I)V
    .locals 2

    .line 22
    sget v0, Luk/rossmarks/fridalab/challenge_06;->chall06:I

    add-int/2addr v0, p0

    sput v0, Luk/rossmarks/fridalab/challenge_06;->chall06:I

    .line 23
    sget v0, Luk/rossmarks/fridalab/challenge_06;->chall06:I

    const/16 v1, 0x2328

    if-le v0, v1, :cond_0

    .line 24
    sput p0, Luk/rossmarks/fridalab/challenge_06;->chall06:I

    :cond_0
    return-void
.end method

.method public static confirmChall06(I)Z
    .locals 6

    .line 13
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    .line 14
    sget v2, Luk/rossmarks/fridalab/challenge_06;->chall06:I

    if-ne p0, v2, :cond_0

    sget-wide v2, Luk/rossmarks/fridalab/challenge_06;->timeStart:J

    const-wide/16 v4, 0x2710

    add-long/2addr v2, v4

    cmp-long p0, v0, v2

    if-lez p0, :cond_0

    const/4 p0, 0x1

    return p0

    :cond_0
    const/4 p0, 0x0

    return p0
.end method

.method public static startTime()V
    .locals 2

    .line 8
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    sput-wide v0, Luk/rossmarks/fridalab/challenge_06;->timeStart:J

    return-void
.end method
