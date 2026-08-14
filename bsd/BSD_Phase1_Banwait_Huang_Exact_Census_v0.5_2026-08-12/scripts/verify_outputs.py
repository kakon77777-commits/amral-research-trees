#!/usr/bin/env python3
"""Independent, read-mostly verifier for the v0.5 exact artifact census."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_sha1(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_base(path: Path) -> dict[str, dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header = "cremona_label,source,lmfdb_label"
    try:
        start = next(i for i, line in enumerate(lines) if line.replace(" ", "") == header)
    except StopIteration as exc:
        raise ValueError(f"base header not found: {path}") from exc
    rows: dict[str, dict[str, str]] = {}
    for row in csv.DictReader(lines[start:]):
        normalized = {key: value.strip() for key, value in row.items()}
        label = normalized["cremona_label"]
        if label in rows:
            raise ValueError(f"duplicate base label: {label}")
        rows[label] = normalized
    return rows


def parse_twists(path: Path) -> dict[str, set[int]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"twist map is not an object: {path}")
    result: dict[str, set[int]] = {}
    for label, values in raw.items():
        if not isinstance(label, str) or not isinstance(values, list):
            raise ValueError(f"invalid twist entry: {label!r}")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
            raise ValueError(f"non-integer twist for {label}")
        if len(values) != len(set(values)):
            raise ValueError(f"duplicate twist for {label}")
        result[label] = set(values)
    return result


def pair_set(rows: list[dict[str, str]]) -> set[tuple[str, int]]:
    return {(row["curve_label"], int(row["twist"])) for row in rows}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="defaults to ROOT/logs/independent_verification.json",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    report_path = args.report or root / "logs" / "independent_verification.json"
    results = root / "results"

    checks: dict[str, bool] = {}
    details: dict[str, object] = {}

    required = [
        "results/summary.json",
        "results/raw_file_manifest.json",
        "results/results_sha256.json",
        "results/base_removed.csv",
        "results/base_added.csv",
        "results/base_stable.csv",
        "results/algorithm1_removed_census.csv",
        "results/algorithm1_unexplained_removed.csv",
        "results/twists_removed_by_upstream_base_deletion.csv",
        "results/algorithm2_removed_twists.csv",
        "results/algorithm2_added_twists.csv",
        "results/algorithm2_stable_curve_census.csv",
        "results/new_base_twists.csv",
        "results/old_base_curves_missing_from_old_twist_map.csv",
        "inputs/metadata/algorithm1_removed_metadata.json",
    ]
    checks["required_files_present"] = all((root / path).is_file() for path in required)
    if not checks["required_files_present"]:
        missing = [path for path in required if not (root / path).is_file()]
        write_json(report_path, {"status": "FAIL", "checks": checks, "missing": missing})
        print(json.dumps({"status": "FAIL", "missing": missing}, indent=2))
        return 1

    summary = json.loads((results / "summary.json").read_text(encoding="utf-8"))
    manifest = json.loads((results / "raw_file_manifest.json").read_text(encoding="utf-8"))
    recorded_hashes = json.loads((results / "results_sha256.json").read_text(encoding="utf-8"))

    old_base = parse_base(root / "inputs" / "old" / "ec_labels_500k.txt")
    new_base = parse_base(root / "inputs" / "new" / "ec_labels_500k.txt")
    generator_base = parse_base(
        root / "sources" / "generator_7286794" / "ec_labels_500k.txt"
    )
    old_twists = parse_twists(root / "inputs" / "old" / "twists_of_ec_labels_500k.json")
    new_twists = parse_twists(root / "inputs" / "new" / "twists_of_ec_labels_500k.json")

    b_old = set(old_base)
    b_new = set(new_base)
    b_removed = b_old - b_new
    b_added = b_new - b_old
    b_stable = b_old & b_new
    old_keys = set(old_twists)
    new_keys = set(new_twists)
    missing_old = b_old - old_keys

    computed_base = {
        "old": len(b_old),
        "new": len(b_new),
        "removed": len(b_removed),
        "added": len(b_added),
        "stable": len(b_stable),
    }
    checks["summary_base_counts_recomputed"] = summary["base"] == computed_base
    checks["base_partitions_recomputed"] = (
        b_old == b_removed | b_stable
        and b_new == b_added | b_stable
        and not (b_removed & b_stable)
        and not (b_added & b_stable)
    )
    checks["generator_base_equals_old_twist_keys"] = set(generator_base) == old_keys
    checks["old_missing_keys_exactly_later_base_additions"] = missing_old == b_old - set(
        generator_base
    )
    checks["stable_domain_twist_keys_complete"] = b_stable <= old_keys and b_stable <= new_keys
    checks["no_orphan_twist_keys"] = old_keys <= b_old and new_keys <= b_new

    expected_upstream = {
        (label, twist) for label in b_removed for twist in old_twists.get(label, set())
    }
    expected_removed = {
        (label, twist)
        for label in b_stable
        for twist in old_twists[label] - new_twists[label]
    }
    expected_added = {
        (label, twist)
        for label in b_stable
        for twist in new_twists[label] - old_twists[label]
    }
    expected_newbase = {
        (label, twist) for label in b_added for twist in new_twists.get(label, set())
    }
    old_total = sum(map(len, old_twists.values()))
    new_total = sum(map(len, new_twists.values()))
    lhs = old_total - new_total
    rhs = (
        len(expected_upstream)
        + len(expected_removed)
        - len(expected_added)
        - len(expected_newbase)
    )
    computed_twists = {
        "old_total_pairs": old_total,
        "new_total_pairs": new_total,
        "upstream_removed": len(expected_upstream),
        "stable_removed": len(expected_removed),
        "stable_added": len(expected_added),
        "newbase_added": len(expected_newbase),
        "lhs": lhs,
        "rhs": rhs,
        "old_twist_key_count": len(old_keys),
        "new_twist_key_count": len(new_keys),
        "old_base_curves_without_materialized_twist_entry": len(missing_old),
        "stable_filter_mismatch_count": sum(
            new_twists[label]
            != {twist for twist in old_twists[label] if abs(twist) % 3 != 0}
            for label in b_stable
        ),
    }
    checks["summary_twist_counts_recomputed"] = summary["twists"] == computed_twists
    checks["global_accounting_identity_recomputed"] = lhs == rhs
    checks["stable_current_equals_old_filtered_by_3"] = not computed_twists[
        "stable_filter_mismatch_count"
    ]
    checks["stable_removed_all_divisible_by_3"] = all(
        abs(twist) % 3 == 0 for _, twist in expected_removed
    )

    base_removed_rows = read_csv(results / "base_removed.csv")
    base_added_rows = read_csv(results / "base_added.csv")
    base_stable_rows = read_csv(results / "base_stable.csv")
    checks["base_csv_membership_exact"] = (
        {row["curve_label"] for row in base_removed_rows} == b_removed
        and {row["curve_label"] for row in base_added_rows} == b_added
        and {row["curve_label"] for row in base_stable_rows} == b_stable
    )
    checks["upstream_pair_csv_exact"] = pair_set(
        read_csv(results / "twists_removed_by_upstream_base_deletion.csv")
    ) == expected_upstream
    checks["stable_removed_pair_csv_exact"] = pair_set(
        read_csv(results / "algorithm2_removed_twists.csv")
    ) == expected_removed
    checks["stable_added_pair_csv_exact"] = pair_set(
        read_csv(results / "algorithm2_added_twists.csv")
    ) == expected_added
    checks["newbase_pair_csv_exact"] = pair_set(
        read_csv(results / "new_base_twists.csv")
    ) == expected_newbase
    checks["missing_old_key_csv_exact"] = {
        row["curve_label"]
        for row in read_csv(results / "old_base_curves_missing_from_old_twist_map.csv")
    } == missing_old

    class_counter: Counter[str] = Counter()
    stable_census = read_csv(results / "algorithm2_stable_curve_census.csv")
    stable_rows_by_label = {row["curve_label"]: row for row in stable_census}
    stable_rows_valid = set(stable_rows_by_label) == b_stable
    for label in b_stable:
        row = stable_rows_by_label.get(label)
        if row is None:
            continue
        removed = old_twists[label] - new_twists[label]
        added = new_twists[label] - old_twists[label]
        category = (
            "MIXED"
            if removed and added
            else "SHRINK_ONLY"
            if removed
            else "EXPAND_ONLY"
            if added
            else "UNCHANGED"
        )
        class_counter[category] += 1
        stable_rows_valid &= (
            int(row["old_twist_count"]) == len(old_twists[label])
            and int(row["new_twist_count"]) == len(new_twists[label])
            and int(row["removed_twist_count"]) == len(removed)
            and int(row["added_twist_count"]) == len(added)
            and row["algorithm2_class"] == category
        )
    computed_classes = {
        "unchanged": class_counter["UNCHANGED"],
        "shrink_only": class_counter["SHRINK_ONLY"],
        "expand_only": class_counter["EXPAND_ONLY"],
        "mixed": class_counter["MIXED"],
    }
    checks["stable_curve_census_exact"] = stable_rows_valid
    checks["summary_stable_classes_recomputed"] = (
        summary["algorithm2_curve_classes"] == computed_classes
    )

    metadata = json.loads(
        (root / "inputs" / "metadata" / "algorithm1_removed_metadata.json").read_text(
            encoding="utf-8"
        )
    )
    metadata_by_label = {record["curve_label"]: record for record in metadata["records"]}
    failure_counts: Counter[str] = Counter()
    algorithm1_valid = set(metadata_by_label) == b_removed
    isogeny_gate_labels: set[str] = set()
    for label in b_removed:
        record = metadata_by_label.get(label)
        if record is None:
            continue
        degrees = {int(value) for value in record["isogeny_degrees"]}
        hit = bool(degrees & {3, 5, 7})
        a3_hit = abs(int(record["a3"])) == 3
        expected_class = (
            "BOTH"
            if hit and a3_hit
            else "ISOGENY_ONLY"
            if hit
            else "A3_ONLY"
            if a3_hit
            else "UNEXPLAINED"
        )
        algorithm1_valid &= record["failure_class"] == expected_class
        failure_counts[expected_class] += 1
        if hit:
            isogeny_gate_labels.add(label)
    computed_algorithm1 = {
        "isogeny_only": failure_counts["ISOGENY_ONLY"],
        "a3_only": failure_counts["A3_ONLY"],
        "both": failure_counts["BOTH"],
        "unexplained": failure_counts["UNEXPLAINED"],
    }
    checks["algorithm1_metadata_classes_recomputed"] = algorithm1_valid
    checks["old_missing_keys_equal_isogeny_gate_labels"] = missing_old == isogeny_gate_labels
    checks["algorithm1_core_summary_recomputed"] = all(
        summary["algorithm1"][key] == value for key, value in computed_algorithm1.items()
    )

    observed_blobs = {
        entry["role"]: entry["git_blob_sha1"]
        for entry in [
            *manifest["files"],
            *manifest["twist_generation_provenance_files"],
        ]
    }
    paths_by_role = {
        entry["role"]: root / entry["path"]
        for entry in [
            *manifest["files"],
            *manifest["twist_generation_provenance_files"],
        ]
    }
    checks["manifest_git_blobs_recomputed"] = all(
        git_blob_sha1(paths_by_role[role]) == expected
        and observed_blobs[role] == expected
        for role, expected in manifest["expected_git_blob_sha1"].items()
    )
    checks["manifest_sha256_recomputed"] = all(
        sha256(root / entry["path"]) == entry["sha256"]
        for entry in [
            *manifest["files"],
            *manifest["twist_generation_provenance_files"],
        ]
    )
    checks["result_hashes_recomputed"] = all(
        (results / entry["path"]).stat().st_size == entry["bytes"]
        and sha256(results / entry["path"]) == entry["sha256"]
        for entry in recorded_hashes["files"]
    )
    checks["summary_internal_checks_all_true"] = all(summary["checks"].values())
    checks["summary_status_complete"] = summary["status"] == "v0.5 EXACT ARTIFACT CENSUS COMPLETE"

    details.update(
        {
            "base": computed_base,
            "algorithm1_core": computed_algorithm1,
            "twists": computed_twists,
            "algorithm2_curve_classes": computed_classes,
            "check_count": len(checks),
            "passed_check_count": sum(checks.values()),
        }
    )
    passed = all(checks.values())
    payload = {
        "schema_version": "1.0",
        "status": "PASS" if passed else "FAIL",
        "method": "independent raw-input reparse and output/hash cross-check",
        "checks": checks,
        "details": details,
    }
    write_json(report_path, payload)
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
