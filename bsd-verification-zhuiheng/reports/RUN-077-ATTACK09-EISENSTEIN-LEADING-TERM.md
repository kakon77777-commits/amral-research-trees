# RUN-077 — GPT-6's Attack 09, the package: the minus eigenline, the forty cusp paths and λ₈(0) = L₁₁(E ⊗ χ₈, x⁻¹) ≡ 5 (mod 11) reproduced coordinate for coordinate; the Eisenstein data, the Kummer unit's logarithm, the smoothing and adjoint factors and the leading-term algebra recomputed; the theorem read — and what the package settles about RUN-076

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Proof_Attack_09_Eisenstein_Leading_Term`](../data/external/gpt6-proof-attacks/extracted/09/BSD_Proof_Attack_09_Eisenstein_Leading_Term.md), with its [`attack09_result.json`](../data/external/gpt6-proof-attacks/extracted/09/attack09_result.json) and `INPUTS.json` — the seventh GPT-6 package, received 2026-09-13 ([provenance](../data/external/gpt6-proof-attacks/PROVENANCE.json)); its narration had been answered a day earlier at [RUN-076](./RUN-076-ATTACK09-AUXILIARY-CHARACTER.md)
**Tools:** [`src79_attack09_eisenstein_leading_term.py`](../code/src79_attack09_eisenstein_leading_term.py), [`src78_attack09_auxiliary_character.py`](../code/src78_attack09_auxiliary_character.py), [`src70_kurihara_modular_symbols.py`](../code/src70_kurihara_modular_symbols.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src79-attack09-eisenstein-leading-term.json`](../data/gate-logs/src79-attack09-eisenstein-leading-term.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Attack 09's one new number is `λ₈(0) = L₁₁(F, x⁻¹)`, `F = f_E ⊗ χ₈` — the ordinary 11-adic L-function of the twist at the full character `x ↦ x⁻¹` of `Z₁₁^×`, the odd Teichmüller branch at `s = 0`, a non-critical point, which the package itself says is "not the central complex L-value". It is computed mod 11 from the first layer on the **minus** modular symbol `Φ_E⁻` (the condition `v(c,d) + v(−c,d) = 0`, normalised at its first nonzero coordinate, index 3): `S_a = Σ_{b odd} χ₈(b)·Φ_E⁻((8a + 11b)/88)`, `μ_F(a + 11Z₁₁) = α_F⁻¹·S_a` with `α_F = χ₈(11)·α_E ≡ 4`, and `λ₈(0) ≡ Σ_a a⁻¹·μ_F(a + 11Z₁₁) = 4⁻¹·9 ≡ 5`. **This gate rebuilds the minus line from the Manin relations and finds the package's 390-coordinate vector identical; walks the forty paths with its own continued fractions and finds all forty index sequences and all forty symbol values identical; and gets the ten `S_a = (4,9,3,4,3,8,7,8,2,7)`, the ten measures `(1,5,9,1,9,2,10,2,6,10)`, the weighted sum `9` and `λ₈(0) = 5`.** The Hecke relation the measure rests on holds for the twisted symbols at level 121 with `a₁₁(F) = 4`. Also recomputed: `B_{2,χ₈} = 2` and the constant term `−1/2`; the 32 coefficients of `f_β = E₂(1,χ₈)(q) − E₂(1,χ₈)(q¹¹)` and `U₁₁ f_β = −11 f_β` (12 residuals, all 0); the Hecke polynomial `U² + 10U − 11 = (U − 1)(U + 11)`; `ε = 1 + √2`, `N(ε) = −1`, `ε^σ = −ε⁻¹`, `ε²⁴ = 768398401 + 543339720√2 ≡ 1 + 110√2 (mod 121)`, `log₁₁ ε ≡ 55√2 (mod 121)`, `log₁₁ ε/(11√2) ≡ 5 (mod 11)`; `𝒮₅(0) = 26`; the adjoint Euler multiplier `≡ 3`; `A₀D_E ≡ 9`; the leading-term coefficients `[t²] = A₀Cκ₀`, `[t³] = A₀Cκ₁ + A₁Cκ₀ − ½A₀Cκ₀`, Coleman `[t³] = A₀Ca₂`; and the algebra of (20) with `416 = 16·26`. **What the package settles about RUN-076: that round, written from the narration, analysed the central value `L(E, χ₈, 1)` and the even (plus-line) first layer, which vanish — and which the package does not use. Both computations are right about their own objects; RUN-076's inference that the auxiliary form must change is withdrawn there. The two are the same eigenline seen from two sides: RUN-076's minus-line branch `T₉⁻ = 3` for `χ₈` is `−8⁹` times the package's weighted sum `9`. Under the package's own criterion, `λ_D(0) ≢ 0`, evaluated here for every even `D ≤ 100`, `χ₈` passes (and so does `χ₅`, with `λ₅(0) ≡ 8`); only `D = 57, 97` fail.** Loeffler–Rivero's Proposition C1.12 / Theorem C1.13, decency and non-criticality are cited and read; `C`, `n`, `B₂` and `𝔰₁₁` are null in the package and untouched here; the package says "BSD 尚未證明；canonical frontier 不更新".

---

## §3 — the new computation, path by path

The package's table and this gate's, side by side (all values in `F₁₁`; `a⁻¹` is the inverse mod 11):

| `a` | `S_a` (package) | `S_a` (here) | `μ_F` | `a⁻¹` | `a⁻¹μ_F` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 4 | 4 | 1 | 1 | 1 |
| 2 | 9 | 9 | 5 | 6 | 8 |
| 3 | 3 | 3 | 9 | 4 | 3 |
| 4 | 4 | 4 | 1 | 3 | 3 |
| 5 | 3 | 3 | 9 | 9 | 4 |
| 6 | 8 | 8 | 2 | 2 | 4 |
| 7 | 7 | 7 | 10 | 8 | 3 |
| 8 | 8 | 8 | 2 | 7 | 3 |
| 9 | 2 | 2 | 6 | 5 | 8 |
| 10 | 7 | 7 | 10 | 10 | 1 |

`Σ_a a⁻¹S_a = 42 ≡ 9`; `λ₈(0) = α_F⁻¹·9 = 3·9 = 27 ≡ 5`. Under each `S_a`
sit four paths `{∞, (8a + 11b)/88}`, `b ∈ {1, 3, 5, 7}`; the package lists
each path's Manin-symbol indices and value, and this gate's continued
fractions give the same index sequence and the same value for all forty
(e.g. `19/88 → [0, 292, 77, 87, 305, 95, 4]`, value 1; `41/88 →
[0, 195, 329, 338, 296]`, value 9). The package's `Φ_F(0) = 0` (even
character on the odd symbol) is 0 here too. `α_F ≡ 4` is the unit root of
`x² − a₁₁(F)x + 11` with `a₁₁(F) = χ₈(11)·a₁₁(E) = 4`.

The line itself: the package reads the stress-test package's 2-dimensional
Hecke space from `INPUTS.json` and imposes `v(c,d) + v(−c,d) = 0`; this gate
builds the space from the Manin relations at level 389 mod 11, the Hecke
operators at 2, 3, 5 and the minus condition — `65 → 2 → 1`, first nonzero
coordinate 3 — and the two 390-coordinate vectors agree in every
coordinate (284 of them nonzero). The measure's distribution relation,
`Σ_{b=0}^{10} Φ_F((a + 11b)/121) = a₁₁(F)Φ_F(a/11) − Φ_F(a)`, holds for
every `a` on these twisted symbols.

## §2 — the auxiliary form

| the package says | recomputed |
| --- | --- |
| `B_{2,χ₈} = 8Σ_{a=1}^{8} χ₈(a)(a²/64 − a/8 + 1/6) = 2` | 2, and 2 again by `8·Σ χ₈(a)B₂(a/8)` |
| `a₀(f) = −B_{2,χ₈}/4 = −1/2` | `−1/2` |
| `a_n(f) = Σ_{d|n} χ₈(d)d`; `f_β = f(q) − f(q¹¹)`, 32 coefficients | `1, 1, −2, 1, −4, −2, 8, 1, 7, −4, −11, −2, …` identical |
| `U² + 10U − 11 = (U − 1)(U + 11)`, `f_β` the slope-1 refinement | `a₁₁(f) = 1 − 11 = −10`; roots `1, −11` |
| `a_n(f_β) = (−11)^k a_m(f)` for `n = 11^k m`; `U₁₁ f_β = −11 f_β` | `a_{11n}(f_β) + 11a_n(f_β) = 0` for `n = 1..12` |
| decency: `χ₈` even, nontrivial, `χ₈(11) = −1 ≠ 1`, conductor 8 | `χ₈(−1) = 1`, `χ₈(11) = χ₈(3) = −1` |
| `ε = 1 + √2`, `N(ε) = −1`, `ε^σ = −ε⁻¹`, `2` a nonsquare mod 11 | all four |
| `ε²⁴ = 768398401 + 543339720√2 ≡ 1 + 110√2 (mod 121)` | exact, and the residues |
| `log₁₁(ε) = log₁₁(ε²⁴)/24 ≡ 55√2 (mod 121)`, higher terms `≡ 0` | the series to three terms exactly in `Q(√2)`; `u²/2 ≡ 0 (mod 121)`; `55√2` |
| `log₁₁(ε)/(11√2) ≡ 5 (mod 11)` | 5 |

Non-criticality as a statement about `H¹_f(Q, Q₁₁(χ₈)(1)) → H¹_f(Q₁₁, ·)`,
and its equivalence with Loeffler–Rivero's condition, are cited
(Bellaïche–Dasgupta Remark 1.5; Loeffler–Rivero Theorem A4.5) and read.

## §4–§5 — the factors and the extraction

| the package says | recomputed |
| --- | --- |
| `𝒮₅(0) = 5² − χ₈(5)⁻¹ = 26`, `gcd(5, 6·8·389·11) = 1` | 26; coprime |
| adjoint multiplier `(1 − β/α)(1 − β/(11α)) ≡ 1·(1 − 7⁻²) ≡ 3` | 3 |
| `A₀D_E = 26λ₈(0) ≡ 9` | 9 |
| `[t²]` of `C·𝒜(t)·log(1+t)·z†(t)` is `A₀Cκ₀`; `[t³]` is `A₀Cκ₁ + A₁Cκ₀ − ½A₀Cκ₀` | the same three monomials with the same coefficients |
| `Col` first coefficient at `t³`: `A₀Ca₂` | the same |
| (19) ⇔ (1); (20) from (3) with `416 = 16·26` | `h(x, adj(H)ℓ) = det(H)·ℓ(x)` on 200 random instances; the rearrangement exact |

The orders in (18) — class 2, regulator 3 — follow from these coefficients
being nonzero given the accepted inputs `κ† ≠ 0`, `a₂ ≠ 0`, `A₀ ≠ 0`,
`C ≠ 0`; that is what the package proves and what is checked. Lemma 09.4
(the leading-line quotient is frame- and uniformiser-independent) and the
diagonal counterexample `F(X,t) = Xⁿ(t²v + Xw)` are read.

## What it settles about RUN-076

| | RUN-076 (from the narration) | the package |
| --- | --- | --- |
| the quantity | `L(E, χ₈, 1)` and the plus-line first layer (the central value, `s = 1`) | `L₁₁(E ⊗ χ₈, x⁻¹)`: minus line, branch `ω⁻¹`, `s = 0`, non-critical |
| its value | 0 exactly; every even branch 0 mod 11; `L(E, χ₈ψ, 1) = 0` for the order-5 `ψ` | `≡ 5 (mod 11)` |
| the same line? | the minus eigenline built there, index-3 normalisation, `T₉⁻ = 3` | the same vector; `T₉⁻ = −8⁹·9 ≡ 3` |
| the auxiliary form | "replace `χ₈` by `χ₅`" — for the central value | `χ₈` passes its own criterion; so does `χ₅` (`λ₅(0) ≡ 8`) |

The package's criterion on every even `D ≤ 100` prime to 11, `λ_D(0) =
α_F⁻¹Σ_a a⁻¹Σ_b χ_D(b)Φ⁻(a/11 + b/D)` with `α_F = χ_D(11)α_E`: nonzero for
`5, 8, 12, 13, 17, 21, 24, 28, 29, 37, 40, 41, 53, 56, 60, 61, 65, 69, 73,
76, 85, 89, 92, 93`; zero for `57, 97`. (Values at this scale, one unit per
line; nonvanishing is scale-free.) There is no archimedean cross-check for
a non-critical value; what RUN-076 does supply is that the index-3
normalisation of the minus line is a unit multiple (`λ⁻ = 6`) of the
`Ω⁻`-normalised symbol on 14 twists, so the package's "5 is an 11-unit" is
meaningful in the Néron normalisation too — the point its §3.1 flags.

## The labels

| where | what |
| --- | --- |
| §3 | "不能把式 (8) 改成平凡分支的中心值，也不能把它等同於複數 L(F,1)" |
| §1, §7 | "使用已發表的退化定理，並非本輪程式已算出的 cohomology vector"; `C`, `n`, `B₂`, `𝔰₁₁` "尚未完成" |
| §8 | "BSD 尚未證明；canonical frontier 不更新" |
| the output | `C_value`, `n_value`, `B2_coordinates`, `s11` all null; `BSD_proved: false`; `canonical_frontier_updated: false`; scope "not the central complex L-value" |

## A control the minus line turned into a defect

Since RUN-068 the drill has carried a *control* that flips the path sign
convention, `(−1)^i` for `(−1)^{i−1}` in the continued-fraction
decomposition of `{∞, a/n}`, with the note that a plus functional cannot
see it (`(−c:d) = (c:−d)` and the plus functional is even in `d`). The
minus functional is odd in `d`, so the same flip negates every minus
symbol — `S_a = (7, 2, 8, 7, 8, 3, 4, 3, 9, 4)` instead of
`(4, 9, 3, 4, 3, 8, 7, 8, 2, 7)`, `λ₈(0) ≡ 6` instead of `5` — which this
gate, comparing signed values with the package, catches. RUN-076's
minus-line identities are homogeneous and do not see it. The entry is now
a defect named for this check; RUN-068's statement about the plus
functional stands.

## The drill

**341 defects, 341 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 72 controls undisturbed, over 106 checks.

The 7 planted for this gate, each turning `attack09-leading-term` red and nothing else:

| planted defect | went red |
| --- | --- |
| the path's sign alternates as (-1)^i in place of (-1)^(i-1) — invisible to a plus functional (RUN-068's control), but it negates every minus symbol, and Attack 09's forty values are signed | `attack09-leading-term` |
| Attack 09's chi_8 is replaced by the odd character (-8/.) | `attack09-leading-term` |
| the twisted unit root alpha_F is taken as alpha_E instead of chi_8(11) alpha_E | `attack09-leading-term` |
| the moment is taken against x instead of x^-1 | `attack09-leading-term` |
| the Eisenstein refinement is taken at the eigenvalue 1 instead of -11 | `attack09-leading-term` |
| the unit's logarithm is read from epsilon^12, which is not 1 mod 11 | `attack09-leading-term` |
| the smoothing integer is taken as 7, giving 48 instead of 26 | `attack09-leading-term` |


## What this round does not claim

* **Loeffler–Rivero's degeneration is not applied.** That the extra factor
  is `L₁₁(F, σ_t x⁻¹)` in the package's normalisation is the theorem as
  cited; this round checks the number the package computes for it.
* **Decency and non-criticality are read**, with the Kummer-unit
  computation that the package offers as the local input.
* **`λ₈(0) ≢ 0` is a mod-11 statement at the package's scale**, made
  scale-free by the unit relation of RUN-076 §4; no 11-adic digit beyond
  the first is claimed for it.
* **Nothing about `C`, `n`, `B₂`, `𝔰₁₁`, the regulator or `L''(E, 1)`** —
  the package's table of open steps is its own, and this round adds
  nothing to it.
