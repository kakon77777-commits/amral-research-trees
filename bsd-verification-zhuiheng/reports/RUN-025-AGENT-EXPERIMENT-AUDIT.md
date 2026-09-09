# RUN-025 — the Phase 1 agent experiment against its own freeze conditions, and a scanner that needed three corrections to measure anything

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`06_Phase1_Agent_Experiment`](../../../amral/public/bsd/phase0/files/06_Phase1_Agent_Experiment.md) §6's five success conditions and §7's five freeze conditions, audited against the corpus the experiment produced
**Tools:** [`src27_agent_experiment_audit.py`](../code/src27_agent_experiment_audit.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src27-agent-experiment-audit.json`](../data/gate-logs/src27-agent-experiment-audit.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the freeze condition 「將 analytic Ш 當 actual Ш」 is not triggered. Across all 85 documents there are 36 numeric claims about Ш in 14 documents, and every one carries a label: 5 say analytic **in the symbol itself** (`Ш_an`), 7 carry both labels, 7 actual, 4 analytic, 1 by provenance, 9 are stated as required hypotheses rather than as claims, and 3 are unlabelled within 300 characters — all three read as imported results whose provenance is stated earlier in their section. The corpus's own specification document writes `Ш_{\mathrm{an}} = 1`, which is the strongest form the separation can take: it is in the notation. And one success condition is settled here rather than asserted — Banwait–Huang reproducibility, which RUN-007, RUN-008 and RUN-012 established by rebuilding 122,247 isogeny determinations and all 247,391 twist pairs independently. The round's own scanner needed **three** corrections before it measured anything, and each was a silent under-report of exactly the kind RUN-024 had just found in `src02`.**

---

## Why audit the experiment's own conditions

`06_Phase1_Agent_Experiment` is the specification for the run that produced
Phase 1 and Phase 2. It sets five success conditions and five under which
「本輪不算有效研究」 — the round does not count as valid research. Those are the
corpus's standards for its own methodology, and this line is now infrastructure
for an attack that intends to reuse it.

Most of the ten need reading. **One does not**, and it is the one this arm has
already caught itself failing:

> 將 analytic $\Sha$ 當 actual $\Sha$

RUN-019 audited that pattern against this tree and found RUN-017's headline
guilty. The question is symmetric.

## The measurement

Every numeric claim about Ш in the 85 documents, classified by how it is
labelled. **36 claims across 14 documents:**

| how the claim is labelled | count |
| --- | --- |
| **analytic by its own subscript** (`Ш_{\mathrm{an}}`, `Ш_{\rm an}`) | **5** |
| both labels present | 7 |
| labelled actual | 7 |
| labelled analytic | 4 |
| labelled by provenance (inherited / imported) | 1 |
| stated as a hypothesis, not a claim | 9 |
| **unlabelled within 300 characters** | **3** |

The five that carry the label **in the notation** are the strongest evidence
available, and one of them is in the specification document itself
(`06_Phase1_Agent_Experiment.md:202`, `\Sha_{\mathrm{an}}=1`). A corpus that
writes the analytic subscript is not one that has confused the two orders.

**All three unlabelled claims were read, because the gate's job is to say where
to look and not to pronounce.** They are:

| where | claim | reading |
| --- | --- | --- |
| `v1.3:324` | `Ш(E/Q)[11^∞] = 0 ✓` | a row in a checklist of imported results; the section states the provenance above the block |
| `v0.5:94` | `#Ш(E/Q)[11^∞] = 1` | the BKS `p`-part formulation, using the imported certificate |
| `v0.3:129` | `Ш(E/Q)[11^∞] = 0` | a factor in a valuation computation, imported from Phase 2 |

None asserts that an analytic order is an actual one. **The freeze condition is
not triggered.**

## The other nine conditions

§7's remaining four are not triggered as far as this arm can see, and each entry
says what "as far as this arm can see" means:

| freeze condition | this arm |
| --- | --- |
| 只抄 LMFDB | RUN-004 recomputed 40,749 discriminants and 135,787 valuations; RUN-016 recomputed 40,749 conductors; all agreed. **A corpus that only copied would also agree** — this is consistency, not proof of independence |
| 只算數值比 | exact finite certificates exist and were recomputed in exact arithmetic: `det M_loc = 2` (RUN-011), the Selmer cube (RUN-022), v0.8's whole boxed chain (RUN-020) |
| 無法追溯 theorem hypotheses | RUN-021 traced every P5 gate to an exact finite computation or a named external theorem, and found none that could not be traced |
| 無法分辨 weak / strong / p-part | the three are distinct headings in `01_BSD_Statement_and_Quantifier_Audit` §1.1–1.3 and are used distinctly downstream |

§6's success conditions divide differently. Only the third is **settled** here:

> **3. Banwait–Huang 算法可重現 — met, and by an independent implementation.**
> RUN-007 and RUN-008 closed 122,247 isogeny determinations both ways; RUN-012
> rebuilt all 247,391 twist pairs, with 36,687 of 36,687 curves agreeing.
> Reproduction by a second implementation is a stronger reading of this
> condition than the experiment asserting it.

Condition 2 is partly met in this arm's own experience — R2+ is `389.a1`,
verified across RUN-011, RUN-020, RUN-022 and RUN-023; R0 is `696.e1`, whose
analytic rank 0 was established in RUN-014; **no R1 certificate has ever passed
through this arm.** Conditions 1, 4 and 5 are readings, not computations, and
the gate says so rather than scoring them.

## Three corrections before the scanner measured anything

This is the part worth keeping. RUN-024 had just found `src02`'s detector
structurally incapable of firing, and wrote the lessons down. The scanner built
here, one round later, needed all three of them applied — the first two after it
had already produced a number.

**First pass: vocabulary too narrow.** It flagged 8 apparent unlabelled claims.
Reading all eight found **zero** violations: two were false positives (a
`\text{P4 Sha-control closed at }p=11` that is not a numeric claim at all, and a
`Ш(E')[2]=0` that is a *required hypothesis* under 「再要求」), and the other six
carried labels the vocabulary did not know — the provenance words `inherited`
and `imported`, and the subscript `Ш_{\rm an}`.

**Second pass: the tightened claim pattern dropped real claims.** Pinning the
structure removed the false positives and also removed five **genuine** analytic
claims, because `_\{[^}]{0,30}\}` stops at the inner brace of `_{\mathrm{an}}`.
The specification document's own `\Sha_{\mathrm{an}}=1` was among the losses. A
subscript that may nest one level fixed it.

**Third: the classifier needed buckets, not a binary.** A required hypothesis is
not a claim about the world; an inherited value has said where it stands. Nine
and one rows respectively, which counted as unlabelled would have tripled the
finding.

So the honest sequence is 8 flagged → 0 real → 5 more found by widening → 3
remaining, all read. The drill now pins each correction as a fixture, because
each failure mode was a **silent under-report** and not an error: the nested
subscript, the notation-level label, the hypothesis bucket and the provenance
bucket each turn `sha-labelling` red when removed.

## The drill

**108 defects, 108 caught by the check named for each — none uncaught, none
caught by the wrong check. 20 controls, none disturbed, over 51 checks. Fifteen
minutes and forty-four seconds.**

## What this round does not claim

* **Nothing about BSD.** It audits a methodology specification against the
  corpus that specification produced.
* **"Not triggered" is not "passed".** Four of §7's five conditions are judged
  from what this arm happened to verify in other rounds, and the entries say so
  — the LMFDB one in particular is consistency, which a copied corpus would also
  show.
* **Six of the ten conditions are readings.** The gate scores one freeze
  condition mechanically and one success condition from prior rounds' outputs;
  the rest it reports without scoring, because a specification's completeness
  and its choice of "the top three bottlenecks" are not computations.
* **The scan is over the curated 85.** A claim in the archived packages that the
  curation did not carry is out of its reach.
* **A label is not a justification.** This gate measures whether the corpus
  *distinguishes* analytic from actual Ш, not whether any particular value is
  right — and RUN-019's audit of `#Ш = 1` headlines applies to labelled claims
  exactly as much as to unlabelled ones.
