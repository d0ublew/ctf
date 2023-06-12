package anonymous;

import android.os.Bundle;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;
import anonymous.hackermessageboard.C0568R;

public class Board extends AppCompatActivity {
    Button flagText;

    /* access modifiers changed from: protected */
    public void onStart() {
        super.onStart();
        Button button = (Button) findViewById(C0568R.C0571id.FlagText);
        this.flagText = button;
        button.setText("Access granted. Congrats.");
    }

    /* access modifiers changed from: protected */
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView((int) C0568R.layout.activity_board);
    }
}
