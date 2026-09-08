# RUN-008 — the half with no evidence: 36,687 kept curves, and what the base actually is

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the curves Algorithm 1 **kept** — the direction the census's own checks are structurally blind to — and the base's own selection criterion
**Tools:** [`src09_kept_curves_removal_gate.py`](../code/src09_kept_curves_removal_gate.py), [`src08_modular_curve_confirmation.py`](../code/src08_modular_curve_confirmation.py)
**Logs:** [`src09-kept-curves.json`](../data/gate-logs/src09-kept-curves.json)

**Result: all 110,061 isogeny determinations on the kept curves decided, zero hits, zero undecided. With RUN-007 that closes Algorithm 1's removal criterion in both directions over the entire 40,749-curve base — 122,247 determinations, no disagreement anywhere. Two things came out of doing it that the pass itself does not say: the base is not one population but two, split exactly by 2-torsion; and RUN-007's agreement tested nothing about the twist-invariance it relies on, because the base contains no twist pairs at all.**

---

## The direction with no evidence in it

Every round so far audited the 4,062 **removed** curves. That is where the
evidence is — each removed curve carries a row saying why. RUN-007 named the
other half and left it:

> an error in that direction is the one the census's own
> `algorithm1_all_removed_explained` check can never see: a missed isogeny
> wrongly *keeps* a curve, and a keep leaves no evidence to audit.

Algorithm 1 removes a base curve for a rational 3-, 5- or 7-isogeny, or for
`|a₃| = 3`, and reports `UNEXPLAINED = 0`. The contrapositive is a claim about
every survivor:

> **kept ⟹ no rational 3-, 5- or 7-isogeny, and `|a₃| ≠ 3`.**

36,687 curves, 110,061 isogeny determinations, and not one row in any results
file. `algorithm1_all_removed_explained` cannot reach them: it audits removals,
and a wrongly-kept curve produces no removal to audit. The check is sound and it
is blind in exactly one direction.

## The result

| | kept but **has** a rational isogeny | confirmed none | undecided |
| --- | ---: | ---: | ---: |
| **n = 3** | **0** | 36,687 | 0 |
| **n = 5** | **0** | 36,687 | 0 |
| **n = 7** | **0** | 36,687 | 0 |

`|a₃| = 3` among the kept: **0**. `j = 0` or `1728`: **0**, and the carve-out
branch is reachable — `27a1` and `32a1` trigger it.

Together with RUN-007's 12,186 determinations on the removed curves, Algorithm
1's criterion is now verified in **both directions across the whole base**:
**122,247 isogeny determinations, zero disagreements, zero undecided.**

## Three things measured rather than read

**The partition.** `kept ⊔ removed = the old base` was recomputed here from the
label file and the census CSV — 36,687 ⊔ 4,062 = 40,749, no overlap, arithmetic
present for every kept curve — rather than taken from the package's own `checks`
block. A package's self-audit is a claim about the package.

**The factorisations.** `j`'s denominator reaches **48 digits** among the kept
curves, past what Pollard rho reaches in any reasonable time. It never had to:
`den(j)` divides `Δ`, and for a minimal model the primes of `Δ` are the primes
of the conductor — which the package supplies as `discriminant_valuations`. So
the factorisation is handed over. This gate reconstructs `∏ p^{v_p}` and compares
it against the `Δ` it computes from the a-invariants itself, and refuses the
shortcut on any curve where the two differ.

> **40,749 agree, 0 disagree.** Not one curve needed a general factorisation.

A supplied factorisation that has been checked is data. One that has not is an
assumption wearing a number's clothes — and it would have silently shrunk the
candidate set, turning an unfinished search into a false "no rational point."

**a₃**, straight off the minimal model.

## The base is two populations, not one

The base is not "the elliptic curves of conductor below 500,000." It is:

| source | curves | rational 2-torsion | undecided |
| --- | ---: | ---: | ---: |
| `Zha16_no_2_tors` | 37,002 | **0** | 0 |
| `CLZ20` | 3,747 | **3,747** | 0 |

A rational 2-isogeny is exactly a rational 2-torsion point, and `X₀(2)` has the
same shape as the others — `j = (t+256)³/t²`, with `N(0) = 2²⁴` again a pure
power of `n`, and `E[2]` unchanged by a quadratic twist because `χ_d` lands in
`{±1}` and `−1 = +1` in `F₂`. So the same complete method decides it.

The first label is exactly true: **zero** of its 37,002 curves has 2-torsion. The
second is the perfect complement: **every one** of its 3,747 does. Nothing is
wrong here — but the base is a union of two disjoint families defined by their
2-part, and only one of them says so in its name. Any argument that treats the
40,749 as a uniform population is wrong on 9.2% of it in a way the labels do not
announce.

Two further properties of the population, both exact and neither obvious:

* **No curve in the base has an integral `j`.** All 40,749 have potentially
  multiplicative reduction at some prime — a real constraint, and one worth
  knowing for the Phase 2 line, which is about non-semistable families.
* **All 40,749 `j`-invariants are distinct.**

## What RUN-007's agreement did not test

That last line is not a curiosity. RUN-007 and this round both decide isogenies
from `j` alone, and the step that licenses it is Phase 2's
[`03_Quadratic_Twist_Invariance_Bridge`](../../amral/public/bsd/phase2/files/03_Quadratic_Twist_Invariance_Bridge.md)
Candidate Lemma A — irreducibility of `ρ̄_{E,p}` is invariant under twisting by a
character. If that failed, two curves sharing a `j` could differ in isogeny
status, and a `j`-only method could not match a per-curve source on both.

The base contains **zero** pairs of curves sharing a `j`. So:

> **RUN-007's 12,186 agreements tested nothing about twist invariance.** The
> method used it as a proven input, and the population gave it no opportunity to
> fail.

This does not weaken RUN-007 — Lemma A is standard representation theory, cited
rather than claimed — but "the j-only method matched a per-curve source
everywhere" would be worthless as *evidence for* twist invariance, and it is
worth saying so before anyone reads it that way. This arm's own work gets the
vacuity check too.

## An agreement running the other way

RUN-007 derived, independently, why RUN-006's method stops at `n = 3`: for
`n ≥ 5` a Galois-stable subgroup has `(n−1)/2` distinct x-coordinates and Galois
need only preserve the set, so an isogeny is a rational *factor* of `ψ_n`, not a
rational root. Phase 2's
[`04_Local_p_Isogeny_Kernel_Criterion`](../../amral/public/bsd/phase2/files/04_Local_p_Isogeny_Kernel_Criterion.md)
states the same thing at the local level: `x(P) ∈ Q_p ⟺ λ² = 1`, so the kernel
polynomial has a linear factor exactly when the kernel character is quadratic —
which for `n = 3` is automatic, the kernel polynomial being linear already.

The corpus already contained the obstruction RUN-007 spent a round rediscovering.
Recording it as corroboration in both directions: the derivation was reached
without the document, and the document says it first.

## What this round does not claim

* **Nothing about BSD.**
* **It verifies that Algorithm 1 applied its stated criterion correctly, in both
  directions. It does not verify that the criterion is the right one** — that
  removing isogeny-carrying and `|a₃| = 3` curves is the correct thing to do is
  the census's design, not its arithmetic.
* **It says nothing about the twist maps**, `247,391` admissible twist pairs, or
  Algorithm 2. Those are separate outputs with separate evidence.
* **The 2-torsion table is a fact about the base's composition, not a defect.**
  No claim is made that the census intended, or should have intended, a uniform
  population.
