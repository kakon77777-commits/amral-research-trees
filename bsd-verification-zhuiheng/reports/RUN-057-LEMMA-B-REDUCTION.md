# RUN-057 — FW-H2 at the twisting prime, by Lemma B: 18 of 19 members pass, member 3529 fails — and every piece had been in this tree since RUN-038

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`03_Quadratic_Twist_Invariance_Bridge`](../../../amral/public/bsd/phase2/files/03_Quadratic_Twist_Invariance_Bridge.md) §1 and Lemma B, joined to [`10_FW_H2_and_Ordinary_Obstruction`](../../../amral/public/bsd/phase2/files/10_FW_H2_and_Ordinary_Obstruction.md) and to [`27`](../../../amral/public/bsd/phase2/files/27_Revised_Derived_Theorem_Candidate.md)'s router
**Tools:** [`src59_lemma_b_reduction.py`](../code/src59_lemma_b_reduction.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src59-lemma-b-reduction.json`](../data/gate-logs/src59-lemma-b-reduction.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: RUN-045 left `H2 = UNKNOWN` at every member's additive prime. RUN-052 ran `06` v0.3 and stopped where the kernel-polynomial test begins. RUN-053 priced that test at factoring a division polynomial of degree up to 7.2 million over `Q_q`. **None of it is needed.** `03` §1 states `ρ̄_{E_q,q} ≅ ρ̄_{E,q} ⊗ χ_q`, and its Lemma B — twist-invariance of the FW-H2 forbidden shape — is, in `08`'s ratio form, an identity: the ratio of two constituents does not see a common twist. So **`FW-H2(E_q, q) ⟺ FW-H2(E, q)`**, and the right-hand side is H2 for the *base* curve at a *good* prime, where the local structure is a theorem and RUN-046 already showed the forbidden shape is exactly `10`'s congruence `a_q² ≡ 1 (mod q)`. Computed on all 19 members: **every one is good and ordinary at `q`, and exactly one has `a_q(E)² ≡ 1 (mod q)` — `q = 3529`, `a_q = 1`, confirmed by three independent point counts.** So the provisional design — `18`, `02`, `06` v0.3, Fouquet–Wan at every odd `p` including `p = q` — **fails H2 at member 3529's own twisting prime.** The revised design, `27`, routes `p = q` to BSTW Theorem 9.21(c), not to FW, and is untouched on its face. **RUN-038's archived log has listed 3529 among the base curve's ordinary obstruction primes for seventeen rounds**; RUN-047 confirmed 3529 in `𝒫` by all three definitions; RUN-035 measured Lemma B's neighbours and left it open; RUN-046 made `10` the whole criterion. Four rounds each held one ingredient. The join is one line. The verdict carries the profile `LEMMA_B_REDUCTION`, **not `07`'s `FW17_EXACT`**: it rests on three cited facts and produces no kernel polynomial.**

---

## The chain

| step | statement | source | status |
| --- | --- | --- | --- |
| S1 | `ρ̄_{E_q,q} ≅ ρ̄_{E,q} ⊗ χ_q` for odd `q` | `03` §1 | **cited** — standard |
| S2 | the FW-H2 forbidden shape is invariant under `⊗` by a character; in `08`'s ratio form the ratio of the two constituents is unchanged by a common twist | `03` Lemma B, `08` | **cited** — Lemma B's 候選 status concerns matching FW's exact shape, on which `03`/`08`/`10` agree (RUN-046, 22,140 pairs) |
| S3 | at a good ordinary `p ≥ 5`, `E[p]|_{G_{Q_p}}` has constituents `ω·ε₁` and `ε₂`, `ε_i` unramified, `ε₂(Frob) ≡ a_p (mod p)`; at a good supersingular `p`, `E[p]|_{G_{Q_p}}` is irreducible | standard | **cited** |
| S4 | at good ordinary `p ≥ 5` the forbidden shape is exactly `a_p² ≡ 1 (mod p)`; the other case needs `ω²` trivial on inertia, i.e. `p ≤ 3` | `10`; RUN-046 | **verified within the corpus** |
| S5 | `E` has good reduction at every `q ∈ 𝒫` | `src16.in_P` | **computed** |
| S6 | `E` is ordinary at every `q ∈ 𝒫` — `q ∤ a_q` | this gate | **computed** — 19 of 19 |
| S7 | `a_q(E)² ≡ 1 (mod q)` at each member | this gate | **computed** — 1 of 19 |

$$\mathrm{FW\text{-}H2}(E_q, q)\ \text{FAILS} \iff E\ \text{ordinary at}\ q\ \ \text{and}\ \ a_q(E)^2 \equiv 1 \pmod q$$

The verdict is conditional on S1–S3 as cited and on S4 as verified *inside the
corpus* rather than against Fouquet–Wan's paper. That is stated in the log as a
field, not left to prose.

## The members

| `q` | `a_q` | ordinary | `a_q² ≡ 1` | FW-H2 at `q` |
| ---: | ---: | --- | --- | --- |
| 241 | −7 | ✔ | | PASS |
| 313 | −21 | ✔ | | PASS |
| 457 | 27 | ✔ | | PASS |
| 673 | −5 | ✔ | | PASS |
| 937 | 7 | ✔ | | PASS |
| 1009 | 21 | ✔ | | PASS |
| 1153 | 47 | ✔ | | PASS |
| 1753 | 63 | ✔ | | PASS |
| 2017 | 41 | ✔ | | PASS |
| 2089 | 29 | ✔ | | PASS |
| 2113 | −37 | ✔ | | PASS |
| 2137 | 79 | ✔ | | PASS |
| 2617 | 21 | ✔ | | PASS |
| 2713 | −31 | ✔ | | PASS |
| 3049 | 79 | ✔ | | PASS |
| 3457 | 33 | ✔ | | PASS |
| **3529** | **1** | ✔ | **✔** | **FAIL** |
| 3769 | −91 | ✔ | | PASS |
| 3793 | 45 | ✔ | | PASS |

No member is supersingular at its own `q`, so nothing escapes through the
irreducible door. `a_3529(E) = 1` by `src15`'s Legendre-symbol count, by
`src57`'s square-table count, and by a deliberately naive loop over all
`(x, y) ∈ F_3529²` — three code paths, one answer. Below 5,000 the family has 23
members and **3529 is still the only one** with `a_q² ≡ 1 (mod q)`.

## What it closes, and what it does not

| | before | after |
| --- | --- | --- |
| RUN-045's Level-1 certificate, H2 at the additive prime | `UNKNOWN` | **decided per member, conditionally** — PASS at 18, FAIL at 1 |
| RUN-052's v0.3 branch 3 | `NOT COMPUTED HERE` | **not needed for the verdict** — Lemma B bypasses the kernel polynomial |
| RUN-053's cost estimate | degree up to 7,193,424 over `Q_q` | **the cost of `07`'s replayable certificate**, not of the verdict |
| `07`'s `FW17_EXACT` profile | not produced | **still not produced** — no kernel polynomial exists in this tree |

The verdict and the certificate are different objects. This round supplies the
first through a theorem chain; `07` asks for the second, and its Rule 4 — a
heuristic certificate emits `UNKNOWN` — is respected by naming the profile
`LEMMA_B_REDUCTION` instead of borrowing `07`'s.

## Which design it breaks

| design | documents | FW at `p = q`? | after this round |
| --- | --- | --- | --- |
| **provisional** | `18`, `02`, `06` v0.3 | **yes** | **broken at member 3529** — the FW route does not deliver `BSD(E_3529, 3529)` |
| **revised** | `27` | **no** — `p = q` → BSTW Theorem 9.21(c), quadratic-twist clause + rank-zero descent, ramK witness 29 | **untouched on its face** — BSTW's hypotheses at `(3529, 3529)` are cited, not verified |

RUN-047/048 read `27`'s router as a partition of all primes with `p = q` sent
to BSTW. So this gate decides a hypothesis that **the corpus's own revised
router had already stopped depending on at `p = q`**. What changes is the
provisional design's status, and the record: the FW-everywhere design that
RUN-045 and RUN-052 compiled has a member it cannot handle, and the corpus
never said so.

## The pieces were in the tree

| ingredient | round | where |
| --- | --- | --- |
| 3529 is an ordinary H2-obstruction prime of the base | **RUN-038** | `src40`'s `no_finite_exception.buckets[2].failures = [3209, 3529]` |
| 3529 ∈ `𝒫` by `18`/`27`, by this tree, by Referee A | **RUN-047** | `src49`'s `three_definitions_of_P` |
| `03` §1 and Lemma B, with B left open | **RUN-035** | `src37` |
| `10`'s congruence is the whole criterion at `p ≥ 5` | **RUN-046** | `src48` |

Four rounds, four ingredients, none joined. **That is a fact about how this
line worked — one document per round — not about the arithmetic.** It is
recorded because a verification arm that only ever reads one document at a
time will miss exactly this class of finding, and the next one should be looked
for on purpose.

### The log read was wrong once

The first draft looked for RUN-038's failures under a flat key that does not
exist and reported "not listed" — a false statement about this line's own
archive. RUN-038 stores its failures per range bucket. The gate now gathers
every bucket. A gate that reports what another round found must read the other
round's log the way that round wrote it.

## A fourth membership condition

`𝒫`'s three definitions (RUN-047) are `q ≡ 1 (mod 24)`, `(q/29) = 1` (redundant),
`f₂` irreducible mod `q`. `01`'s D4 requires `E` ordinary at `p ∣ d` — which 3529
satisfies. **None of them states `a_q(E)² ≢ 1 (mod q)`.**

For the provisional FW-everywhere design that condition is load-bearing, and
without it the family as defined contains a member the design cannot reach. For
`27`'s router it is not needed. Which design the corpus means to stand behind
is a question for the corpus; this round measures both.

## Consistency with RUN-053

RUN-053 showed that at `p ≥ 5` at most one of `φ`, `φ̂` can have a `Q_p`-linear
factor. Here it is identified which: the sub's character `λ = ω·ε₁·χ_q` has
`λ²|_{I_q} = ω² ≠ 1` for `q ≥ 5`, so the sub's test **never** fires; the
quotient's `μ = ε₂·χ_q` has `μ² = ε₂²`, trivial iff `a_q² ≡ 1 (mod q)`. **When
H2 fails at a good ordinary prime, it is always the dual isogeny's kernel
polynomial that has the linear factor.**

## The drill

**243 defects, 243 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 49 controls undisturbed, over 86 checks.

The 6 planted for this gate, each turning `lemma-b-reduction` red and nothing else:

| planted defect | went red |
| --- | --- |
| the ordinary test is inverted, so every member reads supersingular and H2 passes everywhere | `lemma-b-reduction` |
| member 3529 is dropped from the family, and the failure with it | `lemma-b-reduction` |
| RUN-038's failure list is read from a flat key again, so the archive says 3529 was never listed | `lemma-b-reduction` |
| 27's revised router is reported as applying FW at p = q | `lemma-b-reduction` |
| the verdict is reported under 07's FW17_EXACT profile | `lemma-b-reduction` |
| a cited step of the chain is scored computed | `lemma-b-reduction` |


## What this round does not claim

* **Nothing unconditional.** S1, S2, S3 are cited. S4 is verified against the
  corpus's own three statements of H2, not against Fouquet–Wan.
* **Nothing about `27`.** Its `p = q` branch cites BSTW 9.21(c); whether that
  theorem's hypotheses hold at `(3529, 3529)` is not examined.
* **No certificate in `07`'s sense.** No kernel polynomial, no `p`-adic
  factorisation. The profile name says so.
* **Nothing about `BSD(E_3529, 3529)` itself.** One route fails a hypothesis
  there; the statement's truth is untouched.
* **The three counts agree; they are not three implementations of three
  methods.** All three count points mod 3529 — one by Legendre symbol, one by
  a square table, one by brute force over `(x, y)`. Different code, same idea.
* **That the join took until RUN-057 is reported, not explained.**
