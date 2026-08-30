# RUN-042 — Hard-Zeta A-U.2d.14: the round whose central theorem a real orbit can actually be asked about

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d14_Sparse_B_Support_Exhaustion_bundle_v0.1.zip` (source item 61) — 17 sections. Ships a checker report, a constants frontier, a theorem ledger, a route map, literature notes, a `CHECKSUMS.sha256`, a source-validation record, and a verification script.
**Tools:** [`src61_sparse_support_exhaustion.py`](../code/src61_sparse_support_exhaustion.py) · [`src61_drill.py`](../code/src61_drill.py) · [`src61_emit_report_block.py`](../code/src61_emit_report_block.py)
**Logs:** [`src61-au2d14.json`](../data/gate-logs/src61-au2d14.json) · [`src61-drill.json`](../data/gate-logs/src61-drill.json)

**Result: the mathematics verifies, and for the first time in several rounds the central theorem has a real population to be tested on. §3 is about every suffix minimum, not only B sources — and where RUN-041 could find zero B-injections in 460,024 intervals, this run finds 16,251 suffix minima and confirms Theorem 3.1 (`q_{s+1}=1`) and Corollary 3.2 (`7, 11 mod 12`) on every one of them, with zero violations. The A-envelope side of §§6–7 is equally testable and equally clean: 1,885 orbits, the exact product identity `z_A·2^Q = y_A·3^T·∏(1+1/(3Y_j))` holding everywhere. It also explains RUN-041's zero: every one of those 16,251 minima is an A-renewal, and a true suffix minimum with a first crossing would be a B-injection by definition. Two findings. `ψ(σ★)` and `1−σ★` are the same number — `2500/15291` exactly — and the frontier stores both, one ulp apart, side by side under the same key. And the source-validation record now carries sha256 digests of its own, which recompute correctly: the finding RUN-039, RUN-040 and RUN-041 each reported is fixed.**

---

## What it adds, and the shape of the argument

A-U.2d.13 showed completed B-support is polynomially sparse. The obvious escape is to hide the renewals somewhere the count does not see them — in intervals that have started but not finished, or in the complementary A family. This round closes both and then states what remains as an explicit trichotomy.

The B-start count splits exactly:

> `B_st(N) = M_N + U_N`

and the active backlog `U_N` is bounded twice — unconditionally by `1 + C_δ N^{1−θ★}δ_N^{θ★}`, and at local continued-fraction scale by `1 + √(𝒬_N N δ_N)`. Both come from the same two facts: all active intervals contain `N`, so laminarity makes them one nested chain; and none has crossed, so their slacks sit below `δ_N`.

The A side is controlled differently — not by completion but by its own lower envelope. `A_N ≪_ε 2^{E_A(N)}N^ε`, so a bounded or sublogarithmic envelope cannot carry polynomially many A renewals.

Put together, with envelope, slack and continued-fraction scales all subpolynomial, the **entire** suffix-minimum renewal process is `R_N ≤ N^{4/5+o(1)}`; and anything above `4/5` must pay one of three named prices: A-envelope rise, `M_β(N) ≥ N^{χ(κ)}` with `χ(κ)=(5κ−4)/3`, or `δ_N ≥ N^{ζ(κ)}` with `ζ(κ)=(κ+1)/3`.

The trichotomy's arithmetic rests on one identity, `2κ − 1 − χ(κ) = ζ(κ)`, which is exact and was checked over 400 random rational parameters rather than at the paper's own value.

## The round a real orbit can be asked about

This is the part worth dwelling on, because it is a change from the last several rounds.

RUN-039's §7–8 premise was met by one orbit in 66,665. RUN-041's B-injections did not occur at all — zero in 460,024 first-crossing intervals. Both times the honest report was a denominator, and the conditional theorems had to be checked as algebra.

§3 here is different. It is about **every** nonterminal suffix minimum, A or B:

> **Theorem 3.1.** A suffix minimum with `Y_s > 1` on an injective orbit has `q_{s+1} = 1`.

The proof is two lines — suffix-minimality plus injectivity give `Y_{s+1} > Y_s`, and `q ≥ 2` would force `Y_{s+1} ≤ (3Y_s+1)/4 < Y_s` — and both lines are directly measurable. So is Corollary 3.2, which turns `q=1` into `Y_s ≡ 3 mod 4` and then, with the post-entry 3-free property, into `Y_s ≡ 7` or `11 mod 12`.

**16,251 suffix minima across 2,295 orbit windows. Zero violations of either.** The `q=1 ⟺ y ≡ 3 mod 4` equivalence the corollary turns on: zero failures. No source divisible by 3. The ordinal floor `y^{(j)} ≥ 6j−1`: zero.

One measurement detail that matters. Taking a whole convergent orbit gives **no** suffix minima at all — it ends at 1, the global minimum, so nothing earlier is below its own suffix. The population only exists on a finite window, which is what the bundle's own checker scope specifies. A window that included the descent would have reported an empty set and looked like a premise failure; it is a definition failure instead.

## And it explains RUN-041's zero

Every one of those 16,251 minima turns out to be an A-renewal: **zero have a δ crossing inside the window**.

That is not a coincidence, and it retro-explains the previous round. If `s` is a *true* suffix minimum and a first crossing `e(s)` exists, then `Y_{e(s)} ≥ Y_s` by minimality and `≠` by injectivity — so `Y_{e(s)} > Y_s`, which is precisely the B-injection condition. A true suffix minimum with a crossing **is** a B-injection. RUN-041 measured zero of those in 460,024 intervals; this round says why there were none to find.

## The A envelope is testable too

§§6–7 concern the A-renewal family, which does occur. Across 1,885 orbits carrying two or more A-renewals (longest chain 17):

- `E_A(N) = βT − Q` agrees with the direct `δ` difference everywhere;
- the envelope is positive everywhere;
- the exact product identity `z_A·2^Q = y_A·3^T·∏(1+1/(3Y_j))` — written with no `β` in it at all, so no bracket decides it — holds on every segment;
- A-source values and their slacks are strictly increasing;
- `Y_{c_j} ≥ 6j−1` holds;
- Theorem 7.1 in the form its proof actually gives, `6A_N − 1 ≤ z_A`, holds on all 1,885.

One note on Theorem 7.1's statement. Its proof produces `6A_N − 1 ≤ z_A = y_A·2^{E_A}·𝒫_A`, which carries a `y_A` the boxed form drops. The paper is explicit that the constant "absorbs the fixed first post-entry A-source", and `y_A = Y_{c_1}` is indeed a single fixed number, so this is legitimate — but it is the kind of step worth naming, because the absorbed quantity is a *value*, not a count, and a reader skimming the boxed inequality would not see it.

## Finding 1 — one quantity, two values, in the same object

`ψ(κ) := (κ − (1−θ★))/θ★` is §10's unconditional active-slack exponent. At `κ = σ★ = 1/(1+θ★)` it simplifies:

> `ψ(σ★) = (σ★ − 1 + θ★)/θ★ = θ★/(1+θ★) = 1 − σ★`

exactly. Both are `2500/15291 = 0.16349486626119939…`.

The constants frontier stores both, adjacent, under `at_old_sigma`:

```
"psi": 0.16349486626119944,
"one_minus_sigma": 0.16349486626119947
```

They differ by one ulp. Each reproduces its own float64 route bit-for-bit — `(σ − (1−θ))/θ` from the published parents gives the first, `1 − σ` gives the second — so this is one number computed two ways and stored twice, not a wrong value. The paper's own prose prints `ψ(σ★) = 0.1634948662611994…`, which is the correct rounding to 16 places of the exact rational.

It is worth reporting because the bundle puts the two side by side, which is as close as an artifact comes to inviting the comparison, and because a downstream consumer reading the JSON would see a discrepancy where the mathematics has none.

## Finding 2 — the validation record now carries digests, and they check out

RUN-039, RUN-040 and RUN-041 each reported that the source-validation record listed files with encoding and delimiter checks and **no hash on any of them**. Three rounds running.

**That is fixed.** `SOURCE_VALIDATION_AU2d14.json` now carries a `sha256` for each of the six files it covers, and recomputing all six gives zero mismatches and zero entries naming a file that is not there. It also records `checker_rerun: PASS`, `python_compile: PASS`, and a six-entry commit gate with nothing failing.

A digest nobody verifies is the same as no digest, so this run recomputes them rather than reporting their presence. They are correct.

Three files are not in that record: `CHECKSUMS.sha256` and `SOURCE_VALIDATION_AU2d14.json` cannot list themselves, and `verify_Hard_Zeta_AU2d14_sparse_B_support_exhaustion.py` is covered by `CHECKSUMS` instead. So every file in the bundle except the manifest itself is pinned by something.

The ledger is clean: 11 proved items against the paper's 11, all six open problems present including CASP and the Collatz conjecture, and no NO-GO heading unaccounted for.

<!-- BEGIN GENERATED measured block: python code/src61_emit_report_block.py -->

**The constants, exact against the float64 route the artifact took.** Taking `rho* = 4.1164` as the decimal it is written as, every constant in this round is an exact rational.

| constant | exact rational | published | vs exact | vs float64 chain |
| --- | --- | --- | --- | --- |
| `theta_star` | `2500/12791` | 0.19544992572902825 | +1 ulp | exact |
| `active_backlog_unconditional_N_exponent` | `10291/12791` | 0.8045500742709717 | -1 ulp | exact |
| `old_disjoint_backbone_exponent_sigma` | `12791/15291` | 0.8365051337388005 | -1 ulp | exact |
| `AU2d13_completed_support_exponent` | `163609681/169859681` | 0.9632049232448516 | -1 ulp | exact |
| `AU2d13_completed_support_log_exponent` | `31977500/169859681` | 0.1882583307100406 | exact | exact |
| `controlled_total_renewal_support_exponent` | `4/5` | 0.8 | exact | exact |
| `high_support_threshold` | `4/5` | 0.8 | exact | exact |
| `at_old_sigma.chi` | `2791/45873` | 0.06084188956466748 | -27 ulp | exact |
| `at_old_sigma.zeta` | `28082/45873` | 0.6121683779129335 | exact | exact |
| `at_old_sigma.psi` | `2500/15291` | 0.16349486626119944 | +1 ulp | exact |
| `at_old_sigma.one_minus_sigma` | `2500/15291` | 0.16349486626119947 | +2 ulp | exact |

11 constants checked: **0** disagree with both readings of their own formula, 4 are the nearest double to the exact rational, and 7 are what the same formula gives in float64 from an already-rounded parent. `chi` is the outlier again, for the reason RUN-041 named: `5 sigma - 4` collapses 4.18 to 0.18, a **22.91-fold** loss of magnitude.

**One quantity, two values, same object.** `psi(k) = (k-(1-theta*))/theta*` at `k = sigma*` is `theta*/(1+theta*)`, which is exactly `1 - sigma*`. The identity holds: **True**. The frontier stores both under `at_old_sigma`, and they differ by **1 ulp** — `psi` is `'0.16349486626119944'` and `one_minus_sigma` is `'0.16349486626119947'`, while the exact value is `2500/15291 = 0.163494866261199398`. Each reproduces its own float64 route bit-for-bit (2 of 2), so this is one number computed two ways and stored twice, not a wrong value.

**The exponent algebra, as identities in the symbols.** Over 400 random rational parameter pairs: Theorem 4.1's step `rho/(rho+1) = 1-theta` **0** violations; Theorem 9.1's `2k-1-chi(k) = zeta(k)` **0**; section 10's inversion of the backlog bound for `psi` **0**; and `chi(k) > 0` exactly above `4/5` **0**. `chi(4/5) = 0` and `zeta(4/5) = 3/5`.

**Section 3 has a real population, unlike last round's B-side.** A B source does not occur on a convergent orbit; a suffix minimum does. Across 2295 orbit windows, **16251** suffix minima were found and every one of them satisfies Theorem 3.1 (`q_{s+1} = 1`, **0** violations) and Corollary 3.2 (`7, 11 mod 12`, **0**). The equivalence the corollary rests on, `q = 1` iff `y = 3 mod 4` on an odd source, failed **0** times; no source was divisible by 3 (**0**); the ordinal floor `y^(j) >= 6j-1` failed **0**; and the step the proof turns on, `Y_{s+1} > Y_s`, failed **0**.

And a structural fact that explains RUN-041's zero: **all 16251 of them are A-renewals**, with **0** having a delta crossing inside the window. A true suffix minimum with a first crossing would be a B-injection automatically — `Y_{e(s)} >= Y_s` by minimality, strict by injectivity — and there are **0** of those. RUN-041 found 0 B-injections in 460,024 first-crossing intervals; this says why.

**The A envelope, sections 6 and 7, also on real orbits.** 1885 orbits carried two or more A-renewals (largest chain 17). `E_A = beta T - Q` disagreed with the direct `delta` difference **0** times; the envelope was non-positive **0** times; the exact product identity `z_A 2^Q = y_A 3^T prod(1+1/(3Y_j))` — written with no `beta` at all — failed **0**; A-source values were non-increasing **0** and their slacks **0**; the `6j-1` floor **0**. Theorem 7.1 in the form its proof gives, `6 A_N - 1 <= z_A`, was checked on all 1885 and failed **0**.

**The B-side theorems, as algebra.** Theorems 4.1 and 4.2 are conditional on a B source, so they were checked as implications between finite quantities at integer `rho`, where the root is exact and no bracket is needed. Over 400 grid points: **0** and **0** violations, with the antecedent actually holding at 400 and 400 of them. Section 5's division and section 9's case split: **0** and **0** of 400.

**NO-GO 11.1, built rather than argued.** The claim is that a construction exists, so one was built: `t_j = 2^(j^2)`, records at those times, every intermediate above the next record. Enumerating the suffix minima of the result over 9 levels — up to `log2 N = 81` — the record times disagreed with `t_j` **0** times, the count disagreed with `sqrt(log2 N)` **0**, the sequence failed to diverge **0**, and an intermediate fell too low **0**. At the largest `N` there are 9 records.

**The criticality conversion, as the claim rather than the identity.** `delta_m/m = beta - K_m/m` is a rearrangement and testing it would measure nothing. What section 2.3 actually takes from the external input is that `liminf (m/K_m) = 1/beta` gives `limsup (K_m/m) = beta`. Over 200 sequences that reciprocal relation failed **0** times, the monotone conversion **0**, and the CASP sign condition **0**.

**What the prose prints.** 24 decimal instances across the paper and route map, **all 24 followed by an ellipsis**. **7** over-publish against the exact rational, 15 are exact to every digit, 1 is correctly rounded and 1 truncated.

**Artifacts — the three-round finding is fixed.** 9 files, 8 carrying a `CHECKSUMS` digest, **0** mismatches, **0** manifest lines naming a missing file. The source-validation record now carries **sha256 digests of its own**: 6 entries, **6 with a digest**, and recomputing every one gives **0** mismatches and **0** naming a file that is not there. Its commit gate reports PASS with **0** entries not PASS. RUN-039, RUN-040 and RUN-041 each reported this record as digest-free; it no longer is. Files it does not list: `CHECKSUMS.sha256`, `SOURCE_VALIDATION_AU2d14.json`, `verify_Hard_Zeta_AU2d14_sparse_B_support_exhaustion.py` — the first two cannot list themselves, and the third is covered by `CHECKSUMS`.

**Ledger coverage.** The paper lists 11 proved items, 6 explicitly open problems and 1 numbered NO-GO heading; the ledger carries 11, 6 and 5. It has an `open` key (True). Open items with no trace in it: none. NO-GO headings with no trace: none.

**Their counters beside mine.** Different populations, so a difference is information rather than a fault; 0 of their checks had no counterpart here.

| check | theirs | mine |
| --- | --- | --- |
| `finite_suffix_minimum_residue` | 553 | 16251 |
| `active_backlog_algebra` | 20000 | 400 |
| `active_backlog_cf_algebra` | 20000 | 400 |
| `A_envelope_transfer_algebra` | 10000 | 1885 |
| `support_escape_exponent_algebra` | 14 | 400 |
| `criticality_conversion_samples` | 4 | 200 |
| `sparse_set_counterexample_samples` | 360 | 9 |

**Drill.** 33 defects planted one at a time, **33 caught**, 0 malformed, 0 missed; 0 were caught only by a counter other than the one aimed at. All 33 anchors matched exactly one place before anything was planted. 2 of 2 controls undisturbed, and the gate came back byte-identical.

<!-- END GENERATED measured block -->

## The instrument

Three things went wrong on my side, and the drill found all three.

**A threshold test that never crossed its threshold.** The check that `χ(κ) > 0` exactly above `4/5` sampled `κ` from `[0.801, 2)` — entirely above `4/5`, and therefore entirely above `3/5` as well. Moving the threshold to `3/5` changed no verdict, and the drill correctly reported the defect as planting nothing. A threshold check whose sample never straddles the threshold is testing that two `True`s are equal. The sample now spans `(0, 2)`.

**A gate that raised instead of reporting, again.** A defect that let `suffix_minima` return the terminal index made the gate index past the end of the window and die with an `IndexError`. This is the same shape RUN-041 met one round ago: a traceback replaces a readable verdict with an absence, and the drill can only call it malformed. The terminal index is now counted and skipped, with its own counter, so the defect lands on a named verdict.

**Two defects that loosened what they attacked.** One let a suffix minimum admit ties — which an injective orbit never produces, so it was inert. One widened the accepted residue set from `{7,11}` to `{7,11,3}`, which can only reduce violations. Both were correctly refused as "the mutation changes nothing" and re-aimed to push the other way. This is the third round running where the first drill pass has produced defects pointing the wrong direction; the pattern is that attacking a *check* is easy to confuse with attacking the *claim*, and only the latter can go red.

The drill's totals are in the measured block above. Anchors were pre-flighted to exactly one match each, and the gate was verified byte-identical afterwards.

## What this run does not claim

It does not instantiate a divergent CASP orbit, and the B-side theorems of §§4–5 are conditional on one, so they are checked as algebra rather than on data — real orbits supply no active B backlog because they supply no B source at all. It does not certify the inherited `ρ★ = 4.1164`, nor the effective `c_δ` inside `C_δ`, which is never evaluated in this round or in mine. It does not verify the external criticality input of §2.3 — López–Stoll's parity-density theorem is taken as stated, and only the conversion from it (`liminf m/K_m = 1/β` giving `limsup K_m/m = β`) is checked. It does not verify §8's master bound or §9's trichotomy as asymptotic statements; it verifies the finite inequalities and the exponent arithmetic they are assembled from. It does not run the bundle's own verification script — every number here was recomputed independently, per the standing rule from item 35.

No Collatz claim is made or implied.
