# RUN-020 — P5's explicit local-unit cancellation recomputed, and the basis-dependence its §6 does not separate

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_P5_Explicit_Local_Unit_Cancellation_389a1_p11_v0.8`](../../../amral/public/bsd/p5/files/BSD_P5_Explicit_Local_Unit_Cancellation_389a1_p11_v0.8.md) — the boxed chain ending in `u_loc ≡ 4 (mod 11)`, and [`BSD_P5_IMC_Closure_and_GPR_Bridge_v0.5`](../../../amral/public/bsd/p5/files/BSD_P5_IMC_Closure_and_GPR_Bridge_v0.5.md) §1.2's declared inputs
**Tools:** [`src23_p5_local_units.py`](../code/src23_p5_local_units.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src23-p5-local-units.json`](../data/gate-logs/src23-p5-local-units.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: every boxed statement in v0.8 reproduces exactly — including the load-bearing one, `v₁₁(t(16P′)) = 1` with `t(16P′)/11 ≡ 7 (mod 11)`, recomputed from the group law up in exact rational arithmetic on a point whose x-coordinate has a 38-digit numerator. The chain through `log_ω(P)/11 ≡ 4` to `v₁₁(u_loc) = 0`, `u_loc ≡ 4` holds link by link. And one thing the document does not say: the map `R ↦ [t(16R)/11]` is a *homomorphism* `E(Q) → Z/11` with `φ(P) = 7`, `φ(Q) = 1`, so it has an index-11 kernel. `{3P + Q, P}` is a genuine Mordell–Weil basis — determinant −1 — whose first vector lies in that kernel and has `v₁₁(log) = 2`. So "the logarithmic factor contributes exactly one positive power of 11" is a fact about the chosen basis vector, not about the curve. §6's boxed rationality equivalence survives that; §6's parenthetical that multiplication by `u_loc` "neither changes the field-of-definition gate nor the 11-valuation" does not, and the document does not separate the two.**

---

## The chain, link by link

v0.8 isolates every explicitly computable 11-local factor in the rank-2
Burns–Kurihara–Sano BSD element and asks whether a hidden 11-denominator
survives. Its answer is a chain of boxed exact statements. All of it is finite
exact arithmetic over **Q**, and none of it had been recomputed.

| step | document | recomputed |
| --- | --- | --- |
| `Δ_E` | 389 | **389** |
| `#E(F₁₁)`, `a₁₁` | 16, −4 | **16, −4** |
| reduction at 389 | split multiplicative, `v(Δ) = 1` | **I₁, `f = 1`, `c = 1`, `v = 1`** |
| `L₁₁(E,1)⁻¹` | `16/11` | **`16/11`** |
| `L₃₈₉(E,1)⁻¹` | `388/389` | **`388/389`** |
| `v₁₁` of the truncation factor | −1 | **−1** |
| short model | `Y² = X³ − 3024X + 46224` | **same** |
| `P = (0,0) ↦ P′` | `(12, 108)` | **`(12, 108)`, on the curve** |
| `ω′/ω` | `1/6` | **`1/6`** |
| **`v₁₁(t(16P′))`** | **1** | **1** |
| **`t(16P′)/11 mod 11`** | **7** | **7** |
| `log_{ω′}(P′)/11 mod 11` | 8 | **8** |
| `log_ω(P)/11 mod 11` | 4 | **4** |
| `v₁₁(u_loc)`, `u_loc mod 11` | 0, 4 | **0, 4** |

The two bold rows are the ones that matter. `16 = #E(F₁₁)` puts `16P′` inside
the formal group at 11, and the residue of `t(16P′)/11` is what makes the later
cancellation exact rather than approximate — it is also the one step an author
cannot check by inspection, because `x(16P′)` has a 38-digit numerator. It was
recomputed here by double-and-add over **Q** with `Fraction`, no floating point
anywhere.

The document's supporting claim `log_{ω′}(t) ≡ t (mod 11²)` for `t ∈ 11Z₁₁` was
checked rather than accepted: the `n`-th term of the formal logarithm is
`c_n t^n / n` with `c_n` integral at a prime of good reduction, so its valuation
is at least `n − v₁₁(n)`, and no `n ≤ 199` brings that below 2.

## One of the agreements is not evidence

At a good prime,

$$L_p(E,1)^{-1}=1-\frac{a_p}{p}+\frac1p=\frac{p+1-a_p}{p}=\frac{\#E(\mathbf F_p)}{p}.$$

The document computes `16/11` in §3 and separately records `#E(F₁₁) = 16` in §2.
The identity says those are **the same computation**. Their agreement confirms
nothing, and the gate records it as a non-check rather than counting it.

## The residue map is a homomorphism, and it has a kernel

This is what the round adds. `16 = #E(F₁₁)`, so `16R` lands in the formal group
`E₁(Q₁₁)` for **every** `R ∈ E(Q)`, and its class in `E₁/E₂ ≅ F₁₁` is exactly
the residue v0.8 computes. Both maps are homomorphisms, so

$$\varphi:E(\mathbf Q)\longrightarrow \mathbf Z/11,\qquad R\mapsto \bigl[t(16R)/11\bigr]$$

is one. With the standard generators `P = (0,0)` and `Q = (1,0)`:

$$\varphi(P)=7,\qquad \varphi(Q)=1,\qquad \varphi(aP+bQ)=7a+b \pmod{11}.$$

`φ(P) = 7` **is** the document's own boxed residue. The law was verified on all
48 combinations with `|a|, |b| ≤ 3` and disagrees on none. `φ(Q) = 1`, so `φ` is
surjective and its kernel

$$\ker\varphi=\{aP+bQ:\ 7a+b\equiv0\ (\mathrm{mod}\ 11)\}$$

has index exactly 11. On it, `16R ∈ E₂` and the logarithm has valuation ≥ 2 —
found explicitly at `3P + Q`, `2P − 3Q` and their negatives, each with
`v₁₁(t(16R)) = 2`.

**And the kernel meets a basis.** `{3P + Q, P}` has determinant

$$\det\begin{pmatrix}3&1\\1&0\end{pmatrix}=-1,$$

so it is a genuine Z-basis of `E(Q)`, and its **first** vector lies in `ker φ`.

An earlier and weaker reading was available and is worth naming as the trap: the
gate's search over small integral points found 16 of them and **every one** gave
valuation 1, which invites the conclusion that valuation 1 is a property of the
formal group rather than of the choice. It is not. Small integral points are a
biased sample of a rank-2 group, and the homomorphism decides the question that
the sample only suggests.

## What that does and does not touch

v0.8 §6 concludes

$$\beta_\xi u_{\rm loc}\in\mathbf Q_{11}\iff\beta_\xi\in\mathbf Q_{11},$$

and justifies it with "since `u_loc ∈ Z₁₁^× ⊂ Q₁₁^×`, multiplication by `u_loc`
neither changes the field-of-definition gate nor the 11-valuation."

* **The equivalence survives.** It needs only `u_loc ≠ 0`, which holds for any
  basis vector `R` with `16R ≠ O`. Nothing here touches it.
* **The valuation clause does not.** In the basis `{3P + Q, P}` the first vector
  has `v₁₁(log) = 2`, so `v₁₁(u_loc) = −1 + 2 = 1` and multiplication by `u_loc`
  **does** change the 11-valuation, by one.

The document is not wrong: it fixes "a Mordell–Weil basis whose first vector is
`P`" and everything it says is true of that basis. What is new is that its
hypothesis is **not basis-invariant**, and the obstruction is explicit and of
index 11.

**The question that leaves for the attack**, stated as a question because this
round does not answer it: if the BKS rank-2 coefficient is canonical — depending
on `P ∧ Q` rather than on `P` — then `u_loc` cannot be the whole 11-local
factor, because `P ∧ Q` is basis-invariant up to `det = ±1` while `u_loc` is
not. Something else in the normalisation must absorb the index-11 dependence, or
the "explicitly normalized" coefficient of §6 is normalisation-relative in a way
the schematic form does not display. This arm has not read the BKS definition
and does not claim which.

## The corpus already draws this line, in another document

`BSD_P5_Rank2_Scalar_Collapse_389a1_p11_v0.3` §3 is titled "The rationality gate
comes before the valuation gate", and it says why:

> For a generic real number there is no canonical operation `v₁₁: R^× → Z`.

so `v₁₁(𝓑_∞(E)) = 0` "is not even well-typed" until a comparison theorem places
the normalised leading term in an algebraic field with a specified embedding at
11. It then splits P5 into two gates, in order:

$$\mathrm{P5\text{-}RAT}:\ \mathcal B_\infty(E)\in\mathbf Q^\times
\qquad\text{and only after that}\qquad
\mathrm{P5\text{-}VAL}_{11}:\ v_{11}(\mathcal B_\infty(E))=0.$$

**That is exactly the seam this round's measurement lands on.** v0.8 §6 states a
RAT-type conclusion and justifies it with a VAL-type clause in the same
sentence; the RAT half is basis-robust and the VAL half is not. The type
discipline the line states in one document is the discipline the other
document's §6 does not apply — and the failure is not hypothetical, it is the
index-11 kernel above.

There is a second, sharper way to say it. `𝓑_∞(E)` is built from an `L`-value
derivative, a real period and a **Néron–Tate regulator** — and the regulator is
basis-invariant, because a change of basis by `U ∈ GL₂(Z)` sends the height
pairing `H` to `UᵀHU` and `det(U)² = 1`. So `𝓑_∞(E)` is basis-invariant while
`u_loc` is not, and their product in §6 therefore cannot be a basis-invariant
quantity. Either something outside the schematic form absorbs the index-11
dependence, or the "explicitly normalized" rank-2 coefficient is
normalisation-relative in a way the form does not display.

## The regulator, measured across both bases — and what that actually tests

| basis | `Reg` at doubling depth 8 |
| --- | --- |
| `{P, Q}` | `0.152467186` |
| `{3P + Q, P}` | `0.152510157` |

They agree to `4.3 × 10⁻⁵`, which is depth-8 precision (RUN-017's depth-10 value
is `0.152460306865`).

**Invariance itself is a theorem and measuring it would prove nothing.** What the
measurement tests is the other direction: if `{3P + Q, P}` were an index-`k`
subgroup rather than a basis, its regulator would be `k²` times larger — a
factor of 4 at the very least, impossible to miss at any depth. Agreement to the
method's own precision rules out every `k > 1`, so this is an independent
confirmation of the determinant argument, and it is why the round says "basis"
rather than "generating set".

## The chain's declared inputs, recomputed as far as this arm goes

`v0.5` §1.2 lists what every later stage stands on, as "exact
database/certified-computation inputs". A reader cannot tell from that list
which entries are arithmetic and which are imports. Separated:

| input | status here |
| --- | --- |
| `N_E = 389` | **recomputed** — one bad prime, type I₁, `f = 1` |
| `∏_ℓ c_ℓ = 1` | **recomputed** — `c₃₈₉ = 1`, and 389 is the only bad prime |
| `E(Q)_tors = 0` | **recomputed** — `gcd #E(F_p)` over `p = 5,7,11,13,17,19` is 1 |
| `a₁₁ = −4`, good ordinary | **recomputed** — `11 ∤ 389`, `11 ∤ a₁₁` |
| `rank E(Q) = 2` | **cited.** This gate computes no rank; RUN-017's regulator assumed two given generators |
| `c_E^Manin = 1` | **cited** |
| maximal ℓ-adic image for every ℓ | **partly.** RUN-007's `X₀(n)` rules out a rational isogeny of degree 2, 3, 5, 7 — irreducibility at four primes, nothing about the other eight of Mazur's twelve, and nothing about surjectivity |
| `Ш(E/Q)[11^∞] = 0` | **cited** — the Kurihara witness at `n = 397·991` plus the Chan-Ho Kim Selmer structure theorem |

RUN-011 had already recomputed the localization matrix `[[1,2],[1,4]]` from the
group law up and confirmed `det(M_loc) = 2`, which is the exact finite
certificate `v1.3` §3 turns into `det(𝓑_N) ≠ 0`. Worth recording next to it:
`v1.3` §4's coincidence is between **lines**, not scalars — the modular side has
coefficient 6, the arithmetic side 2, and `6 = 3·2` in `F₁₁`. That is all a
"same line" claim needs and less than a leading-term formula needs.

## The drill

**86 defects, 86 caught by the check named for each — none uncaught, none
caught by the wrong check. 19 controls, none disturbed, over 39 checks. Eleven
minutes and forty-eight seconds.**

Gate 23 contributes three checks and six defects. Two of the six were wrong on
their first writing in a way worth recording, because it is the same failure the
drill exists to prevent: a defect that calls the very name it is replacing
recurses instead of computing, and the check goes red on a `RecursionError`
rather than on the defect. That is not a check catching anything. Both are now
bound to the original function, as `_true_x_double` and its siblings already
were — and the first pass looked green only because the harness I was testing
with swallowed exceptions.

## What this round does not claim

* **Nothing about BSD**, and nothing about the P5 chain's conclusions. It
  recomputes v0.8's finite arithmetic and measures one structural fact the
  document leaves out.
* **The document is not contradicted.** Every boxed statement is reproduced. The
  basis-dependence is an addition to what §6 says, not a correction of it.
* **`u_loc`'s role in the actual BKS coefficient is not checked.** Whether the
  index-11 dependence matters depends on the definition, which this arm has not
  read.
* **The rank is assumed, not computed**, here and in RUN-017. Every regulator
  and every basis statement in this arm rests on two generators taken from the
  literature.
* **`φ` is verified on `|a|, |b| ≤ 3`.** It is a homomorphism by construction
  and the check confirms that on 48 combinations; it is not an exhaustive
  statement about `E(Q)`.
