# EldenGirl

### A safety-first, coercive-control recognition toolkit — build it, fork it, improve it.

**MIT.** Open source on purpose: in this category, *"trust us"* is not an acceptable security
model. A survivor should be able to have someone technical read every line and verify the thing
does exactly what it claims — and nothing else.

> **A badly designed app in this space does not fail to help. It gets someone hurt.**
> The threat model comes before the feature list. Read [`docs/THE_APP.md`](docs/THE_APP.md) before you write a line of code.

---

## If you are not here to build

If you need help right now, an app is not the fastest path — a person is. Advocates do safety
planning for free and know things no piece of software can:

| region | line |
|---|---|
| US | 1-800-799-7233 |
| UK | 0808 2000 247 |
| ES | 016 |
| AR | 144 |
| GR | 15900 |
| EU | 116 006 |

**Your phone may not be private.** If someone else has access to your device or your accounts,
consider reading this on a library or a friend's device. See the
[Coalition Against Stalkerware](https://stopstalkerware.org/).

---

## What this repository is

Not one app. **Three tiers with different rules, sharing a threat model and nothing else** — no
code, no storage, no release cycle. (`docs/THE_APP_v1_5.md`, Part 0.)

| tier | what it is | writes | platform | ship |
|---|---|---|---|---|
| [`docs/`](docs/) | the concept site + published spec — pure text + clicks | **0 bytes** | any browser | **first — it's the Pages site** |
| [`android/`](android/) | the encrypted record + dead-drop export | KB ciphertext | Android | second |
| [`ios/`](ios/) | the codex, read-only | 0 bytes | iOS | last, possibly never |

## The concept lab lives in `docs/` — how we test ideas in the open

[`docs/`](docs/) is the front door, the workshop, **and the live site**
(<https://vsavytsk1.github.io/EldenGirl/>). Every concept begins here as **pure,
dependency-free HTML + JS — text and clicks first** — so the community can open it, read every
line, and judge the idea and its path *before* any UI dopamine layer goes on top, and long
before anything native. Only once a concept holds does it earn the goblin layers (the juice, the
creature, the game feel), all of it later wrapped in the secure, disguised app. The published
specification lives here too, because it is meant to be read publicly (Part VII).

**This is a monolith on purpose — no branches, no release trains for the concepts.** A concept
nobody can read is a concept nobody can trust. Everything in `docs/` obeys the same zero-write
law as the rest (G4 scans its HTML/JS): no storage, no network, no install trace. It is served
as a static site (GitHub Pages) and handed over as a URL.

- **It is already live:** repo **Settings → Pages → Deploy from a branch → `main` / `/docs`**
  (GitHub Pages only serves `/(root)` or `/docs`, which is why the concept site lives in `docs/`).
- Add a new concept by dropping a self-contained `.html` file into `docs/` and linking it from
  [`docs/index.html`](docs/index.html). No build step. The gates run on it automatically.

## What ships first

The [`docs/`](docs/) site. It leaves no install record, needs no store approval, runs on a
borrowed machine, and can be handed over as a spoken URL. It holds no user data, so there is
nothing to leak. Native comes second — disguised, with the encrypted record a browser cannot
store safely.

---

## The order of work is not negotiable

```
1  the gates       — executable safety invariants, before a line of product code
2  docs/           — the concept site, zero writes, ships immediately
3  android/ cover  — a calculator that is genuinely a calculator. no real tier yet.
4  android/ entry  — three factors, three seconds, no failure state
5  android/ record — encrypted, weekly export prompt, crypto-shred, dead drop
6  ios/            — codex only. revisit the record tier only if the name blocker moves.
```

## The gates come first, and they fail the build

Ten commandments in prose are advisory. When a machine writes the code — or a hurried human at
1 a.m. — the invariants hold only where the build **fails** without them. The regression here
is not toward malice; it is toward *professionalism*: crash reporting, analytics, a networking
layer, "persist so the user doesn't lose progress." Every one of those is correct everywhere
except here.

```
make gates        # runs everything, exits non-zero on any failure
make gates-fast    # the subset that runs in <5s, for the pre-commit hook
make hooks         # install the pre-commit hook
```

See [`docs/THE_GATES.md`](docs/THE_GATES.md) for what each of G1–G11 checks and which promise it
protects. **Green means nothing broke. It does not mean it works.**

---

## The cover identity is not in this repository, and never will be

The disguise is defeated by a search engine, not an attacker. A public repo plus a canonical
cover name is a five-minute search away from this document. So the cover **name, package, icon
and domain are build parameters with no default** — the distributing organisation chooses its
own, builds, and publishes its own hash. Twenty shelters ship twenty different calculators;
recognising one teaches you nothing about the rest. (`docs/THE_APP_v1_5.md`, Part I.)

**Do not commit a candidate cover name — not in code, not in a test, not in a commit message,
not in this README.**

## Before anyone launches this

Do not ship without a **technology safety review** by people who do this work (US: the NNEDV
Safety Net project). They know failure modes you cannot guess: which disguises are already
burned, what phrasing frightens people off, what a real safety plan contains, and what has
already gotten someone caught. Gates verify the code matches the spec. **They cannot tell you
the spec is right.** (`docs/THE_APP.md`, Part VII.)

---

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first — including the part about how version control
publishes your real name and email.

*Threat model first. Features second. Ship the reading material before the recording.*
*A spell hoarded rots. A spell passed on grows.*

**P = 12 · χ = 2 · always.**
