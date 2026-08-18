# FELRA on the anchor cocycle

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Tool:** FELRA 1.3.0 · [`project.yaml`](./project.yaml) · [`artifacts/`](./artifacts)

The first time this arm drives [FELRA](https://github.com/kakon77777-commits/FELRA)
rather than writing a one-off gate. It asks one question that
[RUN-022](../reports/RUN-022-HARD-ZETA-AU2E1-RESET-BLOCK.md) implies but does not
answer.

## The question

RUN-022 verified Round A-U.2e.1's renormalized anchor identity in **exact rational
arithmetic**, and said so. That was a deliberate choice. What it did not say is
what the choice bought.

On the all-ones spine — `n = 2^(m+1) − 1`, every accelerated valuation `1`, so
`K_m = m` — the anchor has a closed form:

    A_m − n  =  1 − (2/3)^m

exactly rational at every `m`, and strictly less than 1 at every `m`. The round's
own reading is that the faithful renormalized height **only ever increases by
correction mass**, so the gap is positive forever.

## The measurement

| `m` | `A_m − n` in float64 |
| --- | --- |
| 92 | `0.9999999999999999` |
| **93** | **`1.0`** |
| 150 | `1.0` |

**From `m = 93` onward a float64 computation reports the correction mass as
exhausted.** The true gap at `m = 93` is `4.203e-17` and never reaches zero. The
run says `inconsistent` at zero tolerance, which is the correct verdict: float64
and the exact value are not the same number.

Decimal at 40 digits still sees the gap past that horizon, agreeing with the exact
value to `3.6e-41`. So the horizon is a property of the **representation**, not of
the problem, and avoiding it is cheap.

None of this is a defect in the round. It is a statement about what a
reimplementation would report: any float64 anchor cocycle beyond ~93 steps of this
spine says the height has stopped increasing, when it has not. RUN-022 used exact
rationals and is unaffected — this quantifies why that mattered rather than
asserting it.

## The universally quantified half

The horizon is a fact about arithmetic at sampled points. The statement *for every
m* lives in Lean, and the same project checks it: `lean_all_ones_spine` runs
`Collatz/AllOnes.lean` from the [`collatz-lean`](https://github.com/kakon77777-commits/collatz-lean)
development through FELRA's `formal_check` backend — **`verified`**, Lake
5.0.0-src+d8b1897 / Lean 4.33.0, with the checker's identity and the obligation's
hash recorded in the manifest.

The evidence ladder ends at `executed`, with `formally_proved: pass` recorded
above it. It does **not** report a higher level, because the ladder is cumulative
and the rungs between are not run: a Lean proof sitting above an unrun precision
check does not raise the level. That is the ladder behaving correctly, and it is
worth more than a number that flatters the run.

## Three defects this found in FELRA itself

Driving a tool against work somebody cares about is not the same as driving it
against a demonstration built to suit it. All three were fixed in the FELRA repo
(commit `829b819`), and none was reachable from FELRA's own examples.

1. **`decimal_prec` governed only the input conversion.** Arithmetic ran at
   Python's default 28 digits however many the project declared. Found by getting
   `4e-29` from the tool where the same computation by hand at 40 digits gave
   `2e-41`.
2. **A declared `tolerance` below `1e-30` was silently collapsed to zero** by a
   `limit_denominator` that served no purpose. A project asking for `1e-38` was
   given a strict exact comparison it never requested.
3. **`falsified` was driven by `not run.passed`**, conflating "an analysis did not
   meet its declared expectation" with "the claim was refuted". A deliberate
   representation disagreement was reporting the evidence ladder as `falsified` —
   a verdict on the mathematics that the run never reached.

The first two are the same shape: **a declared parameter that was not honoured**,
which is the failure this package exists to catch, sitting inside the package.

## Reproducing

```bash
export LEAN_PROJECT="D:/Ai/work together/lean/collatz"
felra run felra/project.yaml --output felra/artifacts
```

`lean_all_ones_spine` reports `unavailable` rather than failing if Lean is not
installed — a checker that did not run is never a pass.
