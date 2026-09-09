# RUN-030 — the machine-checkable arithmetic certificate for 696.e1, and what building it caught

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`28_Submission_Gate`](../../../amral/public/bsd/phase2/files/28_Submission_Gate.md) — the corpus's own five conditions for writing a theorem paper, and the one of them that is this arm's
**Tools:** [`src32_696e1_certificate.py`](../code/src32_696e1_certificate.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src32-696e1-certificate.json`](../data/gate-logs/src32-696e1-certificate.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `28_Submission_Gate`'s fourth box — "Produce machine-checkable arithmetic certificate for 696.e1" — is delivered. Twenty quantities, every one recomputed from the a-invariants `[0, 1, 0, 8, −16]` alone and compared against the round that logged it, and all twenty agree. And the first draft caught its own author: three values I filled from memory were wrong — `c4` as 448 for the true `−368`, `c6` as `−20512` for `16064`, and the j-invariant that follows from them. A certificate that quotes its author is exactly the artefact a certificate exists to replace, and the design that caught it is that every row is a derivation rather than a remembered number. Rows with no logged predecessor now say so instead of inventing one.**

---

## The box this closes

`28_Submission_Gate` lists five things to do before a theorem paper is written:

```text
[ ] Independent expert referee reproduces all source mappings
[ ] Check latest versions/publication status of BSTW and Fouquet–Wan
[ ] MathSciNet/zbMATH/Scholar novelty sweep
[ ] Produce machine-checkable arithmetic certificate for 696.e1
[ ] Rewrite proof without depending on LMFDB prose where an exact source/
    computation is available
```

Four are for people. **The fourth is this arm's**, and eleven rounds have
produced its content and left it scattered across eleven gate logs. This round
assembles it — and, more to the point, makes it recompute itself.

## What makes it a certificate and not a summary

Every row carries three things: the value, the round that first logged it, and a
**derivation performed here from the a-invariants and nothing else**. A row
whose derivation disagrees with the logged value fails the gate. So what a
referee re-runs is not a table of numbers; it is a program that produces them,
and the agreement is the check.

| quantity | value | from |
| --- | --- | --- |
| discriminant | `−178,176` | RUN-016 |
| `c4`, `c6` | `−368`, `16,064` | computed here |
| `j` | `24334/87` | computed here |
| bad primes | `{2, 3, 29}` | RUN-016 |
| reduction at 2 | `II*`, `f = 3`, `c = 1` | RUN-016 |
| reduction at 3, 29 | `I₁`, `f = 1`, `c = 1` | RUN-016 |
| conductor | `696` | RUN-016 |
| `∏c_p` | `1` | RUN-016 |
| torsion | `1` | RUN-014 |
| root number | `+1` | RUN-014 |
| analytic rank | `0` | RUN-014 |
| `L(E,1)` | `1.631727740071569` | RUN-014 |
| `Ω` | `1.6317277400715688` | RUN-014, repaired RUN-017 |
| `L/Ω` | `1` | RUN-014 |
| **analytic order of Ш** | `1` | RUN-014, unconditional RUN-016 |
| `disc(f₂)` squarefree part | `−174` | RUN-018 |
| `[K_E:Q]` | `16` | RUN-018 |
| `e_E` | `2` | RUN-018 |
| `δ(𝒫_E)` | `1/24` | RUN-009 measured, RUN-018 exact |

**All twenty agree.**

## The first draft quoted its author, and three of three were wrong

Building it, I filled several "logged value" columns from memory. Three were
wrong:

| | I wrote | the truth |
| --- | --- | --- |
| `c4` | 448 | **−368** |
| `c6` | −20,512 | **16,064** |
| `j` | followed from those | **24334/87** |

Nothing downstream had used them — `c4` and `c6` appear in no report of this arm
— so no conclusion moves. What matters is the mechanism: **the certificate's own
design caught its author within one run**, because a row is a derivation and not
a recollection.

The repair is structural, not a correction of three numbers. A row now has two
kinds. *Checked against a logged value* carries what a named round put in its
log and compares. *Computed here, no prior record* says exactly that. **A row
with no logged predecessor no longer invents one**, which is what produced all
three errors.

Two further disagreements in that first run were an artefact I had created: the
float rows compared a value rounded to twelve places against an unrounded one.
They now carry an explicit tolerance of `10⁻⁹`, which is far coarser than the
L-series' own convergence and far finer than anything that would matter.

## And the gate crashed rather than reported

Planting "the certificate is built for a different curve" as a drill defect made
the gate raise a `KeyError`: it indexed `red[2]` directly, and 389.a1's bad
primes are `{389}`. A defect that produces a traceback is not a defect a check
caught — RUN-020 recorded that lesson when two defects recursed instead of
computing, and here it was the gate rather than the defect at fault.

The bad primes are now **found** from the discriminant rather than assumed, and
a missing reduction is reported as a disagreeing row. A certificate built for
the wrong curve should say so.

## The other four boxes

| box | this arm |
| --- | --- |
| independent expert referee | **not ours.** A referee is a person |
| BSTW / Fouquet–Wan publication status | **not ours.** A literature check, and this line's standing rule keeps unpublished work off third-party services while it lives only on GitHub |
| MathSciNet / zbMATH novelty sweep | **not ours**, same reason |
| rewrite without LMFDB prose | **partly, and advanced.** RUN-021 traced every P5 gate to a computation or a named theorem; this certificate replaces the arithmetic half of any LMFDB dependency for 696.e1 |

## What stays cited, and is listed in the certificate itself

* the Manin constant and `BSD(E,2)`, cited from Creutz–Miller in `30`'s (T1),
  verified in no round;
* rational isogeny degrees — RUN-007's `X₀(n)` covers 4 of Mazur's 12;
* **the algebraic rank**, which no round of this arm computes;
* **`#Ш` here is the analytic order**, labelled as such in the row, in its note,
  and in the cited list. RUN-019 audited that substitution as the pattern
  Phase 0 §6 freezes a line for, and the drill now goes red if the labelling is
  stripped while the numbers stay.

## The drill's own state guard fired, and it was right

The first run reported **124 defects all caught by the named check** and then
`20 controls, 20 disturbed a check` with `state restored afterwards: False`.
Every control failing at once is not twenty findings; it is one, and the drill's
own restoration guard is what named it.

The three certificate defects each called `_CERT_MEMO.clear()` in their setup.
So the defect run repopulated the memo **with a corrupted certificate** — the
389.a1 one, or the unlabelled one — and the restore put back only the patched
attribute. Every check and control after that read the stale certificate.

RUN-018 introduced memoisation into this drill and it was safe there, because
nothing patched the memo's inputs. Here three defects do. The fix is to **key
the memo on what the certificate depends on** — the a-invariants and the
identity of the `certificate` function — rather than clearing it by hand:

```python
key = (tuple(cert32.AINVS), id(cert32.certificate))
if _CERT_MEMO.get("key") != key:
    ...
```

Each defect now goes red and the check returns to green after its restore, which
is the property the guard was measuring. **A cache is a piece of state, and a
drill that mutates state must restore it — including state the drill itself
created.**

## The drill

**124 defects, 124 caught by the check named for each — none uncaught, none
caught by the wrong check. 20 controls, none disturbed, state restored, over 58
checks. Twenty minutes and two seconds, on the second run.**

## What this round does not claim

* **The certificate certifies arithmetic, not the theorem.** It says what these
  twenty quantities are and that two independent computations agree on them.
  Nothing in it bears on whether the derived theorem candidate is correct.
* **Agreement is with this tree's own logs.** Where a round was wrong, the
  certificate reproduces the round — which is why RUN-017's period repair and
  RUN-026's height repair had to happen first, and why the period row names
  both.
* **The analytic order of Ш is not the order of Ш.** Said in the row, the note,
  and here.
* **Four of the five boxes remain open** and three of them cannot be closed by
  this arm at all.
