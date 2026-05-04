package com.sunnyapps.sentencebuilder.data

data class SentenceItem(
    val id: String,
    val level: Int,
    val category: String,
    val sentence: String,
    val cards: List<String>,
    val correctOrder: List<String>,
    val distractors: List<String> = emptyList(),
    val audioText: String = sentence,
    val hint: String = "",
    val imageResName: String = "sentence_$id"
)

data class LevelInfo(
    val level: Int,
    val title: String,
    val description: String
)

data class LevelProgress(
    val level: Int,
    val bestScore: Int,
    val stars: Int,
    val completedSentences: Int,
    val totalAttempts: Int,
    val completed: Boolean
)

data class LevelResult(
    val level: Int,
    val levelTitle: String,
    val score: Int,
    val correctSentences: Int,
    val skippedSentences: Int,
    val totalAttempts: Int,
    val hintsUsed: Int,
    val timeSpentSeconds: Long,
    val stars: Int
)
