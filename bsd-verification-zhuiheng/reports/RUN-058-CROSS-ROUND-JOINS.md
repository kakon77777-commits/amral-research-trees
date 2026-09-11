# RUN-058 — Cross-round joins: every prime set in every log, intersected with every other, so that 3529-class findings are looked for rather than stumbled on

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** this line's own 59 archived gate logs — not a corpus document
**Tools:** [`src60_cross_round_joins.py`](../code/src60_cross_round_joins.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src60-cross-round-joins.json`](../data/gate-logs/src60-cross-round-joins.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: RUN-057's finding — member 3529 of the family is an ordinary H2-obstruction prime of the base — had both halves sitting in archived logs for seventeen rounds, unjoined, because a line that reads one document per round never asks whether a set computed in one round meets a set computed in another. This gate asks mechanically. It walks all 59 logs, collects every integer list that is mostly primes and not entirely small (**100** of them), drops the two shapes that are never findings — an intersection inside the scaffolding every gate tests (Mazur's twelve and 29) and a join against a plain initial segment of primes — and intersects the rest pairwise across logs: **325 non-empty intersections**. A join counts as *made* only if some single report names every number **and** references both source rounds; **218** are not — after this report exists, which itself makes 36 of them. **The 3529 join is in the table** — 38 rows contain 3529, 6 touch RUN-038's log — which is the one thing a joins gate must be able to find, or it measures nothing. **And of the 218, none is a new finding.** The largest rows are the base curve's ordinary obstruction primes meeting its surjectivity certificate — global and local facts that coexist, and that RUN-041 already joined by name — and four members of `𝒫` appearing among P5's 23 Kolyvagin-type directions for a *different curve*, which two conditions both favouring primes `≡ 1` mod small moduli explain. That is the right result for a tree that has been careful, and it is now certified rather than assumed. From this round on the gate runs in the drill, so the next join of this class is found by the instrument.**

---

## Why an instrument, and not a habit

RUN-038 computed the set `{7, 113, 211, 1433, 1811, 2693, 3209, 3529}`.
RUN-047 computed the set `𝒫` below 4,000 three ways. RUN-035 recorded `03`'s
Lemma B. RUN-046 made `10`'s congruence the whole of H2 at `p ≥ 5`. Their
intersection at 3529 — and what it means through Lemma B — waited until
RUN-057.

A habit of "look for overlaps" would have caught it, if remembered. An
instrument catches it whether or not anyone remembers. This gate is the
instrument, and its first run doubles as the measurement of how many such
joins were still waiting: **none**.

## What it does

| stage | count |
| --- | ---: |
| integer lists found in 59 logs that are ≥ 80 % primes and not entirely below 50 | **100** |
| dropped as constants (identical in ≥ 4 logs) | 0 |
| pairwise intersections across different logs, non-empty | — |
| minus intersections inside `{2,3,5,7,11,13,17,19,37,43,67,163} ∪ {29}` | — |
| minus joins against an initial segment of primes (a sieve's `primes_tested`) | — |
| minus containments (one set inside the other is a re-read, not a join) | — |
| **surviving intersections** | **325** |
| of those, *made* — some report names every number and both source rounds | **107** |
| **not made** | **218** |

The "made" test is deliberately strict. A report can name a number as a member
of its own round's list without ever meeting the other round; RUN-038's report
names 3529 as an obstruction prime, RUN-047's names it as a member, and
neither joins them. So the test requires one report that carries the numbers
**and** references both rounds — its own round counting as a reference.

## The known join is in the table

| | |
| --- | ---: |
| rows whose intersection contains 3529 | **38** |
| of those, touching RUN-038's log | **6** |

Example row: `src40 :: no_finite_exception.buckets[2].failures` ∩
`src49 :: three_definitions_of_P.per_18_and_27` = `{3529}`. After RUN-057's
report exists it is marked *made*; had this gate run before RUN-057, it would
have been the top unmade row. That is the calibration.

## The 218 that are not made, read

| intersection | between | what it is |
| --- | --- | --- |
| `{7, 113}` and `{7, 29, 113}`, many rows | RUN-038 / RUN-041's ordinary obstruction primes ↔ RUN-036 / RUN-049's surjectivity-certified primes, RUN-045's not-applicable primes | a global fact (surjective mod `p`) and a local fact (`a_p ≡ ±1`) that coexist. RUN-041 already named `P_loc` as RUN-038's set; the rows here pair it with *other* rounds' re-reads of the certified list |
| `{2113, 9769, 16633, 18217}` | RUN-016's 87 family members below 20,000 ↔ RUN-023's 23 admissible Kolyvagin directions for **389.a1 at `p = 11`** | a different curve and a different theorem; both conditions favour primes `≡ 1` mod small moduli, so 4 of 23 landing in `𝒫` is overlap, not a join |
| `{17, 37, 41, 157}` | RUN-045's FW-applicable primes ↔ RUN-047's redundancy tally | small primes appearing in two unrelated bookkeeping lists |
| `{2, 113}`, `{3, 113}`, `{2, 103}`, `{197}` | RUN-019's witness network ↔ RUN-036 / RUN-045 / RUN-049 | the witness network's primes meeting later certification ranges; 197 is one of RUN-045's 7 `UNKNOWN` primes, which says only that RUN-019 used a prime RUN-036 did not reach |

**None is a finding.** Each is either two rounds reading the same upstream fact
under different names, or two unrelated conditions overlapping at the density
one would expect.

### This report makes joins by existing

The first run, before this report was written, counted **254** unmade joins.
The second, with the report in `reports/`, counted **218**. Nothing in the logs
changed. The report names `{7, 113}` beside RUN-038, RUN-041 and RUN-036, and
names the P5 overlap beside RUN-016 and RUN-023 — and that is exactly what
"made" means. **The document that describes the unmade joins is the document
that makes them.** The figures above are the fixpoint, the same on a third run,
and the drill check asserts nothing about them.

## What the gate asserts, and what it leaves to a reader

It asserts three things: at least 20 prime sets were found, at least one
intersection survived, and **the 3529 join is present — specifically the row
where RUN-038's obstruction list meets a membership list of `𝒫`**.

That last clause was sharpened by the drill. The first version accepted any row
containing 3529 that touched RUN-038's log, and a planted defect that inverted
the containment filter — keeping re-reads, dropping real joins — went
**uncaught**, because RUN-057's log re-reads RUN-038's list and the containment
row between them survived. A known-join test that a re-read can satisfy is not
a test of joins. It now requires the other side to be `src49` or `src16`. It does not assert a count of unmade joins — that number is a
measurement the next round is meant to change, and a check that froze it would
be the mistake this line named at RUN-026.

Everything else is a table for a reader. An intersection is a *candidate*.
Most candidates are noise. The ones worth a round are where two different
**computations** meet at a number neither expected — the way RUN-038's
obstruction list met RUN-047's membership list.

## The drill

**243 defects, 243 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 49 controls undisturbed, over 86 checks.

The 4 planted for this gate, each turning `cross-round-joins` red and nothing else:

| planted defect | went red |
| --- | --- |
| the scaffolding filter is widened to every prime below 200,000, so no intersection survives | `cross-round-joins` |
| RUN-038's log is skipped by the scan, so the 3529 join cannot be found | `cross-round-joins` |
| the containment filter is read backwards: re-reads are kept and real joins dropped | `cross-round-joins` |
| the small-prime floor is raised to 4,000, so every set below it — RUN-038's obstruction list included — is discarded | `cross-round-joins` |


## What this round does not claim

* **Not that the tree has no unjoined findings.** It has none of the shape this
  gate can see — integer lists of primes. A join between two *rational* values,
  or between a prime and a curve label, is invisible to it.
* **The filters are judgement.** Mazur's twelve and 29 as scaffolding, 50 as the
  small-prime floor, 80 % as the prime fraction — a different reading would move
  325 and 218. The 3529 row survives every reasonable setting, and that is the
  one the gate is held to.
* **"Not made" is not "wrong".** It means no single report carries the numbers
  together with both rounds. The `P_loc` identity, for instance, *is* made in
  RUN-041 — the rows here pair `P_loc` with rounds RUN-041 did not cite.
* **The P5 overlap is explained, not measured.** That both conditions favour
  `≡ 1 (mod 24)`-type primes is a reading of their definitions; the expected
  overlap density is not computed here.
