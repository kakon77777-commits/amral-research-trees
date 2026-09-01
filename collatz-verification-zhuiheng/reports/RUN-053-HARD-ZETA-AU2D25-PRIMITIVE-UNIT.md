# RUN-053 — Hard-Zeta A-U.2d.25: a bound that is finally sharp, and three synthetic blocks that restate their own setup

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d25_Primitive_Defect_Cylinder_Compensation_Seesaw_Discrepancy_Rigidity_v0.1` (source item 72) — 18 sections, nine files.
**Tools:** [`src72_primitive_unit.py`](../code/src72_primitive_unit.py) · [`src72_drill.py`](../code/src72_drill.py) · [`src72_drill_defects.py`](../code/src72_drill_defects.py) · [`src72_emit_report_block.py`](../code/src72_emit_report_block.py)
**Logs:** [`src72-au2d25.json`](../data/gate-logs/src72-au2d25.json) · [`src72-drill.json`](../data/gate-logs/src72-drill.json)

**Result: the mathematics verifies, and thirteen of sixteen counters reproduce exactly along with their published edge total. The round specialises A-U.2d.24's block bound to a single edge and gets a strip that is sharp at BOTH ends — `-2^q < d < 3`, with `d = 2` attained 9,169 times and the lower end reached to within 126/128 — which is the opposite of last round, where two boxed inequalities each carried a spare factor of three. Three findings. All three synthetic blocks restate their own construction: each `assert` re-derives the line immediately above it, and each is defused here by breaking exactly that line (26,677, 20,000 and 15,253 failures respectively). Their window triangle bound is implied edge by edge — the summed form adds nothing to a per-term inequality that already holds 17,206 times over. And the self-validation record changed shape a twelfth time: its pass flag is now the string `PASS`, and it names no files at all, so nothing records what was validated; the theorem ledger has likewise dropped its no-go key against the paper's nine NO-GO headings.**

---

## The round's move

RUN-052 measured A-U.2d.24's central inequality `|𝔡| < 2^Q 3^L` as loose by exactly a factor of three. This round specialises to one edge and replaces it with

> `-2^q < d < 3`,  and  `d > 0 ⟹ d ∈ {1, 2}`

which is a much stronger statement and, measured, a sharp one. It then collapses the three compensation types into exact arithmetic gates — a ternary-exclusive edge is *atomic* (`q = 1`, `d = 2`, `A′ = B′ = 0`), a binary-exclusive edge is necessarily negative with `q ≥ 2` and a reservoir condition, and a synchronized edge falls into one of two normal forms — and gives the primitive unit an exact transport law

> `u′/u = 2^{−c₂} 3^{c₃} (1 + d/(3n))`.

That last identity is the round's real content: the compensation slope `c₂ − βc₃` *is* the negative primitive-unit log drift, up to an exact relative-defect correction. Everything downstream is priced from it.

## The strip is sharp, and that is worth saying

Measured over all 187,769 quotient-active edges:

* the upper end `d < 3` is **attained 9,169 times** at `d = 2`;
* the largest `−d/2^q` anywhere is **126/128** — the lower end is reached to within one part in 128.

Two rounds ago the analogous bounds were loose by a constant. Here both ends are essentially touched, and the drill felt the difference: last round a defect had to tighten a bound by a factor of twenty-seven before any counter moved, while here pulling either end in by one unit is caught immediately.

## Finding 1 — all three synthetic blocks restate their own setup

Three of the sixteen counters come from generated inputs. Each one's `assert` re-derives the line above it:

```python
up = num // (2**c2)                       # under `num % 2**c2 == 0`
assert (2**c2)*up == (3**c3)*u + omega    # ... i.e. integer division

up = (2**(-c2))*(3**c3)*u + 1
assert up > u                             # a positive multiple of u, plus one

ub = xi + (2**c2b)*(3**g)*upb
assert ub > upb                           # xi >= 1 and the multiplier >= 2
```

Saying so is an assertion; measuring it is not. Each block was rebuilt with exactly the property its assert depends on removed, and nothing else changed:

| block | as shipped | with its construction broken |
| --- | ---: | ---: |
| synchronized (divisibility test dropped) | 0 failures | **26,677** |
| ternary-exclusive (multiplier removed) | 0 failures | **20,000** |
| binary-exclusive (pump removed) | 0 failures | **15,253** |

The arithmetic in each is real. What no generated input can do is violate it, so the 41,594 checks these three counters report are a description of the generator rather than a test of the theorems they sit under. Both real gate populations for the same theorems — 4,310 atomic resets and 9,527 pumps drawn from actual orbits — are checked separately here and hold.

## Finding 2 — the window triangle bound is implied edge by edge

The window check ends with

```python
assert sum(dU) + sum(abs(x) for x in eps) + 1e-10 >= sum(imb)
```

where `dU_i = |log₂(u′/u)|`, `eps_i = log₂(1 + d/(3n))`, `imb_i = |c₂ − βc₃|`. But Theorem 5.1 says `log₂(u′/u) = βc₃ − c₂ + ε` exactly, so per edge

> `|c₂ − βc₃| = |log₂(u′/u) − ε| ≤ |log₂(u′/u)| + |ε|`

by the triangle inequality alone. The summed form is a sum of these, and a sum of non-negative slacks cannot go negative however it is grouped. Measured per term across 17,206 edges: **zero terms with negative slack**, so the aggregate assertion could not have failed either.

The bound is a true consequence of Theorem 5.1, which is itself checked exactly in rationals on every one of the 187,769 edges. It is the third counter of the round that reports a restatement.

## Finding 3 — the validation record's twelfth shape, and a ledger with no no-go key

Eleven previous rounds have each carried a differently-shaped self-validation record. This one:

* the pass flag is the **string** `"PASS"` under the key `status` — a reader looking only for boolean `all_pass`/`overall_pass` returns `None`, and a real `"FAIL"` would vanish with it;
* there is **no file list of any kind** — no `files` map, no `files_checked` array — so nothing records which files were validated;
* digests remain at zero, twelve rounds running.

Separately, the theorem ledger has **no no-go key at all** this round, against the paper's nine NO-GO headings, three of which (12.5, 12.8, 12.9) have no textual counterpart anywhere in it. The proved list matches exactly, 16 to 16.

## What this gate adds beyond theirs

* **Two float-guarded reservoir bounds in exact integers.** `A + β(B+1) < q` is `2^A 3^{B+1} < 2^q` and `A + βB′ < q` is `2^A 3^{B′} < 2^q`. Over 65,429 reservoir tests both routes agree, so their `1e-12` fudge decides nothing.
* **Both ends of the strip scored for attainment**, not just for violation.
* **Every by-construction block given a control** — the three synthetic ones above, plus both window telescopings, which fail on 2,581 and 1,938 of 2,599 windows once one interior edge is dropped.
* **Corollary 5.3's seesaw as a signed claim**: the unit rises on every ternary-exclusive edge and falls on every binary-exclusive one, checked over 13,837 exclusive edges.
* **`ν₂`/`ν₃` of zero return `None`.** Theirs raises, which is safe but puts the guard at every call site.

## Standing items

Per the RUN-032 line, the shape drift, the missing digests and the ledger's dropped no-go key are findings in this log, not gate failures.

<!-- BEGIN GENERATED measured block: python code/src72_emit_report_block.py -->

**The population.** Their enumeration is deterministic — five moduli, odd sources below 12000 not divisible by three, eleven edges per orbit — so it reproduces exactly: **187769** quotient-active edges from **6034** distinct start states over **5** moduli, **0** malformed.

**Theorem 3.1, sharp at both ends.** The one-step strip `-2^q < d < 3` failed **0** times above and **0** below over **187769** edges, and `d > 0 ⟹ d ∈ {1,2}` failed **0** times on **80047** positive defects. Both ends are close: the upper end is **attained 9169 times** at `d = 2`, and the largest `-d/2^q` anywhere is **63/64**. Against the previous round's block bound specialised to one edge, **0** violations. **65429** defects are negative and **42293** are zero.

**The compensation gates, all four populated.** **42293** zero, **131639** synchronized (**75737** positive, **55902** negative), **9527** binary-exclusive, **4310** ternary-exclusive, **0** unclassified. Theorem 4.1's atomic reset: **0** defects not 2, **0** valuations not 1, **0** wrong output depths, **0** outputs not coprime to six, **0** unit-formula failures, **0** units not increasing. Theorem 4.2's pump: **0** non-negative defects, **0** valuations below two, **0** ternary depths not deeper, **0** wrong defect valuations, **0** bad `ξ`, **0** unit-formula failures, **0** units not decreasing. Theorem 4.3's normal forms: **0** wrong valuations, **0** non-coprime `ω`, **0** cylinder failures, **0** positive normal-form failures, **0** non-negative `ω` on the negative side.

**Two float-guarded reservoir bounds, in exact integers.** Their checker writes `A + BETA*(B+1) < q + 1e-12` and `A + BETA*Bp < q + 1e-12`; under `2^{βm} = 3^m` these are `2^A 3^{B+1} < 2^q` and `2^A 3^{Bp} < 2^q`. Over **65429** reservoir tests the exact forms failed **0** and **0** times, and the two routes disagreed **0** times — so their `1e-12` fudge decides nothing here.

**Theorem 5.1, exact in rationals.** `u'/u = 2^{-c₂}3^{c₃}(1 + d/(3n))` was checked as an exact `Fraction` on all **187769** edges: **0** violations. Corollary 5.2 (zero defect preserves the unit) failed **0** times, and Corollary 5.3's seesaw — the unit rises on every ternary-exclusive edge and falls on every binary-exclusive one — failed **0** times over **13837** exclusive edges.

**Theorem 6.1's window products, with the chain broken as a control.** Over **3006** windows covering **17206** edges the quotient correction product failed **0** times and the unit transport **0**. Both hold because consecutive edges chain, and their generator always builds them that way — so each was re-run with one interior edge dropped: **2581 of 2599** broken windows failed the correction product and **1938** failed the unit transport. The assertions have content; no generated input can exercise them.

**Their triangle bound is implied edge by edge.** The window assertion sums three lists and compares the totals — but by Theorem 5.1, `|c₂ − βc₃|` is `|log₂(u'/u) − ε|`, so each term already satisfies `|ΔU| + |ε| ≥ |c₂ − βc₃|`. Measured per term over **17206** edges: **0** with negative slack, and **0** aggregate violations. A sum of non-negative terms cannot go negative however it is grouped, so the summed form adds nothing to the per-edge one.

**Their three synthetic blocks, each with its construction broken.** The synchronized block draws **30000** times and keeps **1594** constructions, whose equation failed **0** times — but `u'` is *defined* as `num // 2^{c₂}` under a divisibility test, so the assertion restates integer division. Dropping only that test: **26677** failures. The ternary-exclusive block ran **20000** trials with **0** failures, where `u'` is built as a multiple of `u` plus one; removing the multiplier: **20000** failures. The binary-exclusive block ran **20000** trials with **0** failures, where `u` is built as `ξ` plus a multiple of `u'`; removing the pump: **15253** failures. All three assertions restate the line above them.

**The published rows.** **30** rows across **5** example groups recomputed from their own fields: **0** quotient-identity failures, **0** depth fields disagreeing, **0** unit fields disagreeing, **0** strip violations, **0** rows whose group name disagrees with their own defect sign.

**The constants.** **4** checked, **1** exact to the last bit, **3** matching the float64 chain rather than the nearest double, **0** disagreeing with both, **0** undecided, **0** missing, **0** where frontier and report disagree. **1** frontier value has no closed form to check against here — `rho_star_inherited`, carried as a four-decimal literal inherited from an earlier round.

**Their sixteen counters.** **13** reproduce exactly. **4** are covered by a different population — their three window counters come from partitions drawn inside the orbit loop, and their synchronized synthetic block draws from an RNG stream shared with that loop, so no standalone reimplementation can match those integers. **0** of their checks are covered by nothing here, and **0** report zero.

**The bundle as shipped.** **9** files, **8** digests listed, **0** mismatches, **0** checksum lines naming a missing file, and `CHECKSUMS.sha256` with no digest anywhere. The self-validation record changed shape for the twelfth round running: its pass flag is now the STRING `PASS` under the key `status`, it lists **0** problems, and it names **no files at all** — so nothing records which files were validated (**0** per-file entries, **0** with a digest). Against the paper, the ledger lists **16** proved items to the paper's **16** and **6** open to **5**, but **carries no no-go key at all** against the paper's **9** NO-GO headings, **3** of which have no textual counterpart anywhere in it. The coverage heuristic passed both its controls.

**The drill.** The instrument self-tests **7** properties before the gate runs, **0** of them failing. **39** defects were planted one at a time: **39** caught by the counter they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed. Seven aim at non-vacuity entries, five of them at this round's own controls.

<!-- END GENERATED measured block -->

## Verdict

Every theorem I can reach independently holds, and the round's central bound is the sharpest of the sweep so far. The three findings are about three counters that describe their generator rather than test a theorem, one that restates a consequence already checked exactly, and two artifacts that have quietly stopped recording what they used to.

Next: item 73, `A-U.2d.26 — Primitive-Unit Oscillation / Critical-Slope Synchronization Rigidity` — the last of the sweep.
