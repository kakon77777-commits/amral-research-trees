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
  been green is indistinguishable from a comment. **Position as of RUN-069:
  every gate is drilled — `src00`–`src10` and `src12`–`src71`, 294 defects, 294
  caught by the named check, 60 controls undisturbed, over 97 checks.** RUN-026's
  first run went **red**, and the two things it found are in that round's report:
  a control whose stated reason had been a consequence of the defect that round
  repaired, and a defect the repaired computation had learned to route around. This
  line read "every gate" for nine rounds while the tree had none; RUN-010
  narrowed it to what was true, and it carried "the corpus-scanning gates are
  not" for fourteen rounds after that. RUN-024 closed it, and drilling those
  four found a check in `src02` that was structurally incapable of firing.
  Gates written after RUN-010 ship with their drill in the same commit.
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
| [017](./reports/RUN-017-BSD-CONSISTENCY.md) | **this arm's own analytic machinery** | `src20` | a real period wrong for three rounds, found by the rank-0 BSD identity; 285 curves close on `#Ш = 1`; `Reg(389.a1) = 0.152460306865` — **corrected to `0.15246013936831948` by [026](./reports/RUN-026-RANK1-BSD-IDENTITY.md)** |
| [018](./reports/RUN-018-TWO-WITNESS-CERTIFICATE.md) | the two-witness criterion | `src21` | `[K_E:Q] = 16`, `e_E = 2`, `δ = 1/24` by exact F₂ rank — and RUN-015's redundancy **is** the factor `e_E` |
| [019](./reports/RUN-019-WITNESS-NETWORK.md) | the witness-network generalisation, and §6's stop rule turned on this arm | `src22` | `31` reaches 138 of 4,063 small models that `30` cannot, all of them failing (T5); 13 meet the whole certificate; LOO fails at 2,457 primes; RUN-017's `#Ш = 1` headline audited as **not progress** |
| [020](./reports/RUN-020-P5-LOCAL-UNITS.md) | P5's explicit local-unit cancellation at `389.a1`, `p = 11` | `src23` | every boxed statement of v0.8 reproduced, including `v₁₁(t(16P′)) = 1` on a 38-digit point — and `R ↦ [t(16R)/11]` is a **homomorphism** with an index-11 kernel, so §6's valuation clause is basis-dependent while its rationality equivalence is not |
| [021](./reports/RUN-021-P5-STATUS-LEDGER.md) | the P5 chain's status ledger, reconciled across ten documents | `src24` | 44 rows, 39 gates, 5 with two statuses and **all five explained**; the blocking graph is acyclic; `P5-LAT11 BLOCKED BY … GPR11` is **ambiguous between three declared gates**; and `P5-BOC-NZ11` and `P5-RESIDUAL-IRR11` are closed **here** by this tree's own computation rather than by the ledgers' citation |
| [022](./reports/RUN-022-P5-CORE-VERTEX.md) | P5's norm-Selmer core vertex | `src25` | the cube reproduced exactly — and §3's `Sel = 0`, §5's transversality and `v1.3`'s `det(𝓑_N) ≠ 0` are **one determinant three times**; `{397, 991}` is **not special**, 230 of 253 admissible pairs give a core vertex |
| [023](./reports/RUN-023-RANK2-BSD-IDENTITY.md) | the rank-2 BSD identity at `389.a1` | `src26` | `L′′/2! = Ω·Reg` closes at **ratio 1.0** with this arm's own period — the **first external test** of RUN-017's `Δ > 0` repair; the period confirmed again by integrating both real components, which agree to `5.8e−12` |
| [024](./reports/RUN-024-CORPUS-GATES-DRILLED.md) | the last four undrilled gates, `src00`–`src03` | `src11`, `src02` | **every gate is now drilled**; drilling them found `src02`'s salvage detector was **structurally incapable of firing** — a same-line window that could never reach a verdict four lines away, and a vocabulary that read `未滿足` as `滿足`; now 6 stated unmet, 0 claimed met, 0 unread |
| [025](./reports/RUN-025-AGENT-EXPERIMENT-AUDIT.md) | the Phase 1 agent experiment against its own §6/§7 conditions | `src27` | the freeze condition 「將 analytic Ш 當 actual Ш」 is **not triggered** — 36 numeric Ш claims, all labelled, 5 of them **in the notation itself**; and the scanner needed **three corrections** before it measured anything |
| [026](./reports/RUN-026-RANK1-BSD-IDENTITY.md) | the rank-1 BSD identity, and this tree's height extrapolation | `src28`, `src20` | the identity closes at `37a1` and `43a1` with **every term computed here**, ratios `1.0000000017` and `1.0000000009`; and `canonical_height` was returning the **worst** of its three extrapolation levels, which corrects RUN-017's regulator precision by two orders of magnitude |
| [027](./reports/RUN-027-SWEEP-COVERAGE.md) | this line's own progress, measured | `src29` | of the 85 documents **21 are the subject of a round, 8 are cited, 56 are not mentioned anywhere**; **Phase 1 has 0 subjects** although six rounds verified its arithmetic — they named the artefacts, never the documents |
| [028](./reports/RUN-028-PHASE1-NUMERIC-CROSSCHECK.md) | Phase 1's stated arithmetic against this tree's own | `src30` | 15 of 23 stated integers appear in our gate logs; **§Q9's accounting identity checks out and four of its six inputs are ours**, the two that are not being tied so one measurement closes both; and the round's own scanner failed in **both** directions |
| [029](./reports/RUN-029-Q9-CENSUS-CLOSURE.md) | §Q9's twist accounting, measured | `src31` | **all eight terms measured from the artefacts**, so the identity is a check and not a definition of its last two; the `1,355` RUN-028 could not place is `40,749 − 39,394`; and a check of mine went red **on success**, having frozen a finding as an invariant |
| [030](./reports/RUN-030-696E1-CERTIFICATE.md) | the machine-checkable arithmetic certificate for `696.e1` | `src32` | `28_Submission_Gate`'s fourth box **delivered** — 20 quantities each recomputed from the a-invariants alone; the first draft quoted its author and **three of three were wrong**; and the drill's state guard caught a memo that outlived the defect it was computed under |
| [031](./reports/RUN-031-MAZUR-DEGREES-CLOSED.md) | Mazur's twelve isogeny degrees, for `696.e1` and every twist of it | `src33` | **all twelve settled** — eleven refuted by an explicit witness prime, and `n = 2`, where the sieve is **structurally vacuous**, settled by `X₀(2)`; the refutation transfers to the whole family, identical on 27 of 27 good primes across three twists with 14–16 sign flips in `a_ℓ`; and a drill control's stated reason turned out **false at `n = 2`** |
| [032](./reports/RUN-032-REFEREE-A-CHECKLIST.md) | Referee A's checklist, run as a program | `src34` | **PASS over the four of seven base lines that are arithmetic**, the other three reported as *cited* rather than scored; all 19 support-set members pass all five `q` conditions; and 200 primes the membership test **rejects** were put through the checklist — 0 pass, so the checklist and `𝒫` agree about who is in the family |
| [033](./reports/RUN-033-GCD-WITNESS-LEMMAS.md) | the GCD witness lemmas under both prime routers | `src35` | all three run with **computed inputs** — 3 split, 29 **nonsplit**, `n_ℓ = 1` each, every gcd 1; the nonsplit restriction leaves **one witness and no spare**; and a searched-for curve where **lemma 1 passes while lemma 3's gcd is 0**, because the gcd of an empty set is 0 and every prime divides 0 |
| [034](./reports/RUN-034-KODAIRA-NOGO-DOMAIN.md) | `05`'s one exact no-go, and where it can fire | `src36` | the no-go **never fires in this family**, and `𝒫`'s own `gcd(q, 696) = 1` is why — firing at `d` needs the base multiplicative at `d`, measured to be exactly `{3, 29}`; and `p = 3`'s character argument is measured **special to 3 among odd primes** |
| [035](./reports/RUN-035-TWIST-INVARIANCE-BRIDGE.md) | the quadratic-twist invariance bridge, lemma by lemma | `src37` | lemma C measured on **both** sides — preserved at every split conductor prime on 19 of 19 members, and the split flag **flips** at an inert one; `ℓ = 2` reported **untestable** after 139 inert `d`, not passing; and RUN-033's lone FW-H3 witness is kept alive by exactly `𝒫`'s split condition, since `d = 17` would turn 29 split. **Lemma B is where the document leaves it, so the bridge is not established** |
| [036](./reports/RUN-036-MOD-ELL-SURJECTIVITY.md) | `24_Manin_Period_Audit`'s asserted "mod-`ℓ` images maximal for all `ℓ`" | `src38` | **surjectivity certified at `ℓ = 2` and every prime `5 ≤ ℓ ≤ 167`** — 38 in all, six maximal classes refuted each by a named Frobenius; **11 of Mazur's twelve** rise from irreducible to surjective; and `ℓ = 3` is blocked by two **structural** facts, `PGL₂(F₃) ≅ S₄` and a nonsplit-Cartan test that is vacuous mod 3 |
| [037](./reports/RUN-037-FW-H3-COMPILER.md) | `09_FW_H3_Exact_Compiler`'s boxed uniform certificate | `src39` | the premise holds — `W₋ = {29}`, `g₋ = 1 = 2⁰` — and the boxed **`∀p>2, FW-H3 = PASS` is false at `p = 29`**: the gcd argument never sees the `ℓ ≠ p` clause, which empties a singleton `W₋`. The family theorem survives, and that is computed too — 29 is routed to P3, whose witness `ℓ = 3` is **split** and so was never available to FW-H3 |
| [038](./reports/RUN-038-FW-H2-ORDINARY.md) | `10`'s ordinary obstruction and the branch FW is left | `src40` | the exact criterion `a_p² ≡ 1 (mod p)` run over 780 good primes: **8 ordinary primes fail H2**, every one with `a_p = ±1`, spread across the range — so no finite exception list can cover them, which is the document's own reason for the routing; the FW branch is **6 supersingular primes**, H3 cleared at each, and RUN-037's exception provably cannot reach them |
| [039](./reports/RUN-039-DERIVED-SUPERSINGULAR-BRIDGE.md) | `11`'s derived supersingular FW bridge, assembled | `src41` | all three residual hypotheses at **6 good supersingular primes** — H3 computed with witness `ℓ = 29`, H1 and H2 kept marked *cited*; `L(E,1) = 1.6317…` recomputed; and `11`'s uniform form is shown true where RUN-037 found `09`'s false — **the same gcd, one quantifier apart**, since `W₋` is made of bad primes and this range is good ones. `c_E = 1` stays **OPEN**, named in the log |
| [040](./reports/RUN-040-ODD-ADDITIVE-BARRIER.md) | `01`'s odd-additive period barrier | `src42` | empty for the base (its only additive prime is 2); each member meets it at exactly `q`, where the twist **forces** `(v(c₄), v(c₆), v(Δ)) = (2,3,6)` — Kodaira `I₀*`, never II/III/IV — so `01`'s condition holds 19 of 19; the excluded types are **constructed** and the condition fails at each; `p ∤ c` is the weaker piece RUN-039's `c_E = 1` was avoiding |
| [041](./reports/RUN-041-FINITE-EXCEPTIONAL-PRIMES.md) | Phase 2's mother problem, with all three sets computed | `src43` | `P_red = ∅` **universally** (Mazur + RUN-031 + RUN-036), `P_ram = ∅` by the document's formula, `P_loc` **not** empty and not stopped — so `04`'s criterion is **not achieved for all odd `p`**, blocked by `P_loc`; the family theorem does not need it, the blocking primes being ordinary and computed **disjoint** from the FW branch; and `04`'s own warning that its `P_ram` formula is a heuristic turns out **exact** — it misses precisely the `ℓ ≠ p` clause RUN-037 found |
| [042](./reports/RUN-042-BASE-CERTIFICATE-COMPARE.md) | the corpus's own base certificate, row by row | `src44` | **22 rows: 17 recomputed here, all agree; 5 marked not computable rather than scored**; and the 2-division cubic needed comparing by **square class** — `15`'s `disc = −11136` and RUN-036's `−45,613,056` differ by `64²`, so a value comparison would have reported a disagreement between two correct models; the document's refusal of the circular `Ш` inference is **read from the file**, not assumed |
| [043](./reports/RUN-043-CLAIM-LADDER-POSITION.md) | this line's own position on `07`'s claim ladder | `src45` | **C1, and partial** — H2 and H3 have exact executable meaning here, **H1 is cited**, and **C2 is not reached at all**: this arm checks residual hypotheses and cites the theorem that consumes them, and reporting higher would be `07`'s own fifth forbidden upgrade. All five forbidden-upgrade guards audited **against the archived logs, not the prose**; the three-round stop rule **not triggered**; 42 of 42 reports carry an explicit limits section |
| [044](./reports/RUN-044-CHEBOTAREV-AUDIT.md) | `25`'s density derivation, every field-theoretic step | `src46` | `disc(f₂) = −11136`, `F₀ = Q(√−174)`, `Q(√−6) ⊂ Q(ζ₂₄)` but `Q(√29)` not, `[K:Q] = 16`, `S₃`'s single nontrivial proper normal subgroup, `[LK:Q] = 48`, class size 2, **`δ = 1/24`** — and the compatibility is shown **against a transposition, where it fails and the density would be 0**. Three routes to `1/24`: this one, RUN-018's `e_E/(3[K_E:Q])`, RUN-009's measurement |
| [045](./reports/RUN-045-FW-HYPOTHESIS-COMPILER.md) | `02`'s hypothesis compiler, Levels 1 and 2 | `src47` | the Level-1 certificate emitted **in the document's own keys** for 45 odd primes — 34 `FW_APPLICABLE`, 4 `FW_NOT_APPLICABLE`, 7 `UNKNOWN`, every deviation an earlier round arriving (`p = 3` H1, `p = 7, 113` H2, `p = 29` H2+H3); Level 2 **not achieved**, so the gate emits the mandated *FW verified for tested primes* and nothing more; and `02`'s third prohibition turns out **contested** by `08` |
| [046](./reports/RUN-046-H2-CHAIN-AND-H3-DISPUTE.md) | the H2 chain's consistency, and the corpus's own H3 disagreement | `src48` | `03`'s Jordan–Hölder lemma and `08`'s ratio test verified **the same statement over 22,140 character pairs, 0 mismatches**; `10`'s single congruence is complete at every good ordinary `p ≥ 5` and **not at `p = 3`**, because `χ_cyc²` is unramified exactly when `p − 1 ∣ 2`; and **`02` forbids equating the divisibility criterion with H3 while `08` and `09` do exactly that** — reported, not resolved |
| [047](./reports/RUN-047-PROVISIONAL-VS-REVISED.md) | the derived theorem before and after the referee | `src49` | **three definitions of `𝒫`, one set** — `18`/`27`'s three conditions, this tree's test and Referee A's five all give the same 19 primes below 4,000 and 23 below 5,000; **one of the document's conditions is implied by the other two** (RUN-018 knew, over a range fifty times wider — what is new is that it sits in the corpus's own definition); of `18`'s five referee items `27` answers one, defers one, leaves three; and `27`'s six-branch router is a **partition**, with the witnesses it names computed here from the other end |
| [048](./reports/RUN-048-CANDIDATE-SCHEMA-AND-SIEVE.md) | `13`'s schema and `14`'s sieve, control included | `src50` | `14`'s odd local table recomputes exactly; the control is **found by conductor, not quoted**, and **has a nonsplit prime and still fails** — one reservoir, no distinct witness at `p = 29`, which is `14`'s whole point and RUN-033's lemma 2 returning nothing for the first time; `13`'s B1/B2 are RUN-033's lemma 1 and RUN-037's premise under other names; of its six obligations **1 cited, 3 partly, 2 open, none closed** |
| [049](./reports/RUN-049-SOURCE-AUDITS.md) | the corpus's own source audits, audited | `src51` | **two of this arm's conclusions move**: `23` quotes the exact local condition RUN-046 said this arm did not hold, and its weight-2 specialisation `a_ℓ = −1` checks out (`a₂₉ = −1` nonsplit, `a₃ = +1` split) — so the derivation `02` asked for is in the corpus, and `18`'s first referee item is **addressed**, not open. And **`22` invokes maximality where Skinner C lists irreducibility** — the stronger premise is the one RUN-036 could not certify at 3, and `22`'s case C is `p = 3` |
| [050](./reports/RUN-050-NOVELTY-AND-ROUTES.md) | `26`'s novelty rule and `01`'s route matrix | `src52` | `NO HIT ≠ NOVELTY PROOF` stands and **none of its four remaining steps is work this arm can do**; across 50 reports **21 novelty-term sentences, 11 refusals, 10 pinned quotations, 0 unaccounted** — including this round's own five, pinned rather than exempted; `01`'s PRIMARY GO route is best covered and its STOP route untouched, while **two rounds worked HOLD routes**, named rather than defended |
| [051](./reports/RUN-051-CONSENSUS-AND-EXPERIMENT.md) | `00`'s enclosure consensus and `06`'s agent experiment | `src53` | `00` §6 forbids three substitutions for the unclosed `∀p > 2`, and **the third is about this arm's own RUN-036** — all three guards are fields in the archived logs, so with `05`'s three and `07`'s five that is **eleven prohibitions across three documents, audited in one place, all clear**; `06`'s success gate stands at **2 of 4** with both gaps marked open by the corpus's own documents; and **`06`'s step 4 wrote 「不得默認相同」 about H3 while `08` and `09` did exactly that** |
| [052](./reports/RUN-052-COMPILER-TARGETS-AND-V03.md) | `02`'s next compiler targets and `06` v0.3's decision procedure | `src54` | v0.3 exists to close RUN-045's own `UNKNOWN`, so it was run per member and **stops at its first branch**: branch 1 never fires (every odd additive prime is potentially *good*), `H3` passes with witness `ℓ = 29` at all 19, `H1` is `UNKNOWN` beyond RUN-036's range, and the isogeny-kernel test that would settle `H2` is local data this tree does not compute — **2 of 5 decided**. And **`02`'s target 3 has an empty domain here**: `g_mult^odd = 1` has no odd prime divisor, which is *inapplicable*, not achieved |
| [053](./reports/RUN-053-LOCAL-ISOGENY-KERNEL.md) | `04`'s local `p`-isogeny kernel criterion | `src55` | **the test RUN-052 called unreachable was in the corpus, named in one earlier report**, and the v0.3 procedure that needs it does not cite it. Its chain checks out with **`p` odd load-bearing at step 2** — at `p = 2` every point is its own negative and the criterion passes for free. And a consequence `04` does not state: `λ·μ = ω`, so both tests firing forces `ω² = 1 ⟺ (p−1) ∣ 2`, true at exactly `{2,3}` over 46 primes — **at every `p ≥ 5` the two tests are mutually exclusive**. Not run on the family: its hypothesis is *local* reducibility and RUN-036's certificate is *global* |
| [054](./reports/RUN-054-FAMILY-SCHEMA-AND-SPEC.md) | `05`'s family-theorem schema and `07`'s implementation spec | `src56` | `05` refuses to be a theorem claim; **its two self-declared dangers are exactly where this line independently stopped** (RUN-041, RUN-039) — agreement, not progress. Its hybrid routes `p ∈ {3,5,7}` away from FW, and this line has **five independent structural reasons across four rounds** for `p = 3`. `07` specifies the missing test: **6 of 14 keys fillable, 0 of 6 fixtures runnable**, and its fourth forbidden inference `global irreducible → local irreducible` **is the substitution RUN-053 refused before reading it**. Prohibitions **11 → 15 across four documents** |
| [055](./reports/RUN-055-THEOREM-2-18-CONDITION-MAP.md) | `01_Theorem_2_18_Condition_Map` — **first Phase 1 subject** | `src57` | the map recomputed on **all 40,749 base curves and all 247,391 twist pairs**: E1 all pass, **E2 agrees with the census by set (2,709)**, **E4 — stated by the map, never a census removal class — holds on every curve**, 8b's three non-square conditions hold on all 3,747 CLZ20 curves with the 2-torsion point found by exact integer bisection, and **D/E/F on every twist pair: zero failures** — the admissibility side of Algorithm 2 rebuilt, not re-run. RUN-008's two populations *are* branches 8a/8b. And the 1,355 curves missing from the upstream twist blob **are exactly the 1,355 isogeny curves** |
| [056](./reports/RUN-056-PAPER-VS-CODE-PROVENANCE.md) | `02_Paper_vs_Current_Code_Audit` | `src58` | the mechanism behind RUN-055's provenance finding, read from the archived diffs: Algorithm 1's isogeny rule went **strict → relaxed → strict + `a₃`** across the three pinned commits, with the blob frozen at the first — and at `7286794` it is `set(bad_primes) and set([3,5,7])`, which Python evaluates to `{3,5,7}` unconditionally. The relaxed rule predicts all 1,355 isogeny curves in the OLD base escape its trigger: **1,355 of 1,355 do**. `02` §6's pins: 1 present / 1 partial / **1 absent (paper version)** / 2 N/A by the package's stated scope; §7's rank fields **0 of 4** |
| [057](./reports/RUN-057-LEMMA-B-REDUCTION.md) | `03` §1 + Lemma B, joined to `10` and to `27`'s router | `src59` | **FW-H2 at the twisting prime decided without a kernel polynomial**: `ρ̄_{E_q,q} ≅ ρ̄_{E,q} ⊗ χ_q` and Lemma B give `FW-H2(E_q,q) ⟺ FW-H2(E,q)`, and at a good ordinary prime that is `10`'s congruence. All 19 members good and ordinary at `q`; **exactly one has `a_q² ≡ 1 (mod q)` — `q = 3529`, `a_q = 1`**, three independent counts. The provisional FW-everywhere design (`18`/`02`/`06`) **fails H2 at member 3529's own twisting prime**; `27`'s router sends `p = q` to BSTW and is untouched on its face. **RUN-038's log had listed 3529 for seventeen rounds** — four rounds held one ingredient each, none joined. Profile `LEMMA_B_REDUCTION`, not `07`'s `FW17_EXACT` |
| [058](./reports/RUN-058-CROSS-ROUND-JOINS.md) | this line's own 59 logs — the joins instrument | `src60` | every prime set in every log intersected with every other: **100 sets, 325 intersections after filtering scaffolding, prime segments and containments**; a join counts as *made* only if one report names the numbers **and** both rounds — **107 made, 218 not, and none of the 218 is a new finding**. The 3529 join is in the table, and the drill sharpened the known-join test when a re-read satisfied it. **The report describing the unmade joins is the document that makes them** — 254 → 218 between two runs with nothing in the logs changed |
| [059](./reports/RUN-059-ONE-COMMIT-AND-DELTA.md) | `07`, `11`, `12`, `14` — one commit, four angles | `src61` | `07`'s predicates are the diff lines RUN-056 located; **every figure in `11` recomputes exactly** and its two pool percentages imply one pool (178,364); the histogram `11` called unknown is **2,707 / 1,353 / 2 — the fixture's 12:1 is 1:2 at 500K, right in direction**; `12`'s delta and `14`'s Gate A are one operation, performed (OLD − (isogeny ∪ `a₃`) = CURRENT, 36,687); `14`'s six Gate B items all computed; Gate C run by nobody |
| [060](./reports/RUN-060-ALGORITHM2-REPLAY.md) | `09` and `15` — Algorithm 2 OLD → CURRENT | `src62` | **`15`'s 2×2 recomputed to the pair** (247,391 / 21,306 / 0 / 0, `|T_O|` = 268,697) with this tree's own transcription of the deleted predicate; §6 and §7 to the curve; **why the expand branch could never fire — the deleted predicate is vacuous on the kept base, 0 of 36,687**; `09`'s two synthetic cases run as claimed. **Correction to RUN-055**: the 1,355 identity is stated in `15` §8 and should have been cited |
| [061](./reports/RUN-061-REMOVED-13-AND-SOUNDNESS.md) | `08` and `03` | `src63` | **`08`'s thirteen rows, 13 of 13** on first failure and LMFDB label against the 500K census under `08`'s own ordering; 26b1 is the `BOTH` class; the fixture's 9/2/1/1 is 1,233 / 115 / 7 / 2,707 at 500K; `03`'s six gates: four N/A by the package's scope, S4 audited at RUN-056, **S6's seven fields 6 of 7 — no timestamp** |
| [062](./reports/RUN-062-DISCREPANCY-CORPUS.md) | `02_Official_Discrepancy_Corpus` — the adversarial four | `src64` | **the negative control RUN-055's 8b instrument never had**: 62a1, 66b1, 105a1, 141c1 read from the pinned ecdata shard, none in the base, each with one rational 2-torsion point and **`f'(x₀)` a perfect square — 4 of 4**, as `02` says; a dead square test is caught only here. Three of four `ainvs` typed from memory were wrong. And **the ecdata shard's pin reproduces only as CRLF** — the package hashed a Windows checkout, 64,687 bytes = one per line |
| [063](./reports/RUN-063-PHASE1-CLOSURE.md) | `16`, `10`, `01`, `00`, `00_v02` — Phase 1's closure and fixtures | `src65` | **`16`'s eight items, 8 of 8 independently redone here**; the `<150` fixture recovered from the census — 25 → 12, 10/15 → 7/5, the 13 removed are `08`'s; `00`'s two hand fixtures reproduce exactly, no negative `d` ever admissible; and **the other half of RUN-055: with `04`'s bound `d < 1000`, completeness holds on all 36,687 stable curves — 0 absent, 0 extra** — Algorithm 2's admissibility side in both directions. `10`'s label not awarded |
| [064](./reports/RUN-064-PHASE1-PROTOCOLS.md) | the six Phase 1 protocol documents — Phase 1 at 23 of 25 subject + 2 cited (typed as 25 of 25; corrected at RUN-065) | `src66` | `04`'s seven required outputs 0 of 7 by name, five with analogues; `04` refuses the full-reproduction claim and so does this line; `05`'s stop rule applied to this line's last twelve rounds — no freeze; `05`'s record fields 5 of 7 in RUN-061; `06`'s principle *code version ≠ theorem semantics version* with numbers; `06`'s six briefs — this line fulfils D, E, F, and D's six discrepancy classes come to 0 |
| [065](./reports/RUN-065-PHASE0-MAPS.md) | `02`, `04`, `08` — Phase 0's three maps; Phase 0 at 10 of 10 | `src67` | `02`'s four open rows still open, no report claims one closed; 4 of 7 strong-BSD components computed here, the regulator without saturation, Ш never; `04`'s 首選 route the most worked at 23 to 9, the 紅燈 route with no round and 0 of 85 claimants (RUN-003); `08`'s six briefs and Referee E's eight leaps all covered, 28 attributions verified by signature phrase; **RUN-064's 25 of 25 was typed — the instrument says 23 + 2 cited, corrected** |
| [066](./reports/RUN-066-ALGORITHM2-MIRROR-AND-DIFF.md) | `03`, `13` — the Algorithm 2 mirror and the non-monotone diff; **Phase 1 at 25 of 25 in the instrument's sense** | `src68` | `03`'s point-count formula held against brute-force enumeration on 269,696 (curve, p) pairs, 0 disagreements; its cubic is this tree's monic form under X = 4x on all 40,749 curves; its inertness hypotheses hold on all 241,542 Zhai pairs (257,959 prime divisors, none even / non-coprime / bad / with a root); `13`'s +1899 / −53404 reproduced with git exactly; at entry level 0 twists added, 46,091 removed (21,306 stable + 24,785 with their base curves); every added line a comma drop (1,851) or a re-alignment (48), 0 new content; deletions account to the line |
| [067](./reports/RUN-067-ANOMALOUS-NORM-LOCALIZATION.md) | P5 `Anomalous_Norm_Localization_v1.1` — every exact figure of §2, §5, §7 | `src69` | recomputed with the gate's own group law, nothing read from RUN-011: `P'` generates `E(F₃₉₇)` and `E(F₉₉₁)` (orders 374, 1045), `Q' = 244 P'` and `356 P'`, the four cofactor multiples, slopes 2 and 4 = the logarithms mod 11, `det M_loc = 2`, `ρ` surjective with image 390,830, the document's kernel basis a basis, `v₁₁ = 2`, `J_S = 1`; seven `CLOSED_EXACT` rows, one `OPEN`, and the ratio 3 asserted by no report of this line; `θ̄_n` left to RUN-068 |
| [068](./reports/RUN-068-KURIHARA-MODULAR-SYMBOLS.md) | P5 `RUGZPB_P2_P4_v0.2` — the P4 certificate's one computation | `src70` | **mod-11 modular symbols for Γ₀(389) built here**: rank 325, dimension 65 = 2g+1 with g = 32 from the genus formula, Hecke at 2, 3, 5 → 2, plus → 1, eigenvalues −5, −3, −6, 5 at 7, 13, 17, 19 as point-counted; over all 392,040 units **δ₃₉₇·₉₉₁ = 5 ≠ 0 at λ(1,5) = 1, raw product sum 43,605,160 — the stress-test package's figures to the term, a third implementation**; `θ̄_n ≡ 5·X₃₉₇X₉₉₁ (mod I³)` with the other five coefficients 0; rank-1 numbers at 397 and 991 both 0; the manuscript's 6 stays unreproduced, the theorem's input `δ ≠ 0` verified |
| [069](./reports/RUN-069-DETERMINANTAL-BOCKSTEIN.md) | P5 `Determinantal_Kurihara_Semilocal_v1.3` — **the 85th document; the sweep at 85 of 85** | `src71` | `det(B_N) = 2·XY` computed in `F₁₁[G]/I³` by the ring's own multiplication, `(1+X)¹¹ ≡ 1` automatic; under all 100 generator changes the line and `ord_I = 2` invariant, the coefficient reaching every unit; the ratio θ/det is 8 at the disclosed scale, 3 in the manuscript's, and primitive-root choice alone reaches all ten units — checked on the full sum for two other root pairs; Kim's hypotheses computed: `ρ̄₁₁` surjective by witnesses at 2 and 3, `E(ℚ₁₁)[11] = 0`, `c₃₈₉ = 1`, torsion trivial, the Manin constant left external; 3 closed labels, 2 open, none closed here |

## Layout

| path | what |
| --- | --- |
| `code/` | gates and their drills, one `srcNN_*` per round |
| `reports/` | `RUN-NNN-*.md`, one per round, numbered with its gate |
| `data/gate-logs/` | the archived stdout of every gate — the evidence reports cite |
| `data/external/` | snapshots of anything fetched from outside this repository |
