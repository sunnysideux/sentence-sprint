package com.sunnyapps.sentencebuilder.domain

import com.sunnyapps.sentencebuilder.data.SentenceItem

class GameEngine {
    fun cardBankFor(sentence: SentenceItem, seed: Int = sentence.id.hashCode()): List<String> {
        return (sentence.cards + sentence.distractors).shuffled(kotlin.random.Random(seed))
    }

    fun isComplete(placedCards: List<String?>): Boolean {
        return placedCards.isNotEmpty() && placedCards.all { it != null }
    }

    fun validate(sentence: SentenceItem, placedCards: List<String?>): Boolean {
        if (!isComplete(placedCards)) return false
        return placedCards.filterNotNull() == sentence.correctOrder
    }

    fun nextEmptySlot(placedCards: List<String?>): Int {
        return placedCards.indexOfFirst { it == null }
    }

    fun nextHintSlot(sentence: SentenceItem, placedCards: List<String?>): Int {
        return sentence.correctOrder.indices.firstOrNull { index ->
            placedCards.getOrNull(index) != sentence.correctOrder[index]
        } ?: -1
    }

    fun withHintApplied(sentence: SentenceItem, placedCards: List<String?>): List<String?> {
        val slot = nextHintSlot(sentence, placedCards)
        if (slot == -1) return placedCards
        return placedCards.toMutableList().apply {
            this[slot] = sentence.correctOrder[slot]
        }
    }
}
