package kotlinx.coroutines;

import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.DebugMetadata;
import kotlin.coroutines.jvm.internal.SuspendLambda;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function2;

@Metadata(mo15831d1 = {"\u0000\b\n\u0002\b\u0002\n\u0002\u0018\u0002\u0010\u0000\u001a\u0002H\u0001\"\u0004\b\u0000\u0010\u0001*\u00020\u0002H@"}, mo15832d2 = {"<anonymous>", "T", "Lkotlinx/coroutines/CoroutineScope;"}, mo15833k = 3, mo15834mv = {1, 6, 0}, mo15836xi = 48)
@DebugMetadata(mo16546c = "kotlinx.coroutines.InterruptibleKt$runInterruptible$2", mo16547f = "Interruptible.kt", mo16548i = {}, mo16549l = {}, mo16550m = "invokeSuspend", mo16551n = {}, mo16552s = {})
/* compiled from: Interruptible.kt */
final class InterruptibleKt$runInterruptible$2 extends SuspendLambda implements Function2<CoroutineScope, Continuation<? super T>, Object> {
    final /* synthetic */ Function0<T> $block;
    private /* synthetic */ Object L$0;
    int label;

    /* JADX INFO: super call moved to the top of the method (can break code semantics) */
    InterruptibleKt$runInterruptible$2(Function0<? extends T> function0, Continuation<? super InterruptibleKt$runInterruptible$2> continuation) {
        super(2, continuation);
        this.$block = function0;
    }

    public final Continuation<Unit> create(Object obj, Continuation<?> continuation) {
        InterruptibleKt$runInterruptible$2 interruptibleKt$runInterruptible$2 = new InterruptibleKt$runInterruptible$2(this.$block, continuation);
        interruptibleKt$runInterruptible$2.L$0 = obj;
        return interruptibleKt$runInterruptible$2;
    }

    public final Object invoke(CoroutineScope coroutineScope, Continuation<? super T> continuation) {
        return ((InterruptibleKt$runInterruptible$2) create(coroutineScope, continuation)).invokeSuspend(Unit.INSTANCE);
    }

    public final Object invokeSuspend(Object obj) {
        IntrinsicsKt.getCOROUTINE_SUSPENDED();
        if (this.label == 0) {
            ResultKt.throwOnFailure(obj);
            return InterruptibleKt.runInterruptibleInExpectedContext(((CoroutineScope) this.L$0).getCoroutineContext(), this.$block);
        }
        throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
    }
}
