# Lean queue — claims this arm cannot settle, held until the hardware is ready

**Status: DEFERRED, deliberately and on Neo.K's instruction (2026-08-14).**

Neo.K has Lean available. Everything requiring it is collected here rather than
started, because a mathlib-backed project is heavy on both CPU and disk, and the
C: drive is currently at **36.7 GiB free of 232 GiB (15.8%)**. A new drive and a
full drive reorganisation are planned first.

Nothing in this queue is blocked on knowing what to do. It is blocked on
hardware. This document exists so that when the drive arrives, the work is
already sorted, scoped and ordered, and nobody has to re-derive why each item is
here.

## Why these items and not the others

This arm's instrument is exact integer and rational arithmetic. It settles a
claim completely when the claim is **finite** — a bounded interval, a bounded
word length, a finite parameter box. It settles a `∀`-quantified claim **not at
all**; it can only instantiate it.

So the split is not "hard versus easy". It is:

| | instrument |
|---|---|
| finite domain, exact arithmetic | this arm — **done**, see `RUN-002-OT-SERIES.md` |
| `∀` over an infinite domain, but elementary | Lean, cheap — the queue's front |
| `∀` over algebraic structures integers cannot express | Lean, expensive — the queue's back |
| the conjecture itself | neither |

Six finite claim groups are already independently re-derived. Everything below is
a statement whose truth this arm has confirmed on every case it can reach and
**cannot** confirm in general.

## The queue, cheapest first

### 1. Paper 02, Theorems A–F, for all words

The best first target: small, self-contained, and needs nothing from mathlib
beyond `ℤ` and `ℚ`.

- `F_w(x) = (3^{u(w)} x + b_w) / 2^{|w|}` for **all** `w ∈ {D,U}*`
- the recurrence `b_{wD} = b_w`, `b_{wU} = 3b_w + 2^{|w|}`
- the closed form `b_w = Σ_t 2^{j_t−1} 3^{u−t}`
- the concatenation law, the matrix representation
- the order extremes `3^u − 2^u ≤ b_w ≤ 2^{k−u}(3^u − 2^u)`

All six are inductions on word length. This arm verified them exhaustively to
`k ≤ 16` (131,070 words) against a referee that assumes none of them, so the
statements are not in doubt — what Lean adds is the quantifier.

**Why start here:** if the induction formalises cleanly, every later item reuses
the same `b_w` machinery. If it does not, that is worth knowing before spending
CPU-hours on anything bigger.

### 2. Paper 07, Theorems A–D and §25, for all odd `(m, r)`

Structurally identical to item 1 with `3 → m` and `1 → r`, plus:

- `α_m = ln2/ln m` is irrational for odd `m > 1`. The paper's proof is two lines
  (`m^p = 2^q` with `m` odd is impossible) and should formalise almost trivially.
  This arm can only confirm `m^u ≠ 2^k` on a finite box, which is not the claim.

Doing this immediately after item 1 tests whether the Paper 02 development
generalises the way the paper says it does — which is Paper 07's whole thesis.

### 3. Paper 03, the local identityisation

`ψ_w ∘ T^k ∘ φ_w^{-1} = id` on each cylinder, and the word↔residue bijection
`{D,U}^k ↔ ℤ/2^kℤ` for all `k`.

Verified here pointwise on cylinders and, in the opposite direction, as a
bijection for every `k ≤ 20`. The general statement is a short argument; the
`r_w = 0` boundary that the repair ledger corrects is the one place to be careful,
and it is exactly where a formalisation would earn its keep.

### 4. Paper 06, Theorems A–C and F

The accelerated affine closure and the run-length correspondence for **all**
valuation words, and the one-step density `δ(κ = j) = 2^{−j}`.

The density claim is a counting argument over `ℤ/2^{j+1}ℤ` and should be
comfortable. Theorem D's log drift is already verified here as an exact rational
identity, so it needs no analysis in Lean either.

### 5. Paper 09, Theorems A and F — the real quantifier content

- **Theorem A:** Collatz `⟺ ∀n>1, σ(n) < ∞`. The forward direction is strong
  induction and should be short. This is the statement that makes every finite
  verification meaningful, so having it formal is worth more than its difficulty
  suggests.
- **Theorem F:** `σ(n) = ∞ ⟺ n` anchors an infinite hard branch. Needs the
  2-adic embedding and the eventual-stabilisation characterisation of an ordinary
  positive integer inside `ℤ₂`. Heavier — mathlib has `PadicInt`, so the
  ingredients exist.

This arm measured `K(2^40) = 550`, one value of the function Theorem A's
framework defines. Formalising Theorem A would not raise that bound by one; it
would make precise what the bound *is a bound on*.

### 6. Hard-Zeta — the two repaired claims

- the `n ≥ 2` stopping domain: `Ẽ_w = H_w ∩ [2,∞)`, `E_k^C = ⊔_{|w|=k} Ẽ_w`.
  **This one is partly checkable here** — that the union is a genuine disjoint
  partition of the hard set with `n = 1` excluded is a finite statement per `k`,
  and it is the natural next non-Lean task.
- the invariant-measure route, now stated conditionally on a compactification,
  tightness, and the regularity needed to pass dynamics to a weak limit.
  Formalising the *hypotheses* is the value here, not the conclusion.

### 7. Paper 08 — only the universally quantified half remains

Paper 08 walks the coefficient algebra from `ℤ` outward: general commutative
rings, zero divisors, unordered fields, matrices and noncommutative algebras,
Möbius transformations, degree `> 1` polynomial maps — asking where RCOT first
breaks.

**This entry has shrunk.** An earlier version of it wrote Paper 08 off entirely,
on the grounds that integers cannot express general rings, noncommutative algebras
or Möbius maps. That was wrong about what the paper needs. A *structural breakage
theorem* is tested by an explicit **witness** that the property fails, plus
confirmation that the properties above it survive — and both are finite. All of
that is now done: see `RUN-002-OT-SERIES.md` §8 and
`../data/gate-logs/ot-paper08-recheck.json`, which carries a concrete witness for
every rung of §43's ladder.

What genuinely remains for Lean is only the **universally quantified** half: "for
*every* commutative ring `R` and *every* ideal `I`, `[A_w] ∈ (R/I)^×` implies a
unique residue chart", and the same for the regular-multiplier and degree-growth
theorems. Those are clean statements and mathlib has the algebra for them, so this
is no longer the worst item in the queue — but it is still the one with the least
leverage, because the finite witnesses already tell a reader where each theorem
stops applying.

## Practical notes for when the drive arrives

- **Keep the toolchain off C:.** `elan` installs to `~/.elan` by default, which
  is on C: on this machine. Set `ELAN_HOME` to the new drive *before* the first
  install, and put the project's `.lake` build directory there too. A mathlib
  cache plus `.olean` artifacts runs to several GB, and a first build without the
  cache is CPU-hours rather than minutes.
- **Take the mathlib cache** (`lake exe cache get`) rather than building it.
- **This tree is already portable.** Nothing in
  `collatz-verification-zhuiheng/` hardcodes an absolute path; the one path input
  is the `COLLATZ_TREE_ROOT` environment variable, which defaults to the tree's
  own location. The archived `[3, 2^40]` chunk logs and every gate log are
  relative, so the tree survives being moved between drives without a re-run.
  `code/requirements.txt` is empty on purpose and there are no crates, so there
  is nothing to reinstall either.
- **A Lean development would be its own research tree**, not a subdirectory of
  this one — separate author, separate scope, per the repository protocol.

## What is explicitly not in this queue

- The Collatz conjecture. Neither instrument settles it, and the series says so
  in its own words.
- Anything the finite instrument already settles exactly. Formalising a claim
  this arm has verified on every case in its domain adds the quantifier, not
  confidence about the cases.
