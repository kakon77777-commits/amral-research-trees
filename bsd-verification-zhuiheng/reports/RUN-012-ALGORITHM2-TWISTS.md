# RUN-012 — all 247,391 twists rebuilt, and a docstring that contradicts its own code

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Algorithm 2's twist maps — the largest unverified artifact in the Phase 1 line, and the gap RUN-008 declared
**Tools:** [`src13_algorithm2_twists.py`](../code/src13_algorithm2_twists.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src13-algorithm2-twists.json`](../data/gate-logs/src13-algorithm2-twists.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: 36,687 of 36,687 twist lists reproduced exactly — every one of the 247,391 pairs, both branches, zero divergence. Three things came out of doing it. The generator's CLZ docstring states a condition its own code does not compute, and the published artifact follows the code. The entry-level twist census that `13_500K_Twist_Output_NonMonotonicity` asked for closes: 21,306 entries removed, **zero added**, so the non-monotone branch that document warned about is real in the code and empty in the output. And RUN-007's `a_p` carried a guard that could never fire.**

---

## The gap RUN-008 named

> It says nothing about the twist maps, 247,391 admissible twist pairs, or
> Algorithm 2. Those are separate outputs with separate evidence.

## Two branches, and they are the two populations RUN-008 found

Algorithm 2 routes each base curve by source: **CLZ20** for curves with
`E(Q)[2] = Z/2Z`, following Cai–Li–Zhai (2020); **Zha16_no_2_tors** for curves
without 2-torsion, following Zhai (2016).

RUN-008 measured that split from the arithmetic alone — 3,747 curves with a
rational 2-torsion point, 37,002 with none, no overlap, decided by `X₀(2)` — and
reported it as an unexplained fact about the base's composition. **It is the
branch condition.** The two families are the two theorems.

| | `M` range | conditions |
| --- | --- | --- |
| **CLZ** | `1 … 1000` | squarefree; `gcd(M, 3N) = 1`; `p ∤ a_p` for every `p \| M`; `p ≡ 1 (mod 4)` and a 2-adic condition for every `p \| M`; `M ≡ 1 (mod 8)`; `(M/q) = 1` for every odd `q \| N` |
| **Zhai** | `−1000 … 1000`, negative only when `Δ_E < 0` | squarefree; `gcd(M, 3N) = 1`; `p ∤ a_p` for every `p \| M`; `M ≡ 1 (mod 4)`; every `p \| M` inert in `Q(E[2])`; `(M/q) = 1` for every `q \| N`, including `q = 2` |

Everything was recomputed rather than re-run: point counts by Legendre symbols,
Kronecker symbols from scratch, squarefreeness by trial division, inertness from
the 2-division cubic. The generator's source was read for the *definitions* — a
criterion has to come from somewhere — and for nothing else.

The method was checked against the corpus's own stated fixture before it was
trusted: `03_Algorithm2_Independent_Reproduction` records 7 twists for `46a1` on
the CLZ branch and 21 for `106d1` on the Zhai branch. Both reproduce exactly.

## The result

| branch | curves | **exact list match** |
| --- | ---: | ---: |
| `CLZ20` | 3,743 | **3,743** |
| `Zha16_no_2_tors` | 32,944 | **32,944** |
| **total** | **36,687** | **36,687** |

Not a curve with a twist missing, not a curve with a twist too many.

## A condition stated twice, and differently

The CLZ branch's docstring says condition (c) is

> `p ≡ 1 (mod 4)` and **`ord_2(a_p) = 1`** for all primes `p | M`

and the line beneath it computes

> `(p + 1 - a_p).valuation(2) == 1`, which is **`ord_2(#E(F_p)) = 1`**.

These are not the same condition. `p = 5` with `a_p = 2` gives `ord_2(a_p) = 1`
but `ord_2(#E(F_p)) = ord_2(4) = 2`. So the gate was run **both ways**:

| reading | CLZ curves whose list it reproduces |
| --- | ---: |
| the code — `ord_2(#E(F_p)) = 1` | **3,743 of 3,743** |
| the docstring — `ord_2(a_p) = 1` | **19 of 3,743** |

The artifact follows the code. On `46a1` the docstring reading returns 18 twists
where the artifact has 7, and they are disjoint apart from `M = 1`.

The 19 are the curves where the two conditions happen to select the same set;
they are agreement by coincidence, not by equivalence. **One of the two
statements in that file is wrong about the other**, and this round does not
adjudicate which of them CLZ20's theorem actually requires — that is a question
about a published paper, not about this artifact. What it settles is that the
file disagrees with itself and that the output followed the executable half.

## The entry-level census the corpus asked for

`13_500K_Twist_Output_NonMonotonicity` observes that one commit changed this file
by `+1899 / −53404` lines, warns that 1,899 is a count of **added diff lines and
not of new twists**, and says exactly what would settle it:

> 完整 entry-level census 需要物化 old/current JSON 後 parse set difference.

It also predicts the change need not be monotone — tightening `gcd(M, N)` to
`gcd(M, 3N)` removes candidates, while deleting the old `disc_valuation_condition`
could add them — and records that the 12-curve small fixture observed **0** output
deltas, so neither branch was covered.

| | measured here |
| --- | ---: |
| old twist keys / new twist keys / stable | 39,394 / 36,687 / 36,687 |
| keys only in old | 2,707 |
| `unchanged` | **31,250** |
| `shrink_only` | **5,437** |
| `expand_only` | **0** |
| `mixed` | **0** |
| twist entries removed | **21,306** |
| twist entries **added** | **0** |
| every removed entry divisible by 3 | **yes** |
| curves where new = old with multiples of 3 dropped | **36,687 of 36,687** |

So: **the expand branch is real in the code and empty in the output.** Deleting
`disc_valuation_condition` added not one twist across the whole domain. The 1,899
added diff lines are structural — re-indentation and re-keying — exactly as that
document suspected and could not then show.

The key accounting also closes without being read from the package: 2,707 keys
present in the old twist map and absent from the new are exactly the `A3_ONLY`
removals, and the 1,355 isogeny-gate removals were never in the old twist map at
all — 39,394 + 1,355 = 40,749.

## Negative twists: in scope, and correctly absent

The Zhai loop runs `M` from `−1000` and skips negative `M` only when `Δ_E > 0`,
so curves with negative discriminant have negative twists in scope. Not one of
the 247,391 pairs is negative, which is either a correct outcome or a silent
omission — and those look identical until someone enumerates.

Enumerated: **22,858** Zhai-branch curves have `Δ < 0`, so the scope is not
vacuous — that is 62% of the branch, each with a thousand negative candidates to
consider. The criteria admit **zero** of them. The absence is right.

## A guard of mine that could never fire

RUN-007's `a_p` ended with

```python
# a singular reduction shows up as a count that Hasse cannot accommodate
return ap if abs(ap) * abs(ap) <= 4 * p else None
```

**That comment is false and the branch was dead.** At a prime of bad reduction
`a_p` is `0` or `±1` — split multiplicative `+1`, non-split `−1`, additive `0` —
which satisfies `|a_p| ≤ 2√p` for every `p`. The guard could not distinguish
anything. Probed at eight bad primes across five curves it returned `0` or `±1`
every time, comfortably inside Hasse, and `None` never once.

RUN-007's verdicts are unaffected: its caller filters bad primes with
`divides_discriminant()` before reaching `a_p`, so the dead guard was never
load-bearing, and the corrected version re-runs **byte-identical**. But the
comment asserted something untrue about the code beneath it, which is the same
shape as the finding above — and it was mine.

## The drill, extended twice

Gate 13 shipped with its drill in the same commit, and this round went back for
the four gates RUN-010 had left: `src04`–`src07`.

**48 defects, 48 caught by the check named for each. 14 controls, none disturbed.**

The run that added them caught **44 of 49**, and the five misses were worth more
than the passes. Three were checks that could not see a real defect:

* a relational assertion on the `F₃` point counts survived subtracting one from
  both — now pinned absolutely to `(7,7)` and `(3,2)`;
* a fixture with `3 ∤ N` on both curves could not exercise `gcd(M, 3N)` — a
  `shrink_only` curve was added, whose old list carried `177, 501, 669`;
* the Hasse guard above, which nothing could reach.

Two were mutations that are **no-ops on the actual population**, and they moved to
controls with the reason rather than being dropped: `(n−1)² ≡ 1² (mod n)`, so the
last residue of a square test is redundant; and dropping the denominator-3 half of
RUN-006's rational root theorem **changes no verdict on any of the 4,062 census
curves** — 1,232 stay `True`, 2,805 stay `False`, 25 stay undecided — because every
curve there with a root of denominator 3 also has an integer root. That branch of
RUN-006 never decided anything, and saying so is worth more than a defect list
that quietly omitted it.

## What this round does not claim

* **Nothing about BSD**, and nothing about whether the twist conditions are the
  right ones. It verifies that Algorithm 2's stated criteria were applied
  correctly, on every curve, in both directions.
* **It does not adjudicate the docstring against CLZ20's theorem.** Which of the
  two 2-adic conditions the published theorem requires is a question about a
  paper this arm has not read. What is settled is that the file contradicts
  itself and the output followed the code.
* **Inertness is tested by irreducibility of the 2-division cubic mod `p`.**
  Irreducible mod `p` ⟹ `p` inert always; the converse can fail when `p` divides
  the index, which needs `p | disc(cubic)`. That is not vacuous here — 109,497
  `(curve, p)` pairs qualify — so the guarantee is the one the exact agreement
  gives: on every pair that actually reached the test, this criterion and the
  generator's number-field one returned the same answer, because a single
  disagreement would have changed a list and no list differs. The same caveat is
  one the corpus's own `03_Algorithm2_Independent_Reproduction` states about its
  mirror.
* **`src00`–`src03` remain undrilled** — the corpus-scanning gates, whose claims
  are about text rather than arithmetic.
