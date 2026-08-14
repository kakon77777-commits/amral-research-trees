# Collatz Operation Translation Series — SSSP Repaired Package v1.0

This is the repaired one-click handoff package for the Collatz Operation Translation Series.

## Start here

1. Read `SERIES_INDEX.md`.
2. The nine core papers are in `core_series/`.
3. The Hard-Zeta follow-on research program is in `research_program/`.
4. Read `AUDIT_AND_CORRECTIONS.md` for what was changed and why.
5. Before editing, run `python tools/verify_series.py .`.

## Why Paper 09 appears here even though it was absent from the uploaded 7z

The uploaded 7z contained Papers 01–08 plus the Hard-Zeta follow-on paper. Paper 08 and Hard-Zeta both depend on Paper 09. The user's existing Library contains the completed Paper 09 and a complete series index declaring the core series 9/9 complete. The original Library copy is preserved under `provenance/original/09__...` and the repaired source appears in `core_series/`.

## Validation result at package creation

- strict UTF-8 source validation: PASS
- canonical math delimiter policy: PASS
- MathJax: 3,027 formulas rendered; 0 errors
- display formulas: 2,204
- inline formulas: 823
- finite/algebraic theorem regression suite: PASS
- SSSP repair audit validation: PASS / 0 issues
- SSSP repair audit key math blocks: 5/5 rendered

These checks do **not** claim a proof of the global Collatz conjecture. They validate source integrity and the finite/algebraic claims exercised by the regression suite.
