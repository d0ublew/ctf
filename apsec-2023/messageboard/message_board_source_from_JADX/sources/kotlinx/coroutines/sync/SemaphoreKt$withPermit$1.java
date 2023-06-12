package kotlinx.coroutines.sync;

import kotlin.Metadata;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.coroutines.jvm.internal.DebugMetadata;
import kotlin.jvm.functions.Function0;

@Metadata(mo15833k = 3, mo15834mv = {1, 6, 0}, mo15836xi = 176)
@DebugMetadata(mo16546c = "kotlinx.coroutines.sync.SemaphoreKt", mo16547f = "Semaphore.kt", mo16548i = {0, 0}, mo16549l = {85}, mo16550m = "withPermit", mo16551n = {"$this$withPermit", "action"}, mo16552s = {"L$0", "L$1"})
/* compiled from: Semaphore.kt */
final class SemaphoreKt$withPermit$1<T> extends ContinuationImpl {
    Object L$0;
    Object L$1;
    int label;
    /* synthetic */ Object result;

    SemaphoreKt$withPermit$1(Continuation<? super SemaphoreKt$withPermit$1> continuation) {
        super(continuation);
    }

    public final Object invokeSuspend(Object obj) {
        this.result = obj;
        this.label |= Integer.MIN_VALUE;
        return SemaphoreKt.withPermit((Semaphore) null, (Function0) null, this);
    }
}
