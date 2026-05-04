# Public Source Package Notes

This is the public source package for Sentence Sprint.

Included:

- Native Android source code.
- Bundled offline WebP sentence images used by the app.
- Play Store preparation drafts and checklist.
- Image/resource management scripts.

Not included:

- Private upload keystores or passwords.
- Local Gradle signing properties.
- Android SDK/JDK/tooling caches.
- Build outputs such as APKs and AABs.
- Raw generated PNG draft archive in `image_pilot/`.

To publish this app yourself, create your own upload key and configure signing
locally. Do not commit `.jks`, `.keystore`, passwords, or Play Console
credentials.
