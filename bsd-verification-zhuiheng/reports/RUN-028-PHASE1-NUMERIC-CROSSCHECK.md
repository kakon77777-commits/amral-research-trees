# RUN-028 — Phase 1's stated arithmetic against this tree's own, and a scanner that failed in both directions

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the 25 Phase 1 documents — chiefly [`V0_5_EXACT_CENSUS_REPORT`](../../../amral/public/bsd/phase1/files/V0_5_EXACT_CENSUS_REPORT.md) §Q9's global accounting identity — against every number in this tree's 29 gate logs
**Tools:** [`src30_phase1_numeric_crosscheck.py`](../code/src30_phase1_numeric_crosscheck.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src30-phase1-numeric-crosscheck.json`](../data/gate-logs/src30-phase1-numeric-crosscheck.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: of the 23 distinct integers Phase 1's documents state, 15 appear in this tree's own gate logs and 8 do not. `V0_5_EXACT_CENSUS_REPORT` §Q9's global accounting identity checks out as arithmetic — `293482 − 247391 = 46091` and `24785 + 21306 − 0 − 0 = 46091` — and **four of its six independent inputs are ours**: RUN-012 rebuilt all 247,391 twist pairs and measured 21,306 removed, 0 added, the expansion branch empty over the whole domain. The two that are not ours, `old_total_twist_pairs = 293482` and `upstream_removed = 24785`, are tied by the identity, so **one measurement would close both** — the cheapest open item this round found. The round's own scanner failed twice, in opposite directions: it first over-reported 30 values with no counterpart, of which most were digit runs inside a git SHA or an LMFDB curve label, and then a third mask was needed for `\gcd(3,138)` being read as the number 3,138 — found by reading the gate's own absent list, not by any check.**

---

## The question this round asks

RUN-027 measured that **none of Phase 1's 25 documents has been the subject of a
round**, while six rounds verified that line's arithmetic down to 122,247
isogeny determinations and all 247,391 twist pairs. Those rounds were aimed at
the artefacts the documents describe.

Reading the documents is one job. This does the harder half, which reading
cannot do: **does the arithmetic the documents state agree with the arithmetic
this tree computed?**

## Four outcomes

| outcome | count |
| --- | --- |
| **confirmed** — the value appears in our gate logs too | **15 distinct** (38 occurrences) |
| **absent** — we have no counterpart | **8 distinct** (19 occurrences) |
| masked — a git SHA, a curve label, a LaTeX argument pair | 32 |
| malformed — a table column that ran together in the markdown | 1 |

Confirmed includes every headline figure of the Phase 1 line: `247391`,
`40749`, `39394`, `36687`, `31250`, `21306`, `4062`.

**A confirmation is a coincidence of integers, not a proof.** Two different
quantities can share a value, so the gate keeps every context and this report
reads the ones that carry weight rather than counting matches as agreement.

## The absent eight, read

| value | what it is | checkable here? |
| --- | --- | --- |
| `293482` | `old_total_twist_pairs`, §Q9 | **yes, and worth doing** |
| `24785` | `R_upstream`, Algorithm 1's own twist removals, §Q4 | **yes, and worth doing** |
| `46091` | §Q9's `lhs` and `rhs` | derived from the two above |
| `1355` | base labels a replay could not rebuild without re-running Algorithm 2 | a real count, not recomputed |
| `53404`, `4064` | lines removed in a git diff of the twist JSON and label list | real, but about files rather than the census |
| `500000` | `conductor < 500000`, a scope bound in a plan | not a computed quantity |
| `2024` | the year range "2024–2026" | not a quantity |

So the genuinely open arithmetic is two numbers, and they are the same question.

## §Q9's accounting identity

`V0_5_EXACT_CENSUS_REPORT` states a closed accounting of the twist census:

```text
old_total_twist_pairs = 293482      new_total_twist_pairs = 247391
lhs                   = 46091       upstream_removed      = 24785
stable_removed        = 21306       stable_added          = 0
newbase_added         = 0           rhs                   = 46091
accounting identity   = PASS
```

Two separable things, and both are done here.

**The arithmetic.** `lhs = old − new = 46091` ✓. `rhs = upstream_removed +
stable_removed − stable_added − newbase_added = 46091` ✓. The two agree ✓.

**The provenance**, which is what an audit adds:

| input | ours? |
| --- | --- |
| `new_total_twist_pairs = 247391` | **RUN-012** rebuilt all 247,391 pairs |
| `stable_removed = 21306` | **RUN-012**: 21,306 removed at entry level |
| `stable_added = 0` | **RUN-012**: 0 added |
| `newbase_added = 0` | **RUN-012**: the expansion branch is empty over the whole domain |
| `old_total_twist_pairs = 293482` | **no round has counted the pre-change census** |
| `upstream_removed = 24785` | **no round has counted Algorithm 1's own twist removals** |

Four of six, and the two missing are tied: `old = new + upstream + stable`, so
measuring either pins the other. That is the smallest open item in Phase 1 and
it is now named.

## The scanner failed in both directions, and the second fault was found by reading

RUN-027 named a pattern in this tree: **a scan built from the form the author
remembers writing rather than from the forms the corpus contains**, four rounds
running, always a silent under-report. This round produced the mirror image and
then the original.

**Over-report.** The first run listed 30 values with no counterpart. Reading them
found most were not quantities at all: `1a0489c3c3099dd0c248624e6621df73ae8f0d43`
yields `248624`, `3099`, `6621` because stretches of hex are all digits, and
`66166b1`, `302606a1`, `156854b1` are LMFDB labels. Masking both took 30 to 9.

**Then the original, found by reading the remaining nine.** `\gcd(3,138)=3` is a
LaTeX argument pair, and the thousands-separator form read it as `3,138`. A
third mask took 9 to 8.

**Neither was caught by a check.** They were caught because the gate prints its
absent list with context, on the stated ground that the list is where to look —
the same discipline `src02` uses for the rejected route's vocabulary. A gate
that had only reported the count would have shipped 30, then 9, and both would
have read as findings about the corpus rather than about the scanner.

## A mask that is measured at exactly zero

The curve-label mask catches **nothing the SHA mask does not already catch** —
0 occurrences are its alone — because every LMFDB label in these documents
(`66166b1`, `302606a1`) is a valid hexadecimal string. It is kept, because an
isogeny class letter past `f` would break that coincidence, and the drill
records it as a control with the measurement attached rather than as coverage
this corpus cannot provide.

## The drill

**118 defects, 118 caught by the check named for each. 20 controls, none
disturbed, over 56 checks. Eighteen minutes and twenty-nine seconds.**

Gate 30 contributes one check and three defects. The check pins both directions
of the scanner's failure: the masks must catch a SHA and a label, must **not**
catch a real count, and the masked list must not be empty — a mask that matches
nothing is a filter that is not running, which is how the under-reporting family
begins.

## What this round does not claim

* **Agreement of integers is not verification of claims.** 15 values matching is
  15 coincidences that are very unlikely to be coincidences, and no more. What
  each number *means* is settled by the round that computed it, not by this one.
* **The documents have still not been read line by line.** This round reads
  their arithmetic. RUN-027's coverage measure will still show Phase 1's
  documents as subjects only when a round is aimed at their content.
* **The masks are heuristics** and each one is a judgement about what a digit
  run means. All three are printed with what they matched, so a wrong judgement
  is visible rather than silent.
* **§Q9's identity holding says the census is self-consistent**, not that it is
  right. Two of its inputs are unverified here and the identity cannot
  distinguish a matched pair of errors from none.
