# THE APP · v1.3
### The platform layer — what each OS actually permits, and the forest

**Vladyslav Savytskyy** · Ancient Korinthos → Buenos Aires · 2026
*Supplement to `THE_APP.md` and `THE_APP_v1_2.md`. This one is the engineering reality check:
what the platforms let you do, what they refuse, and what that costs.*

---

## PART 0 · THE FOREST, SIZED

**Hide a tree in a forest** — and the forest already exists. A typical phone carries **40–80
apps**, most of them utilities nobody remembers installing. One more calculator is invisible
by base rate alone. You are not building camouflage; you are joining a crowd that is already
there.

But the decoy count has a sweet spot:

```
K   his search cost   her cost                 verdict
1        1 open       trivial                  no forest at all
2        2 opens      trivial                  GOOD
3        3 opens      trivial                  GOOD
5        5 opens      a real burden            over-engineered
8        8 opens      she will forget          over-engineered
```

**K = 3.** One door, two neighbours. Beyond that you are taxing her memory to buy him three
extra taps — the exact bad trade v1.2 rejected.

---

# PART I · WHAT EACH PLATFORM ACTUALLY ALLOWS

This is the section that decides the product. **Verify against current developer docs before
building — these APIs change, and the restrictive direction is the trend.**

### iOS — the icon moves, the name does not

| capability | status | detail |
|---|---|---|
| change app icon at runtime | ⚠️ **yes, with a mandatory alert** | `setAlternateIconName(_:completionHandler:)`, iOS 10.3+ |
| **silent** icon change | ❌ **no** | the system shows *"You have changed the icon for…"* — public API cannot suppress it |
| change **display name** at runtime | ❌ **no** | `CFBundleDisplayName` is static in Info.plist. Localisation only. |
| icons generated at runtime | ❌ **no** | alternate icons must be declared in Info.plist and bundled at build time |
| hide the app from the home screen | ❌ **no** | the user can hide it into the App Library manually — that is all |

> **The iOS blocker is the name.** You choose the cover identity at *build* time, ship it, and
> live with it. Runtime icon switching exists but announces itself, so treat it as unusable
> for this threat model. **On iOS, the disguise is a build decision, not a feature.**

*(Historic workarounds that swizzled the alert away are fragile and a review risk. Do not.)*

### Android — both the icon and the name move

```xml
<activity-alias android:name=".Calc"  android:label="Calculator"
    android:icon="@mipmap/ic_calc"  android:targetActivity=".MainActivity"
    android:enabled="true">
  <intent-filter><action android:name="android.intent.action.MAIN"/>
    <category android:name="android.intent.category.LAUNCHER"/></intent-filter>
</activity-alias>
```

Toggle with `PackageManager.setComponentEnabledSetting(...)` at runtime: **icon and label both
change.** This is the real mechanism, it is old and stable, and it is why Android is the
primary platform for this product.

**The honest caveats:**
- The switch may **remove the home-screen shortcut** — she re-adds it from the drawer. Warn her.
- **Settings → Apps still shows the true package label** on most builds. The disguise covers
  the launcher, not the settings list. Choose a package name and app label that are *both*
  innocuous, because there is nowhere to hide the second one.
- Android 13+ tightened notification and component behaviour; re-test on every API bump.

### Samsung — Secure Folder is the strongest mainstream option

Knox-backed **Secure Folder** creates a separately encrypted container with its own lock. Apps
inside are **absent from the main app list and launcher entirely.**

- ✅ Genuinely strong isolation, hardware-backed, and it is a **stock Samsung feature** —
  which means its presence is unremarkable on a Samsung phone
- ⚠️ **The folder itself is visible.** He sees Secure Folder exists. Its contents are the
  secret, not its existence — and "why do you have a locked folder" is a conversation.
- ✅ Mitigation: it can be hidden from the app screen and the quick panel, and Samsung markets
  it for ordinary privacy — **it has a boring, true explanation**, which is exactly the D1
  standard from v1.2.

**If she has a Samsung, this beats anything you can build.** Document it as a recommendation
inside the app rather than reimplementing it badly.

### GrapheneOS — the strongest isolation, and a tell

You named it, and it is the right instinct technically:

- ✅ **User profiles with per-profile encryption.** A second profile is genuinely isolated —
  separate keys, apps invisible across the boundary, and the profile can be ended so its data
  is at rest again. This is what security people actually use.
- ✅ Hardened memory allocator, exploit mitigations, **no Google Play Services by default**
  (sandboxed if you want them), granular network/sensor permissions per app.
- ⚠️ **Pixel-only.** Limited hardware.
- ⛔ **And here is the problem the threat model creates: an unusual OS is itself a signal.**
  *"Why does your phone look different?"* GrapheneOS is superb against a technical adversary
  and **actively counterproductive against an intimate one who notices her phone changed.**

> **The base-rate principle cuts both ways.** A calculator among eighty apps disappears.
> A hardened OS on a phone that used to be stock does not. Recommend GrapheneOS to people who
> already run it or can plausibly explain it — never as a step in an escape plan.

### The platform matrix

| | icon change | name change | true hiding | tell risk | verdict |
|---|---|---|---|---|---|
| **iOS** | with alert | ❌ | ❌ | low | build-time disguise only |
| **Android (stock)** | ✅ | ✅ | partial | low | **primary target** |
| **Samsung Knox** | ✅ | ✅ | ✅ strong | **low — it is stock** | **best mainstream** |
| **GrapheneOS profile** | n/a | n/a | ✅ **strongest** | **high — the OS is the tell** | expert users only |

---

# PART II · PURE MATH, ZERO BLOAT

### Assets

```
3 launcher icons × 6 densities, PNG RGBA   ~3,943 KB
same 3 icons as vector path data              ~1.2 KB
in-app UI drawn on Canvas / Compose               0 KB
                                        → 3,286× smaller
```

**Launcher icons must be real bitmaps** on both platforms — that is not negotiable. So:
**generate them from math at build time**, ship the PNGs, and keep the generator in the repo.
Everything *inside* the app is drawn: Compose `Canvas` on Android, SwiftUI `Path`/`Canvas` on
iOS. Mochi is already pure canvas, so the pattern is proven.

**The security dividend is bigger than the size dividend:** a bundle with no image assets has
**nothing to reverse-engineer.** No one pulls the APK and finds a suspicious PNG. There is no
art. There are only equations that happen to draw a cat.

### The dependency budget

```
third-party SDKs        0        (every one is an exfil surface + supply chain risk)
analytics               0
crash reporting         0        (or local-only, user-initiated export)
network permission      NOT DECLARED
location permission     NOT DECLARED
```

**Do not request the network permission at all.** An app that *cannot* talk is stronger than
one that promises not to — and a reviewer can verify the manifest in seconds.

---

# PART III · THE V CHECK ON STARTUP

Integrity verification, done without becoming dependent on Google.

**What it must do:**
1. **Signature check** — compare the running signing certificate against the constant compiled
   in. Detects a repackaged/trojanised build.
2. **Package name check** — someone rebuilt it under another id.
3. **Debugger / instrumentation check** — `Debug.isDebuggerConnected()`, tracer checks.
4. **Store hash** — publish reproducible-build hashes so a technical friend can verify.

**What it must NOT do:**
- ⛔ **Play Integrity / SafetyNet.** It phones Google, it fails on GrapheneOS and on any
  de-Googled phone, and it makes the most secure users the ones you lock out. Wrong direction.
- ⛔ **Refuse to run on a rooted device.** Root is not evidence of compromise, and the people
  most likely to be root are the people most likely to be protecting themselves.

**On failure, do not shout.** No red screen, no "TAMPERING DETECTED" — that is a disclosure to
anyone holding the phone. **The correct failure is to quietly refuse to open the real tier and
present the decoy.** The cover app keeps working. Nothing happened.

---

# PART IV · THE LISTENER SCAN

You asked for it, it is worth building, and it is the most dangerous feature in the document.
Read the whole section before writing any of it.

### What is technically detectable on Android

Stalkerware needs privileges it cannot hide, so you enumerate the privileges rather than the
apps:

```
1. ACCESSIBILITY SERVICES  — the big one. reading the screen and keystrokes needs this.
   AccessibilityManager.getEnabledAccessibilityServiceList()

2. DEVICE ADMIN / DEVICE OWNER — remote wipe, lock, policy
   DevicePolicyManager.getActiveAdmins()

3. NOTIFICATION LISTENERS — reads every notification, including message previews
   Settings.Secure "enabled_notification_listeners"

4. USAGE STATS / APP USAGE access

5. OVERLAY permission (SYSTEM_ALERT_WINDOW) — screen capture and phishing overlays

6. SIDELOADED / UNKNOWN-SOURCE installs — getInstallerPackageName() == null

7. DEVELOPER OPTIONS + USB DEBUGGING enabled
   Settings.Global ADB_ENABLED
```

**Report what has the power, not what the name is.** Known-package blocklists (Echap, the
Coalition Against Stalkerware) go stale in weeks and miss anything renamed. **The permission is
the signal.**

### On iOS

Far less is possible and you must say so plainly. Check for **MDM enrolment and configuration
profiles**, jailbreak indicators, and unexpected profile-based restrictions. That is roughly
the ceiling. **Do not imply iOS is clean because your scan found nothing.**

### ⚠️ The part that could get someone hurt

**DO NOT AUTO-REMOVE ANYTHING. DO NOT EVEN OFFER A ONE-TAP REMOVE.**

This is settled advocate guidance, and the reason is brutal:

> **Removing stalkerware tells him she knows.** The monitoring stops, he notices within hours,
> and he now knows she found it and is acting. Separation is already the most dangerous period —
> and this is the same escalation trigger with a different name.

**The correct behaviour of this feature is to inform, then get out of the way:**

```
✅  show what has the power, in plain language
✅  say clearly: "this may mean someone can see your screen and messages"
✅  say clearly: "REMOVING IT WILL TELL THEM YOU KNOW"
✅  say clearly: "talk to an advocate before you change anything" + the number
✅  point out: a monitored phone can still be worked around — a library computer,
    a friend's phone, a device he has never touched
❌  no remove button
❌  no "clean my phone"
❌  no severity score, no green tick. never tell anyone their phone is safe.
```

**And the deepest trap:** if the device is monitored, **the scan result is visible to him too**
— screenshotted, keylogged, or read from the notification he sees. So the scan must run behind
the real tier, produce no notification, no log, no file, and no screenshot-able summary that
persists. **Show it once, on screen, and never store it.**

---

## Where v1.3 loses, first, because you'd check anyway

- **Platform APIs move, and always toward restriction.** Everything in Part I needs verifying
  against current Apple and Android developer documentation before you build. Treat the table
  as a starting map, not a spec.
- **The iOS name blocker may be fatal to the concept there.** If the cover identity must be
  fixed at build time, iOS may be a *reading* app only — with the record living on Android or
  Samsung Knox. That is an acceptable answer and better than pretending.
- **"Settings shows the real name" is not fully solved on Android.** Choose a package name and
  label that are innocuous *in both places*, because you only get one.
- **A listener scan cannot prove absence.** It detects privilege, not intent, and it is blind to
  anything at OS or firmware level. **Never render a verdict of "clean."**
- **GrapheneOS is the strongest tech and possibly the wrong advice.** An unusual OS is a
  conversation she may not be able to afford.
- **I am not a mobile security auditor.** Part VII of `THE_APP.md` stands: this needs a real
  technology safety review before anyone relies on it.

---

*Join a forest that already exists. Generate the assets, do not ship them.*
*Detect the power, never the name. Inform, never remove.*

**P = 12 · χ = 2 · always.**
