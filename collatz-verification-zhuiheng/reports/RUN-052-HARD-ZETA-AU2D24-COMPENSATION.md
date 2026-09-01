# RUN-052 — Hard-Zeta A-U.2d.24: every counter reproduced, two theorems with none, and two bounds carrying the same spare three

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d24_Binary_Replenishment_Ternary_Reset_Rigidity_v0.1` (source item 71) — 24 sections, ten files.
**Tools:** [`src71_compensation.py`](../code/src71_compensation.py) · [`src71_drill.py`](../code/src71_drill.py) · [`src71_emit_report_block.py`](../code/src71_emit_report_block.py)
**Logs:** [`src71-au2d24.json`](../data/gate-logs/src71-au2d24.json) · [`src71-drill.json`](../data/gate-logs/src71-drill.json)

**Result: the mathematics verifies, and this is the strongest reproduction of the sweep — eleven of eleven counters reproduce exactly, plus their published segment total, because the whole enumeration is deterministic. The round prices the nonzero-defect regions that must perform A-U.2d.23's replenishment, through two compensation depths `c₂ = Q + A′ − A` and `c₃ = L + B − B′` measured against the pure multiplier. Four findings. Theorems 7.1 and 7.2 — the ultrametric alignment laws, on the two largest populations in the round — are asserted inside their validator and counted nowhere, so they appear in no counter. Two assertions in the exclusive branches restate their own hypotheses: `c₃ ≤ 0` IS `B′ ≥ B + L` by the definition of `c₃`, measured over 466,864 comparisons with zero disagreements. Two of the round's boxed inequalities carry the same spare factor of three — the defect barrier's largest ratio is exactly 1/3 and the CRT window's is exactly 1/3, and both sharp forms are attained. And the self-validation record changed shape for the eleventh round running, this time dropping the overall pass flag entirely.**

---

## The round's move

A-U.2d.23 showed a zero-defect return transports valuations at a fixed rate — `ν₂(n′) = ν₂(n) − Q`, `ν₃(n′) = ν₃(n) + L` — consuming a binary reservoir to build a ternary one. If linear temporal mass hides in such resonances, the nonzero-defect regions have to replenish. This round determines what that costs.

For a contiguous path with `x = r + Mn`, `z = s + Mn′`, `n, n′ > 0`, set `A = ν₂(n)`, `A′ = ν₂(n′)`, `B = ν₃(n)`, `B′ = ν₃(n′)` and define the **compensation depths**

> `c₂ := Q + A′ − A`,  `c₃ := L + B − B′`

against the pure multiplier `A′ = A − Q`, `B′ = B + L`, which would give `c₂ = c₃ = 0`. Then `𝔡 = 0` exactly when both vanish; the quadrant `c₂ ≤ 0, c₃ ≤ 0` holds no nonzero defect; and a synchronized event (`c₂ > 0` and `c₃ > 0`) carries an exact primitive cylinder equation `2^{c₂}u′ = 3^{c₃}u + ω` with `gcd(ω, 6) = 1`, confined to a small CRT window.

It is a clean, entirely finite piece of arithmetic, and their enumeration of it is fully deterministic — four moduli, odd sources below 5000, fourteen steps, windows of length at most six. That is why every count reproduces.

## Finding 1 — the alignment laws have no counter

Theorems 7.1 and 7.2 are the round's exact valuation identities:

> `c₂ > 0 ⟹ ν₂(𝔡) = A` and `𝔡/2^A ≡ −3^L n/2^A (mod 2^{c₂})`
> `c₃ > 0 ⟹ ν₃(𝔡) = B′` and `𝔡/3^{B′} ≡ 2^Q n′/3^{B′} (mod 3^{c₃})`

The paper calls them "exact valuation identities, not statistical conditions," and they are what makes the primitive decomposition of Theorem 8.1 possible at all. Their validator asserts both. Nothing increments a counter for either, so neither appears in the shipped report.

The populations are not small — they are the two largest in the round: 219,440 segments with `c₂ > 0` and 217,771 with `c₃ > 0`, against the 216,114 synchronized events that *do* get two counters of their own. Measured here, zero violations of all four statements.

This is the second round running with an uncounted theorem, after A-U.2d.23's Theorem 7.1. The pattern is the same: a claim asserted inside a validator, with the counter attached to something adjacent.

## Finding 2 — two assertions restate their own hypotheses

Their validator ends with:

```python
if c2>0 and c3<=0:
    assert Bp >= Bt+L
if c2<=0 and c3>0:
    assert A-Ap >= Q
```

Both are their own hypotheses written out. `c₃ = L + B − B′`, so `c₃ ≤ 0` **is** `B′ ≥ B + L`; `c₂ = Q + A′ − A`, so `c₂ ≤ 0` **is** `A − A′ ≥ Q`. Neither assertion can fail, whatever the data.

Rather than assert that, both members of each pair are evaluated separately on every segment: **466,864 comparisons, zero disagreements**. The two counters carrying these branches — `binary_exclusive_overcharge` (3,326) and `ternary_exclusive_overdrain` (1,657) — do count a real population, and the segments in them do get Theorem 7.1's genuine check. But the assertion each counter is *named* for is a definition.

## Finding 3 — two boxed inequalities carry the same spare factor of three

Theorem 5.1 is called "the central finite inequality of A-U.2d.24":

> `|𝔡| < 2^Q 3^L`

Measured over all 233,432 segments, the largest value of `|𝔡|/(2^Q 3^L)` is exactly **1/3**. The sharp form `|𝔡| ≤ 2^Q 3^{L−1}` holds everywhere and is **attained 1,213 times**.

Theorem 9.1's CRT window is the same story:

> `|ω|/(2^{c₂}3^{c₃}) < 2^{−A′}3^{−B}`

Largest ratio, again exactly **1/3**; the sharp form `3|ω|2^{A′}3^{B} ≤ 2^{c₂}3^{c₃}` holds and is **attained 261 times**.

Both published bounds are true and loose by the same constant, and in both cases the tight version is reached — so this is not an artefact of a small sample. It cost the drill something to notice: a defect that merely halved the barrier was invisible, and had to be taken to a twenty-seventh before a counter moved.

By contrast Theorem 4.1's affine-correction bound is **attained on 42,602 of 233,432 segments**. The round contains both kinds, and only the tight one reads as tight.

## Finding 4 — the self-validation record, eleventh shape

Every previous round's record has had a `files` map of per-file results and some overall pass flag. This one has neither: `files_checked` is a bare list of names, `json_parse` and `python_compile` are plain booleans, and there is **no `all_pass`, no `overall_pass`, no pass flag of any kind**.

A reader that assumed the old shape would report the flag as `None` — which is exactly how a real `False` becomes invisible, the failure mode RUN-051 caught when the key was renamed. This gate now accepts every shape seen and records which one it found, plus a counter for "no pass flag at all". Digests remain at zero, eleven rounds running.

The bundle also carries a tenth file for the first time — a `build_` script alongside the verifier.

## What this gate adds beyond theirs

* **Both alignment laws, counted**, on 219,440 and 217,771 segments.
* **The sharp forms of Theorems 5.1 and 9.1**, with their attainment counts, so the spare factor of three is a measurement rather than a remark.
* **Two controls, drilled.** Their telescoping identity holds because consecutive blocks share an endpoint, and their quadrant block holds because both terms carry `2^{Q+A′}3^{B+L}`. Each is re-run with exactly that property broken — 427 of 1,184 partitions fail, and 12,069 of 20,000 quadrant draws fail — which shows each assertion has real content that no generated input can exercise. Both controls are themselves drill targets, because a control that stops firing proves nothing.
* **`ν₂`/`ν₃` of zero return `None`.** Theirs raises `ValueError`, which is safer than a sentinel but puts the guard at every call site rather than in the function.

## Standing items

Per the RUN-032 line, the shape drift and the missing digests are findings in this log, not gate failures.

<!-- BEGIN GENERATED measured block: python code/src71_emit_report_block.py -->

**The population.** Their enumeration is fully deterministic — four moduli, odd sources below 5000 not divisible by three, fourteen accelerated steps, windows of length at most six — so it reproduces exactly: **233432** quotient-active segments over **4** moduli from **2415** distinct start states, **0** malformed, longest segment **6**.

**Theorem 4.1, which is attained.** The affine-correction bound `0 < B_P ≤ 2^{Q−L}(3^L − 2^L)` failed **0** times below and **0** above over **233432** segments, and the looser boxed form `< 2^{Q−L}3^L` failed **0**. The upper bound is **reached on 42602 of 233432 segments (18.3%)** — a live, binding estimate.

**Theorem 5.1, which carries a spare factor of three.** The central barrier `|𝔡| < 2^Q 3^L` failed **0** times — but the largest ratio `|𝔡|/(2^Q 3^L)` anywhere in the population is exactly **1/3**. The sharp form `|𝔡| ≤ 2^Q 3^{L−1}` also holds, **0** violations, and is **attained 1213 times**. The published inequality is loose by a factor of three and the tight one is reached; a drill defect that merely halved the bound was invisible and had to be taken to a twenty-seventh before it could bite.

**Theorem 6.1 and Corollary 6.2.** `𝔡 = 0 ⟺ c₂ = c₃ = 0` failed **0** times over **233432** segments (**12335** zero-defect, **221097** nonzero), with **0** zero defects carrying nonzero compensation and **0** the other way. The no-double-deficit corollary failed **0** times. The three nonzero classes are populated: **216114** synchronized, **3326** binary-exclusive, **1657** ternary-exclusive.

**Theorems 7.1 and 7.2, which their report never counts.** The ultrametric alignment laws are asserted inside their validator and incremented nowhere, so they appear in no counter — on the two largest populations of the round. Measured here: binary alignment over **219440** segments with **0** valuation and **0** congruence failures; ternary alignment over **217771** with **0** and **0**. **0** segments had a positive depth alongside a zero defect.

**Theorems 8.1 and 9.1, and the same spare three.** Over **216114** synchronized events the primitive cylinder equation `2^{c₂}u' = 3^{c₃}u + ω` failed **0** times, its two residue forms **0** and **0**, and the coprimality of `u`, `u'`, `ω` failed **0** and **0**. The CRT window failed **0** times — and its largest ratio is exactly **1/3**, the same spare factor the defect barrier carries. The sharp form `3|ω|2^{A'}3^{B} ≤ 2^{c₂}3^{c₃}` holds with **0** violations and is **attained 261 times**. **0** windows sit within a factor of two of failing.

**Theorem 11.1, and two assertions that restate their hypotheses.** The exclusive branches gave **3326** binary-exclusive and **1657** ternary-exclusive events, **0** and **0** violations, and **0** nonzero defects fell outside the trichotomy. But their validator's two exclusive assertions are their own hypotheses written out: by the definitions `c₃ = L + B − B'` and `c₂ = Q + A' − A`, `c₃ ≤ 0` IS `B' ≥ B + L` and `c₂ ≤ 0` IS `A − A' ≥ Q`. Evaluating both members of each pair separately on every segment — **466864** comparisons — they disagreed **0** and **0** times.

**Theorem 12.1, with its construction broken as a control.** Over **2018** partitions covering **7210** blocks the two telescoping sums failed **0** and **0** times, and **0** zero blocks carried nonzero compensation. That is not evidence on its own: the identity holds because consecutive blocks share an endpoint, so `A'ᵢ` and `Aᵢ₊₁` are the same valuation of the same number, and their generator always builds it that way. Re-running with only that property broken — every block's start shifted by one — the same sums failed on **427 of 1184** partitions (binary) and **406** (ternary). The assertion has real content; no generated input can exercise it.

**Their two synthetic blocks, each with a control.** The random-word bound ran **20000** trials: **0** below, **0** above, **0** with valuation under the length, and the upper bound **attained 267 times**. The forbidden-quadrant block ran **20000** trials with **0** divisibility and **0** size violations (**8** of them landing on a zero defect) — but in that quadrant both terms carry `2^{Q+A'} 3^{B+L}`, so the divisibility is a consequence of how the inputs are built. Dropping only the quadrant constraint and regenerating: **12069 of 20000** divisibility failures and **249** size failures. The arithmetic is real and the generator cannot violate it.

**The published rows.** **8** synchronized and **8** exclusive rows recomputed from their own fields: **0** depth fields disagreeing, **0** quotient-identity failures, **0** barrier failures, **0** rows whose class disagrees with their own depths.

**The constants.** **4** checked, **1** exact to the last bit, **3** matching the float64 chain rather than the nearest double, **0** disagreeing with both, **0** undecided, **0** missing, **0** where frontier and report disagree. Cross-read, **2** frontier constants are never computed by the checker: `beta_minus_1`, `two_minus_beta`.

**Their eleven counters.** **11** reproduce exactly — the strongest reproduction of the sweep, because the whole enumeration is deterministic. **1** is covered by a different population (their partitions are drawn inside the orbit loop, mine from a separate sampler). **0** of their checks are covered by nothing here, and **0** report zero. Two theorems — 7.1 and 7.2 — have no counter of theirs to compare against at all.

**The bundle as shipped.** **10** files — one more than every previous round, a `build_` script joining the verifier — **9** digests listed, **0** mismatches, **0** checksum lines naming a missing file, and `CHECKSUMS.sha256` with no digest anywhere. The self-validation record changed shape for the eleventh round running: it now names files as a bare list rather than per-file results (**0** per-file entries, **0** with a digest), its `json_parse` and `python_compile` are plain booleans instead of records, and **it carries no overall pass flag at all** — `all_pass` and `overall_pass` are both gone. Its top-level booleans are all true (**0** not true). `CHECKSUMS.sha256`, `SOURCE_VALIDATION_AU2d24.json` absent from it entirely. Against the paper, the ledger lists **16** proved items to the paper's **16**, **6** open to **6**, and **8** no-go entries to the paper's **8** headings; **0** open items and **1** no-go headings have no ledger counterpart. The coverage heuristic passed both its controls.

**The drill.** The instrument self-tests **8** properties before the gate runs, **0** of them failing. **38** defects were planted one at a time: **38** caught by the counter they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed. Six aim at non-vacuity entries, two of them at this round's own controls — a control that stops firing proves nothing, so it is drilled like everything else.

<!-- END GENERATED measured block -->

## Verdict

Every theorem I can reach independently holds, and the deterministic enumeration means the agreement is counter-for-counter rather than approximate. The four findings are about two theorems their report never mentions, two assertions that restate definitions, two bounds looser than they read, and a validation record that has now changed shape eleven times. None contradicts a result.

Next: item 72, `A-U.2d.25 — Primitive Defect Cylinder / Compensation-Seesaw Discrepancy Rigidity`.
