# AMRAL AI Research-Tree Protocol

This is the repository-level persistence contract for future AI research under Neo.K's direction. Its purpose is simple: another human or AI should be able to discover what existed, distinguish claims from evidence, and replay the computational part without access to the originating chat.

## One research line, one top-level tree

Create a descriptive top-level directory and add a matching row to the root `README.md`. Do not silently merge an independent route into another agent's tree, rewrite another agent's provenance, or treat proximity in the repository as agreement between researchers.

Every research-tree root must contain a `README.md` stating:

- researcher or agent identity, date, problem, route, and collaboration boundary;
- exact epistemic status, especially whether the problem is solved, only reduced, or only searched inside finite bounds;
- a map of reports, code, data, logs, and their recommended reading order;
- reproducible commands and observed tool versions when computation matters;
- source URLs, snapshots, digests, and known external antecedents when relevant.

## Preserve the evidence layers

Use subdirectories that fit the work, normally `reports/`, `code/`, and `data/`. Keep machine-readable results beside prose conclusions. Preserve raw completed run streams when they are material to a numerical claim, including negative results and superseded attempts; label incomplete or superseded runs rather than deleting history. Exclude secrets, caches, compiled binaries, debugger files, and regenerable build output.

Do not promote any of the following into a global mathematical conclusion:

- a finite search with no hit;
- a timeout, crash, resource limit, or software error;
- verification relative to one implementation;
- an exact certificate for a neighboring or weaker problem;
- the fact that a file has been published in this repository.

## Publish as a durable handoff

Before publishing, verify the intended file scope, preserve unrelated working-tree changes, run the cheapest decisive replay checks, scan the staged material for secrets and machine-local paths, and inspect the final diff. Commit with a single-purpose message and push to the repository's GitHub remote using its current branch/review policy. Record any failed or incomplete publication step explicitly; a local commit must not be described as public GitHub state.

Git history is part of the provenance. Avoid destructive history rewrites and do not replace a newer research tree with an older local copy.
