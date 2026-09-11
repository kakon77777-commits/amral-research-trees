# RUN-065 — Phase 0's three maps, read after 64 rounds: four open rows still open, the 首選 route the most worked at 23 to 9, the 紅燈 route with no round and no claimant, every one of Referee E's eight leaps caught at least once — and RUN-064's 25 of 25 was typed, not measured

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`02_Known_Theorem_Closure_Map`](../../../amral/public/bsd/phase0/files/02_Known_Theorem_Closure_Map.md), [`04_External_Route_Matrix`](../../../amral/public/bsd/phase0/files/04_External_Route_Matrix.md), [`08_Local_Agent_Handoff_Prompts`](../../../amral/public/bsd/phase0/files/08_Local_Agent_Handoff_Prompts.md) — the three Phase 0 documents no round had taken as its subject
**Tools:** [`src67_phase0_maps.py`](../code/src67_phase0_maps.py), [`src29_sweep_coverage.py`](../code/src29_sweep_coverage.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src67-phase0-maps.json`](../data/gate-logs/src67-phase0-maps.json), [`src29-sweep-coverage.json`](../data/gate-logs/src29-sweep-coverage.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Phase 0's three maps route rather than prove — a closure table, a route matrix, six agent briefs — and were written before any round of this line ran. Read after sixty-four, each is scored the way RUN-050 scored `01`'s route matrix and RUN-064 scored `06`'s handoff: which rounds sit on which row is a reading, and everything that can be computed about the reading is. **`02`'s table has four open rows — rank ≥ 2, Ш finite in general, the full leading coefficient, all E/ℚ — and no report of this line claims any of them closed**; of `02` §5's seven components of a strong-BSD certificate, four were computed here (Tamagawa, torsion, period, leading term), the regulator was computed without saturation being verified, and the two Ш components never — RUN-023's `#Ш = 1` is BSD-inferred, an input. **`04`'s 首選 route, strong-BSD twist families, is the most worked at 23 rounds; the runner-up, the certificate frontier `04` calls 控制層, has 9**; the route `04` marks 紅燈 — Neo's own 格點秩收斂 — has no round here, and RUN-003's scan of all 85 documents found 0 claiming its conditions met. **`08`'s six briefs A–F each have rounds that did them, and Referee E's eight leaps each have a round that caught an instance** — the circular-Ш assumption named at RUN-023, the numerical-to-proof leap in RUN-013's float64, RUN-017's period and RUN-055's float, the rank-0/1-to-high-rank leap held at HOLD in RUN-050, the normalization mismatch in RUN-042's square class and RUN-062's CRLF. Every one of the 52 rounds the reading cites exists, and all 28 attributions carry a signature phrase the gate finds in the cited report. **With this round Phase 0 is 10 of 10 by the sweep instrument's strongest bucket. Re-measuring also corrects RUN-064: Phase 1 is 23 of 25 the subject of a round and 2 cited only — `03_Algorithm2_Independent_Reproduction` and `13_500K_Twist_Output_NonMonotonicity`, in RUN-012's body, on no subject line — where RUN-064 typed 25 of 25. Across the corpus: 80 of 85 the subject of a round, 5 cited only (those two, and the three P5 documents this report is the first to name), 0 unmentioned.**

---

## How a map is scored

A map has no arithmetic to recompute. What it has is a claim about *where
work should go* and *what it must not say*, and after 64 rounds both are
checkable against this tree's own reports. The gate therefore does four
things, only the first of which is a reading:

1. **Assigns** each round to a row, a route, a brief — the reading, kept in
   the gate's constants so that it is one place, not many;
2. **Checks every round cited exists** — 52 distinct rounds are cited across
   the three maps, and a `RUN-0nn` that does not exist would go red;
3. **Checks every attribution by signature** — each "RUN-023 records `#Ш = 1`
   as BSD-inferred" carries the phrase `BSD-inferred` and the gate looks for
   it in RUN-023's report; 28 such phrases, 12 for `02`'s components and 16 for
   `08`'s leaps;
4. **Checks the prohibitions** — no report may claim an open row closed, no
   round may sit on the 紅燈 route, and RUN-003's log must still say no
   document claims that route's conditions met.

A reading that cites a round for a finding the round does not contain is the
failure mode RUN-060 met (RUN-055 presenting `15` §8's identity as its own,
the other way round); the signature phrases are the guard against it here.

## `02_Known_Theorem_Closure_Map`

`02` §8 is an eight-row table. Where this line's rounds sit:

| row (`02`) | `02`'s status | rounds of this line on it |
| --- | --- | --- |
| modularity and analytic continuation | 已關閉 | — |
| weak BSD at analytic rank 0/1 | 核心已關閉 | RUN-014, RUN-026 |
| *p*-parts at rank 0/1 | 大量新閉包 | RUN-011, RUN-020, RUN-021, RUN-022 (the P5 chain) |
| infinite strong-BSD twist families | 已存在 | RUN-009, RUN-015, RUN-033, RUN-037, RUN-045, RUN-057 |
| weak BSD at rank ≥ 2 | **開放** | RUN-023 — an identity with Ш as input, not a closure |
| Ш finite in general | **開放** | — |
| full leading coefficient | **開放** | RUN-014, RUN-017, RUN-023, RUN-026, RUN-030 — identities at finitely many curves |
| all E/ℚ | **開放** | — |

The computed part: all 64 reports were scanned for the phrases that would
claim an open row closed (*rank 2 BSD is proved*, *Ш finite in general*,
*strong BSD proved*, *BSD for all E/ℚ*, and variants). **None occurs.** The
rank-2 and leading-coefficient rounds sit on open rows as computations of an
identity at one curve, and say so. The one report the scan skips is this
one — it quotes the phrases it looks for, and matched itself on the first
run, as `src54`'s census detector matched its own log at RUN-054; a report
about the scan is not a subject of the scan.

`02` §5 lists the seven components a strong-BSD certificate must close, and
§6 boxes the lesson from Keller–Stoll: *完整 BSD 證書是可工程化的，但每個
component 都必須獨立閉合*. Held against this line:

| component (`02` §5) | here | where |
| --- | --- | --- |
| actual Ш finite | **never** | RUN-023 records `#Ш = 1` as *BSD-inferred* — the identity's input |
| actual order of Ш | **never** | not computed anywhere in this line |
| regulator on a saturated basis | partial | regulator at RUN-023 (rank 2) and RUN-026 (rank 1, heights computed here); **saturation verified in neither** |
| local Tamagawa factors | computed | RUN-016 (`c₂` closed on the base), RUN-023 (`∏c_p = 1`) |
| torsion | computed | RUN-023, RUN-026, RUN-030; RUN-031 (Mazur's twelve degrees for 696.e1) |
| period convention | computed | RUN-017 (the period wrong for three rounds, found by the identity), RUN-014, RUN-023, RUN-030 |
| exact leading term | computed | RUN-014 (`L(E,1) = Ω`), RUN-023 (`L''(1)/2!`), RUN-026 (`L'(1)`) |

Four of seven, one partial, two never. That is the honest shape of this line
against `02`'s box: the components it could compute it computed, and the one
`02` says must close independently — Ш — it has only ever assumed.

## `04_External_Route_Matrix`

`04`'s ten routes with their Phase 1 verdicts, and the count of this line's
rounds on each:

| route (`04`) | verdict | rounds here |
| --- | --- | ---: |
| Gross–Zagier–Kolyvagin | 基線 | 0 |
| *p*-adic zeta / Iwasawa | 綠燈 | 4 |
| **Strong-BSD twist families** | **首選** | **23** |
| *p*-converse | 綠燈 | 0 |
| generalized Kato / higher GZ | 黃燈 | 0 |
| exact computational BSD | 綠燈 | 5 |
| Selmer arithmetic statistics | 輔助 | 0 |
| numerical BSD atlas | 僅作資料層 | 6 |
| 格點秩收斂 | **紅燈** | **0** |
| Faithful certificate frontier | 控制層 | 9 |

Two facts are computed from the counts: the 首選 route is the most worked,
by 23 to the runner-up's 9; and the 紅燈 route has no round. A third is read
from RUN-003's log rather than from this reading: that round scanned all 85
documents of the corpus for the rejected route's conditions being claimed met
and found **0** — so the route `04` closes is closed in the corpus as well as
in this line. `04` §4's MCDM estimate `(G5, U3, X2–X3, P4–P5)` ends with the
sentence *這是研究路由評估，不是數學定理*, and the gate checks that sentence
is there.

The rank-1 and rank-2 identities (RUN-023, RUN-026) are placed on *exact
computational BSD*, not on Gross–Zagier–Kolyvagin: they are numerical
identities at one curve each, not GZK arguments, and GZK has no round here.

## `08_Local_Agent_Handoff_Prompts`

Six briefs, written before any round ran:

| brief | what `08` asks | this line |
| --- | --- | --- |
| A · Statement Auditor | dependency DAG; never *rank equality = full BSD*; never *analytic Ш = actual Ш* | RUN-004 (`01` §6's table recomputed), RUN-002 (the ladder's eleven rungs), RUN-043 (this line's place on it), RUN-051 (eleven prohibitions in one place) |
| B · Banwait–Huang Reproducer | samples, then conductor ≤ 500,000; `unknown`, never guessed | RUN-055 … RUN-064 (the census recomputed, no Sage run); RUN-045's `LOCAL_H2 = UNKNOWN` kept visible |
| C · Certificate Schema Engineer | numeric evidence / rigorous computation / external theorem / conditional theorem / actual proof kept apart | RUN-030 (the 696.e1 certificate), RUN-032 (Referee A's checklist as a program), RUN-048 (the schema and the sieve) |
| D · Rank-2 Wall Analyst | 389.a1, every term with *value / how / rigorous? / theorem? / assumption?* | RUN-023 (every term; `#Ш` the named assumption), RUN-026 (rank 1, every term computed here) |
| E · Adversarial Referee | eight leaps to hunt; `PASS / FAIL / OPEN` only | RUN-010 and every round after it; RUN-062 (the adversarial corpus); RUN-037 (a false box); RUN-046 (the corpus against itself) |
| F · Internal Theory Quarantine | Neo.K's lattice/PRC drafts: translatable / circular / new obligations; never into the external proof | RUN-003 (the rejection holds and the corpus strengthened it), RUN-019 (the witness-network generalisation admits nothing) |

E's eight leaps, each with a round that caught an instance and the phrase the
gate verifies in that round's report:

| leap (`08`, Agent E) | caught at | phrase found |
| --- | --- | --- |
| circular BSD assumption | RUN-023 | `BSD-inferred` |
| numerical-to-proof leap | RUN-013, RUN-017, RUN-055 | `float64`, `period`, `float` |
| finite-to-global leap | RUN-041, RUN-051 | `P_loc`, `substitut` |
| *p*-part-to-full leap | RUN-043, RUN-021 | `C1`, `ledger` |
| rank 0/1-to-high-rank leap | RUN-050, RUN-026 | `High rank 2+`, `rank-1` |
| isogeny double counting | RUN-008, RUN-031 | `122,247`, `Mazur` |
| database incompleteness | RUN-063, RUN-055 | `36,687`, `247,391` |
| normalization mismatch | RUN-042, RUN-062 | `square class`, `CRLF` |

Several of these instances are this line's own: the period RUN-017 had wrong
for three rounds, the float root finder RUN-055 replaced, the rank-1 identity
RUN-050 holds at HOLD rather than extending. `08` asked for a referee that
hunts these leaps in *all outputs*; the drill has been that referee since
RUN-010, and the instances above are what it found when pointed at itself.

## Phase 0 at 10 of 10; the sweep re-measured; RUN-064 corrected

`src29` re-run with this round's report in place: **85 documents — 80 the
subject of a round, 5 cited only, 0 not mentioned.**

| sub-line | subject of a round | cited only | unmentioned |
| --- | ---: | ---: | ---: |
| Phase 0 | **10 of 10** | 0 | 0 |
| Phase 1 | 23 of 25 | 2 | 0 |
| Phase 2 | 40 of 40 | 0 | 0 |
| P5 | 7 of 10 | 3 | 0 |

The three P5 documents (`BSD_P5_Anomalous_Norm_Localization_389a1_p11_v1.1`,
`BSD_P5_Determinantal_Kurihara_Semilocal_389a1_p11_v1.3`,
`BSD_RUGZPB_P2_P4_389a1_p11_v0.2`) were *not mentioned* before this round and
are *cited only* after it — by this report, here, as the rounds to come. That
is the instrument doing what RUN-027 built it to do: a mention is not a round.

**RUN-064 wrote "Phase 1 closes at 25 of 25". The instrument says 23 of 25
subject, 2 cited only** — `03_Algorithm2_Independent_Reproduction` and
`13_500K_Twist_Output_NonMonotonicity`, both worked in RUN-012's body and on no
round's subject line. The 25 was typed, and RUN-029's rule reaches typed
counts as well as typed coefficients. A correction note is added to RUN-064
and its README row; those two documents are RUN-066's subject, and Phase 1
closes in the instrument's sense when that round is committed.

## The drill

**275 defects, 275 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 55 controls undisturbed, over 93 checks.

The 5 planted for this gate, each turning `phase0-maps` red and nothing else:

| planted defect | went red |
| --- | --- |
| 02's open row 'Sha finite in general' is read as 已關閉 | `phase0-maps` |
| the regulator is counted fully computed, saturation included | `phase0-maps` |
| a leap's attribution points at a finding the cited round does not contain: RUN-023 for 'Sha computed exactly' | `phase0-maps` |
| the 紅燈 route is given RUN-003 as a round on it | `phase0-maps` |
| a round that does not exist is cited on the twist-family route: RUN-099 | `phase0-maps` |


## What this round does not claim

* **The row assignments are a reading.** Which route a round "belongs to" is
  a judgement kept in one place; the gate verifies that every cited round
  exists and contains the attributed finding, not that the assignment is the
  only defensible one.
* **Nothing about the open rows moves.** Four open at `02`, four open now;
  this round records that this line never said otherwise.
* **"Caught an instance" is not "caught every instance."** E's leaps have at
  least one caught case each; the drill's 260 defects are the fuller record.
* **The 紅燈 finding is RUN-003's.** This round reads its log; it does not
  rescan the corpus.
* **Saturation is unverified.** The regulator rows at RUN-023 and RUN-026 are
  counted partial for that reason, not promoted.
* **Phase 0's 10 of 10 is the instrument's strongest bucket, not a closure of
  its content.** RUN-002, RUN-003, RUN-004, RUN-013, RUN-024, RUN-025 and this
  round each took Phase 0 documents as subjects; the maps were the last three.
* **The three P5 documents are named, not read.** Their citation here is the
  instrument's own record that they are next.
