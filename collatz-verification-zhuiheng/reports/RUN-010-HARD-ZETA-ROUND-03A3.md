# RUN-010 — Round 03-A.3: the zero-lift spine, and a tree that collapses to paths

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A3_Endpoint_Parity_Dynamics_v0.1.md` + `Hard_Zeta_ROUTE_MAP_v0.6.md` (2026-08-11 21:37) — source item 27
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (spine layer) · [`src12_hardzeta_round03a3_recheck.py`](../code/src12_hardzeta_round03a3_recheck.py) · [`src12_drill.py`](../code/src12_drill.py)
**Logs:** [`src12-hardzeta-round03a3-recheck.json`](../data/gate-logs/src12-hardzeta-round03a3-recheck.json) · [`src12-drill.json`](../data/gate-logs/src12-drill.json)

**Result: 25/25 checks. 15/15 planted defects caught by the check named for each — 10 in the spine chain, 3 in this run's own measurement. 2/2 null controls undisturbed.**

---

## What Round 03-A.3 does

Round 03-A.2 produced one bit per step. This round collects them into a single
2-adic state and finds the structure behind them:

```
Ξ_m = −(3M_m + 1)·3^{−(m+1)} ∈ ℤ₂           the endpoint state
c_{m+1} = [Ξ_m]_q                            choosing exponent q selects q bits
M_{m+1} mod 2 = bit_q(Ξ_m)                   Endpoint Bit-Selection
Ξ_{m+1} = (Ξ_m − [Ξ_m]_q)/2^q − 3^{−(m+2)}   cut and shift
```

and then the result that matters:

> **`t_{m+1} = 0 ⟺ q = q*_m := v₂(3·Ŷ_m + 1)`** — the Unique Zero-Lift Edge.

**Every node has at most one source-preserving child.** So the tree of exact codes
carries a deterministic sub-object — the *spine* — and §24 says it stays inside
the coefficient frontier iff `q*_m ≤ Q_m := ⌊β(m+1)⌋ − K_m`.

All of it checks, over 13,929 node/exponent pairs: the endpoint recurrence, the
coarse lift digit and its range, its identification with the low bits of the
state, the bit-selection theorem, the cut-and-shift recurrence, the lift-digit
decomposition, both routes to `q*`, the zero-lift bit conditions, the edge itself,
the ejection of every other exponent, and the Spine Ejection Criterion checked
against actually following the edge. **1,742 zero-lift edges occurred and no node
ever had two source-preserving children.**

§13's parity-only example reproduces to the digit — code `(1,2,1,1)`, `K=5`,
coarse `27`, `M=71` odd; extend by `q=2` → `K=7`, coarse `91`, `M=175` **still
odd**, yet `c₅=2` so `t₅=1` and the anchor is ejected.

---

## A different verdict from RUN-009 — and the paper got there first

[`RUN-009`](RUN-009-HARD-ZETA-ROUND-03A2.md) priced the previous round's
endpoint-parity route as *equivalent, not cheaper*. **This round retires that
route itself**: §37 is a "New No-Go: Parity-Only Proof", §13 is its
counterexample, and route map v0.6 states plainly that endpoint-even is
*"sufficient but too strong"*.

Same conclusion, reached independently on the theory side. I record that as
agreement, not as a finding of mine.

What replaces it is **not** another restatement. The target — *no infinite
subcritical spine* — is still equivalent to CST, and §39 lists it as unproved. But
the search space collapses from a **branching tree** to a **set of deterministic
paths**, one per canonical source, with no branching freedom at all. That is a
structural gain, and it is what makes §40's proposed tools — continued fractions,
Diophantine rigidity — applicable in the first place: they act on orbits, not on
trees.

So the pricing method from RUN-009 discriminates rather than always answering
"equivalent". Here the target is equivalent and the *object* is genuinely smaller.

---

## The measurement: spine survival, and the identity behind it

Spine length obeys an exact identity, verified on every trace:

> **node depth + spine steps = the canonical source's own subcritical lifetime**

| node | source | spine steps | ejected at | source lifetime |
|---|---|---|---|---|
| `(1,2,1,1)` | 27 | 32 | `q*=3 > Q=2` | 36 = 4+32 |
| `(1,1,2,1,1)` | 103 | 20 | `q*=4 > Q=3` | 25 = 5+20 |
| `(1,1,2)` | 7 | 0 | `q*=3 > Q=2` | 3 = 3+0 |

The spine survival profile, to depth 11:

| `m` | nodes | max steps | mean | longest-lived source |
|---|---|---|---|---|
| 3 | 3 | 33 | 11.00 | 27 |
| 6 | 30 | 30 | 9.40 | 27 |
| 7 | 85 | **43** | 6.26 | 1,407 |
| 9 | 476 | 42 | 5.10 | 15,039 |
| 10 | 961 | **74** | 6.38 | 35,655 |
| 11 | 2,652 | 73 | 6.06 | 35,655 |

Two things follow. A spine is **never longer than its source's life**, so asking
how long spines can run is asking how large `τ_c` can be — CST again, but now
*per source* rather than *per tree*. And the longest-lived sources are 3, 7, 27,
1407, 15039, 35655 — where 27 and 35655 are exactly the anchors
[`RUN-007`](RUN-007-HARD-ZETA-ROUND-03A.md) measured, while 1407 and 15039 are new
here: long-lived from a given depth without being global `τ_c` records.

Every spine traced terminated; none hit the iteration limit, so these are lengths
and not bounds.

---

## Two findings about my own checks

**A truncation that crashed instead of reporting.** `Ξ_m` is a 2-adic integer kept
to finitely many bits. A drill that cut the precision to 4 bits produced a
traceback rather than a named failure — and a traceback names nothing. There is
now an explicit precision check that fires before any bit is read out of the state.

**An "at most one" that passes for free.** The uniqueness check — *no node has two
source-preserving children* — is satisfied trivially if you only probe one
candidate exponent, or if you find none at all. A drill narrowing the probe to a
single exponent went uncaught. There is now a companion guard requiring the probe
to span more than one exponent **and** to have actually found source-preserving
children: **1,581** of them across the sweep. Third instance of the
empty-observable class in this arm.

---

## What this does not establish

Nothing about Collatz, and nothing on §39's unproved list. *No infinite
subcritical spine* is untouched: every spine measured here terminates, which is
what a true conjecture and a merely bounded search look like equally.
