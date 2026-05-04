package com.sunnyapps.sentencebuilder.ui.components

import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.ui.theme.SlotBorder

@Composable
fun DropSlot(
    index: Int,
    text: String?,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = 60.dp)
            .semantics {
                contentDescription = if (text == null) "Empty slot ${index + 1}" else "Slot ${index + 1}: $text"
            }
            .clickable(enabled = text != null, role = Role.Button, onClick = onClick),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = if (text == null) Color.White.copy(alpha = 0.46f) else Color.White),
        border = BorderStroke(2.dp, if (text == null) SlotBorder else MaterialTheme.colorScheme.secondary),
        elevation = CardDefaults.cardElevation(defaultElevation = if (text == null) 0.dp else 4.dp)
    ) {
        Box(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
            contentAlignment = Alignment.Center
        ) {
            AnimatedContent(targetState = text, label = "slotContent") { value ->
                Text(
                    text = value ?: "Slot ${index + 1}",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = if (value == null) FontWeight.Normal else FontWeight.Bold,
                    color = if (value == null) SlotBorder else MaterialTheme.colorScheme.onSurface,
                    textAlign = TextAlign.Center
                )
            }
        }
    }
}
