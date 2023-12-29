.class Luk/rossmarks/fridalab/MainActivity$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


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

    .line 34
    iput-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 2

    .line 37
    invoke-static {}, Luk/rossmarks/fridalab/challenge_01;->getChall01Int()I

    move-result p1

    const/4 v0, 0x1

    if-ne p1, v0, :cond_0

    .line 38
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    iget-object p1, p1, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x0

    aput v0, p1, v1

    .line 39
    :cond_0
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    invoke-virtual {p1}, Luk/rossmarks/fridalab/MainActivity;->chall03()Z

    move-result p1

    if-eqz p1, :cond_1

    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    iget-object p1, p1, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x2

    aput v0, p1, v1

    .line 40
    :cond_1
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    const-string v1, "notfrida!"

    invoke-virtual {p1, v1}, Luk/rossmarks/fridalab/MainActivity;->chall05(Ljava/lang/String;)V

    .line 41
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    invoke-virtual {p1}, Luk/rossmarks/fridalab/MainActivity;->chall08()Z

    move-result p1

    if-eqz p1, :cond_2

    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    iget-object p1, p1, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x7

    aput v0, p1, v1

    .line 43
    :cond_2
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity$1;->this$0:Luk/rossmarks/fridalab/MainActivity;

    invoke-static {p1}, Luk/rossmarks/fridalab/MainActivity;->access$000(Luk/rossmarks/fridalab/MainActivity;)V

    return-void
.end method
