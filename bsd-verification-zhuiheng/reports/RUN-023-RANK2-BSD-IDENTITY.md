# RUN-023 — the rank-2 BSD identity at 389.a1, and the first external test of RUN-017's period repair

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1`](../../../amral/public/bsd/p5/files/BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1.md) §6, the canonical rank-2 wall probe — and §9's multiplicity no-go
**Tools:** [`src26_rank2_bsd_identity.py`](../code/src26_rank2_bsd_identity.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src26-rank2-bsd-identity.json`](../data/gate-logs/src26-rank2-bsd-identity.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the rank-2 BSD identity closes at 389.a1 to machine precision with this arm's own real period. §6 records `L''(E,1)/2! ≈ 0.759316500288426770`, `Reg ≈ 0.15246017794314375`, `∏c_p = 1`, `#tors = 1` and a BSD-inferred `#Ш = 1`; with those the formula reduces to `L''/2! = Ω·Reg`, and `Ω(389.a1) = 4.98042512171011` computed here gives the ratio `1.0` with relative difference `0`. That is the first external test of RUN-017's finding that this tree's real period was doubled on the `Δ > 0` branch — 389.a1 has `Δ = 389 > 0`, so it is the branch that was wrong, and had the repair not been made the ratio would read `2`. The period is confirmed a second time by direct integration over both components of `E(R)`, sharing no code with the AGM: the two components agree to `5.8 × 10⁻¹²`, their sum matches the AGM to `4.4 × 10⁻¹¹`, and one component is `0.5000000000` of it exactly.**

---

## Why this was the round to do

RUN-017 found that this tree's `real_period` multiplied by an extra 2 on the
`Δ > 0` branch, and had done so for three rounds. Nothing caught it because
RUN-014's drill froze `Ω(37a1)` **taken from the same function** — a regression
baseline against your own output measures drift and nothing else. Everything
already published survived, because the Phase-2 anchor and all 247,391 twists
have `Δ < 0`.

So the repaired branch had never been tested against a number from outside this
tree, on a curve that actually uses it. §6 of the rank-uniform document supplies
exactly that: a rank-2 curve with `Δ = 389 > 0` and three recorded quantities
that, with the stated `∏c_p` and torsion, determine a period.

## The identity

With `∏c_p = 1`, `#E(Q)_tors = 1` and `#Ш = 1`, the rank-2 BSD formula is

$$\frac{L''(E,1)}{2!}=\Omega_E\cdot\mathrm{Reg}(E).$$

| substituted | ratio `L''_doc / (Ω·Reg)` | relative difference |
| --- | --- | --- |
| our AGM period, document's `Reg` | **`1.0`** | **`0`** |
| our integrated period, document's `Reg` | `0.9999999999911392` | `8.9 × 10⁻¹²` |
| our AGM period, our `Reg` at depth 10 | `0.9999991543890829` | `8.5 × 10⁻⁷` |

**The limiting term is our regulator, not our period.** Substituting the
document's regulator closes the identity to machine precision; substituting ours
moves it by `8.5 × 10⁻⁷`, which is what doubling depth 10 delivers. Our
regulator and the document's differ by `1.29 × 10⁻⁷`, inside RUN-017's own
stated residual of `1.6 × 10⁻⁶`.

## The period, three ways

`Δ = 389 > 0`, so `E(R)` has two components. The cubic
`(2y+1)² = 4x³ + 4x² − 8x + 1` has real roots

$$e_3=-2.0403022003,\qquad e_2=0.1354092402,\qquad e_1=0.9048929601,$$

giving a bounded "egg" over `[e₃, e₂]` and an unbounded component over
`[e₁, ∞)`. Both were integrated directly, with no code shared with the AGM:

| | value |
| --- | --- |
| bounded (egg) component | `2.4902125608800123` |
| unbounded component | `2.490212560874229` |
| **the two agree to** | **`5.8 × 10⁻¹²`** |
| sum — the full real locus | `4.980425121754241` |
| AGM, `src15` | `4.98042512171011` |
| **integration vs AGM** | **`4.4 × 10⁻¹¹`** (relative `8.9 × 10⁻¹²`) |
| **one component / AGM** | **`0.5000000000`** |

Two things make those numbers worth more than the agreement itself.

**The endpoint singularities cancel identically rather than numerically.** On the
egg, `x = mid + half·cos θ` produces a Jacobian `sin θ` that kills the
inverse-square-root singularities at both ends exactly; the integral is then so
well-conditioned that `n = 1,000` already agrees with `n = 400,000` to
`7 × 10⁻¹¹`. On the unbounded side, `x = e₁ + t²` makes `dx/√(4t²(x−e₂)(x−e₃))`
into `dt/√((x−e₂)(x−e₃))` — the singularity cancels algebraically.

**The tail has a closed form and it is used as a check.** Beyond `T` the
unbounded integrand behaves like `1/t²`, so the truncation error is exactly
`2/T` for the two signs of `y`. At `T = 4000` that is `5.0 × 10⁻⁴`, and it is
precisely the gap between the truncated value and the egg. Adding it lands the
two components on each other to `5.8 × 10⁻¹²` — so the closed form is confirmed
by the agreement rather than assumed, and the drill asserts it by running two
different cut-offs, which a single cut-off could never distinguish.

**Which convention BSD needs is therefore measured, not chosen:** the identity
closes with the integral over the **full real locus**, and one component is
exactly half of it. A gate that integrated the identity component alone would be
out by the same factor of two RUN-017 removed.

## §9's multiplicity no-go, read

The same document's §9 proves that order of vanishing is not continuous under
ordinary function convergence, with the witness

$$f_a(z)=z(z+a),\qquad \mathrm{ord}_0 f_a=1\ (a\ne0),\qquad \mathrm{ord}_0 f_0=2,$$

and `f_a → f_0` uniformly on compacts. The witness is correct, and it is worth
recording what it does **not** leave open, because the obvious sharpening is one
the document has already made.

For a holomorphic family converging locally uniformly, the *counted* number of
zeros in a small disc is conserved — the two zeros of `f_a` sit at `0` and `−a`,
both inside `|z| < r` once `|a| < r`. So it is only the order **at the point**
that jumps, while the multiplicity **near** the point is stable. That is a
Rouché/Hurwitz statement, and **Corollary 9.2 already names "Rouché-type
multiplicity control" among the mechanisms a grid route would have to supply**.
The no-go is stated at exactly the right scope: it blocks pointwise order, does
not claim to block neighbourhood counting, and lists the latter as work to be
done. This round confirms the scope and adds nothing to it.

That matters for an attack in one specific way. BSD's analytic rank is the order
at `s = 1` **exactly**, not a count over a neighbourhood, so even a route that
established Hurwitz-type stability would recover the wrong invariant — and the
witness shows by how much: the discrepancy is precisely the zeros that sit at
distance `|a|` and return to the point only in the limit.

## The drill

**99 defects, 99 caught by the check named for each — none uncaught, none
caught by the wrong check. 20 controls, none disturbed, over 46 checks.
Fourteen minutes and thirty-four seconds.**

Gate 26 contributes two checks and four defects. One of them exists to make a
past failure unrepeatable: **"the real period is doubled again on the `Δ > 0`
branch"** turns `rank2-bsd-identity` red, and the check asserts the sensitivity
directly — halving the period must send the ratio to exactly `2`. RUN-017's
error can no longer return silently, because the number it would break is now
external to this tree.

The cost was managed before the run rather than after, for the third time in
this line. `rank2-bsd-identity` first cost **30 seconds** because it compared
our regulator at doubling depth 10; over 99 defects that is three quarters of an
hour. It now runs at depth 8 — 0.17s — **with the tolerance set to what depth 8
measures**: the differences from the document's regulator are `2.4 × 10⁻⁴`,
`5.8 × 10⁻⁵`, `7.0 × 10⁻⁶`, `1.3 × 10⁻⁷` at depths 6, 7, 8, 10, so `2 × 10⁻⁵`
passes depth 8 and fails depth 7. A tolerance of `2 × 10⁻⁶` would have been
depth 10's and would have made the check fail on its own settings. The gate
still reports the depth-10 value.

## What this round does not claim

* **No `L`-derivative is computed.** `L''(E,1)/2!` is the document's number. This
  round supplies `Ω` and tests the identity; it does not independently confirm
  the leading coefficient, and the document itself marks analytic rank 2 as
  still requiring a rigorous certificate.
* **`Ш = 1` is assumed, not computed** — it is BSD-inferred in §6 and used here
  only to state the identity. Nothing below computes Ш, and treating the
  identity's closure as evidence about Ш would be the substitution Phase 0 §6
  names and RUN-019 audited.
* **Whether §6's three numbers are mutually independent cannot be read off the
  document.** What is established is that *this arm's* period, computed from the
  curve with no shared code, satisfies the identity their `L''` and `Reg`
  define.
* **The rank is cited.** `r_alg = 2` and the generators `P = (0,0)`, `Q = (1,0)`
  come from the literature, as they have in every round of this arm that used
  them.
