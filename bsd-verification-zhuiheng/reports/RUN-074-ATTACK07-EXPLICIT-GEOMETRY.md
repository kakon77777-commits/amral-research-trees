# RUN-074 — GPT-6's Attack 07: an explicit genus-3 curve on E × E, a tangent function, a Bézout certificate mod 11 and a four-term chain with boundary 4·Z_PQ — every algebraic fact recomputed exactly, and the comparison with Kato left where the document leaves it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Proof_Attack_07_Explicit_Secondary_Geometry`](../data/external/gpt6-proof-attacks/extracted/07/BSD_Proof_Attack_07_Explicit_Secondary_Geometry.md), with its [`attack07_result.json`](../data/external/gpt6-proof-attacks/extracted/07/attack07_result.json) — the fifth GPT-6 package
**Tools:** [`src76_attack07_explicit_geometry.py`](../code/src76_attack07_explicit_geometry.py), [`src74_attack05_local_log.py`](../code/src74_attack05_local_log.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src76-attack07-explicit-geometry.json`](../data/gate-logs/src76-attack07-explicit-geometry.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Attack 07 stops deriving and builds. For `E: y² + y = x³ + x² − 2x`, `P = (0,0)`, `Q = (1,0)` and `A = E × E`, it writes down the locus of equal `y`-coordinates as a conic through `(0,1)`, parametrises it as `x₁ = n/d`, `x₂ = m/d` with `d = u² + u + 1`, `n = −3u − 2`, `m = 1 − u − 2u²`, lifts it to a hyperelliptic curve `C: W² = F₈(u)` of genus 3, takes the tangent function `g = 2x₁ + 3x₂ − 3` and three coordinate curves, and proves `∂Γ_PQ = 4([(P,Q)] − [(P,O)] − [(O,Q)] + [(O,O)])`: a rational chain bounding the exterior product of the two Mordell–Weil divisors — the "null-homotopy data" Attack 06 said the secondary pairing needs. **Every algebraic fact recomputes with this tree's own exact polynomial arithmetic and group law**: `f₀(x₁) − f₀(x₂)` factors as stated; `m = d + un` and the conic vanishes identically on the parametrisation; `F₆ = d³ + 4n³ + 4n²d − 8nd²` and `F₈ = dF₆` expand to the stated coefficients and `W² = F₈` is exactly `(2y+1)²d⁴`; the document's `S`, `T` satisfy `S·F₈ + T·F₈′ ≡ 1 (mod 11)` and `F₈` is squarefree over `Q` — degree 8, monic, genus 3; `g = −(3u+2)²/d` identically, its zero `u₀ = −2/3` has `d = 7/9`, `(x₁, x₂) = (0, 1)`, `W² = (49/81)²`, `Y = ±1`, so the two points over it are `(P, Q)` and `(−P, −Q)`; `F₆ ≡ 4n³ (mod d)` and `gcd(n, d) = 1`, the premises of its pole analysis; the four divisors with coefficients `(1, −2, 2, −4)` sum to `4·Z_PQ` and the diagonal chains to `2·Z_RR`; `P + Q = (−2, −1)`, `P + R = (5/4, −13/8)`, `Q + R = (1/9, −19/27)`, supports disjoint from `{O, P, Q}`. **The document says the comparison of this data with Kato's derived class is not constructed, `𝔰₁₁` is unknown, and this is not a BSD proof; nothing here says otherwise.**

---

## §2 — the curve

| the document says | recomputed |
| --- | --- |
| `f₀(x₁) − f₀(x₂) = (x₁ − x₂)(x₁² + x₁x₂ + x₂² + x₁ + x₂ − 2)` | identity, 200 random rational pairs |
| `x₂ = 1 + ux₁` gives `x₁ = n/d`, `x₂ = m/d` | `m = d + u·n` exactly; the conic's numerator is the zero polynomial |
| `F₆ = u⁶ + 27u⁵ + 106u⁴ + 87u³ − 14u² − 21u + 1` | same |
| `F₈ = u⁸ + 28u⁷ + 134u⁶ + 220u⁵ + 179u⁴ + 52u³ − 34u² − 20u + 1` | same |
| `W² = F₈` is the model: `Y² d⁴` with `Y² = 4x³ + 4x² − 8x + 1` at `x = n/d` | the numerator of `Y²` over `d³` is `F₆` exactly |
| `SF₈ + TF₈′ ≡ 1 (mod 11)` with `S = 7 + 7u + 3u² + u³ + 9u⁴ + 6u⁵`, `T = 8 + 3u + u² + 10u³ + 9u⁴ + 10u⁵ + 2u⁶` | `[1]` |
| `F₈` squarefree over `Q`, genus `(8 − 2)/2 = 3` | `gcd(F₈, F₈′) = 1`; degree 8, monic |

## §3 — the tangent function

| the document says | recomputed |
| --- | --- |
| `g = 2x₁ + 3x₂ − 3 = −(3u + 2)²/d` | numerator `−9u² − 12u − 4` |
| `u₀ = −2/3`: `d = 7/9`, `W = ±49/81`, `Y = ±1` | `F₈(u₀) = (49/81)²`; `Y = W/d² = ±1` |
| the two points over `u₀` map to `(P, Q)` and `(−P, −Q)` | `((0,0),(1,0))` and `((0,−1),(1,−1))`, both on `E` |
| `F₆ ≡ 4n³ (mod d)`, `n` and `d` coprime | remainders equal; `gcd(n, d) = 1` |
| `g → −9` as `u → ∞` | leading coefficients `−9/1` |

The orders `ord d = 2`, `ord W = 1`, `ord x_i = −2`, `ord Y = −3`, `ord g = −2`
at the two poles over `d = 0` are the document's local-parameter argument;
the facts it rests on are the two rows above it, and they hold.

## §4–5 — the chains

| chain | boundary, recomputed |
| --- | --- |
| `(C,g) − 2(H₋,x₁) + 2(V_P,x₂−1) − 4(V_O,x₂−1)` | `4[(P,Q)] − 4[(P,O)] − 4[(O,Q)] + 4[(O,O)]` = `4·Z_PQ` |
| `Γ_PP`, `Γ_QQ` (diagonal, `x − a`) | `2·Z_PP`, `2·Z_QQ` |
| denominators of the four `B_{ij}` | 4, 4, 2, 2 — all units at 11 |

The three cancellations the document names — at `(−P,−Q)`, `(P,−Q)`,
`(O,−Q)` — occur exactly.

## §7 — the shifted points

`R = P + Q = (−2, −1)`, `P + R = (5/4, −13/8)`, `Q + R = (1/9, −19/27)`, all
on `E`, none equal to `O`, `P` or `Q` — the disjoint-support condition its
rigidified line bundles need.

## The labels

| phrase | present |
| --- | --- |
| 與 Kato 導出類的幾何比較 — 尚未構造 | yes |
| 不是完整 BSD 證明 | yes |
| `𝔰₁₁` 的有理性及值仍未知 | yes |
| its output: `boundary_residual` empty, `genus` 3 | yes |

## The drill

**314 defects, 314 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 65 controls undisturbed, over 102 checks.

The 4 planted for this gate, each turning `attack07-geometry` red and nothing else:

| planted defect | went red |
| --- | --- |
| F_6 is formed with +8nd^2 in place of -8nd^2 | `attack07-geometry` |
| the Bezout certificate's T is multiplied by F_8 instead of F_8' | `attack07-geometry` |
| the chain coefficients are (1, -2, 2, -2) | `attack07-geometry` |
| the tangent line is written 2x_1 + 3x_2 + 3 | `attack07-geometry` |


## What this round does not claim

* **The valuations at the poles are read**, not computed: the local-parameter
  argument is a proof whose polynomial premises are checked here.
* **The 1-motive of §7.2 is a definition**; whether it is the right secondary
  data for Kato's class is exactly what the document says is not done.
* **`4·[Z_PQ] = 0` in `CH₀(A)`** is what the chain proves; the document does
  not claim 4 is the exact order, and neither does this round.
* **Nothing about `𝔰₁₁`, the regulator or `L''(E,1)`** — the document builds
  geometry and stops before the comparison; so does this round.
