package kotlin.collections;

import java.util.Iterator;
import kotlin.Metadata;
import kotlin.jvm.internal.markers.KMappedMarker;

@Metadata(mo15831d1 = {"\u0000\u0010\n\u0002\u0018\u0002\n\u0002\u0010(\n\u0002\u0010\u0007\n\u0002\b\u0005\b&\u0018\u00002\b\u0012\u0004\u0012\u00020\u00020\u0001B\u0005¢\u0006\u0002\u0010\u0003J\u000e\u0010\u0004\u001a\u00020\u0002H\u0002¢\u0006\u0002\u0010\u0005J\b\u0010\u0006\u001a\u00020\u0002H&¨\u0006\u0007"}, mo15832d2 = {"Lkotlin/collections/FloatIterator;", "", "", "()V", "next", "()Ljava/lang/Float;", "nextFloat", "kotlin-stdlib"}, mo15833k = 1, mo15834mv = {1, 7, 1}, mo15836xi = 48)
/* compiled from: Iterators.kt */
public abstract class FloatIterator implements Iterator<Float>, KMappedMarker {
    public abstract float nextFloat();

    public void remove() {
        throw new UnsupportedOperationException("Operation is not supported for read-only collection");
    }

    public final Float next() {
        return Float.valueOf(nextFloat());
    }
}
