# RUN-029 — §Q9's twist accounting, every term measured, and the 1,355 placed

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`V0_5_EXACT_CENSUS_REPORT`](../../../amral/public/bsd/phase1/files/V0_5_EXACT_CENSUS_REPORT.md) §Q9 and §Q4, against the two twist artefacts on the archive branch — the open item RUN-028 named one round ago
**Tools:** [`src31_q9_census_closure.py`](../code/src31_q9_census_closure.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src31-q9-census-closure.json`](../data/gate-logs/src31-q9-census-closure.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: §Q9's global accounting identity is now verified with every one of its eight terms measured directly from the artefacts, not four measured and two back-solved. `old_total_twist_pairs = 293,482` and `upstream_removed = 24,785` — the two RUN-028 named as the cheapest open item in Phase 1 — are both confirmed, and so are `stable_removed = 21,306`, `stable_added = 0` and `newbase_added = 0` by direct set difference over 39,394 old and 36,687 new labels. The counting rule was **calibrated on a number this tree had already verified** rather than chosen: the trivial-twist-inclusive sum over the new artefact is 247,391, which is what RUN-012 rebuilt, while the exclusive sum is 210,704. And a third value from RUN-028's absent list is placed: the `1,355` a replay document could not rebuild is exactly `40,749 − 39,394`, the base curves with no twist entry at all.**

---

## The item this closes

RUN-028 checked §Q9's identity as arithmetic and found four of its six
independent inputs already computed by this tree in RUN-012. It named the other
two and said the identity ties them, so one measurement would close both. That
was true, and it would have left the identity a **tautology in those two
terms** — an equation cannot check numbers that were derived from it.

Both twist artefacts turn out to be on the archive branch:

```
origin/agent/bsd:bsd/BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12/inputs/{old,new}/twists_of_ec_labels_500k.json
```

so every term is measured and nothing is inferred.

## The counting rule is calibrated, not assumed

The artefact maps each label to its list of twist discriminants **including the
trivial `d = 1`**, so "twist pairs" could mean the sum of list lengths or that
minus one per label. Over the new artefact those are:

| rule | value |
| --- | --- |
| counting the trivial twist | **247,391** |
| excluding it | 210,704 |

RUN-012 rebuilt **247,391** pairs. So the document counts the trivial twist, and
that rule is then applied unchanged to the old artefact. **The rule is fixed by
a number this tree had already verified, not chosen to make the old count come
out right** — which is the difference between a calibration and a fit.

## Every term, measured

| label sets | count |
| --- | --- |
| old | 39,394 |
| new | 36,687 |
| dropped | 2,707 |
| **added** | **0** |

| term | measured | stated | |
| --- | ---: | ---: | --- |
| `old_total_twist_pairs` | **293,482** | 293,482 | ✓ |
| `new_total_twist_pairs` | 247,391 | 247,391 | ✓ |
| `lhs` | 46,091 | 46,091 | ✓ |
| `upstream_removed` | **24,785** | 24,785 | ✓ |
| `stable_removed` | 21,306 | 21,306 | ✓ |
| `stable_added` | 0 | 0 | ✓ |
| `newbase_added` | 0 | 0 | ✓ |
| `rhs` | 46,091 | 46,091 | ✓ |

`lhs = rhs` ✓, and now that is a **check** rather than a definition of its last
two terms.

The label arithmetic is its own confirmation of RUN-008: the new artefact has
36,687 labels, exactly the kept set that round closed both ways, and 0 labels
were added — the same emptiness RUN-012 measured on the expansion branch, seen
here from a different direction.

## The 1,355, placed

RUN-028's absent list carried `1,355`, from a replay document reporting a set of
that size it could not rebuild without re-running Algorithm 2. It is

$$40{,}749 - 39{,}394 = 1{,}355,$$

the base curves from RUN-004's census that have **no entry in the twist artefact
at all**. So the twist file does not cover the whole base, and the shortfall is
exactly the figure the replay document reports. That takes RUN-028's eight
unplaced values to five, and the three closed here were the only ones that were
census arithmetic — the rest are a scope bound, a year range, two git-diff line
counts and one real count of a different kind.

## The drill went red on the baseline, and the reason was mine

RUN-027's `sweep-coverage` check froze two **measurements** as invariants:
"Phase 1 subjects must be 0" and "link matching must find at most 17". RUN-028
and RUN-029 name `V0_5_EXACT_CENSUS_REPORT` on their subject lines and link it,
so both numbers moved — and the check failed on the baseline, **on success**.

A check that freezes a measurement the work is meant to change will fail exactly
when the work succeeds. RUN-027's Phase 1 row was that round's **finding**, not
an invariant. Both assertions are replaced: the classifier's ability to separate
the four buckets is asserted on a fixture whose answer is fixed by construction,
and the link comparison asserts the **relation** the round actually claimed —
stem matching finds strictly more — rather than yesterday's absolute.

**121 defects, 121 caught by the check named for each — none uncaught, none
caught by the wrong check. 20 controls, none disturbed, over 57 checks.
Twenty-one minutes and forty-nine seconds, on the second run.**

## What this round does not claim

* **Agreement with the artefacts is not agreement with reality.** These counts
  say the report describes the files it shipped with. If both were generated by
  the same wrong process, this round would not see it — what it rules out is a
  report whose numbers do not match its own inputs.
* **The artefacts are taken as given.** Their provenance is the archive branch,
  recorded here by blob id; RUN-001 established that branch's relationship to
  the drop zone by content hash, and nothing further is claimed about how the
  files were produced.
* **`stable_removed` counts discriminants, not curves.** The decomposition is
  over (label, twist) pairs throughout, which is the unit §Q9 uses.
* **Nothing here bears on BSD.** It is a census audit, and its value is that the
  Phase 2 line stands on this base.
