# RUN-048 — Hard-Zeta A-U.2d.20: the round whose central object is a loop, and the two things "loop" turns out to mean

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d20_Mesoscopic_Ternary_Return_Discrepancy_Rigidity_bundle_v0.1.zip` (source item 67) — 20 sections, nine files.
**Tools:** [`src67_return_loops.py`](../code/src67_return_loops.py) · [`src67_drill.py`](../code/src67_drill.py) · [`src67_emit_report_block.py`](../code/src67_emit_report_block.py)
**Logs:** [`src67-au2d20.json`](../data/gate-logs/src67-au2d20.json) · [`src67-drill.json`](../data/gate-logs/src67-drill.json)

**Result: the mathematics verifies, and all twelve of the bundle's counters are reproduced exactly from the definition — 7136 bridges, 27,337 boundary levels, 29,282 transition pairs, 3,826 loop-mass levels, 1,802 clean runs, and the three synthetic blocks. A-U.2d.19 showed a fixed ternary modulus has too little magnitude resolution; this round asks what a growing one can see, and finds two structures with opposite characters — an `O(log h)` endpoint boundary layer that a near-full modulus resolves faithfully, and a bulk carrying linear mass of modular return loops with at most three valuation labels each. The sharpest object in it is Theorem 11.1's loop certificate `(2^{Q_C} − 3^{L_C})r_C ≡ B_C (mod M)`, and the bundle never checks it: its loop block verifies mass lower bounds only. Built from the real orbits, the certificate holds on all 34,970 loops. Three findings. "Return loop" names two different objects and the period bounds one of them: the erased cycle (0 violations, longest 13) and the orbit segment carrying the certificate, of which 14,539 of 34,970 exceed the period and 24,798 differ from their own cycle. Theorem 9.1's finite lower bound is positive on 4 of 3,826 levels, so a comparison against it discriminates almost nothing — my drill found that by planting four defects in my own section and watching none of them move a counter. And `fixed_power_high_lift_algebra`, 10,000 iterations, contains three assertions: one arranged by the line above it, one that is the same inequality restated, and one on a constant computed outside the loop.**

---

## The round's two structures

A-U.2d.19 left a target: work at a growing modulus `3^{k(h)} = h^{Θ(1)}`. This round determines what that can and cannot see, and the answer splits.

**The endpoint is temporally local.** With `Q_ℓ` the valuation sum of the final `ℓ` edges,

> `Z ≡ Σ_{j=1}^{k} 3^{j−1}2^{−Q_j} (mod 3^k)`

— a **k-term** sum. At polynomial precision the canonical endpoint is an `O(log h)` boundary layer, and the source side is automatically faithful because zero total lift forces `P_r ≤ ⌈βh⌉ − ⌈β(h−r)⌉ ≤ 2r`. So the two bridge boundaries are arithmetically asymmetric, which is NO-GO 14.2.

**The bulk is full of return loops.** With `M = 3^k` and `s_k = ord_M(2) = 2M/3`, a residue transition `r' ≡ (3r+1)2^{−q}` determines `q` modulo `s_k`, so labels below `s_k` are unique and labels below `2M` have at most three sheets. Deleting low-lift vertices and `q ≥ 2M` edges and loop-erasing what remains leaves a linear mass of modular return loops — `(1 − β/3 − o(1))h`, with `1 − β/3 = 0.4716791664…` — each carrying an exact certificate.

Almost all of it is exact integer or exact modular arithmetic, which is why this round checks end to end.

## The certificate, which the bundle does not check

Theorem 11.1 is the sharpest thing in the round:

> `(2^{Q_C} − 3^{L_C}) r_C ≡ B_C (mod M)`

for a modular return loop `C` with length `L_C`, total valuation `Q_C`, code correction `B_C`, and return residue `r_C`. The shipped checker performs the same loop erasure but verifies only the mass lower bound; the certificate appears in no assertion.

It is worth checking because it is not a restatement. It is the accelerated affine identity `2^{Q_C}·V_j = 3^{L_C}·V_i + B_C` — exact integers — read modulo `M` after using `V_i ≡ V_j`. So this gate checks **both**: the integer identity on the segment, and the certificate that follows from it. Over **34,970** loops built from the real orbits: zero violations of either, and zero loops where both sides of the certificate are zero mod `M` and it therefore says nothing.

## Finding 1 — "return loop" names two objects, and the period bounds one of them

Corollary 10.2 counts loops by dividing the linear mass by their length, using "each erased loop has length at most `s_k`". Theorem 11.1 attaches a certificate to a loop. These are not the same loop.

The **erased cycle** is the object the length bound is about: the stack vertices from a residue's first occurrence onwards, all carrying distinct unit residues. There are only `s_k = 2M/3` units, so the bound is immediate. Measured: **0 violations**, longest cycle **13**.

The **orbit segment** is the object the certificate is about: positions `i` to `j` in the actual orbit with `V_i ≡ V_j`. It is what carries an affine identity, because it is contiguous. And it can enclose previously erased loops, so it is not bounded by the period at all: **14,539 of 34,970** exceed `s_k` — 41.6% — the longest running **73** edges, the whole tail. **24,798** (70.9%) differ from their own erased cycle.

Both statements are true of their own object. Applying either bound to the other reads as a violation, which is exactly what happened here: my first version measured segment length against the period and reported 973 violations of a theorem that was not being tested. The fix was to return both lengths and apply each bound to the thing it is about — and to say so, because a reader of Corollary 10.2 and Theorem 11.1 in sequence has no signal that the word changed meaning between them.

## Finding 2 — Theorem 9.1's finite bound is vacuous, and my own check inherited that

The finite loop-mass bound is

> `mass ≥ h + 1 − (b + 2L + 1)·s_k`

where `b` counts `q ≥ 2M` edges and `L` the low-lift vertices. Rebuilt from the construction over 3,826 bridge-precision levels: **0 masses below the bound**, and the bound is **positive on 4 of them**. On the other 3,822 it is negative, and `mass ≥ negative` is not a test. Where it is positive the smallest slack is 21, and it is never attained.

The interesting part is that I did not notice until the drill did. Four planted defects in that section — reading the lift forwards instead of backwards, dropping an endpoint from the deletion rule, counting stack depth from the wrong end, weakening the bound — all came back with the verdict differing but **no failure counter moving**. They changed observations and nothing else, because the only failure counter in the section compared against a bound that discriminates 4 levels in 3,826.

The repair is three checks that are **total**, holding at every level regardless of the bound's sign:

- a clean run contains no low-lift vertex,
- a clean run contains no `q ≥ 2M` edge,
- loop erasure conserves edges: `erased + (residual path − 1) = run length`.

All three read zero, and all four defects are now caught. This is the same lesson as the vacuity counters I have been writing beside published bounds for five rounds — arriving, this time, pointed at my own gate. A bound that cannot discriminate cannot be the only consumer of the code beneath it.

## Finding 3 — the fourth synthetic block shape, and a repair that never runs

`fixed_power_high_lift_algebra`, 10,000 iterations, asserts three things:

```python
eta = min(0.98, max(gamma+0.01, eta))
assert gamma < eta          # arranged by the line above
err_exp = 1-eta+gamma
assert err_exp < 1          # the same inequality, restated
assert C_LOOP > 0           # a constant computed outside the loop
```

The first is arranged one line earlier. The second is algebraically identical to the first. The third is loop-invariant — `C_LOOP = 1 − β/3` never changes. Measured over the same ranges: the two inequalities agreed on all 10,000 samples, and the constant varied on none.

`boundary_alias_no_go_algebra` is a **fourth shape**, distinct from the guarded assertion of RUN-045, the cancelling parameter of RUN-046, and the restated definition of RUN-047:

```python
lhs_log = (1-gamma)*hlog - log(hlog)
if lhs_log <= 0:
    hlog = max(hlog, 10/(1-gamma)); lhs_log = (1-gamma)*hlog - log(hlog)
assert lhs_log > 0
```

The assertion is preceded by a **repair** that fixes any input which would have failed it. So the measurable question is how often the repair fires — and over 10,000 samples at the same ranges it fires **zero** times, smallest left side **0.9389**. The assertion is protected by a branch that is itself unreachable. Four rounds, four shapes; in every case the block is honestly scoped and the count honestly reported, and in every case the issue is what a reader takes `10000` to mean.

## What else this recheck adds

**Theorem 3.1 in the form it is stated in.** The bundle compares the k-suffix's full endpoint representative against `Z mod 3^k`. That is the same *value*, but the theorem's content is that the terms past `j = k` contribute nothing — which is what makes it "boundary locality". Here the truncated sum, the full sum, their agreement, and the divisibility of the tail terms are four separate counters.

**Both halves of Theorem 4.1.** The left inequality is zero total lift plus suffix supercriticality; the right is `a_j ≤ 2` summed. The bundle chains them in one `assert`, so a failure of either reads the same. Both are tight here: the left is attained on 13,493 of 27,337 prefixes and the right on 4,933, with the largest `P_r/r` exactly **2.0**.

**Theorem 5.1's period, checked sharp in both directions.** The bundle verifies uniqueness below `s_k` and at most three labels below `2M`. Neither is a statement that `s_k` is the *right* period: both would hold if the true period were three times longer. So the collision AT `s_k` is a counter (0 residues without one) and so is the attainment of three sheets (all 242 residues carry exactly three). Without those, `ord_M(2)` could be an upper bound rather than the order — which is precisely the error the aliasing argument of A-U.2d.19 turns on.

**The bundle's float loop depth against an exact integer one.** Its per-bridge precision range is `range(1, min(4, int(log(h,3))+1))`, computed with a float logarithm. Measured against the exact largest `e` with `3^e ≤ h`: zero disagreements. It is safe, and now that is a measurement.

## Two things about the bundle worth recording

The constants frontier and the checker report **agree** this round — RUN-047's one-ulp `β` disagreement did not recur, and all three published constants are the correctly rounded double. One report key pair, `linear_clean_loop_mass_constant` and `linear_clean_loop_mass_constant_decimal`, carries the same value under two names.

The source-validation record carries **zero per-file digests** — the seventh consecutive round in which its content has changed shape — and six of the nine files are absent from it entirely, including the checker report, the constants frontier, the ledger and the verification script. `CHECKSUMS.sha256` still pins eight of nine, so nothing is unverifiable; the manifest is carrying what the record dropped, as it has since RUN-044.

<!-- BEGIN GENERATED measured block: python code/src67_emit_report_block.py -->

**The population.** **7136** bridges from **6686** distinct sources (longest tail 73), of which **7136** have zero total lift and **0** do not — the fourth round running in which the positive-lift branch has no finite instance.

**Theorem 3.1, in the form it is stated in.** The boxed statement is a **k-term** sum, and its content is that the terms past `j = k` contribute nothing modulo `3^k`. Over **7136** bridges and **27337** levels: the truncated sum **0** violations, the full sum **0**, the two disagreeing **0**, a tail term not divisible by the modulus **0**, and the bundle's own form — the k-suffix's endpoint representative against `Z mod 3^k` — **0**. Same value, different sentence: the bundle verifies that the suffix determines the residue, not that only the first k terms of the sum do.

**Theorem 4.1, both halves separately.** `P_r <= ceil(beta h) - ceil(beta(h-r)) <= 2r` has a left inequality that is zero total lift plus suffix supercriticality and a right one that is `a_j <= 2` summed; the bundle asserts them in one chained expression, so a failure of either reads the same. Over **27337** prefixes: **0** and **0** violations. Both are tight — the left is **attained 13493** times (49.4%) and the right **4933** — and the largest `P_r / r` seen is exactly **2.0**, so `2r` is reached. A single valuation exceeded `2r` **0** times.

**Theorem 5.1 and Corollary 5.2, checked sharp.** Over **5** precisions: the period disagreeing with `2M/3` **0** times; **29282** transition pairs below the period with **0** label collisions; and **0** residues where no collision occurs AT the period — the sharpness the bundle does not test, and without which a period three times too long would pass. Over **242** sheet checks, **0** residues carried more than three labels and **242** carried exactly three, so the bound is attained on every one; **0** precisions failed to attain it.

**Theorem 6.1's alias budget.** Over **16934** bridge-precision pairs: **0** violations of `B_k s_k <= Q_h`, **0** of the `q >= 2M` form, and **0** total valuations disagreeing with `ceil(beta h)`. **7197** of the pairs actually contain an alias-large edge, and the largest count on one bridge is **28** — so the budget is not bounding an empty set.

**The return loops and Theorem 11.1's certificate.** **34970** loops built from the real orbits across **5652** bridge-precision pairs, total edge mass **233773**. The certificate `(2^{Q_C} - 3^{L_C}) r_C = B_C mod M`: **0** violations. The exact integer identity it is a shadow of: **0**. Loop endpoints not congruent: **0**. Certificates trivially zero on both sides: **0**. The bundle's loop block verifies mass lower bounds only, so the certificate is checked here for the first time.

**"Return loop" names two objects, and the period bounds one of them.** The ERASED CYCLE — the stack vertices from the first occurrence on, all carrying distinct unit residues — is bounded by `s_k = 2M/3` because there are only that many units to be distinct in: **0** violations, longest cycle seen **13**. The ORBIT SEGMENT carrying the certificate is a different thing, because it can enclose previously erased loops: **14539 of 34970** exceed the period (41.6%), longest **73**, and **24798** (70.9%) differ from their own erased cycle at all. Applying either bound to the other object reads as a violation; the certificate holds on all 34970 regardless.

**Theorem 9.1's finite bound is vacuous on almost everything.** Rebuilt from the construction over **2970** bridges, **3826** bridge-precision levels and **1802** clean runs: **0** masses below the bound. But the bound `h + 1 - (b + 2L + 1) s_k` is **positive on 4 of 3826 levels** (0.1%) — everywhere else it is negative and the comparison says nothing. Where it is positive the smallest slack is **21** and it is attained **0** times. So three checks that ARE total were added instead: a clean run must contain no low-lift vertex (**0**) and no `q >= 2M` edge (**0**), and loop erasure must conserve edges, `erased + (path - 1) = run` (**0**). The drill found that gap: four defects in this section moved nothing until those three existed. Total clean mass **6767**; residual paths longer than the period **0**; the bundle's float loop depth disagreeing with the exact integer one **0**.

**Their two synthetic blocks, and a fourth shape.** `fixed_power_high_lift_algebra` runs **10000** iterations and asserts three things: `gamma < eta`, arranged by the `max(gamma+0.01, eta)` on the line above (**0** could have failed); `1-eta+gamma < 1`, which is the same inequality restated (**0** samples where the two differed); and `C_LOOP > 0` on a constant computed outside the loop (**0** samples where it varied). `boundary_alias_no_go_algebra` is the fourth shape this sweep has seen: the assertion is preceded by a **repair branch** that fixes any input that would fail it. Over **10000** samples the repair fired **0** times and **0** would have failed without it — the smallest left side before the repair is **0.9389**, after it **0.9389**. The repair is not merely protective; at these sampling ranges it never runs.

**Their near-full diagnostic rows**, rebuilt: **14** of **14** reproduced, **0** disagreeing `k`, **0** alias bounds, **0** faithful-run bounds, **0** modulus-bracket violations. The two end-to-end trend assertions — the alias fraction falling and the faithful run growing — hold (**0**, **0**), and the rows are not monotone in between, which the bundle's own comment says.

| `log10 h` | `k` | alias bound | alias fraction | faithful run |
| --- | --- | --- | --- | --- |
| 20 | 40 | 19 | 0.4750 | 2 |
| 40 | 81 | 53 | 0.6543 | 1 |
| 60 | 123 | 48 | 0.3902 | 2 |
| 80 | 165 | 44 | 0.2667 | 3 |
| 100 | 207 | 40 | 0.1932 | 5 |
| 120 | 248 | 112 | 0.4516 | 2 |
| 140 | 290 | 102 | 0.3517 | 2 |
| 160 | 332 | 93 | 0.2801 | 3 |
| 180 | 374 | 85 | 0.2273 | 4 |
| 200 | 416 | 78 | 0.1875 | 5 |
| 220 | 458 | 71 | 0.1550 | 6 |
| 240 | 500 | 65 | 0.1300 | 7 |
| 260 | 542 | 59 | 0.1089 | 9 |
| 280 | 583 | 163 | 0.2796 | 3 |

**All twelve published loop examples, rebuilt from the map.** **0** not found in my population, **0** disagreeing `X`, **0** `Z`, **0** lengths, **0** moduli, **0** periods, **0** low-vertex counts, **0** large-edge counts, **0** lower bounds, and **0** masses below their own published bound.

| `y` | `X` | `Z` | `h` | `M` | `s_k` | low vertices | `q >= 2M` | their mass | their bound |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 671 | 1007 | 767 | 13 | 3 | 2 | 9 | 0 | 2 | 0 |
| 671 | 1007 | 767 | 13 | 9 | 6 | 9 | 0 | 1 | 0 |
| 1051 | 1577 | 1067 | 11 | 3 | 2 | 7 | 0 | 4 | 0 |
| 1051 | 1577 | 1067 | 11 | 9 | 6 | 7 | 0 | 4 | 0 |
| 1343 | 2015 | 1615 | 8 | 3 | 2 | 7 | 0 | 1 | 0 |
| 1583 | 2375 | 2287 | 17 | 3 | 2 | 13 | 0 | 1 | 0 |
| 1639 | 2459 | 1663 | 11 | 3 | 2 | 8 | 0 | 1 | 0 |
| 1639 | 2459 | 1663 | 11 | 9 | 6 | 8 | 0 | 1 | 0 |
| 1663 | 2495 | 1687 | 11 | 3 | 2 | 5 | 0 | 5 | 0 |
| 1663 | 2495 | 1687 | 11 | 9 | 6 | 5 | 0 | 5 | 0 |
| 2111 | 3167 | 2287 | 18 | 3 | 2 | 14 | 0 | 1 | 0 |
| 2815 | 4223 | 3383 | 8 | 3 | 2 | 4 | 0 | 3 | 0 |

**Constants.** 3 checked: **0** disagree with both readings of their own formula, 3 are the nearest double, 0 are the float64 chain, 0 brackets could not decide, and the frontier and the report disagree on **0** — RUN-047's finding did not recur. **1** group of report keys carries the same value under two names: `linear_clean_loop_mass_constant`, `linear_clean_loop_mass_constant_decimal`.

| constant | frontier | report | verdict |
| --- | --- | --- | --- |
| `beta` | 1.584962500721156 | 1.584962500721156 | exact |
| `linear_return_loop_mass_constant` | 0.47167916642628127 | 0.47167916642628127 | exact |
| `linear_return_loop_count_coefficient` | 0.707518749639422 | 0.707518749639422 | exact |

**Artifacts.** 9 files, 8 carrying a `CHECKSUMS` digest, **0** mismatches, **0** manifest lines naming a missing file; the only file with no digest anywhere is `CHECKSUMS.sha256`. The source-validation record names **3** files and digests **0** of them, reporting `status = PASS` with **0** issues, `json_parse_ok = True`, `python_compile_ok = True`, and **0** per-file flag sets not fully true. 6 files are absent from it: `CHECKSUMS.sha256`, `Hard_Zeta_AU2d20_checker_report.json`, `Hard_Zeta_AU2d20_constants_frontier.json`, `Hard_Zeta_AU2d20_theorem_ledger.json`, `SOURCE_VALIDATION_AU2d20.json`, `verify_Hard_Zeta_AU2d20_mesoscopic_return_discrepancy.py`.

**Ledger coverage.** The paper lists 14 proved items, 6 open problems and 8 NO-GO headings; the ledger carries 15, 6 and 7, with an `open` key (True). Open items with no trace: none. NO-GO headings with no trace: none. The heuristic deciding those lists has controls at both ends and failed neither (0, 0).

**Their counters beside mine**, keyed on their names rather than mine: 0 of 12 had no counterpart here, 0 are reported as zero, and **12 of 12 are reproduced exactly** from the definition.

| check | theirs | mine |
| --- | --- | --- |
| `finite_local_bridges` | 7136 | 7136 |
| `zero_lift_bridges` | 7136 | 7136 |
| `endpoint_boundary_locality` | 27337 | 27337 |
| `source_boundary_valuation_budget` | 27337 | 27337 |
| `transition_label_faithfulness` | 29282 | 29282 |
| `three_sheet_bound` | 242 | 242 |
| `alias_budget_actual` | 16934 | 16934 |
| `clean_loop_mass_finite` | 3826 | 3826 |
| `clean_loop_cycles` | 1802 | 1802 |
| `near_full_boundary_algebra` | 14 | 14 |
| `fixed_power_high_lift_algebra` | 10000 | 10000 |
| `boundary_alias_no_go_algebra` | 10000 | 10000 |

**Instrument and drill.** 11 instrument self-checks, 0 failed. The mutation drill planted **50** defects: **50** caught by the check they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed.

<!-- END GENERATED measured block -->

## Instrument

Eleven self-checks, each naming a world in which it fails.

One of them was wrong, and it is worth recording because the check caught me rather than the subject. The first version asserted that the residue map `r ↦ (3r+1)2^{−q}` is injective on units. It is not: `3r mod 3^k` is **three-to-one**, collapsing residues that agree mod `3^{k−1}`. I wrote a plausible sentence without naming the world it fails in, which is the discipline this gate is built on, and the instrument reported it on the first run. The mechanism the round actually reads is the other variable — for a fixed source residue, `q ↦ r'` has period exactly `ord_M(2)` — and that is what the instrument checks now, along with the collapsing direction stated correctly, so the false claim is on the record rather than deleted.

The rest: `ceil(βℓ)` both ways round, as at RUN-046 and RUN-047; the order of 2 modulo `3^k` with both maximal proper divisors ruled out; `a_j ≤ 2`, which is what turns the source budget into `2r`; and the loop walker on two hand cases, one with a loop and one without — a walker that always returned a loop would pass the first alone.

## Drill

Fifty defects, one at a time, each planted at a pre-flighted unique anchor, with the gate restored byte for byte after every run. **50 caught, 0 missed, 0 malformed, both controls undisturbed, the gate byte-identical at the end.**

Eight needed re-aiming, and six of those were the finding above: my `clean_mass` section had one failure counter and it compared against a vacuous bound. That is the drill working exactly as intended — the defects were fine, the gate was not.

Of the other two, one was mathematically identical to what it replaced: dropping the modular inverse from `2^{−q}` leaves the **period** unchanged, because `ord(2^{−1}) = ord(2)`, and everything this gate reads about that map is periodic. Re-aimed at base 4, whose order is half, it was caught immediately. The other made the walker's own bookkeeping inconsistent and the gate reported it through the section guard — RUN-046's change still earning its place.

**The run also produced the first infrastructure failure of the sweep.** Mid-drill, Windows returned `OSError: [Errno 22] Invalid argument` on a restore write — an indexer or the just-finished `py_compile` holding the handle for a moment — and the drill died with the gate half-managed. The pristine sidecar recovered it and the gate was **verified byte-identical** before anything else happened, which is the whole reason the sidecar is written before the first plant. But a restore that can die is a restore that can leave a planted defect behind, so every gate write now retries with a short backoff and raises loudly rather than continuing with a mutated file.
