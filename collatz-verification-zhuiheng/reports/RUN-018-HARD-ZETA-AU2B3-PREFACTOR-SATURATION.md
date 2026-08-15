# RUN-018 — Round A-U.2b.3: the subject corrected a defect this arm reproduced faithfully and did not notice

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2b3_bundle.zip` (source item 36) — Round A-U.2b.3 *Queue-Prefactor Saturation, Pointed/Unpointed Correction and Third-Order No-Gain*, its diagnostics script and JSON, three figures, the **corrected A-U.2b.2 v0.1.1**, plus `A_Line_ROUTE_MAP_v1.4`
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (A-U.2b.3 layer) · [`src20_hardzeta_au2b3_recheck.py`](../code/src20_hardzeta_au2b3_recheck.py) · [`src20_drill.py`](../code/src20_drill.py)
**Logs:** [`src20-au2b3-recheck.json`](../data/gate-logs/src20-au2b3-recheck.json) · [`src20-drill.json`](../data/gate-logs/src20-drill.json)

**Result: 17/17 checks. 27/27 planted defects caught by the check named for each — 10 in the definition layer, 11 in this run's own measurement, 6 in the documents. 2/2 null controls undisturbed. Coverage audit clean.**

---

## The correction, and why this arm missed it

Round A-U.2b.2 defined `Q_{r,D}` in §4 as the set of exponent words for which
**there exists** an admissible starting deficit. Its shipped dynamic program
summed `V_r` over *all* starting deficits, which counts each word once **per**
admissible start. Those are different objects — at `r = 4, D = 2`, 66 against 48.

RUN-018 is not where that was found. **The subject found it**, and ships both a
corrigendum in the route map and a corrected `v0.1.1` of the previous paper.

RUN-017 reproduced the DP by a deliberately different method — prefix sums where
theirs used suffix sums, exact integer credits where theirs multiplied a float —
and validated it against brute-force enumeration. All nine rows matched exactly.
The verification was sound and the object was wrong, because **my brute force
enumerated from every starting state too**. It was written from the *script's*
reading, so it confirmed the script against itself. Two implementations agreeing
is not verification when both descend from the same source — which this arm's
charter already says, and which I applied to the *method* while leaving the
*specification* unread.

That is now a standing rule here: **a paper plus a program is two claims.**
Implement from the prose, watch the quantifiers, and add an explicit check that
definition and program agree. Everything in this run is implemented from §4–§7's
prose, and the identity `Q = P_D − P_{D−1}` is verified against a direct
enumeration of *words* — the check that was missing.

**What the correction costs RUN-017: the label, not the conclusion.**

| `r` | rate (pointed) | rate (unpointed) | shift |
|---|---|---|---|
| 200 | 1.5187691 | 1.5172835 | 1.49 × 10⁻³ |
| 800 | 1.5700178 | 1.5691920 | 8.3 × 10⁻⁴ |
| 2000 | 1.5787055 | 1.5783565 | 3.5 × 10⁻⁴ |
| 5000 | 1.5825043 | 1.5823625 | **1.4 × 10⁻⁴** |

The entropy still saturates on `β`, so the Prefix-Constraint First-Order No-Gain
verdict stands. And the Second-Order Barrier never used the DP data at all — it
runs on the weak-composition sums `A(r,D)`, `B(r,D)` — so it is untouched.
A-U.2b.2 v0.1.1 says both in its own corrigendum; the table above is what
confirms it independently. RUN-017 has been amended in place.

---

## The identities, from the definitions

```
S_j  = Σ_{i≤j} (e_i − b_i)
R(e) = max_j S_j − min_j S_j
```

A word is admissible from `d_0` exactly when `0 ≤ d_0 − S_j ≤ D` for all `j`,
i.e. `max_j S_j ≤ d_0 ≤ D + min_j S_j`, giving **`D − R(e) + 1`** starts. Checked
by trying every starting deficit on every admissible word at five shapes — not by
trusting the formula.

From there `P = Σ_{R(e)≤D}[D − R(e) + 1]` against the DP, and
`Q = #{e : R(e) ≤ D}` against `P_D − P_{D−1}`, both exact at seven shapes. And a
check that the two counts **genuinely differ** at every shape tested, because if
they agreed the whole corrigendum would be empty and every check above would be
about one object rather than two.

---

## The diagnostics, and what they show

All nine published rows reproduce with **worst deviation exactly 0** across all
eight columns — computed from the definitions above rather than from the shipped
script.

Two measurements worth keeping:

**The pointing multiplicity settles.** `P/Q` runs 1.229 → 1.463 → 1.581 → 1.622 →
1.635 → **1.638** at `r = 10000`. A bounded ratio is precisely why the correction
cannot move the exponential rate or the `r^{−1/2}` prefactor scale — the two
counts differ by a constant factor, not a growing one. That is the quantitative
content of §22–§23's "the constants are unchanged".

**The centered prefactor is bounded but not monotone.** `r·H(z) − log₂Q − ½log₂r`
sits in a band of width 2.33 (5.54 to 7.87), bottoms at `r = 5000` and rises
again at 8000 and 10000. That is consistent with `Q = Θ(r^{−1/2}2^{rH})` and is
all a finite table can show; it is reported as a band, not as a convergence,
because it is not one.

---

## The round's own epistemic bookkeeping

§33 splits its results three ways rather than the usual two, and that is worth
recording:

- **self-contained exact results** — the pointed/unpointed identity, canonical
  pointing, the DP correction, the packing formulation;
- **standard analytic dependency** — the saturation *lower* bound leans on
  lattice local-limit and positive-drift ballot/bridge estimates, which the round
  names rather than absorbing;
- **unproved** — phase-specific wedge constants, CASP, Terras, Collatz.

A round that has just corrected itself declaring exactly which of its results
rest on imported analysis is the right response to having been wrong once.

**The packing branch is declared closed**, with its seven exhausted items
itemised: composition entropy, the sharp first-order constant, the Stirling tax,
exact queue prefix constraints, the exact queue prefactor, the pointed/unpointed
correction, and third-order queue-only no-gain. What remains is named: A-U.2c
(noncompact anchor cocycle), A-U.2d (transducer rationality), A-U.2e (multiscale
return arithmetic).

**The correction ships under a new filename.** `v0.1.1` is added; `v0.1` is not
overwritten in place. A corrigendum that reused the old name would erase its own
history, and this one supersedes by version instead — checked, along with the
absence of any silent same-name edit anywhere in the bundle.

---

## Findings about my own checks

**A no-op with a mathematical reason behind it — the most interesting one yet.**
I planted a defect that walks the deficit backwards: `d ← d − b_j + e_j` instead
of `d ← d + b_j − e_j`. It changed nothing. The reason is real: the number of
admissible starts depends only on `R(e) = max_j S_j − min_j S_j`, and that is
**invariant under `S → −S`**. Reversing the walk reflects the partial sums and
leaves the range, hence the multiplicity, exactly where it was. Confirmed on
every admissible word at four shapes. Replaced by a defect that widens the
corridor by one, which does move the count.

**Two guards that are redundant with each other, so loosening *either* is
invisible.** The word enumeration prunes on `R(e) ≤ D` during the walk *and*
filters on `multiplicity > 0` at the end. Because `R(e)` is monotone in the
prefix, anything surviving the prune already satisfies the filter — so both
directions of loosening are no-ops, and I planted each in turn before seeing why.
The one guard that is *not* doubled is the excess range: a word needs
`e_j ≤ D + 1` to be admissible, so narrowing the loop to `D` drops real words
(48 → 43 at `r = 4, D = 2`). That is the defect the check needed.

Related, same run: `not edited` in the provenance check is vacuously true on a
clean bundle, so deleting it is invisible — the defect now miscomputes `edited`
instead.

**A section slice that reached into a later section.** The "packing branch
closed" check searched from §31 to the end of the file, and §33's self-contained
list repeats the same words — so removing an item from §31's list left every word
still findable. Narrowed to §31 alone.

**One defect fired the wrong check, informatively.** A wrong `floor_beta` does not
disturb the corridor check, because that check reads `x_star` from the shipped
JSON and never calls `floor_beta` at all. Retargeted to the diagnostics, which it
does break.

---

## What this does not establish

§33's unproved list. The Queue-Prefactor Saturation theorem's lower bound is an
analytic dependency by the round's own account, so what is checked here is its
finite shadow: nine corridors, a bounded centered prefactor, and a settling
multiplicity ratio. `Θ` is not established by a table. The packing branch being
closed is a statement about what *this* family of arguments can yield, and the
three successor routes are untouched.
