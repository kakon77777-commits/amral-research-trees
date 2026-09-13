# RUN-081 — PC-002 (the local GPT-6 line's relative regulator germ and Farey cup normalisation): the four 11-adic series of 389.a1 and 19.a1 recomputed to t¹²⁰ from the level-1331 layer with this line's own eigenlines — 2420 summand rows, 484 coefficients, Q(t) with Weierstrass degree 2 and leading term 7 — identical; the cup pairing rebuilt on the cocycle spaces, J_E = 1, J_0 = 3, Q_∪ and its four-line invariance; the comparison theorem read

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`PC-002-RELATIVE-REGULATOR.md`](../data/external/gpt6-local-period-calibration/reports/PC-002-RELATIVE-REGULATOR.md) with [`pc002-inputs.json`](../data/external/gpt6-local-period-calibration/data/pc002-inputs.json), [`pc002-relative-regulator.json`](../data/external/gpt6-local-period-calibration/data/pc002-relative-regulator.json) and [`pc002-cup-normalization.json`](../data/external/gpt6-local-period-calibration/data/pc002-cup-normalization.json) — the second round of the local GPT-6 line, commit `85cf079` ([provenance](../data/external/gpt6-local-period-calibration/PROVENANCE.json))
**Tools:** [`src83_pc002_relative_regulator.py`](../code/src83_pc002_relative_regulator.py), [`src82_pc001_calibrator_19a1.py`](../code/src82_pc001_calibrator_19a1.py), [`src79_attack09_eisenstein_leading_term.py`](../code/src79_attack09_eisenstein_leading_term.py), [`src70_kurihara_modular_symbols.py`](../code/src70_kurihara_modular_symbols.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src83-pc002-relative-regulator.json`](../data/gate-logs/src83-pc002-relative-regulator.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: PC-002 defines, for `E = 389.a1` and `E₀ = 19.a1` at `p = 11` on the eigenlines pinned at PC-001 and RUN-068/077, the ordinary series `L_i(t) = L₁₁(E_i, σ_t)` and the twisted odd-branch series `λ_i(t) = L₁₁(E_i ⊗ χ₈, x⁻¹σ_t)` with `σ_t(12) = 1 + t`, and computes `Q(t) = L_Eλ_E/(L_0λ_0) mod (11, t¹²¹)` from the `11³` layer — `Q = 7t² + 10t³ + 9t⁴ + 7t⁵ + 6t⁶ + 7t⁹ + t¹⁰ + …` — by a finite-layer lemma that certifies 121 coefficients from 1210 residue balls per curve; then a Farey cup pairing `J_N(u,v) = (1/6)Σ_i (u_i v_{Ri} − v_i u_{Ri})` on closed edge cochains, with `J_E ≡ 1`, `J_0 ≡ 3`, and `Q_∪ = (J_0/J_E)Q`, invariant under rescaling the four eigenlines. **All of it recomputes exactly.** The four frozen input vectors are this line's own two 389 eigenlines (RUN-068's engine, `λ(1,5) = 1` and index 3 ↦ 1) and RUN-080's two 19 eigenlines; the cyclotomic exponents `e_u = log⟨u⟩/log 12 mod 121` by discrete logarithm of `u^{−120}` base 12; for each of the 2420 units `u mod 1331`, the plus symbols at `u/1331` and `u/121`, the eight twisted minus symbols, the ordinary and twisted measures and the `x⁻¹`-weighted term are identical to the line's rows, all 2420; the group-basis and `t`-basis coefficients of `L_E`, `λ_E`, `L_0`, `λ_0` (121 each) are identical, the first eleven of `L_E` being Attack 04's `(0,0,2,2,2,0,5,6,10,7,0)`; the numerator, the denominator (constant term `9·4 ≡ 3`) and `Q`'s 121 coefficients are identical, Weierstrass degree 2, leading coefficient 7; the level-121 layer agrees to width 11 and the `121 → 1331` distribution relation holds on all 220 cells (and `1331 → 14641` on all 2420 when the gate is run deep). The cup pairing on the 65- and 3-dimensional cocycle spaces is alternating with rank 64 and 2, the cusp gauge `−e₀ + e_N` is a cocycle spanning each radical, `J_E = 1`, `J_0 = 3`, `Q_∪`'s 121 coefficients are identical, and a random four-line rescaling leaves `Q_∪` fixed. Read, not verified: that `Q` is `(D_E/D_0)(R_E/R_0)|_{X=0}` (Loeffler–Rivero C1.9–C1.11 and the smoothing identity (8)); the identification of the `Γ₀` cup with the adjoint-period/Petersson convention, which the line says is not done ("不能直接把 3/1 當成 D_0/D_E"); the torsion-free-cover proof that (6) is the cup product of the compactified curve — what is checked is the formula's algebra on these cochains. `Q` and `Q_∪` are, as the line says, analytic comparison targets, not a measured regulator; `C`, `𝔰₁₁`, the Beilinson–Flach class and BSD are untouched.**

---

## §2–§3 — the four series

The measures, with `α_E ≡ 7`, `α_{E,χ} ≡ 4`, `α_0 ≡ 3`, `α_{0,χ} ≡ 8`:
`μ_i(u + 11³Z) = α_i⁻³Φ_i⁺(u/1331) − α_i⁻⁴Φ_i⁺(u/121)` and the same with
`Φ_{i,χ₈}(r) = Σ_{b odd} χ₈(b)Φ_i⁻(r + b/8)` and `α_{i,χ}`; the exponent
`e_u` with `⟨u⟩ = u·ω(u)⁻¹ = u^{−120} (mod 1331)`, `12^{e_u} ≡ ⟨u⟩`;
`L_i(t) = Σ_u μ_i(u)(1+t)^{e_u}`, `λ_i(t) = Σ_u u⁻¹μ_{i,χ}(u)(1+t)^{e_u}` in
`F₁₁[t]/(t¹²¹)`.

| | units | rows identical | group coefficients | `t` coefficients | width-11 vs level 121 | `121 → 1331` cells |
| --- | ---: | ---: | --- | --- | --- | ---: |
| `389.a1` | 1210 | 1210 / 1210 | `L`, `λ` identical | `L`, `λ` identical (121 each) | agree | 110, 0 failures |
| `19.a1` | 1210 | 1210 / 1210 | identical | identical | agree | 110, 0 failures |

| series | first eleven coefficients |
| --- | --- |
| `L_E` | `0, 0, 2, 2, 2, 0, 5, 6, 10, 7, 0` (Attack 04 / RUN-071) |
| `λ_E` | `5, 9, 10, 6, 6, 2, 0, 8, 8, 9, 10` (its constant term is RUN-077's `λ₈(0) = 5`) |
| `L_0` | `9, 3, 10, 3, 1, 6, 9, 6, 2, 0, 6` (constant term RUN-080's 9) |
| `λ_0` | `4, 3, 10, 9, 4, 10, 2, 7, 3, 8, 3` (constant term RUN-080's 4) |
| `Q = L_Eλ_E/(L_0λ_0)` | `0, 0, 7, 10, 9, 7, 6, 0, 0, 7, 1` — identical to `t¹²⁰` |

The denominator's constant term is `9·4 ≡ 3`, a unit, so the division
loses nothing; `ord_t Q = 2` with leading `(2·5)/(9·4) ≡ 7`. As the line
says, this is a Weierstrass degree mod 11, not a statement about the
characteristic-zero order.

The finite-layer lemma (5) is theory the line proves; what is exercised
here is its consequence: the level-121 layer produces the same first
eleven coefficients, and every coarse ball's measure is the sum of its
eleven refinements at the next layer — `121 → 1331` on 220 cells in the
drilled check, `1331 → 14641` on 2420 cells in the deep run, with the
level-14641 series agreeing with the level-1331 series to `t¹²⁰`.

## §4 — the cup pairing

`R(c,d) = (d, −c−d)` on the darts `i ∈ P¹(F_N)`; `J_N(u,v) = 6⁻¹Σ_i (u_i v_{Ri} − v_i u_{Ri})` mod 11.

| level | cocycle dimension | rank | radical | cusp gauge `−e₀ + e_N` | `J(plus, minus)` |
| ---: | ---: | ---: | ---: | --- | ---: |
| 389 | 65 | 64 | 1 | a cocycle, in the radical | **1** |
| 19 | 3 | 2 | 1 | a cocycle, in the radical | **3** |

The cocycle spaces are the duals of the Manin quotients (the nullspaces of
the `S` and `R` relations); the eigenlines are cocycles, the form is
alternating, its rank is `2g`, and the radical is the cusp gauge. So
`Q_∪ = (J_0/J_E)Q = 3Q`: `0, 0, 10, 8, 5, 10, 7, 0, 0, 10, 3, …`, identical to
`t¹²⁰`. Rescaling the four lines by `a, b, c, d`: `Q ↦ (ab/cd)Q`,
`J_E ↦ abJ_E`, `J_0 ↦ cdJ_0`, `Q_∪` fixed — checked on a random draw. The
line's own restriction is repeated: this is invariance under the four
eigenline units, not under arbitrary cochain representatives.

## The labels

| where | what |
| --- | --- |
| the results | "式 (2)–(3) 是具體的解析比較目標；不是由原始 BF 類座標測量出的 regulator" |
| §3 | "單憑 mod 11 展開，不能推出 characteristic-zero 的常數及一次項恰為零" |
| §4 | "不是任意更換 cochain 代表時所有解析函數都不變" |
| §5 | "不能直接把 3/1 當成 D_0/D_E"; "再往後仍需真正的 BF leading class" |
| the output | `actual_BF_regulator_measured: false`, `BF_class_coordinates_computed: false`, `Coleman_weight_trace_jet_computed: false`, `adjoint_period_ratio_computed: false`, `C_computed: false`, `s11_computed: false`, `BSD_proved: false`; `matched_to_LR_adjoint_periods: false` |

## The drill

**374 defects, 374 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 81 controls undisturbed, over 111 checks.

The 7 planted for this gate, each turning `pc002-relative-regulator` red and nothing else:

| planted defect | went red |
| --- | --- |
| PC-002's twisted unit roots are taken as alpha instead of chi_8(11) alpha | `pc002-relative-regulator` |
| PC-002's lambda series integrate x instead of x^-1 | `pc002-relative-regulator` |
| the Teichmuller projection is taken as u^-121, so <u> is not a power of 12 | `pc002-relative-regulator` |
| the Farey cup pairing is divided by 2 instead of 6 | `pc002-relative-regulator` |
| the Farey cup pairing is taken with the opposite orientation R^-1 | `pc002-relative-regulator` |
| PC-002's measures have their second term added instead of subtracted | `pc002-relative-regulator` |
| PC-002's series are produced from the level-121 layer, which certifies only 11 coefficients | `pc002-relative-regulator` |


## What this round does not claim

* **(4) — `Q = (D_E/D_0)(R_E/R_0)|_{X=0}`** — Loeffler–Rivero as cited; read.
* **The cup formula as the cup product of `H¹` of the compactified curve**
  — the torsion-free-cover proof is read; the algebra of (6) on these
  cochains is what is checked.
* **The `Γ₀`-to-adjoint-period identification** — not done by the line,
  not here; `3` is a cup ratio at the pinned scales, not `D_0/D_E`.
* **Nothing about `C`, `𝔰₁₁`, the Beilinson–Flach class, the weight-`X`
  trace jet, or BSD.**
