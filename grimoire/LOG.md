# THE LOG
### The build journal — documentation is the exorcism (Path VIII)

*The monkey brain is exhausted and scared. It forgets what it did and why. So we write
it down: what was built, what was decided, what was learned. A session unlogged runs as
a background process forever.*

**P = 12 · χ = 2 · always.**

---

## 2026-07-23 · Day One · the repo, the gates, the first two sims

**Where it started:** a clean, empty public repo — `github.com/vsavytsk1/EldenGirl` — and
a stack of concept docs. The mission: a safety-first coercive-control recognition toolkit,
cloneable, so the girlies have an easier time.

**What got built, in order (the spec's own sequencing — gates first, always):**

1. **The gates, before any product code.** `gates/run_gates.py` — the eleven safety
   invariants (G1–G11), standard-library only, wired into a `Makefile`, a **pre-commit
   hook**, and **GitHub Actions CI**. They *fail* the build; they never warn.
2. **The three tiers scaffolded.** `docs/` (public reading), `android/` (a genuine
   calculator cover with FLAG_SECURE, zero-permission manifest, backup exclusion, the
   no-learning text wrapper), `ios/` (codex-only, snapshot obscuring). They share a
   threat model and nothing else.
3. **The concept lab, served from `docs/`.** GitHub Pages only allows `/(root)` or
   `/docs` — so the concept site lives in `docs/`, next to the published spec.
4. **The grimoire + `MONSTER_MANUAL.md`** — the core scroll, the twelve tactics with
   move / tell / clean line / counter / grounded root.
5. **The first Spini Sim** — the sourced statistics as a solemn dot-field, each dot a
   person, no score, no reward on a death toll. Front-paged the README with the case for
   why the training ground is necessary.

**Live at the end of the day (all verified, all zero-write):**
- `vsavytsk1.github.io/EldenGirl/` — the hub
- `/training-ground.html` — the 12 monsters (v1.2)
- `/spini-sim.html` — the scale of it (v1)

**Decisions that matter (so future-me does not re-litigate them):**
- **GitHub Pages folder is `/docs`, not `/lab`.** GitHub offers no arbitrary folder. The
  duplicate `web/` tier was removed so two copies of a safety-critical file cannot drift.
- **Cover identity is a build parameter with no default.** Placeholders only in the repo;
  the disguise is defeated by a search engine, so it never ships in a tracked file.
- **`docs/` and `grimoire/` are public by design** — exempt from the lexicon/identity
  gates (G3/G11) but still bound by the zero-write law (G4). The disguised tiers
  (`android/`, `ios/`) are what those gates guard.
- **Every statistic ships with its source or shows `(sourcing)`.** No fabricated numbers,
  ever. `grimoire/monsterStats.md` (fully cited research) → `grimoire/SPINI_SIM.md` (the
  data scroll) → the sim.

**What the monkey brain learned (curses met, and their counters):**
- `python` alone printed nothing in this shell — use the **full interpreter path**
  (Curse 18, the Windows devour). Logged in `/memories`.
- GitHub Pages deploys on a **separate ~30–90s job**; the URL 404s if checked too soon
  (Curse 29, deploy lag). Watch it go green, then verify.
- The GitHub web UI **caches** — the repo/actions pages showed stale "empty" / "run #1"
  long after the push landed. Trust `git ls-remote` and the rev hashes, not the cache.
- Gate false-positives were fixed **on the gate, never by weakening the code**: G3 now
  strips comments and skips build-only files (it models what *ships*); G11 excludes XML
  schema/DTD URLs and the project's own `*.github.io` host.

**Still human-owned, not for a machine (v1.5 Part IV):** the android entry sequence, the
decoy tier, the panic wipe (key-before-data ordering), the encrypted record. And the
non-negotiable before any launch: the **advocate / technology-safety review** (Part VII).

**Commits today:** `ec4c4f0` → `d81216d` → `b6b73bd` → `a8db7ed` → `6788943` →
`4db8f69` → `2e6e656`. Gates green on every one.

> *A spell hoarded rots. A spell passed on grows.*
> *Green means nothing broke. It does not mean it works.*

**P = 12 · χ = 2 · always.**
