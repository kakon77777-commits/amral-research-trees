# RUN-038 — The ordinary obstruction, measured, and the branch FW is actually left

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`10_FW_H2_and_Ordinary_Obstruction`](../../../amral/public/bsd/phase2/files/10_FW_H2_and_Ordinary_Obstruction.md) — three boxed statements and a routing decision that rests on the size of a set
**Tools:** [`src40_fw_h2_ordinary.py`](../code/src40_fw_h2_ordinary.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src40-fw-h2-ordinary.json`](../data/gate-logs/src40-fw-h2-ordinary.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `10`'s cheap exact criterion for good ordinary `p` — FW-H2 fails exactly when `a_p(E)² ≡ 1 (mod p)` — is run over all 780 good odd primes below 6,000. It fails at **eight**: `7, 113, 211, 1433, 1811, 2693, 3209, 3529`, and **every one has `a_p = ±1` exactly**, which Hasse forces for `p ≥ 7` and which is measured rather than quoted, since the inequality is not tight below that. They appear in three of the four ranges the bound is split into, so the failure set is not a finite list a theorem could except away — **which is precisely the document's stated reason for keeping ordinary primes on the ordinary theorem instead of routing them to FW.** The branch FW is left is non-empty and small: **six good supersingular primes**, `23, 251, 1061, 2297, 5479, 5591`, where `10` gives H1 and H2 free and only H3 remains — and RUN-037's compiler clears H3 at every one. RUN-037's single exception cannot reach here, because `W₋` consists of bad primes and this branch of good ones. The potentially-multiplicative branch, which `10` also excludes from FW, is **empty** for this curve, agreeing with RUN-034 from the other side.**

---

## The criterion, and why it is cheap

For good ordinary `p` the residual representation semisimplifies as
`ᾱ ⊕ χ̄_cyc ᾱ⁻¹` with `ᾱ` unramified and Frobenius value `a_p mod p`, so H2
fails exactly when `ᾱ² = 1`:

$$a_p(E)^2\equiv 1\pmod p.$$

One trace per prime. Run over 780 good odd primes below 6,000:

| `p` | 7 | 113 | 211 | 1433 | 1811 | 2693 | 3209 | 3529 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `a_p` | 1 | 1 | −1 | −1 | −1 | 1 | 1 | 1 |

**Every failure has `a_p = ±1` on the nose.** That is Hasse: `|a_p| ≤ 2√p`, so
`a_p ≡ ±1 (mod p)` leaves only `a_p = ±1` unless `1 − p` also fits inside the
interval, which needs `p − 1 ≤ 2√p` and so `p ≤ 5`. The gate checks the small
range rather than quoting the inequality where it does not hold — there are no
failures below 7 here, and that is reported as a measurement.

## The set does not stop, which is the whole argument

`10` says plainly that there is no clean finite-exception theorem to lean on, and
that is a claim about a set. Bucketed:

| range | count | primes |
| --- | ---: | --- |
| `(0, 1500]` | 4 | 7, 113, 211, 1433 |
| `(1500, 3000]` | 2 | 1811, 2693 |
| `(3000, 4500]` | 2 | 3209, 3529 |
| `(4500, 6000]` | 0 | — |

Three of four ranges carry a failure. A set that had dried up after the first
bucket would have made the routing decision unnecessary — FW could have covered
ordinary primes with a finite exception list. It does not dry up, so it cannot.

## The branch FW is actually left

`10`'s first box gives good supersingular primes H1 and H2 for free, from the
niveau-2 fundamental characters, leaving only H3. Below 6,000 there are six:

`23, 251, 1061, 2297, 5479, 5591` — the primes with `a_p = 0`.

RUN-037's compiler settles H3 at every one of them, with witness `ℓ = 29`. And
RUN-037's single exception — `p = 29`, where `W₋ = {29}` and the `ℓ ≠ p` clause
empties the candidate set — **cannot reach this branch**, because `W₋` is made of
bad primes and every prime here is a prime of good reduction. The gate checks
that rather than reasoning to it.

So the FW branch for this curve is: six primes below 6,000, all three hypotheses
accounted for, two of them by citation and one by computation.

## The third box, from the other side

`10` also sends potentially multiplicative primes away from FW, since their local
semisimplification is already the forbidden `ψ ⊕ ψχ̄_cyc`. Measured over the whole
bad-prime set:

| `p` | reduction | potential |
| ---: | --- | --- |
| 2 | additive | potentially good |
| 3 | multiplicative | potentially multiplicative |
| 29 | multiplicative | potentially multiplicative |

3 and 29 are potentially multiplicative because they *are* multiplicative. The
branch `10` excludes — **additive** and potentially multiplicative — is **empty**
for this curve. RUN-034 reached the same conclusion from `05`'s exact no-go, by a
different route and over the whole twist family. Two documents, two rounds, same
answer.

## The drill

**152 defects, 152 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 26 controls undisturbed, over 66 checks.

The 4 planted for this gate, each turning `fw-h2-ordinary` red and nothing else:

| planted defect | went red |
| --- | --- |
| the H2 criterion tests a_p = 1 and forgets a_p = -1 | `fw-h2-ordinary` |
| the supersingular set comes back empty | `fw-h2-ordinary` |
| a bad prime is admitted into the good supersingular branch | `fw-h2-ordinary` |
| the ordinary failure set comes back empty, so the routing argument rests on nothing | `fw-h2-ordinary` |


## What this round does not claim

* **H1 and H2 at supersingular primes are cited, not verified.** That the
  niveau-2 fundamental characters make the local residual type irreducible is
  `10`'s statement and this round takes it as given; what is computed is which
  primes are in that branch and that H3 holds there.
* **The ordinary theorem itself is untouched.** This round measures why ordinary
  primes must not take the FW route; it says nothing about whether the theorem
  they do take applies.
* **The bound is 6,000.** That the failure set continues past it is the
  document's expectation and Lang–Trotter's heuristic, not a measurement — what
  is measured is that it has not stopped below the bound.
* **Supersingular primes below a bound are a measurement, not a density claim.**
  Six is what the range contains.
* **`a_p` is computed by point counting** on each reduced curve, the same routine
  RUN-014 and RUN-031 use.
