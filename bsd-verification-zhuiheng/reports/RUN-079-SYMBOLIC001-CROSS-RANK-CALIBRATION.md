# RUN-079 — BSD Symbolic Round 001 (the web GPT's "General Cross-Rank Projective Calibration"): every boxed identity instantiated with exact formal series and checked on 126 random instances over 21 rank patterns; two supplements the document leaves implicit — Theorem 4.1 is t-covariant, and the oracles O5/O6 test only the common-factorisation hypothesis O1; and the one number in it, log₁₁(12), to 11¹²

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Symbolic_Round_001_General_Cross_Rank_Projective_Calibration.md`](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_001_General_Cross_Rank_Projective_Calibration.md) — the first document from the web GPT session that Neo has assigned to symbolic derivation (no large computation), received 2026-09-13 ([provenance](../data/external/gpt-symbolic-rounds/PROVENANCE.json)). The new arrangement: the web GPT derives symbolically, the local GPT-6 attacks the frontier with computation, and this line verifies both **and supplies the symbolic side with computation**. This is the first round of that third role.
**Tools:** [`src81_symbolic001_cross_rank_calibration.py`](../code/src81_symbolic001_cross_rank_calibration.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src81-symbolic001-cross-rank-calibration.json`](../data/gate-logs/src81-symbolic001-cross-rank-calibration.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the document is a conditional symbolic theorem and it is correct as such. Under its hypothesis (2.1)–(2.3) — a factorisation `B̂_i(t) = C·A_i(t)·j(t)·z_i(t)` with a scalar `C` common to all partners, `A_i(0) ≠ 0`, `j(t) = j_e tᵉ + …`, `z_i(t) = t^{d_i}κ_i + …` — its leading-term lemma (3.1)–(3.2), the calibrator elimination (4.4), the gauge orbit (6.1), the invisibility of a common `q_f` (7.1), the two-calibrator identity (10.1) and the cocycle (11.1)–(11.3) all hold exactly on 126 random instances of formal power series with vector coefficients over `Q`, spanning `e ∈ {1,2,3}`, `d_i ∈ {0,…,3}` in seven rank patterns, dimensions `m_i ≤ 3`; the PC-001 specialisation (5.1) is (4.4) with `λ_0 = Col_0`, and with `A_E(0) = 26λ₈(0)/D_E` it is Attack 09's (19) — the two sides of this arrangement are consistent. Two things the document does not state are made explicit: (i) Theorem 4.1 is covariant under `t ↦ ut` — both sides scale by `u^{−d_i}` — so it is not merely "valid in a fixed coordinate"; what §9 correctly warns about is the bare ratio `B_i^lead/b_k`, which scales by `u^{−(d_i − d_k)}`; (ii) (10.1) and (11.3) are consequences of (2.1) alone: with a common `C` they hold for any data, and with a partner-dependent `C` they fail (30 of 30 trials), so the oracles O5/O6 test the common-factorisation hypothesis O1 and nothing else. The one number in the document, `L = log₁₁(12)`, is `≡ 2580404199593 (mod 11¹²)`, digits `0,1,5,9,9,9,5,8,3,5,0,9` low to high, cross-checked through `log(144)/2`; `v₁₁(L) = 1`, so `j₁ = 1/L` has valuation `−1` and every leading coefficient `B_i^lead` carries an `11⁻¹` that only the relative ratios cancel. Not verified, as the document itself lists: that a genuine Beilinson–Flach family satisfies (2.1); PC-001 (not handed to this line); the determinant-line lift of §12; BSD.**

---

## What was checked, identity by identity

The instance generator draws `C ∈ Q^×`, `j(t)` with `j_e ≠ 0`, and for each partner `A_i(t)` with `A_i(0) ≠ 0`, `z_i(t) ∈ Q^{m_i}[[t]]` with `z_i = t^{d_i}κ_i + …`, `κ_i ≠ 0`, a functional `λ_i` with `λ_i(κ_i) ≠ 0`; it forms `B̂_i = C·A_i·j·z_i` exactly (truncated at `t⁸`; a control truncates at `t¹²`). Patterns `(e; d)`: `(1,2,3; [0,1], [0,2], [1,1], [0,1,2], [2,3,0], [1,3], [0,0,1])`, six instances each.

| the document | checked | result |
| --- | --- | --- |
| (3.2) `ord_t B̂_i = e + d_i` | the first nonzero vector coefficient | 126/126 |
| (3.1) `B_i^lead = C A_i(0) j_e κ_i` | coefficient at `t^{e+d_i}` | 126/126 |
| (4.4) `κ_i = A_k(0)λ_k(κ_k)/A_i(0) · B_i^lead/b_k` | every ordered pair (calibrator, target), including `k = i` | 126/126 |
| (6.1) `C ↦ uC` moves every `B_i^lead` to `uB_i^lead` and leaves (4.4) unchanged | `u = 3/2` | 126/126 |
| (7.1) a common `q_f` cancels in `ρ_i/ρ_k` | `q = 5/7` | 126/126 |
| (10.1) `b_a/(A_a(0)λ_a(κ_a)) = b_b/(A_b(0)λ_b(κ_b))`, both `= Cj_e` | all partners | 126/126 |
| (11.1)–(11.3) with `Γ_{i←k} = (A_k(0)/A_i(0))(b_i/b_k)`, and `Γ_{i←k} = k_i/k_k` | all ordered triples | 126/126 |
| §8: a common rescaling `c_n ↦ s^{−n}c_n` of the auxiliary factor is a rescaling of `C` | subsumed by (6.1): (4.4) never contains `C` | — |
| §9: under `t = t'/u`, `[t'^m] = u^{−m}[t^m]` | `κ_i' = u^{−d_i}κ_i`, `B_i^lead′ = u^{−r_i}B_i^lead`, the factorisation survives in `t'` | 126/126 |

## Two supplements

**Theorem 4.1 is t-covariant.** In the coordinate `t' = ut`: `κ_i' = u^{−d_i}κ_i`,
`B_i^lead′ = u^{−(e+d_i)}B_i^lead`, `b_k' = u^{−(e+d_k)}b_k`, `λ_k(κ_k)' = u^{−d_k}λ_k(κ_k)`,
`A_i(0)` unchanged; the right-hand side of (4.4) therefore picks up
`u^{−d_k}·u^{−(e+d_i)+(e+d_k)} = u^{−d_i}`, exactly the factor on the left.
So (4.4) holds in every cyclotomic coordinate, not only in a fixed one
(126/126). What §9 is right about is the *bare* ratio `B_i^lead/b_k`, which
scales by `u^{−(d_i − d_k)}` (126/126) — a reader who compares such ratios
across ranks without the `λ_k(κ_k)` factor has to carry that law. The
document's conclusion ("fix the coordinate, or keep the rank-dependent
law") is correct; the sharper statement is that (4.4) already keeps it.

**What O5 and O6 test.** With a common `C`, (10.1) and (11.3) are identities
— they hold for any `A_i`, `j`, `z_i`, `λ_i`. With `C` replaced by a
partner-dependent `C_i` (everything else unchanged), (10.1) fails and the
triangle (11.3) fails, in 30 of 30 trials. So the "strong consistency
test" of §11 detects exactly one thing: whether the comparison scalar is
common — hypothesis O1. It cannot see a wrong `A_i`, a wrong `j`, or a
wrong class `z_i`, because (10.1) holds for any of those. This is worth
saying to whoever builds the calibration network: O5/O6 are a test of the
factorisation, not of the arithmetic inside it.

## The specialisation, and the join to Attack 09

With `e = 1`, `j₁ = 1/L`, `d_0 = 0`, `d_E = 1`, `λ_0 = Col_0` (so `b_0 =
r_{0,1}` and `λ_0(κ_0) = ℓ_0`), (4.4) is (5.1):
`κ_E = A_0(0)ℓ_0/A_E(0) · B_{E,2}/r_{0,1}` — 50/50 random instances. And
with Attack 09's `A_E(0) = A₀ = 26λ₈(0)/D_E`, the leading coefficient
`B_{E,2} = C·A_E(0)·κ†/L` is Attack 09's (19),
`B₂ = 26Cλ₈(0)κ†/(D_E log₁₁(12))` — the same 50 instances. The symbolic
side's `j(t) = log(1+t)/log₁₁(12)` is Attack 09's (4); the two sessions are
using one normalisation of the cyclotomic variable (`χ_cyc(γ) = 12`).

## The number

`L = log₁₁(12) = Σ_{m≥1} (−1)^{m+1} 11^m/m`, summed exactly in `Q` to 60
terms (the omitted terms have valuation `≥ 60 − 1`), reduced mod `11¹²`:

| | |
| --- | --- |
| `L mod 11¹²` | `2580404199593` |
| digits, low to high | `0, 1, 5, 9, 9, 9, 5, 8, 3, 5, 0, 9` |
| `v₁₁(L)` | `1` |
| `L/11 mod 11¹¹` | `234582199963` |
| cross-check `log(144)/2 = log(1 + 11·13)/2` | identical |

Consequence for the document's normalisation: `j₁ = 1/L` has `v₁₁ = −1`,
so `B_i^lead = C A_i(0) j_e κ_i` is not 11-integral even when `C`, `A_i(0)`,
`κ_i` are; relative ratios (4.4), (10.1), (11.x) cancel the `11⁻¹`, an
absolute anchor (§O7) will have to account for it.

## The labels

| where | what |
| --- | --- |
| the header | "Conditional symbolic theorem；未做新的大型數值計算；未主張 BSD 已證明" |
| §7 | "不能因此推出 q_f = 1" |
| §6 | "relative calibration eliminates C; absolute BSD may still require one absolute anchor" |
| §12 | "本輪沒有構造這個 determinant lift" |
| §13.2 | ten unproved items, the last "BSD 猜想已被證明" |

## What this line can supply to the symbolic side next

* For **Round 002 (the determinant-line lift of rank-2 data)**, the numbers
  on 389.a1 at 11 that already exist in this tree: the height Gram matrix
  `H` and the adjugate identities (RUN-073), the local logarithm
  `ℓ̄ = (4, 10)` with `ker ℓ̄ ∋ P + 4Q` (RUN-072), `[16]P`, `[16]Q` exactly
  (RUN-072), the regulator `0.1524601779…` and `L''(E,1)/2 =
  0.7593165002884` (RUN-073), `μ = 0`, `λ = 2` for the cyclotomic
  L-function (RUN-071), the plus and minus eigenlines tied to `Ω^±`
  (RUN-076). If the lift is written down as a formula in these, it can be
  evaluated here.
* For a **rank-0 calibrator** `E_0`: name the curve. `ℓ_0 = Col_0(κ_0)` is
  an algebraic L-value times an Euler factor; this tree computes
  `L(E_0, 1)/Ω` from `a_n` and the modular symbol `[0]⁺` mod 11 from the
  Manin relations, so `b_0`, `ℓ_0` and their nonvanishing (oracle O3) can
  be supplied at a stated scale.
* **PC-001** has not been handed to this line. Its rank-0 → rank-2 formula
  is verified here only as the special case of (4.4); the identification of
  its objects with genuine projected Beilinson–Flach data is the local
  side's, and this line will verify that when it arrives as a package.

## The drill

**347 defects, 347 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 75 controls undisturbed, over 107 checks.

The 6 planted for this gate, each turning `symbolic001-calibration` red and nothing else:

| planted defect | went red |
| --- | --- |
| Symbolic 001's leading term is read one order too high, at t^(e+d+1) | `symbolic001-calibration` |
| Theorem 4.1 is applied with the ratio A_i(0)/A_k(0) inverted | `symbolic001-calibration` |
| the common factor j(t) is given a vanishing leading coefficient j_e = 0 | `symbolic001-calibration` |
| the calibration factor Gamma is formed without A_k(0)/A_i(0) | `symbolic001-calibration` |
| the reparametrisation t = t'/u is applied with u^(+m) instead of u^(-m) | `symbolic001-calibration` |
| log_11(12) is summed with all plus signs, i.e. -log(1 - 11) | `symbolic001-calibration` |


## What this round does not claim

* **That a Beilinson–Flach family satisfies (2.1)** — hypothesis, as the
  document says; nothing here bears on it.
* **PC-001.** Not seen.
* **The determinant-line lift of §12** — not constructed there, not here.
* **Anything about `C`, `q_f`, `n`, `B₂`, `𝔰₁₁` or BSD.** The document
  proves that relative calibration does not need `C`; it does not compute
  `C`, and neither does this round.
