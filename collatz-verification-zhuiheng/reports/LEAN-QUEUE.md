# Lean queue — claims this arm cannot settle by finite computation

**Status: ACTIVE from 2026-08-16.** Neo.K released the hardware constraint —
C: is back to 262 GiB free, D: to 332 GiB, and compute is no longer a limit. The
development lives at `D:\Ai\work together\lean\collatz\`, classified by
subject from the start rather than sorted later, on Neo.K's instruction.

Toolchain: `elan`, Lean `v4.33.0`, mathlib pinned to the matching tag, cache
taken rather than built. `.lake` is 7.3 GiB and sits on D:.

| queue item | state |
|---|---|
| §6b — the finite-local no-go | **DONE 2026-08-16**, `Collatz/AllOnes.lean` |
| 1 — Paper 02, Theorems A–F for all words | **DONE 2026-08-16**, `Collatz/AffineAtlas.lean` |
| 2 — Paper 07, generalised `mx+r` and §25 | **DONE 2026-08-16**, `Collatz/Generalized.lean` |
| 3 — Paper 03, residue cylinders | **DONE 2026-08-16**, `Collatz/ResidueCylinder.lean` |
| everything else below | open, in the order given |

**Published:** https://github.com/kakon77777-commits/collatz-lean (Apache-2.0),
with CI running the build, the axiom audit, the audit's own drill, and the
cross-check against this tree on every push.

**What "done" means here.** Seven theorems, no `sorry`, `#print axioms` showing
only `propext` / `Classical.choice` / `Quot.sound` — and two things beyond that,
because a compiling proof is a proof *about the definitions in the file*:

- `Collatz/Audit.lean` evaluates a start whose occupancy is **positive**
  (`n = 27` gives `[1,2,1,1,1,1,2,2,1,2]`). Without it the no-go would be a
  statement about a quantity that cannot be positive.
- `gate/crosscheck_against_finite_arm.py` confronts `Collatz.orbit` and
  `Collatz.kappa` with this tree's `hz_accel_code.accel_code` and
  `orbit_endpoints` — written from Round 03-A.1's prose, never from the Lean.
  6 starts, 83 exponent values and 83 orbit values, elementwise, 0
  disagreements, with a disagreement control so the comparison can fail.

Two choices made the proof short enough to be worth reading. The subcriticality
condition `K_j < j log₂ 3` is stated as the **integer** statement
`2 ^ K_j < 3 ^ j`, so no real numbers appear anywhere; and the orbit invariant is
stated as `Y i + 1 = 3^i · 2^(m+1-i)` rather than `Y i = … − 1`, which keeps
natural subtraction out of the induction entirely.

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

### 1. Paper 02, Theorems A–F, for all words — DONE 2026-08-16

`Collatz/AffineAtlas.lean`. All six, plus §14's order defect as an exact
identity and a sharpness result showing Theorem F's bounds are attained.

**The queue's own reason for putting this first held.** The `b_w` machinery is
now available to every later item, and the induction was clean — the whole file
is elementary, with `ℚ` used only for Theorem A's statement.

Two things the finite arm's exhaustive check to `k ≤ 16` could not have told me,
because both are about how the statement is *written* rather than whether it is
true:

- **Theorem E multiplies in the opposite order to reading.** A word runs left to
  right, so `F_w = σ_k ∘ ⋯ ∘ σ₁` and hence `M_{wv} = M_v · M_w`. §16 says this;
  the tidier-looking statement would have been false.
- **`b_w` should be defined by the recursion `List` recurses on** (cons), with
  the paper's right-append recurrence proved as a corollary of Theorem D.
  Defining it the paper's way would have buried Theorem A under list-reversal
  lemmas.

The cross-check for this item is **exhaustive**: every word of length ≤ 10,
2,047 of them, `u(w)` and `b_w` against this tree's `compose_affine`, with Lean
emitting each word's encoding so the comparison does not rest on both sides
enumerating in the same order.

The original entry, kept because its reasoning is what made it first:

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

### 2. Paper 07, Theorems A–D and §25, for all odd `(m, r)` — DONE 2026-08-16

`Collatz/Generalized.lean`. **The queue's stated reason for doing this
immediately after item 1 was to test whether the Paper 02 development
generalises the way Paper 07 says it does. It does, and the test is a
theorem.** §6's "`(m,r) = (3,1)` immediately recovers Paper 02" is
`bG_three_one` / `FG_three_one`, with the two developments defined
independently — neither definition mentions the other.

Also proved: §2's odd-branch integrality (so no admissibility hypothesis is
needed to keep `U_{m,r}` integral), the concatenation law and recurrence, the
closed form, and §33's "`r` only changes the finite geometry" as the exact
statement `b^{(m,r)}_w = r · b^{(m,1)}_w`.

**§25 was the first place in the queue where real numbers were unavoidable, and
it turned out to need almost no analysis.** The content is the integer statement
that an odd power is never a power of two (`odd_pow_ne_two_pow`), proved first
and standing alone; `Irrational (Real.logb m 2)` is derived from it in a dozen
lines. Later items with a `log` threshold should be read the same way — find the
integer statement underneath before importing analysis.

Cross-checked at 3,066 comparisons against this tree's `compose(word, m, r)`
over six parameter pairs, including `m = 1` (§19 says that case needs separate
understanding) and `r = 7`, because a parameter that only ever appears as `1`
is not being tested.

The original entry:

Structurally identical to item 1 with `3 → m` and `1 → r`, plus:

- `α_m = ln2/ln m` is irrational for odd `m > 1`. The paper's proof is two lines
  (`m^p = 2^q` with `m` odd is impossible) and should formalise almost trivially.
  This arm can only confirm `m^u ≠ 2^k` on a finite box, which is not the claim.

Doing this immediately after item 1 tests whether the Paper 02 development
generalises the way the paper says it does — which is Paper 07's whole thesis.

### 3. Paper 03, the local identityisation — the bijection DONE 2026-08-16

`Collatz/ResidueCylinder.lean`. The word↔residue correspondence is done:
`parityWord_eq_iff_modEq` (two integers follow the same length-`k` word iff they
are congruent mod `2^k`), with injectivity and the count. Plus `iterate_eq_F`,
the bridge from the `ℕ` dynamics to Paper 02's `ℚ` algebra — no admissibility
hypothesis needed, because the word is read off `n` itself — and
`cylinder_congruence`, which is what makes Theorem C's `r_w ≡ −b_w·3^{−u}` well
posed.

**The queue said the `r_w = 0` boundary was where a formalisation would earn its
keep, and it did.** `AUDIT_AND_CORRECTIONS.md` records that the original
induction used `r_w ∈ Ω_w`, which has no witness for the all-`D` cylinder since
its canonical residue is `0` and the domain is the *positive* integers. The
repair is `cylinder_has_positive_member`, and Lean forced it to be stated for
**every** cylinder rather than patched onto the one that breaks.

**One trap that was mine, not the paper's.** Periodicity is *not*
`parityWord (n + 2^k) k = parityWord n k` proved by naive induction: the `U`
branch sends `n + c·2^k ↦ T n + 3c·2^{k−1}`, so the multiplier is multiplied by
3, and an induction hypothesis fixed at `c = 1` cannot be applied to its own
successor. Quantifying over all odd `c` closes it; the `c = 1` form is then a
corollary. **Worth remembering for any later periodicity claim in this series.**

Still open from this item: the charts `φ_w, ψ_w` themselves and §16's
`ψ_w ∘ T^k ∘ φ_w^{-1} = id`, plus §18's exact recovery. The congruence and the
transport identity are the inputs to both, so they are now in place.

The original entry:

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

### 6b. Hard-Zeta A line — CASP and its two escape hatches (added 2026-08-15)

Round 03-A.5 closes the A-line reduction onto a single `∀`-statement, so it lands
here by definition. From `RUN-012`:

- **CASP — Critical Anchored Spine Exclusion.** *No positive integer generates an
  infinite self-generated valuation spine satisfying `K_m < m log₂3` at every
  prefix.* This is the whole remaining A line. This arm can only exhibit spines
  that die: the longest measured is `n = 35655` at 84 steps. Instantiation is not
  evidence, and the report says so.
- **The finite-local no-go, §5–§6. — DONE 2026-08-16.** *There is no positive
  `g(m)` with `N_{≥2}(m) ≥ g(m)` for every positive start.* Formalised as
  `Collatz.finite_local_no_go` and `Collatz.arbitrarily_long_zero_occupancy` in
  `lean/collatz/Collatz/AllOnes.lean`. It was picked first for the reason given
  when it was queued — it is the **cheapest** item and needs nothing beyond `ℕ`
  and `v₂`, and it is a statement about *proof methods*, so it retires a whole
  strategy class rather than settling one number. The witness family
  `2^{m+1} − 1` was verified here to `m = 40`; the Lean adds `∀ m`.
  A sharpness statement the finite arm had not recorded is proved alongside it
  (`Collatz.kappa_at_m_ge_two`): the run of ones ends **exactly** at `m`, since
  `3·Y_m + 1 = 2(3^{m+1} − 1)` and `3^{m+1} − 1` is even. So the witness realizes
  the length-`m` all-one code and no longer — sharp, not merely sufficient.
- **The occupancy/tail dichotomy, §24–§26.** Regime L is invisible to this
  instrument by construction — every finite spine has bounded valuation, so
  `L_R ≡ 0` above it. Formalising the *dichotomy* (that a saturating subsequence
  must fall into U or L) is elementary; excluding either regime is not.
- **Not to be formalised from this tree:** the López–Stoll input that A.5 §14
  leans on. It is an unrefereed preprint, and its statement — verified verbatim
  in the abstract, see `data/external/` — should be taken as a *hypothesis* in any
  formal development, exactly as the subject's own bibliography instructs.

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

## Practical notes, now that the drive is here

- **The toolchain is on C: and that is now fine.** `~/.elan` is 13 GiB with four
  toolchains already installed, against 262 GiB free — so the earlier plan to
  relocate it is moot. What did matter is the `.lake` build tree: 7.3 GiB, and it
  sits with the project on D:.
- **Taking the cache is not optional.** 8,690 files, about twenty seconds to
  build afterwards. Building mathlib instead is CPU-hours.
- **Take the mathlib cache** (`lake exe cache get`) rather than building it.
- **This tree is already portable.** Nothing in
  `collatz-verification-zhuiheng/` hardcodes an absolute path; the one path input
  is the `COLLATZ_TREE_ROOT` environment variable, which defaults to the tree's
  own location. The archived `[3, 2^40]` chunk logs and every gate log are
  relative, so the tree survives being moved between drives without a re-run.
  `code/requirements.txt` is empty on purpose and there are no crates, so there
  is nothing to reinstall either.
- **The Lean development is its own tree**, at `D:\Ai\work together\lean\collatz\`
  — separate author, separate scope, per the repository protocol, and classified
  by subject from the start on Neo.K's instruction (2026-08-16) so that later
  subjects get sibling directories rather than a sort-out.
- **Cross-check every development against this arm.** A Lean theorem is a theorem
  about the definitions in the Lean file. `gate/crosscheck_against_finite_arm.py`
  is the pattern: confront the formal definitions with the Python ones written
  independently from the same prose, elementwise, with a control that makes the
  comparison able to fail.

## What is explicitly not in this queue

- The Collatz conjecture. Neither instrument settles it, and the series says so
  in its own words.
- Anything the finite instrument already settles exactly. Formalising a claim
  this arm has verified on every case in its domain adds the quantifier, not
  confidence about the cases.
