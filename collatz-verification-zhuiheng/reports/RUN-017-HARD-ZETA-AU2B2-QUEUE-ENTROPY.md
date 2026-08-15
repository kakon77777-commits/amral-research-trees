# RUN-017 — Round A-U.2b.2: the lever bought nothing at first order, and the shipped JSON is not the shipped script's output

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2b2_bundle.zip` (source item 35) — Round A-U.2b.2 *Queue-Entropy Saturation, Second-Order Packing Barrier and Prefix-Constraint No-Gain*, its `verify_…queue_second_order.py` and `…constants_and_queue.json`, three figures, plus `A_Line_ROUTE_MAP_v1.3`
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (A-U.2b.2 layer) · [`src19_hardzeta_au2b2_recheck.py`](../code/src19_hardzeta_au2b2_recheck.py) · [`src19_drill.py`](../code/src19_drill.py)
**Logs:** [`src19-au2b2-recheck.json`](../data/gate-logs/src19-au2b2-recheck.json) · [`src19-drill.json`](../data/gate-logs/src19-drill.json)

**Result: 19/19 checks. 27/27 planted defects caught by the check named for each — 12 in the A-U.2b.2 layer, 10 in this run's own measurement, 5 in the artifact. 2/2 null controls undisturbed. Coverage audit clean.**

---

## Which lever was pulled, and what it bought

A-U.2b.1 §28 listed five things that could beat `c_pack`. This round pulls the
first — **queue entropy** — on the reasonable hypothesis that requiring the
deficit to stay in its corridor at *every* prefix must cost the block count
something.

It does not. The round's own **Prefix-Constraint First-Order No-Gain** theorem
says the all-prefix queue language has the same first-order entropy `H(γ+x)` as
the unconstrained composition count, so `c_pack` stands unchanged. Measured on
the subject's own dynamic program:

| `r` | `D` | rate `= log₂|Q|/r` | gap to `β` |
|---|---|---|---|
| 50 | 2 | 1.1539 | 0.431 |
| 200 | 11 | 1.5188 | 0.066 |
| 800 | 45 | 1.5700 | 0.015 |
| 2000 | 113 | 1.5787 | 0.0063 |
| 5000 | 284 | **1.5825** | **0.00246** |

Monotone, and closing on `β = 1.58496`. The corridor constraint costs a
`2^{o(r)}` factor and nothing more.

**The second-order term came from somewhere else.** Not from the five levers at
all — from the **Stirling prefactor**, the `r^{−1/2}` that the first-order
argument threw away. That gives

```
h* = H'(z*) = log₂(1 + 1/z*) = 1.3550907472…
d_pack = 1/(2h*) = 0.3689789787331466…
```

and the barrier `limsup (D_N − c_pack log₂N)/log₂log₂N ≥ d_pack`.

So the honest accounting is: **one of the five levers was tried and returned
zero; the gain came from a sixth thing that was not on the list.** Four levers
remain untried.

---

## The dynamic program, checked by reimplementation

The subject ships an exact deficit-corridor DP and a table of its output. That
table is the strongest thing here to check, so it is checked by a **reimplemented
DP** that differs in two deliberate ways:

- it accumulates from the **low** end via prefix sums, where the subject
  accumulates from the high end via suffix sums;
- it takes its credits from **exact integer** `floor_beta`, where the subject
  multiplies a float `γ` and floors.

And the reimplementation is validated against **brute-force enumeration** at
seven small shapes before being used to grade anything.

**All nine published rows reproduce** — both the rate and the centered gap, to
every printed digit.

The float question is not rhetorical: `⌊γ·j⌋` computed in floating point could
slip by one where `γj` lands near an integer, and that would silently change the
credit word the whole table is built on. Checked over `j ≤ 20000`: **no
disagreement**. A clean result, but one that could have gone the other way.

The second-order constants likewise reproduce independently — `h*` to 80 digits,
`d_pack` to 82, and the safe margin `½ − h*·0.36 = 0.0121673310…` to 82.

---

## The envelope is exhausted again — third round running

§26 generalises the block scale to `r = L/β + s·ℓ` and gives two exponents,
both of which must be negative:

```
P₁ = h*·d + s(β − h*x*) − ½
P₂ = h*(d − x*s) − ½
```

Scanning `s` over `[−0.5, 0.5]` and maximising the admissible `d`:

| | `s` | `d` |
|---|---|---|
| optimum | **0.000** | **0.3689789787331466** |
| published `d_pack` | — | 0.3689789787331466 |

`s = 0` is exactly the optimum and `d_pack` is exactly the ceiling. And it is a
genuine corner, not an arbitrary choice: moving `s` up breaks `P₁` (because
`β − h*x* = 1.508 > 0`), moving it down breaks `P₂`. Both sides are exhibited.

That makes **three consecutive rounds published at their own supremum** —
A-U.2b.1, and now both constants of A-U.2b.2. A-U.2b, by contrast, published 67%
of what its scheme allowed. The practice changed at A-U.2b.1 and has held.

---

## The shipped JSON was not produced by the shipped script

The bundle carries `verify_Hard_Zeta_AU2b2_queue_second_order.py` and
`Hard_Zeta_AU2b2_constants_and_queue.json`. They do not correspond:

| | script | JSON |
|---|---|---|
| rows | 8 (`r = 100 … 5000`) | **9** (`r = 50` as well) |
| row fields | `log2_count_over_r`, `beta_minus_rate`, `centered_gap` | `rate`, `centered_gap` |

The script would emit an extra column (`beta_minus_rate`), would not emit the
`r = 50` row, and names the rate field differently. **So the JSON came from a
different revision of the generator than the one shipped beside it.**

**Every number in it is nevertheless correct.** All nine rows, including the one
the shipped script would not produce, reproduce exactly under this arm's
independent DP. So this is a stale generator/output pairing — a provenance
defect in the artifact, not a wrong result.

It is worth naming precisely because of what this tree recorded yesterday about
where mathematics and computation fail to meet: this is squarely a defect of
*realization*. The mathematics is intact, the numbers are right, and the thing
that broke is the pairing between a program and the file it claims to have
written. RUN-016 built a check for exactly this shape after seeing the artifact
convention start; here it has something to find.

What is *checked* rather than merely recorded is the weaker, falsifiable claim:
every row the script would emit appears in the JSON, so the JSON does not
contradict its generator. A drill defect that removes a row the script emits
fails that check.

---

## Three findings about my own checks

**A check that a completely wrong root would have passed.** "0.36 clears the
criterion `h*·d < ½` and lies below `d_pack`" is satisfied *more* easily by a
**larger** `d_pack`. A drill defect that flips the bisection direction lands the
root on `z = 1` instead of `z* = 0.6418` — giving `h = 1` and `d_pack = 0.5` —
and `0.36` still clears both. The check now also pins the root itself:
`|H(z*) − β| < 10⁻⁴⁰`. That is the difference between checking a consequence and
checking the thing the consequence comes from.

**A `≥` where the undamaged value is exactly zero.** The two block-scale
exponents are exactly `0` at `s = 0`, `d = d_pack` — that is what makes it the
optimum. So a defect deleting the `s`-dependence leaves them at zero, and a
`≥ 0` test passes for entirely the wrong reason. Both are now strict `> 0` at
`s = ±0.05`, where the undamaged values are `+0.075` and `+0.004`.

**A near-tie mistaken for a defect, and a redundant guard.** Reading `d_pack` as
the safe constant gives `h·d_pack = 0.4999999999999999999999` — below `½` by
rounding, so it passes; replaced with a value genuinely above the threshold. And
widening the brute-force deficit guard to `−1` is a no-op, because the excess
loop already stops at `d + b` and never produces a negative deficit: the loop
bound and the guard are redundant with each other. Excluding `e = 0` removes real
paths instead. That is the twelfth no-op of the loosening family in this arm.

---

## What this does not establish

§34's unproved list: the exact polynomial prefactor of the queue count, whether a
queue ballot factor could raise `d_pack`, exclusion below higher-order
boundaries, CASP, Terras, Collatz. The saturation theorem is a limit statement;
what is checked here is a monotone approach on nine finite corridors, with the
gap still at `2.5 × 10⁻³` at `r = 5000`. The block-scale optimality is optimality
*within this envelope*, and the round says so.
