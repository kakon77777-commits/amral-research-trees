# src/pnp_glc_i0/

The candidate implementation itself. `two_sat.py` (not version-suffixed) is the base
2-SAT solver; `parity.py` and `oracles.py` are the PARITY admission-reality test and
independent correctness oracles described in `../../README.md`. `experiment.py` and
`semantic_validator.py` are the base versions of the experiment driver and external
validator; `experiment_v0XX.py` / `semantic_validator_v0XX.py` are the versioned
successors used by that round's `scripts/build_artifacts_v0XX.py` and by
`../../tests_v0XX/`. `__main__.py` is the CLI entry point used in `../../README.md`'s
"Reproduce" section.
