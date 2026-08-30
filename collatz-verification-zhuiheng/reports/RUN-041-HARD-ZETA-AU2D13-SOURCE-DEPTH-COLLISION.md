# RUN-041 — Hard-Zeta A-U.2d.13: a collision assembled from five finite links, and a constants family with one parameter

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d13_Dense_Source_Depth_Exponent_Collision_bundle_v0.1.zip` (source item 60) — 18 sections. Ships a checker report, a constants frontier, a theorem ledger, a route map, literature notes, a `CHECKSUMS.sha256`, a source-validation record, and a verification script. No builder this round.
**Tools:** [`src60_source_depth_collision.py`](../code/src60_source_depth_collision.py) · [`src60_drill.py`](../code/src60_drill.py) · [`src60_emit_report_block.py`](../code/src60_emit_report_block.py)
**Logs:** [`src60-au2d13.json`](../data/gate-logs/src60-au2d13.json) · [`src60-drill.json`](../data/gate-logs/src60-drill.json)

**Result: the mathematics verifies, and the round is the most structurally honest of the recent set — it proves a genuine unconditional no-go (positive-linear completed B-density is impossible) rather than another exponent improvement, and it says plainly that this does not close CASP. Every link of its five-step collision is finite and each was checked separately: the mod-12 source floor, two duration floors, the pigeonhole localization, Jensen and AM–HM on the origin gaps, and the source corridor. The one genuinely arithmetic input — the local best-approximation bound `‖qβ‖ > 1/((M_β(N)+2)q)` — was decided from the exact continued fraction of `log₂3` over 111,000 values of `q`, with zero violations and a tightest margin of 4.7%. Two things worth carrying forward. First, the whole constants family collapses to one rational parameter: `σ★ = 1/(1+θ★)` and `κ₁₃ = 1/(1+θ★²)`, closed forms the paper never states, which makes both exactly checkable. Second, `χ★` sits 27 ulps from its exact value — not an error but a three-link rounding chain ending in a 22.9-fold cancellation, and the only constant in the set where that matters. RUN-039's ledger finding, still open at RUN-040, is fixed: the `open` key is back, with the Collatz conjecture in it.**

---

## What it actually proves, and what it declines to

The previous four rounds each lowered an exponent. This one does something different in kind: it shows that a whole branch of the survivor space is empty.

> **Corollary 7.2.** There is no fixed `δ > 0` and unbounded sequence of `N` with `M_N ≥ δN`.

That is unconditional — no Huge-PQ assumption, no controlled continued fractions. The positive-linear completed-B premise that generated the Highly Nested escape in every previous round is gone. And §14 immediately says what that does *not* buy: a divergent branch could still use sublinear temporal support, so eliminating the dense branch "does not by itself close CASP or Collatz". The round is careful in the direction where carelessness would be rewarded.

The mechanism is a chain, and its shape is the interesting part:

> support count → source height → duration floor → localized depth and span → large slack → source-corridor contradiction

Each arrow is a finite statement. None of them needs the A-U.2d.12 block hierarchy — §11 says so explicitly, and that self-assessment is accurate: nothing in §§3–8 uses it.

## The constants family has one parameter, and two of its closed forms are unstated

The paper gives `ρ★ = 4.1164` and `θ★ = 1/(ρ★+1)`. It then quotes `σ★ = 0.8365051337388005…` from A-U.2d.3 as an inherited decimal with no formula, and defines `κ₁₃ := (ρ★+1)/(ρ★+1+θ★)`.

Taking `ρ★` as the exact decimal it is written as, all five constants are exact rationals — and two of them have much simpler forms than the paper gives:

| constant | closed form | exact rational |
| --- | --- | --- |
| `θ★` | `1/(ρ★+1)` | `2500/12791` |
| `σ★` | **`1/(1+θ★)`** | `12791/15291` |
| `κ₁₃` | **`1/(1+θ★²)`** | `163609681/169859681` |
| `λ₁₃` | `κ₁₃·θ★` | `31977500/169859681` |
| `χ★` | `(5σ★−4)/3` | `2791/45873` |

`σ★ = 1/(1+θ★)` is not stated anywhere in the bundle, and neither is `κ₁₃ = 1/(1+θ★²)`. Both hold exactly, and the published doubles agree with them to within one ulp *and* reproduce their float64 chains bit-for-bit — which is about as much evidence as a decimal can carry that the closed form is the right one rather than a numerical coincidence.

It matters practically: it turns two headline exponents from numbers one approximates into numbers one decides. `κ₁₃ < 1` is then not a numerical observation but the statement `θ★ ≠ 0`.

## The one arithmetic input, decided rather than estimated

Everything else in the round is combinatorics and convexity. §4.2 adds one real piece of number theory:

> `‖qβ‖ > 1/(𝒜_N q)` for every `1 ≤ q ≤ N`, where `𝒜_N = M_β(N) + 2`

This is the standard local best-approximation bound, and it is decidable: the partial quotients of `log₂3` come from an integer-comparison continued fraction, so no logarithm enters the derivation of `M_β(N)` at all. Checked over every `q` below three scales — 111,000 values — it holds with **zero** violations.

It is also not slack. At its tightest, `q·‖qβ‖·𝒜_N` comes to **1.047**, at `q = 665` — a convergent denominator, as it must be. A bound with 4.7% of margin at its worst point is doing real work, which is worth saying, because most of the inequalities in this sweep have had orders of magnitude to spare.

## Every other link, checked on its own

The exponent algebra was checked as *identities in the symbols*, not at the paper's own `(ρ, θ)`: §7's assembly is the identity `(1+θ)(ρ+1) − θρ = ρ+1+θ`, §8's produces `M^{5/2}/(𝒜^{3/2}N²)`. Evaluated over 400 random rational parameter pairs, both hold everywhere. Solving for `κ` and inverting the CF master for `(5κ−4)/3` likewise.

Jensen for `x^{−ρ}` and the AM–HM case held on every tuple, including forced equal-gap tuples where both sides meet exactly — the only configuration where a wrong exponent would still pass. The paper's own `ρ★` was checked separately through certified brackets rather than assumed to follow from the integer cases.

Lemma 5.1 held on every random family, and its control did what a control should: shortening the intervals below the window width broke the overlap in 382 of 400 families. A lemma that passes because it cannot fail is worth nothing, and this one can fail.

## Finding 1 — the object of the round does not occur on a real orbit

A B-injection is a first coefficient crossing with `Y_{e(s)} > Y_s`. Scanning 460,024 first-crossing intervals across every odd 3-free start below 40,000, there are **zero**. The closest any interval comes is `z/y = 0.9761`.

This is not a defect — these are theorems about the hypothetical injective divergent CASP branch, where B-injections are the defining feature. But it has a consequence for how this run reports: Theorems 4.1 and 6.1 are conditional on B-survival, so on real data their antecedent is never satisfied and "zero violations" would be a statement about an empty set.

So they were not reported that way. What is testable on every interval was tested instead:

- the exact product identity `z·2^Q = y·3^L·∏(1+1/(3Y_j))`, written with no `β` at all — **0 violations in 25,799**;
- the equivalence that turns B-survival into an inequality on `D`, namely `z > y ⟺ 2^Q < 3^L·P` — **0 violations**, and this is the step §4 actually uses;
- `D > 0` at every first crossing — **0 failures**;
- §4.2's *unconditional* slack floor `D > 1/(𝒜_N L)` — **0 violations in 25,799**;
- Theorem 4.1's algebra on the 96 intervals where its antecedent does happen to hold — **0 violations**.

One denominator is worth stating plainly because it looks like a finding and is not. Of 24,764 suffix-minimum first-crossing sources, **11,823 fall outside `7, 11 mod 12`**. A-U.2d.9's residue law is about *B sources*, of which there are none here, so those are not counterexamples — they are the size of the gap between the population the law constrains and the population a real orbit offers. Reporting that number as a violation would have been the exact mistake RUN-034 made with a 100% violation rate.

## Finding 2 — `χ★` is 27 ulps out, and the cause is a 22.9-fold cancellation

Four of the five constants sit within one ulp of their exact rationals. `χ★` sits at **−27**.

The cause is arithmetic, and it can be named exactly. `χ★ = (5σ★−4)/3` evaluated in float64 from the *published* `σ★` double reproduces the published `χ★` at **0 ulps** — so that is the route it took. And `5σ★ = 4.1825` minus `4` leaves `0.1825`: a **22.9-fold** loss of magnitude, which converts `σ★`'s single inherited ulp into roughly 23, plus the operations' own rounding.

So the chain is three links deep: `ρ★ = 4.1164` is not representable in binary → `θ★` inherits that → `σ★` inherits it again → `5σ★ − 4` amplifies it 23-fold. Nothing here is wrong; the last two digits of a constant derived from a rounded irrationality-measure bound are not load-bearing. It is recorded because the gate had to be taught to tell this apart from an error, and because the ulp budget it allows `χ★` is now *derived from the measured cancellation* rather than chosen.

## Finding 3 — twelve of twenty-three printed decimals assert digits they do not have

Across the paper and the route map these five constants are printed 23 times. **All 23 carry an ellipsis**, which asserts that the digits shown are correct and that more follow.

**Twelve are over-published** against the exact rational: `θ★` at 16 of 17 correct places, `σ★` and `κ₁₃` at 15 of 16, `χ★` at 15 of 17. Ten instances are exact — every one of them either a 10-digit rendering or `λ₁₃`, which is the single constant in the family whose float64 evaluation lands on the correctly rounded value. One `χ★` instance is truncated rather than rounded.

The pattern is consistent and benign: the artifacts print `repr()` of a float64 computation and append `\ldots`. It only becomes visible because the closed forms above make an exact reference available.

## Finding 4 — the ledger, mostly fixed

RUN-039 found A-U.2d.11 shipped no open-problems list at all; RUN-040 found A-U.2d.12 had not fixed it, and that the Collatz conjecture appeared nowhere in the ledger as an open problem.

**That is fixed.** This ledger has an `open` key carrying all four of §16.4's items, the Collatz conjecture among them. Proved items match at 10 and 10.

One gap remains, smaller: the paper has six numbered NO-GO headings and the ledger records five. The missing one is **NO-GO 12.5** — "current computations or probabilistic Syracuse mixing are needed" — which is the one asserting the proof needs no computational verification floor. Of the six it is arguably the one a downstream reader would most want machine-readable, since it is a claim about what the proof does *not* depend on.

The source-validation record still carries no digests at all: it lists seven files with encoding and delimiter checks and no hash on any of them. Third round running. It has gained `checker_exit_code`, `checker_reran` and `commit_gate_passed` fields, which is a different kind of provenance — a record that the checker was re-run, but not of what it was run against.

<!-- BEGIN GENERATED measured block: python code/src60_emit_report_block.py -->

**The constants family is one rational parameter.** Taking the paper's own `rho* = 4.1164` and `theta* = 1/(rho*+1)` at face value, every headline exponent has an exact closed form -- two of which the paper never states:

| constant | closed form | exact rational | published | vs exact | vs float64 chain |
| --- | --- | --- | --- | --- | --- |
| `theta_star` | 1/(rho*+1) | `2500/12791` | 0.19544992572902825 | +1 ulp | exact |
| `old_disjoint_backbone_sigma_star` | **1/(1+theta*)** | `12791/15291` | 0.8365051337388005 | -1 ulp | exact |
| `unconditional_support_exponent_kappa13` | **1/(1+theta*^2)** | `163609681/169859681` | 0.9632049232448516 | -1 ulp | exact |
| `unconditional_log_exponent_lambda13` | kappa13 * theta* | `31977500/169859681` | 0.1882583307100406 | exact | exact |
| `pq_pressure_at_old_sigma` | (5 sigma* - 4)/3 | `2791/45873` | 0.06084188956466748 | -27 ulp | exact |
| `controlled_CF_support_exponent` | 2 / (5/2) | `4/5` | 0.8 | exact | exact |
| `controlled_CF_log_exponent` | 1 / (5/2) | `2/5` | 0.4 | exact | exact |
| `support_PQ_factor_exponent` | (3/2) / (5/2) | `3/5` | 0.6 | exact | exact |

8 constants checked. **0** disagree with both readings of their own formula, **4** are the nearest double to the exact rational, and **4** are what the same formula gives when evaluated in float64 from an already-rounded parent. `chi*` is the outlier at -27 ulps, and the reason is arithmetic rather than error: `5 sigma* - 4` collapses 4.18 to 0.18, a **22.91-fold** loss of magnitude that turns `sigma*`'s single ulp into about that many. Its allowed budget here is derived from that factor (92 ulps), not chosen.

**The exponent algebra, as identities rather than at one point.** Section 7 assembles `M^(rho+1+th)/N^(rho+1)` out of `r ~ M^(1+th)/N` and `S ~ M^th`, which is the identity `(1+th)(rho+1) - th*rho = rho+1+th`; section 8 assembles `M^(5/2)/(A^(3/2) N^2)`. Checking either at the paper's own `(rho, theta)` would prove nothing about the transcription, so both were evaluated over 400 random rational parameter pairs: **0** and **0** violations. Solving the support inequality for `kappa` and inverting the CF master for the partial-quotient exponent gave **0** and **0**. The named instances come out `163609681/169859681`, `2791/45873`, `4/5` and `1/3`.

**The convexity steps.** Section 7 needs Jensen for `x^-rho` and section 8 the AM-HM case. Over 384 tuples: **0** and **0** violations, with 84 forced equal-gap tuples where both sides meet exactly -- the only place a wrong exponent would still pass. The paper's own `rho*` was then checked separately through certified brackets on 40 tuples: **0** violations, **0** undecided.

**The localization lemma.** Lemma 5.1 -- intervals of length `>= 4W` with starts inside one window of width `W` all contain the latest start -- held on 400 random families, **0** violations. Its control matters more: shortening the same intervals below the window width broke the overlap in 382 of 400 families, so the lemma is not passing because it cannot fail. The pigeonhole behind Lemma 5.2 was checked by construction rather than by formula on 400 families, **0** violations.

**The one arithmetic input, decided from the exact continued fraction.** Section 4.2 needs `||q beta|| > 1/((M_beta(N)+2) q)` for every `q <= N`. The partial quotients of `log2 3` come from `src47`'s integer-comparison route, so no logarithm decides anything; only the final comparison uses a sixty-digit bracket against a gap near `1e-7`. Across 3 scales and **111000** values of `q`: **0** violations, **0** undecided. The bound is not slack -- at its tightest, `q*||q beta||*A_N` comes to **1.0470**, at `N = 1000`, `q = 665`.

| `N` | `M_beta(N)` | `A_N` | tightest `q` | `q ||q beta|| A_N` |
| --- | --- | --- | --- | --- |
| 1000 | 23 | 25 | 665 | 1.0470 |
| 10000 | 23 | 25 | 665 | 1.0470 |
| 100000 | 23 | 25 | 665 | 1.0470 |

**On real orbits, the object of the round does not occur.** A B-injection is a first coefficient crossing with `Y_{e(s)} > Y_s`. Across 25799 first-crossing intervals from 885 orbits there are **0** of them; the closest any interval gets is `z/y = 0.9761` (orbit 703, `y = 3431`, `L = 29`). That is a fact about convergent orbits, not a defect -- the theorems are about the hypothetical divergent branch -- but it means Theorems 4.1 and 6.1 cannot be exercised here, and their zero violations would be vacuous. What is testable everywhere was tested instead.

The exact product identity `z 2^Q = y 3^L prod(1+1/(3Y_j))`, written with no `beta` at all, held on all 25799 intervals (**0** violations), and so did the equivalence that turns B-survival into an inequality on `D` (**0**). `D > 0` at every first crossing (**0** failures). Section 4.2's unconditional slack floor `D > 1/(A_N L)` was checked on **25799** intervals: **0** violations. Theorem 4.1's algebra was exercised on the **96** intervals where its antecedent actually holds: **0** violations.

A denominator worth stating plainly: of 24764 suffix-minimum first-crossing sources, 11823 fall outside `7, 11 mod 12`. That is **not** a counterexample to A-U.2d.9's residue law, which is about B sources, of which there are none. It is the size of the gap between the population the law constrains and the population a real orbit offers.

**The conditional theorems as algebra.** Over 400 synthetic parameter points: Theorem 4.1 **0** violations (antecedent satisfiable at 396 of them), the unconditional duration floor **0** (400), the section 6 corridor implication **0** of 400, and Lemma 5.2's pigeonhole **0** of 400.

**What the prose prints.** 23 decimal instances of these five constants appear across the paper and route map, **all 23 of them followed by an ellipsis** -- which asserts the digits shown are correct and more follow. **12** are over-published against the exact rational, 10 are exact to every digit, and 1 is truncated rather than rounded. `lambda13` is the only constant printed correctly everywhere it appears.

**Artifacts.** 9 files, 8 carrying a digest, **0** mismatches, **0** manifest lines naming a file that is not there; the only file with no digest anywhere is `CHECKSUMS.sha256`, which cannot pin itself. The validation record lists 7 files and **7 of them carry no hash** -- it records `checker_reran = True`, `commit_gate_passed = True` and `issues = []` instead. That is the third round running with a digest-free validation record.

**Ledger coverage — the finding from the last two rounds is fixed.** The paper lists 10 proved items, 4 explicitly open problems and 6 numbered NO-GO headings; the ledger carries 10, 4 and 5. It **has an `open` key** this time (True), and all 4 open items are present, the Collatz conjecture among them. NO-GO headings with no trace in it: ["12.5"].

**Their counters beside mine.** Different populations, so a difference is information rather than a fault; 0 of their checks had no counterpart here.

| check | theirs | mine |
| --- | --- | --- |
| `b_anchor_sequence` | 20000 | 25799 |
| `window_common_overlap` | 10000 | 400 |
| `cf_local_bound_diagnostic` | 16100 | 111000 |
| `support_exponent_algebra` | 5 | 8 |
| `pq_pressure_grid` | 200 | 400 |
| `localized_scaling_grid` | 5000 | 400 |

**Drill.** 33 defects planted one at a time, **33 caught**, 0 malformed, 0 missed; 0 were caught only by a counter other than the one aimed at. All 33 anchors matched exactly one place before anything was planted. 2 of 2 controls undisturbed, and the gate came back byte-identical.

<!-- END GENERATED measured block -->

## The instrument

Four things went wrong on my side.

**A power that was not the power I wanted.** The Jensen check began by raising `Fraction(1,g)` to the 41164th power, on the theory that this cleared the rational exponent `ρ★ = 41164/10000`. It does not — it computes `g^{−41164}`, a different inequality entirely, on integers with ninety thousand digits. Jensen holds for every `ρ > 0`, so the bulk now runs at small integer `ρ` where the arithmetic is exact and cheap, with a smaller bracketed sample at `ρ★` itself so the paper's own exponent is not taken on faith.

**The fail-open branch, reintroduced one round after learning it.** RUN-040's lesson was that a "this matches the float64 chain, so it is a rounding" branch must be bounded, or it swallows a constant that is simply wrong. I wrote that lesson down and then wrote the branch again with the chain test *before* the magnitude cap, which is the same failure with the clauses in a different order. Caught by reading the code while designing a defect aimed at it. The cap now comes first, and for `χ★` it is computed from the measured cancellation factor rather than picked.

**An identity dressed as a claim.** The first version of the §6 check asked whether `H < log₂(1+N/(3y₁))` follows from `(2^H−1)y₁ < N/3`. Those are the same statement rearranged, so the check could only ever measure my own logarithm — and it cost 36 seconds a run to do it. The claim in §6 is the *implication* from two inherited facts, `y_r > 2^H y₁` and `y_r − y₁ < L₁/3`, and that is now tested with rational `2^H` and no logarithm anywhere.

**A continued fraction computed four terms past its own need.** Asking for 15 partial quotients of `log₂3` takes 22.8 seconds; asking for 14 takes 0.04, because the fifteenth is 55 and deciding it means comparing integer powers with ten million bits. Fourteen terms reach `q_k = 190537`, past every scale the check uses. The same lesson as RUN-039's eight-minute gate, in a different costume: stop the computation where the claim stops needing it.

**Three defects that pointed the wrong way.** The drill's first pass caught 30 of 33 and classified three as "the mutation changes nothing" — correctly, and all three for the same reason: each *loosened* the thing it attacked. Widening the ulp cap cannot bite while every constant is right; dropping the upper side of `‖qβ‖` only makes the distance larger, so the bound gets easier; and taking convergents past the scale can only raise `𝒜_N`, which loosens it again. A defect a correct check tolerates is no evidence about the check, so all three were re-aimed to push the other way: a constant shifted past its budget whose float64 chain still matches (which is caught *only* because the cap is now tested first), a floor taken one too high, and convergents stopping far short of the scale. That is the harness doing its job — the verdict "changes nothing" is a fact about the defect, and reading it as a pass would have been the error.

**A gate that raised instead of reporting.** The re-aimed floor defect made every one of the 111,000 brackets undecided — which is exactly what `undecided_brackets` exists to say, and it is already a declared failure counter. But the row-building code then called `round(None, 4)` and the gate died with a `TypeError`. A traceback is the one verdict a gate must never return: it replaces a readable answer with an absence, and the drill can only classify it as malformed. The all-undecided path now reports itself. The defect the drill was aimed at turned out to be a defect in the drill's subject, which is the arrangement working.

**And the shell ate a backslash for the third time this session**, turning a `\n` inside a drill anchor into a real line break. The memory note for this says to use the Write tool for escape-heavy patches; I used a heredoc anyway. It was caught by compiling, as it has been every time, but the fix is to stop reaching for the heredoc, not to keep catching it.

The drill's totals are in the measured block above. Anchors were pre-flighted to exactly one match each, "the mutation changes nothing" is classified as malformed rather than missed, and the gate was verified byte-identical afterwards.

## What this run does not claim

It does not instantiate a divergent orbit, prove positive linear completed B-density, or certify the inherited `ρ★ = 4.1164` — that comes from A-U.2d.3 and is used here only through `‖qβ‖ ≥ c_δ q^{−ρ★}`, whose effective constant `c_δ` is not evaluated anywhere in this round or in mine. It does not verify Theorems 7.1 and 8.1 as asymptotic statements; it verifies the finite inequalities they are assembled from, and the exponent arithmetic that turns those into `κ₁₃` and the `4/5` barrier. The two theorems conditional on B-survival are checked as algebra, because real orbits supply no instance of their antecedent. It does not run the bundle's own verification script — every number here was recomputed independently, per the standing rule from item 35.

No Collatz claim is made or implied.
