.class public Luk/rossmarks/fridalab/MainActivity;
.super Landroid/support/v7/app/AppCompatActivity;
.source "MainActivity.java"


# instance fields
.field public completeArr:[I


# direct methods
.method public constructor <init>()V
    .locals 1

    .line 24
    invoke-direct {p0}, Landroid/support/v7/app/AppCompatActivity;-><init>()V

    const/16 v0, 0x8

    .line 25
    new-array v0, v0, [I

    fill-array-data v0, :array_0

    iput-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    return-void

    nop

    :array_0
    .array-data 4
        0x0
        0x0
        0x0
        0x0
        0x0
        0x0
        0x0
        0x0
    .end array-data
.end method

.method static synthetic access$000(Luk/rossmarks/fridalab/MainActivity;)V
    .locals 0

    .line 24
    invoke-direct {p0}, Luk/rossmarks/fridalab/MainActivity;->changeColors()V

    return-void
.end method

.method private chall02()V
    .locals 2

    .line 117
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x1

    aput v1, v0, v1

    return-void
.end method

.method private changeColors()V
    .locals 12

    const v0, 0x7f070027

    .line 66
    invoke-virtual {p0, v0}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/TextView;

    const v1, 0x7f070028

    .line 67
    invoke-virtual {p0, v1}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v1

    check-cast v1, Landroid/widget/TextView;

    const v2, 0x7f070029

    .line 68
    invoke-virtual {p0, v2}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v2

    check-cast v2, Landroid/widget/TextView;

    const v3, 0x7f07002a

    .line 69
    invoke-virtual {p0, v3}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v3

    check-cast v3, Landroid/widget/TextView;

    const v4, 0x7f07002b

    .line 70
    invoke-virtual {p0, v4}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v4

    check-cast v4, Landroid/widget/TextView;

    const v5, 0x7f07002c

    .line 71
    invoke-virtual {p0, v5}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v5

    check-cast v5, Landroid/widget/TextView;

    const v6, 0x7f07002d

    .line 72
    invoke-virtual {p0, v6}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v6

    check-cast v6, Landroid/widget/TextView;

    const v7, 0x7f07002e

    .line 73
    invoke-virtual {p0, v7}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v7

    check-cast v7, Landroid/widget/TextView;

    .line 74
    iget-object v8, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v9, 0x0

    aget v8, v8, v9

    const/high16 v9, -0x10000

    const v10, -0xff0100

    const/4 v11, 0x1

    if-ne v8, v11, :cond_0

    .line 75
    invoke-virtual {v0, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_0

    .line 77
    :cond_0
    invoke-virtual {v0, v9}, Landroid/widget/TextView;->setTextColor(I)V

    .line 79
    :goto_0
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    aget v0, v0, v11

    if-ne v0, v11, :cond_1

    .line 80
    invoke-virtual {v1, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_1

    .line 82
    :cond_1
    invoke-virtual {v1, v9}, Landroid/widget/TextView;->setTextColor(I)V

    .line 84
    :goto_1
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x2

    aget v0, v0, v1

    if-ne v0, v11, :cond_2

    .line 85
    invoke-virtual {v2, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_2

    .line 87
    :cond_2
    invoke-virtual {v2, v9}, Landroid/widget/TextView;->setTextColor(I)V

    .line 89
    :goto_2
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x3

    aget v0, v0, v1

    if-ne v0, v11, :cond_3

    .line 90
    invoke-virtual {v3, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_3

    .line 92
    :cond_3
    invoke-virtual {v3, v9}, Landroid/widget/TextView;->setTextColor(I)V

    .line 94
    :goto_3
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x4

    aget v0, v0, v1

    if-ne v0, v11, :cond_4

    .line 95
    invoke-virtual {v4, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_4

    .line 97
    :cond_4
    invoke-virtual {v4, v9}, Landroid/widget/TextView;->setTextColor(I)V

    .line 99
    :goto_4
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x5

    aget v0, v0, v1

    if-ne v0, v11, :cond_5

    .line 100
    invoke-virtual {v5, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_5

    .line 102
    :cond_5
    invoke-virtual {v5, v9}, Landroid/widget/TextView;->setTextColor(I)V

    .line 104
    :goto_5
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x6

    aget v0, v0, v1

    if-ne v0, v11, :cond_6

    .line 105
    invoke-virtual {v6, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_6

    .line 107
    :cond_6
    invoke-virtual {v6, v9}, Landroid/widget/TextView;->setTextColor(I)V

    .line 109
    :goto_6
    iget-object v0, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x7

    aget v0, v0, v1

    if-ne v0, v11, :cond_7

    .line 110
    invoke-virtual {v7, v10}, Landroid/widget/TextView;->setTextColor(I)V

    goto :goto_7

    .line 112
    :cond_7
    invoke-virtual {v7, v9}, Landroid/widget/TextView;->setTextColor(I)V

    :goto_7
    return-void
.end method


# virtual methods
.method public chall03()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public chall04(Ljava/lang/String;)V
    .locals 2

    const-string v0, "frida"

    .line 125
    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_0

    .line 126
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v0, 0x3

    const/4 v1, 0x1

    aput v1, p1, v0

    :cond_0
    return-void
.end method

.method public chall05(Ljava/lang/String;)V
    .locals 2

    const-string v0, "frida"

    .line 131
    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    const/4 v0, 0x4

    if-eqz p1, :cond_0

    .line 132
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x1

    aput v1, p1, v0

    goto :goto_0

    .line 134
    :cond_0
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x0

    aput v1, p1, v0

    :goto_0
    return-void
.end method

.method public chall06(I)V
    .locals 2

    .line 139
    invoke-static {p1}, Luk/rossmarks/fridalab/challenge_06;->confirmChall06(I)Z

    move-result p1

    if-eqz p1, :cond_0

    .line 140
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v0, 0x5

    const/4 v1, 0x1

    aput v1, p1, v0

    :cond_0
    return-void
.end method

.method public chall07(Ljava/lang/String;)V
    .locals 2

    .line 145
    invoke-static {p1}, Luk/rossmarks/fridalab/challenge_07;->check07Pin(Ljava/lang/String;)Z

    move-result p1

    const/4 v0, 0x6

    if-eqz p1, :cond_0

    .line 146
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x1

    aput v1, p1, v0

    goto :goto_0

    .line 148
    :cond_0
    iget-object p1, p0, Luk/rossmarks/fridalab/MainActivity;->completeArr:[I

    const/4 v1, 0x0

    aput v1, p1, v0

    :goto_0
    return-void
.end method

.method public chall08()Z
    .locals 2

    const v0, 0x7f07002f

    .line 153
    invoke-virtual {p0, v0}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    .line 154
    invoke-virtual {v0}, Landroid/widget/Button;->getText()Ljava/lang/CharSequence;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    const-string v1, "Confirm"

    .line 155
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 6

    .line 29
    invoke-super {p0, p1}, Landroid/support/v7/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    const p1, 0x7f09001c

    .line 30
    invoke-virtual {p0, p1}, Luk/rossmarks/fridalab/MainActivity;->setContentView(I)V

    const p1, 0x7f07002f

    .line 33
    invoke-virtual {p0, p1}, Luk/rossmarks/fridalab/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroid/widget/Button;

    .line 34
    new-instance v0, Luk/rossmarks/fridalab/MainActivity$1;

    invoke-direct {v0, p0}, Luk/rossmarks/fridalab/MainActivity$1;-><init>(Luk/rossmarks/fridalab/MainActivity;)V

    invoke-virtual {p1, v0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 48
    invoke-static {}, Luk/rossmarks/fridalab/challenge_06;->startTime()V

    .line 49
    new-instance p1, Ljava/util/Random;

    invoke-direct {p1}, Ljava/util/Random;-><init>()V

    const/16 v0, 0x32

    .line 50
    invoke-virtual {p1, v0}, Ljava/util/Random;->nextInt(I)I

    move-result p1

    add-int/lit8 p1, p1, 0x1

    .line 51
    invoke-static {p1}, Luk/rossmarks/fridalab/challenge_06;->addChall06(I)V

    .line 52
    new-instance v0, Ljava/util/Timer;

    invoke-direct {v0}, Ljava/util/Timer;-><init>()V

    new-instance v1, Luk/rossmarks/fridalab/MainActivity$2;

    invoke-direct {v1, p0}, Luk/rossmarks/fridalab/MainActivity$2;-><init>(Luk/rossmarks/fridalab/MainActivity;)V

    const-wide/16 v2, 0x0

    const-wide/16 v4, 0x3e8

    invoke-virtual/range {v0 .. v5}, Ljava/util/Timer;->scheduleAtFixedRate(Ljava/util/TimerTask;JJ)V

    .line 62
    invoke-static {}, Luk/rossmarks/fridalab/challenge_07;->setChall07()V

    return-void
.end method
