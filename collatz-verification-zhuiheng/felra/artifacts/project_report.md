# FELRA Project Report — Where a float64 anchor stops seeing the correction mass

- Project ID: `collatz-anchor-representation`
- Overall result: **ATTENTION REQUIRED**
- Claims supported in declared domain: `True`
- Analyses completed successfully: `False`
- Generated at: `2026-08-18T14:34:16.924949+00:00`
- Configuration SHA-256: `2ec4ff5c1364dd80d6f220817169b6eb8460a763388522b7a44af712b6d5a1fb`
- Result SHA-256: `d732687c1dbaaec526b6dd21f4437944f09294751c1515693c3f4d45447b9bd3`

> All results are finite-budget computational evidence, not universal proofs.

## Claims

- **PASS** `correction_mass_never_exhausts` — On the all-ones spine the anchor gap 1 - (2/3)^m is positive at every m ([report](claims/correction_mass_never_exhausts/validation_report.md))

## Analyses

- **PASS** `anchor_gap_below_the_horizon` — The anchor gap at small m ([report](analyses/anchor_gap_below_the_horizon/analysis_report.md))
- **FAIL** `anchor_gap_at_the_horizon` — Where float64 reports the correction mass as exhausted ([report](analyses/anchor_gap_at_the_horizon/analysis_report.md))
- **PASS** `decimal_still_sees_it` — Decimal at 40 digits against the exact value, past the float64 horizon ([report](analyses/decimal_still_sees_it/analysis_report.md))
- **PASS** `lean_all_ones_spine` — The all-ones spine's properties, machine-checked in Lean 4 ([report](analyses/lean_all_ones_spine/analysis_report.md))

## Reproducibility

- Replay project: `replay_project.yaml`
- Provenance artifact: `provenance\provenance.json`
- Provenance artifact: `provenance\provenance.dot`
- Provenance artifact: `provenance\provenance.svg`

## Warnings

- Analysis anchor_gap_at_the_horizon did not complete successfully.
- Analysis lean_all_ones_spine: a formal verdict is about the obligation as written; it does not establish that the obligation states the intended claim
