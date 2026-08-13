from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pnp_glc_i0.semantic_validator_v024 as validator  # noqa: E402
from pnp_glc_i0.semantic_validator_v024 import (  # noqa: E402
    FAIL,
    PASS,
    UNKNOWN,
    ArtifactIndex,
    _artifact_closure,
    _direct_receipt_reference_map,
    _independent_oracle_status,
    _operational_reference_status,
    _trace_authenticity_status,
    load_json,
    sha256_bytes,
    validate_bytes,
    validate_path,
)


class SemanticValidatorV024Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema_path = (
            ROOT / "schemas" / "run-record.schema.v0.2.4-candidate.json"
        )
        cls.schema_bytes = cls.schema_path.read_bytes()
        cls.schema = load_json(cls.schema_path)
        cls.manifest = load_json(ROOT / "fixtures-v0.2.4" / "manifest.json")
        cls.store = ArtifactIndex(ROOT)

    def test_schema_metaschema(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_frozen_predecessors_are_bitwise_preserved(self) -> None:
        expected = {
            ROOT.parent / "run-record.schema.json":
                "3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4",
            ROOT / "schemas" / "run-record.schema.v0.2.1-candidate.json":
                "567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B",
            ROOT / "src" / "pnp_glc_i0" / "semantic_validator_v021.py":
                "C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4",
            ROOT / "SHA256SUMS-v0.2.1.txt":
                "4F5925CD2A449549F9629017E538F5FA341FA8BAECB4A5BB3F8B93ED005EBD6A",
            ROOT / "schemas" / "run-record.schema.v0.2.2-candidate.json":
                "BDBB386CE7EAAB5377344BF29762CCBE45EA6371AC72742DE509467CB70BB556",
            ROOT / "src" / "pnp_glc_i0" / "semantic_validator_v022.py":
                "7DA459E8AD9FB3F8A49FAA312A612F05484588143F36FF0918D090D6B1965AE5",
            ROOT / "SHA256SUMS-v0.2.2-candidate.txt":
                "AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B",
            ROOT / "schemas" / "run-record.schema.v0.2.3-candidate.json":
                "DCE6F0C95B95D9377BA7AF9F9537BDC277CDF0E68CE74B9AD3BF83DB2B011895",
            ROOT / "src" / "pnp_glc_i0" / "semantic_validator_v023.py":
                "B0DC4EC989F93EBD557C4C8BFA3004E33B2BBAE0EB0F8FA5622489B2D148097B",
            ROOT / "SHA256SUMS-v0.2.3-candidate.txt":
                "7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817",
        }
        for path, digest in expected.items():
            with self.subTest(path=path.name):
                actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
                self.assertEqual(actual, digest)

    def test_fixture_manifest(self) -> None:
        for name, expected in self.manifest["fixtures"].items():
            with self.subTest(fixture=name):
                report = validate_path(
                    ROOT / "fixtures-v0.2.4" / f"{name}.json",
                    self.schema_path,
                    ROOT,
                ).to_dict()
                for key, value in expected.items():
                    self.assertEqual(report[key], value, report["issues"])

    def test_ref_type_receipt_substitution_keeps_signature_but_fails(self) -> None:
        record = load_json(
            ROOT / "fixtures-v0.2.4" / "receipt-ref-substitution.json"
        )
        trace = self.store.load_json(record["validation_receipt"]["trace_sha256"])
        closure = _artifact_closure(
            _direct_receipt_reference_map(record), self.store
        )
        operational, issues = _operational_reference_status(
            record, trace, self.store, closure
        )
        self.assertEqual(_trace_authenticity_status(record, self.store), PASS)
        self.assertEqual(operational, FAIL)
        self.assertIn("operational-role-binding", {issue.code for issue in issues})
        self.assertFalse(
            validate_path(
                ROOT / "fixtures-v0.2.4" / "receipt-ref-substitution.json",
                self.schema_path,
                ROOT,
            ).record_accepted
        )

    def test_valid_signature_cross_role_substitution_fails(self) -> None:
        path = ROOT / "fixtures-v0.2.4" / "cross-role-contract-invariant.json"
        record = load_json(path)
        self.assertEqual(_trace_authenticity_status(record, self.store), PASS)
        report = validate_path(path, self.schema_path, ROOT)
        codes = {issue.code for issue in report.issues}
        self.assertIn("direct-role-type", codes)
        self.assertIn("signed-operational-map-mismatch", codes)
        self.assertFalse(report.record_accepted)

    def test_oracle_declaration_is_bound_to_problem_family(self) -> None:
        for name in (
            "parity-with-2sat-oracle-declaration",
            "2sat-with-parity-oracle-declaration",
            "2sat-sat-with-unsat-oracle-declaration",
            "2sat-unsat-with-sat-oracle-declaration",
            "parity-with-2sat-oracle-oracle_id-only",
            "parity-with-2sat-oracle-entrypoint-only",
            "parity-with-2sat-oracle-name-only",
            "parity-with-2sat-oracle-checks-only",
            "parity-with-2sat-oracle-obligations-only",
        ):
            with self.subTest(fixture=name):
                path = ROOT / "fixtures-v0.2.4" / f"{name}.json"
                record = load_json(path)
                self.assertEqual(_trace_authenticity_status(record, self.store), PASS)
                self.assertEqual(
                    _independent_oracle_status(record),
                    PASS,
                    "the actual family-selected oracle still verifies; this fixture targets declaration provenance",
                )
                report = validate_path(path, self.schema_path, ROOT)
                self.assertIn(
                    "oracle-declaration-family-binding",
                    {issue.code for issue in report.issues},
                )
                self.assertFalse(report.record_accepted)

    def test_schema_requires_typed_oracle_identity(self) -> None:
        checker = Draft202012Validator(self.schema)
        baseline = load_json(ROOT / "fixtures-v0.2.4" / "legit.json")
        for field in ("oracle_id", "entrypoint", "obligations"):
            with self.subTest(field=field):
                mutated = copy.deepcopy(baseline)
                mutated["mechanism"]["oracle"].pop(field)
                self.assertFalse(checker.is_valid(mutated))

    def test_robust_public_key_type_confusion_fails(self) -> None:
        path = ROOT / "fixtures-v0.2.4" / "robust-ref-type-confusion.json"
        record = load_json(path)
        self.assertEqual(_trace_authenticity_status(record, self.store), PASS)
        report = validate_path(path, self.schema_path, ROOT)
        self.assertIn("direct-role-type", {issue.code for issue in report.issues})
        self.assertFalse(report.record_accepted)

    def test_supported_api_binds_schema_bytes(self) -> None:
        self.assertFalse(
            hasattr(validator, "validate_record"),
            "mapping plus claimed-hash helper must remain private",
        )
        record_bytes = (
            ROOT / "fixtures-v0.2.4" / "legit.json"
        ).read_bytes()
        report = validate_bytes(record_bytes, b"{}", ROOT)
        self.assertFalse(report.structural_ok)
        self.assertEqual(report.issues[0].code, "schema-byte-pin-mismatch")

    def test_negative_zero_is_rejected_in_raw_parse_domain(self) -> None:
        report = validate_path(
            ROOT / "fixtures-v0.2.4" / "negative-zero.json",
            self.schema_path,
            ROOT,
        )
        self.assertFalse(report.structural_ok)
        self.assertEqual(report.issues[0].code, "record-parse")
        self.assertIn("negative zero", report.issues[0].message)

    def test_ill_typed_supported_parameters_fail_closed_without_exception(self) -> None:
        record = load_json(ROOT / "fixtures-v0.2.4" / "legit.json")
        record["problem"]["generator"]["parameters"] = {}
        record_bytes = (
            json.dumps(record, ensure_ascii=False, sort_keys=True).encode("utf-8")
        )
        report = validate_bytes(record_bytes, self.schema_bytes, ROOT)
        self.assertFalse(report.record_accepted)
        self.assertIn(
            "problem-context-unreadable", {issue.code for issue in report.issues}
        )

    def test_unpaired_surrogate_has_explicit_scalar_diagnostic(self) -> None:
        report = validate_path(
            ROOT / "fixtures-v0.2.4" / "unpaired-surrogate.json",
            self.schema_path,
            ROOT,
        )
        self.assertIn(
            "canonical-unicode-scalar", {issue.code for issue in report.issues}
        )
        self.assertFalse(report.record_accepted)

    def test_malformed_envelope_precedes_unknown_spec_classification(self) -> None:
        case_root = ROOT / "artifacts-v0.2.4" / "closure-classification"
        case_manifest = load_json(case_root / "manifest.json")
        expected_statuses = case_manifest["expected_status"]
        self.assertGreaterEqual(len(expected_statuses), 16)
        self.assertIn(FAIL, set(expected_statuses.values()))
        self.assertIn(UNKNOWN, set(expected_statuses.values()))
        for name, expected in expected_statuses.items():
            with self.subTest(case=name):
                path = case_root / f"{name}.json"
                reference = f"sha256:{sha256_bytes(path.read_bytes())}"
                closure = _artifact_closure({"run-spec": reference}, self.store)
                self.assertEqual(closure.status, expected)

        supported_path = ROOT / "artifacts-v0.2.4" / "run-standard.v0.2.4.json"
        supported_ref = f"sha256:{sha256_bytes(supported_path.read_bytes())}"
        self.assertEqual(
            _artifact_closure({"run-spec": supported_ref}, self.store).status,
            PASS,
        )

    def test_envelope_classification_records_fail_closed_end_to_end(self) -> None:
        for name in (
            "malformed-unsupported-envelope",
            "shape-valid-unsupported-envelope",
        ):
            with self.subTest(fixture=name):
                path = ROOT / "fixtures-v0.2.4" / f"{name}.json"
                record = load_json(path)
                self.assertEqual(_trace_authenticity_status(record, self.store), PASS)
                report = validate_path(path, self.schema_path, ROOT)
                self.assertTrue(report.structural_ok)
                self.assertFalse(report.semantic_ok)
                self.assertFalse(report.record_accepted)

    def test_closure_edge_scope_has_one_normative_judgment(self) -> None:
        spec = load_json(
            ROOT
            / "artifacts-v0.2.4"
            / "artifact-closure-spec.v0.2.4.json"
        )
        judgments = spec["judgments"]
        generic = judgments["GenericEdgeShape"]
        header = judgments["SupportedEnvelopeHeader"]
        supported = judgments["SupportedEdgeRelation"]
        unsupported = judgments["UnsupportedEnvelope"]
        self.assertIn("every edge", generic["quantifier"])
        self.assertIn(
            "artifact_type is present in the current EDGE_RELATIONS domain",
            generic["does_not_require"],
        )
        self.assertIn(
            "envelope.spec_id equals urn:evemisslab:pnp-glc:artifact-closure:0.2.4",
            header["applicable_when"],
        )
        self.assertIn("envelope.version equals 0.2.4", header["predicate"])
        self.assertEqual(
            supported["applicable_iff"],
            "judgments.SupportedEnvelopeHeader holds",
        )
        self.assertIn("unsupported spec_id", supported["not_applicable_when"])
        self.assertEqual(unsupported["result"], UNKNOWN.upper())

        future_path = (
            ROOT
            / "artifacts-v0.2.4"
            / "closure-classification"
            / "shape-valid-unsupported-future-type.json"
        )
        future_ref = f"sha256:{sha256_bytes(future_path.read_bytes())}"
        self.assertEqual(
            _artifact_closure({"run-spec": future_ref}, self.store).status,
            UNKNOWN,
        )

    def test_schema_gate_assignment_conformance(self) -> None:
        cheat = copy.deepcopy(load_json(ROOT / "fixtures-v0.2.4" / "cheat.json"))
        cheat["validation_receipt"]["gates"][
            "advice_generation_pass"
        ] = "not-applicable"
        self.assertFalse(Draft202012Validator(self.schema).is_valid(cheat))

        legit = copy.deepcopy(load_json(ROOT / "fixtures-v0.2.4" / "legit.json"))
        legit["validation_receipt"]["admission_pass"] = False
        legit["validation_receipt"]["final_completion"] = False
        legit["validation_receipt"]["gates"][
            "proof_verification_pass"
        ] = "not-applicable"
        self.assertFalse(Draft202012Validator(self.schema).is_valid(legit))

    def test_all_gate_applicability_mutations_are_schema_rejected(self) -> None:
        checker = Draft202012Validator(self.schema)
        for fixture_name in ("legit", "robust-legit", "neutral-legit"):
            baseline = load_json(
                ROOT / "fixtures-v0.2.4" / f"{fixture_name}.json"
            )
            for gate, current in baseline["validation_receipt"]["gates"].items():
                with self.subTest(fixture=fixture_name, gate=gate):
                    mutated = copy.deepcopy(baseline)
                    mutated["validation_receipt"]["admission_pass"] = False
                    mutated["validation_receipt"]["final_completion"] = False
                    mutated["validation_receipt"]["gates"][gate] = (
                        PASS if current == "not-applicable" else "not-applicable"
                    )
                    self.assertFalse(checker.is_valid(mutated))

        legit = copy.deepcopy(load_json(ROOT / "fixtures-v0.2.4" / "legit.json"))
        legit["validation_receipt"]["admission_pass"] = False
        legit["validation_receipt"]["final_completion"] = False
        legit["validation_receipt"]["gates"]["run_class_nonempty"] = (
            "not-applicable"
        )
        self.assertFalse(Draft202012Validator(self.schema).is_valid(legit))

    def test_prov_derive_regressions_remain_closed(self) -> None:
        for name in ("fabricated-states-999", "fabricated-transition-digest"):
            with self.subTest(name=name):
                path = ROOT / "fixtures-v0.2.4" / f"{name}.json"
                record = load_json(path)
                self.assertEqual(_trace_authenticity_status(record, self.store), PASS)
                self.assertFalse(validate_path(path, self.schema_path, ROOT).record_accepted)

    def test_private_signing_key_is_not_published(self) -> None:
        self.assertEqual(list(ROOT.rglob("*.pem")), [])


if __name__ == "__main__":
    unittest.main()
