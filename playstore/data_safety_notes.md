# Play Console Data Safety Notes

These notes describe the intended Data Safety answers for the current implementation. The final developer must verify the app before submission.

Package name: `com.sunnyapps.sentencebuilder`

## Data Collected

Recommended answer: None.

The app does not collect personal data.

## Data Shared

Recommended answer: None.

The app does not share data with third parties.

## Security Practices

No data is transmitted from the app to any server.

Progress is stored locally on the device only.

## Third-Party SDKs

The app does not include advertising SDKs, analytics SDKs, Firebase, tracking SDKs, social SDKs, or payment SDKs.

## Permissions

The app should not request INTERNET, location, camera, microphone, contacts, or storage permissions.

## Final Verification

Before Play Console submission, verify the merged AndroidManifest and release build to confirm that no unnecessary permissions or SDKs have been added.

Recommended command:

```powershell
.\gradlew.bat clean test lintDebug assembleRelease bundleRelease
```
