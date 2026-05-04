package com.sunnyapps.sentencebuilder.domain

object ScoreCalculator {
    const val MAX_POINTS_PER_SENTENCE = 10

    fun sentenceScore(attempts: Int, usedHint: Boolean): Int {
        if (usedHint) return 3
        return when (attempts.coerceAtLeast(1)) {
            1 -> 10
            2 -> 7
            3 -> 5
            else -> 3
        }
    }

    fun stars(score: Int, totalSentences: Int): Int {
        if (totalSentences <= 0) return 0
        val percent = score.toFloat() / (totalSentences * MAX_POINTS_PER_SENTENCE)
        return when {
            percent >= 0.85f -> 3
            percent >= 0.60f -> 2
            else -> 1
        }
    }
}
