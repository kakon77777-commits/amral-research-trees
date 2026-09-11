# RUN-066 — `03`'s Algorithm 2 mirror checked by a different computation on 269,696 (curve, p) pairs; `13`'s +1899 / −53404 reproduced with git to the line, and every added line accounted for — none a twist; Phase 1 closes at 25 of 25 in the instrument's sense

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`03_Algorithm2_Independent_Reproduction`](../../../amral/public/bsd/phase1/files/03_Algorithm2_Independent_Reproduction.md), [`13_500K_Twist_Output_NonMonotonicity`](../../../amral/public/bsd/phase1/files/13_500K_Twist_Output_NonMonotonicity.md) — the two Phase 1 documents RUN-012 worked in its body and no round had on its subject line
**Tools:** [`src68_algorithm2_mirror_and_diff.py`](../code/src68_algorithm2_mirror_and_diff.py), [`src29_sweep_coverage.py`](../code/src29_sweep_coverage.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src68-algorithm2-mirror-and-diff.json`](../data/gate-logs/src68-algorithm2-mirror-and-diff.json), [`src29-sweep-coverage.json`](../data/gate-logs/src29-sweep-coverage.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `03` is the corpus's standard-library mirror of Algorithm 2 — a point-count formula, a 2-division cubic, an inertness argument, two fixtures. This tree's own `point_count` turns out to be the same formula, so agreeing with it would have been the same computation twice; the formula was instead held against a **brute-force enumeration of every (x, y) ∈ F_p²** on all 40,749 base curves at every odd prime ≤ 23 — **269,696 pairs, 0 disagreements**, Hasse's bound never violated, and this tree's `point_count` agreeing with the enumeration on every pair as well. `03` §4's cubic `4x³ + b₂x² + 2b₄x + b₆` is this tree's monic form under `X = 4x` — `16·f(x) = F(4x)` on all 40,749 curves — and `03` §5's claim that `(d, 3N) = 1` does the work of excluding the ramified primes holds on **every one of the 241,542 Zhai pairs of the CURRENT map: 257,959 prime divisors of `d`, none even, none dividing `3N`, none dividing the discriminant, the cubic rootless mod every one**. 46a1's seven and 106d1's twenty-one read back from both maps. `13` observed a commit diff of the twist JSON as `+1899 / −53404` and warned that 1,899 added *lines* are not 1,899 new twists. **`git diff --no-index --numstat` on the package's OLD and CURRENT blobs gives +1899 / −53404 exactly.** At entry level, **0 twists were added and 46,091 removed** — 21,306 on the stable base (RUN-060's figure; the package's `algorithm2_removed_twists.csv` has 21,306 rows) and 24,785 with their 2,707 deleted base curves — so the output was, in fact, monotone. And every one of the 1,899 added lines is classified: **1,851 are a deleted line minus its trailing comma** — the footprint of a surviving curve losing its last-listed twist, which 1,979 of them did — and **48 are lines git deleted and re-added unchanged** across a deleted key; **0 carry new content**. The deletions account exactly: 46,091 twist lines + 2 × 2,707 key lines + 1,851 + 48 = 53,404. `13`'s twelve `<150` survivors show 0 output deltas, as it says. **With these two on a subject line, Phase 1 is 25 of 25 by the instrument's strongest bucket — the count RUN-064 typed and RUN-065 corrected — and the corpus stands at 82 of 85, the three P5 documents remaining.**

---

## `03` §1 — the formula, and why agreeing with `point_count` would prove nothing

`03` writes, for odd `p`, `D_x = (a₁x + a₃)² + 4(x³ + a₂x² + a₄x + a₆)` and
`#{y} = 1 + χ_p(D_x)`. This tree's `point_count` (RUN-055's instrument, in
`src57`) is a square-table form of the same sum. Comparing them would be
RUN-042's failure mode — a check green because it compares a thing with
itself. The gate instead enumerates `(x, y) ∈ F_p²` and tests the Weierstrass
equation directly, `O(p²)` with no character sum, then compares three ways:

| | pairs | disagreements |
| --- | ---: | ---: |
| `03`'s formula vs enumeration | 269,696 | **0** |
| this tree's `point_count` vs enumeration | 269,696 | **0** |
| `(p + 1 − #E)² ≤ 4p` (Hasse) | 269,696 | **0** violations |

All 40,749 base curves, `p ∈ {3, 5, 7, 11, 13, 17, 19, 23}`, good primes only
(`03` §2's ordinary test is for good `p`). The formula is *not* defined at
`p = 2` — `4 ≡ 0` — and `03` says "odd `p`"; the gate's implementation refuses
`p = 2` rather than returning a number.

## `03` §4 — one cubic, two forms

`03` writes the 2-torsion `x`-coordinates as roots of `4x³ + b₂x² + 2b₄x + b₆`.
This tree has used the monic form `X³ + b₂X² + 8b₄X + 16b₆` in `X = 4x` since
RUN-042. They are the same polynomial: `16·f(x) = F(4x)`, verified on all
40,749 curves at seven integer points each, with `b₂, b₄, b₆` computed as `03`
writes them. **0 failures.**

## `03` §5 — the limitation, and the hypothesis that closes it

`03` is candid that its inertness test is *cubic reduction mod p* rather than
`F.ideal(p).is_prime()`, and says the theorem's `(d, 3N) = 1` excludes the
ramified bad primes so that the two agree on the fixture. The equivalence
*no root mod p ⟺ irreducible mod p ⟺ p inert in the cubic field* needs the
cubic separable mod `p` and `p` not dividing the index — both guaranteed when
`p ∤ 2Δ`. On every Zhai pair of the CURRENT map:

| | count |
| --- | ---: |
| Zhai curves in the map | 32,944 |
| pairs `(E, d)` | 241,542 |
| prime divisors `p ∣ d` | 257,959 |
| `p = 2` | **0** |
| `gcd(d, 3N) ≠ 1` | **0** |
| `p ∣ Δ_min(E)` | **0** |
| cubic has a root mod `p` | **0** |

So the mirror's shortcut is exact on the data it was run on — not because the
fixture happened to agree, but because the map's own admissibility conditions
put every `p` where Dedekind applies.

## `03` §3, §6 — the fixtures

46a1 → `1, 185, 265, 305, 745, 785, 905` in `03`, in the OLD map, in the
CURRENT map. 106d1 → 21 in all three. RUN-063 recomputed both from `00`'s
hand fixtures with this tree's own admissibility predicate; the gate reads
that recomputation's agreement as well.

## `13` — the diff, reproduced and taken apart

| | `13` | recomputed |
| --- | ---: | ---: |
| added lines | 1,899 | **1,899** (`git diff --no-index --numstat`) |
| deleted lines | 53,404 | **53,404** |

`13`'s argument: if the JSON changed only because base curves were deleted,
additions could be at most a few punctuation lines, not 1,899 — so a semantic
change is active on the large domain. Its warning: 1,899 is a *line* count,
and an entry-level census is needed before anyone says "1,899 new twists".
Both are right, and the census sharpens the first:

| entry level | count |
| --- | ---: |
| OLD keys → CURRENT keys | 39,394 → 36,687 (−2,707, +0) |
| OLD pairs → CURRENT pairs | 293,482 → 247,391 |
| pairs **added** | **0** |
| pairs removed with their base curve | 24,785 (package CSV: 24,785) |
| pairs removed on the stable base | 21,306 (package CSV: 21,306; RUN-060: 21,306) |
| stable curves with any twist removed | 5,437 (RUN-060 §7: 5,437) |
| stable curves whose **last-listed** twist was removed | 1,979 |

The output was monotone in fact — `T_C ⊂ T_O` — which is consistent with `13`
(*need not be* monotone) and with RUN-060 (the expand branch had nothing to
fire on). And the 1,899 added lines, each one classified against the deleted
lines of the same diff:

| kind of added line | count |
| --- | ---: |
| a deleted line minus its trailing comma — a surviving curve's new last twist | **1,851** |
| a deleted line re-added unchanged — git re-aligning across a deleted key | **48** |
| new content | **0** |

The deletions then account exactly: 46,091 removed twist lines + 2 × 2,707
structural lines for the deleted keys + 1,851 + 48 = **53,404**. So `13`'s
premise — that base deletion alone cannot produce 1,899 additions — holds
for the right reason: **a deleted base curve takes its whole block, and only
a removal on a *surviving* curve can turn `785,` into `785`.** The additions
are the footprints of the stable-base shrink, not new twists; 1,979 curves
lost their last twist, and git shows 1,899 of those as an added line (the
difference is the diff algorithm's alignment, not arithmetic — the count that
matters, 0 new pairs, does not depend on it).

`13`'s last point — the twelve `<150` survivors have `T_old(E) = T_new(E)`
each, so the small fixture had 0 output deltas for this semantic diff — holds:
the twelve of RUN-063's fixture, lists identical in both maps.

## Phase 1, now closed in the instrument's sense

`src29` re-run: Phase 1 **25 of 25 the subject of a round**, 0 cited only, 0
unmentioned. Corpus: 82 of 85 subject, 3 cited only — the three P5 documents
RUN-065 named as next.

## The drill

**280 defects, 280 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 56 controls undisturbed, over 94 checks.

The 5 planted for this gate, each turning `algorithm2-mirror-and-diff` red and the checks listed:

| planted defect | went red |
| --- | --- |
| 03's D_x loses its factor 4, so the formula counts the wrong curve | `algorithm2-mirror-and-diff` |
| the mirror's cubic is written with b4 in place of 2b4 | `algorithm2-mirror-and-diff` |
| Hasse's bound is applied as a_p^2 <= p | `algorithm2-mirror-and-diff` |
| the OLD map is read from the CURRENT file, so nothing was ever removed | `paper-vs-code`, `one-commit-and-delta`, `algorithm2-replay`, `algorithm2-mirror-and-diff` |
| a re-aligned added line is classified as new content | `algorithm2-mirror-and-diff` |


## What this round does not claim

* **`03`'s mirror is not re-run.** Its code is not in the package; its stated
  formula, cubic, argument and fixtures are what is checked, each by this
  tree's own computation.
* **The enumeration is at `p ≤ 23`.** Larger primes are covered by RUN-055's
  `point_count` up to 997, which this round shows agrees with enumeration on
  every pair it was tested on — not on every pair it has ever been used on.
* **"Inert" is not computed in a number field.** The gate verifies the
  hypotheses under which the cubic-mod-`p` test *is* the inertness test; it
  does not call `F.ideal(p).is_prime()`.
* **The line diff is git's.** `+1899 / −53404` is reproduced with the same
  tool `13` used; a different diff algorithm could align the 48 differently.
  The entry-level figures do not depend on any diff.
* **Phase 1 closed is a coverage statement.** Every document has been a
  round's subject; what each round did not do is in its own report.
