# RUN-084 — BSD Symbolic Rounds 010–012 (the web GPT's proof-obligation architecture, reciprocity-kernel dichotomy, adelic descent): the architecture read against itself and against this line's logs, its one scalar identity evaluated on 389.a1; every boxed statement of the reciprocity and adelic rounds instantiated exactly; the rational-reconstruction mechanism run on this line's own [16]P and [16]Q with the explicit precision threshold — and one slip found, the sign in Theorem 19.1

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [Round 010](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_010_Four_Bridge_Closure_Diagram_and_Minimal_Missing_Theorems.md), [Round 011](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_011_Reciprocity_Kernel_Nonannihilation_and_Minimal_Leading_Term_Theorem.md), [Round 012](../data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_012_Adelic_Descent_Principal_Idele_Obstruction_and_Rational_Reconstruction.md) — the three symbolic documents that arrived in the drop folder later on 2026-09-13 ([provenance](../data/external/gpt-symbolic-rounds/PROVENANCE.json)); Rounds 008 and 009, which 010 cites, were not in the folder
**Tools:** [`src86_symbolic010_012_architecture_reciprocity_adelic.py`](../code/src86_symbolic010_012_architecture_reciprocity_adelic.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src86-symbolic010-012-architecture-reciprocity-adelic.json`](../data/gate-logs/src86-symbolic010-012-architecture-reciprocity-adelic.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result. Round 010 is a synthesis, not a theorem, and it is internally consistent: the chain (5.1) parsed from the document is `A0 → … → A10` over the alphabet `S / C / T`, and its only two pure-`T` arrows are exactly the two the text singles out as theorem-level cuts — `A3 → A4` (T1, global descent, §11) and `A8 → A9` (T6, complex comparison, §22); the seventeen-row obligation matrix (§31) agrees with its own typing (`T ⟺ "no"`, `C ⟺ "yes"`, `S ⟺ "yes, already symbolic"`), its six `T` rows are T1–T6 of §25 in order, and the four cuts of (27.1) partition `{T1, …, T6}` as `{1}, {2,3,4}, {5}, {6}`. Of its ten "symbolically closed" invariants, S1–S8 are statements this line has instantiated on exact random instances (RUN-079, 082, 083 — read here from those gate logs, the named checks green), S9–S10 belong to Rounds 008–009 which were not delivered (S10's equality case is Round 011's (5.1), checked below); no-go N1 is RUN-083's `√3 ∈ Q₁₁ ∖ Q`. Its schematic (24.1), `L''(E,1)/2 = Ω_E·Reg(E)·q_fin`, holds on `389.a1` with this tree's own `Ω = 4.980425121710` (RUN-017), the regulator `0.15246017794314` and `L''/2 = 0.7593165002884` (RUN-026/073), with `q_fin = 1` (Tamagawa 1, torsion 1, `Ш` taken as 1): ratio `1.000000000000`. Round 011 — every boxed statement instantiated on 40 exact random instances, a quarter with the reciprocity channel zero: the kernel dichotomy (3.1–3.2); tensor nonannihilation (4.1); the `𝔪`-adic order theorem `ord ℒ = e + m` on genuine two-variable families `U·E·λ(Z_tr)` (5.1) and its one-variable form (17.1); one witness (7.1); the lifted functional kills exactly `L` (8.2); `c' = uc` (9.1); a nonzero annihilator vector gives a nonzero quotient functional under a perfect pairing (10.1); the determinant criterion `det Φ ≠ 0 ⟺ Φ̄ ≠ 0 ⟺ Φ̄ iso` for `Φ(L) ⊂ L_W`, checked in a non-adapted basis (11.3–11.5, 12.1); **nonannihilation ≠ directional criticality** — a binary form `τ_m` with a rational root direction has `(id ⊗ λ)τ_m ≠ 0` while `τ_m(ξ_crit) = 0` (14.1), and along the path `sξ_crit` the analytic order is strictly larger than `e + m` while along a generic `ξ` it is `e_ξ + m` (15.1–15.2, 23.1) with leading coefficient exactly `U(0)·E_e(ξ)·λ(τ_m(ξ))` (23.2); cross-curve transport and the calibrator witness (19.2, 20.1); the `dim Q = 2` countermodel (§25) and the `d = 2` determinant criterion (§26); the consistency triangle (§30). Round 012 — every boxed statement instantiated on explicit ideles of `Q` with rational components at `{2, 3, 5, 7, 11, 13, ∞}`: valuations as lattice classes (2.1); `Π p^{d_p}` as the positive representative and the injectivity of the valuation vector mod sign (3.1–3.2, 13.1, 23.1); `a = q₀·u` (6.4); Theorem 7.1 in both directions on diagonal and non-diagonal ideles; the unit obstruction, the norm identity `‖a‖ = |a_∞|/q₀`, and the no-go (9.4) by an idele of norm 1 with every valuation zero that is not principal (8.1, 9.2–9.4, 10.1, 24.1); `a² = Π p^{2d_p}` (12.1); `S`-unit reconstruction (14.1); the finitely-many-exact-checks no-go (18.1); the ledger (20.3) with the explicit idele that has `𝔫 = 1`, `𝔲 = 1` and is not principal (the sign condition the document says is needed); and §21 made explicit — rational reconstruction from a residue mod `11^k` is unique when `11^k > 2MN`, exhaustively at `11³` for `|m|, n ≤ 25`, with the extended Euclidean algorithm recovering every admissible fraction, and a collision at `11²`; the same mechanism recovers, from their residues, the exact formal parameters `z = −x/y` of this line's `[16]P` and `[16]Q` (RUN-072; 39- and 54-digit numerators and denominators) at `k = 76` and `k = 104` and fails at a third of that precision — with `z mod 121 = 99, 66`, RUN-072's numbers. **One slip: Theorem 19.1 allows the diagonal sign `ε = −1` while its hypothesis 2 fixes `u_p = 1` outside `S`; the idele with `u = −1` on `S` and at `∞` and `u = +1` outside is not principal by the round's own Theorem 7.1, so the "if" direction is false at `ε = −1` and the correct finite check is `u_ℓ = 1` on `S`, `u_∞ = 1`.** Everything else the three documents box is right as a conditional statement; what they list as not proved — the actual descent, support, reciprocity and comparison theorems, `S`, `d_ℓ`, BSD — they list, and this round adds nothing to those lists.**

---

## Round 010 — what a synthesis can be checked against

| statement | how | result |
| --- | --- | --- |
| (5.1) the chain | parsed from the document: nodes, arrows, alphabet | `A0 … A10`, ten arrows `T/C, S, S/C, T, T/C, T/C, T/C, T/C, T, S` |
| the pure-`T` arrows are the two theorem-level cuts the text names | §11 (T1 at `A3 → A4`), §22 (T6 at `A8 → A9`) | arrows 3 and 8, exactly |
| §31 obligation matrix | each row's type vs its "can local compute finish it?" | 17 rows, all consistent |
| the six `T` rows are T1–T6 of §25 | keyword match in order | descent, support, complex identification, fundamental-line, reciprocity, complex-to-`p`-adic |
| (27.1) the cuts partition `{T1, …, T6}` | parsed from §27 | `{1}, {2,3,4}, {5}, {6}` |
| S1–S8, N1 | this line's gate logs | `src81` theorem 4.4 126/126; `src84` 5.2, 9.1, 11.1, 10.1, 9.1, 23.1, 4.2, 6.3, 14.2, 17.2; `src85` 8.1, 9.1, 14.2, 15.1, 18.1, 4.1 — all green |
| S9, S10 | Rounds 008–009 | not in the folder; S10's equality case is Round 011 (5.1), below |
| (24.1) on `389.a1` | `Ω · Reg · q_fin` vs `L''/2` | `4.980425121710 × 0.15246017794314 × 1 = 0.7593165002884`, ratio `1.000000000000` |

The document's own caveat on (24.1) stands: which torsion, Tamagawa,
`Ш` and period conventions enter is for the fundamental-line theorem to
decide (T4); the instance says only that with the tree's `Ω`, the
corpus regulator and `L''/2`, the finite factor is `1` — which is the
rank-2 BSD identity this line checked at RUN-026.

## Round 011 — the one-dimensional transverse quotient

`H = K²`, `L = Kκ`, `Q = H/L`, `λ: Q → A` a scalar `c`; families in
`K[[X, t]]` truncated at total degree 6; 40 instances, 10 with `c = 0`.

| statement | instantiated as | instances |
| --- | --- | ---: |
| 3.1, 3.2, 4.1, 7.1 | `ker λ = Q ⟺ c = 0`; `c ≠ 0 ⇒ cτ ≠ 0` on `K^{m+1}` | 40/40 |
| 5.1 | `ℒ = U·E·c·Z_tr`, `ord_𝔪 ℒ = e + m` for `c ≠ 0`, `ℒ ≡ 0` for `c = 0` | 40/40 |
| 8.2, 9.1 | `λ̃ = λ∘π`: kernel `= L` iff `c ≠ 0`, `= H` iff `c = 0`; `λ̃(uq + aκ) = uc` | 40/40 |
| 10.1 | `β(x, η) = xᵀBη`, `B` invertible, `η ∈ L^⊥ ∖ 0`: `β(κ, η) = 0`, `β(q, η) ≠ 0` | 40/40 |
| 11.3–11.5, 12.1 | `Φ = P_W [[a,b],[0,d]] P⁻¹` with random `P, P_W`: `Φ(κ) = aκ_W`, `det Φ ≠ 0 ⟺ Φ̄ ≠ 0 ⟺ d ≠ 0`; `μΦ̄ ≠ 0` | 40/40 (8 with `d = 0`) |
| 14.1 | `τ_m = (X − rt)·g`: `c·τ_m ≠ 0`, `τ_m(r, 1) = 0` | 40/40 |
| 15.1, 15.2, 23.1, 23.2 | along `sξ`: `r_ξ = e_ξ + m` with leading coefficient `U(0)·E_e(ξ)·c·τ_m(ξ)`; along `sξ_crit`: `r > e + m` | 30/30 |
| 17.1 | one variable, `Z = t^m·unit`: `ord ℒ = e + m` | 30/30 |
| 19.2, 20.1 | `ψ_i λ_i = u_i λ_* φ_i` on three partners; `b₀ = λ₀(q₀) ≠ 0 ⇒` all `λ_i ≠ 0` | 40/40 |
| §25, §26 | every nonzero functional on `K²` has a kernel vector, exhibited; `det Λ ≠ 0 ⇒ Λτ ≠ 0` | 40/40 |
| §30 | `c = 0 ⇒` no order equality, so order equality with `τ_m(ξ) ≠ 0` forces `c ≠ 0` | 10/10 |

The distinction the round is built on — §14 and §32, channel zero versus
directional criticality — is visible in the instances: with `c = 0` the
whole section vanishes; with `c ≠ 0` and `ξ` on the exceptional divisor
the order along that path exceeds `e + m` while every other direction
gives `e_ξ + m` exactly. Round 011 §13's warning is repeated here for
this line's own material: RUN-072's localisation `ℓ̄ = (4, 10)` mod 11 with
`ker ℓ̄ ∋ P + 4Q` is a candidate `M_loc`, not an identified `Φ`.

## Round 012 — ideles of `Q`

Ideles carry rational components at `{2, 3, 5, 7, 11, 13, ∞}` and `1`
elsewhere; "principal" is decidable exactly (all components one rational).

| statement | instantiated as | instances |
| --- | --- | ---: |
| 2.1 | `v_ℓ(u·a) = v_ℓ(a)` for `ℓ`-units `u`, `ℓ ∈ {2,3,5}` | 40/40 |
| 3.1, 3.2, 13.1 | `Π p^{v_p(a)} = |a|`; same valuation vector `⟺` same `|a|` | 40/40 |
| 6.4, 7.1, 7.3, 9.2 | diagonal ideles: `u_p` units, `u_v = ε`, `a = εq₀`, `‖a‖ = 1` | 40/40 |
| 7.1 both directions | random non-diagonal ideles: principal `⟺` all `u_v = ε` | 40/40 |
| 9.3 | `|a_∞| Π p^{−v_p(a_p)} = |a_∞|/q₀` exactly | 40/40 |
| 8.1, 9.4, 10.1, 24.1 | `a_p = u_p q₀` with random units, `a_∞ = q₀`: every `d_p` that of `q₀`, `‖a‖ = 1`, not principal | 40/40 |
| 12.1, 32.1 | `a² = Π p^{2d_p}` | 40/40 |
| 14.1 | `S`-units rebuilt from their valuations on `S`, zero outside | 40/40 |
| 18.1 | equal to `q` at `2, 3, 5, ∞` and in every valuation, a unit change at 13: not principal | 40/40 |
| 19.1 (corrected) | `u_p = 1` outside `S`: principal `⟺ u_ℓ = 1` on `S` and `u_∞ = 1` | 40/40 |
| 20.3 | `𝔫 = 1`, `𝔲 = 1` for the diagonal; `a_∞ = −q₀`, `u_p = +1` has both and is not principal | 40/40 |
| 23.1 | `p^{d_p}Z_p` for random `(d_p)` reconstruct `a₀` with `v_p(a₀) = d_p`, `0` outside | 40/40 |

### §21 — rational reconstruction, with the threshold made explicit

* Modulus `11³ = 1331`, bounds `|m| ≤ 25`, `1 ≤ n ≤ 25` (`2MN = 1250 <
  1331`): all admissible fractions have distinct residues — checked
  exhaustively — and the extended Euclidean algorithm returns each one.
* Modulus `11² = 121`, the same bounds: `−25/21 ≡ −24/25 ≡ 91`.
* Modulus `11⁶`, `|m|, n ≤ 40`, 40 random fractions: all recovered.
* **On this line's own objects.** `z = −x/y` of `[16]P` and `[16]Q` on
  `389.a1` — RUN-072's points, whose `x`-coordinates have 37/36- and
  53/53-digit numerators and denominators — are `11`-integral with
  `v₁₁(z) = 1`, `z mod 121 = 99` and `66` (RUN-072's `s_P`, `s_Q`); `z`
  has 39/39 and 54/54 digits. With the height bound `M = N = 10^{39}`
  (resp. `10^{54}`) the threshold is `k = 76` (resp. `104`), and from the
  residue mod `11^k` the exact rational comes back; at `k = 25` (resp.
  `34`) the algorithm returns an integer that is not `z`. This is (21.1)
  in the document's own words: rationality + a height bound + enough
  precision reconstruct; precision alone does not.

### The slip in Theorem 19.1

Hypotheses: finite support in `S`; `u_p = 1` for every `p ∉ S`; exact
units on `S`; the real component. Claim: principal iff there is
`ε ∈ {±1}` with `u_ℓ = ε` on `S` and `u_∞ = ε`. Take `S = {2, 3, 5}`,
`u_2 = u_3 = u_5 = u_∞ = −1`, `u_7 = u_11 = u_13 = 1`: the claim says
principal with `ε = −1`; Theorem 7.1 (every `u_v` equal to one sign)
says not, and directly the components are `−q₀` at four places and `q₀`
at three, the diagonal image of nothing. The "only if" direction holds
and forces `ε = +1`; the correct finite check is `u_ℓ = 1` on `S` and
`u_∞ = 1`. A small slip, but §30's "red flag" is about exactly this
kind of sign bookkeeping. The gate records the counterexample and checks
the corrected statement.

## The labels

| document | header | what it says of itself |
| --- | --- | --- |
| 010 | "未主張 BSD 已證明" | §37: "這不等於 BSD proof closure"; §30 no-go N1–N6 |
| 011 | "未主張 BSD 已證明" | §34 "本輪沒有證明", ending "10. BSD。" |
| 012 | "no claim that BSD is proved" | §37 "Not proved", ending "10. BSD." |

## The drill

**382 defects, 382 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 85 controls undisturbed, over 112 checks.

The 8 planted for this gate, each turning `symbolic010-012-adelic` red and nothing else:

| planted defect | went red |
| --- | --- |
| Symbolic 010's (24.1) is evaluated on 389.a1 with the finite factor doubled | `symbolic010-012-adelic` |
| Symbolic 011's order theorem is read as e + m + 1 | `symbolic010-012-adelic` |
| the reciprocity kernel dichotomy is asserted for a two-dimensional transverse quotient | `symbolic010-012-adelic` |
| the leading coefficient (23.2) is taken without the analytic unit U(0) | `symbolic010-012-adelic` |
| the induced quotient map of an upper-triangular Phi is read off the (1,2) entry b instead of d | `symbolic010-012-adelic` |
| Symbolic 012's diagonal units are taken as {+1} only, so a negative rational is not principal | `symbolic010-012-adelic` |
| the p-adic absolute value is taken as p^(+v), so the idele norm is not \|a_inf\|/q_0 | `symbolic010-012-adelic` |
| rational reconstruction is claimed unique when 11^k > MN instead of 2MN | `symbolic010-012-adelic` |

Because the (24.1) instance uses the tree's live `Ω`, regulator and AGM, five defects planted for older checks — the real period doubled or one-component (`rank2-bsd-identity`, `real-period-vs-integration`), the regulator inverted (`rank2-bsd-identity`), the AGM stopped after one step (`anchor-11a1`) — now also turn this check red; the drill log records every check that went red for each of them, and the named check catches each.

## What this round does not claim

* **Any T-type obligation** — descent, support, complex identification,
  fundamental-line assembly, explicit reciprocity, complex comparison —
  none is proved by the documents or touched here.
* **Rounds 008–009** — not delivered; S9 and S10 are not checked beyond
  S10's equality case.
* **Any actual `S`, `d_ℓ`, unit class, or the rationality of the actual
  determinant** — the reconstruction instance uses objects whose
  rationality is known by construction.
* **Nothing about `C`, `𝔰₁₁`, or BSD.**
