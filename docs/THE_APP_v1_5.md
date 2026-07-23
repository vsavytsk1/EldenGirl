# THE APP · v1.5
### The build layer — the repository as threat surface, and gates instead of rules

**Vladyslav Savytskyy** · Ancient Korinthos → Buenos Aires · 2026
*Supplement to `THE_APP.md`, `v1_2` (adversarial), `v1_3` (platform) and `v1_4` (ephemeral).
This one covers what happens when the spec becomes a repository and someone — or something —
starts writing code against it.*

---

## PART 0 · THE SEQUENCING CORRECTION

The brief is *"a repo for iOS and Android."* Three of the four existing documents argue
against that as step one, and they are right.

- `THE_APP.md` Part VI: **ship the web version first.** No install record, no store approval,
  handed over as a spoken URL.
- `v1.4` Part III: the training tier is **one HTML file that writes zero bytes.** That is not a
  precursor to the native app; it is the *better* architecture for that half.
- `v1.3`, in its own honest-failure section: `CFBundleDisplayName` is static, **so iOS may be a
  reading app only.**

So the repo is not two platforms. It is **three tiers with different rules**, and pretending
otherwise invites the agents to build the thing the spec already talked you out of.

| tier | what it is | writes | platform | ship |
|---|---|---|---|---|
| **`web/`** | codex + training ground | **0 bytes** | any browser | **first — it exists** |
| **`android/`** | the record, encrypted, dead-drop export | KB ciphertext | Android / Knox | second |
| **`ios/`** | codex only, until proven otherwise | 0 bytes | iOS | **last, and possibly never** |

> **Do not let a monorepo become a monolith.** The tiers share a threat model and a lexicon.
> They share no code, no storage, and no release cycle. `v1.4` Part II: *they should never
> have been one binary.*

---

## PART I · THE REPOSITORY IS A LEAK SURFACE

This is the finding that changes the work, and no existing version covers it.

`THE_APP.md` Part III requires **open source and reproducible builds** — correct, and the only
honest answer to *"trust us."* `v1.2` D3 requires that **no artefact anywhere says what it is.**

Put those in the same room and they fight.

```
public repo + canonical cover name in it
        → search "Calculator Plus" + "github"
        → repository titled "coercive-control recognition app"
        → D3 is dead, and no code change revives it
```

He does not need to be technical. He needs five suspicious minutes with her phone, a cover
name to type, and a search box. **The disguise is defeated by a search engine, not an attacker.**

### The resolution: the cover is a build parameter with no default

```
in the repo          COVER_NAME     = "PLACEHOLDER"
                     COVER_PACKAGE  = "org.placeholder.app"
                     COVER_ICON     = generated from a seed at build time
                     COVER_DOMAIN   = unset

in the repo          nothing else. no candidate list, no "e.g.", no screenshots,
                     no example values in the README, none in the tests.
```

The distributing organisation — a shelter, a helpline, a clinic, per `THE_APP.md` Part VI —
**chooses its own identity, builds, and publishes its own hash.** Reproducibility survives
intact: the build is deterministic *given the parameters*, and the org publishes the
parameters alongside the hash so a survivor's technical friend can still verify. He cannot
search his way from a cover name to this document, because the pairing exists only in that
org's release notes, not in a globally indexed file.

**This has a second dividend, larger than the first.** A single canonical cover is a single
point of failure — `THE_APP.md` already concedes *the disguise is an arms race, assume yours
will be recognised.* Parameterised identity means **there is no "the" cover to burn.** Twenty
organisations ship twenty calculators. Recognising one teaches you nothing about the rest.

### The rest of the repo leaks too

- **Repository and organisation name.** Indexed, permanent, and screenshotted into forks.
- **Commit messages and issue titles.** As searchable as the README, and nobody redacts them.
  *"fix decoy PIN timing"* in a commit log is the whole product in four words.
- **`git log` is a list of real names and email addresses.** A survivor who contributes is
  deanonymised by the version control system. Say so in `CONTRIBUTING.md`, before the first
  pull request, not after.
- **The releases page** ties a binary to a date to a download count.
- **Any hosted agent you use to write this.** A prompt is a record. **The cover identity must
  never be typed into a third-party tool** — which is easy, because per the above it is not in
  the repo either.

---

## PART II · GATES, NOT RULES

> **A rule an agent can ignore is not a rule. Compile it, or lose it.**

`THE_APP.md` Part II is ten commandments in prose. Prose is advisory. When a machine writes
the code — and when a hurried human writes it at 1 a.m., which is the same problem — the
commandments hold only where the build **fails** without them.

And the failure mode here is specific and predictable. A competent code generator has been
trained on the entire industry's idea of good practice, and good practice says: add crash
reporting, add structured logging, add analytics so you can improve, add a networking layer,
cache the assets, persist the user's progress so they don't lose it. **Every one of those is
correct everywhere except here.** The regression is not toward malice. It is toward
professionalism, which in this product is the same thing.

So the invariants get teeth. Full implementable version in `THE_GATES.md`; the shape:

| gate | invariant | catches |
|---|---|---|
| **G1** | **merged** manifest declares zero permissions | a library injecting `INTERNET` via manifest merger |
| **G2** | dependency graph empty but for an allowlist, **transitively** | S8 erosion one convenient import at a time |
| **G3** | release-artifact string table matches no forbidden term | D3 — "helpline", "abuse", "safety plan" in the binary |
| **G4** | one hour of use changes **zero bytes** in the sandbox | `v1.4`'s zero-write claim, asserted instead of hoped |
| **G5** | `FLAG_SECURE` set on every window | S7, silently lost by one new Activity |
| **G6** | no logging in release, no mapping file in the artefact | the debug line nobody removed |
| **G7** | backup **and device-transfer** exclusion both configured | S4 — see Part III, the API 31 change |
| **G8** | keys are `ThisDeviceOnly`, never synchronizable | Adversary B, arriving via iCloud Keychain |
| **G9** | every text field carries the no-learning flags | Part III, the keyboard |
| **G10** | zero bitmap assets except the generated launcher icons | `v1.3` Part II, drifting back |

**A gate warns nobody. A gate fails the build.** If it can be merged yellow, it will be.

**Run them in a pre-commit hook as well as in CI**, because an agent iterating locally for
three hours should hit the wall at minute two, not at review.

---

## PART III · THE GAPS THE EARLIER VERSIONS LEFT

Ordered by how much damage each does if missed.

### 1 · The keyboard. This is the one that gets someone hurt.

Nothing in four documents mentions the input method, and **the IME is a logging device that
ships with the phone.** Words typed into the record tier enter the keyboard's personal
dictionary. On Gboard that dictionary **syncs to a Google account** — possibly an account he
holds, which is Adversary B arriving through a door nobody guarded.

The failure is not theoretical and it is grotesque: a word she typed into her record
autocompletes, months later, in a message **to him.**

```
Android   IME_FLAG_NO_PERSONALIZED_LEARNING   (API 26+, on imeOptions)
          TYPE_TEXT_FLAG_NO_SUGGESTIONS
          android:importantForAutofill="no"
          never touch the clipboard — it is readable by anything with overlay access
          ⚠️ a third-party IME may ignore all of it. it is a request, not a control.

iOS       autocorrectionType = .no, spellCheckingType = .no, smart* = .no
          ⚠️ there is no public API that stops the keyboard learning from a visible field.
             secureTextEntry does stop it, and hides the text, which defeats journaling.
             this residue is unfixable. say so in the app.
```

And the mirror image, which belongs in `v1.3` Part IV: **an iOS custom keyboard with Full
Access is a keylogger, and it is visible in Settings.** iOS surfaces less than Android, but it
surfaces *that* — and the current listener-scan section undersells it.

### 2 · Accessibility and D3 are in direct conflict

`v1.3` Part II is right that Canvas-drawn UI has **nothing to reverse-engineer** — no
suspicious PNG in the APK. It has a second security property nobody noticed: **Canvas content
is absent from the accessibility tree.** There are no strings to read.

Now recall `v1.3` Part IV: the number-one stalkerware privilege is the **accessibility
service**, because that is how you read the screen.

So adding TalkBack support — the `semantics {}` labels the "later, with advocate review"
list promises — **hands every word of the codex to exactly the software the listener scan
exists to detect.** Screen readers and screen stealers use the same pipe.

> **This is not solvable in code and I will not pretend it is.** State it in the spec, put it
> to the advocate review, and let people who work with blind survivors decide. The options are
> ugly: no accessibility support in the real tier (excludes people), full support (leaks to
> monitors), or accessibility only in the ephemeral web tier where the content is public
> anyway. **The third is my guess and it is a guess.**

### 3 · The cover's history holds her entry sequence

`v1.2` D1 demands a calculator she actually uses — **history, memory, the lot.** `v1.2` Factor
2 makes entry *a calculation*. Therefore her entry number is sitting in the cover's own
visible history, where the whole design assumes he will look.

Exclude the entry pattern from cover history explicitly. **A gap in a history nobody audits
beats a record he can read.**

### 4 · No re-lock policy exists anywhere in the spec

She opens the real tier, puts the phone down, he picks it up. Four documents and not one line
about this.

**Re-lock on background. Immediately. No grace period, no "5 minutes", no biometric shortcut
back in** (`v1.2`: biometrics are compellable). Resume always to the cover, never to where she
was. A grace period is a convenience feature that hands him an open door.

### 5 · `allowBackup="false"` may be stale — verify it

API 31 introduced `dataExtractionRules`, which configures **cloud backup and device-to-device
transfer separately.** A new-phone migration is a backup wearing a different name, and it is
exactly the moment a controlling partner "helps her set up her new phone."

Verify current semantics against Android's documentation — `v1.3` Part I's own warning applies
to `v1.3` — and configure **both** paths explicitly. G7 exists for this.

### 6 · iOS Keychain survives app deletion

Uninstall is not a wipe. Keychain items persist. Two consequences:

- **Delete key material explicitly** — panic wipe cannot rely on the user deleting the app
- `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` **and** `kSecAttrSynchronizable = false`, or
  the key rides iCloud Keychain into an account he controls

### 7 · The photo leaks before your app ever sees it

`v0.3` offers optional photos. The photo exists **in the gallery first**, with EXIF GPS —
which quietly reintroduces the location data S9 bans. Deleting it moves it to **Recently
Deleted for 30 days** on both platforms, where it is one tap from visible.

**Capture in-app, never import; strip EXIF; and say plainly that a photo taken with the normal
camera is already outside the app's protection.** The origin is the leak, not the store.

### 8 · The voice memo breaks D3 and the spec has not admitted it

`THE_APP.md` v0.3 offers voice memo as the safer alternative to typing — good instinct, and it
does dodge the keylogger. But it requires the **microphone permission**, and D3 says *no
distinctive permissions: a calculator asking for storage is a question mark.* A calculator
asking for the microphone is not a question mark, it is an answer.

Unresolved, honestly:

- ⚠️ **Drop the voice memo.** Cleanest for D3, loses the option that suits low-literacy users
  and shaking hands.
- ⚠️ **Ship it in a cover that plausibly needs a mic** — a voice-notes or tuner cover. Then
  the cover choice is downstream of the feature set, which is a real cost.
- ⛔ **Ship it in the calculator anyway.** No. That is the permission that gets her asked.

### 9 · Store policy, not just store leakage

`THE_APP.md` Part VI weighs the *leak* of a store listing and never the *policy*. **Apple
guideline 2.3.1 prohibits hidden or undocumented features. Google's deceptive-behaviour policy
covers runtime label and icon switching** — the `activity-alias` mechanism `v1.3` Part I builds
on.

Navigable: **disclose the disguise to the review team in the review notes.** Reviewers under
NDA are not the threat model; they have seen DV apps before. Hiding it from them is how you
get a takedown, and a takedown means **she loses the tool with no warning and no way to ask
why.**

### 10 · Two small ones

- **Quick exit should land on the cover, not a browser.** The weather-page convention comes
  from DV *websites*, where you are already in a browser. Launching one from a native app
  writes history and looks strange. Falling back to a working calculator writes nothing.
- **A sideloaded build trips your own scanner.** `v1.3` Part IV flags null installer package as
  a stalkerware signal, and the APK-sideload distribution route in `THE_APP.md` Part VI
  produces exactly that. Also: `getInstallerPackageName()` is deprecated at API 30 in favour
  of `getInstallSourceInfo()`. Decide what the scan says about *itself*.

---

## PART IV · WHAT TO HAND THE AGENTS

### Order of work

```
1  THE GATES            — before a line of product code. they are the spec, executable.
2  web/                 — one HTML file, zero writes, ships to an advocacy org immediately
3  android/ cover       — a calculator that is genuinely a calculator (D1). no real tier yet.
4  android/ entry       — three factors, three seconds, no failure state
5  android/ record      — encrypted, weekly export prompt, crypto-shred, dead drop
6  ios/                 — codex only. revisit the record tier only if v1.3's name blocker moves.
```

**Steps 1–3 are shippable on their own.** A working cover with the codex behind it and nothing
stored is `THE_APP.md`'s v0.1, and it holds no user data at all — *nothing to leak.*

### The blocklist for helpful defaults

Give the agents this verbatim, because every item is something a good engineer adds unasked:

```
⛔ crash reporting, error tracking, Sentry, Crashlytics — of any kind
⛔ analytics, telemetry, "anonymous" usage metrics, A/B infrastructure
⛔ any network client, any HTTP library, any retrofit/ktor/URLSession call
⛔ logging that survives release builds
⛔ persistence "so the user doesn't lose progress" in the training tier — it is meant to be lost
⛔ a splash screen, an onboarding carousel, a rating prompt, a changelog dialog
⛔ biometric unlock (v1.2: compellable — this is not a preference)
⛔ a wrong-entry state of any kind: no shake, no toast, no counter, no lockout
⛔ deep links, share sheets, app shortcuts, widgets, notification channels
⛔ a dependency added to save an afternoon
```

### Where a human must look, and it cannot be the agents

- **The threat model itself.** Never generated, never refactored by a machine.
- **Anything touching the entry sequence, the decoy tier, or the panic wipe.** Key-before-data
  ordering (`v1.4` Part VI) is exactly the kind of thing that gets "cleaned up" into
  data-before-key by a refactor that looks tidier.
- **Every string that ships.** Read them. All of them.
- **The five-minute hostile test** (`v1.2` D5) — a suspicious, technical person with the phone
  in their hand. A machine cannot run this and neither can the person who built it.
- **`THE_APP.md` Part VII stands and nothing here replaces it.** Gates verify the code does
  what the spec says. They cannot tell you the spec is right.

---

## Where v1.5 loses, first, because you'd check anyway

- **Gates verify the checkable, and the checkable is not the important part.** G1–G10 catch
  regressions. They do not catch a design that is wrong, a cover that is already burned, or a
  phrasing that frightens someone off the app. **A green build means nothing broke, not that it
  works.**
- **The parameterised-cover model shifts work onto advocacy organisations** who have no build
  engineer and no time. If that makes it undeployable in practice, the model is wrong and the
  right answer is a small number of trusted builders publishing signed binaries — which
  reintroduces the searchable pairing. **I do not know which way this goes and it should be
  the first question asked at the safety review.**
- **The accessibility conflict is stated, not solved.** I have offered a guess and labelled it
  a guess. Someone who works with blind survivors will have a better one.
- **API specifics rot.** The API 31 backup change, the API 26 IME flag, the API 30 installer
  deprecation — all needed verifying when I wrote this and will need it again. `v1.3`'s rule
  applies to every version including this one: **treat the tables as a starting map.**
- **Agent-written code fails in ways review is bad at catching** — plausible, idiomatic, and
  subtly wrong, which is the hardest kind to see. The gates exist because I do not trust review
  here, including my own.
- **I am not a security auditor and I am not a DV professional.** Five documents in, that is
  still the most important sentence in the stack.

---

*The repository is part of the threat surface. A search engine does not respect your intentions.*
*A rule an agent can ignore is not a rule — compile it.*
*The keyboard is a logging device that came with the phone.*

**P = 12 · χ = 2 · always.**
