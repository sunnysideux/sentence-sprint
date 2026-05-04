package com.sunnyapps.sentencebuilder.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ProgressStoreTest {
    @Test
    fun localProgressModelUpdatesBestValuesAndAttempts() {
        val current = LevelProgress(
            level = 2,
            bestScore = 50,
            stars = 1,
            completedSentences = 12,
            totalAttempts = 20,
            completed = false
        )

        val updated = ProgressStore.updateProgress(
            current = current,
            score = 70,
            stars = 2,
            completedSentences = 30,
            attempts = 35,
            completed = true
        )

        assertEquals(70, updated.bestScore)
        assertEquals(2, updated.stars)
        assertEquals(30, updated.completedSentences)
        assertEquals(55, updated.totalAttempts)
        assertTrue(updated.completed)
    }

    @Test
    fun lowerReplayScoreDoesNotReplaceBestScore() {
        val current = LevelProgress(
            level = 3,
            bestScore = 90,
            stars = 3,
            completedSentences = 30,
            totalAttempts = 10,
            completed = true
        )

        val updated = ProgressStore.updateProgress(
            current = current,
            score = 40,
            stars = 1,
            completedSentences = 20,
            attempts = 12,
            completed = true
        )

        assertEquals(90, updated.bestScore)
        assertEquals(3, updated.stars)
        assertEquals(30, updated.completedSentences)
        assertEquals(22, updated.totalAttempts)
    }
}
