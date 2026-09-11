# RUN-068 — the RUGZPB P4 certificate's one proof-critical computation, done a third time from scratch: mod-11 modular symbols for Γ₀(389) built here, the 389.a1 plus-eigenline found at 65 → 2 → 1, and the Kurihara number δ₃₉₇·₉₉₁ = 5 ≠ 0 at the disclosed scale — the manuscript's 6 still unreproduced, the theorem's input verified

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_RUGZPB_P2_P4_389a1_p11_v0.2`](../../../amral/public/bsd/p5/files/BSD_RUGZPB_P2_P4_389a1_p11_v0.2.md) — the P4 closure `Ш(389.a1/ℚ)[11^∞] = 0`, the second of the three P5 documents RUN-065 named
**Tools:** [`src70_kurihara_modular_symbols.py`](../code/src70_kurihara_modular_symbols.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src70-kurihara-modular-symbols.json`](../data/gate-logs/src70-kurihara-modular-symbols.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)
**Cross-line:** the Witness line's [stress-test Kurihara package](../../../amral/public/bsd/stress-test/files/kurihara/README.md), whose disclosed scale and figures this round reaches independently

**Result: the P4 document proves `Ш(389.a1/ℚ)[11^∞] = 0` from Kim's Theorem 1.8 and one exact finite fact — the mod-11 Kurihara number at `n = 397·991` is nonzero — and reports that number as `δ = 6` in a "deterministic normalization" it never discloses. The Witness line's stress-test package rebuilt the computation with a disclosed scale, `λ(1,5) = 1` in the ordering `(1,0), (1,1), …, (1,388), (0,1)`, found `δ = 5`, and recorded the manuscript's 6 as literally unreproduced. **This round is a third implementation, this line's own, sharing no code with either**: Manin symbols on `P¹(F₃₈₉)` with the `S` and `R` relations, Hecke operators by Merel's determinant-`q` matrices acting on the bottom row, the plus condition `λ(c,d) = λ(−c,d)`, a sparse elimination over `F₁₁` in three stages, and the path `{∞, a/n}` by continued fractions — every `a_q` point-counted here. **The relation matrix has rank 325 and the quotient dimension 65 = 2g + 1 with g(X₀(389)) = 32 computed from the genus formula; the Hecke conditions at 2, 3, 5 cut it to 2; the plus condition to 1; the first nonzero coordinate is index 5, exactly where the stress-test scale sits; and the eigenline has eigenvalues −5, −3, −6, 5 at 7, 13, 17, 19, as point counting says it must — the check that the operators are right.** Then, over all 392,040 = φ(n) units: **`δ = 5 (mod 11)` at `λ(1,5) = 1`, with integer raw product sum 43,605,160 — the stress-test package's figure to the unit, which means every one of the 392,040 terms agrees.** Beyond δ, the whole of `θ̄_n` modulo `I³` was computed: its constant, `X`, `Y`, `X²` and `Y²` coefficients all vanish and its `XY` coefficient is 5 — so `ord_I(θ̄_n) = 2` and `θ̄_n ≡ 5·X₃₉₇X₉₉₁ (mod I³)`, which is P5 v1.1 §1's `6·X₃₉₇X₉₉₁` at the disclosed scale, the figure RUN-067 left for this round. The rank-1 Kurihara numbers at 397 alone and 991 alone are 0, as Kim's theorem requires when the Selmer corank is 2. The manuscript's 6 is a different, undisclosed scale, and stays what the stress-test line said it is: not reproduced. **What the theorem needs — nonvanishing — is now verified three ways, and the P4 closure rests on it plus Kim's theorem plus rank 2 plus trivial torsion, none of which this round assumes.**

---

## What the document rests on

§5's proof: `ν(393427) = 2` and `δ̃₃₉₃₄₂₇ ≠ 0` give `ord(δ̃) ≤ 2`; Kim's
Theorem 1.8 gives `cork Sel = ord(δ̃)`; rank 2 gives `cork ≥ 2`; so
`ord = cork = 2`, the divisible part is everything, and `Ш[11^∞] = 0`. The
theorem is external; rank 2 and trivial torsion are curve data; **the one
thing the package computes is `δ ≠ 0`**, and it is the one thing this round
recomputes.

## The modular symbols, built here

| stage | this round | the document | the stress-test package |
| --- | ---: | ---: | ---: |
| generators (`P¹(F₃₈₉)`) | 390 | 390 | 390 |
| relation rows | 780 | — | 780 |
| relation rank | **325** | 325 | 325 |
| quotient dimension | **65** = 2·32 + 1 | 65 | 65 |
| after `T₂, T₃, T₅` with `a_q = −2, −2, −3` | **2** | 2 | 2 |
| after plus | **1** | 1 | 1 |
| first nonzero coordinate | **index 5** | — | index 5 |
| eigenvalues at 7, 13, 17, 19 | **−5, −3, −6, 5** | −5, −3, −6, 5 | −5, −3, −6, 5 |

The genus is not read: `g(X₀(389)) = 1 + 390/12 − ε₂/4 − ε₃/3 − 1` with
`ε₂ = 2` (`389 ≡ 1 mod 4`) and `ε₃ = 0` (`389 ≡ 2 mod 3`) gives 32, and
`2g + (cusps − 1) = 65` is what the elimination found. The Hecke action is
Merel's: `T_q m(c,d) = Σ m((c,d)·h)` over `h = [[a,b],[c',d']]` with
`ad − bc = q`, `a > b ≥ 0`, `d > c ≥ 0` — 4, 7, 15, 25, 63, 93, 109 matrices
at 2, 3, 5, 7, 13, 17, 19. That the eigenline isolated by three primes then
has the point-counted eigenvalue at four more is the check that this
convention, and the row-vector action, are right; a transposed action does
not pass it.

## The sum

| | this round | stress-test package | manuscript |
| --- | ---: | ---: | ---: |
| terms | 392,040 = φ(n) | 392,040 | — |
| `δ_n^(λ)` at `λ(1,5) = 1` | **5** | 5 | — |
| integer raw product sum | **43,605,160** | 43,605,160 | — |
| `δ` in the manuscript's scale | — | — | 6 |

The raw sum agreeing to the integer is the strong statement: it is
`Σ λ({∞,a/n})·log₅(a)·log₆(a)` with every factor a representative in
`0…10`, so it agrees only if the eigenline, the path convention, and both
logarithm tables agree term by term. Three implementations — the package's
producer (NumPy, cusp-path Hecke), its verifier (sparse elimination, Farey
parents, Merel), and this gate (sparse elimination, continued fractions,
Merel) — reach the same 392,040 terms.

## `θ̄_n` modulo `I³`, whole

Writing `σ_a = (1+X)^{i_a}(1+Y)^{j_a}` with `i_a = log₅(a mod 397)` and
`j_a = log₆(a mod 991)` reduced mod 11, `θ̄_n = Σ_a [a/n]^+ σ_a` has, modulo
`I³`, six coefficients:

| coefficient | sum | value |
| --- | --- | ---: |
| 1 | `Σ λ_a` | **0** |
| `X` | `Σ λ_a i_a` | **0** |
| `Y` | `Σ λ_a j_a` | **0** |
| `X²` | `Σ λ_a·i_a(i_a−1)/2` | **0** |
| `Y²` | `Σ λ_a·j_a(j_a−1)/2` | **0** |
| `XY` | `Σ λ_a i_a j_a` | **5** |

So `ord_I(θ̄_n) = 2` and `[θ̄_n]₂ = 5·X₃₉₇X₉₉₁` — P5 v1.1 §1's statement
with 5 in place of its 6, the two scales differing by the unit the document
does not disclose. The `X²` and `Y²` coefficients vanishing is what the norm
relations predict at Kolyvagin primes with `a_ℓ ≡ ℓ + 1 (mod 11)`; the
constant term vanishing is `L(E,1) = 0`; the linear terms vanishing are the
rank-1 Kurihara numbers, computed separately at level 397 and at level 991
and both **0** — Kim's theorem says exactly this when the corank is 2.

## The document's other figures

| the document says | here |
| --- | --- |
| `a₂ = −2, a₃ = −2, a₅ = −3` | point-counted, same |
| `a₃₉₇ = 24, a₉₉₁ = −53`; both `≡ 1 (mod 11)`; `a_ℓ − ℓ − 1 ≡ 0` | RUN-067, same |
| primitive roots 5 mod 397 and 6 mod 991 | verified: orbits of length 396 and 990 |
| `a₁₁ = −4`, good ordinary | RUN-011, RUN-067 |
| Tamagawa product 1, trivial torsion | `v₃₈₉(Δ) = 1`; gcd of point counts 1 (RUN-011) |
| rank 2, Manin constant 1, maximal mod-`ℓ` image | external; the mod-11 image is certified at RUN-069 |
| `δ = 6` | **not reproduced** — 5 at the only disclosed scale; the invariant `δ ≠ 0` holds |

## A symmetry the drill found

One planted defect refused to go red: the path written with `(−1)^i` in place
of `(−1)^{i−1}`, so that every symbol `m(q_i, s·q_{i−1})` becomes
`m(q_i, −s·q_{i−1})`. It cannot be caught, and the reason is a fact about the
functional rather than a gap in the check: `(−c : d) = (c : −d)` projectively,
so a functional with `λ(c,d) = λ(−c,d)` is also even in `d`, and the plus part
of `{∞, a/n}` does not see the sign of the second coordinate at all. The minus
part would; the Kurihara number is built from the plus part. The perturbation
is recorded as a control — a convention the answer is invariant under — and
the check that "caught" nothing was right not to.

## The drill

**294 defects, 294 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 60 controls undisturbed, over 97 checks.

The 4 planted for this gate, each turning `kurihara-modular-symbols` red and the checks listed:

| planted defect | went red |
| --- | --- |
| Merel's matrices act on the column instead of the bottom row — the transposed Hecke action | `kurihara-modular-symbols` |
| the plus condition is taken as Stein's star, lambda(c,d) = -lambda(-c,d) | `kurihara-modular-symbols` |
| the primitive root mod 991 is taken as 7 in place of 6, scaling the logarithms by 7 | `kurihara-modular-symbols` |
| multiples of 397 are not skipped, so the sum runs over more than phi(n) terms | `kurihara-modular-symbols`, `determinantal-bockstein` |


## What this round does not claim

* **Kim's Theorem 1.8 is not checked.** It is the external input; this round
  verifies what the document feeds it.
* **The manuscript's 6 is not called wrong.** A different normalization of a
  one-dimensional eigenline is a unit away; the document never wrote its
  normalization down, so 6 is unreproducible rather than false.
* **No Néron scale.** `λ(1,5) = 1` is a disclosed convention, not the canonical
  modular symbol; the bridge from this `δ` to Kim's canonical one is §4's
  argument, a theorem step, which this round reads and does not compute.
* **Rank 2 is taken from the curve's record.** RUN-023 verified the rank-2
  identity with the generators `P, Q`; a descent proving `rank = 2` is not in
  this tree.
* **Nothing about `BSD(E, 11)` in the leading-coefficient sense**, which the
  document itself excludes; `P5` and `P6` stay `OPEN`.
