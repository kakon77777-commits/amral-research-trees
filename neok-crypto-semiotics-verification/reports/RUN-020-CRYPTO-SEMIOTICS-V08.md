# RUN-020 — Crypto–Semiotics Theory Compiler v0.8: the counts all reproduce, and the two things that do not are both about artifacts that were never re-run

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `NeoK_Crypto_Semiotics_Theory_Compiler_v0.8.zip` (source item 38) — the theory compiler through its v0.8 *Obligation Execution Layer*
**Source SHA-256:** `b0a7ae85f94c2e9ee748ad96bb4f7585295770d7c6e338d43b24be6867a54e47` (3,467,925 bytes, 290 entries, 23.9 MiB unpacked)
**Tools:** [`cs01_v08_recheck.py`](../code/cs01_v08_recheck.py) · [`cs02_guard_pinning.py`](../code/cs02_guard_pinning.py) · [`cs01_drill.py`](../code/cs01_drill.py)
**Logs:** [`cs01-v08-recheck.json`](../data/gate-logs/cs01-v08-recheck.json) · [`cs02-guard-pinning.json`](../data/gate-logs/cs02-guard-pinning.json) · [`cs01-drill.json`](../data/gate-logs/cs01-drill.json)

**Result: 11/11 checks. 11/11 planted defects caught by the check named for each. 1/1 null control undisturbed. Coverage audit clean.**

---

## The sweep leaves Hard-Zeta here

Items 1–37 were Collatz. Item 38 is a different subject and the instruments
change with it. This is not a paper: it is a compiler that turns 264 claims into
2,490 formal obligations under a seven-gate promotion model, plus a v0.8 layer
that advances three claims by shipping executable security models — an
AES-256-GCM carrier wrapper, an X25519/HKDF/AES-GCM cloud-compromise capsule,
and a persistent-security-runtime state machine — each with a pytest suite and a
TLA+ specification.

So the questions are different. Not "does the proof hold" but: do the counts
recompute, do the profile fields follow the rule the prose states, does the
shipped data validate against the shipped schema, do the formal artifacts
specify the models that were actually validated, and does "7/7 tests passed"
mean the guards are pinned.

**The package is honest about its own limits, and that made this run easier.** It
says in its own words that internal wrapper validation is not a cryptographic
proof, that the X25519 envelope is a reference KEM-DEM construction and not
RFC 9180 HPKE, that no independent review has happened, and — the sentence that
turned out to matter most — that **TLC/Apalache was not run in this environment.**

## What reproduces

Everything countable.

| Figure | README says | recomputed |
|---|---|---|
| claims | 264 | **264** |
| formal obligations | 2490 | **2490** |
| evidence gaps | 608 | **608** |
| obligation dependency edges | 714 | **714** |
| promotion profiles | 264 | **264** |

The v0.8 layer carries the same population underneath the three claims it
advances: 2,490 obligations over 264 distinct claim ids, 264 profiles.

**Their own test suites reproduce on a different platform.** The shipped
`validation_results.json` was captured on Linux under `/opt/pyvenv` with pytest
9.0.2. Re-run here on Windows with pytest 9.1.1 and `cryptography` 49.0.0:
**7 + 7 + 4 = 18 passed**, `reachable_states` 10 and 62, zero violations —
identical. That is the cross-platform half the package cannot claim for itself.

**The CTCL trust model re-derives from its own TLA+.** Transcribing
`CTCL_CloudCompromise.tla` rather than their `finite_model.py`: `uploaded`,
`cloudCompromised` and `clientKeyStolen` are each monotone, and
`plaintextKnown` can only turn on when `uploaded ∧ clientKeyStolen`. So the
reachable set is the 8 states with `¬plaintextKnown` plus the 2 with it —
**10**, and both of those require the client key to be stolen, so
`CloudOnlySecrecy`'s antecedent is false throughout: **0 violations.** The model
does not overclaim endpoint security, and says so itself.

**The promotion rule from the prose reproduces 205 of 206 profiles.** The
quantifier is in `02_promotion_gate_spec.md`, not in the field name: for target
gate `G_k`, only blocking obligations at gate order **≤ k** count. Reading it
that way took `unresolved_blocking_count` from 15 disagreements to **1**, and
`promotion_decision` to 1.

## The two things that do not

Both are about artifacts that exist but were never re-run against the layer that
came after them. Neither touches a security claim.

### 1. The shipped TLA+ does not specify the model that was validated

`PersistentSecurityRuntime.tla` pins `authorized = TRUE` and
`verificationOK = TRUE` in `Init`, and **no action ever changes them** — both
appear in every `UNCHANGED` tuple. Therefore `VerifyFail`'s guard
`~verificationOK` is never enabled, the `Rollback` stage is unreachable, and
`rollbackRecorded` is always `FALSE`.

Running TLC on the file as written would explore **16 states** and would never
exercise the rollback behaviour the report highlights — "failed verification
forces rollback before learning".

Their `runtime_model.py` is a different, **stronger** model: it takes an explicit
environment choice at the `Respond` and `Verify` boundaries, letting the
environment set `authorized` and `verification_ok`. That is where 62 comes from,
and it decomposes exactly:

| `(authorized, verificationOK)` | states | `Rollback` reachable |
|---|---|---|
| `(T, T)` | 16 | no |
| `(T, F)` | 18 | **yes** |
| `(F, T)` | 14 | no |
| `(F, F)` | 14 | no |
| **union** | **62** | |

Adding two environment actions to the `.tla` reproduces **62 exactly**, makes
`Rollback` reachable, and leaves both safety properties intact — 0 states where a
high-risk response is applied without approval, 0 where one is applied
unauthorized. **So the gap is coverage, not correctness.** The validated model is
the stronger one; the formal artifact is weaker than advertised, and a future
TLC run would silently confirm less than a reader expects.

### 2. One profile escaped both the schema and the rule — the same one

Validating the shipped data against the shipped JSON Schema:

| data | rows | rejected |
|---|---|---|
| v0.7 promotion profiles | 264 | 0 |
| v0.7 obligations | 2490 | 0 |
| v0.8 obligations | 2490 | 0 |
| **v0.8 promotion profiles** | 264 | **1** |

The one rejection is `CL-N21-005`: `promotion_decision` is `"ready_at_target"`,
which the shipped enum does not contain — the only such value across all 264.

And `CL-N21-005` is also the **single** profile whose `unresolved_blocking_count`
does not follow the prose gate rule. Its eight obligations are six blocking at
gate ≤ G3 all `satisfied`, one non-blocking, and one at `G4_external_validation`
that is `partially_satisfied`. The rule gives 0 unresolved for target G3; the
profile says 1, counting the G4 one.

Both anomalies land on the same claim, and it is the third of the three the v0.8
layer executed. The coherent reading is that this profile was **edited rather
than regenerated**, so it missed both the generator and the validator the README
advertises.

### And a figure that cannot be re-derived at all

`readiness_score` is the v0.8 report's headline metric — "Readiness: 0.3182 →
0.75". No shipped document defines it and no shipped script computes it;
`promotion_gate.py` only prints it. Four candidate scopes were tried
(blocking/all obligations × gate-restricted/not); the best leaves **64 of 206**
claims unexplained. This arm has had the same problem in its own charter, so the
observation comes with a suggestion rather than a complaint: ship the generator,
or state the formula in the gate spec beside the promotion rule.

## Does "7/7 tests passed" mean the guards are pinned?

Each guard in the Ω-wrapper was removed in turn and **two** questions asked
separately, because they have different answers: does any of their tests go red,
and does the module's behaviour actually change.

| verdict | guards | meaning |
|---|---|---|
| **pinned** | 4 | a test goes red |
| **unpinned** | 3 | behaviour changes, no test notices |
| **redundant** | 2 | no test notices *and* nothing changes — `cryptography` re-catches it |

The three unpinned ones, with what the damaged module then accepts:

- **the carrier profile/glyph check** → accepts a carrier with a foreign profile
- **the canonicality check in `decode_packet`** → accepts a non-canonical
  re-encoding of the same packet
- **the packet-shape check** → accepts a packet carrying undeclared extra fields

None of these breaks AEAD confidentiality — the ciphertext is still authenticated
— but all three are carrier-level malleability the module deliberately refuses
and no test would notice losing. Three small tests would close it.

Reporting the redundant two as "unpinned" would have overstated the finding, and
reporting them together as "9 guards, 5 not covered" would have been wrong in
both directions. Hence the split.

## Findings about my own checks

**A vacuous mutation, caught by measuring.** The first version of the guard probe
used `aad if aad else b""` as the "recover ignores the aad" defect. That
expression is **identical to `aad` for every input**, so the probe reported an
unpinned guard where nothing had been changed. Corrected to `b""`, it is caught
by their random-round-trip test.

**A no-op with a mathematical reason.** Dropping the `(risk = Low ∨ approved)`
conjunct from `ApplyResponse` changes nothing, because `PrioritizeDone` already
refuses to enter `Respond` while risk is High and approval is absent — 0 of the 8
reachable `Respond` states satisfy it. That conjunct is redundant with the
upstream guard. The `authorized` conjunct is the one that is not doubled, and
that is what the drill now plants.

**Two checks assert a negative**, which is easy to make unfalsifiable by
accident. Both are drilled by making the negative *false* — readiness is fed a
circular computation that trivially matches, and the TLA+ transcription is given
the missing actions — and each must go red. Both do.

**Two comparisons I got wrong before the data corrected me**, recorded because
the pattern repeats: I compared the report's "unresolved blocking" against
`blocking_obligation_count` when the profile has a field literally called
`unresolved_blocking_count`, and I counted 80 "curated targets" with a regex that
counted repeat mentions. The package was right both times.

## What this does not establish

- **No cryptographic claim is verified here.** The reduction is not mechanized,
  there is no ProVerif/Tamarin model, no side-channel analysis and no independent
  review. The package says all of this itself.
- **The X25519/HKDF envelope is a reference construction**, not RFC 9180 HPKE,
  and this run does not test it against any production suite.
- **TLC/Apalache still has not been run** — the finding above is a *hand
  reachability analysis* transcribed from the TLA+ text, which is not the same
  thing as a model checker's verdict, though it is enough to establish the state
  counts and the unreachability of `Rollback`.
- The 23.9 MiB payload is **not mirrored into this tree**; only its SHA-256 is
  recorded. Whether to archive it in full is Neo's call.

**Next:** item 39 is `NeoK_Crypto_Semiotics_Theory_Compiler_v0.9.zip`, the same
line — expect it to be a layer on top of this one, and the first question is
whether `CL-N21-005` still carries `ready_at_target`.
