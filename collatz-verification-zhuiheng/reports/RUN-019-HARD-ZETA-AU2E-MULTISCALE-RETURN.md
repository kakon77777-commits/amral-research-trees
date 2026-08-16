# RUN-019 — Round A-U.2e: every exact identity holds, and both inequalities turn out to be the same line, on the vacuous side of which every computable spine sits

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2e_bundle.zip` (source item 37) — Round A-U.2e *Multiscale Return Arithmetic*, plus `A_Line_ROUTE_MAP_v1.5`, re-shipping A-U.2b.1, A-U.2b.2 v0.1.1 and A-U.2b.3
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (A-U.2e layer) · [`src21_hardzeta_au2e_recheck.py`](../code/src21_hardzeta_au2e_recheck.py) · [`src21_drill.py`](../code/src21_drill.py)
**Logs:** [`src21-au2e-recheck.json`](../data/gate-logs/src21-au2e-recheck.json) · [`src21-drill.json`](../data/gate-logs/src21-drill.json)

**Result: 20/20 checks. 25/25 planted defects caught by the check named for each — 8 in the definition layer, 13 in this run's own measurement, 4 in the documents. 2/2 null controls undisturbed. Coverage audit clean. Anchor audit clean at 277 anchors across 17 drills.**

---

## What the round does

With the packing branch closed, A-U.2e stops counting words and asks a different
question: how far must a genuine positive-integer spine deviate from the
**mechanical critical word** `a_m = ⌊βm⌋ − ⌊β(m−1)⌋`?

Its chain is short. The deficit's increment *is* the deviation,

    d_m − d_{m−1} = a_m − q_m,

so the L1 deviation `V_N` is the deficit path's total variation and splits into
an upward half `U_N` (credits the mechanical word spends and the orbit does not)
and a downward half `W_N`, with `U_N − W_N = d_N`. Mismatches then contaminate
factor complexity, `p_N(r) ≤ (r+1) + r·J_N`; return separation forces
`N − r + 1 ≤ p_N(r)` once `2^{r+1} > M_N`; and the two combine into a barrier
`J_N ≥ (N − 2r_N)/r_N`. Finally §3 gives a reset geometry whose affine identity,
stated with the irrational slack `δ_m = βm − K_m`, clears to an identity between
integers.

## The identities, from the definitions

All four are exact and all four hold, on every prefix of seven subcritical
spines. `V` and the directional split are not read off the library — the check
recomputes the deficit path's variation independently and compares.

| `n` | `N` | `J_N` | `V_N` | `U_N` | `W_N` | `d_N` |
|---|---|---|---|---|---|---|
| 27 | 36 | 22 | 25 | 13 | 12 | 1 |
| 103 | 25 | 15 | 17 | 9 | 8 | 1 |
| 703 | 50 | 30 | 38 | 20 | 18 | 2 |
| 1407 | 50 | 32 | 41 | 21 | 20 | 1 |
| 10087 | 65 | 45 | 55 | 28 | 27 | 1 |
| 15039 | 51 | 28 | 34 | 18 | 16 | 2 |
| 35655 | 84 | 54 | 65 | 33 | 32 | 1 |

`U_N` equals `#{m : a_m = 2, q_m = 1}` exactly, which is §1's claim that the only
way to gain deficit is to skip a credit the mechanical word would have spent.
Both directions occur on every spine, so the identity is not being graded on a
sample that only moves one way.

**The Reset Affine Identity holds in exact integers.** Cleared of `2^{−K_b}` and
`3^b`, §3's

    Y_b = 2^{δ_b−δ_a} Y_a + (2^{δ_b}/3) Σ_{i=a}^{b−1} 2^{−δ_i}

becomes

    Y_b·2^{K_b} = Y_a·2^{K_a}·3^{b−a} + Σ_{i=a}^{b−1} 3^{b−1−i}·2^{K_i},

verified at 1,554 windows with no floating point anywhere. The Deficit-Drop
Slope Identity's content — a deficit drop is exactly a locally contracting block,
`3^{b−a} < 2^{K_b−K_a}` — holds with both outcomes present.

The one-sided dichotomy's monotone branch also checks out: on each spine's
longest nondecreasing deficit stretch, *every* mismatch is a skipped credit and
their count is exactly the deficit gain.

| `n` | stretch | gain | mismatches | of which skipped credits |
|---|---|---|---|---|
| 27 | 18→28 | 4 | 4 | 4 |
| 703 | 1→12 | 5 | 5 | 5 |
| 15039 | 27→44 | 6 | 6 | 6 |
| 35655 | 10→18 | 4 | 4 | 4 |

## The two inequalities are one line

This is the run's finding, and it was not visible until the numbers were on the
table.

A word of length `N` has at most `N − r + 1` factors of length `r`, whatever it
is. So the contamination bound says something only when its cap falls below that
ceiling:

    (r+1) + r·J_N < N − r + 1   ⟺   J_N < (N − 2r)/r.

The right-hand side **is the packing theorem's floor.** Contamination constrains
the word only *below* the threshold that return separation forbids. Verified row
by row across 42 rows with **0 disagreements**, and with both outcomes present so
the equivalence is not being graded on rows that all fall the same way.

Which means a single number decides whether either half is visible at a given
size — and on real spines that number is on the wrong side:

| `n` | `N` | `r_N` | `N/r_N` | `J_N` | floor `(N−2r)/r` | fraction of `J_N` pinned |
|---|---|---|---|---|---|---|
| 27 | 36 | 12 | 3.00 | 22 | 1.00 | 4.5 % |
| 103 | 25 | 12 | 2.08 | 15 | 0.08 | 6.7 % |
| 703 | 50 | 17 | 2.94 | 30 | 0.94 | 3.3 % |
| 1407 | 50 | 17 | 2.94 | 32 | 0.94 | 3.1 % |
| 10087 | 65 | 20 | 3.25 | 45 | 1.25 | 4.4 % |
| 15039 | 51 | 22 | 2.32 | 28 | 0.32 | 3.6 % |
| 35655 | 84 | 24 | 3.50 | 54 | 1.50 | 3.7 % |

The barrier's floor is `N/r_N − 2`, and `N/r_N` runs 2.08 to 3.50 because these
spines die after 25–84 steps while their peaks are 12–24 bits wide. So the floor
lands between 0.08 and 1.50 against a measured `J_N` between 15 and 54 — it pins
**3.1 % to 6.7 %** of the mismatches actually present. The bound would still be
satisfied if all but one or two of them vanished. Correspondingly, the
contamination bound is informative at `r = 1` only; at `r = 2..6` its cap exceeds
`N − r + 1`, which every word satisfies for free.

Real spines have `J_N/N` between 0.55 and 0.69, putting `J_N` **15 to 32 times**
above the line. **Passing the packing inequality is not evidence, and this run
says so rather than reporting a green check.**

## The reset geometry, by contrast, does bind

Same round, opposite verdict. The First-Return Reset Bound also clears to
integers for integer threshold `h`:

    3^{a+1}·Y_b  <  3·2^{h+K_a}·Y_a + 3^a·(b−a),

and across **190 first-return windows** — 166 of them spanning more than one
step, the longest gap 66 — the true `Y_b` reaches **0.203 to 0.938** of its cap.
That bound is doing real work at this scale.

But it is doing it with one hand. §3 reads the bound as contraction *plus* an
affine correction accumulating linearly over the reset interval. **The correction
is never what makes the bound true here**: the contraction term alone bounds
`Y_b` at all 190 windows, and adding `(b−a)/3` moves the worst case by
4.62 × 10⁻⁴. The reset really is pure contraction at these sizes; the second term
is an asymptotic provision.

That was found because the drill said so. Removing `(b−a)` from the correction
changed nothing, which is a no-op — and rather than swap in a defect that would
be caught, the no-op became a check with its own defect naming it.

## Findings about my own checks

**A vacuous check, found by measuring the mutation before writing it.** The first
candidate defect for the contamination bound was to halve `J_N`. Measured before
committing: the cap has 3.6× to 9.4× of slack, so halving is invisible. Pushing
further showed the cap exceeds `N − r + 1` for every `r ≥ 2` — the check could
not fail at all. The response was not to find a sneakier mutation but to move the
falsifiable content into two checks that *can* fail: the algebraic equivalence
above, and a check on the measured quality itself (`fraction_pinned < 0.25`,
saturation `> 0.5`). Both are drilled.

**A check that genuinely cannot be broken here, stated as such.** No perturbation
of the bound, the peak, or the exponent can push a measured `J_N` of 15–54 below
a floor of 1.5. The packing inequality is unfalsifiable at these sizes. Its
defect therefore targets what *is* checkable — that the tool verifies the
separation hypothesis `2^{r+1} > M_N` instead of assuming it — and the drill's
docstring records the reason rather than implying coverage it does not have.

**Numbers computed, not typed.** The run's summary paragraph is generated from
the measurement rows. An early draft had "22 to 36" hand-typed where the
measurement said 22 to 180, and another said "two orders of magnitude" where the
spread was 30×. The sentence is now built from `min`/`max` of the same arrays it
describes, so it cannot drift.

**The suite's own headline figure was wrong, and its first fix was wrong too.**
The charter said "fourteen mutation drills, 304 planted defects" — a number typed
into prose, checked by nothing, stale for many rounds. Replacing it with a script
([`suite_totals.py`](../code/suite_totals.py)) exposed a second problem: drill
logs have used **three** different shapes, and the first version read only one,
reporting **383 where the logs held 461**. Two entire drills contributed zero and
the total still looked plausible. It now classifies every log explicitly and
refuses what it cannot interpret. Writing its own log through a shell redirect
then fed it a zero-byte file, which it crashed on rather than refusing — that is
now the sixth planted defect in
[`suite_totals_drill.py`](../code/suite_totals_drill.py). The charter and README
cite the script; neither states the number.

## What this does not establish

Round A-U.2e's exact identities are verified; its asymptotic content is not, and
this arm cannot verify it. Specifically **not** established here:

- **Regime M's `d_N ≳ √N`** and `Y_N ≳ 2^{√N}` — statements about a hypothetical
  counterexample's tail, with no finite instance to test. Real spines reach
  `d_N ≤ 2` and die.
- **Regime R's `Ω(N/log N)` bidirectional variation** — same.
- The **mismatch packing barrier as a barrier.** It holds on every spine measured
  and constrains 3–7 % of what is there.
- **CASP, Terras's conjecture, and the Collatz conjecture itself** remain open;
  §6 says so and the check confirms the ledger says so.

The bundle is trimmed rather than edited: it drops A-U.1, A-U.2a and A-U.2b,
and the three predecessors it does re-ship are byte-identical to their originals.

**Next:** A-U.2e.1 (Reset-Block Arithmetic), A-L (Giant Valuation Tail),
A-U.2d (Transducer Rationality) — the three successors `ROUTE_MAP v1.5` names.
