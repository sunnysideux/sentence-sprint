package com.sunnyapps.sentencebuilder.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SentenceRepositoryTest {
    @Test
    fun repositoryReturnsCorrectSentenceCountPerLevel() {
        (1..5).forEach { level ->
            assertEquals(30, SentenceRepository.sentenceCount(level))
        }
        assertEquals(150, SentenceRepository.sentences.size)
    }

    @Test
    fun scratchPrototypeSentencesAreIncluded() {
        val allSentences = SentenceRepository.sentences.map { it.sentence }.toSet()
        assertTrue("Ram eats cake." in allSentences)
        assertTrue("He plays chess." in allSentences)
        assertTrue("The cat catches mice." in allSentences)
        assertTrue("Ravi washes his hands." in allSentences)
        assertTrue("She reads books." in allSentences)
        assertTrue("The dog barks at the car." in allSentences)
        assertTrue("Cows eat grass." in allSentences)
        assertTrue("The monkey climbs a tree." in allSentences)
    }

    @Test
    fun allSentencesUseWordGroupCards() {
        SentenceRepository.sentences.forEach { item ->
            assertEquals(item.cards, item.correctOrder)
            assertTrue(item.cards.isNotEmpty())
        }
    }
}
