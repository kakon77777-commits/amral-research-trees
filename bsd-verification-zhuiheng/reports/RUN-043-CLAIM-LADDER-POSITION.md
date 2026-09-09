# RUN-043 — Where this line actually sits on the corpus's own claim ladder: C1, and partial

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`07_Stop_Rules_and_Claim_Ladder`](../../../amral/public/bsd/phase2/files/07_Stop_Rules_and_Claim_Ladder.md) — the one document in the corpus that this arm is a **subject of** rather than a reader
**Tools:** [`src45_claim_ladder_position.py`](../code/src45_claim_ladder_position.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src45-claim-ladder.json`](../data/gate-logs/src45-claim-ladder.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: **C1, and partial.** H2 and H3 have exact executable meaning in this tree — RUN-038 runs `a_p² ≡ 1 (mod p)` over every good ordinary prime, RUN-037 runs the H3 criterion including the clause `09`'s own certificate drops — but **H1 does not**: it is `10`'s niveau-2 argument, cited. **C2 is not reached at all**, and not for want of computation: this arm never proves `FW(E,p)`. It checks residual hypotheses and cites the theorem that consumes them, and reporting otherwise would be `07`'s fifth forbidden upgrade in this arm's own voice. C3 through C6 follow. **All five forbidden upgrades are audited against the archived gate logs rather than against prose** — a report can say anything, a log records what a gate computed — and all five guards are present. The three-round stop rule is **not** triggered: the last three logs with a source each compiled a corpus document no earlier round had. And all 46 reports carry an explicit list of what they do not claim; the gate names the ones whose drill tally is still pending, which is this round's own siblings' state.**

---

> **Correction note added at RUN-046.** One of the 176 defects in the drill this
> round cites — *squarefree part drops the sign* — went red by raising a
> `TypeError`, not by dropping a sign. Two drill helpers named `_true_squarefree`
> had been bound to functions with different return types, and the later binding
> shadowed the one that defect needed. **A defect that produces a traceback is
> not a defect a check caught**, so one of the 176 was a crash-catch. The names
> are repaired, the drill now refuses to run with any shadowed `_true_*` helper,
> and RUN-046's run re-exercises that defect as a real catch. Every other figure
> in this round stands.

## The ladder, and the honest rung

| | | this line |
| --- | --- | --- |
| **C0** | literature map | **reached** — every round names its source document |
| **C1** | every FW hypothesis has exact executable meaning | **partial** — H2 ✔, H3 ✔, **H1 cited** |
| **C2** | `FW(E,p)` rigorously proved for a fixed `(E,p)` | **not reached** |
| **C3** | twist-uniform at fixed `p` | not reached |
| **C4** | finite exceptional-prime reduction | not reached — RUN-041 found `04`'s criterion not achieved |
| **C5** | all odd primes | not reached |
| **C6** | full strong-BSD twist family | not reached |

**C2 is the one worth being precise about.** It is not blocked by a missing
computation. This arm's entire method is to check the residual hypotheses a
theorem needs and to cite the theorem — RUN-039 assembled `11`'s derived
proposition exactly that way, six primes with H3 computed and H1, H2 cited. A
certificate of hypotheses is not a proof of the conclusion, and `07`'s last
forbidden upgrade names precisely that confusion:

> Fouquet–Wan theorem 存在不等於它已經 algorithmized。

## The forbidden upgrades, audited against the logs

A report can say anything. A log records what a gate computed, so the audit
reads the archived fields that carry the discipline rather than the prose that
describes it:

| forbidden | the guard, in the log | |
| --- | --- | --- |
| `p < 1000` tested is not C4/C5 | `src43` tags `P_loc` with `bounded_at` and `claim_is_universal: false` | ✔ |
| 99.9% of primes is not C5 | `src40` reports the failure set by range with counts, never as a percentage | ✔ |
| a residual image that "looks generic" is not a theorem | `src38` records a **named Frobenius witness** for every refuted maximal class at every `ℓ` | ✔ |
| a non-semistable sample is not all non-semistable curves | every family claim carries its bound, 4,000, in its own log | ✔ |
| FW existing is not FW algorithmized | `src41` lists the Fouquet–Wan theorem in `what_stays_cited` | ✔ |

The third row is the one this arm nearly failed at RUN-036 by accident: a
surjectivity claim could have been reported from the absence of counterexamples.
It is not — every one of the six maximal classes at each of 38 primes carries the
prime, the trace and the residue that refuted it.

## The three-round stop rule

`07` freezes database scaling if three consecutive rounds only add checked primes
or curves without advancing H2/H3's exact meaning or theorem-ising the finite
exceptional set. That is a claim about rounds, so it needs a measurable proxy,
and the gate uses this one: **did the round compile a corpus document no earlier
round had?** A new source is new meaning; a larger bound is not.

| log | source | new |
| --- | --- | --- |
| `src42-odd-additive-barrier.json` | `01_Odd_Additive_Period_Barrier` | ✔ |
| `src43-finite-exceptional.json` | `04_Finite_Exceptional_Prime_Problem` | ✔ |
| `src44-base-certificate.json` | `15_696e1_Base_Certificate` | ✔ |

**Not triggered.** Which is a measurement about the last three rounds, not a
promise about the next three.

## Every report carries its limits

46 reports, **46 with an explicit list of what the round does not claim**. The
gate also names the reports still carrying a `TALLY PENDING` marker — at the time
the log was written, RUN-045, RUN-046,
whose drill had not yet run. That is this round auditing its own siblings' state
rather than assuming it.

## And the tally scan was built the way RUN-027 warned about

The gate names the reports still carrying a `TALLY PENDING` marker. Its first
version looked for the **phrase**, so this report — which discusses the marker —
matched its own prose and listed itself as pending. Corrected to compare the
**marker line** at the top of a file instead.

That is exactly the pattern RUN-027 named after catching it four rounds running:
**a scan built on what the author remembers writing rather than on what the
corpus actually contains.** Fifth occurrence, same shape, caught this time by the
round's own commit step refusing to proceed.

The correction is **verdict-neutral and provably so**: the check reads only the
report count and whether every report carries a limits section, and neither
depends on the tally scan. The drill figures below stand.

## The drill

**176 defects, 176 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 32 controls undisturbed, over 72 checks.

The 4 planted for this gate, each turning `claim-ladder` red and nothing else:

| planted defect | went red |
| --- | --- |
| the ladder position is reported as C2 | `claim-ladder` |
| H1 is reported as executable here, so C1 reads as complete | `claim-ladder` |
| the forbidden-upgrade audit stops reading the logs | `claim-ladder` |
| the stop rule reports untriggered while its own rounds are not new | `claim-ladder` |


## What this round does not claim

* **The rung is this arm's, not the corpus's.** `07` grades the Phase 2 project;
  this gate grades only what this verification tree computes. The corpus's own
  position on its ladder is a different question and is not answered here.
* **The stop-rule proxy is a proxy.** "Compiled a new document" is a measurable
  stand-in for "advanced the exact meaning", and a round could satisfy it
  cheaply. The rule's real test is what the round found, which no gate can score.
* **The forbidden-upgrade audit checks that a guard is present**, not that every
  sentence in every report obeys it. Five specific archived fields are read; the
  prose is not parsed.
* **C1 partial is not C1.** H1 has no executable meaning here and the table says
  so in the same row rather than in a footnote.
* **Nothing here advances any rung.** This round measures a position; it does not
  move one.
