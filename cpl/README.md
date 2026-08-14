# cpl/ — Critical-Line Proportion Ladder

**Mirrored by:** Claude (Sonnet 5) via Claude Code (`eigenself: anthropic/claude-sonnet-5`, `slice: Claude Code (CLI coding agent)`, `instance: neo-k-amral-2026-07-26`), on Neo.K's (許筌崴) instruction.
**Date mirrored:** 2026-08-14 (CTCL-verified instant `2026-08-14T17:17:19.81Z`).
**Collaboration boundary:** the 10 packages below were produced by Neo.K's own separate AI-autonomous research process, downloaded from his local `Downloads/CPL/` folder. This Claude Code session did **not** author the CPL research itself — it only mirrors the packages into this durable, AI-native repository exactly as received (flattening one redundant zip-nesting level), and separately built a curated presentation of the v1 subset at [amral.evemisslab.com/cpl/](https://amral.evemisslab.com/cpl/). Per-package claims below are drawn from each package's own files, not reinterpreted.

## Problem and external antecedent

CPL does **not** attempt to prove or disprove the Riemann Hypothesis. It is a follow-on to a real, published, externally-verifiable paper:

> Claude, *"More Than Two Thirds of the Zeros of the Riemann Zeta Function Lie on the Critical Line"* (2026-08-10). Official Lean companion: [github.com/anthropics/zeta-23-lean](https://github.com/anthropics/zeta-23-lean) — confirmed real via `gh api repos/anthropics/zeta-23-lean` (public, Apache-2.0, 151 stars, pushed 2026-08-10) and independent news coverage before any of this content was built into the public site, given the stakes of presenting a hallucinated claim as real.

That paper unconditionally raised the proportion of critical-line zeros from 41.6% (Pratt–Robles–Zaharescu–Zeindler) to 67.25%. It explicitly does **not** resolve RH and says nothing about the remaining 32.8% of zeros. CPL's own question: can the paper's self-acknowledged 68.185% certificate ceiling be independently reconstructed, and can 67.25% be pushed toward 70/80/90%?

## Route: single-thread version progression, not branches

Unlike `bsd/`'s four parallel sub-lines, CPL is one linear thread — each version builds on the last. Formal object: `P_q` = liminf proportion of simple critical-line zeros ≥ q.

| Packages | Content (self-reported) |
|---|---|
| `CPL_Claude_67_25_Research_Pack_2026-08-11` (v1 base) | Definition of `P_q`; proof-graph reconstruction of the 67.25% result into Z/L/P modules with 5 Proof Obligations left for independent reproof; target ladder — `P_2/3` and `P_67.25` proven, `P_68.185` marked `OPEN-RECONSTRUCTION-01`, `P_70`/`P_80`/`P_90` rough estimates only, `P_99` explicitly marked "not conjectured — do not extrapolate." Fully curated on the public site (`/cpl/p/00-overview/` through `/03-ceiling-scope/`). |
| `CPL_Claude_67_25_Research_Pack_v2_2026-08-11` … `v5`, `v7` (v2–v7, **v6 absent** — not produced by the source research, not an omission on our part) | Scaffolding toward reconstructing the paper's own 68.185% certificate ceiling. Found the exact adjacent constant `0.681828687463832…` by reading the official Lean source directly. Built a from-scratch toy linear-programming model that reproduces the paper's "open-band adversarial" argument structure; an N=4 exact-rational toy bound reached 69.82110925%, self-labeled **"not a Riemann zeta theorem."** A full N=256 external certificate was never obtained through v7. |
| `CPL_Claude_Research_Pack_v8_2026-08-11`, `v9` | Support axis and arithmetic-input scale. Reconstructs the generalized operator behind the paper's own support ladder (1.04 / 1.26 / 1.70) and numerically extends it to `σ95 ≈ 2.26`, `σ99 ≈ 4.19` — values not listed in the original paper, self-labeled **"not a new theorem stated by the paper."** Translates support requirements into prime-pair displacement scale. |
| `CPL_Claude_Research_Pack_v10_2026-08-11`, `v11` | Weakened hypotheses and literature audit. Proposes a test-specific hypothesis far weaker than full Hardy–Littlewood; audits real 2024 literature (Matomäki–Radziwiłł–Shao–Tao–Teräväinen) and finds it **insufficient to support a P70 claim** as-is. |

None of v2–v11 is curated on the public site yet — deferred to a future session, not forgotten.

## Reading order

`v1 base` → `v2` → `v3` → `v4` → `v5` → `v7` (v6 does not exist) → `v8` → `v9` → `v10` → `v11`. Read v1's `00_README.md` first regardless — every later version assumes its `P_q` definition and the "proven / open / forbidden-to-extrapolate" status vocabulary it sets up.

## Reproducible commands and tool versions

Each package records its own dependencies and replay notes in its own files (see e.g. `notes/03_Ceiling_Scope_67_25_vs_68_185.md` in the v1/v2 packages for the Lean cross-reference method). No single environment file covers all 10 packages — check the specific package being replayed.

## Provenance

Original source: `C:\Users\kakon\Downloads\CPL\` (10 `.zip` files, 19MB extracted). Each zip's own internal folder-nesting has been flattened by one level on import here. No other content transformation was applied.
