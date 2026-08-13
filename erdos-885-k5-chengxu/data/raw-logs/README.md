# Raw run logs

These are the original stdout and stderr captures from the independent route. Rust progress and record updates were intentionally written to stderr, so a nonempty `.err.log` is not by itself a failed run. Empty streams and interrupted or superseded chunks are retained as provenance; they are not evidence of a mathematical result.

For the aggregate claims, `../../code/verify_run_logs.py` uses an explicit allow-list of completed, disjoint ranges. In particular, the incomplete aggregate runs for public packets 64–71 are superseded by the eight completed per-packet logs, and the `_v2` direct-search logs supersede earlier interrupted chunks.

`SHA256SUMS` covers all 119 original `.log` files byte-for-byte. The verifier checks this manifest before interpreting any completed run.

Four logs retain non-secret machine-local source/temporary paths emitted by PowerShell or Rust. They are intentionally preserved for byte integrity; the secret-pattern scan found no credential material.
