package com.sunnyapps.sentencebuilder.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material.icons.rounded.School
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.data.LevelInfo
import com.sunnyapps.sentencebuilder.data.LevelProgress
import com.sunnyapps.sentencebuilder.ui.theme.CardBlue
import com.sunnyapps.sentencebuilder.ui.theme.Leaf

@Composable
fun LevelCard(
    info: LevelInfo,
    sentenceCount: Int,
    progress: LevelProgress,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(role = Role.Button, onClick = onClick),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        border = BorderStroke(1.dp, CardBlue.copy(alpha = 0.18f)),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Row(
            modifier = Modifier.padding(18.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = if (progress.completed) Icons.Rounded.CheckCircle else Icons.Rounded.School,
                contentDescription = null,
                tint = if (progress.completed) Leaf else CardBlue
            )
            Spacer(Modifier.width(14.dp))
            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("Level ${info.level}", style = MaterialTheme.typography.labelLarge, color = CardBlue)
                Text(info.title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text("$sentenceCount sentences", style = MaterialTheme.typography.bodyMedium)
                Text(
                    text = if (progress.bestScore > 0) "Best score: ${progress.bestScore}" else "Best score: Not played yet",
                    style = MaterialTheme.typography.bodyMedium
                )
                Text(
                    text = if (progress.completed) "Completed" else "Not completed yet",
                    style = MaterialTheme.typography.labelMedium,
                    color = if (progress.completed) Leaf else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.65f)
                )
            }
            StarRating(stars = progress.stars)
        }
    }
}
