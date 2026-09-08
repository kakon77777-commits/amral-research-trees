# RUN-007 — the 5- and 7-isogeny gap closed, and both directions decided for the first time

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the `has_isogeny_5` and `has_isogeny_7` columns of the Banwait–Huang census's removal evidence — the gap RUN-006 declared, plus a re-derivation of RUN-006's own column by an unrelated route
**Tools:** [`src07_isogeny_reducibility_sieve.py`](../code/src07_isogeny_reducibility_sieve.py), [`src08_modular_curve_confirmation.py`](../code/src08_modular_curve_confirmation.py)
**Logs:** [`src07-isogeny-reducibility.json`](../data/gate-logs/src07-isogeny-reducibility.json), [`src08-modular-curve.json`](../data/gate-logs/src08-modular-curve.json)

**Result: all 12,186 isogeny determinations — 4,062 curves × three primes — recomputed independently and decided, with zero disagreements, zero undecided and zero carve-outs. The census's 3-, 5- and 7-isogeny columns are correct on every curve. The 3-column is now settled twice, by two methods sharing no arithmetic. What made this possible was abandoning a method that could only refute.**

---

## Closing a gap this arm declared

RUN-006 verified the 3-isogeny column exactly and named what it had not done:

> **The 5- and 7-isogeny columns are still unverified** — 115 and 7 curves.
> ψ₅ and ψ₇ are degree 12 and 24, and the same three-method approach should
> reach them, but it has not been run.

That expectation was wrong, and finding out *why* is the first result of this round.

## Why RUN-006's method does not generalise

For `n = 3` a Galois-stable subgroup is `{O, P, −P}`, determined by the single
value `x(P)`. Stability is therefore exactly `x(P) ∈ Q`, and the question
collapses to a **rational root** of `ψ₃`.

For `n = 5` the subgroup `{O, ±P, ±2P}` has four non-zero points but **two**
distinct x-coordinates, `x(P)` and `x(2P)`. Galois need only preserve the *set*.
So a rational 5-isogeny is a degree-2 **rational factor** of `ψ₅`, not a rational
root — and for `n = 7`, a degree-3 factor of `ψ₇`. Root-finding does not reach a
factorisation problem. RUN-006's method is special to `n = 3`, and saying "the
same approach should reach them" was an assumption, not a plan.

## Part one — a sieve that refutes, and admits it cannot confirm

A rational `n`-isogeny makes the mod-`n` Galois representation reducible, hence
conjugate to upper-triangular. Then for every prime `p` of good reduction with
`p ≠ n`, the characteristic polynomial of Frobenius `x² − a_p x + p` has a root
mod `n` — that is, **`a_p² − 4p` is a square mod `n`**. Contrapositive:

> some good `p` with `a_p² − 4p` a non-residue mod `n` ⟹ **no** rational `n`-isogeny.

`a_p = p + 1 − #E(F_p)`, with `#E(F_p)` from Legendre symbols rather than by
counting pairs: each `x` contributes `1 + χ(d)` for `d = (a₁x+a₃)² + 4(x³+a₂x²+a₄x+a₆)`.
That is `O(p)` per prime instead of `O(p²)`, and exact.

Over 28 primes up to 113:

| | package says `True` | refuted by a prime | contradicting the package | left unresolved |
| --- | ---: | ---: | ---: | ---: |
| **n = 3** | 1,233 | 2,829 | **0** | 1,233 |
| **n = 5** | 115 | 3,947 | **0** | 115 |
| **n = 7** | 7 | 4,055 | **0** | 7 |

The refutation set is *exactly* the package's `False` set for all three primes —
not one curve misplaced — and the `n = 3` run, checked against RUN-006's exact
answer, produced **zero violations**.

Most refutations come cheap: the first prime tried settles the majority
(`p = 5` refutes 1,285 of the `n = 3` cases, `p = 7` refutes 1,830 of the `n = 5`
cases), and no witness beyond `p = 67` was ever needed.

**And this is still not verification.** A sieve of this shape is one-sided by
construction: passing at every prime tested is not evidence of an isogeny, only
an absence of counter-evidence. The 1,233 / 115 / 7 curves are reported
`unresolved`, not `agree`. That is the same discipline RUN-006 applied when its
first version reported 1,233 curves unresolved rather than counting a sieve pass
as agreement — and here it left the *entire* positive claim untouched.

## Part two — X₀(n), and a method that decides

A quadratic twist carries a curve's rational subgroups with it: a subgroup stable
under `ρ` is stable under `χ_d·ρ`, because `−1` preserves every subgroup. So
**whether `E/Q` has a rational `n`-isogeny depends only on `j(E)`** — and `j`
determines `E` up to quadratic twist exactly when `j ≠ 0, 1728`.

`X₀(3)`, `X₀(5)` and `X₀(7)` have genus 0 with a rational point, so each admits a
rational parametrisation of the `j`-line:

$$j = \frac{(t+27)(t+3)^3}{t}, \qquad j = \frac{(t^2+250t+3125)^3}{t^5}, \qquad j = \frac{(t^2+13t+49)(t^2+245t+2401)^3}{t^7}.$$

Hence **`E` has a rational `n`-isogeny ⟺ `j(E) = f_n(t)` for some rational `t ≠ 0`**.
This decides *both* directions. It is the first method in this line that does.

### Why a 35-digit denominator is searchable

`j`'s denominator in this population reaches **35 digits** (min 3, median 10), so
the naive rational-root route — factor the denominator, enumerate divisor pairs —
is the same wall RUN-006 hit at 26 digits, now worse. The structure of `X₀(n)`
removes it.

Write `f_n = N(t)/tᵐ` with `N` monic of degree `d`, and `D = d − m`. In all three
cases `N(0)` is a **pure power of `n`** — `729 = 3⁶`, `3125³ = 5¹⁵`, `49·2401³ = 7¹⁴`.
That is the cusp structure, not a coincidence. Put `t = u/v` in lowest terms:

$$j = \frac{A}{v^{D}u^{m}}, \qquad A = \sum_i c_i u^i v^{d-i}.$$

Then `A ≡ u^d (mod v)` gives `gcd(A, v) = 1`, and `A ≡ c₀v^d (mod u)` gives that
every prime of `gcd(A, u)` divides `n`. Feeding both back through `j = num/den`
in lowest terms:

$$\mathbf{den} = v^{D}\cdot|u'|^{m}\cdot n^{w}, \qquad u' = \text{the } n\text{-free part of } u.$$

So the `n`-free part of the denominator factors as `v'^D·|u'|^m` **and nothing
else**. For `n = 5` that means `|u'| ≤ den^{1/5}` — about `10⁷` even at 35 digits —
and for `n = 7`, `|u'| ≤ den^{1/7}`. The only remaining freedom is a power of `n`,
and the archimedean size of `j` bounds it to a range of a few dozen. Every test is
an integer identity: `den·Σ cᵢUⁱV^{d−i} = num·Uᵐ·V^D`.

### The gate validates itself before it is allowed to run

A method that has not reproduced a known answer is not evidence. `self_check()`
runs six curves whose isogeny structure is known independently of this package —
and **exits rather than report** if any comes out wrong:

| curve | `n` | expected | `t` found |
| --- | ---: | --- | --- |
| `11a1` | 5 | yes, two 5-isogenies | `−11`, `−1375` |
| `49a1` | 7 | yes (and `j` an integer, so `den = 1`) | `−7` |
| `26b1` | 7 | yes | `−98/13` |
| `14a1` | 3 | yes | `−729/28`, `−64/7` |
| `26a1` | 3 | yes | `−729/26`, `−8/13` |
| `37a1` | 3, 5, 7 | **no**, trivial isogeny class | — |

18 of 18 reproduced, including every negative. `11a1` returning exactly two
values of `t` is the sharpest of these: the count, not just the existence, matches.

### The result

| | package `True` | confirmed `True` | confirmed `False` | **disagrees** | undecided | set aside |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **n = 3** | 1,233 | 1,233 | 2,829 | **0** | 0 | 0 |
| **n = 5** | 115 | 115 | 3,947 | **0** | 0 | 0 |
| **n = 7** | 7 | 7 | 4,055 | **0** | 0 | 0 |

Every one of the 4,062 denominators factored; none of the 12,186 searches was
cut. Sample witnesses: `38b1` has a 5-isogeny at `t = −250/19`, `1230k1` a
7-isogeny at `t = −1470/41`.

## The carve-out was measured, not assumed

`j = 0` and `j = 1728` are excluded by the argument above — those curves have
extra automorphisms, so `j` determines them up to sextic and quartic twist rather
than quadratic. The gate sets them aside rather than answering them.

It set aside **zero** curves. That number is only worth anything with the second
half of the measurement: the branch is reachable — `27a1` and `32a1` trigger it —
and the census genuinely contains no curve with `j = 0` or `j = 1728`. (It
contains no curve with integral `j` at all.) A vacuous carve-out reported as a
pass would have been a claim about nothing.

## Two independent methods on the same column

`n = 3` was run here **as a control, not for its own sake**. RUN-006 decided all
4,062 by rational roots of `ψ₃`; this gate decided all 4,062 by rational points on
`X₀(3)`. The two share no arithmetic — one factors `b₈` and scans a monic
quartic, the other exploits the cusp structure of a modular curve — and they
agree with the package and with each other on every curve.

Had they disagreed, **the disagreement would have been the finding, ahead of
either verdict**. That is the lesson RUN-006 paid for: a gate reported
`EXACT_DISAGREES` on `183430x1` because a constant was mistyped, on a curve whose
answer had been established by hand minutes earlier.

## What this round does not claim

* **Nothing about BSD.**
* **It does not check the curves the census kept.** 36,687 base curves carry no
  isogeny column, so nothing here tests them — and an error in that direction is
  the one the census's own `algorithm1_all_removed_explained` check can never
  see: a missed isogeny wrongly *keeps* a curve, and a keep leaves no evidence to
  audit. The method built here is complete and applies to them unchanged. Named
  as the next gap, not passed over.
* **It does not verify that removing curves with a 3/5/7-isogeny is the right
  criterion.** It verifies the census applied its stated criterion correctly.
* **The sieve of part one remains one-sided** and is reported that way. Its value
  is that it refuted 10,831 of the 12,186 determinations cheaply and by an
  argument independent of part two, and disagreed with neither.
