# artifacts-v0.2.2/auth/

Signed `.trace-auth.json` fixtures used to test the candidate's trace-authenticity
checking. Includes both fixtures that should validate cleanly (`legit`, `neutral-legit`,
`robust-legit`, ...) and fixtures that are deliberately broken in a specific way
(`bad-trace-signature`, `cheat`, `fabricated-states-999`, `fabricated-transition-digest`,
`malformed-role-edge`, `missing-transitive-ref`, ...) -- the negative fixtures exist to
confirm the validator actually rejects each specific kind of tampering, not just that
it accepts good input.

This snapshot corresponds to candidate v0.2.2. The blocker(s) being tested/closed at this round: CLOSURE-CLASS-01. For the full narrative, see `../CURRENT-v0.2.2-candidate.md` and `../VALIDATION-REPORT-v0.2.2-candidate.md` (filenames vary slightly by round -- check `../` for the exact match).
