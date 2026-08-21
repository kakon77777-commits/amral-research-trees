# RUN-023 — Hard-Zeta A-U.2e.2: the round holds, its two headline inequalities turn out to be one inequality, and its Diophantine gate is a partition rather than a choice

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `Hard_Zeta_Phase_II_Round_AU2e2_bundle.zip` (source item 41) — First-Crossing Correction Caps, a Diophantine Survival Gate, and A/B Atomic Multiplication, with Aletheia as 協作整理
**Tools:** [`src41_first_crossing_survival.py`](../code/src41_first_crossing_survival.py) · [`src41_drill.py`](../code/src41_drill.py) · [`src41_emit_report_block.py`](../code/src41_emit_report_block.py) · [`felra/au2e2`](../felra/au2e2/project.yaml)
**Logs:** [`src41-au2e2.json`](../data/gate-logs/src41-au2e2.json) · [`src41-drill.json`](../data/gate-logs/src41-drill.json)

**Result: every checkable claim in the round holds, exactly, on every first coefficient crossing below 2·10⁵. No defect found in the mathematics. Three findings about the round's *structure* — two of which make it tidier than it is stated, one of which says where its evidence can and cannot reach — and one measurement that is not vacuous.**

---

## The half of this round that is about an empty set

The round splits cleanly, and saying so first is most of the work.

**Unconditional**, holding at every first coefficient crossing:

> `B_L ≤ L·3^(L−1)` · `Y_{a+L} ≤ 2^(−D)(Y_a + L/3)` · `Y_a ≤ c_fc`

**Conditional** on a *surviving* first crossing — one where the coefficient
skeleton turned contracting and the value still did not fall:

> `L ≥ 3(2^D − 1)Y_a` · the Duration–Diophantine Dichotomy · the Polynomial
> Survival-Time Corollary · the A/B Atomic Multiplication Theorem

A surviving first crossing **is a counterexample to the Terras
coefficient-stopping conjecture**. So the second group is not merely unverified
here — it is about a set this run measures to be **empty**, and a report saying
"all conditional bounds hold" over an empty set would be the emptiest kind of
pass. The census is in the generated block below: `0` survivors in `99999` starts.

That is the expected outcome, and it is not a criticism of the round. "If a
counterexample exists it must look like this" is exactly how this program is meant
to work. But it fixes what this arm is allowed to claim: the conditional theorems
are checked here as **algebra**, on synthetic configurations satisfying the round's
hypotheses, and labelled `is_algebra_not_orbit_data` in the log. Nothing in this
run says such a configuration is reachable by the Collatz map. That is the open
question.

Everything is exact. `Q_L > β·L` is evaluated as `2^Q_L > 3^L`, `2^D` as the
rational `2^Q_L / 3^L`, and `p/q < log₂3` as `2^p < 3^q`. **No logarithm is
evaluated anywhere in the decision path** — a float check here would be a check of
the float library. Where a quantity genuinely needs `ln 2` or `β`, it is bracketed
by exact rationals and a comparison the bracket cannot settle is reported as
undecided rather than rounded.

---

## Finding 1 — the Reset Inequality is the Correction Bound restated

The round states two inequalities in sequence, as though the second added
something:

> **First-Crossing Correction Bound** `B_L ≤ L·3^(L−1)`
> **First-Crossing Reset Inequality** `Y_{a+L} ≤ 2^(−D)(Y_a + L/3)`

Substituting the closed form `Y_{a+L}·2^Q_L = 3^L·Y_a + B_L` and clearing
denominators turns the second into `3(3^L Y_a + B_L) ≤ 3^L(3Y_a + L)`, in which
**the `Y_a` terms cancel identically**, leaving `3B_L ≤ L·3^L` — the first
inequality. So the reset inequality holds for *every* `Y_a` whatsoever and carries
no information about the starting height at all. Its slack is exactly three times
the correction bound's:

> `rhs − lhs = 3·(L·3^(L−1) − B_L)`

That identity is asserted exactly at every crossing in the sweep (zero violations,
below), and confirmed independently by z3 over a declared box — see the FELRA
section.

This is not an error in the round. It is a simplification: A-U.2e.2 has one
correction inequality, not two, and the extra `2^(−D)` factor the round notes as
an improvement over A-U.2e.1 comes from the prefix hypothesis alone.

## Finding 2 — the Dichotomy's two branches are a partition, not a choice

The round states:

> every surviving crossing satisfies `L ≥ √(3ln2/2 · Y_a)` **or** `Q_L/L` is a
> continued-fraction convergent of `log₂3`

and presents these as alternative escape routes. Checking "no configuration fails
both" turned out to be a weak test, because one branch holds everywhere — and the
reason is worth stating, because it makes the dichotomy sharper than an either/or.

The correction cap gives `Y_a ≤ L / (3(2^D − 1))`, and `2^D − 1 ≥ D·ln2`. So

> if `D ≥ 1/(2L)` then `Y_a ≤ L / (3·ln2/(2L)) = 2L²/(3ln2)`,

which **is** the duration branch. And when `D < 1/(2L)`, that is precisely
Legendre's hypothesis, so `Q_L/L` in lowest terms is a convergent. The two branches
are the two sides of a partition on `D` against `1/(2L)`, each side delivering its
own branch from the cap or from Legendre. Neither can fail on its own side, and
"satisfies neither" is impossible rather than merely unobserved.

(The reduction in lowest terms is safe in the direction the round needs it: if
`Q_L/L` is not reduced, its reduced denominator is smaller, so `|β − p/q| <
1/(2L²) ≤ 1/(2q²)` and Legendre's hypothesis is *more* than satisfied.)

## Finding 3 — where the round's evidence cannot reach, stated by a refusal

FELRA v1.8.0's proof-obligation export renders a claim as SMT-LIB2 and hands it to
z3. Asked for the round's inequality in general form — with `L` symbolic, so that
`3^L` and `2^Q_L` have variable exponents — it **refused**:

> `only a literal non-negative integer exponent can be rendered exactly; 3 ** y cannot`

which is the correct answer and a real boundary: the round's central inequality is
not solver-checkable in general, only slice by slice at fixed `L`. The refusal is
recorded in `felra/au2e2/artifacts` rather than worked around, because an
obligation that is *nearly* the claim is an obligation about a different claim.

---

## The measurement that is not vacuous

Nothing survives, so the Diophantine gate itself cannot be tested on orbits. What
can be tested is whether its mechanism leaves a trace **below** the survival
threshold: among first crossings ranked by how near they come to the correction
cap, does `Q_L/L` land on the Stern–Brocot path to `log₂3` — its convergents and
semiconvergents — more often than for crossings generally?

It does, and the control is the point. The base rate over the whole population and
the rate over the *furthest* crossings are both in the table below, because "the
top ten contain `8/5`" is worth nothing until you know where ordinary crossings
land. The gate refuses to publish the comparison at all unless the control set is
disjoint from the sample it controls for.

This is an independent replication of the kind of structure Niu 2026 observed, on
a different sample — first crossings from every odd start, rather than enumerated
paradoxical ratios — and reached without evaluating a logarithm. It supports the
round's mechanism; it does not verify the gate, which remains conditional.

**The path itself is cross-checked by a second method.** It is built here by
mediant descent, deciding `p/q < log₂3` as `2^p < 3^q`. A separate run of the
recursive continued-fraction algorithm on exact `Fraction`s — which never forms
either of those powers — returns `log₂3 = [1;1,1,2,2,3,1,5,2,23,2,2,1,1,55,1]`,
whose convergents `3/2, 8/5, 19/12, 65/41, 84/53, 485/306, 1054/665` all lie on
the path. Two computations sharing no code and no comparison agreeing on the whole
set is worth more than either agreeing with itself; three of those convergents are
also the classical equal temperaments, written down for unrelated reasons
centuries earlier. The CF algorithm is not run in the gate — its deep partial
quotients (`23`, `55`) make the intermediate fractions enormous and it takes
minutes — so its output is pinned in `check_best_approximations` instead.

<!-- BEGIN GENERATED measured block: python code/src41_emit_report_block.py -->

| what | measured | value |
| --- | --- | --- |
| odd starts walked | first crossing found for each | `99999` |
| **surviving first crossings** | Y_{a+L} ≥ Y_a, i.e. coefficient crossed and no descent | `0` |
| largest c_fc / Y_a attained | survival needs ≥ 1 | `0.572331380543576` |
| …at | the start reaching it | `n = 63` |
| correction bound violations | B_L ≤ L·3^(L−1), exact | `0` |
| correction-bound tightness, L ≥ 2 | max B_L / (L·3^(L−1)) | `0.851852` |
| reset-inequality violations | cleared of denominators, exact | `0` |
| reset slack-identity violations | rhs − lhs = 3·(L·3^(L−1) − B_L), exact at every crossing | `0` |
| cap threshold, both sides | probed at ⌊c_fc⌋ and ⌊c_fc⌋+1 per crossing | `0` |
| smallest 2·L·D on a real orbit | Legendre regime is 2LD < 1 | `0.751875` |
| …at | and its coefficient ratio | `n = 95, Q/L = 8/5` |
| defects planted / caught by their own check | `code/src41_drill.py` | `16 / 16` |

**The near-miss clustering, with its control.** Ranking every first crossing by how near it comes to the correction cap, and asking how often `Q_L/L` lands on the Stern-Brocot path to `log₂3` (its convergents and semiconvergents):

| sample | size | on the path | share |
| --- | --- | --- | --- |
| top 10 by `c_fc/Y_a` | 10 | 6 | 60.0% |
| top 100 | 100 | 64 | 64.0% |
| top 1000 | 1000 | 663 | 66.3% |
| **all first crossings (control)** | 99999 | 12915 | 12.92% |
| bottom 1000 — furthest from the cap | 1000 | 0 | 0.0% |

`L = 1` forces `Q/L = 2/1`, which is on the path for a trivial reason and inflates every share, so the same comparison restricted to `L ≥ 2`: top 1000 `78.0%` against a population base rate of `25.83%`, with the bottom 1000 at `0.0%`.

**The constant.** The round prints `1.019666990169…`; recomputed from an exact bracket around `ln 2` it is `1.019666990168808`, which rounds to the printed twelve decimals. The bracket is tight enough that both ends agree to twenty digits: `1.01966699016880896776`.

**The dichotomy's partition.** Of `34` synthetic configurations satisfying the round's hypotheses, `33` sit on the `D ≥ 1/(2L)` side and `1` on the `D < 1/(2L)` side; the duration branch failed on the duration side `0` times, and `0` configurations satisfied neither branch. `0` were left undecided by the rational bracket around `log₂3`.

Every figure above is emitted by `code/src41_emit_report_block.py` from the two gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instruments, and two things the drill caught in them

`src41_drill.py` plants defects in the recheck and requires each to be caught **by
the check named for it**. A defect caught only by some other check is recorded as
a miss, because it means the named check is not aimed at what it claims to cover.
Two misses on the first pass, and both were real weaknesses in this arm's
instruments rather than in the round:

- **The cap could be computed wrongly and nothing went red.** On real orbits the
  cap-equivalence check compares `False` against `False` at every single start —
  no start reaches the cap, and none survives — so corrupting the cap's
  denominator left the whole run green. The gate now probes each crossing's cap
  **at its own threshold from both sides**, at `⌊c_fc⌋` and `⌊c_fc⌋+1`, which
  exercises both answers regardless of where the real start sits.
- **A check that crashes is not a check that failed.** A wrong power made the
  correction bound's limit zero at `L = 1`; the violation was recorded and then
  the run died computing a ratio, so the caller saw no verdict at all. Degenerate
  bounds are now reported.

A third instrument fault was found without the drill: the reset inequality's
`lhs/rhs` ratio tends to `1` as `Y_a` grows for any `B` whatsoever, so its maximum
over a sample reports the largest start in the sample and nothing about the bound.
It has been replaced by the exact slack identity of Finding 1 — which measures
something, and is the same fact z3 confirms.

## FELRA v1.8.0, driven at real work

This is the first use of the proof-obligation export on this line. Four claims
about the `L = 5, Q_L = 8` slice — the crossing at the convergent `8/5` — were
rendered to SMT-LIB2 and checked, each against a discriminating twin with the
conclusion flipped:

| claim | verdict | obligation / twin |
| --- | --- | --- |
| the correction bound implies the reset inequality | **verified** | `unsat` / `sat` |
| the reset inequality on its own | **refuted** | `sat` / `sat` |
| the two are **equivalent**, in both directions | **verified** | `unsat` / `sat` |
| the general form, `L` symbolic | **refused** | not renderable exactly |

The second row is the case that matters for the tool as well as the round: both
the obligation and its twin are satisfiable, because the claim holds at some points
of the box and fails at others. That is the correct mathematical situation, and an
earlier version of FELRA's twin guard reported it as `unknown` — the defect that
surfaced from running a claim known to be false rather than from re-reading code.

---

## Route map

`ROUTE_MAP v1.7` names `A-U.2e.3 — Infinite-Support Elimination` next, and the
sweep's file ordering puts `AU2e3` at item 42. The two orderings agree again.

The round's own next-step list also asks to fold the Universal First-Crossing
Correction Cap into the B-line residue separation. Finding 1 is relevant there:
the cap is `c_fc ≤ L/(3(2^D − 1))`, and it is the *only* correction inequality
this round produces — the reset inequality is the same statement and adds no
constraint on `Y_a`.

## What this run does not claim

1. That a surviving first crossing exists. None was found, and finding one would
   refute the Terras coefficient-stopping conjecture.
2. That the conditional theorems apply to anything reachable by the Collatz map.
   They were checked as algebra on synthetic configurations.
3. That the clustering measurement verifies the Diophantine gate. It measures a
   trace below the threshold, with a control; the gate itself stays conditional.
4. That `C_∞` or `R_∞` is finite, or that the A/B Atomic Multiplication Theorem's
   hypothesis is satisfiable. Both are open, and both are stated as open in §9 of
   the round.
