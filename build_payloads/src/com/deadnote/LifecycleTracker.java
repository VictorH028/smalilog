package com.deadnote;

import android.app.Activity;
import android.app.Application;
import android.content.Context;
import android.os.Bundle;

public class LifecycleTracker implements Application.ActivityLifecycleCallbacks {

    private static final String TAG = "SMALILOG_ACTIVITY";

    private LifecycleTracker() {}

    /**
     * Acepta cualquier Context (Activity, Application, Service)
     * y obtiene la instancia global de Application.
     */
    public static void init(Context context) {
        if (context == null) return;
        try {
            Context appContext = context.getApplicationContext();
            if (appContext instanceof Application) {
                ((Application) appContext).registerActivityLifecycleCallbacks(new LifecycleTracker());
            }
        } catch (Throwable ignored) {
            /* Fail-safe */
        }
    }

    @Override
    public void onActivityResumed(Activity activity) {
        try {
            if (activity == null) {
                RemoteLog.w(TAG, "Actividad visible: null");
                return;
            }
            RemoteLog.d(TAG, "Actividad visible: " + activity.getClass().getName());
        } catch (Throwable ignored) {
            /* Fail-safe */
        }
    }

    @Override public void onActivityCreated(Activity a, Bundle b) {}
    @Override public void onActivityStarted(Activity a) {}
    @Override public void onActivityPaused(Activity a) {}
    @Override public void onActivityStopped(Activity a) {}
    @Override public void onActivitySaveInstanceState(Activity a, Bundle b) {}
    @Override public void onActivityDestroyed(Activity a) {}
}

