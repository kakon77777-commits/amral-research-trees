# GLC0 (Lean source modules)

The actual Lean 4 source for the `glc0-lean` project (see the parent directory's
README for what this formalization does and does not cover):

- `Admission.lean` -- the admission/gate logic being formalized.
- `Core.lean` -- core definitions shared across the other modules.
- `Countermodels.lean` -- the two counterexamples referenced in the parent README
  (halt does not imply output; standard does not imply robust).
- `Runs.lean` -- run-record / trace-related definitions.
- `System.lean` -- the overall system assembly.
- `TaskSpec.lean` -- task specification definitions.

`../GLC0.lean` (one level up) is the project's root import file; `../AxiomAudit.lean`
is a standalone check confirming the build introduces no new axioms beyond Lean's own
`propext`/`Quot.sound`.
