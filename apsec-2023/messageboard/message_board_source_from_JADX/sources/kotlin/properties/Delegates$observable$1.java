package kotlin.properties;

import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function3;
import kotlin.jvm.internal.Intrinsics;
import kotlin.reflect.KProperty;

@Metadata(mo15831d1 = {"\u0000\u0019\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004*\u0001\u0000\b\n\u0018\u00002\b\u0012\u0004\u0012\u00028\u00000\u0001J)\u0010\u0002\u001a\u00020\u00032\n\u0010\u0004\u001a\u0006\u0012\u0002\b\u00030\u00052\u0006\u0010\u0006\u001a\u00028\u00002\u0006\u0010\u0007\u001a\u00028\u0000H\u0014¢\u0006\u0002\u0010\b¨\u0006\t"}, mo15832d2 = {"kotlin/properties/Delegates$observable$1", "Lkotlin/properties/ObservableProperty;", "afterChange", "", "property", "Lkotlin/reflect/KProperty;", "oldValue", "newValue", "(Lkotlin/reflect/KProperty;Ljava/lang/Object;Ljava/lang/Object;)V", "kotlin-stdlib"}, mo15833k = 1, mo15834mv = {1, 7, 1}, mo15836xi = 176)
/* compiled from: Delegates.kt */
public final class Delegates$observable$1 extends ObservableProperty<T> {
    final /* synthetic */ Function3<KProperty<?>, T, T, Unit> $onChange;

    /* JADX INFO: super call moved to the top of the method (can break code semantics) */
    public Delegates$observable$1(T t, Function3<? super KProperty<?>, ? super T, ? super T, Unit> function3) {
        super(t);
        this.$onChange = function3;
    }

    /* access modifiers changed from: protected */
    public void afterChange(KProperty<?> kProperty, T t, T t2) {
        Intrinsics.checkNotNullParameter(kProperty, "property");
        this.$onChange.invoke(kProperty, t, t2);
    }
}
