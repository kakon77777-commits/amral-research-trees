# RUN-030 — the New-Chat Handoff: 132 documents reshipped 27 times without a byte of drift, and one lemma compressed into a stronger one than the round proves

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Collatz_New_Chat_Handoff_v1.0.zip` (source item 48) — a handoff document and a start prompt, plus six round documents that also ship in item 47.
**Tools:** [`src48_handoff_fidelity.py`](../code/src48_handoff_fidelity.py) · [`src48_drill.py`](../code/src48_drill.py) · [`src48_emit_report_block.py`](../code/src48_emit_report_block.py)
**Logs:** [`src48-handoff.json`](../data/gate-logs/src48-handoff.json) · [`src48-drill.json`](../data/gate-logs/src48-drill.json) · [`handoff-v1-literature-check.json`](../data/external/handoff-v1-literature-check.json) · [`hardzeta-corpus-manifest.json`](../data/external/hardzeta-corpus-manifest.json)

**Result: the handoff is an accurate compression, and the two places it is not are worth more than usual because of what this document is. Every number in it traces to a round; every one of 132 documents reshipped across 27 bundles is byte-identical; every status disclaimer survives. But its occupancy lemma is the round's lemma multiplied by √2 — contradicting the constant it prints three lines later — and the withdrawn citation has moved from a round's footnotes into the standing bibliography a new conversation is told to work from.**

---

## This item is not a round, so the check is not the usual one

Every earlier item in the sweep asserted mathematics, and the question was whether
it held. This one asserts **what the other documents say**. It compresses nine
rounds into fifteen pages, and §0 instructs a fresh conversation to treat it as
the formal state of the research line.

That changes what an error costs. A defect inside A-U.2d.2 sits in A-U.2d.2. A
defect here is inherited by every round written after it, by a reader who has been
told not to go back and re-derive the basics.

So this run checks fidelity, mechanically:

- **every number** must trace to a round document, verbatim or as a correct
  rounding of one;
- **every reshipped document** must be byte-identical to its other copies;
- **every status** must survive the compression — nothing conditional promoted,
  nothing external presented as proved;
- and the **intermediate lemmas** must be the round's lemmas, not stronger ones
  that happen to imply the same conclusion.

What is deliberately *not* checked is whether the mathematics holds. RUN-019
through RUN-029 did that, round by round.

## Three things that could have gone wrong and did not

**No document has drifted.** The line reships its prior rounds in every bundle —
132 distinct markdown documents, 27 of them appearing in more than one bundle, one
of them shipped **8** times. Every filename resolves to exactly **one** hash. For
a corpus assembled by hand over months, that is the result worth stating first,
and it is the one a reader would otherwise have to take on trust. The full
manifest is archived so it can be re-derived without the source folder.

**Every number traces.** Thirteen numeric constants, ten appearing verbatim in
round documents and three — `κ_rot`, `σ★`, and the second continued-fraction
coefficient — appearing as **correct roundings** of longer literals in the rounds.
Nothing invented, nothing mistyped, and the three shortenings are correct
roundings rather than truncations.

**Every disclaimer survives.** The handoff still refuses to claim Collatz, Terras
or CASP; still marks the Diophantine exponent and the criticality theorem as
*external inputs*; still carries the non-telescoping no-go for the rotation
headroom; and still carries the caveat that "first crossing" here is the
accelerated-endpoint coefficient crossing and not the modified-step one. A
compression that keeps its caveats is doing the harder half of the job.

## Finding 1 — the occupancy lemma is stronger in the handoff than in the round

§15 of the handoff states, in three consecutive claims:

> `Λ_L ≥ 𝒪_L/12` …  `𝒪_L ≳ √L` …  `U_β(L) − C_L ≥ (1/(12√2) − o(1))√L`

The first and third are the round's. The second is not. A-U.2d.2 proves an
explicit bound,

> `𝒪_L ≥ (√(H² + 2N) − H)/2 − 1`,

which at the `H = o(√L)` limit the round itself takes converges to `√L/√2`, not
`√L` — measured here at `0.7071` and tending to `1/√2`. The round never states the
bare `√L` form anywhere.

The consequence is internal: **the handoff's own first two lines yield
`κ_rot = 1/12 = 0.0833`, and its third line prints `1/(12√2) = 0.0589`.** The two
contradict each other by exactly `√2`, and the *stated* intermediate is the
stronger one.

Nothing downstream is corrupted — every later number in the handoff uses the
correct `κ_rot`. But this is a bootstrap document, and a new conversation reading
§15 has an apparently-proved lemma from which it can legitimately derive a
constant the line does not have.

**This is the characteristic failure of a compression**: the conclusion is copied
correctly and the step that produced it is rounded off. It is the reason this run
checks intermediate lemmas at all, rather than only checking that the constants
match.

## Finding 2 — the withdrawn citation moves from a footnote into the bibliography

`arXiv:2605.13886` (Niu), withdrawn 2026-05-20, appears for the **fifth** time.

The four previous occurrences were citations inside rounds. This one is different
in kind: it is an entry in §25's 常用文獻 — the standing reference list §0 tells a
fresh conversation to work from — with no note that the paper has been withdrawn.
The earlier occurrences propagated an unmarked withdrawal *within* the line. This
one propagates it *forward*, into work that has not been written yet.

The list annotates elsewhere: the López–Stoll entry carries 「外部 criticality
input，保留 caveat」, and the section closes by warning against treating
unaccepted Collatz proofs as established. So the format supports caveats and the
omission is a choice rather than a limitation.

The same section also carries the **Wu–Wang title defect** RUN-029 found — *log 3*
rendered as *log₂ 3* — now in the bibliography rather than in one round's notes.

**And one reference the handoff adds is entirely correct.** `arXiv:2111.02635` is
Lagarias, *The 3x+1 Problem: An Overview* — cited by no round document, verified
here, and exactly what it is described as. A survey is a sensible thing for a
bootstrap list to carry, and it is the only entry the handoff introduces.

---

<!-- BEGIN GENERATED measured block: python code/src48_emit_report_block.py -->

**The occupancy lemma, both ways.** The round's explicit bound divided by `√L`, at the `H = o(√L)` limit the round itself takes:

| `L` | `1e4` | `1e6` | `1e8` | `1e10` | `1e12` |
| --- | --- | --- | --- | --- | --- |
| bound / `√L` | `0.697071425` | `0.7061064276` | `0.7070067777` | `0.7070967812` | `0.7071057812` |

It tends to `1/√2` (`True`), not to `1`. The handoff states the bare `√L` form (`True`) which the round never states (`True`), keeps the divisor `12` (`True`), and keeps the round's `κ_rot` (`True`) — so its own first two lines give `0.08333333333` where its third gives `0.0589255651`, a factor of `1.414213562`.

| what | measured against | value |
| --- | --- | --- |
| distinct markdown documents across every Hard-Zeta bundle | hashed from the zips, not from an extracted copy | `132` |
| …reshipped in more than one bundle | the ones that could drift | `27` |
| …most times a single document is shipped | `Hard_Zeta_Phase_I_Round_01_Exact_Refinement_v0.1.md` | `8` |
| **documents resolving to more than one hash** | must be zero | `0` |
| numeric constants in the handoff and start prompt | 10 verbatim in a round, 3 as a correct rounding of one | `13` |
| …printing a number found in no round document | arXiv identifiers excluded and checked as references instead | `0` |
| …disagreeing with a closed form or exact rational | 5 closed forms, 3 exact rationals | `0` |
| required statements the compression dropped | 6 checked: disclaimers, external-input flags, the no-go, the index caveat | `0` |
| forbidden statements found | 3 checked, each fired on a counterexample | `0` |
| absence checks that could never fire | the guard on those checks | `0` |
| arXiv identifiers in the handoff | 1 introduced by the handoff itself, 0 of those unchecked | `7` |
| entries in the standing reference list | 1 carries a caveat, so the format supports one | `11` |
| files the handoff names as current | 10 markdown found in the corpus, 2 are not markdown | `12` |
| …named but missing | must be zero | `0` |
| defects planted / caught by the check named for each | 1 of the entries is a robustness property; 0 malformed | `16 / 16` |

**Literature.** `arXiv:2605.13886`, withdrawn 2026-05-20, appears for the **5th time** and for the first time in a standing bibliography, with no note.

The one reference the handoff adds that no round cites is `arXiv:2111.02635`, *The 3x+1 Problem: An Overview* by Jeffrey C. Lagarias — verified, and accurately described.

Every figure above is emitted by `code/src48_emit_report_block.py` from the gate logs and the archived literature record. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

**Drill 16/16 by the check named for each, both controls clean, no malformed
mutations in the final pass.**

A fidelity check has a failure mode a mathematical check does not. Its
**locators** can stop finding anything — and a locator that finds nothing reports
its subject as clean. Both halves of Finding 1 went missing that way on the first
pass:

- one search normalised whitespace on the haystack but not the needle, so
  `\mathcal O_L` became `\mathcalO_L` in the text and never matched. The gate
  reported the handoff as *not making the claim it plainly makes*, and the finding
  silently disappeared. **A search that normalises one side only is a search that
  answers "no".**
- the constant tracer treated `2111.02635` as a number with five decimals and
  reported it as appearing in no round document. True, and completely the wrong
  reading: it is an arXiv identifier, and the right check for a reference is
  whether it resolves and says what it is said to say. That would have been a
  finding published against a correct citation.

So the gate now carries a **failure for every locator that comes back empty** —
the reference list must contain at least four arXiv identifiers to count as
located, the file manifest must name at least five files, and each half of the
occupancy arithmetic must be found. Six of the sixteen drill defects break a
locator rather than a comparison, because that is where this kind of check dies
quietly.

**Two defects were re-aimed after the pre-flight named them.** Replacing the
whitespace-squeezer with the identity function changed nothing — the handoff
happens to write that lemma in exactly the canonical spacing, so both sides
matched unsqueezed. And pointing the reference-list locator at the following
section changed nothing either, until the locator was taught to recognise its
subject: §26 is a list of working-style bullets and passed a bullet count
happily. Third item running that the pre-flight has paid for itself.

## Route map

Item 48 is a handoff rather than a round, so the nine-item run of file-order
agreeing with the route map ends here by kind rather than by disagreement. Item 49
returns to the numbered line.

## What this run does not claim

1. That any of the mathematics the handoff summarises is correct. That was
   RUN-019 through RUN-029, and this run deliberately re-checks none of it.
2. That the handoff is complete. Fidelity is not coverage: a claim it simply
   omits leaves no trace for this check to find.
3. That the reference list is right beyond the entries checked. Two entries
   (Rozier 1805.00133, López–Stoll 2101.12747) were not fetched, and the run says
   so rather than counting them as verified.
4. That the corpus is every document the line has produced — only every markdown
   document shipped inside a `Hard_Zeta*.zip` in the source folder.
