# RUN-080 — PC-001 (the local GPT-6 line's cross-curve calibration): the rank-0 calibrator 19.a1 rebuilt over Q from the Manin relations — the plus and minus rational eigenlines identical to the line's, five Hecke checks, every first-layer residue — and the archimedean alignment the line lists as not done: both of its modular-symbol periods are Néron periods up to a unit at 11, with λ₀⁺ = 1

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`PC-001-CROSS-CURVE-CALIBRATION.md`](../data/external/gpt6-local-period-calibration/reports/PC-001-CROSS-CURVE-CALIBRATION.md) with its [review record](../data/external/gpt6-local-period-calibration/reports/PC-001-REVIEW.md) and [`calibrator-19a1.json`](../data/external/gpt6-local-period-calibration/data/calibrator-19a1.json) — the first round of the local GPT-6 session's own line, `agent/bsd-period-calibration` in this repository, commit `002e5d5`, branched from this line at RUN-076 and read here by `git archive` ([provenance](../data/external/gpt6-local-period-calibration/PROVENANCE.json)). This line does not edit that branch and does not run its scripts.
**Tools:** [`src82_pc001_calibrator_19a1.py`](../code/src82_pc001_calibrator_19a1.py), [`src15_phase2_anchor.py`](../code/src15_phase2_anchor.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src82-pc001-calibrator-19a1.json`](../data/gate-logs/src82-pc001-calibrator-19a1.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: PC-001 does two things. It derives the cross-curve calibration identity (2), `κ_E = A_0(0)ℓ_0/A_E(0) · B_{E,2}/r_{0,1}`, which is RUN-079's (4.4) with `λ_0 = Col_0` and was checked there; and it builds a rank-0 calibrator at `p = 11`: `E₀ = 19.a1`, `y² + y = x³ + x² − 769x − 8470`, `a₁₁ = 3`, ordinary, with its modular symbols over `Q` from the twenty Manin generators of `P¹(F₁₉)`. Rebuilt here with an independent rational Manin engine — dense exact elimination over `Q`, its own continued fractions, its own point counts — the space has dimension 3, `T₂` has the cusp eigenvalue 0 twice and the Eisenstein eigenvalue 3 once, and the primitive integer plus vector `(2, 0, 6, 6, 3, −3, −6, 0, 0, −6, −6, 0, 0, −6, −3, 3, 6, 6, 0, −2)` and minus vector `(0, 0, 0, 0, 1, 1, 0, …, 0, −1, −1, 0, 0, 0, 0)` are the line's, coordinate for coordinate; both are eigenvectors for `T₃, T₅, T₇, T₁₁, T₁₃` with the point-counted eigenvalues `−2, 3, −1, 3, −4`. At the line's normalisation (plus coordinate 0 ↦ 1, minus coordinate 4 ↦ 1) every residue in its table is reproduced: `α₀ ≡ 3`, `χ₈(11)α₀ ≡ 8`, `Φ⁺(0) = 1`, the ordinary first-layer measures `(10, 6, 3, 10, 3, 3, 10, 3, 6, 10)` summing to `L₁₁(E₀, 1) ≡ 9 = (1 − 3⁻¹)²·1`, the twisted cusp sums `(4, 4, 0, 2, 9, 2, 9, 0, 7, 7)`, `Σ a⁻¹S_a ≡ 10`, `L₁₁(E₀ ⊗ χ₈, x⁻¹) ≡ 8⁻¹·10 ≡ 4`, the wrong-character moment 8, the smoothing `26 ≡ 4`, the adjoint multiplier 7, the product 1, and the distribution relation at level 121 for both measures; and `a₁₁(17.a1) = 0`, the partner the line rejected. Then the supplement. The line writes that its periods "must still be matched to the Kato/adjoint conventions" and declines to identify them with Néron periods. The archimedean half of that is done here as at RUN-076: for the even fundamental `D ≤ 100` with root number `χ_D(−19) = +1`, `L(E₀, χ_D, 1)·√D/Ω⁺(E₀)` from the `a_n` is an exact integer — `1` at `D = 1`, `9` at `5, 17, 28, 61, 73, 85`, `36` at `24, 92, 93` — and the plus-line sums at the line's scale equal these residues **with unit `λ₀⁺ = 1`**: the line's plus normalisation is the `Ω⁺`-normalised modular symbol on the nose, `[0]⁺ = L(E₀,1)/Ω⁺(E₀) = 1`. For the odd `D` with root number `+1`, the ratios `L(E₀, χ_D, 1)√|D| / L(E₀, χ₋₆₈, 1)√68` are the exact rationals `1, 1, 1, 4, 1, 4, 1, 1, 1` (and `0` at `−87, −83, −23`), and the minus-line sums are `2 ×` these residues: one unit `λ₀⁻`. So both normalisations are Néron normalisations up to a unit at 11, and the line's "nonzero mod 11" is nonzero at the Néron scale. Not verified: Loeffler–Rivero's degeneration and the common quotient transport, the construction of `B_{E,2}` and `r_{0,1}` (the line says they are not constructed), the Kato/Coleman/adjoint alignment beyond the archimedean one, and BSD — none of which the line claims.**

---

## §3 — the calibrator

| the line says | recomputed |
| --- | --- |
| Manin dimension 3 over `Q`; `g(X₀(19)) = 1` | 3 (= 2g + 1) |
| `T₂`: cusp eigenvalue 0, Eisenstein 3, separated | cusp space dimension 2, Eisenstein 1 |
| point counts `a₂, a₃, a₅, a₇, a₁₁, a₁₃ = 0, −2, 3, −1, 3, −4` | same |
| plus primitive vector, coordinate 0 is 2 | `(2, 0, 6, 6, 3, −3, −6, 0, 0, −6, −6, 0, 0, −6, −3, 3, 6, 6, 0, −2)`, identical |
| minus primitive vector, coordinate 4 is 1 | `(0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, −1, −1, 0, 0, 0, 0)`, identical |
| Hecke checks at 3, 5, 7, 11, 13 | both lines eigenvectors with the point-counted eigenvalues |
| mod-11 vectors at its normalisation | identical |

| quantity | the line | here |
| --- | ---: | ---: |
| `α₀` (unit root of `x² − 3x + 11`) | 3 | 3 |
| `χ₈(11)α₀` | 8 | 8 |
| `Φ⁺(0)` | 1 | 1 |
| ordinary measures `μ(a + 11Z₁₁)` | `10, 6, 3, 10, 3, 3, 10, 3, 6, 10` | same |
| `L₁₁(E₀, 1) = Σ_a μ = (1 − α₀⁻¹)²Φ⁺(0)` | 9 | 9, both ways |
| twisted sums `S_a` | `4, 4, 0, 2, 9, 2, 9, 0, 7, 7` | same |
| `Σ a⁻¹S_a` | 10 | 10 |
| `L₁₁(E₀ ⊗ χ₈, x⁻¹) = (χ₈(11)α₀)⁻¹·10` | 4 | 4 |
| the moment against `x` instead | 8 | 8 |
| distribution relation at 121, both measures | zero residuals | 20 zeros |
| smoothing `26` | 4 | 4 |
| adjoint multiplier `(1 − 11α⁻²)(1 − α⁻²)` | 7 | 7 |
| product of the three nonzero factors | 1 | 1 |
| `a₁₁(17.a1)` | 0 | 0 |

## §2 — the identity

(2) is RUN-079's Theorem 4.1 with the calibrator's functional `λ_0 = Col_0`
and `e = 1`, `d_0 = 0`, `d_E = 1`; (3) is Attack 09's (20) with
`A_0(0)ℓ_0/r_{0,1}` in place of `log₁₁(12)D_E/(26Cλ₈(0))`. Both were
checked on exact random instances at RUN-079 and RUN-077. The line's
statement that a common quotient transport `q_f` cancels in the ratio of
two consistently projected classes, and its refusal to set `q_f = 1`, are
the same gauge statement as RUN-079 §7. The review record's CONCUR /
CHALLENGE disposition — concur on the projected-ratio lemma, challenge to
identifying the constant with a raw leading coefficient — is read and is
consistent with what this line found.

## The supplement — both periods are Néron periods up to a unit

`Ω⁺(E₀) = 0.453253244496` (Δ = −19, one real component). Even `D`, root number `χ_D(−19) = +1`:

| `D` | `L(E₀, χ_D, 1)·√D/Ω⁺` | plus-line sum `S_D` at the line's scale |
| ---: | ---: | ---: |
| 1 | **1** | 1 |
| 5, 17, 28, 61, 73, 85 | 9 | 9 |
| 24, 92, 93 | 36 | 3 (`≡ 36`) |

Odd `D`, root number `+1`, ratios to `D = −68` (the imaginary period cancels):

| `D` | ratio `L(χ_D)√|D| / L(χ₋₆₈)√68` | minus-line sum `S_D` |
| ---: | ---: | ---: |
| −68, −47, −43, −35, −20, −7, −4 | 1 | 2 |
| −39, −24 | 4 | 8 |
| −87, −83, −23 | 0 | 0 |

`λ₀⁺ = 1` on 10 nonzero pairs; `λ₀⁻ = 2` (the minus sum at the reference)
on 9 nonzero pairs, zero sets included. The archimedean alignment the
line's §3 says must still be done is therefore done; what remains is the
line's own list — the Kato, Coleman and adjoint transports, which are not
archimedean and which this line does not reach.

## The labels

| where | what |
| --- | --- |
| §2 | "它們仍要求真正構造 B_{E,2} 與 r_{0,1}。本輪沒有以式 (1) 反向定義這兩個輸入" |
| §3 | "這不是對某一 isogenous curve 的 Neron period 數值作未聲明的換算"; "Kato/Coleman/adjoint 規範必須與這兩條模符號 period 對齊" |
| §5 | "真實 BF 類、C 的數值、s11 及完整 BSD 結論仍未產出" |
| the review | CONCUR on the conditional lemma; CHALLENGE on identifying its constant with the raw ES coefficient |
| the output | `actual_BF_family_computed: false`, `C_computed: false`, `s11_computed: false`, `BSD_proved: false` |

## The drill

**374 defects, 374 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 81 controls undisturbed, over 111 checks.

The 7 planted for this gate, each turning `pc001-calibrator` red and the checks listed:

| planted defect | went red |
| --- | --- |
| PC-001's plus line is normalised at coordinate 2 instead of coordinate 0 | `pc001-calibrator`, `pc002-relative-regulator` |
| PC-001's twisted unit root is taken as alpha_0 instead of chi_8(11) alpha_0 | `pc001-calibrator` |
| PC-001's moment is taken against x instead of x^-1 | `pc001-calibrator` |
| PC-001's smoothing integer is taken as 3, giving 10 instead of 26 | `pc001-calibrator` |
| the Eisenstein T_2 eigenvalue at level 19 is looked for at 2 instead of 3 | `pc001-calibrator`, `pc002-relative-regulator` |
| PC-001's measure has its second term added instead of subtracted | `pc001-calibrator` |
| the calibrator's twisted L-series are cut at e^-5, so no value is a rational | `pc001-calibrator` |


## What this round does not claim

* **The degeneration (1) and its common `C_π`** — Loeffler–Rivero as cited;
  read.
* **`B_{E,2}`, `r_{0,1}`** — not constructed by the line, not here.
* **The Kato/Coleman/adjoint alignment** — only the archimedean alignment
  is supplied; the line's statement stands for the rest.
* **Nothing about `𝔰₁₁` or BSD.**
