# RUN-082 — BSD Symbolic Rounds 002–004 (the web GPT's determinant-line lift, anchored projective jet, higher projective jets): every boxed identity instantiated exactly on random instances and every one holds; the gauge weights 2 and 4 confirmed independent of the jet order; the one slip a reader could make — a calibrator power that follows the jet order — exercised as a negative control

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [Round 002](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_002_Determinant_Line_Lift_of_Rank_2_Calibration.md), [Round 003](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_003_Anchored_Projective_Jet_and_Bockstein_Bridge.md), [Round 004](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_004_Higher_Projective_Jets_and_First_Nonzero_Determinant_Order.md) — three of the six symbolic documents Neo dropped on 2026-09-13 afternoon in `C:\Users\kakon\Downloads\BSD_Symbolic_Round` ([provenance](../data/external/gpt-symbolic-rounds/PROVENANCE.json)); pure symbolic derivation, no computation in them
**Tools:** [`src84_symbolic002_004_determinant_jets.py`](../code/src84_symbolic002_004_determinant_jets.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src84-symbolic002-004-determinant-jets.json`](../data/gate-logs/src84-symbolic002-004-determinant-jets.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the three documents are conditional linear-algebra statements about a two-dimensional space `H` and formal families in it, and they are correct as such — every boxed identity was instantiated with exact arithmetic (exterior algebra on `K²`, formal families in one and two variables with vector coefficients truncated at total degree 5, unit renormalisations, coordinate changes, companion operators) on 60 random instances each, and every one holds. Round 002: the single-vector no-go (Theorem 2.1, by `g_b = diag(1, b)`); the two-class determinant law `Δ̂ = C²a₁a₂Δ` (5.2); the gauge-balance criterion (7.1); the calibration `Δ_E = a₀²k₀²/(a_{E,1}a_{E,2})·Δ̂_E/b₀²` (8.3) and its rank-`r` form (9.1); the height determinant as a tensor, `R_h(Δ⊗Δ) = det Gram` quadratic in `Δ` (10.2), weight 4 (11.1), the calibrated regulator (12.1); `κ ∧ (uD + a)κ = u·κ ∧ Dκ` (16.2); the jet wedge `κ₀' ∧ κ₁' = u⁻³κ₀ ∧ κ₁` under `t' = ut + at²`, checked by substituting the inverse series (17.1); the `q_f` degrees `−2`, `−4` and their cancellation by `b₀²`, `b₀⁴` (§18). Round 003: the anchored jet `𝒥_Z(ξ) = κ ∧ dZ₀(ξ)` and the unit-shear theorem `𝒥_{gZ} = g₀²𝒥_Z` for arbitrary unit series `g` (4.2), so the first-order transport contamination `dC₀`, `dA₀` disappears (5.2); the projective derivative unit-invariant (8.1); a nonzero `KS_Z` has a one-dimensional kernel and any transverse direction gives a nonzero anchored jet (10.1); the raw `u ∧ v` is *not* invariant under `g = 1 + aX + bt` while `κ ∧ u`, `κ ∧ v` are (12.1–12.2, §13) — the document's correction of its own Round 002 candidate is right; the mod-`L` Bockstein criterion (14.2) and its affine ambiguity (§15); the covector law `𝐉_Z' = 𝐉_Z J⁻¹` under `(X',t') = J(X,t)`, checked by substituting `J⁻¹(X',t')` into the family (16.1); the anchored calibration (18.1). Round 004: `m_proj`, `τ_m`; unit invariance of the order, `τ_m(gZ) = g₀τ_m(Z)`, `𝒫_m(gZ) = 𝒫_m(Z)` (6.1–6.3); `𝒜_m = κ ∧ τ_m` independent of the lift (8.2) with gauge weight 2 for `m = 1, 2, 3` (9.1) and 4 for its self-pairing (10.1); the symmetric covariant law under a linear coordinate change (11.2); the order additivity `ord π(FZ) = e + m` (13.2); the higher Bockstein criterion and ambiguity (17.2, §18); the degree-`m` binary form and its evaluation on a direction (19.1); the calibration and regulator laws with exponents 2 and 4 for every `m` (23.1, 24.1); and §25's diagnostic, `𝒜_m/b₀^m ≠ 𝒜_m/b₀²` unless `m = 2`, planted as a defect. The documents' own "not proved" lists — that a Beilinson–Flach family satisfies any hypothesis, `KS_Z ≠ 0`, the arithmetic Bockstein, the lattice identification, BSD — are read as stated.**

---

## What was checked

`H = K²`, `det H ≅ K` by `a ∧ b = a₀b₁ − a₁b₀`; families `Z(X,t) = Σ Z_{ij}X^i t^j` with vector coefficients, `Z₀₀ = κ ≠ 0`, truncated at total degree 5 (a control truncates at 7); units `g(X,t)` with `g₀ ≠ 0`; symmetric `h` with `det h ≠ 0`; 60 instances per round from one seed (a control changes it).

| round | identity | instances |
| --- | --- | ---: |
| 002 | 2.1, 5.2, 7.1, 8.3, 9.1 (`r = 3`), 10.2, 11.1, 12.1, 16.2, 17.1, §18 | 60/60 each |
| 003 | 4.2, 5.2, 8.1, 10.1, 12.2, §13, 14.2, §15, 16.1, 18.1 | 60/60 each |
| 004 | 6.1, 6.2, 6.3, 8.2, 9.1, 10.1, 11.2, 13.2, 17.2, §18, 19.1, 23.1, 24.1, §25 | 60/60 each, `m ∈ {1,2,3}` |

Three of these are worth a sentence.

**(17.1), Round 002.** The document states `κ₁' = u⁻²κ₁ − au⁻³κ₀` and the
wedge law `u⁻³`. The gate does not take the formula on trust: it inverts
`t' = ut + at² + O(t³)` to `t = t'/u − at'²/u³ + O(t'³)`, substitutes into
`z = tκ₀ + t²κ₁`, and reads off the coefficients — they are the document's,
and the wedge is `u⁻³κ₀ ∧ κ₁`. A defect that writes `u⁻²` goes red.

**(12.2) versus §13, Round 003.** Under `g = 1 + aX + bt`, `ũ ∧ ṽ = u ∧ v +
a·κ ∧ v − b·κ ∧ u`, which changes unless `a·κ ∧ v = b·κ ∧ u`; the anchored
pair `(κ ∧ u, κ ∧ v)` does not change. This is the document's own
correction of Round 002's mechanism B, and it is right. A defect that
anchors with `u ∧ v` instead of `κ` goes red.

**(11.2) and (13.2), Round 004.** The covariance of the first nonzero jet
under `(X',t') = J(X,t)` is checked by composing the degree-`m` binary form
`Σ τ_{ij}X^i t^j` with `J⁻¹` and comparing with the jet of the substituted
family — equal, with `m_proj` unchanged; and multiplying by a scalar series
`F` of order `e` moves the first transverse order to exactly `e + m` (the
associated graded ring is a domain). The exponents 2 and 4 do not move
with `m`: with `b₀ = C₀a₀k₀`, `𝒜_m(Z_E) = a₀²k₀²/A_E² · 𝒜_m(Ẑ_E)/b₀²` for
`m = 1, 2, 3` alike, and the self-pairing needs `b₀⁴`.

## The labels

| document | header | the unproved list ends with |
| --- | --- | --- |
| 002 | "no claim that BSD is proved" | "10. BSD." |
| 003 | "未主張 BSD 已證明" | "8. BSD 已證明。" |
| 004 | "未主張 BSD 已證明" | "9. BSD。" |

## The drill

**374 defects, 374 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 81 controls undisturbed, over 111 checks.

The 7 planted for this gate, each turning `symbolic002-004-jets` red and nothing else:

| planted defect | went red |
| --- | --- |
| Symbolic 002-004's determinant gauge weight is taken as 1 instead of 2 | `symbolic002-004-jets` |
| Symbolic 002-004's regulator gauge weight is taken as 2 instead of 4 | `symbolic002-004-jets` |
| the jet wedge law is written u^-2 instead of u^-3 | `symbolic002-004-jets` |
| the anchored jet is replaced by Round 002's raw wedge u ^ v, which is not unit-invariant | `symbolic002-004-jets` |
| the order additivity is read as e + m + 1 | `symbolic002-004-jets` |
| the covector law is applied with J instead of J^-1 | `symbolic002-004-jets` |
| the calibrator power is made to follow the jet order m instead of the exterior degree 2 | `symbolic002-004-jets` |


## What this round does not claim

* **That any of the hypotheses is satisfied by a genuine arithmetic
  family** — the documents' own lists (Round 002 §24, Round 003 §26, Round
  004 §27) stand; nothing here bears on `KS_Z ≠ 0`, the Bockstein operator,
  the lattice identification or BSD.
* **Nothing about `C`, `q_f`, `𝔰₁₁`.** The documents show the common scalar
  cancels at every level with the right power; they do not compute it and
  neither does this round.
