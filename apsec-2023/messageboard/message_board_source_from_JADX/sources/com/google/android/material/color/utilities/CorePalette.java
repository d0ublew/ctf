package com.google.android.material.color.utilities;

public final class CorePalette {

    /* renamed from: a1 */
    public TonalPalette f172a1;

    /* renamed from: a2 */
    public TonalPalette f173a2;

    /* renamed from: a3 */
    public TonalPalette f174a3;
    public TonalPalette error;

    /* renamed from: n1 */
    public TonalPalette f175n1;

    /* renamed from: n2 */
    public TonalPalette f176n2;

    /* renamed from: of */
    public static CorePalette m55of(int i) {
        return new CorePalette(i, false);
    }

    public static CorePalette contentOf(int i) {
        return new CorePalette(i, true);
    }

    private CorePalette(int i, boolean z) {
        Hct fromInt = Hct.fromInt(i);
        double hue = fromInt.getHue();
        double chroma = fromInt.getChroma();
        if (z) {
            this.f172a1 = TonalPalette.fromHueAndChroma(hue, chroma);
            this.f173a2 = TonalPalette.fromHueAndChroma(hue, chroma / 3.0d);
            this.f174a3 = TonalPalette.fromHueAndChroma(60.0d + hue, chroma / 2.0d);
            this.f175n1 = TonalPalette.fromHueAndChroma(hue, Math.min(chroma / 12.0d, 4.0d));
            this.f176n2 = TonalPalette.fromHueAndChroma(hue, Math.min(chroma / 6.0d, 8.0d));
        } else {
            this.f172a1 = TonalPalette.fromHueAndChroma(hue, Math.max(48.0d, chroma));
            this.f173a2 = TonalPalette.fromHueAndChroma(hue, 16.0d);
            this.f174a3 = TonalPalette.fromHueAndChroma(60.0d + hue, 24.0d);
            this.f175n1 = TonalPalette.fromHueAndChroma(hue, 4.0d);
            this.f176n2 = TonalPalette.fromHueAndChroma(hue, 8.0d);
        }
        this.error = TonalPalette.fromHueAndChroma(25.0d, 84.0d);
    }
}
