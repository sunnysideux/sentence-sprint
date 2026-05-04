package com.sunnyapps.sentencebuilder.ui.components

import androidx.compose.foundation.layout.Row
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Star
import androidx.compose.material.icons.rounded.StarBorder
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import com.sunnyapps.sentencebuilder.ui.theme.Sunshine

@Composable
fun StarRating(stars: Int, modifier: Modifier = Modifier) {
    Row(modifier = modifier.semantics { contentDescription = "$stars stars earned" }) {
        repeat(3) { index ->
            Icon(
                imageVector = if (index < stars) Icons.Rounded.Star else Icons.Rounded.StarBorder,
                contentDescription = null,
                tint = if (index < stars) Sunshine else Color(0xFF8A96A8)
            )
        }
    }
}
