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

> ✅ **STATUS: SOURCED (first pass, 2026-07).** The tables below are filled from
> `monsterStats.md`, every figure with its body, year, and geography. Re-verify before
> each release; these numbers move. Any future row with no source stays `— (sourcing)`
> and does not ship.
>
> **Do not conflate the two headline numbers:** "1 in 3 / 736M" (all women 15+,
> including non-partner sexual violence) and "27%" (ever-partnered women 15–49, IPV)
> come from the *same* 2018 WHO exercise but measure *different populations*.

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
| P1 | Women who have experienced physical/sexual IPV or non-partner sexual violence in their lifetime | ~1 in 3 (**736 million**) | global, women 15+ | WHO 2018 est. (pub. 2021) | WHO Violence Against Women Prevalence Estimates 2018 |
| P2 | Lifetime physical/sexual **IPV** | **27%** (UI 23–31%) | ever-partnered women 15–49, global | WHO 2018 (pub. 2021) | WHO VAW Prevalence Estimates 2018 |
| P3 | **Past-year** IPV | **13%** (UI 10–16%) | ever-partnered women 15–49, global | WHO 2018 (pub. 2021) | WHO VAW Prevalence Estimates 2018 |
| P4 | "Starts early" — already experienced IPV | **~1 in 4** (24–26%) | young women 15–24, global | WHO 2018 (pub. 2021) | WHO VAW Prevalence Estimates 2018 |
| P5 | Non-partner sexual violence | **6%** (UI 4–9%, ~1 in 17) | women 15–49, 137 countries | WHO 2018 (pub. 2021) | WHO VAW Prevalence Estimates 2018 |
| P6 | Lifetime sexual assault since age 16 | **25.6%** (~1 in 4) | adult women, England & Wales | YE March 2025 | ONS Crime Survey for England & Wales (CSEW) |
| P7 | Experienced physical violence, sexual violence, or threats in adulthood | **1 in 3**; sexual violence incl. rape **1 in 6** | women, EU-27 (114,023 interviewed) | 2024 | Eurostat / FRA / EIGE Gender-Based Violence Survey |
| P8 | Partner violence or abuse since age 15 | **27%** (2.7 million) | women, Australia | ABS PSS 2021-22 | ABS Personal Safety Survey |

> **Regional spread (lifetime IPV, WHO 2018):** highest in the WHO African & South-East
> Asia regions (~33% each) and Eastern Mediterranean (31%); by SDG subregion up to **51%
> in Melanesia**; lowest **16% in Southern Europe.** Higher recorded rates often signal
> better data and awareness, not more violence — say so on the chart.

### B · Lethality — the cost in lives
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| L1 | Women/girls killed by intimate partner or family per day | **137 per day** (~1 every 10 min) | global | 2024 (pub. Nov 2025) | UNODC / UN Women Femicides report |
| L2 | Women/girls killed by partner/family in the year | **~50,000** (60% of all female intentional killings) | global | 2024 | UNODC / UN Women |
| L3 | The asymmetry — victims killed by partner/family | women **60%** vs men **11%** | global | 2024 | UNODC / UN Women |
| L4 | Highest regional femicide rate | Africa **3.0 per 100,000** (~22,600 victims) | Africa | 2024 | UNODC / UN Women |
| L5 | Reporting collapse (lower-bound caveat) | only **37 countries** reported (from 75 in 2020); motive missing in ~40% | global | 2023 | UNODC / UN Women |

### C · The moment of danger — leaving
*The counter-intuitive, load-bearing statistic: risk rises around separation.*
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| D1 | Raised homicide risk after separating from a controlling partner | odds ratio **≈ 3.6** | US 11-city study | Campbell et al. 2003 | *Am. J. Public Health*; Danger Assessment |
| D2 | Strongest lethality factor — perpetrator's access to a gun | odds ratio **≈ 7.6** | US 11-city study | Campbell et al. 2003 | *Am. J. Public Health* |
| D3 | Femicide victims separated / taking steps to separate when killed | **41%** (30% killed within 1st month, ~70% within 1st year) | UK | UK Femicide Census | UK Femicide Census |
| D4 | Victims with a restraining order killed soon after issue | ~**1 in 5** within 2 days; ~1 in 3 within a month | US | Campbell/IPH data | intimate-partner-homicide research |

### D · Coercive control specifically
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| C1 | Coercive-control offences **recorded** | **49,557** | England & Wales | YE March 2025 | Home Office / ONS police-recorded crime |
| C2 | Coercive-control **convictions** (the attrition) | only **853** (98% of offenders male) | England & Wales | YE Dec 2024 | MoJ / CPS |
| C3 | Completed coercive-control investigations resulting in a charge | ~**3%** (local analysis) | England & Wales | recent | local police analysis (flag as local) |
| C4 | Criminalised as a distinct offence | Serious Crime Act **2015** (in force Dec 2015) | England & Wales | 2015 | Serious Crime Act 2015 |
| C5 | Partner economic abuse since age 15 | women **~1 in 6 (16%)**; men 7.8% | Australia | ABS PSS 2021-22 | ABS Personal Safety Survey |

### E · Technology, stalking, surveillance
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| T1 | Unique users affected by stalkerware (vendor lower-bound) | **31,031** (up 5.8% YoY), across 175 countries | global, Kaspersky users only | 2023 | Kaspersky State of Stalkerware 2023 |
| T2 | Distinct stalkerware apps detected | **195** (TrackView most common, 4,049 users) | global | 2023 | Kaspersky State of Stalkerware 2023 |
| T3 | Survey respondents reporting/suspecting stalking | **~40%**; 39% reported abuse from a current/former partner | 21,000-person survey | 2023 | Arlington Research (w/ Kaspersky) |

> ⚠️ Stalkerware detections reflect **one vendor's user base** and drastically
> understate the true total. Show as a lower bound, never as "the" number.

### F · Reporting gap — the dark figure (lead with this)
| id | figure | value | geography | year | source |
|----|--------|-------|-----------|------|--------|
| R1 | Women experiencing violence who seek help of any sort | **< 40%** | global | UN Women benchmark | UN Women |
| R2 | Of those who seek help, who go to police | **< 10%** | global | UN Women benchmark | UN Women |
| R3 | Sexual offences reported vs women disclosing sexual violence | **< 5%** recorded | EU-27 | 2024 | Eurostat / FRA / EIGE GBV Survey |
| R4 | Rape/penetration victims who report to police | fewer than **1 in 6 (16%)** | England & Wales | CSEW (YE 2017 + 2020) | ONS Crime Survey for England & Wales |
| R5 | Recorded rapes resulting in a charge that same year | **~2.7%** ("fewer than 3 in 100"; rises to ~3.2–3.9% on later revision) | England & Wales | YE Dec 2024 | Home Office / ONS / CPS |
| R6 | Reasons women don't report | embarrassment **40%**; "police couldn't help" **38%**; "humiliating" **34%** | England & Wales | ONS | ONS |

### THE FUNNEL (the central visual — "of 100 rapes in England & Wales")
*Assembled from ONS/Home Office/CPS/MoJ, which use different units and periods — show that caveat.*
```
100 experienced   →   ~16 reported   →   recorded   →   ~2.7% of recorded charged   →   convicted
```
> **The point of the funnel:** the official statistics capture only a sliver. The abuse
> that never reaches a report is exactly the abuse this project's reading material is for.

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
