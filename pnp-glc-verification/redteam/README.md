# redteam (AI-2)

AI-2's own output directory -- read-only conformance/red-team reports. AI-2 checks
frozen evidence (signatures, byte-identity, existing test replays) against whatever
narrow scope AI-1 assigns it for that round; it does not rebuild the candidate or
re-verify algorithmic correctness from scratch (that's AI-5's job).

Filename pattern: `AI-2_I0_v0.2.X_..._<PASS|FAIL>[_<blocker-id>]_v0.1.md`. Read any
individual `PASS` narrowly -- it means AI-2's specific assigned checks passed, not
that the candidate as a whole was accepted; see the corresponding `integrator/`
report for the reconciled overall status. `AI-2_Phase0_...` is the role's own charter
document; the `v0*_*.py` and `candidate_projection_redteam_repro.py` files are AI-2's
reproduction scripts for specific rounds.
