package com.sunnyapps.sentencebuilder.domain

object HintPolicy {
    const val MAX_HINTS_BEFORE_SKIP = 3

    fun shouldSkipAfterHint(hintsForSentence: Int): Boolean {
        return hintsForSentence >= MAX_HINTS_BEFORE_SKIP
    }

    fun skippedSentenceScore(): Int = 0
}
