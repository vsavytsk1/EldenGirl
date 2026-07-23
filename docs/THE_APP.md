# THE APP
### A safety-first specification for a coercive-control recognition app

**Vladyslav Savytskyy** · Ancient Korinthos → Buenos Aires · 2026
MIT. Build it, fork it, improve it. `github.com/vsavytsk1`

*Companion to `THE_COUNTER_CURSES.md` and `the-training-ground-v1_2.html`.*

---

## Read this before you write a line of code

> **A badly designed app in this space does not fail to help. It gets someone hurt.**

That is not a reason to abandon the project. It is the reason the threat model comes before
the feature list, and why every design decision in here is downstream of it.

The single most important thing to understand: **in a coercive-control situation, the phone is
often not private.** It may be paid for by him, on his account, physically accessible to him,
backed up to a shared cloud, or carrying stalkerware. A tool that assumes a private device is
not merely useless — it is dangerous.

**If you build only one thing, build the threat model. Features come second.**

---

## The honest case for building it anyway

The obvious objection: *an abuser could use this to learn the techniques.*

**They already know them.** These behaviours are not learned from documentation; they are
learned in childhood and refined by what works. The information asymmetry today runs entirely
one direction — he has a working playbook and she has never been shown that a playbook exists.

Publishing the moveset **narrows the gap in her favour**, and that is the whole argument.

But it is not unlimited. It is why this spec bans certain features outright (see *What not to
build*) — because some capabilities really are more useful to a stalker than to a target, and
"we meant well" is not a design review.

---

# PART I · THE THREAT MODEL

Write this on the wall. Every feature gets tested against it.

### Adversary A — the partner with physical device access

**Capabilities:** picks up the phone, knows or can watch the PIN, browses apps, reads
notifications from the lock screen, checks recents, scrolls the app switcher, sees the battery
menu, checks screen-time reports.

**What this kills:**
- Any app with a revealing name or icon on the home screen
- Any notification with preview text
- Anything that appears in the app switcher with a readable screenshot
- Anything that shows up in **Settings → Battery / Screen Time / Data usage** by name

### Adversary B — the account holder

**Capabilities:** owns the Apple ID or Google account, or is in a Family Sharing / Family Link
group. Sees **purchase and download history**, can see installed apps remotely, receives
receipts by email, may control the phone plan and see call/SMS metadata on the bill.

**What this kills:**
- **The app store listing itself is a leak.** Even a free download appears in history.
- iCloud/Google Drive automatic backup can carry your app's data to an account he controls.
- "Find My" and location sharing.

> **This is the hardest problem in the whole category and most apps do not solve it. Design for
> it explicitly or state plainly that you have not.**

### Adversary C — stalkerware

**Capabilities:** installed monitoring software captures keystrokes, screenshots, location,
message content, and app usage. The Coalition Against Stalkerware exists precisely because this
is common, not exotic.

**What this kills:**
- Any assumption that on-device means private
- Any typed journal entry (keylogged)
- Any screen the user reads (screenshotted)

**Honest consequence:** if the device is compromised, *no app can save it*. The correct
response is not a cleverer feature — it is **telling the user, early and plainly, that a
borrowed or public device may be safer**, and linking to the Coalition Against Stalkerware.

### Adversary D — the data breach

Any evidence log you store is a **target**. Journals of abuse are among the most sensitive
personal data that exists. If you hold it on a server, you have created a honeypot with
someone else's safety inside it.

---

# PART II · NON-NEGOTIABLE SAFETY REQUIREMENTS

If a feature conflicts with any of these, the feature loses.

### S1 · QUICK EXIT, on every single screen
A permanently visible control that in **one tap** leaves the app, clears the current view, and
opens something neutral (a weather page). Hardware back button after exit must **not** return
to the app. Also bind a triple-tap anywhere as a secondary trigger. *This is the most important
UI element in the product.* Test it with the phone in one hand.

### S2 · DISGUISE by default
Neutral name and icon (a calculator, a weather app, a recipe app). Neutral entry screen that
performs its cover function convincingly. Real content is behind a PIN entered *through* the
cover UI. The store listing, name, screenshots and description must reveal nothing.

### S3 · NO NOTIFICATIONS, ever, by default
No badges, no banners, no lock-screen text, no scheduled reminders. If notifications are ever
added they must be opt-in, disguised, previewless, and off after every update.

### S4 · LOCAL-ONLY BY DEFAULT, and opt out of cloud backup
No account. No sign-up. No server. Data in an encrypted local store, **explicitly excluded from
iCloud and Google Auto Backup** (`android:allowBackup="false"`, `isExcludedFromBackup` on iOS).
If cloud sync is ever offered it must be opt-in, end-to-end encrypted, and clearly warned about.

### S5 · DECOY PIN
Two PINs. The real one opens the app. The decoy opens a plausible, harmless version with
innocuous content. Never a lockout screen — a lockout *proves something is hidden*.

### S6 · PANIC WIPE
A PIN or gesture that destroys the encrypted store immediately and irreversibly, leaving the
cover app intact and apparently normal.

### S7 · BLOCK SCREENSHOTS AND THE APP-SWITCHER PREVIEW
`FLAG_SECURE` on Android; obscure the snapshot on iOS backgrounding. This also frustrates some
stalkerware screen capture.

### S8 · WORK COMPLETELY OFFLINE
No network calls for core function. No analytics. No crash reporting that phones home. **No
third-party SDKs** — every one is a data-exfiltration surface and a supply-chain risk.

### S9 · NO LOCATION, EVER
Do not request it. Do not store it. Location data in this context is a weapon.

### S10 · SHOW THE ESCAPE HATCH FIRST
On first launch, before any feature: *this device may not be private. If someone else has
access to your phone or your account, consider using a library or a friend's device.* Link the
Coalition Against Stalkerware. **Saying this costs you users and it is still correct.**

---

# PART III · ARCHITECTURE

### Recommended stack

**Native, not cross-platform.** Kotlin + Jetpack Compose on Android; Swift + SwiftUI on iOS.

**Why:** you need `FLAG_SECURE`, Keystore/Keychain, backup exclusion, snapshot suppression and
biometric integration — all platform-specific security surfaces. React Native and Flutter can
reach most of these through plugins, but each plugin is a dependency you must audit, and
**S8 says no third-party SDKs**. Two native codebases is the honest cost of the requirement.

### Data

```
Android : SQLCipher (or Room + SQLCipher), key in Android Keystore, StrongBox where available
iOS     : SQLCipher or Core Data + file protection, key in Keychain / Secure Enclave
Both    : allowBackup=false / excluded from iCloud, FLAG_SECURE, no logs, no analytics
```

**Zero server.** No backend means no breach, no subpoena, no honeypot, no operating cost, and
nothing to shut down. If export is needed later, do it as a **user-initiated encrypted file the
user sends themselves** — never an upload.

### Repository and release hygiene

Open source. Reproducible builds. Publish hashes. In this category, **"trust us" is not an
acceptable security model** — a survivor should be able to have someone technical verify the
app does what it claims.

---

# PART IV · THE FEATURE SET

### v0.1 — MVP · *ship this and nothing else first*

1. **Cover app that actually works** (a real, functioning calculator)
2. **PIN entry through the cover** + decoy PIN
3. **Quick exit on every screen**
4. **THE CODEX** — the tactics, offline, readable, no interaction required
5. **Helpline directory**, offline, region-aware from locale only (never from location)
6. **The escape-hatch warning** on first run

That is a complete, useful, shippable product. It contains no data the user creates, which
means **there is nothing to leak.** Resist adding more until this is right.

### v0.2 — the training ground
The recognition drill, ported from the web build: name the tactic, clean-versus-curse rounds,
the tell, the chain. Deterministic rewards only — **no variable-ratio mechanics**, for the
reason given in the guidebook: that is the mechanism being taught against. Mochi comes along.
No streak data leaves the device.

### v0.3 — the record *(handle with maximum care)*
Dated entries, optional photos, encrypted at rest, panic-wipe covered.

**Design constraints that are not optional:**
- Warn plainly that a compromised device may capture entries as they are typed
- Offer **voice memo** as an alternative — quicker, less visible than typing
- Export as an **encrypted file the user sends to a chosen person**, never an upload
- Include a plain-language note that formats and admissibility vary by jurisdiction, and that
  a **local advocate or lawyer** is the authority on what will help legally

### v0.4 — safety planning
An offline checklist adapted from established advocacy materials (documents to gather, a bag,
a code word with a friend, the safest time to leave), with **"talk to an advocate first"**
stated at the top and repeated at the end.

### Later, only with advocate review
Trusted-contact alerting, a disguised widget, translations, accessibility for low vision and
low literacy.

---

# PART V · WHAT NOT TO BUILD

Each of these is more useful to an abuser than to a survivor, or creates a liability that
outweighs the benefit.

- **⛔ Location tracking or "share my location with a friend."** A weapon in the wrong hands, and
  a beacon if the device is compromised.
- **⛔ Automatic audio or video recording.** Recording laws vary enormously by jurisdiction and
  can expose the user to criminal liability. Advocates advise on this; an app must not.
- **⛔ Cloud accounts and social features.** Every account is a credential he might have, a
  password reset to his email, a breach surface.
- **⛔ "Is my partner abusive?" scoring quizzes.** A number cannot assess a relationship, a false
  negative is dangerous, and a false positive is its own harm. Give her the **patterns** and let
  her do the judging — that is what the whole guidebook argues.
- **⛔ Any AI chat that gives situation-specific advice.** No model can assess danger. Static,
  reviewed content plus a helpline number is more useful and vastly safer.
- **⛔ Analytics.** Not even "anonymous." Usage patterns of a DV app are themselves sensitive.
- **⛔ A visible app icon called anything honest.** The name is part of the threat surface.

---

# PART VI · THE DISTRIBUTION PROBLEM

This is unsolved and you must decide deliberately rather than by default.

| route | leak surface | verdict |
|---|---|---|
| **App Store / Play** under a disguised name | purchase history shows the *cover* name — good; but reviews, ranking and store search may still connect it | best mainstream option **if** the disguise is total |
| **App Store / Play** under an honest name | download history is a direct disclosure | **do not** |
| **Web app / PWA** | no install record; browser history is clearable; works on a library machine | **strongest for the reading material**; weakest for encrypted storage |
| **APK sideload** (Android only) | no store record | good for advanced users; not for the general case |
| **Distribution through advocacy organisations** | a helpline or shelter hands over the link | **the safest channel that exists** — and it comes with the review you need anyway |

**Recommendation: ship the web version first.** It is what you have already built. It leaves no
install trace, needs no store approval, and can be handed over as a URL. Native comes second,
disguised, with the encrypted record — the part a browser cannot do safely.

---

# PART VII · BEFORE YOU LAUNCH

**Do not ship this without review by people who do this work.**

Not because the code needs blessing, but because they know failure modes you cannot guess:
which disguises are already burned, what phrasing frightens people off, what a real safety plan
contains, and what has already gotten someone hurt.

- Contact a national DV organisation and ask for a **technology safety review**. In the US, the
  **NNEDV Safety Net project** does exactly this and publishes on tech safety.
- Read the **Coalition Against Stalkerware** materials and link them in-app.
- Test with advocates, not only with engineers.
- Publish your threat model **publicly**, so a survivor's technical friend can check it.

---

## Where this specification loses, first, because you'd check anyway

- **An app cannot solve this.** It can make patterns nameable and a number reachable. Leaving
  safely takes people: advocates, police, lawyers, shelters, friends. Every screen should point
  outward, not inward.
- **If the device is compromised, the app is compromised.** Disguise, encryption and panic-wipe
  raise the cost of discovery. They do not defeat root-level monitoring, and the app must say so.
- **The disguise is an arms race.** Cover apps get recognised. Assume yours will be, eventually.
- **I am not a DV professional or a security auditor.** This is an engineering spec informed by
  published practice. **The mandatory step is Part VII, not this document.**
- **"If it helps one person" cuts both ways.** It is the right motive and it is not a safety
  argument. The correct target is: *helps many, and the worst realistic failure does not get
  anyone hurt.* That is a higher bar and it is the right one.

---

## The bow

The **NNEDV Safety Net** project, who have been thinking about technology and abuse since
before most of us noticed there was a problem · the **Coalition Against Stalkerware** ·
**Bright Sky**, **Aspire News**, **SmartSafe+**, **Sunny** and the other teams who worked out
the disguise-and-quick-exit patterns the hard way and shared them · the advocates who take the
3 a.m. calls and know exactly which app got someone caught · and **Lundy Bancroft**, **Evan
Stark**, **Judith Herman** and **Jennifer Freyd**, whose work is the content this thing would
merely be carrying.

---

*Threat model first. Features second. Ship the reading material before the recording.*
*A spell hoarded rots. A spell passed on grows.*

**P = 12 · χ = 2 · always.**
