# bsd/ — Birch and Swinnerton-Dyer conjecture

**Mirrored by:** Claude (Sonnet 5) via Claude Code (`eigenself: anthropic/claude-sonnet-5`, `slice: Claude Code (CLI coding agent)`, `instance: neo-k-amral-2026-07-26`), on Neo.K's (許筌崴) instruction.
**Date mirrored:** 2026-08-14 (CTCL-verified instant `2026-08-14T17:17:19.81Z`).
**Collaboration boundary:** the 25 packages below were produced by Neo.K's own separate AI-autonomous / semi-autonomous research process, downloaded from his local `Downloads/BSD/` folder. This Claude Code session did **not** author the BSD research itself — it only mirrors the packages into this durable, AI-native repository exactly as received (flattening one redundant zip-nesting level, excluding `__pycache__`/`.pyc`), and separately built a curated presentation of the Phase0 subset at [amral.evemisslab.com/bsd/](https://amral.evemisslab.com/bsd/). Per-package authorship, methodology, and epistemic claims below are drawn from each package's own `README.md` / report files, not reinterpreted.

## Problem

Birch and Swinnerton-Dyer conjecture (BSD) — one of the seven Clay Mathematics Institute Millennium Prize Problems. **No package in this tree claims to prove BSD.** The organizing tool across all 25 packages is a curve-level certificate ladder:

```
C0 (identity) → C6 (weak BSD) → C7 (single-prime strong form)
→ C8 (Sha finite + exact) → C9 (full strong BSD) → C10 (family theorem)
```

Every claim in this tree should be read as "curve X, prime p, reached rung CN" — never as a bare BSD true/false verdict.

## Route: four sub-lines, different maturity

| Sub-line | Packages here | Status (self-reported by the packages, not our gloss) |
|---|---|---|
| **Phase0 — Global Enclosure** | `BSD_Global_Enclosure_Phase0_2026-08-12/` (9 docs) | Framework only. Decision: GO into Phase 1. Doc 05 is a **formal audit that rejects** Neo.K's own prior "lattice-point rank convergence" idea as carrying circular-reasoning risk — verdict "archive as exploratory analogy, do not use as a Phase 1 proof route." Fully curated on the public site at `/bsd/phase0/`. |
| **Phase1 — Banwait–Huang reproduction** | `BSD_Phase1_Banwait_Huang_Reproduction_v0.1` … `v0.4`, `BSD_Phase1_Banwait_Huang_Exact_Census_v0.5`, `BSD_Phase1_Banwait_Huang_Semantic_Replay_v0.6` (6 packages) | Reproduces the algorithmic census from arXiv:2601.16044 (conductor < 500,000). Converged count: 36,687 base curves pass, 247,391 admissible twist pairs — but that count is `DIRECT_PRIMARY_SOURCE` (taken from the official output and consistency-audited, 0 mismatches found), **not independently re-derived from scratch**. Only 2 curves / 28 twists were independently recomputed. Not yet curated on the public site. |
| **Phase2 — non-semistable family (696.e1)** | `BSD_Phase2_NonSemistable_Bridge_v0.1`, `BSD_Phase2_FW_Compiler_v0.2`, `BSD_Phase2_First_NonSemistable_Family_v0.3`, `BSD_Phase2_696e1_Referee_Audit_v0.4`, `BSD_696e1_Theorem_Note_v1.0`, `BSD_FW_H2_Local_Isogeny_Compiler_v0.3` (6 packages) | Explicit infinite twist family (density 1/24) for curve 696.e1, covering a case Banwait–Huang's method doesn't reach. Survived an internal 6-sub-referee adversarial audit that caught and fixed one real citation error. Current status: **"DERIVED THEOREM CANDIDATE"** — deliberately not elevated to "new theorem," pending external review. Not yet curated on the public site. |
| **P5 — single-prime strong BSD for 389.a1 at p=11** | `BSD_P5_Anomalous_Norm_Localization_v1.1`, `BSD_P5_Norm_Selmer_Core_Vertex_v1.2`, `BSD_P5_Determinantal_Kurihara_Semilocal_v1.3`, `BSD_P5_ETNC_Escape_Audit_v0.4`, `BSD_P5_Explicit_Local_Unit_Cancellation_v0.8`, `BSD_P5_IMC_Closure_and_GPR_Bridge_v0.5`, `BSD_P5_uGPR_Minimal_Gate_v0.6`, `BSD_RUGZPB_P2_P4_Rank2_v0.2` (8 packages) | Curve 389.a1 (rank 2) at prime p=11. `Sha[11^∞] = 0` is closed; several sub-lemmas are closed, including v1.1's exact anomalous-prime norm-localization isomorphism at 397/991 (`det M_loc = 2 ∈ F_11^×`) — but v1.1 itself flags that the standard regulator backend "cannot be inserted at these Kolyvagin primes without a new comparison theorem." The **core target — bridging the analytic leading term to the algebraic regulator at p=11 — remains OPEN across every package**, most recently stated explicitly: "does not prove BSD and does not prove local descent of the normalized complex leading coefficient." Not yet curated on the public site. |
| — | `BSD_Two_Witness_NonSemistable_Criterion_v0.1`, `BSD_Witness_Network_Finite_Exception_Criterion_v0.2`, `BSD_LMFDB_Exact_Census_Compiler_v0.5`, `BSD_Fixed_Additive_Period_Compiler_v0.4`, `BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1.md` (5 items) | Supporting/auxiliary packages feeding the sub-lines above (witness criteria for the non-semistable route, LMFDB census tooling, a standalone reduction note). See each item's own README/content. |

## Reading order

1. `BSD_Global_Enclosure_Phase0_2026-08-12/` — read `docs/00_...` through `docs/08_...` in numeric order first; this is the framework everything else sits inside.
2. Phase1 packages in version order (`v0.1` → `v0.6`).
3. Phase2 packages in version order (`v0.1` → `v1.0` Theorem Note); `BSD_FW_H2_Local_Isogeny_Compiler_v0.3` is a dependency of the Phase2 route.
4. P5 packages: `Anomalous_Norm_Localization_v1.1` → `Norm_Selmer_Core_Vertex_v1.2` → `Determinantal_Kurihara_Semilocal_v1.3` is the main spine; the other five are supporting audits/gates for that spine.

**Note on `BSD_P5_Anomalous_Norm_Localization_v1.1`'s provenance:** like `cpl/`'s v6 (see that tree's README), this package had no standalone top-level zip in the original `Downloads/BSD/` folder — it only existed nested inside `BSD_P5_Norm_Selmer_Core_Vertex_v1.2`'s own `dependencies/` folder. Extracted out to its own top-level directory here on import, same reasoning as v6.

## Reproducible commands and tool versions

No single environment file covers all 25 packages — **each package records its own dependencies** (typically a `requirements.txt` alongside a `scripts/` or `code/` directory, e.g. `numpy`) and its own replay instructions in its own `README.md` / `NEXT_HANDOFF.md`. Check the package you're replaying, not this file, for exact commands and versions. Several P5-line packages carry a `results/replay_output.txt` and a `CHECKSUMS.sha256` alongside their scripts — diff a fresh run's output against those before trusting a claim of reproduction.

## What is curated vs. what is only here

Only **Phase0** (9 docs) has a human-facing curated presentation, at [amral.evemisslab.com/bsd/phase0/](https://amral.evemisslab.com/bsd/phase0/) — built from these same source files (mirrored a second time under `amral/public/bsd/phase0/files/` in the `unbounded-axiom` repo). Phase1, Phase2, and P5 exist **only in this raw form** as of the mirror date above; curating them into detail pages is deferred to a future session, not forgotten.

## Provenance

Original source: `C:\Users\kakon\Downloads\BSD\` (25 items: 24 `.zip` + 1 loose `.md`, 92MB extracted), **plus 1 package (`BSD_P5_Anomalous_Norm_Localization_v1.1`) recovered from a nested zip inside another package** — 26 top-level directories/files total in this tree. Each zip's own internal folder-nesting has been flattened by one level on import here (each zip extracts to `<name>/<name>/...`; this repo keeps `<name>/...`). No other content transformation was applied.
