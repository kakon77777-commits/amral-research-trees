# RUN-037 — The FW-H3 certificate is false as stated, at exactly one prime, and the family survives it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`09_FW_H3_Exact_Compiler`](../../../amral/public/bsd/phase2/files/09_FW_H3_Exact_Compiler.md) — a definition, an exact criterion, and a boxed uniform certificate that a single finite base computation is supposed to license for every odd `p`
**Tools:** [`src39_fw_h3_compiler.py`](../code/src39_fw_h3_compiler.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src39-fw-h3.json`](../data/gate-logs/src39-fw-h3.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: the document's premise holds for 696.e1 — `W₋ = {29}` is non-empty and `g₋ = 1 = 2⁰` is a power of two — and its boxed conclusion `∀p > 2, FW-H3(E,p) = PASS` is **false at `p = 29`**. Run at 77 odd primes below 400, the criterion passes at 76 and fails at one. The reason is a clause the gcd argument never touches: `FW-H3` requires a witness `ℓ ∈ W₋` with **`ℓ ≠ p`**, and when `W₋` is a singleton that clause deletes the only candidate. The gcd shows no odd prime divides every witness valuation, which is the *third* condition; the second is invisible to it. **The family theorem is unaffected, and that is also computed**: `p = 29` is a fixed multiplicative prime, which `12_Hybrid_Odd_Prime_Router` sends to P3 — the leave-one-out over *all* multiplicative primes — where RUN-033 found the witness `ℓ = 3`. And 3 is **split**, so FW-H3 could never have used it: the branch that takes 29 is carrying a witness the failing criterion was not allowed. Every one of the 19 members has the same `W₋`, the same `g₋` and the same single failing prime.**

---

## What the document compiles

`09` is the exact statement of the hypothesis every other Phase 2 document
gestures at:

$$W_-(E)=\{\ell:\ell\parallel N_E,\ E\text{ nonsplit multiplicative at }\ell\}$$

$$\mathrm{FW\text{-}H3}(E,p)\iff\exists\ell\in W_-(E),\ \ell\ne p,\ p\nmid v_\ell(\Delta_{\min})$$

and then offers to settle it once and for all. With
`g₋(E) = gcd_{ℓ∈W₋} v_ℓ(Δ_min)`:

> 若 `W₋(E) ≠ ∅` 且 `g₋(E) = 2^a`，則沒有 odd prime 同時整除所有 witness
> valuations。因此 … `∀p>2, FW-H3(E,p) = PASS`. 只需一個有限 base certificate.

For 696.e1 the inputs are the ones RUN-033 computed: the only nonsplit
multiplicative prime is 29, with `v₂₉(Δ_min) = 1`. So `W₋ = {29}`, `g₋ = 1`, and
1 is `2⁰`. **The premise holds.**

## The conclusion does not

The criterion has three clauses and the gcd argument addresses one. Tested
directly at every odd prime below 400:

| | |
| --- | --- |
| odd primes tested | 77 |
| `FW-H3` passes | 76 |
| **fails** | **`p = 29`** |

At `p = 29` the only element of `W₋` is 29 itself, and `ℓ ≠ p` removes it. There
is no candidate left, so the existential is empty — not because a valuation was
divisible, but because the candidate set was.

This is what a singleton `W₋` costs. RUN-033 reported it as measured fragility —
*one witness, no spare* — without knowing where the cost would land. It lands
here.

## Does the gap reach the family theorem?

Only if some failing `p` actually asks FW-H3. It does not, and the gate checks
rather than assumes:

| `p` | router branch | that branch's witness | usable by FW-H3? |
| ---: | --- | ---: | --- |
| 29 | **P3, fixed multiplicative** | `ℓ = 3` | **no — 3 is split** |

`12_Hybrid_Odd_Prime_Router` P3 handles a fixed multiplicative `p | N` with a
leave-one-out over **all** multiplicative primes, which is
`00_GCD_Witness_Lemmas` lemma 2 and not FW at all. RUN-033 ran that leave-one-out
and got `3 ↦ 29` and `29 ↦ 3`. The witness for `p = 29` is 3, which is split
multiplicative and therefore not in `W₋` — so the branch that takes 29 is using a
witness the FW criterion was never allowed to use.

The two facts fit exactly: FW-H3 fails at 29 because `W₋` is `{29}`, and 29 is
routed elsewhere because it is a bad prime. **The certificate's gap and the
router's exception are the same prime, for opposite reasons.**

## The family

Run on all 19 members below 4,000:

* `W₋` identical to the base's — `{29}` — for **19 of 19**;
* `g₋ = 1` for **19 of 19**;
* the same single failing prime, `29`, for **19 of 19**.

Which is `09`'s own closing section — the H3 witness is preserved along the
family when every `ℓ | N` splits in `Q(√d)` — running rather than asserted, and
it is RUN-035's lemma C seen from the compiler's side.

## Where the premise refuses

A premise that has only ever been satisfied has not been tested. Over 408
nonsingular models:

| curve | `W₋` | valuations | `g₋` | premise |
| --- | --- | --- | ---: | --- |
| `[0, −1, 0, −8, −8]` | **empty** | — | 0 | **refused** — 0 is not a power of two |
| `[0, −1, 1, −1, −6]` | `{3}` | `v₃ = 3` | **3** | **refused** — and the criterion really does fail at `p = 3` |

The second row is the one that matters: the premise refuses *and* the conclusion
it would have licensed is genuinely false there. The first is the empty-set case
again, and it is worth noting that `09` excludes it explicitly — `W₋(E) ≠ ∅` is
in the premise — which is the one place the corpus does guard the empty set that
RUN-033 had to guard by hand.

## The drill

**152 defects, 152 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 26 controls undisturbed, over 66 checks.

The 4 planted for this gate, each turning `fw-h3-compiler` red and nothing else:

| planted defect | went red |
| --- | --- |
| FW-H3 drops the ell != p clause, so the gap disappears | `fw-h3-compiler` |
| W_- admits the split multiplicative primes too | `fw-h3-compiler` |
| g_- is reported as 1 whatever the valuations are | `fw-h3-compiler` |
| every gcd is called a power of two, so the premise never refuses | `fw-h3-compiler` |


## What this round does not claim

* **The gap is in the stated generality, not in the family theorem.** The boxed
  line is false as written; every use of it in this corpus is at a prime that
  never reaches FW. Both are said, and neither replaces the other.
* **`p = 29`'s own branch is not verified here.** That P3 has a witness is
  RUN-033's leave-one-out; whether the multiplicative theorem P3 invokes applies
  is Referee B's territory and untouched.
* **The criterion is run below 400**, and the family compiler below 200 per
  member. Both are far above `max W₋ = 29`, which is the only place the `ℓ ≠ p`
  clause can bite — but the bound is stated rather than argued away.
* **`W₋` is read through Tate's algorithm** on each model, which is what
  identifies `ℓ ‖ N` and the nonsplit type; it is not read off the document.
* **H3 is one of three hypotheses.** H1 and H2 are `10`'s, not this round's.
