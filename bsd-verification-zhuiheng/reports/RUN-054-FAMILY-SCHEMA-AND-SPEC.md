# RUN-054 — A schema that refuses to be a theorem, a spec for the test nobody ran, and eleven prohibitions becoming fifteen

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`05_NonSemistable_Family_Theorem_Schema`](../../../amral/public/bsd/phase2/files/05_NonSemistable_Family_Theorem_Schema.md) and [`07_Local_Agent_Implementation_Spec`](../../../amral/public/bsd/phase2/files/07_Local_Agent_Implementation_Spec.md) — the last two Phase 2 documents that had never been a round's subject
**Tools:** [`src56_family_schema_and_spec.py`](../code/src56_family_schema_and_spec.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src56-family-schema-and-spec.json`](../data/gate-logs/src56-family-schema-and-spec.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `05` opens by refusing to be a theorem — 「本文件不是定理宣稱，而是列出完整 proof obligations」 — and lists five bridge hypotheses. **None is proved here; two the corpus marks open itself.** Its two self-declared dangers land exactly where this line independently stopped: **Gap A** (`∀p>2` not finite-ized) is RUN-041's `P_loc`, and **Gap B** (Manin-constant period splicing) *is* bridge hypothesis 4, which is RUN-039's open `c_E = 1`. That is agreement, not progress, and it is reported as agreement. Its hybrid strategy routes `p = 2` to Theorem 2.14 and **`p ∈ {3,5,7}` to Banwait, away from Fouquet–Wan** — and this line has, from the archived logs, **five independent structural reasons across four rounds** for `p = 3` being out of instrument reach, every one found without consulting this plan. `07` then specifies the very test RUN-052 called unreachable: a replayable JSON with `phi.kernel_linear_factor_Qp` and `dual_phi.kernel_linear_factor_Qp`, four backend rules, six fixtures, four forbidden inferences. **Of its 14 required keys this tree can fill 6; the verdict key `fw17_h2` is not one of them, and 0 of its 6 fixtures are runnable.** Its **fourth forbidden inference is `global irreducible → local irreducible`** — the exact substitution RUN-053 refused an hour earlier, reasoning from `00` §6 and before reading this document. And the prohibition count RUN-051 closed at eleven **becomes fifteen across four documents**, all clear.**

---

## `05` refuses to be a theorem, and that has to be respected

> 本文件不是定理宣稱，而是列出完整 proof obligations。

Scoring it as a theorem claim would be this arm inventing a claim the corpus
declined to make. So the gate scores the obligations.

| # | bridge hypothesis | state |
| --- | --- | --- |
| 1 | FW-H1/H2/H3 hold for the base `E` | **PARTIAL** — H3 computed, H1 bounded by RUN-036's range, H2 `UNKNOWN` |
| 2 | H1/H2 preserved under quadratic twist | **PARTIAL** — `03`'s Lemma B is a candidate by its own text (RUN-035) |
| 3 | `d`'s splitting conditions keep the H3 witness locally | **MEASURED HERE** — RUN-034, RUN-040, RUN-052: witness `ℓ = 29` at every member |
| 4 | FW period / Manin normalization compatible with Banwait's convention | **OPEN** — and it is Gap B |
| 5 | `L(E_d,1) ≠ 0` feeds the FW rank-zero corollary | **SUPPLIED** — RUN-016, RUN-039 |

The boxed conclusion `∀d ∈ 𝒟(E), BSD(E_d)` is **not reachable here**, and one of
the two obstacles is a lemma the corpus itself calls a candidate.

## The two gaps are where this line already stopped

| gap | `05`'s words | this line |
| --- | --- | --- |
| **A** | `∀p > 2` is not yet finite-ized | RUN-041 computed `P_red = ∅`, `P_ram = ∅`, `P_loc` non-empty and **not known finite** |
| **B** | the modular-form-period → Néron-period Manin constant at small `p` needs a clean join | RUN-039 left `c_E = 1` open; RUN-040 ran `01`'s weaker sufficient condition instead |

**Both still open, and the agreement is the point rather than a result.** A
schema naming its own two dangers, and an independent arm halting at the same
two places without having read it, is a consistency check on both — and nothing
more than that. Neither is closer to closed than it was.

## `p = 3`: five reasons, four rounds, and the corpus routing around it

`05`'s hybrid sends `p ∈ {3,5,7}` to Banwait's existing small-prime theorems,
**not** to Fouquet–Wan. Independently, from the gate logs:

| round | reason |
| --- | --- |
| **RUN-034** | `05_Kodaira` gives `p = 3` its own character-structure section |
| **RUN-036** | the nonsplit-Cartan test is **vacuous mod 3** — no witness exists to record |
| **RUN-036** | `PGL₂(F₃) ≅ S₄`, so the projective `A₄`/`S₄`/`A₅` tests cannot separate at 3 |
| **RUN-046** | `χ_cyc²` is trivial on inertia at 3, so `10`'s single congruence is not the whole criterion — `(p−1) ∣ 2` |
| **RUN-053** | `ω² = 1` at 3, so `04`'s two kernel tests can **both** fire — the only odd prime where they are not mutually exclusive |

Read from the archived logs by field, not from the reports' prose — the count is
computed so that "the fifth time" is never typed from memory.

**These are reasons the *instruments* fail at 3**, not a claim that BSD is harder
there. What is worth noting is that the corpus's own plan routes around exactly
the prime its own machinery cannot reach, and `07`'s **Fixture A is `p = 3`
reducible**.

## `07` specifies the test, and this tree can fill less than half of it

`07` demands a replayable record: 輸出必須可 replay，不可只回 boolean.

| | |
| --- | --- |
| required keys | **14** |
| fillable in this tree | **6** — `curve`, `p`, `profile`, `potential_reduction`, `potentially_multiplicative`, `evidence` |
| not fillable | **8** — `local_reducibility_Fp`, both `phi` blocks, both `dual_phi` blocks, `global_abs_irreducible`, and **`fw17_h2` itself** |
| fixtures runnable | **0 of 6** |

`global_abs_irreducible` is worth its own line: RUN-036 certifies **surjective**
at 38 primes and **irreducible** at Mazur's degrees, and absolute irreducibility
beyond that range is `UNKNOWN`. The spec wants a `PASS`; this arm has a range.

**The keys this tree cannot fill are exactly the kernel-polynomial ones RUN-052
named.** The shape of the gap is identical measured from either end — which is
the useful part, because it means the two rounds are describing one gap, not two.

Zero of six fixtures is the honest number. Every fixture needs local reducibility
or a kernel polynomial, and a gate that scored higher would be counting fixtures
it can *restate* rather than run.

## `07`'s four backend rules, and one this line already learned the hard way

| # | rule | this arm |
| --- | --- | --- |
| 1 | prefer certified local machinery; **do not decide a `Q_p` root by floating-point approximation** | **RUN-006 was bitten by exactly this**, on `ψ₃` |
| 2 | "a local `p`-isogeny exists", without kernel-character evidence, is not an H2 verdict | this arm emits no H2 verdict at the additive prime at all |
| 3 | the linear factor must be an exact `p`-adic factorization / Hensel certificate | not attempted |
| 4 | a heuristic local-irreducibility certificate must emit `UNKNOWN`, never `PASS` | the same rule this line states as *`unmeasured` is a real verdict* |

Rule 1 is not an abstraction here. RUN-006 scanned `ψ₃` for real roots with
**floating-point evaluation** and got a confidently wrong answer on the one hard
curve — an answer that *would have been reported as a finding against the
package*. Same class of object, different field. `07` forbids in `Q_p` the
method that already failed this line in `ℝ`.

## The fourth forbidden inference

`07` closes with four shortcuts it calls 禁止:

| forbidden | guard |
| --- | --- |
| Kodaira type alone → `PASS` | RUN-034 found `05`'s no-go **silent** in the potentially-good case and did not upgrade |
| no `Q_p`-rational `p`-torsion → `PASS` | no log in this tree emits a `PASS` from a torsion absence |
| potentially supersingular → `PASS` | RUN-039 kept the branch's quantifier ranges and emitted no H2 `PASS` |
| **global irreducible → local irreducible** | **RUN-053 refused it explicitly, before reading this document** |

The fourth is the one worth stopping on. RUN-053 wrote a field —
`global_surjectivity_does_not_settle_this` — reasoning from `00` §6's third
prohibition one level down. `07` names the same substitution outright.

**Two independent routes to the same rule.** That is not a result about BSD; it
is evidence that the rule is the natural one to reach from either side, which is
worth more than either statement alone.

## Eleven becomes fifteen

| document | prohibitions | audited in |
| --- | ---: | --- |
| `05_Kodaira_Prefilters_and_NoGo` | 3 | RUN-034 |
| `07_Stop_Rules_and_Claim_Ladder` | 5 | RUN-043 |
| `00_Phase2_Global_Enclosure_Consensus` | 3 | RUN-051 |
| **`07_Local_Agent_Implementation_Spec`** | **4** | **this round** |
| | **15** | **all clear** |

Note the numbering: the new list is in a document numbered `07` that is **not**
the `07` RUN-051 counted. `07_Stop_Rules_and_Claim_Ladder` and
`07_Local_Agent_Implementation_Spec` are different documents in different
sub-lines, and a count that merged them by number would have lost four
prohibitions.

**Four documents, written at different times, each forbidding a different way of
overclaiming, and none forbidding the same one twice.**

## The drill

**223 defects, 223 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 43 controls undisturbed, over 82 checks.

The 6 planted for this gate, each turning `family-schema-and-spec` red and nothing else:

| planted defect | went red |
| --- | --- |
| 05's five bridge hypotheses are scored as all proved | `family-schema-and-spec` |
| 05's Gap A is reported closed | `family-schema-and-spec` |
| the p = 3 reasons come back empty, so the count would be typed from prose | `family-schema-and-spec` |
| 07's verdict key fw17_h2 is reported fillable in this tree | `family-schema-and-spec` |
| the prohibition count merges the two documents numbered 07, losing four | `family-schema-and-spec` |
| 07's six regression fixtures are scored runnable here | `family-schema-and-spec` |


## What this round does not claim

* **`05` is not scored as a theorem**, because it declines to be one. What is
  scored is the state of its obligations.
* **Gap A and Gap B are not closer to closed.** Two independent parties naming
  the same gap is a consistency check, not progress on it.
* **The `p = 3` reasons are about instruments.** Five ways this line's machinery
  cannot reach 3 is not a statement about the difficulty of BSD at 3.
* **The schema-coverage count is a reading of `07`'s example JSON**, which is an
  illustration rather than a formal schema; a different segmentation of the
  nested keys would move 14 and 6 together.
* **Zero of six fixtures runnable is a limit of this tree**, not a criticism of
  the fixtures — they are well chosen, and Fixture A picks the exact prime five
  other rounds independently found exceptional.
* **The convergence on the fourth forbidden inference is real but small.** Both
  statements are refusals; neither computes anything.
