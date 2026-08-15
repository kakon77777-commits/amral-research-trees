# RUN-011 — Round 03-A.4: the deficit ledger, and what CF tools can actually reach

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A4_Spine_Valuation_Rigidity_v0.1.md` + `Hard_Zeta_ROUTE_MAP_v0.7.md` (2026-08-11 21:52) — source item 28
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (deficit-queue layer) · [`src13_hardzeta_round03a4_recheck.py`](../code/src13_hardzeta_round03a4_recheck.py) · [`src13_drill.py`](../code/src13_drill.py)
**Logs:** [`src13-hardzeta-round03a4-recheck.json`](../data/gate-logs/src13-hardzeta-round03a4-recheck.json) · [`src13-drill.json`](../data/gate-logs/src13-drill.json)

**Result: 26/26 checks. 16/16 planted defects caught by the check named for each — 11 in the ledger layer, 3 in this run's own measurement. 2/2 null controls undisturbed.**

---

## What Round 03-A.4 does

Round 03-A.3 made the spine deterministic. This round asks what staying on one
**costs**:

```
d_m = ⌊βm⌋ − K_m                 the integer deficit; subcritical ⟺ d_m ≥ 0
d_m = d_{m−1} + b_m − e_m        b_m ∈ {0,1} Sturmian, e_m = q_m − 1
Σ_{i≤m}(q_i − 1) ≤ ⌊γm⌋          the credit ledger, γ = β − 1 ≈ 0.585
```

Every unit of extra 2-adic valuation is paid out of a Sturmian budget. §9–§12 then
re-read the same ledger as **cylinder occupancy** — `q_i ≥ r` exactly when
`Y_{i−1} ≡ −3^{−1} (mod 2^r)` — and the strongest statement, §26–§32, is that any
infinite positive subcritical spine has `Y_m → ∞`: a CST counterexample would be a
genuinely **divergent** orbit.

All of it holds. The Sturmian increment is always a bit; the recurrence and the
telescoped ledger hold at every step; subcritical is exactly a non-negative
deficit; high valuation is exactly membership of one residue class and those
cylinders nest; occupancy stays inside the budget; the excursion identity holds in
exact integers; the logarithmic and bounded-deficit bounds bracket the endpoint;
no endpoint repeats; and where the Legendre gate opens, `K_m/m` really is a
convergent of β.

The `β` machinery is anchored against named values rather than its own shape: the
continued fraction comes out `[1,1,1,2,2,3,1,5,2,23,2,2]` and the convergents
include **19/12** and **84/53** — the equal-temperament fractions.

---

## Two things worth separating

**§18's "Spine Excursion Identity" is Paper 06's affine formula in log
coordinates.** Multiply through by `2^{K_m}` and it becomes

```
Y_m·2^{K_m} = 3^m·n + Σ_i 3^{m−1−i}·2^{K_i}
```

which this run verifies in exact integers, no floating point at all. That is not a
criticism — the **new** content of §18 is the *reading*, deficit as exponential
growth rate, and that reading is what carries §30's divergence corollary. Worth
separating so the novelty is credited to the right half.

**The Haar gap is real, and measured.** §12 contrasts a Haar-typical total
cylinder density of exactly **1** against a budget of `γ ≈ 0.585`. On real spines:

| `n` | lifetime | credit spent / budget | mean excess valuation |
|---|---|---|---|
| 27 | 36 | 16 / 19 | 0.471 |
| 703 | 50 | 13 / 19 | 0.382 |
| 10087 | 65 | 17 / 19 | 0.500 |
| 35655 | 84 | 13 / 19 | 0.382 |

Every measured spine spends well under the Haar rate of 1 per step. So the
discrepancy exists rather than being an artefact of the bound — and §13 and §45's
No-Go 2 are right to stop there: a measure-one statement about Haar-typical orbits
cannot become a theorem about every anchored positive-integer orbit. This run adds
nothing that closes that gap.

---

## The Legendre gate, measured

§34 says continued-fraction tools apply rigorously only when `δ_m < 1/(2m)`. §35
calls that "ultra-tight contact". How restrictive is it in practice?

| `n` | depths examined | gate open at | fraction |
|---|---|---|---|
| 27 | 24 | `m = 2` | 4.2% |
| 103, 703, 1407, 10087, 15039 | 24 each | — | **0%** |
| 35655 | 24 | `m = 4` | 4.2% |

**The gate opens on 2 of 168 depths across seven spines.** Five of the seven never
open it at all. So §35's restriction is not a technicality — for essentially the
whole spine, continued-fraction tools have no rigorous purchase, and §45's No-Go 3
("bounded deficit is not enough to get a convergent") is quantitatively the normal
case rather than the exception.

Where the gate does open, `K_m/m` is genuinely a convergent, so the criterion is
doing real work — just very rarely.

---

## Three findings about my own checks

**An equivalence that only ever saw one side.** *Subcritical ⟺ `d_m ≥ 0`* was
tested only at depths inside the subcritical lifetime, where both halves are
always true, so it passed for free — a planted defect in `deficit` slipped
through. The loop now runs **one step past** the lifetime, with a guard requiring
both outcomes to appear. Fourth empty-observable in this arm.

**A constant offset that cancels.** Shifting the Sturmian credit by a constant is
invisible to the recurrence, because `b_m` is a *difference* of consecutive credit
values. Only the telescoped ledger sees it. The defect was retargeted at the check
that can.

**`<` versus `<=` was a no-op for the fifth time.** In the continued-fraction
loop, `acc·P == Q` would require an exact power relation between rationals, which
`log₂3` being irrational forbids. Replaced with a mutation of the tail recursion,
which does move the expansion.

Also worth recording as a cost note: `beta_convergents(40)` with exact rationals
does not terminate in reasonable time — β's tenth partial quotient is 23 and the
exact tail explodes past it. Twelve terms is instant and covers every denominator
this run needs. The function now says so in its docstring.

---

## What this does not establish

Nothing on §46's unproved list. The divergence corollary is checked only in the
direction a finite spine can show — endpoints grow, none repeats — which is
consistent with the theorem and with any bounded search equally.
