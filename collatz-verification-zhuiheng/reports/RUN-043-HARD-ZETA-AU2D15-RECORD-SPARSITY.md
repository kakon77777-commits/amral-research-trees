# RUN-043 — Hard-Zeta A-U.2d.15: an inequality that needs no premise, and a checker report that publishes both its honest zeros and their vacuous twins

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d15_Suffix_Minimum_Record_Sparsity_Rigidity_bundle_v0.1.zip` (source item 62) — 19 sections. Ships a checker report, a constants frontier, a theorem ledger, a route map, literature notes, a `CHECKSUMS.sha256`, a source-validation record, and a verification script.
**Tools:** [`src62_record_sparsity.py`](../code/src62_record_sparsity.py) · [`src62_drill.py`](../code/src62_drill.py) · [`src62_emit_report_block.py`](../code/src62_emit_report_block.py)
**Logs:** [`src62-au2d15.json`](../data/gate-logs/src62-au2d15.json) · [`src62-drill.json`](../data/gate-logs/src62-drill.json)

**Result: the mathematics verifies. A-U.2d.14 ended on a genuine logical obstruction — divergence alone permits suffix-minimum times as sparse as `N^{o(1)}`, so no polynomial record lower bound follows from record theory — and this round supplies the Collatz-specific replacement, enclosing the record count between two slack coordinates and deriving `Δ_N + δ_N ≥ (1−o(1))log₂N`. It also collapses one of the previous round's three escapes: the A-envelope is now bounded by the current slack. The piece I could test hardest is §10's `N₁(s,g) ≥ (2−β)g + (δ_{s+g}−δ_s)`, which needs no premise at all — 127,813 pairs rooted at suffix minima and 59,130 rooted anywhere, zero violations, and a tightest slack of exactly zero, so the bound is attained rather than loose. Theorem 4.1's population, by contrast, is empty on a convergent orbit: 8,447 record edges all ascend, so the total downward variation it bounds is identically zero. The bundle says this itself, twice, with honest zero counts — and then reports 23,018 and 35,616 evaluations of the same fact in the form where it cannot fail. One regression: the source-validation record has lost the per-file digests it gained one round ago.**

---

## What it adds

The previous round left a hole it named precisely. `A-U.2d.14`'s NO-GO 11.1 showed that an abstract divergent integer sequence can have suffix-minimum times `t_j = 2^{j²}`, hence only `√(log₂N)` records — so record theory alone will never yield a polynomial lower bound. The missing input had to be Collatz-specific.

This round supplies it by bounding the record count from both sides in terms of slack:

> `2^{−Δ_N}·N^{1−o(1)} ≤ 𝖱_N ≤ 2^{δ_N}·N^{o(1)}`, hence **`Δ_N + δ_N ≥ (1−o(1))log₂N`**

with `δ_N` the current slack and `Δ_N = max_{c₁≤n≤N} δ_n` the historical maximum. The upper bound comes from the record values being increasing elements of `7,11 mod 12` (so `Y_{c_R} ≥ 6𝖱_N − 1`) together with the exact multiplier; the lower bound from the state ceiling `Y_max ≤ 2^{Δ_N}N^{o(1)}` and the fact that a record-free gap can only contain as many distinct 3-free odd states as fit below that ceiling.

It also merges one of the previous round's escape coordinates: since every A-renewal is a suffix minimum, `E_A(N) ≤ δ_N + o(log N)`. The trichotomy is down to two independent coordinates plus the inherited partial-quotient pressure.

## The piece that needs no premise

Most of this sweep's recent rounds have had a central theorem conditional on the hypothetical divergent branch, and I have spent several reports explaining which populations were empty. §10 is different.

> `N₁(s,g) ≥ (2−β)g + (δ_{s+g} − δ_s)`

Its derivation is two steps, neither of which uses suffix minimality: every non-one valuation is at least two, so `K_t − K_s ≥ 2g − N₁`; and `K_t − K_s = βg − (δ_t − δ_s)` is the definition of `δ`. So the inequality holds on **every** segment of **every** orbit.

I checked it on 127,813 `(s,g)` pairs rooted at suffix minima and, as a control that the premise really is unnecessary, on 59,130 more rooted at arbitrary indices. **Zero violations in both.** The valuation-sum identity it rests on: zero violations.

The tightest case has slack exactly **0.0** — at `g = 1` with `N₁ = 1`, where the inequality is an equality. A bound that is attained is not one you can pass by accident, and the drill confirms it: adding **one** to the right-hand side turns it red.

Worth noting separately: the bare floor `(2−β)g`, without the slack correction, also never failed on this population. The correction term is what makes the inequality exact, but on real orbits the `41.5%` density floor holds on its own.

## What is not testable, and the bundle says so first

Theorem 4.1 bounds `V⁻_rec(N) = Σ(δ_{c_j} − δ_{c_{j+1}})_+`, the total *downward* variation of slack sampled at records.

On a convergent orbit there is none. RUN-042 established that every true suffix minimum is an A-renewal — a suffix minimum with a first crossing would be a B-injection by definition, and there are none — so record slack strictly ascends. Measured here: **8,447 record edges, 8,447 ascending, 0 descending, 0 undecided.** `V⁻_rec` is identically zero, and Theorem 4.1 has nothing to constrain.

The bundle knows. §18 says plainly that "known terminating integer orbits do not supply an example of the hypothetical divergent B-record descent mechanism, so the checker does not pretend to instantiate one", and its report carries two zero counts saying the same thing numerically: `record_slack_drop_edge: 0` and `record_descent_implies_crossing: 0`. That is the right way to publish an empty population, and it is worth saying so — three rounds of this sweep have turned on exactly this distinction.

What *is* testable underneath the theorem was tested: the exact multiplier `Y_b·2^p = Y_a·3^g·P` (written with no `β`, so no bracket decides it) on all 8,447 edges, the product concatenation `∏P_j = 𝒫_{c₁,c_R}` exactly, Lemma 11.1's value span `Y_max − Y_s ≥ 3g − 7`, the `U₆` capacity bound behind it, and §7's state-ceiling identity. All zero violations.

## Finding 1 — the honest zeros have two vacuous twins in the same report

The checker report lists nine checks. Two are zero, correctly. Two others are large:

| check | theirs |
| --- | --- |
| `record_slack_drop_edge` | **0** |
| `record_descent_implies_crossing` | **0** |
| `record_total_down_variation` | 23,018 |
| `record_tail_drop` | 35,616 |

These are not independent. `record_slack_drop_edge = 0` says no record edge descends. If no edge descends, then `V⁻_rec = 0` on every chain, so every one of the 23,018 `record_total_down_variation` evaluations was checking `0 < log₂𝒫` — true whenever `𝒫 > 1`, which it always is. The same applies to the 35,616 tail-drop evaluations: with no descent, `(δ_{c_R} − δ_N)_+ = 0`.

This follows from their own two numbers, not from any assumption about their code. I did not run their script.

It matters because of how the two shapes read. A reader scanning the report sees `23,018` beside `record_total_down_variation` and concludes the descent budget theorem is well exercised. It is exercised zero times; it is *evaluated* 23,018 times in the configuration where its left-hand side is zero. My own counters report the same distinction the other way round — `theorem_4_1_checked: 0` — and the zeros are the informative number.

## Finding 2 — the validation record has lost its digests again

RUN-039, RUN-040 and RUN-041 each reported that the source-validation record carried encoding checks and no hashes. RUN-042 reported that fixed: `SOURCE_VALIDATION_AU2d14.json` carried a `sha256` per file, and all six recomputed correctly.

`SOURCE_VALIDATION_AU2d15.json` has **no per-file entries at all**. Its keys are `round, date, status, canonical_math, markdown, json_parse, python_compile, checker_commit_gate, checker_stdout_sha256, issues` — aggregate verdicts rather than a per-file table.

It is not simply worse. It has gained `checker_stdout_sha256`, which pins the checker's *output* — a different and useful kind of provenance, and one nothing else in the bundle records. But it pins the output, not the inputs, and the per-file digests that would let a reader verify what was checked are gone one round after appearing.

`CHECKSUMS.sha256` still covers 8 of the 9 files (all but itself), and all eight recompute correctly, so the bundle's coverage is intact. It is the validation record's own content that regressed.

A side effect worth naming: with no per-file digests in that record, the code path that verifies them has nothing to verify. My drill planted a defect that inverts that comparison and it was correctly reported as changing nothing — the branch is unreachable on this bundle.

## Finding 3 — `2−β` is two ulps out, by the usual route

`q1_density_floor_2_minus_beta` is published as `0.4150374992788439`. The nearest double to the true `2 − log₂3` is `0.4150374992788438`, two ulps below. And `2.0 − published_β` in float64 gives the published value at **0 ulps**.

`β` itself is published exactly. The two ulps come from the subtraction: `2 − 1.585` collapses the magnitude by a factor of about 4.8, which is enough to turn `β`'s last-bit rounding into two. The same shape as `χ★`'s 27 ulps at RUN-041, at a much smaller scale.

The ledger is otherwise clean: 14 proved items against the paper's 14, 5 open against 5, 8 NO-GO headings against 8, and nothing missing from any of them.

<!-- BEGIN GENERATED measured block: python code/src62_emit_report_block.py -->

**Section 10's inequality, on segments that need no premise.** `N_1(s,g) >= (2-beta) g + (delta_{s+g} - delta_s)` was checked on **127813** pairs rooted at a suffix minimum and, as a control that the root really is unnecessary, **59130** rooted anywhere: **0** and **0** violations. The valuation-sum identity it rests on failed **0** times, and no valuation below one was seen (**0**). The tightest case has slack **0.0** — attained, not loose — at `g = 1` with `N_1 = 1`. The bare floor `(2-beta)g` without the correction term failed **0** times on this population.

**The record process.** 1085 orbits carried two or more records (longest chain 15), giving **8447** record edges. The exact multiplier `Y_b 2^p = Y_a 3^g P` — written with no `beta`, so no bracket decides it — failed **0** times; the product concatenation `prod P_j = P_{c1,cR}` **0**; record values were non-increasing **0**; Lemma 11.1's span `Y_max - Y_s >= 3g-7` **0** of 8447; the `U_6` capacity behind it **0**; and section 7's state-ceiling identity **0**.

**Theorem 4.1 has an empty population, and so does its tail.** Of the 8447 record edges, **8447 ascend, 0 descend, 0 are undecided**. So `V^-_rec` is identically zero: the theorem was exercised **0** times (**0** violations), and the tail bound **0** times out of 1085 tails examined. The bundle reports the same thing — `record_slack_drop_edge` and `record_descent_implies_crossing` are both zero in its own checker report, and section 18 says it in prose.

**The enclosure, as the exponent algebra it is.** Over 400 grid points, with the slacks sampled relative to `log2 N` so the hypothesis is reachable (**291** of them satisfy it): Theorem 8.1 **0** violations, Corollary 8.2 **0**, and the inversion behind Corollary 6.3 **0**.

**Corollary 12.1 needs a B source.** Across 1314 orbits and **9637** suffix minima there are **0**, so it was exercised **0** times. That denominator is the report, not the zero violations.

**Constants.** 5 checked: **0** disagree with both readings of their own formula, 3 are the nearest double, 2 are what the same formula gives in float64, and 0 brackets could not decide.

| constant | published | nearest double | vs bracket | vs float64 chain |
| --- | --- | --- | --- | --- |
| `beta` | 1.584962500721156 | 1.584962500721156 | exact | exact |
| `q1_density_floor_2_minus_beta` | 0.4150374992788439 | 0.4150374992788438 | +2 ulp | exact |
| `theta_star` | 0.19544992572902825 | 0.19544992572902822 | +1 ulp | exact |
| `inherited_controlled_renewal_support_exponent` | 0.8 | 0.8 | exact | exact |
| `rho_star` | 4.1164 | 4.1164 | exact | exact |

**Artifacts.** 9 files, 8 carrying a `CHECKSUMS` digest, **0** mismatches, **0** manifest lines naming a missing file; the only file with no digest anywhere is `CHECKSUMS.sha256`. The source-validation record carries **0 per-file entries and 0 digests** (`carries none`) — it reports `status = PASS` and does carry a checker-stdout digest, but the per-file table RUN-042 verified is gone. Its top-level keys are now ``canonical_math`, `checker_commit_gate`, `checker_stdout_sha256`, `date`, `issues`, `json_parse`, `markdown`, `python_compile`, `round`, `status``.

**Ledger coverage.** The paper lists 14 proved items, 5 open problems and 8 NO-GO headings; the ledger carries 14, 5 and 8, with an `open` key (True). Open items with no trace: none. NO-GO headings with no trace: none. The heuristic that decides those two lists now has controls at both ends and failed neither (0, 0).

**Their counters beside mine.** 0 of their checks had no counterpart here; **2** of the nine they report as zero, and **2** of those we both report as zero. The two large counts beside them — `record_total_down_variation` and `record_tail_drop` — are evaluations of a quantity their own `record_slack_drop_edge = 0` makes identically zero.

| check | theirs | mine |
| --- | --- | --- |
| `exact_segment_product_identity` | 14000 | 8447 |
| `record_first_step_q1` | 90759 | 127813 |
| `record_values_mod12` | 90759 | 8447 |
| `record_slack_drop_edge` | 0 | 0 |
| `record_total_down_variation` | 23018 | 0 |
| `record_tail_drop` | 35616 | 0 |
| `q1_density_exact_algebra` | 90759 | 127813 |
| `record_free_span_units` | 90759 | 8447 |
| `record_descent_implies_crossing` | 0 | 0 |

**Instrument self-checks:** 9, 0 failed.

**Drill.** 30 defects planted one at a time, **30 caught**, 0 malformed, 0 missed; 0 were caught only by a counter other than the one aimed at. All 30 anchors matched exactly one place before anything was planted. 2 of 2 controls undisturbed, and the gate came back byte-identical.

<!-- END GENERATED measured block -->

## The instrument

This round the drill found two genuine misses — defects my gate did not notice at all — and that is the first time in several rounds. Both were real holes.

**A classification with no failure counter.** The record-slack direction test sorts each edge into ascending, descending or undecided. Inverting it flipped all 8,447 edges from ascending to descending and **nothing complained**: all three counters are observations, and the derived `theorem_4_1_checked` merely fell to zero, which it already was. The fix is an invariant rather than another observation: `V⁻_rec` accumulates *positive parts*, so a negative total means the classification and the arithmetic have come apart. That is now a failure counter, and the defect lands on it.

**A coverage heuristic with no control.** The ledger check reports two lists — open items and NO-GO headings with no trace in the ledger — and those lists were read by nothing. A mutated heuristic that accuses *everything* went unnoticed. Worse, the honest version had already false-positived for real this round: it flagged "CASP and the Collatz conjecture" as absent because the ledger abbreviates it to "CASP and Collatz" and my word filter dropped `CASP` as too short. So the heuristic was both wrong and unguarded. It now has controls at both ends — text certainly present must be found covered, text certainly absent must not — and both are failure counters.

Before changing it I checked that the corrected heuristic still flags RUN-041's NO-GO 12.5 as genuinely absent from the A-U.2d.13 ledger. It does, so that published finding stands.

**A grid whose antecedent almost never held.** The enclosure algebra sampled `δ_N` and `Δ_N` independently of `log₂N`, so Corollary 8.2's hypothesis was satisfiable at 40 of 400 points and the defect aimed at it changed nothing. Sampling the slacks relative to `L` takes it to 291 of 400. This is the same vacuity RUN-042 found in a threshold check whose sample never straddled its threshold — a grid that does not reach the region a claim lives in is not testing the claim.

**Three defects that could not bite, and one that could not be built.** Two swapped a quantity for another of the same value — a residue pair with identical density, a guard rather than the strict test it guards. One attacked the ulp-cap ordering, which cannot be planted alone: with every constant correct there is nothing for a mis-ordered cap to let through, so it was re-aimed at a constant shifted past its cap whose float64 chain still matches. And the validation-digest defect is unreachable on this bundle for the reason in Finding 2.

**A killed drill left its defect behind.** The first attempt hit a two-minute timeout and was terminated between planting `D21` and its `finally` restore, leaving the mutated residue test live in the gate. The pristine sidecar is there for exactly this and worked: the file was restored, the gate re-verified green, and the run relaunched. It is the third time in this sweep's history that a drill has been killed mid-plant, and the first where the protection was exercised rather than merely present.

The drill's totals are in the measured block above. Anchors were pre-flighted to exactly one match each, and the gate was verified byte-identical afterwards.

## What this run does not claim

It does not instantiate a divergent CASP orbit. Theorem 4.1, its tail corollary and Corollary 12.1 are conditional on record descents or on a B source, and a convergent orbit supplies neither — 9,637 suffix minima and zero B sources — so those are reported with their denominators rather than as green. It does not verify the asymptotic forms of Theorems 6.1, 7.2 or 8.1; it verifies the finite identities and the exponent algebra they are assembled from, on a grid whose antecedent is satisfiable. It does not certify the inherited `ρ★ = 4.1164`, the A-U.2d.12 product theorem whose `C_ε` every asymptotic step here consumes, or the López–Stoll criticality input, which §2.3 itself marks as not needed for this round's principal theorems. It does not run the bundle's own verification script — every number here was recomputed independently, per the standing rule from item 35.

No Collatz claim is made or implied.
