# RUN-027 — how much of the 85-document sweep has actually been walked, measured

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** this line's own progress — the 85 curated documents against the 26 reports and 30 gates that claim to be walking them
**Tools:** [`src29_sweep_coverage.py`](../code/src29_sweep_coverage.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src29-sweep-coverage.json`](../data/gate-logs/src29-sweep-coverage.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: 21 of the 85 documents have been the subject of a round, 8 more are cited in a report's body, and 56 are not mentioned anywhere — in any report, in any gate. The checkpoint has been carrying "Phase 1 ~22; Phase 2 ~27" as hand-written estimates for rounds; the measurement is harsher and differently shaped. The sharpest finding is Phase 1: **0 of its 25 documents are the subject of any round**, and 23 are not mentioned at all, even though RUN-004 through RUN-008 and RUN-012 verified that line's computational content down to 122,247 isogeny determinations and all 247,391 twist pairs. Those rounds named `results/summary.json`, `algorithm1_removed_census.csv` and the `has_isogeny_3` column — data artefacts — and never one `.md` in `phase1/files/`. So this arm has been conflating two senses of "walked", and only one of them is the plan's unit.**

---

## Why measure this

The plan is 85 curated documents, one per round, order and depth at this arm's
discretion. Twenty-six rounds in, the checkpoint says "Phase 1 ~22; Phase 2 ~27"
— numbers written by hand and carried forward. This arm's standing rule is that
a number in its records should be a measurement, and it had never applied that
rule to its own progress.

## Four buckets, because one would lie

"Cited" is not "verified", so a single count would overstate the sweep. Each
document lands in exactly one bucket, strongest first:

| bucket | meaning | count |
| --- | --- | --- |
| **subject of a round** | named on a report's `**Subject:**` line — a round was aimed at it | **21** |
| cited in a report | named in a report's body but not its subject | 8 |
| named only in gate code | appears in a gate but in no report | 0 |
| **not mentioned** | no round has touched it in any of those ways | **56** |

Per sub-line:

| sub-line | subject | cited | gate only | not mentioned |
| --- | ---: | ---: | ---: | ---: |
| phase0 | 7 | 0 | 0 | 3 |
| p5 | 7 | 0 | 0 | 3 |
| **phase1** | **0** | 2 | 0 | **23** |
| phase2 | 7 | 6 | 0 | 27 |

## The Phase 1 row is the finding

Six rounds went into Phase 1 — RUN-004 through RUN-008 and RUN-012. Between them
they recomputed 40,749 discriminants and 135,787 valuations, closed 122,247
isogeny determinations both ways, rebuilt all 247,391 twist pairs with
36,687 of 36,687 curves agreeing, and found four errors of their own. That work
is real and it is in this repository.

**And not one of those rounds named a document.** Their subject lines read:

> the Banwait–Huang census's removal of 4,062 base curves — `results/summary.json`
> and `results/algorithm1_removed_census.csv`
>
> the `has_isogeny_3` column of the Banwait–Huang census's removal evidence
>
> Algorithm 2's twist maps — the largest unverified artifact in the Phase 1 line

They were aimed at the **artefacts** the Phase 1 documents describe, not at the
documents. That is a defensible thing to have done — the artefacts are where the
arithmetic is — but it means the sweep, taken in its own unit, records nothing
for those documents.

**So there are two senses of "walked", and this arm has been reporting one and
counting the other:**

* the line's **computational content** verified — Phase 1 is largely done in
  this sense, and every report names the artefacts it used: 26 of 26 reports
  name at least one, 31 distinct across the line;
* the **documents read on the record** — Phase 1 has zero.

The plan's unit is the second. Neither number is presented as the other here,
and the checkpoint's estimate is replaced by both.

## Matching by stem, not by link — and why that mattered

Only **17** of the 85 documents are cited anywhere as a markdown link. The rest
are named in prose: `30_Two_Witness_Criterion_v0.1`, "Phase 0 doc 03",
`BSD_P5_uGPR_Minimal_Gate…`. A link scan would have reported a sweep roughly
four times smaller than it is.

That is the same silent under-report this tree has now produced in **four
consecutive rounds** — RUN-024's `src02` window, RUN-025's Ш vocabulary and
nested subscript, RUN-026's single-element `min`, and this scanner's first
instinct. The pattern is stable enough to name: **a scan built from the form the
author happens to remember writing, rather than from the forms the corpus
actually contains.** The remedy has been the same every time — enumerate the
alias set, print it with the result, and let a reader see what was matched on.

## What completing the sweep would now mean

56 documents untouched, of which 23 are in Phase 1 and 27 in Phase 2. Two
Phase 0 documents and three P5 documents remain. At the depth these rounds have
run, that is not 56 more rounds; several Phase 1 documents describe artefacts
already verified and would be read rather than recomputed. But the count is now
a measurement, and the plan's own unit is the one being counted.

## The drill

*(TALLY PENDING — filled from the drill log before this round is committed)*

## What this round does not claim

* **A bucket measures attention, not correctness.** Being the subject of a round
  says a round was aimed at the document; what that round settled is in its own
  *what this round does not claim* section, every time.
* **"Not mentioned" is not "not verified".** The Phase 1 row is the proof of
  that: 23 documents unmentioned while the content they describe was checked
  more thoroughly than most of the corpus.
* **The alias set is a heuristic.** It covers filenames, stems and the Phase 0
  `doc NN` form. A document referred to purely by description — "the census
  report" — is invisible to it, and would land in *not mentioned* wrongly.
* **This gate reads only this tree.** Work on the corpus done elsewhere, by
  anyone else, is outside it.
