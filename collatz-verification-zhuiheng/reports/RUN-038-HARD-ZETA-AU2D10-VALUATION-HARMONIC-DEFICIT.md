# RUN-038 — Hard-Zeta A-U.2d.10: the bridge the previous round refused to build, a countermodel that checks out against its own closed forms, and a ledger that is finer than its paper

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d10_Valuation_Class_Harmonic_Deficit_Rigidity_bundle_v0.1.zip` (source item 57) — 24 sections. Ships a checker, its report, a constants frontier, a theorem ledger, a `CHECKSUMS.sha256` and a source-validation record.
**Tools:** [`src57_valuation_harmonic_deficit.py`](../code/src57_valuation_harmonic_deficit.py) · [`src57_drill.py`](../code/src57_drill.py) · [`src57_emit_report_block.py`](../code/src57_emit_report_block.py)
**Logs:** [`src57-au2d10.json`](../data/gate-logs/src57-au2d10.json) · [`src57-drill.json`](../data/gate-logs/src57-drill.json)

**Result: A-U.2d.9 ended by refusing to turn its diameter gain into a harmonic one and named what was missing — a value-order bridge. This round supplies one, and it is again a single exact edge identity, which telescopes. The product exponent moves `1/9 → 4/45`. Everything decidable holds: the identity on 70,810 edges, the telescope and the two harmonic capacities on 68,311 segments, the mod-9 target-cost law on every edge, and Theorem 15.1's span bound on all 27,345 prefixes that meet its premise — which, as at A-U.2d.9, is what a first-crossing interval already is. The round also bounds itself with a countermodel, and that countermodel is internally consistent with its own closed forms to three sizes. Two observations: the rounding chain recurs with its root drifting this time, and the theorem ledger is for once *finer* than the paper's own list rather than lossier.**

---

## The bridge, and why it is one line again

A-U.2d.9 proved that the realized state set of a proper prefix has a stretched
diameter, then declined to convert that into a product bound, saying so
explicitly: the gain is about the diameter, not about where in value-order the
mass sits, and promoting one to the other needs a theorem nobody had.

The bridge turns out to be the edge equation itself:

> `1/Y_j − 1/Y_{j+1} = (3 − 2^q)/(3Y_j) + 1/(3Y_j Y_{j+1})`

Multiply by three and sum, and the left side telescopes:

> `Σ (2^{q_{j+1}} − 3)/Y_j = −3/y + 3/z + C_cross`

That is exact, unconditional, and it couples each edge's **valuation** to the
**reciprocal weight of its source** — which is precisely value-order
information. Large reciprocal mass in expensive valuation classes has to be paid
for out of the cheap `q = 1` class. Bound the cheap classes' harmonic capacity
and the product exponent falls from `1/9` to `4/45`, with a polynomial deficit
`η = 1/45` against A-U.2d.9's own envelope.

The exponents are exactly rational and check out as such: `4/45`, `1/45 = 1/9 −
4/45`, and the constant `289/70` decomposes exactly as
`(6/5)(2) + (4/5)(2) + (1/5)(9/14)`.

## What is testable here, and what is not

Three different kinds of premise appear in this round and the gate keeps them
apart.

**Unconditional.** The identity and the telescope hold on every edge and every
segment, with no hypothesis at all. So do the mod-9 target-cost law, the
`q = 1` and `q = 2` harmonic capacities, and the total reciprocal-mass bound of
Theorem 7.1 — none of these needs the orbit to survive.

**Conditional and unattainable.** Theorem 4.1 is the telescope plus `z > y`, and
Lemma 5.1 needs every state *including the endpoint* at or above the source.
Neither is met by a single real segment, because a first-crossing endpoint is by
construction the place the slack drops. Both were measured, and applied nowhere.
What can still be checked is that Theorem 4.1 **is** the telescope plus that
premise — the two are equivalent on all 68,311 segments, which is universal
algebra and holds.

**Conditional and met.** Theorem 15.1's premise is first-crossing subcriticality
`Σq_j < βm`, which is what a first-crossing interval *is*, decidable as the
integer comparison `2^Q < 3^m`. Every prefix satisfies it, so the span theorem
was genuinely tested — on all 27,345 of them — and holds. Its ingredients were
checked rather than accepted: the mod-9 cost table was **rederived** from
`2^q m ≡ 4 or 7 (mod 9)` instead of transcribed and trusted, and the class
capacity `N ≤ W/9 + 2` was enumerated.

## The countermodel, checked against its own closed forms

Section 16 is the round limiting itself: a relaxation satisfying every static
one-point valuation constraint while retaining exponent `1/9`, which proves the
`4/45` gain cannot have come from static information. That is the sort of
self-imposed limit worth checking as carefully as a claim.

The construction is fully specified, and its two closed forms —
`D(t) = Σ t^{k−1}/(3·2^k) = 1/(3(2−t))` and an average valuation tending to
`2/(2−t)` — can be eliminated against each other. What is left is a relation
between the round's *own reported numbers*:

> `avg_q → 6·|S_X|/X`

Their three reported sizes satisfy it with a gap of `2.0×10⁻³`, `7.2×10⁻⁴`,
`1.8×10⁻⁴` — shrinking monotonically, which is exactly what the `+ o(X)` in
`|S_X| = D(t)X + o(X)` predicts — and the `t` recovered from the density
converges to `0.5999`. Both series match their closed forms as exact rationals,
`t_β = 2(1 − 1/β)` is exactly where the average reaches `β`, and the class
densities `d_k = 1/(3·2^k)` check out by enumeration.

My first attempt at this was not a check. It enumerated a different set and
printed its average beside theirs, which reads like a reproduction and is not
one. Reading the construction properly turned a coincidence of names into a
decidable relation between their own figures.

## Observation 1 — the rounding chain, now with a drifting root

The pattern RUN-036 named at A-U.2d.8 and RUN-037 traced through four links is
here again, and this time the **root** drifts too:

> `C₁₀ = e^{289/1470}·7^{1/15}·13^{1/45}` — **+1 ulp**
> `C₁₀^{(r)} = C₁₀/6` — **+2 ulps**
> `c₁₀ = (C₁₀^{(r)})^{−45/41}` — **−1 ulp**
> `μ10 = (45θ★−4)/41 = 1496/12791` — **+1 ulp**
> `C_rel = C₁₀/(63/25)^{1/9}` — **exact**

and every link reproduces by redoing the arithmetic in float64 on the
already-rounded parent. Three of the paper's inline decimals are consequently
over-published by a digit. `β`, the four rational exponents `1/6`, `1/9`,
`4/45`, `1/45`, the mod-9 span coefficient and `C_rel` are all the exact nearest
doubles.

Nothing follows from any of it — these are last bits — but it is now the third
consecutive round with the same mechanism, and naming a cause is worth more than
reporting a drift.

A related thing went **right**. A-U.2d.9's span coefficient `24(4−β)/17` is
quoted here, and RUN-037 found that round's own constants frontier had it one
ulp wrong while its paper and checker report had it correct. The value quoted
forward is the correct one: the error did not propagate.

## Observation 2 — a ledger that is finer than its paper

Every earlier round's JSON ledger under-reported the paper's own list. This one
does the opposite: section 22.1 numbers **17** internally proved results and the
ledger lists **18**.

The extra entry is not an invention. Prose item 11 reads "improved nested-depth
bound and source inversion", and the ledger splits it into its two halves — a
depth bound and an inversion — both of which the prose item names.

The keyword check flags the depth half as having no counterpart, and that is a
vocabulary artifact rather than a finding: the ledger writes "low-source depth
bound" where the paper writes "nested-depth bound", so no long word is shared.
Its sibling, "source inversion", matches prose item 11 directly. A name-based
test cannot settle whether a list is complete — that is what item 51's lesson
said — so the counts are the measured part and the pairing is read.

The `NO-GO` count looks like it goes the other way — the paper carries **nine**
`NO-GO` headings against the ledger's **seven** — and it does not. Section 19 is
a summary section, and two of its entries restate boundaries the paper already
proved in place: `19.4` restates `16.1` (static valuation counting cannot
reproduce the gain) and `19.5` restates `17.1` (one-step aggregate balance
cannot be iterated below `4/45`). The ledger lists each boundary once. So the
difference is the paper's own duplication, not a ledger omission, and the
ledger's seven is the count of *distinct* boundaries.

That pairing was found two ways that agree: by reading the two section bodies,
and by a check that pairs `NO-GO` titles sharing distinctive words. The check
also proposes `19.6 restates 19.2`, which is spurious — those two share only
`product` and `exponent` — so it is reported as the heuristic it is, with the
counts as the decidable part.

The inherited, external and open lists agree exactly.

## The two manifests, and a validation record that narrowed

`CHECKSUMS.sha256` covers all eight non-self files and every digest reproduces.
The source-validation record covers **three** — the markdown sources only — and
its own notes say what it is for: UTF-8 decoding, LaTeX delimiter parity, control
characters, line endings. It is a source-text validator, not a manifest, and the
two together still cover everything except `CHECKSUMS.sha256` itself.

Worth stating precisely rather than as a gap, because the coverage did narrow:
item 54's record listed seven files and item 55's listed seven; this one lists
three, and the JSON and Python files are covered by `CHECKSUMS` alone. Its shape
is a dict under `files` — item 53's shape, returning after item 54's list and
item 55's three purpose-named blocks. Six bundles, four distinct shapes, and now
a repeat.

---

<!-- BEGIN GENERATED measured block: python code/src57_emit_report_block.py -->

**The reciprocal flow, exactly.** Theorem 3.1 is an identity between rationals and Corollary 3.2 telescopes it; neither needs a hypothesis.

| what | measured against | value |
| --- | --- | --- |
| accelerated edges from 2499 orbits | Theorem 3.1 | `70810` |
| …**violations of the identity** | `1/Y_j − 1/Y_{j+1} = (3−2^q)/(3Y_j) + 1/(3Y_jY_{j+1})` | `0` |
| first-crossing segments | longest `L` = 51 | `68311` |
| …**violations of the telescope** | `Σ(2^q−3)/Y_j = −3/y + 3/z + C_cross` | `0` |
| …where the balance is not equivalent to `z > y` | Theorem 4.1 IS the telescope plus that premise | `0` |
| …**meeting `z > y`**, the premise Theorem 4.1 needs | a first-crossing endpoint is where the slack drops | `0` |
| …Theorem 4.1 applied / violated | premise-gated | `0 / 0` |
| …**meeting Lemma 5.1's premise** | every state, the endpoint included, at or above the source | `0` |
| …cross term above `1/y² + 1/(2y)` / above `9/(14y)` | premise-gated; 2352 segments have a source below 7 | `0 / 0` |

**The harmonic capacities, which need no survival premise at all.**

| what | measured against | value |
| --- | --- | --- |
| segments checked | longest `L` = 51 | `68311` |
| …**violations of Theorem 6.1** `S₁ ≤ 2/y + log(1+6L/y)/6` | 33939 segments have no `q = 1` edge at all | `0` |
| …**violations of Theorem 6.2** `S₂ ≤ 2/y + log(1+12L/y)/12` | must be zero | `0` |
| …**violations of Theorem 7.1** | `S_tot < log(1+6L/y)/5 + log(1+12L/y)/15 + 289/(70y)` | `0` |
| …where `289/70` fails to decompose | `(6/5)(2) + (4/5)(2) + (1/5)(9/14)`, exactly | `0` |
| low-source segments `7 ≤ y ≤ L` | of 68311; Corollaries 9.1 and 9.2 live here | `241` |
| …**violations of Corollary 9.1** `𝒫 < C₁₀(L/y)^{4/45}` | must be zero | `0` |
| …**violations of Theorem 9.2** `𝒫/𝒫₆ ≤ C_rel(L/y)^{−1/45}` | the polynomial gain beyond the 3-sieve | `0` |
| …violations of the `𝒫₆ ≥ (63L/25y)^{1/9}` floor it rests on | must be zero | `0` |
| …admissible positions above `y + 3k + 1` | the A-U.2d.9 placement this round reuses | `0` |

**The exponent, empirically.** `P_RF` is an envelope, so a real segment need only stay under it; what is checked is that the envelope's own measured exponent falls toward `4/45 = 0.0889`.

| `y` | `L` | `P_RF` exponent → `4/45` | `𝒫₆` exponent → `1/9` |
| --- | --- | --- | --- |
| `7` | `200` | `0.12640` | `0.09645` |
| `7` | `800` | `0.11857` | `0.09936` |
| `7` | `3200` | `0.11346` | `0.10135` |
| `7` | `12800` | `0.10986` | `0.10278` |
| `11` | `200` | `0.10537` | `0.08777` |
| `11` | `800` | `0.10188` | `0.09242` |
| `11` | `3200` | `0.09963` | `0.09559` |
| `11` | `12800` | `0.09805` | `0.09786` |

Non-monotone steps toward `4/45`: `0`, out to `L = 12800`.

**The mod-9 target cost, and the span theorem whose premise real orbits meet.** As at A-U.2d.9, first-crossing subcriticality is what a first-crossing interval *is*, decidable as `2^Q < 3^m`.

| what | measured against | value |
| --- | --- | --- |
| edges checked against the mod-9 law | `2^q·m ≡ 4 or 7 (mod 9)` | `68311` |
| …**targets outside `{4,7} (mod 9)`** | must be zero | `0` |
| …**edges below their target cost** | `q ≥ c(m mod 9)` | `0` |
| cost-table entries rederived from the valuation arithmetic | the table is checked, not transcribed and trusted | `6` |
| …disagreeing with it | must be zero | `0` |
| capacity windows enumerated | `N_c ≤ W/9 + 2` | `20` |
| …exceeding that capacity | must be zero | `0` |
| proper prefixes examined | longest `m` = 50 | `27345` |
| …**meeting subcriticality** `2^Q < 3^m` | 0 fail | `27345` |
| …failing the valuation floor `Σq ≥ 3m − W/3 − 6` | the step the span bound rests on | `0` |
| …**Theorem 15.1 applied / violated** | `W > 3(3−β)m − 18` | `27345 / 0` |

**The round's own countermodel, checked against its own closed forms.** Section 16 gives `D(t) = Σ t^{k−1}/(3·2^k) = 1/(3(2−t))` and an average valuation tending to `2/(2−t)`. Eliminating `t` between them leaves a relation between the round's *reported* numbers: `avg_q → 6·|S_X|/X`.

| `X` | reported count | reported `avg_q` | implied by the density | gap | `t` recovered |
| --- | --- | --- | --- | --- | --- |
| `30000` | `7137` | `1.4253888188` | `1.427400` | `2.01e-03` | `0.598851` |
| `100000` | `23802` | `1.4274010587` | `1.428120` | `7.19e-04` | `0.599557` |
| `300000` | `71423` | `1.4282794058` | `1.428460` | `1.81e-04` | `0.599891` |

The gap shrinks monotonically across the three sizes, which is what the `+ o(X)` in `|S_X| = D(t)X + o(X)` predicts, and the recovered `t` converges. Both series agree with their closed forms as exact rationals (`0` and `0` disagreements), `t_β = 2(1−1/β)` is exactly where the average reaches `β` (`0` failures), the class densities `d_k = 1/(3·2^k)` check out on `4` classes, and no reported average exceeds `β` (`0`). The round's `max_rf_actual_ratio` is `0.9999997719832745`, at most one: `True`.

**Constants, against their closed forms.**

| constant | published | closed form | ulps |
| --- | --- | --- | --- |
| `C10_uniform_product` | `1.4671545685859186` | `exp(289/1470) * 7^(1/15) * 13^(1/45)` | `1` |
| `C10_depth` | `0.24452576143098645` | `C10/6` | `2` |
| `c10_source_inversion` | `4.691924627937959` | `C10_depth^(-45/41)` | `-1` |
| `relative_deficit_constant` | `1.3239628839265873` | `C10/(63/25)^(1/9)` | `0` |
| `mod9_target_span_coefficient` | `4.245112497836532` | `3(3-beta)` | `0` |
| `beta` | `1.584962500721156` | `log2 3` | `0` |
| `static_countermodel_t_beta` | `0.7381404928570849` | `2(1 - 1/beta)` | `-2` |
| `theta_star` | `0.19544992572902825` | `1/(rho+1)` | `1` |
| `dense_root_source_floor_exponent_mu10` | `0.1169572355562505` | `(45 theta-4)/41 = 1496/12791` | `1` |
| `AU2d10_product_exponent` | `0.08888888888888889` | `4/45` | `0` |
| `eta10_relative_to_AU2d9` | `0.022222222222222223` | `1/9 - 4/45` | `0` |
| `AU2d9_product_exponent` | `0.1111111111111111` | `1/9` | `0` |
| `AU2d8_product_exponent` | `0.16666666666666666` | `1/6` | `0` |

The chain again, and this time the **root itself drifts**. Every link reproduces by redoing the arithmetic in float64 on the already-rounded parent: `C₁₀/6` gives the published `C₁₀^{(r)}` (`True`), that raised to `−45/41` gives `c₁₀` (`True`), the float64 `θ★` through `μ10`'s formula gives `μ10` (`True`), and `C₁₀/(63/25)^{1/9}` gives `C_rel` (`True`).

The two artifacts disagree on `0` constants and use `4` different names for the same quantity (`4` keys appear only in the checker report, `5` only in the frontier).

A-U.2d.9's span coefficient is quoted here as `3.40946470486425`. The correctly rounded double is `3.40946470486425`; that round's own constants frontier had `3.4094647048642504`, so the wrong value did **not** travel forward.

| the paper prints | verdict |
| --- | --- |
| `AU2d9_span_coefficient_quoted` = `3.40946…` | exact to every published digit |
| `four_forty_fifths` = `0.088888…` | truncated rather than rounded at the last digit |
| `relative_deficit_constant` = `1.3239628839…` | exact to every published digit |
| `C10_depth` = `0.2445257614…` | exact to every published digit |
| `c10_source_inversion` = `4.6919246279…` | exact to every published digit |
| `theta_star` = `0.19544992572902825…` | OVER-PUBLISHED |
| `mu10` = `0.1169572355562505…` | correctly rounded at the last digit |
| `mod9_target_span_coefficient` = `4.245112497836532…` | OVER-PUBLISHED |
| `C10_uniform_product` = `1.4671545685859186…` | OVER-PUBLISHED |
| `mu8_from_AU2d8` = `0.0345399108…` | truncated rather than rounded at the last digit |
| `mu9_from_AU2d9` = `0.0948811664…` | exact to every published digit |
| `t_beta` = `0.738140492857…` | exact to every published digit |

**The ledger against the paper's own section 22, and the manifests.**

| the paper says | the JSON ledger says | shortfall |
| --- | --- | --- |
| §22.1 proved internally: `17` | `proved_internally`: `18` | `-1` |
| §22.2 inherited: `9` | `inherited_internal`: `9` | `0` |
| §22.3 external grounding: `3` | `external_primary_grounding`: `3` | `0` |
| §22.4 explicitly open: `6` | `open`: `6` | `0` |

The paper carries `9` `NO-GO` headings (`16.1, 17.1, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7`) against the ledger's `7`; titles with no ledger entry sharing a distinctive word: *19.4 Static valuation-class counting can reproduce the new gain*.

| what | measured against | value |
| --- | --- | --- |
| files in the bundle | `CHECKSUMS.sha256` lists 8, the validation record 3 | `9` |
| …digests that do not reproduce, in either manifest | must be zero | `0` |
| …where the two manifests disagree | on the files both list | `0` |
| …files covered by neither | CHECKSUMS.sha256 | `1` |
| validation-record shape | dict of file records under `files` (item 53) | `—` |
| the checker's named checks independently confirmed | of 10; 4 named as not covered here | `6` |
| this run's own bracket self-checks | 0 failed | `8` |
| defects planted / caught by the check named for each | 1 robustness property; 0 malformed; 2 controls, 2 undisturbed | `35 / 35` |

**Not covered here**, named rather than implied: *q1_q2_residue_classes*; *uniform_relative_deficit_grid*; *static_valuation_only_countermodel*; *relaxation_sharpness_diagnostic*.

Every figure above is emitted by `code/src57_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

Brackets come from `src53`, `src54` and `src55`, certified there. Three of this
gate's own errors were caught before publication, and two of them would have been
findings against correct arithmetic.

**A false 352.** Lemma 5.1 sums `1/n²` over odd `n ≥ y`, so it needs every state
of the segment — the endpoint included — to be at least `y`. Applied without
that, it flagged 352 segments of a lemma that holds. With the premise measured,
it is applied to none, which is the honest answer.

**A comparison between two envelopes.** I checked `P_RF` against `P₆` and found
ten cases where the first exceeded the second — but the round takes their
**minimum**, `P₁₀ = min(P₆, P_RF)`, precisely because neither dominates.
Theorem 9.2's deficit is about the *actual* product against `P₆`, which is a
different check and passes. Two envelopes are not a claim about one bounding the
other.

**A bracket too loose to identify what it judged.** `C₁₀` multiplies three
irrational roots, and at the 25-digit default their errors compounded to a
bracket `2.7×10⁻²⁵` wide — not enough to pin a 17-place decimal, so
`C₁₀^{(r)}` came back unidentified. Forty digits fixed it. This is RUN-036's
lesson met from the other side: there the reference was rendered too coarsely,
here it was computed too coarsely.

A fourth problem was speed, and the fix matters because of what it avoided. The
capacity check evaluated two eighty-term logarithm series **per segment**, which
took 85 of the gate's 88 seconds and made a larger orbit sweep unaffordable. The
tempting response is to lower the population guard until what you already have
looks sufficient. Memoising the series instead took the run to 26 seconds at a
*larger* limit, so the guards were met rather than adjusted: **70,810** edges
against a threshold of 50,000, and 241 low-source segments against 200.

The drill took three passes, and its `malformed` classification did the work
each time. The first returned 24 of 35 with **ten** mutations reported as "the
mutation changes nothing" — not misses, but defects that were never planted.
Three kinds turned up, and only the first would have been a hole:

* two aimed inside blocks the premise gate leaves **empty** — nothing can be
  planted in code that no segment reaches, which is itself a confirmation that
  the gate is empty rather than merely quiet;
* one aimed at a validation-record branch this bundle does not take, since its
  `files` is a dict and the mutation disabled the list branch;
* the rest simply **too weak**. Halving a logarithmic coefficient, or shifting
  an exponent from `4/45` to `1/45`, leaves bounds these segments still satisfy
  comfortably. A defect that a correct check legitimately tolerates measures
  nothing; making them decisive — dividing a bound by a thousand — is what turns
  "no violations" into evidence.

A fourth anchor matched zero times: an earlier re-aim had been written through a
shell heredoc that mangled its escapes, so the patch silently never applied. The
pre-flight named it rather than scoring it a miss.

## What the checker claims and this run did not check

The report names ten checks. Six are independently confirmed here — the
reciprocal-flow identity, the cross-term bound, the two harmonic capacities, the
actual product bound, the mod-9 target table, and the mod-9 span. The other four
are **named** in the log: the `q=1`/`q=2` residue classes, the uniform
relative-deficit grid, the static countermodel's own run, and the relaxation
sharpness diagnostic.

The checker's scope warning — that it instantiates no divergent orbit, proves no
linear B-density, certifies no Diophantine constant, and does not prove Collatz —
is intact and correct.

## Route map

`ROUTE_MAP v2.10`. The constants frontier names item 58 as
`A-U.2d.11 — Multi-Step Reciprocal-Transport Rigidity`, which is the round the
open list says is needed to go below `4/45`.

## A note on item 56

The sweep's item 56 is `Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0.zip`,
not a Hard-Zeta round. The source manifest records it as already archived and
rechecked at RUN-002, so this run verified that claim rather than redoing it: the
zip's digest matches the manifest, and all **50** entries reproduce byte-for-byte
against `collatz-ot-series-neok/`, with nothing missing, differing or extra.

## What this run does not claim

1. That Theorem 4.1 or Lemma 5.1 hold. Their premises are met by no real
   segment. Theorem 4.1's *equivalence* to the telescope plus `z > y` was
   checked; the conclusion was not.
2. That the `4/45` exponent holds asymptotically. What was measured is that the
   envelope's finite-`L` exponent falls toward it, and that every real segment
   stays under the uniform bound. A trend and a bound, not a proof.
3. That the dense-support root-source floor (§11) or the master inequality
   (§12.4) hold. Only their constants and relations were recomputed.
4. That the countermodel is a valid relaxation of the Collatz dynamics. It is an
   abstract construction, the round says so, and what was checked is that it is
   internally consistent with its own closed forms.
5. That the mod-9 diameter gain can be promoted to a harmonic exponent. The
   round's `NO-GO 19.6` forbids it and this run did not test the stronger claim.
6. That the shipped checker is correct. It was read, never run.
