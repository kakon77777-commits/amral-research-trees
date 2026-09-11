# RUN-063 — Phase 1's closure claim scored item by item, the fixtures reproduced from the census, and the other half of RUN-055: completeness

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`16_Phase1_Closure_and_Phase2_Interface`](../../../amral/public/bsd/phase1/files/16_Phase1_Closure_and_Phase2_Interface.md), [`10_Phase1_Gate_v03`](../../../amral/public/bsd/phase1/files/10_Phase1_Gate_v03.md), [`01_Small_Fixture_Version_Regression`](../../../amral/public/bsd/phase1/files/01_Small_Fixture_Version_Regression.md), [`00_Phase1_Consensus`](../../../amral/public/bsd/phase1/files/00_Phase1_Consensus.md), [`00_Phase1_v02_Consensus`](../../../amral/public/bsd/phase1/files/00_Phase1_v02_Consensus.md)
**Tools:** [`src65_phase1_closure.py`](../code/src65_phase1_closure.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src65-phase1-closure.json`](../data/gate-logs/src65-phase1-closure.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json); full completeness run in [`data/external/twist-map-completeness-full.json`](../data/external/twist-map-completeness-full.json)

**Result: `16` boxes 「Banwait–Huang Reproduction = COMPLETE」 on an eight-item list. **Every item on it has an independent recomputation in this tree** — seven by earlier rounds, the eighth (the `<150` fixture, which the package does not carry) recovered here from the census by conductor: the OLD base has **25** curves below 150, the CURRENT base **12**, the 13 removed are `08`'s thirteen to the label, and the branch split is **10 CLZ20 + 15 Zha16 → 7 + 5**, exactly as `01` states. `00` prints two Algorithm 2 branches computed by hand — 46a1's seven twists and 106d1's twenty-one — and **both lists reproduce exactly** from this tree's transcription of `01`'s conditions, including 106d1 over `00`'s negative range, where **no negative `d` is admissible**; nor is one on any of 200 Zha16 curves with `Δ < 0`, which is why the map's all-positive `d` and `00`'s symmetric range do not conflict. And RUN-055's missing half: that round verified every map entry admissible and said completeness could not be measured without the enumeration bound. **`04_Algorithm1_Environment_and_Gaps` states the bound — twists up to 1000** — and with it `{d < 1000 : admissible}` equals the map on every curve sampled and, in the full run, on **all 36,687 stable curves and 247,391 pairs: 0 admissible-but-absent, 0 present-but-inadmissible**. Algorithm 2's admissibility side is reproduced from `01`'s text in both directions. `10`'s four regression layers each have this line's content; the label `10` defines is for a *reproduction run*, the package says it is not one, and **no label is awarded**.**

---

## `16`'s eight, scored

| # | `16` says Phase 1 completed | redone independently by |
| ---: | --- | --- |
| 1 | Theorem 2.18 predicate map | **RUN-055** — all 40,749 and 247,391 |
| 2 | Algorithm 2 independent reproduction | **RUN-055** (soundness) + **this round** (completeness, with `04`'s bound) |
| 3 | paper / current-code soundness audit | **RUN-056**, **RUN-061** |
| 4 | `<150` version regression | **this round** — not in the package; recovered from the census |
| 5 | 13 removed curves first-failure closure | **RUN-061**, 13 of 13 |
| 6 | 500K exact artefact census | **RUN-004 … RUN-008**, then RUN-055 |
| 7 | Algorithm 1 4,062 removal-cause closure | **RUN-059** |
| 8 | stable-domain OLD → CURRENT replay | **RUN-060**, to the pair |

**8 of 8.** What `16` calls COMPLETE is the corpus's Phase 1. `04` in the same
corpus refuses the sentence *Full Algorithm 1 independently reproduced*, and so
does this line: nothing here ran Sage, a descent, or the LMFDB scan that
produces the 36,687 from scratch. What is reproduced is everything the archived
artefacts can carry.

## `01`, from the census

| | `01` | census |
| --- | ---: | ---: |
| old fixture (2026-05-22) | 25 | **25** curves with `N < 150` in the OLD base |
| of which CLZ20 / Zha16 | 10 / 15 | **10 / 15** |
| current fixture (2026-06-03) | 12 | **12** of those in the CURRENT base |
| of which CLZ20 / Zha16 | 7 / 5 | **7 / 5** |
| removed | 13 | **13**, and they are `08`'s thirteen |
| added | 0 | **0** |

The twelve: 46a1, 69a1, 77c1, 94a1, 106d1, 114b1, 115a1, 118c1, 118d1, 141b1,
141e1, 142c1.

## `00`'s two fixtures

| curve | branch | range in `00` | `00`'s list | recomputed | in the map |
| --- | --- | --- | --- | --- | --- |
| 46a1 `[1,−1,0,−10,−12]` | CLZ20 | `1 ≤ d ≤ 1000` | 7 values | **the same 7** | the same 7 |
| 106d1 `[1,1,0,−27,−67]` | Zha16 | `−1000 ≤ d ≤ 1000` | 21 values | **the same 21**, none negative | the same 21 |

`00` says both agree with the official fixture 「完全一致」. They agree with
this tree's predicate too — a third implementation, written from `01`'s
prose rather than from the code.

### Negative `d`

`01`'s E.3 forbids `d < 0` only when `Δ_E > 0`. On 200 Zha16 curves with
`Δ_E < 0`, **none admits a negative `d` below 1000 in absolute value**. The map
has no negative `d` anywhere. Consistent — and the reason none passes is *not*
established here.

## Completeness

RUN-055: every map entry is admissible (soundness). Not measurable then: every
admissible `d` is in the map (completeness), for want of the bound.

`04`: 「twists up to 1000」.

| | |
| --- | ---: |
| bound | `d < 1000` |
| stable curves | 36,687 |
| pairs in the map | 247,391 |
| admissible but absent | **0** |
| present but inadmissible | **0** |

Both directions, on the whole stable domain, from `01`'s text. That is
Algorithm 2's admissibility side reproduced — not the certificate side (`𝒮`,
descent), which needs Sage, and not the base list, which needs the LMFDB scan.

## `10`'s four layers

| layer | content | this line |
| --- | --- | --- |
| A | current 12 positive | recovered from the census — this round |
| B | old-only 13 must fail at the predicate map | RUN-061, 13 of 13 under `08`'s ordering |
| C | discrepancy four must stay rejected | RUN-062, `f'(x₀)` square on 4 of 4; three reasons cited |
| D | Algorithm 2 unit fixtures `TWIST_GCD_3N`, `TWIST_DISC_VAL_GATE_REMOVED` | RUN-060, `09`'s Cases A and B |

`10`: only A+B+C+D together allow `REPRODUCTION-QUALIFIED`; else
`OUTPUT-MATCHED`; the two must not be mixed. **No label is awarded here.** The
label is for a reproduction run, and this line verified the four layers'
*content* against archived artefacts; it did not run the reproduction the label
names.

## The drill

**270 defects, 270 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 54 controls undisturbed, over 92 checks.

The 5 planted for this gate, each turning `phase1-closure` red and nothing else:

| planted defect | went red |
| --- | --- |
| one of the twelve is reported still removed, so the current fixture reads 13 | `phase1-closure` |
| the admissibility predicate drops the ordinary condition D4 | `phase1-closure` |
| the twist bound is taken as 2,000, so admissible d above 1,000 read as absent from the map | `phase1-closure` |
| 16's checklist is scored with a ninth item | `phase1-closure` |
| 10's label REPRODUCTION-QUALIFIED is awarded | `phase1-closure` |


## What this round does not claim

* **Not a reproduction of Algorithm 1.** The base list's 36,687 is a column
  identity here (RUN-059), not an independent scan of conductors below 500,000.
* **Completeness is exact under `01`'s conditions and `04`'s bound.** A
  condition the paper applies and `01` omits would be invisible to this — but
  then the map would have shown *extra* entries, and it shows none.
* **"No negative `d`" is a measurement on 200 curves plus the map's contents**,
  not a theorem about the conditions.
* **`00`'s 「完全一致 with the official fixture」 is `00`'s claim.** This round
  agrees with `00`; it did not read the official fixture, which the package
  does not carry.
