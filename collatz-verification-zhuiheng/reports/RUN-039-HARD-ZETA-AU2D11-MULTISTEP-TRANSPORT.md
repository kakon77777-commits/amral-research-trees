# RUN-039 — Hard-Zeta A-U.2d.11: an exact rational certificate, which is the first headline number in this sweep that could be checked with no reference of my own

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d11_Multi_Step_Reciprocal_Transport_Rigidity_bundle_v0.1.zip` (source item 58) — 19 sections. Ships a checker, its report, a constants frontier, a theorem ledger, a `CHECKSUMS.sha256`, a source-validation record, and two new things: a **transport-certificates** file and the **builder script** that generated every other artifact.
**Tools:** [`src58_multistep_transport.py`](../code/src58_multistep_transport.py) · [`src58_drill.py`](../code/src58_drill.py) · [`src58_emit_report_block.py`](../code/src58_emit_report_block.py)
**Logs:** [`src58-au2d11.json`](../data/gate-logs/src58-au2d11.json) · [`src58-drill.json`](../data/gate-logs/src58-drill.json)

**Result: this is the most checkable round the sweep has been given. Its headline exponent `1373/25856` is not an estimate but the value of an exact rational dual certificate, and a certificate is verified by checking a finite list of rational inequalities — no tolerance, no sampling, and no reference computation of mine that could itself be the wrong one. All three shipped certificates verify: 294 inequalities, zero violations, every `α` exactly what Corollary 5.3's formula gives, and each level's declared tail cutoff exactly the point where monotonicity takes over. Section 3's transport identity holds on every residue class of every segment. Two findings, both about the machine-readable record rather than the mathematics: the ledger has no list of open problems at all — the first round in the sweep without one — and the builder script, which produced every artifact in the bundle, is the one file no digest pins.**

---

## A number that needed nothing of mine to check

Every previous round in this sweep gave me a bound or a constant, and checking it meant computing a reference and then arguing that my reference was the better one. Item 53's slack comparisons, item 54's Gamma identity, item 57's harmonic capacities — all of them reduce to *my computation against theirs*, and the argument that mine is right is always available to be wrong.

This round does something different. Its exponent comes from a **dual certificate**: a positive potential `a_r` on the units modulo `3^h` and non-negative multipliers `μ_{r,k}` satisfying

> `−3a_r + 2^k a_{T(r,k)} + μ_{r,k} ≥ 1`   for every `r` and every `k ≥ 1`

with `T_h(r,k) = ((3r+1)·2^{−k}) mod 3^h`, after which Corollary 5.3 reads the exponent straight off:

> `α_h = (1/3) Σ_{r,k} μ_{r,k} / (3^h 2^{k+1})`

Both halves are finite and rational. The certificate either satisfies its inequalities or it does not; `α` either equals the published rational or it does not. There is nothing to calibrate.

All three levels verify — 18, 60 and 216 inequalities for moduli 3, 9 and 27 — with zero violations, every potential positive, every multiplier non-negative, and every transition landing back inside the unit group, which is what makes the transport closed at all.

The tail deserves a note. The inequality is stated for *every* `k ≥ 1`, and the multipliers have finite support, so past some point it must hold from the `2^k a_{T}` term alone. That point is computable: the smallest `K` with `2^K a_min − 3a_max ≥ 1`. For the three levels it comes out **4, 5 and 7** — exactly the `tail_k` each certificate declares. The round's own cutoffs are the right ones, and this run computed them rather than accepting them.

`α = 1373/25856` recomputes exactly at level 3, `A = 3α` at every level, and the gain over A-U.2d.10 is exactly

> `η11 = 4/45 − 1373/25856 = 41639/1163520`

which matches the reported float and the frontier's own exact string.

## What else is decidable, and what is not

**Section 3's transport identity** is a flow conservation law per residue class — reciprocal mass arriving in class `b` at one step is the mass leaving it at the next, up to two boundary terms and a cross term. It is exact, needs no hypothesis, and holds on every unit residue of every segment tested.

**Section 4's channel** is a CRT statement: `q(n) = k` together with `n ≡ r (mod 3^h)` selects exactly one class modulo `3^h 2^{k+1}`. Enumerated directly, and the capacity bound `H_{h,k}` that follows was checked on the sorted members of those classes.

**Theorem 5.2** is the exception. Its proof drops a boundary term using `z > y`, which no real segment satisfies — the same premise A-U.2d.10's Theorem 4.1 needed and the same answer. It was measured and applied nowhere.

The drill's positive control here returned something the previous two rounds did not. Deleting the premise gate — applying the certified mass bound to every segment regardless — produces **no violations at all**. At items 54 and 57 the same experiment produced thousands, which is what showed those gates were load-bearing. Here the bound simply has enough slack that its conclusion survives dropping its hypothesis on this data.

That is a fact about the bound, not a hole in the check, and it is worth saying rather than engineering around: the certified mass bound is not tight on real orbits. The defect was made decisive by also tightening the constant a millionfold, at which point a correct check must and does refuse it.

**Section 12's hierarchy** — floating LP values for moduli 81 through 2187 — the round labels diagnostics-only in its own scope warning, and repeats the point as `NO-GO 13.3`. What this run checked is that the diagnostics are internally consistent: each row's product exponent is its reciprocal coefficient over three, the sequence decreases, and the three rows that overlap the *certified* levels agree with the exact rationals.

## Finding 1 — the ledger has no open-problems list

Section 17.4 is headed "Diagnostic / explicitly open" and carries six bullets: the floating LP values, the conjectured `α_h → 0` decay, a general symbolic construction of the dual potentials, uniform-in-`h` control strong enough to select `h = h(L)`, the merger of Highly Nested into Huge Partial Quotients, and the Collatz conjecture.

The JSON ledger's corresponding key is named `diagnostic_only` and contains three entries, all of them diagnostics. The four genuinely **open** items have no machine-readable record — including the Collatz conjecture itself, which is the one entry a downstream reader most needs to see.

A-U.2d.9's ledger carried an `open` list of six; A-U.2d.10's carried one of six. This is the first ledger in the sweep with no open list at all. The key's name is honest about what it holds, which is exactly why the omission is easy to miss: nothing is mislabelled, something is simply absent.

Section 17.1 is short by two as well, and both are substantive: the deterministic transition map `T_h(r,k)` — the definition the entire certificate rests on — and the polynomial deficit relative to A-U.2d.10, which is the round's own statement of what it improved. Section 17.2 goes the other way, splitting seven prose bullets into nine ledger fragments, which is a granularity choice rather than a loss.

## Finding 2 — the builder is the one file nothing pins

The bundle ships `build_AU2d11_artifacts.py`, at 35 KB the largest file in it — larger than the paper — and the script that generated every other artifact. It is the first time the sweep has been given the generator alongside its output.

`CHECKSUMS.sha256` lists nine files and every digest reproduces. It does not list the builder. The source-validation record lists ten files *including* the builder, but carries **no digests at all** — its fields are `utf8`, `lf_only`, `control_chars`, `forbidden_math_delimiters`, `pass`. So the builder's bytes are pinned by nothing in the bundle.

That is the item-51 lesson at its sharpest. A manifest that covers the outputs but not the tool that produced them leaves the provenance chain open at exactly the link that matters: swap the builder and every digest still checks out.

This run **read** the builder and did not run it, on the same principle that has kept every shipped checker unexecuted throughout the sweep.

## The constants

The rounding chain is shorter here than in the last three rounds. `C₁₁ = exp(((Σμ)/7 + Σ μ ln(1+D)/D + 51a_max/98)/3)` — a closed form I had to derive from the proof, since the paper prints only its value — is the exact nearest double, and so is `C₁₁/6`. Only the last two links drift by one ulp, and both reproduce in float64 from the already-rounded parent.

Worth saying plainly: the paper prints `C₁₁` to **twenty** digits and all twenty are correct. Against three consecutive rounds of over-published last digits, that is a change in the right direction.

All five exponents — `7/80`, `99/1472`, `1373/25856`, `4/45`, `41639/1163520` — are the exact nearest doubles, and the three exact rational **strings** the frontier ships reproduce character for character.

---

<!-- BEGIN GENERATED measured block: python code/src58_emit_report_block.py -->

**The three dual certificates, checked exactly.** A level-`h` certificate must satisfy `−3a_r + 2^k a_{T(r,k)} + μ_{r,k} ≥ 1` for every unit `r` mod `3^h` and every `k ≥ 1`. The tail is not assumed: past `K` with `2^K a_min − 3a_max ≥ 1` the inequality holds from the transport term alone, and `K` is computed.

| level | modulus | units | multipliers | declared `tail_k` | computed | inequalities | violations | `α_h` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `3` | `2` | `4` | `4` | `4` | `18` | `0` | `7/80` |
| `2` | `9` | `6` | `8` | `5` | `5` | `60` | `0` | `99/1472` |
| `3` | `27` | `18` | `18` | `7` | `7` | `216` | `0` | `1373/25856` |

| what | measured against | value |
| --- | --- | --- |
| certificate inequalities checked | across 3 levels | `294` |
| …**violations** | exact rationals, must be zero | `0` |
| potentials not positive / multipliers negative | Definition 5.1 requires both | `0 / 0` |
| units with no potential listed | the certificate must be total | `0` |
| …**transitions leaving the unit group** | `T(r,k)` must stay coprime to 3, or the transport is not closed | `0` |
| multipliers beyond the declared tail | must be zero | `0` |
| levels whose computed tail exceeds the declared one | the declared `tail_k` must actually suffice | `0` |
| …**`α` disagreeing with Corollary 5.3** | `α_h = (1/3)Σ μ_{r,k}/(3^h 2^{k+1})`, exactly | `0` |
| …`A` not three times `α` | must be zero | `0` |
| …checker report disagreeing with the certificate file | modulus, tail, `A` and `α` compared field by field | `0` |

The strongest certified exponent is `1373/25856`, which the checker report agrees with (`True`), and the exponents decrease with level (`True`). The gain over A-U.2d.10 recomputes as `η11 = 4/45 − α = 41639/1163520`, matching the reported float (`True`).

**Section 3's transport identity and section 4's channel, on real orbits.**

| what | measured against | value |
| --- | --- | --- |
| segments from 1499 orbits | longest `L` = 51 | `38101` |
| residue transport identities checked | one per unit residue mod 27 per segment | `685818` |
| …**violations of Theorem 3.1** | exact Fractions, must be zero | `0` |
| …states outside the unit group | A-U.2d.9's sieve, re-verified here | `0` |
| …**meeting `z > y`**, the premise Theorem 5.2 needs | a first-crossing endpoint is where the slack drops | `0` |
| channels checked | `q(n)=k` and `n≡r (mod 3^h)` by CRT | `18` |
| …**not selecting exactly one class mod `3^h 2^{k+1}`** | must be zero | `0` |
| …modulus disagreeing with `3^h 2^{k+1}` | must be zero | `0` |
| …capacity windows / violations of `H_{h,k}` | sorted members of one class, all at least `y` | `54 / 0` |

| what | measured against | value |
| --- | --- | --- |
| Theorem 5.2 applied / violated | premise-gated on `z > y` | `0 / 0` |
| low-source segments `7 ≤ y ≤ L` | of 38101 | `141` |
| …**violations of the uniform mod-27 envelope** | `𝒫 < C₁₁(L/y)^{1373/25856}` | `0` |
| hierarchy rows read | section 12's floating diagnostics | `7` |
| …where the exponent is not the coefficient over three | must be zero | `0` |
| …not decreasing in `h` | must be zero | `0` |
| …**certified levels disagreeing with the diagnostic** | `h = 1, 2, 3` appear in both and must agree | `0` |
| the report labels the floating hierarchy diagnostic-only | its own scope warning | `True` |

**Constants, against their closed forms.**

| constant | published | closed form | ulps |
| --- | --- | --- | --- |
| `C11_uniform_product` | `6.0763970012888` | `exp(((sum mu)/7 + sum mu ln(1+D)/D + 51 a_max/98)/3)` | `0` |
| `C11_depth` | `1.0127328335481334` | `C11/6` | `0` |
| `c11_source_inversion` | `0.98672687648103` | `(C11/6)^(-25856/24483)` | `1` |
| `theta_star` | `0.19544992572902825` | `1/(rho+1)` | `1` |
| `alpha_mod3` | `0.0875` | `7/80` | `0` |
| `alpha_mod9` | `0.06725543478260869` | `99/1472` | `0` |
| `alpha_mod27` | `0.05310179455445545` | `1373/25856` | `0` |
| `alpha10` | `0.08888888888888889` | `4/45` | `0` |
| `eta11` | `0.035787094334433445` | `4/45 - alpha_27` | `0` |
| `dense_root_source_floor_exponent_mu11` | `0.15033097576480636` | `(theta-alpha)/(1-alpha) = 47077957/313162053` | `1` |

The three exact rational strings the frontier ships reproduce: `alpha_mod27_exact` True, `A_mod27_exact` True, `eta11_exact` True.

The chain is shorter this round — the root `C₁₁` is the exact nearest double and so is `C₁₁/6` — but the last two links still drift, and reproduce in float64 from the already-rounded parent: `C₁₁/6` gives the published depth constant (`True`), that to the `−25856/24483` gives `c₁₁` (`True`), and the float64 `θ★` and `α` through `μ11`'s formula give `μ11` (`True`).

| the paper prints | verdict |
| --- | --- |
| `alpha10` = `0.088888…` | truncated rather than rounded at the last digit |
| `alpha_mod9` = `0.0672554347…` | truncated rather than rounded at the last digit |
| `alpha_mod27` = `0.05310179455445545…` | correctly rounded at the last digit |
| `eta11` = `0.035787094334433445…` | OVER-PUBLISHED |
| `C11_uniform_product` = `6.0763970012888005265…` | truncated rather than rounded at the last digit |
| `C11_depth` = `1.0127328335481334…` | exact to every published digit |
| `c11_source_inversion` = `0.9867268764810297…` | OVER-PUBLISHED |
| `mu11` = `0.15033097576480636…` | OVER-PUBLISHED |
| `theta_star` = `0.19544992572902825…` | OVER-PUBLISHED |
| `relative_deficit_vs_P_RF` = `5.102553714775606…` | exact to every published digit |
| `mu8_from_AU2d8` = `0.0345399108…` | truncated rather than rounded at the last digit |
| `mu9_from_AU2d9` = `0.0948811664…` | exact to every published digit |
| `mu10_from_AU2d10` = `0.1169572356…` | correctly rounded at the last digit |

**The manifests.**

| what | measured against | value |
| --- | --- | --- |
| files in the bundle | `CHECKSUMS.sha256` lists 9, the validation record 10 | `11` |
| …digests that do not reproduce | must be zero | `0` |
| **validation records carrying a digest at all** | its fields are `control_chars`, `forbidden_math_delimiters`, `lf_only`, `pass`, `utf8` | `0` |
| …listed in the validation record but not in `CHECKSUMS` | build_AU2d11_artifacts.py | `1` |
| …**files with no digest anywhere** | CHECKSUMS.sha256, build_AU2d11_artifacts.py | `2` |
| the artifact builder is shipped / has a digest | it generated every other artifact in the bundle | `True / False` |
| the checker's named checks independently confirmed | of 5; 2 named as not covered here | `3` |
| this run's own bracket self-checks | 0 failed | `10` |
| defects planted / caught by the check named for each | 1 robustness property; 0 malformed; 2 controls, 2 undisturbed | `33 / 33` |

**The ledger against the paper's own section 17.**

| the paper says | the JSON ledger says | shortfall |
| --- | --- | --- |
| §17.1 proved internally: `11` | `proved_internal`: `9` | `2` |
| §17.2 inherited: `7` | `inherited_internal`: `9` | `-2` |
| §17.3 external grounding: `3` | `external_grounding`: `3` | `0` |
| §17.4 diagnostic / explicitly open: `6` | `diagnostic_only`: `3` | `3` |

The paper carries `6` `NO-GO` headings (`13.1, 13.2, 13.3, 13.4, 13.5, 13.6`).

**Not covered here**, named rather than implied: *actual_suffix_minimum_growing_segments*; *uniform_low_source_segments*.

Every figure above is emitted by `code/src58_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

Brackets come from `src53`, `src54` and `src55`, certified there. One of this gate's own errors is worth recording because the wrong fix was so available.

Computing `(L/y)^{1373/25856}` through `_pow_bracket` means raising to the **1373rd power** and then bisecting a **25856-th root** of a number with a thousand digits. The gate took eight minutes and could not reach a population that satisfied its own guards. The tempting response — the one I have now watched myself reach for twice — is to lower the guard until the population it already had looks sufficient.

The right fix was arithmetic: `x^{p/q} = exp((p/q) ln x)`, using two brackets that were already certified. Eight minutes became twenty seconds, and the guards were met rather than adjusted. Fractional powers with large numerator and denominator want the logarithm, and that is now a helper rather than a lesson.

The other correction was smaller and caught by an assertion I had written for exactly that purpose: the reciprocal `1/(C₁₁/6)` is below one, where the log series wants an argument at least one, so the helper now takes the reciprocal and flips which end of the bracket it returns.

## What the checker claims and this run did not check

The report names five checks. Three are independently confirmed here — the exact dual inequalities, the residue transport equalities, and the harmonic capacity tests. The other two are **named** in the log: the suffix-minimum growing-segment sample and the uniform low-source segment sample.

The checker's scope warning is unusually careful and is correct as written: the `h = 1, 2, 3` rational certificates are theorem inputs, the `h ≥ 4` floating values are diagnostics only, and no divergent orbit, linear B-density or Collatz theorem is asserted.

## Route map

`ROUTE_MAP v2.11`. The constants frontier names item 59 as
`A-U.2d.12 — 3-Adic Transport Hierarchy Closure`, which the open list says is where `α_h → 0` would have to be proved.

## What this run does not claim

1. That Theorem 5.2 holds. Its premise `z > y` is met by no real segment; it was measured and applied nowhere.
2. That `α_h → 0`. The floating hierarchy suggests it, the round says it is not proved, and `NO-GO 13.5` forbids reading the deeper values as a proof of exponent zero.
3. That the certificates are *optimal* duals. What was verified is that they are **valid** — every inequality holds and the exponent formula evaluates as published. A better certificate at the same modulus would give a smaller `α`, and nothing here rules one out.
4. That the mod-27 envelope's constant `C₁₁` is the best available. It was recomputed from the proof's own steps and matches to twenty digits; whether the steps are tight was not tested.
5. That the dense-support source floor (§10) holds. Only its exponent and the relation it comes from were recomputed.
6. That the shipped checker or the shipped builder is correct. Both were read, neither was run.
