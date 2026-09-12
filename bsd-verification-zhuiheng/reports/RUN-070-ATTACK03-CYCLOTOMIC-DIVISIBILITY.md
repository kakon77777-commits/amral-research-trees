# RUN-070 — GPT-6's Attack 03, "cyclotomic divisibility": every finite identity in it recomputes, its own counterexample holds in the ring, and it says in its own words that its core lemma is unproved

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Proof_Attack_03_Cyclotomic_Divisibility`](../data/external/gpt6-proof-attacks/extracted/03/BSD_Proof_Attack_03_Cyclotomic_Divisibility.md) — the first of five packages a ChatGPT (GPT-6, web) session produced from the handoff bundle of 2026-09-11, received from Neo.K on 2026-09-12 ([provenance](../data/external/gpt6-proof-attacks/PROVENANCE.json)); packages 01 and 02 were not among the files handed over
**Tools:** [`src72_attack03_cyclotomic_divisibility.py`](../code/src72_attack03_cyclotomic_divisibility.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src72-attack03-cyclotomic-divisibility.json`](../data/gate-logs/src72-attack03-cyclotomic-divisibility.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: a new author enters the corpus, and the same rules apply to it. Attack 03 takes the P5 inputs this line verified (the matrix `M_loc`, `det = 2`, the finite Selmer group, `a₁₁ = −4`) and builds an algebraic route: a relaxed Selmer complex modelled as `[R³ → R²]` with `A = (B c)`, a candidate class `z_det = (−adj(B)c, det B)` defined by the adjugate identity, and a reduction of "Kato's class equals `z_det` up to a unit" to one one-sided divisibility `h_∞ ∈ D_∞·Ω` in the Iwasawa algebra, with a conditional Theorem 6.1 turning that divisibility into the unit comparison. **Everything finite in it recomputes.** Lemma 3.1 — `A·z_det = 0` and `q(z_det) = det B` — holds in the actual ring `F₁₁[G]/I³` of RUN-069 with the actual `B ≡ [[X,2X],[Y,4Y]]` and 25 random `c`, and over `Z` in the document's explicit coordinates; the §5 constants all check (`11 − a₁₁ + 1 = 16` a unit; `χ(U_m) = m/f_χ` on all four character types with `ε(U_m) = 393427 ≡ 1`; `388/389 ≡ 9`; `9·5 ≡ 1`, which is why its `κ` collapses to `u₀`; the ordinary unit root `≡ 7 ≠ 1`). **Its §7 counterexample is exactly right**: in `Z₁₁[C₁₁]`, `X₀N₀ = 0`, `h₀ = D₀u` with `u = 1 + N₀/11` — trivial branch 2, every nontrivial branch 1, all units — and `u ∉ Z₁₁[C₁₁]`, so `h₀ ∉ D₀R₀`: branch-wise divisibility does not glue, and the document uses this to say plainly that the direct Euler-system argument is missing a step. **And it labels itself**: Theorem 6.1 is "條件性", the core lemma is "尚未證明", the document "不是完整 BSD 證明". Nothing here moves an `OPEN` label, and the document does not claim to.**

---

## What the document is

A derivation, not a computation: it constructs an object (`z_det`) from
inputs this line has verified, proves a conditional theorem about it, and
identifies the one arithmetic statement that would complete the argument —
the integral divisibility `h_∞ ∈ D_∞·Ω` including the congruences between
characteristic-zero branches — and says it has not proved it. Its cited
external results (BKS I/II, Milne) are read here, not checked. What can be
computed is the algebra it rests on and the constants it uses, and that is
what the gate does.

## Lemma 3.1 — the adjugate identity, in the actual ring

`A = (B c)`, `z_det := (−adj(B)c, det B)`. Then `A·z_det = −B adj(B) c + c det B = 0`
and the last coordinate is `det B`. Checked two ways:

| where | `B` | `c` | `A·z_det` | `q(z_det)` |
| --- | --- | --- | --- | --- |
| `F₁₁[G]/I³` (RUN-069's ring) | `[[X, 2X], [Y, 4Y]]`, `det = 2XY` | 25 random elements | **0**, 25 of 25 | `2XY` |
| `Z`, the document's explicit form `(bc₂ − ec₁, dc₁ − ac₂, ae − bd)` | random in `[−50, 50]` | random | **0**, 200 of 200 | `det` |

## §5 — the constants

| the document says | recomputed |
| --- | --- |
| `a₁₁ = −4` | point-counted, `−4` |
| `11 − a₁₁ + 1 = 16`, a unit | 16; `16 mod 11 = 5 ≠ 0` |
| `χ(U_m) = m/f_χ` for `U_m = (1 + 36N_γ)(1 + 90N_η)` | nontrivial/nontrivial: 1 = 1; trivial at 397 only: 397; at 991 only: 991; trivial/trivial: 393427 — all four |
| `ε(U_m) = m ≡ 1 (mod 11)` | `393427 ≡ 1` |
| `388/389 ≡ 9 (mod 11)` | `3 · 4⁻¹ = 3 · 3 = 9` |
| `κ = 9 · 5 · u₀ = u₀` | `45 ≡ 1` |
| residual Frobenius on the ordinary quotient `7 ≠ 1` | `x² + 4x + 11 ≡ x(x + 4)`, unit root 7 |

## §7 — the counterexample, verified in the ring

The document's point: character-wise divisibility in `Z₁₁[G]` does not imply
integral divisibility, because the branches are glued by congruences. Its
example, recomputed as vectors on `g⁰ … g¹⁰`:

| | |
| --- | --- |
| `X₀N₀` | 0 |
| `h₀ = D₀ + N₀` vs `D₀ · (1 + N₀/11)` | equal |
| `u = 1 + N₀/11` in `Z₁₁[C₁₁]` | **no** — every coefficient has 11 in its denominator |
| `u` on the trivial branch / on each nontrivial branch | 2 / 1 — units everywhere |
| `D₀ = 11 + X₀` on the trivial branch / nontrivial | 11 / `11 + (ζ − 1)`, nonzero — a non-zero-divisor |
| `h₀ ∈ D₀R₀` | **no** — the unique quotient is `u` |

Attack 04 later notes that this `D₀` has augmentation `≡ 0`, which is why
its own denominator-clearing lemma excludes it; RUN-071 checks that.

## The labels

| phrase | present |
| --- | --- |
| 核心算術整除引理仍未證出 | yes |
| 不是完整 BSD 證明 | yes |
| 條件性完成定理 (Theorem 6.1) | yes |
| 候選核心引理（尚未證明） | yes |
| any claim that BSD is proved | none |

## The drill

**314 defects, 314 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 65 controls undisturbed, over 102 checks.

The 4 planted for this gate, each turning `attack03-cyclotomic` red and nothing else:

| planted defect | went red |
| --- | --- |
| the adjugate is written without its off-diagonal minus signs | `attack03-cyclotomic` |
| U_m's second factor is given the coefficient 36 as well, so chi(U_m) is wrong on the characters trivial at 991 | `attack03-cyclotomic` |
| the counterexample's u is taken as 1 + N_0 with no 11 in the denominator, so it is integral and the point is lost | `attack03-cyclotomic` |
| the unit-root search admits the root 0, so two residues come back | `attack03-cyclotomic` |


## What this round does not claim

* **Proposition 2.1 is read, not checked.** The shape of the relaxed Selmer
  complex (`h¹ = 3`, `h² = 2`, the surjective local map) is a cohomological
  derivation from cited results; this line has no instrument for it.
* **Theorem 6.1 is conditional on three hypotheses the document lists**, and
  the third is the unproved core lemma. Verifying the algebra of its proof is
  not verifying its hypotheses.
* **Nothing about Kato's class.** The identification `h = q(z_K) = θ_{F,S}` in
  §5 is cited to BKS II and read.
* **The document's honesty is a finding about the document**, not about the
  mathematics: an author that labels its gap is easier to verify, not righter.
