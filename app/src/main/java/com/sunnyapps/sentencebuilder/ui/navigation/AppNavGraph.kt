package com.sunnyapps.sentencebuilder.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.sunnyapps.sentencebuilder.data.LevelResult
import com.sunnyapps.sentencebuilder.data.SentenceRepository
import com.sunnyapps.sentencebuilder.ui.screens.GameScreen
import com.sunnyapps.sentencebuilder.ui.screens.HomeScreen
import com.sunnyapps.sentencebuilder.ui.screens.HowToPlayScreen
import com.sunnyapps.sentencebuilder.ui.screens.LevelSelectionScreen
import com.sunnyapps.sentencebuilder.ui.screens.PrivacyLegalScreen
import com.sunnyapps.sentencebuilder.ui.screens.ProgressScreen
import com.sunnyapps.sentencebuilder.ui.screens.ResultScreen

@Composable
fun AppNavGraph() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
                onStartGame = { navController.navigate("game/1") },
                onChooseLevel = { navController.navigate("levels") },
                onProgress = { navController.navigate("progress") },
                onHowToPlay = { navController.navigate("how_to_play") },
                onPrivacyLegal = { navController.navigate("privacy_legal") }
            )
        }
        composable("levels") {
            LevelSelectionScreen(
                onBack = { navController.navigateUp() },
                onLevelSelected = { level -> navController.navigate("game/$level") }
            )
        }
        composable(
            route = "game/{level}",
            arguments = listOf(navArgument("level") { type = NavType.IntType })
        ) { backStackEntry ->
            val level = backStackEntry.arguments?.getInt("level") ?: 1
            GameScreen(
                level = level,
                onBack = { navController.navigateUp() },
                onLevelComplete = { result ->
                    navController.navigate(
                        "result/${result.level}/${result.score}/${result.correctSentences}/${result.skippedSentences}/${result.totalAttempts}/${result.hintsUsed}/${result.timeSpentSeconds}/${result.stars}"
                    ) {
                        popUpTo("game/$level") { inclusive = true }
                    }
                }
            )
        }
        composable(
            route = "result/{level}/{score}/{correct}/{skipped}/{attempts}/{hints}/{seconds}/{stars}",
            arguments = listOf(
                navArgument("level") { type = NavType.IntType },
                navArgument("score") { type = NavType.IntType },
                navArgument("correct") { type = NavType.IntType },
                navArgument("skipped") { type = NavType.IntType },
                navArgument("attempts") { type = NavType.IntType },
                navArgument("hints") { type = NavType.IntType },
                navArgument("seconds") { type = NavType.LongType },
                navArgument("stars") { type = NavType.IntType }
            )
        ) { backStackEntry ->
            val level = backStackEntry.arguments?.getInt("level") ?: 1
            val info = SentenceRepository.getLevel(level)
            val result = LevelResult(
                level = level,
                levelTitle = info.title,
                score = backStackEntry.arguments?.getInt("score") ?: 0,
                correctSentences = backStackEntry.arguments?.getInt("correct") ?: 0,
                skippedSentences = backStackEntry.arguments?.getInt("skipped") ?: 0,
                totalAttempts = backStackEntry.arguments?.getInt("attempts") ?: 0,
                hintsUsed = backStackEntry.arguments?.getInt("hints") ?: 0,
                timeSpentSeconds = backStackEntry.arguments?.getLong("seconds") ?: 0L,
                stars = backStackEntry.arguments?.getInt("stars") ?: 0
            )
            ResultScreen(
                result = result,
                onPlayAgain = { navController.navigate("game/$level") },
                onChooseAnotherLevel = { navController.navigate("levels") },
                onHome = {
                    navController.navigate("home") {
                        popUpTo("home") { inclusive = true }
                    }
                }
            )
        }
        composable("progress") {
            ProgressScreen(onBack = { navController.navigateUp() })
        }
        composable("how_to_play") {
            HowToPlayScreen(onBack = { navController.navigateUp() })
        }
        composable("privacy_legal") {
            PrivacyLegalScreen(onBack = { navController.navigateUp() })
        }
    }
}
