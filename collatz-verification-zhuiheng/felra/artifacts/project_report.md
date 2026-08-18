# FELRA Project Report — Where a float64 anchor stops seeing the correction mass

- Project ID: `collatz-anchor-representation`
- Overall result: **ATTENTION REQUIRED**
- Claims supported in declared domain: `True`
- Analyses completed successfully: `False`
- Generated at: `2026-08-18T14:47:33.284723+00:00`
- Configuration SHA-256: `bf5ebf86113a5de0eafdd76e3c802e4edfbb46360a05c175dcc5b127fa08e2d7`
- Result SHA-256: `38d51d9170af85193899199af86191a7aaacce07942ecd3701b15df60ff7f5ca`

> All results are finite-budget computational evidence, not universal proofs.

## Claims

- **PASS** `correction_mass_never_exhausts` — On the all-ones spine the anchor gap 1 - (2/3)^m is positive at every m ([report](claims/correction_mass_never_exhausts/validation_report.md))

## Analyses

- **PASS** `anchor_gap_below_the_horizon` — The anchor gap at small m ([report](analyses/anchor_gap_below_the_horizon/analysis_report.md))
- **FAIL** `anchor_gap_at_the_horizon` — Where float64 reports the correction mass as exhausted ([report](analyses/anchor_gap_at_the_horizon/analysis_report.md))
- **PASS** `decimal_still_sees_it` — Decimal at 40 digits against the exact value, past the float64 horizon ([report](analyses/decimal_still_sees_it/analysis_report.md))
- **PASS** `lean_whole_development_axiom_audit` — Every theorem in collatz-lean, and what each one rests on ([report](analyses/lean_whole_development_axiom_audit/analysis_report.md))

## Reproducibility

- Replay project: `replay_project.yaml`
- Provenance artifact: `provenance\provenance.json`
- Provenance artifact: `provenance\provenance.dot`
- Provenance artifact: `provenance\provenance.svg`

## Warnings

- Analysis anchor_gap_at_the_horizon did not complete successfully.
- Analysis lean_whole_development_axiom_audit: a formal verdict is about the obligation as written; it does not establish that the obligation states the intended claim
