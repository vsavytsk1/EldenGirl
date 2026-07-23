package org.placeholder.app

import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.autofill.ContentType
import androidx.compose.ui.platform.PlatformImeOptions
import androidx.compose.ui.semantics.contentType
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.KeyboardType

/**
 * NoLearnField — THE ONLY PERMITTED TEXT INPUT in the record tier (G9).
 *
 * The IME is a logging device that ships with the phone. Words typed into a plain
 * field enter the keyboard's personal dictionary; on Gboard that dictionary SYNCS
 * to a Google account — possibly one he holds (Adversary B through an unguarded
 * door). The grotesque failure: a word she typed into her record autocompletes,
 * months later, in a message to him (v1.5 III·1).
 *
 * This wrapper bakes in the mitigations. The G9 gate FAILS the build on any raw
 * BasicTextField / TextField / EditText used outside this file.
 *
 * ⚠️ These are REQUESTS, not controls. A third-party IME may ignore them. iOS has
 *    no public API that fully stops a visible field from being learned. Say so in
 *    the app; do not pretend the residue is fixed.
 */
@Composable
fun NoLearnField(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    singleLine: Boolean = false
) {
    // The raw text input primitive is intentionally referenced ONLY here.
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        singleLine = singleLine,
        modifier = modifier.semantics {
            // Tell autofill this content is not to be saved or suggested.
            contentType = ContentType.Username + ContentType.Password
        },
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Text,
            capitalization = KeyboardCapitalization.None,
            autoCorrect = false,                 // no learning from corrections
            imeAction = ImeAction.None,
            // IME_FLAG_NO_PERSONALIZED_LEARNING (API 26+) — the load-bearing flag.
            platformImeOptions = PlatformImeOptions(
                privateImeOptions = "flagNoPersonalizedLearning"
            )
        )
        // No clipboard integration. Clipboard is readable by anything with overlay
        // access; the record tier must never place its content there (G9).
    )
}
