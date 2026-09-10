# RUN-052 — v0.3's decision procedure, run until it leaves this tree; and a compiler target with an empty domain

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`02_Next_Compiler_Targets`](../../../amral/public/bsd/phase2/files/02_Next_Compiler_Targets.md) and [`06_Witness_Network_v03_Integration`](../../../amral/public/bsd/phase2/files/06_Witness_Network_v03_Integration.md) — what to build next, and the design that answers the first item
**Tools:** [`src54_compiler_targets_and_v03.py`](../code/src54_compiler_targets_and_v03.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src54-compiler-targets.json`](../data/gate-logs/src54-compiler-targets.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `06` v0.3 exists to close the exact `UNKNOWN` that RUN-045 emitted — its stated improvement is *A2 H2 UNKNOWN → exact finite local isogeny test*. So the procedure was run, per member, at each member's odd additive prime. **It reaches its first branch and stops.** Branch 1 (potentially multiplicative ⟹ `FAIL`) **never fires**: every twist's odd additive prime is potentially *good*, measured at RUN-034. Branches 2 and 3 — `E[p]` irreducible over `F_p`, then the kernel polynomials of a local `p`-isogeny and its dual — are local Galois data **this tree does not compute**. `H3` computes and passes at all **19** members with witness `ℓ = 29`; `H1` is `UNKNOWN` at every member because all 19 lie above RUN-036's certified range; `PERIOD` is RUN-039's open item. **Two of five steps decided, one partial, two outside this arm** — and `FINAL` is unreachable. Second finding: **`02`'s target 3 has an empty domain on this curve.** It asks for an ordinary finite-exception compiler for `p | g_mult`, and RUN-033 computed `g_mult^odd = 1`, which no odd prime divides. That is not the target achieved; it is the target **inapplicable**, and the two are reported as different things. `𝒜_odd` is exactly `{q}` for every member and **empty for the base curve**, so `06`'s claim that the odd additive primes stay a finite table holds here — the `∀p` quantifier does not reinflate. Both of `02`'s discipline lines are obeyed.**

---

## The procedure, run to where it stops

`06` v0.3 is written as pseudocode for a **fixed odd additive prime**. Run at
`q` for each of the 19 members of `𝒫` below 4,000:

| step | verdict here | why |
| --- | --- | --- |
| `GLOBAL_H1` | **UNKNOWN** at all 19 | every member is above RUN-036's certified range; irreducibility holds by RUN-031, absolute irreducibility is not certified |
| `LOCAL_H2` branch 1 | **not taken**, at all 19 | the odd additive prime is potentially **good**, so the `FAIL` branch never fires |
| `LOCAL_H2` branch 2 | **not computed here** | `E[p]` irreducible over `F_p` — local |
| `LOCAL_H2` branch 3 | **not computed here** | kernel polynomials of a local `p`-isogeny and its dual — local |
| `H3` | **PASS** at all 19, witness `ℓ = 29` | computed |
| `PERIOD` | **OPEN** | RUN-039 left `c_E = 1` open; RUN-040 ran `01`'s weaker sufficient condition |
| `FINAL` | **not reachable** | `LOCAL_H2` and `PERIOD` are not decided |

**Two decided, one partial, two outside.** The one branch that would actually
resolve `A2`'s `UNKNOWN` — the isogeny-kernel test that v0.3 was designed
around — is the one this arm cannot run.

That is worth stating plainly rather than scoring as a near miss. RUN-045
emitted `H2 = UNKNOWN` at the additive prime because `05`'s no-go decides only
the potentially multiplicative case and RUN-034 found it silent otherwise. `06`
v0.3 is the right instrument for that gap. **Running it here narrows nothing**,
because the branch it adds needs arithmetic this tree does not do — and the
result of running it is knowing precisely which branch that is.

## Branch 1 never fires, which is itself the measurement

If any member's odd additive prime were potentially multiplicative, v0.3 would
return `FAIL` immediately and the curve would leave the family. None is. Every
one of the 19 twists is potentially **good** at `q`, which is the case `05`'s
no-go was silent about (RUN-034) and the case RUN-042's period barrier is
about.

So the family survives v0.3's cheap branch and lands entirely in the expensive
one. **The uniformity is the finding**: there is no member for which this arm
gets a free answer.

## `𝒜_odd` stays a finite table

`06` claims the odd additive primes 依然只產生有限 table，因此 `∀p` 沒有重新膨脹.
Measured:

| | |
| --- | --- |
| base curve `696.e1`, `𝒜_odd` | **empty** — its only additive prime is 2 |
| every member `E_q`, `𝒜_odd` | **exactly one prime, and it is `q`** |

The claim holds, and holds in the strongest form available: one row per member,
none for the base. Twisting by `q` adds `q` and nothing else.

## `02`'s four targets, including the one with no domain

| # | target | this arm |
| --- | --- | --- |
| 1 | Additive FW-H2 compiler | `06` v0.3 is the design; its decisive branch is local. **H2 stays `UNKNOWN`** (RUN-045) |
| 2 | Period compiler | **`PERIOD_SAFE` not emitted**; RUN-040 checked the weaker `p ∤ c` on all 19 |
| 3 | Ordinary finite-exception compiler for `p ∣ g_mult` | **domain is empty** — `g_mult^odd = 1` |
| 4 | Only then, census | **no census exists**; RUN-045 keeps 7 `UNKNOWN` rows visible |

Target 3 deserves the emphasis. RUN-033 computed `g_mult^odd = 1` from the two
odd multiplicative primes' data, and **no odd prime divides 1**. There is no
finite exception to compile on this curve, so a compiler for target 3 would
have nothing to consume.

**Inapplicable is not achieved.** A scoring rule that counted an empty domain
as a pass would report three of four targets in hand, and that would be false.
The log records `target_3_domain_is_empty: true` next to the divisor list,
which is empty, so the distinction survives into the data rather than living
only in this sentence.

## Both discipline lines obeyed

> **No database scaling until this is exact.**

Target 1 is not exact here, and no census over the search pool exists in this
tree. Obeyed — though obeyed by *not having built the thing*, which is a
weaker kind of compliance than passing a test, and the log says so.

> The `UNKNOWN` rows must remain visible.

RUN-045's Level-1 certificate carries **7** `UNKNOWN` rows in its emitted
output, not in a footnote. Obeyed.

**The check for the first line was wrong when it was first written.** It
scanned the gate-log filenames for the word *census* and matched
`src19-conductor-census.json`, which is a conductor table — a completely
different object — and turned the gate red. `02` §4 specifies the census by its
five status columns (`GENERIC_PASS`, `FINITE_EXCEPTION_PASS`,
`ADDITIVE_LOCAL_UNKNOWN`, `PERIOD_UNKNOWN`, `TRUE_REJECT`), so the check looks
for at least three of those in a log's contents. **A check that matches on a
name matches things that merely share a name.**

**And then the fixed version matched itself.** It was green when it ran, and
red at the next round's drill baseline — because the five status names are
written into `src54-compiler-targets.json`, which the detector then scans. The
first run passed only because the gate's own log did not exist yet.

**A check whose first run is green because its own output is not there yet has
not been tested.** That is a new entry in this line's drill discipline, next to
*a cache is state* and *a control whose stated reason is false is not a
control*. The repair excludes this gate's own log by name and records the
exclusion and its reason in the output, and a ninth defect was planted for it:
remove the exclusion and `compiler-targets` goes red.

Both of the round's own defects were caught by machinery rather than by
reading — the filename match turned the gate red on its first run, and the
self-match turned it red at the drill baseline. Neither was noticed by looking
at the code.

## The drill

**212 defects, 212 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 41 controls undisturbed, over 80 checks.

The 5 planted for this gate, each turning `compiler-targets` red and nothing else:

| planted defect | went red |
| --- | --- |
| v0.3's two local branches are reported computed in this tree | `compiler-targets` |
| the base curve is reported carrying an odd additive prime | `compiler-targets` |
| 02's target 3 is scored achieved where its domain is empty | `compiler-targets` |
| the census detector goes back to matching on the filename | `compiler-targets` |
| the census detector stops excluding this gate's own log, which carries the five status names it searches for | `compiler-targets` |


## What this round does not claim

* **Nothing about `LOCAL_H2`.** Branches 2 and 3 are not computed, not
  estimated, and not inferred from branch 1 not firing.
* **Running v0.3 is not implementing v0.3.** This gate executes the decidable
  part of a published procedure against this family; it does not build the
  compiler `02` target 1 asks for.
* **`𝒜_odd` is measured on the 19 members below 4,000**, by the same
  `odd_additive_primes` RUN-040 used. A larger bound is a different
  measurement.
* **The empty domain is this curve's**, not a statement about `02`'s target 3
  in general. Another curve with `g_mult^odd > 1` would give it work.
* **`H1 = UNKNOWN` is a range limit, not a negative result.** RUN-036 certified
  38 primes; the 19 members all sit above them.
* **The discipline-line audit checks artefacts, not intent.** It verifies that
  no five-column census exists in this tree and that the `UNKNOWN` rows are in
  the emitted output.
* **The census detector now has a hand-written exclusion.** Skipping this
  gate's own log by name is correct for this gate and does not generalise: a
  later gate that writes the same five strings would trip it again.
