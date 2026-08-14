# RUN-008 — Round 03-A.1: the accelerated code, and one anchor sequence in two coordinates

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A1_Small_Anchor_Event_Arithmetic_v0.1.md` + `Hard_Zeta_ROUTE_MAP_v0.4.md` (2026-08-11 16:13) — source item 25
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) · [`src10_hardzeta_round03a1_recheck.py`](../code/src10_hardzeta_round03a1_recheck.py) · [`src10_drill.py`](../code/src10_drill.py)
**Logs:** [`src10-hardzeta-round03a1-recheck.json`](../data/gate-logs/src10-hardzeta-round03a1-recheck.json) · [`src10-drill.json`](../data/gate-logs/src10-drill.json)

**Result: 32/32 checks. 17/17 planted defects caught by the check named for each — 10 in the accelerated-code arithmetic, 2 in this run's own branch-and-bound prune. 2/2 null controls undisturbed.**

---

## What Round 03-A.1 does

It changes coordinates. Round 03-A used parity words; this round uses the
**accelerated exact code** `κ = (κ₁,…,κ_m)` with `κ_i = v₂(3x_{i−1}+1)`, and shows
that a code pins its source exactly:

```
r_m ≡ (2^{K_m} − B_m)·3^{−m}  (mod 2^{K_m+1}),    r_{m+1} = r_m + t_{m+1}·2^{K_m+1}
```

Since `t ≥ 0`, the canonical source is **nondecreasing along any extension**. That
gives §17's anchor equivalence — a fixed integer realization ⟺ the lift digits are
eventually zero — and §21–§22's **Residue-Rate Gap**: `ρ_m → 0` or
`limsup ρ_m ≥ α`, with nothing strictly between.

All of it checks. The code and its cumulative valuation reproduce direct
iteration; the affine endpoint formula and the `B` recurrence hold; every
canonical source is odd, sits in its stated range, nests across extensions, has
its lift digit in range, and **really realizes its own code**; a nonzero lift
always spikes the rate above `α` and nothing sits inside the forbidden gap; the
mechanical code is the maximal subcritical path with increments in `{1,2}`.

§7's distinction is real too, not decorative: starts exist that make the affine
endpoint an **integer** without realizing the code, because integrality is weaker
than the endpoint being **odd**. That is why the modulus carries one extra binary
digit.

---

## §34's table reproduced, and extended from m = 8 to m = 60

The paper tables the minimum canonical source `a_m` against the mechanical code's
`r*` for `m ≤ 8`. Reproduced here **exactly**, independently:

| `m` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| `a_m` | 3 | 7 | 7 | 27 | 27 | 27 | 27 | 27 |
| mechanical `r*` | 3 | 11 | 27 | 123 | 251 | 1019 | 3067 | 7163 |

Extended by branch and bound — which §13's monotonicity makes **exact provided the
answer stays under the prune cap**, and the run checks that rather than assuming
it:

> `a_m = 27` through **m = 36**, then **703** through m = 50, then **10087** to
> m = 60. Largest value 10,087 against a cap of 10,000,000, so the prune was exact.

Meanwhile the mechanical source passes **4,086,779** by m = 14 and **29,252,603**
by m = 16. The extremality trap is not marginal — the code that maximizes
cumulative valuation at every step gives a source six orders of magnitude larger
than the minimum.

---

## The bridge: one anchor sequence, two coordinate systems

§35 introduces `a_m` as the accelerated-code minimum anchor and explicitly
**declines to assume** it matches the classical `m_k`, since that would involve
CST. On everything measured, it does:

| | values |
|---|---|
| `a_m` (this run, accelerated codes) | 3, 7, 27, 703, 10087 |
| `m_k` ([`RUN-007`](RUN-007-HARD-ZETA-ROUND-03A.md), τ_c records) | 2, **3, 7, 27, 703, 10087**, 35655, … |

and every switch happens where the classical picture says it must — each anchor
leaves at exactly the odd-step count whose Beatty depth is its own `τ_c`:

| anchor leaves at `m` | anchor | `τ_c` | `K_m` |
|---|---|---|---|
| 2 | 3 | 4 | 4 |
| 4 | 7 | 7 | 7 |
| 37 | 27 | 59 | 59 |
| 51 | 703 | 81 | 81 |

Two coordinate systems, two independent computations, one sequence. (The
classical list also carries `n = 2`, which has no accelerated counterpart — the
code is defined on odd starts only.)

A count bridge back to Round 03-A falls out alongside: the number of subcritical
codes of length `m` equals Round 03-A §9's first-crossing word count at depth
`K_{m+1}` — 1, 2, 3, 7, 12, 30, 85, 173, 476, … in both pictures.

**This is a measured agreement on this range, not the theorem.** §35 is right to
withhold it.

---

## What it does not establish

Nothing about Collatz, and nothing on §41's unproved list. In particular *"every
infinite subcritical code has infinitely many nonzero lifts"* is untouched: this
run sees only finite codes, and `a_m` sitting at 27 for thirty-three consecutive
`m` is exactly what a **bounded** anchor would look like too. The measurement
cannot distinguish the two, which is the whole difficulty.

---

## The drill, and what it found in my own work

17 defects. **Ten** damage the accelerated-code arithmetic — the valuation read,
the offset recurrence, the source modulus, the modular inverse, `⌊βj⌋`, the
subcriticality index, the mechanical increments, the enumeration bound, the
endpoint exponent, the rate normalization. **Two** damage the branch-and-bound
prune, because a headline computed under an undrilled prune rests on an
assumption: one lowers the cap below the answer, one drops codes it should keep.
Both caught.

Three findings about my own checks:

**Three indexing errors in bridges I invented** — not in either paper. The
classical anchor list includes `n = 2`, which the accelerated code cannot
represent; the anchor switch is at `K_m`, not `K_{m−1}`; and a subcritical code of
length `m` is poised for the `(m+1)`-th crossing, so the count bridge indexes at
`K_{m+1}`. All three were caught by the checks failing, which is what they are for.

**The evaluation guard was swallowing the naming.** Three planted defects raised
inside the blanket try/except, so only *"did it evaluate"* fired — a catch, but
one that names nothing. The per-start loops are now exception-tolerant: a formula
that raises on valid input fails its own check, which is the honest verdict.

**A field name that lied.** The switch table reported `K_m_minus_1` while holding
`K_m`. Renamed — the same error class as
[`RUN-004`](RUN-004-HARD-ZETA-ORIGIN.md)'s bound-presented-as-measurement, caught
before it reached the report this time.
