# bsd-verification-zhuiheng

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Started:** 2026-09-08, at Neo.K's direction, as the line after Collatz.

An independent verification arm pointed at the BSD research line — an
instrument, not a co-author. It recomputes what it can reach and says plainly
what it cannot.

## What this arm does not claim

**Nothing here bears on the Birch and Swinnerton-Dyer conjecture.** No package
in the subject corpus claims to prove BSD, and this tree makes no claim the
corpus does not. Every result is of the form *"curve X, prime p, reached rung
CN"* on the corpus's own certificate ladder, which Phase 0 doc 03 defines with
**eleven** rungs:

| | | |
| --- | --- | --- |
| **C0** identity | **C1** local arithmetic | **C2** numerical analytic rank |
| **C3** rigorous analytic rank | **C4** algebraic lower bound | **C5** algebraic upper bound |
| **C6** weak BSD | **C7** single-prime strong | **C8** Sha finite and exact |
| **C9** full strong BSD | **C10** family theorem | |

Never a bare true/false verdict, because the subject does not state one.

**C2 and C3 are written out deliberately.** This README first carried the
abbreviated chain `C0 -> C6 -> C7 -> C8 -> C9 -> C10`, copied from a derived
summary without reading doc 03 — and that abbreviation drops the rung boundary
the ladder exists to hold. C2 is *numerical* analytic rank, whose own status
line in doc 03 reads `evidence` and which the framework says need not carry a
rigorous zero-order certificate; C3 is the rigorous one. Doc 03's own 絕對禁止
list forbids treating an integer returned by `rank()` as a proof.
[RUN-002](./reports/RUN-002-LADDER-VOCABULARY.md) measures where else that
abbreviation appears.

## The corpus, and where it actually lives

Established by [RUN-001](./reports/RUN-001-CORPUS-IDENTITY.md), because it was
in four places and they disagree:

| location | what | role |
| --- | --- | --- |
| `amral/public/bsd/{phase0,p5,phase1,phase2}/files/` | **85 curated `.md`** | what the public site serves; the sweep unit, one per round |
| `amral-research-trees` branch `agent/bsd` | 25 packages, **292 `.md`** + scripts, inputs, results, `SHA256SUMS.json` | the archived research, byte-exact from the drop zone |
| `amral/drops/BSD/` | the same 25 zips | the drop zone they were mirrored from |
| `我的研究/學術討論/論文/數學/BSD` | 10 items, all 2026-08-12 | an older partial copy, superseded |

**The archive is ahead of the site, not behind it.** The site's 2026-08-18 date
on Phase 2 is a curation date. Where a round needs to recompute rather than
read, the executable material is on `agent/bsd`.

## The four sub-lines

Status is each sub-line's own self-report, not this arm's gloss.

| sub-line | docs | what it is |
| --- | ---: | --- |
| **Phase 0** — Global Enclosure | 9 | The framework. Its doc 05 is a formal audit that **rejects Neo.K's own prior "lattice-point rank convergence" idea** as carrying circular-reasoning risk — verdict: archive as exploratory analogy, do not use as a proof route. |
| **P5** — 389.a1 at `p = 11` | 10 | Rank-2 curve, single prime. `Sha[11^∞] = 0` closed; several sub-lemmas closed. **The core target — bridging the analytic leading term to the algebraic regulator — is OPEN in every package**, and each says so. |
| **Phase 1** — Banwait–Huang reproduction | 25 | The 500,000-conductor algorithmic census of arXiv:2601.16044. 36,687 base curves, 247,391 admissible twist pairs. |
| **Phase 2** — 696.e1 non-semistable family | 40 | An explicit infinite twist family (density 1/24) for a case Banwait–Huang's method does not reach. Status **"DERIVED THEOREM CANDIDATE"** — deliberately not elevated to "new theorem," pending external review. |

## Where this arm expects to earn its place

The `agent/bsd` README states, about Phase 1's headline count:

> `DIRECT_PRIMARY_SOURCE` — taken from the official output and
> consistency-audited (0 mismatches found), **not independently re-derived from
> scratch**. Only 2 curves / 28 twists were independently recomputed.

Two of 36,687. That is not a doubt about the number; it is the line stating its
own evidence grade — *transcribed and cross-checked*, not *recomputed*. Closing
that gap is what an independent arm is for, and it is unusual and creditable
that the subject says it about itself before anyone asks.

## Method

Carried over from the 73-item Collatz sweep, which closed 2026-09-03:

* **Recompute; never re-run their script.** A bundle's own verifier passing
  shows the bundle is self-consistent, not that it is right.
* **Every gate gets a mutation drill**, and a planted defect must be caught by
  the check *named for it* — not merely by some check. A gate that has only ever
  been green is indistinguishable from a comment.
* **Controls, or the drill measures nothing.** Something that must not trip.
* **`unmeasured` is a verdict.** A check that could not run has no result, and
  reporting one would be worse than not checking.
* **Numbers are emitted, never typed.** Any figure in a report traces to an
  archived gate log.

## Layout

| path | what |
| --- | --- |
| `code/` | gates and their drills, one `srcNN_*` per round |
| `reports/` | `RUN-NNN-*.md`, one per round, numbered with its gate |
| `data/gate-logs/` | the archived stdout of every gate — the evidence reports cite |
| `data/external/` | snapshots of anything fetched from outside this repository |
