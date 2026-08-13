from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pnp_glc_i0.semantic_validator import (  # noqa: E402
    ArtifactIndex,
    load_json,
    sha256_bytes,
    validate_path,
)


class SemanticValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema_path = ROOT / "schemas" / "run-record.schema.v0.2.0-candidate.json"
        cls.schema = load_json(cls.schema_path)
        cls.manifest = load_json(ROOT / "fixtures" / "manifest.json")

    def test_schema_metaschema(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_v01_is_bitwise_preserved(self) -> None:
        v01 = ROOT.parent / "run-record.schema.json"
        digest = hashlib.sha256(v01.read_bytes()).hexdigest().upper()
        self.assertEqual(
            digest,
            "3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4",
        )

    def test_fixture_manifest(self) -> None:
        for name, expected in self.manifest["fixtures"].items():
            with self.subTest(fixture=name):
                report = validate_path(
                    ROOT / "fixtures" / f"{name}.json",
                    self.schema_path,
                    ROOT,
                ).to_dict()
                for key, value in expected.items():
                    self.assertEqual(report[key], value, report["issues"])

    def test_schema_implications_are_one_way(self) -> None:
        record = copy.deepcopy(load_json(ROOT / "fixtures" / "legit.json"))
        record["validation_receipt"]["admission_pass"] = False
        record["validation_receipt"]["final_completion"] = False
        validator = Draft202012Validator(self.schema)
        self.assertTrue(validator.is_valid(record))

        report = validate_path(
            ROOT / "fixtures" / "legit.json",
            self.schema_path,
            ROOT,
        )
        self.assertTrue(report.record_accepted)

    def test_receipt_binds_all_required_hashes(self) -> None:
        record = load_json(ROOT / "fixtures" / "legit.json")
        receipt = record["validation_receipt"]
        for key in (
            "schema_sha256",
            "validator_sha256",
            "projection_spec_sha256",
            "candidate_projection_sha256",
            "trace_sha256",
        ):
            self.assertRegex(receipt[key], r"^(sha256:)?[0-9a-f]{64}$")
        self.assertIn(receipt["trace_sha256"], receipt["resolved_evidence_hashes"])

    def test_artifact_index_pins_hash_parse_use_bytes(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.json"
            original = b'{"version":1}'
            path.write_bytes(original)
            index = ArtifactIndex(Path(directory))
            reference = f"sha256:{sha256_bytes(original)}"
            path.write_bytes(b'{"version":2}')
            self.assertTrue(index.contains(reference))
            self.assertEqual(index.load_json(reference), {"version": 1})


if __name__ == "__main__":
    unittest.main()
