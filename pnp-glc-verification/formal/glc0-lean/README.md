# GLC0 Lean 4 Phase 1 kernel

This project mechanizes the Phase 0 resource-neutral GLC core without importing
Mathlib or any P/NP library.

## Locked toolchain

- Lean: `leanprover/lean4:v4.30.0`
- Lake: `5.0.0`

## Modules

- `GLC0.TaskSpec`: legal-input domain and correctness relation.
- `GLC0.System`: fixed algorithm witness with separate step, halt, and emit
  relations.
- `GLC0.Runs`: partial traces, prefix/maximality, standard/admissible/fair
  policies, and the two mode-specific meanings of the shared nonempty-run gate.
- `GLC0.Core`: `GoodTerminal`, `Solved0`, `GLC0Std`, `GLC0Robust`,
  `good_terminal_unfold`, and `robust_to_std`.
- `GLC0.Countermodels`: terminal-without-output and well-formed
  standard-but-not-robust models.
- `GLC0.Admission`: four-valued gates, run/resource applicability, and
  fail-closed unknown evidence.

Fairness is an uninterpreted policy predicate. Zero debt is a parameter of the
GLC0 definitions. Neither a complexity library nor any four-layer equivalence
claim appears in this project.

## Verification

```powershell
lake clean
lake build
lake env lean AxiomAudit.lean
```

The two requested positive theorems, `good_terminal_unfold` and
`robust_to_std`, are reported by Lean as depending on no axioms. The
countermodel proofs use only Lean's standard `propext` and, for the
standard-not-robust construction, `Quot.sound`; this project declares no
custom axioms and contains no `sorry` or `admit`.
