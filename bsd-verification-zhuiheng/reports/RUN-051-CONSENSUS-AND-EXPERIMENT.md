# RUN-051 — Phase 2's own framing: eleven prohibitions in one place, and a success gate at two of four

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`00_Phase2_Global_Enclosure_Consensus`](../../../amral/public/bsd/phase2/files/00_Phase2_Global_Enclosure_Consensus.md) and [`06_Phase2_Agent_Experiment`](../../../amral/public/bsd/phase2/files/06_Phase2_Agent_Experiment.md) — the documents that set the phase's problem and the experiment meant to solve it
**Tools:** [`src53_consensus_and_experiment.py`](../code/src53_consensus_and_experiment.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src53-consensus-and-experiment.json`](../data/gate-logs/src53-consensus-and-experiment.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `00` §6 names `∀p > 2` as the unclosed quantifier and forbids three substitutions for it, and **the third is about this arm's own RUN-036**: *the residual representation is generically surjective* must not stand in for the quantifier. All three guards are present in the archived logs — `src38` names the 38 primes it reached and marks `ℓ = 3` partial, `src43` tags `P_loc` with its bound and `claim_is_universal: false`, `src47` marks the 7 primes above RUN-036's range **UNKNOWN** rather than extrapolating. With `05`'s three (RUN-034) and `07`'s five (RUN-043) that is **eleven prohibitions across three documents, audited in one place, all clear**. `00` §5's main problem — `BH2(E,d) + ∀p>2 FW(E_d,p) ⟹ BSD(E_d)` — has its left half cited and its right half compiled but **not closed**; the compiler emits exactly what `02` mandates for that state. And `06`'s four-condition success gate stands at **2 of 4**: H2's exact specialisation is supplied and verified here, H3's is supplied and **disputed inside the corpus**, `03`'s twist-invariance Lemma B is marked a candidate by its own document, and RUN-041 found `04`'s finite-prime reduction not achieved. **`06`'s step 4 carries the warning 「不得默認相同」 about H3, and the corpus did default to the same — in `08` and `09`, while `02` forbade it.** That is RUN-046's finding, sitting in the experiment plan as an instruction that was written down and then not followed.**

---

## `00` §6 forbids three substitutions, and one of them is about us

| forbidden | the guard, in the logs | |
| --- | --- | --- |
| most `p` are fine | `src40` reports the ordinary H2 failure set by range with counts, never as a fraction | ✔ |
| all `p ≤ B` are fine | `src43` tags `P_loc` `bounded_at: 6000` with `claim_is_universal: false` | ✔ |
| the residual representation is **generically surjective** | `src38` names the **38** primes it certified and marks `ℓ = 3` partial; `src47` marks **7** primes above that range `UNKNOWN` | ✔ |

The third row is worth dwelling on. RUN-036 is the round that certified `ρ̄_ℓ`
surjective at 38 primes, and it is a good result — and `00`, written before it,
says in advance that exactly such a result must not be allowed to stand in for
`∀p > 2`. The guard is not a sentence in a report; it is `src47` emitting
`UNKNOWN` for every prime past 167 rather than reading the pattern forward.

## Eleven prohibitions, three documents, one audit

| document | prohibitions | audited in | clear |
| --- | ---: | --- | --- |
| `05_Kodaira_Prefilters_and_NoGo` | 3 | RUN-034 | ✔ |
| `07_Stop_Rules_and_Claim_Ladder` | 5 | RUN-043 | ✔ |
| `00_Phase2_Global_Enclosure_Consensus` | 3 | **this round** | ✔ |

**Eleven, and the three lists do not overlap.** `05` forbids reading H2 off a
Kodaira table; `07` forbids climbing the claim ladder on partial evidence; `00`
forbids substituting anything for the prime quantifier. Three documents written at
different times, each anticipating a different way of overclaiming, and none of
them anticipating the same one twice.

## The main problem, and which half this arm touched

$$\mathrm{BH2}(E,d) + \forall p>2\ \mathrm{FW}(E_d,p) \Longrightarrow \operatorname{BSD}(E_d)$$

* **`BH2`** — Theorem 2.14's 2-part and nonvanishing conditions. **Cited.**
  RUN-014 computed its arithmetic inputs (`v₂(L^alg) = 0`, trivial torsion,
  `Δ < 0`); the theorem itself is not verified anywhere in this tree.
* **`∀p > 2 FW`** — where RUN-037, 038, 039, 041 and 045 went. The hypotheses
  have exact executable meaning and the certificate is emitted per prime. **The
  quantifier is not closed**, and the compiler emits *FW verified for tested
  primes*, which is the output `02` mandates in that state.

`00` says plainly what that state means: the route may only give a fixed
finite-prime-set `p`-part theorem until a finite exceptional-prime reduction
exists. RUN-041 measured that it does not.

## `06`'s success gate: two of four

| condition | state |
| --- | --- |
| H2 exact specialisation | **supplied, verified here** — `10` + `03` + `08`, shown one statement over 22,140 character pairs at RUN-046 |
| H3 exact specialisation | **supplied, disputed within the corpus** — `08`/`09` state it, `02` forbids equating it with H3, `23` derives it (RUN-046, RUN-049) |
| twist-invariance lemmas | **incomplete** — `03`'s Lemma B is 「標準表示論推導候選」 by its own text |
| finite-prime reduction on one nontrivial curve class | **not achieved** — RUN-041 |

`06` stakes something on the gate: 這已經是新的標準語言數學結果. It is not met,
and **neither of the two gaps is this arm's to close** — one is a lemma the
corpus marks as a candidate, the other a theorem nobody has.

## Step 4 said not to, and the corpus did

`06`'s step 4 briefs an agent to compare Fouquet–Wan's auxiliary `ℓ` condition
with Banwait's `p ∤ v_ℓ(Δ_E)` and to output *exact equivalence* or *strict
implication* or *not equivalent* — with the instruction:

> 不得默認相同。

`08` boxes them as an *iff* under the title *exact translation* and `09` states
the same three conditions as its definition, while `02` says the identification
must not be made. RUN-046 found that; RUN-049 found `23` supplying the
derivation that would justify it.

**The instruction was written down in the experiment plan and then not followed
by two of the documents the experiment produced.** That is not a mathematical
error — `23` may well be right — but it is exactly the failure step 4 was
written to prevent, and it took an independent arm reading four documents to
notice.

## This arm did not run the experiment

`06`'s seven steps are a plan for the corpus's own agents. Five of the seven have
resulting documents in the corpus, and this line verified those documents. It did
not select 60 curves, build local prime tables, or derive anything symbolically.

Scoring *steps this line performed* would conflate two roles, so the gate scores
what exists and who checked it. Step 7's census does not exist, and RUN-045's
certificate keeps its 7 `UNKNOWN` rows in its emitted output — which is step 7's
other instruction, 「UNKNOWN 不可吞掉」, obeyed by a round that never reached
step 7.

## A guard fired on the round that built it

RUN-050's novelty scan turns red on any novelty-term sentence that is neither a
refusal nor a pinned quotation. **It went red at this round's drill baseline**,
on a sentence inside RUN-050's own report — the drill table row naming the
planted defect *the classified novelty quotations are unpinned*.

Nothing in RUN-050 could have caught it. **A report's drill table is written
into the report after the gate that scans it has already run**, so a round's
tally is invisible to its own scan and becomes visible one round later. The
mention is descriptive, so it is pinned like the other ten, with that reason
recorded.

The mechanism behaving this way is the point: the scan was built so that an
unaccounted mention turns it red rather than being absorbed, and the first
thing it caught after being built was a sentence in the report that built it.

**And it caught this round twice more.** Two sentences in the section you are
reading carry a novelty term, because reporting where the guard fired means
naming what it guards. Pinned, not exempted. After this round the scan stands
at **30** sentences carrying a novelty term across **52** reports —
**15** refusals, **15** pinned quotations, **0 unaccounted**. Still no
round of this line claims novelty.

**And writing that tally found a third defect in the scan itself.** The
sentence *Still no round of this line claims novelty* came back unaccounted.
It is a refusal, and the refusal word list contains the exact phrase — but the
reports are hard-wrapped, the phrase had landed across a line break as
`no` + newline + `round`, and the refusal test was running on the raw sentence
while the pinning test ran on the flattened one. **The scan could not see one
of this line's own refusals.** Both tests now run on flattened text.

**And fixing that exposed a fourth.** With the wrapping repaired, three
sentences were still being counted as refusals for no reason at all: the
refusal words were matched as bare substrings, and *nothing* contains *not*,
and *another* contains *not*. One of the three was a genuine refusal whose
actual word — *nothing* — was not in the list and had been passing by accident.
The other two were drill-table lines that carry a term only because **this
check is called `novelty-and-routes`**, and a code identifier is not prose.

Three repairs, then: refusal words match on word boundaries, *nothing* joins
the list as the real refusal word it is, and the check's own identifier is
removed before the term test — narrowly, by exact name, because
`26_Novelty_Search_Log` *is* the subject of a round and must stay visible.

**The accident is now counted rather than merely fixed.** The scan reports
`refused_by_substring_only`, and the drill check asserts it is zero — read with
a sentinel default, so a scan that stops reporting the field turns the check
red instead of raising. *A repair nobody counts is a repair nobody can keep.*

## The drill

**212 defects, 212 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 41 controls undisturbed, over 80 checks.

The 4 planted for this gate, each turning `consensus-and-experiment` red and nothing else:

| planted defect | went red |
| --- | --- |
| 00 §6's third guard is reported present with RUN-045's UNKNOWN rows gone | `consensus-and-experiment` |
| 06's success gate is reported met at four of four | `consensus-and-experiment` |
| 00 §5's prime quantifier is reported closed | `consensus-and-experiment` |
| 06's step 4 warning is reported obeyed by the corpus | `consensus-and-experiment` |

And **3 more on another gate's check** — the three repairs this round made to RUN-050's scan, which belong to neither round's own table:

| planted defect | went red |
| --- | --- |
| the refusal test goes back to reading unflattened text, so a refusal broken by a line wrap is invisible | `novelty-and-routes` |
| refusal words go back to matching as substrings, so "nothing" and "another" both count as "not" | `novelty-and-routes` |
| the drill's own check name is left in the prose it scans, so every drill table counts as a mention | `novelty-and-routes` |


## What this round does not claim

* **The guards are fields, not proofs of good faith.** The audit checks that
  `src38`, `src43` and `src47` record their ranges and their unknowns. A report
  could still overclaim in prose, and this gate does not read prose.
* **The success gate's two gaps are not this arm's work.** Naming them is not
  progress on them.
* **`06`'s steps 1 and 2 may have been run** without producing a document in the
  corpus this line can see. Absence of a document is not absence of the work.
* **Theorem 2.14 is cited**, as it has been since RUN-014.
* **Nothing here closes the quantifier**, and the compiler's mandated output is
  reported rather than improved on.
