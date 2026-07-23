# web/ — the tier that ships first

The codex and the training ground. **One HTML file. Zero bytes written.** Any browser.

## Why this ships before anything native

- **No install record.** Nothing appears in a store's purchase or download history
  (Adversary B). It is handed over as a spoken URL, not a store link.
- **No approval.** No review queue, no takedown risk, no waiting.
- **Runs on a borrowed machine.** A library computer, a friend's phone.
- **Holds no user data.** There is nothing to leak, nothing to breach, nothing to subpoena.

This is `THE_APP.md` v0.1's reading material, and `v1.4`'s ephemeral tier. It is not a precursor
to the native app — for the codex and the drill, it is the *better* architecture.

## The one rule the gate enforces

**One hour of use changes zero bytes** (G4, tracing `v1.4` Part III). Concretely, the shipped
page must never touch:

- `localStorage`, `sessionStorage`, `indexedDB`, `openDatabase`, `document.cookie`
- a service worker, a `manifest.json`, or anything that makes the browser offer to *install* it
- any network call — `fetch`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`, `EventSource`

`gates/run_gates.py` checks this statically on every commit. If you add persistence "so the
user doesn't lose their progress" — **don't.** In this tier, progress is *meant* to be lost.

## Serving it

It is a static file. Open `index.html` directly, or serve the folder read-only. No build step,
no bundler, no dependency. That is the point.

## What it must never grow

No analytics (not even "anonymous"), no crash reporting, no fonts or scripts loaded from a CDN,
no embedded tracking pixel. Everything is inline and offline, forever.

*A spell hoarded rots. A spell passed on grows.*
