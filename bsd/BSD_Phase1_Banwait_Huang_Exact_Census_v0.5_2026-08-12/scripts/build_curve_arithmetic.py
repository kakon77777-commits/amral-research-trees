#!/usr/bin/env python3
"""Extract exact arithmetic needed to replay the historical Algorithm 2 gate."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

from build_algorithm1_metadata import (
    band_name,
    discriminant,
    get_git_commit,
    json_dump,
    load_base_rows,
    parse_cremona,
    sha256,
)


def prime_factors(n: int) -> list[int]:
    n = abs(int(n))
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        factors.append(n)
    return factors


def valuation(n: int, p: int) -> int:
    n = abs(int(n))
    value = 0
    while n and n % p == 0:
        n //= p
        value += 1
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--ecdata", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    ecdata = args.ecdata.resolve()
    output = args.output or root / "inputs" / "metadata" / "old_base_curve_arithmetic.json"
    old_rows = load_base_rows(root / "inputs" / "old" / "ec_labels_500k.txt")
    wanted = set(old_rows)
    bands = sorted({band_name(parse_cremona(label)[0]) for label in wanted})

    curves: dict[str, tuple[list[int], str, Path]] = {}
    mappings: dict[str, tuple[str, str, Path]] = {}
    touched: set[Path] = set()
    for band in bands:
        curve_path = ecdata / "allcurves" / f"allcurves.{band}"
        label_path = ecdata / "alllabels" / f"alllabels.{band}"
        for path in (curve_path, label_path):
            if not path.is_file():
                raise FileNotFoundError(path)
            touched.add(path)
        for line in curve_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 6:
                raise ValueError(f"bad allcurves line: {line}")
            label = f"{parts[0]}{parts[1]}{parts[2]}"
            if label in wanted:
                curves[label] = (list(map(int, ast.literal_eval(parts[3]))), line, curve_path)
        for line in label_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 6:
                raise ValueError(f"bad alllabels line: {line}")
            label = f"{parts[0]}{parts[1]}{parts[2]}"
            if label in wanted:
                mappings[label] = (f"{parts[3]}.{parts[4]}{parts[5]}", line, label_path)

    missing_curves = sorted(wanted - set(curves))
    missing_mappings = sorted(wanted - set(mappings))
    if missing_curves or missing_mappings:
        raise RuntimeError(
            f"ecdata coverage failure: curves={missing_curves[:10]}, mappings={missing_mappings[:10]}"
        )

    records = []
    label_mismatches = []
    for label in sorted(wanted, key=parse_cremona):
        row = old_rows[label]
        ainvs, curve_line, curve_path = curves[label]
        mapped_lmfdb, label_line, label_path = mappings[label]
        if mapped_lmfdb != row.lmfdb_label:
            label_mismatches.append(
                {"curve_label": label, "input": row.lmfdb_label, "ecdata": mapped_lmfdb}
            )
        conductor = parse_cremona(label)[0]
        delta = discriminant(ainvs)
        bad_primes = prime_factors(conductor)
        records.append(
            {
                "curve_label": label,
                "lmfdb_label": row.lmfdb_label,
                "source": row.source,
                "conductor": conductor,
                "ainvs": ainvs,
                "discriminant": delta,
                "conductor_primes": bad_primes,
                "discriminant_valuations": {str(p): valuation(delta, p) for p in bad_primes},
                "evidence": {
                    "allcurves_path": curve_path.relative_to(ecdata).as_posix(),
                    "allcurves_line": curve_line,
                    "alllabels_path": label_path.relative_to(ecdata).as_posix(),
                    "alllabels_line": label_line,
                },
            }
        )

    source_files = [
        {
            "path": path.relative_to(ecdata).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(touched)
    ]
    checks = {
        "record_count_matches_old_base": len(records) == len(old_rows),
        "all_labels_unique": len({record["curve_label"] for record in records}) == len(records),
        "cremona_to_lmfdb_mapping_exact": not label_mismatches,
        "all_conductor_prime_valuations_positive": all(
            all(value > 0 for value in record["discriminant_valuations"].values())
            for record in records
        ),
    }
    payload = {
        "schema_version": "1.0",
        "provenance": {
            "ecdata_repository": "https://github.com/JohnCremona/ecdata.git",
            "ecdata_commit": get_git_commit(ecdata),
            "method": "ecdata allcurves/alllabels extraction and exact integer discriminant factor valuations",
            "source_files": source_files,
        },
        "old_base_count": len(old_rows),
        "checks": checks,
        "diagnostics": {"label_mismatches": label_mismatches},
        "records": records,
    }
    json_dump(output, payload)
    print(json.dumps({"output": str(output), "record_count": len(records), "checks": checks}, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
