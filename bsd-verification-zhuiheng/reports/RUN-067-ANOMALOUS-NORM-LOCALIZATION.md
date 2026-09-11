# RUN-067 — P5 v1.1's every exact figure recomputed from the group law up: `P'` generates both finite groups, `Q' = 244 P'` and `356 P'`, the slopes 2 and 4, `ρ` surjective with image 390,830, the kernel basis a basis, `J_S = 1`; and the ratio 3 asserted by no one

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_P5_Anomalous_Norm_Localization_389a1_p11_v1.1`](../../../amral/public/bsd/p5/files/BSD_P5_Anomalous_Norm_Localization_389a1_p11_v1.1.md) — the first of the three P5 documents RUN-065 named as the last not yet a round's subject
**Tools:** [`src69_anomalous_norm_localization.py`](../code/src69_anomalous_norm_localization.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src69-anomalous-norm-localization.json`](../data/gate-logs/src69-anomalous-norm-localization.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: v1.1 is the P5 document with the most exact arithmetic in it, and RUN-011 — which took the sub-line's foundations as its subject rather than this file — recomputed the object it turns on: the matrix `M_loc = [[1,2],[1,4]]` and its determinant `2`. What no round had touched is §7, where v1.1 goes further than the matrix: it claims `P'` **generates** `E(F₃₉₇)` and `E(F₉₉₁)`, gives the discrete logarithms `Q' = 244 P'` and `Q' = 356 P'`, four explicit multiples, the simultaneous-reduction map `ρ(a, b) = (a + 244b, a + 356b)`, its surjectivity by a Chinese-remainder compatibility, an explicit kernel basis, its determinant `390,830 = 374 · 1045`, the index `[E(ℚ) : E^S(ℚ)] = 390,830` with `v₁₁ = 2`, and `J_S = 1`. **Every one of those is recomputed here with its own affine group law over `F_ℓ`, nothing read from RUN-011's log, and every one agrees**: the short model and the generator images derived from `[0,1,1,−2,0]`; `#E(F₃₉₇) = 374 = 34·11` and `#E(F₉₉₁) = 1045 = 95·11` by enumeration; `ord(P') = 374` and `1045`, so both groups are cyclic on `P'`; `Q' = 244 P'` and `356 P'` by exhaustive stepping; `34P' = (281,236)`, `34Q' = (11,334)`, `95P' = (39,97)`, `95Q' = (865,243)`; the slopes `34Q' = 2·(34P')` and `95Q' = 4·(95P')` in the order-11 subgroups — which are, as they must be, `244 mod 11` and `356 mod 11`; `ρ` has image `390,830` of `390,830` because `356 − 244 = 112 ≡ 2` is a unit mod `gcd(374, 1045) = 11`; the document's basis `(5742, −22), (−254980, 1045)` lies in the kernel and has determinant `390,830`, so it is a basis; `v₁₁(390,830) = 2`; the cokernel is trivial, `J_S = 1`. The document's gate-state table has seven `CLOSED_EXACT` rows and one `OPEN`; it declines, in its own words, to assert that `6/2 = 3` is a Mazur–Tate comparison constant, and **no report of this line promotes that ratio or calls the open comparison closed.** RUN-011's terminological point stands: `a₁₁ = −4`, so `E` is ordinary and *not* anomalous at 11 in Mazur's sense — v1.1's "anomalous" is `11 ∣ #E(F_ℓ)` at the two ramified directions, and its own §2 says so.**

---

## What was recomputed, and how

The gate carries its own arithmetic: `b`- and `c`-invariants from the
a-invariants, the short model `Y² = X³ − 27c₄X − 54c₆`, the change of
coordinates `X = 36x + 3b₂`, `Y = 108(2y + a₁x + a₃)`, affine addition and
doubling over `F_ℓ`, point counting by Euler's criterion, orders from the
divisors of the group order, discrete logarithms by exhaustive stepping.
Nothing is imported from `src12` (RUN-011) — a second implementation agreeing
with the first is worth more than the first run twice.

## §2 — the model and the collision

| v1.1 says | recomputed |
| --- | --- |
| `Y² = X³ − 3024X + 46224` | `c₄ = 112`, `c₆ = −856`; `−27c₄ = −3024`, `−54c₆ = 46224` |
| `P = (0,0), Q = (1,0) ↦ P' = (12,108), Q' = (48,108)` | both on the minimal model; images exactly these; both on the short model |
| `#E(F₃₉₇) = 374 = 34·11` | 374 by enumeration; `a₃₉₇ = 24` |
| `#E(F₉₉₁) = 1045 = 95·11` | 1045 by enumeration; `a₉₉₁ = −53` |
| Kurihara condition `a_ℓ − ℓ − 1 ≡ 0 (mod 11)` | 0 at both |
| `v₁₁(#E(F_ℓ)) = 1` at both | 1 and 1 |
| `11 ∣ (ℓ − 1)/2` | 198 = 18·11, 495 = 45·11 |
| tame, good reduction | `ℓ ≠ 11`; `389 ∤ ℓ` |

## §5 — the four multiples and the two slopes

| v1.1 says | recomputed |
| --- | --- |
| `34P' = (281,236)`, `34Q' = (11,334)` in `E(F₃₉₇)` | exactly |
| `34Q' = 2·(34P')` | slope 2 in the order-11 subgroup |
| `95P' = (39,97)`, `95Q' = (865,243)` in `E(F₉₉₁)` | exactly |
| `95Q' = 4·(95P')` | slope 4 |
| `M_loc = [[1,2],[1,4]]`, `det = 2` | `[[1,2],[1,4]]`, `2` |

A consistency the document does not spell out but the gate checks: since
`Q' = k P'` with `k = 244` and `356`, the slope in the order-11 subgroup must
be `k mod 11` — `244 ≡ 2`, `356 ≡ 4`. It is.

## §7 — the part no round had touched

| v1.1 says | recomputed |
| --- | --- |
| `ord₃₉₇(P') = 374`, `ord₉₉₁(P') = 1045` — `P'` generates both | 374, 1045; both groups cyclic on `P'` |
| `Q' = 244 P'` in `E(F₃₉₇)`, `Q' = 356 P'` in `E(F₉₉₁)` | 244, 356 |
| `ρ(a,b) = (a + 244b, a + 356b)` surjective | image `390,830 = 374·1045`; the compatibility `(356 − 244) b ≡ v − u (mod 11)` is solvable for every target because `112 ≡ 2` is a unit |
| kernel basis `(5742, −22), (−254980, 1045)` | both in the kernel; determinant `390,830` = the index, so a basis |
| `[E(ℚ) : E^S(ℚ)] = 390,830`, `v₁₁ = 2` | `390,830 = 2·5·11²·17·19`; `v₁₁ = 2` |
| `J_S = 1` | cokernel of order `390,830 / 390,830 = 1` |
| Tamagawa at 389 contributes nothing | `v₃₈₉(Δ) = 1`: Kodaira `I₁`, `c₃₈₉ = 1` |

## The labels

v1.1's §10 table: seven rows `CLOSED_EXACT`, one `OPEN`
(`P5-ANOM-BocCOMP₁₁⁽²⁾`). Its §8 says of the quotient `6/2 = 3` of the two
displayed normalizations: *3 is not asserted to be a Mazur–Tate comparison
constant.* The gate scans every report of this line for a sentence promoting
that ratio or calling the open comparison closed. **None.** Of the seven
`CLOSED_EXACT` rows, five are recomputed above — the two divisibilities, the
determinant, Theorem 6.1's isomorphism (nonzero determinant with both local
quotients one-dimensional), `J_S = 1`; the other two, the inherited
`ord_I(θ̄_n) = 2` and `[θ̄_n]₂ ≠ 0`, are the one part of v1.1 this round does
not touch.

## The drill

**285 defects, 285 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 57 controls undisturbed, over 95 checks.

The 5 planted for this gate, each turning `anomalous-norm-localization` red and nothing else:

| planted defect | went red |
| --- | --- |
| the change of coordinates uses X = 36x + b2 in place of 36x + 3b2, so the generator images move | `anomalous-norm-localization` |
| the doubling formula drops the A term: 3x^2 in place of 3x^2 + A | `anomalous-norm-localization` |
| the discrete logarithm is searched only up to the cofactor, so Q' = 244 P' is never found | `anomalous-norm-localization` |
| rho's image is computed without the compatibility factor, so it reads 35,530 and rho is not surjective | `anomalous-norm-localization` |
| the label count includes section 0's definition, so CLOSED_EXACT reads 8 | `anomalous-norm-localization` |


## What this round does not claim

* **§1's `θ̄_n ≡ 6 X₃₉₇X₉₉₁ (mod I³)` is not recomputed.** It is a modular-symbol
  computation inherited from v1.0 and shared with the RUGZPB P4 certificate;
  it is the subject of a later round, not a figure read here.
* **Proposition 4.1 is a proof, not a computation.** Its hypotheses — tame,
  totally ramified, degree `p ≠ ℓ`, good reduction — are verified on the data;
  the proposition itself is read, not checked.
* **`Ш(E/ℚ)[11]` is not touched**, as at RUN-011: the P5 documents carry it as
  inherited, and Theorem 6.1's "exact arithmetic closure" is about
  `E(ℚ)/11E(ℚ)`, which this round's figures do establish.
* **Nothing about the open comparison.** `P5-ANOM-BocCOMP` is `OPEN` in the
  document and stays so here.
