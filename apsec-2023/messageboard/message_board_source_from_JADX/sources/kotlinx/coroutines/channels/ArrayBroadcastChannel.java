package kotlinx.coroutines.channels;

import java.util.List;
import java.util.concurrent.CancellationException;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function1;
import kotlin.ranges.RangesKt;
import kotlinx.coroutines.CancellableContinuationImplKt;
import kotlinx.coroutines.DebugKt;
import kotlinx.coroutines.internal.ConcurrentKt;
import kotlinx.coroutines.internal.LockFreeLinkedListNode;
import kotlinx.coroutines.internal.Symbol;
import kotlinx.coroutines.selects.SelectInstance;
import kotlinx.coroutines.selects.SelectKt;

@Metadata(mo15831d1 = {"\u0000\u0001\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\b\n\u0002\b\u0003\n\u0002\u0010\u0003\n\u0000\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u0002\n\u0002\b\u0005\n\u0002\u0010\t\n\u0002\b\u0006\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010\u0011\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0010\n\u0002\u0010!\n\u0002\u0018\u0002\n\u0002\b\b\n\u0002\u0018\u0002\n\u0002\u0018\u0002\b\u0000\u0018\u0000*\u0004\b\u0000\u0010\u00012\b\u0012\u0004\u0012\u00028\u00000L2\b\u0012\u0004\u0012\u00028\u00000M:\u0001JB\u000f\u0012\u0006\u0010\u0003\u001a\u00020\u0002¢\u0006\u0004\b\u0004\u0010\u0005J\u0019\u0010\t\u001a\u00020\b2\b\u0010\u0007\u001a\u0004\u0018\u00010\u0006H\u0017¢\u0006\u0004\b\t\u0010\nJ\u001f\u0010\t\u001a\u00020\r2\u000e\u0010\u0007\u001a\n\u0018\u00010\u000bj\u0004\u0018\u0001`\fH\u0016¢\u0006\u0004\b\t\u0010\u000eJ\u0019\u0010\u000f\u001a\u00020\b2\b\u0010\u0007\u001a\u0004\u0018\u00010\u0006H\u0002¢\u0006\u0004\b\u000f\u0010\nJ\u000f\u0010\u0010\u001a\u00020\rH\u0002¢\u0006\u0004\b\u0010\u0010\u0011J\u0019\u0010\u0012\u001a\u00020\b2\b\u0010\u0007\u001a\u0004\u0018\u00010\u0006H\u0016¢\u0006\u0004\b\u0012\u0010\nJ\u000f\u0010\u0014\u001a\u00020\u0013H\u0002¢\u0006\u0004\b\u0014\u0010\u0015J\u0017\u0010\u0017\u001a\u00028\u00002\u0006\u0010\u0016\u001a\u00020\u0013H\u0002¢\u0006\u0004\b\u0017\u0010\u0018J\u0017\u0010\u001b\u001a\u00020\u001a2\u0006\u0010\u0019\u001a\u00028\u0000H\u0014¢\u0006\u0004\b\u001b\u0010\u001cJ#\u0010\u001f\u001a\u00020\u001a2\u0006\u0010\u0019\u001a\u00028\u00002\n\u0010\u001e\u001a\u0006\u0012\u0002\b\u00030\u001dH\u0014¢\u0006\u0004\b\u001f\u0010 J\u0015\u0010\"\u001a\b\u0012\u0004\u0012\u00028\u00000!H\u0016¢\u0006\u0004\b\"\u0010#J4\u0010'\u001a\u00020\r2\u0010\b\u0002\u0010%\u001a\n\u0012\u0004\u0012\u00028\u0000\u0018\u00010$2\u0010\b\u0002\u0010&\u001a\n\u0012\u0004\u0012\u00028\u0000\u0018\u00010$H\u0010¢\u0006\u0004\b'\u0010(R\u001c\u0010*\u001a\n\u0012\u0006\u0012\u0004\u0018\u00010\u001a0)8\u0002X\u0004¢\u0006\u0006\n\u0004\b*\u0010+R\u0014\u0010/\u001a\u00020,8TX\u0004¢\u0006\u0006\u001a\u0004\b-\u0010.R\u0018\u00102\u001a\u000600j\u0002`18\u0002X\u0004¢\u0006\u0006\n\u0004\b2\u00103R\u0017\u0010\u0003\u001a\u00020\u00028\u0006¢\u0006\f\n\u0004\b\u0003\u00104\u001a\u0004\b5\u00106R$\u0010;\u001a\u00020\u00132\u0006\u00107\u001a\u00020\u00138B@BX\u000e¢\u0006\f\u001a\u0004\b8\u0010\u0015\"\u0004\b9\u0010:R\u0014\u0010<\u001a\u00020\b8TX\u0004¢\u0006\u0006\u001a\u0004\b<\u0010=R\u0014\u0010>\u001a\u00020\b8TX\u0004¢\u0006\u0006\u001a\u0004\b>\u0010=R$\u0010A\u001a\u00020\u00022\u0006\u00107\u001a\u00020\u00028B@BX\u000e¢\u0006\f\u001a\u0004\b?\u00106\"\u0004\b@\u0010\u0005R6\u0010D\u001a\u001e\u0012\n\u0012\b\u0012\u0004\u0012\u00028\u00000$0Bj\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00028\u00000$`C8\u0002X\u0004¢\u0006\f\n\u0004\bD\u0010E\u0012\u0004\bF\u0010\u0011R$\u0010I\u001a\u00020\u00132\u0006\u00107\u001a\u00020\u00138B@BX\u000e¢\u0006\f\u001a\u0004\bG\u0010\u0015\"\u0004\bH\u0010:¨\u0006K"}, mo15832d2 = {"Lkotlinx/coroutines/channels/ArrayBroadcastChannel;", "E", "", "capacity", "<init>", "(I)V", "", "cause", "", "cancel", "(Ljava/lang/Throwable;)Z", "Ljava/util/concurrent/CancellationException;", "Lkotlinx/coroutines/CancellationException;", "", "(Ljava/util/concurrent/CancellationException;)V", "cancelInternal", "checkSubOffers", "()V", "close", "", "computeMinHead", "()J", "index", "elementAt", "(J)Ljava/lang/Object;", "element", "", "offerInternal", "(Ljava/lang/Object;)Ljava/lang/Object;", "Lkotlinx/coroutines/selects/SelectInstance;", "select", "offerSelectInternal", "(Ljava/lang/Object;Lkotlinx/coroutines/selects/SelectInstance;)Ljava/lang/Object;", "Lkotlinx/coroutines/channels/ReceiveChannel;", "openSubscription", "()Lkotlinx/coroutines/channels/ReceiveChannel;", "Lkotlinx/coroutines/channels/ArrayBroadcastChannel$Subscriber;", "addSub", "removeSub", "updateHead", "(Lkotlinx/coroutines/channels/ArrayBroadcastChannel$Subscriber;Lkotlinx/coroutines/channels/ArrayBroadcastChannel$Subscriber;)V", "", "buffer", "[Ljava/lang/Object;", "", "getBufferDebugString", "()Ljava/lang/String;", "bufferDebugString", "Ljava/util/concurrent/locks/ReentrantLock;", "Lkotlinx/coroutines/internal/ReentrantLock;", "bufferLock", "Ljava/util/concurrent/locks/ReentrantLock;", "I", "getCapacity", "()I", "value", "getHead", "setHead", "(J)V", "head", "isBufferAlwaysFull", "()Z", "isBufferFull", "getSize", "setSize", "size", "", "Lkotlinx/coroutines/internal/SubscribersList;", "subscribers", "Ljava/util/List;", "getSubscribers$annotations", "getTail", "setTail", "tail", "Subscriber", "kotlinx-coroutines-core", "Lkotlinx/coroutines/channels/AbstractSendChannel;", "Lkotlinx/coroutines/channels/BroadcastChannel;"}, mo15833k = 1, mo15834mv = {1, 6, 0}, mo15836xi = 48)
/* compiled from: ArrayBroadcastChannel.kt */
public final class ArrayBroadcastChannel<E> extends AbstractSendChannel<E> implements BroadcastChannel<E> {
    private volatile /* synthetic */ long _head;
    private volatile /* synthetic */ int _size;
    private volatile /* synthetic */ long _tail;
    private final Object[] buffer;
    private final ReentrantLock bufferLock;
    private final int capacity;
    private final List<Subscriber<E>> subscribers;

    private static /* synthetic */ void getSubscribers$annotations() {
    }

    /* access modifiers changed from: protected */
    public boolean isBufferAlwaysFull() {
        return false;
    }

    public final int getCapacity() {
        return this.capacity;
    }

    public ArrayBroadcastChannel(int i) {
        super((Function1) null);
        this.capacity = i;
        if (i < 1 ? false : true) {
            this.bufferLock = new ReentrantLock();
            this.buffer = new Object[i];
            this._head = 0;
            this._tail = 0;
            this._size = 0;
            this.subscribers = ConcurrentKt.subscriberList();
            return;
        }
        throw new IllegalArgumentException(("ArrayBroadcastChannel capacity must be at least 1, but " + getCapacity() + " was specified").toString());
    }

    private final long getHead() {
        return this._head;
    }

    private final void setHead(long j) {
        this._head = j;
    }

    /* access modifiers changed from: private */
    public final long getTail() {
        return this._tail;
    }

    private final void setTail(long j) {
        this._tail = j;
    }

    private final int getSize() {
        return this._size;
    }

    private final void setSize(int i) {
        this._size = i;
    }

    /* access modifiers changed from: protected */
    public boolean isBufferFull() {
        return getSize() >= this.capacity;
    }

    public ReceiveChannel<E> openSubscription() {
        Subscriber subscriber = new Subscriber(this);
        updateHead$default(this, subscriber, (Subscriber) null, 2, (Object) null);
        return subscriber;
    }

    public boolean close(Throwable th) {
        if (!super.close(th)) {
            return false;
        }
        checkSubOffers();
        return true;
    }

    public void cancel(CancellationException cancellationException) {
        cancel(cancellationException);
    }

    /* access modifiers changed from: private */
    /* renamed from: cancelInternal */
    public final boolean cancel(Throwable th) {
        boolean close = close(th);
        for (Subscriber<E> cancelInternal$kotlinx_coroutines_core : this.subscribers) {
            cancelInternal$kotlinx_coroutines_core.cancel(th);
        }
        return close;
    }

    /* access modifiers changed from: protected */
    public Object offerInternal(E e) {
        Lock lock = this.bufferLock;
        lock.lock();
        try {
            Closed<?> closedForSend = getClosedForSend();
            if (closedForSend == null) {
                int size = getSize();
                if (size >= getCapacity()) {
                    return AbstractChannelKt.OFFER_FAILED;
                }
                long tail = getTail();
                this.buffer[(int) (tail % ((long) getCapacity()))] = e;
                setSize(size + 1);
                setTail(tail + 1);
                Unit unit = Unit.INSTANCE;
                lock.unlock();
                checkSubOffers();
                return AbstractChannelKt.OFFER_SUCCESS;
            }
            lock.unlock();
            return closedForSend;
        } finally {
            lock.unlock();
        }
    }

    /* access modifiers changed from: protected */
    public Object offerSelectInternal(E e, SelectInstance<?> selectInstance) {
        Lock lock = this.bufferLock;
        lock.lock();
        try {
            Closed<?> closedForSend = getClosedForSend();
            if (closedForSend == null) {
                int size = getSize();
                if (size >= getCapacity()) {
                    return AbstractChannelKt.OFFER_FAILED;
                }
                if (!selectInstance.trySelect()) {
                    Object already_selected = SelectKt.getALREADY_SELECTED();
                    lock.unlock();
                    return already_selected;
                }
                long tail = getTail();
                this.buffer[(int) (tail % ((long) getCapacity()))] = e;
                setSize(size + 1);
                setTail(tail + 1);
                Unit unit = Unit.INSTANCE;
                lock.unlock();
                checkSubOffers();
                return AbstractChannelKt.OFFER_SUCCESS;
            }
            lock.unlock();
            return closedForSend;
        } finally {
            lock.unlock();
        }
    }

    private final void checkSubOffers() {
        boolean z;
        boolean z2 = false;
        loop0:
        while (true) {
            z = z2;
            for (Subscriber<E> checkOffer : this.subscribers) {
                if (checkOffer.checkOffer()) {
                    z2 = true;
                } else {
                    z = true;
                }
            }
            break loop0;
        }
        if (z2 || !z) {
            updateHead$default(this, (Subscriber) null, (Subscriber) null, 3, (Object) null);
        }
    }

    static /* synthetic */ void updateHead$default(ArrayBroadcastChannel arrayBroadcastChannel, Subscriber subscriber, Subscriber subscriber2, int i, Object obj) {
        if ((i & 1) != 0) {
            subscriber = null;
        }
        if ((i & 2) != 0) {
            subscriber2 = null;
        }
        arrayBroadcastChannel.updateHead(subscriber, subscriber2);
    }

    private final void updateHead(Subscriber<E> subscriber, Subscriber<E> subscriber2) {
        Send takeFirstSendOrPeekClosed;
        Symbol tryResumeSend;
        while (true) {
            Lock lock = this.bufferLock;
            lock.lock();
            if (subscriber != null) {
                try {
                    subscriber.setSubHead(getTail());
                    boolean isEmpty = this.subscribers.isEmpty();
                    this.subscribers.add(subscriber);
                    if (!isEmpty) {
                        return;
                    }
                } finally {
                    lock.unlock();
                }
            }
            if (subscriber2 != null) {
                this.subscribers.remove(subscriber2);
                if (getHead() != subscriber2.getSubHead()) {
                    lock.unlock();
                    return;
                }
            }
            long computeMinHead = computeMinHead();
            long tail = getTail();
            long head = getHead();
            long coerceAtMost = RangesKt.coerceAtMost(computeMinHead, tail);
            if (coerceAtMost <= head) {
                lock.unlock();
                return;
            }
            int size = getSize();
            while (head < coerceAtMost) {
                this.buffer[(int) (head % ((long) getCapacity()))] = null;
                boolean z = false;
                boolean z2 = size >= getCapacity();
                head++;
                setHead(head);
                size--;
                setSize(size);
                if (z2) {
                    do {
                        takeFirstSendOrPeekClosed = takeFirstSendOrPeekClosed();
                        if (takeFirstSendOrPeekClosed != null) {
                            if (!(takeFirstSendOrPeekClosed instanceof Closed)) {
                                tryResumeSend = takeFirstSendOrPeekClosed.tryResumeSend((LockFreeLinkedListNode.PrepareOp) null);
                            }
                        }
                    } while (tryResumeSend == null);
                    if (DebugKt.getASSERTIONS_ENABLED()) {
                        if (tryResumeSend == CancellableContinuationImplKt.RESUME_TOKEN) {
                            z = true;
                        }
                        if (!z) {
                            throw new AssertionError();
                        }
                    }
                    this.buffer[(int) (tail % ((long) getCapacity()))] = takeFirstSendOrPeekClosed.getPollResult();
                    setSize(size + 1);
                    setTail(tail + 1);
                    Unit unit = Unit.INSTANCE;
                    lock.unlock();
                    takeFirstSendOrPeekClosed.completeResumeSend();
                    checkSubOffers();
                    subscriber = null;
                    subscriber2 = null;
                }
            }
            lock.unlock();
            return;
        }
    }

    private final long computeMinHead() {
        long j = Long.MAX_VALUE;
        for (Subscriber<E> subHead : this.subscribers) {
            j = RangesKt.coerceAtMost(j, subHead.getSubHead());
        }
        return j;
    }

    /* access modifiers changed from: private */
    public final E elementAt(long j) {
        return this.buffer[(int) (j % ((long) this.capacity))];
    }

    @Metadata(mo15831d1 = {"\u0000J\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\u0003\n\u0002\b\u0004\n\u0002\u0010\u0000\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\b\n\u0002\u0010\t\n\u0002\b\u0006\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\u0018\u0002\b\u0002\u0018\u0000*\u0004\b\u0001\u0010\u00012\b\u0012\u0004\u0012\u00028\u00010'2\b\u0012\u0004\u0012\u00028\u00010(B\u0015\u0012\f\u0010\u0003\u001a\b\u0012\u0004\u0012\u00028\u00010\u0002¢\u0006\u0004\b\u0004\u0010\u0005J\r\u0010\u0007\u001a\u00020\u0006¢\u0006\u0004\b\u0007\u0010\bJ\u0019\u0010\u000b\u001a\u00020\u00062\b\u0010\n\u001a\u0004\u0018\u00010\tH\u0016¢\u0006\u0004\b\u000b\u0010\fJ\u000f\u0010\r\u001a\u00020\u0006H\u0002¢\u0006\u0004\b\r\u0010\bJ\u0011\u0010\u000f\u001a\u0004\u0018\u00010\u000eH\u0002¢\u0006\u0004\b\u000f\u0010\u0010J\u0011\u0010\u0011\u001a\u0004\u0018\u00010\u000eH\u0014¢\u0006\u0004\b\u0011\u0010\u0010J\u001d\u0010\u0014\u001a\u0004\u0018\u00010\u000e2\n\u0010\u0013\u001a\u0006\u0012\u0002\b\u00030\u0012H\u0014¢\u0006\u0004\b\u0014\u0010\u0015R\u001a\u0010\u0003\u001a\b\u0012\u0004\u0012\u00028\u00010\u00028\u0002X\u0004¢\u0006\u0006\n\u0004\b\u0003\u0010\u0016R\u0014\u0010\u0017\u001a\u00020\u00068TX\u0004¢\u0006\u0006\u001a\u0004\b\u0017\u0010\bR\u0014\u0010\u0018\u001a\u00020\u00068TX\u0004¢\u0006\u0006\u001a\u0004\b\u0018\u0010\bR\u0014\u0010\u0019\u001a\u00020\u00068TX\u0004¢\u0006\u0006\u001a\u0004\b\u0019\u0010\bR\u0014\u0010\u001a\u001a\u00020\u00068TX\u0004¢\u0006\u0006\u001a\u0004\b\u001a\u0010\bR$\u0010!\u001a\u00020\u001b2\u0006\u0010\u001c\u001a\u00020\u001b8F@FX\u000e¢\u0006\f\u001a\u0004\b\u001d\u0010\u001e\"\u0004\b\u001f\u0010 R\u0018\u0010$\u001a\u00060\"j\u0002`#8\u0002X\u0004¢\u0006\u0006\n\u0004\b$\u0010%¨\u0006&"}, mo15832d2 = {"Lkotlinx/coroutines/channels/ArrayBroadcastChannel$Subscriber;", "E", "Lkotlinx/coroutines/channels/ArrayBroadcastChannel;", "broadcastChannel", "<init>", "(Lkotlinx/coroutines/channels/ArrayBroadcastChannel;)V", "", "checkOffer", "()Z", "", "cause", "close", "(Ljava/lang/Throwable;)Z", "needsToCheckOfferWithoutLock", "", "peekUnderLock", "()Ljava/lang/Object;", "pollInternal", "Lkotlinx/coroutines/selects/SelectInstance;", "select", "pollSelectInternal", "(Lkotlinx/coroutines/selects/SelectInstance;)Ljava/lang/Object;", "Lkotlinx/coroutines/channels/ArrayBroadcastChannel;", "isBufferAlwaysEmpty", "isBufferAlwaysFull", "isBufferEmpty", "isBufferFull", "", "value", "getSubHead", "()J", "setSubHead", "(J)V", "subHead", "Ljava/util/concurrent/locks/ReentrantLock;", "Lkotlinx/coroutines/internal/ReentrantLock;", "subLock", "Ljava/util/concurrent/locks/ReentrantLock;", "kotlinx-coroutines-core", "Lkotlinx/coroutines/channels/AbstractChannel;", "Lkotlinx/coroutines/channels/ReceiveChannel;"}, mo15833k = 1, mo15834mv = {1, 6, 0}, mo15836xi = 48)
    /* compiled from: ArrayBroadcastChannel.kt */
    private static final class Subscriber<E> extends AbstractChannel<E> implements ReceiveChannel<E> {
        private volatile /* synthetic */ long _subHead = 0;
        private final ArrayBroadcastChannel<E> broadcastChannel;
        private final ReentrantLock subLock = new ReentrantLock();

        /* access modifiers changed from: protected */
        public boolean isBufferAlwaysEmpty() {
            return false;
        }

        public Subscriber(ArrayBroadcastChannel<E> arrayBroadcastChannel) {
            super((Function1) null);
            this.broadcastChannel = arrayBroadcastChannel;
        }

        public final long getSubHead() {
            return this._subHead;
        }

        public final void setSubHead(long j) {
            this._subHead = j;
        }

        /* access modifiers changed from: protected */
        public boolean isBufferEmpty() {
            return getSubHead() >= this.broadcastChannel.getTail();
        }

        /* access modifiers changed from: protected */
        public boolean isBufferAlwaysFull() {
            throw new IllegalStateException("Should not be used".toString());
        }

        /* access modifiers changed from: protected */
        public boolean isBufferFull() {
            throw new IllegalStateException("Should not be used".toString());
        }

        public boolean close(Throwable th) {
            boolean close = super.close(th);
            if (close) {
                ArrayBroadcastChannel.updateHead$default(this.broadcastChannel, (Subscriber) null, this, 1, (Object) null);
                Lock lock = this.subLock;
                lock.lock();
                try {
                    setSubHead(this.broadcastChannel.getTail());
                    Unit unit = Unit.INSTANCE;
                } finally {
                    lock.unlock();
                }
            }
            return close;
        }

        public final boolean checkOffer() {
            Closed closed;
            boolean z = false;
            while (true) {
                closed = null;
                if (!needsToCheckOfferWithoutLock() || !this.subLock.tryLock()) {
                    break;
                }
                try {
                    Object peekUnderLock = peekUnderLock();
                    if (peekUnderLock != AbstractChannelKt.POLL_FAILED) {
                        if (peekUnderLock instanceof Closed) {
                            closed = (Closed) peekUnderLock;
                            break;
                        }
                        ReceiveOrClosed takeFirstReceiveOrPeekClosed = takeFirstReceiveOrPeekClosed();
                        if (takeFirstReceiveOrPeekClosed == null) {
                            break;
                        } else if (takeFirstReceiveOrPeekClosed instanceof Closed) {
                            break;
                        } else {
                            Symbol tryResumeReceive = takeFirstReceiveOrPeekClosed.tryResumeReceive(peekUnderLock, (LockFreeLinkedListNode.PrepareOp) null);
                            if (tryResumeReceive != null) {
                                if (DebugKt.getASSERTIONS_ENABLED()) {
                                    if (!(tryResumeReceive == CancellableContinuationImplKt.RESUME_TOKEN)) {
                                        throw new AssertionError();
                                    }
                                }
                                setSubHead(getSubHead() + 1);
                                this.subLock.unlock();
                                takeFirstReceiveOrPeekClosed.completeResumeReceive(peekUnderLock);
                                z = true;
                            }
                        }
                    }
                } finally {
                    this.subLock.unlock();
                }
            }
            this.subLock.unlock();
            if (closed != null) {
                close(closed.closeCause);
            }
            return z;
        }

        /* JADX INFO: finally extract failed */
        /* access modifiers changed from: protected */
        /* JADX WARNING: Removed duplicated region for block: B:12:0x002a  */
        /* JADX WARNING: Removed duplicated region for block: B:13:0x002e  */
        /* JADX WARNING: Removed duplicated region for block: B:15:0x0032  */
        /* JADX WARNING: Removed duplicated region for block: B:18:0x003e  */
        /* JADX WARNING: Removed duplicated region for block: B:20:0x0041  */
        /* Code decompiled incorrectly, please refer to instructions dump. */
        public java.lang.Object pollInternal() {
            /*
                r8 = this;
                java.util.concurrent.locks.ReentrantLock r0 = r8.subLock
                java.util.concurrent.locks.Lock r0 = (java.util.concurrent.locks.Lock) r0
                r0.lock()
                java.lang.Object r1 = r8.peekUnderLock()     // Catch:{ all -> 0x0048 }
                boolean r2 = r1 instanceof kotlinx.coroutines.channels.Closed     // Catch:{ all -> 0x0048 }
                r3 = 1
                if (r2 == 0) goto L_0x0011
                goto L_0x0015
            L_0x0011:
                kotlinx.coroutines.internal.Symbol r2 = kotlinx.coroutines.channels.AbstractChannelKt.POLL_FAILED     // Catch:{ all -> 0x0048 }
                if (r1 != r2) goto L_0x0017
            L_0x0015:
                r2 = 0
                goto L_0x0022
            L_0x0017:
                long r4 = r8.getSubHead()     // Catch:{ all -> 0x0048 }
                r6 = 1
                long r4 = r4 + r6
                r8.setSubHead(r4)     // Catch:{ all -> 0x0048 }
                r2 = r3
            L_0x0022:
                r0.unlock()
                boolean r0 = r1 instanceof kotlinx.coroutines.channels.Closed
                r4 = 0
                if (r0 == 0) goto L_0x002e
                r0 = r1
                kotlinx.coroutines.channels.Closed r0 = (kotlinx.coroutines.channels.Closed) r0
                goto L_0x002f
            L_0x002e:
                r0 = r4
            L_0x002f:
                if (r0 != 0) goto L_0x0032
                goto L_0x0037
            L_0x0032:
                java.lang.Throwable r0 = r0.closeCause
                r8.close(r0)
            L_0x0037:
                boolean r0 = r8.checkOffer()
                if (r0 == 0) goto L_0x003e
                goto L_0x003f
            L_0x003e:
                r3 = r2
            L_0x003f:
                if (r3 == 0) goto L_0x0047
                kotlinx.coroutines.channels.ArrayBroadcastChannel<E> r0 = r8.broadcastChannel
                r2 = 3
                kotlinx.coroutines.channels.ArrayBroadcastChannel.updateHead$default(r0, r4, r4, r2, r4)
            L_0x0047:
                return r1
            L_0x0048:
                r1 = move-exception
                r0.unlock()
                throw r1
            */
            throw new UnsupportedOperationException("Method not decompiled: kotlinx.coroutines.channels.ArrayBroadcastChannel.Subscriber.pollInternal():java.lang.Object");
        }

        /* JADX INFO: finally extract failed */
        /* access modifiers changed from: protected */
        public Object pollSelectInternal(SelectInstance<?> selectInstance) {
            Lock lock = this.subLock;
            lock.lock();
            try {
                Object peekUnderLock = peekUnderLock();
                boolean z = true;
                boolean z2 = false;
                if (!(peekUnderLock instanceof Closed)) {
                    if (peekUnderLock != AbstractChannelKt.POLL_FAILED) {
                        if (!selectInstance.trySelect()) {
                            peekUnderLock = SelectKt.getALREADY_SELECTED();
                        } else {
                            setSubHead(getSubHead() + 1);
                            z2 = true;
                        }
                    }
                }
                lock.unlock();
                Closed closed = peekUnderLock instanceof Closed ? (Closed) peekUnderLock : null;
                if (closed != null) {
                    close(closed.closeCause);
                }
                if (!checkOffer()) {
                    z = z2;
                }
                if (z) {
                    ArrayBroadcastChannel.updateHead$default(this.broadcastChannel, (Subscriber) null, (Subscriber) null, 3, (Object) null);
                }
                return peekUnderLock;
            } catch (Throwable th) {
                lock.unlock();
                throw th;
            }
        }

        private final boolean needsToCheckOfferWithoutLock() {
            if (getClosedForReceive() != null) {
                return false;
            }
            if (!isBufferEmpty() || this.broadcastChannel.getClosedForReceive() != null) {
                return true;
            }
            return false;
        }

        private final Object peekUnderLock() {
            long subHead = getSubHead();
            Closed<?> closedForReceive = this.broadcastChannel.getClosedForReceive();
            if (subHead >= this.broadcastChannel.getTail()) {
                if (closedForReceive == null) {
                    closedForReceive = getClosedForReceive();
                }
                return closedForReceive == null ? AbstractChannelKt.POLL_FAILED : closedForReceive;
            }
            Object access$elementAt = this.broadcastChannel.elementAt(subHead);
            Closed<?> closedForReceive2 = getClosedForReceive();
            return closedForReceive2 != null ? closedForReceive2 : access$elementAt;
        }
    }

    /* access modifiers changed from: protected */
    public String getBufferDebugString() {
        return "(buffer:capacity=" + this.buffer.length + ",size=" + getSize() + ')';
    }
}
