# `code/` — the verification engine and its gates

| File | What it is |
|---|---|
| `collatz_verify.rs` | The engine. Rust, no external crates, `u128` arithmetic with explicit guards. Modes: `--self-test`, `--verify`, `--records`, `--trace`. |
| `collatz_ref.py` | The reference. Pure Python, arbitrary-precision integers, no sieve, deliberately slow and deliberately obvious. If the two ever disagree, believe this one first. |
| `reference_crosscheck.py` | Runs both implementations on identical intervals at several sieve sizes and compares them quantity by quantity. |
| `anchors.py` | Exact two-sided comparison of the engine's record output against the archived OEIS snapshots in `../data/external/`. |
| `mutation_drill.py` | Plants defects in the engine one at a time, rebuilds, and checks that the gates catch each one — plus controls that must be caught by nothing. |
| `verify_run_logs.py` | Reads only the archived chunk logs and decides whether they actually tile `[3, N]`. Refuses to aggregate logs with a gap, an overlap, or a bad count. |
| `build_results.py` | Assembles `../data/results.v1.json` from archived gate logs only. Fails rather than emit a summary with a hole in it. |
| `run_verification.sh` | Drives a full run as disjoint, separately logged chunks. |

No third-party dependencies. `requirements.txt` is empty on purpose — the
Python here is standard library only, so there is no version of a numeric
package that could quietly change an answer.

## Reading order for the engine

`collatz_verify.rs` is written to be read top to bottom:

1. the header comment states what a completed run does and does not prove;
2. `build_tables` derives the `k`-step congruence tables by simulation, so the
   sieve is a computation rather than an assumed closed form;
3. `descend_below` is the only place the map is iterated during verification,
   and both guards live in its loop;
4. `verify_range` uses the `k`-step jump **only as a filter** — whenever the
   filter does not settle the question it re-walks from `n` itself, because the
   trajectory may dip below `n` and rise again within the first `k` steps;
5. `self_test` is the internal gate, including a check that the overflow guard
   still trips.

## Commands

```bash
rustc -O --edition 2021 code/collatz_verify.rs -o build/collatz_verify.exe

./build/collatz_verify.exe --self-test
./build/collatz_verify.exe --from 3 --to 1000000000 --sieve 20 --threads 16
./build/collatz_verify.exe --records 10000000 --threads 16
./build/collatz_verify.exe --trace 27

python code/collatz_ref.py 3 300000
python code/collatz_ref.py constants
python code/reference_crosscheck.py 3 300000
python code/anchors.py 100000000
python code/mutation_drill.py
python code/verify_run_logs.py --tag t40 --expect-to 1099511627776
python code/build_results.py --tag t40 --expect-to 1099511627776
```

The gate scripts write their JSON to stdout; the archived copies used to build
`results.v1.json` live in `../data/gate-logs/`.

`--sieve k` is a performance knob only. Every quantity the engine reports is
invariant under it, and the self-test fails if that stops being true.
