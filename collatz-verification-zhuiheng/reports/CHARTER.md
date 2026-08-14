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

## Standing position on scale

The published verification frontier is far above anything this arm produces
locally. Convergence has been verified to at least `2^68` (Barina, *Convergence
verification of the Collatz problem*, The Journal of Supercomputing, 2021),
with the distributed effort reporting further progress since. This arm has not
independently checked that literature claim and does not restate it as its own.

Local runs here are therefore **never** a record attempt. Their purpose is to
have an instrument whose behaviour is known, on hardware we control, that can
be pointed at whatever the theory side actually needs checked. Choosing a bound
this arm can finish and fully archive is preferred over choosing a bound that
sounds impressive.
