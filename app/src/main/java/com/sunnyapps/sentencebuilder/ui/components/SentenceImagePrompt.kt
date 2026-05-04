package com.sunnyapps.sentencebuilder.ui.components

import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.data.SentenceItem
import com.sunnyapps.sentencebuilder.ui.theme.CardBlue

@Composable
fun SentenceImagePrompt(
    sentence: SentenceItem,
    modifier: Modifier = Modifier
) {
    val imageId = remember(sentence.imageResName) {
        SentenceImageResources.idFor(sentence.imageResName)
    }

    Card(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.92f)),
        border = BorderStroke(1.dp, CardBlue.copy(alpha = 0.24f)),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Look and build the sentence",
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.Bold,
                color = CardBlue
            )
            AnimatedContent(targetState = imageId, label = "sentenceImagePrompt") { targetImageId ->
                if (targetImageId != 0) {
                    Image(
                        painter = painterResource(targetImageId),
                        contentDescription = "Picture prompt for: ${sentence.sentence}",
                        modifier = Modifier
                            .fillMaxWidth()
                            .aspectRatio(16f / 9f)
                            .clip(RoundedCornerShape(18.dp))
                            .semantics {
                                contentDescription = "Picture prompt for: ${sentence.sentence}"
                            },
                        contentScale = ContentScale.Crop
                    )
                } else {
                    Text(
                        text = "Picture prompt unavailable",
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier
                            .fillMaxWidth()
                            .aspectRatio(16f / 9f)
                            .padding(16.dp)
                    )
                }
            }
        }
    }
}
