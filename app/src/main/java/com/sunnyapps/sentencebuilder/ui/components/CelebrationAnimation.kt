package com.sunnyapps.sentencebuilder.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import com.sunnyapps.sentencebuilder.ui.theme.CardBlue
import com.sunnyapps.sentencebuilder.ui.theme.Coral
import com.sunnyapps.sentencebuilder.ui.theme.Leaf
import com.sunnyapps.sentencebuilder.ui.theme.Sunshine

@Composable
fun CelebrationAnimation(visible: Boolean, modifier: Modifier = Modifier) {
    AnimatedVisibility(visible = visible, modifier = modifier) {
        val transition = rememberInfiniteTransition(label = "celebration")
        val drift by transition.animateFloat(
            initialValue = 0f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(tween(900, easing = LinearEasing), RepeatMode.Restart),
            label = "confettiDrift"
        )
        Canvas(modifier = Modifier.fillMaxSize()) {
            val colors = listOf(Sunshine, CardBlue, Leaf, Coral, Color.White)
            repeat(18) { index ->
                val x = ((index * 53) % 100) / 100f * size.width
                val y = ((index * 31) % 100) / 100f * size.height * 0.6f + drift * 30f
                drawCircle(
                    color = colors[index % colors.size].copy(alpha = 0.65f),
                    radius = 5f + (index % 4) * 2f,
                    center = Offset(x, y)
                )
            }
        }
    }
}
