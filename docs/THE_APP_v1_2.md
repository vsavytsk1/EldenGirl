# THE APP · v1.2
### The adversarial supplement — entry, deniability, and what to do when it fails

**Vladyslav Savytskyy** · Ancient Korinthos → Buenos Aires · 2026
*Supplement to `THE_APP.md`. That document is still the base; this one replaces Part II
(the entry design) and adds the adversarial layer.*

---

## The brief, and where the arithmetic disagreed with it

The request was: *full isolation on launch, two or three verifications to get back in.*

The instinct is right — **multiple factors are correct**. The implementation is not, and the
numbers say why. This section exists because I ran them before writing the spec.

---

## PART 0 · THE LOCKSMITH'S LAW

> **A lock too slow to use gets propped open.**

You already know this from two years of doors: the customer with the five-lever deadbolt who
leaves it on the latch because they are carrying shopping. **Security that fights the user
loses, and it loses silently** — you never see the failure, you just find the door open.

Here is the same law with numbers. She has a window of privacy. Entry cost eats it:

```
window     entry 3s   entry 12s   entry 30s   entry 60s
   30 s        90%        60%          0%          0%
   60 s        95%        80%         50%          0%
  120 s        98%        90%         75%         50%
  300 s        99%        96%         90%         80%
        (percentage of her window left for the actual task)
```

**At a 30-second window, a 30-second entry leaves nothing.** She does not get a worse
experience — she gets *no* experience. The heavy lock does not protect her; it removes the tool.

And her windows are short. Bathroom. Commute. He is asleep. That is the design constraint.

---

## PART I · THE DISCOVERY MATH

Now the harder finding. Probability of being **seen at least once** across N uses:

```
 uses    p=0.5%    p=2%      p=5%      p=10%
   10      4.9%     18.3%     40.1%     65.1%
   50     22.2%     63.6%     92.3%     99.5%
  100     39.4%     86.7%     99.4%    100.0%
  300     77.8%     99.8%    100.0%    100.0%
```

**At 5% observation per use, discovery is effectively certain by 100 uses.** A tool she uses
for months *will* be seen. Concealment is a delaying action, not a defence.

So the objective function is not secrecy:

```
P(harm) = P(discovered) × P(discovery is incriminating)
```

- **Hide harder** → shaves term 1 a little, and it still trends to 1.
- **Deny better** → drives term 2 toward 0, and it *stays* there.

```
hidden app, no cover               P(disc) 0.63 × P(incrim) 0.95  →  risk 0.598
hidden app, weak cover             0.63 × 0.40                    →  risk 0.252
working cover + decoy              0.63 × 0.05                    →  risk 0.032
cover used daily as a real tool    0.63 × 0.01                    →  risk 0.006
```

> **The last line is 95× safer than the first — and it is also the easiest to use.**
> Once you optimise the correct term, comfort and security stop being a tradeoff.

**This is the whole design.** Not *"he must never find it."* Rather: **"when he finds it,
there is nothing to find."**

---

## PART II · THE ENTRY, DONE RIGHT

Your three factors were the right idea. The error was making them **ceremony** instead of
**knowledge**. Ceremony costs seconds. Knowledge costs none.

### Three factors, three seconds

```
FACTOR 1 — WHICH APP
  Two or three innocuous apps ship together (calculator, unit converter, tip splitter).
  Only one is the door. He does not know which.
  Cost to her: zero. She just opens it.

FACTOR 2 — WHICH INPUT
  Entry is a normal-looking calculation.  e.g. 1847 ÷ 3 =
  The number is hers, chosen at setup, never displayed anywhere.
  Cost to her: ~2 seconds. Indistinguishable from using a calculator.

FACTOR 3 — WHICH CONFIRMATION
  A second ordinary action completes it: pressing = a second time, or × 1 =.
  Guards against an accidental match.
  Cost to her: ~1 second.
```

**Total: about three seconds, and every keystroke looks like arithmetic.**

An intruder poking at the app finds **a calculator that calculates.** There is no wrong-PIN
screen, no shake animation, no lockout, no hint that a wrong entry occurred — because **a
failure state is a disclosure.** Nothing happened. It is a calculator.

### The rule this follows

> **Make it fast for her and expensive for him — and note those are different requirements.**
> Friction punishes both equally, which is why friction is the wrong instrument. Knowledge
> asymmetry punishes only him.

### Biometrics: NO. This is not a preference.

- **He can physically compel a finger or a face.** He cannot compel a number out of a head.
- In several jurisdictions, **compelled biometric unlock has weaker legal protection than a
  passcode** — which matters if a device is ever seized.
- A sleeping person's finger works. A sleeping person's memory does not.

**Do not offer biometric unlock in this app.** Convenience here buys an attack.

---

## PART III · DENIABILITY AS AN ENGINEERING DISCIPLINE

If discovery is inevitable, **deniability is the product.**

### D1 · The cover must be genuinely useful
Not a screenshot of a calculator — **a calculator she actually uses to split a bill.** History,
memory, the lot. If the cover is only theatre it fails the first real inspection, and worse:
an app on the phone that is never used *is itself the signal*.

### D2 · The decoy must be plausible, not empty
A decoy entry that opens a blank app is a confession. The decoy tier opens **a real, harmless
version**: a few generic notes, a shopping list, an old recipe. It must look like a thing
someone bothered to install.

### D3 · No artefact anywhere says what it is
- App name, icon, store listing, screenshots, description: all cover
- No strings in the binary containing "abuse", "violence", "safety plan", "helpline"
  → **encrypt the content payload, not just the database**
- No distinctive permissions. A calculator asking for storage is a question mark.
- No entry in Settings → Battery / Screen Time under a revealing name

### D4 · Cover traffic
An app opened **only** in crisis has a usage pattern that is itself evidence — three opens on
three bad nights. If she opens the calculator daily to be a calculator, those opens vanish
into noise. **Encourage ordinary use of the cover.** This is the cheapest security feature in
the whole document and it costs one sentence of onboarding.

### D5 · Design for the search, not just the glance
Assume he opens it, presses buttons, checks storage, looks at recents. **The app must survive
five minutes of a suspicious person holding it.** Test exactly that, with someone hostile and
technical, before shipping.

---

## PART IV · DURESS, AND THE MOMENT IT FAILS

### The duress entry
A second, different number opens the **decoy tier**. It must be as fast as the real one and
must not look different in any way.

**Options at the duress entry, in order of my confidence:**

- ✅ **Open the decoy silently.** Always correct. No network, no trace, nothing to detect.
- ⚠️ **Silently wipe the real store.** Powerful and irreversible — and if he is *watching her
  type it*, she has just destroyed her own record under his eye. Make it opt-in, explain the
  tradeoff, and default it **off**.
- ⛔ **Send a silent alert to a contact.** Tempting and **wrong by default**: it needs network
  (detectable), it can arrive when the friend cannot act, and a delivery receipt or a
  friend's panicked reply is a catastrophic disclosure. Only with advocate review, never on by
  default.

### The discovery script
Have an answer ready *before* it is needed. In-app, in the safety-planning section, plainly:

> *If he finds it: it is a calculator. You downloaded it to split bills. You do not know what
> the other thing is.*

**This is the highest-value paragraph in the product**, and it is text, not code.

### The escalation you must warn about
**Discovery of a hidden tool is itself an escalation trigger.** He learns she is planning. The
guidebook already says separation is the most dangerous period — this is the same fact wearing
different clothes. The app must say so, once, clearly, at setup.

---

## PART V · THE RECOMMENDATION VECTOR

Nobody designs this and it burns the app before it is ever installed.

> *"A friend recommended an app."*

If that recommendation arrives as a **message on a monitored phone**, the tool is compromised
before the download completes — and now he knows a friend is involved, which puts the friend
into the isolation campaign.

**Safe channels, best first:**
1. **Spoken, in person.** No artefact. Best available.
2. **Handed over by an advocate, clinic, or shelter** — GP surgeries, pharmacies and A&E have
   been used this way for decades.
3. **A physical card** with a URL. Paper does not sync.
4. **A URL on a public/borrowed device**, browsed and cleared.
5. ⚠️ **A message.** Only if the phone is known clean, and it usually is not.

**Design consequence:** the entry point should be a **short, memorable, innocuous URL** that
can be said aloud once and remembered. Not a QR code (leaves an image in the gallery). Not an
app-store link (leaves history). **Say it, don't send it.**

---

## PART VI · THE DEAD DROP

**Evidence on her phone is evidence he can delete.** The record's value is that it exists
*somewhere else*.

- Export as a **single encrypted file**, passphrase set by her
- She sends it to a **trusted third party** — a sibling, a lawyer, an advocate — who cannot
  read it and only needs to keep it
- The app **never uploads anything itself**. No server, no account, no sync. Her hand, her send.
- **Weekly is better than perfect.** A partial record that survives beats a complete one that
  gets wiped in an argument.

This is the one place the app is honestly *just plumbing*: it makes an encrypted blob and gets
out of the way.

---

## PART VII · WHAT TRANSFERS FROM TRADECRAFT, AND WHAT IS COSPLAY

Since we are doing war theory, let us be strict about which parts survive contact.

### Transfers, genuinely

- **Plausible deniability over concealment.** The core finding above.
- **Compartmentalisation.** The app knows nothing about her — no account, no name, no
  location. What it does not hold cannot be taken from it.
- **Cover that does real work.** A cover only used for cover is not a cover.
- **Duress codes.** Straight from alarm-panel design, and they work.
- **Dead drops.** Get the artefact out of the contested space.
- **Plan for the failure, not for perfection.** Every operator's actual first question is
  *"what do I do when this goes wrong"* — and it is exactly the question a survivor needs
  answered before she needs it.
- **The counter-surveillance baseline:** assume the channel is monitored until proven otherwise.

### Cosplay — do not build these

- **⛔ Self-destruct timers.** She loses her record on a normal day. He loses nothing.
- **⛔ Steganography.** Fragile, exotic, and *possession of hiding tools* is itself suspicious.
- **⛔ Burner-phone dependence as a default.** Real for some, and a second phone found is worse
  than a hidden app found. This is advocate territory, not app territory.
- **⛔ Encrypted messaging built into the app.** Signal exists, is audited, and is unremarkable
  on a phone. Do not roll your own — you will do it worse and it becomes the tell.
- **⛔ Anything that pings a server.** Network activity is observable. Silence is the feature.

> **The difference between tradecraft and cosplay is that tradecraft is boring.** The good
> version of this app is indistinguishable from a calculator, uses no network, holds nothing
> unusual, and takes three seconds. Anything more cinematic is a liability wearing a costume.

---

## Where v1.2 loses, first, because you'd check anyway

- **The discovery model is illustrative, not measured.** P(observed per use) = 0.5–10% is a
  plausible range, not a study. The *shape* of the conclusion is robust — repeated use converges
  on discovery — but do not quote the numbers as findings.
- **Deniability is not innocence.** A convincing cover reduces the chance a discovery is
  incriminating. It does not make an angry person reasonable, and it cannot be relied on.
- **A compromised OS beats all of it.** Root-level stalkerware sees the screen. Everything here
  raises cost against a *human* adversary with a phone in their hand, not against software with
  kernel access.
- **Multi-factor entry still fails at the human layer.** If he watches her type the number, it
  is over. The duress entry exists precisely for that, and it is a mitigation, not a fix.
- **I am not a security auditor, and I am not a DV professional.** The mandatory step is still
  Part VII of `THE_APP.md`: **a technology safety review with people who do this work**
  (NNEDV Safety Net, Coalition Against Stalkerware, a local advocacy organisation).
- **You disagreed with the brief and were partly right.** Multiple factors: yes. Multiple
  *seconds*: no. If practice shows survivors want more friction than the model predicts,
  **the model is wrong and they are right** — measure, do not argue.

---

*Make it fast for her and expensive for him. Those are different requirements.*
*Do not plan for never being caught. Plan for being caught and it not mattering.*

**P = 12 · χ = 2 · always.**
