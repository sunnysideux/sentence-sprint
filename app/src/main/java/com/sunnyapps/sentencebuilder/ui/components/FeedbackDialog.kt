package com.sunnyapps.sentencebuilder.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.ui.theme.Leaf

@Composable
fun FeedbackDialog(
    message: String,
    positive: Boolean,
    modifier: Modifier = Modifier
) {
    if (message.isNotBlank()) {
        Box(
            modifier = modifier
                .fillMaxWidth()
                .background(
                    color = if (positive) Leaf.copy(alpha = 0.14f) else MaterialTheme.colorScheme.error.copy(alpha = 0.10f),
                    shape = RoundedCornerShape(18.dp)
                )
                .padding(14.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = message,
                style = MaterialTheme.typography.titleMedium,
                color = if (positive) Leaf else Color(0xFF9A4C3D),
                fontWeight = FontWeight.Bold
            )
        }
    }
}
