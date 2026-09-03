# The shapes a check takes when it cannot fail

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Drawn from:** the 73-item recheck of Neo.K's Collatz Operation Translation
Series and Hard-Zeta rounds, 2026-08-10 to 2026-09-03 — 52 run reports, 54
falsifiability drills, 1,433 planted defects.

---

## What this is, and the one sentence that keeps it honest

Across seventy-three source items the **mathematics held everywhere it could be
reached**. What did not hold, repeatedly, was the *checking apparatus*: scripts
that ship beside a theorem and report zero violations over hundreds of thousands
of instances, where the zero was guaranteed before the first instance was
generated.

So, before anything else:

> **Finding one of these is a defect in the evidence offered for a claim. It is
> not a refutation of the claim.** In every instance catalogued below the
> statement being checked was, as far as this arm could determine, true. What was
> wrong was that the check could not have discovered otherwise.

That distinction is the whole point of the catalogue. A reader who takes "their
checker cannot fail" to mean "their theorem is wrong" has learned the opposite of
what these findings say.

Two of the eight shapes below were found in **this arm's own** checks, not in
anyone else's. They are marked. A catalogue of other people's blind spots that
contains none of your own is not a catalogue; it is an accusation.

---

## The criterion

Every shape here is an instance of one test:

> An assertion cannot fail if it is a restatement or an algebraic consequence of
> **its own guard, its own definitions, or the code that precedes it**.

The second clause is the one that takes work. It is *not* enough that an
assertion is a true theorem about validly constructed inputs — almost every
assertion in a verification script is that, and it is exactly what an assertion
is for. The question is narrower and harder:

**Given how this input was constructed and admitted, is there any assignment at
all that reaches this line and violates it?**

A check fails this test when the answer is no *for reasons already fixed by the
lines above it*. It passes when the answer is no only *because the theorem is
true* — which is the case for a real test, and which no amount of running can
distinguish from the first case, because both print `0`.

This is why a mutation drill does not find them. A drill perturbs the code and
asks whether some check goes red. A check that cannot go red was already green
before the perturbation and stays green after it, so the drill scores it as
passing, forever. **These have to be found by reading, before running anything,
and asking what the world would have to look like for the line to come out
false.**

---

## The eight shapes

### 1. The assertion restates its own guard

The tightest form, and the hardest to see, because the guard and the assertion
are usually many lines apart.

```python
if c2 > 0 and c3 <= 0:
    assert Bp >= Bt + L
if c2 <= 0 and c3 > 0:
    assert A - Ap >= Q
```

Three sections earlier, the same file defines

```
c2 = Q + A' - A          c3 = L + B - B'
```

so `c3 <= 0` **is** `B' >= B + L`, and `c2 <= 0` **is** `A - A' >= Q`. Each
assertion is the guard that admitted it, rearranged. Neither can fail on any
input, in any universe.

**How it was measured, rather than argued:** both members of each pair were
evaluated separately on every segment — **466,864 comparisons, 0
disagreements**. Two expressions that never disagree over half a million
segments are one expression.

**What to do:** state the theorem's content as a relation between quantities the
guard does *not* determine. Here that meant checking the compensation depths
against orbit data rather than against each other.

---

### 2. The assertion is entailed by its own setup — *found in this arm's own work*

Two routes, both ending in a check that reads like an empirical finding and is
arithmetic about the setup.

**Entailed by the selection.** "Excess valuation density stays under γ",
measured only on subcritical spines. But *subcritical* **means** `K_m ≤ ⌊βm⌋`,
which is `E_m ≤ ⌊γm⌋` rewritten. The filter that chose the data is the claim. A
counterexample would have to be a subcritical spine that is not subcritical.

**Entailed by the definition.** "Tail leakage vanishes above the largest
valuation", where `L_R = (1/m) Σ (q_i − R)_+`. Above the top valuation every term
is `(negative)_+ = 0`. Not a fact about spines; arithmetic about `max`.

Neither was found by the mutation drill. Both were found by asking the question
in the criterion above before running anything.

**What to do:** name the population *and* the predicate out loud, in that order,
and check whether the second is the first with the words changed.

---

### 3. A guarded assertion counts samples, not tests

A bundle's checker reported `random_exact_residue_checks: 7990` and
`quantile_jensen_tests: 10000`. All three assertion sites are guarded, and the
counters increment outside the guard:

```python
if n < 2 ** (Q + 1):            # rarely true for a short prefix of a large n
    assert source_rep(w) == n
if cur < 3 ** h:
    assert endpoint_rep(w) == cur
random_residue_checks += 1      # increments either way

if h > 3 * Z:                   # 3Z averages above h over the sampled ranges
    assert avg >= log2(h / (3 * Z))
quantile_tests += 1             # increments either way
```

Reimplementing the sampling scheme independently at its own stated parameters
gave the real rates: the source assertion runs on **10.0%** of samples, the
endpoint assertion on **7.6%**, Jensen on **33.8%**, and the quantile bound is
non-trivial on **5.0%**.

Note what this is and is not. Wherever a guard opens, the assertion passes —
**zero violations**. This is a measurement of what the reported number *means*,
not a defect in their mathematics. "10,000 tests" was 3,380 tests.

**What to do:** increment the counter inside the guard, and publish both numbers
— samples drawn and assertions evaluated. They are different facts and a reader
cannot recover one from the other.

---

### 4. A bound that is vacuous on every finite instance

A theorem read `#{i : H_i < A} < 3Z · 2^A`. It is non-trivial only when
`3Z · 2^A < h`. On this population the endpoint satisfies `Z ≡ 7 or 11 (mod 12)`,
so `Z ≥ 7` and `3Z ≥ 21`, while the longest tail found was 35. Across **10,488
instances** — every bridge crossed, with twelve integer values of `A` — **not one
was non-vacuous**. Reporting "0 violations" there is reporting `0 < 42` ten
thousand times.

The interesting part is what the proof actually bounds. It is one line: every
index with `H_i < A` contributes more than `2^{-A}` to `S = Σ_i 2^{-H_i}`, so

> `#{H_i < A} · 2^{-A} < S`

and `S < 3Z` is a *further* relaxation applied afterwards. Keeping `S` gives
**136 non-vacuous instances**, all clean — and `S` had already been computed for
an identity two sections earlier, so it cost nothing.

**Why this shape is so common:** a published bound is usually stated in the form
the asymptotic argument needs, which means the last relaxation has already been
applied. That relaxation is exactly what makes it vacuous at finite scale.

**What to do:** read the proof, not the boxed line. The quantity the proof
bounds is one step back and is often already in the checker's memory.

---

### 5. A headline identity that is a definition

A paper's central boxed result, an *Exact Endpoint–Laplace Identity*:

> `Σ_{i<h} 2^{-H_i} = 3(Z − 2^{-E} X)`

with a note that it is exactly rational, no floating point. Both true. But
`2^{-H_i} = 3^{h-i} / 2^{Q-P_i}`, so multiplying through by `2^Q` gives

> `Σ_{i<h} 3^{h-i} 2^{P_i} = 3(2^Q Z − 3^h X)`

whose left side is `3 · Σ_i 3^{h-1-i} 2^{P_i}` — **term by term the definition of
`B_w`** three sections earlier. The identity restates a definition. A checker
that verifies it in exact rationals, which the shipped one did, has verified its
own exponent bookkeeping.

The falsifiable statement is one line below and is a different sentence: whether
**real orbit data** satisfies the affine relation `2^Q Z = 3^h X + B_w`. That one
an off-by-one in `P_i`, a wrong power, or a mis-built word all break.

**What to do:** clear denominators on any boxed identity and compare it term by
term against the definitions in scope. If it survives, it is a result.

---

### 6. A guard at exact equality never opens

A two-level test — an outer comparison against the loose end of a certified
bracket, an inner strict test against the tight end:

```python
if Fraction(n1) < (2 - b_hi) * l_up + h_hi:      # outer: "could this fail?"
    if Fraction(n1) < (2 - b_lo) * l_up + h_lo:  # inner: the real test
        violations += 1
```

The drill planted `+ 1` on the inner threshold and reported **changes nothing**.
The reason is the population's own shape: the bound is **attained**, tightest
slack exactly `0.0`. At the case that matters, the outer guard is a strict `<`
evaluated at equality, so it is `False`, and the inner line is unreachable in
exactly the situation it exists for. Every other case has slack far larger than
the tightening. The check was decorative at its only interesting point.

**What to do:** one comparison against the *certain* end of the bracket, not two
against opposite ends. And measure attainment: a bound whose tightest slack is
`0.0` is a different object from one with room, and the difference is invisible
in a violation count.

---

### 7. An empty population from the domain you chose, not from rarity

A premise required `Y_s = min_{m ≥ s} Y_m`. Scanning a thousand orbits found
**zero**, and the first reading — trained by the previous two rounds — was
"another premise real orbits do not meet; report the denominator and check the
algebra instead."

That reading was wrong. A convergent Collatz orbit ends at 1, the global
minimum. Over a whole orbit, "less than everything after you" is satisfiable by
**nothing**, because 1 is after everything. The population was not rare; the
definition was unsatisfiable **on the domain that had been chosen**.

Taking a finite window that stops before the descent — which the bundle's own
checker scope specified, and which had already been read — gives **16,251
instances across 2,295 orbits**, and the theorem verifies on every one.

**What to do:** an empty count has at least two causes calling for opposite
responses. Genuine rarity → report the denominator honestly. An unsatisfiable
definition on your chosen domain → fix the domain, and check the source's own
stated scope first, because it may already say so.

---

### 8. A structural zero is not a weak zero — *the shape that corrects the reflex*

After five consecutive rounds of counters that could not go red, a reflex forms.
By the sixth the reflex was wrong.

The counter said: *no two erasure intervals cross*. It never fires. But not
because it is weak — because a crossing is **unrepresentable** in that
construction. The stack is truncated at every repeat, so a residue that could
form a crossing has already been removed. Trying to plant one by leaving a
removed residue reachable does not produce a crossing; it raises `IndexError`,
because the retained-time array was truncated with the stack.

**Both diagnoses produce `0`. Only one of them is a criticism of the author.**

The responses differ too. A weak check should be strengthened or replaced. A
structural one is fine to keep — it is cheap and it documents an invariant — but
it is **not evidence**, and it cannot distinguish itself from a predicate that is
simply broken. So the predicate gets exercised by hand on a constructed crossing
to prove it still recognises one.

**What to do:** before calling a zero a finding, try to *build* a violation. If
the construction is impossible, say "structural"; if it merely never occurs, say
"weak". Those are different reports.

---

## What this catalogue does not claim

Stated as plainly as the findings, because a reader who takes only the headline
away will take the wrong thing:

* **It says nothing about whether any of these theorems are true.** Every
  statement whose checker is criticised here held wherever this arm could reach
  it. A defect in a checker is a defect in evidence.
* **It says nothing about the Collatz conjecture.** Every claim rechecked across
  all seventy-three items is a finite statement about finite objects.
* **It is not a completeness claim.** These are the shapes that were found. A
  ninth almost certainly exists; the eighth was found only after five rounds had
  trained a reflex that the eighth then broke.
* **It is not an accusation of carelessness.** Shapes 4 and 5 arise from
  ordinary, correct mathematical writing — stating a bound in the form the
  asymptotic argument needs, boxing the identity a reader should carry. The
  defect appears only when a *checker* is written against the published form
  rather than against the proof.

---

## The procedure this reduces to

1. **Read the checker before running it**, and for each assertion ask: what
   would the world have to look like for this line to come out false?
2. **Trace every guard back to the definitions of the symbols it names.** If the
   guard entails the assertion, it is shape 1.
3. **Count assertions evaluated, not samples drawn.** Move the counter inside the
   guard, or publish both numbers.
4. **Evaluate every bound's non-vacuity separately from its violation count**,
   and read the proof for the quantity one relaxation back.
5. **Measure attainment.** Tightest slack `0.0` changes what a guard does.
6. **Try to construct a violation of any zero before reporting it**, so a
   structural zero is not filed as a weak one.
7. **Run the same seven steps against your own checks.** Two of the eight shapes
   here came from this arm's own scripts, and the drill would have scored them
   green forever.

---

## Where each figure comes from

An earlier draft of this line claimed every figure here is emitted from a gate
log rather than typed. **That was false, and it is the failure this document is
about, committed by the document itself.** The prose is hand-written and the
figures were transcribed into it; what makes them checkable is not the writing
but the report each one is quoted from.

| shape | source |
| --- | --- |
| 1 · assertion restates its guard | [RUN-052](./RUN-052-HARD-ZETA-AU2D24-COMPENSATION.md) |
| 2 · entailed by its own setup | this arm's pre-run audit of its own 03A-series checks. **Not recorded in a RUN report** — it lives in working notes, which is why it is the least checkable item here and is flagged as such rather than given a citation it does not have. |
| 3 · counts samples, not tests | [RUN-045](./RUN-045-HARD-ZETA-AU2D17-SMALL-ENDPOINT-CYLINDER.md) |
| 4 · vacuous on every finite instance | [RUN-045](./RUN-045-HARD-ZETA-AU2D17-SMALL-ENDPOINT-CYLINDER.md) |
| 5 · identity that is a definition | [RUN-045](./RUN-045-HARD-ZETA-AU2D17-SMALL-ENDPOINT-CYLINDER.md) |
| 6 · guard at exact equality | [RUN-043](./RUN-043-HARD-ZETA-AU2D15-RECORD-SPARSITY.md) |
| 7 · empty by domain, not by rarity | [RUN-042](./RUN-042-HARD-ZETA-AU2D14-SPARSE-SUPPORT.md) |
| 8 · structural zero | [RUN-050](./RUN-050-HARD-ZETA-AU2D22-DEFECT-TREE.md) |

The suite-level counts in the header — 73 items, 52 reports, 54 drills, 1,433
defects — *are* emitted, by `code/suite_totals.py` and
`code/build_source_manifest.py` into
[`../data/results.v1.json`](../data/results.v1.json), whose
`explicit_non_claims` field carries the boundaries stated above. The underlying
logs are in [`../data/gate-logs/`](../data/gate-logs/).
