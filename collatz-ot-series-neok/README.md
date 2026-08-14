# Collatz Operation Translation Series — Neo.K

**Author of the research: Neo.K**（許筌崴, 一言諾科技有限公司 / EveMissLab).
Nine closed core papers on the Collatz conjecture plus a follow-on research
program, previously published on Neo.K's experiment site and archived here as
the raw source layer.

This directory is **Neo.K's research tree, not an AI agent's.** It is placed in
this repository verbatim, on Neo.K's instruction, so that the source layer sits
beside the verification work rather than only in a chat attachment. Archived
2026-08-14 (Asia/Taipei) by 數學戰士「墜衡」 (Claude Opus 5), who wrote this
README and nothing else here.

## Contents

[`Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0/`](./Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0/)
— the SSSP Repaired v1.0 package, **byte-exact**, 49 payload files plus its own
`CHECKSUMS.sha256`. Nothing was added, removed, reformatted, or renamed. Its
manifest, repair ledger, per-file diffs, preserved originals, aggregate source
digest and its own verifier are all as the author shipped them.

Read it in the order its own `AI_HANDOFF.md` prescribes: `manifest.json`,
`validation.json`, `SERIES_INDEX.md`, `AUDIT_AND_CORRECTIONS.md`, then the target
paper. The package's `AI_HANDOFF.md` also sets the editing rules for it, and they
govern — in particular, provenance is not to be modified in place, and a
downstream change must produce a new package with new hashes and new diffs.

| | |
|---|---|
| Core series | 9/9 papers, `core_series/` |
| Follow-on program | Hard-Zeta / Faithful Global Quantifier Compression, `research_program/` |
| Repair date | 2026-08-14 |
| Source-set aggregate SHA-256 | `96b1b9ccb64a62a0d4fc3942d6cdf7af63c5ffe2ae3369799b7c20d1fe24f155` |
| SSSP anchor | `Collatz_OT_Series_Repair_Audit_2026_08_14_v1`, revision 8 |

## Epistemic status — the author's own, not restated by the archiver

**The Collatz conjecture is not proved here, and the package says so itself** in
at least three places (`README.md`, `validation.json`'s `scope_warning`, and
`AI_HANDOFF.md`'s scope warning). `PASS` in this package means source/package
integrity plus finite and algebraic regression checks. It does not mean the
conjecture is settled.

Each paper carries its own statement of what it does and does not prove; Paper 02
§31 and Paper 06 §42 are explicit lists of non-claims. Read those rather than
inferring completion from a document's presence in this repository.

## Verifying this copy

The package ships its own verifier, and the copy in this repository passes it:

```bash
cd Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0
PYTHONUTF8=1 python tools/verify_series.py .
```

`PYTHONUTF8=1` is required on a cp950 Windows host. Without it the run aborts at
step 7 of 9, because `tools/generate_math_inventory.py` writes UTF-8 JSON to
stdout and cp950 cannot encode the `ö` of "Möbius" in Papers 07 and 08. This is a
known defect in the package, reported but **not fixed here** — fixing it in place
would violate the package's own provenance rule and change its hashes. See the
verification tree's report.

The MathJax step reports `SKIP` unless a local `mathjax-full` install is present.
That is the package's own design and is correct behaviour: it refuses to report a
pass it did not earn.

## Independent verification of the finite claims

Separately and independently, [`../collatz-verification-zhuiheng/`](../collatz-verification-zhuiheng/)
re-derives this series' finite claims from the papers' own theorem statements,
rather than by re-running the package's regression suite. See
[`RUN-002-OT-SERIES.md`](../collatz-verification-zhuiheng/reports/RUN-002-OT-SERIES.md)
for what has been re-derived so far, what it agrees with, and what remains open.

That is a separate research tree with a separate author and a separate scope. Its
conclusions are its own and do not amend anything in this package; proximity in
this repository is not agreement between researchers.
