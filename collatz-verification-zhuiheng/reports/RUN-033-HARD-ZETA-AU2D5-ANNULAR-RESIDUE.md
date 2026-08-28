# RUN-033 — Hard-Zeta A-U.2d.5: the exact-code separation holds in both directions, every B-source really is 3 mod 4, and one section mixes an unconditional corollary with a cap that is vacuous on real orbits

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d5_Annular_Farey_Residue_Coupling_bundle_v0.1.zip` (source item 51). Ships a checker, its report, a constants frontier, a source-validation record and a stdout transcript.
**Tools:** [`src51_annular_residue.py`](../code/src51_annular_residue.py) · [`src51_drill.py`](../code/src51_drill.py) · [`src51_emit_report_block.py`](../code/src51_emit_report_block.py)
**Logs:** [`src51-au2d5.json`](../data/gate-logs/src51-au2d5.json) · [`src51-drill.json`](../data/gate-logs/src51-drill.json)

**Result: the mathematics holds. Section 4's exact-code arithmetic is verified in both directions — not only that realizing sources lie in the claimed class, but that every member of that class realizes the code. Section 6's residue corollary holds on 27,556 real sources with zero violations. The renewal identity and both determinants are exact in integers where the shipped checker reports a float residual. Four findings, none mathematical — and one of them is that section 6's own depth cap is vacuous on every orbit that exists.**

---

## Two more results that need no hypothetical object

RUN-032 noted A-U.2d.4 was the first round in this line whose core held on orbits
that exist. A-U.2d.5 adds two more, and both are pure integer arithmetic.

**Section 4.** For a code `w = (a₁…a_k)`, `Q = Σaⱼ`, `B_w = Σⱼ 3^{k−1−j} 2^{Aⱼ}`,
every realization from odd source `x` to odd endpoint `z` satisfies

> `2^Q z = 3^k x + B_w`

so one code selects one source class mod `2^{Q+1}` and one endpoint class mod
`3^k`, and a repeated code forces `|x−x′| ≥ 2^{Q+1}` and `|z−z′| ≥ 2·3^k`. No
CASP hypothesis appears anywhere in it.

**Section 6.** If the first crossing has `L ≥ 2` then `s+1` is a proper
subcritical prefix, so `q_{s+1} < β < 2`, so `q_{s+1} = 1`, so `v₂(3y+1) = 1`,
so **`y ≡ 3 (mod 4)`**. Again true of any orbit.

## Checked in both directions, which is the half that is usually skipped

"One code selects one source class" has two halves. That realizing sources lie in
the class is the easy one, and checking only that cannot tell *one* class from
*some* class. So the run also takes members of the claimed class the code was
never observed at — `x + m·2^{Q+1}` — and requires each to realize the same code.
**1,200 such members, zero failures.** Without that half the check would pass on a
class ten times too large.

## Finding 1 — section 6 mixes an unconditional corollary with a vacuous cap

The first half of §6 is unconditional and it holds: **27,556** real sources with
`L ≥ 2`, **0** violations of `q_{s+1} = 1`, **0** of `y ≡ 3 (mod 4)`.

The second half is not. The depth cap `r < 1 + U_β(L)/4 ≤ 1 + L/12` is derived
from the source corridor

> `4(r−1) < y_r − y₁ < U_β(L)`

and that right-hand bound is a **B-survival property**, not something a real orbit
owes anyone. Measured: of **10,214** real chains with distinct increasing sources,
**0** satisfy it. The cap is vacuous on orbits that exist — the same shape as the
surviving crossings RUN-023 measured zero of.

Nothing is wrong with the derivation. What is worth saying is that one section
carries a result testable on every orbit and a result testable on none, under one
heading, with no marker between them.

**This run got that wrong first.** Checking the cap without its premise flagged
**10,214 of 10,214** — a rate that is a statement about the check, not about the
round. A hundred-percent violation rate should always be read as a question about
the instrument first.

## Finding 2 — exact integers where the checker reports a float residual

The renewal identity `A_i + D_i = D_{i+1} + E_i` and both determinants are
`aβ + b` for integers `a, b`, so the residual is the **pair `(0,0)`**. Recomputed
that way: **27,556** edges, **0** errors. The shipped validation reports
`max_float_residual = 1.93e-12` for the same identities.

**Fourth round in this line.** RUN-027 (`U_β(L)` rational vs 80-digit `mpmath`),
RUN-029 (the exponent chain rational), RUN-032 (A-U.2d.4's identity integral),
and now this. The pattern is stable enough to state as one: *this line reaches for
higher precision where it could reach for exactness.*

## Finding 3 — two names one file, again; and constants that moved between bundles

`checker_stdout.txt` is **byte-identical** to the checker report — **second bundle
running**, after item 50, and the validation record lists both with the same hash.

Two constants shared with item 50 **changed value between the bundles**:
`disjoint_backbone_power` and `dense_overlap_required_power`. They are exact
rationals, so the two cannot both be the nearest double — and item 51's are the
exact ones, where RUN-032 measured item 50's at 1 and 2 ulps out. The artifacts
improved; nothing in either round turns on it.

## Finding 4 — the validation record changed schema, and my reader did not notice

Item 50's `SOURCE_VALIDATION` keys a dict by filename. Item 51 ships a **list of
records**. My reader, written for item 50, found **zero** files and would have
reported a clean bundle — the only reason it surfaced is a non-vacuity guard that
fails when fewer than five entries are verified.

That is exactly RUN-028's finding landing on my own code: *a reader that knows one
shape returns zero for the other, and the total still looks plausible.* The
shapes are now enumerated with the bundle that introduced each, and anything
neither shape **refuses** rather than contributing nothing. With that fixed: **8
of 8** listed files verify, and the single uncovered file is the record itself —
the one file a manifest cannot hash.

---

<!-- BEGIN GENERATED measured block: python code/src51_emit_report_block.py -->

| what | measured against | value |
| --- | --- | --- |
| **§4** affine identity `2^Q z = 3^k x + B_w` violations | exact integers, 400 random codes | `0` |
| …source class mod `2^(Q+1)` violations | forward direction | `0` |
| …endpoint class mod `3^k` violations | forward direction | `0` |
| …**class members that fail to realize the code** | the reverse direction, 1200 members drawn from the class itself | `0` |
| **§4.3** repeated-code pairs formed | the separation theorem's domain | `400` |
| …source gap not a multiple of `2^(Q+1)` | must be zero | `0` |
| …endpoint gap not `2·3^k·m` | must be zero | `0` |
| …smallest source gap seen, in units of `2^(Q+1)` | 1 means the bound is attained | `1` |
| shipped sample pairs recomputed from the code alone | 0 disagreements | `5` |
| **§6** real sources with `L ≥ 2` | of 54825 first-crossing sources on 2000 orbits | `27556` |
| …**`q_(s+1) ≠ 1`** | must be zero | `0` |
| …**`y ≢ 3 (mod 4)`** | must be zero | `0` |
| chains with distinct increasing sources | §6's own premise | `10214` |
| …**of those, inside the source corridor `y_r − y₁ < U_β(L)`** | the premise the depth cap needs | `0` |
| …depth-cap violations among those | vacuously zero | `0` |
| renewal identity errors | β-linear integer pairs over 27556 edges | `0` |
| …the residual the shipped checker reports | it evaluates in `float` | `1.9326762412674725e-12` |
| plateau / strict-drop edges | both branches must be inhabited | `16072 / 11484` |
| determinants that are not positive integers | must be zero | `0` |
| laminarity violations | 41539 nested, 137627 disjoint pairs sampled | `0` |
| the checker's own claims independently confirmed | of 8 it states; 1 not covered here | `7` |
| validation-record files verified | record shape: list of file records (item 51) | `8` |
| …uncovered files | the record itself (`True`) | `1` |
| constants differing from the exact rational's nearest double | of 5 checked | `1` |
| …**that moved between item 50 and item 51** | same quantity, two bundles | `2` |
| defects planted / caught by the check named for each | 1 robustness property; 0 malformed | `18 / 18` |

**Between the bundles.** `dense_overlap_required_power`: item 50 `0.16349486626119947` (2 ulp), item 51 `0.1634948662611994` (0 ulp); `disjoint_backbone_power`: item 50 `0.8365051337388005` (1 ulp), item 51 `0.8365051337388006` (0 ulp).

Every figure above is emitted by `code/src51_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

**Drill 18/18 by the check named for each, both controls clean, no malformed
mutations in the final pass.** D13 and D14 replant this run's own two mistakes —
the premise-free cap and the unrecognised record shape — so neither can return
quietly.

Two defects were re-aimed after the pre-flight named them. One renamed a key in
the cross-bundle comparison table, which **raises** rather than changing a result;
a robustness property has to leave the code valid or it tests the interpreter.
Sixth item running that the pre-flight has paid for itself.

**A second reader was used, once, and then stood down.** For claim enumeration
this run delegated §§5–11 of the round to GLM-5.3-Flash through MACR, whose
design assigns the worker no verification and no acceptance authority. Every
returned line was adjudicated by exact string match against the source, so an
invented claim would have been rejected mechanically: **7 of 7 accepted verbatim,
0 rejected, US$0.0037.** Two things came out of it worth keeping. MACR's
outbound-leak guard reads LaTeX set-builder notation `\{u>s:\delta_u…\}` as a
Windows drive path — measured with its own compiled pattern, **25 of 132**
Hard-Zeta documents (19%) would be refused and **every hit examined was
mathematics, with zero true positives**; the refusal is in the safe direction but
its pattern cannot separate the two, and a tighter regex I proposed **failed its
own test**. And per the operator's decision the same day, no further unpublished
material goes to a third-party provider until the sweep is complete and the AMRAL
authorship page exists; the remaining items are this arm's own work.

## Route map

`ROUTE_MAP v2.5`. Item 52 is `A-U.2d.6 — Farey-Order Entropy Collision`, which
this bundle's constants frontier names as the next round.

## What this run does not claim

1. That the master constraint of §11 holds. It quantifies over B-injection
   configurations in a CASP candidate; only its arithmetic was checked.
2. That §6's depth cap is wrong. It is **untested**, because nothing real
   satisfies its premise, and this run says so rather than scoring it either way.
3. That the corridor-threshold claim in the checker's own list was verified. One
   of its eight — "2-adic and 3-adic corridor threshold definitions dominate
   `U_β(L)`" — is **not covered here**; the other seven are independently
   confirmed.
4. That the shipped checker is correct. It was read, never run; what was compared
   is its published figures against an independent recomputation.
5. That the exact-code results say anything about Collatz. They are arithmetic
   about exponent codes, and the round says the same.
