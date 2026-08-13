# pnp-glc-verification

Source: a 7-role adversarial verification pipeline run via Codex, 2026-08-09 onward, testing an engineering candidate related to the GLC (P/NP Dynamic Four-Layer Closure) framework. Each role is its own directory, `outputs/` from the original run (build artifacts — compiled Lean `.lake/build/`, Python `__pycache__/` — are excluded; everything else, including intermediate iteration reports and test fixtures, is kept as-is):

| Directory | Role | Mandate |
|---|---|---|
| [`integrator/`](./integrator/) | AI-1 | Reconciles the other roles' dispositions against the frozen manifest; adjudicates when they disagree; the authoritative "current status" for any given candidate version. |
| [`redteam/`](./redteam/) | AI-2 | Read-only conformance checks against frozen evidence — signatures, existing test replays, narrowly-scoped re-checks assigned by AI-1. Explicitly does not do independent rebuilds or algorithmic re-verification. |
| [`formal/`](./formal/) | AI-3 | Formal-interface review: completeness of the candidate's normative judgment graph, plus a Lean 4 formalization (`glc0-lean/`) — kept deliberately narrow in scope, not claiming to formalize the framework's core claims. |
| [`engineering/`](./engineering/) | AI-4 | Builds the candidate itself (`pnp-glc-i0/`) and runs its own self-tests. Its own documents explicitly disclaim any P=NP/P≠NP conclusion. |
| [`ai5/`](./ai5/) | AI-5 | Independent engineering replay — does not call the candidate's own verifier; reimplements every check from scratch to catch anything the candidate's self-testing might have missed or gamed. |
| [`scholar-traditional/`](./scholar-traditional/) | AI-6 | Blind review from a traditional computational-complexity-theory standpoint, run separately from the engineering pipeline above. |
| [`scholar-bridge/`](./scholar-bridge/) | AI-7 | Cross-paradigm review comparing the GLC framework's own vocabulary against standard complexity-theory concepts; checks whether AI-6's verdict holds up as the engineering pipeline progresses. |

## Reading the version history

Reports are versioned (`v0.2`, `v0.2.1`, ... `v0.2.6` at time of writing) and each iteration's disposition is in its own filename (`..._PASS_...` / `..._FAIL_<blocker-id>_...`). A later version superseding an earlier one does not mean the earlier report was wrong — most blockers found in early iterations were genuinely fixed, then a *different* one surfaced one layer deeper. Do not read a `PASS` from one role in isolation: AI-1's report is the one that reconciles all roles into a single current status, and it is the one to check first.

**Curated status snapshot** (as of v0.2.6, not automatically kept in sync with this repo): [amral.evemisslab.com/glc-framework/verification/](https://amral.evemisslab.com/glc-framework/verification/). That page mirrors only the most current handful of files from each role; this directory has the fuller history.
