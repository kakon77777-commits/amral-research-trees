# formal (AI-3)

AI-3's own output directory. Top-level files are AI-3's formal-interface acceptance
reports, filename pattern `AI-3_I0_v0.2.X_..._<PASS|FAIL>[_<blocker-id>]_v0.1.md`,
plus `AI3_Phase0_Formalization_Map_v0.1.md` (the role's own scoping document) and
`AI3_Phase1_Lean4_Addendum_v0.1.md` (status note on the Lean project below).
`AI3_v022_CLOSURE_CLASS_01_regression_v0.1.py` is a reproduction script for one
specific round.

`glc0-lean/` is a real Lean 4 project (has its own README) -- a compiled, kernel-
audited formalization that is deliberately narrow in scope: a 4-valued gate and a
fail-closed lemma, not a formalization of the GLC framework's core claims. See its
own README for exactly what is and isn't proved there.
