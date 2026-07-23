# THE GATES
### The safety invariants, executable — build this before you build the app

**Vladyslav Savytskyy** · Ancient Korinthos → Buenos Aires · 2026
*Companion to `THE_APP.md` Part II and `v1.5` Part II. This is task one. Not task two.*

---

## The contract

> **Every gate fails the build. None of them warn.**

A gate that warns is a comment. Exit non-zero, block the merge, and run the whole set in a
pre-commit hook as well as in CI so an agent iterating locally hits the wall in minute two
rather than at review.

```
make gates          runs everything, exits non-zero on any failure
make gates-fast     the subset that runs in <5s, for the pre-commit hook
```

Gates are numbered to match `v1.5`. Each traces to a numbered requirement in `THE_APP.md`
Part II or a named rule in `v1.2` / `v1.3` / `v1.4`, and **the trace is written in the failure
message** — so someone who breaks one is told which promise they broke, not just which regex
matched.

**Everything below is untested against a real project.** The commands are the right ones; the
paths, task names and tool versions are yours to fix. Treat it as a specification with worked
examples, not as a working pipeline.

---

## G1 · ZERO PERMISSIONS, IN THE **MERGED** MANIFEST
*Traces to: S8, S9, `v1.3` Part II*

Checking `AndroidManifest.xml` in source is the classic mistake. **The manifest merger injects
permissions from libraries**, and `INTERNET` arrives this way constantly.

**Defensive declaration** — put this in the app manifest so a merge cannot add it back:

```xml
<uses-permission android:name="android.permission.INTERNET" tools:node="remove" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" tools:node="remove" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" tools:node="remove" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" tools:node="remove" />
```

**Check the built artefact, not the source:**

```bash
aapt2 dump permissions app-release.apk | grep -E '^permission:' && FAIL
# or
apkanalyzer manifest permissions app-release.apk   # must print nothing
```

Also inspect the merged manifest report at
`app/build/outputs/logs/manifest-merger-release-report.txt` and fail on any `INJECTED` line.

**iOS equivalent:** fail if `Info.plist` contains any `NS*UsageDescription` key, or any
entitlement beyond keychain access.

```bash
codesign -d --entitlements :- MyApp.app
plutil -p MyApp.app/Info.plist | grep -i 'UsageDescription' && FAIL
```

---

## G2 · DEPENDENCY ALLOWLIST, TRANSITIVE
*Traces to: S8 — "no third-party SDKs"*

The allowlist lives in `gates/allowed-deps.txt`, one coordinate per line, **no version
wildcards**. Anything not on it fails, including anything pulled in transitively.

```bash
./gradlew :app:dependencies --configuration releaseRuntimeClasspath \
  | grep -oE '[a-z0-9.\-]+:[a-z0-9.\-]+:[0-9][^ ]*' \
  | sort -u > /tmp/actual.txt
comm -23 /tmp/actual.txt gates/allowed-deps.txt | grep . && FAIL
```

**Adding a line to the allowlist is a human decision that needs a reason in the commit
message.** That friction is the point. If an agent can edit the allowlist to make its own build
pass, the gate does nothing — protect the file (CODEOWNERS, or check it against a hash).

**iOS:** no SPM packages, no CocoaPods, no Carthage. Fail if `Package.resolved`,
`Podfile.lock` or `Cartfile.resolved` exists at all.

---

## G3 · THE STRING TABLE SAYS NOTHING
*Traces to: `v1.2` D3 — "no strings in the binary containing…"*

Run against the **release** artefact, post-shrinking, because that is what he can pull off the
phone.

```bash
# Android: DEX strings, not just resources
apkanalyzer dex packages --defined-only app-release.apk > /tmp/dex.txt
unzip -p app-release.apk resources.arsc | strings >> /tmp/dex.txt
strings app-release.apk >> /tmp/dex.txt

grep -i -F -f gates/forbidden-lexicon.txt /tmp/dex.txt && FAIL
```

`gates/forbidden-lexicon.txt` — at minimum, and in **every language you localise into**:

```
abuse        violence     helpline     hotline      shelter
coercive     survivor     stalker      escape       refuge
safety plan  restraining  domestic     perpetrator  evidence
```

**The content payload is encrypted at rest and decrypted in memory** (`v1.2` D3: *encrypt the
content payload, not just the database*), so no codex text should appear in the binary at all.
If this gate is passing only because you spelled things carefully, it is not passing.

⚠️ **Class and method names too.** `DecoyManager`, `PanicWipe`, `AbuseTactic` survive into DEX
unless obfuscated, and obfuscation is not a substitute for not naming them that.

**iOS:**

```bash
strings -a MyApp.app/MyApp | grep -i -F -f gates/forbidden-lexicon.txt && FAIL
```

---

## G4 · ONE HOUR OF USE, ZERO BYTES
*Traces to: `v1.4` Part III — "diff the sandbox. if a single byte changed…"*

The load-bearing gate for the ephemeral tier. Instrumented test, real device or emulator.

```kotlin
@Test fun sandbox_is_untouched_by_an_hour_of_use() {
    val roots = listOf(context.filesDir, context.cacheDir,
                       context.noBackupFilesDir, context.dataDir)
    val before = roots.flatMap { it.walkTopDown().toList() }
        .associate { it.path to (it.length() to it.lastModified()) }

    exerciseEveryScreen(iterations = 500)   // navigate, answer drills, rotate,
                                            // background, foreground, low-memory
    Runtime.getRuntime().gc()
    SystemClock.sleep(2_000)                // let any lazy flush actually flush

    val after = roots.flatMap { it.walkTopDown().toList() }
        .associate { it.path to (it.length() to it.lastModified()) }

    assertEquals("ZERO-WRITE VIOLATION (v1.4 Part III)", before, after)
}
```

**Watch for:** `SharedPreferences` created by a library you did not know had one, WebView data
directories, Compose or Room debug caches, and anything under `app_webview/`.

Fail also if these files exist at all:

```bash
find app_sandbox -name '*.xml' -path '*shared_prefs*' && FAIL
find app_sandbox -name '*.db' -o -name '*.db-journal' -o -name '*.db-wal' && FAIL
```

**Web tier equivalent** — same principle, cheaper:

```js
// gates/web-zero-write.spec.js  (Playwright)
await page.goto(URL); await exerciseEverything(page);
const storage = await page.evaluate(() => ({
  local: localStorage.length, session: sessionStorage.length,
  cookies: document.cookie.length,
  dbs: indexedDB.databases ? indexedDB.databases() : [],
  sw: navigator.serviceWorker?.controller ? 1 : 0,
}));
expect(storage).toEqual({ local: 0, session: 0, cookies: 0, dbs: [], sw: 0 });
```

Plus: **fail if `manifest.json` or any service worker file exists in the web build at all**
(`v1.4` Part III — a manifest makes the browser want to install it).

---

## G5 · `FLAG_SECURE` EVERYWHERE
*Traces to: S7*

Set it centrally in an `Application.ActivityLifecycleCallbacks` so a new Activity cannot miss
it, then assert it per-Activity in an instrumented test:

```kotlin
activityScenarioRule.scenario.onActivity {
    val flags = it.window.attributes.flags
    assertTrue("S7: FLAG_SECURE missing on ${it::class.simpleName}",
        flags and WindowManager.LayoutParams.FLAG_SECURE != 0)
}
```

And a static check that catches removal:

```bash
grep -rn "clearFlags(.*FLAG_SECURE" --include=*.kt src/ && FAIL
```

**iOS:** no `FLAG_SECURE` equivalent. Assert instead that a snapshot-obscuring view is
installed on `sceneWillResignActive` and removed on `sceneDidBecomeActive` — and test it by
backgrounding and reading the snapshot from the sandbox, because the API contract is not the
behaviour.

---

## G6 · SILENT IN RELEASE
*Traces to: S8*

```bash
grep -rnE '\b(Log\.[vdiwe]|println|System\.out|NSLog|print\()' --include=*.kt --include=*.swift src/ && FAIL
```

Belt and braces in `proguard-rules.pro`:

```
-assumenosideeffects class android.util.Log { public static *** [vdiwe](...); }
```

And: **do not ship the R8 mapping file**, do not upload it anywhere, and fail if the release
bundle contains one.

---

## G7 · BACKUP **AND** DEVICE-TRANSFER EXCLUSION
*Traces to: S4, `v1.5` Part III·5*

Both, separately, because API 31 split them:

```xml
<application
    android:allowBackup="false"
    android:dataExtractionRules="@xml/data_extraction_rules"
    android:fullBackupContent="false">
```

```xml
<!-- res/xml/data_extraction_rules.xml -->
<data-extraction-rules>
    <cloud-backup><exclude domain="root" /><exclude domain="file" />
        <exclude domain="database" /><exclude domain="sharedpref" /></cloud-backup>
    <device-transfer><exclude domain="root" /><exclude domain="file" />
        <exclude domain="database" /><exclude domain="sharedpref" /></device-transfer>
</data-extraction-rules>
```

Gate: parse the merged manifest, fail unless `allowBackup="false"` **and** the rules file
exists **and** both `<cloud-backup>` and `<device-transfer>` exclude every domain.

**iOS:** assert `isExcludedFromBackup` on every URL the app writes, in a test — not in a
comment. The store lives in `Application Support/`, excluded, with file protection
`.completeUnlessOpen` or stricter.

⚠️ **Verify current semantics before trusting this file.** It was written against
documentation that moves.

---

## G8 · KEYS STAY ON THE DEVICE
*Traces to: S4, Adversary B, `v1.5` Part III·6*

```bash
grep -rn "kSecAttrSynchronizable" --include=*.swift src/ | grep -v "kCFBooleanFalse" && FAIL
grep -rn "kSecAttrAccessible" --include=*.swift src/ \
  | grep -v "WhenUnlockedThisDeviceOnly" && FAIL
```

Android: `KeyGenParameterSpec` with `setUserAuthenticationRequired(false)` — **biometrics are
banned** (`v1.2` Part II), and:

```bash
grep -rniE "BiometricPrompt|FaceID|TouchID|LocalAuthentication" --include=*.kt --include=*.swift src/ && FAIL
```

**Test that panic wipe destroys the key first.** Not "test that panic wipe works" — test the
*ordering*, by killing the process between the two steps and asserting the ciphertext is
unreadable (`v1.4` Part VI: **key first, always**).

---

## G9 · NO TEXT FIELD LEARNS
*Traces to: `v1.5` Part III·1*

Every editable field in the record tier, without exception:

```bash
grep -rn "TextField\|EditText\|UITextView\|UITextField" --include=*.kt --include=*.swift src/ \
  > /tmp/fields.txt
# each hit must have the no-learning flags within its declaration block —
# implement as a lint rule, not a grep, once the codebase has shape
```

Cleanest enforcement: **a single wrapper composable/component is the only permitted text
input**, with the flags baked in, and the gate fails on any raw `TextField` outside it. Also
fail on any clipboard use in the record tier.

---

## G10 · NO ART
*Traces to: `v1.3` Part II*

```bash
find src/main/res -name '*.png' -o -name '*.jpg' -o -name '*.webp' \
  | grep -v 'mipmap.*ic_launcher' | grep . && FAIL
```

Launcher icons must be real bitmaps and are the sole exception. **They are generated at build
time from the seed in `COVER_ICON`** and the generator lives in the repo; fail if a launcher
PNG is committed rather than produced.

---

## G11 · THE COVER IDENTITY IS NOT IN THE REPO
*Traces to: `v1.5` Part I*

The gate that protects the disguise from the search engine.

```bash
# no real cover values anywhere in tracked files
grep -rniE "$(cat gates/reserved-identity-patterns.txt | paste -sd'|')" \
  --exclude-dir=.git . && FAIL

# the placeholders must still be placeholders
grep -q 'COVER_NAME *= *"PLACEHOLDER"' gradle.properties || FAIL
```

Also fail on:
- any committed `*.keystore`, `*.jks`, `*.p12`, `*.mobileprovision`
- any screenshot of the cover UI, anywhere, including in the README
- any candidate cover name in a test fixture — **tests leak identities too**

**And read your commit messages.** No gate catches *"fix decoy PIN timing"*; a human writing
the log carefully does. Put the rule in `CONTRIBUTING.md` alongside the warning that `git log`
publishes contributors' real names and email addresses.

---

## What the gates do not do

- They do not check that the entry sequence is fast, that the cover is convincing, or that the
  decoy tier is plausible. **Those need a hostile human with the phone in their hand**
  (`v1.2` D5).
- They do not detect a burned cover, a frightening string, or a wrong safety-planning
  instruction. Those need advocates (`THE_APP.md` Part VII).
- They cannot tell you the spec is right. **They only tell you the code still matches it.**

> **Green means nothing broke. It does not mean it works.**

---

*Compile the promise or lose it.*
*Check the artefact, never the source.*

**P = 12 · χ = 2 · always.**
