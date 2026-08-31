# RUN-046 — Hard-Zeta A-U.2d.18: the round that makes the slack profile an integer, and the branch that has no finite instance

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d18_Double_Canonical_Critical_Cylinder_Spectral_Rigidity_bundle_v0.1.zip` (source item 65) — 24 sections. Ships a checker report, a constants frontier, a theorem ledger, a route map, literature notes, a `CHECKSUMS.sha256`, a source-validation record and a verification script. Nine files: the bundle README and `CHECKER_STDOUT` of the previous round are gone.
**Tools:** [`src65_lift_cocycle.py`](../code/src65_lift_cocycle.py) · [`src65_drill.py`](../code/src65_drill.py) · [`src65_emit_report_block.py`](../code/src65_emit_report_block.py)
**Logs:** [`src65-au2d18.json`](../data/gate-logs/src65-au2d18.json) · [`src65-drill.json`](../data/gate-logs/src65-drill.json)

**Result: the mathematics verifies, on the bundle's own population, and all twelve of its counters are reproduced exactly from the definition — 1228 bridges, 4337 recurrence steps, 125 collapse cases, six countermodels, and the two synthetic blocks. The round's move is to replace A-U.2d.17's real-valued slack with an integer one: `m_ℓ = Q_ℓ − ⌈βℓ⌉` with `H_{h−ℓ} = m_ℓ + ε_ℓ`. Since `⌈βℓ⌉ = (3^ℓ).bit_length()` and `2^{ε_ℓ} = 2^{⌈βℓ⌉}/3^ℓ`, every statement in sections 7 through 14 is exact rational arithmetic with no logarithm anywhere — including Theorem 11.1's `𝒫↓ < 2`, which the bundle floats, and Theorem 12.2's mechanical cocycle, which is the round's real contribution. Three findings. Every one of the 1228 bridges has zero total lift, so the positive-lift branch of Theorem 15.1 and the whole of Theorem 10.1's rarity bound have no finite instance at this scale — while the interior profile is far from flat, reaching a lift of 8. Two of the bundle's twelve counters test a quantity against itself: `near_linear_gap_algebra` asserts that `N/(R+1)` is positive for `N ≥ 10⁶`, and `positive_lift_drop_algebra` asserts an inequality in which `β` cancels exactly, leaving `m + ε ≥ 1` for an integer `m ≥ 1`. Twenty thousand assertion executions, no information. And the source-validation record has changed content for the fifth consecutive round — 7 per-file digests last round, 3 this one, with the execution return code and the counter cross-check gone.**

---

## The coordinate: a real profile becomes an integer one

A-U.2d.17 gave the suffix slack `H_i = Σ_{k>i} q_k − β(h−i) > 0`. This round reads the same object from the other end. For suffix length `ℓ`, with `Q_ℓ` the suffix valuation sum,

> `ε_ℓ := ⌈βℓ⌉ − βℓ ∈ (0,1)`,  `m_ℓ := Q_ℓ − ⌈βℓ⌉`,  `H_{h−ℓ} = m_ℓ + ε_ℓ`

and full suffix-supercriticality is exactly `m_ℓ ≥ 0`. That is worth more than a change of notation, because `m_ℓ` is an **integer** and `ε_ℓ` is a mechanical function of `ℓ` alone — nothing about the orbit enters it.

Three consequences make the round checkable end to end:

- `⌈βℓ⌉ = (3^ℓ).bit_length()`, since `βℓ` is never an integer;
- `2^{ε_ℓ} = 2^{⌈βℓ⌉}/3^ℓ`, an exact rational;
- `a_ℓ := ⌈βℓ⌉ − ⌈β(ℓ−1)⌉ ∈ {1,2}`, and `β > 3/2` forbids two consecutive ones.

So Theorem 8.1's recurrence `m_{ℓ+1} − m_ℓ = q_{h−ℓ} − a_{ℓ+1}` is integer arithmetic, Theorem 12.2's cocycle `U_{ℓ+1} = (2^{a_{ℓ+1}}U_ℓ − 2^{−m_{ℓ+1}})/3` is exact rational arithmetic, and Theorem 11.1's `𝒫↓ < 2` — which the shipped checker evaluates by floating an exact Fraction and comparing to `2.0` — is `(Z/X)·2^{⌈βh⌉}/3^h < 2`, decided in integers.

## Is their float64 ceiling safe? Measured, not assumed

The shipped checker computes `ceil(BETA*l)` with `BETA = log2(3)` in float64, at lengths up to 4096. That is a genuine risk: `βℓ` never lands on an integer, but a float64 product can, and the ceiling would come out one too low — silently, in a quantity every later statement depends on.

It is safe here, and this recheck says so with numbers rather than with confidence. The exact ceiling was compared against the float64 one over 20,000 levels; the closest `βℓ` comes to an integer in that range is `2.62 × 10⁻⁵`, at `ℓ = 15601` — the denominator of a convergent of `log₂3` — against a float64 error near `7 × 10⁻¹²`. The margin is about **3.7 million to one**.

The comparison itself is done twice by different routes. A certified `β` bracket scaled to 200 bits decides `⌊βℓ⌋` by integer division whenever its two ends agree, which they do at every level; and the exact `(3^ℓ).bit_length()` route is run at six levels including the minimiser, so the fast route is anchored to the certified one rather than trusted. Building `3^ℓ` at every level up to 20,000 costs half a minute in `Fraction` gcds; the fixed-point route costs two seconds and gives the same answer.

## Finding 1 — every bridge has zero total lift, so one branch of the dichotomy is empty

Theorem 15.1 splits closed near-linear bridges into a zero-lift class with `m_h = 0` and a positive-lift class with `m_h ≥ 1`, and Theorem 10.1 bounds the second at `o(log N)` occurrences by charging each one at least `r + 1 − β` of the inherited record-slack descent budget.

On the bundle's own population of **1228 bridges**, `m_h = 0` on **every single one**. The positive-lift branch has no finite instance, so Theorem 10.1's rarity bound — correct as stated — bounds an empty set here, and the bundle's `zero_lift_constant_product: 1228` and `zero_lift_harmonic_bound: 1228` are the full population rather than a subclass of it.

RUN-045 found the same on A-U.2d.17's smaller population of 874. This is the same fact on a 40% larger one, under the bundle's own wider definition, which makes it a property of the object rather than of a cutoff.

It is not that the lift profile is trivial. The largest **interior** lift reached is **8**, and there are 1044 descents across the population, every one of them by exactly one unit and every one at a mechanical `a = 2` position, as Theorem 8.1 requires. The excursion structure the round is about is fully present; only its endpoint value is pinned.

That sharpens rather than weakens the round: on everything reachable, `E = ε_h` exactly, `𝒫↓ < 2` applies to all of it, and Corollary 11.2's constant reciprocal-mass bound is a statement about every bridge rather than about a distinguished class.

## Finding 2 — two of their twelve counters test a quantity against itself

The shipped checker's twelve counters include two blocks of 10,000 iterations each. Neither can fail.

**`near_linear_gap_algebra`.** The block draws `N ∈ [10⁶, 10¹²)` and `η ∈ [0, 0.2)`, sets `R = max(1, ⌊N^η⌋)` and `lower = N/(R+1)`, and asserts

```python
assert lower > 0
```

with a comment explaining that the exponent tends to `≥ 1 − η`. The exponent statement is never evaluated. `N ≥ 10⁶` and `R ≥ 1` make `lower ≥ 500000`, and across 10,000 samples at the same ranges the smallest left side is **134,322**. The block is 10,000 executions of `500000 > 0`.

**`positive_lift_drop_algebra`.** The block draws integer `m ∈ [1,20]` and `ε ∈ [0,1)`, sets `E = m + ε` and `drop = E − (β−1)`, and asserts

```python
assert drop >= 2 - BETA - 1e-15
```

Subtract the two sides: `(m + ε − β + 1) − (2 − β) = m + ε − 1`. **`β` cancels exactly.** What is being tested is `m + ε ≥ 1 − 10⁻¹⁵` for an integer `m ≥ 1` and `ε ≥ 0`.

This recheck demonstrates the cancellation rather than restating it: the same expression is evaluated with `β` at both ends of a certified bracket, and the two results are identical on all 10,000 samples — which is operationally what "`β` does not participate" means. The tightest margin is exactly **0.0**, attained at `m = 1, ε = 0`, confirming the bound is `m + ε ≥ 1` and nothing more.

Neither block is wrong, and neither claims more than it does in the scope warning. But `near_linear_gap_algebra: 10000` and `positive_lift_drop_algebra: 10000` are 20,000 of the report's 24,000-odd assertion executions, and they carry no information about `β`, about the bridge, or about the round.

## Finding 3 — the validation record has changed content for the fifth round running

Tracked across five rounds: RUN-042 found per-file digests present; RUN-043 found them replaced by a single `checker_stdout_sha256`; RUN-044 found neither; RUN-045 found seven per-file digests, seven sizes, an `all_ok` flag, an issues list, and both a compile and an execution return code, with the checker counts cross-checked against the report.

`SOURCE_VALIDATION_AU2d18.json` carries **three** per-file digests — the three Markdown documents — all matching, with byte counts, per-file `ok` flags and an `all_ok`. The three JSONs appear only as `json_parse` booleans. Gone since last round: the execution return code, the `checker_counts` cross-check, and four of the seven digests. `CHECKSUMS.sha256` still pins eight of the nine files, the omission being itself, so nothing is unverifiable — the manifest carries what the record dropped.

Three files are absent from the validation record entirely: `CHECKSUMS.sha256`, the record itself, and `verify_Hard_Zeta_AU2d18_double_canonical_spectral.py`, the last appearing only as a `python_compile: true`. As at RUN-045, the shipped script's final line writes to a hardcoded `/mnt/data/collatz_hardzeta_work/AU2d18_bundle/` path, so it cannot be run as shipped anywhere else.

## What is checked here that the bundle does not check

**The two halves of Theorem 6.1 separately.** `Z < X < (3Z+1)/2` has an upper half that follows from `y < Z` and a lower half from the record ordering. The shipped checker writes both into one `assert y<Z<X and X < (3*Z+1)/2`; a single counter cannot say which failed.

**`m_ℓ ≥ 0` against the supercriticality it is equivalent to.** The equivalence `Q_ℓ > βℓ ⟺ Q_ℓ ≥ ⌈βℓ⌉ ⟺ 2^{Q_ℓ} > 3^ℓ` is two lines of argument, and it is the join between the round's integer coordinate and the inherited real one. Both routes are computed and compared on all 4,337 positions.

**The Laplace sandwich.** `ε_ℓ ∈ (0,1)` forces the integer sum `Σ2^{−m_ℓ}` to sit strictly between the real one `Σ2^{−m_ℓ−ε_ℓ}` and twice it. That two-sided bracket is the only place a reindexing error could hide while leaving both individual sums looking plausible, and it is checked on every bridge.

**Theorem 14.1's countermodel, component by component.** The construction is rebuilt from the paper's three steps rather than accepted, and the paper's own proof splits its Laplace mass three ways — rise `< 1`, plateau `O(h·2^{−M}) < 1/h`, descent `< 4` because no height is held more than twice. Checking only the total would let two of the three be wrong in compensating directions, so all four are separate counters. All four hold at every length from 128 to 4096.

**Theorem 13.1 reduced.** The residue constraint reads `a_{ℓ+1} + m_{ℓ+1} − m_ℓ ≡ π(V_ℓ) mod 2`, and by Theorem 8.1 the left side is exactly `q_{h−ℓ}`. So the statement is that the valuation's parity is forced by the reverse state's class mod 3 — which is `2 ≡ −1 mod 3` and one line. Both forms are checked, and their agreement is its own counter, so a broken `mech_a` or a broken profile shows up here independently of the recurrence check.

## The vacuity that carried over

Theorem 9.1's quantile corollary `#{ℓ : m_ℓ < A} < 6Z·2^A` is non-trivial only when `6Z·2^A < h`. With `Z ≡ 7 or 11 mod 12` forcing `Z ≥ 7`, and the longest tail at this limit being 42, **not one of the 14,736 instances is non-vacuous** — the same shape RUN-045 found for the `3Z` version, one factor of two worse. Substituting the sum the bound actually relaxes gives **65** non-vacuous instances, all clean. The ceiling is loose by a factor of about 182 at its tightest.

The same holds for the budget itself: `Σ2^{−m_ℓ} < 6Z` is correct on all 1228, with the largest ratio to its ceiling being `0.0055`.

## What this round does not do

It does not prove CASP or Collatz, and the boxed statement says so. The round's own contribution to the frontier is a **negative** one: NO-GO 6.2 retracts the double-cylinder scarcity product that A-U.2d.17's Corollary 4.2 might have invited, on the grounds that `Z < X < (3Z+1)/2` makes the two representatives constant-factor comparable rather than independent; and Theorem 14.1 seals height-only spectral exclusion by construction. What remains is the zero-lift mechanical cocycle with its 3-adic residue constraint, which is exactly where section 21 points the next round.

<!-- BEGIN GENERATED measured block: python code/src65_emit_report_block.py -->

**The exact ceiling, and whether their float64 one is safe.** `ceil(beta l) = (3^l).bit_length()` because `beta*l` is never an integer. The shipped checker computes it as `ceil(log2(3)*l)` in float64. Over **20000** levels the two agree **20000** times out of 20000 (first disagreement: None), the certified fixed-point route was undecided **0** times and disagreed with the exact `3^l` route on **0** of the 6 levels cross-checked. The closest `beta*l` comes to an integer over that range is **2.625e-05**, at l = 15601, against a float64 error near **7.04e-12** — a margin of about **3.7 million**. Their shortcut is safe at these sizes, and now that is a measurement.

**The lift profile, in integers.** **1228** bridges from **1150** distinct sources (longest tail 42), **4337** profile positions. Theorem 6.1's `Z < X < (3Z+1)/2`: **0** upper and **0** lower violations, with `y < Z` failing **0** times and `X = (3y+1)/2` **0**. Theorem 7.1's `m_l >= 0`: **0** negative, and **0** positions where `m_l >= 0` disagreed with the suffix supercriticality it is equivalent to. The decomposition `2^{-H} = 2^{-m} 2^{-eps}`, as exact rationals: **0**. Theorem 8.1's `m_{l+1} - m_l = q_{h-l} - a_{l+1}`: **0**. Across **1044** descents, **0** fell by more than one and **0** happened at a mechanical one — both impossible, and both counted rather than assumed. The total lift disagreed with `Q - ceil(beta h)` **0** times.

**Every bridge has zero total lift.** **1228 of 1228** — the positive-lift branch of Theorem 15.1 and the rarity bound of Theorem 10.1 have **no finite instance at all** at this scale. The profile is not flat, though: the largest interior lift reached is **8**, so the excursion structure the round is about is genuinely present. RUN-045 found the same thing on A-U.2d.17's smaller population; this is the same fact on 1228 bridges under the bundle's own wider definition.

**The Laplace budget, reindexed.** The identity is A-U.2d.17's under `i = h - l`, and RUN-045 showed that one is the definition of `B_w`, so what is checked here is the reindexing itself: term by term against the old order, **0** violations, with the identity **0**. Theorem 9.1's `sum 2^{-m_l} < 6Z`: **0** violations on **1228** bridges, and the integer sum failed to sit between the real one and twice it **0** times — the sandwich `eps in (0,1)` forces and the only place the reindexing could hide. The largest ratio to the ceiling actually seen is **0.0055**, so `6Z` is loose by a factor of about 182. The quantile bound was exercised on **14736** instances with **0** violations, of which **0** were non-vacuous; replacing `6Z` by the sum it bounds gives **65** non-vacuous instances, **0** violations.

**The mechanical cocycle.** On **1228** bridges and **4337** steps: the plain reverse recursion **0** violations; Theorem 12.1's rewritten exponent **0**; Theorem 12.2's normalized form `U_{l+1} = (2^a U_l - 2^{-m_{l+1}})/3` **0**; the closed form `U_h = 2^{eps_h} Z - (1/3) sum 2^{eps_h-eps_l} 2^{-m_l}` **0**; the weights outside `(1/2, 2)` **0**. Boundary conditions: `U_0 != Z` **0** times, and on the **1228** zero-lift bridges `U_h != X` **0**. Theorem 13.1's residue parity **0**, and the fact it reduces to `q = pi(V_l) mod 2` disagreed **0** times; **0** reverse states fell outside `1, 2 mod 3`.

**The zero-lift class, without floating point.** `P_down = (Z/X) 2^{eps_h}` is an exact rational once `m_h = 0`, so Theorem 11.1's `P_down < 2` needs no float. On **1228** zero-lift bridges (**0** positive-lift): the excess decomposition `2^E = 2^{m_h} 2^{eps_h}` **0** violations, the product identity **0**, the bound itself **0**, and Corollary 11.2's reciprocal mass against a certified `4 ln 2 = 2.772589` **0**. The bundle's float64 form with its `1e-12` fudge would have decided differently on **0**. Largest product actually seen **1.007961**, largest reciprocal mass **0.023821** — the ceiling is loose by a factor of about 116, which is worth saying beside a zero.

**Theorem 14.1's countermodel, rebuilt from the paper's three steps** rather than accepted. **6** lengths, **0** failing their precondition. `m_0 = 0` **0** violations, `m_h = 0` **0**, `m_l >= 0` **0**, `q in {1,2,3}` **0**, `sum q = ceil(beta h)` **0**, `sum 2^{-m_l} < 6` **0**. The paper's proof splits that mass three ways and each part has its own bound: rise `< 1` **0** violations, plateau `< 1/h` **0**, descent `< 4` **0**, and a height held more than twice during the descent **0** — checking only the total would let two of the three be wrong in compensating directions.

| `h` | `M` | `max q` | `sum 2^-m` | rise | plateau | descent |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 14 | 3 | 4.737488 | 0.999939 | 0.005493 | 3.732056 |
| 256 | 16 | 3 | 4.467743 | 0.999985 | 0.003250 | 3.464508 |
| 512 | 18 | 3 | 3.867893 | 0.999996 | 0.001770 | 2.866127 |
| 1024 | 20 | 3 | 3.430056 | 0.999999 | 0.000926 | 2.429131 |
| 2048 | 22 | 3 | 3.429607 | 1.000000 | 0.000474 | 2.429133 |
| 4096 | 24 | 3 | 3.429374 | 1.000000 | 0.000240 | 2.429134 |

**Two of their twelve counters test a quantity against itself.** `near_linear_gap_algebra` asserts `lower > 0` for `lower = N/(R+1)` with `N >= 10^6` and `R >= 1`. Over **10000** samples at their stated ranges, **0** could have failed, and the smallest left side seen is **134322**. `positive_lift_drop_algebra` asserts `drop >= 2 - beta - 1e-15` for `drop = (m + eps) - (beta - 1)`; subtract the two sides and `beta` cancels, leaving `m + eps >= 1` with `m >= 1` an integer. Evaluated with `beta` at BOTH ends of a certified bracket over **10000** samples, the two results differ **0** times — which is what it means for the parameter not to participate — and **0** samples could have failed, the tightest margin being **0.0**. Twenty thousand of their assertion executions carry no information about `beta`, the bridge, or the round.

**All twelve published zero-lift examples, rebuilt from the map.** **0** disagreeing values of `X`, **0** of `Z`, **0** exponent words, **0** lengths, **0** total lifts, **0** maximum lifts, **0** lift sums, **0** tail products, **0** reciprocal masses, **0** tails not suffix-supercritical. **1** source appears more than once.

| `y` | `X` | `Z` | `h` | word | lift profile | `sum 2^-m` | `P_down` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 59 | 89 | 67 | 1 | `[2]` | `[0]` | `1` | 1.003745318 |
| 71 | 107 | 91 | 3 | `[1, 2, 2]` | `[0, 0, 0]` | `3` | 1.007961232 |
| 91 | 137 | 103 | 1 | `[2]` | `[0]` | `1` | 1.002433090 |
| 155 | 233 | 175 | 1 | `[2]` | `[0]` | `1` | 1.001430615 |
| 155 | 233 | 167 | 6 | `[2, 1, 1, 1, 2, 3]` | `[1, 1, 1, 0, 0, 0]` | `9/2` | 1.006776288 |
| 187 | 281 | 211 | 1 | `[2]` | `[0]` | `1` | 1.001186239 |
| 223 | 335 | 319 | 5 | `[1, 1, 1, 3, 2]` | `[0, 1, 1, 0, 0]` | `4` | 1.003181622 |
| 251 | 377 | 283 | 1 | `[2]` | `[0]` | `1` | 1.000884173 |
| 283 | 425 | 319 | 1 | `[2]` | `[0]` | `1` | 1.000784313 |
| 347 | 521 | 391 | 1 | `[2]` | `[0]` | `1` | 1.000639795 |
| 379 | 569 | 427 | 1 | `[2]` | `[0]` | `1` | 1.000585823 |
| 443 | 665 | 499 | 1 | `[2]` | `[0]` | `1` | 1.000501253 |

**Their six abstract countermodel rows**, rebuilt: **6** of **6** reproduced, **0** disagreeing `M`, **0** disagreeing `max q`, **0** disagreeing Laplace mass.

**A-U.2d.17's collapse, carried forward.** On the same **1228** bridges: **0** source and **0** endpoint congruence violations, with the source inside its modulus on **132** and the endpoint on **125**, both on **125** (10.2%), and **0** collapse violations there.

**The first-spike slice at the new scale.** Over **1321** orbits, **607** reached the threshold: **0** below it, **0** not minimal, **0** overshooting more than one step's slack gain, **0** violating the length bound, **0** prefix valuations below the length. The bound is attained with no additive constant on **309**. Containment is asymptotic and at these scales holds for a minority: source inside **165** / outside **442**, endpoint inside **142** / outside **465**.

**Constants.** 7 checked: **0** disagree with both readings of their own formula, 3 are the nearest double, 4 are what the same formula gives in float64, 0 brackets could not decide.

| constant | published | nearest double | budget | verdict |
| --- | --- | --- | --- | --- |
| `beta` | 1.584962500721156 | 1.584962500721156 | 4 | exact |
| `beta_minus_1` | 0.5849625007211561 | 0.5849625007211562 | 12 | -1 ulp, the float64 chain |
| `two_minus_beta` | 0.4150374992788439 | 0.4150374992788438 | 20 | +2 ulp, the float64 chain |
| `near_linear_gap_exponent_limit` | 1.0 | 1.0 | 4 | exact |
| `first_hit_single_cylinder_exponent_limit` | 1.7095112913514552 | 1.7095112913514547 | 12 | +2 ulp, the float64 chain |
| `first_hit_formal_joint_ratio_exponent_limit` | 3.4190225827029104 | 3.4190225827029095 | 12 | +2 ulp, the float64 chain |
| `zero_lift_reciprocal_mass_ceiling` | 2.772588722239781 | 2.772588722239781 | 4 | exact |

**Artifacts.** 9 files, 8 carrying a `CHECKSUMS` digest, **0** mismatches, **0** manifest lines naming a missing file; the only file with no digest anywhere is `CHECKSUMS.sha256`. The source-validation record names **3** files and digests **3** of them (**0** digest and **0** size mismatches), reports `all_ok = True`, **3** `json_parse` entries with **0** not true, `python_compile = True`, and **0** per-file `ok` flags not true. 3 files are absent from it: `CHECKSUMS.sha256`, `SOURCE_VALIDATION_AU2d18.json`, `verify_Hard_Zeta_AU2d18_double_canonical_spectral.py`.

**Ledger coverage.** The paper lists 17 proved items, 5 open problems, and 10 NO-GO headings of which 8 are in section 18; the ledger carries 14, 5 and 8, with an `open` key (True). Open items with no trace: none. NO-GO headings with no trace: none. The heuristic deciding those lists has controls at both ends and failed neither (0, 0).

**Their counters beside mine**, keyed on their names rather than mine: 0 of 12 had no counterpart here, 0 are reported as zero, and **12 of 12 are reproduced exactly** from the definition.

| check | theirs | mine |
| --- | --- | --- |
| `finite_local_bridges` | 1228 | 1228 |
| `rank_one_record_ratio` | 1228 | 1228 |
| `lift_profile_nonnegative` | 1228 | 1228 |
| `lift_recurrence_exact` | 4337 | 4337 |
| `lift_laplace_budget` | 1228 | 1228 |
| `mechanical_cocycle_exact` | 4337 | 4337 |
| `zero_lift_constant_product` | 1228 | 1228 |
| `zero_lift_harmonic_bound` | 1228 | 1228 |
| `canonical_collapse_cases` | 125 | 125 |
| `abstract_bounded_q_lift_excursions` | 6 | 6 |
| `near_linear_gap_algebra` | 10000 | 10000 |
| `positive_lift_drop_algebra` | 10000 | 10000 |

**Instrument and drill.** 11 instrument self-checks, 0 failed. The mutation drill planted **52** defects: **52** caught by the check they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed.

<!-- END GENERATED measured block -->

## Instrument

Eleven self-checks, each naming a world in which it fails.

The exact ceiling is tested **both ways round** — that it brackets `βℓ` strictly on both sides, and that it is *not* the floor — because a function returning `(3^ℓ).bit_length() − 1` would pass a one-sided containment test at every level. `2^{ε_ℓ}` must land strictly inside `(1,2)`, which a wrong base breaks immediately. The mechanical alphabet is checked for membership in `{1,2}`, for the absence of two consecutive ones that Theorem 14.1's construction depends on, **and** for the presence of both symbols, since a function returning a constant 2 would satisfy the first two. The residue lemma is enumerated over both classes and forty valuations rather than asserted from `2 ≡ −1 mod 3`. And Corollary 11.2's two elementary inequalities, `ln(1+1/3Y) ≥ 1/(3Y+1) ≥ 1/(4Y)`, are checked at rational points against a certified logarithm bracket.

Two structural changes came out of the drill rather than the reading.

**Every section now reports rather than raises.** Four planted defects made the gate crash — a negative index into `ceil_beta`, a negative shift count in `1 << m`, a `None` in a ratio. A gate that crashes has no verdict, so the drill scored them malformed and any real hole behind them would have stayed invisible. Each section now runs inside a guard that turns an internal exception into a named `errors.<section>_raised` counter, and the classifier tolerates a section that produced nothing.

**`2^k` is written `p2(k)`, not `1 << k`.** A negative lift is a *finding*, reported by `lift.lift_negative`; it must not explode four sections downstream. `2^k` is perfectly well defined for `k < 0`, so the fix is one helper rather than a special case, and after it the two defects that broke the profile are caught by the counter that names a broken profile.

## Drill

Fifty-two defects, one at a time, each planted at a pre-flighted unique anchor, with the gate restored byte for byte after every run. **52 caught, 0 missed, 0 malformed, both controls undisturbed, the gate byte-identical at the end.**

Eight defects needed re-aiming after the first pass, in three groups.

Four made the gate raise, and the fix belonged in the gate — above. That is the third round in a row where a crashing defect exposed a place the gate could not report, and this time the fix is general rather than local.

Three "changed nothing" because they **loosened** what they attacked: permitting a lift of `−10` where none is below zero, permitting a descent of three where none exceeds one, admitting `0 mod 3` where no reverse state is divisible by three. From a green baseline a loosened check finds nothing where a correct one found nothing; the mutation has to make the counter rise, which is RUN-045's lesson arriving in a second form.

One was caught by the right guard under a different name: climbing the abstract lift two at a time makes `q = a + 2 ∈ {3,4}`, so the valuation bound fires before the total-valuation one. That is the invariant doing its job, so the expectation was renamed rather than the defect re-aimed.
