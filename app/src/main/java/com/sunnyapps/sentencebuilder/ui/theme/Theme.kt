package com.sunnyapps.sentencebuilder.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightColors = lightColorScheme(
    primary = CardBlue,
    secondary = Leaf,
    tertiary = Sunshine,
    background = Cream,
    surface = Cream,
    onPrimary = Cream,
    onSecondary = Cream,
    onTertiary = Ink,
    onBackground = Ink,
    onSurface = Ink,
    error = Coral
)

@Composable
fun SentenceBuilderTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColors,
        typography = AppTypography,
        content = content
    )
}
