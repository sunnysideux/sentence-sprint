package com.sunnyapps.sentencebuilder.data

import android.content.Context
import androidx.core.content.edit

class ProgressStore(context: Context) {
    private val preferences = context.getSharedPreferences("sentence_progress", Context.MODE_PRIVATE)

    fun progressFor(level: Int): LevelProgress {
        return LevelProgress(
            level = level,
            bestScore = preferences.getInt(key(level, "bestScore"), 0),
            stars = preferences.getInt(key(level, "stars"), 0),
            completedSentences = preferences.getInt(key(level, "completedSentences"), 0),
            totalAttempts = preferences.getInt(key(level, "totalAttempts"), 0),
            completed = preferences.getBoolean(key(level, "completed"), false)
        )
    }

    fun allProgress(): List<LevelProgress> = (1..5).map(::progressFor)

    fun saveResult(result: LevelResult) {
        val updated = updateProgress(
            current = progressFor(result.level),
            score = result.score,
            stars = result.stars,
            completedSentences = result.correctSentences,
            attempts = result.totalAttempts,
            completed = true
        )
        preferences.edit {
            putInt(key(result.level, "bestScore"), updated.bestScore)
            putInt(key(result.level, "stars"), updated.stars)
            putInt(key(result.level, "completedSentences"), updated.completedSentences)
            putInt(key(result.level, "totalAttempts"), updated.totalAttempts)
            putBoolean(key(result.level, "completed"), updated.completed)
        }
    }

    fun reset() {
        preferences.edit { clear() }
    }

    private fun key(level: Int, name: String): String = "level_${level}_$name"

    companion object {
        fun updateProgress(
            current: LevelProgress,
            score: Int,
            stars: Int,
            completedSentences: Int,
            attempts: Int,
            completed: Boolean
        ): LevelProgress {
            return current.copy(
                bestScore = maxOf(current.bestScore, score),
                stars = maxOf(current.stars, stars),
                completedSentences = maxOf(current.completedSentences, completedSentences),
                totalAttempts = current.totalAttempts + attempts,
                completed = current.completed || completed
            )
        }
    }
}
