# RUN-046 — The H2 chain is consistent, and the corpus disagrees with itself about H3

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`03_FW_H2_Jordan_Holder_Lemma`](../../../amral/public/bsd/phase2/files/03_FW_H2_Jordan_Holder_Lemma.md) and [`08_FW_Weight2_Exact_Translation`](../../../amral/public/bsd/phase2/files/08_FW_Weight2_Exact_Translation.md), against [`10`](../../../amral/public/bsd/phase2/files/10_FW_H2_and_Ordinary_Obstruction.md) and [`02`](../../../amral/public/bsd/phase2/files/02_Fouquet_Wan_Hypothesis_Compiler.md)
**Tools:** [`src48_h2_chain_and_h3_dispute.py`](../code/src48_h2_chain_and_h3_dispute.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src48-h2-chain.json`](../data/gate-logs/src48-h2-chain.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the corpus's three statements of FW-H2 are one statement. `08`'s representation-level ratio test — `H2 FAIL ⟺ αβ⁻¹ ∈ {χ_cyc, χ_cyc⁻¹}` — and `03`'s Jordan–Hölder lemma — `⟺ λ² = 1 or μ² = 1` — are verified **equivalent over 22,140 character pairs with 0 mismatches**, exhausting every cyclic character group of order up to 40 and every value of `ω`. And `10`'s ordinary congruence `a_p² ≡ 1 (mod p)` names only **one** of `03`'s two cases; the other needs `χ_cyc²` unramified, and the mod-`p` cyclotomic character has order `p − 1` on inertia, so that happens exactly when `p − 1 ∣ 2` — at `p = 2` and `p = 3` only. **So `10`'s single congruence is the whole criterion at every good ordinary `p ≥ 5`, and is not at `p = 3`** — the same prime `05` gives its own section and the same prime RUN-036 could not certify. **The H3 news is worse and is reported rather than resolved: `02` states that the divisibility criterion must not be equated with H3, while `08` boxes exactly that criterion as an **iff** under the title *exact translation*, and `09` states the same three conditions as the definition. Two of three treat it as H3 and one forbids it.** No computed value changes under either reading — the verdicts, the witness `ℓ = 29`, and RUN-037's failure at `p = 29` are identical. What changes is what those verdicts are verdicts *about*.**

---

## Three statements of one hypothesis

| document | level | statement |
| --- | --- | --- |
| `08` | representation | `H2 FAIL ⟺ αβ⁻¹ ∈ {χ_cyc, χ_cyc⁻¹}` for `V^ss = α ⊕ β` |
| `03` | Jordan–Hölder | `H2 FAIL ⟺ λ² = 1 or μ² = 1` — a JH character is quadratic or trivial |
| `10` | ordinary case | `H2 FAIL ⟺ a_p(E)² ≡ 1 (mod p)` |

All three take the same input from the Weil pairing: `det E[p] = χ_cyc`, hence
`λμ = ω`. That relation is cited by both documents and proved by neither, and
not by this round either.

## `03` and `08` are the same statement, exhausted

Written additively in a cyclic character group, `λμ = ω` is `l + u ≡ w`,
`λ² = 1` is `2l ≡ 0`, and `αβ⁻¹ ∈ {ω, ω⁻¹}` is `l − u ≡ ±w`. Every order from 1
to 40, every `ω`, every admissible pair:

| | |
| --- | --- |
| pairs checked | **22,140** |
| mismatches | **0** |
| equivalent | **yes** |

Exhausting the finite case is a check. Restating the derivation would not have
been — and the derivation is short enough that restating it is the tempting
thing to do.

## `10` names one case of two, and that is complete only above 3

`03` allows **either** constituent to be the quadratic one. `10` writes the
ordinary semisimplification as `ᾱ ⊕ χ_cyc ᾱ⁻¹` with `ᾱ` **unramified**, and names
the failure `ᾱ² = 1`. The other case is `(χ_cyc ᾱ⁻¹)² = 1`, which forces
`χ_cyc² = ᾱ²` — and `ᾱ` is unramified, so it forces `χ_cyc²` to be unramified
too.

The mod-`p` cyclotomic character has order `p − 1` on inertia. So `χ_cyc²` is
trivial there exactly when `p − 1` divides 2:

| `p` | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| order on inertia | 1 | 2 | 4 | 6 | 10 | 12 | 16 | 18 | 22 |
| second case possible | ✔ | ✔ | — | — | — | — | — | — | — |

**`10`'s single congruence is the whole of H2 failure at every good ordinary
`p ≥ 5`.** At `p = 3` it is not — which is the third time this session `p = 3`
has come out special for a structural reason: `05` gives it its own section
because `F₃ˣ = {±1}`, RUN-036 could not certify `ρ̄₃` because `PGL₂(F₃) ≅ S₄` and
the nonsplit-Cartan test is vacuous mod 3, and here `χ_cyc²` is trivial on
inertia. Three different arguments, one prime.

## The chain, and its weakest link

| | status |
| --- | --- |
| `08` (representation) → `03` (Jordan–Hölder) | **verified here** — exhausted |
| `03` → `10` (ordinary) | **verified here, with its range** — complete for `p ≥ 5` |
| `10` → RUN-038's predicate | the corpus's own derivation, **cited** |
| Fouquet–Wan Theorem 1.7 → `08` | **cited** |

Two links verified, two cited, and the weakest is the theorem itself, which no
round of this arm proves and none pretends to.

## The corpus disagrees with itself about H3

`02_Fouquet_Wan_Hypothesis_Compiler`, on the divisibility criterion:

> 但 Fouquet–Wan 的 exact local condition 更細，**不能直接把這一條當完整 H3**。

`08_FW_Weight2_Exact_Translation`, boxing exactly that criterion:

```text
FW-H3(E, p)  <=>  exists ell || N :  E nonsplit multiplicative at ell
                                     ell != p
                                     p does not divide v_ell(Delta_min)
```

under the title **Exact Translation**. And `09_FW_H3_Exact_Compiler` states the
same three conditions again, as the definition it compiles.

**Two of three treat the criterion as H3; one forbids it.** The gate confirms all
three lines are present in the files and that `08`'s and `09`'s conditions are
identical.

### What turns on it

| | |
| --- | --- |
| under `08` | RUN-037's and RUN-039's H3 verdicts are verdicts on **H3**, and RUN-037's gap at `p = 29` is a gap in FW-H3 for this curve |
| under `02` | they are verdicts on a **compilation**, and the exact condition is unexamined at every prime |
| **either way** | **no computed value changes** — the verdicts, the witness `ℓ = 29`, and the failure at `p = 29` are the same |

### Why this round does not resolve it

Resolving it means reading Fouquet–Wan Theorem 1.7's exact local condition, which
is an external theorem this arm does not hold. RUN-043 placed this line at C1 —
hypothesis compiler — and settling which compilation is right is above that rung.
**Naming the disagreement is what an independent arm can do here; settling it is
not**, and a round that quietly picked the reading that made its own earlier
verdicts look stronger would have been doing the opposite of this arm's job.

## And the drill was counting a crash as a catch

Wiring this round's gates in turned up a collision in the drill's own helper
namespace, and then two more. `_true_squarefree` had been bound twice — to
`src21`'s `squarefree_part`, which returns an integer, and to `src44`'s
`squarefree`, which returns a pair. The later binding won, so the defect
*squarefree part drops the sign* evaluated `abs(...)` on a tuple and raised a
`TypeError`. The named check went red, the drill counted it caught, and **a
defect that produces a traceback is not a defect a check caught** — RUN-020,
RUN-030 and RUN-035 each recorded that, and this is the first time it happened
inside the instrument rather than inside a gate.

`_true_point_count` had been bound twice as well, to two independently written
point counters. Those **agree on every case tested**, so the defect using it
computed the right number through the wrong module — benign in effect, wrong in
provenance, and exactly the kind of thing that stays invisible until it does not.

The collision that surfaced all three was mine: `_true_h3` bound to `src39`'s
two-argument `h3` and to `src47`'s, in that order in the file and the opposite
order in my head.

**The repair is structural, not three renames.** The drill now reads its own
source before running and refuses to start if any `_true_*` name is assigned
twice:

```text
81 _true_* helpers, none shadowed
```

The three names are also fixed, and the two affected defects now go red for the
reasons they are named for. RUN-043 and RUN-044 cite the run that contained the
crash-catch and carry correction notes saying so; every other figure in those
rounds stands.

## The drill

**184 defects, 184 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 34 controls undisturbed, over 74 checks.

The 4 planted for this gate, each turning `h2-chain` red and nothing else:

| planted defect | went red |
| --- | --- |
| the 03-08 equivalence is asserted without exhausting anything | `h2-chain` |
| 10's congruence is called complete at p = 3 as well | `h2-chain` |
| the H3 disagreement is reported resolved | `h2-chain` |
| 02's cautionary line is reported absent, so there is no disagreement | `h2-chain` |


## What this round does not claim

* **The disagreement is not resolved**, and neither document is called wrong.
  Both are quoted and the consequence of each is computed.
* **The Weil-pairing relation `λμ = ω` is cited**, from `det E[p] = χ_cyc`. The
  equivalence verified here is conditional on it.
* **The exhaustion is over cyclic character groups to order 40.** The statement
  is about characters into `F_p^×`, which is cyclic, so the model is faithful —
  but the bound is a bound and is stated as one.
* **The inertia order of `χ_cyc` is `p − 1`** — standard, cited, not derived
  here. What is computed is which primes satisfy `p − 1 ∣ 2`.
* **`10`'s completeness above 5 is about `10`'s criterion**, not about H2 being
  decided: `03` and `08` still rest on the local representation, which this tree
  does not compute.
