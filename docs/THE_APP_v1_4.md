# THE APP · v1.4
### The ephemeral architecture — write nothing, download again

**Vladyslav Savytskyy** · Ancient Korinthos → Buenos Aires · 2026
*Supplement to `THE_APP.md`, `v1_2` (adversarial) and `v1_3` (platform).*

---

## The idea, and why it is the best one in the whole spec

> **Store nothing. When it is gone, it is actually gone. Download it again in twenty seconds
> and keep training.**

This solves a problem the earlier versions could only mitigate. Deniability made discovery
survivable; **ephemerality makes discovery empty.** There is no encrypted blob to explain, no
"what is this file", no forensic artefact at all — because nothing was ever written.

And it works *only* because of a property we already had and had not exploited: **the training
material is public.** Losing it costs nothing. That is what makes the redownload the erase.

---

## PART I · "SECURE DELETE" DOES NOT EXIST ON A PHONE

This needs to be understood before the design makes sense.

NAND flash **writes in pages but erases in blocks**, and a wear-levelling controller decides
where bytes physically land. When the OS asks to overwrite logical sector X, the controller
writes a **new physical page** and marks the old one stale. **The original bytes are still
there**, in a block no software can address.

```
storage      over-provisioned spare (~7%)     visible to the OS?
  64 GB              ~4.5 GB                        no
 128 GB              ~9.0 GB                        no
 256 GB             ~17.9 GB                        no
 512 GB             ~35.8 GB                        no
```

**You cannot reach those blocks. No app can.** This is exactly why NIST SP 800-88 recommends
**cryptographic erase** for flash media rather than overwriting — the overwrite advice is a
holdover from spinning rust and it does not transfer.

### The three architectures, by what they leave behind

```
architecture                          writes         after "deletion"           verdict
plain app, deletes files on exit      megabytes      recoverable (unlink ≠ erase)  BAD
encrypted store + crypto-shred key    KB ciphertext  noise without the key         GOOD
ephemeral: never writes at all        0 bytes        nothing to recover            BEST
```

**A delete button is a comforting lie. Never writing is the truth.**

---

## PART II · THE SPLIT

Here is the thing the earlier versions got wrong by treating this as one product: **the two
halves have opposite storage requirements.**

| | TRAINING + CODEX | THE RECORD |
|---|---|---|
| content | **public** | **private, irreplaceable** |
| cost of loss | zero — redownload | catastrophic |
| storage need | **none** | must persist |
| correct design | **fully ephemeral, zero writes** | **must not live on the phone at all** |

> **They should never have been one binary.** The training tier writes nothing and is
> disposable. The record tier is encrypted and leaves for the dead drop as fast as possible.
> Different products, different rules, possibly different platforms.

---

## PART III · THE EPHEMERAL TIER — ENGINEERING IT

### Ship it as a web app. That is the answer.

You already built it. It is a single HTML file with zero dependencies and no network calls.
As a **PWA that refuses to be installable**, it is the cleanest possible version of this idea.

```
NO service worker          — a cache is persistence wearing a disguise
NO localStorage            — survives the tab
NO sessionStorage          — survives a reload
NO IndexedDB / WebSQL      — survives everything
NO cookies                 — obvious
NO "add to home screen"    — an installed PWA leaves an icon and a manifest
NO manifest.json at all    — makes the browser want to install it
```

**Everything lives in JavaScript variables.** Close the tab and the heap is freed. Streaks,
score, progress, the lot — all gone, and none of it mattered.

**One HTML file, served over HTTPS, that is the whole product.**

### Native, if you must

If the record tier forces a native app, the training tier inside it still writes nothing:

```
Android : no SharedPreferences, no Room, no files.
          add android:noHistory="true" on the activity
          FLAG_SECURE (blocks screenshots and the recents thumbnail)
          android:allowBackup="false"  ·  cacheDir must stay empty
iOS     : no UserDefaults, no Core Data.
          nothing in Documents/, nothing in Caches/
          obscure the snapshot on backgrounding
```

**Test the claim, do not assume it.** Run the app for an hour, then diff the app sandbox
before and after. **If a single byte changed, you have not built an ephemeral app** — you have
built a normal app with good intentions.

---

## PART IV · WHAT THE PLATFORM WRITES ANYWAY

The app writing nothing does not mean the *system* wrote nothing. Be honest about the residue:

| trace | who writes it | mitigation |
|---|---|---|
| **browser history** | the browser | private/incognito tab; clear history |
| **DNS cache / resolver logs** | OS + ISP | none at app level — assume the visit is known |
| **router / ISP records** | the network | none. **the domain must be innocuous.** |
| **screenshots** | the user, or malware | `FLAG_SECURE`; teach her not to screenshot |
| **RAM at time of seizure** | physics | out of scope for this adversary |
| **the URL in autocomplete** | the browser | short URL, incognito, clear |

> **The strongest residue is the domain name.** If she visits `escape-abuse-now.org` the
> hostname is in the router log, the DNS cache and the autocomplete regardless of how
> ephemeral your JavaScript is. **The domain is part of the cover and must be as boring as the
> app icon.** Something like a plausible utility or recipe site — and the content at the root
> should actually be that thing.

---

## PART V · RE-ACQUISITION — THE REDOWNLOAD IS THE ERASE

If it must be re-obtainable in seconds, that path is now part of the threat model.

**Requirements:**
1. **Short, sayable, memorable URL.** Spoken once, remembered. No QR code (leaves an image in
   the gallery), no link in a message (v1.2, Part V).
2. **The root of the domain is a real, boring site.** The tool lives at a path she remembers.
   Anyone who types the bare domain finds a recipe collection.
3. **Loads in seconds on bad signal.** One file, no fonts, no CDN, no analytics. Ours is under
   40 KB — that is a second on 3G and it works on a library machine.
4. **Mirror it.** Multiple hosts, plus the raw file on a code host. Cheap insurance against
   takedown, expiry, or a blocked domain.
5. **She can save the file itself.** One HTML file works from a downloads folder, an SD card,
   an email to herself, a USB stick. **It is portable in the strongest sense: no install, no
   network, no dependency.**

> **This is the property that makes the whole design work.** A file that runs anywhere, holds
> nothing, and can be replaced in twenty seconds is not something anyone can take from her.

---

## PART VI · THE RECORD TIER — CRYPTO-SHRED, THEN LEAVE

The one part that cannot be ephemeral, handled correctly:

```
1. WRITE little            each entry encrypted individually, AES-GCM, key in Keystore/Secure Enclave
2. EXPORT early            prompt for the dead-drop export weekly, not monthly
3. SHRED the key           panic wipe destroys the KEY, not the file
                           → the ciphertext becomes noise no controller can un-noise
4. THEN unlink             cosmetic, but it tidies the visible filesystem
```

**The panic wipe must destroy the key first and the data second.** Reversing that order means
that if the process is interrupted — battery dies, he takes the phone — you may be left with
readable data and no lock. **Key first. Always.**

And per v1.2: **weekly export beats a perfect archive.** A partial record living at a
sibling's address survives an argument. A complete one on the phone does not.

---

## PART VII · WHAT THIS BUYS, HONESTLY

**Discovered mid-session.** The tab is open. Quick exit closes it, the heap is freed, and there
is no history entry if it was a private tab. **Nothing persists to be found later.**

**Phone examined a week later.** Nothing to find. No app, no file, no encrypted blob, no
"what's this". The best possible outcome of an inspection is that it is *boring*, and this is
the only architecture that reaches genuinely boring.

**Phone forensically imaged.** No app artefacts, because none were written. Browser and network
residue may remain — that is what the boring domain is for.

**Phone actively monitored by stalkerware.** ⛔ **Ephemerality does not help.** The screen is
being captured live. Nothing in this document defeats that, and v1.3 Part IV says so: **inform,
never remove, and use a device he has never touched.**

---

## Where v1.4 loses, first, because you'd check anyway

- **Ephemeral ≠ invisible.** It defeats *forensic recovery*. It does not defeat *live
  observation*, whether that is a person behind her or software on the device.
- **The browser is not fully under your control.** Private mode reduces traces; it does not
  eliminate them, and behaviour differs across browsers and versions.
- **The domain is the weak point and it is not solvable in code.** It needs a boring name, a
  real cover site at the root, and mirrors — and the DNS/ISP record still exists.
- **Verify the zero-write claim, do not assert it.** Diff the sandbox. Frameworks write caches
  you never asked for; a single stray `SharedPreferences` from a library breaks the property
  silently.
- **RAM forensics exists** and is out of scope here. It requires seizure and tooling well
  beyond the adversary this document is designed against — say so rather than implying more.
- **"Just download it again" assumes she can reach the internet unobserved.** Sometimes she
  cannot. That is why the single-file-on-a-USB-stick path matters as much as the URL.

---

*You cannot overwrite flash. You can only never write, or destroy the key.*
*Public content should be disposable. Private content should not be on the phone.*
*The redownload is the erase.*

**P = 12 · χ = 2 · always.**
