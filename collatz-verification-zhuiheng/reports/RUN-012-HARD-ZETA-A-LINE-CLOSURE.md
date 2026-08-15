# RUN-012 — the B-line handoff, and whether the A-line closure closes what it says

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_B_Line_Handoff_v0.1.md` (2026-08-11 21:57, source item 29) and `Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip` (22:06, item 30) — carrying Round 03-A.5, `A_Line_Closure_v1.0.md` and `ROUTE_MAP_v0.8_A_CLOSED.md`
**Tools:** [`hz_chart_algebra.py`](../code/hz_chart_algebra.py) (slack layer) · [`hz_accel_code.py`](../code/hz_accel_code.py) (occupancy layer) · [`src14_hardzeta_bline_aline_closure_recheck.py`](../code/src14_hardzeta_bline_aline_closure_recheck.py) · [`src14_drill.py`](../code/src14_drill.py)
**Logs:** [`src14-bline-aline-closure-recheck.json`](../data/gate-logs/src14-bline-aline-closure-recheck.json) · [`src14-drill.json`](../data/gate-logs/src14-drill.json)
**External:** [`lopez-stoll-arxiv-2101.12747.json`](../data/external/lopez-stoll-arxiv-2101.12747.json)

**Result: 30/30 checks. 34/34 planted defects caught by the check named for each — 8 in the B-line slack layer, 11 in the A.5 occupancy layer, 5 in this run's own measurement, 2 in the archived citation, 8 in the documents' scope language. 3/3 null controls undisturbed.**

---

## What is being claimed, and what is not

Item 30 says the A line is **closed**. That is the largest-sounding claim in the
Hard-Zeta programme so far, so the first job is to read what it actually asserts.

`A_Line_Closure_v1.0.md` puts the scope in its own header — *未宣稱：Terras
coefficient-stopping conjecture、Collatz conjecture 已證* — and then spends §9 on
nothing but status language:

> Correct statement: **A 線 reduction program 完成。**
> Incorrect statement: A 線已證明 Terras coefficient-stopping conjecture。
> **No.**

Round 03-A.5 §35 says the same thing as a ledger: thirteen completed reductions,
one open item, and the line *A 線「猜想證明」未完成*.

**So "closed" means the reduction programme is finished, not that anything is
proved.** The claim is correctly scoped, and this run checks it as a scope claim:
the disclaimer must be present, the proof sentence must appear only as the one the
document labels incorrect, the open ledger must still name CASP, and route map
v0.8 must not quietly say something else. Eight of the planted defects are edits to
the documents themselves — five that would let the A-line documents claim more
than they have (dropping the disclaimer, promoting the incorrect sentence to
correct, emptying the open ledger, deleting a completed reduction, and making the
route map disagree with the closure), two that strip the handoff's own no-gos, and
one that silently edits a re-shipped round inside the bundle. Each is caught.

---

## Does "COMPLETE" carry what it says?

Item 30 is named `A_Line_COMPLETE_Rounds_01_03A5`, and it re-ships seven round
papers this arm has already rechecked one at a time as items 19–28. If any of
those copies had been edited, none of that work would transfer to item 30 — so
the bundle's copies are compared by digest against the standalone bundles:

- **7 re-shipped papers, byte-identical**, every one of them (Rounds 01, 02, 03A,
  03A1, 03A2, 03A3, 03A4);
- **3 files new**: Round 03A5, `A_Line_Closure_v1.0.md`, `ROUTE_MAP_v0.8_A_CLOSED.md`.

Nothing else. So the "COMPLETE" claim is faithful, RUN-005 through RUN-011 carry
over to item 30 unchanged, and the genuinely new content is exactly the three
files checked below. A planted edit to a re-shipped round inside the bundle fails
this check.

**Route map v0.7 → v0.8 drops no open question.** v0.8 is a compression — 195
lines to 110 — that removes the machinery (deficit recurrence, nested-cylinder
ledger, the continued-fraction gate) now living in the round papers, and keeps
only the final reduction. v0.7's `# Next choices` listed exactly two: 03-A.5 and
03-B Correction Delay. Both are discharged — 03-A.5 is in this bundle, 03-B is the
handoff — and v0.8 replaces that section with the four remaining A-only routes.
This matters because a route map that quietly loses a live question between
versions is how a programme convinces itself it is finished; RUN-004 caught one
such drop earlier in this line. This one is clean.

---

## The one external dependency, checked

Everything new in A.5 §16–§20 — `liminf d_m/m = 0`, the exclusion of a permanently
deep-deficit regime, the saturating subsequences — rests on a single citation:
López–Stoll, used for the statement that a rational 2-adic integer with a
divergent trajectory must have `liminf h(ℓ)/ℓ = ln2/ln3`.

Fetched and archived: **arXiv:2101.12747**, Josefina López and Peter Stoll,
submitted 2021-01-29. The claimed statement appears **verbatim in the abstract**,
in the same `h`/`ℓ` notation §12 uses:

> "if there is a rational 2-adic integer with a non-cyclic trajectory, then
> necessarily lim inf (h/ℓ) = ln(2)/ln(3)"

Positive integers are rational 2-adic integers, and a positive-integer trajectory
is non-cyclic exactly when it is unbounded, so A.5's specialisation is inside the
cited statement. The subject bibliography flags it as a preprint and tells the
reader to mark it as one — which is the right handling, and no journal reference
has appeared on the listing since.

What I did **not** verify: that the statement is numbered *Theorem 1* inside the
paper, as A.5 calls it. Only the abstract was read. The archived record says so in
its own `not_verified` field, and two drill defects damage that record to confirm
the check is reading it rather than the filename.

---

## Item 29 — the B line, measured in its own coordinates

The handoff restates Round 02's first-crossing test as an **exact integer**:

```
Λ(w) = Δ_w·ν(w) − b_w          Δ_w = 2^k − 3^u
Λ > 0 immediate descent   ·   Λ = 0 boundary   ·   Λ < 0 correction delay
```

and §13 observes that Terras equality on `W_fc` is exactly `Λ(w) ≥ 1`. That is a
better machine-checkable form than the ratio, and it is right to prefer it.

All 81,119 first-crossing words to length 24 clear it. The trichotomy is confirmed
against direct iteration on **all** contracting words, not only first-crossing ones
— the delay branch does occur off `W_fc`, so the equivalence is graded where both
outcomes exist rather than on a set where one side is constantly true.

**The new coordinate reproduces RUN-006 exactly.** The handoff's ratio
`R(w) = b_w/(Δ_w ν(w))` peaks at `251/507` on `UUUDUUDD`; RUN-006 measured
`c_w/ν(w) = ⌊251/13⌋/39 = 19/39 = 0.487` on the same word by Round 02's route. Two
formulas, one word, one value.

**Where the supremum lives.** §12 notes that `sup R < 1` is sufficient for Terras
equality. Measured by length:

| length | words | max `R(w)` | argmax |
|---|---|---|---|
| 5 | 2 | 0.418 | `UUDUD` |
| 7 | 3 | 0.222 | `UUUDUDD` |
| **8** | **7** | **0.495** | **`UUUDUUDD`** |
| 10 | 12 | 0.0097 | `UUDUUUDUDD` |
| 16 | 476 | 0.043 | `UUUDUUUUUDDDUDUD` |
| 20 | 2,652 | 0.0074 | `UUUUDUUUUUDDDUDUDUDD` |
| 24 | 51,033 | 0.048 | `UUDUUUUUUDDUUUUDDDUDUDUD` |

**The supremum over all 81,119 words is attained at length 8**, and no length from
10 to 24 comes within a factor of ten of it — 51,033 words at length 24 and the
worst is 0.048. So the extremal candidate for B line's Round B-01 is a *short*
word, and a proof strategy that works by controlling long words is aiming away
from the binding case.

I state the negative half too: the post-8 maximum does **not** decay. It
oscillates (0.0097, 0.0061, 0.029, 0.014, 0.043, 0.0041, 0.0074, 0.029, 0.0026,
0.048) and its largest value sits at the longest length examined. So there is no
evidence for `max R → 0`; only that nothing has come near the length-8 peak. And
the handoff's own No-Go 4 says this is a finite check and not a proof, which it is.

**No-Go 2, confirmed with witnesses.** §11 warns that a `b_w`-extremal word need
not be `Λ`-extremal, because `ν(w)` moves too. The closed forms `b_min = 3^u − 2^u`
at `U^u D^{k−u}` and `b_max = 2^{k−u}(3^u − 2^u)` at `D^{k−u}U^u` hold against a
full enumeration of every shape with `k ≤ 12`; and in **41** of those shapes the
slack-minimising word is neither of the two. The warning is not defensive
throat-clearing — it has witnesses, and this check fails if it does not find them.

**Round B-01's first two steps are already done.** §26 asks the next line to
begin by generating `W_fc`, computing `(b_w, r_w, ν(w), Λ(w))` exactly for each
word, and then examining the extremal structure. Steps 1 and 2 and most of Step 4
are discharged above. The §25 record `Γ_B(w) = (k, u, Δ_w, b_w, r_w, ν(w), m_w,
Λ(w))` is emitted for both extremal words at every length by
[`bline_gamma_b.py`](../code/bline_gamma_b.py) into
[`data/b-line-gamma-b.json`](../data/b-line-gamma-b.json), so the B line can start
from data rather than regenerate it. That file is an **emitter, not a check** — it
asserts nothing; the checks that grade those quantities are in this run, and the
algebra beneath it is what the drill damages.

What Step 4 still wants and this run does not answer: whether the slack
minimisers form a recursive family, and the U-position pattern. Both are
structural questions rather than measurements, and belong to the line that takes
the handoff.

---

## Item 30 — the finite-local no-go, priced

A.5 §5–§6 is the sharpest thing in the round. Every finite exponent code has
infinitely many positive-integer realizations (`n = r_m + t·2^{K_m+1}`), the
all-one code is subcritical at every prefix, and it is realized by `2^{m+1} − 1`.
Hence arbitrarily long zero-occupancy prefixes exist, hence **no finite
forbidden-pattern argument can finish the A line.** All of it verified — the
closed forms `B_m = 3^m − 2^m`, `r_m = 2^{m+1} − 1`, and `2^{m+1} − 1` actually
running the all-one code, to `m = 40`.

What the round does not say is how *expensive* its witness is. Measured against
the smallest start with the same subcritical reach:

| `m` | §5's witness `2^{m+1}−1` | cheapest start reaching `m` | ratio |
|---|---|---|---|
| 8 | 511 | 27 | 18× |
| 16 | 131,071 | 27 | 4,854× |
| 24 | 33,554,431 | 27 | 1.2 × 10⁶ |
| 36 | 137,438,953,471 | 27 | 5.1 × 10⁹ |

**`n = 27` reaches every depth the all-one family reaches, up to ten orders of
magnitude more cheaply.** The no-go is correct and the witness is honest, but the
witness is wildly non-extremal: the obstruction it exhibits is far denser in the
integers than the family used to exhibit it. Anyone reading §5 as "you need
enormous integers to stay subcritical for long" would have it backwards.

---

## Near-saturation is the normal end state

A.5 §19–§20 says a hypothetical counterexample must satisfy
`E_m/m = (1/m)Σ(q_i − 1) → γ` along a subsequence — asymptotically exhausting the
Sturmian credit while never overspending it. That reads like an exotic
requirement. Measured, it is nearly the ordinary behaviour of a spine at the end
of its life:

| `n` | lifetime | `E_m` / budget | `E_m/m` | `γ − E_m/m` | deficit at death | first overspend |
|---|---|---|---|---|---|---|
| 27 | 36 | 20 / 21 | 0.5556 | 0.0294 | 1 | −1 |
| 103 | 25 | 13 / 14 | 0.5200 | 0.0650 | 1 | −1 |
| 703 | 50 | 27 / 29 | 0.5400 | 0.0450 | 2 | −3 |
| 1407 | 50 | 28 / 29 | 0.5600 | 0.0250 | 1 | −4 |
| 10087 | 65 | 37 / 38 | 0.5692 | 0.0157 | 1 | −4 |
| 15039 | 51 | 27 / 29 | 0.5294 | 0.0556 | 2 | −1 |
| 35655 | 84 | 48 / 49 | 0.5714 | 0.0135 | 1 | −1 |

Every spine dies holding a deficit of **1 or 2**, having spent 93–98% of its
budget. The longest reaches **97.7%** of `γ`.

The shortfall is not a coincidence, and this run checks it as an exact integer
identity rather than as an inequality:

```
E_m = ⌊γm⌋ − d_m      so      γ − E_m/m = ({γm} + d_m)/m
```

With `d_m` small at death, the shortfall is `O(1/m)` with an explicit numerator —
which is why it shrinks from 0.065 at lifetime 25 to 0.0135 at lifetime 84.

**So §19–§20's saturation is not the hard part.** Finite spines already sit within
0.014 of `γ` when they die — 2.3% below it. What A.5 additionally requires of a counterexample is
that this be *sustained forever* rather than terminated by an overspend — and
nothing here touches that. The measurement makes the target less exotic and no
closer.

*Note on the inequality:* `E_m/m < γ` **cannot fail** on a subcritical spine —
subcriticality is `K_m ≤ ⌊βm⌋`, which is `E_m ≤ ⌊γm⌋` rewritten. A check asserting
it would pass by construction. It is replaced by the identity above, drilled by
damaging `excess` and by running one step past each lifetime so both signs of the
deficit appear.

---

## The other branch is invisible

§24–§26 split a hypothetical counterexample into Regime U (uniformly integrable
occupancy) and Regime L (valuation credit leaking to giant `q_i`). The split
`E_m/m = G_R(m) + L_R(m)` holds exactly in Fractions at every `R` tested.

But the largest valuation on any spine measured is **7** (`n = 10087`; the others
are 4–6). So `L_R = 0` for every `R` past that, on every finite spine — Regime L
is empty for any bounded computation, by construction rather than by evidence.
That is exactly why it is the hard branch: no amount of computing can distinguish
"Regime L does not occur" from "Regime L has not occurred yet". §27 makes the same
point about weak-* convergence and unbounded observables, and is right to.

This check is stated so it can fail: the observable must be **non-empty** just
below the top valuation and zero at and above it.

---

## What the closure's ledger costs this arm

§35 lists thirteen completed reductions. Ten of them map to runs already in this
tree (RUN-005 through RUN-011); the remaining three — finite-local no-go, critical
saturation reduction, occupancy/tail dichotomy — are this run. The mapping is
checked, so a reduction the closure claims that no report covers would fail here.
With RUN-012 the A line's reduction chain is rechecked end to end.

---

## A correction to RUN-011

RUN-011's Haar table was measured at `M_MAX = 34` — the depth cap in `src13` —
while its *lifetime* column printed the true lifetime, so four rows paired a
spine's full life with credit counted only to depth 34. The corrected
full-lifetime figures are the table above; RUN-011 has been amended in place with
a note.

The Haar conclusion is unaffected: every spine still spends far under the
Haar-typical rate of 1 per step. The budget reading changes materially, and in the
direction that matters for A.5 — spines end at 93–98% of the Sturmian budget, where
the truncated rows read 68–89%. A depth cap is a legitimate way to bound a
run; printing an uncapped column beside a capped one is what made it a defect.

---

## Three findings about my own checks

**Two checks were vacuous by construction, and the drill was not what found
them.** Both were caught by asking what would have to break for the check to
fail. `E_m/m < γ` cannot fail on a subcritical spine — subcriticality *is* that
inequality, rewritten. `L_R = 0` for `R` above the largest valuation cannot fail
either — `(q − R)_+` is zero for every `q` on the spine by definition. Each was
replaced by a form that can fail: the exact identity `E_m = ⌊γm⌋ − d_m`, drilled by
damaging `excess` and by running one step past every lifetime so both signs of the
deficit appear; and a requirement that the leakage observable be **non-empty** just
below the top valuation, which it is (`1/18` on `n = 27`, down to `1/84` on
`n = 35655`).

**Loosening a threshold was a no-op — the sixth time in this arm.** The mutation
widened the supremum check's `top_k <= 8` to `<= 99` and its tenfold gap to a
tenfold cushion. The real data clears both bounds with room to spare, so neither
widening changed a verdict. Retired and replaced by damaging the aggregation that
builds the per-length maxima, which moves the argmax and therefore the answer.

**An anchor with the wrong indentation tested nothing.** One planted defect
targeted a line inside a loop and quoted it with twelve spaces where the source has
eight. The drill reported it as `anchor absent; nothing was tested` rather than
counting it caught, which is the behaviour that makes the count worth reading — a
drill that silently scored an unapplied mutation as a pass would have inflated the
result by one.

**And once it did apply, it was aimed at the wrong check.** That same defect
prunes every word ending in a run of `U` — including `D^{k−u}U^u`, the claimed
`b`-maximiser — so what it breaks is the *enumeration*, and the check that owns
the enumeration caught it. The witness check I had named survives, because
witnesses remain among the words that are left. Retargeted, and the witness check
was given a defect of its own: make the slack-minimiser be the `b`-maximiser by
construction, and the witness set empties. A defect that fails *a* check is not
the same as a defect that fails *its* check, and the difference is the whole
point of naming them.

---

## What this does not establish

CASP is open, and nothing here bears on it. The finite-local no-go is a statement
about *proof methods*, not about the conjecture — it closes off finite
forbidden-pattern arguments and says nothing about whether a counterexample
exists. The saturation measurements are seven spines with lifetimes under 100; the
paper's own No-Go 4 and §28 both say finite evidence cannot decide an infinite,
anchor-dependent obstruction, and they are right. The López–Stoll dependency is an
unrefereed preprint whose Theorem numbering I did not check.
