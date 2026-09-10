# RUN-049 — The corpus's own source audits, and two of this arm's conclusions that move

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`22_Odd_Prime_Source_Audit`](../../../amral/public/bsd/phase2/files/22_Odd_Prime_Source_Audit.md) and [`23_FW_Supersingular_Source_Audit`](../../../amral/public/bsd/phase2/files/23_FW_Supersingular_Source_Audit.md) — the two places where the corpus checks its own citation chain
**Tools:** [`src51_source_audits.py`](../code/src51_source_audits.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src51-source-audits.json`](../data/gate-logs/src51-source-audits.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: **two conclusions of this arm move, and both move because the corpus had a document this arm had not read.** RUN-046 reported the `02`/`08` seam — whether the divisibility criterion *is* FW-H3 — as unresolvable here, since "resolving it means reading Fouquet–Wan Theorem 1.7's exact local condition, an external theorem this arm does not hold". **`23` quotes that condition**: Assumption 3 as special Steinberg, a twist by an unramified character sending `ℓ` to `(−1)ℓ^{k/2−1}`, and residual ramification. At weight 2 that exponent is 0 and the value is `−1`, so `a_ℓ = −1` — **nonsplit multiplicative**. The gate checks the arithmetic endpoint: `a₂₉ = −1` and 29 is nonsplit, `a₃ = +1` and 3 is split. The derivation `02` asked for is in the corpus, in a document neither `02` nor `08` references. And RUN-047 scored `18`'s first referee item — the exact convention match — as **OPEN** because `27` does not address it; `23`'s H3 section **is** that convention match, and it opens by refusing to guess the normalisation. Corrected: **2 addressed, 1 deferred, 2 open**. Separately, **`22` invokes a stronger premise than its theorem asks for**: its *Important simplification* rests on 「base curve mod-ℓ image 對所有 ℓ maximal」 while Skinner Theorem C lists only that `E_q[p]` be irreducible — and maximality is the one statement RUN-036 could not certify at `ℓ = 3`, which is `22`'s case C. Irreducibility, the weaker premise the theorem actually names, is certified there.**

---

## What `22` and `23` are

They are the only two documents in the corpus that take a cited theorem, list its
hypotheses, and check them one by one for 696.e1. Every hypothesis in them is
either arithmetic this tree has computed or a citation, and separating the two is
the whole job.

| `22`'s case | theorem | hypotheses computed here |
| --- | --- | ---: |
| A — `p = q`, additive twist | BSTW 9.21(c) via BH 2.9 | 5 of 5 |
| B — good ordinary `p` | Skinner Theorem C | 4 of 5 |
| C — multiplicative `p = 3` | Skinner Theorem C | 1 of 2 |
| D — multiplicative `p = 29` | Skinner Theorem C | 2 of 2 |

The uncomputed ones are honest citations: that `L(E_q,1) ≠ 0` in general is
Theorem 2.14's (RUN-015/016 computed it for the members it reached), and that
Skinner C states `p ≥ 3` is a reading of a theorem statement.

## `23` quotes the condition RUN-046 said this arm did not hold

RUN-046 found `02` forbidding the identification of the divisibility criterion
with H3, `08` boxing it as an *iff*, and `09` defining it — and concluded the
disagreement could not be resolved here.

`23` opens its H3 section with **不用自行猜 representation normalization** and
then gives FW's Assumption 3 as three conditions:

* the local automorphic representation is special Steinberg;
* twisted by an unramified character taking `ℓ` to `(−1)ℓ^{k/2−1}`;
* the residual representation is ramified.

At weight 2 the exponent is `k/2 − 1 = 0`, so the value is `−1`, so `a_ℓ = −1`,
which for an elliptic newform is **nonsplit multiplicative**. Checked here:

| | | |
| --- | ---: | --- |
| `a₂₉` | **−1** | 29 nonsplit ✔ |
| `a₃` | **+1** | 3 split ✔ |

The sign is doing real work: it selects the nonsplit prime and excludes the split
one. Together with `v₂₉(Δ) = 1` — so every odd `p ≠ 29` keeps the residual
representation ramified — that is exactly `08`'s and `09`'s three conditions,
**derived** rather than asserted.

**So the corpus is not silent about the convention.** The disagreement between
`02` and `08` *as written* stands: `02` says the criterion must not be equated
with H3 and `08` equates them without pointing at a derivation. What is new is
that the derivation exists, in `23`, which neither document references — and that
RUN-046 reported an unresolvable seam while holding three of the four relevant
documents.

Still cited: **whether FW's Assumption 3 is that triple** is `23`'s reading of
the paper. This round checks its weight-2 arithmetic, not its reading.

## And RUN-047's scoring was wrong on one item

RUN-047 read `18`'s five referee items against `27` and scored the first — *exact
convention match between FW's modular representation and elliptic `E[p]` at the
nonsplit multiplicative witness* — as **OPEN**.

`23`'s H3 section is that convention match. The item is **addressed**.

| | RUN-047 | corrected |
| --- | ---: | ---: |
| addressed | 1 | **2** |
| deferred | 1 | 1 |
| open | 3 | **2** |

The scoring was right about `27` and wrong about the corpus. RUN-047 carries a
correction note, and so does RUN-046.

**Neither correction is an arithmetic error.** Both are this arm scoring a corpus
it had not finished reading — which is a different failure from the ones this
line has been recording, and worth naming as its own kind.

## `22` asks for more than its theorem does

`22`'s closing *Important simplification* reads:

> 由於 base curve mod-`ℓ` image 對所有 `ℓ` maximal，quadratic twist 只 tensor
> 一個 scalar character，故 irreducibility 保持。

Skinner Theorem C, as `22` itself lists it two sections earlier, asks for
`E_q[p]` **irreducible**. Maximality is strictly stronger, and this tree's
position on the two is not the same:

| | this arm |
| --- | --- |
| **irreducible** at every Mazur degree | **certified** — RUN-031's twelve refutations, exhaustive by Mazur's theorem |
| **maximal** | certified at `ℓ = 2` and every prime `5 ≤ ℓ ≤ 167` — **38 primes** — and **not at `ℓ = 3`** |

And `22`'s case C is `p = 3`.

At 3, RUN-036 refuted the Borel — so irreducibility holds — but could not refute
`S₄`, which is the whole projective group there, nor the nonsplit Cartan, whose
test is vacuous mod 3. Both obstructions are structural.

**Nothing is wrong with `22`'s conclusion.** The premise it states is stronger
than the one its theorem needs, and the stronger one is unavailable at exactly
the prime the case is about. Saying so is the point of an audit of an audit.

## The drill

**200 defects, 200 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 39 controls undisturbed, over 78 checks.

The 4 planted for this gate, each turning `source-audits` red and nothing else:

| planted defect | went red |
| --- | --- |
| a_29 comes back +1, so 23's weight-2 sign stops selecting the nonsplit prime | `source-audits` |
| maximality is reported certified at 3, where RUN-036 could not | `source-audits` |
| 22's cited hypotheses are scored as computed | `source-audits` |
| 23's quoted condition is reported absent, so nothing moves | `source-audits` |


## What this round does not claim

* **`23`'s reading of Fouquet–Wan is not verified.** That Assumption 3 is that
  triple is a claim about a paper this tree does not hold. What is checked is
  the weight-2 arithmetic it produces.
* **The `02`/`08` disagreement is not erased.** Two documents still say
  incompatible things about the same criterion; a third supplies the derivation
  one of them wanted. A reader of `02` and `08` alone is still stuck.
* **Skinner Theorem C, BSTW 9.21(c) and Banwait–Huang 2.9/2.10 are cited.** What
  is checked is that their listed hypotheses hold for this curve where this tree
  can compute them.
* **`22`'s conclusion is not challenged**, only its stated reason. Irreducibility
  suffices and is certified; the audit could have said so.
* **Case B's `L(E_q,1) ≠ 0` is cited in general.** RUN-015 and RUN-016 computed
  it for the members they reached, not for the whole family.
