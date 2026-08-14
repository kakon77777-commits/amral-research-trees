# RUN-004 — The Hard-Zeta origin: `Z_k(s)` measured, and `L = 1` refuted

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `Faithful_Global_Quantifier_Compression_Proof_Route_v0.1_bundle.zip` (2026-08-11 11:40) and `..._v0.1.1.md` (13:11) — source items 17–18, the origin of the Hard-Zeta line that 44 of the 64 items descend from
**Tools:** [`hz_zeta_measure.rs`](../code/hz_zeta_measure.rs) · [`src06_hardzeta_origin_recheck.py`](../code/src06_hardzeta_origin_recheck.py) · [`src06_drill.py`](../code/src06_drill.py)
**Logs:** [`src06-hardzeta-origin-recheck.json`](../data/gate-logs/src06-hardzeta-origin-recheck.json) · [`src06-drill.json`](../data/gate-logs/src06-drill.json) · [`hz-zeta-2p32.json`](../data/raw-logs/hz-zeta-2p32.json)

**Result: 24/24 checks. 24/24 planted defects caught by the check named for each. 2/2 null controls undisturbed.**

---

## What the paper builds

§12–§14 give a general bridge. For a countable domain with a **monotone**
certificate system `C_k(x) ⇒ C_{k+1}(x)`, and any strictly positive summable
weights,

```
∀x ∃k : C_k(x)   ⟺   Q_k → 0,      Q_k = Σ_{x ∈ E_k} ω_x,   E_k = { x : ¬C_k(x) }
```

proved by continuity from above on a finite atomic measure. §15–§16 instantiate
it at `σ(n) = inf{ j ≥ 1 : T^j(n) < n }` with `ω_n = n^{-s}`:

```
Collatz  ⟺  Z_k(s) → 0,      Z_k(s) = Σ_{ n ≥ 2, σ(n) > k } n^{-s}
```

for any fixed `s > 1`. §21 then names the proof obligation — **Hard-Zeta Decay** —
in a uniform form `Z_{k+L} ≤ q·Z_k` with `q < 1`, or a weaker cumulative form.

The bridge is correct. Confirming a logical translation is not, however, where a
verification arm earns anything, so this run went after the two things here that
are actually decidable.

---

## 1. `Z_k(s)`, measured

`Z_k(s)` appears throughout the Hard-Zeta line and has never been computed. It is
computable — as a bracket, which is the honest form:

```
Z_k^[2,N](s)  ≤  Z_k(s)  ≤  Z_k^[2,N](s) + Σ_{n>N} n^{-s},     Σ_{n>N} n^{-s} ≤ N^(1-s)/(s-1)
```

together with the **exact** lower bound `Z_k(s) ≥ (min E_k)^{-s}` — exact, not
truncated, because no `n` beyond `N` can be smaller than one already found.

Measured on `[2, 2^32)`, 4,294,967,294 values, `k = 1..160`, `s = 2, 3, 4`:

| `k` | `(min E_k)^{-2}` exact lower | measured `Z_k(2)` | upper with tail | `min E_k` |
|---|---|---|---|---|
| 1 | 1.111111e-01 | 2.337006e-01 | 2.337006e-01 | 3 |
| 2 | 1.111111e-01 | 1.588675e-01 | 1.588675e-01 | 3 |
| **3** | 1.111111e-01 | **1.588675e-01** | 1.588675e-01 | 3 |
| 4 | 2.040816e-02 | 4.273250e-02 | 4.273250e-02 | 7 |
| 8 | 1.371742e-03 | 4.201764e-03 | 4.201765e-03 | 27 |
| 58 | 1.371742e-03 | 1.376509e-03 | 1.376510e-03 | 27 |
| 59 | 2.023435e-06 | 4.750360e-06 | 4.750593e-06 | 703 |
| 96 | 9.828245e-09 | 1.751054e-08 | 1.774337e-08 | 10,087 |
| 160 | 1.368993e-11 | 7.728955e-11 | 3.101202e-10 | 270,271 |

The bracket stops being informative — tail within a factor 10 of the sum — beyond
`k = 125` at `s = 2`, and not at all before `k = 160` at `s = 3` or `s = 4`. That
depth is reported rather than hidden; it is the honest edge of the measurement.

### Why `Z_k` plateaus

`Z_k` is pinned from below by `(min E_k)^{-s}`, and `min E_k` moves only when the
current smallest hard value is finally settled. **`n = 27` holds the floor for
`k = 8..58`.** By `k = 58`, `Z_58(2) = 1.3765e-3` against `27^-2 = 1.3717e-3` — so
at that depth `E_58` is essentially the single value 27, and then 27 drops out and
`Z` falls by a factor of 290 in one step.

---

## 2. The uniform route at `L = 1` is false

Not unproven — **false**, and by an argument short enough to check by eye.

> **σ(n) = 3 is impossible for every n ≥ 2.**
>
> `n` even ⇒ `σ(n) = 1`.
> `n` odd, `(3n+1)/2` **even** ⇒ `T²(n) = (3n+1)/4 < n` for `n > 1`, so `σ(n) = 2`.
> `n` odd, `(3n+1)/2` **odd** ⇒ `T²(n) = (9n+5)/4 > n`, and then `T³(n)` is either
> `(9n+5)/8` or `(27n+19)/8`, both `> n`. So `σ(n) > 3`.

Therefore `E₂ = E₃` **as sets, exactly**, so `Z₂(s) = Z₃(s)` for every `s > 1`, so
**no `q < 1` satisfies `Z_{k+1} ≤ q·Z_k`.** The `L = 1` form of §21's uniform route
cannot hold.

That is a statement about the true infinite sums, not about the measured range.
The measurement confirms it independently — `Z₂` and `Z₃` come out bit-identical
at all three values of `s` — and the recheck also verifies the case split
pointwise on 100,000 odd `n`, so a slip in the derivation could not pass unnoticed.

### What bounds `L` in general

`Z_{k+1} = Z_k` exactly whenever `k+1` is not an **admissible stopping time** —
whenever no `u` has `2^k ≤ 3^u < 2^(k+1)`. Those `k` occur infinitely often.

On `[2, 2^32)` exactly 100 distinct stopping times occur below `k = 160`, and they
are **exactly** the arithmetically admissible ones — no admissible value missing,
no inadmissible value present. The largest gap between consecutive occurring
stopping times is **2**.

So `L = 2` is the smallest `L` this measurement does not refute. It does **not**
follow that `L = 2` works; that is a different claim and this run does not touch it.

---

## 3. A finding about the ROUTE MAP

`ROUTE_MAP_v0.1.md` states the general bridge as an unconditional iff:

> `∀x ∃k : C_k(x)  ⟺  Q_k → 0`, under "已完成的一般橋"

and does **not** carry §12's monotonicity requirement `C_k(x) ⇒ C_{k+1}(x)`. The
paper body is right; the map is a lossy summary of it.

The omitted hypothesis is load-bearing, and the recheck exhibits that rather than
asserting it: take `C_k(x)` true exactly when `k` is even. Then `∀x ∃k : C_k(x)`
holds trivially, while `Q_k` alternates between `0` and the full weight and does
not converge. Without monotonicity, `E_k` is not nested and continuity from above
does not apply.

**The Collatz instantiation is unaffected** — σ's certificate system is monotone —
so this is a defect in the summary, not in the result. It is the same shape as the
Paper 07 finding in [`RUN-003`](RUN-003-PROVENANCE-CHAIN.md): a compressed
restatement that drops a hypothesis its own body carries.

---

## 4. The version chain, counted

v0.1 → v0.1.1 → v0.1.2 (the SSSP-repaired text), measured by counting the two
forms of the chart decomposition rather than by asking whether a string appears:

| | v0.1 | v0.1.1 | v0.1.2 |
|---|---|---|---|
| unrestricted `⨆_{|w|=k} H_w` | **2** | **1** | 0 |
| restricted `⨆_{|w|=k} H̃_w` | 0 | 1 | 2 |
| definitions of `H̃_w = H_w ∩ [2,∞)` | 0 | 4 | 4 |
| "Domain Corrigendum" section | 0 | 1 | 0 |

v0.1 carried the unrestricted union **twice** — once as `E_k=` and once as
`E_k^C=`. v0.1.1 added the corrigendum and the restricted chart and fixed the
first, **but the `E_k^C` one survived a whole version**. v0.1.2 removed it and
dissolved the corrigendum heading into the body.

That is exactly what the SSSP audit claimed ("the v0.1.1 corrigendum correctly
said the domain is `n ≥ 2`, but the main body still wrote `E_k^C = ⨆ H_w`"), now
confirmed from the other end of the chain and with the count attached. The loose
v0.1.1 is also byte-identical to the SSSP package's archived HZ original.

---

## 5. Bridge to Paper 05

`E_k ⊆ { n : T^k(n) ≥ n }` — the hard set is contained in the `k`-block fallback
set of Paper 05's cylinder law, since `σ(n) > k` forces `T^k(n) ≥ n`. Measured at
`2^24` against this arm's engine, which computes the fallback side independently:

| `k` | `|E_k|` | fallback | tightness |
|---|---|---|---|
| 8 | 1,245,184 | 2,424,838 | 0.514 |
| 16 | 541,184 | 1,762,561 | 0.307 |
| 24 | 286,581 | 1,271,627 | 0.225 |

Containment holds, and it loosens with depth: at `k = 24` the cylinder law's
fallback set is over four times the size of the actual hard set, so using it as a
proxy for `E_k` gives away most of the room.

---

## The instrument

`hz_zeta_measure.rs` is deliberately a **separate implementation** from
`collatz_verify.rs`, with its own walk, so the two can disagree. They do not: the
maximum σ on `[2, 2^32)` comes out **447 at n = 2,788,008,987** from both, and the
argmax reproduces under exact Python big-integer iteration.

Summation is Kahan-compensated — the terms arrive in decreasing order, the worst
order for naive accumulation. Cross-checked against `math.fsum`, which is exactly
rounded, on `[2, 2^22)`: **worst relative disagreement 0.0**, i.e. bit-identical.

### A defect in my own measurer, and what caught it

The first version tied the walk cap to `max(ks)`. `sigma_capped` correctly returns
`cap + 1` to mean "greater than the cap" — but the accumulator then reported that
as `max_sigma`, so the run announced `max_sigma = 161` when the true value on the
range is 447. A bound was being presented as a measurement.

The engine cross-check caught it immediately, which is the entire reason that
check exists: **a quantity the tool computes alone is pinned by nothing.** The cap
is now decoupled from the `k` list, and since the walk exits on descent rather
than on the cap, a generous cap costs almost nothing.

### And a claim of mine the drill deleted

The recheck derives the admissible stopping times from exact integer powers, and
I wrote that this was necessary because a floating logarithm could move a
boundary. The drill planted exactly that substitution — and **did not catch it**,
because `int(log(3^u, 2)) + 1` agrees with `bit_length()` for every `u < 640`,
past the point where `3^u` leaves float range entirely.

So the exactness is a robustness choice, not something this measurement can
distinguish. The docstring now says that. Crediting a check with work it is not
doing is the same error as [`feedback-presence-is-not-evidence-of-a-fix`](RUN-003-PROVENANCE-CHAIN.md),
pointed at my own code.

---

## The drill

24 defects across **three** surfaces, each required to fail the check named for it:

- **the measurement** — counts rising with `k`, `Z` rising with `k`, σ = 3 made to
  occur, `Z₂` and `Z₃` separated by one ulp, `max_sigma` off by one, a reported
  minimum that is not hard at that depth, a gap of 3 between stopping times, an
  inadmissible stopping time made to occur, a sum dropped below its own exact
  floor;
- **the documents** — the monotonicity hypothesis removed from the v0.1 body, the
  ROUTE MAP given the hypothesis after all, v0.1.1's corrigendum removed, v0.1.1
  made to fix both unions, v0.1.2 made to keep one;
- **the recheck's own reasoning** — the two-case proof misstated, and the
  non-monotone counterexample made monotone so that it stops being one.

The third surface is the one that matters. Those are the only two places in this
suite where the tool reasons rather than compares.

Two null controls — an annotation where nothing reads, and an unrelated file
beside the documents — disturb nothing.

---

## What this does not establish

Nothing about Collatz.

A finite range cannot see `lim Z_k`: the truncated sum tends to 0 whether or not
the conjecture holds. That is why the tail bound travels with every number here
and why the depth at which the bracket stops being informative is stated rather
than left for a reader to discover.

What it does establish is narrower and real: `Z_k(s)` now has measured values with
rigorous two-sided bounds, and one of the two forms §21 offers for the proof
obligation is closed off.
