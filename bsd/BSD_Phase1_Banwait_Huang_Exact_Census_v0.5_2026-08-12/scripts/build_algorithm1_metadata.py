#!/usr/bin/env python3
"""Build exact Algorithm 1 delta metadata for removed base curves.

The old/current base lists determine the removed Cremona labels.  For every
removed label this script extracts the minimal Weierstrass coefficients and
isogeny matrix row from John Cremona's ``ecdata`` repository, computes the
local coefficient a_3 directly over F_3, and verifies the Cremona-to-LMFDB
label mapping.  No Sage or running LMFDB database is required.

The output is a deterministic JSON evidence packet consumed by
``exact_census.py``.  It records the exact ecdata commit and SHA256 of every
source shard used, so use of a database distinct from the 2026 LMFDB snapshot
is explicit and auditable.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CREMONA_RE = re.compile(r"^(?P<N>[1-9][0-9]*)(?P<class>[a-z]+)(?P<num>[1-9][0-9]*)$")
STRICT_PRIMES = (3, 5, 7)
KNOWN_SOURCES = {"CLZ20", "Zha16_no_2_tors"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_dump(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


@dataclass(frozen=True)
class BaseRow:
    index: int
    cremona_label: str
    source: str
    lmfdb_label: str


def load_base_rows(path: Path) -> dict[str, BaseRow]:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        header_index = next(
            i
            for i, line in enumerate(lines)
            if [cell.strip() for cell in next(csv.reader([line]))]
            == ["cremona_label", "source", "lmfdb_label"]
        )
    except StopIteration as exc:
        raise ValueError(f"base header not found in {path}") from exc

    rows: dict[str, BaseRow] = {}
    for raw_index, cells in enumerate(csv.reader(lines[header_index + 1 :])):
        if not cells or not any(cell.strip() for cell in cells):
            continue
        values = [cell.strip() for cell in cells]
        if len(values) != 3 or values[1] not in KNOWN_SOURCES:
            raise ValueError(f"unparsed data row in {path}: {cells!r}")
        label, source, lmfdb_label = values
        if label in rows:
            raise ValueError(f"duplicate Cremona label in {path}: {label}")
        rows[label] = BaseRow(raw_index, label, source, lmfdb_label)
    return rows


def parse_cremona(label: str) -> tuple[int, str, int]:
    match = CREMONA_RE.fullmatch(label)
    if not match:
        raise ValueError(f"invalid Cremona label: {label}")
    return int(match["N"]), match["class"], int(match["num"])


def band_name(conductor: int) -> str:
    start = (conductor // 10_000) * 10_000
    return f"{start:05d}-{start + 9_999:05d}"


def discriminant(ainvs: Iterable[int]) -> int:
    a1, a2, a3, a4, a6 = map(int, ainvs)
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6


def local_ap_from_model(ainvs: Iterable[int], p: int = 3) -> dict[str, int | bool | str]:
    """Compute a_p from the reduced projective cubic, including bad reduction.

    For good reduction, a_p = p + 1 - #E(F_p).  For bad reduction, the
    local coefficient is p - #E_ns(F_p), where E_ns is the nonsingular locus
    of the reduced cubic.
    """

    a1, a2, a3, a4, a6 = map(int, ainvs)
    points: list[tuple[int, int, int]] = []
    for x in range(p):
        for y in range(p):
            lhs = (y * y + a1 * x * y + a3 * y) % p
            rhs = (x**3 + a2 * x * x + a4 * x + a6) % p
            if lhs == rhs:
                points.append((x, y, 1))
    points.append((0, 1, 0))

    nonsingular = 0
    singular_points: list[list[int]] = []
    for x, y, z in points:
        fx = (a1 * y * z - 3 * x * x - 2 * a2 * x * z - a4 * z * z) % p
        fy = (2 * y * z + a1 * x * z + a3 * z * z) % p
        fz = (
            y * y
            + a1 * x * y
            + 2 * a3 * y * z
            - a2 * x * x
            - 2 * a4 * x * z
            - 3 * a6 * z * z
        ) % p
        if fx == 0 == fy == fz:
            singular_points.append([x, y, z])
        else:
            nonsingular += 1

    delta = discriminant(ainvs)
    good = delta % p != 0
    if good:
        if nonsingular != len(points):
            raise AssertionError("good reduction unexpectedly has a singular point")
        ap = p + 1 - len(points)
        formula = "p+1-projective_point_count"
    else:
        ap = p - nonsingular
        formula = "p-nonsingular_projective_point_count"
    return {
        "a3": ap,
        "discriminant": delta,
        "good_reduction_at_3": good,
        "projective_point_count": len(points),
        "nonsingular_projective_point_count": nonsingular,
        "singular_projective_points": singular_points,
        "formula": formula,
    }


def get_git_commit(repo: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()


def load_shards(
    ecdata: Path, removed: set[str]
) -> tuple[
    dict[str, tuple[list[int], str, Path]],
    dict[tuple[int, str], tuple[list[list[int]], list[list[int]], str, Path]],
    dict[str, tuple[str, str, Path]],
    dict[tuple[int, str], tuple[str, str, Path]],
    set[Path],
]:
    wanted_bands = sorted({band_name(parse_cremona(label)[0]) for label in removed})
    curves: dict[str, tuple[list[int], str, Path]] = {}
    isog: dict[tuple[int, str], tuple[list[list[int]], list[list[int]], str, Path]] = {}
    labels: dict[str, tuple[str, str, Path]] = {}
    aplist: dict[tuple[int, str], tuple[str, str, Path]] = {}
    touched: set[Path] = set()

    wanted_classes = {(parse_cremona(label)[0], parse_cremona(label)[1]) for label in removed}

    for band in wanted_bands:
        allcurves_path = ecdata / "allcurves" / f"allcurves.{band}"
        allisog_path = ecdata / "allisog" / f"allisog.{band}"
        alllabels_path = ecdata / "alllabels" / f"alllabels.{band}"
        aplist_path = ecdata / "aplist" / f"aplist.{band}"
        for path in (allcurves_path, allisog_path, alllabels_path, aplist_path):
            if not path.is_file():
                raise FileNotFoundError(path)
            touched.add(path)

        for line in allcurves_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 6:
                raise ValueError(f"bad allcurves line: {line}")
            label = f"{parts[0]}{parts[1]}{parts[2]}"
            if label in removed:
                curves[label] = (list(map(int, ast.literal_eval(parts[3]))), line, allcurves_path)

        for line in allisog_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 6:
                raise ValueError(f"bad allisog line: {line}")
            key = (int(parts[0]), parts[1])
            if key in wanted_classes:
                class_ainvs = [list(map(int, row)) for row in ast.literal_eval(parts[4])]
                matrix = [list(map(int, row)) for row in ast.literal_eval(parts[5])]
                size = len(class_ainvs)
                if len(matrix) != size or any(len(row) != size for row in matrix):
                    raise ValueError(f"nonsquare isogeny matrix for {key}")
                if any(matrix[i][i] != 1 for i in range(size)):
                    raise ValueError(f"bad isogeny matrix diagonal for {key}")
                if any(matrix[i][j] != matrix[j][i] for i in range(size) for j in range(size)):
                    raise ValueError(f"nonsymmetric isogeny matrix for {key}")
                isog[key] = (class_ainvs, matrix, line, allisog_path)

        for line in alllabels_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 6:
                raise ValueError(f"bad alllabels line: {line}")
            cremona = f"{parts[0]}{parts[1]}{parts[2]}"
            if cremona in removed:
                lmfdb = f"{parts[3]}.{parts[4]}{parts[5]}"
                labels[cremona] = (lmfdb, line, alllabels_path)

        for line in aplist_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) < 4:
                raise ValueError(f"bad aplist line: {line}")
            key = (int(parts[0]), parts[1])
            if key in wanted_classes:
                aplist[key] = (parts[3], line, aplist_path)  # second AP entry is a_3 / W_3 token

    return curves, isog, labels, aplist, touched


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--ecdata", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="defaults to ROOT/inputs/metadata/algorithm1_removed_metadata.json",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    ecdata = args.ecdata.resolve()
    output = args.output or root / "inputs" / "metadata" / "algorithm1_removed_metadata.json"

    old_rows = load_base_rows(root / "inputs" / "old" / "ec_labels_500k.txt")
    new_rows = load_base_rows(root / "inputs" / "new" / "ec_labels_500k.txt")
    removed = set(old_rows) - set(new_rows)
    added = set(new_rows) - set(old_rows)

    curves, isog, labels, aplist, touched = load_shards(ecdata, removed)
    missing_curves = sorted(removed - set(curves))
    missing_labels = sorted(removed - set(labels))
    missing_classes = sorted(
        {parse_cremona(label)[:2] for label in removed} - set(isog),
        key=lambda pair: (pair[0], pair[1]),
    )
    missing_aplist = sorted(
        {parse_cremona(label)[:2] for label in removed} - set(aplist),
        key=lambda pair: (pair[0], pair[1]),
    )
    if missing_curves or missing_labels or missing_classes or missing_aplist:
        raise RuntimeError(
            f"ecdata coverage failure: curves={missing_curves[:10]}, labels={missing_labels[:10]}, "
            f"classes={missing_classes[:10]}, aplist={missing_aplist[:10]}"
        )

    records = []
    numeric_aplist_mismatches = []
    label_mismatches = []
    class_ainvs_mismatches = []
    for label in sorted(removed, key=lambda x: parse_cremona(x)):
        conductor, class_code, curve_number = parse_cremona(label)
        ainvs, allcurves_line, allcurves_path = curves[label]
        class_ainvs, matrix, allisog_line, allisog_path = isog[(conductor, class_code)]
        mapped_lmfdb, alllabels_line, alllabels_path = labels[label]
        aplist_a3_token, aplist_line, aplist_path = aplist[(conductor, class_code)]

        if not 1 <= curve_number <= len(matrix):
            raise ValueError(f"curve number outside isogeny matrix: {label}")
        if class_ainvs[curve_number - 1] != ainvs:
            class_ainvs_mismatches.append(label)
        if mapped_lmfdb != old_rows[label].lmfdb_label:
            label_mismatches.append(
                {"curve_label": label, "input": old_rows[label].lmfdb_label, "ecdata": mapped_lmfdb}
            )

        degrees = sorted(set(matrix[curve_number - 1]))
        local = local_ap_from_model(ainvs, 3)
        if aplist_a3_token not in {"+", "-"}:
            try:
                ecdata_numeric_a3 = int(aplist_a3_token)
            except ValueError:
                ecdata_numeric_a3 = None
            if ecdata_numeric_a3 is not None and ecdata_numeric_a3 != local["a3"]:
                numeric_aplist_mismatches.append(
                    {
                        "curve_label": label,
                        "computed_a3": local["a3"],
                        "aplist_token": aplist_a3_token,
                    }
                )

        hits = [p for p in STRICT_PRIMES if p in degrees]
        failure_class = (
            "BOTH"
            if hits and abs(int(local["a3"])) == 3
            else "ISOGENY_ONLY"
            if hits
            else "A3_ONLY"
            if abs(int(local["a3"])) == 3
            else "UNEXPLAINED"
        )
        records.append(
            {
                "curve_label": label,
                "lmfdb_label": old_rows[label].lmfdb_label,
                "source": old_rows[label].source,
                "conductor": conductor,
                "class_code": class_code,
                "curve_number": curve_number,
                "ainvs": ainvs,
                "isogeny_degrees": degrees,
                "isogeny_set_357": hits,
                "has_isogeny_3": 3 in hits,
                "has_isogeny_5": 5 in hits,
                "has_isogeny_7": 7 in hits,
                "fails_isogeny_gate": bool(hits),
                "a3": local["a3"],
                "abs_a3_eq_3": abs(int(local["a3"])) == 3,
                "failure_class": failure_class,
                "a3_computation": local,
                "ecdata_aplist_a3_token": aplist_a3_token,
                "evidence": {
                    "allcurves_path": allcurves_path.relative_to(ecdata).as_posix(),
                    "allcurves_line": allcurves_line,
                    "allisog_path": allisog_path.relative_to(ecdata).as_posix(),
                    "allisog_line": allisog_line,
                    "alllabels_path": alllabels_path.relative_to(ecdata).as_posix(),
                    "alllabels_line": alllabels_line,
                    "aplist_path": aplist_path.relative_to(ecdata).as_posix(),
                    "aplist_line": aplist_line,
                },
            }
        )

    source_files = []
    for path in sorted(touched):
        source_files.append(
            {
                "path": path.relative_to(ecdata).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    file_format = ecdata / "docs" / "file-format.txt"
    source_files.append(
        {
            "path": file_format.relative_to(ecdata).as_posix(),
            "bytes": file_format.stat().st_size,
            "sha256": sha256(file_format),
        }
    )

    histogram: dict[str, int] = {}
    for record in records:
        histogram[record["failure_class"]] = histogram.get(record["failure_class"], 0) + 1

    checks = {
        "base_added_count_is_zero": len(added) == 0,
        "metadata_record_count_matches_removed": len(records) == len(removed),
        "all_removed_labels_unique": len({record["curve_label"] for record in records}) == len(removed),
        "cremona_to_lmfdb_mapping_exact": not label_mismatches,
        "allcurves_matches_isogeny_class_models": not class_ainvs_mismatches,
        "computed_good_reduction_a3_matches_aplist": not numeric_aplist_mismatches,
        "all_removed_explained": histogram.get("UNEXPLAINED", 0) == 0,
    }
    payload = {
        "schema_version": "1.0",
        "provenance": {
            "ecdata_repository": "https://github.com/JohnCremona/ecdata.git",
            "ecdata_commit": get_git_commit(ecdata),
            "old_algorithm_commit": "1a0489c3c3099dd0c248624e6621df73ae8f0d43",
            "current_algorithm_commit": "31fae20c8df3f1f0383f41112b914d4995d5809d",
            "method": "ecdata allcurves/allisog/alllabels extraction plus direct projective F_3 point count",
            "source_files": source_files,
        },
        "base_counts": {
            "old": len(old_rows),
            "new": len(new_rows),
            "removed": len(removed),
            "added": len(added),
        },
        "failure_class_histogram": dict(sorted(histogram.items())),
        "checks": checks,
        "diagnostics": {
            "label_mismatches": label_mismatches,
            "class_ainvs_mismatches": class_ainvs_mismatches,
            "numeric_aplist_mismatches": numeric_aplist_mismatches,
        },
        "records": records,
    }
    json_dump(output, payload)
    print(json.dumps({"output": str(output), "counts": payload["base_counts"], "histogram": histogram, "checks": checks}, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
