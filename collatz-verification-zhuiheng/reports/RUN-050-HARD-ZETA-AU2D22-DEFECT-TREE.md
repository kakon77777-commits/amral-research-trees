# RUN-050 — Hard-Zeta A-U.2d.22: the strongest checker of the sweep, and the one claim it leaves out

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d22_Loop_Tree_Defect_Renormalization_Rigidity_v0.1` (source item 69) — 20 sections, nine files.
**Tools:** [`src69_defect_tree.py`](../code/src69_defect_tree.py) · [`src69_drill.py`](../code/src69_drill.py) · [`src69_emit_report_block.py`](../code/src69_emit_report_block.py)
**Logs:** [`src69-au2d22.json`](../data/gate-logs/src69-au2d22.json) · [`src69-drill.json`](../data/gate-logs/src69-drill.json)

**Result: the mathematics verifies, and this is the best-checked round of the sweep — sixteen counters, not one of them a synthetic block that cannot fail, breaking a five-round streak. Eleven reproduce exactly on the same population; the other five are drawn from a seeded RNG and are covered here by larger deterministic enumerations. The round closes A-U.2d.21's semantic gap by changing the object: the general path defect `𝔡_M(P;r,s)` is defined for arbitrary endpoints, its quotient-affine matrix composes exactly, and chronological loop erasure that retains the CURRENT occurrence yields contiguous, laminar return intervals — so the quotient-layer identity applies to them. Three findings. Corollary 13.2, which names the constant on the frontier, has no counter at all; measured here, its two halves hold and both converge with `h`, but its conjunction is EMPTY on 240 of 1,080 bridges. Section 5's proof attributes contiguity and laminarity to the retention update, and measurement says otherwise: both retention rules give 0 crossings and 0 non-contiguous intervals, and Theorem 6.1 still reconstructs under the wrong one — what the update actually buys is the tree's shape, 8,796 nested pairs against 153,929. And their laminarity counter cannot fail, not because it is weak but because the stack truncation makes a crossing structurally unrepresentable — which is a different thing from the five cannot-fail blocks of earlier rounds, and is stated here so the zero is not mistaken for evidence.**

---

## The round's move

A-U.2d.21 proved a modular certificate for erased graph cycles and then proved an obstruction against its own next step: a cycle produced by nested chronological erasure need not be a contiguous interval of the original orbit, so the quotient-layer identity cannot be applied to it. RUN-048 had reached the same distinction one round earlier by measurement, and RUN-049 sharpened it — the lift holds on 100% of contiguous cycles and fails on 100% of spliced ones.

This round does not repair the cycle. It **changes the object**. For an arbitrary path `P` with endpoints `r, s` in the quotient layer,

> `𝔡_M(P; r, s) := (B_P + 3^{L_P} r − 2^{Q_P} s) / M ∈ ℤ`

with the quotient-affine matrix

> `R(P) = [[3^{L_P}, 𝔡_M(P)], [0, 2^{Q_P}]]`,  `R(PR) = R(R)·R(P)`.

No return condition is needed, so nothing has to be contiguous for the algebra to hold. What contiguity is then needed *for* is the tree: erasure that retains the current occurrence produces return **intervals**, and those are contiguous by construction, so Theorem 6.1 can factor the whole bridge matrix through the interval tree exactly.

That is a genuine repair, and the checker that ships with it is the strongest of the sweep.

## What their checker does right

Five consecutive rounds shipped counters that could not fail: assertions inside `if`s that never opened, bounds vacuous on every finite instance, identities that were definitions, guards at exact equality. **This round has none.** Its final 12,000-iteration block is a real composition check on residue paths built from actual transitions, not a synthetic identity. Every one of the sixteen counters names something that could come out wrong.

Worth saying plainly, because the previous eight reports have mostly said the opposite.

## Finding 1 — the corollary that names the frontier constant has no counter

The bundle's frontier publishes `faithful_loop_mass_constant = 0.4150374992788439`. It is the round's headline quantitative claim, stated as **Corollary 13.2**:

> the zero-lift critical bridge contains fully valuation-faithful modular return cycles whose total edge mass is `≥ (2 − β − o(1))h`, and whose retained high-lift vertices lie on actual quotient states satisfying the polynomial floor of Theorem 13.1.

The sixteen counters cover every numbered theorem and skip this. That matters more than an ordinary coverage gap, because the corollary's content is a **conjunction** that the bundle only ever tests as two separate statements: Theorem 13.1 is checked on *all* high-lift positions, and the mass bound is inherited from A-U.2d.21. Nothing checks that the vertices carrying the faithful mass are the vertices on the floor. A conjunction whose two sides never meet is vacuous, and no counter would show it.

Measured at the same parameters (`γ = 0.20`, `η = 0.45`, so `0 < γ < η < 1 − γ` holds):

* the intersection is real — **3,203 of 9,445** retained vertices are high-lift, and **0** of them violate the floor;
* but it is **empty on 240 of 1,080 bridges (22.2%)**, which have no high-lift retained vertex at all for the corollary to speak about.

The mass half carries an `o(1)`, so a finite shortfall is not a violation and is not scored as one. What can be measured is the **trend**, since that is what an asymptotic claim asserts — and both deviations shrink with `h`: the mean ratio sits above `2 − β` in every band, the fraction below it falls from 42.3% to 0%, and the vacuity of the second conjunct is gone entirely by `h ≥ 30`. The `o(1)` is doing honest work.

That is a favourable result for the corollary. It is still an untested one in the bundle, and the 22.2% vacuity is the kind of thing a counter exists to surface.

## Finding 2 — the proof credits the retention rule with more than it does

Theorem 5.1's proof sketch derives both contiguity and laminarity from the stack discipline:

> A crossing configuration would require a residue removed from the stack to remain simultaneously available as a retained ancestor, which the algorithm forbids.

The single line that implements this is `stack_t[p] = i` — on a repeat, the retained time advances to the **current** occurrence rather than staying at the first. It is the difference between this round's object and A-U.2d.21's, and the paper leans on it.

Running both rules over the same orbits: they produce **different** interval families on **7,302 of 18,603 levels (39.3%)** — and both give **0** crossings, **0** non-contiguous intervals, **0** misanchored endpoints, and **0** reconstruction failures for Theorem 6.1.

So the update is not what makes the family laminar or contiguous, and Theorem 6.1 does not need it either. Both statements are true under either rule. What the update actually controls is the **shape of the tree**:

| | paper's rule | retaining the first |
| --- | ---: | ---: |
| nested pairs | 8,796 | 153,929 |
| of which sharing a left endpoint | 0 | 130,140 |
| total interval span | 91,524 | 282,503 |

Without it the intervals become a deep stack of prefixes hanging off one point — 17.5× the nesting, 3.1× the span, 84.5% of the nested pairs sharing a left endpoint. The renormalization is a **partition** because of that line, rather than a repeated re-covering of the same prefix. The theorem is true as stated; the mechanism named in its proof is not the one carrying those two conclusions.

## Finding 3 — a zero that is structural, not evidential

Their `contiguous_loop_tree_laminarity` counter (18,603) asserts no two intervals cross. It cannot fail — and neither can mine.

This is a *different* failure mode from the cannot-fail blocks of the last five rounds, and the distinction is worth keeping. Those were weak checks. This one is a check whose negation is unrepresentable: the stack is truncated at every repeat, so a residue that could form a crossing has already been removed from `pos`. Attempting to plant a crossing by leaving a removed residue reachable does not produce one — it raises `IndexError`, because the retained-time array was truncated with the stack.

A counter that cannot go red is not evidence, whatever the reason. So the gate exercises the crossing predicate by hand on a constructed crossing pair, and the report says which of the two kinds of zero this is. Without that, `crossing_pairs = 0` and a broken predicate look identical.

## What this gate adds beyond theirs

* **Order sensitivity of the composition.** RUN-049's headline was a bilinear law tested only on inputs where its two coefficients swap into each other. The matrix product here has the same hazard, so this gate verifies `R(R)R(P) ≠ R(P)R(R)` on the population before believing the law — 92,888 of 106,265 products distinguish the two orders.
* **Two float64 inequalities re-derived in exact integers.** The lift toll `m > Q + log₂(M/Z₀) − 1` is exactly `2^{m+1}Z₀ > 2^Q M`; the quotient floor `n > (2^{m−1}Z − M)/M` is exactly `(n+1)M > 2^{m−1}Z`. Both are computed both ways and any disagreement counted; both routes agree everywhere, so their `1e-12` fudge is not deciding anything.
* **The sign law in integers.** `Q ≤ βL` is exactly `2^Q ≤ 3^L`. Their `BETA*L` float agrees on every case here.
* **Distance to failure for both bounds.** A bound that never comes near failing is loose, not strong, and the honest report is the margin: the quotient floor's tightest is **2.0228×** — nearly attained — and the lift toll's is **15.17×**.
* **`u ≥ 1` in the resonance**, which the paper states and their checker does not test; the smallest `u` seen is 10.
* **Their probe cap, measured.** Theorem 8.1's `only if` half is reached only when the probe exceeds the defect's valuation; their `min(ν+2, 5)` tops out at `min(ν+1, 4)`, so it misses that half whenever `ν ≥ 4`. On this population that costs 34 intervals — a small, real gap, stated as a number.

## Cross-read against the previous round

A-U.2d.21 published `fully_faithful_loop_mass_constant`; this round republishes it as `faithful_loop_mass_constant`. Same digits, same +2 ulp offset from the correctly-rounded double, same float64 chain `2.0 - log2(3)`. A rename with no drift — the reassuring outcome of a cross-read, recorded because per-file checks cannot see it.

## Standing items

The self-validation record is back to per-file `pass` entries but still carries **zero digests** — the ninth round in a row that records passing without recording what it hashed. Per the RUN-032 line, that is a finding in this log, not a gate failure.

<!-- BEGIN GENERATED measured block: python code/src69_emit_report_block.py -->

**The population.** **7845** bridges from **7357** distinct sources (longest tail 73), of which **7845** have zero total lift and **0** do not — the sixth round running in which the positive-lift branch has no finite instance. Their checker publishes `finite_local_bridges` and `zero_lift_bridges` as separate counters; both read **7845**, because a local bridge has minimal `Q` by definition and its total lift is therefore zero. The second counter filters nothing.

**Theorem 3.2, the quotient lift.** `2^Q n' = 3^L n + d` was checked on **249736** deterministically enumerated spans across **18603** bridge-precision levels: **0** violations, and **0** spans where the defect failed to be an integer.

**Theorem 4.1, and the order it is about.** The composition held on **106265** matrix products, with **0** disagreements between the matrix form and the written-out defect form and **0** products whose diagonal was not multiplicative. The previous round's headline was a bilinear law tested only where its two coefficients swap into each other, so the population is measured for order sensitivity here before the law is believed: `R(R)R(P)` differs from `R(P)R(R)` on **92888 of 106265** products (87.4%), and coincides on **13377**. The law is being tested where it can distinguish itself from its reverse.

**Theorem 5.1, and what the retention rule actually buys.** **47860** erasure intervals over **18603** levels: **0** with endpoints not congruent, **0** not contiguous, **0** crossing pairs, and **8796** nested pairs on **3084** levels, so the laminar family is populated rather than trivially empty. But `crossing_pairs` **cannot rise**. The stack truncation makes a crossing structurally unrepresentable — planting the opposite retention rule leaves it at zero, and a variant that keeps a removed residue reachable raises `IndexError` instead of producing one. The predicate is therefore exercised by hand in the instrument, or a zero here would be indistinguishable from a broken test. Their `contiguous_loop_tree_laminarity` counter has the same property.

**What the paper attributes to `stack_t[p] = i`, measured.** Section 5's proof sketch derives contiguity and laminarity from the stack discipline. Running both retention rules over the same orbits: they produce **different** interval families on **7302 of 18603** levels (39.3%), and *both* give **0**/**0** crossings, **0**/**0** non-contiguous intervals and **0**/**0** misanchored endpoints — and Theorem 6.1 still reconstructs under the wrong rule, **0** failures. The update is not what makes the family laminar. What it controls is the tree's shape: nested pairs go from **8796** to **153929**, of which **130140** share a left endpoint under the wrong rule and **0** under the paper's, and the total interval span goes from **91524** to **282503**. The renormalization is a partition because of that line; laminarity would have survived without it.

**Theorem 6.1, the tree reconstruction.** Rebuilding each bridge's matrix from its interval tree and comparing against the direct product: **0** disagreements at the root and **0** at the **47860** interior nodes, with **0** node spans whose defect was not an integer.

**Theorems 7.1–7.3 and 12.1.** The root defect vanished at the canonical modulus on all **7845** bridges, with **0** moduli failing to exceed both endpoints. The ordered weighted expansion summed to zero on **23535** partitions (**0** non-integral blocks), of which **4806** (20.4%) carry a nonzero block and so can exercise Corollary 7.3 — the other 79.6% are all-zero and test nothing. The ultrametric minimum was unpaired **0** times. The prefix/suffix coboundary held at **8641** cuts: **0**, **0** and **0** failures of its three forms.

**Theorem 8.1, both directions.** **94204** probes over **42544** intervals, **0** violations. The equivalence has an `only if` half that is only reached when the probe goes above the defect's valuation: **42539** probes did (45.2%), **51665** did not, and **5** intervals never had their upper half probed at all. Their loop caps the probe at `min(nu+2, 5)`, whose largest step is `min(nu+1, 4)` — above `nu` only when `nu <= 3`. On this population that costs them the upper half on **34** intervals, the largest valuation seen being **5**. A small gap, and worth stating as a number rather than left implicit.

**Theorem 9.1 in exact integers.** `Q <= beta L` is exactly `2^Q <= 3^L`, and the bundle evaluates `BETA*L` in float64. Over **47860** return intervals the sign law failed **0** times, a nonpositive defect was non-supercritical **0** times, and the two routes disagreed **0** times — so on this population their float evaluation decides every case the way exact arithmetic does. **6894** defects were negative, the largest in absolute value running to 98 bits, so the law's contrapositive has a real population.

**Theorems 10.1 and 11.1.** **2935** zero-defect intervals, all supercritical (**0** exceptions). The resonance `n = 2^Q u`, `n' = 3^L u` held with **0** divisibility failures and **0** disagreeing parameters. The paper also asserts `u >= 1`, which their checker does not test: **0** violations, and the smallest `u` seen is **10**, so the claim is satisfied with room rather than at its boundary. The lift toll is guarded in float64 with a `1e-12` fudge and is exactly `2^{m+1} Z0 > 2^Q M` in integers: **0** and **0** violations of its two forms, **0** disagreements between the two routes, and **0** tolls that one fewer lift bit would break. Its tightest margin over the whole population is a factor of **15.1667**.

**Theorem 13.1, and how close it runs.** `n > (2^{m-1} Z - M)/M` is exactly `(n+1) M > 2^{m-1} Z`: **0** violations over **4496** high-lift positions on **1080** bridges, **0** disagreements with their float route, and the floor was nontrivial (right side above the modulus) at **4496** of them. **0** positions sit within a factor of two of failing, and the tightest margin anywhere is **2.0228** — so this bound is nearly attained rather than comfortably loose, which is what makes it worth stating. The smallest quotient seen is **1498**.

**Corollary 13.2, which has no counter of its own.** The round's sixteen checks cover every numbered theorem and skip the corollary that names the frontier constant. Its content is a *conjunction* the bundle only tests as two separate statements: the faithful core's retained high-lift vertices are the ones claimed to sit on Theorem 13.1's floor. Measured over **1080** bridges: **9445** retained vertices, **3203** of them high-lift (33.9%), and **0** below the floor. The conjunction is real — but it is **empty on 240 bridges** (22.2%), which have no high-lift retained vertex for the corollary to speak about. The mass half carries an `o(1)`, so a finite shortfall cannot be a failure: the ratio ranges over **0.090909 to 0.875** and falls below `2 - beta = 0.4150` on **432 of 1080**.

**Both halves of the corollary converge.** An asymptotic claim is tested by its trend, not by a finite count, so both deviations were binned against bridge length:

| `h` | bridges | mean mass/`h` | below 0.4150 | no high-lift retained |
| --- | ---: | ---: | ---: | ---: |
| 0–9 | 248 | 0.4642 | 42.3% | 31.5% |
| 10–19 | 604 | 0.4558 | 40.7% | 25.3% |
| 20–29 | 145 | 0.4507 | 41.4% | 6.2% |
| 30–39 | 55 | 0.4542 | 34.5% | 0.0% |
| 40–49 | 15 | 0.4834 | 6.7% | 0.0% |
| 50–59 | 4 | 0.4581 | 25.0% | 0.0% |
| 60–69 | 7 | 0.4644 | 0.0% | 0.0% |
| 70–79 | 2 | 0.4790 | 0.0% | 0.0% |

The mean sits above the constant in every band, the shortfall falls away with `h`, and the vacuity of the second conjunct disappears entirely by `h >= 30`. The `o(1)` is doing honest work. The tail is thin — **13** bridges above `h = 50` — so the trend is clear and the last rows are not on their own evidence.

**The published rows.** **20** nonzero and **20** zero-defect nodes recomputed: **0** length disagreements, **0** valuations, **0** sign-law failures, **0** zero nodes that were not supercritical, **0** whose endpoints were not congruent to the published residue, **0** failing the lift identity `2^Q n' = 3^L n` recomputed from the published endpoints, and **0** resonance parameters disagreeing.

**The constants.** **2** checked, **1** exact to the last bit, **1** matching the float64 chain rather than the nearest double, **0** disagreeing with both, **0** undecided, **0** missing from the frontier, and **0** where the frontier and the report disagree. The mass constant is republished from the previous round under a shorter name (`fully_faithful_loop_mass_constant` → `faithful_loop_mass_constant`) with **identical digits** and the same +2 ulp offset — cross-read across the two rounds, there is no drift.

**Their sixteen counters.** **11** reproduce exactly on the same population. The other **5** are drawn from their seeded RNG block, so no independent run can match the integer; each is covered here by a deterministic enumeration that is larger than theirs, and the cross-report table names my counter rather than leaving a blank that would read as *not reproduced*. **0** of their checks are covered by nothing here, and **0** of them report zero.

**The bundle as shipped.** **9** files, **8** digests listed, **0** mismatches, **0** checksum lines naming a file that is not there, and `CHECKSUMS.sha256` with no digest anywhere. The validation record carries **3** per-file entries of which **0** carry a digest — the ninth round in a row whose self-validation records `pass` without recording what it hashed. `CHECKSUMS.sha256`, `SOURCE_VALIDATION_AU2d22.json` absent from it entirely. Against the paper, the ledger lists **15** proved items to the paper's **16**, **6** open to **6**, and **6** no-go entries to the paper's **8** headings; **0** open items and **0** no-go headings have no ledger counterpart, and the coverage heuristic passed both its controls.

**The drill.** The instrument self-tests **11** properties before the gate runs, **0** of them failing. **36** defects were planted one at a time: **36** caught by the counter they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed. Two defects aim at non-vacuity entries rather than failure counters, because last round's headline was a law whose second half was only an observation.

<!-- END GENERATED measured block -->

## Verdict

The round's mathematics holds on every count I can reach independently, and the bundle's own checking is the strongest of the sweep. The three findings are about what the checker does not look at (Corollary 13.2), what the proof credits to the wrong mechanism (the retention rule), and one zero that is structural rather than evidential (laminarity). None of them contradicts a theorem.

Next: item 70, `A-U.2d.23 — Quotient-State Resonance and Defect-Carry Rigidity`.
