package androidx.savedstate;

import android.view.View;
import kotlin.Metadata;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.Lambda;

@Metadata(mo15831d1 = {"\u0000\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\u0010\u0000\u001a\u0004\u0018\u00010\u00012\u0006\u0010\u0002\u001a\u00020\u0003H\n¢\u0006\u0002\b\u0004"}, mo15832d2 = {"<anonymous>", "Landroidx/savedstate/SavedStateRegistryOwner;", "view", "Landroid/view/View;", "invoke"}, mo15833k = 3, mo15834mv = {1, 6, 0}, mo15836xi = 48)
/* renamed from: androidx.savedstate.ViewTreeSavedStateRegistryOwner$findViewTreeSavedStateRegistryOwner$2 */
/* compiled from: ViewTreeSavedStateRegistryOwner.kt */
final class C0474x10fac0e3 extends Lambda implements Function1<View, SavedStateRegistryOwner> {
    public static final C0474x10fac0e3 INSTANCE = new C0474x10fac0e3();

    C0474x10fac0e3() {
        super(1);
    }

    public final SavedStateRegistryOwner invoke(View view) {
        Intrinsics.checkNotNullParameter(view, "view");
        Object tag = view.getTag(C0471R.C0472id.view_tree_saved_state_registry_owner);
        if (tag instanceof SavedStateRegistryOwner) {
            return (SavedStateRegistryOwner) tag;
        }
        return null;
    }
}
