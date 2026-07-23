package org.placeholder.app

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * A calculator that is genuinely a calculator (D1). Drawn entirely with Compose —
 * no bitmap assets (G10: nothing to reverse-engineer, and no suspicious PNG in the
 * APK). No history is persisted (nothing to store, nothing to leak), and when the
 * entry sequence is later added by a human it must be EXCLUDED from any visible
 * history (v1.5 III·3).
 */
private val Bg = Color(0xFF0B0B0F)
private val Display = Color(0xFF13131A)
private val KeyDigit = Color(0xFF1E1E28)
private val KeyOp = Color(0xFF2A2438)
private val KeyAccent = Color(0xFFE0A63C)
private val Ink = Color(0xFFECECF2)

@Composable
fun CalculatorScreen() {
    var display by remember { mutableStateOf("0") }
    var stored by remember { mutableStateOf<Double?>(null) }
    var pendingOp by remember { mutableStateOf<String?>(null) }
    var freshEntry by remember { mutableStateOf(true) }

    fun currentValue(): Double = display.toDoubleOrNull() ?: 0.0

    fun formatResult(v: Double): String =
        if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString()

    fun applyPending(next: Double): Double {
        val prev = stored ?: return next
        return when (pendingOp) {
            "+" -> prev + next
            "−" -> prev - next
            "×" -> prev * next
            "÷" -> if (next == 0.0) Double.NaN else prev / next
            else -> next
        }
    }

    fun onKey(key: String) {
        when (key) {
            "AC" -> { display = "0"; stored = null; pendingOp = null; freshEntry = true }
            "±" -> display = formatResult(-currentValue())
            "%" -> display = formatResult(currentValue() / 100.0)
            "+", "−", "×", "÷" -> {
                val v = currentValue()
                stored = if (stored != null && !freshEntry) applyPending(v) else v
                display = formatResult(stored ?: v)
                pendingOp = key
                freshEntry = true
            }
            "=" -> {
                val result = applyPending(currentValue())
                display = if (result.isNaN()) "Error" else formatResult(result)
                stored = null; pendingOp = null; freshEntry = true
            }
            "." -> {
                if (freshEntry) { display = "0."; freshEntry = false }
                else if (!display.contains(".")) display += "."
            }
            else -> { // a digit
                display = if (freshEntry || display == "0") key else display + key
                freshEntry = false
            }
        }
    }

    val rows = listOf(
        listOf("AC", "±", "%", "÷"),
        listOf("7", "8", "9", "×"),
        listOf("4", "5", "6", "−"),
        listOf("1", "2", "3", "+"),
        listOf("0", ".", "=")
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Bg)
            .padding(16.dp),
        verticalArrangement = Arrangement.Bottom
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(bottom = 12.dp),
            contentAlignment = Alignment.BottomEnd
        ) {
            BasicTextDisplay(display)
        }
        rows.forEach { row ->
            Row(
                modifier = Modifier.fillMaxWidth().padding(vertical = 5.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                row.forEach { key ->
                    val isOp = key in listOf("÷", "×", "−", "+", "=")
                    val isTop = key in listOf("AC", "±", "%")
                    val color = when {
                        key == "=" -> KeyAccent
                        isOp -> KeyOp
                        isTop -> KeyOp
                        else -> KeyDigit
                    }
                    val weight = if (key == "0") 2.16f else 1f
                    CalcKey(
                        label = key,
                        bg = color,
                        modifier = Modifier.weight(weight),
                        onClick = { onKey(key) }
                    )
                }
            }
        }
    }
}

@Composable
private fun BasicTextDisplay(text: String) {
    androidx.compose.foundation.text.BasicText(
        text = text,
        maxLines = 1,
        overflow = TextOverflow.StartEllipsis,
        style = androidx.compose.ui.text.TextStyle(
            color = Ink,
            fontSize = 64.sp,
            textAlign = TextAlign.End
        ),
        modifier = Modifier.fillMaxWidth().background(Display).padding(16.dp)
    )
}

@Composable
private fun CalcKey(
    label: String,
    bg: Color,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Box(
        modifier = modifier
            .aspectRatio(if (label == "0") 2.16f else 1f)
            .background(bg)
            .clickable(onClick = onClick)
            .wrapContentHeight(),
        contentAlignment = Alignment.Center
    ) {
        androidx.compose.foundation.text.BasicText(
            text = label,
            style = androidx.compose.ui.text.TextStyle(color = Ink, fontSize = 28.sp)
        )
    }
}
