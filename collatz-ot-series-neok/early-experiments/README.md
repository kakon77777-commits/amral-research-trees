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
