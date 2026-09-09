# RUN-018 — the two-witness criterion's density formula, and where RUN-015's redundancy came from

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`30_Two_Witness_Criterion_v0.1`](../../amral/public/bsd/phase2/files/30_Two_Witness_Criterion_v0.1.md) — the certificate (T1)–(T7), the field `K_E`, and `δ(𝒫_E) = e_E/(3[K_E:Q])`, instantiated at `696.e1`
**Tools:** [`src21_two_witness_certificate.py`](../code/src21_two_witness_certificate.py)
**Logs:** [`src21-two-witness.json`](../data/gate-logs/src21-two-witness.json)

**Result: `[K_E:Q] = 16` and `e_E = 2` computed exactly, giving `δ = 1/24` — the number RUN-009 measured to `0.99900 × 1/24` over primes below 2×10⁷. Every checkable condition of the certificate holds. And the density formula explains the finding RUN-015 could only report: `𝒫`'s third stated condition is redundant *because* `e_E = 2`, and that same factor of 2 is why the density is `1/24` rather than `1/48`.**

---

## The generalisation

`30` lifts the `696.e1` result into a reusable criterion: a finite certificate
(T1)–(T7) on a non-semistable curve whose only additive prime is 2, a Chebotarev
support set, and an explicit density

$$\delta(\mathcal P_E)=\frac{[L_E\cap K_E:\mathbf Q]}{3\,[K_E:\mathbf Q]},\qquad K_E=\mathbf Q\big(\zeta_8,\ \sqrt{\ell^*}\ :\ \ell\mid N_E \text{ odd}\big),$$

with `L_E` the Galois closure of the 2-division cubic and `ℓ* = (−1)^{(ℓ−1)/2}ℓ`.

## The field degree, by exact linear algebra

`K_E` is multiquadratic, so `[K_E:Q] = 2^r` where `r` is the **F₂-rank** of the
exponent vectors of the squarefree parts. For `696 = 2³·3·29` the generators are
`√−1, √2` (from `ζ₈`) and `√(3*) = √−3`, `√(29*) = √29`:

| generator | vector over `(−1, 2, 3, 29)` |
| --- | --- |
| `−1` | `(1,0,0,0)` |
| `2` | `(0,1,0,0)` |
| `−3` | `(1,0,1,0)` |
| `29` | `(0,0,0,1)` |

Rank **4**, so `[K_E:Q] = 2⁴ = 16` — matching the document. That is a rank
computation, not an estimate.

## The intersection, and `e_E`

The 2-division cubic's discriminant has squarefree part `−174`, so `L_E`'s
quadratic resolvent is `Q(√−174)`. Its vector `(1,1,1,1)` is in the span:
`(0,1,0,0) + (1,0,1,0) + (0,0,0,1) = (1,1,1,1)`. So `Q(√−174) ⊂ K_E`, and

$$e_E=[L_E\cap K_E:\mathbf Q]=2,\qquad \delta(\mathcal P_E)=\frac{2}{3\cdot16}=\frac1{24}.$$

RUN-009 measured `0.04162499` over primes below `2×10⁷`, which is
`0.99900 × 1/24`. The formula and the count agree.

## Where RUN-015's redundancy came from

RUN-015 planted a defect that dropped `(q/29) = 1` from the membership test and
**nothing changed** — over 200,000 primes the contradicting cell was empty. It
reported that as a redundancy in the theorem's stated congruence form, correctly,
but could not say why the theorem was written that way.

This is why. The support set is defined by two Chebotarev conditions —
`Frob_q|K_E = 1` and `Frob_q|L_E ∈ C₃`. A 3-cycle acts trivially on the quadratic
resolvent, and the resolvent lies **inside** `K_E`. So the two conditions overlap
in a subgroup of index `e_E`, and the congruence form spells out a condition the
overlap already supplies.

**The redundancy is the factor `e_E`.** It is not an oversight: it is exactly
what makes the density `1/24` and not `1/48`, and the formula in `30` accounts
for it while the congruence form in Corollary 5.1 does not display it. Verified
again here: the members of `𝒫` below 4,000 are the same 19 primes with the
condition and without it.

## The certificate at `696.e1`

| condition | status |
| --- | --- |
| **T1** `E(Q)[2] = 0` | ✓ — no rational 2-isogeny (`X₀(2)`) |
| **T1** `Δ_E < 0` | ✓ `Δ_E = −178,176` |
| **T1** analytic rank 0 | ✓ RUN-014: `w = +1`, `L(E,1) = 1.6317… ≠ 0` |
| **T1** `ord₂ L^{alg}(E,1) = 0` | ✓ `L/Ω = 1` exactly, and `ord₂(1) = 0` |
| **T1** Manin constant odd; `BSD(E,2)` known | **not checked** — cited |
| **T2** `f_E` irreducible, `Gal = S₃` | ✓ resolvent `−174` is not a square |
| **T3** only additive prime is 2 | ✓ `2: II*`, `3: I₁`, `29: I₁` (RUN-016) |
| **T4** 3 multiplicative, `v₃(Δ) = 1` | ✓ |
| **T5** `λ = 29` nonsplit multiplicative, `v₂₉(Δ) = 1` | ✓ |
| **T6/T7** no rational isogeny | ✓ for degrees 2, 3, 5, 7 |

**T6 and T7 are only partly checked.** Mazur's theorem allows prime isogeny
degrees `2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163`; the `X₀(n)` method built
in RUN-007 covers the first four. The other eight are named rather than assumed —
and they matter here, because (T7) is the condition the note says is "included
explicitly to keep the period comparison independent of any auxiliary isogeny
argument".

## The drill, and its cost

**74 defects, 74 caught by the check named for each. 18 controls, none
disturbed, over 33 checks.**

One planted defect moved to the controls with a reason that is a fact about the
field rather than about the code: `K_E` contains `ζ₈`, hence `√−1`, so `√ℓ` and
`√−ℓ` differ by an element already present — adjoining `ℓ*` or `ℓ` gives the
**same field**. Inverting the sign convention cannot change `[K_E:Q]` or what
lies inside it. The `ℓ*` in the definition is there for the reciprocity step of
Lemma 3.2, not for the field, and the check now measures that rather than
asserting it.

The drill had grown to **fifteen minutes** a run, which is a problem in its own
right: one that slow does not get run, and a drill nobody runs is the same
failure as a gate that has only ever been green. The cost is the product of
defects and checks, so three checks were made cheaper without weakening them —
the density scan cut from 300,000 to 60,000 and the pinning scan from 60,000 to
20,000, both far past where the discrimination is settled, and the regulator run
at doubling depth 8 rather than 10, **with tolerances set to what depth 8
actually delivers**. The gate still reports the depth-10 value; the depth is a
parameter now. Eight minutes.

## What this round does not claim

* **Nothing about BSD**, and nothing about Theorem 4.1's proof. It checks the
  certificate's *instantiation* — the arithmetic conditions and the density
  arithmetic — not the seven-step routing that consumes them.
* **T1's Manin constant and `BSD(E,2)` are cited, not verified**, and this round
  does not touch either.
* **T6 and T7 are verified for four of Mazur's twelve degrees.** The isogeny
  class being a singleton is stated by the note and confirmed only that far.
* **The density formula is verified at one curve.** `[K_E:Q]` and `e_E` are
  computed exactly for `696.e1`; the formula's derivation in Proposition 3.3 is
  read, not reproved.
