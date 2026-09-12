# RUN-071 — GPT-6's Attack 04: its one new computation, the mod-11 p-adic L-function of 389.a1 at conductor 121, reproduced from this tree's own modular symbols to the summand — μ = 0, λ = 2 — and its theorem read as the conditional derivation it says it is

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Proof_Attack_04_Mu_Zero_Descent`](../data/external/gpt6-proof-attacks/extracted/04/BSD_Proof_Attack_04_Mu_Zero_Descent.md), with its [`cyclotomic_result.json`](../data/external/gpt6-proof-attacks/extracted/04/cyclotomic_result.json) — the second GPT-6 package
**Tools:** [`src73_attack04_padic_l_mod11.py`](../code/src73_attack04_padic_l_mod11.py), [`src70_kurihara_modular_symbols.py`](../code/src70_kurihara_modular_symbols.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src73-attack04-padic-l-mod11.json`](../data/gate-logs/src73-attack04-padic-l-mod11.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Attack 04 supplies what Attack 03 said was missing — a denominator-clearing lemma (2.1–2.2) that turns divisibility after inverting 11 into integral divisibility provided the tame augmentation of `D_∞` has `μ = 0` — and then computes that `μ = 0` for 389.a1 at 11 from conductor 121 alone. **The computation reproduces exactly from this tree's own modular symbols.** With RUN-068's eigenline at the disclosed scale `λ(1,5) = 1`, the measure `α⁻²[a/121]⁺ − α⁻³[a/11]⁺` (`α ≡ 7`, `α⁻² ≡ 9`, `α⁻³ ≡ 6`) pushed to the cyclotomic quotient through the Teichmüller lift `ω(a) = a¹¹ mod 121` and `a·ω(a)⁻¹ = 12^{j(a)}` gives group-basis coefficients `(4,0,7,0,4,0,7,2,2,7,0)` and `L̄(t) = 2t² + 2t³ + 2t⁴ + 5t⁶ + 6t⁷ + 10t⁸ + 7t⁹ (mod 11, t¹¹)` — **all 110 summands identical to the document's own table, so μ = 0 and λ = 2**, the constant and linear terms vanishing as a rank-2 curve requires. Its Euler-factor arithmetic checks too: `s₃₉₇ ≡ 3`, `s₉₉₁ ≡ 2`, `Ē_ℓ = (1 − (1+t)^{−s})² = 9t² + …, 4t² + …`, `1 − 389⁻¹ ≡ 9`, and the counterexample of Attack 03 has augmentation `≡ 0`, exactly the case Lemma 2.2 excludes. **What the document then proves — Theorem 7.1, Kato's class equal to the cofactor class up to a unit of `Ω` for its relaxed complex — rests on Kato's one-sided bound and Kataoka's Coleman map as cited, and the document says so, saying also that R318 and R319 stay open and that mod-11 data does not give the characteristic-zero order of vanishing.** Verified: the computation. Read: the theorem. Moved: no label.**

---

## The computation, redone

The document's modular symbols are the stress-test package's eigenline; this
round uses RUN-068's — the same functional, reached by a third
implementation and shown to agree to the term — with its own continued-fraction
paths, its own Teichmüller lifts and its own cyclotomic logarithms. Only the
formula is shared.

| step | this round | the document |
| --- | --- | --- |
| unit root of `x² + 4x + 11 (mod 11)` | roots `{0, 7}`, `α ≡ 7` | 7 |
| `α⁻²`, `α⁻³ (mod 11)` | 9, 6 | 9, 6 |
| units mod 121 classified by `j(a)` | 110, 10 per class, 0 unclassified | 110 |
| group-basis `c_j` | `(4,0,7,0,4,0,7,2,2,7,0)` | same |
| `L̄(t)` coefficients `t⁰ … t¹⁰` | `(0,0,2,2,2,0,5,6,10,7,0)` | same |
| summands differing from the document's table | **0 of 110** | — |
| `μ`, `λ` | 0, 2 | 0, 2 |

The `t`-series is determined mod `(11, t¹¹)` by the conductor-121 data because
`(1+t)¹¹ − 1 ≡ t¹¹ (mod 11)` — the document's argument, and the reason a
finite computation can decide `μ` and `λ`. The scale is the disclosed one;
the canonical leading coefficient is `2u₀` for the unit `u₀` RUN-068 could
not fix either.

## The Euler factors and the constants

| the document says | recomputed |
| --- | --- |
| `s₃₉₇ ≡ 3`, `s₉₉₁ ≡ 2 (mod 11)` | `j(397 mod 121 = 34) = 3`, `j(991 mod 121 = 23) = 2` |
| `Ē_ℓ(t) = (1 − (1+t)^{−s_ℓ})²` since `a_ℓ ≡ 2`, `ℓ ≡ 1` | equal as series to `O(t⁵)` at both primes |
| `Ē₃₉₇ = 9t² + …`, `Ē₉₉₁ = 4t² + …` | `9t² + 8t³ + 8t⁴`, `4t² + 10t³ + 3t⁴` |
| `1 − 389⁻¹ ≡ 9` | `1 − 3 = −2 ≡ 9` |
| `λ(h₀) = 2 + 2 + 2 = 6` | arithmetic |
| Attack 03's `D₀ = 11 + X₀` excluded by Lemma 2.2 | `ε(D₀) = 11 ≡ 0` |

## What the theorem needs, and where it is read

Theorem 7.1's chain: Lemma 2.1 (algebra, read) + Lemma 2.2 (algebra, read) +
`μ(D₀) = 0` from Kato's one-sided bound and `μ(h₀) = 0` from the computation
above and Kataoka's Coleman isomorphism (§5, cited) + character-wise
divisibility from Kato's bound on each branch (§6, cited) ⇒ integral
divisibility ⇒ unit comparison via the finite primitivity `2XY ≠ 0` (RUN-069)
and `κ ≠ 0` (RUN-068). The computed links hold. The cited ones are what
they are: theorems this line does not check.

## The labels

| phrase | present |
| --- | --- |
| 沒有證明完整 BSD | yes |
| R318 / R319 仍未關閉 | yes |
| 尚未經（獨立審查） | yes |
| "mod-11 data does not by itself give the characteristic-zero vanishing order" | yes (§3) |

## The drill

**314 defects, 314 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 65 controls undisturbed, over 102 checks.

The 4 planted for this gate, each turning `attack04-padic-l` red and nothing else:

| planted defect | went red |
| --- | --- |
| the Teichmuller lift is taken as a^10 instead of a^11 | `attack04-padic-l` |
| alpha^-3 is used for both terms of the measure | `attack04-padic-l` |
| the cyclotomic generator is taken as 23 = 1 + 2*11 in place of 12 | `attack04-padic-l` |
| s_ell is read from ell mod 11 instead of ell mod 121, so both exponents come out 0 | `attack04-padic-l` |


## What this round does not claim

* **Theorem 7.1 is not verified.** Its computed inputs are; its cited inputs
  (Kim–Lee–Ponsinet's restatement of Kato, Kataoka's Theorems 4.7 and 6.4,
  the perfectness of the Iwasawa complex) are read.
* **`λ = 2` is the mod-11 Iwasawa invariant**, not the characteristic-zero
  order of vanishing of `L₁₁(E, t)`; Attack 05 argues the latter, and RUN-072
  reads that argument.
* **No canonical scale.** `2t²` is the fixed-scale coefficient; `2u₀` is the
  canonical one for an unknown unit `u₀`.
* **The Sage documentation the measure formula is cited to is not consulted**;
  the formula is checked against the document's own per-summand output.
