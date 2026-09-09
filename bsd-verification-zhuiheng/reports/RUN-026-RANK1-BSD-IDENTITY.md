# RUN-026 — the rank this arm had never verified, and the extrapolation defect that closing it exposed

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`06_Phase1_Agent_Experiment`](../../../amral/public/bsd/phase0/files/06_Phase1_Agent_Experiment.md) §3's group R1 — the rank-1 BSD identity at `37a1` and `43a1` — and this tree's own `canonical_height`
**Tools:** [`src28_rank1_bsd_identity.py`](../code/src28_rank1_bsd_identity.py), [`src20_bsd_consistency.py`](../code/src20_bsd_consistency.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src28-rank1-bsd-identity.json`](../data/gate-logs/src28-rank1-bsd-identity.json), [`src20-bsd-consistency.json`](../data/gate-logs/src20-bsd-consistency.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the rank-1 BSD identity closes with every term computed in this tree — the first identity in this line for which that is true. At `37a1` the ratio is `1.0000000017` and at `43a1` `1.0000000009`, with `L'(E,1) = 2 Σ (a_n/n) E₁(2πn/√N)` converged to machine precision at 800 terms, the period agreeing with a direct integration over `E(R)` to `6 × 10⁻¹¹` and `1 × 10⁻¹¹`, and the canonical height carrying the residual. Closing the gap RUN-025 identified — this arm had verified R0 and R2+ and never an R1 curve — exposed a defect in `canonical_height`: it returned `richardson2` unconditionally, and `richardson2` is the **worst** of its three extrapolation levels at every depth tested. `Reg(389.a1)` moves from RUN-017's `0.152460306865` with a claimed residual of `1.6 × 10⁻⁶` to `0.15246013936831948` with a residual of `9.4 × 10⁻⁹`, which is `3.9 × 10⁻⁸` from the independent value in the rank-uniform document. The two agree to seven significant figures; nothing concluded moves, and RUN-017 and RUN-023 now carry correction notes.**

---

## Why rank 1, and why now

`06_Phase1_Agent_Experiment` §3 organises its benchmark into R0, R1 and R2+.
RUN-025, auditing that specification, had to record that this arm had verified
**R0** (`696.e1`, RUN-014) and **R2+** (`389.a1`, RUN-011/020/022/023) and never
once an R1 curve. That is a gap in this tree's own assurance, along exactly the
axis the experiment is organised by, and the kind an attack needs told.

It is also the rank where this arm can do the most. At rank 0 the L-value *is*
the number; at rank 2 RUN-023 took the leading coefficient from a document
because computing `L''` is real work. At rank 1 the root number is `−1` and the
classical leading-term formula

$$L'(E,1)=2\sum_{n\ge1}\frac{a_n}{n}\,E_1\!\left(\frac{2\pi n}{\sqrt N}\right)$$

uses exactly the exponential integral `src15` already implements in-gate. So

$$L'(E,1)=\Omega_E\cdot\hat h(P)\cdot\prod_p c_p\ \big/\ \#E(\mathbf Q)_{\rm tors}^2$$

can be closed with **every term computed here**.

## The identity, on both period branches

`37a1` has `Δ = 37 > 0` and two real components; `43a1` has `Δ = −43 < 0` and
one. RUN-017 found the `Δ > 0` branch doubled and RUN-023 gave the repair its
first external test at rank 2; this adds a rank-1 test on **each** branch, so a
period fault cannot hide in the rank.

| | `37a1` | `43a1` |
| --- | --- | --- |
| conductor recomputed | 37 ✓ | 43 ✓ |
| reduction | `I₁`, `c = 1` | `I₁`, `c = 1` |
| torsion bound | 1 | 1 |
| root number | **−1** | **−1** |
| `L'(E,1)` | `0.30599977383405214` | `0.3435239746184784` |
| converged at 800 terms to | `0` | `0` |
| `Ω` (AGM) | `5.986917292463919` | `5.468689529967584` |
| integration vs AGM | `6.1 × 10⁻¹¹` | `1.3 × 10⁻¹¹` |
| `ĥ(P)` at depth 12 | `0.051111408154313` | `0.062816507033411` |
| `Ω·ĥ·∏c/t²` | `0.30599977332123596` | `0.3435239743227509` |
| **ratio** | **`1.0000000017`** | **`1.0000000009`** |

**The L-series converges at 800 terms and stays there to 20,000** — `E₁(2πn/√37)`
decays exponentially, so by `n = 800` the argument is ~826 and the tail is below
double precision. That is measured, not assumed: the sum is taken at three
truncations and the last two are bit-identical.

**Which term carries the residual is measured too**, by closing the identity at
three doubling depths:

| depth | `37a1`: height self-consistency → identity | `43a1`: height self-consistency → identity |
| --- | --- | --- |
| 10 | `9.7 × 10⁻¹⁵` → `1.68 × 10⁻⁹` | `4.4 × 10⁻⁷` → `2.94 × 10⁻⁶` |
| 11 | `3.9 × 10⁻¹⁴` → `1.68 × 10⁻⁹` | `2.0 × 10⁻⁸` → `2.70 × 10⁻⁷` |
| 12 | `1.6 × 10⁻¹³` → `1.68 × 10⁻⁹` | `1.0 × 10⁻⁸` → `8.61 × 10⁻¹⁰` |

At `43a1` the two columns move together, so the residual **is** the height. At
`37a1` the height is already converged at depth 10 and the identity does not
improve, so its `1.68 × 10⁻⁹` is the floor set by the period and the L-series
instead. Each curve names its own limiting term rather than sharing a claim.

## The defect: `richardson2` was never the best

`canonical_height` computes `ĥ(P) = lim h(x(2ⁿP))/4ⁿ` with two Richardson steps
and returned the second unconditionally. Tracing the sequences at `37a1`, depth
10:

| | last two entries | gap |
| --- | --- | --- |
| raw | `0.051111408154108`, `0.051111408154118` | **`1.0 × 10⁻¹⁴`** |
| `richardson1` | `0.051111661108595`, `0.051111408154121` | `2.5 × 10⁻⁷` |
| `richardson2` | `0.051111195125703`, `0.051111323835963` | `1.3 × 10⁻⁷` |

`richardson1` is **not monotone** in `n`, and `richardson2` is built from its
last two — so it takes a value already correct to `3 × 10⁻¹⁵` and returns one
wrong by `8.4 × 10⁻⁸`. The underlying reason is that `h(x(2ⁿP))/4ⁿ` has no clean
`1/4ⁿ` error expansion for these curves: the local contributions at bad primes
do not decay that way, so `r1` carries structure a second extrapolation
misreads.

On `389.a1` the same defect ran through the regulator, and the parallelogram law
shows it at a glance:

| level | residual at depth 8 | residual at depth 10 |
| --- | --- | --- |
| raw | `+1.42 × 10⁻⁵` | **`+9.45 × 10⁻⁹`** |
| `richardson1` | **`−5.13 × 10⁻⁷`** | `+1.63 × 10⁻⁸` |
| `richardson2` | `−2.41 × 10⁻⁵` | `+1.60 × 10⁻⁶` |

**`richardson2` is worst at both depths**, by one to two orders of magnitude.
RUN-017 reported its `1.6 × 10⁻⁶` as the method's precision.

## The repair, and why the selector is the parallelogram law

`ĥ(P+Q) + ĥ(P−Q) = 2ĥ(P) + 2ĥ(Q)` holds exactly for the true heights, so its
residual is an **external** measure of a level's quality — and it is the right
one, because the obvious alternative fails. Letting each of the four heights
pick its own level by its own self-consistency gave a *worse* regulator
(residual `−5.0 × 10⁻⁷` at depth 10 against `9.4 × 10⁻⁹`), because the law is
only exact when all four are computed the same way: a mixed selection breaks the
identity being used to judge it.

So `regulator` chooses **one** level for all four, by smallest residual, and
reports all three. For a single height with no law available — the rank-1 case —
`canonical_height` chooses by its own sequence's last-two agreement, which picks
`raw` at `37a1` with a gap of `9.7 × 10⁻¹⁵`.

**What moves, and what does not.** `Reg(389.a1)` goes from `0.152460306865` to
`0.15246013936831948`. Those agree to seven significant figures, and RUN-017's
conclusion — a non-zero regulator, hence `P` and `Q` independent, hence a third
independent proof of rank ≥ 2 — is untouched. What was wrong is the **precision
that round claimed**: twelve printed digits and a residual it attributed to the
method. RUN-017 and RUN-023 now carry correction notes pointing here, and the
gate logs in this repository carry the corrected values. RUN-023's comparison
improves as a side effect: our regulator against the rank-uniform document's now
differs by `3.9 × 10⁻⁸` rather than `1.3 × 10⁻⁷`.

## A vacuous check, for the third time in three rounds

The check written to catch the mixed-level regulator **passed on it**. It
compared the chosen level's residual against `min` over the reported levels —
and a mixed-level regulator reports exactly one, so the minimum was that same
number and the comparison held for free. RUN-024 found this class in `src02`,
RUN-025 found a milder form in the Ш scanner, and here it is again in a check
written *by* the round that had just described it.

The fix is the same shape each time: assert that the population the condition
ranges over is the one intended. The check now requires all three levels to be
present, the choice to be among them, and the chosen residual to beat
`richardson2` strictly.

## The drill went red on this round's own changes, and found two things

The first run reported **one defect caught by the wrong check and one control
disturbed**. Both were consequences of the repair above, and neither was
visible any other way.

**A control stopped being one.** "Naive height reads the numerator only" had sat
in the controls since RUN-017 with an explicit reason: reading only `x`'s
numerator rather than `max(|num|, den)` *is* wrong, but it moves the regulator
by `1.16 × 10⁻⁷` "and the regulator is only known to about `1.6 × 10⁻⁶`". **That
`1.6 × 10⁻⁶` was `richardson2`'s error, not the method's.** With the level chosen
by the parallelogram law the regulator is known to `9.4 × 10⁻⁹`, the
perturbation is two orders of magnitude above that, and a defect the computation
could not resolve became one it can. It is now a defect named for
`rank1-identity`, whose 37a1 tolerance of `1 × 10⁻⁸` is the first thing in this
tree precise enough to see it.

**And the regulator learned to route around a defect.** "Richardson extrapolates
against `1/2ⁿ` instead of `1/4ⁿ`" was named for the `regulator` check. Since the
level is now chosen by measurement, a broken Richardson step is simply not
selected — the regulator falls back to `raw` and the check goes green. Measured:
under the corruption the depth-8 regulator moves from `0.15246089` to
`0.15245561` and its residual from `−5.1 × 10⁻⁷` to `+1.4 × 10⁻⁵`, and every
structural assertion in `height-level-selection` still passed, because those
test the **selection logic** and nothing about **what it selects from**.

So the check gained a quality assertion with a measured threshold — at depth 8
an intact first Richardson step reaches `5.1 × 10⁻⁷` and the fallback reaches
`1.4 × 10⁻⁵`, so `5 × 10⁻⁶` separates them and nothing tighter is claimed — and
the defect was renamed to it. **Robustness had bought insensitivity**, which is
worth saying plainly: a computation that can avoid its own broken parts will
stop reporting that they are broken.

## The drill

**113 defects, 113 caught by the check named for each — none uncaught, none
caught by the wrong check. 19 controls, none disturbed, over 54 checks. Eighteen
minutes and two seconds, on the second run; the first is above.**

## What this round does not claim

* **`#Ш = 1` is assumed at both curves**, as the identity's remaining factor. It
  is not computed, and the identity closing is not evidence about Ш — the
  substitution Phase 0 §6 names and RUN-019 audited applies here unchanged.
* **The rank is cited.** That `37a1` and `43a1` have rank 1 with the stated
  generators comes from the literature, as `389.a1`'s rank 2 has in every round
  of this arm.
* **Two curves are two curves.** They were chosen to separate the two period
  branches, not to be a family.
* **`L'` uses the classical formula for `w = −1`** and is meaningless if the
  root number is wrong; both were computed and both came out `−1`, decided.
* **The height's true convergence is not proved**, only measured. The depth
  table shows the residual tracking the height's self-consistency, which is
  evidence about where the error lives and not a bound on it.
