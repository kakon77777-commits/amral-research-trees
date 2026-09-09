# RUN-019 — does the witness-network generalisation admit anything, and the corpus's own stop rule applied to this arm

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`31_Witness_Network_Criterion_v0.2`](../../../amral/public/bsd/phase2/files/31_Witness_Network_Criterion_v0.2.md) and [`00_GCD_Witness_Lemmas`](../../../amral/public/bsd/phase2/files/00_GCD_Witness_Lemmas.md) — the gcd lemmas, the leave-one-out condition, and whether "strictly stronger" is non-empty
**Tools:** [`src22_witness_network.py`](../code/src22_witness_network.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src22-witness-network.json`](../data/gate-logs/src22-witness-network.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the generalisation is not vacuous, and the gap is larger than the document's own sentence claims. Over 4,063 small models meeting the certificate's arithmetic conditions, `30` reaches 3,925 and `31` reaches all 4,063 — 138 models, 3.4%, that only `31` can phrase. Every one of the 138 fails the same hypothesis, (T5), and 100 of them do so while `31`'s exceptional set stays empty. Of the 38 that carry an odd exceptional prime, 31 were testable on the analytic side, 14 have analytic rank 0, and 13 of those also satisfy (T1)'s `ord₂ L^alg(E,1) = 0` — so the set of curves meeting the *whole* certificate that `30` cannot state is non-empty, not merely the arithmetic half. Lemmas 2.1/2.2 hold on 203,745 instances with no failure; the leave-one-out condition itself fails at 2,457 fixed primes over the base, which is a real cost of the generalisation and is reported as one.**

---

## What `31` changes

`30`'s certificate pins `v_ℓ(Δ_E) = 1` at two named primes. `31` replaces that
with gcd conditions on the whole multiplicative witness set:

$$g_{\rm mult}=\gcd_{\ell\in\mathcal M}n_\ell,\qquad g_-=\gcd_{\ell\in\mathcal M^-}n_\ell,\qquad n_\ell=v_\ell(\Delta_E),$$

and takes `R_mult ∪ R_-`, the odd primes dividing them, as a **finite
exceptional set** rather than a condition to be avoided. §3 states the point:

> This is strictly stronger than requiring both gcds to be powers of 2.

"Strictly" is a claim about non-emptiness, and non-emptiness is measurable.

## The lemmas

Lemma 2.1 and 2.2 are elementary: "some `ℓ` has `p ∤ n_ℓ`" fails exactly when
`p` divides every `n_ℓ`, which is exactly `p | gcd`. There is nothing to
approximate. They are still checked rather than asserted, because the statement
quietly needs `M ≠ ∅` for the gcd to exist at all, and the leave-one-out form
needs `M∖{p} ≠ ∅` — and an implementation that silently returns "holds" on an
empty set would pass every population test.

**203,745 instances over the 40,749 base curves that have a multiplicative
prime, no failure.** The gcd form and the "some `ℓ` misses `p`" form agree on
110,146 leave-one-out instances and disagree on none.

## What the leave-one-out condition costs

`LOO(p)` is the condition that lets the network route a prime `p` through the
witness set with `p` itself removed. It is not free:

> **it fails at 2,457 fixed primes over the base population.**

Where it fails, the network has to route `p` by hand. That is a fact about the
population rather than about the theorem, and it is the honest counterweight to
the non-emptiness result below: `31` reaches more curves than `30`, and it also
has a failure mode `30` does not have.

## The gcd statistic over the base

The 40,749 base curves are entirely semistable (RUN-016), so **neither criterion
applies to any of them**. The gcd statistic is still computable, and this is the
largest population this arm has:

| quantity | distribution |
| --- | --- |
| odd part of `g_mult` | `1`: 40,733 · `3`: 16 |
| odd part of `g_-` | `1`: 29,301 · `3`: 2,659 · `5`: 1,222 · `7`: 693 · `9`: 322 (plus 6,053 with no nonsplit prime at all) |
| size of `R_mult ∪ R_-` | `0`: 35,350 · `1`: 5,313 · `2`: 86 |

**13.2% have a non-empty exceptional set**, and it is essentially always `g_-`
that produces it — `g_mult` has odd part 1 on 40,733 of 40,749. The exceptional
set is a real cost, and it is concentrated on the nonsplit side.

## Is the generalisation non-empty — and by how much

A direct search over small models (`a₁ ∈ {0,1}`, `a₂ ∈ {−1,0,1}`, `a₃ ∈ {0,1}`,
`|a₄| ≤ 30`, `|a₆| ≤ 30`) for curves meeting the certificate's *arithmetic*
conditions — `Δ < 0`, no rational 2-torsion, `S₃` two-division field, additive
reduction only at 2, `M` and `M⁻` both non-empty — returns **4,063 candidates**.
Classifying each by which criterion can phrase it at all:

| | count |
| --- | --- |
| `30` and `31` both apply | **3,925** |
| `31` only, exceptional set **empty** | **100** |
| `31` only, with an odd exceptional prime | **38** |
| `30` applies but the exceptional set is non-empty | **0** |

The fourth row must be empty — (T4) and (T5) each supply a valuation 1, which
forces both gcds to 1 — and it is measured rather than assumed.

**Every one of the 138 fails on (T5), and none fails only on (T4).** (T5) asks
for a nonsplit multiplicative prime of valuation exactly 1; among the 38 with an
odd exceptional prime, (T5) is satisfiable for **0** of them and (T4) for 34.
That identifies precisely which hypothesis the generalisation is buying out.

It also shows the document's §3 sentence understates its own result. "Strictly
stronger than requiring both gcds to be powers of 2" is a claim about the 38.
But the 100 in the middle row have `g_-` a power of 2 — a single nonsplit prime
of valuation 2 in 94 cases and 4 in 6 — so they are reached by `31` **with no
exceptional prime at all**, and still cannot be stated by `30`. All 100 satisfy
(T4); it is only (T5) that stops them. The gcd reformulation buys more than
the sentence claims, and most of what it buys is not in the exceptional set.

## The analytic side, which is the half that could still have been empty

Arithmetic non-emptiness is the weaker claim. The certificate also demands an
analytic input — analytic rank 0 and `ord₂ L^alg(E,1) = 0` — and a family that
met the arithmetic conditions and never the analytic ones would leave `31` with
an empty domain regardless. So the 38 were run through the L-series machinery:

| outcome | count |
| --- | --- |
| conductor above the gate's cap, not tested | 7 |
| root number undecided at this truncation | 9 |
| `w = −1`, so the rank is odd | 7 |
| `w = +1` but `L(E,1)` vanishes — rank ≥ 2 | 1 |
| **analytic rank 0, numerics consistent** | **14** |
| **…and of those, `ord₂ L^alg(E,1) = 0`** | **13** |

The three negative outcomes are kept apart on purpose. An undecided root number
is not evidence of positive rank; it says only that this gate did not resolve
the sign at 4,000 terms, and collapsing those nine into "rank ≥ 1" would be a
free result.

The one curve that reaches rank 0 and still fails the certificate is worth
naming. `[0,−1,0,0,−27]`, conductor 17,592, has `c₂ = 2` and `L/Ω = 2`. Its BSD
quotient is 1 — odd — while the quantity (T1) actually names is even. Testing
the quotient instead of `L^alg` would have counted it, and the drill now plants
exactly that defect.

**This round does not compute Ш.** The quotient `L·|E_tors|²/(Ω·∏c_p)` is used
only as a consistency test on the numerics: a value that is not a positive
square integer means the period, the L-value, the torsion bound or a Tamagawa
number is wrong, and the row is not counted. Calling it an order of Ш is the
substitution the corpus's own stop rule names, and the next section is about
that.

## The stop rule, applied to this arm

Phase 0's `00_BSD_Global_Enclosure_Consensus` §6 freezes any route that for
three consecutive rounds only increases numerical precision, restates BSD,
renames the same gap, replays the same formula on a new curve, or **substitutes
analytic Ш for actual Ш** — without new theorem applicability, a new exact
certificate, a new excluded domain, a new family, or a barrier escape. The rule
is written for the research line. It applies to the verification arm too, and
nobody else is going to run it against me.

**RUN-017's headline was of the forbidden kind.** "285 curves close on `#Ш = 1`"
is a formula replayed on new curves, and the `#Ш` in it is the analytic order.
Both patterns, in one sentence. It was reported as a result, and under §6 it is
not one.

The three rounds since:

| round | §6 verdict |
| --- | --- |
| RUN-017 | the `#Ш = 1` headline is **replay + analytic-for-actual**. What survives is the two errors it found in my own work — a real period wrong for three rounds, and a root-number confidence that was not one. Error-finding is not on §6's progress list either. |
| RUN-018 | **new exact certificate.** `[K_E:Q] = 16` and `e_E = 2` by exact linear algebra rather than measurement, and the reason RUN-015's redundancy exists. |
| RUN-019 | **new excluded domain and a new family.** 138 models `30` cannot phrase and `31` can, with the failing hypothesis identified as (T5); 2,457 primes where the leave-one-out condition fails; 13 curves meeting the whole certificate. |

**The line is not frozen**, and the reason it is not is RUN-018 and this round
rather than RUN-017. Recording that is the point of running the rule: the
alternative is a line that keeps producing analytic-Ш rows and never notices,
because the rows all look like results.

## The drill

**80 defects, 80 caught by the check named for each — none uncaught, none
caught by the wrong check. 19 controls, none disturbed, over 36 checks.
Eleven minutes and sixteen seconds.**

Gate 22 contributes three checks and seven planted defects. Two of the checks
are new this round and exist because this round's **headline numbers** come out
of them: `criterion-reach` covers the classifier that produces 3,925 / 100 / 38,
and `analytic-classification` covers the four-way analytic verdict. Both are
drilled the same way as everything else — reading (T5) against `M` instead of
`M⁻`, or letting it accept any odd valuation rather than valuation one, each
turns `criterion-reach` red, and so does a candidate landing in the impossible
cell.

One planted defect did not survive contact and moved to the controls with its
reason:

The runtime is the one number that went the wrong way. RUN-018 cut the drill
from fifteen minutes to eight; the three new checks put it back to nineteen,
because the drill runs **every** check once per defect and a 1.5-second scan
inside a check is a two-minute tax on the run. That was fixed before the run
that produced these numbers rather than after — the candidate list is now taken
once at baseline (a scope statement, written down: neither new check can see a
defect planted inside the search, and neither claims to), the analytic fixture
runs at **1,200 terms because 1,200 is measured** — the smallest truncation at
which all four verdicts agree with the 4,000-term run — and the inherited-contract
assertion moved to the cheapest curves that produce both of its branches. 5.56
seconds per sweep became 1.13, and the drill lands at 11:16 instead of 19
minutes. Every one of the four defects still turns its named check red.

> Dropping the root-number requirement from `is_analytic_rank_zero` changes no
> verdict, because `src15`'s `analyse` already encodes the sign **into** the
> L-value — it returns `L = None` when the sign is undecided and `L = 0.0`
> exactly when `w = −1`. So "L is a non-zero number" and "decided, `w = +1`,
> `L ≠ 0`" are the same predicate, and no fixture can separate them.

That is worth stating rather than omitting, because it says something true about
the code: the sign condition in gate 22 is **inherited, not independently
enforced**. If `src15` ever returned a raw partial sum for `w = −1`, gate 22
would silently begin counting odd-rank curves as rank 0. So the check now
asserts that contract directly — `L` must be `None` when the sign is undecided
and exactly `0.0` when `w = −1` — and stubbing `l_value_at_one` to return a
non-zero constant turns it red.

## What this round does not claim

* **Nothing about BSD**, and nothing about `31`'s routing. It checks the
  elementary lemmas and measures whether the generalisation has anything in it.
* **The search is over small models only.** Absence in that range is not
  absence, and the non-emptiness it finds is narrow in one specific way: **all
  138 have exactly one nonsplit multiplicative prime**, so `g_-` is a single
  valuation and not a gcd at all. What is exercised is "a nonsplit valuation
  greater than 1 is allowed", not "a gcd over several nonsplit primes rescues
  the certificate". The second is the interesting case, and this range contains
  no example of it.
* **The base population is semistable**, so neither criterion applies to any of
  its curves; the gcd statistic is computable there and nothing more.
* **Ш is not computed, here or anywhere in this arm.** The BSD quotient is a
  numerics check, and 13 curves satisfying (T1) is a statement about `L^alg`,
  not about Ш.
* **Seven candidates were not tested at all** — conductor above 60,000 — so the
  analytic tally is a lower bound on the 38, not a census of them.
* **The search itself is not drilled.** `criterion-reach` and
  `analytic-classification` cover the classifiers that read a candidate, not
  `certificate_candidates`, which produces one; both take the candidate list at
  baseline and neither could see a defect planted inside the scan. Its
  conditions are each independently checked elsewhere — discriminant,
  reduction type and conductor by gates 16 and 18, the two-division field by
  gate 21 — but the scan that composes them has no drill of its own, and this
  round's 4,063 rests on that.
