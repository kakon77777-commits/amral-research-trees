# FELRA Project Report — Is the First-Crossing Reset Inequality a second fact, or the Correction Bound restated?

- Project ID: `au2e2-first-crossing-reset`
- Overall result: **ATTENTION REQUIRED**
- Claims supported in declared domain: `False`
- Analyses completed successfully: `False`
- Generated at: `2026-08-21T13:16:23.577125+00:00`
- Configuration SHA-256: `3f0168cc2245df7ee2a746e22ca4bd64e51c73d8eaba98fe1c86ce0721895a79`
- Result SHA-256: `49322281080492c8f387a46bfc086597d4cd785f41fbfa2d6272ce714eeca5db`

> All results are finite-budget computational evidence, not universal proofs.

## Claims

- **PASS** `reset_follows_from_the_correction_bound` — At L=5, the correction bound b <= 405 implies the reset inequality, for every start y in the declared range.
 ([report](claims/reset_follows_from_the_correction_bound/validation_report.md))
- **FAIL** `reset_needs_the_correction_bound` — The reset inequality does NOT hold on its own. FALSE on this domain, and a solver should hand back a counterexample rather than a proof.
 ([report](claims/reset_needs_the_correction_bound/validation_report.md))
- **PASS** `reset_is_equivalent_to_the_correction_bound` — The two are the same statement: each implies the other, so the reset inequality carries no information about y at all.
 ([report](claims/reset_is_equivalent_to_the_correction_bound/validation_report.md))
- **FAIL** `the_general_form_has_a_symbolic_exponent` — With L symbolic the same claim needs 3^L and 2^Q, which SMT-LIB2 cannot render exactly. Declared so that the refusal is on the record.
 ([report](claims/the_general_form_has_a_symbolic_exponent/validation_report.md))

## Analyses

- **PASS** `prove_reset_from_bound` — Export the implication and let z3 settle it over the whole declared box ([report](analyses/prove_reset_from_bound/analysis_report.md))
- **PASS** `refute_reset_alone` — Export the unguarded inequality — a counterexample is the correct outcome ([report](analyses/refute_reset_alone/analysis_report.md))
- **PASS** `prove_equivalence` — The reset inequality IS the correction bound, in both directions ([report](analyses/prove_equivalence/analysis_report.md))
- **FAIL** `refusal_on_symbolic_exponent` — What FELRA will not export, and why the general round is not solver-checkable ([report](analyses/refusal_on_symbolic_exponent/analysis_report.md))

## Reproducibility

- Replay project: `replay_project.yaml`
- Provenance artifact: `provenance\provenance.json`
- Provenance artifact: `provenance\provenance.dot`
- Provenance artifact: `provenance\provenance.svg`

## Warnings

- Analysis refusal_on_symbolic_exponent: refused rather than approximated: an obligation that is nearly the claim is an obligation about a different claim
