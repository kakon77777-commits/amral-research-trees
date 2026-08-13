from __future__ import annotations

import argparse
import json
from pathlib import Path

from .parity import pointwise_table_envelope, stream_parity, verify_prefix_invariant
from .semantic_validator import validate_path
from .two_sat import solve_2sat


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pnp-glc-i0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate run-record fixtures")
    validate.add_argument("records", nargs="+", type=Path)
    validate.add_argument("--schema", required=True, type=Path)
    validate.add_argument("--artifacts", required=True, type=Path)
    validate.add_argument("--require-admission", action="store_true")

    parity = subparsers.add_parser("parity", help="run uniform streaming PARITY")
    parity.add_argument("bits")

    envelope = subparsers.add_parser("parity-envelope", help="show nonuniform table costs")
    envelope.add_argument("max_n", type=int)

    two_sat = subparsers.add_parser("2sat", help="solve clauses such as '1,-2 2,3'")
    two_sat.add_argument("variable_count", type=int)
    two_sat.add_argument("clauses")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "validate":
        exit_code = 0
        for record in args.records:
            report = validate_path(record, args.schema, args.artifacts)
            print(json.dumps({"record": str(record), **report.to_dict()}, ensure_ascii=False))
            if not report.record_valid or (args.require_admission and not report.admission_pass):
                exit_code = 1
        return exit_code
    if args.command == "parity":
        bits = tuple(int(character) for character in args.bits)
        result = stream_parity(bits)
        print(
            json.dumps(
                {
                    "answer": result.answer,
                    "prefix_invariant": verify_prefix_invariant(bits, result),
                    "steps": [step.__dict__ for step in result.steps],
                }
            )
        )
        return 0
    if args.command == "parity-envelope":
        print(json.dumps(pointwise_table_envelope(args.max_n)))
        return 0
    if args.command == "2sat":
        clauses = []
        for item in args.clauses.split():
            left, right = item.split(",", maxsplit=1)
            clauses.append((int(left), int(right)))
        result = solve_2sat(args.variable_count, clauses)
        print(
            json.dumps(
                {
                    "status": result.status,
                    "assignment": result.assignment,
                    "unsat_variable": result.unsat_variable,
                    "positive_to_negative": result.positive_to_negative,
                    "negative_to_positive": result.negative_to_positive,
                }
            )
        )
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
