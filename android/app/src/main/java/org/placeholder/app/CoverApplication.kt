package org.placeholder.app

import android.app.Activity
import android.app.Application
import android.os.Bundle
import android.view.WindowManager

/**
 * Applies the window-security flag to every Activity from one place, so a new
 * Activity added later cannot silently miss it (G5 -> S7). Registering in the
 * Application means there is no per-screen opt-in to forget.
 *
 * FLAG_SECURE blocks screenshots and the app-switcher snapshot, and frustrates
 * some screen-capturing monitoring software (Adversary C).
 */
class CoverApplication : Application() {

    override fun onCreate() {
        super.onCreate()
        registerActivityLifecycleCallbacks(SecureWindowCallbacks)
    }

    private object SecureWindowCallbacks : ActivityLifecycleCallbacks {
        override fun onActivityCreated(activity: Activity, savedInstanceState: Bundle?) {
            // Set once, at creation, before any content is shown.
            activity.window.setFlags(
                WindowManager.LayoutParams.FLAG_SECURE,
                WindowManager.LayoutParams.FLAG_SECURE
            )
        }

        // No grace period and no biometric shortcut back in (v1.5 III·4): the
        // real tier, once it exists, resumes to the cover — never to where she
        // was. Nothing here ever clears FLAG_SECURE.
        override fun onActivityStarted(activity: Activity) {}
        override fun onActivityResumed(activity: Activity) {}
        override fun onActivityPaused(activity: Activity) {}
        override fun onActivityStopped(activity: Activity) {}
        override fun onActivitySaveInstanceState(activity: Activity, outState: Bundle) {}
        override fun onActivityDestroyed(activity: Activity) {}
    }
}
