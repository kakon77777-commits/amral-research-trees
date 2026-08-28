# RUN-035 — Hard-Zeta A-U.2d.7: the crossing slope really does move by whole numbers, the caps above it rest on a premise almost no real chain meets, and the round's new machine-readable ledger under-reports its own paper

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d7_Plateau_Reset_Quantization_Rigidity_bundle_v0.1.zip` (source item 53) — 27 numbered results across 24 sections, the largest bundle in the sweep. Ships a checker, its report, a constants frontier, a source-validation record, a stdout transcript, and — new this round — a machine-readable **theorem ledger**.
**Tools:** [`src53_plateau_reset.py`](../code/src53_plateau_reset.py) · [`src53_drill.py`](../code/src53_drill.py) · [`src53_emit_report_block.py`](../code/src53_emit_report_block.py)
**Logs:** [`src53-au2d7.json`](../data/gate-logs/src53-au2d7.json) · [`src53-drill.json`](../data/gate-logs/src53-drill.json)

**Result: section 3 is the cleanest decidable core this sweep has been given, and it holds exactly — `β` cancels out of the jump law, so every claim in it is settled in integers. Sections 4.3 through 9 are a different kind of statement: each is derived from B-survival inputs, and one chain in tens of thousands meets them, so they were measured for premise satisfaction and their derivations checked on a grid, not imposed on orbits that never agreed to them. Three findings, none mathematical: the new theorem ledger is a lossy rendering of the paper's own section 22, the frontier and the paper disagree on a constant at the last bit, and the source-validation record has changed schema for the third time in four bundles.**

---

## The part that needs no logarithm

Section 3 defines the crossing slope of a nested interval as

> `ξ_i = D_i/L_i = Q_i/L_i − β`

and then proves something better than an estimate about how it moves:

> `ξ_{i+1} − ξ_i = J_i/(L_i L_{i+1})`,  `J_i = Q_{i+1}L_i − Q_i L_{i+1} ∈ ℤ`.

`β` appears in both slopes and cancels in the difference. What is left is a ratio
of integers, so the whole section — the jump law, the `1/(L_iL_{i+1})`
quantization, the plateau specialization `J_i = Π_i ≥ 1`, the strict-drop form
`J_i = (g_i+h_i)D_{i+1} − L_{i+1}(E_i−A_i)`, and the characterization of a
genuine reset as exactly `J_i < 0` — is decidable without evaluating a single
logarithm. So is Theorem 4.4, so is Lemma 5.1, and so is all of section 11.

That is what the measured block below reports, over six figures of renewal edges
drawn from real orbits. Nothing in it disagrees with the round.

The positivity claims of section 1 come out the same way. `A_i`, `D_i` and `E_i`
are each `cβ + k` for integers `c, k`, and `cβ + k = log₂(3^c 2^k)`, so their
signs are decided by comparing `3^c 2^k` with `1`. Theorem 4.4's `E_i − A_i >
1/L_{i+1}` needs one more step and becomes `2^N` against `3^D`. No bracket is
consulted for any of them.

## The check that stopped me publishing a false violation

My first chain builder took the **records of `δ`**: start at a source, then walk
forward taking each index whose slack exceeds the current one. That satisfies
section 1's `δ_{s_1} < δ_{s_2} < ⋯` exactly as written, and it produced **33,052
strict edges with `Δ_i < 1` out of 86,539** — a 38% violation rate against a
boxed claim that the determinant is a positive integer. (Those two figures come
from the discarded construction on a wider sweep than the one measured below;
they are recorded here and in both tool docstrings because the error is the
point, not the sweep size.)

It is wrong, and it is my error, not the round's. Section 1 also asks for
`s_r ≤ t < e_i`: the intervals of a chain all cover a **common point**. Records
only force `δ` to increase, and two record intervals can be *disjoint*, which
makes `h_i = e_i − e_{i+1}` negative and the determinant meaningless. The chain
is the **stalk** — the set of first-crossing intervals covering one position,
which laminarity totally orders and which the sweep already holds on its stack.

Rebuilt that way, `endpoints_not_nested_h_negative` is zero, and `Δ_i < 1` goes
from 33,052 to **zero**. A 38% violation rate against a boxed claim is a
statement about the checker, which is the lesson item 46 charged for and this run
paid a second instalment on. `D1` in the drill replants it.

## What sections 4.3 to 9 actually rest on

Theorem 4.3 caps strict drops by `(2+√2)√(LB)`. Theorem 5.4 caps plateau mass.
Theorem 6.1 combines them into the round's headline depth inequality, 6.2 makes
it explicit, 7.1 inverts it to `y₁ = O(L²/r)`, and 9.4 turns it into a
high-source no-go. Every one of those descends from three inputs declared in
section 1:

> `H = Σ A_i < B(L,y₁)`,  `Σ E_i < 2B(L,y₁)`,  `0 < D_i/L_i < 1/(3y_i ln2)`.

Those are **B-survival properties**. They describe the hypothetical divergent
orbit the programme is trying to rule out. A real Collatz orbit does not owe them
and mostly does not satisfy them — the measured block gives the rates, and the
number of chains meeting all three at once is **one**.

So this run does not claim to have tested those caps. RUN-032 applied a cap to
10,214 chains that had never met its corridor hypothesis and flagged all 10,214,
which measured nothing except the check. Instead:

1. the premises are **measured** and reported as rates;
2. the caps are applied only where the premise holds, and the denominator is
   printed rather than dressed up;
3. the **derivations** are checked on a grid, because an implication is
   arithmetic even when its hypothesis is unavailable — `B < L/(3y₁ln2)`,
   `6.1 ⟹ 6.2`, `X_r` being the positive root, `7.1`'s inversion, `7.2` for
   `r ≥ 9`, `9.3`'s `B < 1/L` and `9.4`'s `(2+√2)√(LB) < 4`.

The drill's `D26` is the control that makes this honest. It deletes the premise
filter, so the caps apply to every chain — and the gate goes **red**. A filter
that had quietly excluded everything and proved nothing would have stayed green.

## Section 9's hypothesis is common; its conclusion needs the unstated half

`y₁ > L²/(3 ln2)` is not a rare condition — thousands of real chains satisfy it,
so the theorem is not vacuous. On those chains the stated conclusions do *not*
hold: most have unequal crossing slopes, most have plateaus, and the deepest goes
well past `r ≤ 4`.

That is not a counterexample and this run does not report it as one. Theorem
9.2's proof needs `ξ_i < 1/(3y₁ln2)` as well, which with the hypothesis gives
`ξ_i < 1/L²` and leaves room for one slope state. Section 1 declares that bound
as B-survival, and **no** high-source real chain satisfies it. The literal
hypothesis is not sufficient on its own; the companion is stated one section
earlier. Worth naming precisely, because a reader who lifts Theorem 9.2 out of
its round will get a false statement.

The part of Lemma 9.1 that is pure arithmetic — two distinct rationals with
denominators at most `L` differ by at least `1/L²` — holds on every chain tested.

## Finding 1 — the new ledger is a lossy copy of the paper's own

`Hard_Zeta_AU2d7_theorem_ledger.json` is the first machine-readable theorem
ledger in this sweep, and it is the artifact most likely to be consumed by
something that never reads the paper. The bundle happens to state the same ledger
twice — section 22 in prose, the JSON alongside it — which makes fidelity
checkable by counting, with no mathematics and no keyword guessing.

Section 22.1 numbers **19** internally proved results; `internal_theorems` lists
**16**. Section 18 carries **7** `NO-GO` headings; `no_go` lists **6**. The
inherited, external and context-only lists agree exactly, as do the round name
and the next round.

The missing no-go is **`NO-GO 18.2 — repeated reset with no endpoint-slack
cost`**, identified two ways that agree: by reading, and by a keyword test that
found no ledger entry sharing any distinctive word of its title. Its *theorem*
is in the ledger under `internal_theorems`; its status as a no-go boundary is
not.

And the ledger and the constants frontier — two machine-readable files in one
bundle — give different `status` strings, the ledger's being the frontier's
minus its first word.

## Finding 2 — the frontier and the paper disagree at the last bit

`high_source_threshold_coefficient_1_over_3ln2` is published as
`0.48089834696298783`. That is **one ulp** above the nearest double to
`1/(3 ln2)`, confirmed twice: against a bracket certified in the gate, and
against `Decimal`'s own `ln`.

The interesting part is that the *paper* has it right. Section 9 prints
`0.4808983469629878…`, which is exactly the correctly rounded double. The two
artifacts in one bundle disagree on the same constant, and the machine-readable
one is the wrong one.

Every other frontier constant is the exact nearest double, the two inherited
powers still sum to one, `2/ln2` is exactly twice `1/ln2` as doubles, and all
four decimals printed in the paper are correct to every digit shown. Item 50's
constants were 1–2 ulps out, items 51 and 52 were exact; this is one slip, not a
relapse, and saying so is the same obligation as reporting it.

## Finding 3 — the validation record has changed schema again

`SOURCE_VALIDATION_AU2d7.json` keys its file records as a **dict under `files`**.
Item 50 used `artifact_sha256_before_manifest`; items 51 and 52 used a **list**
under `files`; this is the third shape in four bundles. A reader written for any
one of them sees zero files and reports zero mismatches, which looks exactly like
a clean bill.

The checker report renamed `verified_claims` to `verified_statements` in the same
bundle, with the same failure mode. Both now have a guard that fires on an empty
read rather than passing quietly, and the drill aims a defect at each.

All listed digests reproduce. `checker_stdout.txt` is byte-identical to the
checker report — the fourth bundle to ship one content under two names, and the
third where they are identical to the byte rather than off by a newline.

## A smaller thing worth keeping

Corollary 7.2's proof turns on the threshold `2b²/a`, printed as `7.7712…`. The
`ln 2` inside `a = 1/ln2` cancels the one inside `b² = (6+4√2)/(3ln2)`, leaving

> `2b²/a = (12 + 8√2)/3`

which is **algebraic** — no logarithm survives — so `2b²/a < 8`, the inequality
the corollary needs, is decidable in exact rationals. The round's decimal is
correct; it just did not have to be a decimal. It is the same pattern RUN-027,
RUN-029, RUN-032 and RUN-033 each found: this line reaches for higher precision
where it could reach for exactness.

---

<!-- BEGIN GENERATED measured block: python code/src53_emit_report_block.py -->

**Section 3, on real orbits.** Every row below is decided in exact rational arithmetic; `beta` cancels out of the jump law, so no logarithm is evaluated anywhere in this table.

| what | measured against | value |
| --- | --- | --- |
| active nested chains built from 1499 orbits | deepest `r` = 17, longest `L` = 51 | `29468` |
| renewal edges across them | 107592 plateau, 36703 strict, of which 6365 have determinant one | `144295` |
| …**violations of the jump law** `xi_{i+1}−xi_i = J_i/(L_iL_{i+1})` | exact Fractions, must be zero | `0` |
| …`J_i ≠ 0` failing the `1/(L_iL_{i+1})` quantization | 1711 edges have `J_i = 0` | `0` |
| …falling below the coarser `1/L²` | the bound section 9 uses | `0` |
| **genuine resets**, `J_i < 0` | of which 195 have determinant one | `21991` |
| …**Theorem 4.4 violations** `E_i − A_i > 1/L_{i+1}` | decided as `2^N` against `3^D`, not as a bracket | `0` |
| plateau edges where `J_i ≠ Π_i` / `Π_i < 1` / the two forms disagree | `Π_i = Q_{i+1}g_i − p_iL_{i+1} = g_iD_{i+1} + L_{i+1}A_i` | `0 / 0 / 0` |
| strict edges where `Δ_i < 1` / the two forms disagree / `J_i` misfits | `Δ_i = r_ig_i − p_ih_i = g_iE_i + h_iA_i` | `0 / 0 / 0` |
| renewal identity `A_i + D_i = D_{i+1} + E_i` failing | as a beta-linear pair, must be the pair `(0,0)` | `0` |
| `A_i`, `D_i`, `E_i` not positive / endpoints not nested | sign decided exactly by `3^c 2^k` against 1 | `0 / 0` |
| **Lemma 5.1** chains where `Σ g_iL_{i+1} ≥ L²/2` | checked on all 29468 chains | `0` |
| **§11** unit strict edges, all with `p_i/g_i < β < r_i/h_i` | the annulus premise, tested not assumed: 0 fail | `6365` |
| …with the mediant below `β`, where `J_i > 0` must hold | 0 counterexamples | `6150` |
| …**unit resets** failing child-slope / mediant / denominator `≥ 2g+h` | of 195 unit resets | `0 / 0 / 0` |
| …Farey-neighbour identity `(p+r)g − p(g+h) = 1` failing | an integer identity, not an estimate | `0` |

**The premises sections 4.3 to 9 stand on.** These are B-survival properties. A real orbit does not owe them, and the point of measuring is that the caps cannot be tested where they are absent.

| premise | of | met |
| --- | --- | --- |
| overshoot `D_i/L_i < 1/(3y_i ln2)` | 173763 nested intervals | `4898` |
| …chains where **every** interval meets it | 29468 chains | `1` |
| origin-slack budget `H < B(L,y₁)` | 29468 chains | `1` |
| endpoint budget `Σ E_i < 2B` | 29468 chains | `9637` |
| **every premise at once** | 29468 chains | `1` |

So Theorems 4.3, 5.4 and 6.1 were applied to **1** chain and held there — a denominator that settles nothing, and is reported rather than dressed up. `U_β(L) ≤ L/3` was verified exactly on every chain (`0` violations).

Section 9's hypothesis is attainable and common — **13433** of 29468 chains satisfy `y₁ > L²/(3 ln2)`. Its conclusions do not follow on them: `569` have all crossing slopes equal, `1792` have no plateau, `10099` have `r ≤ 4` (deepest seen: `16`). That is not a counterexample. Theorem 9.2 also needs the survival slope bound `ξ_i < 1/L²`, which **0** of those 13433 chains satisfy, and section 1 declares it. The separation half of Lemma 9.1 is pure arithmetic and does hold: of 28899 chains with more than one slope, `0` have two distinct `Q_i/L_i` closer than `1/L²`.

**The derivations, which are arithmetic and can be checked.** Over `378` grid points in `(L, y₁, r)`:

| derivation | violations |
| --- | --- |
| `B(L,y₁) < L/(3y₁ln2)`, from `log₂(1+x) < x/ln2` and `U_β(L) ≤ L/3` | `0` |
| Corollary 6.2 is implied by Theorem 6.1 | `0` |
| `X_r` is the positive root of `ax² + bx = r−1` | `0` |
| Theorem 7.1's inversion `y₁ < L²/X_r²` | `0` |
| Corollary 7.2 for `r ≥ 9` | `0` |
| Corollary 9.3's `B < 1/L` | `0` |
| Theorem 9.4's `(2+√2)√(LB) < 4` | `0` |

Corollary 7.2's threshold `2b²/a` is **algebraic**: the `ln 2` in `a` cancels the one inside `b²`, leaving `(12+8√2)/3 = 7.771236166328…`, which is below 8: `True`. The round prints it as `7.7712`.

**The theorem ledger, a new artifact this round, against the paper's own section 22.**

| the paper says | the JSON ledger says |
| --- | --- |
| §22.1 lists `19` internally proved results | `internal_theorems` has `16` — **3 fewer** |
| §18 carries `7` `NO-GO` headings | `no_go` has `6` — **1 fewer** |
| §22.2 lists `6` inherited rounds | `6`, all `6` named and present in the paper |
| §22.3 lists `4` external inputs | `4`, arXiv ids absent from the paper: `0` |
| §22.4 lists `1` context-only source | `1` |

The one `NO-GO` with no ledger entry sharing any of its keywords is **18.2 repeated reset with no endpoint-slack cost**. Round name agrees across ledger, frontier and checker report: `True`; next round agrees: `True`; **status does not**: the ledger says `rigorous reduction; no full contradiction`, the frontier says `strongest rigorous reduction; no full contradiction`.

**Constants, against brackets certified in this file** — `ln 2` from `Σ 1/(k2^k)` with its exact tail, `log₂3` from `(3^q).bit_length()`, `√2` from integer square roots. No floating-point reference is consulted. `1/ln2` to 20 places: `1.44269504088896340735`.

| constant | published | ulps from the nearest double |
| --- | --- | --- |
| `one_over_ln2` | `1.4426950408889634` | `0` |
| `high_source_threshold_coefficient_1_over_3ln2` | `0.48089834696298783` | `1` |
| `strict_explicit_coefficient` | `2.3676490321349077` | `0` |
| `depth_source_simple_coefficient_2_over_ln2` | `2.8853900817779268` | `0` |
| `disjoint_backbone_power` | `0.8365051337388006` | `0` |
| `dense_overlap_required_power` | `0.1634948662611994` | `0` |

| the paper prints | verdict |
| --- | --- |
| `1/ln2` = `1.4426950408889634…` | exact to every published digit |
| `(2+sqrt2)/sqrt(3 ln2)` = `2.3676490321349077…` | truncated rather than rounded at the last digit |
| `(12+8 sqrt2)/3` = `7.7712…` | exact to every published digit |
| `1/(3 ln2)` = `0.4808983469629878…` | exact to every published digit |

The frontier and the paper **disagree** on `1/(3 ln2)`: `False`. The paper's `0.4808983469629878` is the correctly rounded double; the frontier's `0.48089834696298783` is one ulp away. The other `5` frontier constants are exact, the two inherited powers still sum to one (`True`), and `2/ln2` is exactly twice `1/ln2` as doubles (`True`).

| what | measured against | value |
| --- | --- | --- |
| shipped unit-reset examples recomputed | 9 clauses each; 0 failing | `1` |
| validation-record files verified | shape: dict of file records keyed by filename (item 53); uncovered: 1 | `9` |
| the checker's stated claims independently confirmed | of 13 under the key `verified_statements`; 8 named as not covered here | `5` |
| defects planted / caught by the check named for each | 1 robustness property; 0 malformed; 2 controls, 2 undisturbed | `27 / 27` |

**The two transcripts.** `checker_stdout.txt` is byte-identical to the checker report: `True` (both `4876` bytes).

**Not covered here**, named rather than implied: *every strict upper wing has all proper suffixes coefficient-supercritical*; *unit upper-wing rational prefix domination and exact rational-Catalan capacity on enumerated layers*; *unit upper Christoffel correction maximum and Gamma_up > M_up/16 off the aligned code*; *dual endpoint-span suffix envelope and exact additive Christoffel replacement deficit*; *continued-fraction convergent error lower bound on the computed prefix of beta*; *universal strict-drop determinant split and aggregate square-root ingredients*; *negative-reset quantization E_i-A_i > 1/L_{i+1} and aggregate reset budget ingredient*; *sharp dual suffix-supercritical envelope and explicit reverse-mechanical attaining code*.

Every figure above is emitted by `code/src53_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

No floating-point reference is consulted anywhere in this run's constants check.
`ln 2` comes from `Σ_{k≥1} 1/(k 2^k)` with its exact tail bound `1/((N+1)2^N)`;
`log₂3` from `(3^q).bit_length()`, which is `⌊βq⌋` by definition; `√2` from
integer square roots. Each is certified in the file that uses it.

That mattered immediately. The first version of the `β` bracket hard-coded
`190537/120200` as a lower bound. It is `1.58516…` — **above** `β`, so the
"lower" bound was an upper one. The assertion that certifies the bracket is why
that never reached a result, which is the whole argument for certifying an
instrument you could just as easily have trusted. The better answer was that
almost nothing here needs a bracket: the comparisons are all `3^c 2^k` against
`1`, or `2^a` against `3^b`.

The published decimals are **discovered** from the paper rather than asserted —
a hard-coded digit string is a second place to make the typo the check exists to
catch — and a printed decimal this run cannot match to any reference raises a
guard rather than passing unnoticed.

Running the tree's own standing guards afterwards turned up a second one, older
and worse. `audit_drill_anchors.py` exists to catch anchor rot — a drill whose
target string has been refactored away tests nothing and says so only when next
run. It knew three defect-list shapes, all of them the `src07`–`src21`
generation. Every drill from `src22` onward declares `DEFECTS` against `GATE`, a
four-element tuple instead of three, so the audit read **zero anchors for 16 of
31 drills** — the entire current sweep among them — and reported `ok: true`.
The guard had the disease it was written to catch, and its own zero was the
finding, which is what `measure-what-the-check-ignores` says to look for.

It now discovers the shapes instead of listing them, names the 103 defects that
genuinely are not string replacements rather than dropping them, and **refuses**
when a drill yields no auditable anchors and no reason why. Coverage went from
**277** anchors to **502**; none of the 225 newly visible ones is stale, so
nothing was actually broken — but nothing had been watching them either.

The drill's first pass came back **26 of 27**, and the miss was a hole in this
gate rather than a defect that escaped. The derivation failures were collected by
matching key names against the suffixes `violations`, `_implied` and `_x`.
`cor_6_2_not_implied_by_thm_6_1` ends in none of them, so that counter could
increment and nothing would ever read it — a check whose refusal had no reader,
which is the shape RUN-028 named and this gate reproduced. Enumerating the
counters fixed the instance; making the gate **refuse** when it finds an integer
in that block it was never told about fixes the class, so the next counter added
here cannot go unread quietly.

## What the checker claims and this run did not check

The shipped report states its claims under `verified_statements`. Five are
independently confirmed here: the jump law, the plateau and strict determinants,
the unit-reset orientation, the `1/L²` rational separation, and the plateau
determinant split with Lemma 5.1. The rest are **named** in the log rather than
waved at — the upper-wing results of sections 12 to 16, the aggregate
square-root ingredients of Lemmas 4.1 and 4.2, the aggregate reset budget, and
the continued-fraction convergent bound.

The checker's own `not_verified` list — a divergent orbit, the partial quotients
of `log₂3`, the density argument, and a full contradiction — is intact and
correct.

## Route map

`ROUTE_MAP v2.7`. Both the ledger and the constants frontier name item 54 as
`A-U.2d.8 — Quadratic Low-Source Corridor Saturation`, and they agree.

## What this run does not claim

1. That Theorems 4.3, 5.4, 6.1, 6.2, 7.1, 7.2, 9.1, 9.2, 9.3 or 9.4 hold. Their
   premises are B-survival properties; one real chain met all of them, and one
   is not a test. Their **derivations** were checked; the theorems were not.
2. That the section 9 results are false. Real chains failing their conclusions
   is what the missing survival bound predicts, not evidence against the round.
3. That the upper-wing results of sections 12 to 17 hold. Not checked at all.
4. That the CF-depth-source squeeze of section 8 holds. It rests on the local
   continued-fraction bound, which is not checked here or in RUN-034.
5. That the ledger's three missing internal results and one missing no-go are
   errors of substance rather than of transcription. The counts are measured;
   the intent is not mine to state.
6. That the shipped checker is correct. It was read, never run.
