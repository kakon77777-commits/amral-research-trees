# RUN-044 — The Chebotarev audit, every field-theoretic step computed, and the compatibility that could have failed

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`25_Chebotarev_Referee_Audit`](../../../amral/public/bsd/phase2/files/25_Chebotarev_Referee_Audit.md) — eight steps from a cubic to a density, none of them computed anywhere in the corpus
**Tools:** [`src46_chebotarev_audit.py`](../code/src46_chebotarev_audit.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src46-chebotarev.json`](../data/gate-logs/src46-chebotarev.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: every step runs. `f₂ = x³ + x² + 8x − 16` has `disc = −11136 = −2⁷·3·29`, no rational root and a non-square discriminant, so `Gal(L/Q) = S₃`; the squarefree part is `−174`, giving `F₀ = Q(√−174)`. `−174 = −6 × 29`, and `Q(√−6)` sits inside `Q(ζ₂₄)` because its discriminant `−24` divides 24 while `Q(√29)`'s does not and `F₀`'s `−696` does not either — so `F₀ ⊂ K = Q(ζ₂₄, √29)` and `[K:Q] = φ(24)·2 = 16`. `S₃`'s normal subgroups have orders `{1, 3, 6}`, exactly one nontrivial proper one, so `L` has exactly one nontrivial proper Galois subfield and `L ∩ K = F₀`, giving `[LK:Q] = 6·16/2 = 48`. The 3-cycles form a class of size 2, and **`δ = 2/48 = 1/24`**. **The compatibility step is shown against a case where it fails**: a 3-cycle has sign `+1` and acts trivially on `F₀`, agreeing with the identity on `K`; a transposition has sign `−1`, contradicts it, and that condition would give density **0**. Three routes now give the same number — this derivation, RUN-018's formula `δ = e_E/(3[K_E:Q]) = 2/48`, and RUN-009's measurement of `0.99900 × 1/24` below `2×10⁷`.**

---

> **Correction note added at RUN-046.** One of the 176 defects in the drill this
> round cites — *squarefree part drops the sign* — went red by raising a
> `TypeError`, not by dropping a sign. Two drill helpers named `_true_squarefree`
> had been bound to functions with different return types, and the later binding
> shadowed the one that defect needed. **A defect that produces a traceback is
> not a defect a check caught**, so one of the 176 was a crash-catch. The names
> are repaired, the drill now refuses to run with any shadowed `_true_*` helper,
> and RUN-046's run re-exercises that defect as a real catch. Every other figure
> in this round stands.

## The chain, computed

| step | | |
| --- | --- | --- |
| `disc(f₂)` | `−11136` | `= −2⁷·3·29` ✔ |
| rational roots | none | irreducible |
| discriminant a square | no | with irreducibility, `Gal(L/Q) = S₃` |
| squarefree part | `−174` | `F₀ = Q(√−174)` |
| `−174 = −6 × 29` | ✔ | |
| `Q(√−6) ⊂ Q(ζ₂₄)` | disc `−24`, and `24 ∣ 24` | ✔ |
| `Q(√29) ⊂ Q(ζ₂₄)` | disc `29`, and `29 ∤ 24` | **no** — which is why it is adjoined |
| `F₀ ⊂ Q(ζ₂₄)` | disc `−696`, and `696 ∤ 24` | **no** — but `F₀ ⊂ K` |
| `[K:Q]` | `φ(24) × 2 = 8 × 2` | **16** |
| `S₃` normal subgroup orders | `{1, 3, 6}` | exactly one nontrivial proper, of index 2 |
| `L ∩ K` | `F₀` | `K` abelian, so the intersection is abelian and Galois, hence the unique degree-2 subfield — which is inside `K` |
| `[LK:Q]` | `6 × 16 / 2` | **48** |
| class size | 2 | the 3-cycles |
| **`δ`** | **`2/48`** | **`1/24`** |

The containment test is the only field theory imported rather than computed:
`Q(√m) ⊂ Q(ζ_n)` exactly when `|disc(Q(√m))|` divides `n`. Everything else —
the discriminants, the subgroup lattice, the degrees — is arithmetic done here.

## The compatibility could have failed, so both sides are shown

The support condition is *identity on `K`* and *a 3-cycle on `L`*. Those are
conditions on two different fields, and they are only jointly satisfiable if they
agree on the intersection `F₀`. `25` says a 3-cycle fixes `F₀`, and that is
exactly right — but a check that has only ever succeeded has not been tested:

| element | sign | trivial on `F₀`? | consequence |
| --- | ---: | --- | --- |
| 3-cycle | `+1` | **yes** | compatible, class size 2, `δ = 1/24` |
| transposition | `−1` | **no** | contradicts the identity on `K`; class empty, **`δ = 0`** |

`F₀` is the fixed field of `A₃`, so the action on it is the sign character. The
3-cycles are in `A₃` and act trivially; the transpositions are not and do not. If
the corpus's support condition had asked for a transposition, the density would
be zero and the whole family would be empty — so this is the step the derivation
most needed and least showed.

## Three routes, one number

* **this derivation**: `δ = 2/48 = 1/24`;
* **RUN-018's formula**: `δ = e_E / (3[K_E:Q]) = 2 / (3 × 16) = 1/24`, from the
  multiquadratic degree `[K_E:Q] = 16` and `e_E = 2`;
* **RUN-009's measurement**: `0.99900 × 1/24` over primes below `2×10⁷`.

RUN-018 also explained the redundancy the three-cycle condition creates —
`e_E = 2` is exactly why the density is `1/24` and not `1/48` — and this round
recovers the same 2 as a conjugacy-class size. The two derivations meet at the
same integer for the same reason, from opposite ends.

## An observation, recorded and not explained

`|disc(F₀)| = 696`, which is the conductor of `E`. The odd part agreeing is
structural — the 2-division field ramifies only at bad primes, and the odd bad
primes are 3 and 29 — but the 2-part agreeing exactly is not explained by
anything in this tree. It is recorded as an observation in the gate's log rather
than as a finding.

## The drill

**176 defects, 176 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 32 controls undisturbed, over 72 checks.

The 4 planted for this gate, each turning `chebotarev-audit` red and nothing else:

| planted defect | went red |
| --- | --- |
| every quadratic field is called a subfield of Q(zeta_24) | `chebotarev-audit` |
| the support condition asks for a transposition | `chebotarev-audit` |
| the squarefree part is not extracted | `chebotarev-audit` |
| every subgroup is counted as normal | `chebotarev-audit` |


## What this round does not claim

* **Chebotarev's theorem is cited.** What is computed is the field data the
  theorem consumes — degrees, the intersection, the class size — and the
  resulting density; the theorem itself is not proved here.
* **`Q(√m) ⊂ Q(ζ_n) ⟺ |disc| ∣ n` is imported**, being the quadratic case of
  Kronecker–Weber. Everything else in the chain is computed.
* **`L ∩ K = F₀` uses that `K` is abelian**, which is true because `K` is a
  compositum of abelian extensions; the gate records the reason but does not
  verify abelianness by computation.
* **RUN-009's `0.99900` is a measurement over a finite range**, not a proof of
  the density; the agreement is evidence that the derivation and the count are
  about the same set.
* **The `|disc(F₀)| = 696` coincidence is an observation**, not a claim that it
  generalises.
