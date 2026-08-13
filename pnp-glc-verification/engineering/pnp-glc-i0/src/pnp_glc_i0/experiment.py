"""Reproducible bounded I0 experiment runner."""

from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path
from time import perf_counter_ns
from typing import Any

from .oracles import (
    assignment_satisfies_2sat,
    exhaustive_2sat,
    parity_oracle,
    verify_unsat_certificate,
)
from .parity import TruthTableFamily, stream_parity, verify_prefix_invariant
from .semantic_validator import validate_path
from .two_sat import solve_2sat


def _timed(callable_: Any, *args: Any) -> tuple[Any, int]:
    started = perf_counter_ns()
    result = callable_(*args)
    return result, perf_counter_ns() - started


def run_i0(project_root: Path, *, seed: int = 20260809, max_parity_n: int = 12) -> dict[str, Any]:
    schema = project_root / "schemas" / "run-record.schema.v0.2.0-candidate.json"
    fixtures = project_root / "fixtures"

    admission: dict[str, Any] = {}
    for name in (
        "legit",
        "cheat",
        "unknown-gate",
        "self-report",
        "robust-null-spec",
        "neutral-legit",
        "robust-neutral-legit",
        "failed-gate-admission",
        "false-final-completion",
        "tampered-record",
        "tampered-trace",
        "unresolved-event-ref",
        "circular-field",
        "canonicalization-variant",
    ):
        report = validate_path(fixtures / f"{name}.json", schema, project_root)
        admission[name] = {
            "structural_ok": report.structural_ok,
            "semantic_ok": report.semantic_ok,
            "admission_pass": report.admission_pass,
            "final_completion": report.final_completion,
            "record_accepted": report.record_accepted,
            "issue_codes": sorted({issue.code for issue in report.issues}),
        }

    rng = random.Random(seed)
    fixed_program_scaling = []
    pointwise_envelope = []
    for n in range(max_parity_n + 1):
        bits = tuple(rng.randrange(2) for _ in range(n))
        stream, stream_time = _timed(stream_parity, bits)
        fixed_program_scaling.append(
            {
                "n": n,
                "series_semantics": "fixed-program-scaling",
                "build_time_ns": 0,
                "generation_time_ns": 0,
                "update_decode_time_ns": stream_time,
                "program_family_count": 1,
                "advice_bytes": 0,
                "answer": stream.answer,
                "oracle_pass": parity_oracle(bits, stream.answer),
                "invariant_pass": verify_prefix_invariant(bits, stream),
            }
        )

        table, generation_time = _timed(TruthTableFamily.build, n)
        answer, decode_time = _timed(table.decide, bits)
        pointwise_envelope.append(
            {
                "n": n,
                "series_semantics": "pointwise-envelope",
                "build_generation_time_ns": generation_time,
                "decode_time_ns": decode_time,
                "programs_for_length": 1,
                "program_quantifiers": "for-all-lengths-exists-program",
                "table_entries": 1 << n,
                "advice_bytes": table.advice_bytes,
                "answer": answer,
                "oracle_pass": parity_oracle(bits, answer),
            }
        )

    two_sat_cases = [
        {
            "id": "sat-basic",
            "variables": 3,
            "clauses": [(1, 2), (-1, 2), (-2, 3)],
        },
        {
            "id": "unsat-unit-pair",
            "variables": 1,
            "clauses": [(1, 1), (-1, -1)],
        },
    ]
    two_sat_results = []
    for case in two_sat_cases:
        result, solve_time = _timed(
            solve_2sat,
            case["variables"],
            case["clauses"],
        )
        if result.status == "sat":
            oracle_pass = assignment_satisfies_2sat(
                case["clauses"], result.assignment or {}
            )
            certificate_kind = "assignment"
        else:
            oracle_pass = verify_unsat_certificate(
                case["clauses"],
                result.unsat_variable or 0,
                result.positive_to_negative,
                result.negative_to_positive,
            )
            certificate_kind = "mutual-implication-paths"
        exhaustive, oracle_time = _timed(
            exhaustive_2sat,
            case["variables"],
            case["clauses"],
        )
        two_sat_results.append(
            {
                **case,
                "baseline": "implication-graph-plus-SCC",
                "status": result.status,
                "certificate_kind": certificate_kind,
                "certificate_oracle_pass": oracle_pass,
                "exhaustive_crosscheck_pass": (exhaustive is not None)
                == (result.status == "sat"),
                "solve_time_ns": solve_time,
                "oracle_time_ns": oracle_time,
            }
        )

    return {
        "experiment_id": "I0-20260809",
        "status": "Experiment",
        "seed": seed,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "parallel_workers": 1,
        },
        "terminal_only_projection": {
            "legit": {"Y": 1, "C": 1, "outstanding_debt": 0, "decode": "O(n)"},
            "cheat": {"Y": 1, "C": 1, "outstanding_debt": 0, "decode": "O(n)"},
            "excludes": ["admission_pass", "provenance", "construction", "advice"],
            "observation": "terminal-only fields are intentionally indistinguishable",
        },
        "admission": admission,
        "parity": {
            "uniform_fixed_program_scaling": fixed_program_scaling,
            "nonuniform_pointwise_envelope": pointwise_envelope,
            "failure_frontier": {
                "table_materialization_limit": max_parity_n,
                "dominant_hidden_cost": "2^n table/advice generation",
            },
        },
        "two_sat": {
            "baseline": "implication-graph-plus-SCC",
            "correctness_oracles": [
                "SAT assignment checker",
                "UNSAT mutual implication path checker",
                "small-instance exhaustive crosscheck",
            ],
            "cases": two_sat_results,
            "failure_frontier": [
                "clauses wider than two literals",
                "general CNF cannot be converted to 2-CNF for free",
                "incremental update bounds are not claimed",
            ],
        },
        "nonclaims": [
            "experimental acceleration does not imply P=NP",
            "experimental failure does not imply P!=NP",
        ],
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--max-parity-n", type=int, default=12)
    args = parser.parse_args()

    report = run_i0(
        args.project_root.resolve(),
        seed=args.seed,
        max_parity_n=args.max_parity_n,
    )
    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
