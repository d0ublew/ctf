package kotlin;

import kotlin.jvm.functions.Function0;
import kotlin.jvm.internal.InlineMarker;
import kotlin.jvm.internal.Intrinsics;

@Metadata(mo15831d1 = {"\u0000\u0012\n\u0002\b\u0003\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\u001a:\u0010\u0000\u001a\u0002H\u0001\"\u0004\b\u0000\u0010\u00012\u0006\u0010\u0002\u001a\u00020\u00032\f\u0010\u0004\u001a\b\u0012\u0004\u0012\u0002H\u00010\u0005H\bø\u0001\u0000\u0002\n\n\b\b\u0001\u0012\u0002\u0010\u0002 \u0001¢\u0006\u0002\u0010\u0006\u0002\u0007\n\u0005\b20\u0001¨\u0006\u0007"}, mo15832d2 = {"synchronized", "R", "lock", "", "block", "Lkotlin/Function0;", "(Ljava/lang/Object;Lkotlin/jvm/functions/Function0;)Ljava/lang/Object;", "kotlin-stdlib"}, mo15833k = 5, mo15834mv = {1, 7, 1}, mo15836xi = 49, mo15837xs = "kotlin/StandardKt")
/* compiled from: Synchronized.kt */
class StandardKt__SynchronizedKt extends StandardKt__StandardKt {
    /* renamed from: synchronized  reason: not valid java name */
    private static final <R> R m154synchronized(Object obj, Function0<? extends R> function0) {
        R invoke;
        Intrinsics.checkNotNullParameter(obj, "lock");
        Intrinsics.checkNotNullParameter(function0, "block");
        synchronized (obj) {
            try {
                invoke = function0.invoke();
                InlineMarker.finallyStart(1);
            } catch (Throwable th) {
                InlineMarker.finallyStart(1);
                InlineMarker.finallyEnd(1);
                throw th;
            }
        }
        InlineMarker.finallyEnd(1);
        return invoke;
    }
}
