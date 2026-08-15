# RUN-015 — Round A-U.2b: a real elimination, and how far its own constant can go

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2b_bundle.zip` (source item 33) — Round A-U.2b *Sparse Lift Rigidity: Exact Return Separation, Valuation-Language Entropy Gap and Logarithmic Deficit Barrier*, plus `A_Line_ROUTE_MAP_v1.1`
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (A-U.2b layer) · [`src17_hardzeta_au2b_recheck.py`](../code/src17_hardzeta_au2b_recheck.py) · [`src17_drill.py`](../code/src17_drill.py)
**Logs:** [`src17-au2b-recheck.json`](../data/gate-logs/src17-au2b-recheck.json) · [`src17-drill.json`](../data/gate-logs/src17-drill.json)

**Result: 25/25 checks. 34/34 planted defects caught by the check named for each — 16 in the A-U.2b layer, 14 in this run's own measurement, 4 in the documents. 2/2 null controls undisturbed. Coverage audit clean.**

---

## The first round of Phase II that eliminates something

A-U.1 and A-U.2a both ended in no-gos. This one does not. It proves a positive
statement — every positive-integer all-prefix subcritical accelerated orbit has

```
limsup_{N→∞}  D_N / log₂N  ≥  0.01           D_N = max_{m≤N} d_m
```

and therefore `sup_m d_m = ∞`. From that it eliminates outright: the mechanical
critical code, bounded-discrepancy critical codes, bounded-deficit spines,
ultimately periodic subcritical codes, and low-complexity candidates with thin
deficit envelopes.

**It also settles the question RUN-014 left open.** I measured that the
mechanical code — the countermodel that defeated A-U.1 — has positive lift flux,
so A-U.2a's Zero-Flux Boundary Theorem already reached it. A-U.2b now proves it
is unanchored by a completely different route: `K*_m = ⌊βm⌋` exactly, so `d_m = 0`
for every `m`, so `D_N = 0 = o(log N)`, and the barrier applies directly. Verified
here to `m = 400`. **Two independent arguments, same verdict** — and RUN-013's
direct measurement that its lift digits never stop is a third.

---

## The whole thing turns on 2.8395 < 3

The argument is a squeeze between two exponential scales.

**Upward — return separation.** §4's Repeated-Block Congruence: if the same
length-`r` exponent block follows positions `a` and `b`, with block valuation `Q`,
then `Y_a ≡ Y_b (mod 2^{Q+1})`. On an infinite subcritical spine no state repeats
— a repeat would force an accelerated cycle, whose equation
`(2^{Q_cyc} − 3^p)Y = B_cyc > 0` demands `Q_cyc > pβ`, contradicting `K_m < mβ`.
So `|Y_b − Y_a| ≥ 2^{Q+1}`, and §19 turns that into base 3: `Q ≥ ⌊βr⌋ − D` gives
`2^{Q+1} > 3^r/2^D`.

**Downward — how many thin-deficit blocks exist.** §15's ledger
`E_{i,r} = ⌊γ(i+r)⌋ − ⌊γi⌋ + d_i − d_{i+r}` pins the block excess, §16 confines it
to a band of width `2D` around `γr`, and §17 counts the compositions. Stirling
gives the growth base

```
Λ_γ = (1+γ)^{1+γ} / γ^γ
```

I computed it at 60 digits: **`Λ_γ = 2.83951373049775259640…`**, matching the
paper's `2.8395137304…` on every digit stated, and `Λ_γ < 3` with a gap of
`0.1605` — 5.35%.

That gap is the theorem. Thin-deficit codes cannot supply enough distinguishable
length-`r` blocks to keep up with the separation the integers force, so a repeat
must occur too early, and §24's excursion bound `M_N < 2^{D_N+1}(n + N/3)` says the
states are too small to be that far apart. Contradiction.

**The explicit constants, checked rather than believed.** §21 needs
`1/β < c < 1/log₂Λ_γ` to be non-empty — measured, `(0.630930, 0.664168)`, and the
paper's `c = 0.645` is inside. §26's two inequalities at `c = 0.645`, `ε = 0.01`:

| claim | computed | margin |
|---|---|---|
| `βc − 1 − 2ε > 0.0022` | `0.0023008129…` | `1.008 × 10⁻⁴` |
| `c·log₂Λ_{γ+ε/c} < 0.986` | `0.9854014472…` | `5.986 × 10⁻⁴` |

Both clear, and both are tight to the fourth decimal — the constants were chosen
to just pass, and they just pass. Each is drilled by a perturbation *smaller than
its own margin*, so the check has to be reading the real value and not a rounded
one.

---

## The measurement: how far this argument can be pushed

§37 names the next round **A-U.2b.1 — Sharp threshold for `D_N ∼ c log N`**. So
the useful question is what the *existing* scheme can already give, before any new
idea is needed.

The two constraints, read off §22–§24, are

```
block count is o(N):        c · log₂ Λ_{γ + ε/c} < 1
separation beats the peak:  βc − 1 − 2ε > 0
```

Maximising `ε` over `c`:

| | `c` | `ε` |
|---|---|---|
| published | 0.645 | **0.01** |
| this scheme's ceiling | 0.650 | **0.01502** |

**The published `0.01` is a safe round number, not the scheme's limit — the same
argument supports about `0.015`, a 50% improvement with no new ideas.** Anything
past `0.0150` needs a different argument, because at that point the two
constraints meet. That is a concrete starting point for A-U.2b.1: it says where
the cheap gains stop.

---

## Every eliminated family, checked on an instance

- **Mechanical code**: `K*_m = ⌊βm⌋` so `d_m ≡ 0` — verified to `m = 400`. And its
  factor complexity is exactly `p(r) = r + 1` for `r ≤ 24`, confirming §31's
  Sturmian claim, which excludes it a second time through the
  complexity–deficit tradeoff.
- **Ultimately periodic tails**: §33's source `y = B_per/(2^Q − 3^p)` is negative
  for every subcritical period tested, and positive exactly when the period is
  supercritical — both outcomes present, so the implication is not graded on one
  side.
- **Bounded deficit**: `sup d_m < ∞ ⟹ D_N = o(log N)`, so the barrier applies.

Everything upstream holds on real spines too: the repeated-block congruence (on
actual repeats, with a guard that repeats occur at all), the return separation,
the complexity–peak law `M_{p(r)+1} ≥ 2^{r+1}`, the excursion bound in exact
rationals, and the complexity–deficit tradeoff.

**One clarification worth recording.** The all-ones family `2^{m+1}−1` is *not* a
low-deficit family — it is the opposite extreme. `K_j = j` gives `d_j = ⌊γj⌋`,
which grows linearly, the largest deficit possible. The zero-deficit object is the
mechanical code. Both are extremes of the same ledger and it is easy to conflate
them.

---

## What real starts do

The theorem constrains a hypothetical: no positive integer is known to have an
infinite subcritical spine. What exists are finite runs, and they clear the
barrier by two orders of magnitude:

| start | lifetime | `D_N` | `D_N/log₂N` |
|---|---|---|---|
| 27 | 36 | 6 | 1.16 |
| 703 | 50 | 6 | 1.06 |
| 10087 | 65 | 6 | 1.00 |
| 35655 | 84 | 8 | 1.25 |
| `2^17−1` | 62 | 11 | 1.85 |

The only object with `D_N = 0` is the mechanical code — which §30 proves is not a
positive integer. So the check is stated with both outcomes: every real start
clears `0.01`, and the one thing that does not is exactly the countermodel.

---

## Findings about my own checks

**Five defects belonged to different checks than I named — and each miss said
something true.** Replacing the record deficit's `max` by `min` leaves the
complexity–deficit tradeoff intact, because its right-hand side
`r − log₂(n + N/3)` is negative at small `r`, so *any* non-negative deficit
satisfies it. Shortening the subcritical lifetime produces *shorter* orbits and
therefore *fewer* repeats, so "no state repeats" survives it. Shifting the
valuation list never reaches the excursion bound, which reads the deficit and the
endpoints instead. `gamma_decimal()` is read only by the entropy check, not by the
interval check, which computes `β` itself. And flipping the sign inside
`log₂Λ` makes the constant *smaller* — `0.6006` instead of `1.5057` — so the
admissible interval's upper end moves out to `1.665` and `c = 0.645` is still
comfortably inside: the interval **widens** rather than emptying. Each was
retargeted and each orphaned check was given a defect of its own — including one
that makes `orbit_endpoints` return a constant, which is what "no state repeats"
actually needs to be able to fail, and one that computes the interval's lower end
from `γ` instead of `β`, which does empty it.

**The tenth loosening no-op.** Making the peak law read `max(Y)` instead of
`max(Y[:N])` cannot fail: `max(Y) ≥ max(Y[:N])`, so the failure condition
`max < 2^{r+1}` becomes *harder*, not easier. Replaced by shrinking the window to
`Y[:1]`, which moves the answer. Every constant in this drill is instead perturbed
by less than the margin it claims to clear.

**A check that is a corollary of another check.** §16's thin-deficit range
`⌊γr⌋ − D ≤ E ≤ ⌈γr⌉ + D` follows from §15's ledger together with `d ≤ D`, both
already checked — so on a degenerate sample it would hold for free. It now
requires the block excess to actually **vary** across the sample (measured spread
`0…6` at `r = 3`), which is the part that is not entailed.

**A contrast whose sample avoided the interesting case.** "Real spines clear
`D_N/log₂N > 0.01`" passed with margin ~100×, and would have passed no matter what,
because the only object that fails it was not in the sample. It now includes the
mechanical code explicitly and requires **both** outcomes — real starts clearing,
the countermodel at exactly zero. That is the theorem's content rather than a
one-sided sample.

No defect in this drill loosens a comparison. That shape was a no-op nine times in
this arm; every constant here is instead perturbed by less than the margin it
claims to clear.

---

## What this does not establish

§36's own list: `D_N ≍ c log N` is not excluded, nor sparse unbounded deficit
spikes, nor high-complexity critical inputs, nor zero-density nonzero lift events,
nor CASP, CST, or Collatz. The barrier is a statement about infinite orbits and is
not finitely checkable; what is checked here is the exact algebra it rests on, the
constants at 60 digits, and the eliminated families on explicit instances. The
`0.015` ceiling is a property of *this* proof scheme, measured under the two
constraints as I read them from §22–§24 — a different reading of the error terms
would move it.
