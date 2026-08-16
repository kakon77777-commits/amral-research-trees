# Crypto–Semiotics Theory Compiler — verification arm

**數學戰士「墜衡」 / AMRAL Research Lab.** Independent verification of Neo.K's
`NeoK_Crypto_Semiotics_Theory_Compiler` packages. Neo.K is the author of the
subject; this tree is only the instrument pointed at it.

The subject is a **theory compiler**: 264 claims compiled into 2,490 formal
obligations under a seven-gate promotion model, with layers that add governance
(v0.6), formal obligations (v0.7) and executable obligation *execution* (v0.8).
Each package carries every earlier layer inside `00_previous_layers/`.

## What this arm does, and does not

It **does** ask whether the package's own numbers, rules and artifacts are
consistent with the data it ships:

- do the README's headline counts recompute from the shipped JSONL;
- do the promotion-profile fields follow the rule the **prose** states, rather
  than a generator (which is not shipped);
- does the shipped data validate against the shipped JSON Schema;
- do the formal artifacts (TLA+) specify the models the Python actually
  validated;
- and does a green test suite mean the code's guards are pinned?

It does **not** verify any cryptographic claim. There is no reduction proof, no
ProVerif/Tamarin model, no side-channel analysis and no independent review — and
the subject says so itself in every module's *Current limit* section. Nothing
here should be read as strengthening a security claim.

## Standing rules, carried over from the Collatz arm

- **Reimplement the specification, not the program.** A paper plus a program is
  two claims. A referee written from the program can only confirm the program's
  own reading. Both state models here are transcribed from the `.tla` text.
- **Every check must have a defect naming it**, and a defect counts as caught
  only if *that* check fails. `cs01_drill.py` enforces coverage before the
  mutation loop runs.
- **Never mutate a comparison; mutate what is computed.** A loosened comparison
  is usually a no-op, and a no-op that looks like a caught defect is worse than
  no drill.
- **Separate instrument soundness from findings about the subject**, so a real
  defect in the subject's work is never indistinguishable from a broken checker.

## Runs

1. [`reports/RUN-020-CRYPTO-SEMIOTICS-V08.md`](./reports/RUN-020-CRYPTO-SEMIOTICS-V08.md)
   — source item 38, v0.8. Every countable figure reproduces (264 / 2490 / 608 /
   714), their three suites reproduce cross-platform (18 passed), and the CTCL
   trust model re-derives from its own TLA+ at 10 states with 0 violations. Two
   things do not, and both are artifacts that were never re-run against the layer
   after them: the shipped `PersistentSecurityRuntime.tla` reaches **16** states
   with `Rollback` **unreachable** against the reported 62 — two missing
   environment actions close the gap exactly, safety intact — and exactly **one**
   profile of 264 is rejected by the shipped schema, the same one that is the
   only exception to the prose gate rule.

## Running it

```bash
python code/cs01_v08_recheck.py
```

```bash
python code/cs02_guard_pinning.py
```

```bash
python code/cs01_drill.py
```

Each writes a JSON report to stdout; archived copies are in
[`data/gate-logs/`](./data/gate-logs/). Set `CS_SOURCE_ZIP` to point at the
package if it is not in Neo's default source folder. `cs02_guard_pinning.py`
**reports** rather than grades — its `ok` means the probe ran soundly, not that
it found nothing.

The 23.9 MiB source payload is not mirrored here; each run records the source
zip's SHA-256 so a reader can confirm which bytes were measured.

Licensed Apache-2.0 with the rest of `amral-research-trees`.
