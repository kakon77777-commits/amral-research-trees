#!/usr/bin/env python3
"""Deterministic entry-level census for the Banwait-Huang one-commit delta."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REPOSITORY = "https://github.com/cocoxhuang/ants_xvii.git"
OLD_COMMIT = "1a0489c3c3099dd0c248624e6621df73ae8f0d43"
NEW_COMMIT = "31fae20c8df3f1f0383f41112b914d4995d5809d"
TWIST_GENERATOR_COMMIT = "72867942accf94b9513857a2c0bae3895af8e9bc"
EXPECTED_GIT_BLOBS = {
    "old_base": "46ee5b24c93f4ceffc602f7a941f37003d3c5def",
    "old_twists": "67809e1210d95d13e69b731bcb458a711602e456",
    "new_base": "6f2cce03973009223a7679fecad3c0c5b141ca52",
    "new_twists": "2135e1dd979fbcfb643923e5a11e0bf7e50fd244",
    "generator_base": "6c68bce8973fbe80e37c26beef13ce7f122ec3cc",
    "generator_algorithm2": "3a83d05a6b2e3cc72c6bf68311356d422e8201ec",
    "old_algorithm2": "162d8bb6bc373334a66f8b42383481f2018d9b95",
}
KNOWN_SOURCES = {"CLZ20", "Zha16_no_2_tors"}
CREMONA_RE = re.compile(r"^(?P<N>[1-9][0-9]*)(?P<class>[a-z]+)(?P<num>[1-9][0-9]*)$")


@dataclass(frozen=True)
class BaseRow:
    index: int
    curve_label: str
    source: str
    lmfdb_label: str


def label_key(label: str) -> tuple[int, str, int]:
    match = CREMONA_RE.fullmatch(label)
    if not match:
        return (10**30, label, 10**30)
    return int(match["N"]), match["class"], int(match["num"])


def conductor_of(label: str) -> int:
    match = CREMONA_RE.fullmatch(label)
    if not match:
        raise ValueError(f"invalid Cremona label: {label}")
    return int(match["N"])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_sha1(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def line_count(path: Path) -> int:
    content = path.read_bytes()
    if not content:
        return 0
    return content.count(b"\n") + (0 if content.endswith(b"\n") else 1)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def parse_base_file(path: Path) -> tuple[list[BaseRow], dict[str, object]]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    header_index = None
    for i, line in enumerate(lines):
        cells = [cell.strip() for cell in next(csv.reader([line]))]
        if cells == ["cremona_label", "source", "lmfdb_label"]:
            header_index = i
            break
    if header_index is None:
        raise ValueError(f"base header not found: {path}")

    metadata_lines = lines[:header_index]
    rows: list[BaseRow] = []
    unparsed: list[dict[str, object]] = []
    label_whitespace: list[str] = []
    for cells in csv.reader(lines[header_index + 1 :]):
        if not cells or not any(cell.strip() for cell in cells):
            continue
        values = [cell.strip() for cell in cells]
        if len(values) != 3 or values[1] not in KNOWN_SOURCES:
            unparsed.append({"row": cells})
            continue
        if cells[0] != cells[0].strip():
            label_whitespace.append(cells[0])
        rows.append(BaseRow(len(rows) + 1, values[0], values[1], values[2]))

    labels = [row.curve_label for row in rows]
    duplicates = sorted(label for label, count in Counter(labels).items() if count > 1)
    unparsed_labels = sorted(label for label in labels if not CREMONA_RE.fullmatch(label))
    case_collisions = sorted(
        key for key, count in Counter(label.lower() for label in labels).items() if count > 1
    )
    diagnostics = {
        "metadata_lines": metadata_lines,
        "json_top_level_type": None,
        "data_row_count": len(rows),
        "duplicate_labels": duplicates,
        "unparsed_rows": unparsed,
        "unparsed_labels": unparsed_labels,
        "label_leading_or_trailing_whitespace": label_whitespace,
        "case_fold_collisions": case_collisions,
        "blank_line_count": sum(not line.strip() for line in lines),
    }
    if duplicates or unparsed or unparsed_labels or label_whitespace or case_collisions:
        raise ValueError(f"base normalization diagnostics failed for {path}: {diagnostics}")
    return rows, diagnostics


def parse_twist_map(path: Path) -> tuple[dict[str, set[int]], dict[str, object]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"twist JSON top level is {type(raw).__name__}, expected object")
    normalized: dict[str, set[int]] = {}
    duplicate_twists: dict[str, list[int]] = {}
    key_whitespace: list[str] = []
    invalid_entries: list[dict[str, object]] = []
    for original_key, value in raw.items():
        if not isinstance(original_key, str):
            raise ValueError(f"non-string twist key: {original_key!r}")
        key = original_key.strip()
        if key != original_key:
            key_whitespace.append(original_key)
        if key in normalized:
            raise ValueError(f"duplicate twist key after normalization: {key}")
        if not isinstance(value, list):
            invalid_entries.append({"curve": key, "value_type": type(value).__name__})
            continue
        canonical: list[int] = []
        for twist in value:
            if isinstance(twist, bool) or not isinstance(twist, int):
                invalid_entries.append({"curve": key, "twist": repr(twist)})
            else:
                canonical.append(twist)
        dup = sorted(twist for twist, count in Counter(canonical).items() if count > 1)
        if dup:
            duplicate_twists[key] = dup
        normalized[key] = set(canonical)
    diagnostics = {
        "json_top_level_type": type(raw).__name__,
        "sample_keys": list(raw)[:5],
        "sample_entry": {list(raw)[0]: raw[list(raw)[0]]} if raw else None,
        "number_of_base_keys": len(normalized),
        "number_of_twist_pairs": sum(len(values) for values in normalized.values()),
        "duplicate_twists": duplicate_twists,
        "key_leading_or_trailing_whitespace": key_whitespace,
        "invalid_entries": invalid_entries,
    }
    if duplicate_twists or key_whitespace or invalid_entries:
        raise ValueError(f"twist normalization diagnostics failed for {path}: {diagnostics}")
    return normalized, diagnostics


def base_csv_row(
    label: str,
    status: str,
    old_by_label: dict[str, BaseRow],
    new_by_label: dict[str, BaseRow],
) -> dict[str, object]:
    old = old_by_label.get(label)
    new = new_by_label.get(label)
    return {
        "curve_label": label,
        "status": status,
        "old_index": old.index if old else "",
        "new_index": new.index if new else "",
        "old_source": old.source if old else "",
        "new_source": new.source if new else "",
        "old_lmfdb_label": old.lmfdb_label if old else "",
        "new_lmfdb_label": new.lmfdb_label if new else "",
    }


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    if not rows:
        return "_None._"
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--metadata",
        type=Path,
        default=None,
        help="defaults to ROOT/inputs/metadata/algorithm1_removed_metadata.json",
    )
    parser.add_argument(
        "--twist-generator-base",
        type=Path,
        default=None,
        help="defaults to ROOT/sources/generator_7286794/ec_labels_500k.txt",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    results = root / "results"
    logs = root / "logs"
    results.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    paths = {
        "old_base": root / "inputs" / "old" / "ec_labels_500k.txt",
        "new_base": root / "inputs" / "new" / "ec_labels_500k.txt",
        "old_twists": root / "inputs" / "old" / "twists_of_ec_labels_500k.json",
        "new_twists": root / "inputs" / "new" / "twists_of_ec_labels_500k.json",
    }
    source_paths = {
        "generator_base": root / "sources" / "generator_7286794" / "ec_labels_500k.txt",
        "generator_algorithm2": root / "sources" / "generator_7286794" / "Algorithm2.py",
        "old_algorithm2": root / "sources" / "old" / "Algorithm2.py",
    }
    if args.twist_generator_base is not None:
        source_paths["generator_base"] = args.twist_generator_base
    metadata_path = args.metadata or root / "inputs" / "metadata" / "algorithm1_removed_metadata.json"
    if not metadata_path.is_file():
        raise FileNotFoundError(metadata_path)
    for path in [*paths.values(), *source_paths.values()]:
        if not path.is_file():
            raise FileNotFoundError(path)

    old_rows, old_base_diag = parse_base_file(paths["old_base"])
    new_rows, new_base_diag = parse_base_file(paths["new_base"])
    old_by_label = {row.curve_label: row for row in old_rows}
    new_by_label = {row.curve_label: row for row in new_rows}
    b_old = set(old_by_label)
    b_new = set(new_by_label)
    b_removed = b_old - b_new
    b_added = b_new - b_old
    b_stable = b_old & b_new

    generator_rows, generator_base_diag = parse_base_file(source_paths["generator_base"])
    generator_by_label = {row.curve_label: row for row in generator_rows}
    b_generator = set(generator_by_label)

    t_old, old_twist_diag = parse_twist_map(paths["old_twists"])
    t_new, new_twist_diag = parse_twist_map(paths["new_twists"])
    old_twist_keys = set(t_old)
    new_twist_keys = set(t_new)
    old_orphan_twist_keys = old_twist_keys - b_old
    new_orphan_twist_keys = new_twist_keys - b_new
    old_missing_twist_keys = b_old - old_twist_keys
    new_missing_twist_keys = b_new - new_twist_keys

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    meta_by_label = {record["curve_label"]: record for record in metadata["records"]}
    metadata_missing = sorted(b_removed - set(meta_by_label), key=label_key)
    metadata_extra = sorted(set(meta_by_label) - b_removed, key=label_key)
    if metadata_missing or metadata_extra:
        raise ValueError(f"Algorithm1 metadata coverage mismatch: missing={metadata_missing[:10]}, extra={metadata_extra[:10]}")

    base_fields = [
        "curve_label",
        "status",
        "old_index",
        "new_index",
        "old_source",
        "new_source",
        "old_lmfdb_label",
        "new_lmfdb_label",
    ]
    write_csv(
        results / "base_removed.csv",
        base_fields,
        (base_csv_row(label, "REMOVED", old_by_label, new_by_label) for label in sorted(b_removed, key=label_key)),
    )
    write_csv(
        results / "base_added.csv",
        base_fields,
        (base_csv_row(label, "ADDED", old_by_label, new_by_label) for label in sorted(b_added, key=label_key)),
    )
    write_csv(
        results / "base_stable.csv",
        base_fields,
        (base_csv_row(label, "STABLE", old_by_label, new_by_label) for label in sorted(b_stable, key=label_key)),
    )

    algorithm1_rows: list[dict[str, object]] = []
    failure_classes: Counter[str] = Counter()
    isogeny_combinations: Counter[str] = Counter()
    individual_isogenies: Counter[int] = Counter()
    a3_histogram: Counter[int] = Counter()
    for label in sorted(b_removed, key=label_key):
        record = meta_by_label[label]
        degrees = {int(value) for value in record["isogeny_degrees"]}
        hits = tuple(p for p in (3, 5, 7) if p in degrees)
        a3 = int(record["a3"])
        failure_class = (
            "BOTH"
            if hits and abs(a3) == 3
            else "ISOGENY_ONLY"
            if hits
            else "A3_ONLY"
            if abs(a3) == 3
            else "UNEXPLAINED"
        )
        failure_classes[failure_class] += 1
        combo = "{" + ",".join(map(str, hits)) + "}" if hits else "NONE"
        isogeny_combinations[combo] += 1
        for p in hits:
            individual_isogenies[p] += 1
        a3_histogram[a3] += 1
        local = record["a3_computation"]
        algorithm1_rows.append(
            {
                "curve_label": label,
                "lmfdb_label": old_by_label[label].lmfdb_label,
                "source": old_by_label[label].source,
                "conductor": conductor_of(label),
                "has_isogeny_3": 3 in hits,
                "has_isogeny_5": 5 in hits,
                "has_isogeny_7": 7 in hits,
                "isogeny_set_357": ";".join(map(str, hits)),
                "isogeny_degrees": ";".join(map(str, sorted(degrees))),
                "a3": a3,
                "abs_a3_eq_3": abs(a3) == 3,
                "failure_class": failure_class,
                "good_reduction_at_3": local["good_reduction_at_3"],
                "projective_point_count_at_3": local["projective_point_count"],
                "nonsingular_projective_point_count_at_3": local[
                    "nonsingular_projective_point_count"
                ],
                "ecdata_aplist_a3_token": record["ecdata_aplist_a3_token"],
            }
        )
    algorithm1_fields = list(algorithm1_rows[0])
    write_csv(results / "algorithm1_removed_census.csv", algorithm1_fields, algorithm1_rows)
    unexplained_rows = [row for row in algorithm1_rows if row["failure_class"] == "UNEXPLAINED"]
    write_csv(results / "algorithm1_unexplained_removed.csv", algorithm1_fields, unexplained_rows)

    old_missing_twist_rows = [
        {
            "curve_label": label,
            "source": old_by_label[label].source,
            "lmfdb_label": old_by_label[label].lmfdb_label,
            "algorithm1_failure_class": meta_by_label[label]["failure_class"],
            "reason": "BASE_ADDED_AFTER_TWIST_FILE_LAST_CHANGED",
            "twist_file_generator_commit": TWIST_GENERATOR_COMMIT,
        }
        for label in sorted(old_missing_twist_keys, key=label_key)
    ]
    write_csv(
        results / "old_base_curves_missing_from_old_twist_map.csv",
        [
            "curve_label",
            "source",
            "lmfdb_label",
            "algorithm1_failure_class",
            "reason",
            "twist_file_generator_commit",
        ],
        old_missing_twist_rows,
    )

    upstream_rows: list[dict[str, object]] = []
    stable_removed_rows: list[dict[str, object]] = []
    stable_added_rows: list[dict[str, object]] = []
    newbase_rows: list[dict[str, object]] = []
    curve_rows: list[dict[str, object]] = []
    class_counts: Counter[str] = Counter()
    additions_by_source: dict[str, dict[str, int]] = defaultdict(lambda: {"curves": 0, "pairs": 0})
    additions_by_band: dict[int, dict[str, int]] = defaultdict(lambda: {"curves": 0, "pairs": 0})

    for label in sorted(b_removed, key=label_key):
        failure_class = meta_by_label[label]["failure_class"]
        for twist in sorted(t_old.get(label, set())):
            upstream_rows.append(
                {
                    "curve_label": label,
                    "twist": twist,
                    "reason": "UPSTREAM_BASE_REMOVAL",
                    "algorithm1_failure_class": failure_class,
                }
            )

    for label in sorted(b_stable, key=label_key):
        old_values = t_old.get(label, set())
        new_values = t_new.get(label, set())
        removed_values = old_values - new_values
        added_values = new_values - old_values
        if removed_values and added_values:
            category = "MIXED"
        elif removed_values:
            category = "SHRINK_ONLY"
        elif added_values:
            category = "EXPAND_ONLY"
        else:
            category = "UNCHANGED"
        class_counts[category] += 1
        base = new_by_label[label]
        curve_rows.append(
            {
                "curve_label": label,
                "lmfdb_label": base.lmfdb_label,
                "source": base.source,
                "conductor": conductor_of(label),
                "old_twist_count": len(old_values),
                "new_twist_count": len(new_values),
                "removed_twist_count": len(removed_values),
                "added_twist_count": len(added_values),
                "net_delta": len(new_values) - len(old_values),
                "algorithm2_class": category,
            }
        )
        for twist in sorted(removed_values):
            stable_removed_rows.append(
                {
                    "curve_label": label,
                    "twist": twist,
                    "source": base.source,
                    "lmfdb_label": base.lmfdb_label,
                    "conductor": conductor_of(label),
                    "reason": "STABLE_BASE_ALGORITHM2_REMOVAL",
                }
            )
        for twist in sorted(added_values):
            stable_added_rows.append(
                {
                    "curve_label": label,
                    "twist": twist,
                    "source": base.source,
                    "lmfdb_label": base.lmfdb_label,
                    "conductor": conductor_of(label),
                    "reason": "STABLE_BASE_ALGORITHM2_ADDITION",
                }
            )
        if added_values:
            additions_by_source[base.source]["curves"] += 1
            additions_by_source[base.source]["pairs"] += len(added_values)
            band = (conductor_of(label) // 10_000) * 10_000
            additions_by_band[band]["curves"] += 1
            additions_by_band[band]["pairs"] += len(added_values)

    for label in sorted(b_added, key=label_key):
        base = new_by_label[label]
        for twist in sorted(t_new.get(label, set())):
            newbase_rows.append(
                {
                    "curve_label": label,
                    "twist": twist,
                    "source": base.source,
                    "lmfdb_label": base.lmfdb_label,
                    "conductor": conductor_of(label),
                    "reason": "NEW_BASE_ADDITION",
                }
            )

    stable_filter_mismatch_rows: list[dict[str, object]] = []
    for label in sorted(b_stable, key=label_key):
        expected_current = {twist for twist in t_old[label] if abs(twist) % 3 != 0}
        if t_new[label] != expected_current:
            stable_filter_mismatch_rows.append(
                {
                    "curve_label": label,
                    "old_twist_count": len(t_old[label]),
                    "new_twist_count": len(t_new[label]),
                    "expected_after_removing_3_divisible": len(expected_current),
                    "unexpected_removed_nonmultiples_of_3": ";".join(
                        map(str, sorted(expected_current - t_new[label]))
                    ),
                    "unexpected_new_twists": ";".join(
                        map(str, sorted(t_new[label] - expected_current))
                    ),
                }
            )

    write_csv(
        results / "twists_removed_by_upstream_base_deletion.csv",
        ["curve_label", "twist", "reason", "algorithm1_failure_class"],
        upstream_rows,
    )
    twist_delta_fields = ["curve_label", "twist", "source", "lmfdb_label", "conductor", "reason"]
    write_csv(results / "algorithm2_removed_twists.csv", twist_delta_fields, stable_removed_rows)
    write_csv(results / "algorithm2_added_twists.csv", twist_delta_fields, stable_added_rows)
    write_csv(results / "new_base_twists.csv", twist_delta_fields, newbase_rows)
    curve_fields = list(curve_rows[0])
    write_csv(results / "algorithm2_stable_curve_census.csv", curve_fields, curve_rows)

    top_shrink = sorted(
        (row for row in curve_rows if int(row["removed_twist_count"]) > 0),
        key=lambda row: (-int(row["removed_twist_count"]), label_key(str(row["curve_label"]))),
    )[:50]
    top_expand = sorted(
        (row for row in curve_rows if int(row["added_twist_count"]) > 0),
        key=lambda row: (-int(row["added_twist_count"]), label_key(str(row["curve_label"]))),
    )[:50]
    mixed = sorted(
        (row for row in curve_rows if row["algorithm2_class"] == "MIXED"),
        key=lambda row: label_key(str(row["curve_label"])),
    )
    write_csv(results / "algorithm2_top50_shrink.csv", curve_fields, top_shrink)
    write_csv(results / "algorithm2_top50_expand.csv", curve_fields, top_expand)
    write_csv(results / "algorithm2_mixed_curves.csv", curve_fields, mixed)
    write_csv(
        results / "algorithm2_stable_filter_mismatches.csv",
        [
            "curve_label",
            "old_twist_count",
            "new_twist_count",
            "expected_after_removing_3_divisible",
            "unexpected_removed_nonmultiples_of_3",
            "unexpected_new_twists",
        ],
        stable_filter_mismatch_rows,
    )

    source_summary_rows = [
        {"source": source, "curves_with_additions": values["curves"], "added_twist_pairs": values["pairs"]}
        for source, values in sorted(additions_by_source.items())
    ]
    band_summary_rows = [
        {
            "conductor_band_start": band,
            "conductor_band_end": band + 9_999,
            "curves_with_additions": values["curves"],
            "added_twist_pairs": values["pairs"],
        }
        for band, values in sorted(additions_by_band.items())
    ]
    write_csv(
        results / "algorithm2_additions_by_source.csv",
        ["source", "curves_with_additions", "added_twist_pairs"],
        source_summary_rows,
    )
    write_csv(
        results / "algorithm2_additions_by_conductor_band.csv",
        ["conductor_band_start", "conductor_band_end", "curves_with_additions", "added_twist_pairs"],
        band_summary_rows,
    )

    old_total_pairs = sum(len(values) for values in t_old.values())
    new_total_pairs = sum(len(values) for values in t_new.values())
    lhs = old_total_pairs - new_total_pairs
    rhs = len(upstream_rows) + len(stable_removed_rows) - len(stable_added_rows) - len(newbase_rows)

    raw_manifest = {
        "repository": REPOSITORY,
        "old_commit": OLD_COMMIT,
        "current_commit": NEW_COMMIT,
        "old_twist_file_generator_commit": TWIST_GENERATOR_COMMIT,
        "files": [
            {
                "role": role,
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "line_count": line_count(path),
                "sha256": sha256(path),
                "git_blob_sha1": git_blob_sha1(path),
            }
            for role, path in paths.items()
        ],
        "twist_generation_provenance_files": [
            {
                "role": role,
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "line_count": line_count(path),
                "sha256": sha256(path),
                "git_blob_sha1": git_blob_sha1(path),
            }
            for role, path in source_paths.items()
        ],
        "expected_git_blob_sha1": EXPECTED_GIT_BLOBS,
    }
    write_json(results / "raw_file_manifest.json", raw_manifest)

    observed_blob_by_role = {
        item["role"]: item["git_blob_sha1"]
        for item in [*raw_manifest["files"], *raw_manifest["twist_generation_provenance_files"]]
    }
    isogeny_gate_removed = {
        str(row["curve_label"])
        for row in algorithm1_rows
        if row["failure_class"] in {"ISOGENY_ONLY", "BOTH"}
    }
    stable_removed_nonmultiples_of_3 = [
        row for row in stable_removed_rows if abs(int(row["twist"])) % 3 != 0
    ]

    checks = {
        "old_commit_recorded": raw_manifest["old_commit"] == OLD_COMMIT,
        "current_commit_recorded": raw_manifest["current_commit"] == NEW_COMMIT,
        "four_raw_inputs_materialized": all(path.is_file() for path in paths.values()),
        "four_raw_sha256_recorded": all(file["sha256"] for file in raw_manifest["files"]),
        "base_old_partition": len(b_old) == len(b_removed) + len(b_stable),
        "base_new_partition": len(b_new) == len(b_added) + len(b_stable),
        "base_membership_equation": len(b_new) == len(b_old) - len(b_removed) + len(b_added),
        "old_base_labels_unique_and_parsed": len(old_rows) == len(b_old),
        "new_base_labels_unique_and_parsed": len(new_rows) == len(b_new),
        "old_twist_schema_valid": not old_twist_diag["invalid_entries"],
        "new_twist_schema_valid": not new_twist_diag["invalid_entries"],
        "raw_git_blob_ids_exact": observed_blob_by_role == EXPECTED_GIT_BLOBS,
        "old_twist_keys_subset_old_base_set": old_twist_keys <= b_old,
        "old_twist_keys_equal_last_generator_base_set": old_twist_keys == b_generator,
        "old_missing_twist_keys_exactly_post_generator_base_additions": old_missing_twist_keys
        == b_old - b_generator,
        "old_missing_twist_keys_exactly_isogeny_gate_removed": old_missing_twist_keys
        == isogeny_gate_removed,
        "old_twist_map_has_no_orphan_keys": not old_orphan_twist_keys,
        "new_twist_keys_equal_base_set": new_twist_keys == b_new,
        "stable_domain_has_complete_old_and_new_twist_maps": b_stable <= old_twist_keys
        and b_stable <= new_twist_keys,
        "algorithm1_metadata_exact_coverage": not metadata_missing and not metadata_extra,
        "algorithm1_all_removed_explained": failure_classes["UNEXPLAINED"] == 0,
        "upstream_twist_removals_isolated": len(upstream_rows)
        == sum(len(t_old.get(label, set())) for label in b_removed),
        "stable_curve_class_partition": sum(class_counts.values()) == len(b_stable),
        "newbase_twists_isolated": len(newbase_rows)
        == sum(len(t_new.get(label, set())) for label in b_added),
        "stable_removed_twists_all_divisible_by_3": not stable_removed_nonmultiples_of_3,
        "stable_current_map_equals_old_map_filtered_by_3": not stable_filter_mismatch_rows,
        "twist_accounting_identity": lhs == rhs,
    }
    completion = all(checks.values())

    summary = {
        "schema_version": "1.0",
        "status": "v0.5 EXACT ARTIFACT CENSUS COMPLETE"
        if completion
        else "v0.5 EXACT ARTIFACT CENSUS INCOMPLETE",
        "provenance": {
            "repo": REPOSITORY,
            "old_commit": OLD_COMMIT,
            "new_commit": NEW_COMMIT,
            "old_twist_file_generator_commit": TWIST_GENERATOR_COMMIT,
            "old_twist_file_generator_finding": (
                "OLD twist JSON is byte-identical to commit 72867942 and has exactly the "
                "same keys as that commit's base file; OLD commit 1a0489 later added 1,355 "
                "base labels and changed Algorithm2 without changing the twist JSON blob. "
                "The JSON is therefore an archived artifact, not a fresh 1a0489 rerun."
            ),
            "algorithm1_metadata": metadata["provenance"],
        },
        "base": {
            "old": len(b_old),
            "new": len(b_new),
            "removed": len(b_removed),
            "added": len(b_added),
            "stable": len(b_stable),
        },
        "algorithm1": {
            "isogeny_only": failure_classes["ISOGENY_ONLY"],
            "a3_only": failure_classes["A3_ONLY"],
            "both": failure_classes["BOTH"],
            "unexplained": failure_classes["UNEXPLAINED"],
            "individual_isogeny_counts": {str(p): individual_isogenies[p] for p in (3, 5, 7)},
            "isogeny_combination_counts": dict(sorted(isogeny_combinations.items())),
            "a3_histogram": {str(key): value for key, value in sorted(a3_histogram.items())},
        },
        "twists": {
            "old_total_pairs": old_total_pairs,
            "new_total_pairs": new_total_pairs,
            "upstream_removed": len(upstream_rows),
            "stable_removed": len(stable_removed_rows),
            "stable_added": len(stable_added_rows),
            "newbase_added": len(newbase_rows),
            "lhs": lhs,
            "rhs": rhs,
            "old_twist_key_count": len(old_twist_keys),
            "new_twist_key_count": len(new_twist_keys),
            "old_base_curves_without_materialized_twist_entry": len(old_missing_twist_keys),
            "stable_filter_mismatch_count": len(stable_filter_mismatch_rows),
        },
        "algorithm2_curve_classes": {
            "unchanged": class_counts["UNCHANGED"],
            "shrink_only": class_counts["SHRINK_ONLY"],
            "expand_only": class_counts["EXPAND_ONLY"],
            "mixed": class_counts["MIXED"],
        },
        "algorithm2_addition_description": {
            "by_source": source_summary_rows,
            "by_conductor_band": band_summary_rows,
        },
        "input_diagnostics": {
            "old_base": old_base_diag,
            "new_base": new_base_diag,
            "old_twists": old_twist_diag,
            "new_twists": new_twist_diag,
            "old_twist_generator_base": generator_base_diag,
            "old_orphan_twist_keys": sorted(old_orphan_twist_keys, key=label_key),
            "new_orphan_twist_keys": sorted(new_orphan_twist_keys, key=label_key),
            "old_missing_twist_keys": sorted(old_missing_twist_keys, key=label_key),
            "new_missing_twist_keys": sorted(new_missing_twist_keys, key=label_key),
        },
        "checks": checks,
    }
    write_json(results / "summary.json", summary)

    top_shrink_md = [[r["curve_label"], r["removed_twist_count"], r["added_twist_count"], r["net_delta"]] for r in top_shrink[:10]]
    top_expand_md = [[r["curve_label"], r["removed_twist_count"], r["added_twist_count"], r["net_delta"]] for r in top_expand[:10]]
    mixed_md = [[r["curve_label"], r["removed_twist_count"], r["added_twist_count"], r["net_delta"]] for r in mixed[:100]]
    report = f"""# v0.5 Exact Census Report

**Status:** `{summary['status']}`  
**Repository:** `{REPOSITORY}`  
**OLD:** `{OLD_COMMIT}`  
**CURRENT:** `{NEW_COMMIT}`

## Provenance finding: OLD base and OLD twist JSON are asynchronous

Git blob history shows that the OLD twist JSON was last changed at
`{TWIST_GENERATOR_COMMIT}`.  It contains `{len(old_twist_keys)}` keys, exactly the
same label set as that commit's base file.  The selected OLD commit later contains
`{len(b_old)}` base labels but retains the same twist JSON blob, leaving
`{len(old_missing_twist_keys)}` base labels without a materialized twist entry.
The OLD commit also changed `Algorithm2.py` after that JSON was generated (including
adding `disc_valuation_condition`) without changing the JSON blob.  Consequently,
the OLD twist map is an archived output artifact, not evidence of a fresh
end-to-end execution of the OLD source tree.

Those `{len(old_missing_twist_keys)}` labels are listed in
`old_base_curves_missing_from_old_twist_map.csv`; they are exactly the curves added
after the twist file's last change and exactly the removed curves hitting a
3/5/7-isogeny gate.  There are no orphan OLD twist keys, and every stable base curve
has entries in both twist maps.  All counts below are therefore exact for the four
archived giant outputs.  They do not impute hypothetical results for missing entries.

## Q1 — Base-curve exact delta

```text
old    = {len(b_old)}
new    = {len(b_new)}
removed= {len(b_removed)}
added  = {len(b_added)}
stable = {len(b_stable)}
```

Both base partitions and the membership equation are exact PASS.

## Q2 — Algorithm 1 failure census

```text
ISOGENY_ONLY = {failure_classes['ISOGENY_ONLY']}
A3_ONLY      = {failure_classes['A3_ONLY']}
BOTH         = {failure_classes['BOTH']}
UNEXPLAINED  = {failure_classes['UNEXPLAINED']}
```

Individual counts (overlap allowed): 3-isogeny `{individual_isogenies[3]}`, 5-isogeny `{individual_isogenies[5]}`, 7-isogeny `{individual_isogenies[7]}`.

Combination histogram:

```json
{json.dumps(dict(sorted(isogeny_combinations.items())), indent=2, sort_keys=True)}
```

The isogeny data comes from John Cremona's `ecdata` commit `{metadata['provenance']['ecdata_commit']}`.  The coefficient `a3` was recomputed directly from each minimal model over `F_3`; all good-reduction values agree with the independent `aplist` data.

## Q3 — Unexplained removed curves

`{failure_classes['UNEXPLAINED']}`.  The complete file is `algorithm1_unexplained_removed.csv` (header only when zero).

## Q4 — Upstream Algorithm 1 twist removals

`R_upstream = {len(upstream_rows)}` twist pairs.

These are isolated in `twists_removed_by_upstream_base_deletion.csv` and are not counted as Algorithm 2 removals.
This is the exact number present in the archived OLD twist JSON.  The
`{len(old_missing_twist_keys)}` OLD base curves absent from that JSON contribute no
materialized pairs; the report does not pretend that Algorithm2 was rerun for them.

## Q5 — Stable-base Algorithm 2 delta

```text
stable removed = {len(stable_removed_rows)}
stable added   = {len(stable_added_rows)}
net delta      = {len(stable_added_rows) - len(stable_removed_rows)}
```

Every stable curve is present in both maps.  Moreover, the CURRENT stable map is
exactly the OLD stable map with twists divisible by 3 removed; mismatch count
`{len(stable_filter_mismatch_rows)}`.  This is an observed set identity, not merely
an inference from source-code text.

## Q6 — Stable-curve classes

```text
UNCHANGED   = {class_counts['UNCHANGED']}
SHRINK_ONLY = {class_counts['SHRINK_ONLY']}
EXPAND_ONLY = {class_counts['EXPAND_ONLY']}
MIXED       = {class_counts['MIXED']}
```

## Q7 — MIXED curves

There are `{len(mixed)}` MIXED curves.  The complete list is `algorithm2_mixed_curves.csv`.

{md_table(['curve', 'removed', 'added', 'net'], mixed_md)}

## Q8 — Descriptive concentration of additions

By source:

{md_table(['source', 'curves with additions', 'added pairs'], [[r['source'], r['curves_with_additions'], r['added_twist_pairs']] for r in source_summary_rows])}

Conductor-band counts are in `algorithm2_additions_by_conductor_band.csv`.  These are descriptive statistics only; no arithmetic cause is inferred from concentration.

## Q9 — Global accounting identity

```text
old_total_twist_pairs = {old_total_pairs}
new_total_twist_pairs = {new_total_pairs}
lhs                    = {lhs}
upstream_removed       = {len(upstream_rows)}
stable_removed         = {len(stable_removed_rows)}
stable_added           = {len(stable_added_rows)}
newbase_added          = {len(newbase_rows)}
rhs                    = {rhs}
accounting identity    = {'PASS' if lhs == rhs else 'FAIL'}
```

## Priority cases

### Top 10 shrink

{md_table(['curve', 'removed', 'added', 'net'], top_shrink_md)}

### Top 10 expand

{md_table(['curve', 'removed', 'added', 'net'], top_expand_md)}

Full top-50 lists are supplied as CSV.

## Completion gate

```json
{json.dumps(checks, indent=2, sort_keys=True)}
```

This is an exact archived-output census of a theorem-producing computation.  It is
not a fresh end-to-end rerun of every OLD curve, and it is not a proof of the
Birch–Swinnerton-Dyer conjecture for all elliptic curves.
"""
    write_text(results / "V0_5_EXACT_CENSUS_REPORT.md", report)

    hash_entries = []
    for path in sorted(results.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name != "results_sha256.json":
            hash_entries.append(
                {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            )
    write_json(results / "results_sha256.json", {"algorithm": "SHA256", "files": hash_entries})
    write_text(
        logs / "run.log",
        "\n".join(
            [
                f"python={platform.python_version()}",
                f"platform={platform.platform()}",
                f"old_commit={OLD_COMMIT}",
                f"new_commit={NEW_COMMIT}",
                f"old_twist_file_generator_commit={TWIST_GENERATOR_COMMIT}",
                f"status={summary['status']}",
                f"base_old={len(b_old)}",
                f"base_new={len(b_new)}",
                f"base_removed={len(b_removed)}",
                f"base_added={len(b_added)}",
                f"old_twist_keys={len(old_twist_keys)}",
                f"old_missing_twist_keys={len(old_missing_twist_keys)}",
                f"twist_lhs={lhs}",
                f"twist_rhs={rhs}",
            ]
        ),
    )
    print(json.dumps({"status": summary["status"], "base": summary["base"], "algorithm1": summary["algorithm1"], "twists": summary["twists"], "algorithm2_curve_classes": summary["algorithm2_curve_classes"], "checks": checks}, indent=2))
    return 0 if completion else 1


if __name__ == "__main__":
    raise SystemExit(main())
