package com.sunnyapps.sentencebuilder.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.sunnyapps.sentencebuilder.ui.components.ScreenScaffold

@Composable
fun PrivacyLegalScreen(onBack: () -> Unit) {
    var answer by remember { mutableStateOf("") }
    var unlocked by remember { mutableStateOf(false) }
    var showError by remember { mutableStateOf(false) }

    ScreenScaffold {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.Rounded.ArrowBack, contentDescription = "Back")
            }
            Text("Privacy & Legal", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.ExtraBold)
            Text(
                text = "This grown-up area explains privacy and publishing information.",
                style = MaterialTheme.typography.bodyLarge
            )

            if (!unlocked) {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White)) {
                    Column(
                        modifier = Modifier.padding(18.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Text("Grown-up check", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                        Text("To continue, answer this: What is 8 + 4?")
                        OutlinedTextField(
                            value = answer,
                            onValueChange = {
                                answer = it.filter(Char::isDigit).take(2)
                                showError = false
                            },
                            modifier = Modifier.fillMaxWidth(),
                            label = { Text("Answer") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            singleLine = true,
                            isError = showError,
                            supportingText = {
                                if (showError) {
                                    Text("Please ask a grown-up to help with this section.")
                                }
                            }
                        )
                        Button(
                            onClick = {
                                unlocked = answer.trim() == "12"
                                showError = !unlocked
                            },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Continue")
                        }
                    }
                }
            } else {
                PrivacyPolicyCard()
            }
        }
    }
}

@Composable
private fun PrivacyPolicyCard() {
    Card(colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("Sentence Sprint Privacy Summary", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text("Sentence Sprint is an offline educational Android app for sentence-building practice.")
            Text("No account creation, login, name, email address, phone number, location, camera, microphone, contacts, or similar personal information is required.")
            Text("The app does not collect personal information and does not transmit data to any server.")
            Text("Progress such as best scores, stars, completed levels, completed sentence counts, and attempts is stored locally on this device only.")
            Text("The app does not use ads, analytics SDKs, Firebase, social SDKs, payment SDKs, or third-party tracking SDKs.")
            Text("The app does not request internet permission.")
            Text("For privacy questions, use the developer contact email shown on the Google Play listing.")
        }
    }
}
