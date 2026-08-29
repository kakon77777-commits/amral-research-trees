# RUN-036 — Hard-Zeta A-U.2d.8: a Gamma identity that needs no Gamma, a depth cap no real orbit can be tested against, and two rational constants published as their float64 evaluations

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d8_Quadratic_Low_Source_Corridor_Saturation_bundle_v0.1.zip` (source item 54) — 23 sections. Ships a checker, its report, a constants frontier, a theorem ledger, a source-validation record, and — new this round — a `CHECKSUMS.sha256`. It does **not** ship a stdout transcript, the first since item 49.
**Tools:** [`src54_low_source_saturation.py`](../code/src54_low_source_saturation.py) · [`src54_drill.py`](../code/src54_drill.py) · [`src54_emit_report_block.py`](../code/src54_emit_report_block.py)
**Logs:** [`src54-au2d8.json`](../data/gate-logs/src54-au2d8.json) · [`src54-drill.json`](../data/gate-logs/src54-drill.json)

**Result: this round leaves the additive slack machinery for a multiplicative one, and the exchange is a good one — section 3's identity, section 4's envelope and section 5's Gamma representation are all statements about rationals, and all hold exactly. The Gamma identity in particular needs no Gamma evaluated at all. Section 9.1's depth cap is a different kind of claim: its endpoint-gap premise is met by none of the real chains tested, so it was measured rather than imposed. Three findings, none mathematical: two exactly rational constants are published as their float64 evaluations, the theorem ledger under-reports the paper's own section 21 in three of five places, and — reported as an improvement — the bundle's two digest manifests agree, cover everything but one declared file, and close the gap item 51 found.**

---

## The identity that needs no Gamma

Section 5 states the consecutive-odd packing envelope in closed form:

> `𝒫(y,L) = Γ(L+y/2+1/6)Γ(y/2) / (Γ(y/2+1/6)Γ(L+y/2))`

The shipped checker verifies this numerically and reports a worst error of
`3.1×10⁻¹⁰`. There is nothing to verify numerically. For integer `L`, the
functional equation alone turns that quotient into a **Pochhammer ratio**

> `∏_{k<L} (y/2 + k + 1/6)/(y/2 + k)`

and each factor is `(3(y+2k)+1)/(3(y+2k))` after clearing sixths — which is
exactly `𝒫(y,L)`'s own definition. The two sides are the same rational number.
This run's error is not small; it is **zero**, on every pair tested and on every
segment of every orbit swept.

The same is true of the rest of the decidable core. Section 3's identity

> `z/y = (3^L/2^Q)·∏_{j<L}(1 + 1/(3Y_j)) = 2^(−D)·𝒫`

is a product of integer ratios, and `2^(−D) = 3^L/2^Q` because `2^(βL) = 3^L`,
so the two printed forms are one form. Section 4's envelope compares two exact
products. None of it evaluates a logarithm.

Because the exact identity is the whole check, I ran the numeric one anyway as a
second method — `math.lgamma`, a different implementation and a different
representation. That check needed its own correction, below.

## Section 4's premise is met everywhere; section 9.1's is met nowhere

Two premises in this round look similar and behave in opposite ways, and the
difference is the point.

**Section 4** asks that the source be the segment minimum and the states be
distinct. Every segment tested satisfies both — the premise is structural for a
first-crossing interval, not an assumption about divergence. So Theorem 4.1 is
genuinely tested, at scale, and holds.

**Section 9.1** looks like an orbit statement and is not. It is Theorem 7.2
rearranged, and 7.2 is built from the inherited `y_r > 2^H y_1` together with
`z_1 > y_r` — the outer endpoint lying above the innermost source. On real
orbits `z_1 > y_r` holds for **none** of the chains tested, which is what a
first-crossing endpoint is: the place the slack finally drops. So the
endpoint-gap premise is met by nothing, and Theorem 9.1 was applied to nothing.

Applied blind it flags thousands, which is RUN-032's error and RUN-035's, and
this run does not repeat it. What it does instead:

1. the premises are **measured**, each separately, and the denominators printed;
2. the **algebra** of 9.1 — that `1 + (4r−2)/y₁ < 𝒫` and `r < ½ + y₁(𝒫−1)/4`
   are one inequality — is universal, and is checked exactly on every chain;
3. the derivations of 5.2 and 9.2 are checked on a grid, because an implication
   is arithmetic even when its hypothesis is unavailable.

A premise met by zero subjects is the case where "0 violations" and "nothing
tested" produce identical logs, so the drill's `D9` deletes the premise gate and
requires the run to go **red**. It does. That, not the guard, is what makes the
empty denominator honest.

## Finding 1 — two rational constants published as float64 evaluations

`θ★` and `μ★` are not transcendental. They are fixed by `ρ★ = 4.1164`:

> `θ★ = 1/(ρ★+1) = 2500/12791`,  `μ★ = (6θ★−1)/5 = 2209/63955`

The published values sit **1** and **2** ulps from the nearest doubles to those
rationals. That alone would be a last-bit curiosity. The mechanism is what makes
it worth stating: `1/(4.1164+1)` evaluated in float64 reproduces the published
`theta_star` **bit for bit**, and `(6θ−1)/5` from that float reproduces
`mu_star`. They were computed in doubles rather than as the rationals they are,
and the second inherits the first's error.

The inherited `old_dense_overlap_exponent = 2500/15291` is the exact nearest
double, and so are the genuinely transcendental constants — `C_H`, `log₂Y_ver`,
`√(3 ln2·Y_ver)`. The round rounds its **rationals** worse than its
transcendentals, which is the reverse of what one would expect and the same
reach-for-exactness gap RUN-027, RUN-029 and RUN-035 each found somewhere else.

There is a second, smaller edge to it. The paper prints these constants to
seventeen digits followed by an ellipsis. Since the printed digits are the
float64 repr, the last one is not a digit of the constant: `θ★` continues
`…8222…` where the paper shows `…825`. Four constants are affected, and
`decimal_verdict` calls all four over-published. No consequence follows for any
result; the ellipsis simply promises more of a number than it has.

## Finding 2 — the ledger still under-reports, in three places of five

The bundle states its ledger twice, as prose in section 21 and as JSON, so
fidelity is a matter of counting. Section 21.1 numbers **17** internally proved
results and the JSON lists **14**; section 21.3 lists **5** external inputs to
**4**; section 21.5 lists **3** open items to **2**. Sections 21.2 and 21.4
agree exactly.

The missing external input is identified two ways that agree — by reading, and
by a keyword test restricted to words distinctive within the section — as
**the inherited irrationality-measure consequence for `log₂3` through
`ρ★ = 4.1164`**. That is not a peripheral citation: `ρ★` is the constant `θ★`
and `μ★` are both derived from, and section 8's master inequality carries it
explicitly.

Section 21.5's shortfall is different in kind and the check distinguishes them:
no bullet is absent, two are **merged** into one entry.

Two things improved against A-U.2d.7. Section 17's six `NO-GO` headings match the
ledger's six exactly — the gap that round had is closed. And the ledger no longer
declares a `status` or a `next` field, so its disagreement with the constants
frontier cannot recur.

## Finding 3, which is an improvement — two manifests that agree

`CHECKSUMS.sha256` is new. It lists every file in the bundle except itself,
including the validation record; the validation record lists the seven content
files; every digest in both reproduces; and the two agree on every file both
name. Exactly one file is covered by neither — `CHECKSUMS.sha256` itself — and
the validation record's `scope_note` says so in as many words.

That is the direct answer to what RUN-033 found at item 51, where a shipped
manifest covered only the files that could not change. Reporting an improvement
is the same obligation as reporting a defect, and this one is unambiguous.

The validation record's `files` key is a **list** again, after being a dict at
item 53 — dict, list, list, dict, list across five bundles. The reader handles
all three shapes and names which one it used.

## The floors that come from the round I verified last week

Section 15 computes, from the current verification floor `Y_ver = 2075·2^60`,
how long an outer interval must be before a chain of depth `r` is possible —
using **A-U.2d.7's Theorem 7.1**, whose `X_r` root RUN-035 verified. This is the
first place in the sweep where one round's published numbers are recomputable
from the previous round's theorem, and they recompute: the floor integer is
exact, `√(3 ln2·Y_ver)` and `log₂Y_ver` are the exact nearest doubles, and the
depth table lands within two ulps throughout.

One detail is worth naming. The paper tabulates from `r ≥ 9` and calls the
inversion "sharper" there. The inversion is in fact already sharper from `r = 8`,
and the `r ≥ 9` label belongs to A-U.2d.7's **Corollary 7.2**, not to its
Theorem 7.1, which carries no depth restriction. The checker publishes an `r = 5`
row that is correct arithmetic but weaker than the high-source route, so it is
not the binding constraint there. Nothing is wrong; a hypothesis has migrated one
result to its left.

---

<!-- BEGIN GENERATED measured block: python code/src54_emit_report_block.py -->

**Sections 3, 4 and 5 on real orbits.** Every row is decided in exact rational arithmetic. No logarithm and no Gamma function is evaluated anywhere in this table.

| what | measured against | value |
| --- | --- | --- |
| accelerated segments from 1249 orbits | longest `L` = 51, largest source = 425645 | `32207` |
| …**violations of Theorem 3.1** `z/y = (3^L/2^Q)·∏(1+1/(3Y_j))` | exact Fractions, must be zero | `0` |
| …where the `2^(−D)` form differs from the `3^L/2^Q` form | the same thing, since `2^(βL) = 3^L` | `0` |
| segments meeting §4's premise | source is the segment minimum and the states are distinct; 0 and 0 fail | `32207` |
| …**violations of Theorem 4.1** `𝒫 ≤ 𝒫(y,L)` | checked on all 32207 of them | `0` |
| …sorted states falling below `y + 2k` | the bound the envelope rests on | `0` |
| **Theorem 5.1** segments where the Gamma form ≠ the product | as an exact Pochhammer quotient | `0` |
| …designed `(y,L)` pairs, largest `L` = 400 | exact disagreements: 0 | `56` |
| …**disagreeing with `math.lgamma` beyond its cancellation bound** | worst error `9.413e-11`, which is `0.17×` the bound the subtraction costs | `0` |

The shipped checker reports `max_gamma_log2_abs_error = 3.114154424783966e-10` for this identity. This run's error is `0`, because for integer `L` the Gamma quotient **is** the Pochhammer product and there is nothing to compare.

**Theorem 9.1's premise, measured.** 9.1 is Theorem 7.2 rearranged, and 7.2 descends from the inherited `y_r > 2^H y_1` and `z_1 > y_r`. Those describe the hypothetical divergent orbit, not a real one.

| premise | of | met |
| --- | --- | --- |
| §4's packing premise | 24010 chains | `24010` |
| **`z_1 > y_r`**, the outer endpoint above the innermost source | 24010 chains | `0` |
| `y_r ≥ y_1 + 4(r−1)`, the `3 (mod 4)` source spacing | 24010 chains | `23482` |
| **the endpoint-gap premise** `z_1/y_1 > 1 + (4r−2)/y_1` | 24010 chains | `0` |
| every premise at once | 24010 chains | `0` |

So Theorem 9.1 was applied to **0** chains. It was not tested here and this run does not claim otherwise. What *is* universal and was checked on all **24010** chains is the round's algebra: `1 + (4r−2)/y₁ < 𝒫` and `r < ½ + y₁(𝒫−1)/4` are one inequality, and they disagreed on `0` of them. The low-source regime `3 ≤ y₁ ≤ L` is attained by `4048` chains, so the regime itself is not vacuous; the premise above it is.

**Sections 5.2 and 9.2 as implications**, over `36` grid points in `(y, L)` of which `14` are in the low-source regime:

| derivation | violations |
| --- | --- |
| **Theorem 5.2** sharp: `R ≤ 1/(3y ln2) + ln(1+2L/y)/(6 ln2)` | `0` |
| **Theorem 5.2** coarse: `R < L/(3y ln2)` | `0` |
| **Corollary 9.2** follows from the exact cap of 9.1 | `0` |
| …and its inversion `y₁ > c_H(r−½)^(6/5)L^(−1/5)` | `0` |
| `μ★ = (6θ★−1)/5` as stated | `0` |
| the old exponent is `θ★/(1+θ★)` | `0` |

**Section 15's floors, recomputed from A-U.2d.7 — the round RUN-035 verified.** `Y_ver = 2075·2^60 = 2392312122059207475200` recomputes exactly: `True`. Each row is `X_r·√Y_ver` with `X_r` the positive root of `ax²+bx = r−1`, compared against the published double by bracket, never by rendering a decimal.

| depth `r` | published | ulps from the nearest double |
| --- | --- | --- |
| `5` | `50659991084.41252` | `1` |
| `9` | `81834819965.94533` | `2` |
| `10` | `88452959345.04712` | `1` |
| `100` | `367019933202.2054` | `0` |
| `1000` | `1247567355004.7424` | `1` |
| `1000000` | `40681166142272.65` | `1` |

`√(3 ln2·Y_ver)` is `0` ulps from its published value and `log₂Y_ver` is `0`. The inversion first becomes **sharper** than the high-source route at depth `8`; the paper tabulates from `r ≥ 9`, and the checker's `r = 5` row is correct arithmetic that is not the binding constraint there.

**Constants.** `θ★` and `μ★` are exactly rational: `θ★ = 2500/12791` and `μ★ = 2209/63955`, both determined by `ρ★ = 4.1164`.

| constant | published | exact | ulps |
| --- | --- | --- | --- |
| `theta_star` | `0.19544992572902825` | `2500/12791` | `1` |
| `mu_star` | `0.03453991087483388` | `2209/63955` | `2` |
| `new_dense_overlap_exponent` | `0.19544992572902825` | `2500/12791` | `1` |
| `old_dense_overlap_exponent` | `0.1634948662611994` | `2500/15291` | `0` |
| `C_H` | `0.33551748694149397` | `e^(1/9) * 3^(1/6) / 4` (0.3355174869414939) | `0` |
| `c_H` | `3.7080177783204333` | `C_H^(-6/5)` (3.7080177783204337) | `-1` |

The drift is not a mystery. `1/(4.1164+1)` evaluated in float64 reproduces the published `theta_star` bit for bit: `True`; and `(6θ−1)/5` from that float reproduces `mu_star`: `True`. The two rationals were computed in doubles rather than exactly, while the **transcendental** constants — `C_H`, `log₂Y_ver`, `√(3 ln2 Y_ver)` — are the exact nearest doubles.

| the paper prints | verdict |
| --- | --- |
| `C_H` = `0.33551748694149397…` | OVER-PUBLISHED |
| `c_H` = `3.7080177783204333…` | OVER-PUBLISHED |
| `theta_star` = `0.19544992572902825…` | OVER-PUBLISHED |
| `old_dense_overlap_exponent` = `0.1634948663…` | correctly rounded at the last digit |
| `mu_star` = `0.03453991087483388…` | OVER-PUBLISHED |

**The theorem ledger against the paper's own section 21.**

| the paper says | the JSON ledger says | shortfall |
| --- | --- | --- |
| §21.1 proved internally: `17` | `proved_internally`: `14` | `3` |
| §21.2 inherited: `7` | `inherited_internal`: `7` | `0` |
| §21.3 external technical: `5` | `external_technical_input`: `4` | `1` |
| §21.4 external live computational: `1` | `live_computational_input`: `1` | `0` |
| §21.5 heuristic / open: `3` | `heuristic_or_open`: `2` | `1` |

§17's `6` `NO-GO` headings match the ledger's `6` exactly — the gap A-U.2d.7 had is closed. Of §21.3's `5` external inputs the one with no ledger entry sharing a distinctive word is ***inherited irrationality-measure consequence for $\log_2 3$ through $\rho_\star=4.1164$;***. §21.5's three bullets are not missing but **merged** into two entries: `0` bullets have no entry, `0` are undecidable by that test. The ledger no longer carries a `status` (`False`) or a `next` (`False`) field, so A-U.2d.7's disagreement between ledger and frontier cannot recur.

**Two manifests, and they agree.**

| what | measured against | value |
| --- | --- | --- |
| files in the bundle | `CHECKSUMS.sha256` lists 8, the validation record 7 | `9` |
| …digests in `CHECKSUMS` that do not reproduce | must be zero | `0` |
| …digests in the validation record that do not reproduce | must be zero | `0` |
| …**where the two manifests disagree** | on the files both list | `0` |
| …files covered by **neither** | `CHECKSUMS.sha256`; the scope note declares it: `True` | `1` |
| validation-record shape | list of file records (items 51, 52, 54) | `—` |
| a `checker_stdout.txt` is shipped | the first bundle since item 49 without one | `False` |
| the checker's named checks independently confirmed | of 8 under the key `checks`; 5 named as not covered here | `3` |
| defects planted / caught by the check named for each | 1 robustness property; 0 malformed; 2 controls, 2 undisturbed | `25 / 25` |

**Not covered here**, named rather than implied: *low_source_sixth_root_envelope*; *phase_gate_integer_logic*; *interval_mass_identity*; *reset_budget_algebra*; *max_gamma_log2_abs_error*.

Every figure above is emitted by `code/src54_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

Every bracket is imported from `src53_plateau_reset`, certified there rather than
re-derived — `ln 2` from its series with an exact tail, `log₂3` from a bit
length, `√2` from integer square roots. One implementation, not two.

Three of this gate's own errors were caught before publication, and all three
would have produced findings against correct arithmetic.

**The first was a false 75.** Comparing a published double against a rational
bracket by rendering the bracket to a fixed number of decimal places measures the
rendering, not the artifact: `c_H` came back **75 ulps** and `log₂Y_ver`
**78,929**, purely because thirteen and eight places are far coarser than a
double at those magnitudes. Rounding is monotone, so the bracket itself decides —
if `lo` and `hi` round to the same double, that double is the nearest one for
everything between, and if they do not, the honest answer is that the bracket
cannot decide. Both numbers went to `−1` and `0`.

**The second was a false 12.** The `math.lgamma` cross-check compared relative
error, and `ln 𝒫` is a difference of four log-gammas that are individually near
`3×10⁵` and combine to `5×10⁻⁶`. Relative error is meaningless under that much
cancellation; the tolerance has to be the cancellation the subtraction actually
costs. Twelve correct pairs stopped being failures.

**The third was a false 7,091** — Theorem 9.1 applied without its premise,
described above.

Two further problems were performance, not correctness, but both would have
prevented any result at all: the log series was fed `Y_ver ≈ 2.4×10²¹`, where
`u = (x−1)/(x+1)` is `1 − 8×10⁻²²` and eighty terms move nothing while the
intermediate rationals reach `(Y+1)¹⁶¹`; and every transcendental bracket was
carrying `9¹²⁰·120!` underneath into the next series. Range reduction by powers
of two fixed the first, and widening each bracket back onto a fixed denominator
fixed the second. A bracket only ever grows under widening, so it stays valid.

The drill's first pass returned **20 of 24**, and all four were classified
**malformed** rather than missed — the pre-flight distinguishing "the defect was
never planted" from "the check failed to catch it", which is the only reason the
count is informative. One inverted the packing envelope below `1` and made
`ln_bracket` assert, breaking the interpreter rather than the result. The other
three mutated branches unreachable on real data: every bracket in this run
decides, so the code path for one that cannot was never exercised.

Both are worth more than a re-aim. The first exposed a **vacuous check** —
`envelope_below_one` could never fire, since every factor of the product exceeds
one, so it was a counter that could only ever read zero and it is now gone. The
second exposed an instrument that was only ever pointed at the subject: the
brackets had no test of their own. There is now an eight-part self-check with
named failures — `ln 2` from `ln_bracket` must contain the certified bracket,
`ln 4` must be twice it, `exp(ln 2)` must contain `2`, `∛8` must contain `2`,
widening must contain its input — and defects are aimed at it. A range reduction
that divides by three now has somewhere to be caught.

The second pass then taught its own distinction. A defect that truncates the
exponential series to two terms was caught, but not by the containment check I
had named for it — and rightly so. A two-term bracket is **wide, not wrong**: it
still contains the true value, so no containment test can see it. What a bracket
too wide to be useful breaks is *decidability*, and that is where the run caught
it. Precision loss and incorrectness are different failures and want different
checks; naming the wrong one would have scored a working guard as a miss.

## What the checker claims and this run did not check

The report names its checks under `checks`. Three are independently confirmed
here — the product identity, the packing envelope, and the Gamma representation.
The rest are **named** in the log rather than waved at: the sixth-root envelope,
the phase-gate integer logic, the interval-mass identity, and the reset-budget
algebra.

The checker's own scope warning — that it instantiates no divergent orbit and
proves neither Collatz nor linear B-density nor the effective Diophantine
constant nor any asymptotic conclusion — is intact and correct.

## Route map

`ROUTE_MAP v2.8`. The constants frontier names item 55 as
`A-U.2d.9 — Orbit-Packing Deficit Rigidity`.

## What this run does not claim

1. That Theorems 6.1, 7.1, 7.2, 8.1, 9.1 or 9.2 hold. Their premises are
   B-survival properties; no real chain met the endpoint-gap premise, and none
   is a test. Their **derivations** were checked; the theorems were not.
2. That real chains failing 9.1's conclusion is evidence against it. It is what
   the absent premise predicts.
3. That the interval-mass theorem (§13) or the root-source floor (§14) hold.
   Only their constants and the relations between them were recomputed.
4. That `θ★` is the correct dense-overlap exponent. This run checked that the
   published value equals `1/(ρ★+1)` and that `μ★ = (6θ★−1)/5`; the derivations
   that produce those relations were not checked.
5. That the consecutive-odd packing envelope is dynamically attainable. The
   round says explicitly it is not, and lists that among its own open problems.
6. That the shipped checker is correct. It was read, never run.
