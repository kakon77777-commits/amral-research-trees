# scripts/

Build and generation scripts, mostly one per candidate version:
`build_artifacts_v0XX.py` / `build_schema_v0XX.py` / `generate_fixtures_v0XX.py`
(re)generate that round's frozen `artifacts-v0.2.X/` and `fixtures-v0.2.X/` content
deterministically from the versioned source in `../src/pnp_glc_i0/`.
`build_isolation_report_v026.py` and `build_runtime_closure_spec_v026.py` are v0.2.6-
specific additions supporting that round's runtime-isolation and closure-spec checks.
