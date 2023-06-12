package com.google.android.material.carousel;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Outline;
import android.graphics.Path;
import android.graphics.RectF;
import android.os.Build;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewOutlineProvider;
import android.widget.FrameLayout;
import androidx.core.math.MathUtils;
import com.google.android.material.animation.AnimationUtils;
import com.google.android.material.canvas.CanvasCompat;
import com.google.android.material.shape.AbsoluteCornerSize;
import com.google.android.material.shape.ClampedCornerSize;
import com.google.android.material.shape.CornerSize;
import com.google.android.material.shape.ShapeAppearanceModel;
import com.google.android.material.shape.ShapeAppearancePathProvider;
import com.google.android.material.shape.Shapeable;

public class MaskableFrameLayout extends FrameLayout implements Maskable, Shapeable {
    private final RectF maskRect;
    private float maskXPercentage;
    private final MaskableDelegate maskableDelegate;
    private OnMaskChangedListener onMaskChangedListener;
    private Boolean savedForceCompatClippingEnabled;
    private ShapeAppearanceModel shapeAppearanceModel;

    public MaskableFrameLayout(Context context) {
        this(context, (AttributeSet) null);
    }

    public MaskableFrameLayout(Context context, AttributeSet attributeSet) {
        this(context, attributeSet, 0);
    }

    public MaskableFrameLayout(Context context, AttributeSet attributeSet, int i) {
        super(context, attributeSet, i);
        this.maskXPercentage = 0.0f;
        this.maskRect = new RectF();
        this.maskableDelegate = createMaskableDelegate();
        this.savedForceCompatClippingEnabled = null;
        setShapeAppearanceModel(ShapeAppearanceModel.builder(context, attributeSet, i, 0, 0).build());
    }

    private MaskableDelegate createMaskableDelegate() {
        if (Build.VERSION.SDK_INT >= 33) {
            return new MaskableDelegateV33(this);
        }
        return new MaskableDelegateV22(this);
    }

    /* access modifiers changed from: protected */
    public void onSizeChanged(int i, int i2, int i3, int i4) {
        super.onSizeChanged(i, i2, i3, i4);
        onMaskChanged();
    }

    /* access modifiers changed from: protected */
    public void onAttachedToWindow() {
        super.onAttachedToWindow();
        Boolean bool = this.savedForceCompatClippingEnabled;
        if (bool != null) {
            this.maskableDelegate.setForceCompatClippingEnabled(this, bool.booleanValue());
        }
    }

    /* access modifiers changed from: protected */
    public void onDetachedFromWindow() {
        this.savedForceCompatClippingEnabled = Boolean.valueOf(this.maskableDelegate.isForceCompatClippingEnabled());
        this.maskableDelegate.setForceCompatClippingEnabled(this, true);
        super.onDetachedFromWindow();
    }

    public void setShapeAppearanceModel(ShapeAppearanceModel shapeAppearanceModel2) {
        ShapeAppearanceModel withTransformedCornerSizes = shapeAppearanceModel2.withTransformedCornerSizes(new MaskableFrameLayout$$ExternalSyntheticLambda1());
        this.shapeAppearanceModel = withTransformedCornerSizes;
        this.maskableDelegate.onShapeAppearanceChanged(this, withTransformedCornerSizes);
    }

    static /* synthetic */ CornerSize lambda$setShapeAppearanceModel$0(CornerSize cornerSize) {
        return cornerSize instanceof AbsoluteCornerSize ? ClampedCornerSize.createFromCornerSize((AbsoluteCornerSize) cornerSize) : cornerSize;
    }

    public ShapeAppearanceModel getShapeAppearanceModel() {
        return this.shapeAppearanceModel;
    }

    public void setMaskXPercentage(float f) {
        float clamp = MathUtils.clamp(f, 0.0f, 1.0f);
        if (this.maskXPercentage != clamp) {
            this.maskXPercentage = clamp;
            onMaskChanged();
        }
    }

    public float getMaskXPercentage() {
        return this.maskXPercentage;
    }

    public RectF getMaskRectF() {
        return this.maskRect;
    }

    public void setOnMaskChangedListener(OnMaskChangedListener onMaskChangedListener2) {
        this.onMaskChangedListener = onMaskChangedListener2;
    }

    private void onMaskChanged() {
        if (getWidth() != 0) {
            float lerp = AnimationUtils.lerp(0.0f, ((float) getWidth()) / 2.0f, 0.0f, 1.0f, this.maskXPercentage);
            this.maskRect.set(lerp, 0.0f, ((float) getWidth()) - lerp, (float) getHeight());
            this.maskableDelegate.onMaskChanged(this, this.maskRect);
            OnMaskChangedListener onMaskChangedListener2 = this.onMaskChangedListener;
            if (onMaskChangedListener2 != null) {
                onMaskChangedListener2.onMaskChanged(this.maskRect);
            }
        }
    }

    public void setForceCompatClipping(boolean z) {
        this.maskableDelegate.setForceCompatClippingEnabled(this, z);
    }

    public boolean onTouchEvent(MotionEvent motionEvent) {
        if (!this.maskRect.isEmpty() && motionEvent.getAction() == 0) {
            if (!this.maskRect.contains(motionEvent.getX(), motionEvent.getY())) {
                return false;
            }
        }
        return super.onTouchEvent(motionEvent);
    }

    /* access modifiers changed from: protected */
    public void dispatchDraw(Canvas canvas) {
        this.maskableDelegate.maybeClip(canvas, new MaskableFrameLayout$$ExternalSyntheticLambda0(this));
    }

    /* access modifiers changed from: package-private */
    /* renamed from: lambda$dispatchDraw$1$com-google-android-material-carousel-MaskableFrameLayout */
    public /* synthetic */ void mo12078x418c47c0(Canvas canvas) {
        super.dispatchDraw(canvas);
    }

    private static abstract class MaskableDelegate {
        boolean forceCompatClippingEnabled;
        RectF maskBounds;
        ShapeAppearanceModel shapeAppearanceModel;
        final Path shapePath;

        /* access modifiers changed from: package-private */
        public abstract void invalidateClippingMethod(View view);

        /* access modifiers changed from: package-private */
        public abstract boolean shouldUseCompatClipping();

        private MaskableDelegate() {
            this.forceCompatClippingEnabled = false;
            this.maskBounds = new RectF();
            this.shapePath = new Path();
        }

        /* access modifiers changed from: package-private */
        public boolean isForceCompatClippingEnabled() {
            return this.forceCompatClippingEnabled;
        }

        /* access modifiers changed from: package-private */
        public void setForceCompatClippingEnabled(View view, boolean z) {
            if (z != this.forceCompatClippingEnabled) {
                this.forceCompatClippingEnabled = z;
                invalidateClippingMethod(view);
            }
        }

        /* access modifiers changed from: package-private */
        public void onShapeAppearanceChanged(View view, ShapeAppearanceModel shapeAppearanceModel2) {
            this.shapeAppearanceModel = shapeAppearanceModel2;
            updateShapePath();
            invalidateClippingMethod(view);
        }

        /* access modifiers changed from: package-private */
        public void onMaskChanged(View view, RectF rectF) {
            this.maskBounds = rectF;
            updateShapePath();
            invalidateClippingMethod(view);
        }

        private void updateShapePath() {
            if (!this.maskBounds.isEmpty() && this.shapeAppearanceModel != null) {
                ShapeAppearancePathProvider.getInstance().calculatePath(this.shapeAppearanceModel, 1.0f, this.maskBounds, this.shapePath);
            }
        }

        /* access modifiers changed from: package-private */
        public void maybeClip(Canvas canvas, CanvasCompat.CanvasOperation canvasOperation) {
            if (!shouldUseCompatClipping() || this.shapePath.isEmpty()) {
                canvasOperation.run(canvas);
                return;
            }
            canvas.save();
            canvas.clipPath(this.shapePath);
            canvasOperation.run(canvas);
            canvas.restore();
        }
    }

    private static class MaskableDelegateV14 extends MaskableDelegate {
        /* access modifiers changed from: package-private */
        public boolean shouldUseCompatClipping() {
            return true;
        }

        private MaskableDelegateV14() {
            super();
        }

        /* access modifiers changed from: package-private */
        public void invalidateClippingMethod(View view) {
            if (this.shapeAppearanceModel != null && !this.maskBounds.isEmpty() && shouldUseCompatClipping()) {
                view.invalidate();
            }
        }
    }

    private static class MaskableDelegateV22 extends MaskableDelegate {
        private boolean isShapeRoundRect = false;

        MaskableDelegateV22(View view) {
            super();
            initMaskOutlineProvider(view);
        }

        public boolean shouldUseCompatClipping() {
            return !this.isShapeRoundRect || this.forceCompatClippingEnabled;
        }

        /* access modifiers changed from: package-private */
        public void invalidateClippingMethod(View view) {
            updateIsShapeRoundRect();
            view.setClipToOutline(!shouldUseCompatClipping());
            if (shouldUseCompatClipping()) {
                view.invalidate();
            } else {
                view.invalidateOutline();
            }
        }

        private void updateIsShapeRoundRect() {
            if (!this.maskBounds.isEmpty() && this.shapeAppearanceModel != null) {
                this.isShapeRoundRect = this.shapeAppearanceModel.isRoundRect(this.maskBounds);
            }
        }

        /* access modifiers changed from: private */
        public float getCornerRadiusFromShapeAppearance(ShapeAppearanceModel shapeAppearanceModel, RectF rectF) {
            return shapeAppearanceModel.getTopRightCornerSize().getCornerSize(rectF);
        }

        private void initMaskOutlineProvider(View view) {
            view.setOutlineProvider(new ViewOutlineProvider() {
                public void getOutline(View view, Outline outline) {
                    if (MaskableDelegateV22.this.shapeAppearanceModel != null && !MaskableDelegateV22.this.maskBounds.isEmpty()) {
                        int i = (int) MaskableDelegateV22.this.maskBounds.left;
                        int i2 = (int) MaskableDelegateV22.this.maskBounds.top;
                        int i3 = (int) MaskableDelegateV22.this.maskBounds.right;
                        int i4 = (int) MaskableDelegateV22.this.maskBounds.bottom;
                        MaskableDelegateV22 maskableDelegateV22 = MaskableDelegateV22.this;
                        outline.setRoundRect(i, i2, i3, i4, maskableDelegateV22.getCornerRadiusFromShapeAppearance(maskableDelegateV22.shapeAppearanceModel, MaskableDelegateV22.this.maskBounds));
                    }
                }
            });
        }
    }

    private static class MaskableDelegateV33 extends MaskableDelegate {
        MaskableDelegateV33(View view) {
            super();
            initMaskOutlineProvider(view);
        }

        public boolean shouldUseCompatClipping() {
            return this.forceCompatClippingEnabled;
        }

        /* access modifiers changed from: package-private */
        public void invalidateClippingMethod(View view) {
            view.setClipToOutline(!shouldUseCompatClipping());
            if (shouldUseCompatClipping()) {
                view.invalidate();
            } else {
                view.invalidateOutline();
            }
        }

        private void initMaskOutlineProvider(View view) {
            view.setOutlineProvider(new ViewOutlineProvider() {
                public void getOutline(View view, Outline outline) {
                    if (!MaskableDelegateV33.this.shapePath.isEmpty()) {
                        outline.setPath(MaskableDelegateV33.this.shapePath);
                    }
                }
            });
        }
    }
}
