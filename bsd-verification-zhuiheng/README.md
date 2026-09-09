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
* **A gate gets a mutation drill**, and a planted defect must be caught by
  the check *named for it* — not merely by some check. A gate that has only ever
  been green is indistinguishable from a comment. **Position as of RUN-019:
  `src04`–`src10`, `src12`–`src22` are drilled — 80 defects, 80 caught by the
  named check, 19 controls undisturbed, over 36 checks. `src00`–`src03`, the corpus-scanning
  gates, are not.** This line read "every gate" for nine rounds while the tree
  had none; it is narrowed to what is true rather than the gap being left
  unsaid. Gates written after RUN-010 ship with their drill in the same commit.
* **Controls, or the drill measures nothing.** Something that must not trip.
* **`unmeasured` is a verdict.** A check that could not run has no result, and
  reporting one would be worse than not checking.
* **Numbers are emitted, never typed.** Any figure in a report traces to an
  archived gate log.

## Rounds

| round | subject | gate | headline |
| --- | --- | --- | --- |
| [001](./reports/RUN-001-CORPUS-IDENTITY.md) | where the corpus actually lives | `src00` | 85 curated docs on the site, 292 in the tree; four locations reconciled by content hash |
| [002](./reports/RUN-002-LADDER-VOCABULARY.md) | certificate-ladder vocabulary | `src01` | rung usage across all 85 documents |
| [003](./reports/RUN-003-REJECTED-ROUTE.md) | the route Phase 0 rejected | `src02` | the lattice-point rank idea does not recur after its own audit |
| [004](./reports/RUN-004-CURVE-ARITHMETIC.md) | 40,749 discriminants, 135,787 valuations | `src04` | recomputed; the fourth check reported **vacuous** rather than passed |
| [005](./reports/RUN-005-FROBENIUS-AT-THREE.md) | `a₃` over `F₃`, all 4,062 removed curves | `src05` | a bucket was holding two kinds of number |
| [006](./reports/RUN-006-THREE-ISOGENY.md) | the 3-isogeny column | `src06` | 4,062 of 4,062, and two errors of mine caught by a second derivation |
| [007](./reports/RUN-007-FIVE-AND-SEVEN-ISOGENY.md) | the 5- and 7-isogeny columns | `src07`, `src08` | all 12,186 determinations decided both ways via `X₀(n)`; zero disagreements |
| [008](./reports/RUN-008-KEPT-CURVES.md) | the 36,687 curves the census **kept** | `src09` | the direction the census's own checks are blind to; and the base is two populations |
| [009](./reports/RUN-009-PHASE2-DENSITY.md) | Phase 2 Theorem 1.1(1) | `src10` | the density is `1/24`; the obvious answer `1/48` is wrong |
| [010](./reports/RUN-010-GATE-DRILL.md) | **this arm's own gates** | `src11` | 27 defects / 27 caught by the named check — after the first run caught only 24 |
| [011](./reports/RUN-011-P5-LOCALIZATION.md) | P5 — 389.a1 at `p = 11` | `src12` | the v1.1 localization matrix `[[1,2],[1,4]]` recomputed from scratch, det `2 ≠ 0` |
| [012](./reports/RUN-012-ALGORITHM2-TWISTS.md) | Algorithm 2's twist maps | `src13`, `src11` | all 247,391 twists rebuilt, 36,687 of 36,687 lists exact; a docstring that contradicts its own code |
| [013](./reports/RUN-013-GLOBALIZER-FAITHFULNESS.md) | Phase 0's Certificate Globalizer | `src14` | all four claims hold in ℚ; the faithfulness fails in float64 at a computable index |
| [014](./reports/RUN-014-PHASE2-ANCHOR.md) | the Phase 2 anchor, 696.e1 | `src15` | `N = 696` and `r_an = 0` both computed; `L(E,1)/Ω = 1` to one ulp |
| [015](./reports/RUN-015-TWIST-FAMILY.md) | Theorem 1.1(2) and the family's structure | `src16`, `src17` | `L(E^(q),1) ≠ 0` on the two smallest members, `Ш(E^(313)) = 7²`; one of 𝒫's conditions is implied by the others |
| [016](./reports/RUN-016-TATE-AND-CONDUCTORS.md) | Tate's algorithm | `src18`, `src19` | 40,749 conductors recomputed, 0 disagreements; `c₂ = 1` closes the carve-out; the base has no additive prime in it |
| [017](./reports/RUN-017-BSD-CONSISTENCY.md) | **this arm's own analytic machinery** | `src20` | a real period wrong for three rounds, found by the rank-0 BSD identity; 285 curves close on `#Ш = 1`; `Reg(389.a1) = 0.152460306865` |
| [018](./reports/RUN-018-TWO-WITNESS-CERTIFICATE.md) | the two-witness criterion | `src21` | `[K_E:Q] = 16`, `e_E = 2`, `δ = 1/24` by exact F₂ rank — and RUN-015's redundancy **is** the factor `e_E` |
| [019](./reports/RUN-019-WITNESS-NETWORK.md) | the witness-network generalisation, and §6's stop rule turned on this arm | `src22` | `31` reaches 138 of 4,063 small models that `30` cannot, all of them failing (T5); 13 meet the whole certificate; LOO fails at 2,457 primes; RUN-017's `#Ш = 1` headline audited as **not progress** |

## Layout

| path | what |
| --- | --- |
| `code/` | gates and their drills, one `srcNN_*` per round |
| `reports/` | `RUN-NNN-*.md`, one per round, numbered with its gate |
| `data/gate-logs/` | the archived stdout of every gate — the evidence reports cite |
| `data/external/` | snapshots of anything fetched from outside this repository |
