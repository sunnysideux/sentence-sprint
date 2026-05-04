package com.sunnyapps.sentencebuilder.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.data.ProgressStore
import com.sunnyapps.sentencebuilder.data.SentenceRepository
import com.sunnyapps.sentencebuilder.ui.components.LevelCard
import com.sunnyapps.sentencebuilder.ui.components.ScreenScaffold

@Composable
fun LevelSelectionScreen(
    onBack: () -> Unit,
    onLevelSelected: (Int) -> Unit
) {
    val context = LocalContext.current
    val store = remember { ProgressStore(context) }
    val progress = remember { store.allProgress().associateBy { it.level } }

    ScreenScaffold {
        Column(Modifier.fillMaxSize().padding(20.dp)) {
            IconButton(onClick = onBack) {
                Icon(Icons.Rounded.ArrowBack, contentDescription = "Back")
            }
            Text("Choose Level", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.ExtraBold)
            Text("Pick a set of word-card puzzles.", style = MaterialTheme.typography.bodyLarge)
            LazyColumn(
                modifier = Modifier.padding(top = 18.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                items(SentenceRepository.levels) { info ->
                    LevelCard(
                        info = info,
                        sentenceCount = SentenceRepository.sentenceCount(info.level),
                        progress = progress.getValue(info.level),
                        onClick = { onLevelSelected(info.level) }
                    )
                }
            }
        }
    }
}
