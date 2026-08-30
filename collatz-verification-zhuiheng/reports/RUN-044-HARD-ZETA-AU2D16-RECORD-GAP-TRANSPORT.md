# RUN-044 — Hard-Zeta A-U.2d.16: the round where the central coordinate turns out to be an integer identity

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d16_Critical_Record_Gap_Transport_Rigidity_bundle_v0.1.zip` (source item 63) — 19 sections. Ships a checker report, a constants frontier, a theorem ledger, a route map, literature notes, a `CHECKSUMS.sha256`, a source-validation record, a verification script, and two new files: a bundle `README` and a `checker_stdout.txt`.
**Tools:** [`src63_record_gap_transport.py`](../code/src63_record_gap_transport.py) · [`src63_drill.py`](../code/src63_drill.py) · [`src63_emit_report_block.py`](../code/src63_emit_report_block.py)
**Logs:** [`src63-au2d16.json`](../data/gate-logs/src63-au2d16.json) · [`src63-drill.json`](../data/gate-logs/src63-drill.json)

**Result: the mathematics verifies, on the largest real populations this sweep has had in a dozen rounds. The reason is a coordinate change the paper does not spell out: the correction bank `𝒜_n = 2^{−δ_n}Y_n` is exactly `2^{K_n}Y_n/3^n`, because `2^{βn} = 3^n` — so its monotonicity, which Theorem 5.1 rests entirely on, is the integer identity `2^{K_{n+1}}Y_{n+1} − 3·2^{K_n}Y_n = 2^{K_n}`, with no `β` and no bracket anywhere. Checked on 123,005 steps: zero violations. Consecutive suffix minima are plentiful on finite windows, so Lemma 4.1, the ratio cap, interior slack domination, the fully suffix-supercritical tail (11,305 suffixes), the exact tail identity, the value-peak span, both sides of the valuation transport and both landing phases all have genuine populations — 4,069 gaps, zero violations across every one. The two explicit bridges the paper ships in NO-GO 13.7 rebuild exactly from the map, phases included. Three findings, all about the bundle rather than the mathematics: `checker_stdout.txt` is byte-identical to the checker report it sits beside, the source-validation record names four files and digests none of them, and `3−β` is published exact while `2−β` — the same subtraction — is two ulps out.**

---

## The coordinate that makes this round checkable

Section 5 turns on A-U.2d.4's correction bank

> `𝒜_n := 2^{−δ_n}Y_n`,  with  `𝒜_{n+1} − 𝒜_n = (1/3)·2^{−δ_n} > 0`

and everything downstream — Theorem 5.1's interior slack domination, and through it Corollary 5.2's fully suffix-supercritical tail — depends on that increment being right. Written that way it needs `β`, so checking it would mean bracketing `2^{−δ_n}` and arguing about the bracket.

It does not need `β`. Since `δ_n = βn − K_n` and `2^{βn} = 3^n` exactly,

> `𝒜_n = 2^{K_n}·Y_n / 3^n`

and the claimed increment becomes, after clearing denominators,

> `2^{K_{n+1}}·Y_{n+1} − 3·2^{K_n}·Y_n = 2^{K_n}`

which is a statement about integers. It is also immediate once written: `Y_{n+1} = (3Y_n+1)/2^q` and `K_{n+1} = K_n + q`, so the left side is `2^{K_n}(3Y_n+1) − 3·2^{K_n}Y_n = 2^{K_n}`.

Checked on **123,005 steps** across 3,969 orbits: zero violations, zero non-monotone steps, zero increments differing from the claimed value. No logarithm decided any of it.

This matters beyond convenience. Theorem 5.1 is proved *through* the bank — `Y_n > Y_t` plus bank monotonicity gives `𝒜_n < 𝒜_t`, hence `2^{δ_n} > 2^{δ_t}` — so an error in the bank would propagate silently into the paper's central structural claim. Verifying it in integers removes the only place a bracket could have hidden one.

## Consecutive-record gaps, in quantity

The last several rounds have had central theorems conditional on objects a convergent orbit does not supply: RUN-039's `L ≥ y` premise met once in 66,665, RUN-041's B-injections zero in 460,024, RUN-043's record descents zero in 8,447. This round's object is a **consecutive suffix-minimum gap**, and those are everywhere on finite windows.

Across 1,314 orbit windows there are **4,069 gaps with `g ≥ 2`** (longest 38), and every claim about them holds:

- **Lemma 4.1** — the next record lies below every interior state: 0 violations;
- **Theorem 4.2** — the ratio cap `1 < z/y < (3y+1)/(2y)`, exact rationals: 0;
- `q_{s+1} = 1` and `x = (3y+1)/2`: 0;
- **Theorem 5.1** — `δ_n > δ_t` for every interior `n`: 0;
- **Corollary 5.2** — every nonempty suffix of the tail is supercritical, `K_t − K_n > β(t−n)`, on **11,305 suffixes**: 0;
- **Theorem 6.1** — the exact tail identity, written as `z·2^Q = x·3^h·𝒫↓` so no `β` decides it: 0;
- the tail excess `E↓ > 0` and the net record motion `δ_t − δ_s < β − 1`: 0;
- **the value-peak span** `M ≥ z + 3g − 4` from the 6-unit packing: 0.

The transport is equally clean. Theorem 8.1's ascent bound `N₁↑ ≥ (2−β)ℓ↑ + H↑` holds on all 4,069, and its **tightest case has slack exactly 0** — attained, like the analogous bound at RUN-043, so it cannot be passed by accident. The peak never falls at an endpoint (0 of 4,069), which is what makes the two-sided spike well defined.

## The landing phases are exact residue arithmetic, and they hold

Section 9's landing toll is the sharpest small claim in the round:

| `z mod 12` | `z mod 3` | `q_t` | toll |
| --- | --- | --- | --- |
| 7 | 1 | even, `≥ 2` | `≥ 2 − β` |
| 11 | 2 | odd, `≥ 3` | `≥ 3 − β` |

It rests on `z ≡ 2^{−q_t} mod 3`, and since `2 ≡ −1 mod 3` that is `1` for even `q` and `2` for odd — verified directly, and then on real gaps: **3,057 phase-7 endpoints and 1,012 phase-11 endpoints**, with zero violations of the parity, the floor, the mod-3 lemma, or the toll. No landing valuation equalled 1.

The complementary source phase is equally exact: `y ≡ 7 mod 12 ⟹ x ≡ 11 mod 18` and `y ≡ 11 ⟹ x ≡ 17`, which is one line of residue algebra (`(3(12k+7)+1)/2 = 18k+11`) and holds on every gap.

**Both bridges the paper ships in NO-GO 13.7 rebuild exactly.** `(y,x,z) = (71,107,91)` with word `(1,2,2)` and `(223,335,319)` with `(1,1,1,3,2)` — recomputed from the accelerated map rather than accepted: the values, the exponent words, the `q=1` first step, the `y < z <` every interior state geometry, the fully suffix-supercritical tail, and the landing phase. `71 ≡ 11 mod 12` with `107 ≡ 17 mod 18`; `223 ≡ 7` with `335 ≡ 11`. Both land on `z ≡ 7 mod 12` with `q_t = 2`, even and at least 2, as the table requires.

Their checker reports five such examples; the paper publishes two. The three unpublished ones are not verifiable from the bundle.

## Finding 1 — `checker_stdout.txt` is the checker report under a second name

The bundle ships a new file, `checker_stdout.txt`, 2,894 bytes. `Hard_Zeta_AU2d16_checker_report.json` is also 2,894 bytes, and both hash to `8af06b4a1e4c156d…`. They are **byte-identical**.

This is not wrong — a checker that prints its report to stdout produces exactly this — but it adds no verifiable content. A reader who sees a file called `checker_stdout.txt` beside a report JSON reasonably expects a run log: timings, progress, warnings, the things a report omits. What is there is the report.

It is worth naming because of where it came from. RUN-042 found the validation record carrying per-file digests; RUN-043 found those gone and a `checker_stdout_sha256` in their place, and I noted that this pinned the output rather than the inputs. This round ships the output itself — which is the right direction — but the output turns out to be a copy of a file already in the bundle, and the `checker_stdout_sha256` field is gone too.

## Finding 2 — the validation record names four files and digests none

`SOURCE_VALIDATION_AU2d16.json` has a `files` map with **four entries** — the three Markdown documents and the new README — each carrying encoding and delimiter counts and **no `sha256`**. The three JSONs appear only as `*_json_parse: true` booleans in a separate `checks` map, and the verification script only as `checker_python_compile: true`.

Four of the eleven files appear nowhere in it: `CHECKSUMS.sha256`, the validation record itself, `checker_stdout.txt`, and `verify_Hard_Zeta_AU2d16_record_gap_transport.py`.

Coverage is nevertheless intact, because `CHECKSUMS.sha256` lists **10 of the 11** files — everything but itself — and all ten recompute correctly. So nothing in the bundle is unpinned; it is the validation record's own content that has now varied across four consecutive rounds: absent digests (RUN-039–041), present and correct (RUN-042), a stdout digest instead (RUN-043), and now neither.

Its seven `checks` entries are all `true`, including a specific `no_bad_exact_gap_scale_claim` — a self-check against an overclaim the authors evidently guard against by name.

## Finding 3 — the same subtraction, twice, with different last bits

`2 − β` is published as `0.4150374992788439`, two ulps above the nearest double to the true value. `3 − β` is published as `1.415037499278844` and is **exact**.

Both are `k − β` with `β` itself published exactly, and both reproduce their float64 chain at 0 ulps. The difference is magnitude loss: `2 − 1.585` collapses by a factor of 4.8, `3 − 1.585` by 2.1, and only the first is enough to promote `β`'s last-bit rounding into the result. The two published tolls differ by exactly `1.0` in float64, so they remain consistent with each other.

`β − 1` is one ulp low by the same route. The remaining constants — `4/5` and `1/5` — are exact.

<!-- BEGIN GENERATED measured block: python code/src63_emit_report_block.py -->

**The correction bank, in integers.** `A_n = 2^K_n Y_n / 3^n` and the claimed increment is `2^K_{n+1} Y_{n+1} - 3 * 2^K_n Y_n = 2^K_n`, with no `beta` and no bracket. Across 3969 orbits and **123005 steps**: **0** identity violations, **0** non-monotone steps, **0** increments differing from the claimed value. Theorem 5.1 is proved through this coordinate, so it is the one place a bracket could have hidden an error.

**Consecutive-record gaps.** 1314 orbit windows gave **4069** gaps with `g >= 2` (longest 38). Lemma 4.1 **0** violations; Theorem 4.2's ratio cap **0**; `q_{s+1}=1` **0**; `x = (3y+1)/2` **0**; record values non-increasing **0**; Theorem 5.1 **0**; Corollary 5.2 on **11305** tail suffixes **0**; Theorem 6.1's exact identity — written as `z 2^Q = x 3^h P` so no `beta` decides it — **0**; the tail excess non-positive **0**; the net record motion not below `beta-1` **0**; the value-peak span `M >= z+3g-4` **0**.

**Bidirectional transport.** Theorem 8.1's ascent bound was checked on **4069** gaps: **0** violations, tightest slack **0.0** — attained, so it cannot be passed by accident. The peak never fell at an endpoint (**0**) and was always the interior maximum (**0** failures). Theorem 8.2 is labelled an identity and is one, so its two components were checked separately (**0**, **0**); the derived `N_{>=2}` count bound, which is a genuine claim, was exercised on **4069** descents with **0** violations.

**The landing phases.** Across **4069** gaps there were **3057** `7 mod 12` endpoints and **1012** `11 mod 12` endpoints, and none outside those classes (**0**). No landing valuation equalled one (**0**). The parity rule failed **0** times for phase 7 and **0** for phase 11; the toll fell below its floor **0** times; the mod-3 lemma `z = 2^{-q} mod 3` disagreed **0** times; and the source phases `11, 17 mod 18` failed **0** times, with **0** sources outside `7, 11 mod 12`.

**The two bridges NO-GO 13.7 ships, rebuilt from the map.** 2 examples: **0** disagreeing values of `x`, **0** of `z`, **0** exponent words, **0** first steps not of valuation one, **0** geometry violations, **0** tails not suffix-supercritical, **0** landing-phase violations.

| `y` | `x` | `z` | word | `y mod 12` | `x mod 18` | `z mod 12` | `q_t` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 71 | 107 | 91 | `[1, 2, 2]` | 11 | 17 | 7 | 2 |
| 223 | 335 | 319 | `[1, 1, 1, 3, 2]` | 7 | 11 | 7 | 2 |

**Section 10's pigeonhole**, which is the part of that section with content: **0** violations over 400 constructed partitions. There is deliberately no exponent check beside it — `R <= N^(4/5)` forcing `N/R >= N^(1/5)` is `N^4 >= R^5` written twice.

**Constants.** 7 checked: **0** disagree with both readings of their own formula, 4 are the nearest double, 3 are what the same formula gives in float64, 0 brackets could not decide. The two landing tolls differ by exactly one in float64 (1).

| constant | published | nearest double | vs bracket | vs float64 chain |
| --- | --- | --- | --- | --- |
| `beta` | 1.584962500721156 | 1.584962500721156 | exact | exact |
| `beta_minus_1` | 0.5849625007211561 | 0.5849625007211562 | -1 ulp | exact |
| `two_minus_beta` | 0.4150374992788439 | 0.4150374992788438 | +2 ulp | exact |
| `phase7_landing_slack_toll` | 0.4150374992788439 | 0.4150374992788438 | +2 ulp | exact |
| `phase11_landing_slack_toll` | 1.415037499278844 | 1.415037499278844 | exact | exact |
| `controlled_total_renewal_support_exponent` | 0.8 | 0.8 | exact | exact |
| `forced_critical_record_gap_exponent` | 0.2 | 0.2 | exact | exact |

**Artifacts.** 11 files, 10 carrying a `CHECKSUMS` digest, **0** mismatches, **0** manifest lines naming a missing file; the only file with no digest anywhere is `CHECKSUMS.sha256`. Two files carry the same bytes under different names: [["Hard_Zeta_AU2d16_checker_report.json", "checker_stdout.txt"]]. The source-validation record names **4** files and digests **0** of them (0 mismatches), reports `validation_passed = True` with 7 checks and **0** not true, and leaves 4 files unnamed: `CHECKSUMS.sha256`, `SOURCE_VALIDATION_AU2d16.json`, `checker_stdout.txt`, `verify_Hard_Zeta_AU2d16_record_gap_transport.py`.

**Ledger coverage.** The paper lists 16 proved items, 5 open problems and 8 NO-GO headings; the ledger carries 16, 5 and 8, with an `open` key (True). Open items with no trace: none. NO-GO headings with no trace: none. The heuristic deciding those lists has controls at both ends and failed neither (0, 0).

**Their counters beside mine**, keyed on their names rather than mine: 0 of 14 had no counterpart here, and 0 are reported as zero.

| check | theirs | mine |
| --- | --- | --- |
| `record_ratio_cap` | 11713 | 4069 |
| `interior_value_domination` | 11713 | 4069 |
| `bank_monotonicity` | 11713 | 123005 |
| `interior_slack_domination` | 11713 | 11305 |
| `suffix_supercritical_suffixes` | 36433 | 11305 |
| `tail_excess_identity` | 11713 | 4069 |
| `floor_sieved_packing` | 11713 | 4069 |
| `q1_ascent_lower` | 11713 | 4069 |
| `descent_surplus_identity` | 11713 | 4069 |
| `record_gap_value_span` | 11713 | 4069 |
| `landing_phase_toll` | 5873 | 4069 |
| `synthetic_ascent_algebra` | 2300 | 400 |
| `exact_finite_bridge_examples` | 5 | 2 |
| `critical_gap_exponent_arithmetic` | 1 | 400 |

**Instrument self-checks:** 9, 0 failed.

**Drill.** 37 defects planted one at a time, **37 caught**, 0 malformed, 0 missed; 0 were caught only by a counter other than the one aimed at. All 37 anchors matched exactly one place before anything was planted. 2 of 2 controls undisturbed, and the gate came back byte-identical.

<!-- END GENERATED measured block -->

## The instrument

Two things on my side, both found before the drill ran.

**A tautology, again.** My first version of the section 10 check asked whether `1 − κ` equals `1 − κ`. Rewriting it as the substantive step — `R ≤ N^{4/5}` forces `N/R ≥ N^{1/5}` — did not help, because that is `N⁴ ≥ R⁵` written twice. The exponent arithmetic genuinely has no independent content; what section 10 needs beyond it is the pigeonhole (`R` intervals covering `N` steps have one of length at least `N/R`), and that *can* fail. The check is now the pigeonhole alone, with a comment recording why there is no exponent check beside it. This is the third round in which a claim that looked checkable turned out to be a definition restated, and the pattern is worth naming: a step written with an inequality sign is not automatically a claim.

**A comparison keyed on my own vocabulary.** The table putting their checker's counts beside mine reported 11 of 14 as "not reproduced" — which measured my choice of counter names, not my coverage. Keyed on *their* names instead, all 14 have a counterpart. Their populations are larger for most (11,713 gaps against my 4,069, from a wider scan); mine is larger for the bank identity (123,005 against 11,713) and for the exponent grid.

I also treated Theorem 8.2 as what it says it is. It is labelled an *identity*, and it is one: `Q↓ = βℓ↓ + H↓` is the definition of `δ` rearranged and `Σ(q−1) = Q↓ − ℓ↓` is arithmetic, so composing them proves nothing about an orbit. Its two components are checked separately, along with the derived `N_{≥2}` count bound, which is a genuine claim and holds on all 4,069 descents.

**Then the drill found two more, and one of them was mathematics rather than sloppiness.**

The ascent check was written as a two-level guard — a permissive outer test on the upper bracket ends, a strict inner one on the lower. At the tightest case the outer test sits *exactly* at equality and therefore never opens, so raising the inner threshold was invisible: the drill planted `+1` and saw nothing. A bracketed inequality needs one comparison, against the certain lower end of the right-hand side, not two. Flattened, and the same defect now turns it red.

Nothing in the transport section depended on *which* interior point was chosen as the peak. Replacing `max` by `min` moved no counter at all, because every counter it could touch was either a violation count that stayed zero or a population size that does not depend on the choice. That is RUN-043's lesson recurring one round later in a new place: a group of observations needs an invariant somewhere. The peak now has to be the interior maximum, and that is a failure counter.

The third was not a defect in my gate. I planted `2^{−q} mod 3` → `2^{q} mod 3` expecting the missing inverse to show, and it changed nothing — correctly, because `2 ≡ −1 mod 3` has order two, so `2^{−q}` and `2^{q}` are the *same residue*. The inverse in §9's derivation is immaterial at that modulus. The drill's verdict was right and my expectation was wrong; the defect was re-aimed to shift the parity instead.

The drill's totals are in the measured block above. Anchors were pre-flighted to exactly one match each, and the gate was verified byte-identical afterwards.

## What this run does not claim

It does not instantiate a divergent CASP orbit. Every theorem here about a *consecutive suffix-minimum gap* is checked on windows of convergent orbits, where such gaps exist in quantity — but the paper's asymptotic statements (Theorem 10.1's forced `N^{1/5−o(1)}` gap, Theorem 11.1's subpolynomial record values, and the two normal forms of section 12) are conditional on low-current-slack controlled scales that no finite orbit exhibits, and those are not exercised here. It does not verify Theorem 3.1, the floor-robust extension of A-U.2d.12's product theorem, whose `C_ε` every asymptotic step consumes; that inherits an asymptotic result this arm has never certified. It does not certify `ρ★ = 4.1164`, and does not run the bundle's own verification script — every number here was recomputed independently, per the standing rule from item 35.

No Collatz claim is made or implied.
