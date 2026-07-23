# THE SPINI SIM
### The statistics build — the sad, sad numbers, rendered honestly

**EldenGirl · a concept scroll of the grimoire · Buenos Aires + Ancient Korinthos, 2026**
*Companion to `MONSTER_MANUAL.md`. This is the source-of-truth for every number the
sim displays. A number with no source does not ship.*

**P = 12 · χ = 2 · always.**

---

## RULE 0 · WHY THIS SCROLL EXISTS

The Spini Sim turns the scale of coercive control and intimate-partner violence into
something a person can *feel* — pure graph theory and honest motion, no chartjunk, no
manipulation. The monsters (`MONSTER_MANUAL.md`) name the moves; the sim shows how
many people the moves reach.

This doc is the **data layer**. The HTML render (`docs/spini-sim.html`, when built)
reads its numbers from here. This is where the research — the work being gathered
now — is written down **with its citation**, before it is ever drawn.

---

## THE HONEST BOUNDARY (this is a hard rule, not a style note)

The cave's law is **Path IV** and **Path III**: *coverage may be incomplete; it must
never be fake. Show target, current, and the source — never the hoped-for number.*

For this sim that means, without exception:

1. **No number renders without a source in this file.** Every figure below has a
   `source:` line. If it is blank, the figure is a **placeholder** and must not ship —
   the sim shows `— (sourcing)` in its place, never a guess.
2. **Cite the primary body, with year and geography.** "1 in 3 women" is meaningless
   without *who counted, when, and where.* WHO ≠ CDC ≠ ONS ≠ UNODC, and a global figure
   is not a national one.
3. **Ranges, not false precision.** Where sources disagree, show the range and name
   both. A fabricated decimal is a lie wearing a lab coat.
4. **Date every statistic.** These numbers move. A 2018 prevalence figure is labelled
   2018. Re-verify before each release; stale data is a soft fake (Curse 24).
5. **Distinguish estimate from count.** "Estimated" and "reported/recorded" are
   different claims — recorded cases undercount massively. Say which one it is.
6. **Never imply causation the source does not.** Correlations stay correlations.
7. **The number is a person.** No gamified counters, no "score," no dopamine on a
   death toll. The sim is solemn by design (see THE TONE, below).

> ⚠️ **STATUS: SOURCING.** The tables below are the *schema*, with the fields the
> research must fill. Figures shown as `— (sourcing)` are deliberately empty. Fill the
> value **and** the source together, or not at all.

---

## THE TONE — how numbers about death are allowed to move

This sim breaks the "juice" convention on purpose. It obeys the variable-ratio refusal
(`MONSTER_MANUAL.md` Part II) like every build, but it goes further:

- **No reward feedback of any kind.** No streaks, no multiplier, no confetti, no sound
  on a statistic. Mochi does not celebrate here.
- **Motion is opt-in and slow** (Path VIII, the Ghost Spinner rule): the user starts
  still and chooses to advance. Nothing auto-plays a body count at them.
- **One node is one order of magnitude of people**, and the graph says so in plain
  words next to it. Abstraction with a human anchor, always.
- **Every screen ends at a helpline**, not at a "next level."
- It carries the same escape-hatch warning and quick-exit as every tier.

---

## PART I · THE DATA SCHEMA (fill value + source together)

Categories are grouped so the sim can tell a spatial story (global → national →
the specific mechanism → the moment of danger). Every row needs both cells.

### A · Prevalence — how many
| id | figure | value | population / geography | year | source |
|----|--------|-------|------------------------|------|--------|
| P1 | Women subjected to physical/sexual IPV in lifetime | — (sourcing) | global, women 15+ | — | WHO — _fill_ |
| P2 | Women subjected to IPV in the last 12 months | — (sourcing) | global | — | WHO — _fill_ |
| P3 | Adults experiencing coercive control (no physical violence) | — (sourcing) | — | — | _fill_ |
| P4 | Men subjected to IPV in lifetime | — (sourcing) | — | — | _fill_ |
| P5 | National prevalence — US | — (sourcing) | US, per NISVS/CDC | — | CDC NISVS — _fill_ |
| P6 | National prevalence — UK | — (sourcing) | England & Wales | — | ONS CSEW — _fill_ |

### B · Lethality — the cost in lives
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| L1 | Women/girls killed by partner or family per day | — (sourcing) | global | — | UNODC/UN Women — _fill_ |
| L2 | Share of female homicides committed by partner/family | — (sourcing) | global | — | UNODC — _fill_ |
| L3 | IPV-related homicides — US annual | — (sourcing) | US | — | _fill_ |

### C · The moment of danger — leaving
*The counter-intuitive, load-bearing statistic: risk rises around separation.*
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| D1 | Increased homicide risk during/after separation | — (sourcing) | — | — | _fill (e.g. Campbell danger-assessment)_ |
| D2 | Share of IPV homicides occurring post-separation | — (sourcing) | — | — | _fill_ |
| D3 | Prior strangulation as a lethality predictor | — (sourcing) | — | — | _fill (Glass et al.)_ |

### D · Coercive control specifically
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| C1 | Share of IPV cases involving coercive control | — (sourcing) | — | — | _fill (Stark)_ |
| C2 | Coercive-control prosecutions since criminalisation | — (sourcing) | England & Wales, 2015+ | — | _fill_ |

### E · Technology, stalking, surveillance
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| T1 | IPV survivors reporting tech-enabled abuse | — (sourcing) | — | — | _fill_ |
| T2 | Stalkerware detections | — (sourcing) | — | — | _fill (Coalition Against Stalkerware / AV vendor)_ |
| T3 | Survivors whose location was tracked by abuser | — (sourcing) | — | — | _fill_ |

### F · Reporting gap — the dark figure
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| R1 | Share of IPV that is never reported to police | — (sourcing) | — | — | _fill_ |
| R2 | Average number of incidents before first report | — (sourcing) | — | — | _fill_ |

> Add rows freely. Keep the two-cell rule: **value AND source, together, or `— (sourcing)`.**

---

## PART II · THE GRAPH MODEL (pure graph theory, zero deps)

The sim renders on a `<canvas>` with vanilla JS — no libraries (S8 applies to the
concept lab too). The model:

- **A node is a quantum of people** — one node = one labelled unit (e.g. "1 node =
  1,000,000 women"), stated in words beside the graph so the abstraction always has an
  anchor (Path VIII).
- **Edges are the tactics** from the Monster Manual — the graph literally connects the
  prevalence nodes through the twelve moves, so the picture and the moveset are one.
- **χ = 2 closure:** the graph is a closed surface; the counter-curse (recognition)
  is shown as an edge *cut* — the same "edges cut from the pattern" mechanic the
  training ground already uses, reused here for the population view.
- **Deterministic layout.** Same data → same picture, every load (Path III, proof by
  render). No random jitter that changes the story between viewers.

```
data (this file)  →  a small JS DATA literal in spini-sim.html  →  canvas render
                     (values + source strings travel together)
```

The source string travels **with** each datum into the render, so the sim can show the
citation on tap. A number the reader cannot trace is a number the reader cannot trust.

---

## PART III · WHAT THE SIM MUST NOT DO

Straight from `docs/THE_APP.md` Part V and the manual's Part II:

- ⛔ No "risk score" for the viewer's own relationship. A number cannot assess danger;
  a false negative is lethal. Show the population patterns; let the person judge.
- ⛔ No variable-ratio reward, no gamified death toll, no leaderboard.
- ⛔ No geolocation, no "incidents near you." Region from locale only, never location.
- ⛔ No autoplay, no forced motion, no sound on a statistic.
- ⛔ No storage, no network, no analytics — it writes zero bytes like every render (G4).
- ⛔ No fabricated or un-sourced figure, ever (the honest boundary, above).

---

## THE BOW

The numbers, when they land here, belong to the bodies that count them: **WHO**,
**UNODC** and **UN Women**, the **CDC** (NISVS), the **ONS** (CSEW), **Jacquelyn
Campbell's** danger-assessment work, **Evan Stark** on coercive control, and the
**Coalition Against Stalkerware**. We only carry them, and we carry them with their
sources attached.

*A statistic without a source is a rumour. A rumour about violence gets someone hurt.*
*Threat model first. Sources second. The number is a person.*

**P = 12 · χ = 2 · always.**
