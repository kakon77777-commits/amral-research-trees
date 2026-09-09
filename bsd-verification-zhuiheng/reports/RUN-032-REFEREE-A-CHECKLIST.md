# RUN-032 — Referee A's checklist, run as a program, and the direction it does not ask for

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`19_Independent_Referee_Handoff`](../../../amral/public/bsd/phase2/files/19_Independent_Referee_Handoff.md), Referee A — seven conditions on the base curve and five on a member of the support set, with an explicit instruction to output PASS/FAIL
**Tools:** [`src34_referee_a_checklist.py`](../code/src34_referee_a_checklist.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src34-referee-a.json`](../data/gate-logs/src34-referee-a.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Referee A's checklist runs, and the base curve is PASS over the four of its seven lines that are arithmetic — analytic rank 0, `E(Q)[2] = 0`, `Δ < 0`, `v₂(L^alg) = 0`. The other three — optimal, odd Manin, a rigorous source for `BSD(E,2)` — are reported as **cited**, not scored, because a checklist that marked a citation PASS would be reporting a source as a check. All 19 support-set members below 4,000 pass all five of the `q` conditions. And the round adds the direction the handoff does not ask for: of 200 primes `≡ 1 (mod 4)` that the corpus's own membership test **rejects**, none passes Referee A's five — so the checklist and `𝒫` agree about who is in the family. Checking only the members could never have seen a disagreement.**

---

## What the handoff asks for

`19_Independent_Referee_Handoff` opens with an instruction that is unusual and
worth quoting:

> 不要再搜尋更多 curves。先嘗試推翻：`696.e1` family theorem.

Stop looking for more curves; try to break this one. Referee A then gets a
checklist and the instruction **輸出 PASS/FAIL**.

## The base curve

| line | | measured |
| --- | --- | --- |
| optimal | **cited** | — |
| odd Manin | **cited** | — |
| analytic rank 0 | **PASS** | 0 |
| `BSD(E,2)` rigorous source | **cited** | — |
| `E(Q)[2] = 0` | **PASS** | the 2-division cubic has no rational root |
| `Δ < 0` | **PASS** | `−178,176` |
| `v₂(L^alg) = 0` | **PASS** | `L/Ω = 1`, and `ord₂(1) = 0` |

**PASS over the four arithmetic lines; three cited.**

The split is the point. *Optimal* is an isogeny-class statement whose premise
RUN-031 closed one round ago — no rational `n`-isogeny at any of Mazur's twelve
degrees — but which curve the modular parametrisation lands on is a statement
about `X₀(696)` and is not computed here. *Odd Manin* is the Manin constant,
cited in `24_Manin_Period_Audit`. *`BSD(E,2)` rigorous source* is a citation to
the verification of BSD to conductor 5000, which is a source and not a
computation.

Scoring those three PASS would have produced a seven-line PASS that meant less
than the four-line one.

## The support set

19 members below 4,000 — `241, 313, 457, 673, 937, 1009, 1153, 1753, 2017,
2089, 2113, 2137, …` — and **every one satisfies all five conditions**:
squarefree, `gcd(q, 696) = 1`, `q ≡ 1 (mod 4)`, `2, 3, 29` split in `Q(√q)`, and
`q` inert in the 2-division cubic.

The two smallest are 241 and 313, which are the members RUN-015 computed
`L(E^{(241)},1)` and `L(E^{(313)},1)` for, and where it found `#Ш(E^{(313)}) =
49 = 7²`.

## The direction the handoff does not ask for

Referee A is asked to verify the conditions on `q ∈ 𝒫`. That checks the members
and nothing else, and it cannot detect the failure that would matter most: a
prime the corpus's membership test **rejects** that nonetheless satisfies every
one of Referee A's conditions. That would mean the checklist and `𝒫` disagree
about who is in the family.

So the gate runs it: **200 primes `≡ 1 (mod 4)` rejected by the membership test,
of which 0 pass all five.** They agree.

This is the same shape as RUN-008, which checked the census's *kept* curves
because the census's own tests were structurally blind to that direction. A
condition list verified only on the set it defines has been asked half a
question.

## The drill

**136 defects, 136 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 22 controls undisturbed, over 62 checks.

The 2 planted for this gate, each turning `referee-a-checklist` red and nothing else:

| planted defect | went red |
| --- | --- |
| Referee A's q-conditions drop the 2-division-cubic inertness | `referee-a-checklist` |
| Referee A's cited lines are scored as machine-checkable | `referee-a-checklist` |


## What this round does not claim

* **PASS over four lines is not PASS over seven**, and the report says so in
  both places rather than in a footnote.
* **The five `q` conditions are checked below 4,000.** RUN-015 checked the root
  number over 20,000 and RUN-009 the density over 2×10⁷; this bound is the
  checklist's, not the family's.
* **Agreement between the checklist and `𝒫` is agreement between two
  formulations**, both from the corpus. If both encode the same mistake, this
  round would not see it — what it rules out is the two drifting apart.
* **Referees B and C are untouched.** B checks the odd branches' theorem
  hypotheses and C the Fouquet–Wan hypotheses; both need reading of external
  theorems rather than arithmetic, and neither is attempted here.
