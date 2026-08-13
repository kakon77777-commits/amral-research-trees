# artifacts-v0.2.6/

Frozen artifact snapshot for candidate v0.2.6's acceptance round -- the exact JSON
evidence (candidate-projection spec, closure spec, run/fairness records) that AI-1/
AI-2/AI-3/AI-5 each checked against for this round. Subdirectories: `auth/` (signed
trace-authenticity fixtures, both legitimate and deliberately tampered), `traces/`
(raw execution traces), and (from v0.2.3 onward) `closure-classification/` (test
cases for the closure classifier specifically).

This snapshot corresponds to candidate v0.2.6. The blocker(s) being tested/closed at this round: CLOSURE-SUPPORTED-RELATION-RESULT-01 (closed this round) / CLOSURE-OPAQUE-LEAF-TERMINAL-01 / ACCEPTANCE-PACKET-IMPORT-EDGE-COUNT-01. For the full narrative, see `../CURRENT-v0.2.6-candidate.md` and `../VALIDATION-REPORT-v0.2.6-candidate.md` (filenames vary slightly by round -- check `../` for the exact match).
