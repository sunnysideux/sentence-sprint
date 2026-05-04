# Play Console Submission Checklist

## App Identity

- App title: Sentence Sprint
- Package name: `com.sunnyapps.sentencebuilder`
- App type: Game
- Price: Free
- First release track: Internal testing
- First production countries: India, United States, United Kingdom, Canada, Australia, New Zealand, Singapore, United Arab Emirates

## Signing

Use Google Play App Signing with a local upload key.

Create the upload key outside the repository:

```powershell
keytool -genkeypair -v -keystore C:\Users\YOUR_USER\keys\sentence-sprint-upload.jks -alias sentence-sprint-upload -keyalg RSA -keysize 2048 -validity 10000
```

Copy `gradle.properties.example` values into an uncommitted Gradle properties file and replace the passwords.

Do not commit `.jks`, `.keystore`, passwords, or Play Console credentials.

## Store Listing

- Use `store_listing.md` for title, short description, and full description.
- Upload `play_store_icon_512.png`.
- Upload `feature_graphic_1024x500.png`.
- Capture phone screenshots: Home, Level Selection, Game, Result, Progress.
- Capture tablet screenshots if tablet support is promoted.

## App Content

- Ads: No.
- App access: No login or restricted content.
- Data Safety: No data collected, no data shared, no data transmitted.
- Target Audience: all ages 6+, including children.
- Families: opt in if Play Console says the app is eligible.
- Content Rating: educational, no violence, no user-generated content, no purchases, no online interaction.
- Privacy Policy: host `privacy_policy.html` or `privacy_policy_draft.md` through GitHub Pages after replacing `REPLACE_WITH_PLAY_ACCOUNT_EMAIL`.

## Pre-Submission Checks

```powershell
.\gradlew.bat clean test lintDebug assembleRelease bundleRelease
```

Verify the release APK/AAB has no `INTERNET`, location, camera, microphone, contacts, storage, ads, or billing permissions.

Install the internal testing build on a real Android phone before production submission.
