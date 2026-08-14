# RUN-007 — Round 03-A: the coefficient frontier, and the minimum anchor measured

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A_Coefficient_Frontier_v0.1.md` + `Hard_Zeta_ROUTE_MAP_v0.3.md` (2026-08-11 14:17) — source item 24
**Tools:** [`hz_zeta_measure.rs`](../code/hz_zeta_measure.rs) (`--tau-records`) · [`hz_chart_algebra.py`](../code/hz_chart_algebra.py) (Round 03-A layer) · [`src09_hardzeta_round03a_recheck.py`](../code/src09_hardzeta_round03a_recheck.py) · [`src09_drill.py`](../code/src09_drill.py)
**Logs:** [`src09-hardzeta-round03a-recheck.json`](../data/gate-logs/src09-hardzeta-round03a-recheck.json) · [`src09-drill.json`](../data/gate-logs/src09-drill.json) · [`hz-tau-records-2p32.json`](../data/raw-logs/hz-tau-records-2p32.json)

**Result: 36/36 checks. 17/17 planted defects caught by the check named for each — 9 in Round 03-A's own formulas, 3 in this run's own headline measurement. 2/2 null controls undisturbed.**

---

## What Round 03-A does

It takes Round 02's coefficient compartment `C_k` and compresses it until only one
unknown is left.

* `C_k` is a cylinder union over the **irrational ballot tree**
  `S_k = { w : 3^{u_j(w)} > 2^j ∀ j ≤ k }`;
* it can only shrink at **Beatty event depths** `K_u = ⌈u log₂3⌉`, so `C_k` is a
  staircase;
* its atomic mass is an exact finite Hurwitz-zeta sum,
  `C_k(s) = 2^{-ks} Σ_{w∈S_k} ζ(s, x_w)`, `x_w = r_w/2^k`;
* the **Head–Tail Reduction** `0 ≤ C_k(s) − H_k(s) ≤ ζ(s)·2^{-k(s-1)}` kills every
  progression tail;
* so §29: **`C_k(s) → 0 ⟺ m_k → ∞`**, where `m_k = min C_k`.

All of it checks. The survivor DP reproduces the enumerated tree at every depth to
18; the U-child always survives and the D-child survives exactly when the parent
clears the next depth; at most one U-count layer can cross at any depth; the
Beatty schedule is exactly the bit lengths of powers of three; the exact Hurwitz
mass lands inside the brute-force bracket; the duplication transfer, the lift
assignment, the anchor-ejection rule, the event-loss operator, the product
criterion and both forms of the Head–Tail bound all hold.

And §38 keeps an explicit **已證/未證 ledger** whose first unproved item is
`m_k → ∞`. That one quantity now carries the entire coefficient conjecture.

---

## The headline: `m_k` measured, and what it bounds

`m_k = min{ n ≥ 2 : τ_c(n) > k }` is fixed entirely by the **τ_c record holders**,
so one scan of `[2, 2^32)` determines it for every `k` up to the largest τ_c
there. There are **23 records**, and each was re-derived by exact iteration rather
than trusted.

Feeding each measured `m_k` into §28's own inequality
`C_k(s) ≤ Σ_{n≥m_k} n^{-s} + ζ(s)·2^{-k(s-1)}` turns it into a **rigorous upper
bound on the true infinite `C_k(s)`**:

| `k` | `m_k` | `C_k(2) ≥` | `C_k(2) ≤` |
|---|---|---|---|
| 6 | 7 | 2.04e-02 | 1.79e-01 |
| 58 | 27 | 1.37e-03 | 3.77e-02 |
| 80 | 703 | 2.02e-06 | 1.42e-03 |
| 104 | 10,087 | 9.83e-09 | 9.91e-05 |
| 134 | 35,655 | 7.87e-10 | 2.80e-05 |
| 245 | 8,088,063 | 1.53e-14 | 1.24e-07 |
| 375 | 63,728,127 | 2.46e-16 | 1.57e-08 |
| 446 | 2,788,008,987 | 1.29e-19 | 3.59e-10 |
| **447** | **≥ 2^32** | — | **2.33e-10** |

These bound the **real** quantity, not a truncation — §26 already bounds every
progression tail and §28 bounds the heads by their minimum, so nothing is left
outside.

**The measured answer to §38's open question is: the minimum anchor has escaped
23 times, reaching 2,788,008,987, and no further than the scan.** A sequence that
has increased 23 times may still be bounded, and this measurement cannot tell the
difference — which is exactly why §38 lists it as unproved. It is not evidence for
the conjecture.

The plateau structure §30 predicts holds exactly: `m_k` stays put until the
current holder's own `τ_c`, then jumps to the next record. And the record list
ends at `n = 2,788,008,987, τ_c = 447` — the same start and the same value as the
maximum σ that [`RUN-004`](RUN-004-HARD-ZETA-ORIGIN.md) measured, which is Terras
agreeing with itself from a third direction.

---

## A scope note on the Beatty schedule

§7 fixes the crossing U-count at `u ≥ 1`, so its event set is `{K_u : u ≥ 1}`.
The frontier **also changes at depth 1** — that is the `u = 0` layer, the even
numbers, leaving.

So §8's "`C_{k+1} = C_k` unless `k+1 = K_u` for some `u`" is exact for `k ≥ 2` and
not at `k = 1`. It costs the paper nothing: §11 works at `k ≥ 2` (survivors start
`UU`, so the `u = 0` branch is already gone) and §24's product is based at `C_1`,
i.e. *after* that event. Admitting `u = 0` — where `K_0 = 1` — accounts for every
observed change exactly, and this run checks that it does.

---

## Three more gaps the drill found in my own work

**A circular check.** The anchor plateau test derived `m_k` *from* the record list
and then validated it against the same list, so an overstated `τ_c` was consistent
with it by construction and the planted defect passed silently. The records are
now re-derived by exact iteration, and every record below the brute-force range is
confirmed to actually be a record.

**A tautological check.** The "power form and slope form agree" test computed both
sides from the same expression. It now compares `3^u > 2^k` against the floor form
`u ≥ ⌊k·log₃2⌋ + 1` — with a companion check that the comparison saw **both**
outcomes, since agreement on a one-sided sample proves nothing about a boundary.

**`>` versus `>=` was a no-op for the fourth time.** `3^u` and `2^k` are never
equal on the range in use, so that mutation tests nothing. Fourth occurrence in
this arm; it is a property of the subject, not an accident, and mutations here are
now written to change the answer.

Also, one defect crashed instead of failing; the recheck now degrades to a named
failure.

---

## The drill

17 defects. **Nine** damage Round 03-A's own formulas — the survival condition,
the crossing depth, the DP recursion, the tree pruning, the normalized residue,
the lift assignment, the loss ratio's scale factor, the cylinder scale, the head
representative. **Three** damage this run's own headline: a fake record, an
overstated `τ_c`, a reordered list — because a headline nobody drills is a number
nobody has checked.

One of them is worth naming: damaging `survives()` is caught by the cross-check
against `first_crossing_words`, which carries its own independent condition. That
is the whole reason for keeping two routes to the same tree.

Two null controls disturb nothing.

---

## What this does not establish

Nothing about Collatz. Nothing about `m_k` beyond `2^32`. Nothing about whether
`C_k(s) → 0`.

What it does establish: Round 03-A's compression of the coefficient frontier is
correct everywhere it was checked, and the single quantity that compression leaves
behind now has 23 measured values and a rigorous numerical upper bound at each of
them.
