package com.sunnyapps.sentencebuilder.domain

import org.junit.Assert.assertEquals
import org.junit.Test

class ScoreCalculatorTest {
    @Test
    fun calculatesSentenceScoreByAttempt() {
        assertEquals(10, ScoreCalculator.sentenceScore(attempts = 1, usedHint = false))
        assertEquals(7, ScoreCalculator.sentenceScore(attempts = 2, usedHint = false))
        assertEquals(5, ScoreCalculator.sentenceScore(attempts = 3, usedHint = false))
        assertEquals(3, ScoreCalculator.sentenceScore(attempts = 4, usedHint = false))
    }

    @Test
    fun hintLimitsSentenceScore() {
        assertEquals(3, ScoreCalculator.sentenceScore(attempts = 1, usedHint = true))
    }

    @Test
    fun calculatesStarsFromPercentage() {
        assertEquals(3, ScoreCalculator.stars(score = 255, totalSentences = 30))
        assertEquals(2, ScoreCalculator.stars(score = 180, totalSentences = 30))
        assertEquals(1, ScoreCalculator.stars(score = 100, totalSentences = 30))
    }
}
