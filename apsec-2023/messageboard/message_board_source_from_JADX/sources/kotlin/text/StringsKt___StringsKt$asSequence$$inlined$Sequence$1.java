package kotlin.text;

import java.util.Iterator;
import kotlin.Metadata;
import kotlin.sequences.Sequence;

@Metadata(mo15831d1 = {"\u0000\u0011\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010(\n\u0000*\u0001\u0000\b\n\u0018\u00002\b\u0012\u0004\u0012\u00028\u00000\u0001J\u000f\u0010\u0002\u001a\b\u0012\u0004\u0012\u00028\u00000\u0003H\u0002¨\u0006\u0004¸\u0006\u0000"}, mo15832d2 = {"kotlin/sequences/SequencesKt__SequencesKt$Sequence$1", "Lkotlin/sequences/Sequence;", "iterator", "", "kotlin-stdlib"}, mo15833k = 1, mo15834mv = {1, 7, 1}, mo15836xi = 48)
/* compiled from: Sequences.kt */
public final class StringsKt___StringsKt$asSequence$$inlined$Sequence$1 implements Sequence<Character> {
    final /* synthetic */ CharSequence $this_asSequence$inlined;

    public StringsKt___StringsKt$asSequence$$inlined$Sequence$1(CharSequence charSequence) {
        this.$this_asSequence$inlined = charSequence;
    }

    public Iterator<Character> iterator() {
        return StringsKt.iterator(this.$this_asSequence$inlined);
    }
}
