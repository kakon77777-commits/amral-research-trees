# RUN-055 — Theorem 2.18's condition map, recomputed on all 40,749 base curves and all 247,391 twist pairs

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`01_Theorem_2_18_Condition_Map`](../../../amral/public/bsd/phase1/files/01_Theorem_2_18_Condition_Map.md) — the first Phase 1 document to be a round's subject
**Tools:** [`src57_theorem_2_18_condition_map.py`](../code/src57_theorem_2_18_condition_map.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src57-theorem-2-18-condition-map.json`](../data/gate-logs/src57-theorem-2-18-condition-map.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)
**Data:** the v0.5 exact census package, `BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12` — the same inputs RUN-004 through RUN-008 read

**Result: `01` lays Banwait–Huang Theorem 2.18 out as seven base conditions, two branches, and three blocks of twist conditions, and this tree already owned every instrument the map needs. **RUN-008 found the base is two populations — `Zha16_no_2_tors` (37,002) and `CLZ20` (3,747) — and those are the map's branches 8a and 8b**: this line walked into the theorem's branch structure from the data end without having read it. Recomputed here: **E1** holds on all 40,749 (`N = ∏ conductor_primes`). **E2**, `a₃` by point count mod 3, agrees with the census's own column **exactly** — 2,709 curves with `|a₃| = 3`, the same 2,709. **E3**'s 1,355 isogeny removals re-read. **E4** — *stated by the map and not a census removal class* — computed on all 40,749: **every curve passes**. **8b's three non-square conditions** hold on **all 3,747** CLZ20 curves, with the rational 2-torsion point found by exact integer bisection and **exactly one** integer root per curve. And the twist conditions D, E and F, recomputed independently on **every one of the 247,391 (curve, d) pairs** of the new map: **zero failures.** That is the admissibility side of Algorithm 2 rebuilt from the map's own text, not re-run. The census enforces exactly two of the map's conditions — E2 and E3 are its only removal classes — and the rest hold anyway. One provenance fact came out sharp: **the 1,355 base curves missing from the upstream twist blob are exactly the 1,355 isogeny curves**, and the 2,707 `a₃`-removed curves are all *present* in it — the blob was made with E3 applied and E2 not yet. And the first draft's float root-finder **missed 2,154 of 3,747** 2-torsion points; the replacement uses no float at all.**

---

## The map, and where this line already was

| `01` section | condition | instrument in this tree |
| --- | --- | --- |
| E1 | semistable | conductor arithmetic, RUN-004 |
| E2 | `a₃(E) ∈ {−2,…,2}` | point count mod 3, RUN-005 |
| E3 | no rational `p`-isogeny, `p ∈ {3,5,7}` | RUN-006, RUN-007, RUN-008 — `X₀(n)` closed both ways |
| E4 | `∀p∣N ∃q∣N, q≠p`, `E[p]` ramified at `q` | the discriminant valuations RUN-004 verified |
| 8a / 8b | no rational 2-torsion / exactly one | RUN-008's two populations |
| D, E, F | twist admissibility | Kronecker, cubic root counts, point counts — all present since RUN-009/016 |

**RUN-008 reported the base as two populations before this map was read.** `Zha16_no_2_tors` with zero 2-torsion in every curve; `CLZ20` with 2-torsion in every one. `01` §B and §C are *Branch 8a：無 rational 2-torsion* and *Branch 8b：恰有一個 rational 2-torsion*. The partition RUN-008 measured is the theorem's own branch structure.

## E1–E4 on 40,749 curves

| | result |
| --- | --- |
| **E1** | `N = ∏ conductor_primes` on all 40,749, and every valuation table's keys are exactly the conductor primes. **All pass.** |
| **E2** | 22,938 curves good at 3, 17,811 bad at 3 (where `|a₃| ≤ 1` and E2 holds trivially). `a₃` recomputed: histogram `−3: 910, −2: 3,616, −1: 2,779, 0: 5,182, 1: 4,051, 2: 4,601, 3: 1,799`. **`|a₃| = 3` on 2,709 curves — the same 2,709 the census marks**, set equality, not count equality. |
| **E3** | 1,355 removed with a 3/5/7-isogeny: `{3}: 1,233, {5}: 115, {7}: 7`. Re-read; RUN-006/007/008 recomputed it. |
| **E4** | **All 40,749 pass.** 0 prime-conductor curves, so the structural exclusion (no second prime to witness) never bites. |

### E4 is the FW-H3 divisibility criterion, over a different set

On a semistable curve every `p ∣ N` is multiplicative, and at a multiplicative
`q ≠ p` the Tate curve gives: **`E[p]` is ramified at `q` iff `p ∤ v_q(Δ_min)`**.
So E4 reads: for every `p ∣ N`, some `q ∣ N`, `q ≠ p`, has `p ∤ v_q(Δ_min)`.

That is the criterion RUN-037 compiled for FW-H3 — `∃ℓ ∈ W₋, ℓ ≠ p, p ∤ v_ℓ(Δ_min)`
— quantified over **all** multiplicative primes rather than the nonsplit ones
only. The same arithmetic shape, a different quantifier, in a different theorem.
This round computes E4; it does not equate the two theorems' hypotheses.

### What the census actually enforces

| removal class | count | condition |
| --- | ---: | --- |
| `A3_ONLY` | 2,707 | E2 |
| `ISOGENY_ONLY` | 1,353 | E3 |
| `BOTH` | 2 | E2 and E3 |
| | **4,062** | |

E1, E5, E6, E7 are properties of how the base list was *assembled* — semistable,
optimal, analytic rank 0, `BSD(E,2)` known — and need no removal step. **E4 and
8b's non-square conditions are arithmetic the map states and the census does not
test.** They hold on the whole base anyway, and now that is measured rather than
assumed.

## Branch 8b on every CLZ20 curve

`01` §C requires, for `E : y² = f(x)` with rational 2-torsion `(x₀, 0)`:
`f'(x₀)`, `−f'(x₀)` and `−Δ_E` all non-squares in `Q`. The squareness class of
`f'(x₀)` is model-independent (a change of model scales it by `u⁴`), so it is
computed on the monic 2-division cubic `X³ + b₂X² + 8b₄X + 16b₆`, `X = 4x`.

| | 3,747 CLZ20 curves |
| --- | ---: |
| rational 2-torsion `X₀` found | **3,747** |
| exactly one integer root | **3,747** — consistent with `E(Q)[2] ≅ Z/2`, never full 2-torsion |
| `f'(x₀)` a square | **0** |
| `−f'(x₀)` a square | **0** |
| `−Δ_E` a square | **0** |

Not computed: `ord₂ L^alg(E,1)` for either branch, `Ш(E')[2] = 0`, and
`E'(Q)[2] ≅ Z/2` for the 2-isogenous curve. Those are cited.

### The float missed 2,154 of 3,747

The first root-finder bracketed by floating point on a Cauchy bound of order
`10¹¹` and proposed integers for exact checking — RUN-006's rule, *float
proposes, exact decides*. **It came back `unresolved` on 2,154 curves.** Every one
of those has a rational 2-torsion point, integral by Lutz–Nagell, so the float
could not even *propose* correctly at that scale.

The replacement uses no float anywhere: the cubic is monotone between its
critical points, so an integer bisection on each segment finds every integer
root exactly or proves there is none. RUN-006's lesson, one step further.

## The twist conditions on 247,391 pairs

`01` §D–§F, recomputed on every `(curve, d)` in the new map:

| condition | pairs checked | failures |
| --- | ---: | ---: |
| D1 `d` squarefree | 247,391 | **0** |
| D2 `(d, 3N) = 1` | 247,391 | **0** |
| D3 `d ≡ 1 (mod 4)` | 247,391 | **0** |
| D4 `E` ordinary at every `p ∣ d` | 247,391 | **0** |
| E1 (Zha16) every `p ∣ d` inert in `Q[x]/(f₂)` | Zha16 pairs | **0** |
| E2 (Zha16) every `p ∣ N` split in `Q(√d)` | Zha16 pairs | **0** |
| E3 (Zha16) `Δ_E > 0 ⟹ d > 0` | Zha16 pairs | **0** (vacuous — every `d` is positive) |
| F1 (CLZ20) every `p ∣ d` is `≡ 1 (mod 4)` | CLZ20 pairs | **0** |
| F2 (CLZ20) `ord₂ #E(F_p) = 1` | CLZ20 pairs | **0** |
| F3 (CLZ20) `d ≡ 1 (mod 8)` | CLZ20 pairs | **0** |
| F4 (CLZ20) every odd `p ∣ N` split in `Q(√d)` | CLZ20 pairs | **0** |

**This is soundness — every entry present is admissible.** It is an independent
recomputation from the map's text, with this tree's own Kronecker symbol, cubic
root counter and point counter, on data whose provenance RUN-004 fixed. It is not
a re-run of the census script and not a re-run of Algorithm 2.

**Completeness is not measurable here.** The twist map is upstream data
(`cocoxhuang/ants_xvii`); only **200** distinct `d` values appear across the old
map, all positive, largest **997**, and the enumeration rule that produced them
is not in the package. Whether every admissible `d` is *present* cannot be asked
from this tree.

## The twist blob was made under E3 and before E2

> **Correction (RUN-060).** The identity below — the 1,355 base curves missing
> from the upstream blob are exactly the isogeny curves — is stated in words in
> `15_Fresh_Algorithm2_Semantic_Replay` §8, which was in the corpus before this
> round: those curves "全部已被 CURRENT Algorithm1 strict isogeny gate 排除". This
> round should have cited it rather than presenting the identity as identified.
> What this round added was the set equality as a computation and the
> complementary half — that the 2,707 `a₃` curves *are* in the blob; RUN-056
> added the mechanism. The arithmetic stands; the framing is corrected.


RUN-029 measured `1,355 = 40,749 − 39,394` base curves missing from the upstream
twist blob, as a number. Identified:

| | |
| --- | --- |
| base curves missing from the old blob | **1,355** |
| base curves with a 3/5/7-isogeny | **1,355** |
| **the same set** | **yes — set equality** |
| `a₃`-removed curves *present* in the old blob | **2,707 of 2,709** — the two absent are the `BOTH` class |
| either class present in the new map | **0** |

So the upstream blob was generated with the isogeny condition already applied
and the `a₃` condition not yet. The census README records that the upstream
code later added `disc_valuation_condition` — which is **E4** — without
regenerating the blob. **E4 removes nothing from this base**, measured above, so
that omission changed no membership. RUN-056 reads the mechanism from the
archived diffs.

## §G, and what RUN-008 did and did not say

> admissible ⟹ BSD follows from cited theorems
> not admissible ⇏ BSD false

RUN-008 closed the isogeny **criterion** both ways — every kept curve has no
3/5/7-isogeny and every removed one does. That is a statement about the
criterion. §G says the two must not be confused: a curve outside the admissible
family has simply not been reached by these theorems.

## The drill

**233 defects, 233 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 45 controls undisturbed, over 84 checks.

The 5 planted for this gate, each turning `condition-map` red and nothing else:

| planted defect | went red |
| --- | --- |
| E2's agreement with the census is scored by count rather than by set, so a swapped pair passes | `condition-map` |
| a_p comes back as p itself, so every curve is supersingular and every a_3 is 3 | `condition-map` |
| E4 is read in the ∀-form — every q | N must witness — instead of the ∃-form | `condition-map` |
| the 2-torsion root finder goes back to float bracketing on a Cauchy bound | `condition-map` |
| the twist-condition failures are counted but all_pass is reported True regardless | `condition-map` |


## What this round does not claim

* **E5, E6, E7 are cited.** Optimality, analytic rank 0, and `BSD(E,2)` are how
  the base list was assembled; nothing here verifies them.
* **Zero twist failures is soundness, not completeness.** The map's enumeration
  rule is not in the package.
* **E4 holding everywhere is a measurement on this base**, not a theorem about
  semistable curves. Another base could have a prime-conductor curve, where E4
  fails for want of a second prime.
* **The 8b non-squares are three of five conditions.** `Ш(E')[2]` and
  `E'(Q)[2]` are not computed.
* **`d > 0` throughout makes E3 (Zha16) vacuous here.** The condition is stated
  and checked; it never had a case to decide.
* **The E4 ↔ FW-H3 remark is about arithmetic shape**, not about the theorems.
  RUN-046 recorded a live dispute in the corpus about what the divisibility
  criterion is a criterion *for*; this round does not enter it.
