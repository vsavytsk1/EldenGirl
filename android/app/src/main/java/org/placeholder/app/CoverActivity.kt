package org.placeholder.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent

/**
 * The one entry point. It is genuinely a calculator (D1): a real, functioning
 * tool someone would actually use, with no tell that anything else exists.
 *
 * There is NO real tier wired to this yet. The entry sequence, the decoy tier
 * and the panic wipe are reserved for human hands (v1.5 Part IV) and are not
 * generated. This scaffold ships a working cover and nothing behind it —
 * THE_APP.md v0.1 with zero stored data, so there is nothing to leak.
 */
class CoverActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // FLAG_SECURE is already applied by CoverApplication's callbacks.
        setContent { CalculatorScreen() }
    }
}
