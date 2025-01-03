package kotlin;

import kotlin.jvm.functions.Function0;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;

@Metadata(mo15831d1 = {"\u0000\u001c\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\u001a \u0010\u0000\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0001\"\u0004\b\u0000\u0010\u00022\f\u0010\u0003\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0004\u001a*\u0010\u0000\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0001\"\u0004\b\u0000\u0010\u00022\b\u0010\u0005\u001a\u0004\u0018\u00010\u00062\f\u0010\u0003\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0004\u001a(\u0010\u0000\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0001\"\u0004\b\u0000\u0010\u00022\u0006\u0010\u0007\u001a\u00020\b2\f\u0010\u0003\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0004¨\u0006\t"}, mo15832d2 = {"lazy", "Lkotlin/Lazy;", "T", "initializer", "Lkotlin/Function0;", "lock", "", "mode", "Lkotlin/LazyThreadSafetyMode;", "kotlin-stdlib"}, mo15833k = 5, mo15834mv = {1, 7, 1}, mo15836xi = 49, mo15837xs = "kotlin/LazyKt")
/* compiled from: LazyJVM.kt */
class LazyKt__LazyJVMKt {

    @Metadata(mo15833k = 3, mo15834mv = {1, 7, 1}, mo15836xi = 48)
    /* compiled from: LazyJVM.kt */
    public /* synthetic */ class WhenMappings {
        public static final /* synthetic */ int[] $EnumSwitchMapping$0;

        static {
            int[] iArr = new int[LazyThreadSafetyMode.values().length];
            iArr[LazyThreadSafetyMode.SYNCHRONIZED.ordinal()] = 1;
            iArr[LazyThreadSafetyMode.PUBLICATION.ordinal()] = 2;
            iArr[LazyThreadSafetyMode.NONE.ordinal()] = 3;
            $EnumSwitchMapping$0 = iArr;
        }
    }

    public static final <T> Lazy<T> lazy(Function0<? extends T> function0) {
        Intrinsics.checkNotNullParameter(function0, "initializer");
        return new SynchronizedLazyImpl<>(function0, (Object) null, 2, (DefaultConstructorMarker) null);
    }

    public static final <T> Lazy<T> lazy(LazyThreadSafetyMode lazyThreadSafetyMode, Function0<? extends T> function0) {
        Intrinsics.checkNotNullParameter(lazyThreadSafetyMode, "mode");
        Intrinsics.checkNotNullParameter(function0, "initializer");
        int i = WhenMappings.$EnumSwitchMapping$0[lazyThreadSafetyMode.ordinal()];
        if (i == 1) {
            return new SynchronizedLazyImpl<>(function0, (Object) null, 2, (DefaultConstructorMarker) null);
        }
        if (i == 2) {
            return new SafePublicationLazyImpl<>(function0);
        }
        if (i == 3) {
            return new UnsafeLazyImpl<>(function0);
        }
        throw new NoWhenBranchMatchedException();
    }

    public static final <T> Lazy<T> lazy(Object obj, Function0<? extends T> function0) {
        Intrinsics.checkNotNullParameter(function0, "initializer");
        return new SynchronizedLazyImpl<>(function0, obj);
    }
}
