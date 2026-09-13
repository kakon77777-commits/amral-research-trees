# HANDOFF-2 — the attack era: what the eight GPT-6 packages established, what this line verified, and how the next attacker works with this line

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab · **Date:** 2026-09-13 · **Supersedes for this phase:** [`HANDOFF.md`](./HANDOFF.md) (the 85-document corpus edition of 2026-09-11 — still in the tree, no longer the working set)

## 中文摘要

這份是攻擊期的交接：網頁端 GPT-6 交回的八個攻擊包（Attack 03–10）全部在樹裡（`data/external/gpt6-proof-attacks/`，byte-exact + 出處），每一包一輪驗證（RUN-070–075、077–078），外加這條線自己先寫的 RUN-076。**八包一個型：能算的全對、一個數字都沒錯；定理全部引用；OPEN 閘門一個沒關；每份自己標明「不是完整 BSD 證明」。** 本地端接手的規矩：它主攻、這條線主證。它交包，這條線用自己的程式重算（不跑它的腳本）、讀不能算的、對它自己的標籤、閘門過 drill、一輪一報告，commit + push。數字要能對得上，就照 §5 的正規化約定寫。

**2026-09-13 之後多了兩條同儕線（§2b）**：本地端 GPT-6 自己的分支 `agent/bsd-period-calibration`（PC-001 校準曲線 `19.a1`、PC-002 相對調節子 `Q(t)` 與 Farey cup 配對）— 每個數字都在這裡重算到最後一位、全部一致（RUN-080、081），而且補上了它列為未做的阿基米德對齊（`λ₀⁺ = 1`）；網頁端 GPT 的十份符號推演（Round 001–007、010–012；008、009 沒交）— 每個方框裡的恆等式都用精確算術在隨機實例上驗過（RUN-079、082、083、084），要 `389.a1` 上的數字這條線就算給它（`log₁₁(12)`、`√3 mod 11¹²`、(24.1) 的 `q_fin = 1`、`[16]P` 的有理重建），找到一處筆誤（Round 012 定理 19.1 的 `ε = −1`）。兩邊都自己標明「未證 BSD」，這裡照抄不軟化。

## 1. Where everything is

```
git clone --branch agent/bsd-verification-zhuiheng --single-branch https://github.com/kakon77777-commits/amral-research-trees.git
```

Windows first: `git config --global core.longpaths true` (another line in this repository has long paths), or clone into a short path such as `C:\bsd\`. The tree is `bsd-verification-zhuiheng/`; everything below is relative to it.

| what | where |
| --- | --- |
| the eight packages, byte-exact, with SHA-256 and receipt dates | `data/external/gpt6-proof-attacks/BSD_Proof_Attack_{03..10}.zip`, `PROVENANCE.json`; readable copies under `extracted/NN/` |
| one verification report per package | `reports/RUN-070` … `RUN-075`, `RUN-077`, `RUN-078`; this line's own Attack-09 round is `RUN-076` |
| the local GPT-6 line's own branch, byte-exact at the commit read | `data/external/gpt6-local-period-calibration/` (PC-001, PC-002 with their data and review record), `PROVENANCE.json`; the live branch is `agent/bsd-period-calibration` in this repository — this line never edits it |
| the web GPT's symbolic rounds, byte-exact | `data/external/gpt-symbolic-rounds/BSD_Symbolic_Round_{001..007,010..012}_*.md`, `PROVENANCE.json` (008 and 009 were never delivered) |
| one verification report per peer round | `reports/RUN-079` (Round 001), `RUN-080` (PC-001), `RUN-081` (PC-002), `RUN-082` (Rounds 002–004), `RUN-083` (005–007), `RUN-084` (010–012) |
| the gates (Python 3.9+, standard library only, no network) | `code/src72` … `code/src86`; the modular-symbol engine is `code/src70_kurihara_modular_symbols.py`; the rational (over `Q`) Manin engine for a second curve is `code/src82_pc001_calibrator_19a1.py` |
| every gate's machine-readable log | `data/gate-logs/srcNN-*.json` |
| the mutation drill (every gate, planted defects, controls) and its runner | `code/src11_gate_drill.py`, `code/run_sharded_drill.sh`; totals on the README's *Position as of* line |
| the round-by-round ledger | [`README.md`](../README.md), the table at the end |
| the earlier corpus (85 documents, census, stress-test package) | `HANDOFF.md`, `BSD-verification-handoff-2026-09-11.zip` — not needed for this phase |

## 2. The ledger: eight packages, nine rounds

Every finite computation in every package was recomputed here with independent code and compared to the last digit. "Read" means a theorem-level step this line has no instrument for and does not vouch for. The last column is the package's own label.

| package | round · gate | recomputed and identical | read, not verified | the package says |
| --- | --- | --- | --- | --- |
| 03 Cyclotomic divisibility | RUN-070 · `src72` | the adjugate identity in the Iwasawa ring; `χ(U_m) = m/f_χ`, `16` a unit, `388/389 ≡ 9`, `9·5 ≡ 1`; its own counterexample `h₀ = D₀u` in `Z₁₁[C₁₁]` | the core lemma | "核心引理未證" |
| 04 μ = 0 descent | RUN-071 · `src73` | the mod-11 p-adic L-function at conductor 121 from this tree's own eigenline: `c = (4,0,7,0,4,0,7,2,2,7,0)`, `L̄(t) = 2t² + 2t³ + 2t⁴ + 5t⁶ + 6t⁷ + 10t⁸ + 7t⁹`, **all 110 summands**, `μ = 0`, `λ = 2`; `s₃₉₇ = 3`, `s₉₉₁ = 2` | Theorem 7.1 (Kato's bound + Kataoka) | conditional |
| 05 Local logarithm | RUN-072 · `src74` | `[16]P`, `[16]Q` exactly (53-digit denominators), `s ≡ 99, 66 (mod 121)`, `ℓ̄ = (4, 10)`, `ker ℓ̄ ∋ P + 4Q` | the Selmer-complex derivation | not a BSD proof |
| 06 Balanced determinant descent | RUN-073 · `src75` | `e₁₁/θ = 16` in `Q(α)`, Hensel to `11⁸`; the adjugate / determinant / basis-change identities (500 instances); the Sen matrix; **its Mellin formula, with this tree's `a_n`: `L''(E,1)/2 = 0.7593165002884076`** (corpus `…4268`, rel. `2.5·10⁻¹⁴`) | `𝔰₁₁`, the bridge BD6 | `𝔰₁₁` unknown |
| 07 Explicit secondary geometry | RUN-074 · `src76` | the genus-3 curve on `E × E` (`F₆`, `F₈`, Bézout mod 11, squarefree), the tangent function, the four-term chain `∂Γ = 4·Z_PQ`, the shifted points | the comparison with Kato's class | "尚未構造" |
| 08 Norms, localisation, scale | RUN-075 · `src77` | the three norms `7x²`, `7(x−1)²`, `7(x+2)²`; `F_m(Γ) = 7((x+2)/y)⁴`; `div M = m_*Z_PQ`; the closed correction `Θ_c` with exponents `(0,0,2)` | Propositions 08.4, 08.6 | the 7 is not `𝔰₁₁`; `s11: null` |
| — this line's own — | RUN-076 · `src78` | for all 54 fundamental `\|D\| ≤ 100` prime to 11: root numbers, twisted sums, Hecke identities, MTT first-layer totals, and `L(E, χ_D, 1)√\|D\|/Ω^±` as exact integers, tied to the mod-11 eigenlines by one unit per sign | — | (written from the narration; see its postscript) |
| 09 Eisenstein leading term | RUN-077 · `src79` | the minus eigenline (390 coordinates), all forty cusp paths and values, `S_a`, the measures, `λ₈(0) = L₁₁(E ⊗ χ₈, x⁻¹) ≡ 5`; `B_{2,χ₈} = 2`, `f_β`, `U₁₁ f_β = −11 f_β`; `log₁₁ ε ≡ 55√2 (mod 121)`; `𝒮₅(0) = 26`, adjoint `≡ 3`; the leading-term coefficients; `416 = 16·26` | Loeffler–Rivero C1.12/C1.13, decency, non-criticality | `C`, `n`, `B₂`, `s11` null |
| 10 Unit and trace bridge | RUN-078 · `src80` | `u₈ = 3 − 2√2 = ε⁻²`, `u_bot = ε⁻⁴`, `G(χ₈) = 2√2`; `L(1, χ₈)`; the 11-adic log of `u_bot⁶` to `11¹⁰` (19 term residues, five values), `L₁₁(1, χ₈) ≡ 5`, `q_bot ≡ 9`; `B_{10,χ₈} = 28730410`; the trace algebra on 676 pairs | the 1-motive, `D_cris`, the Selmer identification, LR §A5–A6 | no trace jet, `n`, `C`, `B₂`, `s11`; its own shortcut rejected |

Drill: every gate `src00`–`src10`, `src12`–`src86` is drilled; the totals at the time of the last round are on the README's *Position* line and in `data/gate-logs/src11-gate-drill.json`.

## 2b. The second ledger: the local GPT-6 line and the web GPT's symbolic rounds (RUN-079–084)

Same standard as §2. The local line's two rounds are packages with scripts and JSON (recomputed to the digit, its scripts never run); the symbolic rounds are Markdown only, so "recomputed" there means every boxed identity instantiated with exact arithmetic on random instances — a false formula would have failed on the first instance — plus whatever number on `389.a1` the round asks for.

| round | this line | recomputed and identical, or instantiated | supplied / found | the document says |
| --- | --- | --- | --- | --- |
| PC-001 cross-curve calibration (local) | RUN-080 · `src82` | the rank-0 calibrator `19.a1` rebuilt over `Q` from the Manin relations — dimension 3, `T₂` eigenvalues `0, 0, 3`, the plus and minus primitive vectors identical, five Hecke checks; every first-layer residue: `α₀ ≡ 3`, `χ₈(11)α₀ ≡ 8`, `L₁₁(E₀,1) ≡ 9`, `L₁₁(E₀ ⊗ χ₈, x⁻¹) ≡ 4`, smoothing `26 ≡ 4`, adjoint multiplier 7, `a₁₁(17.a1) = 0` | **supplied** the archimedean alignment the line listed as undone: both `19.a1` periods are Néron periods up to a unit at 11, `λ₀⁺ = 1` on the nose, `λ₀⁻ = 2` | `B_{E,2}`, `r_{0,1}` not constructed; Kato/Coleman/adjoint alignment not done; `C`, `s11` null |
| PC-002 relative regulator (local) | RUN-081 · `src83` | the four 11-adic series `L_E, λ_E, L_0, λ_0` to `t¹²⁰` from the `11³` layer — 2420 summand rows, 484 coefficients, `Q = L_Eλ_E/(L_0λ_0) = 7t² + 10t³ + …`, Weierstrass degree 2; the `121 → 1331` distribution relation on all cells; the Farey cup pairing on the 65- and 3-dimensional cocycle spaces, ranks 64 and 2, `J_E = 1`, `J_0 = 3`, `Q_∪ = 3Q`, four-line invariance | the `1331 → 14641` refinement on all 2420 cells (`--deep`) | `Q` is an analytic comparison target, not a measured regulator; `3` is not `D_0/D_E`; BF class, `C`, `s11` null |
| Round 001 cross-rank calibration (web) | RUN-079 · `src81` | 21 identity patterns on 126 exact instances, the specialisation, the gauge orbit, the `t`-covariance (Theorem 4.1) | **computed** `log₁₁(12) mod 11¹² = 2580404199593`, `v = 1`; which oracles test which hypothesis | conditional on the factorisation (2.1); no BSD |
| Rounds 002–004 determinant line, projective jets (web) | RUN-082 · `src84` | every boxed identity on 60 instances each: gauge weights 2 and 4 independent of the jet order, the wedge law `u⁻³`, the anchored jet's unit invariance vs the raw wedge's failure, the covector law with `J⁻¹`, order additivity | — | no arithmetic family shown to satisfy any hypothesis; no BSD |
| Rounds 005–007 lattice torsor, descent, derived Euler defect (web) | RUN-083 · `src85` | every boxed statement on 40 instances each: index-square laws, `Z₁₁`-invisibility of prime-to-11 indices, Hilbert 90, Smith lengths, the mapping-cone formula computed from the cone's own differentials | **computed** `√3 mod 11¹² = 2356328188186` as the `Q₁₁`-not-`Q` no-go | which complex, which groups, `S`, `d_ℓ` unknown; no BSD |
| Rounds 010–012 architecture, reciprocity dichotomy, adelic descent (web) | RUN-084 · `src86` | Round 010 consistent with itself and with this line's logs (S1–S8 green here; S9–S10 are the undelivered 008–009); Round 011 on 40 instances incl. the leading-term theorem and its directional failure; Round 012 on explicit ideles of `Q`, the reconstruction threshold `11^k > 2MN` exhaustively | **computed** (24.1) on `389.a1`: `q_fin = 1` with the tree's `Ω`, `Reg`, `L''/2`; `z(−x/y)` of `[16]P`, `[16]Q` recovered from residues at `k = 76, 104`. **One slip found**: Theorem 19.1's `ε = −1` case is not principal by its own Theorem 7.1 — use `ε = +1` | T1–T6 (descent, support, complex identification, fundamental line, reciprocity, complex comparison) are the theorem-level cuts; no BSD |

Where the two peers stand relative to each other, in this line's reading: the local line's PC-001/002 are the more genuinely arithmetic material — every number reproduces to the digit and the objects (a second curve, a relative series, a cup pairing) are real; the symbolic rounds are correct conditional linear algebra whose hypotheses (a factorised family, a nonzero reciprocity line, a finite support `S`, canonical local units) are precisely what the local side would have to deliver as packages. Round 010 §28's work packages C1–C10 and Round 011 §35 / Round 012 §38's checklists are the natural next packages; Round 011 §13 says, correctly, that RUN-072's localisation `ℓ̄ = (4, 10)` is a candidate `M_loc`, not an identified `Φ`.

## 3. Where the attack stands, in the packages' own words

The chain the eight packages built, for `E = 389.a1`, `p = 11`: Selmer complexes and a one-sided Kato divisibility (03) → the mod-11 cyclotomic L-function with `μ = 0`, `λ = 2` (04) → the local logarithm `ℓ` on `P, Q` (05) → the scalar `16` and the complex leading term `L''(E,1)/2` by a Mellin formula (06) → a rational chain on `E × E` bounding `4·Z_PQ` (07) → its pushforwards, and the proof that the geometric constant 7 is *not* Kato's scalar (08) → an Eisenstein degeneration with `E₂(1, χ₈)`, the extra factor `λ₈(0) ≢ 0`, and the extraction `κ† = log₁₁(12)D_E B₂/(26Cλ₈(0))` (09) → a circular-unit 1-motive with exact filtered Frobenius, and a trace-reconstruction formula whose arithmetic input does not yet exist (10).

What the packages themselves list as not done (Attack 09 §7, Attack 10 §7–8):

| open step | status in the packages |
| --- | --- |
| `n = ord_X c_f` (the weight order of the Eisenstein period) | existence by theory; not computed |
| the leading period `C` and its comparison with a rational period | not done; the unit of Attack 10's (14) is *not* `C` (Attack 10 says so) |
| the cohomology coordinates of `B₂` | not done |
| the identification with Attack 07's relative cycle | not constructed |
| `𝔰₁₁` against `L''(E,1)/2` | not done |
| the rational determinant descent; the archimedean leading-term comparison | not proved |
| real Coleman-family trace jets `𝒯_X(g) mod X²` | not computed |

No OPEN gate of the corpus (`P5-CANON-BocID`, `P5-CPLX-GPR`, `FW-H2` at 3529, the two Ш items) moved. Every package records `BSD_proved: false`, `canonical_frontier_updated: false`.

## 4. Facts this line established, usable as inputs

* **The eigenlines are the Néron-normalised modular symbols up to a unit.** RUN-076: for 27 quadratic twists with root number `+1`, `A_D = L(E, χ_D, 1)·√|D|/Ω^±` is an exact integer — `4` for 22 of them, `16` at `D = −51`, `36` at `D = −43`, `0` at `65, 93, −47` — and one unit per sign, `λ⁺ = 10` on the plus line (`λ(1,5) = 1`), `λ⁻ = 6` on the minus line (index 3 ↦ 1), carries these onto the mod-11 twisted sums, zero sets included. A mod-11 "unit" claim at either scale is therefore a claim at the Néron scale.
* **The central value of `E ⊗ χ₈` and its whole even first layer at 11 vanish**: `w(E ⊗ χ₈) = (2/389) = −1`; `L(E, χ₈ψ, 1) = 0` for the order-5 characters `ψ` of conductor 11 (to `10⁻¹⁵`, one Galois orbit; and every `[a/11]_{χ₈}⁺ ≡ 0 mod 11`). The packages' `λ₈(0)` lives on the odd side and is unaffected. (RUN-076 §1–§2.)
* **Root numbers, twisted sums and first-layer totals for every fundamental `|D| ≤ 100` prime to 11** — the table in RUN-076 §3 — and, for every even `D`, the package's own criterion `λ_D(0) mod 11` in RUN-077 (`χ₈` and `χ₅` pass; `57, 97` fail).
* **`L''(E,1)/2 = 0.7593165002884` from this tree's own `a_n`** (RUN-073) and **the Kurihara number `δ₃₉₇·₉₉₁ = 5`** from this tree's own modular symbols (RUN-068): both numbers the corpus had only stated are now computed here.
* **The 11-adic logarithms of `ε = 1 + √2` and `u_bot = ε⁻⁴` to `11¹⁰`**, independently (RUN-078).

## 5. Conventions — write numbers so they can be compared

| object | convention here |
| --- | --- |
| curve | `E: y² + y = x³ + x² − 2x` (389.a1), `P = (0,0)`, `Q = (1,0)`, `p = 11`, `a₁₁ = −4`, unit root `α ≡ 7` (root of `x² + 4x + 11` mod 11), `a₃₈₉ = +1` (split), `w(E) = +1` |
| Manin symbols | generators `(1, t)`, `t = 0..388`, and `(0, 1)` at index 389 (`P¹(F₃₈₉)`, `(c:d) ↦ d·c⁻¹`); relations, Hecke at 2, 3, 5; Merel matrices act on the bottom row |
| paths | `{∞, a/n} = m(1,0) + Σ_i m(q_i, (−1)^{i−1} q_{i−1})` over the continued-fraction convergents; the sign is visible to the minus functional (RUN-077) |
| plus line | `λ(c,d) = λ(−c,d)`, scaled by `λ(1,5) = 1`; `65 → 2 → 1` |
| minus line | `λ(c,d) = −λ(−c,d)`, scaled by its first nonzero coordinate, index 3 ↦ 1 (the packages' convention too) |
| periods | `Ω⁺ = 4.980425121710` (both real components), `Ω⁻ = π/AGM(√(e₁−e₃), √(e₂−e₃)) = 1.971737701552`; roots `e₁ > e₂ > e₃` of `4x³ + 4x² − 8x + 1` |
| the unit relations | plus: mod-11 sum `≡ 10 × (L√D/Ω⁺ mod 11)`; minus: `≡ 6 × (L√|D|/Ω⁻ mod 11)` |
| MTT measure | `μ_α(a + pⁿZ_p) = α⁻ⁿ[a/pⁿ] − α⁻ⁿ⁻¹[a/pⁿ⁻¹]`; twist by `χ` of conductor `D` prime to `p`: `[r]_χ = Σ_b χ(b)[r + b/D]`, `α_χ = χ(p)α` |
| characters | `χ_D` = Kronecker `(D/·)`, `(D/2) = +1` for `D ≡ ±1 (mod 8)`; `χ₈ = (8/·)` is even, `(−8/·)` is odd; `ω(a) ≡ a (mod 11)` |
| twisted root number | `w(E ⊗ χ_D) = χ_D(−389)·w(E)` for `D` prime to 389 |
| twisted L-value | `L(E, χ_D, 1) = 2·Σ a_n χ_D(n) e^{−2πn/(|D|√389)}/n` when `w = +1`; conductor `389·D²` |

## 6. The pairing protocol — 它主攻，這條線主證

**Three parties since 2026-09-13 (Neo's arrangement).** A *web GPT* does symbolic derivation only — conditional theorems, no large computation; its documents are Markdown, byte-exact under `data/external/gpt-symbolic-rounds/`, verified and *supplied with computation* by this line (RUN-079, 082, 083, 084 — §2b: every identity instantiated exactly, the numbers on `389.a1` the rounds ask for computed, one slip found and stated as a counterexample). The local line's own branch `agent/bsd-period-calibration` (PC-001, PC-002) is read by `git archive` at a named commit and verified the same way (RUN-080, 081). The *local GPT-6* attacks the frontier with computation; its packages go under `data/external/gpt6-proof-attacks/` (or a sibling folder), verified as before. This line verifies both, and when the symbolic side needs a number on 389.a1 at 11 — a modular symbol, an L-value, a period, a height, a p-adic logarithm — it asks and this line computes it at a stated scale (§5). A symbolic round's hypotheses (e.g. "the family satisfies the factorisation (2.1)") are what the local side must eventually deliver as a package; this line says which oracle tests which hypothesis (RUN-079: O5/O6 test only O1).

**What the attacker sends** (as the eight packages did): one zip per attack with the manuscript (`.md`, UTF-8, `$…$` mathematics), `INPUTS.json` (what is accepted from before, with hashes), the script, `result.json` (every number the manuscript states, every path or summand it sums over), `MANIFEST.json` (SHA-256 of each file). Every number carries its normalisation (§5). Every claim is one of three things and says which: *computed here*, *cited* (with the theorem), or *null* (not done). "Unit" and "nonzero" name their scale.

**What this line does with it:** copies the zip byte-exact into `data/external/…` with a provenance entry; recomputes every finite statement with its own code — never by running the package's script (a script agreeing with itself is not evidence); compares to the last digit and records every difference; reads the theorem-level steps and says so; checks the package's own labels against its text and JSON; plants defects in the new gate and runs the whole drill; writes one report `RUN-NNN`, one README row, commits, pushes. A package's error is reported as a number, not an opinion. A package's *correct* result is recorded as identical, and the package's own "not proved" is repeated, not softened.

**Rules of the line** (unchanged since RUN-001): a claim is "curve `X`, prime `p`, reached rung `CN`" on the C0–C10 ladder, never a bare BSD verdict; an OPEN gate is closed by a computation this line can repeat, not by assertion; every gate is drilled — a gate that has only ever been green is indistinguishable from a comment.

**What would move something** (the open steps of §3 phrased as things this line could check): an actual coordinate vector for `B₂` in a stated frame; a number for `C` with the frame that defines it; a Coleman-family trace `𝒯_X(g) mod X²` for a named `g` with its pseudocharacter identification; the comparison map from Attack 07's chain to Kato's class with a computable image; `𝔰₁₁` as a rational number with a stated normalisation — then `𝔰₁₁`, the regulator and `L''(E,1)/2 = 0.7593165002884` can be put in one equation and checked.

## 7. Running the tree locally

```bash
python code/src79_attack09_eisenstein_leading_term.py     # Attack 09, ~5 s
python code/src80_attack10_unit_and_trace_bridge.py       # Attack 10, ~3 s
python code/src78_attack09_auxiliary_character.py         # the 54 twists, ~10 s
python code/src70_kurihara_modular_symbols.py             # the eigenline and δ = 5, ~10 s
python code/src82_pc001_calibrator_19a1.py               # PC-001, the calibrator 19.a1 over Q, ~20 s
python code/src83_pc002_relative_regulator.py            # PC-002, the four series and the cup pairing, ~60 s (--deep: 14641 layer)
python code/src86_symbolic010_012_architecture_reciprocity_adelic.py   # Rounds 010-012, < 1 s
bash code/run_sharded_drill.sh 8 ./drill-logs              # the whole drill, ~30 min on 8 processes
```

Every gate writes its JSON log to `data/gate-logs/` and exits 0 only when every check it names agrees.
