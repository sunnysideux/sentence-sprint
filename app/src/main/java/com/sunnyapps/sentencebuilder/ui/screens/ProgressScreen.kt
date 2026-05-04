package com.sunnyapps.sentencebuilder.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.data.ProgressStore
import com.sunnyapps.sentencebuilder.data.SentenceRepository
import com.sunnyapps.sentencebuilder.ui.components.ScreenScaffold
import com.sunnyapps.sentencebuilder.ui.components.StarRating

@Composable
fun ProgressScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val store = remember { ProgressStore(context) }
    var refreshKey by remember { mutableIntStateOf(0) }
    var showReset by remember { mutableStateOf(false) }
    val progress = remember(refreshKey) { store.allProgress() }
    val completedLevels = progress.count { it.completed }
    val totalSentencesCompleted = progress.sumOf { it.completedSentences }
    val totalAttempts = progress.sumOf { it.totalAttempts }

    ScreenScaffold {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.Rounded.ArrowBack, contentDescription = "Back")
            }
            Text("Progress", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.ExtraBold)
            Card(colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("Levels completed: $completedLevels of 5")
                    Text("Total sentences completed: $totalSentencesCompleted")
                    Text("Total attempts: $totalAttempts")
                }
            }
            progress.forEach { item ->
                val info = SentenceRepository.getLevel(item.level)
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = Color.White)
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Level ${item.level}: ${info.title}", fontWeight = FontWeight.Bold)
                            Text("Best score: ${item.bestScore}")
                            Text("Completed sentences: ${item.completedSentences}")
                            Text(if (item.completed) "Completed" else "Not completed yet")
                        }
                        StarRating(item.stars)
                    }
                }
            }
            OutlinedButton(onClick = { showReset = true }, modifier = Modifier.fillMaxWidth()) {
                Text("Reset Progress")
            }
        }

        if (showReset) {
            AlertDialog(
                onDismissRequest = { showReset = false },
                title = { Text("Reset progress?") },
                text = { Text("This clears locally saved scores and stars on this device.") },
                confirmButton = {
                    Button(onClick = {
                        store.reset()
                        refreshKey += 1
                        showReset = false
                    }) {
                        Text("Reset")
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showReset = false }) {
                        Text("Cancel")
                    }
                }
            )
        }
    }
}
