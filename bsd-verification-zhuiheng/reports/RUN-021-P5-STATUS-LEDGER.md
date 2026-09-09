# RUN-021 — the P5 chain's status ledger, reconciled, and two gates this arm closes on its own evidence

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the ten P5 documents' declared gate statuses — chiefly [`IMC_Closure_and_GPR_Bridge_v0.5`](../../../amral/public/bsd/p5/files/BSD_P5_IMC_Closure_and_GPR_Bridge_v0.5.md), [`uGPR_Minimal_Gate_v0.6`](../../../amral/public/bsd/p5/files/BSD_P5_uGPR_Minimal_Gate_389a1_p11_v0.6.md), [`Rank2_Scalar_Collapse_v0.3`](../../../amral/public/bsd/p5/files/BSD_P5_Rank2_Scalar_Collapse_389a1_p11_v0.3.md) and [`P5_E1_ETNC_ESCAPE_AUDIT`](../../../amral/public/bsd/p5/files/P5_E1_ETNC_ESCAPE_AUDIT.md)
**Tools:** [`src24_p5_status_ledger.py`](../code/src24_p5_status_ledger.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src24-p5-status-ledger.json`](../data/gate-logs/src24-p5-status-ledger.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: 44 ledger rows across 39 distinct gate names, extracted verbatim; five gates carry more than one status and all five are explained, so the chain is internally consistent and its blocking graph is acyclic with roots `P5-DERPER`, `P5-BOC-NZ11` and an ambiguous `GPR11`. Two findings matter for an attack. First, `P5-LAT11 BLOCKED BY BOC-NZ11 + GPR11` names a target that matches three declared gates — `P5-GPR11`, `P5-FULL-GPR11`, `P5-uGPR11` — and v0.6 resolves it to the *minimal* one while explicitly marking the full one "STRONGER_THAN_NEEDED"; read the shorthand the other way and an attack goes after a theorem it does not need. Second, two gates the ledgers close by citation are closed **here** by this tree's own computation: `P5-BOC-NZ11` from RUN-011's `det(M_loc) = 2`, and `P5-RESIDUAL-IRR11` from `j(389.a1) = 1404928/389` not being one of the three non-cuspidal `j` on `X₀(11)` — it is not even an integer — with semistability giving it a second time through Mazur. Both are independent of the justification the ledgers actually offer.**

---

## Why a ledger audit at all

P5 is not one argument. It is ten documents that each declare gate statuses in a
fenced block, and a reader who wants to build on the chain needs three things no
single document answers:

1. does any gate carry **different statuses in different documents**, and is
   that a version-ordered upgrade or an unexplained conflict;
2. is the blocking graph **acyclic**, and what are its roots;
3. for each `CLOSED`, is it closed by an **exact finite computation** that can be
   reproduced, or by a **cited external theorem** — the ledgers write both as the
   same word.

The extraction is mechanical and the rows are printed verbatim, so every line of
the table below can be diffed against its document by eye. A ledger audit that
paraphrased its sources would be worth nothing.

## What the reconciliation found

**44 rows, 4 documents, 39 distinct gate names, 5 carrying more than one
status** — and all five explained:

| gate | earlier | later | reading |
| --- | --- | --- | --- |
| `P5-IMC11` | v0.5 `CLOSED (Burungale–Castella–Skinner)` | v0.6 `CLOSED` | same verdict, terser |
| `P5-BOC-NZ11` | v0.5 `PENDING FINITE SAGEMATH REPLAY` | v0.6 `CLOSED_BY_PUBLISHED_COMPUTATION` | **verdict moved**, version-ordered |
| `P5-LAT11` | v0.5 `BLOCKED BY BOC-NZ11 + GPR11` | v0.6 `EQUIVALENT_TO_uGPR11` | refined, and see below |
| `P5-RAT` | v0.3 `OPEN / ARCHIMEDEAN RANK-2 PERIOD COMPARISON` | audit `BLOCKED BY P5-DERPER` | same verdict, the audit names the blocker |
| `P5-VAL11` | v0.3 `ARITHMETIC TARGET = 0, BUT BLOCKED BY P5-RAT` | audit `BLOCKED BY P5-RAT` | same verdict |

The last two are counted as agreements rather than conflicts on a stated rule:
`OPEN` and `BLOCKED BY X` are the **same verdict at different resolution**, and
only `CLOSED` against either is a real conflict. Without that rule the audit
reports noise; with it, **there is no unexplained conflict anywhere in P5**.

The blocking graph has 5 edges and is acyclic. Its roots — the gates nothing
else in the ledger blocks — are `P5-DERPER`, `P5-BOC-NZ11`, and `GPR11`.

## The one genuine defect in the ledger: an ambiguous edge

`v0.5` writes

> `P5-LAT11   BLOCKED BY BOC-NZ11 + GPR11`

Neither target carries the `P5-` prefix its own row uses. `BOC-NZ11` resolves
uniquely to `P5-BOC-NZ11`. **`GPR11` does not** — three declared gates end in
it:

| candidate | v0.6's status |
| --- | --- |
| `P5-GPR11` | `OPEN CONCEPTUAL GATE` (v0.5) |
| `P5-FULL-GPR11` | **`OPEN_STRONGER_THAN_NEEDED`** |
| `P5-uGPR11` | `OPEN_MINIMAL_CONCEPTUAL_GATE` |

The gate leaves the edge unresolved rather than guessing, and reports it. This
is not pedantry: **v0.6 says `P5-LAT11 EQUIVALENT_TO_uGPR11`**, so the blocker is
the *minimal* gate, while the same document marks the full one as stronger than
needed. A reader who takes v0.5's `GPR11` at face value and goes looking for a
full Generalized Perrin–Riou leading-term theorem is chasing something the chain
itself says it does not need.

## Two gates this arm closes on its own evidence

The ledgers write "closed by an exact finite computation" and "closed by a cited
theorem" with the same word. Separated:

### `P5-BOC-NZ11` — Bockstein non-vanishing

| | |
| --- | --- |
| v0.5 says | `PENDING FINITE SAGEMATH REPLAY` |
| v0.6 says | `CLOSED_BY_PUBLISHED_COMPUTATION` |
| what it needs | `det(𝓑_N) ≠ 0`. `v1.3` §3 gives `det(𝓑_N)(P∧Q) = det(M_loc)·(e₃₉₇∧e₉₉₁)⊗X₃₉₇X₉₉₁`, so it is exactly `det(M_loc) ≠ 0` |
| **this tree** | **RUN-011 recomputed the localization matrix `[[1,2],[1,4]]` from the group law up and got determinant `2` mod 11** |

Neither a SageMath replay nor a published computation is what this tree relies
on. The gate is closed here by an independent recomputation that predates the
question being asked.

### `P5-RESIDUAL-IRR11` — irreducibility of the mod-11 representation

v0.5 closes it with **"maximal 11-adic image"**, and RUN-020 recorded maximal
image for every `ℓ` as cited and unverified — X₀(n) covers four of Mazur's twelve
prime degrees and says nothing about surjectivity. Two independent routes close
it without that claim:

* **`X₀(11)`.** `X₀(11)` is the elliptic curve `11a1`, Mordell–Weil group `Z/5`:
  two cusps and **three** non-cuspidal rational points, with `j`-invariants
  `−11·131³ = −24729001`, `−2¹⁵ = −32768`, `−11² = −121`. A rational 11-isogeny
  would put `j(E)` among those three. Recomputed here,

  $$j(389.a1)=\frac{c_4^3}{\Delta}=\frac{112^3}{389}=\frac{1404928}{389},$$

  which is **not an integer**, so it is none of them.
* **Semistability and Mazur.** RUN-020 recomputed that `389` is the only bad
  prime and its reduction is `I₁`, so `E` is semistable; Mazur's isogeny theorem
  then allows a rational `p`-isogeny only for `p ∈ {2,3,5,7}`. The semistability
  is ours; the theorem is cited.

Either route is strictly weaker in what it assumes than "maximal image for every
`ℓ`", and the first is entirely finite.

### And what stays cited

| gate | ledger | this arm |
| --- | --- | --- |
| `P4-SHA11` | `CLOSED (imported exact project certificate)` | not checked — the Kurihara witness at `n = 397·991` plus the Chan-Ho Kim Selmer structure theorem |
| `P5-IMC11` | `CLOSED (Burungale–Castella–Skinner)` | not checked — an external theorem |
| `P5-BCS-IM-CONDITION` | `CLOSED (explicit unipotent certificate)` | not checked — the certificate is not reproduced here |
| `P5-MAZUR-TATE-WEAK11` | `CLOSED AS EXTERNAL THEOREM INPUT` | not checked — the ledger already labels it external |

`P5-GOOD-ORD11` is closed both ways and agrees: RUN-020 recomputed `Δ = 389` with
`11 ∤ Δ` and `a₁₁ = −4` with `11 ∤ a₁₁`.

## A defect in this round's own gate, found by the round

The first version of the status pattern used a word boundary — `\bCLOSED\b` —
and the underscore is a word character, so it does **not** match inside
`CLOSED_BY_PUBLISHED_COMPUTATION`. v0.6 writes every status that way. The scan
silently dropped **fourteen of forty-four rows**, including *both* readings of
`P5-BOC-NZ11`, which is the single gate the reconciliation exists to compare.
The first run therefore reported "3 gates with more than one status" and a clean
bill on exactly the gate that had moved.

A scan that under-reports produces a shorter table, not an error. So the drill
now pins the row count and five specific `(gate, status)` pairs, and restoring
the word boundary turns `p5-ledger-extraction` red.

## The drill

**91 defects, 91 caught by the check named for each — none uncaught, none
caught by the wrong check. 20 controls, none disturbed, over 42 checks. Twelve
minutes and forty-four seconds.**

Gate 24 contributes three checks and five defects, and one planted defect moved
to the controls with a reason about the pattern rather than about the corpus:

> `ROW` separates a gate name from its status with `\s{2,}`, which reads as
> load-bearing and is not. The gate-name character class already permits a
> space, so with a single-space separator the non-greedy quantifier and the
> later `.strip()` reproduce exactly the same split on every row in the corpus.
> What does the work is the non-greedy name and the strip.

The cycle detector is exercised on a synthetic two-gate cycle, because the
corpus has none and a detector that never fires would pass every real-data
check. The `X₀(11)` defect — dropping one of the three classical `j`-invariants —
is caught by the check pinning that list, and it would **not** have changed the
verdict, since `j(389.a1)` is in neither list. That is the reason to pin a
classical input rather than only its consequence: a corrupted list that happens
not to matter today will matter later.

## What this round does not claim

* **Nothing about BSD**, and nothing about whether any gate's *content* is
  correct. It reconciles what the documents declare and separates computation
  from citation.
* **Only four of the ten P5 documents carry a fenced ledger.** The other six
  declare statuses in prose, which this gate does not parse. The reconciliation
  is therefore over the machine-readable part of the chain, and a conflict
  stated only in prose would not be seen.
* **The two gates closed here are closed on stated grounds, not proved from
  nothing.** `P5-RESIDUAL-IRR11` route 1 uses the classical rational points of
  `X₀(11)`, cited; route 2 uses Mazur's isogeny theorem, cited. What is ours is
  the arithmetic each route needs — `j(E)` and the reduction type.
* **`P5-BOC-NZ11` is closed relative to `v1.3` §3's identification** of
  `det(𝓑_N)` with `det(M_loc)`, which this round reads rather than reproves.
