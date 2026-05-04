package com.sunnyapps.sentencebuilder.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.ui.components.ScreenScaffold

@Composable
fun HowToPlayScreen(onBack: () -> Unit) {
    val steps = listOf(
        "1. Tap the word cards.",
        "2. Put them in the correct order.",
        "3. Tap Check.",
        "4. Use Hint if you are stuck.",
        "5. Complete the level to earn stars."
    )
    ScreenScaffold {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.Rounded.ArrowBack, contentDescription = "Back")
            }
            Text("How to Play", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.ExtraBold)
            Text("Build each sentence one card at a time.", style = MaterialTheme.typography.bodyLarge)
            steps.forEach { step ->
                Card(colors = CardDefaults.cardColors(containerColor = Color.White)) {
                    Text(
                        text = step,
                        style = MaterialTheme.typography.titleLarge,
                        modifier = Modifier.padding(18.dp)
                    )
                }
            }
        }
    }
}
