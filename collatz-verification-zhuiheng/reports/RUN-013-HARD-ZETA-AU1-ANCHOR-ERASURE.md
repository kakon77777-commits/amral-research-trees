# RUN-013 — Round A-U.1: the no-go holds, and the datum it says is missing is measurable

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU1_bundle.zip` (source item 31) — Round A-U.1 *Critical Occupation Measures: Invariant-Limit Theorem, Exponent-Shift Completion Countermodels and Anchor-Erasure No-Go*, plus `A_Line_ROUTE_MAP_v0.9`
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (A-U.1 layer) · [`src15_hardzeta_au1_recheck.py`](../code/src15_hardzeta_au1_recheck.py) · [`src15_drill.py`](../code/src15_drill.py)
**Logs:** [`src15-au1-recheck.json`](../data/gate-logs/src15-au1-recheck.json) · [`src15-drill.json`](../data/gate-logs/src15-drill.json)

**Result: 23/23 checks. 26/26 planted defects caught by the check named for each. 2/2 null controls undisturbed.**

---

## What kind of round this is

Phase I closed the A line onto CASP and split it into two regimes. A-U.1 opens
the first, **and closes it as a route.** That is unusual enough to state plainly:
this round's main result is that its own programme does not work.

The argument has two halves and both are checked here.

**The half that succeeds.** §6–§12 prove a *Critical Invariant-Limit Theorem*: a
critical A-U candidate's empirical measures have weak-\* limits `ν` with

```
S_*ν = ν        ν({−1/3}) = 0        ∫(q−1) dν = γ,  so  ∫q dν = β
```

The route through it is careful — `ν({ξ}) = 0` comes from a **mass bound**
(§8), `ν_m(C_R) ≤ (γ + O(1/m))/(R−1)`, which is what makes `S` almost-everywhere
continuous so weak convergence can be passed through it at all.

**The half that closes the route.** §13–§17 then show those conditions are
*consistent*, by two explicit countermodels. So no contradiction can come from
invariance, uniform integrability and the critical mean alone.

---

## The two countermodels, verified

**§13, the Bernoulli critical measure.** The product measure
`⊗[(1−γ)δ₁ + γδ₂]` on the alphabet `{1,2}` is shift-invariant with
`∫q dμ = 1 + γ = β`, and because `q ≤ 2` its uniform integrability is free. The
mean identity is checked in exact `Fraction`s at seven rationals; since `γ` is
irrational the critical case is pinned by bracketing it — `53/91 < γ < 12/19`
gives means `1.582 < β < 1.632`.

**§15, the mechanical code.** `q*_m = ⌊βm⌋ − ⌊β(m−1)⌋` telescopes to
`K*_m = ⌊βm⌋`, lives in `{1,2}`, and is subcritical at every prefix — all
verified to `m = 300` in exact integers (`2^{K*_m} < 3^m`, no float decides it),
alphabet to `m = 2000`. Its 2-density converges to `γ`:

| `m` | 2-frequency | gap from `γ` |
|---|---|---|
| 100 | 0.5800 | 4.96e−3 |
| 500 | 0.5840 | 9.63e−4 |
| 2000 | 0.5845 | 4.63e−4 |
| 8000 | 0.584875 | 8.75e−5 |

**A cross-check worth recording:** this is the same sequence `hz_accel_code.py`
has carried since RUN-008, where it was implemented from Round 03-A.1's
description as "the maximal subcritical code". A-U.1 §15 states it independently
as a closed formula. The two agree on all 300 terms compared. Two rounds, two
descriptions, one sequence.

**The conjugacy underneath.** §5's `E : 𝔛_∞ → ℕ_{≥1}^ℕ` being a bijection
intertwining `S` with the shift is what lets a symbolic measure be pulled back at
all. Checked in the finite form that carries it: a code is exactly one clopen
cylinder `r_m + 2^{K_m+1}ℤ₂` (with witnesses *outside* it, not only inside),
cylinders nest as codes extend, `E(Sx) = σE(x)` under direct iteration on
integers, and codes with large and supercritical valuations — `(17,3)`,
`(1,1,20)`, `(12,1,5)` — are realized too, since the alphabet is all of `ℕ_{≥1}`
and not merely the legal codes.

---

## The datum the no-go says is missing — measured

§21 identifies what survives: the exact source lift

```
r̂_{m+1} = r̂_m + t_{m+1}·2^{K_m+1}       positive-integer anchor ⟺ t_m = 0 eventually
```

and §22 explains why an occupation measure cannot carry it — `t_m` compares
canonical lifts of the *original source cylinder* across prefix lengths, not any
bounded function of the current tail.

That is a claim about what the occupation measure lacks. It is also, taken
directly, something this arm can compute. So:

| start | lift settles at | nonzero lifts before |
|---|---|---|
| 27 | `m = 3` | 3 |
| 103 | `m = 5` | 4 |
| 703 | `m = 7` | 7 |
| 1407 | `m = 7` | 7 |
| 10087 | `m = 11` | 8 |
| 15039 | `m = 9` | 8 |
| 35655 | `m = 10` | 7 |

**Every genuine integer settles by `m = 11`**, and once it settles the canonical
source *is* that integer — checked, not assumed.

The mechanical code does not settle. To depth 60 it has **42 nonzero lifts**, the
last at **`m = 59`**, and its canonical source climbs monotonically at all 59
steps:

| `m` | 8 | 16 | 24 | 32 | 40 | 48 | 60 |
|---|---|---|---|---|---|---|---|
| source bits | 13 | 25 | 38 | 49 | 64 | 77 | 93 |

RUN-008 saw this source pass 29 million by `m = 16`; followed to `m = 60` it
passes `2^92`. It sits near the top of its permitted range `2^{K_m+1}` the whole
way — the source is roughly `3^m`.

**So the anchor cocycle separates the countermodel from a genuine integer by
`m = 11`, while the occupation measure never separates them at all** — §17 shows
the mechanical code's orbit measures pull back to a critical invariant measure
just like a real orbit's would. That is exactly the asymmetry §22–§23 assert,
made quantitative: the information is not merely absent from the occupation
measure, it is *cheaply available* in the coordinate the occupation measure
discards.

**What this does not decide.** §16 explicitly declines to say whether the
mechanical point `x_★` is an ordinary positive integer, calling that the
anchor-sensitive question. This does not decide it either. What is measured is
that **no positive integer below `2^{K_60+1}` realizes the mechanical code**, and
that its lifts are still nonzero where the computation stops. A finite window
cannot exclude an integer beyond it, and the round is right to leave it open.

---

## Dense but not closed, with a witness

§18's first sentence — every odd residue class holds a positive odd integer — is a
tautology, and I initially wrote it as a check, which could not fail. §18's
content is the second sentence: `ℕ_odd` is dense in `𝒪` but **not closed**. The
mechanical code witnesses that concretely, and that is what is checked instead:
its canonical sources are positive odd integers, each congruent to the next
modulo `2^{K_m+1}` (so the sequence is 2-adically Cauchy), while growing from 3 to
93 bits. A convergent sequence of positive integers whose real size diverges is
exactly how the limit leaves `ℕ_odd`.

---

## The ledger, and what it refuses

§32 lists seven results proved and five not. The unproved list still contains
*Pointed Critical Occupation Rigidity*, *CASP exclusion*, **Terras**, and
**Collatz** — checked, because a negative result of this shape is easy to
misread as progress on the conjecture, and it is not. §33 says it in the paper's
own words: ordinary 2-adic occupation theory can describe counterexample-like
dynamics but cannot tell whether they are anchored by an ordinary positive
integer.

Route map v0.9 carries the same verdict and the same missing condition. The
bundle's two re-shipped Phase I files (the closure and 03A5) are byte-identical to
item 30's copies, so RUN-012 carries over; exactly two files are new.

---

## Four findings about my own checks

**Six checks had no defect naming them.** RUN-012 ended by noting that a drill
count says nothing about a check nothing points at, so this run audits that
before running: every check name must appear as some defect's target, and every
target must name a real check. The first audit found **six** unguarded checks —
cylinder nesting, arbitrary-code realization, the singular mass bound,
mechanical subcriticality, the two-symbol alphabet, and the cylinder-integer
check. Each got a defect. The audit costs one script and would have been worth
running from RUN-005.

**A one-place shift in the anchor cocycle passed.** Dropping the first lift
digit shifts the settling index by one, and the check did not notice, because on
a settled orbit `r_{s+1} = r_s = n` — asserting the source at *one step past* the
settling point is insensitive to where that point is. The assertion is now sharp:
the source must already equal `n` **at** the settling point. That is what pins the
index, and it is the difference between measuring "it settles" and measuring
"it settles here" — and the whole finding above is about *where*.

**A constant offset telescoped away — the same cancellation as RUN-011.**
"`floor_beta` rounds up" looked like a clean defect. It is a no-op: `floor_beta`
enters the mechanical code only as a *difference* `⌊βm⌋ − ⌊β(m−1)⌋`, so any
constant offset cancels, and `K*_m` is unchanged. RUN-011 retired a defect for
exactly this reason (a constant shift in the Sturmian credit is invisible to a
recurrence built from differences). Two instances now, so it is a class, not an
instance: **where a quantity appears only inside a difference, constant-offset
mutations there are structurally dead.** Replaced with a change of base, which
survives telescoping.

**Weakening a requirement is not a defect — third time.** Dropping "Collatz"
from the list of terms the unproved ledger must contain only makes the check ask
for less, and the real document satisfies both versions. Replaced by reading the
*proved* section instead of the unproved one, which moves the answer because that
list names none of the four. Same family as the `<`/`<=` no-ops and the widened
threshold in RUN-012; the reliable form is to damage what is computed, not what
it is compared against.

---

## What this does not establish

Nothing on §32's unproved list. The invariant-limit theorem itself is a statement
about weak-\* limits over an infinite orbit and is not finitely checkable — what
is checked here is the finite arithmetic it rests on (the mass bound on real
spines, the clopen structure of the singular cylinders, and the identity
`g_R = min(q−1, R−1)` that makes the truncated observable continuous). The
separation measured above is a statement about seven integers and 60 code steps.
It shows the cocycle *can* distinguish; it does not show that critical occupancy
forces nonzero lifts, which is §32's unproved item 2 and the actual A-U.2 target.
