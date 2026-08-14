# RUN-009 — Round 03-A.2: the 2–3 bridge, and what §24's route actually costs

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A2_2_3_Infinity_Anchor_Compatibility_v0.1.md` + `Hard_Zeta_ROUTE_MAP_v0.5.md` (2026-08-11 16:43) — source item 26
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (2–3 bridge layer) · [`src11_hardzeta_round03a2_recheck.py`](../code/src11_hardzeta_round03a2_recheck.py) · [`src11_drill.py`](../code/src11_drill.py)
**Logs:** [`src11-hardzeta-round03a2-recheck.json`](../data/gate-logs/src11-hardzeta-round03a2-recheck.json) · [`src11-drill.json`](../data/gate-logs/src11-drill.json)

**Result: 26/26 checks. 14/14 planted defects caught by the check named for each — 9 in the bridge arithmetic, 3 in this run's own finding. 2/2 null controls undisturbed.**

---

## What Round 03-A.2 does

It splits Round 03-A.1's modulus in two. `2^{K_m+1}` becomes a **coarse** residue
mod `2^{K_m}` — the start that merely makes the endpoint an integer — plus one
extra bit `ε_m` that makes the endpoint **odd**. Then it shows that same bit runs
the ternary side as well:

```
3^m·Q_m + B_m = 2^{K_m}·M_m       0 < Q_m < 2^{K_m}
Ŷ_m = M_m + ε_m·3^m               ε_m = 1 − (M_m mod 2)
```

giving §12's **three equivalent bits** — the exact source's high bit, the
endpoint's ternary wrap count, and the complement of the endpoint's parity are
one and the same thing.

**All of it holds**, on every subcritical code to depth 13: the bridge identity,
`Q_m` strictly inside `(0, 2^{K_m})` as §7's sign argument requires, the
coarse/exact split, the synchronization identity, the parity rule, and the wrap
count in `{0,1}`. The exact source really walks to the predicted endpoint under
plain iteration. §30's finite diagnostic reproduces **to the digit** — code
`(1,2,1,1,1,1,2,2,1,1)`, `m=10`, `K=13`, coarse `27`, `M=206`, `ε=1`,
`r̂ = 8219`, `Ŷ = 59255` — and it does illustrate the distinction it is for: `27`
is the *coarse* source there, while the exact source is `8219`.

§22's redundancy boundary checks out too. On all three known anchors the
synchronization bit is zero at **every** depth where `2^{K_m}` exceeds the anchor,
without exception — so once a code is anchored, 3-adic compatibility really is
automatic and adds nothing.

---

## The finding: §24's route is equivalent, not cheaper

§39 sends Round 03-A.3 to look for *"even-parity recurrence **or counterfamily
extraction**"*. This run did the extraction.

§24's proposed sufficient route is:

> subcritical ⟹ `M_m` even infinitely often  ⟹  CST.

Measuring the longest run of consecutive **odd** `M` over subcritical codes:

| depth `m` | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|
| longest odd-`M` run | 2 | 7 | 12 | 17 | 22 | 27 |
| source holding it | 27 | 27 | 27 | 27 | 27 | 27 |

The run grows linearly — and **the code achieving it is the anchored one**. Its
source is constant at 27, so `ε_m = 0` at every depth past `2^{K_m} > 27`, giving
an unbroken odd run that breaks only when the code leaves the subcritical cone
(at `m = 37`, which is `τ_c(27) = 59 = K₃₇` — the same switch RUN-008 measured).

So a subcritical code with an **unbounded** odd-`M` run is exactly a start with
`τ_c = ∞`. The counterfamily §39 asks to extract is the CST counterexample itself.

**§24's route is sound and equivalent — it is not cheaper.** §24 offers it as
"more discrete than a rate lower bound", which is true and is a real change of
shape; what the measurement adds is the price, namely that the discreteness does
not buy a smaller object. Knowing that before spending a round on it is the point
of measuring.

The endpoint parity itself is close to balanced — `M_m` even in 49.9–50.6% of
subcritical codes at every depth past 8 — so there is no cheap bias to exploit
either.

---

## Three findings about my own checks

**A circular check.** The bridge identity `3^m·Q + B = 2^K·M` cannot see a damaged
`B`, because `Q` **and** `M` are both derived from `B` — the identity stays
self-consistent under any offset. A planted defect in the `B` recurrence passed
silently. There is now a route with no `B` in it at all: walk the accelerated map
from `r̂` and compare. Second occurrence of this shape in this arm, after
[`RUN-007`](RUN-007-HARD-ZETA-ROUND-03A.md).

**A convention that never binds, and why.** §4 takes `M_m` in `1 ≤ M_m ≤ 3^m`,
handling `M ≡ 0`. That case is unreachable: every term of `B_m` except the last
carries a factor of 3, so `B_m ≡ 2^{K_{m−1}} (mod 3)` is never divisible by 3, so
`M_m` never lands on `0`. The mutation against it was a no-op for a **provable**
reason, and is retired with that reason attached rather than counted as caught.

**Two defects were invisible to the check I aimed them at.** Reducing `M` by
`3^{m+1}` shifts `M` and `Q` together, so the bridge survives and only the *range*
convention notices. And `accel_code` was exercised only inside the anchored loop,
where truncating its valuation at 2 changes nothing — it now has a direct
comparison against the independent walk, plus a companion check that valuations
above 2 actually occur in the comparison range.

---

## What this does not establish

Nothing about Collatz, and nothing on §38's unproved list. The odd-run measurement
is a beam search to depth 30, not a proof that anchored codes are the only long
runs — it is strong enough to price §24's route, not to close it.
