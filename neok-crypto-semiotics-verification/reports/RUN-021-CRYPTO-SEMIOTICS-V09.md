# RUN-021 — Crypto–Semiotics Theory Compiler v0.9: the model was repaired, TLC was run here, and the repair moved a gap rather than closing it

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `NeoK_Crypto_Semiotics_Theory_Compiler_v0.9.zip` (source item 39) — the theory compiler through its v0.9 *External Formal Validation Attempt*
**Tools:** [`cs03_v09_models.py`](../code/cs03_v09_models.py) · [`cs03_drill.py`](../code/cs03_drill.py) · [`cs03_emit_report_block.py`](../code/cs03_emit_report_block.py)
**Logs:** [`cs03-v09-models.json`](../data/gate-logs/cs03-v09-models.json) · [`cs03-drill.json`](../data/gate-logs/cs03-drill.json) · [`tlc-v09.log`](../data/tlc-v09.log)

**Result: every number the package reports reproduces, under a method it did not use. TLC was obtained and run here, which the package says it could not do, and it agrees with both. One finding, and it is structural rather than arithmetic.**

---

## What v0.9 is

One new layer, `13_external_formal_attempt_v0.9`, and it is a direct answer to
what [RUN-020](./RUN-020-CRYPTO-SEMIOTICS-V08.md) found. That run reported that
the shipped TLA+ runtime model specified a weaker system than the one which had
been validated in Python, that `Rollback` was unreachable in it, and that TLC had
never been run against anything.

v0.9 repairs the model, revalidates the CTCL model symbolically with SymPy, adds
fairness so the liveness property is meaningful, drafts the Ω-wrapper reduction —
and then **refuses to promote anything to G4**, because no model checker was
available in the sandbox that produced it. Its own status file says so plainly:
`tlc_execution: NOT RUN`. The package is honest about its own blocker, which is
the posture that makes the rest of it worth checking rather than worth arguing
with.

Its report states the correction in one sentence: *the v0.8 TLA model did not
actually make authorization/verification environment outcomes reachable and lacked
fairness for liveness.*

## The repair is real, and it is bigger than one branch

The mechanism is visible in the TLA+ text and is worth naming precisely, because
"the model was wrong" is not a diagnosis.

In the v0.8 model, `authorized` and `verificationOK` are **never assigned by any
action**. `Init` sets both `TRUE` and every action leaves them `UNCHANGED`. So
`VerifyFail`, whose guard is `~verificationOK`, and `Deny`, whose guard is
`~(authorized /\ …)`, can never be enabled — and `RollbackDone` is unreachable
behind `VerifyFail`. Three of the fourteen actions were dead, and both of the
model's *environment* outcomes were among them. A model in which the environment
never says no is a model of a system that cannot fail.

In v0.9 those outcomes became nondeterministic assignments rather than guards on
variables nothing writes: `ApplyResponse` sets `authorized' = TRUE`, `Deny` sets
it `FALSE`, `VerifyOK` and `VerifyFail` do the same for `verificationOK`. Every
action is now live and every stage is reachable.

**This arm did not take the counts on trust and did not run the package's own
script.** The TLA+ text was transcribed by hand into an independent enumerator,
and both models were walked from their own initial states. The before and after
are measured, not recalled.

## TLC was run here

The package's blocker was environmental, not mathematical: Java was present, TLC
was not, and its sandbox could not reach the network. That is a blocker this arm
does not have.

`tla2tools.jar` v1.7.4 was fetched and its SHA-1 compared against the value the
package itself recorded — `bee4a54f3ee3d4afc347c3240ec2d9e93b075104` — which
matched, so the package's recorded expectation is confirmed too. The package's own
`run_tlc_when_available.sh` was then used unmodified, which exercises the script as
well as the models. The full transcript is archived as
[`tlc-v09.log`](../data/tlc-v09.log).

**This is not a redundant third opinion.** The package's script and this arm's
enumerator are both *transcriptions* of the TLA+ text, and two transcriptions can
be wrong in the same place. TLC is the only participant that reads the artifact
itself. It is also the only one that checked the **liveness** property: both the
package and this arm had only a hand argument that no cycle avoids `Learn`, where
TLC evaluates `[]<>(stage = "Learn")` under `WF_vars(Next)` over the whole state
space.

Both models check clean, with no error, and the state counts, the generated
counts and the search depths all reconcile with the independent walk.

## The CTCL half, by a different method

The package establishes six symbolic results with SymPy satisfiability. Sixteen
states is small enough to settle by exhaustion instead, which is a different
method rather than the same solver run twice. All six reproduce, including the
sharp one: **`CloudOnlySecrecy` holds on every reachable state but is not
inductive by itself**, failing under exactly two actions.

This run adds one thing the package does not claim. The strengthened invariant —
`CloudOnlySecrecy` together with `plaintextKnown => clientKeyStolen` and
`plaintextKnown => uploaded` — does not merely *imply* the property and survive
every action. Its satisfying set is **exactly** the reachable set, in both
directions. So the strengthening is not one of several sufficient choices; it
characterises reachability, which means it is the strongest inductive invariant
available for this model and no further auxiliary is possible or needed.

The two counterexamples to the unstrengthened induction are recorded in the gate
log rather than merely asserted to exist.

## The finding: the repair moved a gap instead of closing it

The runtime model exists to discharge one obligation, `OBL-N21-005-008`, whose
completion criteria are:

> The model excludes unauthorized high-risk actions, **records rollback paths** and
> demonstrates progress under fair scheduling.

Its claim, `CL-N21-005`, is a **definition**:

> 常駐安全循環為 Observe → Model → Detect → Prioritize → Respond → Verify → Learn。

Seven stages. The obligation's `symbol_ids` list exactly those seven, and a scan
of the entire package finds exactly those seven `SYM-RUNTIME-*` symbols in
existence. **There is no rollback symbol and no approval symbol anywhere in the
registry** — so this is a gap in the definitions, not a broken link.

Now put the two together:

- In **v0.8** the model matched the claim's seven stages and **failed the
  completion criterion**: it could not record a rollback path, because the branch
  that records one was unreachable. The obligation was nevertheless advanced to
  `partially_satisfied`, and the ledger's stated reason is that the TLA+ artifact
  and a Python validation *exist*. Existence was read as satisfaction.
- In **v0.9** the model meets the criterion — rollbacks are recorded — and now
  **exceeds its claim by two stages**, neither of which the claim defines or the
  symbol table names.

The gap did not close. It moved from *the artifact does not do what the criterion
asks* to *the artifact does more than the claim defines*. Both are real, and the
second is the easier one to miss, because the artifact now looks better.

This is not an argument that the model is wrong. A security loop with an approval
wait and a rollback path is obviously the more faithful model of the thing being
described. The point is narrower and, for a theory compiler, sharper: **the
compiler's own traceability says this artifact is evidence for a seven-stage
definition, and it is evidence for a nine-stage one.** Either the claim text and
symbol set should grow to match, or the obligation should say which parts of the
model are outside its claim. Deciding which is Neo's call, not this arm's.

## The one anomalous promotion profile is the same claim

RUN-020 reported that exactly one of the shipped promotion profiles violates the
gate rule the package states in prose. This run identifies it: `CL-N21-005` is the
only profile marked `ready_at_target` while still carrying an unresolved blocking
obligation, and that obligation is `OBL-N21-005-008` — the one the whole of layer
13 exists to advance.

That is not a coincidence and it is not, by itself, a defect. It is what a claim
under active work looks like in a promotion table. It is worth saying only because
the anomaly and the new layer point at the same place, which is a reason to fix
the profile rule rather than the claim.

## Measured

<!-- BEGIN GENERATED measured block: python code/cs03_emit_report_block.py -->

| what | measured | value |
| --- | --- | --- |
| the archive | bytes | `3481122` |
|  | manifest entries whose SHA-256 verifies | `14` |
|  | manifest mismatches | `0` |
| the repaired runtime model | reachable states | `62` |
|  | non-stuttering edges | `86` |
|  | stages reached | `9` |
|  | actions never enabled | `0` |
|  | states in which a rollback is recorded | `2` |
|  | safety invariants holding on every reachable state | `4` |
| the model it replaces | reachable states | `16` |
|  | non-stuttering edges | `19` |
|  | stages reached | `8` |
|  | actions never enabled | `3` |
| the CTCL model, by exhaustion | states enumerated | `16` |
|  | reachable states | `10` |
|  | actions that fail to preserve CloudOnlySecrecy | `2` |
|  | actions that preserve the strengthened invariant | `5` |
| TLC, run here | models checked | `2` |
|  | models completing with no error | `2` |
|  | errors reported | `0` |
|  | distinct states, CTCL | `10` |
|  | distinct states, runtime | `62` |
| the checks themselves | defects planted | `6` |
|  | caught, each for the reason named | `6` |
|  | null controls undisturbed | `2` |
|  | controls requiring the comparison to be able to reject | `7` |

**The three agreeing methods.** The package's own script, this arm's independent hand transcription of the TLA+ text, and TLC reading the `.tla` files themselves all give `62` reachable states for the repaired runtime model. TLC additionally reports `87` states generated, which is one initial state plus this arm's `86` edges, and a search depth of `20`, which is this arm's edge distance `19` plus one — TLC counts states on the longest path where this arm counts steps. Stating the convention is the difference between a reconciliation and an off-by-one nobody chased.

**What was dead before.** `Deny`, `RollbackDone`, `VerifyFail` — every action whose guard tested the negation of a variable that no action ever assigned.

**The symbol set.** The package contains `7` `SYM-RUNTIME-*` symbols in total: `SYM-RUNTIME-DETECT`, `SYM-RUNTIME-LEARN`, `SYM-RUNTIME-MODEL`, `SYM-RUNTIME-OBSERVE`, `SYM-RUNTIME-PRIORITIZE`, `SYM-RUNTIME-RESPOND`, `SYM-RUNTIME-VERIFY`. There is no rollback symbol and no approval symbol, while the repaired model has `9` stages.

**The anomalous profile.** Of `264` promotion profiles, `1` is marked `ready_at_target` while still carrying an unresolved blocking obligation: `CL-N21-005`.

Every figure above is emitted by `code/cs03_emit_report_block.py` from the two gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

## What this run does **not** establish

- **Not G4.** Running TLC here settles the *technical* prerequisite the package
  named — a model checker has now accepted both models with their safety and
  liveness properties — but promotion is a governance decision under the package's
  own policy, which requires external validation rather than any single run by an
  interested party. This arm is an interested party. The decision is Neo's.
- **Not the Ω-wrapper reduction.** It remains a paper draft. Its confidentiality
  step is an equality and its integrity step an inequality with a parser term, and
  that asymmetry is correct for a public deterministic injective encoding — but
  correct-as-a-sketch is what it claims to be, and it lists its own uncovered
  cases.
- **Not the implementation.** No code path, key handling, or envelope construction
  was executed or audited here. The models are models.
- **Not the 23.9 MiB v0.8 payload**, which is still not mirrored into this tree;
  only hashes are recorded.

## A defect of this arm's own, found by its drill

The first version of `cs03_v09_models.py` computed the package's headline claim —
that every action preserves the strengthened invariant — put it in the output, and
**compared it against nothing**. A planted defect that deleted the two auxiliary
invariants left the gate green. The finding this run *adds*, that the strengthening
characterises reachability exactly, was ungraded in the same way.

Both are graded now, and the lesson is the one this arm keeps relearning in new
costumes: **a quantity that is emitted but never compared is decoration, and a
finding that is published but not graded is prose.** The drill is what said so.

A second, smaller one: the obvious anchor for one planted defect matched twice,
because TLC prints its counts on a progress line and again in the final summary.
Spanning the newline to disambiguate then failed as well — the transcript's line
endings are mixed CRLF and LF. The drill's `count == 1` guard reported both as
**uncaught** rather than silently mutating a look-alike.

## Provenance

The archive was read from Neo's source folder and not modified. Its SHA-256 and
byte count are in the gate log. The v0.9 layer's own manifest was verified entry
by entry; every hash matches and the only unlisted file in the layer is the
manifest itself, which cannot list its own hash.

`tla2tools.jar` was fetched for this run, verified against the package's recorded
SHA-1, used, and left out of this repository — it is a third-party binary and a
recorded hash is the archival artifact, not the jar.

**Next:** item 40. If it continues this line, the first question is whether
`CL-N21-005`'s claim text or symbol set grew to cover the approval and rollback
stages, and whether the promotion rule that lets `ready_at_target` coexist with an
unresolved blocker was changed or defended.
