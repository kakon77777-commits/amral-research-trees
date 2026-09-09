# RUN-045 — The hypothesis compiler, run, and a prohibition that turned out to be contested

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`02_Fouquet_Wan_Hypothesis_Compiler`](../../../amral/public/bsd/phase2/files/02_Fouquet_Wan_Hypothesis_Compiler.md) — the document behind the rung RUN-043 placed this line on, with an exact Level-1 output format and three prohibitions
**Tools:** [`src47_fw_hypothesis_compiler.py`](../code/src47_fw_hypothesis_compiler.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src47-fw-compiler.json`](../data/gate-logs/src47-fw-compiler.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the Level-1 certificate is emitted in `02`'s own keys for every odd prime below 200 — 45 rows, **34 `FW_APPLICABLE`, 4 `FW_NOT_APPLICABLE`, 7 `UNKNOWN`** — and every verdict traces to a round of this arm rather than to a fresh assertion. `p = 3` is `UNKNOWN` at H1 because RUN-036 found two *structural* blocks there; `p = 7` and `p = 113` fail H2 because RUN-038 measured `a_p = ±1`; `p = 29` fails both H2 and H3, the latter being exactly RUN-037's finding. **Level 2 is not achieved** — RUN-041 measured `P_loc` non-empty and not known finite — so the gate emits the output `02` mandates in that case, *FW verified for tested primes*, and refuses the upgrade the document forbids. **And `02`'s third prohibition sent this round looking at this arm's own labels — 「不能直接把 `p ∤ ord_ℓ(Δ)` 當完整 H3」 — where it found something larger: **the corpus disagrees with itself**. `08_FW_Weight2_Exact_Translation` boxes exactly that criterion as an **iff** and calls itself the exact weight-2 translation. RUN-046 takes that up. Either way the label was missing: RUN-037's and RUN-039's H3 verdicts are complete H3 under `08` and verdicts on a formulation under `02`, and until this round they said neither. Every H3 row here now carries the formulation it was decided under.**

---

## The compiler's own problem statement

`02` opens by quoting Banwait–Huang against themselves:

> it is not immediately apparent how to algorithmically verify these conditions.

and then turns that into three levels: a hypothesis interface (Level 0), a
per-`(E,p)` certificate (Level 1), and prime-quantifier compression (Level 2).
RUN-043 placed this line at **C1 — hypothesis compiler**, which is this
document's rung. So running it is the direct test of that placement.

## Level 1, in the document's own keys

| `p` | reduction | H1 | H2 | H3 | `ℓ` | claim |
| ---: | --- | --- | --- | --- | ---: | --- |
| **3** | multiplicative | **UNKNOWN** | **FAIL** | PASS | 29 | `FW_NOT_APPLICABLE` |
| 5 | good ordinary | PASS | PASS | PASS | 29 | `FW_APPLICABLE` |
| **7** | good ordinary | PASS | **FAIL** | PASS | 29 | `FW_NOT_APPLICABLE` |
| 11–23 | ordinary / supersingular | PASS | PASS | PASS | 29 | `FW_APPLICABLE` |
| **29** | multiplicative | PASS | **FAIL** | **FAIL** | — | `FW_NOT_APPLICABLE` |
| … | | | | | | |
| **113** | good ordinary | PASS | **FAIL** | PASS | 29 | `FW_NOT_APPLICABLE` |
| 173–199 | good | **UNKNOWN** | PASS | PASS | 29 | `UNKNOWN` |

**34 applicable, 4 not applicable, 7 unknown.** Every deviation is a previous
round showing up where it should:

* `p = 3` — RUN-036 could not certify `ρ̄₃` surjective, and for two **structural**
  reasons rather than a short search: `PGL₂(F₃) ≅ S₄`, and the nonsplit-Cartan
  test is vacuous mod 3. So H1 is `UNKNOWN`, not `PASS`.
* `p = 7, 113` — RUN-038 measured `a₇ = 1` and `a₁₁₃ = 1`, so `a_p² ≡ 1 (mod p)`
  and `10`'s exact criterion fails H2.
* `p = 29` — H2 fails because 29 is multiplicative, and H3 fails because
  `W₋ = {29}` is a singleton and the `ℓ ≠ p` clause empties it. RUN-037's finding,
  arriving in the certificate.
* `p ≥ 173` — beyond the range RUN-036 certified, so H1 is `UNKNOWN`. A gate that
  extrapolated there would be committing `07`'s first forbidden upgrade.

## Level 2, and the output the document mandates

`02` §3 is explicit that scanning `p < 1000` and declaring victory is not the
goal, and equally explicit about what to emit if the compression is not obtained:

> 如果做不到，就只能輸出 `FW verified for tested primes`。不能升級 full BSD。

RUN-041 evaluated `04`'s criterion and found `P_loc` non-empty and not known
finite. So the compression is **not achieved**, and this gate emits exactly the
mandated string and nothing stronger.

## The three prohibitions

| | | |
| --- | --- | --- |
| **H1** | 不得自己用少量 Frobenius traces 猜 | **obeyed** — RUN-031 refuted all twelve of Mazur's degrees, which his theorem makes exhaustive, and RUN-036 refuted every maximal class with a **named** witness. Primes RUN-036 did not reach are `UNKNOWN`, not assumed |
| **H2** | 不得用 `a_p != something` 自行猜等價條件 | **obeyed** — the predicate is `10`'s, derived there from the ordinary semisimplification `ᾱ ⊕ χ_cyc ᾱ⁻¹` and compiled to `a_p² ≡ 1` *second*. Derived first, predicate second, in the order `02` demands |
| **H3** | 不能直接把 `p ∤ ord_ℓ(Δ)` 當完整 H3 | **the corpus disagrees with itself about this one** — `08` boxes the same criterion as an iff. Every H3 row here names its formulation; RUN-046 takes the disagreement up |

## The third prohibition, and what looking at it turned up

RUN-037 reported H3 as run, and RUN-039's table gave it `PASS` with source
*computed here*. `02` says plainly that Fouquet–Wan's exact local condition is
**finer** than the divisibility criterion, and that the criterion must not be
taken as the whole of H3 — so the label looked too wide, and this round set out
to narrow it.

It is not that simple. `08_FW_Weight2_Exact_Translation` boxes

```text
FW-H3(E, p)  <=>  exists ell || N :  E nonsplit multiplicative at ell
                                     ell != p
                                     p does not divide v_ell(Delta_min)
```

as an **iff**, under the title *exact translation*. **The corpus contradicts
itself about whether the criterion is complete H3**, and picking a side quietly
would have been worse than the original omission. RUN-046 is the round that takes
the disagreement up; this one records it and stops.

What is certain either way: those rounds computed the criterion **correctly**,
including the `ℓ ≠ p` clause `09`'s own boxed certificate drops — which is how
RUN-037 found the gap at `p = 29`. **No number moves.** What was missing was the
name of the formulation, and every H3 row in this gate now carries it, along with
a pointer to the condition `02` says is finer.

RUN-037 and RUN-039 carry scope notes pointing here and to RUN-046, in the
pattern RUN-017 and RUN-023 were given.

## The drill

**184 defects, 184 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 34 controls undisturbed, over 74 checks.

The 4 planted for this gate, each turning `fw-compiler` red and nothing else:

| planted defect | went red |
| --- | --- |
| Level 2 reports the quantifier compression achieved | `fw-compiler` |
| the H3 rows stop naming which formulation decided them | `fw-compiler` |
| H1 is reported PASS beyond the range RUN-036 certified | `fw-compiler` |
| the certificate emits keys the specification does not have | `fw-compiler` |


## What this round does not claim

* **`FW_APPLICABLE` is `02`'s enum value, not a proof.** It records that the
  three hypotheses, as this corpus compiles them, are satisfied at that prime.
  The theorem consuming them is external and the H3 row says which formulation
  it was decided under.
* **This round does not settle the `02` / `08` disagreement**, and does not take
  a side. It records that the two documents say different things about the same
  criterion, and leaves the arithmetic of it to RUN-046.
* **H1's `UNKNOWN` above 167 is a limit of RUN-036's range**, not evidence of
  failure. Irreducibility holds for every `p` by Mazur plus RUN-031; **absolute**
  irreducibility is certified only where the surjectivity witnesses reach.
* **H2 at the additive prime is `UNKNOWN`.** `05`'s no-go decides only the
  potentially multiplicative case and RUN-034 found it silent here, and silence
  is not a PASS.
* **Level 2 is not achieved**, and this round supplies no theorem toward it.
  What it supplies is the mandated output for that state.
* **The bound is 200**, chosen so every row can be traced to a named earlier
  round rather than to a fresh computation at scale.
