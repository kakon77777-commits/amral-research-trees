# RUN-072 — GPT-6's Attack 05: the 11-adic formal logarithm of P and Q on 389.a1, recomputed exactly — [16]P and [16]Q to the last digit, s ≡ 99 and 66 (mod 121), ℓ̄ = (4, 10) — and its Selmer-complex derivations read

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Proof_Attack_05_Rank_Two_Regulator`](../data/external/gpt6-proof-attacks/extracted/05/BSD_Proof_Attack_05_Rank_Two_Regulator.md), with its [`local_log_result.json`](../data/external/gpt6-proof-attacks/extracted/05/local_log_result.json) — the third GPT-6 package
**Tools:** [`src74_attack05_local_log.py`](../code/src74_attack05_local_log.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src74-attack05-local-log.json`](../data/gate-logs/src74-attack05-local-log.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Attack 05 carries Attack 04's determinant comparison to the rank-2 regulator, and its one new computation is the normalised local logarithm `ℓ = log_ω/11` on the generators. Because `#E(F₁₁) = 16`, `[16]P` and `[16]Q` lie in the formal group; with `s = −x/y` and `log_ω(s) ≡ s (mod 11²)` for `s ∈ 11Z₁₁`, `ℓ(R) ≡ s([16]R)/(16·11) (mod 11)`. **Recomputed with this tree's own exact group law over Q: `[16]P` and `[16]Q` are identical to the document's coordinates to the last digit (denominators of 36 and 53 digits), `s([16]P) ≡ 99`, `s([16]Q) ≡ 66 (mod 121)`, both of valuation exactly 1, so `(ℓ̄(P), ℓ̄(Q)) = (4, 10)`, `ℓ̄` is surjective, and `ker ℓ̄ = k·(P + 4Q)` (`4 + 40 = 44 ≡ 0`).** The premises check: `a₁₁ = −4 ≢ 1` (non-anomalous), `n − v₁₁(n) ≥ 2` for every `n ≥ 2` (why the logarithm is `s` mod 121), and the auxiliary Euler constant `374·1045/(397·991) = 11²·3230/393427` with `3230/393427 ≡ 7`. **What the document derives from this — `det H_γ ∈ O^×`, `L₁₁(E,t) = t²U(t)` with `U` a unit, `H²(G_{Q,Σ},T) ≅ O ⊕ O/11`, the index `11²`, and `κ_prim = u₀·adj(H_γ)ℓ` — is Selmer-complex mathematics on top of Kato's bound and the Coleman map, read here and not checked; the document itself says the height-matrix entries are not computed and that the complex leading-term comparison remains.** Verified: the number. Read: the theory.**

---

## The computation, redone

The gate carries its own addition and doubling on the general Weierstrass
model `y² + a₁xy + a₃y = x³ + a₂x² + a₄x + a₆` over `Fraction`, its own
11-adic valuation and residue, and the enumeration `#E(F₁₁) = 16` from
RUN-068's point counter.

| | `P = (0, 0)` | `Q = (1, 0)` |
| --- | --- | --- |
| `[16]R` on the curve | yes | yes |
| `x([16]R)` denominator | 36 digits | 53 digits |
| identical to the document's exact coordinates | **yes** | **yes** |
| `s = −x/y`, `v₁₁(s)` | 1 | 1 |
| `s (mod 121)` | **99** | **66** |
| `ℓ̄ = s/(16·11) (mod 11)` | **4** | **10** |

`99/176 = 9/16 ≡ 9·9 = 81 ≡ 4` and `66/176 = 6/16 ≡ 6·9 = 54 ≡ 10`, as the
document's arithmetic requires; `ℓ̄(P + 4Q) = 44 ≡ 0`.

## The premises

| the document uses | recomputed |
| --- | --- |
| `#E(F₁₁) = 16` | 16 by enumeration |
| `a₁₁ = −4`, non-anomalous (`≢ 1`) | `−4 ≡ 7` |
| `log_ω(s) ≡ s (mod 11²)` because `n − v₁₁(n) ≥ 2` for `n ≥ 2` | holds for every `n` in `[2, 400)`; the first tight case is `n = 2` |
| `E₃₉₇(0)E₉₉₁(0) = (374/397)(1045/991) = 11²·3230/393427` | `374·1045 = 390830 = 121·3230`; unit part `≡ 7 (mod 11)` |
| `v₁₁(det J) = 2` matches `v₁₁(𝓔(0)) = 2` | the latter recomputed; the former is a derivation |

## What is derived, not computed — and how the document says it

| claim | rests on | the document's own wording |
| --- | --- | --- |
| `L₁₁(E,t) = t²U(t)`, `U ∈ Λ^×` | Kato's one-sided bound, the mod-11 `λ = 2` of Attack 04, the Coleman isomorphism | §5.2 |
| `det H_γ ∈ O^×` | the same, via `B(t) = tV(t)` | §5.3, "沒有聲稱已數值算出高度矩陣每個 entry" |
| `H²(G_{Q,Σ},T) ≅ O ⊕ O/11`, index `11²` | Selmer duality and the local Euler factors | §4 |
| `κ_prim = u₀·adj(H_γ)ℓ` | Bockstein naturality | Theorem 6.1 |
| the complex comparison | — | §10: "仍待攻克", "本文沒有先假設這個比值有理" |

## The labels

| phrase | present |
| --- | --- |
| 沒有宣稱完整 BSD | yes |
| 尚未經獨立審查 | yes |
| 沒有聲稱已數值算出高度矩陣每個 entry | yes |

## The drill

**314 defects, 314 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 65 controls undisturbed, over 102 checks.

The 4 planted for this gate, each turning `attack05-local-log` red and nothing else:

| planted defect | went red |
| --- | --- |
| the formal parameter is taken as x/y instead of -x/y | `attack05-local-log` |
| the multiple is 15 instead of #E(F_11) = 16, so [15]R is not in the formal group | `attack05-local-log` |
| ell is normalised by 16 alone, not 16*11 | `attack05-local-log` |
| the second Euler factor is inverted, 991/1045 for 1045/991 | `attack05-local-log` |


## What this round does not claim

* **The height matrix is not computed**, by the document or here. Its
  non-degeneracy is derived, and the derivation is read.
* **`ord_{t=0} L₁₁(E,t) = 2` in characteristic zero is the document's
  argument** from Kato's bound plus `λ = 2`; this round supplies the `λ = 2`
  (RUN-071) and the local logarithm, not the argument.
* **Torsion `Z/11` in the relaxed `H²`** is a Selmer-complex statement; this
  line has no instrument that computes a global `H²`.
* **The Sage/Milne/Kim–Lee–Ponsinet/Kataoka citations are not consulted.**
