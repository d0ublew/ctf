package kotlinx.coroutines;

import kotlin.Metadata;

@Metadata(mo15831d1 = {"\u0000\u0012\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\b\u0000\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004R\u0014\u0010\u0002\u001a\u00020\u0003X\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u0005\u0010\u0006¨\u0006\u0007"}, mo15832d2 = {"Lkotlinx/coroutines/BlockingEventLoop;", "Lkotlinx/coroutines/EventLoopImplBase;", "thread", "Ljava/lang/Thread;", "(Ljava/lang/Thread;)V", "getThread", "()Ljava/lang/Thread;", "kotlinx-coroutines-core"}, mo15833k = 1, mo15834mv = {1, 6, 0}, mo15836xi = 48)
/* compiled from: EventLoop.kt */
public final class BlockingEventLoop extends EventLoopImplBase {
    private final Thread thread;

    /* access modifiers changed from: protected */
    public Thread getThread() {
        return this.thread;
    }

    public BlockingEventLoop(Thread thread2) {
        this.thread = thread2;
    }
}
