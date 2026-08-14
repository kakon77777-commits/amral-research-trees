# RUN-006 — Hard-Zeta Round 02: the two compartments, and Terras by word

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_02_Atomic_Hazard_Coefficient_Correction_v0.1.md`, `Hard_Zeta_ROUTE_MAP_v0.2.md`, and their bundle (2026-08-11 13:27) — source items 21–23
**Tools:** [`hz_chart_algebra.py`](../code/hz_chart_algebra.py) (Round 02 layer) · [`src08_hardzeta_round02_recheck.py`](../code/src08_hardzeta_round02_recheck.py) · [`src08_drill.py`](../code/src08_drill.py)
**Logs:** [`src08-hardzeta-round02-recheck.json`](../data/gate-logs/src08-hardzeta-round02-recheck.json) · [`src08-drill.json`](../data/gate-logs/src08-drill.json)

**Result: 23/23 checks. 14/14 planted defects caught by the check named for each — 8 of them in Round 02's own formulas. 2/2 null controls undisturbed.**

---

## What Round 02 does

Three things, in rising order of consequence.

1. It restates Round 01's thresholds in the parent's **quotient coordinate** `a`
   (where `n = r_w + 2^k a`), giving `q_D` and `q_U`. Different formulas for the
   same boundary — so the two rounds can be confronted with each other.
2. §6 replaces "worst chart" with an exact **mass-weighted** identity
   `λ_k = Σ_{|w|=k} π_w ℓ_w`.
3. §10–§20 split the frontier in two. With `τ_c(n) = inf{ j : 3^{u_j(n)} < 2^j }`
   and the unconditional `τ_c ≤ σ`,

   ```
   E_k = C_k ⊔ R_k,   C_k = {τ_c > k},   R_k = {τ_c ≤ k < σ},   Z_k = C_k + R_k
   ```

   The `R` compartment **is** the Terras coefficient-stopping conjecture, and §17
   recasts it as a finite-word inequality.

All of it checks. `q_D`/`q_U` select exactly Round 01's boundary on all 8,190
charts; §7's `β_k` zones agree with Round 01's power comparison on every chart;
§5's parity-restricted sums reproduce Round 01's chart masses; the two-compartment
mass dynamics hold at every level.

---

## §6 is right, and by a wide margin

Round 01's No-Go was about the **worst chart**. §22 there already said that was
the wrong object, and §6 here says what the right one is. The measurement makes
the gap concrete:

| depth `k` | charts | global `λ_k` | worst chart's `ℓ_w` | ratio |
|---|---|---|---|---|
| 6 | 10 | 0.825141 | 0.987820 | 1.2× |
| 9 | 52 | 0.014274 | 0.853184 | 60× |
| 11 | 184 | 0.010520 | 0.987126 | 94× |
| 12 | 323 | 0.025145 | 0.997525 | 40× |

At depth 12 the worst chart loses **99.75%** of its mass while the global hazard
is **2.5%**. Reading the worst chart as the global rate overstates it by a factor
of forty, and that is precisely why Round 01's per-chart No-Go does not close the
programme.

§9's companion point is common rather than exceptional: **1,634 contracting
children produce no first-descent mass at all**. A contracting skeleton is a
necessary condition for hazard, not a sufficient one.

---

## Terras, checked by word rather than by trajectory

§17 recasts the Terras coefficient-stopping conjecture (`σ = τ_c` for all `n ≥ 2`)
as a **finite-word inequality**:

```
ν(w) > ⌊ b_w / (2^|w| − 3^u(w)) ⌋      for every first-crossing word w
```

where `ν(w) = min(Ω_w ∩ [2,∞))`. Round 03-B's task list asks for the minimal
slack. This run enumerates **all 81,119 first-crossing words up to length 24** and
measures it.

**The inequality holds on every one, with room to spare.**

| `\|w\|` | `u` | words | min `ν − c` | max `c/ν` |
|---|---|---|---|---|
| 8 | 5 | 7 | 20 | **0.487179** |
| 13 | 8 | 85 | 186 | 0.028986 |
| 16 | 10 | 476 | 344 | 0.041783 |
| 21 | 13 | 8,045 | 155 | 0.025157 |
| 24 | 15 | 51,033 | 270 | 0.045936 |

The binding quantity is the **ratio** `c_w / ν(w)`, which must stay below 1. Its
largest value over the whole family is **0.487179**, at `w = UUUDUUDD` with
`r = 39`, `b = 251`, `c = 19`, `ν = 39`. Everywhere past length 10 the ratio sits
between 0.002 and 0.05 — Terras is not close to failing anywhere in this range,
and the tight cases are the short words, which are exhaustively settled.

**Why this is worth more than a trajectory check.** Iterating trajectories
confirms `σ = τ_c` for the integers actually visited. This confirms the inequality
for every *word*, which covers every integer in those cylinders at once —
including arbitrarily large ones. It does not extend past length 24, and the
family is infinite.

A structural check falls out alongside: **`h(w) = c_w` for every first-crossing
word**, confirming §15's claim that all proper prefixes are expanding and only the
final one caps.

And the depths line up with [`RUN-004`](RUN-004-HARD-ZETA-ORIGIN.md): the
first-crossing lengths are exactly the bit-lengths of powers of 3, which is
exactly the admissible-stopping-time set measured there. Round 02 supplies the
structural reason for what RUN-004 observed.

---

## The correction compartment is empty here — and that makes a check vacuous

On `[2, 2^18)`, `R_k = 0` for every `k`. Terras holds, so the entire Hard-Zeta
obstruction on this range is the coefficient frontier: `Z_k = C_k` exactly.

That is a real finding, and it also **disables** a check. `C_k + R_k = Z_k` reduces
to `C_k = Z_k` when `R_k` is empty, so *any* definition of `R_k` satisfies it — a
planted mutation of the `R` predicate came back silent for exactly that reason.

The split identity is a tautology of the definitions; what is testable is whether
this file implements it correctly. So it is now exercised on **synthetic `(σ, τ_c)`
data built to make `R_k` non-empty**, while the measured statement is stated for
what it is: *`R_k` is empty on this range*, not *the split identity was verified*.

Same family as [`feedback-empty-observable-passes-any-comparison`]; third
occurrence in this arm, so it is the class and not the instance.

---

## Three more gaps the drill found

**The quotient threshold was tested through a window, which a one-off slips
through.** `q` and `q−1` have different parities, so `n(q−1)` is not even in the
child's cylinder — the window merely moves and still contains `c`. The `+1` in
`q_U`'s numerator changes the floor on only **6 of 2,843** charts, and the check
missed all six. It now pins the threshold through the largest **legal** `a`.

**Two defects crashed rather than failed.** A damaged `ν()` returning 0 divided by
zero; a damaged `τ_c` condition ran off the walk cap. Both now degrade to a named
failure, because a traceback is the one outcome a drill cannot grade.

**Two mutations were retired as no-ops.** `3^u` and `2^j` are never equal, so `<`
and `<=` select the same set wherever they compare those two. Third time this tree
has met that; the mutations were replaced with ones that change the answer.

---

## A note on ROUTE MAP v0.2

[`RUN-004`](RUN-004-HARD-ZETA-ORIGIN.md) reported that ROUTE MAP **v0.1** stated
the general weighted bridge without §12's monotonicity hypothesis. **v0.2 is a
different map** — it states the `C`/`R` split, not the general bridge — so that
finding does not carry over, and this run checks that it doesn't rather than
leaving the earlier report to be misread.

---

## What this does not establish

Nothing about Collatz. Nothing about Terras beyond word length 24 — the family is
infinite and the margin is not shown to stay positive. Nothing about whether
either compartment's mass tends to zero.

What it does establish: Round 02's restatement agrees with Round 01 everywhere it
was checked, the mass-weighted hazard is the right object by a factor of up to 94,
and the Terras reformulation holds on 81,119 words with the worst case at 49% of
its bound.
