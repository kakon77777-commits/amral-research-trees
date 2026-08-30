# RUN-040 — Hard-Zeta A-U.2d.12: a hierarchy that reaches exponent zero, and constants that outrun it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d12_3Adic_Transport_Hierarchy_Closure_bundle_v0.1.zip` (source item 59) — 24 sections. Ships a checker report, a constants frontier, a theorem ledger, a new block-hierarchy data file, a route map, literature notes, a `CHECKSUMS.sha256`, a source-validation record, a verification script, and the builder script.
**Tools:** [`src59_block_hierarchy.py`](../code/src59_block_hierarchy.py) · [`src59_drill.py`](../code/src59_drill.py) · [`src59_emit_report_block.py`](../code/src59_emit_report_block.py)
**Logs:** [`src59-au2d12.json`](../data/gate-logs/src59-au2d12.json) · [`src59-drill.json`](../data/gate-logs/src59-drill.json)

**Result: the mathematics verifies, and almost all of it needs nothing but integer arithmetic. `floor(β m)` is a bit length, `C_m^-` is a finite binomial sum, `γ_m` and `α̂_m` are exact rationals — so the six published levels, and the whole 150-level record set behind them, either reproduce or do not. They reproduce, every field. Lemma 10.1 was re-derived by an exact convolution that never mentions the closed form, and both halves of the closure — the Chernoff decay and the Diophantine floor on the phase gap — hold everywhere tested. The round is also unusually honest: it states three times that it does *not* settle the question A-U.2d.11 left open, and that boundary is accurate. Four findings, none of them a mathematical error: §1 states a premise weaker than §4's arithmetic uses, and under §1's reading Theorem 4.1 fails 221 times out of 999; the premise §§7–8 need is met by exactly one orbit in 66,665; the exponents fall but the explicit constants rise so much faster that at `m = 12` the new certificate only overtakes the old one past `L/y ≈ 10^334677`; and `θ★` carries one float64 rounding that all six source-floor exponents inherit.**

---

## The question it answers is not the question it was asked

A-U.2d.11 ended by asking whether its own finite-state LP exponents `α_h` tend to zero as the modulus `3^h` grows. This round does not answer that. It says so in §16, again as NO-GO 18.2, and again in §24 — and the ledger repeats it. That restraint is worth recording, because the easy move was available and was not taken.

What it does instead is build a *different* hierarchy from information the LP relaxation discards. The LP asks what a single residue-to-residue transport step can do. A real trajectory has to satisfy every overlapping exponent block at once, and that consistency is extra. Fix a block length `m`, and for each start `j` let

> `w_j = (q_{j+1},…,q_{j+m})`,  `Q_j = Σ q_{j+ℓ}`,  `g_j = 2^{Q_j}/3^m`

The exact product identity then gives a reciprocal relation per block, and summing it over `j` telescopes:

> `(g_j − 1)/Y_j = (1/Y_{j+m} − 1/Y_j) + (P_{j,m} − 1)/Y_{j+m}`

Blocks that grow must be financed by blocks that shrink, and shrinking blocks are rare for an arithmetic reason rather than a probabilistic one: an exact word of total valuation `Q` pins its source to one class mod `2^{Q+1}`, so it has only logarithmic harmonic capacity. Counting the words gives

> `C_m^- = Σ_{Q=m}^{⌊βm⌋} C(Q−1,m−1)/(3·2^Q)`,  `γ_m = 2^{⌊βm⌋+1}/3^m − 1`,  `α̂_m = (1/3)(1 + 1/γ_m)·C_m^-`

and that is the entire headline. Every symbol is an integer or a ratio of integers.

## Nothing here needs a logarithm

`⌊β m⌋ = ⌊log₂ 3^m⌋` is `(3**m).bit_length() − 1`, verified against `2^k ≤ 3^m < 2^{k+1}`. So the six shipped levels are decidable outright, and they decide correctly — `q_m`, `C_m^-`, `γ_m` and `α̂_m` all reproduce exactly, and every `alpha_hat_float` is the nearest double to its own exact rational.

The claim that matters more is the sequence, and the bundle ships the running minima to `m = 150`. Recomputing all 150 levels reproduces the record set exactly, on every field. It also confirms the paper's own caution that the sequence is not monotone: `α̂` **rose** at 93 of the 150 levels, because `γ_m` depends on which side of an integer `βm` happens to fall. The record structure, not the ordering, is the real claim — and the record structure is right.

## The generating identity, checked without its closed form

§10 rewrites `3C_m^-` as a lower-tail probability for independent geometric variables, and is careful to say this is an enumeration device, not a model of Collatz valuations. That care is warranted and the identity is exact, so it can be checked — but checking it by re-deriving `C(Q−1,m−1)/2^Q` would be circular: a wrong closed form would agree with itself.

So it was checked by convolving the geometric law directly, a computation that never mentions the binomial. Zero violations. The closed form was then checked separately against brute-force enumeration of compositions. Zero disagreements.

The closure needs both halves, and both hold: `C_m^- ≤ (1/3)e^{−I_β m}` over 150 levels, and the phase gap `γ_m ≥ (ln 2)·ε⁺ ≥ (ln 2)·‖βm‖` over 400. The Chernoff bound is at its tightest at `m = 2`, where the true value is 0.558 of the bound — close enough that the inequality is doing work rather than being trivially slack. `I_β` was also re-derived through the stated optimum `e^{t★} = β/(2(β−1))`, independently of the printed formula, and agrees.

## §15 derives the formula RUN-039 had to guess

Four rounds have now published a "dense source floor" exponent without stating how it was obtained. RUN-039 fitted `μ = (θ★ − α)/(1 − α)` to the four numbers and reported it as a fit.

§15 derives it: from `r ≤ C_ε y₁^{1−ε} L^ε` and `r ≳ N^{θ★}` with `L ≤ N`, one gets `y₁ ≳ N^{(θ★−ε)/(1−ε)}`, and the published exponent is that expression at `ε = α`. So the guess was the right one, and this run could use it as a quoted step: applied to `1/6`, `1/9`, `4/45` and `1373/25856` it reproduces all four inherited numbers, and to the six new `α̂_m` it reproduces all six `dense_source_floor_mu`. That is a cross-round check on five rounds at once.

## Finding 1 — §1 states a weaker premise than §4 uses

§1 fixes the premise as: *for a B interval rooted at `y`, every state **before its endpoint** is a distinct odd integer at least `y`.* The endpoint is explicitly outside.

§4 then bounds the telescoped boundary term by `m/y` using `Y_t ≥ y` for `t = L−m+1,…,L`, and bounds `Σ_{n=0}^{L} 1/Y_n²` by `9/(14y)` because "the states are distinct odd integers at least `y`". Both sums run **to `L` inclusive**. The arithmetic needs the endpoint too.

That is not a quibble, because the endpoint is exactly the state §1 exempts, and it is the small one. Measured on real orbits: taking the segment §4's arithmetic assumes — every state including the endpoint at least `y` — Theorem 4.1 held on all 999 summed balances. Taking §1's stated segment instead, the same source, the same `E_m(y)`, one extra state, gives **221 violations out of 999**.

The mechanism is specific, and it is not a marginal numerical effect. Admitting the endpoint admits one more *block*, the one that ends on the descending step — and that step's 2-adic valuation is unbounded. It enters the balance with weight `g_j = 2^{Q_j}/3^m`, which grows exponentially in that valuation, while `E_m(y)` is only `O_m(1/y)`. The worst case found at `m = 2` is `y = 151`, where the final step has `q = 10`, the closing block carries `g = 2^11/3^2 ≈ 228`, and the left-hand side reaches `0.994` against a bound of `0.0210` — **exceeded by a factor of 47**. At `m = 3` and `m = 4` the same source `y = 943` overshoots by factors of 28 and 21.

The theorem is true as §4 uses it. The repair is to the sentence in §1, or to the summation ranges in §4. It matters because §4's conclusion — that the error is `O_m(1/y)` *independently of `L`* — is called "the first key hierarchy closure", and no `O_m(1/y)` bound can absorb a term that scales like `2^{v_2}` in the closing step.

RUN-038 met this exact shape once already, and on the same question: Lemma 5.1 there also needed every state *including the endpoint* to be at least `y`, and applying it as stated produced 352 spurious violations until the endpoint was put back. Two rounds, two theorems, the same word left out of the same sentence — which is why the premise is now measured under both readings by default rather than assumed.

## Finding 2 — the premise §§7–8 need is met by one orbit in 66,665

Theorem 7.1 needs `y ≥ 7` and `L ≥ y`; Theorem 8.1 and Corollary 8.2 need `L ≥ max{m,y}`. That is a strong demand: the segment must stay above its own source for at least `y` steps.

A wider scan than the gate's own runs over every odd 3-free source from 7 to 200,000 — **66,665** of them, giving 25,000 suffix-minimum segments — and **exactly one** qualifies: `y = 31`, `L = 34`. (The gate's narrower scan, reported in the block below, reaches the same single segment.) The mean excursion length is 6.3 and the longest anywhere in the range is 80, at `y = 45127`. The reason is structural: the excursion above `y` grows like `log y` while `y` grows linearly, so the premise fails harder the further one looks.

Nothing is wrong here — these theorems are about the hypothetical divergent branch, where segments are long by construction. But it means the zero violations reported for Theorems 7.1, 8.1 and Corollary 8.2 rest on a single orbit, and this run reports them as the thin evidence they are rather than as coverage.

## Finding 3 — the exponent goes to zero and the constant goes to infinity faster

Corollary 8.2 is `𝒫 ≤ exp(B_m/3)·(L/y)^{α̂_m}`, and `α̂_12 = 188368/4654215 < 1373/25856` is genuinely below the previous round's exponent. The paper's claim — that for each fixed `m` every constant is explicit and finite — is true.

The constants are also enormous. `B_12 ≈ 2.9×10⁴`, and `B_48 ≈ 3.0×10²⁰`. Giving A-U.2d.11 the most generous possible additive constant, zero, the block certificate at `m = 12` only overtakes it once

> `L/y > 10^334677`

and at `m = 48`, once `L/y > 10^(8.8×10²⁰)`.

Their own report renders this as `max_actual_to_explicit_bound_ratio_by_m: {"12": 0.0}`. That `0.0` is a float64 underflow, not a measurement. Measured in orders of magnitude on the one qualifying segment, the `m = 12` bound exceeds the actual product by about **4227 powers of ten**.

This does not weaken Theorem 13.1. `𝒫 = (L/y)^{o(1)}` is a statement about exponents, and as an exponent statement it is a real advance — it removes any fixed positive local congestion exponent, which is exactly what NO-GO 18.5 claims. It does mean the hierarchy is not a numerical improvement at any scale a finite orbit will reach, and a reader comparing `0.0404` with `0.0531` should know which of the two facts they are looking at.

## Finding 4 — one rounding at the root of `θ★`, inherited six times

`ρ★ = 4.1164` is a decimal, so `θ★ = 1/(ρ★+1)` is the exact rational `2500/12791 = 0.19544992572902822…`, whose nearest double is `0.19544992572902822`. The bundle ships `0.19544992572902825`, one ulp higher.

The cause is not a typo. `4.1164` is not representable in binary; `float(4.1164)` is `4.11639999999999961…`, slightly low, so `1/(1 + float(4.1164))` lands slightly high, and its nearest double is exactly the published value. The formula is right; it was evaluated in float64 from an already-rounded parent.

The consequence is measurable: all six `dense_source_floor_mu` values match that float64 chain at **0 ulps** and the exact rational at 1 (2 at `m = 48`). One rounding at the root, inherited by every level. At the 10 decimal places §15 prints for the four inherited exponents, the difference is invisible.

It is not invisible for `θ★` itself. Inside the three JSON files it is a double, where one ulp is the honest description. But in the prose it is written **six times — five in the paper, once in the route map — always as `0.19544992572902825…`, with an ellipsis**. The ellipsis asserts that those seventeen digits are correct and more follow. The exact rational is `0.19544992572902822296927…`, so the seventeenth digit is `2`, not `5`: sixteen digits correct, one over-published, and the ellipsis promises a continuation that does not exist. Trailing digits of a constant that is itself a rounded inherited quantity are not load-bearing, but an ellipsis is a claim, and this one is the reason the ulp is visible at all.

`I_β` is clean: published to 15 places, and exact to every one of them. `β` is the nearest double.

## The record, and one thing fixed since last round

RUN-039 found that `build_AU2d11_artifacts.py` — the script that generated every other artifact — was the one file no digest pinned. **That is fixed.** `build_AU2d12_artifacts.py` is in `CHECKSUMS.sha256` this time, all ten listed digests reproduce, and the only file with no digest anywhere is the manifest itself, which cannot pin itself.

RUN-039's other finding has not moved. The ledger still has **no `open` key of any kind** — two rounds running. The paper's §22.4 lists four explicitly open problems; three can be pieced together from other keys in the ledger, and the fourth, **the Collatz conjecture**, appears nowhere in it as an open problem. The word "Collatz" occurs only inside the no-go "No full Collatz contradiction follows", and the word "conjecture" does not occur at all. A downstream reader parsing the JSON gets no machine-readable statement that the conjecture is open.

One naming note while here: `explicit_log_prefactor_Bstar` holds `B_m` itself, not `exp(B_m/3)` and not `𝓔*_m`. Recomputing §8's definition in plain float64 reproduces all six published values at a relative gap of zero, so the field is unambiguous — only its name is loose.

The source-validation record also still carries no digests of its own: all nine of its file entries list a name and some formatting checks, and none carries a hash.

<!-- BEGIN GENERATED measured block: python code/src59_emit_report_block.py -->

**The block hierarchy, checked with integer arithmetic only.** `q_m = floor(beta m)` is `(3**m).bit_length() - 1`, so no logarithm enters: `C_m^-`, `gamma_m` and `alpha^_m` are exact rationals and either equal the published values or do not.

| `m` | `q_m` | `alpha^_m` | beats `alpha_27` | `alpha^` float | `mu_m` |
| --- | --- | --- | --- | --- | --- |
| 12 | 19 | `188368/4654215` | yes | exact | `9226122412/57122648977` |
| 19 | 30 | `215272804/8866999629` | yes | exact | `19413944636536/110664237818575` |
| 24 | 38 | `39391833184/2405936496663` | yes | exact | `5510980303400956/30270472790559889` |
| 31 | 49 | `48094578331592/4574038595028093` | yes | exact | `10819918736130839228/57891349917564944291` |
| 36 | 57 | `9041308488735076/1243221667692413607` | yes | exact | `2992406792351623660384/15786400974574252090021` |
| 48 | 76 | `2162968935857911266976/642143559374605232774199` | yes | exact | `1577692362777954538919607484/8185991732302016989398889393` |

6 levels. `q_m` disagreements **0**, `C_m^-` **0**, `gamma_m` **0**, `alpha^_m` **0**, and `alpha^_12 < alpha_27` holds (0 failures). Every `alpha_hat_float` is the nearest double to its own exact rational (0 off). Frontier, checker report and block-data file agree with each other (0, 0 disagreements).

**The record set.** Recomputing every level to `m = 150` gives **57** running minima, and the shipped `record_minima_through_m150` list matches on every field (0 set disagreements, 0 row disagreements). The sequence is genuinely not monotone: `alpha^` rose at **93** of the 150 levels. The smallest value reached is `8.243437555755814e-06`.

**Lemma 10.1 by convolution, not by the closed form.** `3 C_m^- = Pr(G_1+...+G_m <= q_m)` was checked over 60 levels by an exact convolution of the geometric law, which never mentions `binom(Q-1,m-1)` -- **0** violations. The closed form itself was checked against brute-force enumeration of compositions on 63 cases, **0** disagreements.

**The two halves of the closure.** Chernoff: `C_m^- <= (1/3)e^{-I_beta m}` over 150 levels, **0** violations, tightest at `m = 2` where the actual is 0.558 of the bound -- so the inequality is not slack to the point of meaninglessness. The claimed optimum was checked independently: `-f(t)` exceeded `I_beta` at **0** of 199 grid points, and re-deriving `I_beta` through `e^{t*} = beta/(2(beta-1))` gives `0.054979472` (0 identity violations). Diophantine: over 400 block lengths, `eps+` left (0,1) **0** times and `gamma_m >= (ln2) eps+` failed **0**; the convexity step `2^x - 1 >= (ln2)x` failed **0** of 200 grid points.

**Section 15 derives the formula RUN-039 had to fit.** `mu = (theta* - alpha)/(1 - alpha)` is exactly section 15's `(theta* - eps)/(1 - eps)`. Applied to the four inherited exponents `1/6`, `1/9`, `4/45`, `1373/25856` it reproduces all 4 published source exponents, **0** disagreements:

| inherited `alpha` | published `mu` | verdict |
| --- | --- | --- |
| `1/6` | 0.0345399108 | truncated rather than rounded at the last digit |
| `1/9` | 0.0948811664 | exact to every published digit |
| `4/45` | 0.1169572356 | correctly rounded at the last digit |
| `1373/25856` | 0.1503309758 | correctly rounded at the last digit |

**On real orbits.** 500 accelerated segments were built from 1331 sources, none with a repeated state (0). Theorem 3.1 is an exact identity and was checked on **8261** sliding blocks: **0** violations. Theorem 4.1 held on all 999 summed balances (**0**), Theorem 5.1 on all 999 finance inequalities (**0**), and Theorem 6.1 on **5851** exact words (**0**).

**Section 1 states a weaker premise than section 4 uses.** Section 1 asks that every state *before* the endpoint be at least `y`; section 4 then bounds `sum 1/Y_n^2` over `n = 0..L`, endpoint included. Running Theorem 4.1 under section 1's reading -- same source, same bound, one extra state, the one below `y` -- gives **221 violations out of 999**. Under section 4's reading, 0.

**The premise sections 7-8 need is met once.** They require `L >= max{m,y}`. Scanning 19998 odd 3-free sources produced 7500 suffix-minimum segments, of which **1** has `L >= y` (`y = 31`). Mean excursion length is 6.26 and the longest anywhere in the range is 80, at `y = 45127` -- the excursion above `y` grows like `log y` while `y` grows linearly. So Theorems 7.1, 8.1 and Corollary 8.2 were exercised 5 times, and their zero violations are reported as the thin evidence they are, not as coverage.

**Source cylinders.** Section 6 says an exact exponent word of total valuation `Q` selects one source class mod `2^(Q+1)`, and at most two progressions mod `3*2^(Q+1)` after the 3-sieve. Over 15996 sources and 2944 distinct words (largest `Q` reached 22), words spanning more than one class: **0**; more than two phases: **0**. 1825 words had a single source and could not have disagreed, leaving 1119 that could.

**Where the certificate actually overtakes the old one.** Corollary 8.2 is `P <= exp(B_m/3)(L/y)^{alpha^_m}`, and the exponents do fall. The additive constants rise faster. Giving A-U.2d.11 the most generous possible constant -- zero -- the crossover is:

| `m` | `B_m` (recomputed) | `log10(L/y)` before the new exponent wins |
| --- | --- | --- |
| 12 | `29197.107` | 334677.0 |
| 19 | `34020249.265` | 170863395.4 |
| 24 | `5681546744.748` | 22393407782.8 |
| 31 | `7313352430940.096` | 24860015878413.4 |
| 36 | `1271247687679607.644` | 4015594951523517.5 |
| 48 | `301458619610228468203.603` | 8.774902239179183e+20 |

Measured on the one segment that meets the premise, Corollary 8.2's bound exceeds the actual product by these orders of magnitude, by block length: `{"2": 0.5, "3": 1.9, "4": 2.2, "6": 12.9, "12": 4226.7}`. Their own report renders the same ratio at `m = 12` as `0.0`, which is a float64 underflow rather than a measurement.

**Constants and their provenance.** `beta` is the nearest double (0 off). `I_beta` is `0.054979472810817071` and the published 15 digits are exact to every published digit. `theta*` is where a rounding enters: `rho* = 4.1164` makes `theta* = 1/(rho*+1)` the exact rational `2500/12791`, whose nearest double is `0.19544992572902822`, but the artifact ships `0.19544992572902825` -- which is what `1/(1 + float(4.1164))` evaluates to, because `float(4.1164)` is `4.11639999999999961...`. That single rounding is inherited by all 6 `dense_source_floor_mu` values: each matches the float64 chain at 0 ulps and the exact rational at 1 (2 at `m = 48`). Formula disagreements: **0**.

**Artifacts.** 11 files, 10 carrying a digest, **0** mismatches, **0** manifest lines naming a file that is not there. The one file with no digest anywhere is `CHECKSUMS.sha256`. RUN-039's finding is fixed: the builder `build_AU2d12_artifacts.py` **is** covered this time (True). The validation record still carries no digests of its own -- 9 of its entries list a file without one.

**Ledger coverage.** The paper lists 14 proved items, 4 explicitly open problems and 7 numbered NO-GO headings. The ledger carries 13, 0 and 5. It still has no `open` key of any kind -- the second round running. Open items with no trace in it: ["the Collatz conjecture"]. NO-GO headings with no trace: [].

**Their counters beside mine.** Different populations, so a difference is information rather than a fault; 0 of their checks had no counterpart here.

| check | theirs | mine |
| --- | --- | --- |
| `exact_sliding_block_identities` | 38336 | 8261 |
| `exact_summed_block_balances` | 306 | 999 |
| `finite_block_error_bounds` | 306 | 999 |
| `exact_code_source_residue_checks` | 1340 | 2944 |
| `repeated_code_same_residue_checks` | 171871 | 12941 |
| `chernoff_capacity_checks` | 150 | 150 |
| `symbolic_diophantine_envelope_numeric_sanity_checks` | 447 | 400 |
| `actual_explicit_product_bound_checks` | 12 | 5 |

**Drill.** 35 defects planted one at a time, **35 caught**, 0 malformed, 0 missed; 0 were caught only by a counter other than the one aimed at. All 35 anchors matched exactly one place before anything was planted. 2 of 2 controls undisturbed. The gate came back byte-identical.

<!-- END GENERATED measured block -->

## The instrument

Four things went wrong on my side and are worth recording, because three of them were instruments rather than mathematics.

**A gate that took 110 seconds per level.** `check_diophantine` called an exponential series on arguments widened to 60 digits; `_exp_bracket` multiplies its argument in 120 times, so the intermediate rationals reached seven thousand digits. Twenty levels took 110 seconds. The fix is the one RUN-039 already learned in a different guise — keep the operands small, since a bracket wider than necessary is still a bracket while a slow one is not usable. Widening arguments to 18 digits and matching the term count took 60 levels to 0.41 seconds. One check was also deleted rather than sped up: `γ_m = 2^{ε⁺} − 1` is not a claim, it is the same number written twice, and bracketing an exponential to "confirm" it would only have measured my own series.

**Three comparisons that measured my own instrument.** `B_m` is a float64 sum reaching `3×10²⁰`, so its last bit is accumulated rounding, not a published digit — an ulp test on it reported four spurious disagreements until it was replaced by a relative comparison. `I_β` is published to 15 significant digits where a double carries 17, so asking how many ulps away it sits measured the two digits the artifact did not write; it reads "exact to every published digit" under a decimal comparison. And `θ★` needed to be compared against *both* readings of its formula before the 1-ulp gap could be named as a cause rather than reported as an error. All three are the same lesson RUN-036 paid for: a comparison needs its reference at the precision the reference was actually published to.

**An off-by-one in my own convolution.** The Lemma 10.1 check truncated each level's distribution at that level's own `q_m + 1`, but `q_{m+1}` can exceed `q_m + 1`, so the next level was convolved from a distribution missing its top states. Caught by reading the code, before it could report a violation against correct arithmetic.

**A heredoc that ate a backslash — twice.** This machine's shell drops one backslash level even through a quoted heredoc. I ran a canary to check, saw it print `\d+\s`, and read that as success; it was the failure, since the source said `\\d+\s`. The result was a regex `\ldots` that raised `bad escape \l`, and later a `newline="\n"` that became a literal newline inside a string. Both were caught by compiling, but the canary was the real error: I read it for whether it printed something plausible instead of whether the count survived.

**A patch that silently did nothing.** One of the edits above was applied by `str.replace` with the wrong indentation and **no assertion**, so it matched zero places and reported success. Nothing failed until the emitter crashed on the field that was never added. Every other edit in the same script carried `assert old in t` and would have raised immediately. A replacement without an assertion is not an edit, it is a wish — and the surrounding script proved the habit was already there and simply not applied to that one line.

**Two weaknesses the drill found in the gate, which is what it is for.** A counter named `epsilon_plus_below_the_nearest_integer_distance` tested `ε⁺ ≥ ‖βm‖` — but `‖βm‖` is `min(βm − q, ε⁺)`, so `ε⁺` is one of the two arguments of that minimum and the inequality holds by definition. Written as a check it was a branch that **could never fire**, reading green over 400 levels while testing nothing; it has been replaced by `0 < ε⁺ < 1`, which a phase read from the wrong side can actually break. And the provenance escape hatch added for `θ★` — "this matches the float64 chain, so it is a rounding, not an error" — was **unbounded**, so when the drill planted a `θ★` built from the wrong exponent entirely, the counter stayed silent and a sibling check caught it instead. An excuse for a rounding has to be bounded like one; it is now capped at two ulps.

Three defects also had to be re-aimed rather than the gate changed: one dropped only the topmost convolution state, which cannot change a sum taken below it ("the mutation changes nothing" — inert, not missed); one flipped a sign so hard that `I_β·150` left the exponential series' stated domain and the gate raised instead of answering; and one built a `Fraction` from a float once `Q` fell below 3. A defect that crashes the subject tests the crash, not the check.

The drill's totals are in the measured block above. Every anchor was pre-flighted to exactly one match before anything was planted, "the mutation changes nothing" is classified as malformed rather than missed, and the gate was verified byte-identical afterwards.

## What this run does not claim

It does not instantiate a divergent orbit, does not prove positive linear completed B-density, and does not independently certify the inherited effective Diophantine constant `ρ★ = 4.1164` — that is imported from A-U.2d.3, and over `m ≤ 400` the observed `ε⁺` never comes within seven orders of magnitude of the floor it asserts, so this run's data neither confirms nor stresses it. It does not verify Theorem 12.1's limit, which is a statement about all `m`; it verifies the two inequalities the limit is assembled from, at 150 and 400 levels respectively. It does not run the bundle's own verification script — every number here was recomputed independently, per the standing rule from item 35.

No Collatz claim is made or implied.
