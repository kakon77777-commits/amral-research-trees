# RUN-016 — 40,749 conductors from scratch, `c₂` closed, and a base with no additive prime in it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Tate's algorithm — the census's conductor column, the `c₂` two rounds carved out, and the Kodaira types Phase 2's `01` and `05` route on
**Tools:** [`src18_tate_algorithm.py`](../code/src18_tate_algorithm.py), [`src19_conductor_census.py`](../code/src19_conductor_census.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src19-conductor-census.json`](../data/gate-logs/src19-conductor-census.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: all 40,749 conductors recomputed from the a-invariants, zero disagreements — a column nothing had checked. `696.e1` is Kodaira type II\* at 2 with `c₂ = 1`, which closes the carve-out RUN-014 and RUN-015 both declared and turns their `c₂·#Ш = 1` into `#Ш = 1`. And the base has **no additive reduction anywhere**: every one of its 135,787 bad primes is multiplicative, every conductor is squarefree, so the Banwait–Huang census reaches no non-semistable curve at all — which is exactly the gap Phase 2 exists to fill, now measured.**

---

## Three debts, one algorithm

RUN-014 and RUN-015 both reported `c₂·#Ш` as a single quantity because the
anchor's reduction at 2 is additive. RUN-004 recomputed 40,749 discriminants and
135,787 valuations, and RUN-008 verified the discriminant factorisations, but no
round has recomputed a **conductor**. And Phase 2's `01_Odd_Additive_Period_Barrier`
and `05_Kodaira_Prefilters_and_NoGo` both route on Kodaira types, which nothing
had computed.

Tate's algorithm returns all of it: the type, the Tamagawa number `c_p`, the
conductor exponent `f_p`, and whether the model is minimal.

## The census's conductor column

| | |
| --- | ---: |
| base curves | 40,749 |
| conductors recomputed from the a-invariants | 40,749 |
| **disagreements** | **0** |

Nothing is read but the curve. RUN-014 verified one conductor by an entirely
different route — which `N` makes the functional equation close, giving `N = 696`
with a residual 339 times smaller than the runner-up — and the two agree.

## The base has no additive prime in it

| | |
| --- | ---: |
| bad primes across the base | 135,787 |
| of type `I_n` (multiplicative) | **135,787** |
| of any additive type | **0** |
| curves with a non-squarefree conductor | **0** |

A curve is semistable exactly when its conductor is squarefree, equivalently
when every bad prime is multiplicative. **Not one of the 40,749 fails that.**

So the Banwait–Huang census reaches no non-semistable curve — and `696.e1`, with
its additive prime 2, sits outside that base by construction rather than by
choice. That is the whole reason the Phase 2 line exists, stated in its documents
as motivation and measured here as a fact about the data.

## `c₂`, and what it closes

| `p` | Kodaira | `f_p` | `c_p` |
| ---: | --- | ---: | ---: |
| 2 | **II\*** | 3 | **1** |
| 3 | I1 (split multiplicative) | 1 | 1 |
| 29 | I1 (non-split multiplicative) | 1 | 1 |

`N` recomputed: **696**. `∏c_p = 1`.

RUN-014 measured `L(E,1)/Ω = 1.0000000000000002` and, with trivial torsion, read
`c₂·#Ш = 1` from it — declining to split the product. Tate gives `c₂ = 1`
outright, so

$$\#Ш(696.e1)=1$$

follows without the reading. Two independent routes, and the second one settles
what the first could only bound.

## `c_q` for the family, twice over

RUN-015 derived `c_q = 1` for the twists from `L/Ω = 49`, trivial torsion,
Cassels's square theorem and the bound `c_q ∈ {1,2,4}`. Tate gets there without
any of that:

| `q` | Kodaira at `q` | `f_q` | `c_q` | roots of `f₂` mod `q` | potential reduction |
| ---: | --- | ---: | ---: | ---: | --- |
| 241 | I0\* | 2 | **1** | 0 | potentially good |
| 313 | I0\* | 2 | **1** | 0 | potentially good |
| 457 | I0\* | 2 | **1** | 0 | potentially good |
| 673 | I0\* | 2 | **1** | 0 | potentially good |
| 937, 1009, 1153, 1753 | I0\* | 2 | **1** | 0 | potentially good |

Type I0\* has `c = 1 + #roots of the step-7 cubic mod q`, and **𝒫's third
condition is exactly that `f₂` is irreducible mod `q`** — zero roots. So the
condition that RUN-009 found pinning Frobenius and RUN-015 found forcing
ordinariness also forces the Tamagawa number to 1. The two derivations of
`c_q = 1` share nothing.

## The two Phase 2 documents

**`05_Kodaira_Prefilters_and_NoGo`** states an exact no-go: additive **and**
potentially multiplicative ⟹ `FW17_H2_FAIL`. At the twisting prime `E` has good
reduction, so its quadratic twist is potentially **good** there — `v_q(j)` is
unchanged and non-negative. Measured on all eight members checked: **potentially
good, every one. The no-go does not fire.** It is a fact about the family, not a
hope.

**`01_Odd_Additive_Period_Barrier`** names a published Manin-constant condition
that excludes "additive potentially ordinary of Kodaira type II, III, or IV".
The type at the twisting prime is **I0\*** for every member checked — **not in
the excluded set.**

That does not establish the Manin condition; it removes one of the ways it could
have failed, and says which one.

## Four errors of mine, and what each was hiding

This gate was wrong four times before it was right, and every one was found by a
check rather than by inspection.

**The step-2 closed form.** A first version used a remembered formula to move the
singular point to the origin and returned `f₂ = 4` for `696.e1`, giving `N = 1392`.
Replaced by *finding* that point — for `p = 2` and `3` there are only four or nine
candidates, and those are exactly the cases whose closed forms are easy to
misremember.

**The step-7 normalisation, demanded too strongly.** Requiring `p³|a₄` and
`p⁴|a₆` forces the last two coefficients of step 7's cubic to vanish mod `p`, so
the cubic becomes `T²(T+b)` and **type I0\* can never be returned**. Thirteen
hand-picked curves and two thousand census conductors all passed anyway, because
none of them was I0\* at 2 or 3. Weakened to what the cubic actually needs —
`p|a₂`, `p²|a₄`, `p³|a₆` — and the drill now carries a curve that is I0\* at 2 so
the mistake cannot come back quietly.

**An `O(p²)` singular-point scan on the `p ≥ 5` path.** At a conductor prime near
500,000 that is `2.5 × 10¹¹` operations for a fact one Legendre symbol settles —
split multiplicative iff `−c₆` is a square mod `p`. The census run went from
"longer than ten minutes for 4,000 curves" to **0.1 seconds for 4,000**.

**A check that passed on nothing.** The family list was built from a sieve
returning a flag array rather than a list of primes, so it came out empty — and
the gate's own `ok` condition, an `all(...)` over it, was vacuously true. The
guard that now refuses fewer than ten members is there because of it.

## The drill

**67 defects, 67 caught by the check named for each. 16 controls, none
disturbed.**

The most useful addition is **Ogg's formula** as an independent check:
`f = v(Δ) − m + 1`, where `m` is the number of components of the special fibre
and depends only on the Kodaira type. The algorithm computes `f` branch by
branch and never consults that relation, so requiring it constrains every
exponent from outside. Two defects — an additive exponent taken as 1 instead of
2, and type II\* given `f = v(Δ) − 7` — are caught by it and by nothing else.

## What this round does not claim

* **Nothing about BSD.** It computes local invariants.
* **`#Ш(696.e1) = 1` follows from the BSD formula holding for that curve**, which
  Creutz–Miller supplies. Tate removes the ambiguity in `c₂`, not the dependence
  on that theorem.
* **The Manin-constant condition of `01` is not established** — only that the
  Kodaira type at the twisting prime is outside its excluded set.
* **`c_p` at additive primes `p ≥ 5` is computed only for types I0\*, II, III,
  II\* and III\***. IV, IV\* and `I_m*` there return `None` rather than a guess;
  none of them occurs in anything this round needed.
* **The type distribution is a fact about this base**, which is a curated
  no-2-torsion plus CLZ20 population, not about elliptic curves in general.
