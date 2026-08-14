# AI_HANDOFF — Collatz Operation Translation Series SSSP Repaired v1.0

## Read order

1. `manifest.json`
2. `validation.json`
3. `SERIES_INDEX.md`
4. `AUDIT_AND_CORRECTIONS.md`
5. the target paper(s)

## Source rules

- Treat files in `core_series/` and `research_program/` as the current repaired UTF-8 scholarly source artifacts.
- Do not reconstruct formal source from chat rendering.
- Canonical math delimiters are only `$...$` and `$$...$$`.
- Do not convert LaTeX into Unicode mathematical glyphs and then use the Unicode form as replacement source.
- Do not perform `unicode_escape`-style round trips.
- Do not silently rewrite backslashes, delimiters, or formula whitespace.
- Do not overwrite `provenance/original/` or existing diffs to make a later edit look original.

## Before any edit

Run:

```bash
python tools/verify_series.py .
```

The verifier independently checks hashes, source-set identity, UTF-8, delimiter policy, mechanically regenerates every unified diff, regenerates the aggregate repair diff, reruns MathJax when the local Node/MathJax dependency is available, and reruns the finite theorem-regression suite.

## After any edit

Create a new revision/package. Do not alter the existing provenance evidence in place. A downstream change must produce new hashes and new diffs.

## Important scope warning

`PASS` in this package means source/package integrity and finite/algebraic regression checks passed. It does not mean the Collatz conjecture has been proved.

## SSSP anchor

- document: `Collatz_OT_Series_Repair_Audit_2026_08_14_v1`
- revision: `8`
- snapshot: `sssp://Collatz_OT_Series_Repair_Audit_2026_08_14_v1/versions/r000008-5c38f568dc4b`
- SSSP document hash: `sha256:5c38f568dc4bf377c5029f8edd1a52e02b3a480226c4fe1503b5f2ac695984a9`
- repaired source-set aggregate SHA-256: `96b1b9ccb64a62a0d4fc3942d6cdf7af63c5ffe2ae3369799b7c20d1fe24f155`

The exact source bytes are in this package. SSSP anchors the deterministic source-set digest and repair ledger rather than retranscribing the full papers through a chat serialization layer.
