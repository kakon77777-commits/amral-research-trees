from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import ai5_aerec_probe_v023 as engine


PROFILE = {
    "candidate_version": "0.2.4",
    "validator_module": "pnp_glc_i0.semantic_validator_v024",
    "validator_relative": "src/pnp_glc_i0/semantic_validator_v024.py",
    "schema_relative": "schemas/run-record.schema.v0.2.4-candidate.json",
    "fixture_directory": "fixtures-v0.2.4",
    "artifact_directory": "artifacts-v0.2.4",
    "supported_run_spec_filename": "run-standard.v0.2.4.json",
}

PINNED_MANIFEST_SHA256 = {
    "SHA256SUMS.txt":
        "3353BEE6FE6728835608C6FA1EFD511CC8757A097D9403FCF78C5339C2CAF130",
    "SHA256SUMS-v0.2.1.txt":
        "4F5925CD2A449549F9629017E538F5FA341FA8BAECB4A5BB3F8B93ED005EBD6A",
    "SHA256SUMS-v0.2.2-candidate.txt":
        "AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B",
    "SHA256SUMS-v0.2.3-candidate.txt":
        "7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817",
    "SHA256SUMS-v0.2.4-candidate.txt":
        "73ED3607EAD3F50502DCEFA3142DFFEE01AAC8576C045F05CA96DEB9669F77FE",
}

PINNED_CORE = {
    "schemas/run-record.schema.v0.2.4-candidate.json":
        "16EBCC7DE4196D0C46FC9C309F2060F856E321C0012C5B775390C04234F9DCC8",
    "src/pnp_glc_i0/semantic_validator_v024.py":
        "B744C9C20C510FE39F132E0DFB4AAC50E6E3E573B48B7F1AE19494F5D5195FED",
    "artifacts-v0.2.4/candidate-projection-spec.v0.2.4.json":
        "CCF57716E63AD6B627F48688925054975254A88344E7F84ECBEC9CF0145B9D6D",
    "artifacts-v0.2.4/artifact-closure-spec.v0.2.4.json":
        "579B6F7DA8BE3712FE6130AD900CF0CBA189496100548CBF87655687A7690588",
    "artifacts-v0.2.4/evidence-role-spec.v0.2.4.json":
        "4EFC4C71C6275227B14429E58FCECC4E949459918315D27CC476765C7D24D850",
    "fixtures-v0.2.4/manifest.json":
        "5F79E8DC3EBAD4A9BA8C32C7092CDF52307220D08EF1D83EFD399B12B00B7AB1",
    "artifacts-v0.2.4/closure-classification/manifest.json":
        "09E9E6E4C0F1528C8239606DB6CC0A724B1031973F8D79F504FC22A2793A9159",
    "scripts/reproduce_closure_class_v024.py":
        "5F0FB64D1BB6DA17804088260FCA94A92F21DD4C2F5FAC1A9605F9F3BAD303DB",
    "scripts/reproduce_oracle_decl_family_v024.py":
        "0A0EA8607D2E07E6189ACC52B698E781CF742C6523C4D46FF3F02330AF1B779B",
    "i0-run-report.v0.2.4-candidate.json":
        "FC25C0E04D44ACCC0F5232B4F852056B870D82059F7542D4307EC966C0EB9300",
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
    "parity-with-2sat-oracle-declaration",
    "2sat-with-parity-oracle-declaration",
    "2sat-sat-with-unsat-oracle-declaration",
    "2sat-unsat-with-sat-oracle-declaration",
    "parity-with-2sat-oracle-oracle_id-only",
    "parity-with-2sat-oracle-entrypoint-only",
    "parity-with-2sat-oracle-name-only",
    "parity-with-2sat-oracle-checks-only",
    "parity-with-2sat-oracle-obligations-only",
]

ORACLE_DECLARATION_NEGATIVES = tuple(SMOKE_PREFIX[9:])

EXTERNAL_DISPOSITION_BLOCKERS = [
    {
        "id": "ADVICE-DECL-LEDGER-01",
        "disposition": "FAIL",
        "classification": "declaration-ledger consistency",
        "independently_reproduced": True,
        "frozen_manifest_fixture_present": False,
        "accepted_record_contradiction": (
            "per-n truth-table advice declaration coexists with uniform mode, "
            "no advice generator, no answer access, and zero advice/generation ledger"
        ),
        "correctness_bypass_claim": False,
        "p_np_implication": False,
        "required_repair": (
            "replace free-text advice with typed advice_mode and derive a bidirectional "
            "ExpectedAdviceDecl consistency judgment"
        ),
    }
]

BASE_EXPLICIT_REGRESSION_PROBES = engine.explicit_regression_probes


def closure_scope_audit(validator: Any, candidate_root: Path) -> dict[str, Any]:
    store = validator.ArtifactIndex(candidate_root)
    artifact_root = candidate_root / PROFILE["artifact_directory"]
    classification_root = artifact_root / "closure-classification"
    spec = engine.load_json(artifact_root / "artifact-closure-spec.v0.2.4.json")
    judgments = spec.get("judgments", {})

    def classify(name: str) -> str:
        path = classification_root / f"{name}.json"
        reference = f"sha256:{validator.sha256_bytes(path.read_bytes())}"
        return validator._artifact_closure({"run-spec": reference}, store).status

    generic = judgments.get("GenericEdgeShape", {})
    supported = judgments.get("SupportedEdgeRelation", {})
    unsupported = judgments.get("UnsupportedEnvelope", {})
    checks = {
        "normative-precedence-declared": (
            spec.get("normative_precedence", "").startswith("The judgments object")
        ),
        "generic-envelope-judgment-defined": "GenericEnvelopeShape" in judgments,
        "generic-relation-not-required": len(generic.get("does_not_require", [])) >= 3,
        "supported-relation-iff-supported-header": (
            supported.get("applicable_iff")
            == "judgments.SupportedEnvelopeHeader holds"
        ),
        "unsupported-relation-not-applicable": "unsupported spec_id"
        in supported.get("not_applicable_when", ""),
        "unsupported-result-unknown": unsupported.get("result") == "UNKNOWN",
        "future-unsupported-is-unknown": (
            classify("shape-valid-unsupported-future-type") == validator.UNKNOWN
        ),
        "future-supported-is-fail": (
            classify("supported-future-artifact-type") == validator.FAIL
        ),
    }
    readings_confluent = all(checks.values())
    return {
        "id": "CLOSURE-JUDGMENT-COMPLETENESS-01",
        "repaired_regression_id": "CLOSURE-EDGE-SCOPE-01",
        "disposition": (
            "repaired-local-candidate"
            if readings_confluent
            else "no-change-pending-normative-symbol-closure"
        ),
        "classification": "Definition-interface confluence control",
        "scope_checks": checks,
        "scope_check_count": len(checks),
        "undefined_normative_symbols": (
            [] if checks["generic-envelope-judgment-defined"]
            else ["GenericEnvelopeShape"]
        ),
        "readings_confluent": readings_confluent,
        "implementation_acceptance_bypass": False,
        "p_np_implication": False,
    }


def explicit_regression_probes_v024(
    validator: Any, candidate_root: Path, schema_path: Path
) -> dict[str, Any]:
    result = BASE_EXPLICIT_REGRESSION_PROBES(
        validator, candidate_root, schema_path
    )
    store = validator.ArtifactIndex(candidate_root)
    cases: dict[str, Any] = {}
    for name in ORACLE_DECLARATION_NEGATIVES:
        record, report = engine._fixture_report(
            validator, candidate_root, schema_path, name
        )
        signature = validator._trace_authenticity_status(record, store)
        oracle_status = validator._independent_oracle_status(record)
        issue_codes = sorted(
            {issue["code"] for issue in report.get("issues", [])}
        )
        conformant = (
            signature == validator.PASS
            and oracle_status == validator.PASS
            and not bool(report["record_accepted"])
            and "oracle-declaration-family-binding" in issue_codes
        )
        cases[name] = {
            "trace_authenticity_status": signature,
            "actual_family_oracle_status": oracle_status,
            "record_accepted": bool(report["record_accepted"]),
            "issue_codes": issue_codes,
            "conformant": conformant,
        }
    group = {
        "cases": cases,
        "case_count": len(cases),
        "all_conformant": all(row["conformant"] for row in cases.values()),
        "classification": "declaration provenance; not correctness bypass",
    }
    result["groups"]["ORACLE-DECL-FAMILY-01"] = group
    result["all_conformant"] = (
        result["all_conformant"] and group["all_conformant"]
    )
    return result


def configure_engine() -> None:
    engine.CANDIDATE_VERSION = PROFILE["candidate_version"]
    engine.VALIDATOR_MODULE = PROFILE["validator_module"]
    engine.VALIDATOR_RELATIVE = PROFILE["validator_relative"]
    engine.SCHEMA_RELATIVE = PROFILE["schema_relative"]
    engine.FIXTURE_DIRECTORY = PROFILE["fixture_directory"]
    engine.ARTIFACT_DIRECTORY = PROFILE["artifact_directory"]
    engine.SUPPORTED_RUN_SPEC_FILENAME = PROFILE["supported_run_spec_filename"]
    engine.EXTERNAL_DISPOSITION_BLOCKERS = EXTERNAL_DISPOSITION_BLOCKERS
    engine.PINNED_MANIFEST_SHA256 = PINNED_MANIFEST_SHA256
    engine.PINNED_V023 = PINNED_CORE
    engine.SMOKE_PREFIX = SMOKE_PREFIX
    engine.RISK_PRIOR = {
        **engine.RISK_PRIOR,
        **{name: 12.0 for name in ORACLE_DECLARATION_NEGATIVES},
    }
    engine.closure_edge_scope_witness = closure_scope_audit
    engine.explicit_regression_probes = explicit_regression_probes_v024


def probe(
    candidate_root: Path,
    repetitions: int,
    history_paths: Sequence[Path],
    fail_fast: bool,
    batch_snapshot: bool,
) -> dict[str, Any]:
    configure_engine()
    return engine.probe(
        candidate_root,
        repetitions,
        history_paths,
        fail_fast,
        batch_snapshot,
    )


def main(argv: Sequence[str] | None = None) -> int:
    configure_engine()
    return engine.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
