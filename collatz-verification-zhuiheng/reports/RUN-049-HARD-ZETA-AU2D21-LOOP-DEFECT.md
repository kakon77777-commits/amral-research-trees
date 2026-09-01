# RUN-049 — Hard-Zeta A-U.2d.21: the round that names yesterday's finding, and a law that self-composition cannot see

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d21_Faithful_Return_Loop_Boundary_Layer_Coupling_Rigidity_bundle_v0.1.zip` (source item 68) — 21 sections, nine files.
**Tools:** [`src68_loop_defect.py`](../code/src68_loop_defect.py) · [`src68_drill.py`](../code/src68_drill.py) · [`src68_emit_report_block.py`](../code/src68_emit_report_block.py)
**Logs:** [`src68-au2d21.json`](../data/gate-logs/src68-au2d21.json) · [`src68-drill.json`](../data/gate-logs/src68-drill.json)

**Result: the mathematics verifies, and twelve of the bundle's thirteen counters are reproduced exactly from the definition — 7845 bridges, 18,603 budget levels, 39,395 faithful cycles, 12,000 endpoint and 12,000 source screening words, three synthetic blocks. The thirteenth differs only because I pool 157 self-compositions where the bundle runs 20. The round removes A-U.2d.20's three-sheet ambiguity by cutting at the true unique-label threshold `q ≥ s_k` and paying out of the SURPLUS `Σ(q−1)` rather than the full valuation sum, leaving `(2−β)h` of fully faithful cycle mass; then it shows the coupling that motivated the whole two-scale programme cannot work, because the endpoint modulo `3^K` sees only the final `K` valuations. Two findings. The bundle tests Theorem 11.1's defect semigroup law by composing each cycle with ITSELF, twenty times, with the comment "self-composition is enough to check algebra" — and it is not: at `D = C` the law is symmetric in its two coefficients, so the coefficient-swapped law gives the same answer. Measured here, the swapped law agrees with the true one on all 157 self-compositions and disagrees on all 218 distinct pairs. And three of the thirteen counters — 30,000 executions — cannot fail, in three shapes this sweep has already catalogued. One more thing is worth recording: the round's NO-GO 12.1 is exactly RUN-048's Finding 1, reached independently one round earlier by measurement, and the measurement is sharper than the prohibition — the quotient lift holds on 100% of contiguous cycles and fails on 100% of spliced ones.**

---

## The round's move, and its correction

A-U.2d.20 deleted edges with `q ≥ 2M` and got a linear cycle mass carrying three valuation sheets. This round deletes at the *true* unique-label threshold `q ≥ s_k = 2M/3` and pays for it out of the right resource:

> `Σ_{j=1}^{h}(q_j − 1) = ⌈βh⌉ − h`,  so  `A_k(s_k − 1) ≤ ⌈βh⌉ − h`.

The surplus, not the valuation sum. That is what makes the sharper cut affordable, and it leaves `(2 − β − o(1))h = 0.415…h` of **fully faithful** cycle mass — every retained edge label uniquely determined by its residue pair.

Then the round corrects its own programme. The endpoint tower is temporally local: `Z mod 3^K` depends only on the final `K` valuations, so a polynomial modulus `3^K = h^{O(1)}` has `K = O(log h)` memory and **screens everything a linear distance inside the bridge**. The source side is dual. The two-scale coupling A-U.2d.20 pointed at therefore cannot be done by the endpoint congruence alone.

What survives is the **loop defect**

> `𝔡_M(C; r) := (B_C − (2^{Q_C} − 3^{L_C})r) / M`

— an integer by the cycle certificate, with a semigroup law and a quotient-layer lift. That is the compression variable the next round has to renormalise.

## Finding 1 — the semigroup law is tested only against itself

Theorem 11.1 states

> `𝔡(CD; r) = 3^{L_D}·𝔡(C; r) + 2^{Q_C}·𝔡(D; r)`.

The shipped checker verifies it by calling `compose_defect(r, w, w, M)` — each cycle composed with **itself** — twenty times, with the comment *"self-composition is enough to check algebra."*

It is not. At `D = C` the right-hand side collapses to

> `(3^{L_C} + 2^{Q_C})·𝔡(C)`

which is **symmetric in its two coefficients**. So the wrong law

> `𝔡(CD) = 2^{Q_D}·𝔡(C) + 3^{L_C}·𝔡(D)`

— the same two factors attached to the opposite operands — gives *exactly the same value* on every self-composition. Twenty self-compositions cannot distinguish the published law from that one.

This gate evaluates both, on both kinds of input. The swapped law:

- **disagreed with the true law on 0 of 157** self-compositions;
- **disagreed on 218 of 218** distinct pairs.

Perfect separation. Self-composition is blind to the distinction and any distinct pair sees it immediately. The law itself holds: 0 violations on both kinds of input.

This is the same shape as the vacuity findings of the last five rounds, in a new place — a test whose *input distribution* removes the thing it was meant to test, rather than a guard or a cancelling parameter. And the repair costs nothing: the pool of cycles at a shared residue is already built.

## Finding 2 — three of thirteen counters cannot fail, and the shapes are all familiar

`faithful_core_asymptotic_algebra`, 10,000 iterations:

```python
eta = min(0.99, max(gamma+1e-3, eta))
assert gamma < eta          # arranged by the line above
assert 1-eta+gamma < 1      # the same inequality, restated
assert C_FAITH > 0          # a constant computed outside the loop
```

Identical, line for line, to A-U.2d.20's `fixed_power_high_lift_algebra`. Measured over the same ranges: the two inequalities agreed on all 10,000 samples and the constant varied on none.

`polynomial_precision_horizon_algebra`, 10,000 iterations, asserts `log(C·log h) − log θ − log h < 0` with `log h ≥ 100`. Smallest margin over the same ranges: **92.7**. It is not close.

`near_full_almost_total_loop_algebra`, 10,000 iterations, asserts `1/(log h)^A < 1` with `log h ≥ 100` and `A ≥ 0.05`. Smallest margin: **0.206**.

Thirty thousand executions, none of which can fail — the fifth consecutive round, and the shapes are all catalogued: arranged, restated, loop-invariant, and margin-never-approached. The blocks are honestly scoped, as always; what is worth saying is only what a reader takes `10000` to mean.

The other counters this round are **not** of that kind, and two are genuinely strong. `graph_cycle_certificates` and `fully_faithful_graph_cycles` run the brute-force label-uniqueness scan — for every retained edge, every valuation below `s_k` is tried and exactly one must produce the observed transition. That is 58,619 checks here and it is the one claim in the round that algebra alone cannot settle.

## The round names RUN-048's finding, one round later

Yesterday's recheck of A-U.2d.20 found that "return loop" named two objects: the loop-erased cycle, which the period bounds, and the contiguous orbit segment, which carries the certificate. I measured 14,539 of 34,970 segments exceeding the period and reported it as a semantic ambiguity between Corollary 10.2 and Theorem 11.1.

A-U.2d.21 says the same thing in its own words, in **section 12** and **NO-GO 12.1**:

> "Cycles produced by chronological loop erasure are exact labelled cycles in the modular residue graph, but after nested loops are erased they need not be contiguous intervals of the original integer orbit."

So the finding was correct and the authors reached it independently. That is the right outcome, and it makes the interesting question a different one: *how much* does it matter?

The measurement is sharper than the prohibition. Running the erasure with contiguity tracking over **38,338** graph cycles:

- Theorem 9.1's certificate holds on **every** one — contiguous and spliced alike, 0 violations, and 0 non-integral defects. The round's claim that the certificate survives splicing is exactly right.
- **11,198 cycles are contiguous**, **27,140 are spliced** (70.8%).
- Theorem 10.2's quotient-layer lift holds on **11,198 of 11,198** contiguous cycles and fails on **27,140 of 27,140** spliced ones. Not "may fail" — fails on every single one, with zero accidental survivals.

So NO-GO 12.1 is not a cautious hedge. Applying the quotient lift to an erased graph cycle without checking contiguity would be wrong seven times in ten at this scale, and never right when it is wrong.

## What else this recheck adds

**The screening theorems checked for sharpness.** "Z mod 3^K depends only on the final K valuations" is half a statement; a residue that never moved at all would satisfy it. So over 412 probes the gate also changes the **last** valuation — inside every horizon — and requires the residue to move (0 failures), and changes the **first** — outside it — and requires the residue not to move (0 failures). Both directions, on real bridge words as well as the bundle's synthetic ones.

**The surplus budget is live, and attained.** Unlike A-U.2d.20's loop-mass bound, which was positive on 4 levels in 3,826, Theorem 3.1 binds on **15,022 of 18,603** levels — one more alias edge would have broken it — and its smallest slack is exactly **0**. A bound worth checking, and the contrast with last round's is worth stating: the same author, one round apart, and one bound discriminates on 80.8% of instances where the other managed 0.1%.

**Both halves of the discrimination claim guarded.** My first version counted "the swapped law agrees on a distinct pair" as an observation, so a defect making the two laws identical moved nothing that fails. The drill caught it — the same shape as RUN-048's `clean_mass` gap, in my own headline finding this time. The positive half is now a population that must be non-empty.

## Two things about the bundle

The frontier and the checker report **agree** on all four numeric constants. `2 − β` is published as the float64 chain value, two ulps from the correctly rounded one — the same value RUN-045 flagged, with the same explanation, so it is consistent rather than new.

The source-validation record carries **zero per-file digests** and names only the three Markdown files; six of the nine files are absent from it entirely. That is the eighth consecutive round in which the record has changed shape. `CHECKSUMS.sha256` pins eight of nine and its nine embedded counter values agree with the checker report exactly, so nothing is unverifiable — the manifest is doing the work.

<!-- BEGIN GENERATED measured block: python code/src68_emit_report_block.py -->

**The population.** **7845** bridges from **7357** distinct sources (longest tail 73), of which **7845** have zero total lift and **0** do not — the fifth round running in which the positive-lift branch has no finite instance.

**Theorem 3.1's surplus budget, and it binds.** The surplus identity `sum(q-1) = ceil(beta h) - h` failed **0** times across **7845** bridges. The budget `A_k (s_k - 1) <= surplus` failed **0** times over **18603** bridge-precision levels. Unlike the loop-mass bound of the previous round, this one is **live**: **7910** levels carry an alias-large edge, the largest count on one bridge is **28**, and on **15022 of 18603 levels** (80.8%) one more alias edge would have broken it — with a smallest slack of **0**, so it is not merely tight but attained.

**Theorem 4.1's faithful core.** Over **18603** bridge-precision levels, **39395** cycles and **66290** retained edges: **0** edges at or above the period, **0** labels not unique in the faithful range over **58619** brute-force uniqueness checks — the claim that makes the core *faithful*, and the one thing in the round that cannot be checked by algebra alone. Cycles longer than the period **0**; total faithful mass **66290**. The finite mass bound failed **0** times and is positive on **2873 of 18603 levels** (15.4%), so it discriminates on a minority — better than the previous round's 4 in 3,826, still worth the denominator. The high-lift refinement failed **0** times.

**NO-GO 12.1, measured.** Over **38338** graph cycles from **7845** bridges: **0** fail to return to their residue, **0** violate Theorem 9.1's certificate, and **0** have a non-integral defect — the certificate is exact on *every* cycle, spliced or not, exactly as the round says. Theorem 10.2's quotient-layer lift is a different matter. Of the cycles, **11198 are contiguous** and **27140 are spliced** (70.8%). The lift holds on **11198 of 11198 contiguous** cycles and fails on **27140 of 27140 spliced** ones — with **0** spliced cycles where it happened to hold anyway. A clean separation: licensed everywhere it is licensed, and false everywhere it is not. Largest absolute defect seen **11172119**; **2832** defects are zero (7.4%), so the object is not degenerate.

**Theorem 11.1, and what self-composition cannot see.** Over **46** residue classes: **157** self-compositions and **218** distinct pairs. The true law failed **0** times on self and **0** on distinct pairs. The coefficient-swapped law — `2^{Q_D} d(C) + 3^{L_C} d(D)` instead of `3^{L_D} d(C) + 2^{Q_C} d(D)` — disagreed with the true one on **0 of 157** self-compositions and agreed with it on **0 of 218** distinct pairs, disagreeing on **218**. So the two laws are **indistinguishable under self-composition and separated by every distinct pair**. The bundle runs twenty self-compositions. **0** composite defects were non-integral and **0** composed cycles failed to return; **0** pairs turned out to be the same word.

**Theorems 6.1 and 7.1, on real words and for sharpness.** Over **103** real bridge words and **12000** synthetic endpoint words and **12000** synthetic source words: **0** endpoint screening violations, **0** disagreements between the whole-word residue and the k-term suffix formula, **0** source screening violations. Sharpness matters as much as the horizon: over **412** probes, a change to the LAST valuation — inside every horizon — moved nothing **0** times, and a change to the FIRST — outside it — moved something **0** times. Without both, "depends only on the final K" would be satisfied by a residue that never moves at all.

**Three of the bundle's thirteen counters cannot fail.** `faithful_core_asymptotic_algebra` runs **10000** iterations and asserts `gamma < eta` (arranged by the `max(gamma+1e-3, eta)` on the line above — **0** could have failed), `1-eta+gamma < 1` (the same inequality restated — **0** samples where the two differed), and `C_FAITH > 0` on a constant computed outside the loop (**0** samples where it varied). `polynomial_precision_horizon_algebra` runs **10000** and asserts a quantity whose smallest margin over the same ranges is **92.7** (**0** could have failed). `near_full_almost_total_loop_algebra` runs **10000** and asserts `1/(log h)^A < 1` with `log h >= 100`, smallest margin **0.2057** (**0** could have failed). Thirty thousand executions; fifth round running, and every shape is one this sweep has already catalogued.

**All twenty published cycle examples, rebuilt.** **0** disagreeing lengths, **0** valuation sums, **0** defects, **0** cycles failing to return, **0** certificate violations, **0** labels at or above the period.

| `M` | `r` | word | `L` | `Q` | defect |
| --- | --- | --- | --- | --- | --- |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 9 | 8 | `[1]` | 1 | 1 | 1 |
| 27 | 26 | `[1]` | 1 | 1 | 1 |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 9 | 8 | `[2, 1, 1]` | 3 | 4 | 13 |
| 9 | 8 | `[1]` | 1 | 1 | 1 |
| 27 | 17 | `[2, 1, 1]` | 3 | 4 | 8 |
| 81 | 71 | `[2, 1, 1]` | 3 | 4 | 10 |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 9 | 8 | `[1]` | 1 | 1 | 1 |
| 9 | 8 | `[1]` | 1 | 1 | 1 |
| 9 | 2 | `[1, 3]` | 2 | 4 | -1 |
| 27 | 26 | `[1]` | 1 | 1 | 1 |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 3 | 2 | `[1]` | 1 | 1 | 1 |
| 9 | 8 | `[1]` | 1 | 1 | 1 |
| 9 | 2 | `[1, 3]` | 2 | 4 | -1 |

**Constants.** 4 checked: **0** disagree with both readings of their own formula, 2 are the nearest double, 2 are the float64 chain, 0 brackets could not decide, and the frontier and the report disagree on **0**.

| constant | frontier | report | nearest double | verdict |
| --- | --- | --- | --- | --- |
| `beta` | 1.584962500721156 | 1.584962500721156 | 1.584962500721156 | exact |
| `fully_faithful_loop_mass_constant` | 0.4150374992788439 | 0.4150374992788439 | 0.4150374992788438 | +2 ulp, the float64 chain |
| `fully_faithful_loop_count_coefficient` | 0.6225562489182659 | 0.6225562489182659 | 0.6225562489182658 | +1 ulp, the float64 chain |
| `previous_three_sheet_loop_mass_constant` | 0.47167916642628127 | 0.47167916642628127 | 0.47167916642628127 | exact |

**Artifacts.** 9 files, 8 carrying a `CHECKSUMS` digest, **0** mismatches, **0** manifest lines naming a missing file; `CHECKSUMS.sha256` carry no digest anywhere. The source-validation record names **3** files and digests **0** of them, reporting `status = PASS` with **0** issues and **0** flags not true; its nine counter values disagree with the checker report **0** times. 6 files are absent from it: `CHECKSUMS.sha256`, `Hard_Zeta_AU2d21_checker_report.json`, `Hard_Zeta_AU2d21_constants_frontier.json`, `Hard_Zeta_AU2d21_theorem_ledger.json`, `SOURCE_VALIDATION_AU2d21.json`, `verify_Hard_Zeta_AU2d21_faithful_loop_boundary_coupling.py`.

**Ledger coverage.** The paper lists 16 proved items, 6 open problems and 9 NO-GO headings; the ledger carries 16, 6 and 6, with an `open` key (True). Open items with no trace: none. NO-GO headings with no trace: none. The heuristic deciding those lists has controls at both ends and failed neither (0, 0).

**Their counters beside mine**, keyed on their names rather than mine: 0 of 13 had no counterpart here, 0 are reported as zero, and **12 of 13 are reproduced exactly** from the definition.

| check | theirs | mine |
| --- | --- | --- |
| `finite_local_bridges` | 7845 | 7845 |
| `zero_lift_bridges` | 7845 | 7845 |
| `faithful_surplus_alias_budget` | 18603 | 18603 |
| `finite_fully_faithful_loop_mass` | 18603 | 18603 |
| `finite_high_lift_faithful_loop_mass` | 18603 | 18603 |
| `fully_faithful_graph_cycles` | 39395 | 39395 |
| `graph_cycle_certificates` | 39395 | 39395 |
| `defect_semigroup_self_composition` | 20 | 157 |
| `endpoint_temporal_screening` | 12000 | 12000 |
| `source_temporal_screening` | 12000 | 12000 |
| `polynomial_precision_horizon_algebra` | 10000 | 10000 |
| `near_full_almost_total_loop_algebra` | 10000 | 10000 |
| `faithful_core_asymptotic_algebra` | 10000 | 10000 |

**Instrument and drill.** 9 instrument self-checks, 0 failed. The mutation drill planted **50** defects: **50** caught by the check they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed.

<!-- END GENERATED measured block -->

## Instrument

Nine self-checks, each naming a world in which it fails.

The one that matters most is the pair around the composition law. `B_{CD} = 3^{L_D}B_C + 2^{Q_C}B_D` is checked on hand cases — and then, separately, that it is **not symmetric** in `C` and `D`. Without the second, the whole semigroup finding would be unfounded: if the composition law happened to be symmetric, self-composition would be a legitimate test and the criticism would be wrong. The asymmetry is the premise of the finding, so it is checked rather than assumed.

The rest: `⌈βℓ⌉` both ways round; the order of 2 modulo `3^k` with both maximal proper divisors ruled out; and the eraser on two hand cases, one that produces a cycle and one that produces none, with contiguity read in both.

## Drill

Fifty defects, one at a time, each planted at a pre-flighted unique anchor, with the gate restored byte for byte after every run — and every write retrying a transient OS error, after RUN-048 lost a drill to one. **50 caught, 0 missed, 0 malformed, both controls undisturbed, the gate byte-identical at the end.**

Nine needed re-aiming, and three of them found real gaps in this gate.

The most important: making the swapped law identical to the true one moved **nothing that fails**, because I had guarded only the half of my claim that says self-composition is blind, and left the half that says distinct pairs are not as an observation. That is precisely the RUN-048 shape — a claim with two halves and a counter on one — arriving inside my own headline finding one round later. Both halves are now guarded, and the discrimination is a population that must be non-empty.

Two more were mathematically identical to what they replaced: `x // m` and `(x − r) // m` are the *same integer* when `x = r + Mn` with `0 ≤ r < M`, and rewriting an instrument message changes no assertion. Three probed counters that already read zero or loosened tests that already found nothing — invisible from green, as always. And two were caught by the right counter under a different name.
