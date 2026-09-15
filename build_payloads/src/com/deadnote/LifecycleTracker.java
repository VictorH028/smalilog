package com.deadnote;

import android.app.Activity;
import android.app.Application;
import android.os.Bundle;

public class LifecycleTracker implements Application.ActivityLifecycleCallbacks {

    public static void init(Application app) {
        app.registerActivityLifecycleCallbacks(new LifecycleTracker());
    }

    @Override
    public void onActivityResumed(Activity activity) {
        CompatActivity.onResume(activity);
    }

    @Override public void onActivityCreated(Activity a, Bundle b) {}
    @Override public void onActivityStarted(Activity a) {}
    @Override public void onActivityPaused(Activity a) {}
    @Override public void onActivityStopped(Activity a) {}
    @Override public void onActivitySaveInstanceState(Activity a, Bundle b) {}
    @Override public void onActivityDestroyed(Activity a) {}
}

