# RUN-039 — The derived supersingular bridge, assembled, and the quantifier that saves it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`11_Derived_Supersingular_FW_Bridge`](../../../amral/public/bsd/phase2/files/11_Derived_Supersingular_FW_Bridge.md) — a derived proposition the corpus assembles from external theorems, and says so in its first line
**Tools:** [`src41_derived_supersingular_bridge.py`](../code/src41_derived_supersingular_bridge.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src41-derived-bridge.json`](../data/gate-logs/src41-derived-bridge.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the derived proposition's hypotheses hold for 696.e1 and its residual conditions hold at every good supersingular prime below 6,000 — all six of `23, 251, 1061, 2297, 5479, 5591`, with H3 **computed** (witness `ℓ = 29`) and H1, H2 **cited** from `10`'s niveau-2 argument. `L(E,1) = 1.6317…` is recomputed and non-zero, so the rank-zero `p`-part corollary's analytic input is in place. And the round settles something RUN-037 raised: `11`'s uniform form uses the **same** gcd argument as `09`'s, and `09`'s is false at `p = 29` while `11`'s is not. The only difference is the range of the quantifier — `09` says "for all `p > 2`", `11` says "all good supersingular odd primes" — and `W₋` consists of primes of **bad** reduction while the supersingular branch consists of primes of **good** reduction, so the failing prime is outside `11`'s claim by construction. The disjointness is computed, not observed. **What stays open is named: `c_E = 1`, the safe period condition `11` itself proposes, which this arm does not compute.**

---

## The document says what it is

`11` opens with its own status line, and it is the right one:

> **狀態：** 由現有外部定理拼接出的 derived proposition；不是原論文命名定理。

A proposition spliced from existing external theorems, not a named theorem from
a paper. So the honest thing to check is the splice — which hypotheses this tree
can compute, which it must cite, and whether the assembly holds together.

## The hypotheses, computed

`11` asks for an `ℓ ‖ N_E` with `E` nonsplit multiplicative at `ℓ` and
`p ∤ v_ℓ(Δ_min)`. Both are RUN-033's and RUN-037's measurements:

| | |
| --- | --- |
| `W₋(696.e1)` | `{29}` |
| `v₂₉(Δ_min)` | 1 |
| hypothesis 1 (an `ℓ` exists) | **holds** |
| `g₋ = 1 = 2⁰` | a power of two, so the uniform form's premise holds |

## Six primes, three hypotheses, two sources

| `p` | `a_p` | H1 | H2 | H3 | witness |
| ---: | ---: | --- | --- | --- | --- |
| 23 | 0 | PASS *(cited)* | PASS *(cited)* | **PASS** | `ℓ = 29` |
| 251 | 0 | PASS *(cited)* | PASS *(cited)* | **PASS** | `ℓ = 29` |
| 1061 | 0 | PASS *(cited)* | PASS *(cited)* | **PASS** | `ℓ = 29` |
| 2297 | 0 | PASS *(cited)* | PASS *(cited)* | **PASS** | `ℓ = 29` |
| 5479 | 0 | PASS *(cited)* | PASS *(cited)* | **PASS** | `ℓ = 29` |
| 5591 | 0 | PASS *(cited)* | PASS *(cited)* | **PASS** | `ℓ = 29` |

H1 and H2 come free from `10`'s niveau-2 argument, which RUN-038 recorded as
cited; H3 is this tree's computation. The table separates them per row rather
than in a footnote, because a bridge whose supports are of two different kinds
should not report a single verdict.

## The same gcd, one quantifier apart

RUN-037 found `09_FW_H3_Exact_Compiler`'s boxed line — `∀p>2, FW-H3 = PASS` —
**false at `p = 29`**, because `W₋ = {29}` is a singleton and the `ℓ ≠ p` clause
empties it. `11`'s uniform form rests on the identical premise, `g₋(E) = 2^a`,
and concludes for **all good supersingular odd primes**.

That range cannot contain the failure:

* `W₋` is defined by `ℓ ‖ N_E`, so every member is a prime of **bad** reduction;
* the supersingular branch is, by definition, primes of **good** reduction;
* measured: `W₋ ∩ {supersingular below 6,000} = ∅`, and every prime in `09`'s
  failing set lies outside `11`'s range.

So `11` is true where `09` is false, and the difference is neither the curve nor
the argument — it is where the quantifier is allowed to point. This is the sort
of thing a certificate that is only ever restated cannot show, and it is the
reason RUN-037 tested the conclusion instead of re-deriving it.

## The analytic input

`L(E,1) = 1.631727740072` at 20,000 terms, non-zero, analytic rank 0 —
recomputed here rather than carried from RUN-014. `11` attaches its own caveat
to the corollary in the same sentence, and it is quoted verbatim in the log:

> 惟 period normalization / Manin constant 需另外閉合。

## What stays open, named rather than skipped

`11` proposes its own safe condition — **`c_E = 1`** — precisely to avoid
splicing the modular and Néron periods. This tree computes the real period by
AGM (RUN-014, repaired in RUN-017, confirmed against direct integration) and
**does not compute the Manin constant anywhere**. RUN-030's certificate lists it
among what stays cited, and it stays cited here.

It is the one hypothesis of this derived proposition that this arm cannot close,
and the gate's own log says so in a field rather than in prose.

## The drill

**160 defects, 160 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 28 controls undisturbed, over 68 checks.

The 4 planted for this gate, each turning `derived-bridge` red and nothing else:

| planted defect | went red |
| --- | --- |
| H1 and H2 are relabelled as computed here | `derived-bridge` |
| the safe period condition reports itself closed | `derived-bridge` |
| the contrast with 09 is emptied, so 11's range excludes nothing | `derived-bridge` |
| the rank-zero corollary reports the period question closed | `derived-bridge` |


## What this round does not claim

* **The Fouquet–Wan theorem is not verified.** This round checks its residual
  hypotheses for one curve at six primes; the theorem consuming them is external.
* **H1 and H2 are cited.** The niveau-2 fundamental-character argument is `10`'s
  and is taken as given; only H3 is computed.
* **Six primes below 6,000 is a measurement of a range, not of a density.** The
  uniform form's claim is about all good supersingular odd primes, which is
  infinite; the certificate for it rests on `g₋ = 2^a`, and what is checked here
  is that premise plus the disjointness that makes the range safe.
* **`c_E = 1` is open**, so the rank-zero `p`-part corollary is not asserted for
  this curve — its analytic input is in place and its period input is not.
* **Optimality remains cited**, as in RUN-031 and RUN-036.
