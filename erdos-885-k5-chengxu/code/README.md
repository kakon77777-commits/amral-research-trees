# Code

The six original source files are preserved byte-for-byte. Two small archive verifiers were added afterward:

- `search_dual_k64.rs` — exhaustive `K_(6,3)` / `K_(6,4)` pair-fiber search; the historical filename predates the generic `--rows 3|4` interface.
- `verify_boundary_packets.py` — independent divisor-enumeration checks of exact displayed packets.
- `audit_public_4x6.py` — online parser and exact closure audit of the public 71-packet page.
- `search_scaled_public_4x6.py` — preliminary positive-shift scalar search.
- `search_signed_scaled_public_4x6.py` — complete signed scalar-closure search used for the reported result.
- `search_choudhry_closure.py` — exact bounded search in Choudhry's seven-parameter family.
- `replay_public_4x6_snapshot.py` — runs the public-packet audit against the archived JSON instead of the network.
- `verify_run_logs.py` — checks disjoint range coverage and recomputes the reported aggregate counts from completed logs.

Compiled `.exe` and `.pdb` files are deliberately excluded as regenerable build artifacts. Build the Rust source with `rustc` as shown in the parent README.
