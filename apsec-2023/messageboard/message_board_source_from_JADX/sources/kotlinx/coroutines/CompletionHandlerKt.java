package kotlinx.coroutines;

import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function1;

@Metadata(mo15831d1 = {"\u0000*\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010\u0003\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\u001a8\u0010\r\u001a\u00020\u0006*#\u0012\u0015\u0012\u0013\u0018\u00010\u0002¢\u0006\f\b\u0003\u0012\b\b\u0004\u0012\u0004\b\b(\u0005\u0012\u0004\u0012\u00020\u00060\u0001j\u0002`\u00072\b\u0010\u0005\u001a\u0004\u0018\u00010\u0002H\b\":\u0010\u0000\u001a#\u0012\u0015\u0012\u0013\u0018\u00010\u0002¢\u0006\f\b\u0003\u0012\b\b\u0004\u0012\u0004\b\b(\u0005\u0012\u0004\u0012\u00020\u00060\u0001j\u0002`\u0007*\u00020\b8À\u0002X\u0004¢\u0006\u0006\u001a\u0004\b\t\u0010\n\":\u0010\u0000\u001a#\u0012\u0015\u0012\u0013\u0018\u00010\u0002¢\u0006\f\b\u0003\u0012\b\b\u0004\u0012\u0004\b\b(\u0005\u0012\u0004\u0012\u00020\u00060\u0001j\u0002`\u0007*\u00020\u000b8À\u0002X\u0004¢\u0006\u0006\u001a\u0004\b\t\u0010\f¨\u0006\u000e"}, mo15832d2 = {"asHandler", "Lkotlin/Function1;", "", "Lkotlin/ParameterName;", "name", "cause", "", "Lkotlinx/coroutines/CompletionHandler;", "Lkotlinx/coroutines/CancelHandlerBase;", "getAsHandler", "(Lkotlinx/coroutines/CancelHandlerBase;)Lkotlin/jvm/functions/Function1;", "Lkotlinx/coroutines/CompletionHandlerBase;", "(Lkotlinx/coroutines/CompletionHandlerBase;)Lkotlin/jvm/functions/Function1;", "invokeIt", "kotlinx-coroutines-core"}, mo15833k = 2, mo15834mv = {1, 6, 0}, mo15836xi = 48)
/* compiled from: CompletionHandler.kt */
public final class CompletionHandlerKt {
    public static final Function1<Throwable, Unit> getAsHandler(CompletionHandlerBase completionHandlerBase) {
        return completionHandlerBase;
    }

    public static final Function1<Throwable, Unit> getAsHandler(CancelHandlerBase cancelHandlerBase) {
        return cancelHandlerBase;
    }

    public static final void invokeIt(Function1<? super Throwable, Unit> function1, Throwable th) {
        function1.invoke(th);
    }
}
