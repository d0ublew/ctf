package kotlin.collections;

import java.util.ArrayList;
import java.util.Collection;
import kotlin.Metadata;
import kotlin.jvm.internal.Intrinsics;

@Metadata(mo15831d1 = {"\u0000 \n\u0000\n\u0002\u0010\u001e\n\u0000\n\u0002\u0010\u0011\n\u0000\n\u0002\u0010\u001c\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u000b\n\u0000\u001a#\u0010\u0000\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0001\"\u0004\b\u0000\u0010\u0002*\b\u0012\u0004\u0012\u0002H\u00020\u0003H\u0000¢\u0006\u0002\u0010\u0004\u001a\u001e\u0010\u0000\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0001\"\u0004\b\u0000\u0010\u0002*\b\u0012\u0004\u0012\u0002H\u00020\u0005H\u0000\u001a\u001e\u0010\u0000\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0001\"\u0004\b\u0000\u0010\u0002*\b\u0012\u0004\u0012\u0002H\u00020\u0006H\u0000\u001a,\u0010\u0007\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0001\"\u0004\b\u0000\u0010\u0002*\b\u0012\u0004\u0012\u0002H\u00020\u00052\f\u0010\b\u001a\b\u0012\u0004\u0012\u0002H\u00020\u0005H\u0000\u001a\u0018\u0010\t\u001a\u00020\n\"\u0004\b\u0000\u0010\u0002*\b\u0012\u0004\u0012\u0002H\u00020\u0001H\u0002¨\u0006\u000b"}, mo15832d2 = {"convertToSetForSetOperation", "", "T", "", "([Ljava/lang/Object;)Ljava/util/Collection;", "", "Lkotlin/sequences/Sequence;", "convertToSetForSetOperationWith", "source", "safeToConvertToSet", "", "kotlin-stdlib"}, mo15833k = 2, mo15834mv = {1, 7, 1}, mo15836xi = 48)
/* compiled from: BrittleContainsOptimization.kt */
public final class BrittleContainsOptimizationKt {
    /* JADX WARNING: type inference failed for: r1v0, types: [java.lang.Iterable<? extends T>, java.lang.Object, java.lang.Iterable] */
    /* JADX WARNING: Unknown variable types count: 1 */
    /* Code decompiled incorrectly, please refer to instructions dump. */
    public static final <T> java.util.Collection<T> convertToSetForSetOperationWith(java.lang.Iterable<? extends T> r1, java.lang.Iterable<? extends T> r2) {
        /*
            java.lang.String r0 = "<this>"
            kotlin.jvm.internal.Intrinsics.checkNotNullParameter(r1, r0)
            java.lang.String r0 = "source"
            kotlin.jvm.internal.Intrinsics.checkNotNullParameter(r2, r0)
            boolean r0 = r1 instanceof java.util.Set
            if (r0 == 0) goto L_0x0011
            java.util.Collection r1 = (java.util.Collection) r1
            goto L_0x0046
        L_0x0011:
            boolean r0 = r1 instanceof java.util.Collection
            if (r0 == 0) goto L_0x0037
            boolean r0 = r2 instanceof java.util.Collection
            if (r0 == 0) goto L_0x0025
            java.util.Collection r2 = (java.util.Collection) r2
            int r2 = r2.size()
            r0 = 2
            if (r2 >= r0) goto L_0x0025
            java.util.Collection r1 = (java.util.Collection) r1
            goto L_0x0046
        L_0x0025:
            r2 = r1
            java.util.Collection r2 = (java.util.Collection) r2
            boolean r0 = safeToConvertToSet(r2)
            if (r0 == 0) goto L_0x0035
            java.util.HashSet r1 = kotlin.collections.CollectionsKt.toHashSet(r1)
            java.util.Collection r1 = (java.util.Collection) r1
            goto L_0x0046
        L_0x0035:
            r1 = r2
            goto L_0x0046
        L_0x0037:
            boolean r2 = kotlin.collections.CollectionSystemProperties.brittleContainsOptimizationEnabled
            if (r2 == 0) goto L_0x0040
            java.util.HashSet r1 = kotlin.collections.CollectionsKt.toHashSet(r1)
            goto L_0x0044
        L_0x0040:
            java.util.List r1 = kotlin.collections.CollectionsKt.toList(r1)
        L_0x0044:
            java.util.Collection r1 = (java.util.Collection) r1
        L_0x0046:
            return r1
        */
        throw new UnsupportedOperationException("Method not decompiled: kotlin.collections.BrittleContainsOptimizationKt.convertToSetForSetOperationWith(java.lang.Iterable, java.lang.Iterable):java.util.Collection");
    }

    /* JADX WARNING: type inference failed for: r2v0, types: [java.lang.Iterable<? extends T>, java.lang.Object, java.lang.Iterable] */
    /* JADX WARNING: Unknown variable types count: 1 */
    /* Code decompiled incorrectly, please refer to instructions dump. */
    public static final <T> java.util.Collection<T> convertToSetForSetOperation(java.lang.Iterable<? extends T> r2) {
        /*
            java.lang.String r0 = "<this>"
            kotlin.jvm.internal.Intrinsics.checkNotNullParameter(r2, r0)
            boolean r0 = r2 instanceof java.util.Set
            if (r0 == 0) goto L_0x000c
            java.util.Collection r2 = (java.util.Collection) r2
            goto L_0x0031
        L_0x000c:
            boolean r0 = r2 instanceof java.util.Collection
            if (r0 == 0) goto L_0x0022
            r0 = r2
            java.util.Collection r0 = (java.util.Collection) r0
            boolean r1 = safeToConvertToSet(r0)
            if (r1 == 0) goto L_0x0020
            java.util.HashSet r2 = kotlin.collections.CollectionsKt.toHashSet(r2)
            java.util.Collection r2 = (java.util.Collection) r2
            goto L_0x0031
        L_0x0020:
            r2 = r0
            goto L_0x0031
        L_0x0022:
            boolean r0 = kotlin.collections.CollectionSystemProperties.brittleContainsOptimizationEnabled
            if (r0 == 0) goto L_0x002b
            java.util.HashSet r2 = kotlin.collections.CollectionsKt.toHashSet(r2)
            goto L_0x002f
        L_0x002b:
            java.util.List r2 = kotlin.collections.CollectionsKt.toList(r2)
        L_0x002f:
            java.util.Collection r2 = (java.util.Collection) r2
        L_0x0031:
            return r2
        */
        throw new UnsupportedOperationException("Method not decompiled: kotlin.collections.BrittleContainsOptimizationKt.convertToSetForSetOperation(java.lang.Iterable):java.util.Collection");
    }

    private static final <T> boolean safeToConvertToSet(Collection<? extends T> collection) {
        return CollectionSystemProperties.brittleContainsOptimizationEnabled && collection.size() > 2 && (collection instanceof ArrayList);
    }

    /* JADX WARNING: type inference failed for: r1v0, types: [kotlin.sequences.Sequence, kotlin.sequences.Sequence<? extends T>, java.lang.Object] */
    /* JADX WARNING: Unknown variable types count: 1 */
    /* Code decompiled incorrectly, please refer to instructions dump. */
    public static final <T> java.util.Collection<T> convertToSetForSetOperation(kotlin.sequences.Sequence<? extends T> r1) {
        /*
            java.lang.String r0 = "<this>"
            kotlin.jvm.internal.Intrinsics.checkNotNullParameter(r1, r0)
            boolean r0 = kotlin.collections.CollectionSystemProperties.brittleContainsOptimizationEnabled
            if (r0 == 0) goto L_0x000e
            java.util.HashSet r1 = kotlin.sequences.SequencesKt.toHashSet(r1)
            goto L_0x0012
        L_0x000e:
            java.util.List r1 = kotlin.sequences.SequencesKt.toList(r1)
        L_0x0012:
            java.util.Collection r1 = (java.util.Collection) r1
            return r1
        */
        throw new UnsupportedOperationException("Method not decompiled: kotlin.collections.BrittleContainsOptimizationKt.convertToSetForSetOperation(kotlin.sequences.Sequence):java.util.Collection");
    }

    public static final <T> Collection<T> convertToSetForSetOperation(T[] tArr) {
        Intrinsics.checkNotNullParameter(tArr, "<this>");
        return CollectionSystemProperties.brittleContainsOptimizationEnabled ? ArraysKt.toHashSet(tArr) : ArraysKt.asList(tArr);
    }
}
