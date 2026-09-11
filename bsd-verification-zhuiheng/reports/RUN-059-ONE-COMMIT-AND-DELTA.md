# RUN-059 — One commit, four documents: every figure recomputes, the histogram `11` called unknown is known and reversed, and `14`'s Gates A and B are done

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`07_One_Commit_Semantic_Autopsy`](../../../amral/public/bsd/phase1/files/07_One_Commit_Semantic_Autopsy.md), [`11_500K_One_Commit_Global_Impact`](../../../amral/public/bsd/phase1/files/11_500K_One_Commit_Global_Impact.md), [`12_Delta_Only_Algorithm1_Verifier`](../../../amral/public/bsd/phase1/files/12_Delta_Only_Algorithm1_Verifier.md), [`14_Phase1_Next_Low_Cost_Gate`](../../../amral/public/bsd/phase1/files/14_Phase1_Next_Low_Cost_Gate.md)
**Tools:** [`src61_one_commit_and_delta.py`](../code/src61_one_commit_and_delta.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src61-one-commit-and-delta.json`](../data/gate-logs/src61-one-commit-and-delta.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: four documents describe the commit `1a0489c → 31fae20` from four angles, and RUN-056 read that commit from the package's archived diffs. `07`'s two predicates — `A_old` conditional, `A_new = {3,5,7}` plus a separate `a₃ ≠ ±3` — are the diff lines RUN-056 located, and `07` calls the change 「theorem predicate 的實質收緊，不是效能重構」, which the data confirms: 4,062 curves left. **Every figure in `11` §2–§3 recomputes exactly** — `4064 − 2 = 4062`, 9.9683 %, 90.0317 %, 1.3296 % → 1.1971 % of 3,064,705, the 0.1325-point drop — and its two pre-candidate-pool percentages, 22.8460 % and 20.5686 %, **imply the same pool size, 178,364**, which `11` never states and which is the consistency check on both. `11` §4 said the per-gate histogram of the 4,062 was *still unknown* and warned against extrapolating the small fixture's 9/2/1/1. **It is now known — 2,707 / 1,353 / 2 — and the fixture's isogeny:`a₃` ratio of 12:1 is 1,355:2,709 at 500K.** The warning was right in direction, not only in size. `12`'s delta-only verifier and `14`'s Gate A are one operation, performed: OLD minus (isogeny ∪ `a₃`) **is** the CURRENT base, 36,687, from the columns alone, no re-run. `14`'s Gate B lists six twist-diff items; **all six are computed** — 5,437 stable curves changed, every one by `gcd(3N)` alone, 0 added, 0 both. `14`'s Gate C, the full Sage replay, comes only after A and B agree; **nobody has run it**, and the package says so in its own words.**

---

## `07`, against the diff

| `07` states | RUN-056 located in the archived diff |
| --- | --- |
| `A_old = {3 : 3∣N or ∣a₃∣=3} ∪ {5 : 5∣N} ∪ {7 : 7∣N}` | ✔ removed line, `Algorithm1_old_1a0489_to_current_31fae.diff` |
| `A_new = {3,5,7}` | ✔ added line |
| separately, `a₃(E) ≠ ±3` | ✔ `filter_CONDITION_a3` added |
| 「實質收緊，不是效能重構」 | 4,062 curves left the base — a predicate change, measured |

`07` also states the Algorithm 2 side — `gcd(M,N)=1 → gcd(M,3N)=1` and the
removal of the twist-side `disc_valuation_condition` — which RUN-060 replays.

## `11`, every number

| `11` claims | stated | recomputed |
| --- | ---: | ---: |
| git compare `+2 / −4064`, so rows removed | 4,062 | 4,062 |
| old accepted | 40,749 | 40,749 |
| new accepted | 36,687 | 36,687 |
| removed / old | 9.9683 % | 9.9683 % |
| kept / old | 90.0317 % | 90.0317 % |
| of all 3,064,705 curves | 1.3296 % → 1.1971 % | 1.3296 % → 1.1971 % |
| drop, whole domain | 0.1325 pt | 0.1325 pt |
| drop, pre-candidate pool | 2.2774 pt | 2.2774 pt |

`11` gives the pool as two percentages and never as a count. 40,749 / 0.228460 =
178,364 and 36,687 / 0.205686 = 178,364. **The same pool, to the curve.** A typo
in either percentage would have shown here.

## The histogram `11` called unknown

> 但各 gate 的精確 histogram 仍未知，不能把 `<150` 的 9/2/1/1 比例外推到 500K。

| | isogeny | `a₃` | ratio |
| --- | ---: | ---: | --- |
| `<150` fixture (`08`) | 12 | 1 | 12 : 1 |
| 500K, measured by v0.5 and recomputed at RUN-055 | 1,355 | 2,709 | **1 : 2** |

`11` was right not to extrapolate: the extrapolation would have been wrong in
**direction**. At 500K the `a₃` gate removes twice as many curves as the
isogeny gate; in the fixture it removed one in thirteen.

## `12` and `14` Gate A — one operation

| | |
| --- | ---: |
| OLD base | 40,749 |
| removed by the two columns, isogeny ∪ `a₃` | 4,062 |
| predicted CURRENT | 36,687 |
| actual CURRENT (new twist-map keys) | 36,687 |
| **set equality** | **✔** |

No re-run. `12`'s three failure meanings — a different semantic version, a
different LMFDB release, outputs from different snapshots — do not apply,
because the delta succeeded.

## `14` Gate B — six items

| item | value | where |
| --- | ---: | --- |
| 1 removed base keys | 2,707 | RUN-055 |
| 2 stable base keys | 36,687 | RUN-055 |
| 3 stable curves with twist changes | 5,437 | RUN-060 |
| 4 twists removed only by `gcd(3N)` | 5,437 curves — **all of them** | RUN-060 |
| 5 twists added after deleting the old disc gate | **0** | RUN-060 |
| 6 both-effect curves | **0** | RUN-060 |

## `14` Gate C

> 若 A、B 都和 repository current outputs 一致，再重跑所有 expensive descent。

A and B agree. C has not been run — not by this line, which does not run Sage,
and not by the package, whose `PROVENANCE.md` says a replay "is intentionally
not represented as completed here." `14`'s ordering is respected, and its stop
point is where everyone has stopped.

## The drill

**260 defects, 260 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 52 controls undisturbed, over 90 checks.

The 5 planted for this gate, each turning `one-commit-and-delta` red and nothing else:

| planted defect | went red |
| --- | --- |
| the delta is computed as OLD minus the isogeny set only, forgetting the a_3 column | `one-commit-and-delta` |
| 11's histogram warning is scored unjustified | `one-commit-and-delta` |
| 14's Gate B reports a twist added after the disc gate was deleted | `one-commit-and-delta` |
| 14's Gate C is reported done by this line | `one-commit-and-delta` |
| 07's a_3 filter is reported unlocated in the diff | `one-commit-and-delta` |


## What this round does not claim

* **Nothing about Gate C.** The descent certificates are unrun, and this round
  says so rather than scoring their absence.
* **`11`'s 3,064,705 is taken as given.** It is the size of the LMFDB range the
  paper searched; this tree has no independent count of it.
* **The pool size 178,364 is implied, not stated.** Two percentages agreeing to
  the curve is strong evidence they were computed from one number; it is not
  the number itself.
* **"Right in direction" is about the two gates' shares**, not about any
  individual curve.
