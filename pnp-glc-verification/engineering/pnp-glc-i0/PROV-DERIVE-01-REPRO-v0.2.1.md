# PROV-DERIVE-01 executable regression

Status: **Experiment / Counterexample regression**, not a P/NP claim.

Provenance:

- AI-2 reproduction script SHA-256: `E68BB2C26BF1655F34508EF418D51761BB689FB9E27E20A2EEB37F3C6FD7080D`.
- AI-1 v0.2 FAIL report SHA-256: `D528338E42C7EE1E684C8109C34BDA5BF3A1B1DDCC5643199E03AC280421B4B3`.
- Frozen v0.2 validator SHA-256: `4C50BE9EF563644BC29F3DCEEFB9D9205056631847980FCC763D1E4BA25EB771`.
- v0.2.1 candidate validator SHA-256: `C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4`.

## Case A: fabricated states

Mutation:

```text
record.ledger.counts.states = 999
trace.resource_samples.counts.states = 999
```

The fixture is signed with the valid test key and updates trace/projection/receipt bindings. Expected v0.2.1 derivation:

```text
trace_authenticity_pass = pass
replay_pass              = pass   # mirror/chain layer remains consistent
transition_execution     = pass
resource_derivation      = fail   # distinct event states derive 3, not 999
admission_pass           = false
final_completion         = false
record_accepted          = false
```

## Case B: fabricated transition digest

Mutation:

```text
events[0].output_sha256 = sha256:eeee...eeee
events[1].input_sha256  = sha256:eeee...eeee
trace.events            = mutated record.events
```

Again, the synchronized trace is validly signed and all bindings are refreshed. Expected v0.2.1 derivation:

```text
trace_authenticity_pass = pass
replay_pass              = pass   # mirror/chain layer remains consistent
resource_derivation     = pass
transition_execution    = fail   # pinned PARITY execution derives a different digest
admission_pass           = false
final_completion         = false
record_accepted          = false
```

The regression deliberately keeps `StructuralReplay=pass` in both cases. This demonstrates that rejection comes from execution/resource derivation rather than from a stale hash, broken signature, wrong parity answer, or trace/record inequality.

