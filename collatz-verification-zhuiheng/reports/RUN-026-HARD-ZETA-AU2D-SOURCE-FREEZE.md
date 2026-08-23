# RUN-026 — Hard-Zeta A-U.2d: everything checks, the bi-exact regime is not one any real start is in when it crosses, and one cited reference has been withdrawn

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d_bundle.zip` (source item 44) — Transducer Rationality via Source Freeze, Bi-Exact Renewal, and a Complexity-Transfer No-Go, shipped with `Hard_Zeta_AU2d_Literature_Notes_v0.1.md`
**Tools:** [`src44_source_freeze.py`](../code/src44_source_freeze.py) · [`src44_drill.py`](../code/src44_drill.py) · [`src44_emit_report_block.py`](../code/src44_emit_report_block.py)
**Logs:** [`src44-au2d.json`](../data/gate-logs/src44-au2d.json) · [`src44-drill.json`](../data/gate-logs/src44-drill.json) · [`au2d-literature-check.json`](../data/external/au2d-literature-check.json)

**Result: every theorem in the round holds, exactly, on real orbits — including the 2-adic shift-hereditary source identity, verified with a negative control. Two findings, one about scale and one about provenance. Neither touches the mathematics.**

---

## The round is a negative result about proof architecture, and it says so

A-U.2d does not close CASP. It proves why transducer rationality *alone* cannot:
once a positive integer source freezes, its lift tail is `0^∞` — for **every**
positive integer source. So any statistic reading only that tail takes the same
value on a convergent orbit, on a hypothetical divergent one, and on a CASP
candidate. The round names this the **Transducer Rationality Standalone No-Go**
and draws the right conclusion: a successful proof must add a non-source-only
observable.

That makes it unusually checkable for a Hard-Zeta round. Source freeze, endpoint
exposure, the bi-exact horizon and the adelic bank identity are statements about
**actual positive integers** — no hypothetical object required. All verified here
exactly.

### The deepest one, and it has a negative control

§2's **Shift-Hereditary Source Theorem** says every actual odd endpoint is the
unique 2-adic source of its own future exponent tail:

> `𝓑(σ^s q) = −Σ_{j≥0} 2^{Q_j}/3^{j+1} = Y_s` in `ℤ₂`

Evaluated in `ℤ/2^N` with the modular inverse of 3 — no 2-adic library, nothing
approximated. It holds at every shift tested.

**The control is the part that makes that worth saying.** Pairing one orbit's
series with a *different* orbit's endpoint must fail, and it does; without that,
a modular slip making everything congruent to everything would have read as a
perfect confirmation. Both counts are in the block below.

---

## Finding 1 — the bi-exact regime is not one any exhibitable start is in when it crosses

§15 concludes `F₂₃(y)/L(y) → 0`: the source is frozen and the endpoint exact
*long before* a large B-atom's first coefficient crossing. That is derived from
`L(y) ≥ c·y^κ`, which holds for **surviving** crossings — of which RUN-023 found
**0** below `2·10⁵`.

Asked of starts that exist, the ordering is **reversed, and overwhelmingly**: the
first crossing happens *before* the source freezes on **99.07%** of them. The
share in the round's own regime is under one percent.

This is not a contradiction and not a correction. Real starts do not satisfy §15's
hypothesis, so the theorem says nothing about them. What the number gives is
scale: "the remaining obstruction lives in the bi-exact regime" is a true and
useful localisation, and it points at a regime **essentially nothing exhibitable
is in at the moment it matters**. The horizons are logarithmic and ordinary first
crossings are short, so the two only separate once `L` is forced to grow
polynomially — which is exactly the surviving-B hypothesis, and exactly what has
never been observed.

## Finding 2 — a cited reference has been withdrawn

The bundle ships `Hard_Zeta_AU2d_Literature_Notes_v0.1.md` with four primary
references. All four were fetched and checked against what the notes attribute to
them; the record is archived at
[`data/external/au2d-literature-check.json`](../data/external/au2d-literature-check.json).

**Three are live and say what the notes say they say**, including verbatim
disclaimers: Kramer's *"not a verification method for the Collatz conjecture, but
a symbolic diagnostic approach"*, and Niu's *"no claim toward the Collatz
conjecture or Terras's coefficient-stopping-time conjecture"*.

**The fourth — arXiv:2605.13886, Niu — is WITHDRAWN**, as of 2026-05-20, on the
stated ground that later work by Rozier and Terracol had already enumerated the
relevant data. The notes list it as a primary reference without saying so.

Three things make this a one-line fix rather than a problem:

1. Every claim the notes attribute to it **is** in the paper, verbatim. Nothing
   was misread.
2. It is **not load-bearing**. A-U.2e.4 §12 and A-U.2d §21 both state explicitly
   that they do *not* elevate Niu's numerical observation to a theorem, and derive
   the Farey / Stern–Brocot geometry from the integer determinant instead. No
   theorem in either round rests on it.
3. The withdrawal reason names **Rozier–Terracol (arXiv:2502.00948)**, which the
   notes already cite. The data has a live home.

RUN-025 measured that same Stern–Brocot clustering independently and without
evaluating a logarithm, so this arm's own evidence for the phenomenon does not
depend on the withdrawn paper either.

---

<!-- BEGIN GENERATED measured block: python code/src44_emit_report_block.py -->

| what | measured | value |
| --- | --- | --- |
| 2-adic source identity `𝓑(σ^s q) = Y_s` | evaluated in `ℤ/2^N`, 400 cases across four shifts | `400 matches, 0 mismatches` |
| …**negative controls that correctly failed** | one orbit's series against a different orbit's endpoint | `380` |
| …negative controls that wrongly matched | must be zero | `0` |
| freeze-bound violations `F₂(y) ≤ ⌊log₂ y⌋` | exact, 2041 starts | `0` |
| mean `F₂ / ⌊log₂ y⌋` | how loose the bound runs | `0.5309` |
| max `F₂ / ⌊log₂ y⌋` | 1 means the bound is attained | `1.0` |
| …starts where it is **attained** | so the tightness is measured | `1` |
| endpoint-exposure violations | `m ≥ F₃(y) ⟹ Y_{s+m} < 3^m` | `0` |
| bi-exact horizon violations | `floor_log32`'s defining inequalities and the domination, separately | `0` |
| …starts where `⌊log₂ y⌋` is **strictly** below `⌊log_{3/2} y⌋` | the domination is not vacuous | `2041` |
| contraction violations `S(x) < 2x` | exhaustive over 99999 odd x | `0` |
| the two expressions for `𝒜_m` disagree on | accumulated series against `2^{Q_m}Y_{s+m}/3^m` | `0` |
| `v₂(𝒜_m) ≠ Q_m` on | numerator carries `2^{Q_m}`, both odd elsewhere | `0` |
| Archimedean bound violations before the crossing | `y ≤ 𝒜_m ≤ y + m/3` | `0` |
| …starts where it fails **after** the crossing | the negative half, without which the test is one-sided | `571` |
| defects planted / caught by their own check | `code/src44_drill.py` | `12 / 12` |

**§15, asked of starts that exist.** Section 15 concludes `F₂₃(y) < L(y)` for large surviving B-atoms. On real starts:

| | starts | share |
| --- | --- | --- |
| source frozen **before** the crossing (§15's regime) | 120 | 0.84% |
| the crossing happens **first** | 14153 | 99.07% |
| tie | 13 | |

out of `14286` starts. RUN-023 measured `0` surviving crossings below `2·10⁵`, which is the hypothesis §15 needs.

**The four cited references, checked.** `3` live and saying what the notes attribute to them; `1` withdrawn.

| arXiv | status | every attributed claim present |
| --- | --- | --- |
| `1805.00133` | **live** | yes |
| `2607.10041` | **live** | yes |
| `2502.00948` | **live** | yes |
| `2605.13886` | **WITHDRAWN** (2026-05-20) | yes |

`arXiv:2605.13886` was withdrawn on **2026-05-20** — later work by Rozier and Terracol had already enumerated the relevant data. It is **not load-bearing**: A-U.2e.4 section 12 and A-U.2d section 21 both state explicitly that they do NOT elevate Niu's numerical observation to a theorem, and derive the Farey / Stern-Brocot geometry from the integer determinant instead. No theorem in either round rests on it.

Every figure above is emitted by `code/src44_emit_report_block.py` from the gate logs and the archived literature record. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument, and one thing I could not pin down

`src44_drill.py` plants 12 defects and requires each to be caught **by the check
named for it**. Two habits were carried in from items 42 and 43 and both earned
their place immediately: a subprocess timeout from the start, and defects aimed at
**subjects rather than comparisons**.

Two misses on the first pass:

- **A check comparing a mutated function against itself.** The bi-exact horizon
  bound read `max(F₂,F₃) ≤ ⌊log_{3/2} y⌋+1` — but `F₃` is *defined* as that
  expression, so both sides moved together and replacing `floor_log32` with
  `floor_log2` left the gate green. The gate now asserts `floor_log32`'s
  **defining inequalities** (`3^k ≤ 2^k·y < ` the next one) and the domination
  `⌊log₂ y⌋ ≤ ⌊log_{3/2} y⌋` separately, with a guard requiring the domination to
  be **strict** somewhere.
- **A defect that crashed rather than failed.** A negative shift count raised
  inside the gate, so the drill saw "did not produce JSON" rather than the named
  check firing. **A planted defect must break the result, not the interpreter.**
  Re-aimed at a threshold that is wrong but evaluable.

**One thing is unresolved and is recorded rather than smoothed over.** On that
same first pass the byte-restore control `N2` reported the gate **not** restored
byte-exactly. An immediate integrity check found no leftover mutation and no
control suffix, and a clean re-run passed `N2` with the file's md5 identical
before and after. I do not have a definitive account of the one-off. It is stated
here because a control that fires once and is then explained away by a passing
re-run is exactly the kind of thing this tree exists to not do.

## Route map

`ROUTE_MAP v2.0` and the round's own §23 name **A-U.2d.1 — Bi-Exact
Source–Endpoint Rigidity** as the next line: attack `2^Q z = 3^L y + B` with `y`
and `z` both exact positive integers and `Q/L` near-critical. Items 45–47 are
`AU2d1`, `AU2d2`, `AU2d3`, so the file ordering agrees for the seventh time.

Finding 1 is directly relevant to it: at the scales where that equation is
supposed to bite, `L` is polynomial in `y` while the horizons are logarithmic, and
this run's measurement says nothing exhibitable is there yet.

## What this run does not claim

1. That CASP is closed, or that the round claims to close it. It proves the
   opposite about its own channel and says so.
2. That §15 is wrong. Its hypothesis is about surviving crossings; real starts do
   not satisfy it, and the measurement reports where real starts sit rather than
   contradicting the theorem.
3. That the mathematics in any cited paper is correct — only that the citations
   say what the notes say they say, and that one is withdrawn.
4. That the withdrawn citation affects any result. It does not, and §21 of the
   round already declines to use it as one.
