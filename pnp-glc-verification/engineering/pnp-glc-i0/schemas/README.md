# schemas/

`run-record.schema.vX.Y.Z-candidate.json` -- one JSON Schema per candidate version,
each a stricter/extended version of the run-record structural transport schema
described in `../README.md`. Each schema encodes one-way, fail-closed conditionals
(declaring a gate `pass` doesn't let you also skip proving its prerequisites); see
`../SCHEMA-DIFF-vX-to-vY.md` for a human-readable diff between any two consecutive
versions.
