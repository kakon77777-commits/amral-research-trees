# RUN-083 — BSD Symbolic Rounds 005–007 (the web GPT's determinant-lattice torsor, rational descent and support control, derived determinant complex): every boxed statement instantiated on explicit integer lattices, rational scalars, ℓ-adic valuations and two-term complexes of free Z-modules — the sign calibration of the derived Euler defect shown to reproduce the sublattice law, and the mapping-cone formula checked on cones computed from their own differentials

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [Round 005](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_005_Determinant_Lattice_Torsor_and_Absolute_BSD_Anchor.md), [Round 006](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_006_Rational_Descent_Support_Control_and_Finite_Prime_Closure.md), [Round 007](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_007_Derived_Determinant_Complex_and_Euler_Characteristic_Closure.md) — the last three of the six symbolic documents of 2026-09-13 ([provenance](../data/external/gpt-symbolic-rounds/PROVENANCE.json))
**Tools:** [`src85_symbolic005_007_lattice_torsor_euler.py`](../code/src85_symbolic005_007_lattice_torsor_euler.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src85-symbolic005-007-lattice-torsor-euler.json`](../data/gate-logs/src85-symbolic005-007-lattice-torsor-euler.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the three documents move the absolute-anchor problem from "a mysterious period constant" to a rank-1 lattice torsor with finite local valuation data, and everything they state about that torsor is right. Instantiated exactly on 40 random instances each: Round 005 — `det Λ' = n·det Λ` for a full-rank sublattice of index `n = |det M|`, with the index confirmed as the product of the Smith invariants (5.1–5.2); `Reg(aΔ) = a²Reg` (8.1) and the index-square law `det(MᵀGM) = det(M)² det G` in ranks 2 and 3 (9.1, §10); `a = ±√(ratio)` (11.2); a prime-to-11 index is invisible to the `Z₁₁`-lattice, `p ∤ n ⟺ M invertible mod p` (14.1–14.2); `a` rebuilt from its valuations on a finite support (16.1, 17.2); `h ↦ uh` gives `u²`, together `a²u²` (19.2); the ledger `C⁴n²u²` (20.1); the isogeny law `Reg(E') = d²/I_φ² Reg(E)` from heights `×d` and image index `I_φ` (22.1); `v₁₁(2) = 0` with `2 ≠ ±1` (26.1). Round 006 — Galois fixedness gives `Q_p`-descent, not `Q`-descent: in `Q(√2)`, fixed `⟺` `y = 0`, and trace and norm are rational for every `x + y√2` (3.1, §8); the no-go 4.1 made concrete, `√3 ∈ Q₁₁ ∖ Q` lifted to `11¹²` (`2356328188186`, `5² ≡ 3`); a rational functional detects rationality (7.1–7.2); Hilbert 90 for the quadratic cocycle, constructively `u = 1 + c` (9.1), leaving the `Q^×` torsor (10.1); integrality vs primitiveness (12.1) and the `S`-unit criterion (13.1); the local length formula (14.1); `v_ℓ(det φ) = length coker φ` by the gcd of maximal minors (15.1); support union and the additive ledger (17.1, 18.1); the finite-prime closure and the regulator ratio (20.1–22.1); an exact square fixes `|a|`, a square class does not, an 11-adic unit class is not an `S`-unit class (23.1, 24.1). Round 007 — with `𝒜 = det(C)⁻¹`, the model `R →ϖⁿ R` gives `+n` in degrees `(1,2)` and `−n` in `(0,1)` (§4); `δ = Σ(−1)^i length H^i_tor` equals `v(det M)` for a square complex in degrees `(1,2)` (6.1); `𝒜 = ϖ^{len T₂ − len T₁}D_Λ` (7.1), `q = |T₂|/|T₁|` (8.2), `q/n` (9.2); `ε_ℓ = d_ℓ − δ_ℓ` and the two no-go's, `d = δ = 1` and `len T₁ = len T₂ = 1` (10.3, 11.1, 12.1); additivity on block-triangular complexes (14.2); **the mapping-cone formula (15.1–15.2) checked the hard way** — for chain maps `f = (gA, Bg)` between `Z^n →A Z^n` and `Z^n →B Z^n`, the cone's differentials `d⁰(x) = (−Ax, f¹x)`, `d¹(u,y) = f²u + By` are assembled, `d¹d⁰ = 0` confirmed, its torsion lengths read off by Smith invariants, and `Σ(−1)^i length H^i(Cone)` equals `v_ℓ(det B) − v_ℓ(det A)` on every instance, for every `g`; the lattice-inclusion case (§16) reproducing Round 005's sublattice law; the derived support theorem — the support of the relative scalar equals the support of the cone cohomology (17.1); the chain ledger over three cones (18.1); derived closure ≠ primitive closure (25.1). What none of the three documents proves — which Selmer complex, which degrees, which finite groups in which cones, `S`, `d_ℓ`, `δ_ℓ`, rationality of any actual determinant, BSD — they list, and this round adds nothing to those lists.**

---

## What was checked

| round | statement | instances |
| --- | --- | ---: |
| 005 | 5.2, 8.1, 9.1, §10, 11.2, 14.1, 16.1, 17.2, 19.2, 20.1, 22.1, 26.1 | 40/40 each |
| 006 | 3.1, 4.1 (`√3` to `11¹²`), 7.2, §8, 9.1, 10.1, 12.1, 13.1, 14.1, 15.1, 17.1, 18.1, 20.1, 22.1, 23.1, 24.1 | 40/40 each |
| 007 | §4, 6.1, 7.1, 8.2, 9.2, 10.3, 11.1, 12.1, 14.2, 15.1, §16, 17.1, 18.1, 25.1 | 40/40 each |

## The sign calibration of Round 007, and what it must reproduce

Round 007 fixes its convention by one model: `R →ϖⁿ R` in degrees `(1, 2)`
contributes `+n` to `𝒜 = det(C)⁻¹`, in degrees `(0, 1)` it contributes `−n`;
everything else is devissage. The gate adopts that convention as a
definition and checks what then *must* hold:

* for a lattice inclusion `M ⊂ N` of index `ℓ^c` in degree 1, the cone has
  `H¹ = N/M`, so `δ(Cone) = −c` and `𝒜(N) = ϖ^{−c}𝒜(M)`; since the
  degree-1 line is the determinant itself, `det M = ϖ^c det N` — Round
  005's "sublattice determinant is `index ×` lattice determinant", from
  the other end;
* for a general chain map `f: (Z^n →A Z^n) → (Z^n →B Z^n)` that is an
  isomorphism over `Q`, the relative line is `det(B)/det(A)` up to units,
  so the cone's Euler defect has to be `v(det B) − v(det A)` — and it is,
  computed from the cone's own three-term complex (`n ≤ 2`, `ℓ ∈ {2,3,5}`,
  random `g`), independent of `g`; a cone built with the wrong sign is
  not a complex (`d¹d⁰ ≠ 0`) and is reported red, not as a crash.

So the one free choice in Round 007 is consistent with Rounds 005–006, and
the theorem the documents lean on — determinant valuations are alternating
sums of cone lengths — holds on the instances where it can be computed
from scratch.

## Two concrete instances the documents ask for

* **No-Go 4.1 / 29.1 (Round 006), at `p = 11`.** `3` is a square in `Q₁₁`
  (`5² ≡ 3`): the Hensel lift is `√3 ≡ 2356328188186 (mod 11¹²)`, and no
  rational squares to 3. An `11`-adic determinant `√3·Δ_Λ` is
  `Q₁₁`-rational to any precision and is not from `D_Q`. This is exactly
  the document's point: arbitrary 11-adic precision does not replace a
  global descent theorem.
* **Theorem 14.1 (Round 005) on this line's own curve.** Nothing here is
  computed for `389.a1`; but the framework says what would close the
  absolute anchor there: rationality of `Δ_cal`, a finite support `S`, and
  `d_ℓ` for `ℓ ∈ S` — plus saturation of the lattice `⟨P, Q⟩`, which the
  eight GPT-6 packages take as an accepted input (RUN-072). Its regulator
  `0.1524601779…` (RUN-073, the corpus) is the number any `d_ℓ` would be
  measured against.

## The labels

| document | header | the unproved list ends with |
| --- | --- | --- |
| 005 | "未主張 BSD 已證明" | "9. BSD。" |
| 006 | "未主張 BSD 已證明" | "10. BSD。" |
| 007 | "未主張 BSD 已證明" | "10. BSD。" |

## The drill

**374 defects, 374 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 81 controls undisturbed, over 111 checks.

The 6 planted for this gate, each turning `symbolic005-007-lattice` red and nothing else:

| planted defect | went red |
| --- | --- |
| Symbolic 005's index enters the regulator to the first power, not squared | `symbolic005-007-lattice` |
| a height rescaling h -> uh is given exponent 1 on a rank-2 regulator | `symbolic005-007-lattice` |
| the Euler defect's sign convention is flipped | `symbolic005-007-lattice` |
| the mapping cone is built with d(x,y) = (+d_C x, f x + d_D y), which is not a complex | `symbolic005-007-lattice` |
| the Q_11-not-Q witness is sought as sqrt 2, which has no root mod 11 | `symbolic005-007-lattice` |
| an isogeny of degree d is given exponent 1 on the Gram determinant | `symbolic005-007-lattice` |


## What this round does not claim

* **Which complex, which degrees, which groups.** Round 007 §33 lists ten
  unknowns starting with the Selmer complex's degree convention; this round
  checks the formalism on complexes it builds itself, not on an arithmetic
  one.
* **Any actual `S`, `d_ℓ`, `δ_ℓ`, or rationality of an actual determinant.**
* **Nothing about `C`, `𝔰₁₁`, or BSD.**
