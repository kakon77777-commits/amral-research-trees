# RUN-025 — Hard-Zeta A-U.2e.4: the arithmetic holds, and one inference in §5 does not follow from its own premise

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2e4_bundle.zip` (source item 43) — Renewal Diophantine Rigidity via a Two-Sided Determinant Barrier, Farey Locking, and a Rational-Recycling No-Go
**Tools:** [`src43_renewal_rigidity.py`](../code/src43_renewal_rigidity.py) · [`src43_drill.py`](../code/src43_drill.py) · [`src43_emit_report_block.py`](../code/src43_emit_report_block.py)
**Logs:** [`src43-au2e4.json`](../data/gate-logs/src43-au2e4.json) · [`src43-drill.json`](../data/gate-logs/src43-drill.json)

**Result: every theorem in the round holds, exactly. Both stated constants are exact algebraic identities, not decimal approximations. One thing is different from the last four runs — this report contains an actual finding about the mathematics rather than only about reach: §5's premise is correct and the conclusion drawn from it does not follow, and `log₂3` itself is the counterexample.**

---

## First: this round is far more checkable than the two before it

Items 41 and 42 were dominated by hypotheses nobody can satisfy — a surviving
reset, a CASP orbit. This one is not. Its core is arithmetic about rational
approximants to `β = log₂3`: the determinant identity, the cross-error barrier,
the Farey lock, scale separation, the continued-fraction tax, and both recycling
no-gos are statements about **any** pair of rationals bracketing `β`. They need no
orbit at all, and they are checked here exactly, on real bracketing pairs drawn
from `β`'s own Stern–Brocot descent.

What still needs an orbit — that such approximants arise from one — the round
states as open in its own §13, and this run does not touch it.

## §2 — where the determinant theorem's strength actually lives

`Δ = p₊q₋ − p₋q₊ = q₋d₊ + q₊d₋` with `d₊ = p₊ − βq₊`, `d₋ = βq₋ − p₋`.

Substituting makes the `β` terms cancel, so **the identity holds for any `β`
whatsoever** — checked here by running it at several arbitrary rationals standing
in for `β`, not just at `log₂3`. It is algebra, not arithmetic about this number.

That locates the content. §2's strength is not the identity but the fact that `Δ`
is a **positive integer**, and that comes entirely from the bracketing
`p₋/q₋ < β < p₊/q₊` — verified on every real pair by exact `2^p` against `3^q`,
never by evaluating a logarithm.

## §6 — both constants are exact, and checking them as decimals would have missed that

The round prints `ρ(0.4) = 2` and `ρ(0.25) = 2+√3 ≈ 3.732`. Both are **exact
algebraic identities**:

- `c = 2/5` gives `1 − 4c² = 9/25`, a perfect rational square, so `ρ = 2` is a
  **rational** — provable in `Fraction` with no square root evaluated at all.
- `c = 1/4` gives `1 − 4c² = 3/4`, whose square root is `√3/2`, so `ρ = 2+√3`
  exactly; verified by squaring the surd away.

A decimal comparison would have confirmed the printed digits and said nothing
about whether the closed form is right.

---

## The finding — §5's conclusion does not follow from §5's premise

The round argues:

> **premise** — a Farey-locked bracket's next denominator is at least `q₋ + q₊`
> **conclusion** — therefore record denominators grow at least Fibonacci-type, so
> there are `O(log N)` record updates below `N`

**The premise is correct**, and this run verifies it at every step of the descent
with zero violations: the mediant's denominator is exactly `q₋ + q₊`.

**The conclusion does not follow.** Fibonacci growth needs the bracket to
*alternate* sides. When consecutive mediants land on the same side, one endpoint
stays **frozen** and each step adds a constant — which is linear, not Fibonacci.

And `log₂3` does exactly that. Its continued fraction has a partial quotient of
**23**, and along its own Stern–Brocot descent the convergent `1054/665` sits
frozen as the lower endpoint for 23 consecutive steps while the denominators walk

> `971, 1636, 2301, 2966, 3631, 4296, 4961, 5626, 6291`

in arithmetic progression with common difference **665** — the frozen endpoint's
own denominator.

**Every one of those brackets is Farey-locked.** The determinant is 1 at every
consecutive pair, verified with zero exceptions. So §5's hypothesis is satisfied
*perfectly* and its conclusion still fails. This is not a case the hypothesis
excludes; it is the hypothesis holding and the inference not carrying.

### What is true instead

The conclusion **is** correct if record updates are restricted to
continued-fraction **convergents**, where `q_{k+1} = a_{k+1}q_k + q_{k−1} ≥ q_k +
q_{k−1}` — and this run confirms the convergents satisfy the recursion with zero
failures. But the Farey-lock condition admits **semiconvergents**, and the
Stern–Brocot mediants are exactly the Farey-locked ones. A renewal approximant is
whatever the orbit produces; nothing restricts it to convergents.

So the count of Farey-locked record updates below `N` is `Σaᵢ`, not the number of
convergents — and whether that is `O(log N)` for `β` reduces to whether `β`'s
partial quotients are **bounded**, which is an open question about `log₂3`. The
measured ratio of updates to `log₂N` is not flat; it climbs across the range
sampled, which is in the generated block below.

### What this does and does not cost the round

It does not touch Theorems 1–4 or 6–9. §5 is used to argue that Farey-locked
renewal record updates are *sparse*; the sparsity is weaker than stated, and it is
weakest exactly where `log₂3`'s continued fraction has large partial quotients.
The Renewal Diophantine Rigidity Frontier of §11 does not depend on the growth
rate — its three regimes come from the determinant, and those are intact.

---

<!-- BEGIN GENERATED measured block: python code/src43_emit_report_block.py -->

| what | measured | value |
| --- | --- | --- |
| bracketing pairs formed | every lower approximant against every upper | `272` |
| …with `Δ = 1` (Farey-locked) |  | `41` |
| …with `Δ > 1` | so the positivity check is not tested only where it is automatic | `231` |
| largest `Δ` seen |  | `9126` |
| `Δ ≥ 1` violations | exact integer comparison | `0` |
| identity violations at arbitrary `β` | 4 pairs × 8 substitutions; it is algebra, not arithmetic about log₂3 | `0` |
| cross-error barrier violations | `max(d₋,d₊) ≥ 1/(q₋+q₊)`, β bracketed | `0` |
| …undecided by the β bracket | reported, never rounded | `0` |
| …pairs within a factor 2 of the barrier | so the bound is approached | `18` |
| consecutive brackets **not** Farey-locked | must be zero | `0` |
| locked pairs violating `s ≥ q₋+q₊` | and the mediant attains it | `0` |
| unlocked pairs admitting a cheaper interior | the negative half — 138 checked | `138` |
| continued-fraction tax violations | `1/(q+q′) < |qβ−p| < 1/q′` | `0` |
| recycling monotonicity violations | `g/(2^{gd}−1)` strictly decreasing over 995 samples | `0` |
| defects planted / caught by their own check | `code/src43_drill.py` | `14 / 14` |

**§5, premise against conclusion.** The premise is checked at every step of the descent; the inference is then tested directly.

| | |
| --- | --- |
| premise `q_new = q₋+q₊` violations | `0` |
| steps failing `q_k ≥ q_{k−1}+q_{k−2}` | **`33` of `45`** |
| longest same-side run | **`23`** |
| denominators across it | `971, 1636, 2301, 2966, 3631, 4296, 4961, 5626, 6291` |
| consecutive differences | `665, 665, 665, 665, 665, 665, 665, 665` — constant: `true` |
| **convergents** failing the recursion | `0` |

Record updates against `log₂N`, which would be bounded if the count were `O(log N)`:

| N | updates | log₂N | ratio |
| --- | --- | --- | --- |
| 100 | 10 | 6.6 | **1.51** |
| 1000 | 17 | 10.0 | **1.71** |
| 10000 | 30 | 13.3 | **2.26** |
| 100000 | 43 | 16.6 | **2.59** |

**The two constants, exactly.** `c = 2/5` gives `1 − 4c² = 9/25`, a perfect rational square, so `ρ = 2` — a rational, no square root evaluated. `c = 1/4` gives `1 − 4c² = 3/4`, so `ρ = 2 + sqrt(3)`, recomputed as `3.732050807568877293` against the round's printed `3.732`.

**Scale separation, and where its hypothesis is inhabited at all.** `c = 1/10`: 0 qualifying pairs, 0 violations; `c = 1/4`: 0 qualifying pairs, 0 violations; `c = 2/5`: 5 qualifying pairs, 0 violations, smallest scale ratio `12/5`. A `c` with no qualifying pair is reported as uninhabited rather than as a pass — requiring every `c` to be inhabited would be asking the sample to contain the very configuration the theorem constrains.

Every figure above is emitted by `code/src43_emit_report_block.py` from the two gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## A note the round already makes, and this arm can now speak to

§12 says explicitly that it does **not** elevate Niu 2026's numerical observation
to a theorem, and instead derives the Farey / Stern–Brocot geometry from the
integer determinant. That is the right way round, and RUN-023 is the other half of
it: this arm *measured* the clustering independently — near misses to the
correction cap land on the Stern–Brocot path at **66.3 %** against a population
base rate of **12.9 %** — without evaluating a logarithm. The numerical
observation and the algebraic mechanism now sit on the same page from two
directions.

## The instrument

`src43_drill.py` plants 14 defects and requires each to be caught **by the check
named for it**. Its first pass reported **five misses**, and four were the same
class this tree keeps meeting:

**Weakening a check that never fires is undetectable.** The Farey bound, the CF
tax and §5's premise check all report zero on real data, so loosening their
comparisons moved nothing. The rule that came out of it:

> **To test a check that never fires, break its SUBJECT, not its comparison.**

Re-aimed accordingly — the interior search now accepts an endpoint, the tax uses
the current denominator instead of the next, and the descent stops taking true
mediants. All three then fire.

The fifth miss found a real hole rather than a bad defect: `is_a_perfect_rational_square`
was **decorative** — computed, reported, and read by no verdict. Weakening it
changed nothing because nothing consumed it. It is wired into the result now. (Its
first replacement was also a no-op — `inside == inside` is True exactly where
`inside == root*root` is True — which is the item-42 lesson again: a planted
defect that changes nothing was never planted.)

Three defects guard non-vacuity rather than correctness: emptying the determinant
sample of unlocked pairs, removing the Farey check's negative half, and emptying
every scale-separation hypothesis. All three are caught by guards that refuse a
vacuous pass rather than by violation counts.

## Route map

`ROUTE_MAP v1.9` names **A-U.2d — Transducer Rationality** as the main line, with
**A-U.2e.5** (Farey Renewal Graph) and **A-L** (Giant Valuation Tail) beside it.
The round's own §13 says the same: the remaining question is whether these
approximants can come from a fixed positive-integer exponent transducer. Item 44
is `AU2d`, so the file ordering and the route map agree for the sixth time.

If A-U.2e.5 is written, the finding above is directly relevant: a Farey renewal
graph walk is a walk on the Stern–Brocot tree, and the long same-side runs are
exactly the stretches where such a walk is cheap rather than expensive.

## What this run does not claim

1. That any of the three regimes (Determinant Heavy, Farey Locked, Scale
   Separated) is impossible. The round says none is ruled out and this run adds
   nothing there.
2. That renewal approximants arise from an actual orbit. Open, and stated as open
   in §13.
3. That `β`'s partial quotients are unbounded. The finding is that §5's `O(log N)`
   *depends* on their being bounded, not that they are not.
4. That the scale-separation theorem is exercised at every `c`. At `c = 1/4` and
   `c = 1/10` no bracketing pair in the sample satisfies the hypothesis at all —
   reported as uninhabited rather than as a pass, and consistent with the
   theorem's own claim that ultra-tight two-sided pairs are constrained.
