package com.google.android.material.color.utilities;

import androidx.core.view.ViewCompat;
import java.util.HashMap;
import java.util.function.BiFunction;
import java.util.function.Function;

public final class DynamicColor {
    public final Function<DynamicScheme, DynamicColor> background;
    public final Function<DynamicScheme, Double> chroma;
    private final HashMap<DynamicScheme, Hct> hctCache = new HashMap<>();
    public final Function<DynamicScheme, Double> hue;
    public final Function<DynamicScheme, Double> opacity;
    public final Function<DynamicScheme, Double> tone;
    public final Function<DynamicScheme, ToneDeltaConstraint> toneDeltaConstraint;
    public final Function<DynamicScheme, Double> toneMaxContrast;
    public final Function<DynamicScheme, Double> toneMinContrast;

    static /* synthetic */ TonalPalette lambda$fromArgb$0(TonalPalette tonalPalette, DynamicScheme dynamicScheme) {
        return tonalPalette;
    }

    static /* synthetic */ DynamicColor lambda$getTone$11(DynamicColor dynamicColor, DynamicScheme dynamicScheme) {
        return dynamicColor;
    }

    static /* synthetic */ Double lambda$toneMinContrastDefault$16(Double d) {
        return d;
    }

    public DynamicColor(Function<DynamicScheme, Double> function, Function<DynamicScheme, Double> function2, Function<DynamicScheme, Double> function3, Function<DynamicScheme, Double> function4, Function<DynamicScheme, DynamicColor> function5, Function<DynamicScheme, Double> function6, Function<DynamicScheme, Double> function7, Function<DynamicScheme, ToneDeltaConstraint> function8) {
        this.hue = function;
        this.chroma = function2;
        this.tone = function3;
        this.opacity = function4;
        this.background = function5;
        this.toneMinContrast = function6;
        this.toneMaxContrast = function7;
        this.toneDeltaConstraint = function8;
    }

    public static DynamicColor fromArgb(int i) {
        return fromPalette(new DynamicColor$$ExternalSyntheticLambda6(TonalPalette.fromInt(i)), new DynamicColor$$ExternalSyntheticLambda7(Hct.fromInt(i)));
    }

    public static DynamicColor fromArgb(int i, Function<DynamicScheme, Double> function) {
        return fromPalette(new DynamicColor$$ExternalSyntheticLambda17(i), function);
    }

    public static DynamicColor fromArgb(int i, Function<DynamicScheme, Double> function, Function<DynamicScheme, DynamicColor> function2) {
        return fromPalette(new DynamicColor$$ExternalSyntheticLambda16(i), function, function2);
    }

    public static DynamicColor fromArgb(int i, Function<DynamicScheme, Double> function, Function<DynamicScheme, DynamicColor> function2, Function<DynamicScheme, ToneDeltaConstraint> function3) {
        return fromPalette(new DynamicColor$$ExternalSyntheticLambda5(i), function, function2, function3);
    }

    public static DynamicColor fromPalette(Function<DynamicScheme, TonalPalette> function, Function<DynamicScheme, Double> function2) {
        return fromPalette(function, function2, (Function<DynamicScheme, DynamicColor>) null, (Function<DynamicScheme, ToneDeltaConstraint>) null);
    }

    public static DynamicColor fromPalette(Function<DynamicScheme, TonalPalette> function, Function<DynamicScheme, Double> function2, Function<DynamicScheme, DynamicColor> function3) {
        return fromPalette(function, function2, function3, (Function<DynamicScheme, ToneDeltaConstraint>) null);
    }

    public static DynamicColor fromPalette(Function<DynamicScheme, TonalPalette> function, Function<DynamicScheme, Double> function2, Function<DynamicScheme, DynamicColor> function3, Function<DynamicScheme, ToneDeltaConstraint> function4) {
        return new DynamicColor(new DynamicColor$$ExternalSyntheticLambda0(function), new DynamicColor$$ExternalSyntheticLambda10(function), function2, (Function<DynamicScheme, Double>) null, function3, new DynamicColor$$ExternalSyntheticLambda11(function2, function3, function4), new DynamicColor$$ExternalSyntheticLambda12(function2, function3, function4), function4);
    }

    public int getArgb(DynamicScheme dynamicScheme) {
        int i = getHct(dynamicScheme).toInt();
        Function<DynamicScheme, Double> function = this.opacity;
        if (function == null) {
            return i;
        }
        return (MathUtils.clampInt(0, 255, (int) Math.round(function.apply(dynamicScheme).doubleValue() * 255.0d)) << 24) | (i & ViewCompat.MEASURED_SIZE_MASK);
    }

    public Hct getHct(DynamicScheme dynamicScheme) {
        Hct hct = this.hctCache.get(dynamicScheme);
        if (hct != null) {
            return hct;
        }
        Hct from = Hct.from(this.hue.apply(dynamicScheme).doubleValue(), this.chroma.apply(dynamicScheme).doubleValue(), getTone(dynamicScheme));
        if (this.hctCache.size() > 4) {
            this.hctCache.clear();
        }
        this.hctCache.put(dynamicScheme, from);
        return from;
    }

    public double getTone(DynamicScheme dynamicScheme) {
        double d;
        DynamicScheme dynamicScheme2 = dynamicScheme;
        double doubleValue = this.tone.apply(dynamicScheme2).doubleValue();
        boolean z = true;
        boolean z2 = dynamicScheme2.contrastLevel < 0.0d;
        if (dynamicScheme2.contrastLevel != 0.0d) {
            double doubleValue2 = this.tone.apply(dynamicScheme2).doubleValue();
            doubleValue = doubleValue2 + (((z2 ? this.toneMinContrast : this.toneMaxContrast).apply(dynamicScheme2).doubleValue() - doubleValue2) * Math.abs(dynamicScheme2.contrastLevel));
        }
        Function<DynamicScheme, DynamicColor> function = this.background;
        DynamicColor apply = function == null ? null : function.apply(dynamicScheme2);
        double d2 = 1.0d;
        if (apply != null) {
            Function<DynamicScheme, DynamicColor> function2 = apply.background;
            if (function2 == null || function2.apply(dynamicScheme2) == null) {
                z = false;
            }
            double ratioOfTones = Contrast.ratioOfTones(this.tone.apply(dynamicScheme2).doubleValue(), apply.tone.apply(dynamicScheme2).doubleValue());
            if (z2) {
                double ratioOfTones2 = Contrast.ratioOfTones(this.toneMinContrast.apply(dynamicScheme2).doubleValue(), apply.toneMinContrast.apply(dynamicScheme2).doubleValue());
                if (z) {
                    d2 = ratioOfTones2;
                }
                d = ratioOfTones;
            } else {
                double ratioOfTones3 = Contrast.ratioOfTones(this.toneMaxContrast.apply(dynamicScheme2).doubleValue(), apply.toneMaxContrast.apply(dynamicScheme2).doubleValue());
                if (z) {
                    d2 = Math.min(ratioOfTones3, ratioOfTones);
                }
                if (z) {
                    d = Math.max(ratioOfTones3, ratioOfTones);
                }
            }
            return calculateDynamicTone(dynamicScheme, this.tone, new DynamicColor$$ExternalSyntheticLambda18(dynamicScheme2), new DynamicColor$$ExternalSyntheticLambda1(doubleValue), new DynamicColor$$ExternalSyntheticLambda2(apply), this.toneDeltaConstraint, new DynamicColor$$ExternalSyntheticLambda3(d2), new DynamicColor$$ExternalSyntheticLambda4(d));
        }
        d = 21.0d;
        return calculateDynamicTone(dynamicScheme, this.tone, new DynamicColor$$ExternalSyntheticLambda18(dynamicScheme2), new DynamicColor$$ExternalSyntheticLambda1(doubleValue), new DynamicColor$$ExternalSyntheticLambda2(apply), this.toneDeltaConstraint, new DynamicColor$$ExternalSyntheticLambda3(d2), new DynamicColor$$ExternalSyntheticLambda4(d));
    }

    public static double toneMinContrastDefault(Function<DynamicScheme, Double> function, Function<DynamicScheme, DynamicColor> function2, DynamicScheme dynamicScheme, Function<DynamicScheme, ToneDeltaConstraint> function3) {
        return calculateDynamicTone(dynamicScheme, function, new DynamicColor$$ExternalSyntheticLambda13(dynamicScheme), new DynamicColor$$ExternalSyntheticLambda14(function, dynamicScheme, function2), function2, function3, (Function<Double, Double>) null, new DynamicColor$$ExternalSyntheticLambda15());
    }

    static /* synthetic */ Double lambda$toneMinContrastDefault$15(Function function, DynamicScheme dynamicScheme, Function function2, Double d, Double d2) {
        double doubleValue = ((Double) function.apply(dynamicScheme)).doubleValue();
        if (d.doubleValue() >= 7.0d) {
            doubleValue = contrastingTone(d2.doubleValue(), 4.5d);
        } else if (d.doubleValue() >= 3.0d) {
            doubleValue = contrastingTone(d2.doubleValue(), 3.0d);
        } else {
            if ((function2 == null || function2.apply(dynamicScheme) == null || ((DynamicColor) function2.apply(dynamicScheme)).background == null || ((DynamicColor) function2.apply(dynamicScheme)).background.apply(dynamicScheme) == null) ? false : true) {
                doubleValue = contrastingTone(d2.doubleValue(), d.doubleValue());
            }
        }
        return Double.valueOf(doubleValue);
    }

    public static double toneMaxContrastDefault(Function<DynamicScheme, Double> function, Function<DynamicScheme, DynamicColor> function2, DynamicScheme dynamicScheme, Function<DynamicScheme, ToneDeltaConstraint> function3) {
        return calculateDynamicTone(dynamicScheme, function, new DynamicColor$$ExternalSyntheticLambda8(dynamicScheme), new DynamicColor$$ExternalSyntheticLambda9(function2, dynamicScheme), function2, function3, (Function<Double, Double>) null, (Function<Double, Double>) null);
    }

    static /* synthetic */ Double lambda$toneMaxContrastDefault$18(Function function, DynamicScheme dynamicScheme, Double d, Double d2) {
        if ((function == null || function.apply(dynamicScheme) == null || ((DynamicColor) function.apply(dynamicScheme)).background == null || ((DynamicColor) function.apply(dynamicScheme)).background.apply(dynamicScheme) == null) ? false : true) {
            return Double.valueOf(contrastingTone(d2.doubleValue(), 7.0d));
        }
        return Double.valueOf(contrastingTone(d2.doubleValue(), Math.max(7.0d, d.doubleValue())));
    }

    public static double calculateDynamicTone(DynamicScheme dynamicScheme, Function<DynamicScheme, Double> function, Function<DynamicColor, Double> function2, BiFunction<Double, Double, Double> biFunction, Function<DynamicScheme, DynamicColor> function3, Function<DynamicScheme, ToneDeltaConstraint> function4, Function<Double, Double> function5, Function<Double, Double> function6) {
        DynamicColor dynamicColor;
        double d;
        double d2;
        DynamicScheme dynamicScheme2 = dynamicScheme;
        Function<DynamicScheme, DynamicColor> function7 = function3;
        Function<Double, Double> function8 = function5;
        Function<Double, Double> function9 = function6;
        double doubleValue = function.apply(dynamicScheme2).doubleValue();
        if (function7 == null) {
            dynamicColor = null;
        } else {
            dynamicColor = function7.apply(dynamicScheme2);
        }
        if (dynamicColor == null) {
            return doubleValue;
        }
        double ratioOfTones = Contrast.ratioOfTones(doubleValue, dynamicColor.tone.apply(dynamicScheme2).doubleValue());
        double doubleValue2 = function2.apply(dynamicColor).doubleValue();
        double doubleValue3 = biFunction.apply(Double.valueOf(ratioOfTones), Double.valueOf(doubleValue2)).doubleValue();
        double ratioOfTones2 = Contrast.ratioOfTones(doubleValue2, doubleValue3);
        double d3 = 1.0d;
        if (!(function8 == null || function8.apply(Double.valueOf(ratioOfTones)) == null)) {
            d3 = function8.apply(Double.valueOf(ratioOfTones)).doubleValue();
        }
        if (function9 == null || function9.apply(Double.valueOf(ratioOfTones)) == null) {
            d = 21.0d;
        } else {
            d = function9.apply(Double.valueOf(ratioOfTones)).doubleValue();
        }
        double clampDouble = MathUtils.clampDouble(d3, d, ratioOfTones2);
        if (clampDouble != ratioOfTones2) {
            doubleValue3 = contrastingTone(doubleValue2, clampDouble);
        }
        Function<DynamicScheme, DynamicColor> function10 = dynamicColor.background;
        if (function10 == null || function10.apply(dynamicScheme2) == null) {
            d2 = enableLightForeground(doubleValue3);
        } else {
            d2 = doubleValue3;
        }
        return ensureToneDelta(d2, doubleValue, dynamicScheme, function4, function2);
    }

    static double ensureToneDelta(double d, double d2, DynamicScheme dynamicScheme, Function<DynamicScheme, ToneDeltaConstraint> function, Function<DynamicColor, Double> function2) {
        ToneDeltaConstraint apply = function == null ? null : function.apply(dynamicScheme);
        if (apply == null) {
            return d;
        }
        double d3 = apply.delta;
        double doubleValue = function2.apply(apply.keepAway).doubleValue();
        double abs = Math.abs(d - doubleValue);
        if (abs >= d3) {
            return d;
        }
        int i = C06471.f177x2c744fd[apply.keepAwayPolarity.ordinal()];
        boolean z = true;
        if (i == 1) {
            return MathUtils.clampDouble(0.0d, 100.0d, doubleValue + d3);
        }
        if (i == 2) {
            return MathUtils.clampDouble(0.0d, 100.0d, doubleValue - d3);
        }
        if (i != 3) {
            return d;
        }
        boolean z2 = d2 > apply.keepAway.tone.apply(dynamicScheme).doubleValue();
        double abs2 = Math.abs(abs - d3);
        if (!z2 ? d >= abs2 : d + abs2 > 100.0d) {
            z = false;
        }
        return z ? d + abs2 : d - abs2;
    }

    /* renamed from: com.google.android.material.color.utilities.DynamicColor$1 */
    static /* synthetic */ class C06471 {

        /* renamed from: $SwitchMap$com$google$android$material$color$utilities$TonePolarity */
        static final /* synthetic */ int[] f177x2c744fd;

        /* JADX WARNING: Can't wrap try/catch for region: R(6:0|1|2|3|4|(3:5|6|8)) */
        /* JADX WARNING: Failed to process nested try/catch */
        /* JADX WARNING: Missing exception handler attribute for start block: B:3:0x0012 */
        /* JADX WARNING: Missing exception handler attribute for start block: B:5:0x001d */
        static {
            /*
                com.google.android.material.color.utilities.TonePolarity[] r0 = com.google.android.material.color.utilities.TonePolarity.values()
                int r0 = r0.length
                int[] r0 = new int[r0]
                f177x2c744fd = r0
                com.google.android.material.color.utilities.TonePolarity r1 = com.google.android.material.color.utilities.TonePolarity.DARKER     // Catch:{ NoSuchFieldError -> 0x0012 }
                int r1 = r1.ordinal()     // Catch:{ NoSuchFieldError -> 0x0012 }
                r2 = 1
                r0[r1] = r2     // Catch:{ NoSuchFieldError -> 0x0012 }
            L_0x0012:
                int[] r0 = f177x2c744fd     // Catch:{ NoSuchFieldError -> 0x001d }
                com.google.android.material.color.utilities.TonePolarity r1 = com.google.android.material.color.utilities.TonePolarity.LIGHTER     // Catch:{ NoSuchFieldError -> 0x001d }
                int r1 = r1.ordinal()     // Catch:{ NoSuchFieldError -> 0x001d }
                r2 = 2
                r0[r1] = r2     // Catch:{ NoSuchFieldError -> 0x001d }
            L_0x001d:
                int[] r0 = f177x2c744fd     // Catch:{ NoSuchFieldError -> 0x0028 }
                com.google.android.material.color.utilities.TonePolarity r1 = com.google.android.material.color.utilities.TonePolarity.NO_PREFERENCE     // Catch:{ NoSuchFieldError -> 0x0028 }
                int r1 = r1.ordinal()     // Catch:{ NoSuchFieldError -> 0x0028 }
                r2 = 3
                r0[r1] = r2     // Catch:{ NoSuchFieldError -> 0x0028 }
            L_0x0028:
                return
            */
            throw new UnsupportedOperationException("Method not decompiled: com.google.android.material.color.utilities.DynamicColor.C06471.<clinit>():void");
        }
    }

    public static double contrastingTone(double d, double d2) {
        double lighterUnsafe = Contrast.lighterUnsafe(d, d2);
        double darkerUnsafe = Contrast.darkerUnsafe(d, d2);
        double ratioOfTones = Contrast.ratioOfTones(lighterUnsafe, d);
        double ratioOfTones2 = Contrast.ratioOfTones(darkerUnsafe, d);
        if (!tonePrefersLightForeground(d)) {
            return (ratioOfTones2 >= d2 || ratioOfTones2 >= ratioOfTones) ? darkerUnsafe : lighterUnsafe;
        }
        return (ratioOfTones >= d2 || ratioOfTones >= ratioOfTones2 || ((Math.abs(ratioOfTones - ratioOfTones2) > 0.1d ? 1 : (Math.abs(ratioOfTones - ratioOfTones2) == 0.1d ? 0 : -1)) < 0 && (ratioOfTones > d2 ? 1 : (ratioOfTones == d2 ? 0 : -1)) < 0 && (ratioOfTones2 > d2 ? 1 : (ratioOfTones2 == d2 ? 0 : -1)) < 0)) ? lighterUnsafe : darkerUnsafe;
    }

    public static double enableLightForeground(double d) {
        if (!tonePrefersLightForeground(d) || toneAllowsLightForeground(d)) {
            return d;
        }
        return 49.0d;
    }

    public static boolean tonePrefersLightForeground(double d) {
        return Math.round(d) <= 60;
    }

    public static boolean toneAllowsLightForeground(double d) {
        return Math.round(d) <= 49;
    }
}
