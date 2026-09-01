# RUN-054 — Hard-Zeta A-U.2d.26: a withdrawn constant, a certificate rebuilt from exact rationals, and a PASS for a file that isn't there

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d26_Primitive_Unit_Oscillation_Critical_Slope_Synchronization_Rigidity_v0.1` (source item 73 — the last of the sweep) — 16 sections, ten files.
**Tools:** [`src73_unit_sync.py`](../code/src73_unit_sync.py) · [`src73_drill.py`](../code/src73_drill.py) · [`src73_drill_defects.py`](../code/src73_drill_defects.py) · [`src73_emit_report_block.py`](../code/src73_emit_report_block.py)
**Logs:** [`src73-au2d26.json`](../data/gate-logs/src73-au2d26.json) · [`src73-drill.json`](../data/gate-logs/src73-drill.json)

**Result: the mathematics verifies, and eleven of the twelve compared figures reproduce exactly. This round withdraws `ρ★ = 4.1164` — the numerical Diophantine input carried since A-U.2d.3 and cited in eight of my earlier reports — on the grounds that the Wu–Wang theorem behind it is about `log 3`, not about `β = log 3/log 2`, and re-derives everything from finite continued fractions of β instead. Three findings. RUN-029 raised this exact hypothesis and REFUTED it, on a secondary source that attributes the same bound to `log2/log3`; the two readings cannot both be right, and no recomputation gate can settle which is — the arithmetic was checkable and I checked it, the attribution never was. Their replacement route is checkable, and is verified here in exact rationals rather than their 90-digit floats: 41 certified partial quotients against the 12 they publish, and the separation decided by integer cross-multiplication over 20,000 values with a tightest ratio of 1.047. And the self-validation record attests `PASS` for `build_AU2d26.py`, a file the bundle does not contain and CHECKSUMS does not list.**

---

## The round's move, and the withdrawal

A-U.2d.25 left `rho_star_inherited: 4.1164` in its frontier as a four-decimal literal with no closed form — which RUN-053 flagged one round ago. This round ships a `PROVENANCE_REPAIR` note that goes further:

> A fresh source audit found that the previously cited Wu–Wang 2014 theorem is a theorem about the irrationality measure of `log 3`, not directly about `β = log3/log2`. Therefore the numerical Hard-Zeta input `ρ★ = 4.1164` must not be presented as directly certified by Wu–Wang for `‖qβ‖`.

Earlier exponents that depend on it become "provenance-pending / conditional". The round then makes itself independent of the disputed value by replacing the global irrationality exponent with a **finite** statement about β's own continued fraction:

> `M_β(D) := max{a_{n+1} : q_n ≤ D}`,  `Q_D := M_β(D) + 2`,  and for `1 ≤ b ≤ D`, `|a − βb| > 1/(Q_D b)`.

That is a directly computable claim, and it is the right kind of repair: it replaces a citation with an arithmetic.

## Finding 1 — my own earlier report reached the opposite conclusion

RUN-029, verifying A-U.2d.3, raised exactly this hypothesis and recorded it as refuted:

> **And a specific, quantitative hypothesis about the Diophantine input was raised and refuted.** The value `4.1164` is close to `μ(ln 3) ≤ 5.1163051 − 1`, a published bound on a *different* number, and the round would collapse quantitatively if that were the source… Fan–Queffélec–Queffélec's own text settles it — they give Rhin's bound for `α = log2/log3` as `ρ ≤ 7.616` and state that Wang and Wu improved it to `ρ ≤ 4.11633052`, for that same `α`.

The suspicion was the same one the authors' audit now confirms. My refutation rested on a secondary source's characterisation of which number the bound is about. Their audit says it is `log 3`. Both cannot be right, and I cannot settle it from here: **the arithmetic was checkable and I checked it** — `4.1164 > 4.11633052` by `1737/25000000`, as exact rationals, and the whole exponent chain downstream — **but which theorem is about which number is a claim about the literature, and no recomputation gate can decide that.**

Note also that if the attribution were to `α = log2/log3`, the transfer to `β = log3/log2` would be legitimate, since a number and its reciprocal have the same irrationality measure. So the disagreement is narrow and specific: is Wu–Wang's theorem about `ln 3`, or about `log2/log3`? That question is answered by reading Wu–Wang, not by running anything.

What this arm can say precisely: eight of my reports (RUN-029, 032, 036, 040, 041, 042, 043, 044) carry exponents derived from `ρ★`, and ten archived gate logs mention it. Every one of them verified the *arithmetic* of the chain and none of them certified the *source*. RUN-029 says so in as many words — "It does not certify `ρ★ = 4.1164`". That limit was stated at the time, and it is the limit that matters now.

## Finding 2 — their replacement route, verified in exact rationals

Their checker computes β's continued fraction with `mpmath` at 90 decimal places. A float, however long, is evidence about a float.

This gate takes the terms from the certified rational bracket `beta_tight()` instead: a term is emitted only while both endpoints of the bracket agree on it, and a term shared by both ends is a term of every number in between — hence of β. No floating point is involved, and the certification is checked directly by recomputing each endpoint's own continued fraction and requiring the emitted prefix to be common to both.

That yields **41 certified partial quotients** against the **12** they publish, agreeing on all 12. From them, `M_β(20000) = 23` and `Q_D = 25`. The separation `|a − βb| > 1/(Q_D b)` is then decided by integer cross-multiplication over all 20,000 values of `b`: **0 violations, 0 undecidable**, and the bound is nearly attained — the tightest `|a − βb|·Q_D·b` is **1.047**.

So the replacement route holds, and holds with exact certification rather than numerical confidence. Given that this round exists to remove a disputed numerical input, that seemed the right place to spend the effort.

## Finding 3 — a `PASS` for a file that is not in the bundle

The self-validation record lists nine files, each with `["PASS"]`. One of them is `build_AU2d26.py`. The bundle contains ten files and that is not among them; `CHECKSUMS.sha256` does not list it either.

So the record attests a passing check on a file nothing else in the bundle mentions. That is different in kind from the twelve rounds of shape drift and missing digests already logged: those were things the record failed to say. This is something it says that is not so.

It is reported in this gate's own `artifact_defects` field rather than as a gate failure. `passed` has meant *the mathematics reproduces* across thirty-one reports, and this defect is not in the mathematics — but burying it among the observations would hide it, so it gets a top-level field of its own. **No previous gate in this sweep had a counter for this direction**: every one checked which present files the record omits, and none checked which absent files it names.

## Three more restatements, measured

* **The synchronized reservoir toll** asserts `c₃ ≥ 1`, `B ≥ c₃ − 1`, `n ≥ 3^{c₃−1}` on all 100,449 synchronized edges. All three are consequences of the definitions: `c₃ > 0` is the branch and `c₃` is an integer; `c₃ = 1 + B − B′` makes the second exactly `B′ ≥ 0`, which a 3-adic valuation always is; and `3^B | n` gives the third. Over 200,898 predicate comparisons, zero disagreements.
* **The exponent block** reads `if not (lhs >= 1 − 1e-12): assert lhs < 1 + 1e-12` — the branch is strictly stronger than the assertion. All 1,745 samples that reach it have it implied by its own guard. This is the shape RUN-052 named, appearing again in the closing round.
* **The variation-transfer bound** follows term by term from Theorem 3.1 plus the reverse triangle inequality; measured per term over 140,178 edges, zero negative slack, so the summed form could not have failed.

Two of their blocks also carry two counters each — the CF masters, and the monotone-run/coarea pair whose assertions sit inside a guard the counters are outside.

## What this gate adds beyond theirs

* **β's continued fraction certified from a rational bracket**, and the separation lemma decided in integers.
* **Theorem 3.1 as an exact `Fraction`**, where they allow `2e-11` for an error whose largest observed value is of order `1e-15` — an allowance 11,258 times the error it absorbs, on a statement that needs none.
* **The three definitional clauses measured against the facts they reduce to**, rather than asserted to be tautologies.
* **A control for the variation window** — one edge's unit ratio replaced by an unrelated value makes it fail on 2,029 of 2,029 windows.
* **The forward direction of the validation check**: which files the record names that the bundle does not have.

One drill note worth keeping: a defect that appended an *uncertified* continued-fraction term was invisible, and correctly so — when the bracket cannot decide a term, the term may still be the right one. Uncertified is not the same as wrong, and only a term that is actually wrong breaks the property the instrument tests.

## Standing items

Thirteen rounds without a digest in the self-validation record. Per the RUN-032 line, that and the ledger's dropped no-go key are findings in this log, not gate failures.

<!-- BEGIN GENERATED measured block: python code/src73_emit_report_block.py -->

**The population.** Deterministic again — five moduli, odd sources below 9000 not divisible by three, thirteen edges per orbit — so it reproduces exactly: **140178** quotient-active edges from **4587** start states, **0** malformed, **0** unclassified. By type: **30192** zero, **100449** synchronized, **5541** binary-exclusive, **3996** ternary-exclusive.

**Theorem 3.1's transport identity, exact.** They assert it in float64 with a `2e-11` tolerance. Checked as an exact `Fraction` on all **140178** edges: **0** violations. The largest float error their tolerance was covering is of order **1e-15** — their allowance is **11258 times** the error it needed to absorb, on a statement that is exact in rationals and needs no allowance at all. At their own tolerance, **0** violations.

**Their synchronized reservoir toll: three clauses, all definitional.** Over **100449** synchronized edges the three asserted clauses — `c₃ ≥ 1`, `B ≥ c₃ − 1`, `n ≥ 3^{c₃−1}` — failed **0**, **0** and **0** times. None of them can fail. `c₃ > 0` is the branch condition and `c₃` is an integer, so the first restates it; `c₃ = 1 + B − B′` makes the second exactly `B′ ≥ 0`, which a 3-adic valuation always is (**0** negative in the whole population); and `3^B | n` with the second gives the third. Measured rather than asserted: over **200898** predicate comparisons, the depth clause disagreed with `B′ ≥ 0` **0** times and the `c₃` clause disagreed with its own branch **0** times. Largest synchronized `c₃` seen: **7**.

**The variation-transfer bound, implied term by term.** Their window check sums three lists and compares totals. By Theorem 3.1, `|ΔU| − |c₂ − βc₃|` is bounded by `|ε|` on each single edge by the reverse triangle inequality, so the summed form follows. Measured per term over **140178** edges: **0** with negative slack. Over **2354** windows the aggregate failed **0** times. The control — one edge's unit ratio replaced by an unrelated value — makes it fail on **2029 of 2029** windows, so the assertion has content that their construction cannot exercise.

**Lemma 7.1, certified in exact rationals.** Their checker takes β's continued fraction from a 90-digit float. Here the terms come from the certified rational bracket: a term is emitted only while both endpoints agree on it, so every emitted term is a term of every number in the interval, hence of β. That yields **41** certified partial quotients against the **12** they publish, giving `M_β(D) = 23` and `Q_D = 25` at `D = 20000`, with the largest convergent denominator at or below `D` being **15601**. The separation `|a − βb| > 1/(Q_D b)` was then decided by integer cross-multiplication — no floating point anywhere — over **20000** values of `b`: **0** violations and **0** values the bracket could not decide. The bound is nearly attained: the tightest `|a − βb|·Q_D·b` is **1.047**.

**Theorems 8.1 and 9.1, and two blocks counted twice.** The two CF master inequalities held over **12000** batches: **0** and **0** violations. They come from one block that increments **2** counters. The monotone-run and coarea lemmas likewise share one block incrementing **2** counters, and their assertions sit inside a guard the counters are outside: over **12000** trials the guard opened **12000** times. Violations: **0** monotone-run, **0** coarea identity, **0** coarea crossing.

**Their exponent block asserts what its own guard already gives.** The code reads `if not (lhs >= 1 − 1e-12): assert lhs < 1 + 1e-12`. The branch condition is strictly stronger than the assertion, so the assertion cannot fail. Over **20000** trials, **1745** samples reached the assert and **1745** of them had it implied by the guard, with **0** not implied. The round's real claim — that the master bound forces the half-space `α + χ + 2μ ≥ 1` — is scored separately on the **18255** samples inside it: **0** violations.

**The withdrawn exponent.** The round ships a provenance-repair note (**present: 1**) withdrawing `ρ★ = 4.1164`, and its frontier declares the value unused (**1**). Checked: the numeral appears **0** times in the frontier, **1** in the checker report, and **2** times in the paper outside its own NO-GO section — all in the discussion of the withdrawal, not as an input. The oscillation threshold is the stated one-half (**1**), and β itself is **exact** against the certified bracket.

**The published rows.** **8** rows in **1** groups recomputed from their own fields: **0** quotient-identity failures, **0** depth fields disagreeing, **0** unit fields disagreeing, **0** rows not actually synchronized.

**Their nine counters.** **11** of the twelve compared figures reproduce exactly, including the three population totals they publish. **5** are covered by a different population: their window sampler and their two doubled blocks. **0** of their checks are covered by nothing here, and **0** report zero.

**The bundle as shipped, and one false attestation.** **10** files, **9** digests listed, **0** mismatches, **0** checksum lines naming a missing file, and `CHECKSUMS.sha256` with no digest anywhere — thirteen rounds without a digest in the validation record (**9** per-file entries, **0** with one). Its pass flag is the string `PASS` under `status`. **But the record attests `PASS` for a file the bundle does not contain**: `build_AU2d26.py`. That file is absent from the directory and from `CHECKSUMS.sha256` too, so nothing in the bundle backs the attestation. It is reported in this gate's own `artifact_defects` field rather than as a failure, because `passed` has meant *the mathematics reproduces* for thirty-one reports and this defect is not in the mathematics. Against the paper, the ledger lists **13** proved items to **13**, **8** open to **7**, and **0** no-go entries to the paper's **5** headings (no no-go key at all: **1**), with **2** headings having no counterpart. The coverage heuristic passed both controls.

**The drill.** The instrument self-tests **11** properties before the gate runs, **0** of them failing. **37** defects were planted one at a time: **37** caught by the counter they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the verdict unchanged. Six aim at non-vacuity entries and one at the artifact-defect field, which already reports a real defect — so that one has to make it report MORE, since from a known state only a rise is visible.

<!-- END GENERATED measured block -->

## Verdict

Every theorem I can reach independently holds, and the round's own repair — replacing a disputed citation with a finite, computable certificate — is verified here more strictly than it was shipped. The three findings are a provenance conflict this arm cannot resolve and should not pretend to, a replacement route that survives exact certification, and one attestation that is simply not backed by anything in the bundle.

**This is item 73 of 73. The source sweep is complete.**
