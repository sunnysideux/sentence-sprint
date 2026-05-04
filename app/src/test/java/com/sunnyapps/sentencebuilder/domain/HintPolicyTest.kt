package com.sunnyapps.sentencebuilder.domain

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class HintPolicyTest {
    @Test
    fun firstTwoHintsDoNotSkipSentence() {
        assertFalse(HintPolicy.shouldSkipAfterHint(1))
        assertFalse(HintPolicy.shouldSkipAfterHint(2))
    }

    @Test
    fun thirdHintSkipsSentence() {
        assertTrue(HintPolicy.shouldSkipAfterHint(3))
        assertTrue(HintPolicy.shouldSkipAfterHint(4))
    }

    @Test
    fun skippedSentenceAwardsNoPoints() {
        assertEquals(0, HintPolicy.skippedSentenceScore())
    }
}
