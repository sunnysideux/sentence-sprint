package com.sunnyapps.sentencebuilder.ui.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.BarChart
import androidx.compose.material.icons.rounded.Help
import androidx.compose.material.icons.rounded.Info
import androidx.compose.material.icons.rounded.PlayArrow
import androidx.compose.material.icons.rounded.School
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.ui.components.ScreenScaffold
import com.sunnyapps.sentencebuilder.ui.theme.CardBlue
import com.sunnyapps.sentencebuilder.ui.theme.Coral
import com.sunnyapps.sentencebuilder.ui.theme.Ink
import com.sunnyapps.sentencebuilder.ui.theme.Leaf
import com.sunnyapps.sentencebuilder.ui.theme.Sunshine

@Composable
fun HomeScreen(
    onStartGame: () -> Unit,
    onChooseLevel: () -> Unit,
    onProgress: () -> Unit,
    onHowToPlay: () -> Unit,
    onPrivacyLegal: () -> Unit
) {
    ScreenScaffold {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            FriendlyMascot(Modifier.size(180.dp))
            Spacer(Modifier.height(18.dp))
            Text(
                text = "Sentence Sprint",
                style = MaterialTheme.typography.displaySmall,
                fontWeight = FontWeight.ExtraBold,
                color = Ink,
                textAlign = TextAlign.Center
            )
            Text(
                text = "Build sentences by arranging word cards",
                style = MaterialTheme.typography.titleMedium,
                color = Ink.copy(alpha = 0.76f),
                textAlign = TextAlign.Center
            )
            Spacer(Modifier.height(30.dp))
            Button(
                onClick = onStartGame,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = CardBlue)
            ) {
                Icon(Icons.Rounded.PlayArrow, contentDescription = null)
                Text("Start Game", modifier = Modifier.padding(8.dp))
            }
            OutlinedButton(onClick = onChooseLevel, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Rounded.School, contentDescription = null)
                Text("Choose Level", modifier = Modifier.padding(8.dp))
            }
            OutlinedButton(onClick = onProgress, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Rounded.BarChart, contentDescription = null)
                Text("Progress", modifier = Modifier.padding(8.dp))
            }
            OutlinedButton(onClick = onHowToPlay, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Rounded.Help, contentDescription = null)
                Text("How to Play", modifier = Modifier.padding(8.dp))
            }
            OutlinedButton(onClick = onPrivacyLegal, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Rounded.Info, contentDescription = null)
                Text("Privacy & Legal", modifier = Modifier.padding(8.dp))
            }
        }
    }
}

@Composable
private fun FriendlyMascot(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        drawRoundRect(
            color = CardBlue,
            topLeft = Offset(size.width * 0.18f, size.height * 0.22f),
            size = androidx.compose.ui.geometry.Size(size.width * 0.64f, size.height * 0.58f),
            cornerRadius = CornerRadius(28f, 28f)
        )
        drawRoundRect(
            color = Color.White,
            topLeft = Offset(size.width * 0.25f, size.height * 0.30f),
            size = androidx.compose.ui.geometry.Size(size.width * 0.50f, size.height * 0.42f),
            cornerRadius = CornerRadius(20f, 20f)
        )
        drawCircle(Sunshine, radius = size.width * 0.10f, center = Offset(size.width * 0.36f, size.height * 0.45f))
        drawCircle(Sunshine, radius = size.width * 0.10f, center = Offset(size.width * 0.64f, size.height * 0.45f))
        drawCircle(Ink, radius = size.width * 0.025f, center = Offset(size.width * 0.36f, size.height * 0.45f))
        drawCircle(Ink, radius = size.width * 0.025f, center = Offset(size.width * 0.64f, size.height * 0.45f))
        drawArc(
            color = Coral,
            startAngle = 10f,
            sweepAngle = 160f,
            useCenter = false,
            topLeft = Offset(size.width * 0.38f, size.height * 0.50f),
            size = androidx.compose.ui.geometry.Size(size.width * 0.24f, size.height * 0.18f),
            style = androidx.compose.ui.graphics.drawscope.Stroke(width = 8f)
        )
        rotate(-12f, pivot = Offset(size.width * 0.72f, size.height * 0.20f)) {
            drawRoundRect(
                color = Leaf,
                topLeft = Offset(size.width * 0.66f, size.height * 0.03f),
                size = androidx.compose.ui.geometry.Size(size.width * 0.12f, size.height * 0.34f),
                cornerRadius = CornerRadius(18f, 18f)
            )
            val tip = Path().apply {
                moveTo(size.width * 0.66f, size.height * 0.03f)
                lineTo(size.width * 0.78f, size.height * 0.03f)
                lineTo(size.width * 0.72f, 0f)
                close()
            }
            drawPath(tip, Sunshine)
        }
    }
}
