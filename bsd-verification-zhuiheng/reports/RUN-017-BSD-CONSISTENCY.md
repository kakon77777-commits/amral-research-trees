# RUN-017 — a real period that was wrong for three rounds, and the BSD identity as the thing that found it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** this arm's own analytic machinery — and the rank-0 strong BSD formula used as a joint test of everything under it
**Tools:** [`src20_bsd_consistency.py`](../code/src20_bsd_consistency.py), [`src15_phase2_anchor.py`](../code/src15_phase2_anchor.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src20-bsd-consistency.json`](../data/gate-logs/src20-bsd-consistency.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the real period was computed twice too large for every curve with `Δ > 0` — for three rounds, undetected, because the only thing it was ever compared with was a baseline taken from itself. Numerical integration over `E(R)` settles it in one line. Nothing already reported moves: the anchor and every twist have `Δ < 0`. Beyond that: `285` curves close the rank-0 BSD identity on `#Ш = 1` exactly, which validates four separately computed quantities at once; the regulator of `389.a1` is `0.152460306865`, giving a third independent proof that `P` and `Q` are independent; and RUN-014's root-number test turns out to have reported a confidence it never had.**

---

## The bug, and why no check could see it

`real_period` computes `Ω = ∫_{E(R)}|ω|` by AGM. For `Δ < 0` there is one real
component; for `Δ > 0` there are two, and the branch for that case carried a
spurious factor of 2.

It went unseen for three rounds because of how it was checked. RUN-014's drill
asserts `Ω(37a1) = 11.973834584927838` — **a value taken from this same
function**. Freezing a computation's own output as a regression baseline detects
drift and nothing else. The `Δ < 0` half was genuinely validated (`11a1` gives
`L/Ω = 1/5` exactly, which is `#Ш·c₁₁/#tors² = 1·5/25`), and the `Δ > 0` half
was validated against itself.

Integrating `dx/√(4x³+b₂x²+2b₄x+b₆)` over the real locus — the unbounded
component by `x = e₁ + t²`, the egg by `x = e₃ + (e₂−e₃)sin²u` — shares no code
with the AGM:

| curve | `Δ` | AGM | numerical | ratio |
| --- | ---: | ---: | ---: | ---: |
| 11a1 | −161,051 | 1.2692093043 | 1.2692093043 | **1.00000000** |
| 696.e1 | −178,176 | 1.6317277401 | 1.6317277401 | **1.00000000** |
| 37a1 | 37 | 11.9738345849 | 5.9869172925 | **2.00000000** |
| 389a1 | 389 | 9.9608502434 | 4.9804251217 | **2.00000000** |
| 34a1 | 1,088 | 8.9913266526 | 4.4956633263 | **2.00000000** |

Exactly 1 where the two components do not arise and exactly 2 where they do.

**Nothing already reported moves.** RUN-014's anchor has `Δ = −178,176 < 0`, and
every twist in RUN-015 has `Δ(E^{(q)}) = q⁶·Δ(E) < 0`. Re-running both gates
leaves `L/Ω = 1` and `L/Ω = 49` unchanged to the last digit; the only values that
move are the two `Δ > 0` curves in gate 15's self-check, both of which have
`L(E,1) = 0` either way.

The drill now carries the numerical integration as an independent check, and two
defects against it: dropping the second component, and restoring the doubling
that used to be there.

## The rank-0 BSD identity as a joint test

At rank 0 the strong formula says

$$\frac{L(E,1)}{\Omega}=\frac{\#Ш\cdot\prod_p c_p}{\#E(\mathbf Q)_{\rm tors}^2},$$

and Cassels makes `#Ш` a square. Four separately computed quantities go in — the
`L`-value from point counts, the period by AGM, the torsion by a gcd bound, every
`c_p` by Tate's algorithm — and their combination must land on a **positive
integer square**. There is nothing approximate about that target.

Over the 420 base curves of conductor ≤ 2000:

| | count |
| --- | ---: |
| **BSD closes on a positive integer square** | **285** |
| BSD does not close | 103 |
| sign undecided by the guard | 26 |
| sign says −1 | 6 |

**The value it closes on is `1` for all 285.** Not one lands on 4, 9 or 16 —
which is itself informative about this population — and none of the 103 failures
is within `10⁻⁶` of any integer square, their ratios spreading from 0.19 to 1.12.

That pattern is the signature of a **mis-called sign**, not of a wrong period or
a wrong Tamagawa number. A wrong period scales every ratio by the same factor; a
wrong `c_p` moves one curve to a nearby rational. A wrong sign makes `L(E,1)` a
meaningless number, and meaningless numbers do not cluster near integers.

## What that says about RUN-014's sign test

RUN-014 determines the root number by comparing a smoothed `Λ(2)` against the
Dirichlet series `Σ a_n n^{−2}` and keeping whichever sign matches. It reported a
`residual` and a `gap`, and their ratio read as a confidence — 17,000 for the
anchor, 41 for a curve examined here.

**That ratio is not a confidence.** The residual is `|smoothed − direct|`, which
can be small by accident; so can the drift between partial sums. The honest bound
on the Dirichlet truncation is about `2·log M/√M`, which at these conductors is
**comparable to the gap being measured**. The test is much weaker than it was
presented as, and the 103 non-closing curves are where it broke.

**The anchor's sign survives, for a better reason than the one originally
given.** `L(696.e1,1)/Ω` came out `1` to sixteen digits, with the torsion and
every `c_p` computed by routes that never touch the `L`-series. If `L(E,1)` were
zero that agreement would be an absurd coincidence. The BSD identity is the
stronger sign test, and it is the one the anchor passes.

A guard has been added — the sign is reported as `None` unless the separation
clears the series' own drift by a factor of twenty — but the report of it here is
that **the guard is necessary and not sufficient**, and the honest statement is
that this method decides a sign only when the BSD identity confirms it.

## The regulator of 389.a1

The P5 line's stated core target is bridging the analytic leading term to the
algebraic regulator. The algebraic half is computable.

Canonical heights by `ĥ(P) = lim h(x(2ⁿP))/4ⁿ`, using the `x`-only duplication so
the integers stay small enough for the limit to be reached at all, with two
Richardson steps against the `1/4ⁿ` error:

| | |
| --- | ---: |
| `ĥ(P)`, `P = (0,0)` | 0.327001704779 |
| `ĥ(Q)`, `Q = (1,0)` | 0.476710842792 |
| `ĥ(P+Q)`, `P+Q = (−2,−1)` | 0.920758716485 |
| `ĥ(P−Q)`, `P−Q = (−1,−2)` | 0.686667982418 |
| **parallelogram-law residual** | **1.60 × 10⁻⁶** |
| `⟨P,Q⟩` | 0.058523084457 |
| **regulator** | **0.152460306865** |

The parallelogram law `ĥ(P+Q) + ĥ(P−Q) = 2ĥ(P) + 2ĥ(Q)` is not an input to the
limit, so requiring it constrains the computation from outside.

A non-zero regulator makes `P` and `Q` independent, so this is a **third**
independent proof that `389.a1` has rank ≥ 2 — after RUN-011's localization
determinant `det M_loc = 2 ≠ 0` in `F₁₁`, which shares no arithmetic with it.

## What this round does not claim

* **Nothing about BSD.** The identity is used as a *test of the computations*,
  in the direction where it is known to hold for these curves. Where it closes,
  four routines are validated at once; where it fails, one of the inputs is
  wrong and the round says which one it thinks it is.
* **`#Ш = 1` for the 285 is what the identity gives under the assumption that
  BSD holds for them**, not an independent computation of Ш.
* **The 103 non-closing curves are not claimed to have odd rank.** What is
  claimed is that their sign determination is not trustworthy, and the evidence
  is the shape of the failure rather than a separate rank computation.
* **The regulator is numerical**, to about six digits, with the parallelogram
  law as its only external constraint. It is not an exact height pairing.
* **RUN-014's and RUN-015's conclusions are unchanged.** The period fix touches
  only `Δ > 0`, and every curve in either round has `Δ < 0`. That is stated
  because a correction to a shared routine is exactly the kind of thing that
  should be checked against earlier results rather than assumed harmless.
