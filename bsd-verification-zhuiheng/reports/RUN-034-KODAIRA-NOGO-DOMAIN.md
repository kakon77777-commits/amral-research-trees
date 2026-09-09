# RUN-034 — The exact no-go has no domain in this family, and `𝒫`'s own gcd condition is why

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`05_Kodaira_Prefilters_and_NoGo`](../../../amral/public/bsd/phase2/files/05_Kodaira_Prefilters_and_NoGo.md) — one exact no-go, a structural fact at `p = 3`, a local-torsion detector with a stated non-converse, and a formally forbidden inference table
**Tools:** [`src36_kodaira_prefilters_nogo.py`](../code/src36_kodaira_prefilters_nogo.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src36-kodaira-nogo.json`](../data/gate-logs/src36-kodaira-nogo.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `05`'s exact no-go — `ADDITIVE + POTENTIALLY_MULTIPLICATIVE ⟹ FW17_H2_FAIL` — never fires anywhere in this family, and the reason is one of `𝒫`'s own membership conditions. The base's only additive prime is 2, and it is potentially good (`v₂(j) = 3·4 − 11 = 1 ≥ 0`). Each twist `E^(q)` has additive primes exactly `{2, q}`, both potentially good, on all 19 members below 4,000. That is structural rather than lucky: twisting by `d` makes `d` additive and leaves `j` unchanged, so the potential reduction at `d` is the base's reduction there — and the no-go fires at `d` exactly when the base is **multiplicative** at `d`. Measured over eleven twists it fires at `{3, 29}` and the base is multiplicative at `{3, 29}`: the same set, not merely two small ones. `𝒫` requires `gcd(q, 696) = 1`, which removes `{2, 3, 29}` and so covers every firing `d`. **The condition that reads like bookkeeping is what keeps this no-go out of the family.** Separately, `05`'s `p = 3` step is measured to be special to 3 among odd primes, and its local-torsion clause is recorded as licensing nothing.**

---

## The one exact no-go

`05` is mostly warnings, but it states one thing exactly:

```text
ADDITIVE + POTENTIALLY_MULTIPLICATIVE
=> FW17_H2_FAIL
```

with the reason given in full: such a curve becomes a Tate curve after a
quadratic twist `ψ`, whose residual semisimplification `1 ⊕ ω` twists back to
`ψ ⊕ ψω`, and `ψ² = 1` puts it in exactly the shape FW Theorem 1.7 forbids.
Since Case D of `17_696e1_All_Prime_Router` and P4/P5 of
`12_Hybrid_Odd_Prime_Router` both route into FW, a curve in the family meeting
this antecedent would take the FW branch off the table.

## This gate does not use the table it is auditing

`05` closes by **formally forbidding** three inferences:

```text
potentially supersingular => PASS
potentially good ordinary => FAIL/PASS
Kodaira X                 => automatic H2
```

The finding below is stated as `I₀*` against `I₁*`, which looks like exactly the
third one. It is not: the antecedent is decided throughout by `v_p(j) < 0`, and
the Kodaira symbol is printed **alongside** as a correlate that happens to track
it. A gate that checked the no-go by matching symbols would be committing the
inference it was auditing, so the criterion is kept separate from the label in
the code and the drill goes red if they are swapped.

## Where the no-go fires, by construction

Twisting by `d` makes `d` additive; `j` is twist-invariant, so the potential
reduction at `d` is whatever the base had there. That gives both sides on demand:

| `d` | base at `d` | twist Kodaira at `d` | potential | no-go |
| ---: | --- | --- | --- | --- |
| 2 | additive | `I₇*` | potentially good | silent |
| **3** | **multiplicative** | `I₁*` | **potentially multiplicative** | **FIRES** |
| 5, 7, 11, 13, 23, 31 | good | `I₀*` | potentially good | silent |
| **29** | **multiplicative** | `I₁*` | **potentially multiplicative** | **FIRES** |
| 241, 313 | good | `I₀*` | potentially good | silent |

Fires at `{3, 29}`; base multiplicative at `{3, 29}`. **The same set.** A no-go
that fired nowhere at all would be untested rather than satisfied, which is why
the firing set being non-empty is itself one of the drill's assertions.

## Why the family never meets it

`𝒫`'s third membership condition is `gcd(q, 696) = 1`. The conductor is
`696 = 2³ · 3 · 29`, so the condition removes exactly `{2, 3, 29}` — and every
`d` at which the no-go fires must be a prime where the base is multiplicative,
which means it divides the conductor. So the exclusion covers the whole firing
set, with 2 removed for a different reason (the base is additive but potentially
good there, so the no-go is silent at 2 anyway).

Run over the family directly rather than argued:

* base additive primes: `{2}`, potentially good, no-go silent;
* every member's twist has additive primes exactly `{2, q}` — **19 of 19**;
* the no-go fires at no prime of any member — **19 of 19**.

The condition looked like coprimality bookkeeping to keep the twist clean. It is
also the thing standing between this family and `05`'s only exact no-go.

## `p = 3` is special, measured

`05` argues that at `p = 3` every one-dimensional local constituent is quadratic
or trivial, because `F₃ˣ = {±1}`. True, and the measurement is of the exponent
of `Fₚˣ`:

| `p` | 2 | 3 | 5 | 7 | 11 | 13 | 17 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| exponent | 1 | **2** | 4 | 6 | 10 | 12 | 16 |

Quadratic-or-trivial at 2 and 3 only, so among odd primes the argument is
available at 3 and nowhere else. Checking it only at 3 would not have
distinguished a structural fact from a coincidence — the same separation
RUN-031 had to make for the reducibility sieve at `n = 2`.

## The torsion clause licenses nothing

`05`'s third rule is local — `E(Q_p)[p] ≠ 0 ⟹ FW17_H2_FAIL` — and states its own
non-converse in the document: `NO rational p-torsion != H2 PASS`. This arm
computes the **global** rational torsion, which for 696.e1 is trivial. That is a
strictly stronger vanishing than the local condition, and it still licenses
nothing: the absence of a sufficient condition for FAIL is not a PASS. It is
recorded in the same slot RUN-031 gave `n = 2` — a criterion with no domain here,
not a criterion that passed.

## The drill

**136 defects, 136 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 22 controls undisturbed, over 62 checks.

The 4 planted for this gate, each turning `kodaira-nogo` red and nothing else:

| planted defect | went red |
| --- | --- |
| the no-go is decided by the Kodaira symbol, which 05 forbids | `kodaira-nogo` |
| every prime is reported potentially good, so nothing ever fires | `kodaira-nogo` |
| the p = 3 character fact is reported as holding at every prime | `kodaira-nogo` |
| the twist probe contains only good primes, so the no-go is never offered a chance to fire | `kodaira-nogo` |


## What this round does not claim

* **H2 is not computed.** The no-go is sufficient for FAIL; its antecedent being
  absent leaves H2 exactly where it was. This round removes an obstruction from
  the family's path, and removing an obstruction is not clearing a hypothesis.
* **The Tate-curve argument is cited, not verified.** That `1 ⊕ ω` twists to
  `ψ ⊕ ψω` and that FW Theorem 1.7 forbids that shape are both taken as given;
  what is computed here is only the antecedent.
* **The local torsion condition is not computed.** Only the global rational
  torsion is, and the gate says so in its own log rather than letting the
  stronger statement stand in for the weaker one.
* **The firing set is measured on eleven probe primes** and argued in general
  from the twist-invariance of `j`. Eleven is evidence for the general claim, not
  a proof of it.
* **Referees B and C remain untouched**, as in RUN-032. The FW hypotheses
  themselves need external theorems; this round only establishes that `05`'s
  no-go does not close the door before they are reached.
