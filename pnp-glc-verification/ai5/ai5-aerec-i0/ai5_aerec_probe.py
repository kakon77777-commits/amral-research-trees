from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


V01_SCHEMA_SHA256 = (
    "3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4"
)

PINNED_V021: dict[str, str] = {
    "schemas/run-record.schema.v0.2.1-candidate.json":
        "567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B",
    "src/pnp_glc_i0/semantic_validator_v021.py":
        "C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4",
    "artifacts-v0.2.1/candidate-projection-spec.v0.2.1.json":
        "70CAAE9973A3A02AD8F45364BE2175A51BA62C6C0D75B6C807B7B8DFB5BBD115",
    "artifacts-v0.2.1/artifact-closure-spec.v0.2.1.json":
        "B466BF8D630BAC4B1A42A28F534C5D20A0713D418CCB3826ED69FF71D7585C94",
    "artifacts-v0.2.1/trace-public-key.v0.2.1.json":
        "27D25EBF48C59E9AFF166D32970C3444DC78E25C352F012B3998B0626DFB2A3D",
    "fixtures-v0.2.1/manifest.json":
        "6081A4839BB75C2D80E8B856F7018CD2887ACCCBFD8067BCFDC417B53F4A79B3",
    "i0-run-report.v0.2.1.json":
        "3D7851B23F4F41905E76DEEA7CD54839C4DACBBEA4D50D8F92B124AAB20A6A55",
}

# The smoke prefix deliberately mixes positive controls and known attacks. A validator
# that simply rejects everything must fail before it can look good on negative probes.
SMOKE_PREFIX = [
    "legit",
    "fabricated-states-999",
    "fabricated-transition-digest",
    "2sat-sat",
    "2sat-unsat",
    "bad-trace-signature",
    "missing-transitive-ref",
]

RISK_PRIOR: dict[str, float] = {
    "fabricated-states-999": 8.0,
    "fabricated-transition-digest": 8.0,
    "bad-trace-signature": 5.0,
    "missing-transitive-ref": 5.0,
    "tampered-record": 4.0,
    "tampered-trace": 4.0,
    "unresolved-event-ref": 4.0,
    "canonicalization-variant": 3.0,
}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def verify_pins(candidate_root: Path) -> dict[str, Any]:
    entries: dict[str, Any] = {}
    all_match = True
    for relative, expected in PINNED_V021.items():
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


def _history_stats(history_paths: Iterable[Path]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for path in history_paths:
        payload = load_json(path)
        for name, result in payload.get("fixtures", {}).items():
            row = stats.setdefault(name, {"runs": 0.0, "mismatches": 0.0, "cost_ns": 0.0})
            row["runs"] += 1.0
            row["mismatches"] += 0.0 if result.get("matches_expectation") else 1.0
            row["cost_ns"] += float(result.get("timing_ns", {}).get("median", 1_000_000))
    return stats


def adaptive_fixture_order(
    names: Iterable[str], history_paths: Iterable[Path] = ()
) -> list[str]:
    available = set(names)
    prefix = [name for name in SMOKE_PREFIX if name in available]
    remaining = available.difference(prefix)
    stats = _history_stats(history_paths)

    def score(name: str) -> tuple[float, str]:
        row = stats.get(name)
        prior = RISK_PRIOR.get(name, 1.0)
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
    module = importlib.import_module("pnp_glc_i0.semantic_validator_v021")
    module_path = Path(module.__file__).resolve()
    expected_root = (candidate_root / "src").resolve()
    if expected_root not in module_path.parents:
        raise RuntimeError(f"validator imported from unexpected path: {module_path}")
    return module


def packaging_topology(candidate_root: Path, explicit_v01: Path | None) -> dict[str, Any]:
    expected_parent = candidate_root.parent / "run-record.schema.json"
    internal = candidate_root / "run-record.schema.json"
    supplied = explicit_v01.resolve() if explicit_v01 else None
    supplied_hash = sha256_path(supplied) if supplied and supplied.is_file() else None
    return {
        "candidate_is_self_contained_for_predecessor_test": internal.is_file(),
        "test_expected_parent_path": str(expected_parent),
        "test_expected_parent_present": expected_parent.is_file(),
        "explicit_v01_schema": str(supplied) if supplied else None,
        "explicit_v01_sha256": supplied_hash,
        "explicit_v01_matches": supplied_hash == V01_SCHEMA_SHA256 if supplied else None,
        "observation": (
            "The shipped candidate root does not contain v0.1; both test suites resolve it "
            "from ROOT.parent/run-record.schema.json. A relocated candidate therefore needs "
            "an external compatibility layout."
        ),
    }


def ref_type_01_negative_probe(validator: Any, candidate_root: Path) -> dict[str, Any]:
    """Reproduce the frozen v0.2.1 receipt-role substitution counterexample.

    The probe changes only receipt metadata in memory. It uses existing synthetic test
    artifacts and does not create a signature, access a signing secret, or write into the
    candidate. A role-aware validator is expected to reject the resulting record.
    """
    fixture = candidate_root / "fixtures-v0.2.1" / "robust-legit.json"
    standard_run_spec = candidate_root / "artifacts" / "run-standard.v0.2.0.json"
    schema_path = candidate_root / "schemas" / "run-record.schema.v0.2.1-candidate.json"
    original = validator.load_json(fixture)
    record = copy.deepcopy(original)
    original_projection = validator.candidate_projection_sha256(original)
    substituted_reference = f"sha256:{validator.sha256_path(standard_run_spec)}"
    record["validation_receipt"]["run_spec_ref"] = substituted_reference

    store = validator.ArtifactIndex(candidate_root)
    closure = validator._artifact_closure(
        validator._direct_receipt_reference_set(record), store
    )
    record["validation_receipt"]["resolved_evidence_hashes"] = [
        f"sha256:{reference}" for reference in sorted(closure.references)
    ]
    trace_authenticity = validator._trace_authenticity_status(record, store)
    schema_bytes = schema_path.read_bytes()
    schema = validator._load_json_object_bytes(schema_bytes, source=str(schema_path))
    report = validator.validate_record(
        record,
        schema,
        candidate_root,
        schema_sha256=validator.sha256_bytes(schema_bytes),
    ).to_dict()
    expected_rejection_observed = not bool(report["record_accepted"])
    return {
        "classification": "evidence-role-binding-counterexample",
        "fixture": "robust-legit",
        "mutation_scope": "validation_receipt.run_spec_ref plus recomputed closure only",
        "substituted_reference": substituted_reference,
        "candidate_projection_unchanged": (
            original_projection == validator.candidate_projection_sha256(record)
        ),
        "trace_authenticity_status": trace_authenticity,
        "closure_status": closure.status,
        "expected_rejection_observed": expected_rejection_observed,
        "observed": {
            key: report.get(key)
            for key in (
                "structural_ok",
                "semantic_ok",
                "admission_pass",
                "final_completion",
                "record_accepted",
            )
        },
        "issue_codes": sorted(
            {issue["code"] for issue in report.get("issues", [])}
        ),
        "nonclaim": "This is an executable-interface counterexample with no P/NP implication.",
    }


def probe(
    candidate_root: Path,
    repetitions: int,
    history_paths: Sequence[Path],
    fail_fast: bool,
    explicit_v01: Path | None,
    batch_snapshot: bool,
) -> dict[str, Any]:
    candidate_root = candidate_root.resolve()
    if repetitions < 1:
        raise ValueError("repetitions must be at least 1")

    pins_before = verify_pins(candidate_root)
    if not pins_before["all_match"]:
        return {
            "status": "blocked-pin-mismatch",
            "candidate_root": str(candidate_root),
            "pins_before": pins_before,
            "selection": "no-change",
        }

    validator = import_validator(candidate_root)
    schema_path = candidate_root / "schemas" / "run-record.schema.v0.2.1-candidate.json"
    manifest = load_json(candidate_root / "fixtures-v0.2.1" / "manifest.json")
    expected_fixtures = manifest["fixtures"]
    order = adaptive_fixture_order(expected_fixtures.keys(), history_paths)
    results: dict[str, Any] = {}

    original_artifact_index = validator.ArtifactIndex
    snapshot_file_count: int | None = None
    snapshot_byte_count: int | None = None
    if batch_snapshot:
        # One ArtifactIndex construction snapshots every file exactly once. We then take
        # schema and record objects from those same bytes and reuse the same content store.
        # This keeps TOCTOU closure while avoiding a full-tree rescan for every fixture.
        shared_store = original_artifact_index(candidate_root)
        snapshot_by_path: dict[Path, bytes] = {}
        for entries in shared_store._by_hash.values():
            for path, content in entries:
                snapshot_by_path[path] = content
        snapshot_file_count = len(snapshot_by_path)
        snapshot_byte_count = sum(len(content) for content in snapshot_by_path.values())
        schema_bytes = snapshot_by_path[schema_path.resolve()]
        schema_object = validator._load_json_object_bytes(
            schema_bytes, source=str(schema_path)
        )
        schema_hash = validator.sha256_bytes(schema_bytes)
        records = {
            name: validator._load_json_object_bytes(
                snapshot_by_path[
                    (candidate_root / "fixtures-v0.2.1" / f"{name}.json").resolve()
                ],
                source=name,
            )
            for name in order
        }
        validator.ArtifactIndex = lambda _root: shared_store

        def run_fixture(name: str) -> Any:
            return validator.validate_record(
                records[name],
                schema_object,
                candidate_root,
                schema_sha256=schema_hash,
            )
    else:
        def run_fixture(name: str) -> Any:
            fixture = candidate_root / "fixtures-v0.2.1" / f"{name}.json"
            return validator.validate_path(fixture, schema_path, candidate_root)

    try:
        for name in order:
            # One warmup also supplies the report compared with the frozen manifest.
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

    pins_after = verify_pins(candidate_root)
    external_negative_probes = {
        "REF-TYPE-01": ref_type_01_negative_probe(validator, candidate_root),
    }
    all_external_negative_probes_rejected = all(
        row["expected_rejection_observed"]
        for row in external_negative_probes.values()
    )
    all_evaluated_match = (
        len(results) == len(expected_fixtures)
        and all(row["matches_expectation"] for row in results.values())
    )
    stable = pins_before == pins_after
    medians = [row["timing_ns"]["median"] for row in results.values()]
    return {
        "status": "experiment",
        "epistemic_status": "unpromoted-candidate",
        "candidate_root": str(candidate_root),
        "candidate_validator_sha256": PINNED_V021[
            "src/pnp_glc_i0/semantic_validator_v021.py"
        ],
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "pid": os.getpid(),
        },
        "packaging": packaging_topology(candidate_root, explicit_v01),
        "pins_before": pins_before,
        "pins_after": pins_after,
        "snapshot_stable_during_probe": stable,
        "mode": "fail-fast" if fail_fast else "full",
        "execution_model": (
            "one-immutable-bundle-snapshot" if batch_snapshot else "isolated-rescan-per-record"
        ),
        "snapshot_file_count": snapshot_file_count,
        "snapshot_byte_count": snapshot_byte_count,
        "fixture_order": order,
        "fixtures": results,
        "external_negative_probes": external_negative_probes,
        "all_external_negative_probes_rejected": all_external_negative_probes_rejected,
        "aggregate_timing_ns": {
            "sum_of_fixture_medians": sum(medians),
            "median_fixture": int(statistics.median(medians)) if medians else None,
        },
        "all_manifest_expectations_match": all_evaluated_match,
        "selection": (
            "no-change-control"
            if (
                not all_evaluated_match
                or not stable
                or not all_external_negative_probes_rejected
            )
            else "candidate-remains-unpromoted-pending-independent-acceptance"
        ),
        "nonclaims": [
            "local validation is not independent acceptance",
            "timing is empirical wall time, not an asymptotic complexity claim",
            "experimental success or failure has no P versus NP implication",
        ],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only AEREC probe for the frozen AI-4 I0 v0.2.1 candidate."
    )
    parser.add_argument("--candidate-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repetitions", type=int, default=7)
    parser.add_argument("--history", action="append", default=[], type=Path)
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument(
        "--batch-snapshot",
        action="store_true",
        help="Reuse one immutable full-bundle byte snapshot across all records.",
    )
    parser.add_argument("--v01-schema", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = probe(
        args.candidate_root,
        args.repetitions,
        args.history,
        args.fail_fast,
        args.v01_schema,
        args.batch_snapshot,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({
        "output": str(args.output.resolve()),
        "selection": report.get("selection"),
        "all_manifest_expectations_match": report.get("all_manifest_expectations_match"),
        "snapshot_stable_during_probe": report.get("snapshot_stable_during_probe"),
        "all_external_negative_probes_rejected": report.get(
            "all_external_negative_probes_rejected"
        ),
    }, ensure_ascii=False))
    return 0 if (
        report.get("all_manifest_expectations_match")
        and report.get("all_external_negative_probes_rejected")
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main())
