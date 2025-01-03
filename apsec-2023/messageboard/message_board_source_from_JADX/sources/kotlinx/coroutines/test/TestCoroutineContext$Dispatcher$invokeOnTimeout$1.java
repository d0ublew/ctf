package kotlinx.coroutines.test;

import kotlin.Metadata;
import kotlinx.coroutines.DisposableHandle;

@Metadata(mo15831d1 = {"\u0000\u0011\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000*\u0001\u0000\b\n\u0018\u00002\u00020\u0001J\b\u0010\u0002\u001a\u00020\u0003H\u0016¨\u0006\u0004"}, mo15832d2 = {"kotlinx/coroutines/test/TestCoroutineContext$Dispatcher$invokeOnTimeout$1", "Lkotlinx/coroutines/DisposableHandle;", "dispose", "", "kotlinx-coroutines-core"}, mo15833k = 1, mo15834mv = {1, 6, 0}, mo15836xi = 48)
/* compiled from: TestCoroutineContext.kt */
public final class TestCoroutineContext$Dispatcher$invokeOnTimeout$1 implements DisposableHandle {
    final /* synthetic */ TimedRunnableObsolete $node;
    final /* synthetic */ TestCoroutineContext this$0;

    TestCoroutineContext$Dispatcher$invokeOnTimeout$1(TestCoroutineContext testCoroutineContext, TimedRunnableObsolete timedRunnableObsolete) {
        this.this$0 = testCoroutineContext;
        this.$node = timedRunnableObsolete;
    }

    public void dispose() {
        this.this$0.queue.remove(this.$node);
    }
}
