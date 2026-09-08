# RUN-013 — the Certificate Globalizer is faithful in ℚ and not in float64

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Phase 0's [`07_BSD_Certificate_Globalizer`](../../amral/public/bsd/phase0/files/07_BSD_Certificate_Globalizer.md) — the faithful unresolved mass `𝔅_k(s) = Σ_{i∈H_k} i^{-s}`
**Tools:** [`src14_globalizer_faithfulness.py`](../code/src14_globalizer_faithfulness.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src14-globalizer.json`](../data/gate-logs/src14-globalizer.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: all four of the document's claims hold, verified in exact rational arithmetic rather than argued. Two things follow that it does not say. The monotonicity hypothesis in its limit claim is unnecessary — `s > 1` alone gives it. And the design goal in §0, never to swallow a single uncertified curve, holds in ℚ and fails in float64 at a computable index: for `s = 3` that index is 195,684, which is inside the range this project already works in.**

---

## The object

Phase 0 §0 states the purpose exactly:

> 建立一個不會因為「大多數曲線已認證」就吞掉單一未認證曲線的研究控制量。

Given a computable enumeration of `Q`-isogeny classes and a target rung `ℓ★`,
the unresolved set after round `k` is `H_k = { i : ℓ_k(E_i) < ℓ★ }`, and

$$\mathfrak B_k(s;\ell_\star)=\sum_{i\in H_k} i^{-s},\qquad s>1.$$

## The four claims, checked in exact arithmetic

| claim | verdict |
| --- | --- |
| (1) a single uncertified class leaves positive mass | ✓ |
| (2) `𝔅 = 0 ⟺ H = ∅` | ✓ |
| (3) monotone certification cannot raise the mass | ✓ |
| (4) `𝔅_k → 0` ⟹ every fixed class eventually leaves | ✓ |

All four are computed with `Fraction`, not floats — which matters, because the
whole point of this round is that the two disagree.

## The monotonicity hypothesis is not needed

The document states (4) as

> 若 certificate system monotone，則 `lim 𝔅_k = 0` 表示每個固定 class 最終離開
> unresolved frontier。

`s > 1` makes `Σ i^{-s}` convergent, so dominated convergence delivers the
implication from pointwise departure alone. The gate exhibits a **non-monotone**
witness — `H_k` alternates between a moving head and a far singleton, so
`H_{k+1} ⊄ H_k` infinitely often — and:

| | |
| --- | --- |
| the sequence is monotone | **no** |
| every fixed class still leaves, permanently | **yes** |
| the mass still tends to zero | 1.28e−2 → 1.24e−3 → 1.25e−4 → 1.25e−5 at `k = 39, 401, 4001, 40001` |

The hypothesis is harmless, and it is doing no work.

*(That family's mass falls like `1/(2k)`, so the limit is sampled across four
decades rather than asserted at one `k`. A threshold chosen to make a slow limit
look fast would be measuring the threshold.)*

## Where the faithfulness stops

A single uncertified class at index `i` leaves mass `i^{-s}` — positive in `ℚ`,
always. But in a float64 benchmark it is added to a running total, and once
`i^{-s}` falls below the last representable bit of that total it changes nothing
at all. The benchmark then reports the same number whether that curve is resolved
or not.

| `s` | reference mass `ζ(s)` | first index whose unresolved mass is invisible |
| ---: | ---: | ---: |
| 1.1 | 10.584448 | 3.7 × 10¹³ |
| 1.5 | 2.612375 | 2.3 × 10¹⁰ |
| 2 | 1.644934 | 7.4 × 10⁷ |
| **3** | 1.202057 | **195,684** |

**The larger `s` is, the sooner the metric goes blind.** At `s = 3` a single
unresolved curve past index 195,684 is arithmetically invisible — and this
project's own enumeration already runs to 40,749 base curves out of an LMFDB
that passes conductor 500,000. On that enumeration the last curve still moves the
sum, but only just: its mass at `s = 3` is `1.48 × 10⁻¹⁴`, about fifty-four bits
below `ζ(3)`.

None of this is a defect in the definition. It is the difference between a
quantity being faithful and *a computation of it* being faithful — and §0's goal
is stated about the quantity.

## The use case the weight inverts

§5 lists what `𝔅` is meant to answer, including:

> 高 conductor 曲線是否被永久遺忘。

Two strategies, both plausible, at `s = 2`:

| | unresolved classes | `𝔅` |
| --- | ---: | ---: |
| a certified head and a forgotten tail — indices 30,000 … 40,749 | **10,750** | 8.79 × 10⁻⁶ |
| one stubborn early curve — index 7 alone | **1** | 2.04 × 10⁻² |

**`𝔅` ranks the single early failure as 2,320 times worse than the ten thousand
forgotten ones.** That is a property of the weight `i^{-s}`, not an error — it is
exactly what makes claim (1) true. But it is the opposite of what the §5 use case
needs, and the document lists both without noting that they pull apart.

A metric that never reaches zero while one curve is open, and a metric that
notices a forgotten high-conductor tail, are two different metrics. `𝔅` is the
first. §6 already splits the score by BSD component — weak, `Ш`-finiteness,
strong formula — to stop one total hiding another; the same reasoning applies to
the index weight, and is not applied.

## The drill

**51 defects, 51 caught by the check named for each. 14 controls, none
disturbed.** Gate 14's three are: the mass summed in floats instead of exact
rationals, the empty set given nonzero mass, and invisibility measured at single
precision instead of double.

## What this round does not claim

* **Nothing about BSD.** `07` says so itself, at length and correctly:
  `Certificate Globalizer ≠ Truth Oracle`, and it lists the five further things a
  proof would need. This round adds nothing to that list and subtracts nothing.
* **It does not say the definition is wrong.** All four claims hold. What is
  measured is where a *computation* of the quantity stops being faithful, and
  which of the document's own stated use cases the weight serves poorly.
* **It does not propose a replacement weight.** Choosing one is a research
  decision about what the frontier is for, not an arithmetic fact.
