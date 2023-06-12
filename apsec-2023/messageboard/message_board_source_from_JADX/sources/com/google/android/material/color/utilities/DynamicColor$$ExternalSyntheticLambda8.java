package com.google.android.material.color.utilities;

import java.util.function.Function;

/* compiled from: D8$$SyntheticClass */
public final /* synthetic */ class DynamicColor$$ExternalSyntheticLambda8 implements Function {
    public final /* synthetic */ DynamicScheme f$0;

    public /* synthetic */ DynamicColor$$ExternalSyntheticLambda8(DynamicScheme dynamicScheme) {
        this.f$0 = dynamicScheme;
    }

    public final Object apply(Object obj) {
        return ((DynamicColor) obj).toneMaxContrast.apply(this.f$0);
    }
}
