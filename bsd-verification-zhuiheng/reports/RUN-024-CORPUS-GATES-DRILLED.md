# RUN-024 — the last four undrilled gates, and the vacuous check that drilling them found

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** this tree's own `src00`–`src03`, the corpus-scanning gates, undrilled since they were written — and [`05_Internal_Grid_Rank_Audit`](../../../amral/public/bsd/phase0/files/05_Internal_Grid_Rank_Audit.md)'s four salvage conditions
**Tools:** [`src11_gate_drill.py`](../code/src11_gate_drill.py), [`src02_rejected_route_recurrence.py`](../code/src02_rejected_route_recurrence.py)
**Logs:** [`src02-rejected-route.json`](../data/gate-logs/src02-rejected-route.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `src00`–`src03` are drilled. The README has carried "the corpus-scanning gates are not" since RUN-010, fourteen rounds, and it no longer does. Drilling them found what running them never could: `src02`'s salvage-condition detector was **structurally incapable of firing**. Its pattern searched a 60-character window on a single line; `GR-1`–`GR-4` occur in exactly one document and only as section headings, with the verdict 「目前四項皆未完成」 four lines below. So `GR_conditions_claimed_met: []` was true of nothing — the same empty list would have been reported had the audit declared all four conditions met. The pattern had a second, independent fault: it matched `滿足` inside `未滿足`, so had it ever reached a verdict it would have inverted it. Rewritten, the gate now reads all six mentions and classifies each: **6 stated unmet, 0 claimed met, 0 with no verdict nearby**. Same headline, entirely different standing.**

---

## Why these four were left, and why that had to end

RUN-010 is the round that discovered this tree's README had claimed mutation
drills for nine rounds while the tree had none. The line it wrote then has been
carried, honestly, ever since:

> `src00`–`src03`, the corpus-scanning gates, are not.

Stating a gap is better than hiding one, and it is not the same as closing it.
These four are the gates that run **first** whenever the corpus changes, and the
corpus is going to change: this line is now infrastructure for a formal attack,
not a document sweep. An undrilled gate at the front of the chain is the one
whose silence is most expensive.

## What the four gates claim

| gate | claim |
| --- | --- |
| `src00` | the 85 curated documents match the archived originals **by content hash**, never by filename |
| `src01` | the certificate ladder's **eleven** rungs `C0`–`C10`, and whether a downstream summary drops the `C2`/`C3` boundary between evidence and proof |
| `src02` | the rejected lattice-point route stayed rejected, and its four salvage conditions are never claimed met |
| `src03` | the multiplicity no-go's counterexample, in exact rationals |

## The finding: a check that could not fire

`src02`'s detector was

```
CLAIMED_MET = (GR-?[1-4])[^\n]{0,60}?(PASS|closed|已完成|成立|滿足|proved)
```

and its result had always been the empty list. Two independent faults, and
neither is visible from a green run.

**It was same-line only.** `[^\n]{0,60}` cannot cross a newline. `GR-1` through
`GR-4` appear in the whole 85-document corpus **only** in
`05_Internal_Grid_Rank_Audit.md`, and only as section headings —
`## GR-1：Faithful discretisation` and its three siblings. The document's verdict
is a separate line, four lines below the last of them:

> 目前四項皆未完成。

The detector could never reach it. So the empty list was not a measurement of
the corpus; it was a measurement of the pattern's reach. **Had the audit said
all four conditions were met, the gate would have reported exactly the same
empty list.** This is RUN-016's vacuous-`ok` class again, in a different gate.

**And it had no negation.** `滿足` is a substring of `未滿足`. Tested directly:

| text | old detector says |
| --- | --- |
| `GR-1 已滿足` (met) | claimed met |
| `GR-1 未滿足` (**not** met) | claimed met |
| `GR-2 不成立` (does **not** hold) | claimed met |
| `GR-4 remains unproved` | claimed met |
| `GR-1 is not closed` | claimed met |

Every negated form reads as an affirmation. So the two faults pointed in
opposite directions: the window kept the check from ever seeing the verdict, and
the vocabulary would have inverted the verdict it saw.

## What it says now

`classify_salvage` reports **three** buckets rather than one, over a window that
spans lines, with an explicit negation rule:

| verdict | count |
| --- | --- |
| claimed met | **0** |
| stated unmet | **6** |
| no verdict nearby | **0** |

with the evidence string on each row showing the sentence that decided it —
`…不能預設 BSD。 目前四項皆未完成。` for all six.

The headline is unchanged: no salvage condition is claimed met anywhere in the
corpus. What changed is that this is now a reading of the documents instead of a
property of a regex. **An empty "claimed met" list is evidence only when the
other two buckets show the detector had something to read**, and that is why all
three are reported.

The drill pins both faults. Setting the window back to a single line turns
`rejected-route-verdicts` red — all six mentions become "no verdict nearby",
which is the old behaviour made visible. Removing the negation rule turns it red
the other way — all six flip to "claimed met", which is the inversion.

## A duplication in this arm's own work, found the same way

Reading `src03` closely enough to drill it turned up something about the round
before this one. **RUN-023's §9 section restated what RUN-003 had already
done** — and did it with less.

`src03` recomputes `f_a(z) = z(z+a)` in exact rational arithmetic, over a table
of `a` down to `10⁻¹²`, and its docstring already contains the sharpening
RUN-023 presented as a reading: that the point-order jumps *while the
neighbourhood count is stable*, which is Hurwitz, and that this is why doc 05's
own remedy list asks for control **in a neighbourhood** of `s = 1` rather than
at the point. Its log even shows the count moving from 1 to 2 as `a` drops below
the disc radius.

RUN-023 was not wrong and it credited the source document's Corollary 9.2
correctly. But it presented as a fresh reading something this tree had already
computed more sharply, in round 3. The rule this arm applies to the corpus —
that a restatement is not a result — applies here, and the round is recorded as
a duplication rather than left to read as new.

## The drill

**104 defects, 104 caught by the check named for each — none uncaught, none
caught by the wrong check. 20 controls, none disturbed, over 50 checks. Fifteen
minutes and fifty seconds.**

The four new checks cost **0.01 seconds** per sweep between them, which is worth
stating: the reason these gates went undrilled was never cost. Two of their six
defects are the faults above; the others pin a truncated content hash, the rung
pattern's word boundaries, and the order-versus-degree confusion in `src03`.

One defect had to be rewritten before it caught anything, and the reason is
instructive. Dropping the word boundaries from `\bC(\d{1,2})\b` changes nothing
on the fixture `"C10 only"`, because a greedy `\d{1,2}` already reads `C10` as
one token. The boundaries decide different strings: without the trailing one
`"C123"` yields a spurious `C12`, and without the leading one `"ABC10"` yields a
`C10` that is not a rung reference at all. A fixture that cannot separate the
two versions is not testing the thing it names.

## What this round does not claim

* **Nothing about BSD.** It closes a drill gap in this tree and repairs one of
  this tree's gates.
* **`src00`'s archive comparison is not exercised by the drill.** The check
  covers the hashing property and the curated side; reading the archive branch
  shells out to `git`, and a subprocess once per planted defect is a cost with
  no matching gain. The gate still does it on its own runs.
* **The rewritten `src02` classifier is still a regex.** It decides met versus
  unmet by vocabulary and proximity, which is enough for the one document that
  carries `GR-n` and would not be for prose that argued the point at length.
  Its three buckets exist so that a future corpus which defeats it reports "no
  verdict nearby" rather than a confident empty list.
* **`src01`'s downstream-summary check reads what it is pointed at.** It cannot
  know about a summary nobody registered.
