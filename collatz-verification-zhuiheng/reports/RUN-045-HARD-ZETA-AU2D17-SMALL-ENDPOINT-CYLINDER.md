# RUN-045 — Hard-Zeta A-U.2d.17: the round whose central identity is a definition, and whose content is one line below it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d17_Small_Endpoint_Critical_Bridge_Cylinder_Rigidity_bundle_v0.1.zip` (source item 64) — 20 sections. Ships a checker report, a `CHECKER_STDOUT`, a constants frontier, a theorem ledger, a route map, literature notes, a `CHECKSUMS.sha256`, a source-validation record, a verification script and a bundle README.
**Tools:** [`src64_small_endpoint_cylinder.py`](../code/src64_small_endpoint_cylinder.py) · [`src64_drill.py`](../code/src64_drill.py) · [`src64_emit_report_block.py`](../code/src64_emit_report_block.py)
**Logs:** [`src64-au2d17.json`](../data/gate-logs/src64-au2d17.json) · [`src64-drill.json`](../data/gate-logs/src64-drill.json)

**Result: the mathematics verifies, and the round's own headline is weaker than it reads. `2^{−H_i} = 3^{h−i}/2^{Q−P_i}`, so Theorem 5.1 multiplied by `2^Q` is `Σ_i 3^{h−i}2^{P_i} = 3B_w` — term by term the definition of `B_w`. The Exact Endpoint-Laplace Identity is therefore true by construction, and what has to be checked is the affine relation `2^Q Z = 3^h X + B_w` on real orbit data. That holds on all 874 bridges, along with every other claim in the round: the correction floor, the phase gap, the exact form of Theorem 8.3, the double-canonical congruences, the weighted-area components, and the first-hit slice. Three things this recheck adds that the bundle's checker does not. Jensen is verified on real bridges as an integer inequality, `2^A·S^h ≥ h^h·3^{h(h+1)/2}`, because `h(h+1)/2` is an integer; the shipped checker tests Jensen only on synthetic random slack lists. The double-canonical congruences are checked on all 874 bridges rather than on the 90 that pass the smallness guard, so a congruence failing on a large bridge could not hide. And the shipped checker's three assertion sites all sit behind an `if`, while its counters increment once per sample — measured independently at its own parameters, its source-residue assertion runs on 10.0% of samples, its endpoint assertion on 7.6%, its Jensen assertion on 33.8%, and its quantile bound is non-trivial on 5.0%. Every count the bundle reports about the bridge population — 874, 3,038, 90 — is reproduced exactly from the definition.**

---

## The identity that is a definition, and the line beneath it that is not

Section 5 is the round. It defines the suffix excess

> `H_i := Σ_{k=i+1}^h q_k − β(h−i)`,  `E := H_0 = Q − βh`

and states the Exact Endpoint-Laplace Identity

> `Σ_{i=0}^{h−1} 2^{−H_i} = 3(Z − 2^{−E}X)`.

The paper says, correctly, that this is rational rather than floating: `2^{−H_i} = 3^{h−i}/2^{Q−P_i}` and `2^{−E} = 3^h/2^Q`. Multiply both sides by `2^Q` and it becomes

> `Σ_{i=0}^{h−1} 3^{h−i}·2^{P_i} = 3·(2^Q Z − 3^h X)`.

The left side is `3·Σ_i 3^{h−1−i}2^{P_i}`, which is `3B_w` **by the definition of `B_w` in section 3**. So the identity reduces to `B_w = 2^Q Z − 3^h X`, which is the affine relation of section 3 rearranged. Theorem 5.1 restates a definition.

That is not a criticism of the result — the rearrangement is what makes the round's later sections possible, and the paper's own derivation goes through `c(w) = 2^E Z − X`. It is a statement about **what a checker can learn from it**. Verifying `Σ2^{−H_i} = 3(Z−2^{−E}X)` in exact rationals, as the shipped checker does, verifies the exponent bookkeeping and nothing else. The falsifiable content sits one line below: whether real orbit data satisfies

> `2^Q Z = 3^h X + B_w`.

Both are checked here — the rational form as its own route through `Fraction`, the affine relation in integers — and both are clean on all 874 bridges. When the drill replaced `t["affine_identity_violations"] += 1` with `pass`, the gate did not notice, because the counter was already zero; the defect had to be re-aimed at the arithmetic instead. A check whose counter reads zero cannot be tested by deleting it.

## What `2^{βm} = 3^m` buys, three times over

RUN-044 turned the correction bank into an integer identity by the same substitution. This round it pays three separate times, and each time it replaces a float64 test in the bundle with an exact one.

**Theorem 8.3.** The paper writes `E ≥ log₂(1 + (5−(2/3)^h)/Z)`. Since `2^E = 2^Q/3^h`, that is the rational inequality

> `2^Q/3^h ≥ 1 + (5 − (2/3)^h)/Z`

with no logarithm at all. The shipped checker evaluates both sides in float64 and asserts `E + 1e-12 >= floor`. On this population the fudge never changed a verdict — but the exact form does not need to be trusted, and its tightest slack is `0.025081`, so nothing here is near the edge.

**Theorem 6.1.** `Σ_i H_i = A − β·h(h+1)/2` where `A = Σ_k k q_k`, and `h(h+1)/2` is an **integer**, so `2^{Σ H_i} = 2^A/3^{h(h+1)/2}` exactly. Jensen's `(1/h)ΣH_i ≥ log₂(h/S)` therefore becomes

> `2^A · S^h ≥ h^h · 3^{h(h+1)/2}`,

integers on the left up to the rational `S`. The bundle checks Jensen only on 10,000 synthetic random `H` lists, never on a bridge. Here it is checked on every bridge, and holds on every one.

**Section 10.** `2^{δ_v−δ_s} = 3^{v−s}/2^{K_v−K_s}`, so the first-hit threshold, its minimality, and the overshoot bound are all comparisons of integers once both sides are raised to the denominator of `λ`.

## Three things this recheck adds

**Jensen on real bridges, not on synthetic slack.** Above.

**The congruence separated from the collapse.** Theorem 4.1 has two halves. The congruences `X ≡ r₂(w) mod 2^{Q+1}` and `Z ≡ r₃(w) mod 3^h` hold for *every* positive word; the collapse `r₂(w) = X`, `r₃(w) = Z` additionally needs `X < 2^{Q+1}` and `Z < 3^h`. The shipped checker guards both with a single `if X < 2**(Q+1) and Z < 3**h`, so a congruence that failed on a large bridge would never be seen. Here the congruence is verified on all 874 and the collapse on the 90 that qualify — 10.3% — with the two smallness conditions counted separately (97 sources inside their modulus, 90 endpoints). The paper's "for all sufficiently large critical bridges" is honest: at this scale nine bridges in ten are not large enough, and that denominator belongs beside the 90.

**The bundle's own guard rates.** All three of the shipped checker's assertion sites sit behind an `if`, and all three counters increment once per *sample*. Reimplementing its sampling scheme independently at its stated parameters — `n` odd below 2×10⁶ with `n % 3 ≠ 0`, one to nine accelerated steps; `h` in [10,1000], `Z` in [1,500] — gives the rates in the measured block. The two residue assertions fire on 10.0% and 7.6% of samples because `n < 2^{Q+1}` and `cur < 3^h` are rarely true for a short prefix of a large start. The Jensen assertion fires on 33.8% because its guard is `if h > 3*Z` and `3Z` averages above `h`. The quantile bound is non-trivial on 5.0% because `3Z·2^A ≥ h` otherwise. Wherever a guard does open, the assertion passes — I found zero violations — so this is a measurement of what `random_exact_residue_checks: 7990` and `quantile_jensen_tests: 10000` mean, not a defect.

## Finding 1 — Theorem 6.2 is vacuous on every finite bridge, and a sharper version is not

`#{i : H_i < A} < 3Z·2^A` is non-trivial only when `3Z·2^A < h`. Endpoints on a real bridge satisfy `Z ≡ 7 or 11 mod 12`, so `Z ≥ 7` and `3Z ≥ 21`, while the longest tail found at limit 25,000 is 35. Across 10,488 instances — 874 bridges × twelve integer values of `A` — **not one was non-vacuous**. The theorem is asymptotically sharp and finitely empty, which the paper does not claim otherwise, but a checker reporting "0 violations" over that population is reporting `0 < 21·2` ten thousand times.

The proof, though, gives more than the statement. Every index with `H_i < A` contributes more than `2^{−A}` to `S = Σ_i 2^{−H_i}`, so the honest bound is `#{H_i < A} < S·2^A`, and `S < 3Z` is a further relaxation. Substituting `S` for `3Z` gives **136 non-vacuous instances**, all clean. That is the version worth checking at finite scale, and it costs nothing: `S` is already computed for Theorem 5.1.

## Finding 2 — Theorem 7.2's finite content is attained on 520 of 874 bridges, and Theorem 7.1 is an identity

Theorem 7.1 states `Σ_i H_i = Σ_k k(q_k − β)`. Both sides reduce to `A − β·h(h+1)/2`, so a numerical comparison of them compares a quantity with itself. The shipped checker does exactly that, in float64, with `assert abs(area - weighted) < 1e-10`. What can actually be wrong is the combinatorial rearrangement `Σ_{i<h}(Q − P_i) = Σ_k k q_k` and the triangular sum, and both are integer statements; both are checked here and both are clean.

Theorem 7.2's asymptotic form carries an `o(1)`, which no finite population can refute. Its finite content is that the `q−1` surplus is not centred *before* the midpoint:

> `2(A − M) ≥ (h+1)(Q − h)`,  `M = h(h+1)/2`

— integers, no `β`. It holds on all 874, and it is **exactly attained on 520 of them**: every single-step bridge has one position, `k = 1`, and `(h+1)/2 = 1`. Writing that test with a strict `>` accuses 520 correct bridges, which is what the first version of this gate did. An attained bound is where a check has to be right, and it is also where a check is easiest to get wrong in the accusing direction.

## Finding 3 — the integer-lift escape is empty at finite scale

Section 9 defines `m_h := Q − ⌈βh⌉ ≥ 0` and Theorem 9.1 concludes that a family with polynomially tiny one-sided phase and subpolynomial endpoint must eventually pay `m_h ≥ 1`. Computing `⌈βh⌉` as `(3^h).bit_length()` — exact, no logarithm, since `βh` is never an integer — gives `m_h = 0` on **all 874 bridges**. Every finite bridge in this population sits at the first critical integer, so its excess `E` *is* the one-sided phase `ε_β⁺(h)`, with nothing added.

That is consistent with the theorem, which is asymptotic and conditional, and it makes its dichotomy sharper than it looks: at finite scale the second branch is not merely rare but unobserved, and Theorem 8.3 then reads directly as a lower bound on the endpoint, `Z ≥ (5 − (2/3)^h)/(2^{ε⁺}−1)`.

## Finding 4 — the phase gap floor is not approached

Lemma 8.1 proves `X − Z ≥ 4` by enumerating the combined residue classes mod 36, and the enumeration is right: no `Z ≡ 7, 11 mod 12` has `Z + 2 ≡ 11, 17 mod 18`, while `Z + 4` does for `Z ≡ 7` and `Z ≡ 31 mod 36`. So 4 is admissible. Across 874 local bridges the **smallest gap observed is 16**, and across 4,069 genuine consecutive-record gaps it is also 16. The bound is correct and, unlike the midpoint bound above, nowhere near tight.

## Finding 5 — the bundle keeps improving, and this round is the strongest validation record yet

Three rounds of watching this file: RUN-042 found per-file digests present, RUN-043 found them replaced by a single `checker_stdout_sha256`, RUN-044 found neither. `SOURCE_VALIDATION_AU2d17.json` now carries **seven per-file digests, all matching**, seven per-file byte sizes, all matching, an `all_ok` flag, an empty `issues` list, and both a compile and an execution return code. Its nine `checker_counts` agree with the checker report exactly. `CHECKSUMS.sha256` pins ten of the eleven files, the only omission being itself.

Two smaller notes. Four files are absent from the validation record — `CHECKER_STDOUT_AU2d17.txt`, `CHECKSUMS.sha256`, the record itself, and the verification script, the last appearing only as a `checker_compile` return code. And `CHECKER_STDOUT_AU2d17.txt` is the checker report plus a single trailing newline: RUN-044's equivalent was byte-identical to the report, so this is the same file under a second name, one byte longer. The shipped script's final line writes to a hardcoded `/mnt/data/collatz_hardzeta_work/AU2d17_bundle/` path, so the `checker_execution.returncode: 0` in the validation record can only have been produced on the authoring machine.

## The constants, with budgets sized to their own formulas

Ten constants. Four are the nearest double; five are what the same formula gives in float64; none disagrees with both. The interesting one is `source_entropy_rate_gap_bits_per_h = 0.07931861277485575`, which sits **26 ulps** from the nearest double to `β − 𝔢_β`. A flat four-ulp cap calls that wrong. It is not: `β ≈ 1.585` minus `𝔢_β ≈ 1.506` gives `0.0793`, a magnification of about twenty, and the parent `𝔢_β` is itself two ulps out. Twenty times two is forty, and 26 is inside it. Each constant now carries a budget of `4 × (largest operand / result)`, and — the RUN-041 lesson — the budget is tested **before** the chain excuse, not after it, because in an `elif` chain the order is the bound.

The same applies to the checker report's per-example fields. `E = Q − βh` cancels, and its published values run to 38 ulps at `h = 5`, where `E = 0.0752` against operands near 8. `phase_floor = log₂(1 + x)` with `x ≈ 0.02` loses about `log₂(1/x)` bits the same way, and reaches 45. Every one of the twenty is the float64 chain within its own budget.

## What this round does not do

It does not prove CASP or Collatz, and says so in a box. The remaining gap is stated exactly: no theorem forces the near-critical suffix-supercritical language to place both canonical representatives outside a tiny initial interval, and NO-GO 11.1 explicitly forbids inferring one from the entropy arithmetic. That arithmetic is verified here as a convergence — `log₂C(Q−1,h−1)/h` at `Q = ⌈βh⌉` approaching `𝔢_β = 1.5056…` from below over four levels, with the gap shrinking each time and the rate never exceeding `β` — and it remains, as the paper insists, a diagnostic.

<!-- BEGIN GENERATED measured block: python code/src64_emit_report_block.py -->

**The affine relation, in integers.** Section 5's Endpoint-Laplace identity multiplied by `2^Q` is term-by-term the definition of `B_w`, so the identity carries no information on its own; the content is `2^Q Z = 3^h X + B_w` on real orbit data. Across **874** bridges from **821** distinct sources (longest tail 35): **0** affine violations, **0** disagreements with the closed form for `B_w`, **0** violations of the published rational form, **0** non-positive Laplace sums. Every suffix supercritical on **3038** suffixes: **0**. Lemma 8.2's correction floor **0**. Theorem 8.3, as the rational inequality `2^Q/3^h >= 1 + (5-(2/3)^h)/Z` rather than the bundle's float64 form with its `1e-12` fudge: **0** violations, tightest slack **0.025081**, and the fudge changed the verdict on **0** of them.

**The phases, and the integer lift.** Source outside `11, 17 mod 18` **0**; endpoint outside `7, 11 mod 12` **0**; endpoint not below the source **0**; Lemma 8.1's `X-Z >= 4` **0**, with the smallest gap actually seen **16** — the residue argument admits 4 and nothing near it occurs. The integer lift `m_h = Q - ceil(beta h)` was negative **0** times and **zero on 874 of 874** bridges, so every finite bridge sits at the first critical integer and its excess IS the one-sided phase; the phase left the unit interval **0** times.

**Double-canonical collapse, with the guard counted.** The congruences hold for every word; the collapse to equality needs the smallness, and the shipped checker tests both behind one `if`. Here the congruence is checked on all **874** bridges — **0** source and **0** endpoint violations — while the source lies inside its modulus on **97**, the endpoint on **90**, and both on **90** (10.3%). Theorem 4.1's equality on those: **0** violations, **0** representatives failing their own defining congruence, and **0** cases where the collapse would have been claimed outside the moduli.

**Jensen on real bridges, as an integer inequality.** `2^{sum H_i} = 2^A / 3^{h(h+1)/2}` because the triangular number is an integer, so Theorem 6.1 is `2^A S^h >= h^h 3^{h(h+1)/2}`. On **874** bridges: **0** violations. Corollary 5.2's `S < 3Z` **0**, and the elementary `S < h` **0**. The published weaker form `avg H > log2(h/3Z)` has a **positive right side on 0 of 874** bridges — below that it states nothing — while the exact form is live on every one. Theorem 6.2 was exercised on **10488** instances with **0** violations, of which **0** were non-vacuous; replacing the `3Z` by the `S` it bounds gives **136** non-vacuous instances, **0** violations.

**The weighted area is an identity; its components are not.** Both sides of Theorem 7.1 reduce to `A - beta h(h+1)/2`, so the bundle's float64 comparison with a `1e-10` tolerance compares a quantity with itself. The two pieces that can be wrong are integer statements: the rearrangement `sum_i (Q - P_i) = sum_k k q_k` **0** violations and the triangular sum **0**, with the surplus total **0**. Theorem 7.2's finite content is `2(A - M) >= (h+1)(Q - h)`: **0** bridges below the midpoint, **520 exactly at it** — attained on every single-step bridge, where `k` can only be 1 — and **354** past it, the largest excess 7.184 positions.

**The first-hit slice needs no `O(1)`.** `2^{delta_v - delta_s} = 3^{v-s}/2^{K_v-K_s}`, so every inequality in section 10 is a comparison of integers. Over **1321** orbits, **607** reached the threshold: **0** below it, **0** not minimal, **0** overshooting more than one step's slack gain, **0** violating the length bound, **0** slack-step ratio disagreements, **0** prefix valuations below the length and **0** disagreeing with the cumulative sum. The published `ell >= lambda/(beta-1) log2 N + O(1)` needs no additive constant: it reduces to `K_v - K_s >= v - s`, and the bound is **attained on 309** of the 607. Theorem 10.1's containment is asymptotic and at these scales holds for a minority — source inside its cylinder **165**, outside **442**; endpoint inside **142**, outside **465** — the largest N still outside being 3995.

**Their own counters increment once per sample, not once per assertion.** All three of the shipped checker's assertion sites sit behind an `if`. Reimplementing its sampling scheme independently at its stated parameters: of **26654** residue samples the source formula is actually tested on **2661** (10.0%) and the endpoint formula on **2037** (7.6%), with **0** and **0** violations where they do fire. Of **10000** quantile samples the Jensen assertion runs on **3383** (33.8%) — its `if h > 3Z` guard — and the Markov bound is non-trivial on **500** (5.0%); **0** and **0** violations.

**The record-gap population, where the phase hypotheses apply.** The bundle's bridges are local cylinder witnesses, not orbit records — one source can contribute several, and its own example list does. On **4069** genuine consecutive suffix-minimum gaps from **44** sources: affine **0**, Laplace **0**, `X-Z>=4` **0**, endpoint phase **0**, `Z = 3 mod 4` **0** (the condition that needs the record structure rather than the word), and **0** violations across **11305** suffixes. Smallest gap seen 16.

**All ten published finite examples, rebuilt from the map.** **0** disagreeing values of `X`, **0** of `Z`, **0** exponent words, **0** lengths, **0** first steps not of valuation one, **0** Laplace sums, **0** excess decimals, **0** phase floors, **0** tails not suffix-supercritical, **0** geometry violations. **1** source appears more than once — `y = 155` reaches both `Z = 175` and `Z = 167`, and at most one of those can be its next record.

| `y` | `X` | `Z` | `h` | word | `sum 2^-H_i` | `X - Z` |
| --- | --- | --- | --- | --- | --- | --- |
| 59 | 89 | 67 | 1 | `[2]` | `3/4` | 22 |
| 71 | 107 | 91 | 3 | `[1, 2, 2]` | `69/32` | 16 |
| 91 | 137 | 103 | 1 | `[2]` | `3/4` | 34 |
| 155 | 233 | 175 | 1 | `[2]` | `3/4` | 58 |
| 155 | 233 | 167 | 6 | `[2, 1, 1, 1, 2, 3]` | `3453/1024` | 66 |
| 187 | 281 | 211 | 1 | `[2]` | `3/4` | 70 |
| 223 | 335 | 319 | 5 | `[1, 1, 1, 3, 2]` | `777/256` | 16 |
| 251 | 377 | 283 | 1 | `[2]` | `3/4` | 94 |
| 283 | 425 | 319 | 1 | `[2]` | `3/4` | 106 |
| 347 | 521 | 391 | 1 | `[2]` | `3/4` | 130 |

**NO-GO 11.1's entropy rate, watched converging.** `log2 C(Q-1,h-1)/h -> e_beta` at `Q = ceil(beta h)`, over **4** levels: **0** where the gap to `e_beta` failed to shrink, **0** where the rate exceeded `beta`, which would be impossible.

| `h` | `Q = ceil(beta h)` | rate | gap to `e_beta` |
| --- | --- | --- | --- |
| 50 | 80 | 1.444631 | 0.0610 |
| 200 | 317 | 1.480225 | 0.0254 |
| 800 | 1268 | 1.498080 | 0.0076 |
| 3200 | 5072 | 1.503481 | 0.0022 |

**Constants.** 10 checked: **0** disagree with both readings of their own formula, 4 are the nearest double, 6 are what the same formula gives in float64, 0 brackets could not decide. Each budget is `4 x (largest operand / result)` — the factor by which the formula magnifies one ulp of its inputs — and the budget is tested BEFORE the chain excuse.

| constant | published | nearest double | budget | verdict |
| --- | --- | --- | --- | --- |
| `beta` | 1.584962500721156 | 1.584962500721156 | 4 | exact |
| `beta_minus_one` | 0.5849625007211561 | 0.5849625007211562 | 12 | -1 ulp, the float64 chain |
| `critical_gap_exponent` | 0.2 | 0.2 | 4 | exact |
| `inverse_beta_minus_one` | 1.7095112913514552 | 1.7095112913514547 | 12 | +2 ulp, the float64 chain |
| `first_hit_single_cylinder_exponent_limit` | 0.341902258270291 | 0.34190225827029097 | 12 | +1 ulp, the float64 chain |
| `first_hit_joint_cylinder_exponent_limit` | 0.683804516540582 | 0.6838045165405819 | 12 | +1 ulp, the float64 chain |
| `raw_nearcritical_composition_entropy_bits_per_h` | 1.5056438879463003 | 1.5056438879463008 | 12 | -2 ulp, the float64 chain |
| `source_modulus_bits_per_h` | 1.584962500721156 | 1.584962500721156 | 4 | exact |
| `source_entropy_rate_gap_bits_per_h` | 0.07931861277485575 | 0.07931861277485538 | 80 | +26 ulp, the float64 chain |
| `double_cylinder_modulus_bits_per_h` | 3.169925001442312 | 3.169925001442312 | 4 | exact |

**Artifacts.** 11 files, 10 carrying a `CHECKSUMS` digest, **0** mismatches, **0** manifest lines naming a missing file; the only file with no digest anywhere is `CHECKSUMS.sha256`. No two files carry the same bytes — `CHECKER_STDOUT_AU2d17.txt` is the checker report plus a single trailing newline, where RUN-044's was byte-identical to it. The source-validation record names **7** files and digests **7** of them (**0** digest mismatches, **0** size mismatches), reports `all_ok = True` with **0** issues, a compile return code of 0 and an execution return code of 0, and its nine counter values disagree with the checker report **0** times. 4 files are absent from it: `CHECKER_STDOUT_AU2d17.txt`, `CHECKSUMS.sha256`, `SOURCE_VALIDATION_AU2d17.json`, `verify_Hard_Zeta_AU2d17_small_endpoint_cylinder.py`.

**Ledger coverage.** The paper lists 14 proved items, 5 open problems and 7 NO-GO headings; the ledger carries 14, 5 and 7, with an `open` key (True). Open items with no trace: none. NO-GO headings with no trace: none. The heuristic deciding those lists has controls at both ends and failed neither (0, 0).

**Their counters beside mine**, keyed on their names rather than mine: 0 of 9 had no counterpart here, 0 are reported as zero, and **8 are reproduced exactly** from the definition. The ninth is not a disagreement: `random_exact_residue_checks` is a sample size, and mine is larger.

| check | theirs | mine |
| --- | --- | --- |
| `finite_local_bridges` | 874 | 874 |
| `laplace_identities_exact` | 874 | 874 |
| `canonical_rep_collapses_finite` | 90 | 90 |
| `phase_gap_checks` | 874 | 874 |
| `correction_floor_checks` | 874 | 874 |
| `suffix_supercritical_suffixes` | 3038 | 3038 |
| `weighted_area_identities` | 874 | 874 |
| `random_exact_residue_checks` | 7990 | 26654 |
| `quantile_jensen_tests` | 10000 | 10000 |

**Instrument and drill.** 14 instrument self-checks, 0 failed. The mutation drill planted **50** defects: **50** caught by the check they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed.

<!-- END GENERATED measured block -->

## Instrument

Fourteen self-checks, each naming a world in which it fails.

The `β` bracket comes from two certified logarithms and is tested for width, not only for containment — a bracket that had collapsed would pass a containment test and decide nothing. `log2_int`, which strips a binomial coefficient's exponent with one bit shift, is tested to return the exponent exactly on powers of two **and** strictly more just above one; either test alone would pass for a function that returned the bit length and stopped. `h2_bracket` is tested at `h₂(1/2) = 1`, the one value of binary entropy in closed form, for symmetry about `1/2`, and for the monotonicity on `(1/2,1)` that `entropy_bracket` relies on to swap its ends — that last one is what caught the drill's defect against the entropy formula. `⌊βh⌋` as `(3^h).bit_length() − 1` is checked against the float route over 400 levels. And Lemma 8.1's enumeration is done in both directions: `X − Z = 2` impossible mod 36, `X − Z = 4` possible, because a test that only ruled things out would pass on an empty class list.

One check was removed before shipping. The first version of the canonical-representative section asserted `0 ≤ r < m` after computing `r = ... % m`, which the operator guarantees; it named no failing world. What can be wrong is the modular inverse, so the test is now that each representative satisfies the congruence that defines it. The same pass removed a `q < 1` test in the first-hit section — no accelerated valuation is below one — and replaced it with the slack-step ratio `2^{δ_{n+1}}/2^{δ_n} = 3/2^{q}`, which a wrong index into the cumulative array does break.

## Drill

Fifty defects, one at a time, each planted at a pre-flighted unique anchor, with the gate restored byte for byte after every run. **50 caught, 0 missed, 0 malformed, both controls undisturbed, the gate byte-identical at the end.**

Nine defects had to be re-aimed after the first pass, and the reasons are the interesting part.

Four "changed nothing" because they attacked a counter that already read zero, or removed a check that was already passing: replacing an increment with `pass`, disabling a digest comparison, relaxing `> 0` to `>= 0` on a sum that is never zero. From a green baseline, deleting a check is invisible; the mutation has to make the counter *rise*, not stop rising.

Two loosened what they attacked — comparing `2^{Q−P_i}` against `3^{h−i−1}` instead of `3^{h−i}` weakens the supercriticality test rather than breaking it, and a weakened test finds nothing where a correct one found nothing. Tightening is the direction that discriminates.

One was **still true after the mutation**: shrinking the source modulus from `2^{Q+1}` to `2^{Q−1}` leaves the congruence valid, because a congruence modulo `m` implies the congruence modulo every divisor of `m`. Scoring that as a missed defect would have been a false hole in the gate. Multiplying the modulus by 5 instead — coprime to 3, so the inverse still exists — breaks it properly. This is the same family as RUN-044's `2^{−q} ≡ 2^q mod 3`: a mutation can be a no-op for a reason that lives in the mathematics rather than in the check.

One was too weak by forty digits: swapping the two ends of a bracket that wide moves nothing a double can see. And one was caught by the right guard under a different name — breaking the binary-entropy formula fired the instrument's own monotonicity self-test before it reached any constant, which is the instrument doing its job, so the expectation was renamed rather than the defect re-aimed.
