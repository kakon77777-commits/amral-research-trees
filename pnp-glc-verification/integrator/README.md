# integrator (AI-1)

AI-1's own output directory -- read-only integration/acceptance reports. AI-1 does not
re-run tests itself; it reconciles the frozen manifest against what AI-2 (redteam),
AI-3 (formal), and AI-5 (independent replay) each reported, and adjudicates when they
disagree. Its verdict is the closest thing to "current overall status" for any given
candidate version.

Filename pattern: `AI-1_I0_v0.2.X_..._<PASS|FAIL>[_<blocker-id>]_v0.1.md` -- one report
per acceptance round, plus occasional `_追加分類_ADDENDUM_...` (addendum) files where
a disposition was revised after the fact (e.g. v0.2.3 was briefly marked PASS, then
corrected to FAIL). A few `*_repro_v0.1.py` scripts are AI-1's own reproduction
scripts for specific blocker IDs, kept alongside the report that introduced them.

Root-level `P_NP_動態四層閉合...` and `AI-1_Phase0_...`/`AI-1_AI-3_Phase1_...` files
predate the versioned v0.2.x acceptance cycle -- they're the pipeline's own charter
and earliest-phase integration decisions.
