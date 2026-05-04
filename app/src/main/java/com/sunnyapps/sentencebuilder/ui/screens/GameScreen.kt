package com.sunnyapps.sentencebuilder.ui.screens

import android.speech.tts.TextToSpeech
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material.icons.rounded.Lightbulb
import androidx.compose.material.icons.rounded.Refresh
import androidx.compose.material.icons.rounded.VolumeUp
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.data.LevelResult
import com.sunnyapps.sentencebuilder.data.SentenceRepository
import com.sunnyapps.sentencebuilder.domain.GameEngine
import com.sunnyapps.sentencebuilder.domain.HintPolicy
import com.sunnyapps.sentencebuilder.domain.ScoreCalculator
import com.sunnyapps.sentencebuilder.ui.components.CelebrationAnimation
import com.sunnyapps.sentencebuilder.ui.components.DropSlot
import com.sunnyapps.sentencebuilder.ui.components.FeedbackDialog
import com.sunnyapps.sentencebuilder.ui.components.ScreenScaffold
import com.sunnyapps.sentencebuilder.ui.components.SentenceImagePrompt
import com.sunnyapps.sentencebuilder.ui.components.WordCard
import java.util.Locale
import kotlin.math.roundToInt
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun GameScreen(
    level: Int,
    onBack: () -> Unit,
    onLevelComplete: (LevelResult) -> Unit
) {
    val info = SentenceRepository.getLevel(level)
    val sentences = remember(level) { SentenceRepository.sentencesForLevel(level) }
    val engine = remember { GameEngine() }
    val haptics = LocalHapticFeedback.current
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val shake = remember { Animatable(0f) }

    var sentenceIndex by remember(level) { mutableIntStateOf(0) }
    var score by remember(level) { mutableIntStateOf(0) }
    var correctSentences by remember(level) { mutableIntStateOf(0) }
    var skippedSentences by remember(level) { mutableIntStateOf(0) }
    var totalAttempts by remember(level) { mutableIntStateOf(0) }
    var hintsUsed by remember(level) { mutableIntStateOf(0) }
    var attemptsForSentence by remember(sentenceIndex) { mutableIntStateOf(0) }
    var hintsForSentence by remember(sentenceIndex) { mutableIntStateOf(0) }
    var usedHintForSentence by remember(sentenceIndex) { mutableStateOf(false) }
    var feedback by remember(sentenceIndex) { mutableStateOf("") }
    var feedbackPositive by remember(sentenceIndex) { mutableStateOf(false) }
    var celebration by remember(sentenceIndex) { mutableStateOf(false) }
    var startTime by remember(level) { mutableLongStateOf(System.currentTimeMillis()) }
    var ttsReady by remember { mutableStateOf(false) }
    var textToSpeech by remember { mutableStateOf<TextToSpeech?>(null) }

    val current = sentences[sentenceIndex]
    var placedCards by remember(current.id) { mutableStateOf(List(current.correctOrder.size) { null as String? }) }
    val allCards = remember(current.id) { engine.cardBankFor(current) }
    val animatedProgress by animateFloatAsState(
        targetValue = (sentenceIndex + 1).toFloat() / sentences.size.toFloat(),
        animationSpec = tween(450),
        label = "gameProgress"
    )

    DisposableEffect(Unit) {
        val engineTts = TextToSpeech(context.applicationContext) { status ->
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech?.language = Locale.ENGLISH
                ttsReady = true
            }
        }
        textToSpeech = engineTts
        onDispose {
            engineTts.stop()
            engineTts.shutdown()
        }
    }

    LaunchedEffect(level) {
        startTime = System.currentTimeMillis()
    }

    fun speak(text: String) {
        if (ttsReady) {
            textToSpeech?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "sentence-builder-tts")
        }
    }

    fun availableCards(): List<String> {
        val remaining = allCards.toMutableList()
        placedCards.filterNotNull().forEach { placed ->
            remaining.remove(placed)
        }
        return remaining
    }

    fun moveToNextSentenceOrFinish(
        finalScore: Int = score,
        finalCorrectSentences: Int = correctSentences,
        finalSkippedSentences: Int = skippedSentences
    ) {
        if (sentenceIndex == sentences.lastIndex) {
            val seconds = ((System.currentTimeMillis() - startTime) / 1000L).coerceAtLeast(1L)
            val stars = ScoreCalculator.stars(finalScore, sentences.size)
            haptics.performHapticFeedback(HapticFeedbackType.LongPress)
            onLevelComplete(
                LevelResult(
                    level = level,
                    levelTitle = info.title,
                    score = finalScore,
                    correctSentences = finalCorrectSentences,
                    skippedSentences = finalSkippedSentences,
                    totalAttempts = totalAttempts,
                    hintsUsed = hintsUsed,
                    timeSpentSeconds = seconds,
                    stars = stars
                )
            )
        } else {
            sentenceIndex += 1
        }
    }

    fun checkAnswer() {
        val newAttempts = attemptsForSentence + 1
        attemptsForSentence = newAttempts
        totalAttempts += 1
        if (engine.validate(current, placedCards)) {
            val earned = ScoreCalculator.sentenceScore(newAttempts, usedHintForSentence)
            val updatedScore = score + earned
            val updatedCorrectSentences = correctSentences + 1
            score = updatedScore
            correctSentences = updatedCorrectSentences
            feedback = listOf("Correct!", "Great job!", "Well done!").random()
            feedbackPositive = true
            celebration = true
            haptics.performHapticFeedback(HapticFeedbackType.LongPress)
            speak(current.audioText)
            scope.launch {
                delay(1200)
                celebration = false
                moveToNextSentenceOrFinish(
                    finalScore = updatedScore,
                    finalCorrectSentences = updatedCorrectSentences
                )
            }
        } else {
            feedback = if (newAttempts >= 3) "You can use a hint." else listOf("Try again.", "Almost there.", "Check the order of the cards.").random()
            feedbackPositive = false
            haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
            scope.launch {
                shake.snapTo(0f)
                shake.animateTo(-12f, tween(60))
                shake.animateTo(12f, tween(80))
                shake.animateTo(-7f, tween(70))
                shake.animateTo(0f, tween(90))
            }
        }
    }

    ScreenScaffold {
        CelebrationAnimation(visible = celebration, modifier = Modifier.fillMaxSize())
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(18.dp)
                .offset { IntOffset(shake.value.roundToInt(), 0) },
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                IconButton(onClick = onBack) {
                    Icon(Icons.Rounded.ArrowBack, contentDescription = "Back")
                }
                IconButton(onClick = {
                    haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    speak(if (engine.validate(current, placedCards)) current.audioText else "Look at the picture and build the sentence.")
                }) {
                    Icon(Icons.Rounded.VolumeUp, contentDescription = "Speaker")
                }
            }
            AnimatedContent(targetState = sentenceIndex, label = "sentenceTransition") { targetIndex ->
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(info.title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.ExtraBold)
                    Text("Sentence ${targetIndex + 1} of ${sentences.size}", style = MaterialTheme.typography.titleMedium)
                    Text("Score: $score   Attempts: $totalAttempts", style = MaterialTheme.typography.bodyLarge)
                }
            }
            LinearProgressIndicator(
                progress = { animatedProgress },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(10.dp)
                    .semantics { contentDescription = "Level progress" }
            )
            SentenceImagePrompt(sentence = current)
            FeedbackDialog(message = feedback, positive = feedbackPositive)
            Text("Sentence slots", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                placedCards.forEachIndexed { index, card ->
                    DropSlot(index = index, text = card) {
                        placedCards = placedCards.toMutableList().also { it[index] = null }
                        haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    }
                }
            }
            Text("Card bank", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                availableCards().forEach { card ->
                    WordCard(text = card) {
                        val slot = engine.nextEmptySlot(placedCards)
                        if (slot >= 0) {
                            placedCards = placedCards.toMutableList().also { it[slot] = card }
                            feedback = ""
                            haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                        } else {
                            feedback = "Tap a placed card to remove it first."
                            feedbackPositive = false
                        }
                    }
                }
            }
            Spacer(Modifier.height(4.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Button(
                    onClick = ::checkAnswer,
                    modifier = Modifier.weight(1f),
                    enabled = !celebration
                ) {
                    Text("Check")
                }
                OutlinedButton(
                    onClick = {
                        placedCards = List(current.correctOrder.size) { null }
                        feedback = ""
                        haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    },
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Rounded.Refresh, contentDescription = null, modifier = Modifier.size(18.dp))
                    Text("Reset")
                }
            }
            OutlinedButton(
                onClick = {
                    val updatedHintsForSentence = hintsForSentence + 1
                    hintsForSentence = updatedHintsForSentence
                    usedHintForSentence = true
                    hintsUsed += 1
                    haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                    if (HintPolicy.shouldSkipAfterHint(updatedHintsForSentence)) {
                        val updatedSkippedSentences = skippedSentences + 1
                        skippedSentences = updatedSkippedSentences
                        feedback = "Let's try the next one."
                        feedbackPositive = true
                        speak(current.audioText)
                        scope.launch {
                            delay(1100)
                            moveToNextSentenceOrFinish(
                                finalScore = score + HintPolicy.skippedSentenceScore(),
                                finalSkippedSentences = updatedSkippedSentences
                            )
                        }
                    } else {
                        placedCards = engine.withHintApplied(current, placedCards)
                        feedback = current.hint
                        feedbackPositive = true
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !celebration
            ) {
                Icon(Icons.Rounded.Lightbulb, contentDescription = null, modifier = Modifier.size(18.dp))
                Text("Hint", modifier = Modifier.padding(start = 8.dp))
            }
            Text(
                "Tip: tap a card to place it in the next empty slot. Tap a placed card to send it back.",
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.alpha(0.72f)
            )
        }
    }
}
