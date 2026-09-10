# RUN-048 — The schema, the sieve, and the control curve that was supposed to fail

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`13_Candidate_NonSemistable_Strong_BSD_Family`](../../../amral/public/bsd/phase2/files/13_Candidate_NonSemistable_Strong_BSD_Family.md) and [`14_Candidate_Sieve`](../../../amral/public/bsd/phase2/files/14_Candidate_Sieve.md) — a schema with six obligations, and the sieve that produced the anchor **with a control that fails**
**Tools:** [`src50_candidate_schema_and_sieve.py`](../code/src50_candidate_schema_and_sieve.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src50-candidate-schema.json`](../data/gate-logs/src50-candidate-schema.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `14`'s odd local table for the anchor recomputes exactly — `2` additive `II*` with `v_Δ = 11`, `3` split multiplicative `I₁` with `v_Δ = 1`, `29` **nonsplit** multiplicative `I₁` with `v_Δ = 1`, giving `W_mult^odd = {3, 29}` and `W₋ = {29}` — and its boxed criterion holds. **The control is the point of this round, and the control was run.** `14` eliminates a conductor-116 curve as `FAIL_FIXED_MULTIPLICATIVE_WITNESS`; the gate **found a curve of conductor 116 by search rather than quoting a label** — one model in 7,479 scanned, `[0, 1, 0, −4, 4]` — and confirmed the failure for the stated reason: `2` additive `IV*`, `29` nonsplit multiplicative, so `W_mult^odd = {29}` is a **single** reservoir and the leave-one-out at `p = 29` has **no distinct candidate at all**. It has a nonsplit prime and still fails, which is exactly `14`'s point: the criterion is not "has a nonsplit prime" but **至少兩個 odd multiplicative reservoirs,其中至少一個 nonsplit**. And `13`'s **B1 and B2 are RUN-033's lemma 1 and RUN-037's premise under other names** — both computed here before this document was read. Of `13`'s six obligations: **1 cited, 3 partly, 2 open, none closed**, and `13`'s own rule — 六項完成前,不升級為 theorem — keeps the label where `20` and `27` put it.**

---

## `14`'s table, recomputed

| `p` | reduction | Kodaira | `v_p(Δ)` | |
| ---: | --- | --- | ---: | --- |
| 2 | additive | `II*` | 11 | |
| 3 | multiplicative | `I₁` | 1 | **split** |
| 29 | multiplicative | `I₁` | 1 | **nonsplit** |

`W_mult^odd = {3, 29}`, `W₋ = {29}`, `g_mult^odd = 1`, `g₋ = 1` — both powers of
two, which is `13`'s B1 and B2. RUN-033 computed the same table from the
discriminant without reading either document; RUN-042 compared it against `15`'s
certificate. This is the third independent arrival at the same three rows.

## The control, found rather than quoted

`14` names its control by LMFDB label. **A label is a name, not arithmetic**, and
RUN-030 caught this arm quoting three numbers from memory. So the gate searched
an a-invariant box for curves of conductor 116 and found exactly one:

```text
[0, 1, 0, -4, 4]      2  additive        IV*   vΔ = 8
                     29  multiplicative  I1    vΔ = 1   nonsplit
```

which is the local structure `14` states for its control. Whether this is the
curve LMFDB labels `116.b1` is a question about labels and is not settled here —
what is settled is that a curve of that conductor with that structure exists and
behaves as `14` says.

## It has a nonsplit prime and still fails

| | 696.e1 | the control |
| --- | --- | --- |
| `W_mult^odd` | `{3, 29}` | `{29}` |
| `W₋` | `{29}` | `{29}` |
| at least one nonsplit | ✔ | **✔** |
| at least two reservoirs | ✔ | **✘** |
| leave-one-out at each fixed multiplicative `p` | `3 → 29`, `29 → 3` | `29 → ` **nothing** |
| boxed criterion | **met** | **not met** |

The control passes the test people would think of first — it *has* a nonsplit
multiplicative prime — and fails the one that matters. That is `14`'s boxed
conclusion:

> 至少兩個 odd multiplicative reservoirs，其中至少一個 nonsplit。

and it is why RUN-033's *one witness, no spare* mattered. The anchor has two
reservoirs and one of them is nonsplit; the control has one reservoir that
happens to be nonsplit, and one reservoir cannot supply a **distinct** witness to
itself. RUN-033's lemma 2 is the same statement, and the control is the first
curve in this tree where it returns nothing.

**A criterion whose failing side is never exhibited has not been tested.** `14`
supplied the failing side; this round ran it.

## `13`'s schema

| | | |
| --- | --- | --- |
| **B0** | 2-part anchor, and 建議 `c_E = 1` | **partly** — `v₂(L^alg) = 0`, trivial torsion, `Δ < 0` computed (RUN-014/030); `BSD(E,2)` cited; `c_E = 1` is RUN-039's open item |
| **B1** | `W_mult^odd ≠ ∅`, `g_mult^odd` a power of two | **computed** — RUN-033's lemma 1 |
| **B2** | `W₋ ≠ ∅`, `g₋` a power of two | **computed** — RUN-037's premise |
| **B3** | fixed additive odd primes: exact H1, H2, period/Manin | **open** — RUN-045 marks H2 `UNKNOWN` there |
| **B4** | fixed multiplicative: per-prime check + distinct ramified witness | **computed** — RUN-033's leave-one-out |
| **B5** | twist support restrictions | **computed** — RUN-032's five conditions, RUN-036's images |

B1 and B2 are worth naming twice: this tree computed both **before** reading
`13`, from `00_GCD_Witness_Lemmas` and `09_FW_H3_Exact_Compiler`. The schema and
the lemmas were written by different hands and ask for the same two gcds.

## The six obligations, scored

| | status | where |
| --- | --- | --- |
| fixed additive primes' exact H1 backend | **partly** | RUN-036 certifies surjectivity at 38 primes; `p = 2` is not among them |
| fixed additive primes' exact H2 local residual backend | **open** | RUN-034 found `05`'s no-go silent there; silence is not a PASS |
| fixed multiplicative branch formal theorem table | **cited** | `27`'s router names Skinner Theorem C |
| Manin-period compatibility | **open** | RUN-039's `c_E = 1`; RUN-040 checked the weaker `p ∤ c` |
| all support restrictions' Chebotarev / CRT simultaneous compatibility | **partly** | RUN-044 computed the Chebotarev half |
| final all-prime cover proof | **partly** | RUN-047 ran `27`'s router as a partition; the branch theorems are cited |

**1 cited, 3 partly, 2 open — none closed.** `13`'s own rule is 六項完成前,
不升級為 theorem, and this arm's scoring keeps the label exactly where `20` and
`27` put it. That agreement is the finding: the schema's stopping rule and the
referee's label were set independently and point at the same rung.

## The drill

**192 defects, 192 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 37 controls undisturbed, over 76 checks.

The 4 planted for this gate, each turning `candidate-schema` red and nothing else:

| planted defect | went red |
| --- | --- |
| the control curve cannot be found, so the failing side is never shown | `candidate-schema` |
| the sieve criterion drops the two-reservoir clause | `candidate-schema` |
| additive primes are counted as multiplicative reservoirs | `candidate-schema` |
| one of 13's six obligations is reported closed | `candidate-schema` |


## What this round does not claim

* **The control's identity is not established.** A curve of conductor 116 with
  the stated local structure was found; whether it carries the label `116.b1` is
  a question about a database, not about arithmetic, and this arm does not
  answer it.
* **The search box is a box.** Exactly one conductor-116 model was found in it;
  that is not a claim that the isogeny class has one curve.
* **"Partly" is not "nearly".** Three obligations are scored partly because a
  piece of each was computed; none is close to closed, and the two open ones are
  open at the same place they were at RUN-039.
* **`13` is a schema, not a theorem**, and says so in its first line. Scoring its
  obligations measures distance, not progress toward a proof.
* **B0's `BSD(E,2)` and the Manin constant stay cited**, as they have since
  RUN-030's certificate.
