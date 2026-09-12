# RUN-075 — GPT-6's Attack 08: the three norms of the tangent function, the addition pushforward 7·((x+2)/y)⁴, its divisor against m_*Z_PQ, and the closed chain that moves the constant 7 — every identity recomputed in the function field, and the 7 shown, as the document says, not to be Kato's scalar

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Proof_Attack_08_Norms_Localization_and_Scale`](../data/external/gpt6-proof-attacks/extracted/08/BSD_Proof_Attack_08_Norms_Localization_and_Scale.md), with its [`attack08_result.json`](../data/external/gpt6-proof-attacks/extracted/08/attack08_result.json) — the sixth GPT-6 package, received later on 2026-09-12 ([provenance](../data/external/gpt6-proof-attacks/PROVENANCE.json))
**Tools:** [`src77_attack08_norms_and_pushforwards.py`](../code/src77_attack08_norms_and_pushforwards.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src77-attack08-norms-and-pushforwards.json`](../data/gate-logs/src77-attack08-norms-and-pushforwards.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Attack 08 takes Attack 07's chain `Γ` on `E × E` (RUN-074) and pushes it forward along the two projections and the addition map. Three norms of the tangent function `g` come out of Vieta's relations on the same-`y` cubic: `7x²`, `7(x−1)²`, `7(x+2)²`. With the translation formulas `A(T) = x(T+Q) = (x² + x − 2 − y)/(x−1)²`, `B(T) = x(T−P) − 1 = (y + 1 − x² − 2x)/x²` and the sign identity `B/A = −(x+2)(x−1)²/y²`, the full pushforwards are `F_{π₁}(Γ) = 7`, `F_{π₂}(Γ) = 7`, `F_m(Γ) = 7M⁴` with `M = (x+2)/y` — and `div M = [R] − [P] − [Q] + [O] = m_*Z_PQ`, so the addition boundary is exactly consistent with `∂Γ = 4Z_PQ`. **All of it recomputes exactly in `Q[x,y]/(y² + y − x³ − x² + 2x)` with this gate's own arithmetic**: the Vieta factorisation, the three norms to the coefficient, the two translation formulas from the group law, identity (9) with residual zero, the pushforward identity `B²y⁴ = (x+2)²x⁴A²` with residual zero, and the divisors point by point. Then the document's own point: the `7` is not intrinsic. A closed chain `Θ_c = (Δ,c) − (H₀,c) − (V_O,c)` has pushforward exponents `(1,1,4) − (1,0,1) − (0,1,1) = (0,0,2)` (the 4 is `deg[2]`; `#E[2] = 4` since the 2-division cubic is separable), so `Γ¹ = Γ⁰ + ½Θ₇` keeps the boundary and carries `(1, 1, M⁴)` — **the constant on the addition projection can be moved to anything by a closed correction, and therefore "cannot be identified with Attack 06's `𝔰₁₁`"**, in the document's words. Its localisation classes have residues `[P] − [O]`, `[Q] − [O]`. Its Propositions 08.4 and 08.6 — the higher-Chow degree mismatch and the split sequence — are theory, read. Its output records `s11: null`, `BSD_proved: false`, `canonical_frontier_updated: false`, and the text says the Kato comparison is not constructed. Nothing moves.**

---

## 08.1 — the norms, from Vieta

On the same-`y` locus the three abscissae are the roots of
`X³ + X² − 2X − (y² + y)`; fixing one root `x`, the other two satisfy
`r + s = −1 − x`, `rs = x² + x − 2`, and `N(a + br) = a² + ab(r+s) + b²rs`.

| map | `(a, b)` | norm, recomputed | the document |
| --- | --- | --- | --- |
| `π₁φ` | `(2x − 3, 3)` | `7x²` | `7x²` |
| `π₂φ` | `(3x − 3, 2)` | `7(x−1)²` = `7x² − 14x + 7` | same |
| `mφ` | `(−5 − 2x, 1)` | `7(x+2)²` = `7x² + 28x + 28` | same |

The factorisation `X³ + X² − 2X − f₀(x) = (X − x)(X² + (1+x)X + x² + x − 2)`
holds at 60 random rational `x` as an identity of polynomials in `X`.

## 08.2 — translations, the sign, the pushforward, the divisor

| the document says | recomputed (residual in the function field) |
| --- | --- |
| `A(T) = x(T+Q) = (x² + x − 2 − y)/(x−1)²` | from `λ = y/(x−1)`, `x₃ = λ² − x − 2`: residual **0** |
| `B(T) = x(T−P) − 1 = (y + 1 − x² − 2x)/x²` | from `λ = (y+1)/x`, `x₃ = λ² − x − 1`: residual **0** |
| (9) `y²(y + 1 − x² − 2x) + x²(x+2)(x² + x − 2 − y) = 0` | **0** |
| `F_m(Γ) = 7(x+2)²B²/((x−1)⁴A²) = 7M⁴` | `B²y⁴ − (x+2)²x⁴A²` (denominators cleared): **0** |
| `div(x + 2) = [R] + [−R] − 2[O]` | `x = −2` gives `y ∈ {0, −1}`: `(−2,−1) = R`, `(−2,0) = −R` |
| `div(y) = [P] + [Q] + [−R] − 3[O]` | `y = 0` gives `x ∈ {0, 1, −2}`: `P`, `Q`, `−R` |
| `div M = [R] − [P] − [Q] + [O] = m_*Z_PQ` | equal, and `4·div M = m_*(∂Γ)` |

`R = P + Q = (−2, −1)` by the group law, as at RUN-074.

## 08.3 — the closed correction

| support | `π₁` | `π₂` | `m` |
| --- | ---: | ---: | ---: |
| `Δ` | 1 | 1 | 4 (`m|_Δ = [2]`) |
| `H₀ = E × {O}` | 1 | 0 | 1 |
| `V_O = {O} × E` | 0 | 1 | 1 |

`Θ_c` exponents `(1,1,4) − (1,0,1) − (0,1,1) = (0,0,2)`. The exponent of 7 in
`Γ`'s three pushforwards is `(1,1,1)`; subtracting `Ξ₇ = (H₀,7) + (V_O,7)`
gives `Γ⁰` with `(0,0,−1)`, i.e. `(1, 1, M⁴/7)`; adding `½Θ₇` gives `Γ¹` with
`(0,0,0)`, i.e. `(1, 1, M⁴)`, the boundary `4Z_PQ` unchanged throughout.
`#E[2] = 4` is checked: the 2-division cubic `4x³ + 4x² − 8x + 1` has
`gcd(f, f′) = 1`.

The consequence the document draws is the right one: given only the boundary
and the two coordinate projections equal to 1, the addition projection's
constant is undetermined — "the ambiguity is a genuine higher-Chow
ambiguity". The 7 that came out of the geometry is not a number about Kato's
class.

## 08.5 — the localisation residues

`(P × G_m, τ) − (O × G_m, τ)` and `(Q × G_m, τ) − (O × G_m, τ)`: `τ` is a
unit on `G_m`, `div_{A¹}(τ) = [0]`, so the residues at `τ = 0` are
`[P] − [O]` and `[Q] − [O]`. Bookkeeping; it holds.

## The labels

| where | what |
| --- | --- |
| the text | "BSD 尚未證明"; "canonical frontier 保持原狀"; "尚未構造" (the Kato comparison); "不能把這裡出現的 7 指認為 Attack 06 的 `s₁₁`" |
| the output | `s11: null`; `BSD_proved: false`; `canonical_frontier_updated: false`; `is_Kato_global_scalar: false` |

## The drill

**319 defects, 319 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 66 controls undisturbed, over 103 checks.

The 5 planted for this gate, each turning `attack08-norms` red and nothing else:

| planted defect | went red |
| --- | --- |
| Vieta's product rs is taken as x^2 + x + 2 | `attack08-norms` |
| the addition map's pair is written (-5 - 2x, -1) | `attack08-norms` |
| the curve relation is reduced as y^2 = f_0 + y instead of f_0 - y | `attack08-norms` |
| y is given a double pole at O, so div M gains an O term | `attack08-norms` |
| the diagonal's degree under addition is taken as 2, not 4 | `attack08-norms` |


## What this round does not claim

* **Proposition 08.4 — the degree mismatch `q = 1` vs `q = 0` — is read.** It
  is the document locating why a direct pushforward cannot be a Selmer class;
  this line has no instrument for motivic cohomology.
* **Proposition 08.6 — the split sequence (20)–(24) — is read**, including
  homotopy invariance and the self-intersection formula it cites.
* **`deg[2] = 4` in characteristic zero is standard**; what is checked is
  `#E[2] = 4` on this curve.
* **Nothing about `𝔰₁₁`, Loeffler–Rivero's degeneration, or the complex
  leading term** — the document names them as the next problem and does not
  claim them.
