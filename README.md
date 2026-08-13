# AMRAL Research Trees

Raw, uncurated research output from the AI agents working under [AMRAL Research Lab](https://amral.evemisslab.com/) (Neo.K / EveMissLab). This repository is the **AI-native layer**: math trees and research-data trees exactly as the agents produced them — reports, specs, source code, test fixtures, formal-verification artifacts. It is written for AI-to-AI consumption first; it is not edited for a human reader.

A curated, human-readable presentation of a subset of this material lives at **[amral.evemisslab.com](https://amral.evemisslab.com/)**, built and maintained separately. Writing a plain-language public version of everything here is future work, not something this repository does itself.

## What's in here

| Directory | Source | Curated presentation |
|---|---|---|
| [`p-np-glc/`](./p-np-glc/) | P/NP dual-hypothesis rehearsal (24 rounds + prerequisite) and the GLC four-layer closure framework — the raw research documents | [amral.evemisslab.com/p-np-dual/](https://amral.evemisslab.com/p-np-dual/), [amral.evemisslab.com/glc-framework/](https://amral.evemisslab.com/glc-framework/) |
| [`pnp-glc-verification/`](./pnp-glc-verification/) | A 7-role adversarial verification pipeline testing a GLC-related engineering candidate (integrator, red-team, formal/Lean, engineering, independent replay, two independent scholars) | [amral.evemisslab.com/glc-framework/verification/](https://amral.evemisslab.com/glc-framework/verification/) (status snapshot only, not the full trail) |

More research-line trees get added here as they're produced; each new one gets its own top-level directory and a matching row in the table above.

## What this is not

- Not a claim of any mathematical result. Individual documents inside make their own epistemic-status statements (draft methodology, conjectural, candidate-unpromoted, etc.) — read those, don't assume completion from a document's presence here.
- Not curated, deduplicated, or edited for readability. Directory structure mirrors the agents' own working output as closely as practical, minus build artifacts (compiled Lean output, Python `__pycache__`) that carry no information beyond what's already in source.
- Not necessarily in sync with what's live on amral.evemisslab.com at any given moment — the public site presents a reviewed, framed subset; this repo is the wider raw material it's drawn from.
