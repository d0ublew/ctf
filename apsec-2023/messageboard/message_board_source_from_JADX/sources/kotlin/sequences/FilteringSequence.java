package kotlin.sequences;

import java.util.Iterator;
import kotlin.Metadata;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;

@Metadata(mo15831d1 = {"\u0000\"\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000b\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010(\n\u0000\b\u0000\u0018\u0000*\u0004\b\u0000\u0010\u00012\b\u0012\u0004\u0012\u0002H\u00010\u0002B1\u0012\f\u0010\u0003\u001a\b\u0012\u0004\u0012\u00028\u00000\u0002\u0012\b\b\u0002\u0010\u0004\u001a\u00020\u0005\u0012\u0012\u0010\u0006\u001a\u000e\u0012\u0004\u0012\u00028\u0000\u0012\u0004\u0012\u00020\u00050\u0007¢\u0006\u0002\u0010\bJ\u000f\u0010\t\u001a\b\u0012\u0004\u0012\u00028\u00000\nH\u0002R\u001a\u0010\u0006\u001a\u000e\u0012\u0004\u0012\u00028\u0000\u0012\u0004\u0012\u00020\u00050\u0007X\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\u0003\u001a\b\u0012\u0004\u0012\u00028\u00000\u0002X\u0004¢\u0006\u0002\n\u0000¨\u0006\u000b"}, mo15832d2 = {"Lkotlin/sequences/FilteringSequence;", "T", "Lkotlin/sequences/Sequence;", "sequence", "sendWhen", "", "predicate", "Lkotlin/Function1;", "(Lkotlin/sequences/Sequence;ZLkotlin/jvm/functions/Function1;)V", "iterator", "", "kotlin-stdlib"}, mo15833k = 1, mo15834mv = {1, 7, 1}, mo15836xi = 48)
/* compiled from: Sequences.kt */
public final class FilteringSequence<T> implements Sequence<T> {
    /* access modifiers changed from: private */
    public final Function1<T, Boolean> predicate;
    /* access modifiers changed from: private */
    public final boolean sendWhen;
    /* access modifiers changed from: private */
    public final Sequence<T> sequence;

    public FilteringSequence(Sequence<? extends T> sequence2, boolean z, Function1<? super T, Boolean> function1) {
        Intrinsics.checkNotNullParameter(sequence2, "sequence");
        Intrinsics.checkNotNullParameter(function1, "predicate");
        this.sequence = sequence2;
        this.sendWhen = z;
        this.predicate = function1;
    }

    /* JADX INFO: this call moved to the top of the method (can break code semantics) */
    public /* synthetic */ FilteringSequence(Sequence sequence2, boolean z, Function1 function1, int i, DefaultConstructorMarker defaultConstructorMarker) {
        this(sequence2, (i & 2) != 0 ? true : z, function1);
    }

    public Iterator<T> iterator() {
        return new FilteringSequence$iterator$1(this);
    }
}
