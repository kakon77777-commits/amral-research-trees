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

| Item | Date | What it is | Independent recheck |
|---|---|---|---|
| `finite_collatz_additive_coordinate_mvp_bundle.zip` | 2026-08-10 15:08 | Log-coordinate encoding where the Collatz branches become additive, with a precomputable per-state correction and an exact finite-domain recovery criterion | [`src01-additive-coordinate-recheck.json`](../../collatz-verification-zhuiheng/data/gate-logs/src01-additive-coordinate-recheck.json) |
| `dimension_aware_log_physics_stress_bundle.zip` | 2026-08-10 15:15 | The same coordinate carried off Collatz entirely: SI dimension vectors plus log magnitude, stress-tested on real physics formulas including severe cancellation | [`src02-log-physics-recheck.json`](../../collatz-verification-zhuiheng/data/gate-logs/src02-log-physics-recheck.json) |

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
