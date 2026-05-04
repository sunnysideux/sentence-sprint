package com.sunnyapps.sentencebuilder.ui.screens

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.data.LevelResult
import com.sunnyapps.sentencebuilder.data.ProgressStore
import com.sunnyapps.sentencebuilder.ui.components.ScreenScaffold
import com.sunnyapps.sentencebuilder.ui.components.StarRating
import kotlinx.coroutines.delay

@Composable
fun ResultScreen(
    result: LevelResult,
    onPlayAgain: () -> Unit,
    onChooseAnotherLevel: () -> Unit,
    onHome: () -> Unit
) {
    val context = LocalContext.current
    val haptics = LocalHapticFeedback.current
    val starScale = remember { Animatable(0.2f) }

    LaunchedEffect(result) {
        ProgressStore(context).saveResult(result)
        haptics.performHapticFeedback(HapticFeedbackType.LongPress)
        delay(160)
        starScale.animateTo(1f, tween(520))
    }

    ScreenScaffold {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text("Level Complete!", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.ExtraBold, textAlign = TextAlign.Center)
            Text(result.levelTitle, style = MaterialTheme.typography.titleLarge)
            StarRating(result.stars, modifier = Modifier.scale(starScale.value).padding(vertical = 18.dp))
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = androidx.compose.ui.graphics.Color.White)
            ) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Total score: ${result.score}", style = MaterialTheme.typography.titleMedium)
                    Text("Correct sentences: ${result.correctSentences}")
                    Text("Skipped sentences: ${result.skippedSentences}")
                    Text("Total attempts: ${result.totalAttempts}")
                    Text("Hints used: ${result.hintsUsed}")
                    Text("Time spent: ${formatTime(result.timeSpentSeconds)}")
                    Text("Stars earned: ${result.stars}")
                }
            }
            Button(onClick = onPlayAgain, modifier = Modifier.fillMaxWidth().padding(top = 22.dp)) {
                Text("Play Again")
            }
            OutlinedButton(onClick = onChooseAnotherLevel, modifier = Modifier.fillMaxWidth()) {
                Text("Choose Another Level")
            }
            OutlinedButton(onClick = onHome, modifier = Modifier.fillMaxWidth()) {
                Text("Home")
            }
        }
    }
}

private fun formatTime(seconds: Long): String {
    val minutes = seconds / 60
    val remaining = seconds % 60
    return if (minutes > 0) "${minutes}m ${remaining}s" else "${remaining}s"
}
