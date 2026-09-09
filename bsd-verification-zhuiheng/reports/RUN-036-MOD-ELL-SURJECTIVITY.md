# RUN-036 — "mod-ℓ images maximal for all ℓ", certified for 38 primes and blocked twice at 3

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the sentence [`24_Manin_Period_Audit`](../../../amral/public/bsd/phase2/files/24_Manin_Period_Audit.md) rests its optimality argument on — *base `696.e1` mod-`ℓ` images maximal for all `ℓ`* — asserted in one line and computed nowhere
**Tools:** [`src38_mod_ell_surjectivity.py`](../code/src38_mod_ell_surjectivity.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src38-mod-ell-surjectivity.json`](../data/gate-logs/src38-mod-ell-surjectivity.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `ρ̄_ℓ` is certified surjective for `ℓ = 2` and for every prime `5 ≤ ℓ ≤ 167` — **38 in all**, each by explicitly refuting all six ways a subgroup with surjective determinant can be proper: Borel, the normaliser of a split Cartan, the normaliser of a nonsplit Cartan, and projective image `A₄`, `S₄`, `A₅`. Every refutation is one Frobenius, named in the log. **Eleven of Mazur's twelve degrees are covered** — 2, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163 — which strictly extends RUN-031, where the same twelve were closed only for *reducibility*, one of the six classes. `ℓ = 3` is **not** certified, and for two structural reasons rather than a short search: `PGL₂(F₃) ≅ S₄`, so "projective image `S₄`" *is* surjectivity and cannot be refuted; and the nonsplit-Cartan test is **vacuous mod 3**, proved by exhausting all four residue cases. The other four classes are refuted there, so `ℓ = 3` is reported partially certified and never counted.**

---

## What RUN-031 closed, and what it did not

RUN-031 refuted a rational `n`-isogeny at each of Mazur's twelve degrees, which
is exactly the statement that `ρ̄_n` is **irreducible**. Irreducibility is one of
the ways a subgroup can fail to be everything. For `H ≤ GL₂(F_ℓ)` with
`det H = F_ℓ^×` — and `det ρ̄_ℓ` is the cyclotomic character, which is surjective
— proper means contained in a Borel, in the normaliser of a split Cartan, in the
normaliser of a nonsplit Cartan, or having projective image `A₄`, `S₄` or `A₅`.

`24_Manin_Period_Audit` asserts maximality directly, and its optimality argument
uses it. So the other five classes are load-bearing and had never been touched.

## Each class dies to one Frobenius

Every one of them is a statement about **every** Frobenius, so one good prime
`ℓ'` refutes it. Writing `a = a_{ℓ'}(E)`:

| class | refuted by one `ℓ'` with |
| --- | --- |
| Borel | `a² − 4ℓ'` a non-residue mod `ℓ` |
| `N(split Cartan)` | `a ≢ 0` and `a² − 4ℓ'` a non-residue |
| `N(nonsplit Cartan)` | `a ≢ 0` and `a² − 4ℓ'` a nonzero residue |
| projective `A₄` / `S₄` / `A₅` | the projective order of `Frob_{ℓ'}` outside `{1,2,3}` / `{1,2,3,4}` / `{1,2,3,5}` |

The projective order is read off `u = a²/ℓ' mod ℓ`: `u = 4 → 1`, `u = 0 → 2`,
`u = 1 → 3`, `u = 2 → 4`, `u² − 5u + 5 ≡ 0 → 5`, anything else greater than 5.

Over 106 good primes below 600, all six fall for every `ℓ` from 5 to 167. The
witnesses are small — usually `ℓ' = 5, 7, 11, 13` — and each is recorded with its
trace and its residue in the log rather than summarised.

## `ℓ = 2` is a different computation

`GL₂(F₂) ≅ S₃`, and the image is all of `S₃` exactly when the 2-division cubic is
irreducible with non-square discriminant. Computed here from the `b`-invariants:
the monic cubic is `x³ + 4x² + 128x − 1024`, it has **no rational root**, and its
discriminant is `−45,613,056`, which is negative and so not a square (tested with
an integer square root, not a float one). Surjective.

Its **squarefree part is `−174`** — which is exactly the value RUN-030's
certificate carries for `disc(f₂)`, logged there from RUN-018. Two rounds reached
it by different routes: RUN-018 through Tate's algorithm and the certificate's
row, this one through the monic cubic `x → x/4` scaling. They agree.

## `ℓ = 3` is blocked twice, and neither block is a short search

Refuted at 3: the Borel, the split Cartan normaliser, `A₄` and `A₅`. Not refuted:

* **`S₄`.** `PGL₂(F₃) ≅ S₄`, so "projective image `S₄`" is surjectivity itself.
  There is nothing to refute.
* **`N(nonsplit Cartan)`.** The test needs `a ≢ 0` and `a² − 4ℓ'` a nonzero
  square mod 3. But a nonzero trace forces `a² ≡ 1`, and `4 ≡ 1`, so
  `a² − 4ℓ' ≡ 1 − ℓ'`; that is the nonzero square 1 only when `3 | ℓ'`, which the
  test excludes. **Four residue cases, exhausted** — the same shape RUN-031 had
  to give `n = 2`, and reported the same way: vacuous, not undecided.

So `ℓ = 3` is partially certified. Reporting it as certified because four of six
classes fell would be reporting a partial check as a whole one.

## What this adds to the audit's sentence

| | before | after |
| --- | --- | --- |
| irreducible at Mazur's twelve | RUN-031 | — |
| **surjective** at `ℓ = 2` | — | **computed** |
| **surjective** at 37 primes `5 ≤ ℓ ≤ 167` | — | **computed** |
| Mazur degrees fully surjective | 0 of 12 | **11 of 12** |
| `ℓ = 3` | asserted | four classes refuted, two structurally unrefutable |
| `ℓ > 170` | asserted | Serre's theorem, cited |

## The drill

**144 defects, 144 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 24 controls undisturbed, over 64 checks.

The 4 planted for this gate, each turning `mod-ell-surjectivity` red and nothing else:

| planted defect | went red |
| --- | --- |
| every Frobenius is given projective order 6, so S4 is refuted at 3 where it is the whole group | `mod-ell-surjectivity` |
| the nonsplit-Cartan vacuity at 3 is reported refutable | `mod-ell-surjectivity` |
| a class with no witness is counted as refuted | `mod-ell-surjectivity` |
| the mod-2 verdict stops following from the cubic | `mod-ell-surjectivity` |


## What this round does not claim

* **"For all `ℓ`" is Serre's theorem, cited.** That a non-CM curve has surjective
  `ρ̄_ℓ` for all but finitely many `ℓ` is a theorem this round takes as given; what
  is computed is a finite range, and the report says which primes it reached.
* **Non-CM is not proved here.** A CM curve would have failed the Cartan
  refutations at many `ℓ` and none failed, which is evidence and not a proof. The
  certificate itself does not need the assumption — refuting all six classes
  certifies surjectivity whatever the curve is — but the infinite statement does.
* **The certificate is one-sided.** A class with no witness below the search bound
  would be undecided, not established. That happened only at `ℓ = 3`, where the
  gate goes further and shows no bound could help.
* **The classification of maximal subgroups is cited**, not derived: that a proper
  subgroup with surjective determinant lies in one of those six is standard for
  `ℓ ≥ 5`, and `ℓ = 2` is handled by the `S₃` computation instead.
* **Surjectivity is not optimality.** It closes the audit's stated premise, not
  the conclusion drawn from it — which curve the modular parametrisation lands on
  remains a statement about `X₀(696)`, as RUN-031 and RUN-032 both recorded.
