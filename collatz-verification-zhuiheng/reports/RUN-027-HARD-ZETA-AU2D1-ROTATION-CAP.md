# RUN-027 — Hard-Zeta A-U.2d.1: the rotation cap holds and is attained, and it is exactly rational — plus three defects in the shipped artifacts and none in the mathematics

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d1_bundle.zip` (source item 45) — Bi-Exact Source–Endpoint Rigidity via an Irrational-Rotation Correction Cap, Endpoint-Gap Quantization, and an Improved Diophantine Survival Gate. Ships a verification script, a constants JSON, and literature notes.
**Tools:** [`src45_rotation_cap.py`](../code/src45_rotation_cap.py) · [`src45_drill.py`](../code/src45_drill.py) · [`src45_emit_report_block.py`](../code/src45_emit_report_block.py)
**Logs:** [`src45-au2d1.json`](../data/gate-logs/src45-au2d1.json) · [`src45-drill.json`](../data/gate-logs/src45-drill.json) · [`au2d1-literature-check.json`](../data/external/au2d1-literature-check.json)

**Result: every theorem holds, exactly. The round's central inequality is verified on real first crossings termwise and is ATTAINED. Three findings, all in the shipped artifacts rather than in the mathematics — and one methodological improvement that makes the round's own quantity exactly computable in integers.**

---

## The round sharpens something this arm already verified

RUN-023 checked A-U.2e.2's First-Crossing Correction Bound, which in this round's
notation reads `B/3^L ≤ L/3`. A-U.2d.1 replaces the universal constant `1/3` with

> `U_β(L) := (1/3) · Σ_{j<L} 2^(−{βj})`,  and  `U_β(L)/L → 1/(6 ln 2)`

because `Q_j` is an integer strictly below `βj`, hence at most `⌊βj⌋`, hence
`δ_j ≥ {βj}` **termwise**. The universal linear efficiency drops from `0.3333…`
to `0.2404…` — about 28 % better, and the improvement is code-independent.

Both halves are verified here on real orbits: the termwise inequality
`Q_j ≤ ⌊βj⌋` and the aggregate cap, with zero violations. **The cap is attained**,
which matters — a bound never reached would be a much weaker claim than this one.

## The observation that makes it exact

`U_β(L)` looks like it needs high-precision reals, and the shipped script computes
it in `mpmath` at 80 digits. It does not need them:

> `2^(−{βj}) = 2^(⌊βj⌋ − βj) = 2^(⌊βj⌋) / 3^j`,  since `2^(βj) = 3^j`

and `⌊βj⌋` is exactly `(3**j).bit_length() − 1`. **So `U_β(L)` is a rational
number**, and the whole Irrational-Rotation Correction Cap is an exact inequality
between rationals:

> `B/3^L = (1/3)Σ 2^(Q_j)/3^j  ≤  (1/3)Σ 2^(⌊βj⌋)/3^j = U_β(L)`

No logarithm is evaluated and nothing is approximated. That is a stronger check
than the one the round ships, and it is what turns the three artifact findings
below into measurements rather than impressions.

For the large convergent denominators (up to `190537`) the exact rational is a
90 000-digit object and infeasible, so those use a **second route**: `t_j =
2^(−{βj})` satisfies `t_j = t_{j−1}·2/3` or `·4/3` exactly, since `2^(−γ) = 2/3`.
The two routes are compared wherever both are feasible, and a wrap decision too
close to call is **counted and reported** rather than guessed.

---

## Finding 1 — the shipped JSON publishes more decimals than its own computation supports

The constants file prints `U` to 76–79 decimals. Recomputed as exact rationals,
the first three values are right to every published digit and the rest are not:
the last **2–3 decimals** of `L = 300, 1000, 3000, 10000` are wrong.

The cause is visible in the shipped script: it runs `mp.mp.dps = 80` and sums `L`
terms. Fixed-precision summation of `L` terms costs about `log₁₀ L` digits, and
the measured over-publication — `0, 0, 0, 2, 2, 3, 3` — tracks exactly that.

Every leading digit is correct. Nothing downstream in the round uses those
decimals. But 79 published decimals assert 79 correct decimals, and the last few
are not.

## Finding 2 — the shipped JSON is not what the shipped script produces

Read, not run. The script's output literal names its keys; the JSON's differ:

| script writes | JSON has |
| --- | --- |
| `beta` | `beta_log2_3` |
| `gamma` | *absent* |
| `continued_fraction_denominators` | `cf_denominator_checks` |
| row key `eta` | *absent* |
| row key `difference` | `difference_from_eta` |
| row key `verified_upper` | `verified` |

So re-running the published program would not reproduce the published file. This
is about **provenance**, separate from Finding 1: no value is wrong in any digit
the computation supports.

**This is the same class as item 35 (RUN-017)**, where a shipped JSON had a
different row count and renamed fields from its shipped script while every number
was correct. Second occurrence, so it is a pattern in how these artifacts are
produced rather than a one-off.

## Finding 3 — the withdrawn citation recurs

RUN-026 found that `arXiv:2605.13886` (Niu) has been **withdrawn since
2026-05-20** while listed as a primary reference in the A-U.2d literature notes.
The A-U.2d.1 notes, shipped the same day, cite it again the same way.

Everything RUN-026 said still applies: every claim attributed to it is present and
verbatim, and it is not load-bearing. But one bundle is an oversight and two is a
pattern, so it is repeated here rather than treated as already reported.

### A distinction worth keeping, about the other new reference

The notes cite `arXiv:2303.15992` (Frühwirth & Hauke) as a primary-source
discussion of **Denjoy–Koksma sharpness**, and it is: the abstract establishes
"asymptotic sharpness of the Denjoy–Koksma inequality". That result is **metric**
— for almost every `α`, for `f` with discontinuities or logarithmic singularities
at rationals. This round applies DK at **one specific** `α = log₂3`, and uses only
its **upper** bound, which is deterministic and valid at every `α`. So the
citation is positional and correct.

It is worth stating because a sharpness reference invites the inference that the
bound is tight *here*, and an almost-every result cannot supply that — `log₂3`
could be exceptional. Measured instead: at the twelve convergent denominators the
round checks, DK is used at about **42 %** of its allowance. It is not tight here.

**One trap worth recording, because getting it wrong tightens a bound onto correct
data.** The variation of the 1-periodic extension of `f(x) = (1/3)2^(−x)` is *not*
`(1/3)(1 − 1/2) = 1/6`. The periodic extension **jumps** at the integers, from
`1/2` back up to `1`, so the variation is `(1/3)[(1−1/2) + (1−1/2)] = 1/3`. The
shipped script uses `1/3` and is right. I reached for `1/6` first.

---

<!-- BEGIN GENERATED measured block: python code/src45_emit_report_block.py -->

| what | measured | value |
| --- | --- | --- |
| **cap violations** `B/3^L ≤ U_β(L)` | exact rationals, 9999 real first crossings | `0` |
| termwise violations `Q_j ≤ ⌊βj⌋` | the round's own argument, per term | `0` |
| max `B/3^L ÷ U_β(L)` | 1 means the cap is attained | `1.0` |
| …crossings where it is **attained** | at n = 3 | `7137` |
| mean `B/3^L ÷ U_β(L)` | how much of the new cap real crossings use | `0.917624` |
| constants disagreeing with their closed forms | β, 1/(6ln2), 6ln2, √3·ln2, 1/(6(ln2)²) recomputed | `0` |
| convergent denominators agree | exact mediant descent vs the shipped list | `True (12 of them)` |
| Denjoy–Koksma upper violations | two-sided, at every convergent | `0` |
| Denjoy–Koksma lower violations | the shipped check is upper-only | `0` |
| …exact vs high-precision cross-checks | where both routes are feasible | `6` |
| …undecidable wrap decisions | counted, never guessed | `0` |
| **fraction of the DK allowance used** | max |U(q) − qη| ÷ Var(f) = 1/3 | `0.4161` |
| endpoint-gap identity violations | `B/3^L = (2^D−1)y + 2^{D+1}h`, exact | `0` |
| …crossings where the endpoint DROPS (`h < 0`) | the round's `h ≥ 1` needs the surviving case | `9999` |
| defects planted / caught by their own check | `code/src45_drill.py` | `16 / 16` |

**How much the new cap improves on `L/3`.** `U_β(L) ÷ (L/3)`, which tends to `1/(2 ln 2) = 0.7213…`:

| L | ratio |
| --- | --- |
| 1 | 1.0 |
| 5 | 0.787654 |
| 10 | 0.756048 |
| 34 | 0.733817 |

**Finding 1, quantified.** Published decimals against decimals actually correct, recomputed as exact rationals:

| L | published | correct | over-published by |
| --- | --- | --- | --- |
| 10 | 79 | 79 | **0** |
| 30 | 79 | 79 | **0** |
| 100 | 78 | 78 | **0** |
| 300 | 78 | 76 | **2** |
| 1000 | 77 | 75 | **2** |
| 3000 | 77 | 74 | **3** |
| 10000 | 76 | 73 | **3** |

The over-publication tracks `log₁₀ L`, which is what fixed-precision summation of `L` terms costs.

**The constants, each against its closed form.**

| constant | closed form | published decimals | all correct |
| --- | --- | --- | --- |
| `beta_log2_3` | `log2 3` | 79 | True |
| `eta_beta` | `1/(6 ln 2)` | 80 | True |
| `six_ln2` | `6 ln 2` | 79 | True |
| `improved_sqrt_y_constant` | `sqrt(3) * ln 2` | 79 | True |
| `1/(6 (ln 2)^2)` | `1/(6 (ln 2)^2)` | printed in §4, not shipped | True |

**The references, checked.** `4` Collatz references plus `1` analytic one; all say what the notes attribute to them.

`arXiv:2605.13886` is **WITHDRAWN** (2026-05-20) and is cited as a primary reference for the **second bundle running** — RUN-026 reported it for A-U.2d, and A-U.2d.1 repeats it.

Every figure above is emitted by `code/src45_emit_report_block.py` from the gate logs and the archived literature record. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

`src45_drill.py` plants defects and requires each to be caught **by the check
named for it**. Three habits were carried in from items 42, 43 and 44 — a
subprocess timeout, defects aimed at subjects rather than comparisons, and defects
that must break the result rather than the interpreter. All three were needed, and
two of them were needed *again*, which is worth saying rather than glossing.

**Two of the defects break a FINDING rather than a gate check.** A finding that
cannot disappear is not a finding, it is a sentence. D15 makes the provenance
comparison read the JSON against itself, D16 makes the precision comparison
compare the published string with itself; both are verified by watching the
finding **vanish from the report**, not by watching the failure list grow.

Six misses on the first pass, and one of them is the most useful thing in this
report:

- **D10 — the variation error is invisible to this data, and it is the error I
  nearly made.** Replacing the total variation `1/3` with `1/6` — dropping the
  jump — left the gate **green**, because the largest deviation over the twelve
  shipped convergents is about `0.139`, comfortably under `1/6 = 0.1667`. So a
  check that used the wrong constant would have passed on correct data, and my
  own first instinct was that wrong constant. The cure was not more convergents:
  it was to assert the variation **against its definition** rather than against
  the data. The gate now derives it in exact `Fraction`s as *descent plus jump*
  and reports, separately, that this data could not have caught the error.
- **D3/D4 crashed rather than failed.** A broken recurrence returns an absurd
  magnitude and `quantize` raises; the drill saw "did not produce JSON". The
  cross-check now catches the exception and reports a disagreement — a difference
  too large to quantise is still a difference.
- **D8 hung.** Reversing the mediant descent stops it bracketing, so it never
  converges. The timeout caught it, which is the item-42 habit working, but a
  timeout is not the named check firing. Re-aimed at convergent *detection*.
- **D12 weakened a check that never fires.** `Q_j ≤ ⌊βj⌋` always holds, so
  allowing one more never fires. Tightening it does — and only because the bound
  is **attained**, so this run's attainment measurement is what gave the defect
  something to hit.
- **D15 was my own bug in the drill**, not in the gate: the needle it searched for
  had the wrong case, so it reported the finding as absent at baseline when it was
  present.

A note on the first of those. The variation derivation also had to move from
`Decimal` to `Fraction`: `(1/3 − 1/6)·2` differs from `1/3` by one ulp at any
finite decimal precision, and the first version of that assertion reported the
**correct** value as wrong. An exact statement about a rational should not be
decided by rounding.

## Route map

`ROUTE_MAP v2.1` continues the A-U.2d line. Items 46 and 47 are `AU2d2` and
`AU2d3`, so the file ordering and the route map agree for the eighth time.

## What this run does not claim

1. That CASP is closed. The round produces an improved gate, not a contradiction.
2. That the improved survival gate has ever been exercised. It quantifies over
   surviving crossings, of which RUN-023 found none below `2·10⁵`; on real orbits
   the endpoint-gap parameter `h` is negative at **every** crossing measured here,
   because the endpoint drops.
3. That Denjoy–Koksma is or is not sharp at `log₂3`. The 42 % figure is what was
   used at twelve specific denominators, not an asymptotic statement.
4. That the mathematics in any cited paper is correct — only that the citations
   say what the notes say they say, and that one of them is withdrawn.
