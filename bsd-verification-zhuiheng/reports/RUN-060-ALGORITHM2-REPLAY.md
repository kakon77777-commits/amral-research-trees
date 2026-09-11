# RUN-060 — `15`'s exact replay recomputed to the cell, `09`'s two branches exercised, why the expand branch could never fire — and a correction to RUN-055

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`09_Algorithm2_Twist_Semantic_Diff`](../../../amral/public/bsd/phase1/files/09_Algorithm2_Twist_Semantic_Diff.md), [`15_Fresh_Algorithm2_Semantic_Replay`](../../../amral/public/bsd/phase1/files/15_Fresh_Algorithm2_Semantic_Replay.md)
**Tools:** [`src62_algorithm2_replay.py`](../code/src62_algorithm2_replay.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src62-algorithm2-replay.json`](../data/gate-logs/src62-algorithm2-replay.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `15` does the thing this line respects most — it refuses to re-run Sage and instead *replays* one predicate exactly on archived output. Its §4 is a 2×2 over the stable curves' generator twist pairs, `D` (passes the OLD disc gate) × `G₃` (passes `gcd(d,3N) = 1`): **247,391 / 21,306 / 0 / 0**, `|T_O| = 268,697`. Recomputed here with this tree's own transcription of the deleted predicate and its own gcd: **every cell agrees, to the pair.** So do §6's branch split — CLZ20 5,849 pairs all common, Zha16 262,848 → 241,542 + 21,306 — and §7's curve census, 31,250 / 5,437 / 0 / 0. `15` §7 observes that the expand mechanism 「在這個實際資料域沒有啟動」; **this round says why**: the deleted predicate is *vacuous on the kept base* — 0 of 36,687 curves fail it at any prime `≤ 997`, so 0 of 268,697 pairs do, and deleting a predicate nothing fails can add nothing. `09`'s synthetic Case B does fail it, so the predicate is not empty in principle, only on this data; `09`'s Case A separates the two gcd gates as claimed. **And a correction.** RUN-055 presented "the 1,355 base curves missing from the blob are exactly the isogeny set" as *identified*. `15` §8 already states that those 1,355 were added to the OLD base after the generator JSON and are all excluded by CURRENT's strict isogeny gate. RUN-055 computed the set equality and the other half — that the 2,707 `a₃` curves *are* in the blob; the identity itself was in the corpus and should have been cited. RUN-056's mechanism — the generator's rule was already strict, OLD relaxed it, CURRENT re-tightened — is what `15` does not say, and is what explains §8.**

---

## `15` §1, from the Algorithm 2 diffs

| `15` states | in the package's diff |
| --- | --- |
| `G → O` adds `D(E,d) = disc_valuation_condition` | ✔ `+def disc_valuation_condition` in `Algorithm2_generator_7286794_to_old_1a0489.diff` |
| `O → C` deletes `D` | ✔ `-def disc_valuation_condition` in `Algorithm2_old_1a0489_to_current_31fae.diff` |
| `O → C` tightens `gcd(d,N) = 1` to `gcd(d,3N) = 1` | ✔ the `-`/`+` pair on the gcd line |

The deleted predicate, transcribed for this tree from that diff:

> for every `p ∣ M`, there exists `q ∣ N`, `q ≠ p`, with `p ∤ ord_q(Δ_E)`.

E4's shape, with the outer loop over the twist's primes and the *base* curve's
valuations — RUN-055 noted the resemblance; here it is the object itself.

## `15` §4 — the 2×2, to the pair

| cell | `15` | recomputed |
| --- | ---: | ---: |
| `D=1, G₃=1` — common | 247,391 | **247,391** |
| `D=1, G₃=0` — OLD-only, removed by the factor-3 gate | 21,306 | **21,306** |
| `D=0, G₃=1` — CURRENT-only, could have been added by deleting `D` | 0 | **0** |
| `D=0, G₃=0` | 0 | **0** |
| `|T_O|` | 268,697 | **268,697** |
| `|T_C|` | 247,391 | **247,391** — and equal to the new map's size |

## §6 and §7

| | `15` | recomputed |
| --- | ---: | ---: |
| CLZ20 stable pairs, all common | 5,849 | **5,849**, and **no CLZ20 pair has `3 ∣ d`** — `p ≡ 1 (mod 4)` forbids it, as `15` notes |
| Zha16 stable pairs | 262,848 | **262,848** = 241,542 kept + 21,306 removed |
| curves unchanged / shrink-only / expand-only / mixed | 31,250 / 5,437 / 0 / 0 | **31,250 / 5,437 / 0 / 0** |

## Why the expand branch could never fire

`15` §7: 「expand mechanism 在這個實際資料域沒有啟動」 — observed. `09`: the
`<150` fixture matched exactly on all 12 curves, so neither new branch was
exercised — observed.

| | |
| --- | ---: |
| kept base curves failing `D` at some prime `p ≤ 997` | **0 of 36,687** |
| OLD pairs failing `D` | **0 of 268,697** |

A predicate nothing fails is a predicate whose deletion changes nothing. That
is the reason behind `15`'s zero, and it is a property of this base, not of the
predicate: `09`'s Case B — `v₂(Δ) = 3`, `v₅(Δ) = 6`, `p = 3` — fails `D`, and
this gate runs it and gets the rejection `09` says the old code would give.

`09`'s Case A — `N = 46`, `M = 3`: `gcd(3, 46) = 1`, `gcd(3, 138) = 3` — separates
the two gcd gates. Both of `09`'s synthetic branches are exercised here.

## Correction to RUN-055

RUN-055 wrote:

> One provenance fact came out sharp: the 1,355 base curves missing from the
> upstream twist blob are exactly the 1,355 isogeny curves … *Identified*.

`15` §8, in the corpus since before RUN-055:

> 還有 1,355 條 OLD base curves 是在 generator twist JSON 生成後才加入 OLD base
> file。它們沒有 generator twist entries … 但這 1,355 curves 全部已被 CURRENT
> Algorithm1 strict isogeny gate 排除。

That is the identity, in words. What RUN-055 added was the set equality as a
computation and the complementary half — the 2,707 `a₃`-removed curves are
*present* in the blob. What RUN-056 added is what `15` does not contain: the
generator's own Algorithm 1 rule evaluates to strict `{3,5,7}`, OLD relaxed it,
CURRENT re-tightened it, and the relaxed rule's prediction holds 1,355 of
1,355. **RUN-055 should have cited `15` §8, and a correction note is added to
its report.**

The lesson is the same one RUN-053 met with Lang–Trotter and RUN-058 is built
against: **a finding made from the data may already be in a document not yet
read.** Before the word *identified*, grep the corpus for the number.

## The drill

**260 defects, 260 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 52 controls undisturbed, over 90 checks.

The 4 planted for this gate, each turning `algorithm2-replay` red and nothing else:

| planted defect | went red |
| --- | --- |
| the deleted predicate is transcribed with ∀q in place of ∃q | `algorithm2-replay` |
| one OLD pair is dropped from the replay | `algorithm2-replay` |
| 09's Case B is reported as passing the deleted predicate | `algorithm2-replay` |
| the correction to RUN-055 is dropped: 15 §8 reported absent | `algorithm2-replay` |


## What this round does not claim

* **The replay is of `D` and `G₃` only.** `15` §2 argues the other admissibility
  gates are unchanged across the commits and need no replay; RUN-055 verified
  those gates independently on the CURRENT map, which is the other side of the
  same claim.
* **"Vacuous on the kept base" is bounded at `p ≤ 997`**, the largest twist
  prime present. A twist prime above that would be a different measurement.
* **`15` §8's historical reconstruction of the 1,355 curves' OLD twists is not
  attempted** — `15` says it would need the common gates re-run, and this tree
  agrees.
* **The correction is to RUN-055's framing**, not to its arithmetic, which
  stands.
