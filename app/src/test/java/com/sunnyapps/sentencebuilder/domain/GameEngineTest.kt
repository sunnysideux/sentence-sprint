package com.sunnyapps.sentencebuilder.domain

import com.sunnyapps.sentencebuilder.data.SentenceItem
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class GameEngineTest {
    private val engine = GameEngine()
    private val sentence = SentenceItem(
        id = "test",
        level = 1,
        category = "Test",
        sentence = "The child reads a book.",
        cards = listOf("The child", "reads", "a book"),
        correctOrder = listOf("The child", "reads", "a book"),
        distractors = listOf("writes", "a kite")
    )

    @Test
    fun sentenceValidationAcceptsExactOrder() {
        assertTrue(engine.validate(sentence, listOf("The child", "reads", "a book")))
    }

    @Test
    fun distractorCardsAreNotRequiredForCorrectValidation() {
        assertTrue(engine.validate(sentence, listOf("The child", "reads", "a book")))
        assertFalse(engine.validate(sentence, listOf("The child", "reads", "a book", "writes")))
    }

    @Test
    fun incompleteSlotSequenceIsNotAccepted() {
        assertFalse(engine.validate(sentence, listOf("The child", null, "a book")))
    }

    @Test
    fun wrongOrderIsRejected() {
        assertFalse(engine.validate(sentence, listOf("reads", "The child", "a book")))
    }

    @Test
    fun hintPlacesNextIncorrectCard() {
        val hinted = engine.withHintApplied(sentence, listOf("The child", null, null))
        assertTrue(hinted == listOf("The child", "reads", null))
    }
}
