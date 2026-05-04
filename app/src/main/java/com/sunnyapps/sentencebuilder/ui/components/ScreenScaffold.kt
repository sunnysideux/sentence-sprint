package com.sunnyapps.sentencebuilder.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import com.sunnyapps.sentencebuilder.ui.theme.Coral
import com.sunnyapps.sentencebuilder.ui.theme.Cream
import com.sunnyapps.sentencebuilder.ui.theme.SoftSky
import com.sunnyapps.sentencebuilder.ui.theme.Sunshine

@Composable
fun ScreenScaffold(content: @Composable BoxScope.() -> Unit) {
    Box(modifier = Modifier.fillMaxSize()) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            drawRect(
                brush = Brush.verticalGradient(
                    colors = listOf(Cream, SoftSky)
                )
            )
            drawCircle(Sunshine.copy(alpha = 0.18f), radius = size.minDimension * 0.35f, center = Offset(size.width * 0.08f, size.height * 0.08f))
            drawCircle(Coral.copy(alpha = 0.12f), radius = size.minDimension * 0.28f, center = Offset(size.width * 0.92f, size.height * 0.18f))
            drawCircle(Color.White.copy(alpha = 0.45f), radius = size.minDimension * 0.22f, center = Offset(size.width * 0.85f, size.height * 0.85f))
        }
        content()
    }
}
