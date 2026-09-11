# RUN-069 — P5 v1.3: the finite Bockstein determinant computed in the truncated group ring, the ratio "3" shown to take every value in `F₁₁^×` under a change of primitive roots alone, Kim's hypotheses verified where they are computable — and the last of the 85 documents becomes a round's subject

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_P5_Determinantal_Kurihara_Semilocal_389a1_p11_v1.3`](../../../amral/public/bsd/p5/files/BSD_P5_Determinantal_Kurihara_Semilocal_389a1_p11_v1.3.md) — the third and last of the P5 documents RUN-065 named
**Tools:** [`src71_determinantal_bockstein.py`](../code/src71_determinantal_bockstein.py), [`src70_kurihara_modular_symbols.py`](../code/src70_kurihara_modular_symbols.py), [`src29_sweep_coverage.py`](../code/src29_sweep_coverage.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src71-determinantal-bockstein.json`](../data/gate-logs/src71-determinantal-bockstein.json), [`src29-sweep-coverage.json`](../data/gate-logs/src29-sweep-coverage.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: v1.3 is the P5 document with the least arithmetic and the most algebra: it sets `A = F₁₁[G]`, `G ≅ C₁₁ × C₁₁`, `X = γ₃₉₇ − 1`, `Y = γ₉₉₁ − 1`, defines the finite norm-Bockstein operator with matrix `[[X, 2X], [Y, 4Y]]`, computes its rank-2 determinant as `2·(e₃₉₇∧e₉₉₁) ⊗ X₃₉₇X₉₉₁`, observes that this and `[θ̄_n]₂ = 6·X₃₉₇X₉₉₁` span the same line, and declines to promote the ratio `6/2 = 3` to an invariant. **The determinant is recomputed in `A/I³` by the ring's own multiplication — `X·4Y − 2X·Y = 2XY`, with `(1+X)¹¹ ≡ 1` automatic there — and under all 100 generator changes `γ ↦ γ^a, γ ↦ γ^b` the line and `ord_I = 2` are invariant while the coefficient reaches every unit.** The document is right not to promote the ratio, and the reason is now a computed set: with RUN-068's `δ = 5` at the disclosed scale the ratio is `5/2 = 8`, in the manuscript's it is `3`, and **changing the two primitive roots alone — 120 choices at 397, 240 at 991 — drives `δ` through every unit of `F₁₁` and so the ratio through all ten values**, by the identity `log_{g'} = log_{g'}(g)·log_g`, checked on the full 392,040-term sum for two other root pairs (`(7, 11)` gives 5 again since both scales are 10; `(13, 7)` gives 1). Kim's semi-local theorem's hypotheses, which v1.3 cites as "the standard" ones, are checked where they can be: `p = 11 ≥ 5`; good ordinary (`a₁₁ = −4`); **`ρ̄_{E,11}` surjective, certified by Frobenius witnesses at 2 and 3 that refute the Borel, both Cartan normalisers and the three exceptional images** — RUN-036's method, reimplemented for 389.a1; `E(ℚ₁₁)[11] = 0` because `11 ∤ #E(F₁₁) = 16` and the formal group has no 11-torsion at `e = 1`; `c₃₈₉ = 1` because `v₃₈₉(Δ) = 1`; trivial torsion from a gcd of point counts. The Manin constant is the one hypothesis that is an external record and is left so. The labels: three closed (`KUR-SEMILOC`, `FIN-BocDET`, `MIXEDLINE`), two open (`CANON-BocID`, `CPLX-GPR`), and no report of this line closes either. §8's instruction — *do not recompute the finite group law or Kurihara sum* — this line disobeyed, at RUN-067 and RUN-068, on principle: a certificate that has never been recomputed is a claim. **With this round every one of the corpus's 85 documents has been a round's subject: `src29` re-run gives 85 of 85, 0 cited only, 0 unmentioned.**

---

## §2–§3 — the determinant, in the ring

`A/I³` is `F₁₁[X, Y]/(X, Y)³`, six monomials. The relation `γ¹¹ = 1`, which
is `(1+X)¹¹ = 1` in `A`, needs no imposing: `(1+X)¹¹ = 1 + X¹¹` in
characteristic 11 and `X¹¹ ∈ I¹¹ ⊂ I³`, and the gate confirms
`(1+X)¹¹ ≡ 1 (mod I³)` by multiplying it out. Then

| | |
| --- | --- |
| `B_N` in the bases `P, Q` and `e₃₉₇, e₉₉₁` | `[[X, 2X], [Y, 4Y]]` |
| `det` by the ring's multiplication | `X·4Y − 2X·Y = 2·XY` |
| `det M_loc mod 11` | 2 |
| a scalar times `XY`, and that scalar | yes, 2 |

## Invariance, computed

For `γ₃₉₇ ↦ γ₃₉₇^a`, `γ₉₉₁ ↦ γ₉₉₁^b`, `a, b ∈ F₁₁^×`: `X' = (1+X)^a − 1 ≡
aX + C(a,2)X²`, and `2·X'Y' ≡ 2ab·XY (mod I³)`. Over all 100 pairs:

| | |
| --- | --- |
| `ord_I = 2` preserved | 100 of 100 |
| the line `F₁₁·XY` preserved | 100 of 100 |
| `XY` coefficients reached | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |

Nonvanishing and the line are invariants; the coefficient is not. That is
v1.3 §4's claim, and it holds by computation rather than assertion.

## The ratio

| scale | `[θ̄_n]₂` | `det(B_N)` | ratio |
| --- | ---: | ---: | ---: |
| the manuscript's (undisclosed) | 6 | 2 | 3 |
| the disclosed `λ(1,5) = 1` (RUN-068) | 5 | 2 | 8 |

Both are legitimate; neither is canonical. v1.3 lists the permitted changes —
a primitive root, a generator of either `C₁₁`, a local quotient basis, a
determinant basis — and the first alone suffices to reach anything: for a
primitive root `g'` of 397, `log_{g'}(a) = log_{g'}(5)·log₅(a)`, and as `g'`
runs over the 120 primitive roots `log_{g'}(5) mod 11` runs over all ten
units (likewise 240 roots at 991). So `δ_{g',h'} = δ_{5,6}·u·v` reaches every
unit, and the ratio with the root-independent `det(B_N)` does too:

| root pair | scale at 397 | scale at 991 | predicted `δ` | computed on the full sum |
| --- | ---: | ---: | ---: | ---: |
| `(5, 6)` | 1 | 1 | 5 | 5 (RUN-068) |
| `(7, 11)` | 10 | 10 | 5 | **5** |
| `(13, 7)` | 6 | 7 | 1 | **1** |

Ratios reachable by primitive-root choice alone: `{1, …, 10}` — all of
`F₁₁^×`. "3" is a coordinate, not a number.

## §1 — Kim's hypotheses, where computable

| hypothesis | here |
| --- | --- |
| `p ≥ 5` | 11 |
| good ordinary | `389 ∤ 11`; `#E(F₁₁) = 16`, `a₁₁ = −4 ≢ 0` |
| residual surjectivity `ρ̄_{E,11}` | **certified**: Borel refuted at `q = 2` (`a = −2`, `a² − 8 ≡ 7` a non-residue); split Cartan normaliser at 2; nonsplit Cartan normaliser at 3; `A₄`, `A₅` at 2 (projective order 4); `S₄` at 3 (order 6) |
| local `p`-torsion `E(ℚ₁₁)[11] = 0` | `11 ∤ 16`, and `E₁(ℚ₁₁)` has no 11-torsion since `e = 1 < 10` |
| Tamagawa | `v₃₈₉(Δ) = 1`, Kodaira `I₁`, `c₃₈₉ = 1` |
| trivial torsion | gcd of `#E(F_q)`, good `q < 60`, is 1 |
| Manin constant 1 | **external** — LMFDB/Cremona; not computed in this tree |

## §5–§8 — the labels, and an instruction not followed

Three closed labels — `P5-KUR-SEMILOC = CLOSED`, `P5-FIN-BocDET =
CLOSED_EXACT`, `P5-MIXEDLINE = CLOSED_UP_TO_UNITS` — and two open,
`P5-CANON-BocID` and `P5-CPLX-GPR`. The gate scans every report of this line
for a sentence closing either open gate: none. §8 says *Do not recompute the
finite group law or Kurihara sum*; RUN-067 recomputed the group law and
RUN-068 the sum, and found what the documents said (and, for the sum, what
the stress-test line found instead of what the manuscript said). The
instruction is about where to spend research effort next, and on that it is
right; as a verification rule it is the one this line exists to break.

## The sweep, closed

`src29` re-run with this report in place: **85 documents, 85 the subject of a
round, 0 cited only, 0 unmentioned.** Phase 0 10 of 10, Phase 1 25 of 25,
Phase 2 40 of 40, P5 10 of 10. RUN-027 measured 55; the walk took from
RUN-001 to RUN-069.

## The drill

**294 defects, 294 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 60 controls undisturbed, over 97 checks.

The 5 planted for this gate, each turning `determinantal-bockstein` red and nothing else:

| planted defect | went red |
| --- | --- |
| the 2x2 determinant is computed as ad + bc, the cross term's sign dropped | `determinantal-bockstein` |
| the ring is truncated at I^2 instead of I^3, so XY is killed and the determinant reads 0 | `determinantal-bockstein` |
| the residue test is inverted, so the Borel refutation is certified by a witness whose discriminant IS a residue | `determinantal-bockstein` |
| the local 11-torsion test is inverted: E(Q_11)[11] reported 0 iff 11 divides #E(F_11) | `determinantal-bockstein` |
| the torsion gcd is taken over q = 2 alone, so it reads #E(F_2) = 5 | `determinantal-bockstein` |


## What this round does not claim

* **The canonical identification is untouched.** `P5-CANON-BocID` asks whether
  `B_N` is the Bockstein regulator of Burns–Kurihara–Sano or Nekovář; this
  round computes `B_N`'s determinant, not its identity with anything.
* **Kim's theorem is not checked**, nor Castella–Sano's; the hypotheses under
  which they are cited are.
* **The Manin constant is not computed.** It is recorded as the external
  input it is.
* **"Every document a subject" is coverage, not closure.** What each round did
  not do is in its own report; the open gates of the corpus are open.
