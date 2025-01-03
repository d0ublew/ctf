package kotlin.text;

import kotlin.Metadata;
import kotlin.collections.CharIterator;

@Metadata(mo15831d1 = {"\u0000\u001d\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\b\n\u0000\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\f\n\u0000*\u0001\u0000\b\n\u0018\u00002\u00020\u0001J\t\u0010\u0004\u001a\u00020\u0005H\u0002J\b\u0010\u0006\u001a\u00020\u0007H\u0016R\u000e\u0010\u0002\u001a\u00020\u0003X\u000e¢\u0006\u0002\n\u0000¨\u0006\b"}, mo15832d2 = {"kotlin/text/StringsKt__StringsKt$iterator$1", "Lkotlin/collections/CharIterator;", "index", "", "hasNext", "", "nextChar", "", "kotlin-stdlib"}, mo15833k = 1, mo15834mv = {1, 7, 1}, mo15836xi = 48)
/* compiled from: Strings.kt */
public final class StringsKt__StringsKt$iterator$1 extends CharIterator {
    final /* synthetic */ CharSequence $this_iterator;
    private int index;

    StringsKt__StringsKt$iterator$1(CharSequence charSequence) {
        this.$this_iterator = charSequence;
    }

    public char nextChar() {
        CharSequence charSequence = this.$this_iterator;
        int i = this.index;
        this.index = i + 1;
        return charSequence.charAt(i);
    }

    public boolean hasNext() {
        return this.index < this.$this_iterator.length();
    }
}
