# RUN-050 — The novelty rule this arm cannot advance, and the route matrix it does not follow

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`26_Novelty_Search_Log`](../../../amral/public/bsd/phase2/files/26_Novelty_Search_Log.md) and [`01_Phase2_Route_Matrix`](../../../amral/public/bsd/phase2/files/01_Phase2_Route_Matrix.md) — two documents about discipline rather than arithmetic
**Tools:** [`src52_novelty_and_routes.py`](../code/src52_novelty_and_routes.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src52-novelty-and-routes.json`](../data/gate-logs/src52-novelty-and-routes.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `26`'s box — **`NO HIT ≠ NOVELTY PROOF`** — is the finding, and it stands. It lists four things that must happen before priority is claimed, and **this arm can do none of them**: all four are searches against external literature databases, this tree has no external access, and the standing rule forbids routing unpublished AMRAL work to a third-party provider while it lives only on GitHub. So the box is reported as *not scoreable here*, which is what it is. Across 50 reports, **21 sentences carry a novelty term: 11 are refusals and 10 are classified quotations** — a first, cruder version of the scan called the five quotations it then saw assertions, which is RUN-027's failure mode again, so every quotation is now pinned with its reason and any new unaccounted mention turns the check red. **No round of this line claims novelty.** And `01`'s route matrix, measured against what this line ran: its **PRIMARY GO** route is the most covered (**8 of 8** mapped documents), its **STOP** route is untouched — and **two rounds worked routes marked HOLD and *separate Phase later***, RUN-026 on rank 1 and RUN-023 on rank 2. That is named rather than defended: `01` orders routes by extensibility of the family theorem, a verification arm orders by what has been written down, and the two orderings are different on purpose.**

---

## `26`'s box, and why it cannot be scored here

`26` searched arXiv for the curve, the equation, and the family, found nothing
directly matching, and then wrote the only sentence that governs what may follow:

$$\boxed{\text{NO HIT}\neq\text{NOVELTY PROOF}}$$

with four things still required before priority is claimed:

1. MathSciNet / zbMATH / Google Scholar citation chaining;
2. searching Fouquet–Wan's citing papers;
3. a number theorist checking whether it is a direct corollary of something
   general;
4. checking the 2026 preprints.

**This arm can do none of the four.** They are literature work against external
databases; this tree has no external access; and the standing rule on unpublished
AMRAL research forbids sending it to a third-party provider while it exists only
on GitHub. The honest report is that the box is **not scoreable here** — not that
it passed, and not that it failed.

`28_Submission_Gate` listed five boxes and RUN-030 delivered the one that was
this arm's. This is another that is not.

## No round of this line claims novelty

| | |
| --- | ---: |
| reports scanned | **50** |
| sentences carrying a novelty term | 21 |
| refusals | **11** |
| classified quotations | **10** |
| unaccounted | **0** |

Five of the quotations are `RUN-019` quoting Phase 0's freeze rule, `RUN-030`
quoting `28`'s checklist and its own "not ours" column, and three in `RUN-047`
reporting what `27` defers and what labels the documents carry.

**The other five are in this report.** A round that audits the novelty rule
cannot avoid naming it — the subject line, the box, and the scan's own tally row
all trip the term. They are pinned individually like the rest: **a round that
exempted its own report would have written itself a loophole**, and the check
would then be blind to exactly the document most likely to overclaim.

**A first version of this scan called every one of the first five an
assertion.** A crude refusal-word test cannot tell a quotation from a claim,
which is exactly the pattern RUN-027 named after four rounds of it: *a scan built
on the shapes the author remembers writing rather than the shapes the corpus
contains*. Rather than widen the word list until the red went away, each
quotation is pinned with its reason — and **any new unaccounted mention turns the
check red**, which is how this round's own five were found.

## `01`'s routes, against what this line ran

| route | verdict | documents this line made a subject |
| --- | --- | ---: |
| Higher 2-power descent | **STOP as mainline** | — |
| Non-semistable + odd-`p` patchwork | GO as baseline | **4 of 4** |
| Fouquet–Wan arbitrary reduction | **PRIMARY GO** | **8 of 8** |
| BCS ordinary non-semistable | supporting | **1 of 1** |
| Full rational 2-torsion | HOLD | — |
| Analytic rank 1 | HOLD | — |
| Prime conductor | niche | — |
| High rank 2+ | separate Phase later | — |

The mapping of documents to routes is a reading, not a field in the corpus; what
is computed is the count given that reading, and the gate says so.

The shape is what it should be: the primary route is where the documents are and
where the rounds went, and the route marked STOP has no documents and no rounds.

## Two rounds on routes the matrix does not prioritise

| round | route | verdict | what it did |
| --- | --- | --- | --- |
| **RUN-026** | Analytic rank 1 | **HOLD** | the rank-1 BSD identity at 37a1 and 43a1, closed with every term computed in this tree |
| **RUN-023** | High rank 2+ | **separate Phase later** | the rank-2 identity at 389.a1, closing at ratio 1.0 |

Neither was an attempt to extend the family theorem. Both verified an identity a
document stated, which is what this arm is for — and RUN-026 is the round that
found `canonical_height` returning its worst extrapolation level, which corrected
a regulator this line had been carrying since RUN-017.

**`01` orders routes by extensibility; a verification arm orders by what exists
and is checkable.** Those are different orderings and neither is wrong. The
measurement is worth making because assuming they agree would be a way of
mistaking a project plan for a work log.

## The drill

**200 defects, 200 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 39 controls undisturbed, over 78 checks.

The 4 planted for this gate, each turning `novelty-and-routes` red and nothing else:

| planted defect | went red |
| --- | --- |
| 26's box is reported as a step this arm can take | `novelty-and-routes` |
| the classified novelty quotations are unpinned | `novelty-and-routes` |
| 01's STOP route is reported covered | `novelty-and-routes` |
| the two rounds on non-prioritised routes are hidden | `novelty-and-routes` |


## What this round does not claim

* **Nothing about novelty.** `26`'s box is reported, its four steps are listed as
  outside this arm's reach, and no verdict is offered.
* **The route mapping is a reading.** Assigning corpus documents to `01`'s eight
  routes is judgement; only the counts are computed, and a different reading
  would move them.
* **Coverage is not merit.** That the PRIMARY GO route is best covered says where
  the documents are, not that the work there is more valuable.
* **The novelty scan reads sentences, not meaning.** It checks that every
  novelty-term sentence is a refusal or a pinned quotation; a claim phrased
  without any of the four terms would pass it unseen.
* **`01`'s verdicts are the corpus's**, not this arm's. Whether STOP is the right
  call for higher 2-descent is not a question this round examines.
