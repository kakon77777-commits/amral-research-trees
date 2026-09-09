# RUN-031 — Mazur's twelve isogeny degrees, closed for 696.e1 and every twist of it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the limitation this arm has carried since RUN-018 — `X₀(n)` decides four of Mazur's twelve — and [`24_Manin_Period_Audit`](../../../amral/public/bsd/phase2/files/24_Manin_Period_Audit.md), whose optimality argument rests on it
**Tools:** [`src33_mazur_degrees_closed.py`](../code/src33_mazur_degrees_closed.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src33-mazur-degrees.json`](../data/gate-logs/src33-mazur-degrees.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: all twelve of Mazur's prime isogeny degrees are now settled for 696.e1. Eleven are refuted outright by an explicit witness prime — one `ℓ` at which `x² − a_ℓ x + ℓ` is irreducible mod `n`, which no rational `n`-isogeny permits — and `n = 2`, where the criterion is **structurally vacuous** because every element of `F₂` is a square, is settled by RUN-007's `X₀(2)`. Three degrees now carry two independent proofs. And the refutation transfers to the whole twist family: `a_ℓ(E^{(d)}) = χ_d(ℓ)·a_ℓ(E)` with `χ_d(ℓ) = ±1`, so `a_ℓ² − 4ℓ` is unchanged — measured identical on 27 of 27 good primes across three twists, with 14 to 16 sign flips in `a_ℓ` among them, so the invariance is shown where it could have failed rather than vacuously. That closes the premise `24_Manin_Period_Audit`'s optimality argument rests on.**

---

## The limitation, and why it was load-bearing

Since RUN-018 every round that touched the anchor has carried the same line:
RUN-007's `X₀(n)` method decides **four** of the twelve prime degrees Mazur's
theorem allows — 2, 3, 5, 7 — and the other eight are named rather than checked.
RUN-030's certificate lists it among what stays cited.

It is not decorative. `24_Manin_Period_Audit` argues:

> base `696.e1` mod-ℓ images maximal for all ℓ. Quadratic twisting preserves
> residual irreducibility, so `E_q` has no rational prime-degree isogeny; hence
> its **Q**-isogeny class has no other nonisomorphic curve and `E_q` is itself
> the optimal representative.

so the period comparison depends on it.

## The tool was already in the tree

If `E` admits a rational `n`-isogeny then `ρ̄_n` is reducible, so for every prime
`ℓ` of good reduction with `ℓ ≠ n` the characteristic polynomial of Frobenius
splits over `F_n`:

$$x^2-a_\ell x+\ell \text{ factors mod } n \iff a_\ell^2-4\ell \text{ is a square mod } n.$$

**One `ℓ` at which it is a non-residue refutes the isogeny outright.** That is
RUN-007's reducibility sieve, one-sided and exact. It needs no parametrisation,
no list of `j`-invariants, and **nothing recalled** — which after RUN-030 caught
three numbers quoted from memory is the point.

| `n` | witness | |
| --- | --- | --- |
| 2 | — | **sieve structurally vacuous**; `X₀(2)`, RUN-007 |
| 3 | `ℓ = 11`, `a = −2`, `a²−4ℓ ≡ 2` | also `X₀(3)` |
| 5 | `ℓ = 7`, `a = 1`, `≡ 3` | also `X₀(5)` |
| 7 | `ℓ = 5`, `a = −3`, `≡ 3` | also `X₀(7)` |
| 11 | `ℓ = 7`, `a = 1`, `≡ 6` | |
| 13 | `ℓ = 5`, `a = −3`, `≡ 2` | |
| 17 | `ℓ = 5`, `a = −3`, `≡ 6` | |
| 19 | `ℓ = 5`, `a = −3`, `≡ 8` | |
| 37 | `ℓ = 17`, `a = 7`, `≡ 18` | |
| 43 | `ℓ = 5`, `a = −3`, `≡ 32` | |
| 67 | `ℓ = 11`, `a = −2`, `≡ 27` | |
| 163 | `ℓ = 11`, `a = −2`, `≡ 123` | |

**Eleven refuted, twelve covered, three with two independent proofs.**

## `n = 2` is not a search that fell short

Every element of `F₂` is a square — `0² = 0`, `1² = 1` — so `a_ℓ² − 4ℓ` is a
square mod 2 for **every** `ℓ`, and the sieve can never refute there. That is a
structural fact, not a bound that a longer search would pass, and reporting it
as "no witness below 600" would have been the same mistake as reporting an
empty list as a finding.

It is settled instead by a method that **decides** rather than refutes:
RUN-007's `X₀(2)`, which found no rational 2-isogeny, and the 2-division cubic
has no rational root.

## The refutation transfers to every twist

For a quadratic twist, `a_ℓ(E^{(d)}) = χ_d(ℓ)·a_ℓ(E)` with `χ_d(ℓ) = ±1`. The
sign is **squared away**, so `a_ℓ² − 4ℓ` is identical for `E` and every twist at
any `ℓ` good for both. A witness for the base is therefore a witness for the
whole family.

Measured on three family members RUN-015 and RUN-016 worked with:

| `d` | good primes compared | discriminant identical | `a_ℓ` sign flips |
| --- | ---: | ---: | ---: |
| 241 | 27 | **27** | 14 |
| 313 | 27 | **27** | 16 |
| 409 | 27 | **27** | 16 |

The sign-flip column is what makes this a measurement rather than a
tautology: on roughly half the primes `a_ℓ` genuinely changes, and the
discriminant still does not.

The one caveat is stated in the gate: a witness transfers only while `ℓ` stays
good for the twist, so `ℓ` must not divide the twisting discriminant. All the
witnesses above are small primes and every `d` in the support set is `≡ 1 (mod
24)` and coprime to 696, so no witness is lost — but that is a property of these
`d`, not a theorem.

## What this does and does not close

**Closed:** RUN-018's, RUN-030's and the Manin audit's shared premise — 696.e1
and every quadratic twist of it admit no rational prime-degree isogeny, at any
degree Mazur's theorem allows.

**Not closed:** optimality itself. Having a singleton isogeny class means the
optimal curve *is* this curve, which is the audit's inference — but which curve
the modular parametrisation actually lands on is a statement about `X₀(696)` and
is not computed here. The certificate's cited list keeps that line.

## The drill's own control went red, and the new check was right

The first run covering this round reported 128 defects, 128 caught by the check
named for each, 0 uncaught, 0 caught by the wrong check — and **one control
disturbed a check**:

```text
DISTURBED control: square-test mod n drops its last residue, which
                   (n-1)^2 = 1^2 makes redundant      red: mazur-degrees
```

That control has been in the drill for several rounds. Its argument is that
removing the last residue from the square test changes nothing, because
`(n−1)² ≡ 1²` puts the same value back. True — for `n ≥ 3`. **At `n = 2` the
residue being dropped *is* the 1**: `n − 1 = 1`, the identity degenerates to
`1 = 1`, and the set of squares mod 2 genuinely loses a member.

Nothing had ever exercised `n = 2` before. This round made the vacuity there
load-bearing, and the control's justification stopped being true the moment a
check arrived that could test it.

The repair is to the control, not to the check that caught it. Its reason now
reads "for `n ≥ 3`", and the stand-in keeps the full range at `n = 2`. **A
control whose stated reason is false is not a control** — it is an untriaged
defect filed in the wrong list, and it had been passing for rounds because
nothing looked at the one degree where it fails.

## The drill

**136 defects, 136 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 22 controls undisturbed, over 62 checks.

The 2 planted for this gate, each turning `mazur-degrees` red and the checks listed:

| planted defect | went red |
| --- | --- |
| the square test mod n always says yes, so no witness is ever found | `reducibility-sieve`, `mazur-degrees` |
| the quadratic twist returns the curve unchanged | `mazur-degrees`, `gcd-witness-lemmas`, `kodaira-nogo` |


## What this round does not claim

* **The sieve refutes; it does not decide.** A degree with no witness below the
  bound would be undecided, not cleared. Eleven had one, and the twelfth is
  vacuous rather than open — those are different statements and both are made.
* **Mazur's theorem is cited.** That the twelve are the only possible prime
  degrees is a theorem, not a computation, and this round takes it as given.
* **Prime degrees only.** Composite-degree isogenies factor through prime ones,
  which is why the twelve suffice — also cited.
* **The twist transfer is measured on three members**, and argued in general
  from the character identity. Twenty-seven primes each is evidence, not a
  proof over the family.
