# RUN-009 — Theorem 1.1(1): the density is 1/24, and the obvious answer is 1/48

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** `29_Theorem_Note_v1.0`, Theorem 1.1 part (1) — the natural density of `𝒫` — and the arithmetic of the base curve the family theorem is anchored on
**Tools:** [`src10_phase2_density_and_base.py`](../code/src10_phase2_density_and_base.py)
**Logs:** [`src10-phase2-density.json`](../data/gate-logs/src10-phase2-density.json)

**Result: the note's density 1/24 is correct, and the answer a reader would reach by multiplying the three conditions together — 1/48 — is wrong. Measured over the primes below 2×10⁷, the density is 0.04162499, which is 0.99900 × (1/24) and 1.99800 × (1/48). Every arithmetic claim about the base curve 696.e1 checks out, including the one the proof leans on hardest: 29 is nonsplit multiplicative.**

---

## What was checkable, and what was not

Theorem 1.1 has three parts. Parts (2) and (3) — `L(E^(q),1) ≠ 0` and strong BSD
for every `q ∈ 𝒫` — are a synthesis of cited theorems of Skinner,
Burungale–Skinner–Tian–Wan and Fouquet–Wan. **This arm does not recompute them
and does not claim to have checked them.**

Part (1) is arithmetic:

$$\mathcal P=\Big\{q \text{ prime}: q\equiv 1 \ (\mathrm{mod}\ 24),\ \Big(\tfrac{q}{29}\Big)=1,\ f_2 \text{ irreducible mod } q\Big\},\qquad f_2(x)=x^3+x^2+8x-16,$$

and the note claims `δ(𝒫) = 1/24`.

## Why this one is worth checking rather than reading

Three conditions of density `1/8`, `1/2` and `1/3` multiply to **`1/48`**. The
note says `1/24`. Either the note is off by a factor of two, or the conditions
are not independent — and which it is decides whether a stated density anywhere
else in this corpus can be taken at face value.

## They are not independent, and the entanglement is exact

$$\operatorname{disc}(f_2)=-11136=-2^7\cdot 3\cdot 29,\qquad \text{squarefree part } \mathbf{-174=(-6)\cdot 29}.$$

`f₂` has no rational root and its discriminant is not a square, so its splitting
field is an `S₃`-extension — whose quadratic subfield is therefore `Q(√−174)`.

Now `q ≡ 1 (mod 24)` gives `q ≡ 1 (mod 8)` and `q ≡ 1 (mod 3)`, hence
`(−1/q) = (2/q) = (3/q) = 1` and so `(−6/q) = 1`. The second condition is
`(29/q) = 1`. Therefore

$$\Big(\frac{\operatorname{disc}(f_2)}{q}\Big)=\Big(\frac{-174}{q}\Big)=\Big(\frac{-6}{q}\Big)\Big(\frac{29}{q}\Big)=1$$

for **every** `q` that already passes the first two conditions. Frobenius is
pinned inside `A₃`, where the 3-cycles are 2 of 3 rather than 2 of 6. The third
condition has conditional density `2/3`, not `1/3`, and

$$\delta(\mathcal P)=\frac18\cdot\frac12\cdot\frac23=\frac1{24}. \qquad\checkmark$$

`Q(√−174) ⊂ Q(ζ₂₄, √29)` is the whole of it: the cubic's quadratic resolvent is
already inside the field the first two conditions live in.

## The pinning as a falsifiable prediction, tested

An argument that explains a number is not the same as a measurement of it. The
pinning makes a prediction sharp enough to fail:

> for `q ≡ 1 (mod 24)` with `(q/29) = 1`, `f₂ mod q` has 0 or 3 roots and
> **never exactly one**.

Over every such prime below `2×10⁷` — computed by `x^q mod f₂` in `F_q[x]`, not
by scanning residues:

| | count |
| --- | ---: |
| primes with `q ≡ 1 (mod 24)` and `(q/29) = 1` | 79,204 |
| `f₂ mod q` splits completely (3 roots) | 26,315 |
| `f₂ mod q` irreducible (0 roots) | 52,889 |
| **exactly one root — must be zero** | **0** |

Conditional density of irreducibility: **0.667757**, against the predicted
`2/3 = 0.666667`.

## The density, measured

| `x` | `\|𝒫 ∩ [1,x]\| / π(x)` | `× 24` | `× 48` |
| ---: | ---: | ---: | ---: |
| 10⁵ | 0.042010 | 1.0082 | 2.0165 |
| 10⁶ | 0.041096 | 0.9863 | 1.9726 |
| 10⁷ | 0.041631 | 0.9991 | 1.9983 |
| **2×10⁷** | **0.04162499** | **0.99900** | **1.99800** |

`1/24 = 0.04166667`. `1/48 = 0.02083333`. The two candidates are a factor of two
apart, so counting separates them without needing any delicacy about the rate of
convergence.

## The anchor

A family theorem is worth no more than the curve it is anchored on, so the note's
§2 arithmetic was recomputed from the a-invariants `[0,1,0,8,−16]` rather than
read:

$$\Delta_E=-178176=-2^{11}\cdot 3\cdot 29,\qquad c_4=-368.$$

| claim in the note | checked |
| --- | --- |
| conductor `696 = 2³·3·29` | not squarefree ⟹ **`E` is not semistable** ✓ |
| additive at 2 | `v₂(N) = 3 > 1` ✓ — and the model is minimal at 2, since `v₂(c₄) = 4` but `v₂(Δ) = 11 < 12` |
| 3 is multiplicative | `v₃(Δ) = v₃(N) = 1`; `#E_ns(F₃) = 2 = 3 − 1` ⟹ **split** |
| **29 is nonsplit multiplicative** | `v₂₉(Δ) = v₂₉(N) = 1`; `#E_ns(F₂₉) = 30 = 29 + 1` ⟹ **nonsplit** ✓ |

The last row is the one the proof leans on: the note uses 29 as the uniform
Fouquet–Wan auxiliary prime *because* it is nonsplit multiplicative. Split
reduction there would not have served the same role, and the fact is one line of
arithmetic — so it is checked rather than carried.

## What this round does not claim

* **Nothing about BSD**, and nothing about parts (2) and (3) of Theorem 1.1.
  They depend on four cited theorems this gate does not touch. A verified part
  (1) is not partial credit toward the rest.
* **It does not check the novelty question**, which
  [`20_Adversarial_Referee_Verdict`](../../../amral/public/bsd/phase2/files/20_Adversarial_Referee_Verdict.md)
  already separates from validity and routes to its own gate.
* **It does not verify the citation repair** that the same document records —
  "Miller *most* ≠ all conductor < 5000", repaired by Creutz–Miller Theorem 1.1.
  That is a claim about an external paper's statement, and no computation here
  bears on it.
* **The density is a statement about `𝒫`, not about the twists.** That every
  `q ∈ 𝒫` yields a twist satisfying strong BSD is part (3), untested here.
