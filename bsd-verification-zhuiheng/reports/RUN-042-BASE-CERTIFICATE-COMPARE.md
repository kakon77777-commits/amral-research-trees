# RUN-042 — The corpus's own base certificate, compared row by row, and the discriminant that needed care

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`15_696e1_Base_Certificate`](../../../amral/public/bsd/phase2/files/15_696e1_Base_Certificate.md) — the corpus's certificate for the anchor, against the independent one this tree built at RUN-030
**Tools:** [`src44_base_certificate_compare.py`](../code/src44_base_certificate_compare.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src44-base-certificate.json`](../data/gate-logs/src44-base-certificate.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: 22 rows compared. **17 are recomputed here and every one agrees** — the a-invariants, `N = 696` summed from Tate's conductor exponents, `Δ_min = −2¹¹·3·29`, trivial torsion, analytic rank 0, `∏c_p = 1`, `L/Ω = 1`, `v₂(L^alg) = 0`, and the whole 2-division-cubic block: `f₂ = x³ + x² + 8x − 16` irreducible, `disc = −11136 = −2⁷·3·29` not a square, Galois closure `S₃`, quadratic resolvent `Q(√−174)`. **5 rows this arm cannot compute are marked as such rather than scored**: the algebraic rank, optimality, the Manin constant, `Ш_an = 1`, and the conductor-5000 BSD verification. **And the discriminant row needed care that a naive comparison would have got wrong**: three different cubics are in play, `15`'s `disc = −11136` and RUN-036's `−45,613,056` differ by `4096 = 64²`, so the comparison has to be by **square class**, not by value — same squarefree part `−174`, same resolvent, same Galois closure. A value comparison would have reported a disagreement that is not one.**

---

## Two certificates for one curve

RUN-030 built a machine-checkable certificate for 696.e1 in this tree, twenty
quantities each derived from the a-invariants alone. `15_696e1_Base_Certificate`
is the corpus's own. Two certificates for one curve should agree, and where they
cannot they should say which rows are computations and which are citations.

## What agrees

| row | | row | |
| --- | --- | --- | --- |
| `y² = x³ + x² + 8x − 16` | ✔ | `∏ c_p = 1` | ✔ |
| `N = 696 = 2³·3·29` | ✔ | `\|E(Q)_tors\| = 1` | ✔ |
| `Δ_min = −2¹¹·3·29` | ✔ | `Reg = 1` | ✔ *(empty determinant)* |
| `Δ_min < 0` | ✔ | `L(E,1)/Ω_E = 1` | ✔ |
| `E(Q)_tors = 0` | ✔ | `v₂(L^alg) = 0` | ✔ |
| analytic rank 0 | ✔ | `f₂ = x³ + x² + 8x − 16` | ✔ |
| `696 < 5000` | ✔ | `f₂` has no rational root | ✔ |
| `disc(f₂) = −11136 = −2⁷·3·29` | ✔ | not a square | ✔ |
| Galois closure `S₃` | ✔ | resolvent `Q(√−174)` | ✔ |

`N = 696` is summed from Tate's conductor exponents rather than quoted, and
`Reg = 1` is flagged as a convention — the empty determinant at rank 0 — not as
an independent measurement.

## What this arm cannot compute, marked rather than scored

* **algebraic rank 0** — no round of this arm computes it. RUN-030's certificate
  lists it among what stays cited, and it stays cited.
* **optimal** — RUN-031 closed the premise and RUN-036 certified the mod-`ℓ`
  images; which curve the modular parametrisation lands on is still not computed.
* **Manin constant = 1** — not computed anywhere in this tree. RUN-039 left
  `c_E = 1` open and RUN-040 checked `01`'s condition for the weaker `p ∤ c`
  instead.
* **`Ш_an = 1`** — the **analytic** order, from LMFDB.
* **the conductor-5000 BSD verification** — a source. Only the inequality
  `696 < 5000` is checked here.

A certificate that scored those five would be reporting citations as checks,
which is the distinction RUN-032 had to make for Referee A's seven lines.

## The discriminant needed care

Three cubics are in play and all three are correct:

| | | discriminant |
| --- | --- | ---: |
| the 2-division polynomial | `4x³ + b₂x² + 2b₄x + b₆` | — |
| `15`'s `f₂` | `x³ + x² + 8x − 16` — the above over 4, monic **because `a₁ = a₃ = 0`** | `−11,136` |
| RUN-036's | `x³ + 4x² + 128x − 1024` — from `x → x/4` | `−45,613,056` |

`−45,613,056 = 4096 × (−11,136)` and `4096 = 64²`. **The same square class**, so
the same squarefree part `−174`, the same quadratic resolvent and the same
Galois closure — which is what the certificate rows actually claim.

Comparing by value would have reported a disagreement between this round and
RUN-036, both of them right. The gate compares by square class and says so in
the row rather than normalising quietly, because the reader needs to know that
two of this arm's own rounds used different models.

The squarefree part also matches RUN-030's certificate, which carries `−174`
from RUN-018. Three routes, one number.

## The refusal is part of the certificate

`15` states outright that it does **not** use

```text
analytic Sha = 1 => actual Sha = 1
```

and calls the inference circular. The gate reads the document and confirms the
refusal is there. A certificate's disclaimers are part of what it certifies: if
that line were dropped, every `Ш` row in the corpus would change meaning while
the numbers stayed the same. RUN-025 counted 36 numeric `Ш` claims in the corpus
and found all of them labelled; this is the same check from the certificate's
side.

## The drill

**168 defects, 168 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 30 controls undisturbed, over 70 checks.

The 4 planted for this gate, each turning `base-certificate` red and nothing else:

| planted defect | went red |
| --- | --- |
| the cited certificate rows are scored as computed | `base-certificate` |
| the discriminant is compared by value instead of square class | `base-certificate` |
| the document is never read, so the refusal is assumed | `base-certificate` |
| the certificate is compared against a different curve | `base-certificate` |


## What this round does not claim

* **Agreement is with the corpus, not with the world.** Both certificates are
  about the same curve from the same a-invariants; a shared error in those would
  not show here. What is ruled out is the two drifting apart.
* **The five cited rows are not verified**, and four of them cannot be by this
  arm at all.
* **`Reg = 1` is a convention at rank 0**, not a regulator computation. RUN-026's
  regulator machinery is for positive rank and is not used here.
* **The `Ш` refusal is checked as present in the document**, not as obeyed
  throughout the corpus — RUN-025 did that, over 36 claims, and this round does
  not repeat it.
* **`L(E,1)` is computed at 20,000 terms**, the same truncation RUN-014 used and
  RUN-032 measured against a shorter one.
