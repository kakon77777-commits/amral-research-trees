# RUN-005 — Hard-Zeta Phase I / Round 01: the chart algebra, checked

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_01_Exact_Refinement_v0.1.md` and its bundle (2026-08-11 13:12) — source items 19–20
**Tools:** [`hz_chart_algebra.py`](../code/hz_chart_algebra.py) · [`src07_hardzeta_round01_recheck.py`](../code/src07_hardzeta_round01_recheck.py) · [`src07_drill.py`](../code/src07_drill.py)
**Logs:** [`src07-hardzeta-round01-recheck.json`](../data/gate-logs/src07-hardzeta-round01-recheck.json) · [`src07-drill.json`](../data/gate-logs/src07-drill.json)

**Result: 33/33 checks. 20/20 planted defects caught by the check named for each — 13 of them planted in the paper's own formulas. 2/2 null controls undisturbed.**

---

## What Round 01 is

Round 01 turns Hard-Zeta from a definition into an **algebra**. Each chart `w ∈
{D,U}^k` carries `(r_w, u_w, b_w, m_w, h(w))`, and §2–§6 give a child's data as
closed formulas in the parent's — so the hard height updates *recursively* rather
than by rescanning every prefix. §9 splits a parent's hard set four ways, §10–§13
turn that into an exact Dirichlet-mass conservation law, and §16–§17 recast the
whole thing as a survival/hazard process with `Collatz ⟺ H_K(s) → ∞`.

Almost all of it is finitely checkable. [`hz_chart_algebra.py`](../code/hz_chart_algebra.py)
is those formulas rendered executable — copied from the paper, nothing rearranged,
integer arithmetic throughout — and the recheck confronts it with direct iteration
of `T` that assumes none of it.

**Everything checks.** The child recursion reproduces iteration on 655,350 cases;
the recursive hard height reproduces the hard set of all 2,046 charts to depth 10;
the four-way identity partitions every parent with all four pieces disjoint; mass
conservation holds chart by chart; the trichotomy is exhaustive (719 Zone A, 197
Zone B, 107 Zone C); Zone C loses no mass; and the `U^k` closed form
`Z_{U^k}(s) = 2^{-ks}·ζ(s, 1−2^{-k})` is exact.

---

## The strongest check available: two routes to the same number

The chart algebra computes `Z_w(s)` **exactly** — a finite sum where `h(w)` is
finite, a Hurwitz zeta where it is not. So `Σ_{|w|=k} Z_w(s)` is the *true infinite*
`Z_k(s)`.

[`RUN-004`](RUN-004-HARD-ZETA-ORIGIN.md) measured the same `Z_k(s)` by brute force
over `[2, 2^32)` and bracketed it. The two routes share no code and no method.

**The exact value lands inside the measured bracket at all 22 depths.** At `s = 2`:

| `k` | measured lower | exact (chart algebra) | measured upper |
|---|---|---|---|
| 1 | 2.3370055002e-01 | 2.3370055014e-01 | 2.3370055025e-01 |
| 4 | 4.2732501438e-02 | 4.2732501481e-02 | 4.2732501670e-02 |
| 8 | 4.2017644760e-03 | 4.2017644933e-03 | 4.2017647088e-03 |
| 16 | 3.8847132107e-03 | 3.8847132182e-03 | 3.8847134435e-03 |

That tests Round 01's algebra and RUN-004's bracket at the same time, in one
comparison. 157,625 charts are still alive at depth 22.

---

## How RUN-004's result sits against Round 01's No-Go

§21 proves a **per-chart** No-Go: for any fixed `L`, no `ε_L > 0` makes *every*
nonempty hard chart lose an `ε_L` fraction over `L` more steps, because the `U^k`
subtree conserves mass exactly. Verified here for `L = 1..5` — minimal `k` = 2, 4,
6, 7, 9, first-descent mass literally `0.0` in each.

§22 then says plainly that this does **not** exclude global total contraction.

RUN-004's result lives exactly there, and neither statement subsumes the other:

| | §21 No-Go | RUN-004 |
|---|---|---|
| object | one chart's mass | the global total `Z_k` |
| holds for | every `L` | `L = 1` |
| mechanism | `U^k` expanding subtree | `σ(n) = 3` impossible |

In Round 01's own language RUN-004 says **`λ₂(s) = 0`**, and this run confirms it
from the chart algebra rather than from the brute-force measurement — the layer's
total first-descent mass comes out as a literal `0.0`.

The hazard vanishes identically at **k = 2, 5, 8, 10, 13, 16, 18, 21** on the
computed range — exactly the depths where `k+1` is not an admissible stopping
time — while reaching 0.825 where it does not vanish.

**What that sharpens:** §26 asks whether a non-summable lower bound on `λ_k(s)`
can be established. A *uniform positive* lower bound cannot exist — `λ_k` is
identically zero infinitely often. The cumulative form `Σ λ_k = ∞` that §17
already prefers is untouched: zero terms cost a sum nothing, while being fatal to
a per-step bound.

---

## A hazard budget, from Round 01's own §16

§17 makes Collatz equivalent to `H_K(s) → ∞`, so *how fast* `H_K` can grow is the
whole question. It has an exact cap, in two lines from the paper's own machinery:

> `Z_K = Z_k · ∏_{j=k}^{K−1} (1 − λ_j)` — §16
> `n₀ ∈ E_K` whenever `σ(n₀) > K`, so `Z_K ≥ n₀^{−s}`
>
> ⟹ `Σ_{j=k}^{K−1} −log(1 − λ_j) = log(Z_k / Z_K) ≤ log(Z_k · n₀^s)`

**A single small value that stays hard for a long time caps what every level in
that window can contribute, together.** `n = 27` has `σ = 59`, so it holds the
floor from `k = 8` to `k = 58`:

> **Fifty levels share a total budget of 1.1194 nats at `s = 2`.**
> The fourteen levels inside computational reach have used 0.1047 — 9.4% of it.

This is **not** a no-go: infinitely many bounded windows can still sum to
infinity. It is a rate obstruction, and it is what any proof of `H_K → ∞` has to
survive. The same bound at `n₀ = 703` (`σ = 81`) gives 7.64 nats for 72 levels, and
at `n₀ = 35655` (`σ = 135`) 15.49 nats for 126 — looser, because the budget scales
with `n₀^s`. The **smallest** long-surviving value is always the binding one.

---

## Three things the drill taught me about my own checks

The recheck passed on its first run. It then failed 8 of 20 planted defects, and
three of those exposed real gaps.

**The cap cannot be pinned by members.** §5's `c_v = ⌊b_v/δ_v⌋` was checked by
sampling the first few cylinder members and asking whether `n ≤ c_v` matched the
observed descent. That cannot see an off-by-one: the cylinder has spacing
`2^{k+1}`, so *every* threshold in `(c_v, next member]` selects the same set. Only
**10 charts in the entire sweep** even have a member at or below `c_v`. The cap is
now pinned as the integer statement it is — `δ·c ≤ b < δ·(c+1)`.

The same reasoning retired a defect: shifting §8's stratum floor by one is a
**no-op** for the identical reason. Worth recording as a fact about the algebra —
§8's `c_v + 1` is a canonical choice, not a forced one.

**The zone labels needed their meaning checked, not their existence.** §19's
trichotomy was verified by "no chart fails to match a zone", which a loosened
threshold satisfies while silently relabelling Zone B as Zone A. The labels are
now checked against `δ_D` and `δ_U` directly.

**The phenomenon under study defeated the drill for it.** A defect that compared
the cumulative hazard against the wrong endpoint index went uncaught — because
that endpoint is depth 22, one of the **zero-hazard** levels, where `Z₂₁ = Z₂₂` and
a wrong index makes no difference. The identity is now checked at every endpoint,
and the redundant single-endpoint line, which could not have failed, is gone.

Also: two defects crashed the tool rather than failing a check. A traceback is the
one outcome a drill cannot grade, so the recheck now degrades to a named failure
instead.

---

## The drill

20 defects, **13 of them in the paper's own formulas** — a child residue using the
wrong parity, the affine offset off by a factor, the up-step uncounted, the target
base numerator wrong, the hard height dropping the parent's constraint, the cap
off by one, the stratum ignoring the parent's height, the drift-gap sign flipped,
a zone threshold loosened, the `n = 0` guard dropped, the Euler–Maclaurin
corrections dropped, `n = 1` let into the chart mass, the `U^k` chart given a
finite height.

Each asks: *if Round 01's recursion were wrong in this specific way, would the
brute-force confrontation notice?* All 20 caught by the check named for each.
Breaking the recursion turns almost everything red at once, so "the run went red"
would have been worthless here.

Two null controls — an annotation nothing reads, an unrelated file beside the
documents — disturb nothing.

---

## What this does not establish

Nothing about Collatz, and nothing about whether the hazard sum diverges.

Round 01 is an exact bookkeeping layer, and this run confirms the bookkeeping. The
hazard budget is a constraint on how any future proof can spend, not a proof and
not a refutation.
