# RUN-041 — Phase 2's mother problem, with all three sets computed

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`04_Finite_Exceptional_Prime_Problem`](../../../amral/public/bsd/phase2/files/04_Finite_Exceptional_Prime_Problem.md) — the question Phase 2 exists to answer, with an explicit success standard and an explicit failure standard
**Tools:** [`src43_finite_exceptional_primes.py`](../code/src43_finite_exceptional_primes.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src43-finite-exceptional.json`](../data/gate-logs/src43-finite-exceptional.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: ten rounds have now computed all three of `04`'s sets for 696.e1, so its criterion can be evaluated instead of discussed. `P_red = ∅` **universally** — Mazur's theorem makes twelve degrees exhaustive and RUN-031 refuted every one, with RUN-036 certifying surjectivity besides. `P_ram = ∅` by the document's own formula — `W₋ = {29}` with `v₂₉(Δ) = 1`, so `{p : p | 1}` is empty. `P_loc` is **not** empty: RUN-038's eight ordinary primes below 6,000, still appearing at the top of the range. So **`04`'s success criterion is not achieved for all odd `p`, and `P_loc` is the factor that blocks it** — which is `04`'s own §5 failure standard, reached honestly. But the family theorem does not need it: `P_loc` is defined at **ordinary** primes and FW is used only on the **supersingular** branch, and the two sets are computed here to be disjoint. `04`'s mother problem and `12`'s routing solve different problems, and the corpus uses the routing. **And `04`'s warning about its own `P_ram` formula — 此式只能作 compiler heuristic，不能直接當 theorem — turned out exact: RUN-037 found the formula returns `∅` while the criterion is genuinely obstructed at `p = 29`, because the formula has no term for the `ℓ ≠ p` clause.**

---

## The mother problem, and the standard it sets

`04` asks how `∀p > 2, FW(E,p)` becomes a finite certificate, and answers with a
shape rather than a theorem:

$$p\notin P_{\rm red}(E)\cup P_{\rm loc}(E)\cup P_{\rm ram}(E)\Longrightarrow \mathrm{FW}(E,p),$$

with all three finite, effectively computable and certificate-producing. It also
writes the failure standard, and the last line of it is a rule about reporting:

> 此時必須降級，不得用「tested up to $B$」替代全稱量詞。

## The three sets

| set | value | status |
| --- | --- | --- |
| `P_red` | **∅** | **universal** — Mazur's twelve are exhaustive and all twelve are refuted (RUN-031), with surjectivity certified besides (RUN-036) |
| `P_ram` (the formula) | **∅** | `W₋ = {29}`, `v₂₉(Δ) = 1`, and `{p : p ∣ 1}` is empty |
| `P_loc` | `7, 113, 211, 1433, 1811, 2693, 3209, 3529` | **8 members below 6,000, and it has not stopped** — RUN-038 |

The first row is the only one that is universal, and it is universal for a
reason that is a theorem plus twelve computations rather than a search. The
third is a bounded measurement and is tagged as one in the log, with
`claim_is_universal: false` — which is `04` §5's rule applied to this round's own
reporting rather than to someone else's.

## The document warned about its own formula, and the warning was exact

`04` §2 offers `P_ram(E) = ⋂_{ℓ∈W(E)} {p : p ∣ v_ℓ(Δ_E)}` and immediately says:

> **注意：Fouquet–Wan H3 比 ramification alone 更細；此式只能作 compiler
> heuristic，不能直接當 theorem。**

RUN-037 found the precise instance. The formula returns `∅`, so it says no prime
obstructs H3. The criterion itself — run rather than modelled — is obstructed at
`p = 29`, because `FW-H3` requires a witness `ℓ ≠ p` and `W₋ = {29}` has nothing
else to offer. The formula models the ramification condition and has **no term
for the `ℓ ≠ p` clause**.

| | |
| --- | --- |
| formula set | `∅` |
| criterion actually obstructed at | `{29}` |
| what the formula misses | `{29}` |

The corpus warned that its heuristic was not a theorem; this arm found where the
gap is. Neither half is worth much without the other.

## The criterion, evaluated

**Not achieved for all odd `p`.** Two of three sets are empty; `P_loc` is not,
and is not known finite. By `04` §5 the route therefore remains a per-prime
theorem rather than a full-BSD family closure — *if* FW is the route being taken
at those primes.

## It is not, and that is computed

`10_FW_H2_and_Ordinary_Obstruction` says ordinary primes keep the ordinary
theorem precisely because this set does not thin out, and `12_Hybrid_Odd_Prime_Router`
P2 routes them there. So the primes that block `04`'s criterion are primes the
corpus's own router never sends to FW.

Measured rather than argued: `P_loc` is defined by `a_p² ≡ 1 (mod p)` at
**ordinary** primes, the FW branch is the **supersingular** ones, and

$$P_{\rm loc}\cap\{\text{supersingular}\} = \varnothing$$

because a prime cannot be both. So `04`'s mother problem and `12`'s routing are
answering different questions: one asks for FW everywhere, the other never asks
FW where it would fail.

## The drill

**168 defects, 168 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 30 controls undisturbed, over 70 checks.

The 4 planted for this gate, each turning `finite-exceptional` red and nothing else:

| planted defect | went red |
| --- | --- |
| the P_ram heuristic is reported as exact | `finite-exceptional` |
| the structural vacuity at n = 2 is treated as an unfound witness | `finite-exceptional` |
| the bounded local measurement is reported as universal | `finite-exceptional` |
| a supersingular prime is put into P_loc, so the branches overlap | `finite-exceptional` |


## What this round does not claim

* **`P_loc` is not claimed infinite.** Eight members below 6,000 and no sign of
  stopping is what was measured; that it continues is Lang–Trotter's heuristic
  and `10`'s expectation, and the log tags the row `claim_is_universal: false`.
* **`P_red = ∅` is universal, and that rests on Mazur's theorem**, which is
  cited. What this arm computed is the twelve refutations.
* **`P_loc` here is the *ordinary* local set.** `04` §3 asks for FW-H2 in
  explicit local terms generally; `10` supplies it for good ordinary `p` and
  that is what is run. The additive branch's H2 is `05`'s territory (RUN-034).
* **The routing is the corpus's, not this arm's.** This round checks that the
  blocking primes are outside the branch FW is used on; whether `12`'s ordinary
  theorem applies to them is Referee B's question and untouched.
* **`04`'s success criterion is a shape, not a theorem**, and nothing here
  supplies the theorem it asks for.
