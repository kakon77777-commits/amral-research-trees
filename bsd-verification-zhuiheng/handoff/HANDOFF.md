# BSD verification line — complete handoff bundle

**From:** 數學戰士「墜衡」(Zhui Heng), the independent verification arm of AMRAL Research Lab (EveMissLab, Neo.K)
**Line:** `bsd-verification-zhuiheng`, branch `agent/bsd-verification-zhuiheng` of `kakon77777-commits/amral-research-trees`
**State at handoff:** 69 rounds, RUN-001 … RUN-069; all 85 curated documents of the corpus have been a round's subject; 97 checks, 294 planted defects all caught by the check named for each, 60 controls undisturbed
**Provenance of this copy:** see `MANIFEST.json` (git commit, SHA-256 of every file, the drill and sweep totals as read from the logs)

> **給 Neo 的一段。** 這個包是這條線的全部：驗證樹（程式、69 份報告、每個閘門的存檔 log）、語料 85 份、25 個研究包的原始 zip、Phase 1 普查包（八個閘門要讀它）、見證那條線的 Kurihara 交叉驗證包、以及 git bundle（69 輪的 commit 訊息就是敘事）。第 5 節是「已驗證的」與「還開著的」，用語料自己的標籤；第 7 節是接手的人可以做什麼。任何人拿到這個包，不需要網路、不需要 Sage，Python 3.11 加 git 就能重跑每一個閘門與整個 drill。

---

## 1. What this is

The corpus is Neo.K's BSD research line: 85 curated documents in four sub-lines
(Phase 0 framework, P5 = 389.a1 at p = 11, Phase 1 = a 500,000-conductor
census after Banwait–Huang, Phase 2 = an infinite non-semistable twist family
of 696.e1), archived as 25 research packages. **This bundle is the verification
line that walked all 85 of them**, one gate per round, recomputing every figure
it could reach with its own code, never running the corpus's scripts, and
drilling every gate with planted defects that must be caught by the check named
for them.

Nothing in this bundle bears on the Birch and Swinnerton-Dyer conjecture as a
theorem. No document in the corpus claims to prove BSD, and this line makes no
claim the corpus does not. Every result has the form *curve X, prime p, reached
rung C_N* on the corpus's own eleven-rung certificate ladder (Phase 0 doc 03),
never a bare verdict.

## 2. Layout of the bundle

```
HANDOFF.md                                   this file
MANIFEST.json                                provenance + SHA-256 of every file
amral-research-trees/
  bsd-verification-zhuiheng/                 THE TREE (git HEAD of the branch)
    README.md                                method, the round table (all 69), layout
    code/src00 … src71_*.py                  one gate per round; census_pkg.py resolves the census package
    code/src11_gate_drill.py                 the mutation drill (--shard k/n, --merge)
    code/run_sharded_drill.sh                8-way parallel drill + merge
    reports/RUN-001 … RUN-069-*.md           one report per round
    data/gate-logs/*.json                    the archived output of every gate — what every number in a report cites
    data/external/                           the ecdata shard fetched at a pinned commit (+ provenance), twist-map completeness on all 36,687 curves
amral/public/bsd/{phase0,p5,phase1,phase2}/files/   THE CORPUS: 85 curated .md, exactly as the site serves them
amral/public/bsd/stress-test/files/          the Witness line's stress-test audit incl. its Kurihara certificate package (cross-line reference, read-only)
census/BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12/   the Phase 1 census package (inputs, results, sources) that eight gates read
research-packages/                           the 25 archived research packages (zips) + the RUGZPB v0.1 note, byte-exact from the drop zone
git/bsd-verification-zhuiheng.bundle         git bundle of the branch — 69 rounds of commit messages, each a full account of its round
```

The relative layout matters: gates locate the corpus at
`../../amral/public/bsd/...` from the tree, and the census package via
`code/census_pkg.py` (environment variable `BSD_CENSUS_PKG`, else the original
machine path, else `<bundle>/census/<package>`). Keep the layout, or set the
variable.

## 3. Verify the bundle

```
python -c "import json,hashlib,pathlib;m=json.load(open('MANIFEST.json',encoding='utf-8'));bad=[f for f,h in m['files'].items() if hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()!=h['sha256']];print('files',len(m['files']),'mismatches',bad)"
```

The git bundle: `git bundle verify git/bsd-verification-zhuiheng.bundle`, then
`git clone git/bsd-verification-zhuiheng.bundle -b agent/bsd-verification-zhuiheng`
gives the full history. The tree in `amral-research-trees/` is that branch's
HEAD (commit in `MANIFEST.json`), tracked files only.

## 4. Run it

Requirements: **Python 3.11+ standard library only** (no NumPy, no Sage, no
network), and `git` on PATH for one gate (`src68` reproduces a line diff with
`git diff --no-index`). Everything runs from the tree directory.

```
cd amral-research-trees/bsd-verification-zhuiheng

# one gate — writes its log to data/gate-logs/ and exits 0 iff every one of its checks agrees
python code/src70_kurihara_modular_symbols.py       # ~10 s: modular symbols for Γ₀(389) mod 11, the Kurihara number
python code/src67_phase0_maps.py                    # ~1 s
python code/src29_sweep_coverage.py                 # the sweep: 85 documents, which bucket each is in

# the drill: every planted defect must be caught by the check named for it
python code/src11_gate_drill.py                     # single process, ~3–4 h
bash code/run_sharded_drill.sh 8 /tmp/drill         # 8 shards + merge, ~45 min on a laptop
```

Expected at handoff: the sweep prints `subject of a report 85`; the drill ends
with `294 defects, 294 caught by the check named for them`, `uncaught by any
check: 0`, `caught by the wrong check: 0`, `60 controls, 0 disturbed a check`,
`state restored afterwards: True`. A gate's log is deterministic; re-running a
gate and diffing its log against the archived one is a legitimate check on this
bundle (the `seconds` fields will differ; nothing else should).

The slow gates are the ones that recompute the census from scratch (`src04`,
`src06`–`src08`, `src13`, `src57`, `src65`'s full completeness is a separate
tool, `code/tools_full_completeness.py`, ~17 min); everything else runs in
seconds. The drill's checks use samples where a full gate is slow, and say so
in their docstrings.

## 5. What is established, and what is open

**Read the labels, not this summary.** The corpus labels its own claims
(`CLOSED_EXACT`, `OPEN`, `NO_GO`, `unknown`, `DERIVED THEOREM CANDIDATE`); this
line records for each whether the figure recomputes, and never promotes a label.
The full round table is in the tree's `README.md` (§ Rounds) and is appended
to this file at build time; each row links its report and its gate.

### 5.1 Verified here — the strongest statements, by sub-line

| sub-line | recomputed independently in this tree | rounds |
| --- | --- | --- |
| Phase 1 (census) | every discriminant, conductor and valuation of the 40,749 base curves; all 122,247 rational-isogeny determinations for n ∈ {3,5,7} decided both ways via X₀(n); all 247,391 twist pairs rebuilt; Theorem 2.18's conditions E1–E7 and both branches on every curve and pair; twist-map completeness in both directions on all 36,687 stable curves under the stated bound d < 1000; Algorithm 1's three rule versions read from the diffs and tested on the data; Algorithm 2's OLD→CURRENT replay to the cell; the four adversarial curves rejected 4/4; the ecdata pin shown to reproduce only after CRLF conversion; the +1899/−53404 line diff accounted for line by line (0 new twists) | 004–008, 012, 016, 055–057, 060–063, 066 |
| Phase 2 (696.e1 family) | density 1/24 (not the naive 1/48) with 0 violations over 79,204 primes; the real period corrected and the BSD identity closing; the 696.e1 certificate; mod-ℓ images certified maximal for 38 primes, blocked twice at 3; FW-H3's certificate false as stated at exactly one prime, the family surviving; **Lemma B reduction**: FW-H2 at the twisting prime decided by the congruence a_q² ≡ 1 (mod q) without the kernel polynomial — 18 of 19 members pass, **member q = 3529 fails**; the Chebotarev audit; the corpus's H2 chain consistent; the corpus disagreeing with itself about H3 (02 vs 08) | 009, 017, 030, 036, 037, 044–046, 057 |
| P5 (389.a1, p = 11) | the localization matrix M_loc = [[1,2],[1,4]], det 2; every exact figure of v1.1 §2/§5/§7 from the group law up (P′ generates both finite groups, the discrete logs, ρ surjective with image 390,830, J_S = 1); **the Kurihara number δ₃₉₇·₉₉₁ = 5 (mod 11)** from modular symbols built in this tree, at the disclosed scale λ(1,5) = 1, with the same 392,040 terms as the Witness line's package — the manuscript's "6" is an undisclosed scale and stays unreproduced; θ̄ₙ ≡ 5·X₃₉₇X₉₉₁ (mod I³) with the other five coefficients 0; the rank-1 Kurihara numbers 0; det(B_N) = 2·XY in the group ring; ρ̄_{E,11} surjective by Frobenius witnesses; E(ℚ₁₁)[11] = 0; c₃₈₉ = 1 | 011, 020–022, 067–069 |
| Rank identities | the rank-2 BSD identity at 389.a1 closes to machine precision **with #Ш = 1 as input** (BSD-inferred, not computed); the rank-1 identity at 37a1 and 43a1 with every term computed here | 023, 026 |
| Phase 0 (framework) | ladder vocabulary across all 85; the rejected lattice-rank route does not recur (0 of 85 documents claim its conditions met); the certificate globalizer faithful in ℚ and not in float64; the agent experiment against its own freeze conditions; the three maps scored against 64 rounds | 002, 003, 013, 025, 065 |

### 5.2 Open — in the corpus's own words, untouched by this line

| gate | where it is declared | what it asks |
| --- | --- | --- |
| `P5-ANOM-BocCOMP₁₁⁽²⁾` | P5 v1.1 §9–10 | an integral anomalous finite Bockstein/extended-height regulator for the rank-2 lattice and {397, 991}, valid when 11 ∣ #E(F_ℓ), whose image in I²/I³ matches [θ̄ₙ]₂ up to an 11-adic unit |
| `P5-CANON-BocID₁₁⁽²⁾` | P5 v1.3 §6 | that the finite operator B_N is, as a canonically normalized element, the Bockstein regulator of Burns–Kurihara–Sano / Nekovář |
| `P5-CPLX-GPR₁₁⁽²⁾` | P5 v1.3 §6, RUGZPB P5 | the derived arithmetic determinant against L⁽²⁾(E,1)/2! / (Ω⁺·Reg_∞) — the rank-2 leading-coefficient comparison |
| RUGZPB P6, P7 | RUGZPB §9 | all-prime gluing of the fixed-prime closure; the rank-2 wall atlas across several curves |
| FW-H2 at q = 3529 | RUN-057 | the one family member below 4000 whose twisting prime fails a_q² ≡ 1 (mod q); the corpus's LOCAL_H2 stays `unknown` there |
| the H3 dispute | RUN-046 | Phase 2 docs 02 and 08 disagree about FW Theorem 1.7's local condition; this line runs both readings and has asked Neo.K to rule |
| Ш, twice | Phase 0 doc 02 §5; RUN-065 | of the seven components of a strong-BSD certificate, "Ш finite" and "the order of Ш" were never computed anywhere in this line; the regulator was computed without saturation being verified |
| the four open rows | Phase 0 doc 02 §8 | weak BSD at rank ≥ 2; Ш finite in general; the full leading coefficient; all E/ℚ — open in the corpus, and no report of this line says otherwise |

External inputs this line took as records and did not compute: rank(389.a1) = 2
(no descent in this tree), the Manin constant, Kim's Theorem 1.8 and
Castella–Sano's nonvanishing theorem, FW's theorems, LMFDB labels. Each is
named in the report that uses it.

## 6. The rules this line ran under

A successor that keeps these can trust the bundle's figures; one that drops
them should say so.

1. **Recompute; never run their script.** A package's own verifier passing shows self-consistency, not correctness. This line has never executed a script from the corpus; where a figure could not be recomputed it is marked `unmeasured` or `not recomputed here`, never inferred.
2. **A gate is not evidence until it has been drilled.** Every check must catch a planted defect *by name*, and controls (perturbations that must not trip) are planted alongside. A check that has only ever been green is indistinguishable from a comment. RUN-042's lesson: a check that has only seen passing data is untested — build the negative control (RUN-062's four adversarial curves).
3. **Numbers are emitted, never typed.** Every figure in a report traces to an archived log; the drill tallies are filled into reports by a script from the log. RUN-029's rule — *a number from memory is a number from nowhere* — caught three of four a-invariants typed from memory at RUN-062 and a typed "25 of 25" at RUN-064.
4. **Score a document against what it claims**, not against a pipeline it declines (RUN-054, 056, 061: N/A by scope is a verdict).
5. **A finding from data may already be in an unread document.** Grep the corpus before writing "identified" (RUN-060's correction to RUN-055).
6. **A reading is not a computation.** Where a round maps rounds to rows (RUN-050, 064, 065), the mapping is kept in one place and everything computable about it is computed: cited rounds exist, attributed findings are found by signature phrase, prohibitions are scanned.
7. **Corrections stay visible.** Errors of this line are recorded in the round that found them and in a correction note on the round that made them (RUN-006, 017, 026, 055, 056, 064). Nothing is silently rewritten.
8. **Independence across lines.** The Witness line's Kurihara package and this line's RUN-068 share no code; their agreement to the term (raw sum 43,605,160) is evidence precisely because of that.

## 7. What a successor could do next

Listed in the order this line would have taken them. None is required to
understand the bundle; all are what the corpus itself says is next.

**A. The open gates of §5.2, in the corpus's own terms.** The P5 chain has been
reduced, by the corpus and now by verification, to two comparisons at one
curve and one prime — `CANON-BocID` and `CPLX-GPR`. Everything finite around
them is now computed three ways. A theorem-level attack on either would be the
first thing in this corpus that moves an `OPEN` label.

**B. Pave toward formalization.** The finite statements verified here are
candidates for a proof assistant (the comparator this line identified is the
BSD statement in `google-deepmind/formal-conjectures`, `BSD.lean`). In
increasing order of weight:
- 389.a1 arithmetic (RUN-067): #E(F₃₉₇) = 374, #E(F₉₉₁) = 1045, the discrete logs, the surjectivity of ρ — decidable, small, exact;
- the Lemma B reduction (RUN-057): `FW-H2(E_q, q) ⟺ a_q² ≡ 1 (mod q)` at a good ordinary prime, given ρ̄_{E_q,q} ≅ ρ̄_{E,q} ⊗ χ_q and twist-invariance — a lemma with a two-line proof and a computable hypothesis;
- the modular-symbol computation (RUN-068): the mod-11 plus-eigenline of Γ₀(389) and δ ≠ 0 — a finite linear-algebra fact whose statement is elementary, whose *meaning* (via Kim's theorem) is not; formalizing the computation is feasible, formalizing the theorem is a project.

**C. What would count as completing something.** On the corpus's ladder, this
line's strongest rungs are C1 (local arithmetic, everywhere), C2/C3 at the
specific curves, and C7/C8-type statements only at (389.a1, 11) and only as
*"the finite input to Kim's theorem is verified"*. Moving 389.a1 to C9 needs
`CPLX-GPR`. Moving the 696.e1 family to C10 needs FW-H2 at 3529 (or a reason
it can be excluded) and the H3 ruling. Neither is a computation.

**D. What not to do.** Do not report a rank computed by a floating-point
routine as a proof (Phase 0 doc 03 forbids it; RUN-013 measured why). Do not
promote the ratio 6/2 = 3 or 5/2 = 8 to an invariant (RUN-069 shows it takes
every value in F₁₁^×). Do not close an `OPEN` gate by citing this bundle: it
verifies inputs, not theorems.

## 8. Corrections this line made to itself

Recorded because a verification line that hides its own errors is not one.
RUN-006 (a float scan gave an impossible answer; `9·b₈` should have been
`27·b₈`), RUN-017 (a real period wrong for three rounds, found by the BSD
identity), RUN-026 (a control whose reason had been a consequence of the defect
it repaired), RUN-055 → RUN-060 (an identity presented as new that `15` §8
already stated), RUN-056 (a pin row corrected after RUN-062's CRLF finding),
RUN-062 (three of four a-invariants typed from memory were wrong), RUN-064 →
RUN-065 ("25 of 25" typed; the instrument said 23 + 2). Each has a note in the
report it corrects.

## 9. Contact and identity

This line is one named identity's work — 墜衡 (Zhui Heng), an AI verification
arm run by Neo.K at EveMissLab — and is presented as such. Its counterpart
lines (Witness's stress-test audit, the corpus's own `agent/bsd` archive) are
included where this line cites them and are not edited by it. Questions about
the corpus go to Neo.K; questions about a figure in this bundle are answered
by the gate log it cites.

---

*The round table from the tree's README follows, appended at build time.*
