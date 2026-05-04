# Sentence Sprint

Public source package for `Sentence Sprint`.
Sentence Sprint is a native Android educational game for school-age learners. 
Learners arrange word-group cards in the correct order to build meaningful English sentences.

The app is rebuilt as a clean Android project inspired by a Scratch prototype, not as a line-by-line port. It is fully offline, has no login, no ads, no analytics, no Firebase, and no unnecessary permissions.
### To install
Download APK: https://github.com/sunnysideux/sentence-sprint/releases/download/v1.0.0/Sentence.Sprint.apk

## We are looking for android app testers!
In case you are available for testing this (or any other ed-tech related apps/game):
1. Join the google group: https://groups.google.com/g/ed_tech_apps/
2. Download the game for Android: https://play.google.com/store/apps/details?id=com.sunnyapps.sentencebuilder
   (OR) On web: https://play.google.com/apps/testing/com.sunnyapps.sentencebuilder


### Credits
The design of the game was isnpired from a game designed to teach sentence construction. Here's the corresponding publication:
Design and Development of a Sentence Construction Game for Deaf and Hard of Hearing (DHH) Users: A Qualitative Usability Study. (2023). International Conference on Computers in Education. https://doi.org/10.58459/icce/2023/1094


# Technical Info.
## Build And Run

Open the project in Android Studio, let Gradle sync, then run the `app` configuration on an emulator or Android device.

Command line, after a JDK 17 and Android SDK are installed:

```bash
./gradlew clean
./gradlew assembleDebug
```

On Windows PowerShell:

```powershell
.\gradlew.bat clean
.\gradlew.bat assembleDebug
```

## Test

```bash
./gradlew test
./gradlew lintDebug
```

## Generate Release Bundle

Android App Bundle generation is supported through the Android Gradle Plugin:

```bash
./gradlew bundleRelease
```

The unsigned or locally signed bundle will be created under:

```text
app/build/outputs/bundle/release/
```

Before publishing, configure release signing locally in Android Studio or with Gradle properties. Do not commit keystore files, passwords, or private signing material to this repository.

To create a local upload key for Google Play App Signing:

```powershell
keytool -genkeypair -v -keystore C:\Users\YOUR_USER\keys\sentence-sprint-upload.jks -alias sentence-sprint-upload -keyalg RSA -keysize 2048 -validity 10000
```

Then copy the values from `gradle.properties.example` into an uncommitted Gradle properties file, such as `%USERPROFILE%\.gradle\gradle.properties`, and replace the passwords. When those properties are present, the release build automatically uses the upload signing config. This public repository does not include private signing keys or passwords.

## How To Add New Sentences

Add items in [SentenceRepository.kt](app/src/main/java/com/sunnyapps/sentencebuilder/data/SentenceRepository.kt).

Each item uses word-group cards:

```kotlin
SentenceItem(
    id = "l1_31",
    level = 1,
    category = "Simple Sentences",
    sentence = "The little boy plays football.",
    cards = listOf("The little boy", "plays", "football"),
    correctOrder = listOf("The little boy", "plays", "football"),
    distractors = listOf("reads", "a pencil")
)
```

Do not split sentences into individual words when a natural phrase works better for a young learner.

## Scoring

- Correct on first attempt: 10 points
- Correct on second attempt: 7 points
- Correct on third attempt: 5 points
- Correct after a hint or after more attempts: 3 points
- No negative score

Stars are based on level score:

- 3 stars: 85% or higher
- 2 stars: 60% to 84%
- 1 star: below 60%

## Haptics

The app uses subtle Compose haptic feedback for card placement, hints, correct answers, incorrect answers, and level completion. It uses standard platform haptic feedback types so devices without strong haptics should still run safely.

## Animations

The app includes lightweight Compose animations for card scale, slot content changes, incorrect-answer shake, success celebration, progress bar movement, sentence transitions, and result star reveal.

## Sentence Images

Each game round shows a permanent picture prompt above the sentence slots. The picture is the main prompt for the activity: learners look at the image and build the sentence that describes it.

The bundled images are offline WebP assets in `app/src/main/res/drawable-nodpi/` and are named from sentence ids, such as `sentence_l1_01.webp`.

For new reviewed artwork, use the two-step pilot workflow:

```bash
python scripts/manage_sentence_images.py pilot-prompts
```

Generate the 10 pilot PNG drafts into `image_pilot/`, review them, then convert approved drafts into app resources:

```bash
python scripts/manage_sentence_images.py convert-pilot
python scripts/manage_sentence_images.py validate
```

After the pilot style is approved, generate the remaining sentence art as reviewed batch sheets in `image_pilot/batch_sheets/`, crop the sheets into per-sentence PNG drafts, convert all 150 drafts to optimized WebP resources, and create contact sheets for visual QA:

```bash
python scripts/manage_sentence_images.py crop-batches
python scripts/manage_sentence_images.py convert-all
python scripts/manage_sentence_images.py contact-sheets
python scripts/manage_sentence_images.py validate
```

The contact sheets are written to `image_pilot/contact_sheets/` and should be checked before a release build.

Note: this public GitHub package intentionally omits the raw `image_pilot/` PNG draft archive to keep the repository small. The app is still fully buildable because the approved WebP images are included in `app/src/main/res/drawable-nodpi/`.

The older deterministic placeholder generator remains available only as a fallback for rebuilding placeholder assets:

```bash
python scripts/generate_sentence_images.py
```

## Local Progress

Progress is stored locally on the device in SharedPreferences:

- Best score per level
- Stars per level
- Completed levels
- Completed sentence count
- Total attempts

No personal data is collected. No data is transmitted to any server. No ads or analytics SDKs are used. The app works offline.

## Google Play Preparation

- App title: Sentence Sprint
- Package name: `com.sunnyapps.sentencebuilder`
- Target age: all ages 6 and above
- Version code: 2
- Version name: 1.0.1
- Target SDK: 35
- No ads
- No login or accounts
- No personal data collection
- No analytics SDK
- No internet permission
- No unnecessary permissions
- First release track: Internal testing
- First production countries: India, United States, United Kingdom, Canada, Australia, New Zealand, Singapore, United Arab Emirates
- Privacy policy source files: `playstore/privacy_policy_draft.md` and `playstore/privacy_policy.html`

Before production release:

- Create a private release signing key and keep it outside source control.
- Generate an Android App Bundle with `./gradlew clean test lintDebug assembleRelease bundleRelease`.
- Complete Play Console Data Safety based on the final implementation.
- Complete Target Audience and Content settings for all ages 6+, including children.
- Complete the Content Rating Questionnaire.
- Replace `REPLACE_WITH_PLAY_ACCOUNT_EMAIL` in the privacy policy files, publish the privacy policy through GitHub Pages, and paste that public URL into Play Console.
- Upload final store listing assets from the `playstore/` folder.
- Test through an internal or closed testing track before production release.
- Use `playstore/play_console_submission_checklist.md` as the Play Console checklist.

## Known Limitations

- The first version uses a polished tap-to-place card interaction for stability. The data and game logic are structured so true drag-and-drop can be added later without changing sentence content or scoring.
- TextToSpeech quality depends on the speech engine installed on the device.
- Store screenshots were not captured in this environment because no Android SDK/emulator was detected locally during project creation.

## Public Repository Notes

- Repository name: `sentence-sprint`
- License: all rights reserved
- The included privacy policy files use `REPLACE_WITH_PLAY_ACCOUNT_EMAIL`; replace it with a public support email before using GitHub Pages or submitting to Google Play.
- Do not commit local files such as `local.properties`, `.jks`, `.keystore`, APKs, AABs, or Gradle signing secrets.
