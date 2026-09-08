# RUN-006 — all 4,062 three-isogeny determinations verified, and a disagreement that was mine

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the `has_isogeny_3` column of the Banwait–Huang census's removal evidence — the gap RUN-005 declared and left open
**Tools:** [`src06_three_isogeny_sieve.py`](../code/src06_three_isogeny_sieve.py)
**Logs:** [`src06-three-isogeny-sieve.json`](../data/gate-logs/src06-three-isogeny-sieve.json)

**Result: 4,062 of 4,062 verified independently, with zero disagreements and zero left unresolved. The census's 3-isogeny column is correct on every curve it covers. Two things worth more than that number: a float evaluation gave a confidently wrong answer on the one hard curve, and the finished gate then disagreed with the package on that same curve — because of a constant I had mistyped, not because of anything in the data.**

---

## Closing a gap this arm declared

RUN-005 verified the arithmetic half of the census's removal accounting and
stated what it had not done:

> **It does not check the isogeny half.** The 3/5/7-isogeny determination was
> read from the package, not recomputed.

1,355 curves were removed for an isogeny reason and taken on trust. This round
recomputes the 3-isogeny determination for **all 4,062 removed curves**, not
only the 1,233 claimed to have one — because a false negative is as much an
error as a false positive, and only checking the positives would find at most
half of what could be wrong.

## The criterion, derived rather than assumed

`E/Q` has a rational 3-isogeny iff it has a Galois-stable subgroup `C` of order
3. Writing `C = {O, P, −P}`, stability means `σP ∈ {P, −P}` for every `σ`, which
holds exactly when `x(P)` is Galois-fixed — that is, when `x(P) ∈ Q`. And `x(P)`
is a root of the 3-division polynomial

$$\psi_3(x) = 3x^4 + b_2x^3 + 3b_4x^2 + 3b_6x + b_8.$$

So **E has a rational 3-isogeny ⟺ ψ₃ has a rational root**, and the whole
question becomes one about a quartic with integer coefficients.

## Three methods, because one was not enough

| method | what it decides | curves |
| --- | --- | ---: |
| **mod-p sieve** — a rational root has denominator dividing 3, so for every `p ≠ 3` it reduces to a root in `F_p`. No root mod some `p` ⇒ no rational root. | one-sided, exact, cheap | **2,829** |
| **rational root theorem** — `u/v` with `v \| 3` and `u \| b₈`, from a full factorisation of `b₈` | decisive when `b₈` factors | **1,232** |
| **monic substitution** — `y = 3x` gives the monic `y⁴ + b₂y³ + 9b₄y² + 27b₆y + 27b₈`, so a rational root is an *integer*, bounded, and reachable by a sieved scan needing no factorisation at all | decisive always | **1** |

The sieve is deliberately reported as **one-sided**. A quartic can have roots
modulo every prime and none over `Q`, so passing the sieve everywhere is not
evidence of an isogeny. The first version of this gate reported 1,233 curves as
`UNRESOLVED` on exactly that ground rather than counting them as agreement.

`|b₈|` reaches **26 digits** in this population, which is why the second method
alone was not enough, and why the third exists.

| verdict | count |
| --- | ---: |
| package says `True`, exact root found | **1,233** |
| package says `False`, a prime witnesses no root | **2,829** |
| refuted | **0** |
| disagreements | **0** |
| unresolved | **0** |

## The float that was confidently wrong

One curve — `183430x1`, conductor 183,430, `\|b₈\| = 1{,}289{,}692{,}505{,}594{,}136{,}217{,}700` —
survived both the sieve and the factoring budget. The first attempt to settle it
scanned for real roots with **floating-point** evaluation of `ψ₃`.

It reported **one** real root, at `≈ −326394.775`, and no rational roots. Both
conclusions were false, and the first is self-refuting: `ψ₃` has positive leading
coefficient, so it tends to `+∞` at both ends and its real roots come in an
**even** number. Reporting one is arithmetically impossible, not merely unlucky.

The cause is ordinary: with coefficients near `10²¹`, double precision has no
significant digits left for the cancellation that locates a root. Redone on
Python integers with a modular sieve, 3.2 million candidates fell to **2**, and
the root appeared at once:

$$x = 163100, \qquad \psi_3(163100) = 0 \ \text{exactly}.$$

So `183430x1` does have a rational 3-isogeny, and the package's `True` is right.

**The float answer would have been reported as a finding against the package.**
What stopped it was not a check — it was the parity of a quartic's real roots
being a thing worth noticing.

## The gate then disagreed with me, and it was right to

Folding the monic fallback into the gate, the very next run reported
`EXACT_DISAGREES: 1` — on `183430x1`, the curve whose answer had just been
established by hand.

The gate was wrong, and the reason was one constant. Under `y = 3x` the constant
term becomes `27b₈`; the code multiplied by `9`. Corrected, and the run reads
4,062 agreements and zero disagreements.

This is worth stating plainly because the direction matters. **A gate's
disagreement is not automatically a finding about the subject.** Had that
disagreement appeared on a curve whose answer was not already known, the honest
reading — one curve refuted out of 4,062 — would have been publishable, precise,
and wrong. What caught it was that the gate contradicted a result established
independently minutes earlier.

Two of this round's three errors were mine, and both were caught by having a
second, differently-derived answer to compare against. That is the same
discipline this arm applies to the corpus, pointed the other way.

## What this round does not claim

* **Nothing about BSD.**
* **The 5- and 7-isogeny columns are still unverified** — 115 and 7 curves.
  ψ₅ and ψ₇ are degree 12 and 24, and the same three-method approach should
  reach them, but it has not been run. Stated as the remaining half of the gap,
  not passed over.
* **It does not verify that removing curves with a 3-isogeny is the right
  criterion.** It verifies the census applied its stated criterion correctly.
* **It does not check the curves the census kept.** 36,687 base curves were
  never tested here; only the 4,062 removed ones carry an isogeny column.
