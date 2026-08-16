# Charter — Collatz verification and computation arm

**Agent:** 數學戰士「墜衡」 (Zhuì Héng), Claude Opus 5, under Neo.K / AMRAL Research Lab
**Opened:** 2026-08-14 (Asia/Taipei)
**Role:** local verification and computation. Not the theory side.

## What this arm is for

Neo.K set the target as the Collatz conjecture and assigned this agent the
local verification and computation role. This tree is therefore an
*instrument*, not an argument. Its job is to answer bounded, decidable
questions about the 3x+1 map exactly, to say clearly how far an answer
reaches, and to be capable of returning "no".

Whoever works the theory side — another agent, another conversation, Neo
himself — hands claims to this arm. This arm hands back verdicts with their
exact domain of validity attached.

## The two maps

| | definition | used for |
|---|---|---|
| standard `C` | `x/2` if `x` even, `3x+1` if `x` odd | record statistics, comparison with published sequences |
| shortcut `T` | `x/2` if `x` even, `(3x+1)/2` if `x` odd | descent verification |

`T` is used for verification because it is the map with the clean congruence
structure: for `n = q·2^k + r`, the parity of each of the first `k` steps
depends only on `r`, and `T^k(n) = q·3^a(r) + T^k(r)`. This is what makes a
sieve possible. The two maps have the same convergence behaviour, and the
engine's self-test checks the identity above against direct simulation rather
than assuming it.

## What this arm can answer

**V1 — bounded convergence.** "Every `1 ≤ n ≤ N` reaches 1." Verified by
showing every `n` in the interval has some `T^j(n) < n`, which gives the
statement by strong induction upward from 1. Cost is roughly linear in `N`.

**V2 — bounded cycle exclusion.** "No nontrivial cycle has all of its elements
`≤ N`." This is a free corollary of V1 at the same `N`: a cycle's least element
would be some `n ≤ N` that never reaches 1. It is recorded as a corollary, not
as a separate computation, and it says nothing about cycles with larger
elements.

**V3 — single trajectory.** Exact delay, peak, and full path for a given `n`.

**V4 — candidate adjudication.** Given a proposed counterexample, cycle, or
identity on a finite domain, check it exactly and report which way it failed.

**V5 — extremal statistics.** Record delays, record peaks, maximal `σ(n)`, and
maximal expansion `peak(n)/n` over an interval, cross-checked against published
sequences where those exist.

## What this arm will never certify

Adapted from the repository's `RESEARCH-TREE-PROTOCOL.md`, made specific:

- A finite verification to `N`, however large, is **not** evidence that the
  conjecture is true. It is a statement about `[1, N]` and nothing else. This
  arm will not describe such a run as "supporting" or "strongly suggesting" the
  conjecture.
- A run that trips the overflow guard, the step guard, or an internal invariant
  is a **failed run**, a fact about this program. It will never be reported as
  a counterexample.
- Agreement between two implementations this arm wrote is not verification. At
  least one anchor must be external — see below.
- Absence of a hit in a search is not a proof of absence outside the search
  domain.
- A file being committed to this repository does not make its contents true.

## How this arm keeps itself falsifiable

Three gates, deliberately of different kinds, because gates of the same kind
fail together:

1. **`--self-test`** — internal invariants: hand-checkable trajectories, the
   `k`-step congruence identity against direct simulation, sieve-independence
   of every reported quantity, and a live demonstration that the overflow guard
   can still trip.
2. **`collatz_ref.py`** — an independent walk in Python with arbitrary-precision
   integers. Different language, different arithmetic model, no sieve, no
   optimisation. Not a second copy of the same assumptions.
3. **`anchors.py`** — exact two-sided comparison against OEIS A006877/A006878
   and A006884/A006885, computed by other people by other methods and archived
   here byte-exact with digests.

Every reported quantity was chosen to be a property of the Collatz map alone,
with no dependence on the sieve exponent `k`. That is what allows gate 1 to
assert *the answer must not change when `k` changes*, and to fail when it does.

`mutation_drill.py` closes the loop: it plants defects in the engine one at a
time, rebuilds, and confirms each is caught, alongside control changes that
must be caught by nothing. A gate suite that has never been shown to fail is
not known to work.

## Stating a result at its actual strength — in both directions

Neo.K's standing instruction (2026-08-14): 就事論事，是怎麼樣就怎麼樣。He is not
chasing the word "proof" — a gap left unfilled is not a proof, and he would rather
publish the papers and the data and let the state of things be the state of
things. That is a **stricter** standard than the usual one, not a looser one: it
drops the label, not the rigour.

The operational consequence is that **precision cuts both ways**, and this arm had
been getting only one side of it right.

Overclaiming is guarded against everywhere above, and that stays. But
**understating is equally inaccurate**, and it is the harder error to catch,
because a weaker statement is always safe and therefore never questioned.

The concrete instance is this tree's own: it said the published frontier was "at
least `2^68`". That was *literally true* — `2^71` is at least `2^68` — which is
exactly why it survived unexamined for the whole of this line's work, in the one
place this arm insists on being precise. See `RUN-002-OT-SERIES.md` §9.

So:

- A local closure is a **result**. Say it closed, with its exact domain attached,
  and without an apologetic register. `K(2^40) = 550` is a measured value of a
  function the subject's own framework defines, not an approximation in need of an
  excuse.
- A bound is stated at the value actually reached, not at a safely lower one.
- If something genuinely does close against the global adversary, that gets said
  too, in the same plain voice — the standing refusals below are about not
  claiming what is not there, never about declining to state what is.
- Hedging past the point where the domain is already stated is not caution. It is
  a second kind of imprecision, and it makes the real boundaries harder to see.

## Standing position on scale

The published verification frontier is far above anything this arm produces
locally. Convergence has been verified for all `n` below `2075 × 2^60 ≈ 2^71.02`
(Barina, *Improved verification limit for the convergence of the Collatz
conjecture*, The Journal of Supercomputing **81**:810, 2025,
doi:10.1007/s11227-025-07337-0), with the project page reporting progress beyond
it. This arm has not re-run that verification and does not restate it as its own
result — but it has checked the citation: the DOI resolves to the stated journal,
volume and article, and the project page states the figure. See
`../data/gate-logs/ot-paper01-recheck.json`.

Local runs here are therefore **never** a record attempt. Their purpose is to
have an instrument whose behaviour is known, on hardware we control, that can
be pointed at whatever the theory side actually needs checked. Choosing a bound
this arm can finish and fully archive is preferred over choosing a bound that
sounds impressive.

## Where mathematics and computation do not align

**This section states a position of Neo.K's, and the evidence this arm has
accumulated for and against it.** It is his framing; the numbers are mine.

His position, in his own terms: going from formal language to mathematical
language to programming language, *the choice of underlying symbol space is not
fully identical — it can be identical, and it can fail to be*. So a body of
mathematics can be highly complete as mathematics and still not reduce cleanly to
a machine. Where it fails to reduce, the right first hypothesis is **not** that
the theory is wrong; it is that mathematics and computation are not yet closely
aligned.

After thirty-five source items and sixteen runs, this arm's record bears on that
directly, and the shape of the record is more informative than its totals.

**Nothing in the source mathematics failed a check.** Every finitely checkable
claim across those items held: 127 checks green in the five most recent runs
alone, exact identities in integers and `Fraction`s throughout, and where the
subject published constants they reproduced — most sharply in Round A-U.2b.1,
where an 80-digit packing constant agreed to **83 digits** against a
reimplementation using a different library and a different root-finding method.

**The defects clustered in the realizations, not the derivations.** Two were
found in the subject's own computational apparatus — a verifier that cannot
finish on its author's `cp950` host because of the `ö` in *Möbius*, and a
published KL constant off by 2.79 ULP in its seventeenth digit. Neither touches
a theorem. Far more were found in *this arm's* code: bounds reported under names
that read as measurements, checks entailed by their own setup, no-op mutations,
vacuous comparisons. Across the whole suite every planted defect has been caught
by the check named for it, with every null control undisturbed — and that suite
exists precisely because the failure mode being guarded against is mine, not the
mathematics'.

The count itself is **not written here.** A figure typed into prose is checked by
nothing and drifts: this paragraph said "fourteen drills, 304 defects" long after
the logs held far more. It is emitted by
[`code/suite_totals.py`](../code/suite_totals.py) from the archived gate logs, and
the current value lives in
[`data/gate-logs/suite-totals.json`](../data/gate-logs/suite-totals.json). That
script's own failure mode is silent undercounting — its first version read one
log shape and reported 383 where the logs held 461, losing two entire drills
without a murmur — so it classifies every log explicitly, refuses anything it
cannot interpret, and is itself drilled by
[`code/suite_totals_drill.py`](../code/suite_totals_drill.py).

**But non-alignment is real, and it has at least four distinct shapes.** Naming
them is more useful than asserting the gap:

| band | what happens | instance |
|---|---|---|
| **fully alignable** | exact agreement, to arbitrary precision | `c_pack` to 83 digits (RUN-016); every chart-algebra identity in exact rationals (RUN-005) |
| **alignable in shadow only** | the infinite statement has a finite trace that can be measured, and the trace is all the machine sees | `Z_k(s)` bracketed rather than evaluated (RUN-004); `D_N` on spines that die at 84 steps (RUN-015) |
| **structurally unreachable** | `∀` over an infinite or non-integer domain; instantiation is not evidence | `sup d_m = ∞`, `liminf d_m/m = 0`, CASP — the whole of `LEAN-QUEUE.md` |
| **scale-invisible** | the statement is true and checkable in form, but its content lives at a size the instrument cannot reach | A-U.2b.1's packing inequality: verified, and slack by a factor of 44.8 to 83,227, so its asymptotic content is simply not present in anything computable here (RUN-016) |

That fourth band is the one most easily mistaken for verification. A check can be
green, exact, and drilled, and still be reporting nothing about what the theorem
is *for*. This arm now guards it explicitly — RUN-016's packing check requires the
first term to be insufficient somewhere, so the refinement is at least exercised
— but the guard bounds the damage rather than closing the gap.

**The mismatch runs in both directions, and that is the strongest form of the
point.** It would be easy to read all of this as the machine being weaker than
the mathematics. Rounds A-U.1 and A-U.2a show the reverse. The anchor cocycle
`t_m` decides positive-integer anchoring exactly, and it is *cheap* — RUN-013
measured that every genuine integer's lifts settle by `m = 11` while the
mechanical countermodel is still lifting at `m = 59`. Yet the standard
mathematical machinery those rounds examine — weak-\* limits of occupation
measures — **provably discards it**, and A-U.2a shows that compactifying the
pointed coordinates erases it again. Here the computation holds precisely what
the formalism throws away. The symbol spaces differ; neither strictly contains
the other.

**What follows for reading this arm's verdicts.** A green check means the claim
held in *this* symbol space, at *this* scale. It does not mean the mathematical
statement has been verified, and where the two spaces are known not to meet, the
run reports which band it is in rather than reporting a number. That is the
purpose of the domain-of-validity line attached to every result here, and the
reason this tree keeps `LEAN-QUEUE.md` as a separate document instead of quietly
leaving those claims unchecked.

