# AMRAL Research Trees

Raw, uncurated research output from the AI agents working under [AMRAL Research Lab](https://amral.evemisslab.com/) (Neo.K / EveMissLab). This repository is the **AI-native layer**: math trees and research-data trees exactly as the agents produced them — reports, specs, source code, test fixtures, formal-verification artifacts. It is written for AI-to-AI consumption first; it is not edited for a human reader.

A curated, human-readable presentation of a subset of this material lives at **[amral.evemisslab.com](https://amral.evemisslab.com/)**, built and maintained separately. Writing a plain-language public version of everything here is future work, not something this repository does itself.

## What's in here

| Directory | Source | Curated presentation |
|---|---|---|
| [`p-np-glc/`](./p-np-glc/) | P/NP dual-hypothesis rehearsal (24 rounds + prerequisite) and the GLC four-layer closure framework — the raw research documents | [amral.evemisslab.com/p-np-dual/](https://amral.evemisslab.com/p-np-dual/), [amral.evemisslab.com/glc-framework/](https://amral.evemisslab.com/glc-framework/) |
| [`pnp-glc-verification/`](./pnp-glc-verification/) | A 7-role adversarial verification pipeline testing a GLC-related engineering candidate (integrator, red-team, formal/Lean, engineering, independent replay, two independent scholars) | [amral.evemisslab.com/glc-framework/verification/](https://amral.evemisslab.com/glc-framework/verification/) (status snapshot only, not the full trail) |
| [`cpl/`](./cpl/) | Critical-Line Proportion Ladder — 10 packages, single-thread version progression (v1–v11, v6 absent) extending a real published paper on Riemann zeta zero proportions | [amral.evemisslab.com/cpl/](https://amral.evemisslab.com/cpl/) (v1 only; v2–v11 not yet curated) |

More research-line trees get added here as they're produced; each new one gets its own top-level directory and a matching row in the table above. See [`RESEARCH-TREE-PROTOCOL.md`](./RESEARCH-TREE-PROTOCOL.md) for the persistence contract every tree here follows.

## What this is not

- Not a claim of any mathematical result. Individual documents inside make their own epistemic-status statements (draft methodology, conjectural, candidate-unpromoted, etc.) — read those, don't assume completion from a document's presence here.
- Not curated, deduplicated, or edited for readability. Directory structure mirrors the agents' own working output as closely as practical, minus build artifacts (compiled Lean output, Python `__pycache__`) that carry no information beyond what's already in source.
- Not necessarily in sync with what's live on amral.evemisslab.com at any given moment — the public site presents a reviewed, framed subset; this repo is the wider raw material it's drawn from.

## About this repository, and why it's on GitHub

This is a public GitHub repository, licensed under [Apache-2.0](./LICENSE) (see `LICENSE`). Public and open-source here means: anyone can read, clone, fork, and reuse this content under the license's terms. It does **not** mean any individual document has been reviewed, validated, or endorsed as correct — see "What this is not" above. Being open by default is deliberate, matching how the rest of AMRAL/EveMissLab's work is published; there's no separate private staging step before content lands here.

## Authorization

The research in this repository is produced by AI agents working autonomously or semi-autonomously under Neo.K's direction, as part of AMRAL Research Lab (see [`/research-modes/`](https://amral.evemisslab.com/research-modes/) on the public site for what "autonomous" vs. "semi-autonomous" means here — autonomy level is a separate axis from who is credited as author). Neo.K, as founder and human principal of AMRAL / EveMissLab, authorizes both the autonomous/semi-autonomous research process itself and the publication of its raw output in this repository. This authorization covers the *process*; it does not itself make any individual document's claims true — each document's own stated epistemic status still governs how it should be read.

Authorship of individual documents follows whatever that document itself states (most already self-identify a lead researcher and any collaborating editor, e.g. "主導研究者" / "協作整理" fields in the P/NP series) — this root README doesn't attempt to restate or override that per-document attribution.

## Maintenance

README files throughout this tree — this one included — are living documents, not a one-time snapshot. When a directory's content changes (a new version lands, a file is added or removed, a round's status changes), that directory's README should be revisited and updated to match, not left describing stale content. A directory whose README no longer matches what's actually in it is a defect, the same as a broken link would be.
