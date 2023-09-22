package com.example.glass.translateapi;

import android.app.Dialog;
import android.content.Context;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.view.Window;

import com.example.glass.camera2trans.R;

public class ApiResponseAlert {
    public static void showAlert(Context context, String headerText, String bodyText) {
        final Dialog dialog = new Dialog(context);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.custom_alert_dialog);


        TextView header = dialog.findViewById(R.id.alert_header);
        header.setText(headerText);

        TextView body = dialog.findViewById(R.id.alert_body);
        body.setText(bodyText);

        Button exitButton = dialog.findViewById(R.id.exit_button);

        exitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dialog.dismiss(); // Dismiss the dialog when the exit button is clicked
            }
        });

        dialog.show();
    }
}
