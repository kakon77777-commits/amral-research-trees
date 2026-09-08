# RUN-005 — every removed curve recounted over F₃, and a bucket that holds two different things

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the Banwait–Huang census's removal of 4,062 base curves — `results/summary.json` and `results/algorithm1_removed_census.csv`
**Tools:** [`src05_frobenius_at_three.py`](../code/src05_frobenius_at_three.py)
**Logs:** [`src05-frobenius-at-three.json`](../data/gate-logs/src05-frobenius-at-three.json)

**Result: the census's removal accounting is exact. 4,062 point counts over F₃ recomputed from the a-invariants with zero mismatches, every a₃ agreeing with both the package and ecdata, the published histogram reproduced bucket for bucket, and all five accounting identities holding. The removal criterion turns out to be exactly `|a₃| = 3`. One structural observation: the `a₃ = 1` bucket holds 611 Frobenius traces and 64 reduction-type conventions, which are different kinds of number wearing the same label.**

---

## The naming trap, first

The census's `a3` column is **not** the Weierstrass coefficient `a₃`. It is the
trace of Frobenius at `p = 3`:

$$a_3 = 3 + 1 - \#E(\mathbb F_3)$$

The package's own columns settle it: `14a1` records `a3 = -2` beside
`projective_point_count_at_3 = 6`, and `4 − 6 = −2`. A gate that took the column
name at face value and compared against the Weierstrass `a₃` — which this arm
had in hand from RUN-004 — would have reported **4,062 mismatches against
entirely correct data**, and the report would have been about a defect that does
not exist.

## What was recomputed

Exhaustive counting over `F₃ × F₃` plus the point at infinity, from the
a-invariants alone. Exact integers, no float, because every quantity is an
integer.

| check | scope | result |
| --- | ---: | ---: |
| projective points over F₃ | 4,062 | **0 mismatches** |
| nonsingular projective points over F₃ | 4,062 | **0 mismatches** |
| `a₃` vs the package's own column | 4,062 | **0 mismatches** |
| `a₃` vs ecdata's aplist token | 3,998 | **0 disagreements** |
| published `a₃` histogram, rebuilt | 5 buckets | **all 5 match** |

The remaining 64 carry `-` rather than an integer in ecdata's aplist — its
placeholder at a bad prime. Those are **counted and reported**, not silently
skipped: a comparison that quietly declines to run on part of its population is
the shape this arm exists to catch.

### The accounting identities

| identity | |
| --- | --- |
| `a3_only + isogeny_only + both = removed` — 2,707 + 1,353 + 2 = 4,062 | ✓ |
| `old − removed + added = new` — 40,749 − 4,062 + 0 = 36,687 | ✓ |
| `Σ individual_isogeny_counts = isogeny_only + both` — 1,233+115+7 = 1,355 | ✓ |
| `isogeny_combination_counts.NONE = a3_only` — 2,707 | ✓ |
| `unexplained = 0` | ✓ |

## What the criterion actually is

Cross-tabulating the recomputed `a₃` against the package's own `failure_class`
makes the rule exact rather than inferred:

| `a₃` | A3_ONLY | BOTH | ISOGENY_ONLY |
| ---: | ---: | ---: | ---: |
| −3 | 908 | 2 | 0 |
| −2 | 0 | 0 | 622 |
| −1 | 0 | 0 | 56 |
| +1 | 0 | 0 | 675 |
| +3 | 1,799 | 0 | 0 |

**The a₃ mechanism removes exactly the curves with `|a₃| = 3`** — 910 + 1,799 =
**2,709**, which is both the package's `abs_a3_eq_3` count and `a3_only + both`.
The isogeny mechanism removes curves with `a₃ ∈ {−2, −1, +1}`, totalling 1,353.

This also disposes of something that looked like a finding and is not. The
published histogram has no `a₃ = 0` and no `a₃ = 2` bucket, and by Hasse
`|a₃| ≤ 2√3 < 4` so both values are possible. The absence is not an omission:
those curves are simply not removed. And the apparent asymmetry — `−2` present,
`+2` absent — is an artifact of reading **two different mechanisms' rows in one
histogram**. Cross-tabulating dissolved it. Asserting it before cross-tabulating
would have been a finding about my own reading.

## The bucket that holds two different things

The gate's first run reported the histogram matching in four buckets and
disagreeing in one: `a₃ = 1`, stored **675**, recomputed **611**. The gap is 64,
and 64 is exactly the number of removed curves with bad reduction at 3.

That was not a data error. It was the gate computing `a₃ = 4 − #E(F₃)`, which is
only defined at a prime of good reduction, and declining to guess at the other
64.

The 64 are resolved from the nonsingular point count, which fixes the reduction
type without assuming any convention on the package's behalf: `#E_ns(F₃) = p−1`
is split multiplicative, `p+1` non-split, `p` additive. **All 64 have
`#E_ns(F₃) = 2 = p−1` — split multiplicative — so `a₃ = +1` for every one**, by
the standard convention. With those added, the bucket reads 675 and the
histogram matches exactly.

So the `a₃ = 1` bucket contains:

* **611** curves where `a₃ = 1` is a count of points on a smooth curve, and
* **64** curves where `a₃ = 1` is a convention recording split multiplicative
  reduction, and where ecdata itself writes `-` rather than a number.

Both are correctly labelled `a₃ = 1`, and the sum is right. They are not the
same kind of fact. Nothing downstream in this census distinguishes them, and
nothing observed here needs them distinguished — but a later step that treats
the `a₃ = 1` bucket as 675 smooth Frobenius traces would be wrong about 64 of
them, and the histogram alone gives no way to notice.

## What this round does not claim

* **Nothing about BSD.**
* **It does not verify the census's 36,687 / 247,391 headline.** It verifies the
  removal step that produces 36,687 from 40,749 — the twist-pair count is a
  separate object and a later round.
* **It does not verify that `|a₃| = 3` is the right admissibility criterion.**
  It measures that the package applied that criterion exactly and accounted for
  every curve it removed. Whether the criterion is the correct one is a question
  about Banwait–Huang's method, not about this implementation of it.
* **It does not check the isogeny half.** The 3/5/7-isogeny determination was
  read from the package, not recomputed; recomputing it needs isogeny
  computation this gate does not do. Stated as a gap, not passed over.
