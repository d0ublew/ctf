package kotlinx.coroutines.internal;

import kotlin.Metadata;
import kotlin.jvm.internal.PropertyReference0Impl;
import kotlinx.coroutines.DebugStringsKt;

@Metadata(mo15833k = 3, mo15834mv = {1, 6, 0}, mo15836xi = 48)
/* compiled from: LockFreeLinkedList.kt */
/* synthetic */ class LockFreeLinkedListNode$toString$1 extends PropertyReference0Impl {
    LockFreeLinkedListNode$toString$1(Object obj) {
        super(obj, DebugStringsKt.class, "classSimpleName", "getClassSimpleName(Ljava/lang/Object;)Ljava/lang/String;", 1);
    }

    public Object get() {
        return DebugStringsKt.getClassSimpleName(this.receiver);
    }
}
