# `code/` — the verification engine and its gates

| File | What it is |
|---|---|
| `collatz_verify.rs` | The engine. Rust, no external crates, `u128` arithmetic with explicit guards. Modes: `--self-test`, `--verify`, `--records`, `--block`, `--trace`. |
| `collatz_ref.py` | The reference. Pure Python, arbitrary-precision integers, no sieve, deliberately slow and deliberately obvious. If the two ever disagree, believe this one first. |
| `reference_crosscheck.py` | Runs both implementations on identical intervals at several sieve sizes and compares them quantity by quantity. |
| `anchors.py` | Exact two-sided comparison of the engine's record output against the archived OEIS snapshots in `../data/external/`. |
| `mutation_drill.py` | Plants defects in the engine one at a time, rebuilds, and checks that the gates catch each one — plus controls that must be caught by nothing. |
| `verify_run_logs.py` | Reads only the archived chunk logs and decides whether they actually tile `[3, N]`. Refuses to aggregate logs with a gap, an overlap, or a bad count. |
| `build_results.py` | Assembles `../data/results.v1.json` from archived gate logs only. Fails rather than emit a summary with a hole in it. |
| `run_verification.sh` | Drives a full run as disjoint, separately logged chunks. |
| `ot_paper02_recheck.py` | Independent re-derivation of Paper 02 of Neo.K's Operation Translation Series, written from the paper's theorem statements. Its referee route assumes no theorem of the paper at all. |
| `ot_paper06_recheck.py` | The same for Paper 06 (valuation language). Referee is direct iteration of the accelerated odd map on genuine odd integers, so every valuation word tested is one an actual integer produced. Also verifies §14's bridge back to Paper 02. |
| `ot_paper07_recheck.py` | The same for Paper 07 (generalized `(mx+r)`), over 24 `(m, r)` pairs. Evaluates the §17 geometric sum without ever dividing by `(m-2)`, so the `m = 1` case is reached with no singularity, and measures the Diophantine margin that makes the paper's floating floor safe. |
| `ot_paper09_recheck.py` | The same for Paper 09 (finite certificate frontier). Its sigma is the same definition the engine measures, so it links the archived `[3, 2^40]` run to the paper's K(N), and it reconciles §24's boundary corrections exactly. |
| `ot_recheck_drill.py` | Falsifiability drill for all four rechecks: perturbs each asserted formula and requires the check *named for that formula* to fail. |

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

python code/ot_paper02_recheck.py 16
python code/ot_paper06_recheck.py 20001
python code/ot_paper07_recheck.py 8 3000
python code/ot_paper09_recheck.py 11 20
python code/ot_recheck_drill.py
./build/collatz_verify.exe --block 16 --to 1048576
```

On a cp950 Windows host, prefix the Python commands with `PYTHONUTF8=1` — these
scripts print UTF-8 JSON containing CJK, and the default console encoding cannot
carry it. (The same class of defect was found in the subject package's own
verifier; see `../reports/RUN-002-OT-SERIES.md`.)

The gate scripts write their JSON to stdout; the archived copies used to build
`results.v1.json` live in `../data/gate-logs/`.

`--sieve k` is a performance knob only. Every quantity the engine reports is
invariant under it, and the self-test fails if that stops being true.
