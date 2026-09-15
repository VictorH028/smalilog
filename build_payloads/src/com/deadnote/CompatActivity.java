package com.deadnote;

import android.app.Activity;

public final class CompatActivity {
    private CompatActivity() {}

    public static void onResume(Activity activity) {
        String activityName = activity.getClass().getName();
        RemoteLogger.d("SMALILOG_ACTIVITY", "Actividad visible: " + activityName);
    }
}

