# RUN-014 — the Phase 2 anchor: `r_an = 0` computed, and `L(E,1) = Ω` to the last bit

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`21_Base_BSD_Anchor_Repair`](../../amral/public/bsd/phase2/files/21_Base_BSD_Anchor_Repair.md) — the two arithmetic facts the repair moves the whole Phase 2 family theorem onto
**Tools:** [`src15_phase2_anchor.py`](../code/src15_phase2_anchor.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src15-phase2-anchor.json`](../data/gate-logs/src15-phase2-anchor.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: both facts hold. `N = 696` is selected by the functional equation over its nearest competitor by a factor of 339, without Tate's algorithm. The root number is `+1` and `L(696.e1, 1) = 1.631727740072 ≠ 0`, so `r_an = 0`. And `L(E,1)/Ω = 1.0000000000000002` — one, to within a single unit in the last place — which with trivial torsion and `c₃ = c₂₉ = 1` forces `c₂ · #Ш = 1`.**

---

## What the repair moved the weight onto

`21` records a careful correction. v0.3 argued from Banwait–Huang's historical
remark that Miller verified full BSD for **most** rank 0/1 curves below conductor
5000 — from which `696 < 5000` does not follow. The repair cites Creutz–Miller
Theorem 1.1 instead:

> `N < 5000` and `r_an ≤ 1` ⟹ full BSD.

That is the right kind of repair — it replaces an inference from "most" with a
theorem that quantifies over all. And it moves the load onto two arithmetic
facts about `696.e1`: **`N = 696`** and **`r_an = 0`**.

RUN-009 checked neither. It verified the discriminant, the reduction types and
the non-semistability, and took the conductor from the note.

## The root number is measured, not assumed — and 37a1 is why

The convenient formula

$$L(E,1)=2\sum_{n\ge1}\frac{a_n}{n}e^{-2\pi n/\sqrt N}$$

is valid **only when `w = +1`**. `37a1` shows what happens if that is forgotten:
it has rank 1, so `L(E,1) = 0` — and the same sum evaluates to `0.19`. A nonzero
sum is no evidence of a nonzero `L`-value.

So the sign is read off instead of assumed. At `s = 2` the Dirichlet series
`Σ a_n n^{−2}` converges absolutely and needs no functional equation at all,
while the smoothed formula for `Λ(2)` depends on `w`. Evaluating both signs and
keeping whichever matches determines `w` numerically:

| curve | `Σ a_n n^{−2}` | smoothed, `w = +1` | smoothed, `w = −1` | picked | known |
| --- | ---: | ---: | ---: | :-: | :-: |
| `11a1` | 0.546045816 | 0.546048036 | 0.212403460 | **+1** | +1 ✓ |
| `37a1` | 0.381578708 | 0.573749146 | 0.381575408 | **−1** | −1 ✓ |
| `389a1` | 0.360097631 | 0.360092864 | 0.430502866 | **+1** | +1 ✓ |
| **`696.e1`** | **1.068637376** | **1.068630094** | 0.942865445 | **+1** | — |

For the anchor the residual is `7.28 × 10⁻⁶` and the gap to the other sign is
`0.1258` — **seventeen thousand times larger**.

## The conductor, selected rather than assumed

That comparison closes only with the right `N`, so running it over candidate
conductors picks one out:

| `N` | residual |
| ---: | ---: |
| 174 | 2.085 × 10⁻² |
| 348 | 1.287 × 10⁻² |
| **696** | **7.283 × 10⁻⁶** |
| 1044 | 4.816 × 10⁻³ |
| 1392 | 6.446 × 10⁻³ |
| 2088 | 6.457 × 10⁻³ |
| 4176 | 2.469 × 10⁻³ |

`N = 696` wins by a factor of **339** over the runner-up. That is a verification
of the conductor by a route that never runs Tate's algorithm — the functional
equation simply does not close on a wrong one.

## The anchor

| | |
| --- | --- |
| `p = 2` | additive, `a₂ = 0` |
| `p = 3` | split multiplicative, `a₃ = +1` |
| `p = 29` | non-split multiplicative, `a₂₉ = −1` |
| root number `w` | **+1** |
| real period `Ω` | 1.631727740071569 |
| `L(E,1)` | **1.631727740071569** |
| **`r_an = 0`** | **yes** |
| `#E(Q)_tors` | **1** (gcd of `#E(F_p)` over good `p ≤ 120`) |
| `c₃ · c₂₉` | 1 |
| **`L(E,1)/Ω`** | **1.0000000000000002** |

`L(E,1)` and `Ω` agree to every digit float64 has; their ratio differs from 1 by
`2.2 × 10⁻¹⁶`, which is one unit in the last place.

## What that ratio forces

At rank 0 the strong BSD formula reads

$$\frac{L(E,1)}{\Omega}=\frac{\#Ш\cdot\prod_p c_p}{\#E(\mathbf Q)_{\rm tors}^2}.$$

With `#tors = 1` and `c₃ = c₂₉ = 1`, the measured ratio gives

$$\boxed{c_2\cdot\#Ш = 1,}$$

and both are positive integers, so `c₂ = 1` and `Ш` is trivial.

**This is a consistency reading, not an independent proof of either factor.** It
uses the BSD formula that Creutz–Miller supplies for this curve. Read the other
way — if `c₂` and `#Ш` were known independently to be 1 — the same measurement
would be a verification of strong BSD for `696.e1` to sixteen digits. The round
does not compute `c₂`: the reduction at 2 is additive and its Tamagawa number
needs Tate's algorithm, which this gate does not implement.

## Every piece validated before the anchor was touched

The gate refuses to run on `696.e1` until it reproduces three curves whose
answers are fixed outside it:

* **`11a1`** — torsion `Z/5`, `c₁₁ = 5`, `Ш` trivial, so `L/Ω` must be exactly
  `5/25 = 1/5`. Measured: `0.20000000000000004`, off by `2.8 × 10⁻¹⁷`. Real
  period `1.2692093042795534`. Torsion bound `5`.
* **`37a1`** — rank 1: `w = −1` and `L(E,1) = 0`.
* **`389a1`** — rank 2 with `w = +1`: `L(E,1) = 0` *despite* the sign being
  positive. This is the case that separates "the sum vanishes" from "the sign
  kills it", and it is the one that makes the `37a1` lesson precise rather than
  anecdotal.

## The drill, and three checks that could not see a defect

**59 defects, 59 caught by the check named for each. 14 controls, none
disturbed.**

Gate 15's eight defects include the Hecke recursion losing its `−p·a_{p^{k−1}}`
term, `L(E,1)` losing its factor of two, an inverted split/non-split test, and
`E₁` implemented without the Euler–Mascheroni constant. `E₁` is written in the
gate with no dependencies at all; **mpmath appears only in the drill**, as the
independent implementation to check it against — agreement to `2.1 × 10⁻¹⁵`
relative across nine arguments spanning `0.05` to `120`.

Three of the eight escaped on the first run, and all three for the same reason:
**the check's tolerance was looser than the quantity's precision.** Undisturbed,
`|L/Ω − 1/5|` is `2.8 × 10⁻¹⁷`; a one-step AGM shifts the real period by
`1.4 × 10⁻¹²` and an inverted split test shifts the ratio by `2.6 × 10⁻¹⁰` — both
invisible inside the `1e-9` window the first version used. The third had no
assertion on the real period for a curve with `Δ > 0` at all, so dropping the
second component of `E(R)` changed nothing it looked at.

A tolerance chosen for looking round rather than for matching the computation is
a check that cannot see a real defect. The windows are now set to the measured
precision, and the reason is written where the numbers are.

## What this round does not claim

* **Nothing about BSD in general**, and nothing about the family theorem. It
  checks the two arithmetic facts the anchor repair rests on.
* **It does not verify Creutz–Miller Theorem 1.1**, which is a published theorem
  this arm has not read. It verifies that `696.e1` satisfies its hypotheses.
* **`c₂` is not computed** — additive reduction needs Tate's algorithm. Only the
  product `c₂ · #Ш` is measured.
* **`Ш` is not computed.** That it must be trivial follows from BSD holding, not
  from anything measured here.
* **The `L`-values are floating-point.** They are reported at the precision they
  have — sixteen digits for the anchor ratio, `7.3 × 10⁻⁶` for the root-number
  residual — and no claim is made beyond it.
