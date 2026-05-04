package com.sunnyapps.sentencebuilder.data

import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

class SentenceImageResourceTest {
    @Test
    fun everySentenceHasImageResourceName() {
        SentenceRepository.sentences.forEach { sentence ->
            assertTrue(sentence.imageResName.isNotBlank())
            assertTrue(sentence.imageResName == "sentence_${sentence.id}")
        }
    }

    @Test
    fun everyExpectedSentenceImageFileExists() {
        val resourceDir = File("src/main/res/drawable-nodpi")
        SentenceRepository.sentences.forEach { sentence ->
            val image = File(resourceDir, "${sentence.imageResName}.webp")
            assertTrue("Missing image for ${sentence.id}: ${image.path}", image.isFile)
        }
    }
}
