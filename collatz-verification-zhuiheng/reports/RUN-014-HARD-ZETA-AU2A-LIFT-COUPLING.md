# RUN-014 — Round A-U.2a: the algebra holds, and it already reaches A-U.1's countermodel

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2a_bundle.zip` (source item 32) — Round A-U.2a *Lift–Occupation Coupling: Source-Digit Transducer, Adelic Synchronization, Lift Flux and Compact Pointed No-Go*, plus `A_Line_ROUTE_MAP_v1.0`
**Tools:** [`hz_accel_code.py`](../code/hz_accel_code.py) (A-U.2a layer) · [`src16_hardzeta_au2a_recheck.py`](../code/src16_hardzeta_au2a_recheck.py) · [`src16_drill.py`](../code/src16_drill.py)
**Logs:** [`src16-au2a-recheck.json`](../data/gate-logs/src16-au2a-recheck.json) · [`src16-drill.json`](../data/gate-logs/src16-drill.json)

**Result: 28/28 checks. 30/30 planted defects caught by the check named for each — 15 in the A-U.2a layer, 10 in this run's own measurement, 5 in the documents. 2/2 null controls undisturbed.**

---

## What this round adds, and where it stops

A-U.1 left the anchor cocycle as the datum occupation theory cannot carry.
A-U.2a builds the algebra that couples it to the dynamics — and then ends in a
**second** no-go: under the compact normalized coordinates every positive-integer
anchor collapses to `(X, Z, λ) = (0,0,0)`, so the anchor value is erased again.
The repair, an unbounded anchor height `A_m = R_m`, is faithful but noncompact.

Almost all of it is exact algebra, so almost all of it is checked exactly —
integers and `Fraction`s, with no floating-point comparison anywhere in a
verdict.

**The inverse-code series.** `𝓑(q) = −Σ_j 2^{K_j}/3^{j+1}` converges 2-adically
to the exact source, and satisfies `3𝓑(q) + 1 = 2^{q_1}𝓑(σq)`. Both hold on every
prefix of eight codes to depth 24.

**The Source Block-Digit Theorem.** `t_{m+1}` read off the source's binary
expansion at positions `K_m+1 … K_{m+1}` equals the lift computed as a difference
of canonical representatives — two different derivations, same digit, everywhere
checked. And `R_m = 1 + Σ_i t_i 2^{K_{i−1}+1}` exactly.

**The amplification law.** `Ẽ_m − E_m = 2 t_{m+1} 3^m` — a single lift digit in
the source is magnified by `2·3^m` at the endpoint. Verified in exact integers,
with a guard requiring nonzero lifts to actually occur in the sample, since a law
about lifts is untested where every lift is zero.

**The pointed recurrences and the decoupling.** `X_{m+1} = 2^{−q}X_m + λ_{m+1}`
and `Z_{m+1} = (Z_m + 2t + 3^{−(m+1)})/2^q` hold in Fractions, and
`C_m = Z_m − 2X_m = B_m/(2^{K_m}3^m)` obeys `C_{m+1} = (C_m + 3^{−(m+1)})/2^q`
with the lift digit **absent**.

That the recurrence does not *mention* `t` is weaker than `C` being independent
of it, so the sharp form is checked separately: for every source in a code's
cylinder — not only the canonical one — `E/3^m − 2n/2^{K+1}` comes out the same.
The `n` terms cancel identically. That is what makes "the lift enters only `X`"
a theorem rather than a notational accident.

**The synchronization bound.** `0 < C_m ≤ 2^{−m}[1 − (2/3)^m] < 2^{−m}`, so
`Z_m = 2X_m + O(2^{−m})` — checked as the two-sided inequality it is.

**The two rival completions.** §27's negative completion
`x_− = −(2^{K_m} + B_m)/3^m` runs the same `m` valuations as the code and lands on
`−1`, the accelerated fixed point — verified by iterating the accelerated map on
exact rationals. §28's critical completion gives `K_{m+j} = ⌊β(m+j)⌋ − d_m`, still
subcritical, for every subcritical prefix tested. So each finite pointed
observation is compatible with a positive integer, a negative rational, and a
formal critical path at once, which is §29's Finite Pointed Indistinguishability.

---

## The measurement: A-U.2a's machinery already reaches A-U.1's countermodel

§26 sorts candidates into three classes by lift flux:

1. **positive lift flux** — `limsup λ̄_M > 0`;
2. **zero-density sparse leakage** — `λ̄_M → 0` but `t_m > 0` infinitely often;
3. **true anchor** — `t_m = 0` eventually.

The Zero-Flux Boundary Theorem disposes of class 1. §26 says the last two "may be
indistinguishable to ordinary compact occupation", and the abstract states the
gap outright: **lift density 0 does not give finitely many lifts.**

So: which class is the mechanical code — the countermodel that defeated A-U.1?

| `M` | `λ̄_M` | `X̄_M` | lift density |
|---|---|---|---|
| 40 | 0.331 | 0.511 | 0.725 |
| 80 | 0.338 | 0.522 | 0.713 |
| 150 | 0.328 | 0.511 | 0.687 |
| 250 | 0.336 | 0.518 | 0.692 |
| 400 | 0.338 | 0.523 | 0.673 |

**`λ̄` sits at ≈ 0.34 and does not decay — the mechanical code is in class 1.**

That is worth stating plainly: **A-U.2a's flux machinery already excludes the
object that defeated A-U.1.** The countermodel which made ordinary occupation
theory useless is *not* a witness for the class that remains open. Round A-U.2b
is named "Sparse Lift Rigidity" and its job is class 2 — and nothing in Phase II
so far exhibits an inhabitant of class 2. Whether that class is even non-empty is
the question A-U.2b should answer first; if it is empty, the gap the abstract
flags closes for free, and if it is not, the witness is the thing to look at.

This is the same route-pricing that RUN-009 applied to the endpoint-parity route:
enumerate what actually blocks the road before spending a round on it.

---

## The compact collapse, measured

For a genuine anchor `X_m = n/2^{K_m+1}`, so it falls at rate `2^{−βm}`. For the
countermodel the source keeps pace with its own modulus and `X` stays order one:

| mean `X` over `m = 30…59` | value |
|---|---|
| `n = 27` | 1.8 × 10⁻¹³ |
| `n = 35655` | 7.3 × 10⁻¹⁰ |
| mechanical code | **0.459** |

Nine to twelve orders of magnitude. So the compact coordinate **does** separate
anchors from the countermodel — and that is precisely the Compactness–Fidelity
Tradeoff: it separates them by sending *every* anchor to the same point, which is
why the anchor value `n` cannot be recovered from the limit.

One honest caveat on the pointwise values: `X_m` for the mechanical code
**oscillates** (0.87 at `m=8`, 0.44 at 16, 0.68 at 40, 0.065 at 60), so a
single-depth comparison is not a stable statement. The separation above is stated
on the mean, which is both the stable statistic and the one occupation theory is
actually about. The pointwise table is reported, not asserted on.

---

## Where the boundary term is not negligible

§18's bracket `(1/2)X̄_M ≲ λ̄_M ≲ X̄_M` holds "after the boundary term vanishes".
Measured, that caveat earns its place. For `n = 27` at `M = 59`:

```
X̄ = 0.0603      λ̄ = 0.0254      X̄/2 = 0.0301
```

so `λ̄ < X̄/2` — the lower bracket **fails** without the boundary term. The term is
`|X_M − X_0|/M ≈ 0.5/59 ≈ 0.0085`, and `X̄/2 − 0.0085 = 0.0216 ≤ 0.0254` restores
it. The reason is structural: `X_0 = 1/2` for every code while `X_M → 0` for an
anchor, so the entire boundary contribution is the initial height, decaying like
`1/M`. Asymptotically the paper is right; at any depth this arm can reach, the
bracket must be quoted with the term included.

---

## Six findings about my own checks

**A mutation that makes a check vacuous is invisible to a drill.** The decoupling
check's first defect replaced the per-source computation with the canonical one —
turning the check into "does `base` equal `base`". It passed, and the drill scored
it a miss, correctly: a drill asks *does this check fail*, and a vacuous check
passes. So this failure mode cannot be found by mutation testing at all. The only
defence is the discipline that finds it beforehand — guard that the observable is
non-trivial, which here means the cylinder must contain more than one source and
`C` must be recomputed from each. The defect was replaced by one that makes the
check genuinely fail (compare against the wrong cylinder). Worth stating because
it bounds what a 30/30 drill score means.

**A check was structurally blind to an error in `B_m`.** "The endpoint is a
positive odd integer" cannot detect a damaged affine offset, because `R_m` is
*derived* from `B_m` — the two errors propagate into `E = (3^m R_m + B_m)/2^{K_m}`
and cancel. A quantity defined to make an identity hold cannot be used to test
that identity's inputs. Fixed by adding a check that recomputes `B_m` from §9's
closed form `Σ_i 3^{m−i}2^{K_{i−1}}`, independently of `R`. That is a check the
suite was simply missing, and the drill is what exposed the gap.

**One defect belonged to a different check than I named.** Halving the source
modulus does *not* break the adelic dichotomy — `R = n mod 2^K` still equals `n`
once the modulus passes `n`, so the branch structure survives. What it destroys is
the extra digit that makes the endpoint odd. Retargeted, and the dichotomy was
given a defect that actually moves it.

**The series check found a bug in my own implementation first.** `𝓑(q)` summed
over `j < m` disagreed with the exact source by precisely `2^{K_m}`. The `j = m`
term is *not* zero modulo `2^{K_m+1}` — only from `j = m+1` on does `2^{K_j}`
vanish there, because `K_{m+1} ≥ K_m + 1`. Planted back as the drill's first
defect, since a bug made while writing a check is the best evidence that the
check can catch it.

**The flux balance telescopes over `X_0 … X_{M−1}`, not `X_1 … X_M`.** My first
version was off by one and the identity failed by a visible margin. `X_0 = 1/2`
comes from the empty prefix and is a real term. Also planted back as a defect.

**The separation was stated pointwise, where the observable oscillates.** Changed
to the mean, as above. A single-depth comparison would have been a claim the data
does not support, and it happened to pass only because `m = 60` was not one of
the countermodel's low points.

**Four no-op defects in one drill, all of the same family.** Every one loosened a
requirement the data already satisfied: a cap widened from `(2/3)^m` to `(2/4)^m`,
a two-sided bracket cut to one side, a range `lam[20:]` narrowed to `lam[20:21]`,
and the vacuous rewrite above. None can fail, because weakening a satisfied
condition leaves it satisfied. This is the sixth, seventh, eighth and ninth
instance in this arm. The rule is now unconditional: **do not mutate the
comparison, mutate what is computed.** All four were replaced accordingly — a
*halved* cap, a bracket demanding `λ̄ ≥ X̄`, a range starting where the lifts are
nonzero, and a baseline from the wrong prefix.

Every check has at least one defect naming it, and the drill now enforces that
with a coverage audit that runs **before** the mutation loop and aborts if any
check is unguarded — the procedure RUN-013 introduced, now a gate rather than a
habit.

---

## What this does not establish

Nothing on §33's unproved list: that a critical subcritical input must have
infinitely many nonzero lifts, CASP, CST, coefficient-frontier extinction,
correction-delay extinction, or Collatz. The Zero-Flux Boundary Theorem and the
sparse-lift consequence are statements about weak-\* limits and densities over
infinite orbits; what is checked here is the exact algebra underneath them and
the counting inequality of §25 on a finite window. The measurement that the
mechanical code has positive flux is a statement about one explicit code to
`M = 400`, and it says where that code sits — not that class 2 is empty.
