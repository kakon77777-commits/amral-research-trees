from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


PINNED_MANIFEST_SHA256: dict[str, str] = {
    "SHA256SUMS.txt":
        "3353BEE6FE6728835608C6FA1EFD511CC8757A097D9403FCF78C5339C2CAF130",
    "SHA256SUMS-v0.2.1.txt":
        "4F5925CD2A449549F9629017E538F5FA341FA8BAECB4A5BB3F8B93ED005EBD6A",
    "SHA256SUMS-v0.2.2-candidate.txt":
        "AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B",
    "SHA256SUMS-v0.2.3-candidate.txt":
        "7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817",
}

CANDIDATE_VERSION = "0.2.3"
VALIDATOR_MODULE = "pnp_glc_i0.semantic_validator_v023"
VALIDATOR_RELATIVE = "src/pnp_glc_i0/semantic_validator_v023.py"
SCHEMA_RELATIVE = "schemas/run-record.schema.v0.2.3-candidate.json"
FIXTURE_DIRECTORY = "fixtures-v0.2.3"
ARTIFACT_DIRECTORY = "artifacts-v0.2.3"
CLOSURE_CLASSIFICATION_DIRECTORY = "closure-classification"
SUPPORTED_RUN_SPEC_FILENAME = "run-standard.v0.2.3.json"
EXTERNAL_DISPOSITION_BLOCKERS: list[dict[str, Any]] = []

PINNED_V023: dict[str, str] = {
    "schemas/run-record.schema.v0.2.3-candidate.json":
        "DCE6F0C95B95D9377BA7AF9F9537BDC277CDF0E68CE74B9AD3BF83DB2B011895",
    "src/pnp_glc_i0/semantic_validator_v023.py":
        "B0DC4EC989F93EBD557C4C8BFA3004E33B2BBAE0EB0F8FA5622489B2D148097B",
    "artifacts-v0.2.3/candidate-projection-spec.v0.2.3.json":
        "35D21683177A849FD8AD331451A818BE1EE2E7605CF4B11F54FF5CCCFED69251",
    "artifacts-v0.2.3/artifact-closure-spec.v0.2.3.json":
        "4E978EF2A2DF0FED51E94E89E6305294A9B7965AD86AB6888EE857DA4854643B",
    "artifacts-v0.2.3/evidence-role-spec.v0.2.3.json":
        "FB5C3BE06BA68716492B96664BF8FD5C6154C1159025E5F1D278FAD1C0B3CBFB",
    "fixtures-v0.2.3/manifest.json":
        "189967B7F60968BE2ACED2A0B4EE5E8885FBBFD997916BA18F55B33F3A4AA5D1",
    "artifacts-v0.2.3/closure-classification/manifest.json":
        "46721DBE2E8A5E4CE1144DA2957C7688059637149DDDADFF766B517001C6DE06",
    "i0-run-report.v0.2.3-candidate.json":
        "7D32357291B59DE472A266BAAD63F7BBB469B60F58BCD727DF5D3A35899125EB",
}

SMOKE_PREFIX = [
    "legit",
    "fabricated-states-999",
    "fabricated-transition-digest",
    "2sat-sat",
    "2sat-unsat",
    "receipt-ref-substitution",
    "robust-ref-type-confusion",
    "malformed-unsupported-envelope",
    "shape-valid-unsupported-envelope",
    "bad-trace-signature",
]

POSITIVE_CONTROLS = (
    "legit",
    "neutral-legit",
    "robust-legit",
    "robust-neutral-legit",
    "2sat-sat",
    "2sat-unsat",
)

RISK_PRIOR: dict[str, float] = {
    "fabricated-states-999": 10.0,
    "fabricated-transition-digest": 10.0,
    "receipt-ref-substitution": 10.0,
    "robust-ref-type-confusion": 10.0,
    "cross-role-contract-invariant": 9.0,
    "malformed-unsupported-envelope": 9.0,
    "shape-valid-unsupported-envelope": 9.0,
    "bad-trace-signature": 7.0,
    "missing-envelope-spec-id": 7.0,
    "malformed-role-edge": 7.0,
    "tampered-record": 6.0,
    "tampered-trace": 6.0,
    "unresolved-event-ref": 6.0,
}

KNOWN_FROZEN_BLOCKER = {
    "id": "CLOSURE-EDGE-SCOPE-01",
    "disposition": "FAIL",
    "classification": "Definition-interface ambiguity",
    "summary": (
        "The frozen closure spec does not scope the pinned parent-role-child "
        "relation explicitly to supported spec_id values."
    ),
    "implementation_acceptance_bypass": False,
    "p_np_implication": False,
}

MANIFEST_LINE = re.compile(r"^([0-9A-F]{64})  (.+)$")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest().upper()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def compare_expected(
    observed: Any, expected: Any, path: str = "$"
) -> list[dict[str, Any]]:
    mismatches: list[dict[str, Any]] = []
    if isinstance(expected, Mapping):
        if not isinstance(observed, Mapping):
            return [{"path": path, "expected": expected, "observed": observed}]
        for key, value in expected.items():
            child = f"{path}.{key}"
            if key not in observed:
                mismatches.append({"path": child, "expected": value, "observed": None})
            else:
                mismatches.extend(compare_expected(observed[key], value, child))
        return mismatches
    if observed != expected:
        mismatches.append({"path": path, "expected": expected, "observed": observed})
    return mismatches


def percentile_nearest_rank(samples: Sequence[int], fraction: float) -> int:
    if not samples:
        raise ValueError("samples must not be empty")
    ordered = sorted(samples)
    rank = max(1, (len(ordered) * int(fraction * 100) + 99) // 100)
    return ordered[min(rank - 1, len(ordered) - 1)]


def parse_checksum_manifest(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = MANIFEST_LINE.fullmatch(line)
        if not match:
            raise ValueError(f"malformed checksum line {path.name}:{number}")
        entries.append((match.group(2), match.group(1)))
    if not entries:
        raise ValueError(f"empty checksum manifest: {path}")
    return entries


def _allowed_manifest_target(candidate_root: Path, relative: str) -> Path:
    target = (candidate_root / Path(relative)).resolve()
    root = candidate_root.resolve()
    compatibility_file = root.parent / "run-record.schema.json"
    if target == compatibility_file or root == target or root in target.parents:
        return target
    raise ValueError(f"manifest path escapes frozen bundle: {relative}")


def frozen_manifest_state(candidate_root: Path) -> dict[str, Any]:
    candidate_root = candidate_root.resolve()
    manifests: dict[str, Any] = {}
    all_match = True
    union_paths: set[str] = set()
    for name, expected_manifest_hash in PINNED_MANIFEST_SHA256.items():
        manifest_path = candidate_root / name
        observed_manifest_hash = (
            sha256_path(manifest_path) if manifest_path.is_file() else None
        )
        rows: dict[str, Any] = {}
        missing = 0
        mismatches = 0
        entries = parse_checksum_manifest(manifest_path) if manifest_path.is_file() else []
        for relative, expected in entries:
            target = _allowed_manifest_target(candidate_root, relative)
            observed = sha256_path(target) if target.is_file() else None
            matches = observed == expected
            rows[relative] = {
                "expected_sha256": expected,
                "observed_sha256": observed,
                "matches": matches,
            }
            union_paths.add(str(target))
            if observed is None:
                missing += 1
            elif not matches:
                mismatches += 1
        manifest_matches = observed_manifest_hash == expected_manifest_hash
        row_match = manifest_matches and not missing and not mismatches
        all_match = all_match and row_match
        manifests[name] = {
            "expected_manifest_sha256": expected_manifest_hash,
            "observed_manifest_sha256": observed_manifest_hash,
            "manifest_matches": manifest_matches,
            "entry_count": len(entries),
            "missing": missing,
            "mismatches": mismatches,
            "all_match": row_match,
            "entries": rows,
        }
    return {
        "all_match": all_match,
        "manifest_path_count": len(union_paths),
        "manifests": manifests,
    }


def verify_core_pins(candidate_root: Path) -> dict[str, Any]:
    entries: dict[str, Any] = {}
    all_match = True
    for relative, expected in PINNED_V023.items():
        path = candidate_root / Path(relative)
        observed = sha256_path(path) if path.is_file() else None
        matches = observed == expected
        entries[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "matches": matches,
        }
        all_match = all_match and matches
    return {"all_match": all_match, "entries": entries}


def _history_stats(history_paths: Iterable[Path]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for path in history_paths:
        payload = load_json(path)
        for name, result in payload.get("fixtures", {}).items():
            row = stats.setdefault(
                name, {"runs": 0.0, "mismatches": 0.0, "cost_ns": 0.0}
            )
            row["runs"] += 1.0
            row["mismatches"] += 0.0 if result.get("matches_expectation") else 1.0
            row["cost_ns"] += float(
                result.get("timing_ns", {}).get("median", 1_000_000)
            )
    return stats


def adaptive_fixture_order(
    names: Iterable[str], history_paths: Iterable[Path] = ()
) -> list[str]:
    available = set(names)
    prefix = [name for name in SMOKE_PREFIX if name in available]
    remaining = available.difference(prefix)
    stats = _history_stats(history_paths)

    def score(name: str) -> tuple[float, str]:
        prior = RISK_PRIOR.get(name, 1.0)
        row = stats.get(name)
        if row and row["runs"]:
            mismatch_rate = row["mismatches"] / row["runs"]
            mean_cost = max(1.0, row["cost_ns"] / row["runs"])
            utility = (prior + 20.0 * mismatch_rate) / mean_cost
        else:
            utility = prior / 1_000_000.0
        return (-utility, name)

    return prefix + sorted(remaining, key=score)


def import_validator(candidate_root: Path) -> Any:
    source_root = str((candidate_root / "src").resolve())
    sys.path.insert(0, source_root)
    for name in list(sys.modules):
        if name == "pnp_glc_i0" or name.startswith("pnp_glc_i0."):
            del sys.modules[name]
    module = importlib.import_module(VALIDATOR_MODULE)
    module_path = Path(module.__file__).resolve()
    expected_root = (candidate_root / "src").resolve()
    if expected_root not in module_path.parents:
        raise RuntimeError(f"validator imported from unexpected path: {module_path}")
    return module


def _fixture_report(
    validator: Any, candidate_root: Path, schema_path: Path, name: str
) -> tuple[Mapping[str, Any], dict[str, Any]]:
    path = candidate_root / FIXTURE_DIRECTORY / f"{name}.json"
    record = validator.load_json(path)
    report = validator.validate_path(path, schema_path, candidate_root).to_dict()
    return record, report


def explicit_regression_probes(
    validator: Any, candidate_root: Path, schema_path: Path
) -> dict[str, Any]:
    store = validator.ArtifactIndex(candidate_root)

    def rejection_group(names: Sequence[str]) -> dict[str, Any]:
        cases: dict[str, Any] = {}
        for name in names:
            record, report = _fixture_report(
                validator, candidate_root, schema_path, name
            )
            signature = validator._trace_authenticity_status(record, store)
            cases[name] = {
                "trace_authenticity_status": signature,
                "record_accepted": bool(report["record_accepted"]),
                "issue_codes": sorted(
                    {issue["code"] for issue in report.get("issues", [])}
                ),
                "conformant": signature == validator.PASS
                and not bool(report["record_accepted"]),
            }
        return {
            "cases": cases,
            "all_conformant": all(row["conformant"] for row in cases.values()),
        }

    prov_derive = rejection_group(
        ("fabricated-states-999", "fabricated-transition-digest")
    )
    ref_type = rejection_group(
        (
            "receipt-ref-substitution",
            "robust-ref-type-confusion",
            "cross-role-contract-invariant",
        )
    )

    classification_root = (
        candidate_root / ARTIFACT_DIRECTORY / CLOSURE_CLASSIFICATION_DIRECTORY
    )
    classification_manifest = validator.load_json(
        classification_root / "manifest.json"
    )
    classification_cases: dict[str, Any] = {}
    for name, expected in classification_manifest["expected_status"].items():
        path = classification_root / f"{name}.json"
        reference = f"sha256:{validator.sha256_bytes(path.read_bytes())}"
        observed = validator._artifact_closure(
            {"run-spec": reference}, store
        ).status
        classification_cases[name] = {
            "expected": expected,
            "observed": observed,
            "matches": observed == expected,
        }
    supported_path = (
        candidate_root / ARTIFACT_DIRECTORY / SUPPORTED_RUN_SPEC_FILENAME
    )
    supported_ref = f"sha256:{validator.sha256_bytes(supported_path.read_bytes())}"
    supported_observed = validator._artifact_closure(
        {"run-spec": supported_ref}, store
    ).status
    end_to_end = rejection_group(
        ("malformed-unsupported-envelope", "shape-valid-unsupported-envelope")
    )
    closure_class = {
        "artifact_cases": classification_cases,
        "artifact_case_count": len(classification_cases),
        "all_artifact_cases_match": all(
            row["matches"] for row in classification_cases.values()
        ),
        "supported_control": {
            "expected": validator.PASS,
            "observed": supported_observed,
            "matches": supported_observed == validator.PASS,
        },
        "end_to_end": end_to_end,
    }
    closure_class["all_conformant"] = (
        closure_class["all_artifact_cases_match"]
        and closure_class["supported_control"]["matches"]
        and end_to_end["all_conformant"]
    )

    positive_cases: dict[str, Any] = {}
    for name in POSITIVE_CONTROLS:
        _record, report = _fixture_report(
            validator, candidate_root, schema_path, name
        )
        positive_cases[name] = {
            "record_accepted": bool(report["record_accepted"]),
            "conformant": bool(report["record_accepted"]),
        }
    positive_control = {
        "cases": positive_cases,
        "all_conformant": all(
            row["conformant"] for row in positive_cases.values()
        ),
        "purpose": "Reject-all implementations cannot pass this control.",
    }

    groups = {
        "PROV-DERIVE-01": prov_derive,
        "REF-TYPE-01": ref_type,
        "CLOSURE-CLASS-01": closure_class,
        "positive-controls": positive_control,
    }
    return {
        "groups": groups,
        "all_conformant": all(row["all_conformant"] for row in groups.values()),
        "nonclaim": "These are bounded executable-interface regressions, not P/NP conclusions.",
    }


def closure_edge_scope_witness(
    validator: Any, candidate_root: Path
) -> dict[str, Any]:
    """Record the independently accepted v0.2.3 specification ambiguity.

    This is not another malformed-artifact probe.  The same shape-valid future
    envelope is UNKNOWN under the supported-only relation reading, while the
    unqualified ``edge_shape.expected_type`` sentence admits a reasonable global
    relation reading for which no pinned future parent/role relation exists.
    """
    store = validator.ArtifactIndex(candidate_root)
    path = (
        candidate_root
        / "artifacts-v0.2.3"
        / "closure-classification"
        / "shape-valid-unsupported-future-type.json"
    )
    reference = f"sha256:{validator.sha256_bytes(path.read_bytes())}"
    implementation_status = validator._artifact_closure(
        {"run-spec": reference}, store
    ).status
    closure_spec = load_json(
        candidate_root
        / "artifacts-v0.2.3"
        / "artifact-closure-spec.v0.2.3.json"
    )
    return {
        **KNOWN_FROZEN_BLOCKER,
        "witness_path": str(path),
        "witness_sha256": sha256_path(path),
        "implementation_status": implementation_status,
        "frozen_edge_sentence": closure_spec["edge_shape"]["expected_type"],
        "reasonable_readings": {
            "global_pinned_relation": (
                "FAIL because no pinned relation exists for the future parent/role"
            ),
            "supported_spec_only": "UNKNOWN before relation traversal",
        },
        "readings_confluent": False,
        "required_repair": (
            "Version the interface and separate GenericEdgeShape from "
            "SupportedEdgeRelation; do not modify v0.2.3 bytes."
        ),
    }


def probe(
    candidate_root: Path,
    repetitions: int,
    history_paths: Sequence[Path],
    fail_fast: bool,
    batch_snapshot: bool,
) -> dict[str, Any]:
    candidate_root = candidate_root.resolve()
    if repetitions < 1:
        raise ValueError("repetitions must be at least 1")

    manifests_before = frozen_manifest_state(candidate_root)
    pins_before = verify_core_pins(candidate_root)
    if not manifests_before["all_match"] or not pins_before["all_match"]:
        return {
            "status": "blocked-pin-mismatch",
            "candidate_root": str(candidate_root),
            "frozen_manifests_before": manifests_before,
            "pins_before": pins_before,
            "selection": "no-change-control",
        }

    validator = import_validator(candidate_root)
    schema_path = candidate_root / SCHEMA_RELATIVE
    fixture_manifest = load_json(
        candidate_root / FIXTURE_DIRECTORY / "manifest.json"
    )
    expected_fixtures = fixture_manifest["fixtures"]
    order = adaptive_fixture_order(expected_fixtures.keys(), history_paths)
    results: dict[str, Any] = {}

    original_artifact_index = validator.ArtifactIndex
    snapshot_file_count: int | None = None
    snapshot_byte_count: int | None = None
    if batch_snapshot:
        shared_store = original_artifact_index(candidate_root)
        snapshot_by_path: dict[Path, bytes] = {}
        for entries in shared_store._by_hash.values():
            for path, content in entries:
                snapshot_by_path[path] = content
        snapshot_file_count = len(snapshot_by_path)
        snapshot_byte_count = sum(len(content) for content in snapshot_by_path.values())
        schema_bytes = snapshot_by_path[schema_path.resolve()]
        record_bytes = {
            name: snapshot_by_path[
                (
                    candidate_root / FIXTURE_DIRECTORY / f"{name}.json"
                ).resolve()
            ]
            for name in order
        }
        validator.ArtifactIndex = lambda _root: shared_store

        def run_fixture(name: str) -> Any:
            return validator.validate_bytes(
                record_bytes[name], schema_bytes, candidate_root
            )
    else:
        def run_fixture(name: str) -> Any:
            fixture = candidate_root / FIXTURE_DIRECTORY / f"{name}.json"
            return validator.validate_path(fixture, schema_path, candidate_root)

    try:
        for name in order:
            observed = run_fixture(name).to_dict()
            mismatches = compare_expected(observed, expected_fixtures[name])
            samples: list[int] = []
            for _ in range(repetitions):
                started = time.perf_counter_ns()
                run_fixture(name)
                samples.append(time.perf_counter_ns() - started)
            results[name] = {
                "matches_expectation": not mismatches,
                "mismatches": mismatches,
                "observed": {
                    key: observed.get(key)
                    for key in (
                        "structural_ok",
                        "semantic_ok",
                        "admission_pass",
                        "final_completion",
                        "record_accepted",
                    )
                },
                "issue_codes": sorted(
                    {issue["code"] for issue in observed.get("issues", [])}
                ),
                "timing_ns": {
                    "repetitions": repetitions,
                    "minimum": min(samples),
                    "median": int(statistics.median(samples)),
                    "p95_nearest_rank": percentile_nearest_rank(samples, 0.95),
                    "maximum": max(samples),
                },
            }
            if fail_fast and mismatches:
                break
    finally:
        validator.ArtifactIndex = original_artifact_index

    explicit = explicit_regression_probes(
        validator, candidate_root, schema_path
    )
    specification_blocker = closure_edge_scope_witness(
        validator, candidate_root
    )
    pins_after = verify_core_pins(candidate_root)
    manifests_after = frozen_manifest_state(candidate_root)
    path_set_stable = manifests_before == manifests_after
    all_evaluated_match = (
        len(results) == len(expected_fixtures)
        and all(row["matches_expectation"] for row in results.values())
    )
    medians = [row["timing_ns"]["median"] for row in results.values()]
    probe_execution_ok = (
        all_evaluated_match
        and explicit["all_conformant"]
        and path_set_stable
        and pins_before == pins_after
    )
    local_candidate_retention_allowed = (
        probe_execution_ok
        and specification_blocker["readings_confluent"]
        and not EXTERNAL_DISPOSITION_BLOCKERS
    )
    return {
        "status": "experiment",
        "epistemic_status": "unpromoted-candidate",
        "candidate_root": str(candidate_root),
        "candidate_validator_sha256": PINNED_V023[VALIDATOR_RELATIVE],
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "pid": os.getpid(),
        },
        "frozen_manifests_before": manifests_before,
        "frozen_manifests_after": manifests_after,
        "manifest_path_set_stable_during_probe": path_set_stable,
        "pins_before": pins_before,
        "pins_after": pins_after,
        "mode": "fail-fast" if fail_fast else "full",
        "execution_model": (
            "one-immutable-bundle-snapshot"
            if batch_snapshot
            else "isolated-rescan-per-record"
        ),
        "snapshot_file_count": snapshot_file_count,
        "snapshot_byte_count": snapshot_byte_count,
        "fixture_order": order,
        "fixtures": results,
        "fixture_count": len(results),
        "all_manifest_expectations_match": all_evaluated_match,
        "explicit_regression_probes": explicit,
        "known_specification_blocker": specification_blocker,
        "external_disposition_blockers": EXTERNAL_DISPOSITION_BLOCKERS,
        "probe_execution_ok": probe_execution_ok,
        "local_candidate_retention_allowed": local_candidate_retention_allowed,
        "independent_acceptance_observed": False,
        "promotion_allowed": False,
        "aggregate_timing_ns": {
            "sum_of_fixture_medians": sum(medians),
            "median_fixture": int(statistics.median(medians)) if medians else None,
        },
        "selection": (
            "candidate-remains-unpromoted-pending-independent-acceptance"
            if local_candidate_retention_allowed
            else "no-change-control"
        ),
        "nonclaims": [
            "local validation is not independent acceptance",
            "timing is empirical validation throughput, not solver speed or asymptotic complexity",
            "experimental success or failure has no P versus NP implication",
        ],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only AEREC probe for the frozen AI-4 I0 "
            f"v{CANDIDATE_VERSION} candidate."
        )
    )
    parser.add_argument("--candidate-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--history", action="append", default=[], type=Path)
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument(
        "--batch-snapshot",
        action="store_true",
        help="Reuse one immutable full-bundle byte snapshot across all records.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = probe(
        args.candidate_root,
        args.repetitions,
        args.history,
        args.fail_fast,
        args.batch_snapshot,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({
        "output": str(args.output.resolve()),
        "selection": report.get("selection"),
        "fixture_count": report.get("fixture_count"),
        "all_manifest_expectations_match": report.get(
            "all_manifest_expectations_match"
        ),
        "manifest_path_set_stable_during_probe": report.get(
            "manifest_path_set_stable_during_probe"
        ),
        "explicit_regressions_conformant": report.get(
            "explicit_regression_probes", {}
        ).get("all_conformant"),
        "probe_execution_ok": report.get("probe_execution_ok"),
        "local_candidate_retention_allowed": report.get(
            "local_candidate_retention_allowed"
        ),
        "independent_acceptance_observed": report.get(
            "independent_acceptance_observed"
        ),
        "promotion_allowed": report.get("promotion_allowed"),
    }, ensure_ascii=False))
    return 0 if report.get("probe_execution_ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
