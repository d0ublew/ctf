package anonymous;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import anonymous.hackermessageboard.C0568R;

public class MainActivity extends AppCompatActivity {
    Button button;
    TextView errorBox;
    EditText textBox;

    /* access modifiers changed from: protected */
    public void onStart() {
        super.onStart();
        this.button = (Button) findViewById(C0568R.C0571id.button);
        this.textBox = (EditText) findViewById(C0568R.C0571id.inviteText);
        this.errorBox = (TextView) findViewById(C0568R.C0571id.Error);
        this.button.setOnClickListener(new MainActivity$$ExternalSyntheticLambda0(this));
    }

    /* access modifiers changed from: package-private */
    /* renamed from: lambda$onStart$0$anonymous-MainActivity  reason: not valid java name */
    public /* synthetic */ void m135lambda$onStart$0$anonymousMainActivity(View view) {
        String obj = this.textBox.getText().toString();
        System.out.println(obj);
        if (obj.isEmpty()) {
            return;
        }
        if (obj.equals(getResources().getString(C0568R.string.someText))) {
            switchActivities();
        } else {
            this.errorBox.setVisibility(0);
        }
    }

    /* access modifiers changed from: protected */
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView((int) C0568R.layout.activity_main);
    }

    private void switchActivities() {
        startActivity(new Intent(this, Board.class));
    }
}
