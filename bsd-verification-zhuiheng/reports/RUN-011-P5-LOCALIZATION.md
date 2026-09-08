# RUN-011 — P5's localization matrix, recomputed from scratch

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the P5 sub-line's foundations — `389.a1` at `p = 11`, the ramified directions `397` and `991`, and the 2×2 matrix over `F₁₁` the v1.1 certificate turns on
**Tools:** [`src12_p5_localization.py`](../code/src12_p5_localization.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src12-p5-localization.json`](../data/gate-logs/src12-p5-localization.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the localization matrix `[[1,2],[1,4]]` comes back exactly, recomputed from the group law up rather than read — determinant `2 ≠ 0` in `F₁₁`. So does the short model `Y² = X³ − 3024X + 46224` and the generator images `(12,108)`, `(48,108)`. And `397` and `991` are not merely admissible ramified directions: they are the two smallest, out of 25 below 20,000.**

---

## The one object everything rests on

P5 puts everything on one curve, one prime, and one matrix. Version 1.1 states

$$M_{\rm loc}=\begin{pmatrix}1&2\\1&4\end{pmatrix},\qquad \det M_{\rm loc}=2\in\mathbf F_{11}^{\times},$$

the images of the Mordell–Weil generators `P = (0,0)`, `Q = (1,0)` under
localization at `ℓ = 397` and `ℓ = 991`. The nonzero determinant is the whole
point: it is what makes localization **injective** on `E(Q)/11E(Q)`.

## It is computable, so it was computed

For `ℓ` of good reduction and `L_ℓ/Q_ℓ` totally tamely ramified of degree 11
(`ℓ ≠ 11`), the norm quotient is

$$E(\mathbf Q_\ell)/N E(L_\ell)\;\simeq\;E(\mathbf F_\ell)/11\,E(\mathbf F_\ell),$$

so the localization of a global point is just its **reduction mod `ℓ`** read in
that quotient. When `11 ‖ #E(F_ℓ)` the quotient is cyclic of order 11, and for
`R ∈ E(F_ℓ)` the class of `R` is carried by `m·R` with `m = #E(F_ℓ)/11` — zero
exactly when `R ∈ 11·E(F_ℓ)`. Each row is then fixed up to a unit, so the ratio
within a row and the vanishing of the determinant are both well defined.

| `ℓ` | `#E(F_ℓ)` | `v₁₁` | cofactor `m` | `m·P` | `m·Q` | row |
| ---: | ---: | ---: | ---: | --- | --- | --- |
| 397 | `374 = 2·11·17` | 1 | 34 | `(217, 30)` | `(11, 115)` | `[1, 2]` |
| 991 | `1045 = 5·11·19` | 1 | 95 | `(744, 133)` | `(822, 620)` | `[1, 4]` |

$$\boxed{\text{recomputed } [[1,2],[1,4]] \;=\; \text{v1.1's } M_{\rm loc}, \qquad \det = 2 \neq 0 \in \mathbf F_{11}}$$

`v₁₁ = 1` at both is not incidental. If `11²` divided `#E(F_ℓ)`, the norm
quotient would be two-dimensional and the row would not be a single `F₁₁` value
at all. The gate checks the valuation rather than just divisibility.

## The rest of the arithmetic, also recomputed

| the documents say | checked |
| --- | --- |
| `E = 389.a1`, `[0,1,1,−2,0]`, conductor 389 | 389 is prime; `Δ = 389`, `c₄ = 112`, `c₆ = −856` |
| `P = (0,0)`, `Q = (1,0)` are the generators | both satisfy the minimal model exactly |
| short model `Y² = X³ − 3024X + 46224` | `−27c₄ = −3024`, `−54c₆ = 46224` — derived, not copied |
| `P' = (12,108)`, `Q' = (48,108)` | `X = 36x + 3b₂`, `Y = 216y + 108a₁x + 108a₃` gives exactly these, and both satisfy the short model |
| `E(Q)_tors` trivial | `gcd` of `#E(F_p)` over good `p ≤ 43` is **1** |
| `p = 11` is good | `11 ≠ 389`; `#E(F₁₁) = 16`, `a₁₁ = −4`, so **ordinary** |
| `#E(F₃₉₇) = 374 = 34·11`, `#E(F₉₉₁) = 1045 = 95·11` | both exact |
| Kurihara/Kolyvagin condition `a_ℓ ≡ ℓ + 1 (mod 11)` | holds at both; `a₃₉₇ = 24`, `a₉₉₁ = −53`, and both are `≡ 2 (mod 11)` as `ℓ ≡ 1` forces |
| degree-11 real cyclotomic subfields at 397 and 991 | `397 ≡ 991 ≡ 1 (mod 11)`; and the *real* subfield is automatic, since `ℓ − 1 = 11k` with `k` even |
| tame | neither `ℓ` is 11 |

**One terminological point, recorded so it is not mistaken later.** `E` is
ordinary at 11 but **not anomalous** in the classical Mazur sense — `a₁₁ = −4`,
and `−4 ≢ 1 (mod 11)`. The corpus's "anomalous" in these titles refers to
something else, which its own §2 states plainly: the ramified directions are
anomalous *for the classical non-anomalous Mazur–Tate height setup*, because
Burns–Kurihara–Sano Hypothesis 2.2(iii) wants `11 ∤ #E(F_ℓ)` while the Kurihara
condition wants exactly the opposite. The two requirements are mutually
exclusive by construction, which is why the document reports a `NO_GO` there
rather than a route.

## How special the two directions are

`397` and `991` are not the only primes meeting the criterion, and the gate says
how far from unique they are rather than leaving it unsaid. Scanning every prime
below **20,000** for `ℓ ≡ 1 (mod 11)` with `11 | #E(F_ℓ)`:

> **25 admissible**: 397, 991, 1321, 2113, 3389, 3433, 4643, 5501, 6029, 6337,
> 9769, 11177, 11243, 11903, 12541, 13553, 14411, 15401, 15511, 16633, 17491,
> 17623, 18217, 19009, 19867.

**397 and 991 are the two smallest.** The pair is the natural minimal choice, not
an unexplained selection — and there are 23 more directions available if the
argument ever needs them.

## The drill, in the same commit

RUN-010 closed a gap where this tree's README claimed drills it did not have.
Gate 12 therefore ships with its own, in the same commit:

**33 defects, 33 caught by the check named for each. 11 controls, none disturbed.**

Six of the new defects target gate 12 — a doubling formula missing its `2a₂x`
term, `y₃` without the `a₃` correction, scalar multiplication that never doubles,
a point count that forgets the point at infinity, `b₂` computed as `a₁² + 2a₂`,
and the wrong generator substituted for `Q`.

**One of them turned out not to be a defect at all, and it stayed as a control.**
`389.a1` has `a₁ = 0`, so removing the `−a₁y` term from the doubling formula is
identically a no-op. No drill on this curve can test that branch. It is listed
as a control with the reason attached, because a defect list that quietly
dropped it would read as coverage this gate does not have.

## What this round does not claim

* **Nothing about BSD**, and nothing about the rank-2 leading-term formula.
* **`Ш(E/Q)[11] = 0` is not checked.** The P5 documents carry it as an
  *inherited* dependency and label it as such; nothing here bears on it.
  `Sel₁₁(E/Q) ≅ (Z/11)²` follows from rank 2, trivial torsion **and** that
  vanishing — this round supplies the first two and takes no position on the
  third.
* **The comparison the whole sub-line names as OPEN is untouched**: the complex
  analytic leading term against the algebraic regulator. Every P5 package says
  it is open, and this round does not move it.
* **A reproduced matrix is not a proof of the certificate it sits in.** It
  confirms that one computed object is what the document says it is.
