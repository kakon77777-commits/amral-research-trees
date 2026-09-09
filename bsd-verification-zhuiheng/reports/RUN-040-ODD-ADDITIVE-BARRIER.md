# RUN-040 — The odd-additive period barrier, met at one prime per member and cleared structurally

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`01_Odd_Additive_Period_Barrier`](../../../amral/public/bsd/phase2/files/01_Odd_Additive_Period_Barrier.md) — an obstruction that is not Iwasawa-theoretic but arithmetic-of-periods, and the published sufficient condition that clears it
**Tools:** [`src42_odd_additive_period_barrier.py`](../code/src42_odd_additive_period_barrier.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src42-odd-additive-barrier.json`](../data/gate-logs/src42-odd-additive-barrier.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the barrier is **empty for the base curve** — 696.e1's only additive prime is 2, and `01`'s obstruction is about a fixed *odd* additive prime — and each of the 19 members meets it at exactly one prime, `q` itself. There the Kodaira type is `I₀*` for **19 of 19**, because the twist forces the valuations: `d` squarefree, coprime to `N` and good for `E` scales `c₄` by `d²`, `c₆` by `d³` and `Δ` by `d⁶`, so at `p = d` they are exactly `(2, 3, 6)` — measured on every member, and `(2,3,6)` is `I₀*`, never II, III or IV. With `q ≥ 241 ≥ 11` and optimality cited, `01`'s sufficient condition is met throughout, and `p ∤ c` follows from the cited Manin-constant result. **The excluded types are shown to be reachable rather than assumed non-empty**: `y² = x³ + 11` is type II, `y² = x³ + 11x` is type III, `y² = x³ + 121` is type IV, and the condition correctly fails at each. This is the piece RUN-039 left open, approached from the weaker side `01` actually needs.**

---

## The obstruction is about periods, not Iwasawa theory

`01` makes a distinction worth keeping: Fouquet–Wan permits arbitrary reduction
type at `p`, so a fixed odd additive bad prime is **not** excluded at the theorem
level. What fails is period normalisation — FW Corollary 1.10 uses the modular
period, which differs from the Néron period by the Manin constant. At a good
supersingular `p` that is harmless, since the Manin constant's prime divisors sit
at additive primes. At a fixed **additive** `p` that escape is unavailable,
because `p` is exactly such a prime.

So every odd-additive extension needs an explicit period certificate, and `01`
names a published sufficient condition:

* `p ≥ 11`;
* the local reduction is **not** additive potentially ordinary of Kodaira type
  II, III or IV;
* the twist is optimal.

Then `p ∤ c`.

## The base curve never meets it

696.e1 is additive only at 2. `01`'s obstruction is about an **odd** additive
prime, and `12_Hybrid_Odd_Prime_Router` sends `p = 2` to Banwait–Huang at P0,
which never reaches this period argument. So the barrier's domain is empty for
the base — reported as empty, with the reason, rather than as "passed".

## Each member meets it exactly once, and clears it by construction

| | measured |
| --- | --- |
| the odd additive prime is exactly `q` | **19 of 19** |
| Kodaira type there is `I₀*` | **19 of 19** |
| valuations `(v_q(c₄), v_q(c₆), v_q(Δ))` are `(2, 3, 6)` | **19 of 19** |
| `p ≥ 11` (smallest member is 241) | **19 of 19** |
| `01`'s condition met | **19 of 19** |

The third row is why the second is not a coincidence. A quadratic twist by `d`
scales `c₄ → d²c₄`, `c₆ → d³c₆`, `Δ → d⁶Δ`; when `d` is squarefree, coprime to
the conductor and good for `E`, the valuations at `p = d` are forced to
`(2, 3, 6)` exactly. That is Kodaira `I₀*` — and `I₀*` is not among II, III, IV
for any member, at any bound.

## The excluded types are reachable, and the condition fails there

A condition whose excluded set is never exhibited has not been tested. Rather
than search, the gate constructs candidates and lets Tate's algorithm say what
they are:

| type | curve | `p` | condition met? |
| --- | --- | ---: | --- |
| **II** | `y² = x³ + 11` | 11 | **no** |
| **III** | `y² = x³ + 11x` | 11 | **no** |
| **IV** | `y² = x³ + 121` | 11 | **no** |

All three of the excluded types occur, at a prime satisfying `p ≥ 11`, and the
condition correctly refuses each. So "no member is II, III or IV" is a finding
about the family and not about the emptiness of the category.

## What is not computed is said

"Potentially ordinary" is part of the excluded description, and this arm does not
compute the ordinarity of a potential good reduction. **It is not needed here**:
the Kodaira type alone already places every member outside the excluded set,
whatever the ordinarity turns out to be. The gate records
`potentially_ordinary_computed: false` on every row rather than leaving the
reader to assume it was checked.

And `p ∤ c` itself is a **cited** theorem. What this round checks is that its
hypotheses hold.

## What this closes of RUN-039

RUN-039 left `c_E = 1` open — `11_Derived_Supersingular_FW_Bridge`'s own safe
period condition, proposed to avoid the modular-versus-Néron splice. `01` asks
for less and gets it at the prime that needs it: **`p ∤ c`**, not `c = 1`. The
`p`-part of BSD needs `p` not to divide the Manin constant, not the constant to
be 1, so the weaker statement is the one the argument actually consumes.

The Manin constant is still not computed anywhere in this tree, and that has not
changed. What has changed is that for the odd-additive branch the corpus's own
cited route is now checked rather than assumed: its three hypotheses hold on
every member.

## The drill

**160 defects, 160 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 28 controls undisturbed, over 68 checks.

The 4 planted for this gate, each turning `odd-additive-barrier` red and nothing else:

| planted defect | went red |
| --- | --- |
| the barrier's p >= 11 floor is raised above the family | `odd-additive-barrier` |
| the excluded Kodaira types come back unreachable | `odd-additive-barrier` |
| the even additive prime is counted as an odd one | `odd-additive-barrier` |
| the twist valuations are read off the untwisted model | `odd-additive-barrier` |


## What this round does not claim

* **The Manin-constant theorem is cited, not verified**, and `c_E` is still not
  computed anywhere in this tree.
* **Optimality is cited**, as it has been since RUN-031 — RUN-036 closed the
  premise the audit's optimality argument rests on, not optimality itself.
* **"Potentially ordinary" is not computed.** The type clears the condition
  without it here; on a curve where the type were II, III or IV, this arm could
  not decide the condition at all, and the gate says so per row.
* **The `(2,3,6)` forcing is measured on 19 members** and argued in general from
  the twist scaling. It holds for `d` squarefree, coprime to `N` and good for
  `E` — all three being membership conditions of `𝒫`, which is the fourth time
  this session those conditions have carried weight.
* **The base's `p = 2` is out of scope**, not cleared: `01` is about odd additive
  primes, and 2 is routed elsewhere.
