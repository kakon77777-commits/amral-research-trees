# RUN-073 — GPT-6's Attack 06: the local multiplier 16 recomputed in Q(α), its adjugate identities and Sen matrix checked, and its complex-side Mellin formula evaluated with this tree's own a_n — L''(E,1)/2 = 0.7593165002884 to 14 digits, the first computation of that value in this tree

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Proof_Attack_06_Balanced_Determinant_Descent`](../data/external/gpt6-proof-attacks/extracted/06/BSD_Proof_Attack_06_Balanced_Determinant_Descent.md), with its [`attack06_result.json`](../data/external/gpt6-proof-attacks/extracted/06/attack06_result.json) — the fourth GPT-6 package
**Tools:** [`src75_attack06_scalar_and_mellin.py`](../code/src75_attack06_scalar_and_mellin.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src75-attack06-scalar-and-mellin.json`](../data/gate-logs/src75-attack06-scalar-and-mellin.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Attack 06 fixes normalisations, proves under listed inputs that the derived Kato class is `κ† = 16·𝔰₁₁·adj(H)ℓ` with `𝔰₁₁ ∈ Z₁₁^×` unknown, shows that lifting the whole cyclotomic first jet to an ordinary motive fails at the Hodge–Tate condition, and writes down the complex target as a Mellin integral. **The finite content all recomputes.** In `Q(α)` with `α² + 4α + 11 = 0`: `e₁₁ = (1 − α⁻¹)² = 214/121 + (26/121)α`, `c_α = 107/88 + (13/88)α`, `θ = c_α/11`, and `e₁₁/θ = 16 = 11 − a₁₁ + 1` exactly — the document's values to the fraction; Hensel-lifting `α` to `11⁸` gives `33341821` and the residues `e₁₁ ≡ 5`, `θ ≡ 1`, identical to its output. Lemma 3.1's two identities (`adj(H + c·llᵀ)l = adj(H)l`, `det(H + c·llᵀ) = det H + c·lᵀadj(H)l`) and the basis-change law `det(AᵀHA) = (det A)²det H` hold on 500 random integer instances; the Sen matrix `[[0,1],[0,0]]` is nonzero with square zero. **And the formula it states for the complex side — `L''(E,1)/2 = (2π/√389)∫₁^∞ f_E(iy/√389)(log y)² dy` — evaluated with `a_n` from this tree's own point counts (`a₃₈₉ = +1` counted on the node) gives `L(E,1) = −2.5·10⁻¹⁶` and `L''(E,1)/2 = 0.759316500288408`, against the `0.759316500288427` the corpus stated and RUN-023 took as input: relative difference `2.5·10⁻¹⁴`, quadrature noise.** RUN-023 verified the rank-2 BSD identity with that number as given; this round is the first time this tree has computed it. What the document leaves open it leaves open: `𝔰₁₁` is not computed, and the bridge BD6 — a rational element whose 11-adic realisation is `𝔰₁₁·b` and whose real regulator is the Mellin integral — is labelled "未證".**

---

## §2 — the multiplier, in the number field

`Q(α)` is represented as `u + vα` with `α² = −4α − 11`; inverses go through
the conjugate `α ↦ −4 − α`.

| quantity | this round | the document |
| --- | --- | --- |
| `α + β`, `αβ` | `−4`, `11` | `−4`, `11` |
| `e₁₁ = (1 − α⁻¹)²` | `214/121 + (26/121)α` | same |
| `c_α = (1 − α⁻¹)(1 − β⁻¹)⁻¹` | `107/88 + (13/88)α` | same |
| `θ = c_α/11` | `107/968 + (13/968)α` | same |
| `e₁₁/θ` | **16**, exactly | 16 |
| `11 − a₁₁ + 1` | 16 | 16 |
| `α mod 11⁸` (Hensel from 7) | 33341821 | 33341821 |
| `e₁₁`, `θ mod 11⁸` | 58539629, 43851017 | same |
| `e₁₁`, `θ mod 11` | **5, 1** | 5, 1 |

Lemma 2.2's identity `11(1 − α⁻¹)(1 − β⁻¹) = 11 − a₁₁ + 1` is `#E(F₁₁)` for any
good ordinary prime; the document says so and it is right.

## §3, §4, §6 — the algebra

| identity | instances | failures |
| --- | ---: | ---: |
| `adj(H + c·llᵀ) l = adj(H) l` | 500 | 0 |
| `det(H + c·llᵀ) = det H + c·lᵀ adj(H) l` | 500 | 0 |
| `det(AᵀHA) = (det A)² det H` | 500 | 0 |
| `Θ_J = [[0,1],[0,0]]`: `Θ ≠ 0`, `Θ² = 0` | — | holds |

Random integers in `[−10⁶, 10⁶]`: polynomial identities of this degree that
hold on 500 such points hold identically (Schwartz–Zippel).

## §7 — the Mellin formula, evaluated

With `ε = +1` (split multiplicative at 389, `a₃₈₉ = 1`), the document's
derivation is `Λ(1 + s) = ∫₁^∞ f(iy/√N)(y^s + y^{−s}) dy`, so `Λ(1) = 2∫ f`,
`Λ'(1) = 0` identically, and `Λ''(1) = 2∫ f (log y)²`; with `L(1) = 0` the
Gamma and conductor factors contribute nothing at second order and
`L''(1)/2 = (2π/√N)∫₁^∞ f(iy/√N)(log y)² dy`. Evaluated term by term:

| | value |
| --- | --- |
| `a_p` used | point-counted for `p ≤ 220`; `a₃₈₉ = 1` on the node |
| `L(E,1)` by the same series | `−2.5·10⁻¹⁶` |
| `L''(E,1)/2` by the Mellin formula | **0.7593165002884076** |
| the corpus's value (RUN-023's input) | 0.7593165002884268 |
| relative difference | `2.5·10⁻¹⁴` |
| last term used | `3·10⁻³⁶` |

The remaining `2·10⁻¹⁴` is the adaptive Simpson rule's floor at `10⁻¹⁵`
tolerance; a control that loosens the tolerance to `10⁻¹³` stays within
`10⁻⁹`, a defect that cuts the integrals at `y = 1 + 5/c` does not.

## The labels

| phrase | present |
| --- | --- |
| 本輪沒有解出 `𝔰₁₁` | yes |
| BD6 未證 | yes |
| 並非完整 BSD 證明 | yes |
| `canonical_global_scalar_s11: null` in the output | yes |

## The drill

**314 defects, 314 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 65 controls undisturbed, over 102 checks.

The 4 planted for this gate, each turning `attack06-scalar-and-mellin` red and nothing else:

| planted defect | went red |
| --- | --- |
| the minimal polynomial of alpha is taken as A^2 + 4A - 11 | `attack06-scalar-and-mellin` |
| beta is taken as 11*alpha instead of 11/alpha | `attack06-scalar-and-mellin` |
| the Hecke recursion at prime squares uses a_p^2 instead of a_p^2 - p | `attack06-scalar-and-mellin` |
| the Mellin integrals are cut at y = 1 + 5/c instead of 1 + 60/c | `attack06-scalar-and-mellin` |


## What this round does not claim

* **Proposition 2.1 (`h(x, κ†) = θ⁻¹a₂ℓ(x)`) is Rubin's formula as cited to
  BKS I**, read. The 16 is the local factor; the document is explicit that
  the canonical multiplier is `16·𝔰₁₁` with `𝔰₁₁` unknown.
* **Proposition 4.1's Hodge–Tate conclusion** uses Sen's theorem as cited;
  the matrix is checked, the theorem is not.
* **The Mellin agreement is numerical**, to 14 digits: it confirms the
  formula and the corpus's value against each other, and is not a proof that
  `ord_{s=1} L(E,s) = 2`.
* **BD6 is open**, as the document says; nothing here bears on `𝔰₁₁`'s
  rationality.
