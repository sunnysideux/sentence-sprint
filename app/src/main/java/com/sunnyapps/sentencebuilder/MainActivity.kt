package com.sunnyapps.sentencebuilder

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.sunnyapps.sentencebuilder.ui.navigation.AppNavGraph
import com.sunnyapps.sentencebuilder.ui.theme.SentenceBuilderTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SentenceBuilderTheme {
                AppNavGraph()
            }
        }
    }
}
