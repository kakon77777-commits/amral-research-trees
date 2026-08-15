# RUN-016 — Round A-U.2b.1: the constant reproduces to 80 digits, by a different method

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2b1_bundle.zip` (source item 34) — Round A-U.2b.1 *Sharp Packing–Entropy Threshold*, its `verify_…packing_entropy.py` and `…constants.json`, two figures, plus `A_Line_ROUTE_MAP_v1.2`
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (A-U.2b.1 layer) · [`src18_hardzeta_au2b1_recheck.py`](../code/src18_hardzeta_au2b1_recheck.py) · [`src18_drill.py`](../code/src18_drill.py)
**Logs:** [`src18-au2b1-recheck.json`](../data/gate-logs/src18-au2b1-recheck.json) · [`src18-drill.json`](../data/gate-logs/src18-drill.json)

**Result: 21/21 checks. 25/25 planted defects caught by the check named for each — 12 in the A-U.2b.1 layer, 9 in this run's own measurement, 4 in the artifact. 2/2 null controls undisturbed. Coverage audit clean.**

---

## The prediction RUN-015 made, and what happened

RUN-015 measured that A-U.2b's proof scheme tops out at `ε = 0.01502`, and said:

> Anything past `0.0150` needs a different argument, because at that point the
> two constraints meet.

A-U.2b.1 supplies a different argument. Instead of the pigeonhole "a block must
recur", it bounds **how often** a block can recur: all occurrences of one block
are positive, distinct, congruent modulo `2^{Q+1}` and at most `M_N`, so

```
occ_N(v) ≤ 1 + M_N/2^{Q+1}
```

and summing over blocks gives the packing inequality
`N − r + 1 ≤ A(r,D_N) + (M_N/2^{r+1})·B(r,D_N)`.

That reaches `c_pack = 0.03585676…` — **2.388× the old scheme's ceiling**. The
prediction held in the way that mattered: tuning could not get there, and new
arithmetic did.

| | `c` |
|---|---|
| A-U.2b published | 0.01 |
| A-U.2b's scheme ceiling (RUN-015) | 0.01502 |
| **A-U.2b.1 `c_pack`** | **0.03585676003404867** |
| A-U.2b.1 safe witness | 0.035 |

**And this round is tight where the previous one was not.** A-U.2b published
**66.6%** of what its own scheme allowed. A-U.2b.1 publishes the supremum itself
— §24 proves `sup F = F(x*) = x*/β = c_pack` — and rounds down only for the
explicit witness, which is **97.6%** of it. There is no slack left to find here.

---

## The first round to ship its own numerical artifact — checked as one

The bundle carries a `verify_…py` and a `constants.json` giving `c_pack` to 80
digits. That is exactly the discipline this arm argues for: a published number
that is the output of something that runs.

It is also something to be careful with. Re-running the author's script would
test only that the script is deterministic. So the constants are **recomputed
here from scratch** — by bisection in the standard library's `decimal`, against
the subject's `mpmath.findroot`. Different library, different root-finding
method, and this tree has no third-party packages, so running their script was
never an option anyway.

| constant | digits agreeing |
|---|---|
| `β = log₂3` | 80 |
| `γ = β − 1` | 82 |
| `z* ` | 82 |
| `x* = z* − γ` | 83 |
| **`c_pack = x*/β`** | **83** |

Every digit published, and then some. The JSON's recorded bracket
`[0.0568, 0.0569]` genuinely straddles the root, with both sign values
reproducible. `H(γ) = 1.5056438879…` and `H(1) = 2` bracket `β` as §20 needs, and
§26's explicit witness checks out: `a = 0.035/0.056 = 0.625`,
`H(γ+0.056) = 1.5838351063… < β`, `aH = 0.9898969414… < 1`.

A drill defect perturbs a single digit **at position 41** of `c_pack` inside the
JSON, far past anything a float comparison would notice. The check catches it.

---

## The variational structure, verified symbolically and numerically

Two exact identities carry §23, and both are checked against independent
computations rather than read off the page:

```
H'(z)          = log₂(1 + 1/z) > 0          against a central difference at 1e-25
H(z) − z·H'(z) = log₂(1 + z)                to within 1e-40 at five points
```

The second is what makes `F(x) = x/H(γ+x)` strictly increasing: with `z = γ+x`,
`H(z) − x·H'(z) = log₂(1+z) + γ·H'(z) > 0`. Verified monotone on 56 sample
points across the feasible interval.

Hence `sup_{0<x<x*} F = F(x*) = x*/H(z*) = x*/β = c_pack`, checked to `1e-40`,
with `F` just below `x*` strictly smaller.

**§27's optimality is checked as two failures, not as an assertion.** Past `x*`,
`H(γ+x) ≥ β` and the second packing term stops being `o(N)`; below `x*` but with
`c ≥ F(x)`, `aH ≥ 1` and the first term stops being `o(N)`. Both are exhibited
numerically. That is what makes "maximal for this envelope" a checkable claim
rather than a summary.

---

## The packing machinery on real orbits

- **§7's block excess identity** `E_i = ⌊γ(i+r)⌋ − ⌊γi⌋ + d_i − d_{i+r}` holds on
  every block of every spine tested.
- **§8's range** needs `⌈γr⌉ = ⌊γr⌋ + 1`, which needs `γr` non-integral — checked
  for `r ≤ 199` by confirming `2^{⌊βr⌋} ≠ 3^r`, rather than assumed from `γ`'s
  irrationality.
- **§6's per-block packing bound** holds on every block, with a guard that blocks
  occurring more than once actually appear in the sample — a bound on repeats is
  untested where nothing repeats.
- **§9–§10's `A` and `B`** are confronted with a direct enumeration of the blocks
  they claim to count, at 15 shapes.
- **§11's inequality** holds in exact rationals at every window tested.

---

## The limit of what a finite check can see here

The drill found something worth stating about my own check of §11 rather than
about the paper. Mis-weighting the `B` term does **not** break the packing
inequality on any orbit I can compute — because the inequality is not close at
these sizes:

| | value |
|---|---|
| windows tested | 28 |
| where the `A` term alone is insufficient | 4 |
| minimum slack ratio (RHS/LHS) | **44.8** |
| maximum slack ratio | 83,227 |

So the right side exceeds the left by between one and five orders of magnitude,
and a check that only asserts `LHS ≤ RHS` would notice a gross implementation
error and nothing finer. **The asymptotic content of the multi-occurrence
refinement is simply not visible on orbits this short** — the refinement matters
as `N → ∞`, and my longest spine is 84 steps.

The check now carries a non-degeneracy guard instead of pretending otherwise: it
requires the `A` term alone to be *insufficient* somewhere, so the `B` term is
actually exercised. It is (at `n = 35655`, `r = 2`: `A = 66` against
`N − r + 1 = 83`). A defect that empties `B` now fails the check; one that merely
mis-weights it does not, and the report says which.

---

## Findings about my own checks

**The bundle check failed, and it was right to.** I wrote the expected new-file
count as five; the bundle has **six** — the paper, the route map, the
verification script, the constants JSON, and *two* figures. The three predecessor
rounds are byte-identical. Correcting my own expectation rather than the check is
the point: the count is now `== 3` reshipped and `== 6` new, both exact, so a
future bundle that quietly adds or drops a file fails here.

**A dead defect.** One planted defect damaged `block_excess()` — which this tool
never calls, because it computes the excess from `cumulative` directly. It tested
nothing and the run did not even go red. Replaced.

**Two more no-ops, and one of them was subtle.** Dropping the digit-agreement
threshold from 50 to 0 is the eleventh loosening no-op in this arm. The subtler
one: making the script-field check read the *constants JSON* instead of the
script still passes, because the JSON contains the same field **names** as keys.
Retargeted to the route map, which contains none of them.

**Two defects fired the wrong check, and both were informative.** A wrong
`floor_beta` leaves `2^{⌊βr⌋} ≠ 3^r` true, so the non-integrality check survives
it; and a mis-weighted `B` leaves the packing inequality standing, as above.

---

## What this does not establish

§35's unproved list: the true sharp lower bound on `D_N/log N`, exclusion of the
`c ≥ c_pack` regime, CASP, Terras, Collatz. `c_pack` is optimal **for this
envelope** — weak-composition block counting, exact residue packing, and the
excursion-height upper bound — and §28 lists what would be needed to beat it.
Nothing here bears on whether any of those five levers exists. The packing
inequality is verified on finite orbits; the barrier it implies is a statement
about infinite ones.
