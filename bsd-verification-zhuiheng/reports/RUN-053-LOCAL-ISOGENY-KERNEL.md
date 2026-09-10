# RUN-053 — The criterion RUN-052 said it could not run was in the corpus, cited once; and it has a consequence it does not state

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`04_Local_p_Isogeny_Kernel_Criterion`](../../../amral/public/bsd/phase2/files/04_Local_p_Isogeny_Kernel_Criterion.md) — the local test for FW17-H2
**Tools:** [`src55_local_isogeny_kernel.py`](../code/src55_local_isogeny_kernel.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src55-local-isogeny-kernel.json`](../data/gate-logs/src55-local-isogeny-kernel.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: RUN-052 recorded `LOCAL_H2` branches 2 and 3 as `NOT COMPUTED HERE` and named the missing instrument — the kernel polynomials of a local `p`-isogeny and its dual. **`04` is that instrument, written out in full.** It had been named in exactly **one** earlier report, RUN-008, and the `06` v0.3 procedure that needs it does not cite it. Its five-step chain checks out, and **`p` odd is load-bearing at step 2**: on a Weierstrass model `−(x,y) = (x, −y−a₁x−a₃)`, so `P = −P` *is* the 2-torsion condition — at `p = 2` every point is its own negative, the clause `σ(P) = ±P` holds for every `σ` with no Galois input at all, and the criterion would report `λ² = 1` unconditionally. **And the round's finding is a consequence `04` does not state.** The Weil pairing gives `det E[p] = ω`, so `λ·μ = ω`. `04`'s test applied to `φ` is `λ² = 1`; applied to `φ̂` it is `μ² = 1`. Both at once forces `ω² = 1` — and `ω` surjects onto `(Z/p)^×` because `Q_p(ζ_p)/Q_p` is totally ramified of degree `p−1`, so `ω² = 1 ⟺ (p−1) ∣ 2`. Checked by brute force over **46** primes: true at exactly `{2, 3}`. **So at every `p ≥ 5` the two tests are mutually exclusive** — `04`'s "one isogeny plus its dual is enough" is tight in a stronger sense than it claims, and the second test is only ever consulted after the first has failed. That is `(p−1) ∣ 2` for the **second** time in this corpus, reached from a different document by a different route than RUN-046's. **The criterion is not run on the family**, and the reason is stated rather than worked around: its hypothesis is local reducibility, RUN-036's certificate is about **global** surjectivity, and reading one as the other would be `00` §6's forbidden substitution one level down.**

---

## The chain, and where the hypotheses sit

`04` assumes `E[p]|_{G_{Q_p}}` reducible with a stable line `C ≅ Z/p`, and
`σ(P) = λ(σ)P` on a generator.

| step | rests on |
| --- | --- |
| `x(P) = x(−P)` | nothing — true for every point on every such model |
| `x(P) ∈ Q_p ⟺ σ(P) = ±P ∀σ` | **`p` odd** |
| `σ(P) = ±P ∀σ ⟺ λ(G_{Q_p}) ⊆ {±1}` | `C` Galois-stable and cyclic of order `p` |
| `λ(G_{Q_p}) ⊆ {±1} ⟺ λ² = 1` | nothing — `{±1}` is the 2-torsion of `F_p^×` |
| `λ² = 1 ⟺ ker φ's kernel polynomial has a `Q_p`-linear factor` | **`E[p]` locally reducible** — without a stable line there is no `λ` |

### `p` odd, exhibited rather than asserted

On a Weierstrass model `−(x, y) = (x, −y − a₁x − a₃)`, so `P = −P` says
`2y + a₁x + a₃ = 0` — which is exactly the condition defining `E[2]`. **Every
point of `E[2]` is its own negative.** At `p = 2` the clause `σ(P) = ±P` is
therefore satisfied by every `σ` with no Galois input, and the criterion would
return `λ² = 1` for free.

A criterion whose excluded case is never exhibited has not been tested. This is
the discipline RUN-042 applied to `01`'s excluded Kodaira types, applied here to
a hypothesis rather than a type.

## The consequence `04` does not state

`04` gives the dual's kernel character as `μ = ω λ^{-1}`, which is the same as
saying `λ·μ = ω` — the Weil pairing, `det E[p] = ω`. Then:

* `04`'s test on `φ` is **`λ² = 1`**
* `04`'s test on `φ̂` is **`μ² = 1`**
* both at once ⟹ `(λμ)² = ω² = 1`

and `ω : G_{Q_p} → (Z/p)^×` is **surjective**, because `Q_p(ζ_p)/Q_p` is totally
ramified of degree `p − 1`. So `ω² = 1` iff squaring is trivial on all of
`(Z/p)^×` — a finite computation, run over 46 primes rather than asserted:

$$\omega^2 = 1 \iff (p-1) \mid 2 \iff p \in \{2, 3\}$$

> **At every `p ≥ 5`, at most one of `φ` and `φ̂` can have a `Q_p`-linear
> factor.**

`04` argues that one isogeny plus its dual suffices — that no enumeration of all
local `p`-isogenies is needed. **That is true in a stronger form than it states:**
the two tests are not merely sufficient together, they are *mutually exclusive*,
so the second is only ever consulted after the first has failed and they can
never both confirm.

At `p = 3` they can: `(Z/3)^× = {1, 2}` and `1² ≡ 2² ≡ 1`.

### The closed form was wrong and the computation caught it

The gate carries both the brute-force column and the closed form `(p−1) ∣ 2`,
and asserts they agree. **The first draft wrote the divisibility backwards** —
`(p−1) % 2 == 0`, which is *2 divides p−1* — and the two columns disagreed at
exactly `p = 2`, where `p − 1 = 1` divides 2 and 2 does not divide 1.

The gate exited 1. That is why the closed form is carried *beside* the
computation rather than replacing it.

## `(p−1) ∣ 2`, the second time

| round | document | route |
| --- | --- | --- |
| **RUN-046** | `10` + `03` | `10`'s ordinary congruence names one of `03`'s two cases; the other needs `χ_cyc²` unramified, and `χ_cyc` has order `p−1` on inertia |
| **RUN-053** | `04` | the two kernel characters multiply to `ω`, so both tests firing forces `ω² = 1` |

**Counted from the reports, not from memory** — the scan reports which files
carry the pattern and the fragments it matched, because RUN-029's failure mode
was a count assembled from the shapes the author remembered writing.

The same structural fact — the mod-`p` cyclotomic character has order `p − 1` —
constraining two different criteria from two different documents.

## Why the criterion is not run here

`04`'s chain begins *assuming* `E[p]|_{G_{Q_p}}` is reducible. **This tree has
not decided that**, and one thing it must not do is borrow RUN-036's answer:

| what RUN-036 gives | what `04` needs |
| --- | --- |
| **global** mod-`ℓ` surjectivity at 38 primes ⟹ global irreducibility | reducibility of the restriction to a **decomposition group at `p`** |

A globally surjective representation can restrict to a reducible one at `p` —
that is the ordinary case. **The global certificate is about a different group.**
Reading the 38 certified primes as settling the local question would be `00` §6's
third prohibition one level down, and the gate records a field saying so rather
than leaving it to prose.

## What it would cost, stated rather than guessed

| | |
| --- | --- |
| kernel polynomial degree, `(q−1)/2` | **120 – 1,896** over the 19 members |
| `q`-division polynomial degree, `(q²−1)/2` | **29,040 – 7,193,424** |

The kernel polynomial itself is small. **Finding** it means locating a
Galois-stable line — factoring the `q`-division polynomial over `Q_q`. Neither is
attempted here, and the precondition is undecided anyway.

## The document was there the whole time

| | |
| --- | --- |
| reports naming `04` before this round | **1** — RUN-008 |
| `06` v0.3's branch 3, at RUN-052 | `NOT COMPUTED HERE` |

RUN-052 reported that the instrument to settle `LOCAL_H2` was missing from this
tree. It was: **the tree does not compute it.** What the round did not know is
that the corpus specifies it exactly, in a document cited once, which the v0.3
procedure that needs it does not reference.

**That is the finding, and it is about the corpus, not about the arithmetic.**

## The drill

**223 defects, 223 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 43 controls undisturbed, over 82 checks.

The 5 planted for this gate, each turning `local-isogeny-kernel` red and nothing else:

| planted defect | went red |
| --- | --- |
| 04's chain drops the `p` odd hypothesis from step 2, where p = 2 makes the clause vacuous | `local-isogeny-kernel` |
| the closed form goes back to (p-1) % 2, which is the divisibility backwards | `local-isogeny-kernel` |
| omega squared is reported trivial at every prime | `local-isogeny-kernel` |
| the two kernel tests are reported mutually exclusive at p = 3 too | `local-isogeny-kernel` |
| the precondition is reported settled by RUN-036's global surjectivity | `local-isogeny-kernel` |


## What this round does not claim

* **Nothing is decided about `LOCAL_H2`.** RUN-045's `UNKNOWN` stands unchanged.
* **The mutual-exclusivity result constrains the two tests' joint behaviour.**
  It does not decide either one, and it does not tell you whether FW17-H2 fails.
* **The chain is checked for internal consistency and hypothesis-tracking**, not
  re-derived from Fouquet–Wan. `04`'s boxed equivalence is taken as the
  document's, with its steps made explicit.
* **`ω` surjective is cited**, from total ramification of `Q_p(ζ_p)/Q_p`. What is
  computed here is the consequence — that squaring is trivial on `(Z/p)^×`
  exactly at `p ∈ {2, 3}`.
* **The degree figures are arithmetic, not a feasibility study.** Whether a
  backend could factor a degree-7.2-million polynomial over `Q_q` is not
  measured here.
* **That `04` was cited once is a fact about this corpus and this line's
  reports**, not a judgement about why.
