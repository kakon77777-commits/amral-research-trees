# Early experiments — Neo.K

**Author: Neo.K.** Prototype bundles and benchmarks produced alongside the
Operation Translation Series, archived here byte-exact as they were.

These predate or run beside the nine-paper series and are **not** load-bearing for
it. The series itself says so: Paper 01 files representation-dependent
descriptions under evidence class `S`, and Paper 02 §28 states plainly that an
exact certificate need not depend on a floating logarithm. So reading these as
early experiments rather than results is the series' own position, not a demotion
applied here.

They are archived because the working record is part of the research, not
scaffolding around it — the process is the result, and a relay needs the whole
trail, including the routes that were later replaced.

| Item | Date | What it is | Status |
|---|---|---|---|
| `finite_collatz_additive_coordinate_mvp_bundle.zip` | 08-10 15:08 | Log-coordinate encoding where the Collatz branches become additive, with an exact finite-domain recovery criterion | **rechecked** — [`src01`](../../collatz-verification-zhuiheng/data/gate-logs/src01-additive-coordinate-recheck.json), 7/7 |
| `dimension_aware_log_physics_stress_bundle.zip` | 08-10 15:15 | The same coordinate carried off Collatz entirely: SI dimension vectors plus log magnitude, stress-tested on real physics | **rechecked** — [`src02`](../../collatz-verification-zhuiheng/data/gate-logs/src02-log-physics-recheck.json), 10/10 |
| `collatz_operation_translation_finite_verification_prototype.zip` | 08-10 22:07 | The finite verification prototype: the `k`-block identity, and a table of 58,651 cylinder certificates | **rechecked** — [`src03`](../../collatz-verification-zhuiheng/data/gate-logs/src03-finite-prototype-recheck.json) 11/11, plus a [scaling cross-check](../../collatz-verification-zhuiheng/data/gate-logs/src03-scaling-crosscheck.json) |
| `collatz_ot_v3_threshold_benchmark.csv` | 08-10 22:16 | The k-sweep: `k ∈ {8,12,16,18,20}` at three domain sizes | **rechecked** — [`src04`](../../collatz-verification-zhuiheng/data/gate-logs/src04-v3-threshold-recheck.json), 8/8 |
| `collatz_operation_translation_v3_threshold_bundle.zip` | 08-10 22:16 | The descent test compiled to a residue-indexed integer threshold | **rechecked** — same log |

Presence in this directory is **not** a verification claim — that is the
repository protocol's rule, and worth restating wherever a status column could be
misread. Where an item is marked *archived only*, the bytes are here and hashed
against the source manifest and nothing has been checked about their contents.

## What item 01 establishes, stated at its actual strength

On `{1..N}` the branches are exactly additive in log coordinates:

```
even:  L' = L − ln 2
odd:   L' = L + ln 3 + δ_n ,   δ_n = ln(1 + 1/(3n))
```

and nearest-integer decoding is exactly recoverable whenever the log-coordinate
error stays below `ln(1 + 1/(2N))`.

The recheck confirms all of it, and adds two things the bundle does not say:

- The odd-branch identity is **exact over the rationals** — `3n·(1 + 1/(3n)) = 3n+1`
  — so it needs no floating point at all. The bundle verifies it at 80 decimal
  digits; the identity is better than that.
- The recovery margin is **tight, not merely sufficient**. `N·(e^ε − 1)` equals
  exactly `1/2` at `ε = ln(1 + 1/(2N))`, so the stated bound *is* the failure
  threshold for the worst state `m = N`, and decoding does fail just past it.
  Calling it only "a sufficient condition" would understate it.

And what it does not give: nothing about unbounded `n`. The margin shrinks like
`1/(2N)`, so the precision needed to keep decoding exact grows without bound as
the domain does. It is a finite-domain representation result, which is how the
bundle presents it.

## Item 02 — a branch, not a continuation

Seven minutes after item 01, and its subject is **no longer Collatz**. It keeps
the same representation — magnitude as a logarithm, so products become sums — and
adds an SI dimension vector, then stress-tests the pair on sphere volume, pendulum
period, the quantum phase-space cell, Stefan–Boltzmann, blackbody flux,
relativistic energy, and the Lorentz factor at `β = 1 − 10⁻⁴⁰`.

All 10 checks pass. Three of them are worth naming, because the recheck reaches
them by routes the bundle does not use:

- **Stefan–Boltzmann is an external anchor, not a self-comparison.** Since the
  2019 SI revision `k_B`, `h` and `c` are *exact defined constants*, so
  `σ = 2π⁵k_B⁴/(15h³c²)` is exactly determined and CODATA's digits are an
  expectation nobody here authored. Computed `5.670374419184429453970996732E-8`
  against CODATA `…731E-8`, relative difference `1.6E-28`.
- **The `(2πħ)³ = h³` cancellation is exact, not numerical.** With `ħ = h/(2π)`
  no `π` survives at all, so the bundle's demonstration at 120 digits is
  confirming an identity.
- **The Lorentz case has a cancellation-free route.** `1 − β² = (1−β)(1+β)` needs
  no log-difference trick whatsoever — only enough precision to hold `10⁻⁴⁰`. It
  reproduces the bundle's `7.0710678118654752440084436210E+19` to `7E-30`, which
  means the two methods genuinely agree rather than one method agreeing with
  itself. And `1.0 − 1e−40 == 1.0` in binary64, exactly as claimed.

### Where it sits in the line

This is **the road not taken**. Item 01 put log coordinates on Collatz; item 02
carried the same coordinate to dimensional physics. The nine-paper series then
goes the *other* way entirely — exact affine operators over the integers, with
Paper 02 §28 stating outright that an exact certificate need not depend on a
floating logarithm.

So this branch is not an ancestor of the series' method. It is kept because it
shows the alternative was actually tried, and how far it genuinely goes: quite
far, and exactly reproducibly, which is why abandoning it was a choice rather
than a retreat.

## Item 03 — the ancestor of this arm's engine

Items 01 and 02 were representation experiments the series later set aside. **This
one is different.** It states the block identity

```
T^k(r + a·2^k) = T^k(r) + a·3^s
```

that the verification engine's congruence sieve is built on, picks `k = 16`, and
reports 938,413 bulk-certified values on `[1, 2^20)` — the same figure Paper 05
and Paper 09 §24 later carry.

And it ships a **dataset**, not just a claim: 58,651 cylinder certificates, one
per contracting residue, each with its own descent threshold. That is the best
thing anyone can hand a verification arm, because every row can be confronted
with direct iteration instead of trusted.

**11/11 checks pass, every row verified.** Base values, odd-step counts,
multipliers and domain bounds all reproduce under direct iteration; the table
holds exactly the contracting residues; its size is exactly Paper 05's
`A₁₆ = 58651`; and the reported rule counts at `k = 8, 10, 12, 14` — 219, 848,
3302, 12911 — all follow the same binomial law.

The thresholds are **exact, not merely safe**: `a_min` equals
`⌊(T^k(r) − r)/(2^k − 3^s)⌋ + 1` clamped to the domain floor, on all 58,651 rows.

### A weakness in my own check, caught and fixed

The first version tested threshold exactness by probing `a_min − 1` directly. That
point only lands inside the positive domain for **2 of the 58,651 rows** — so the
check passed on two observations and would have read as though it had verified all
of them. It now derives the threshold independently for every row and compares,
with those 2 rows still probed by iteration so the derivation stays anchored to
something outside itself.

### Scaling, against a separate implementation

The bundle's scaling table was cross-checked with this arm's Rust engine:

| | certified | fallback | prune ratio |
|---|---|---|---|
| `2^20` | 938,413 ✓ | 110,161 ✓ | `0.8949420832482972` ✓ |
| `2^22` | 3,753,661 ✓ | 440,641 ✓ | `0.8949429487910027` ✓ |
| `2^24` | 15,014,653 ✓ | 1,762,561 ✓ | `0.8949431651762921` ✓ |

Every column, to sixteen decimal places.

That agreement needed one thing resolved first. The ratios disagreed in the 7th
decimal until the denominators were compared: the bundle's is `2^e − 2`, one short
of the `2^e − 1` integers in `[1, 2^e)`. The missing value is `n = 1` — the
terminal state, which needs no verification — so the bundle's domain is `[2, 2^e)`.
Excluding `n = 1` reconciles every column exactly. Neither side was wrong; the
domains were stated differently, and that is the sort of thing worth pinning down
rather than rounding away.

### What it does and does not give

It is a **finite-range accelerator**, and the bundle says so itself: *"not a proof
of the Collatz conjecture."* Certifying 89.494% of a range faster leaves the rest
to explicit iteration and says nothing beyond the range.

Its relation to this arm's engine is direct ancestry, with one difference worth
recording: the engine uses the `k`-step jump **only as a filter** and re-walks from
`n` whenever it does not settle the question, because a trajectory can dip below
`n` and rise again inside the first `k` steps. The prototype's certificates avoid
that issue by only ever claiming descent *at* the `k`-th step — a narrower claim,
and a sound one.

## Items 04–05 — the k-sweep, and why bigger k is not better

Nine minutes after item 03. The descent test is compiled into a residue-indexed
integer threshold — the hot loop becomes a mask, a shift, a lookup and one integer
comparison — and `k` is swept over `{8, 12, 16, 18, 20}` at three domain sizes.

**8/8 checks pass**, including all **15 `(k, domain)` pairs cross-checked against
this arm's Rust engine**, a separate implementation. Every `certified` and
`fallback` count matches exactly, every prune ratio equals `certified/total`
exactly, and every domain total is `2^e − 2` on the `[2, 2^e)` convention.

### The prune ratio is not monotone in `k`

| `k` | measured at `2^24` | Paper 05's `P_k = A_k/2^k` | `⌊αk⌋` |
|---|---|---|---|
| 8 | 0.855468375 | 0.855468750 | 5 |
| 12 | 0.806152261 | 0.806152344 | 7 |
| **16** | **0.894943165** | **0.894943237** | **10** |
| 18 | 0.881057665 | 0.881057739 | 11 |
| 20 | 0.868411943 | 0.868412018 | 12 |

It rises to `k = 16`, then **falls** at 18 and 20. That is not noise and not a
defect — the measured ratios *are* Paper 05's cylinder density, agreeing to about
`7×10⁻⁸`, with the residual being the finite-domain boundary correction that
shrinks as the domain grows (verified).

The mechanism is the staircase. `P_k = P(Bin(k,½) ≤ ⌊αk⌋)` with `α = ln2/ln3 ≈
0.63093`, and `⌊αk⌋` advances by 0 or 1 per step, so the *ratio* `⌊αk⌋/k` moves:
`10/16 = 0.625`, `11/18 = 0.611`, `12/20 = 0.600`. It drifts further below `α` as
`k` goes 16 → 20, and the prune ratio drops with it. `P_k → 1` only in the limit,
and not from below at every step.

**Practical consequence worth stating plainly:** choosing a larger `k` costs more
table-build time *and* can give a worse prune ratio. `k = 16` is a favourable step
of that staircase.

### Reading the bundle's "best configuration" precisely

The README says *"Best measured configuration at `n < 2^24`: k = 18, prune ratio =
88.106%"*. Both numbers are correct on the bundle's own data — `k = 18` **is** best
by amortized speedup, and 88.106% **is** its prune ratio.

But `k = 16` has the better prune **ratio**, 89.494%. The two are claims about
different quantities, and the README places the `k = 18` ratio directly beside the
word "best", where it can be read as claiming that too. Separating them costs
nothing and prevents the misreading.

### Not reproduced

Every timing column. They are machine-specific, and no check here depends on one.
