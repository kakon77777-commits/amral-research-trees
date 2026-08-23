# RUN-028 — Hard-Zeta A-U.2d.2: the saturation equivalence is an exact iff and holds both ways, the gap prediction survives contact with real orbits, and two of my own instruments turn out to have been measuring nothing

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d2_bundle.zip` (source item 46) — Rotation-Envelope Attainability via Boundary-Occupancy Loss, Second-Order Non-Attainment, and a Mechanical-Mismatch Collision. Ships a verification script, a constants JSON, and literature notes.
**Tools:** [`src46_attainability.py`](../code/src46_attainability.py) · [`src46_drill.py`](../code/src46_drill.py) · [`src46_emit_report_block.py`](../code/src46_emit_report_block.py) · [`report_block_guard.py`](../code/report_block_guard.py) · [`emitter_guard_demo.py`](../code/emitter_guard_demo.py)
**Logs:** [`src46-au2d2.json`](../data/gate-logs/src46-au2d2.json) · [`src46-drill.json`](../data/gate-logs/src46-drill.json) · [`au2d2-literature-check.json`](../data/external/au2d2-literature-check.json) · [`emitter-guard-demo.json`](../data/gate-logs/emitter-guard-demo.json) · [`report-block-guard-selftest.json`](../data/gate-logs/report-block-guard-selftest.json)

**Result: the round's one unconditional theorem is verified as an exact `iff`, in both directions, on every real first crossing. Its asymptotic non-attainment bound makes a falsifiable prediction about orbits that exist, and that prediction holds. Two artifact findings, both recurrences, and two in my own instruments — the guard certifying these reports' figures could not fail, and the suite's defect total had been refusing to compute for seven rounds. Nothing wrong in the mathematics, and two failure modes I went looking for and did not find.**

---

## The claim that does not need a hypothetical object

Most of A-U.2d.2 is about **surviving** crossings — the `Θ(√L)` non-attainment
gap, the relative-efficiency barrier, the survival headroom — and RUN-023
measured **0** of those below `2·10⁵`. That half is conditional, as usual.

§17 is not. The **Rotation-Envelope Saturation Equivalence** says

> `B/3^L = U_β(L)`  **⟺**  `Q_j = ⌊βj⌋` for every `j < L`

— the envelope is attained exactly when the proper-prefix code is completely
mechanical. Both sides are exact: `U_β(L)` is rational (RUN-027) and `⌊βj⌋` is a
bit length, so this is an **iff between integers**.

Verified in both directions on 9,999 real first crossings. All four cells of the
contingency table are reported below, and **both diagonals are inhabited** — an
equivalence checked only where it is easy is half-checked, so the run fails if
either diagonal is empty as well as if either off-diagonal is not.

## A prediction the round's own data can be held to

The non-attainment gap `G(y, L)` is asymptotic and clamps to zero at small `L`.
That gives a falsifiable statement about orbits that exist even though the
theorem behind it is about surviving crossings that do not:

> wherever `G > 0`, the envelope must **not** be attained.

Measured: **75** crossings have `G > 0`, and **0** of them attain the envelope.
The largest `L` at which attainment occurs is **9**; the smallest `L` at which
`G > 0` among real crossings is **19**. An asymptotic bound and exact data
agreeing at their boundary is worth more than either alone.

---

## Two failure modes looked for and not found

Worth stating because a run that only reports what it found overstates how much
of the space it swept.

**The shipped script switched from `mpmath` to plain `float`.** Item 45's script
ran at 80 digits; this one uses `math.log2`, `math.sqrt`, and — the part that
invited a closer look — `math.ceil(math.log2(y + N/3))`. A ceiling of a floating
logarithm is the classic off-by-one: if `y + N/3` sits a hair under a power of
two, the rounded log can land above it and `H` flips, moving every number in the
file.

Recomputed against an exact integer route (the least `k` with `2^k ≥ y + N/3` in
`Fraction`s): **0 mismatches across all 15 rows**, with the closest approach to a
power of two at `0.0247` in `log₂` — against a float `log2` error of order
`10⁻¹⁵`, a margin of **13.4 orders of magnitude**. The failure mode is not
present, and the margin is measured rather than asserted.

**No over-publication either.** Item 45's JSON printed 79 decimals from an 80-dps
sum and the last few were wrong. This one prints float `repr`, which claims about
17 significant digits and delivers them. Nothing to report.

## Finding 1 — the JSON is still not what its script produces

Third occurrence of the item-35 class (items 35, 45, 46):

| script writes | JSON has |
| --- | --- |
| row key `y` | *absent* |
| row key `relative_gap_lower_estimate` | `relative_gap` |

Top-level keys match this time; the divergence is entirely in the rows. Every
value is correct — recomputed from the round's own formula, 0 disagreements — so
this is provenance, not arithmetic. But re-running the published program would
still not reproduce the published file.

**A correction to my own check, made before the finding was published.** The
provenance comparison first used a `[a-z_]+` pattern to read the script's row
keys, which silently dropped `L`, `G` and `G_over_sqrt_L` — all of which start
with a capital — and reported three keys as missing from the JSON when they were
present. **A provenance check that miscounts is worse than none**, because it
inflates a real finding into a wrong one. Fixed to `[A-Za-z_]+` before anything
was written down.

## Finding 2 — the withdrawn citation recurs a third time, now under a "rechecked" heading

`arXiv:2605.13886` (Niu) has been **withdrawn since 2026-05-20**. RUN-026 reported
it for the A-U.2d notes; RUN-027 reported the recurrence for A-U.2d.1. The
A-U.2d.2 notes cite it again — and this time under the heading **"Collatz primary
references rechecked"**.

Everything said before still holds: every claim attributed to it is present and
verbatim, and it is not load-bearing anywhere in the line. What changes is that
the notes now assert a recheck was performed, and a recheck that does not surface
a withdrawal is the thing worth flagging. Three bundles is not an oversight.

---

<!-- BEGIN GENERATED measured block: python code/src46_emit_report_block.py -->

**The Saturation Equivalence, all four cells.** `B/3^L = U_β(L)` against `Q_j = ⌊βj⌋ ∀ j<L`, both sides exact, on `9999` real first crossings:

| | mechanical prefix | not mechanical |
| --- | --- | --- |
| **envelope attained** | `7137` | **`0`** |
| **not attained** | **`0`** | `2862` |

Both off-diagonals are empty, and both diagonals are inhabited (`True`) — so the equivalence is exercised in both directions, not only where it is easy.

| what | measured against | value |
| --- | --- | --- |
| largest `L` at which the envelope is attained | exact rationals | `9` |
| crossings where the round's gap `G > 0` | the prediction's whole domain | `75` |
| **…of those, attained anyway** | the round predicts zero | `0` |
| smallest `L` with `G > 0` among real crossings | for comparison with the line above | `19` |
| constants disagreeing with their closed forms | η=1/(6ln2), κ_rot=1/(12√2), ln2/(2√2), and κ/η = the relative constant | `0` |
| shipped `G` rows disagreeing | recomputed from the round's own formula, 15 rows | `0` |
| float-vs-exact ceiling mismatches | `ceil(log2(y+N/3))` against an integer route, 15 rows | `0` |
| …closest approach to a power of two | in `log₂`, across those rows | `0.024674` |
| …margin over float `log2` error | orders of magnitude | `13.4` |
| defects planted / caught by the check named for each | 4 of the entries are robustness properties, not defects | `12 / 12` |

**Provenance.** Row keys the script writes that the JSON lacks: `y, relative_gap_lower_estimate`. Row keys the JSON has that the script never writes: `relative_gap`. Top-level keys match: `True`.

**Literature.** `arXiv:2605.13886` has been withdrawn since 2026-05-20 and is cited for the **3rd bundle running**.

Every figure above is emitted by `code/src46_emit_report_block.py` from the gate logs and the archived literature record. None is typed into this file, and that is checked rather than claimed: see the guard report below.

<!-- END GENERATED measured block -->

---

## The instrument — and a change that should have been made three items ago

The drill's first pass reported two misses, and **both were my own defects rather
than gaps in the checks**: one raised (`1 << -1`, a negative shift) and one was a
no-op (`<` → `<=` differs only when `y + N/3` is exactly a power of two, which it
never is here).

That is the fourth item where a malformed defect cost a full pass — items 42, 44,
45, and this one. So rather than fix the two and move on, the drill now runs a
**pre-flight on every mutation** before attributing anything:

| screened | reported as |
| --- | --- |
| the gate did not terminate | `malformed: the gate did not terminate` |
| the gate raised | `malformed: the gate raised` |
| the whole report is identical to baseline | `malformed: the mutation changes nothing` |

**A defect that changes nothing was never planted**, and saying that is different
from saying a check missed it. Blaming the check for the drill's own aim is a way
of quietly inflating how well the checks are covered.

**Four of the twelve entries are robustness properties, not defects** — the item-45
lesson applied deliberately this time rather than discovered. Each breaks
something and asserts that the gate **stays green** because another check covers
it: weakening the "both diagonals inhabited" guard, breaking the constants'
mutual-consistency relation, reading `G` back out of the JSON instead of
recomputing it, and re-introducing the lowercase-only regex. If a future refactor
removes the covering check, they go red.

## Finding 3 — my own report emitters shipped a guard that could not fail

Found while writing this run's emitter, in my own tooling rather than in the
subject's. Every report block in this arm is generated from the gate logs so that
no figure is typed by hand, and since RUN-025 the emitters have carried what
looked like a check that the generation is honest:

```python
digits = [m.start() for m in re.finditer(r"\d", block)]
missed = [i for i in digits
          if (block[:i] + ("9" if block[i] != "9" else "0") + block[i+1:]) == block]
```

Replacing one character of a string and asking whether the result equals the
original. It is `False` for every string and every substitution, so `missed` was
empty in every possible universe. The emitters printed `digits_guarded: 227`, `172`, `222` — a
count of the digits in the block, dressed as a count of digits checked — and
measured nothing at all. Shipped in **src43, src44 and src45**, and it would have
gone into this one by copy.

The property it was reaching for is real and has a real failure mode: *every
figure in the block must come from a log, not from the emitter's own format
strings.* So perturb the **log** and require the block to move. A number read
from a log follows it; a number typed into prose does not.

[`code/report_block_guard.py`](../code/report_block_guard.py) does that for every
value in every log, stores the resulting set of load-bearing figures beside the
gate logs, and goes red when a figure stops tracking. All four emitters now use
it — **55, 50, 72 and 28** figures respectively — and all four reports regenerate
byte-identically, so nothing published was wrong; it was only unguarded.

**Shown rather than asserted.**
[`code/emitter_guard_demo.py`](../code/emitter_guard_demo.py) freezes one figure
in each of the four emitters at today's value, the way a copy-paste would, and
requires the emitter to go red — with the unchanged emitter green as the control
([`emitter-guard-demo.json`](../data/gate-logs/emitter-guard-demo.json), 4/4).

Two of its own first attempts changed nothing: the demo replaced ``` `9999` ```
with the same literal, and two emitters print that figure without backticks, so
the substring never occurred. Green for the wrong reason — the same malformed
mutation the drill pre-flight above exists to catch, committed twice in one
sitting, by me, in the tool built to demonstrate rigour. The demo now screens
every freeze against a perturbed log before reading its verdict.

Two things worth saying plainly. The vacuous guard survived three rounds of
review because it *printed a number that went up*, and a count that grows reads
like coverage. And the automatic version of the stronger property — *no number
anywhere in the block is typed* — was built, measured, and abandoned: perturbing
`13.4` produced `97.05`, whose `0` was not there before, and a figure printed as
`len([])` has no digit in the log to perturb at all. Both came back as
accusations against correct code. The guard claims the scope it can defend.

## Finding 4 — the suite's defect total refused to compute, and had been refusing for seven rounds

Found by running it, which is the only reason it was found.

[`code/suite_totals.py`](../code/suite_totals.py) exists because the README and
the charter quote "N planted defects, all caught by the check named for each",
and a figure typed into prose drifts. It was built with one explicit rule, which
is written at the top of the file: **anything it cannot interpret is listed and
makes it exit non-zero, rather than quietly contributing nothing.**

That rule worked exactly as designed. `src22` renamed one tally key, `src41`
renamed both, and from that point the script refused on every run:

```
"uninterpreted": ["src22-drill.json", "src41-drill.json", … "src46-drill.json"],
"ok": false
```

And the archived summary it feeds kept saying `drills: 20, uninterpreted: [], ok:
true`, because a refusal writes nothing. **Seven drills and 91 defects were
outside the published figure for seven rounds**, including this run's own. The
aggregator's own drill had been dead the whole time too — its first act is to
require a green baseline, and the baseline was not green.

| | before | after |
| --- | --- | --- |
| drills counted | `20` | **`27`** |
| defects planted / caught | `467 / 467` | **`560 / 560`** |
| controls undisturbed | `48 / 48` | **`62 / 62`** |

The number was never wrong about what it counted; it was wrong about what it
covered, which is the harder kind to notice. Three changes: the tally shapes are
enumerated with the run that introduced each, **every row now reports which shape
it used** so the next rename is visible in the output instead of only in an exit
code, and the drill grew two entries — one that removes the newest shape again
and requires the total to move, one that shortens a `caught` count *in that
shape*, because a shape can be recognised while its numbers go unread. 8/8, both
controls quiet.

**The lesson is not about schemas.** A check that refuses is only half a control;
the other half is somebody reading the refusal. This one printed `ok: false` and
exited `1` for seven rounds into a workflow that never looked at either.

## Route map

`ROUTE_MAP v2.2` continues the line; item 47 is `AU2d3`, so the file ordering and
the route map agree for the ninth time.

## What this run does not claim

1. That the `Θ(√L)` non-attainment gap holds. It quantifies over surviving
   crossings, of which none is known; only its consequence for real orbits was
   tested.
2. That the boundary-occupancy machinery of §§1–16 is verified. It is not — those
   sections rest on the surviving-crossing setting throughout.
3. That the float arithmetic in the shipped script is adequate in general. It was
   checked **at the fifteen shipped points** and is adequate there by a wide
   margin; a different `(y, L)` could land near a boundary.
4. That the withdrawn citation affects any result. It does not, in any of the
   three rounds that cite it.
