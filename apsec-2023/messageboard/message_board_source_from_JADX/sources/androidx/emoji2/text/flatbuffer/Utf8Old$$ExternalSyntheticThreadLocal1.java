package androidx.emoji2.text.flatbuffer;

import com.android.tools.r8.annotations.SynthesizedClassV2;
import java.util.function.Supplier;

@SynthesizedClassV2(kind = 21, versionHash = "7a5b85d3ee2e0991ca3502602e9389a98f55c0576b887125894a7ec03823f8d3")
/* compiled from: D8$$SyntheticClass */
public final /* synthetic */ class Utf8Old$$ExternalSyntheticThreadLocal1 extends ThreadLocal {
    public final /* synthetic */ Supplier initialValueSupplier;

    public /* synthetic */ Utf8Old$$ExternalSyntheticThreadLocal1(Supplier supplier) {
        this.initialValueSupplier = supplier;
    }

    /* access modifiers changed from: protected */
    public /* synthetic */ Object initialValue() {
        return this.initialValueSupplier.get();
    }
}
