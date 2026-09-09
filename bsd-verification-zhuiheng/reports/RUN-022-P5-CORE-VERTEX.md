# RUN-022 — P5's norm-Selmer core vertex: the cube reproduced, three boxed statements shown to be one determinant, and how special 397 and 991 are

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`BSD_P5_Norm_Selmer_Core_Vertex_389a1_p11_v1.2`](../../../amral/public/bsd/p5/files/BSD_P5_Norm_Selmer_Core_Vertex_389a1_p11_v1.2.md) — the Selmer cube, the two rank-1 faces and their transversality
**Tools:** [`src25_p5_core_vertex.py`](../code/src25_p5_core_vertex.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src25-p5-core-vertex.json`](../data/gate-logs/src25-p5-core-vertex.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: v1.2's Selmer cube reproduces exactly — kernel lines `F₁₁(Q − 2P)` and `F₁₁(Q − 4P)`, dimensions `2 → 1, 2 → 1, 1∩1 → 0`, cardinalities `121 → 11 → 1`, `det M_loc = 2`. Two things follow that the documents do not say. First, `Sel^{N_{397,991}} = 0` (§3), the transversality of the two rank-1 faces (§5) and `det(𝓑_N) ≠ 0` (`v1.3` §3) are **the same determinant three times** — three boxed statements, one fact, and none of them is evidence for either other. Second, `{397, 991}` is not special: over the 23 admissible directions below 20,000, **230 of the 253 pairs give a core vertex — 90.9%** — and the 23 that degenerate is exactly what uniform `k` would predict. The round also corrects two things in this tree's own RUN-011: its `usable` flag excludes `ℓ = 19009` for a reason that stops one step short of the real one, and its `admissible` list of 25 counts a direction its own row computation rejects.**

---

## The cube, reproduced

Each localization row is the image of `(P, Q)` in `E(F_ℓ)/11·E(F_ℓ)`, normalised
to `(1, k_ℓ)`. RUN-011 computed those rows from the group law up; this round
takes them and does the linear algebra v1.2 boxes.

| v1.2's claim | recomputed |
| --- | --- |
| `Sel^{N_397} = F₁₁(Q − 2P)` | **`Q − 2P`** |
| `Sel^{N_991} = F₁₁(Q − 4P)` | **`Q − 4P`** |
| `Sel^{N_{397,991}} = 0` | **0** |
| dimensions `2 → 1, 2 → 1, 1∩1 → 0` | **`{∅: 2, 397: 1, 991: 1, both: 0}`** |
| cardinalities `121 → 11 → 1` | **`[121, 11, 1]`** |
| `det M_loc = 2` | **2** |

## Three boxed statements, one determinant

With every row normalised to `(1, k)`, two directions give

$$M_{\rm loc}=\begin{pmatrix}1&k_1\\1&k_2\end{pmatrix},\qquad \det M_{\rm loc}=k_2-k_1,$$

and `det = 2` is `k_991 − k_397 = 4 − 2`. Then:

* **§3's `Sel^{N_{397,991}} = 0`** holds iff `det ≠ 0`;
* **§5's transversality of the two rank-1 faces** — the lines `Q − 2P` and
  `Q − 4P` being distinct — holds iff `det ≠ 0`;
* **`v1.3` §3's `det(𝓑_N) ≠ 0`**, which that document derives as
  `det(𝓑_N)(P∧Q) = det(M_loc)·(e₃₉₇∧e₉₉₁)⊗X₃₉₇X₉₉₁`, holds iff `det ≠ 0`.

All three are `k_991 ≠ k_397`. The gate reports them together with that reading
attached, because three boxed statements spread across two documents read as
three confirmations, and they are one arithmetic fact. This is the same shape as
RUN-020's finding that v0.8's `16/11` and its `#E(F₁₁) = 16` are one
computation.

## How special is `{397, 991}` — measured

RUN-011 noted that 397 and 991 are the two smallest admissible directions and
did not compute the pairwise matrices. Because a pair of `(1, k)` rows
degenerates exactly when the two `k` agree, the whole question is the
distribution of `k`:

| `k` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| directions | 3 | 3 | 3 | — | 3 | 1 | 1 | 2 | 1 | 1 | 5 |

23 admissible directions below 20,000, 10 of the 11 residues occupied, **253
pairs of which 230 give a core vertex — 90.9%**. The 23 degenerate pairs are
exactly the `253/11 = 23` that uniform `k` predicts.

So the core-vertex condition is generic, and the chosen pair is the two smallest
directions rather than a distinguished one. That is a fact worth having before
an attack builds anything on the choice: **nothing in the construction depends
on 397 and 991 in particular**, and there are 229 other pairs below 20,000 that
would serve.

## Two corrections to this tree's own RUN-011

Both are about that gate rather than about the corpus.

**Its `usable` flag means "the row normalises to `(1, k)`", not "a row
exists".** A row can have shape `(1, k)`, `(0, 1)` or `(0, 0)`, and only the
first normalises. At `ℓ = 19009` RUN-011 reports

> `usable: false` — "P lands in 11·E(F_ℓ); the row cannot be normalised to 1"

The exclusion is **right in effect and its stated reason stops one step short**.
If only `P` died, the row would be `(0, 1)` and the direction would impose a
perfectly good condition, `Sel^{N_{19009}} = F₁₁·P`. What is actually true there
is that **`Q` dies as well**, so the row is `(0, 0)` and the direction imposes
no condition at all. RUN-011's `both_are_11_torsion: true` for that prime is
likewise vacuous — the identity is 11-torsion. The row shapes are counted here
rather than assumed, so "every row is `(1, k)`" is reported as a measurement
over this range (**23 of 23**) and not as a theorem.

**Its `admissible` list counts 25 while its own row computation rejects one of
them.** `ℓ = 19867` has `v₁₁(#E(F_ℓ)) = 3`; the list's stated criterion asks only
that 11 divide `#E(F_ℓ)`, while the row computation asks that it divide it
exactly once — which it must, or the norm quotient is not one-dimensional and a
single residue `k` does not describe the row. The two used different criteria in
one log. This gate uses the second, giving **23**, and records the discrepancy
rather than quietly reporting a different number from a prior round.

`19867` is also, as it happens, **the only prime below 20,000 with `v₁₁ ≥ 2`** —
which is why that branch cannot be exercised by any fixture cheap enough to run
once per planted defect, and why the valuation test is now a one-line predicate
the drill can test directly.

## The drill

**95 defects, 95 caught by the check named for each — none uncaught, none
caught by the wrong check. 20 controls, none disturbed, over 44 checks.
Thirteen minutes and fourteen seconds.**

Gate 25 contributes two checks and four defects, at a cost of 0.08 seconds per
sweep. The scan runs at 3,000 rather than the gate's 20,000, and the reason is
stated in the check rather than left as a tuning knob: below 6,000 every row is
`(1, k)` and the only skip reason is `v₁₁ = 0`, so real data exercises the
common path and nothing else. The two structural cases the corpus produces only
near 20,000 — a `(0, 1)` row and a `(0, 0)` one — are supplied as fixtures,
because a classifier whose other branches are never taken is not tested by a
scan that never reaches them.

## What this round does not claim

* **Nothing about BSD.** It reproduces v1.2's finite linear algebra and measures
  the genericity of the construction's inputs.
* **The rows are RUN-011's**, recomputed there from the group law; this round
  takes them as given and does the algebra on top. The identification of
  `E(Q_ℓ)/N E(L_ℓ)` with `E(F_ℓ)[11]` for a tame totally ramified degree-11
  extension is cited by that round, not proved here.
* **`dim Sel^{N_∅} = 2` needs `Ш(E/Q)[11] = 0`**, which is inherited by the whole
  P5 chain and is not touched here, plus rank 2, which is cited. Only the
  trivial torsion is ours.
* **The pair scan is below 20,000.** Genericity in that range is not genericity.
* **`v1.3` §3's identification of `det(𝓑_N)` with `det(M_loc)`** is read, not
  reproved — the same standing limitation RUN-021 recorded.
