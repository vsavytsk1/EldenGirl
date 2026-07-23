# android/ — the encrypted record tier (ships second)

Its own build. Shares a threat model with `docs/` and `ios/` and **nothing else** — no code, no
storage, no release cycle (`docs/THE_APP_v1_5.md`, Part 0).

## What is here now

**The cover, and only the cover.** A calculator that is genuinely a calculator (D1): it works,
it stores nothing, and there is no tell that anything else exists. This is `THE_APP.md` v0.1
with zero user data — nothing to leak.

| file | what it does | gate |
|---|---|---|
| `app/src/main/AndroidManifest.xml` | defensive `tools:node="remove"` on every risky permission; `allowBackup=false` | G1, G7 |
| `res/xml/data_extraction_rules.xml` | excludes both cloud-backup and device-transfer, every domain | G7 |
| `CoverApplication.kt` | sets `FLAG_SECURE` on every Activity from one place | G5 |
| `CoverActivity.kt` | the single entry point | — |
| `CalculatorScreen.kt` | the working calculator, drawn in Compose (no bitmaps) | G10 |
| `NoLearnField.kt` | the **only** permitted text input, IME-learning disabled | G9 |
| `proguard-rules.pro` | strips logging from release; mapping file never shipped | G6, G3 |
| `tools/generate_launcher_icon.py` | generates the launcher icon from the seed at build time | G10 |

## What is deliberately NOT here

Reserved for human hands (`v1.5` Part IV) — a machine must not generate these:

- **The entry sequence** (three factors, three seconds, no failure state)
- **The decoy tier** (a plausible, harmless second PIN)
- **The panic wipe** (key-before-data ordering — `docs/THE_APP_v1_4.md`, Part VI)
- **The encrypted record** (SQLCipher, key in the Keystore `ThisDeviceOnly`, no biometrics)

When those arrive, they bring their gate teeth with them: G2 (the encrypted-store dependency,
added with a reasoned commit), G4 (the one-hour zero-write instrumented test), G8 (key-first
wipe ordering), and the runtime FLAG_SECURE assertion.

## The cover identity is not in this module

`namespace` and `applicationId` resolve to `org.placeholder.app` here. The real values come from
an **untracked** `cover.properties` at build time (see the root `.gitignore` and
`app/build.gradle.kts`). Do not commit a real name, package, domain, icon, or keystore. G11
fails the build if you do.

## Building

Requires a JDK 17 and the Android SDK. There is no `gradlew` wrapper committed yet; generate one
with a local Gradle 8.9+ (`gradle wrapper`) or open the folder in Android Studio. CI runs the
source-level gates on every push; the artefact-level gates (merged manifest, resolved dependency
graph, binary strings, sandbox zero-write) wire in once `assembleRelease` produces something to
scan — see `.github/workflows/gates.yml`.

**Green means nothing broke. It does not mean it works.** The five-minute hostile test and the
advocate review (`docs/THE_APP.md`, Part VII) are not optional and cannot be automated.
