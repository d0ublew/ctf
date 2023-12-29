.class Luk/rossmarks/fridalab/MainActivity$2;
.super Ljava/util/TimerTask;
.source "MainActivity.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Luk/rossmarks/fridalab/MainActivity;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Luk/rossmarks/fridalab/MainActivity;


# direct methods
.method constructor <init>(Luk/rossmarks/fridalab/MainActivity;)V
    .locals 0

    .line 52
    iput-object p1, p0, Luk/rossmarks/fridalab/MainActivity$2;->this$0:Luk/rossmarks/fridalab/MainActivity;

    invoke-direct {p0}, Ljava/util/TimerTask;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 2

    .line 55
    new-instance v0, Ljava/util/Random;

    invoke-direct {v0}, Ljava/util/Random;-><init>()V

    const/16 v1, 0x32

    .line 56
    invoke-virtual {v0, v1}, Ljava/util/Random;->nextInt(I)I

    move-result v0

    add-int/lit8 v0, v0, 0x1

    .line 57
    invoke-static {v0}, Luk/rossmarks/fridalab/challenge_06;->addChall06(I)V

    .line 58
    invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    return-void
.end method
