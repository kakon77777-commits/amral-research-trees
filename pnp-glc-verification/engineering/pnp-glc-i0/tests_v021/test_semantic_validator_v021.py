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

from pnp_glc_i0.semantic_validator_v021 import (  # noqa: E402
    FAIL,
    PASS,
    ArtifactIndex,
    _artifact_closure,
    _direct_receipt_reference_set,
    _replay_trace,
    _resource_derivation_status,
    _trace_authenticity_status,
    _transition_execution_status,
    canonical_json_bytes,
    load_json,
    sha256_bytes,
    validate_path,
)


class SemanticValidatorV021Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema_path = (
            ROOT / "schemas" / "run-record.schema.v0.2.1-candidate.json"
        )
        cls.schema = load_json(cls.schema_path)
        cls.manifest = load_json(ROOT / "fixtures-v0.2.1" / "manifest.json")
        cls.store = ArtifactIndex(ROOT)

    def test_schema_metaschema(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_frozen_predecessors_are_bitwise_preserved(self) -> None:
        expected = {
            ROOT.parent / "run-record.schema.json":
                "3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4",
            ROOT / "schemas" / "run-record.schema.v0.2.0-candidate.json":
                "1AD5AFA3A76E56AD5C9D0B79DF34B897E337606093D282693932085BF1AF297C",
            ROOT / "src" / "pnp_glc_i0" / "semantic_validator.py":
                "4C50BE9EF563644BC29F3DCEEFB9D9205056631847980FCC763D1E4BA25EB771",
            ROOT / "artifacts" / "candidate-projection-spec.v0.2.0.json":
                "9966B86DBC3884E3327306FF1FEFAF21EFBDE705EE0F10739755BE27C73A1991",
        }
        for path, digest in expected.items():
            with self.subTest(path=path.name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest().upper(), digest)

    def test_fixture_manifest(self) -> None:
        for name, expected in self.manifest["fixtures"].items():
            with self.subTest(fixture=name):
                report = validate_path(
                    ROOT / "fixtures-v0.2.1" / f"{name}.json",
                    self.schema_path,
                    ROOT,
                ).to_dict()
                for key, value in expected.items():
                    self.assertEqual(report[key], value, report["issues"])

    def test_prov_derive_fabricated_states_is_not_derived(self) -> None:
        record = load_json(ROOT / "fixtures-v0.2.1" / "fabricated-states-999.json")
        trace = self.store.load_json(record["validation_receipt"]["trace_sha256"])
        authenticity = _trace_authenticity_status(record, self.store)
        replay = _replay_trace(record, trace, self.store)
        self.assertEqual(authenticity, PASS)
        self.assertTrue(replay.ok, "attack intentionally preserves mirror replay")
        self.assertEqual(_transition_execution_status(record), PASS)
        self.assertEqual(
            _resource_derivation_status(record, trace, replay, authenticity), FAIL
        )
        self.assertFalse(
            validate_path(
                ROOT / "fixtures-v0.2.1" / "fabricated-states-999.json",
                self.schema_path,
                ROOT,
            ).record_accepted
        )

    def test_prov_derive_fabricated_transition_is_not_executable(self) -> None:
        record = load_json(
            ROOT / "fixtures-v0.2.1" / "fabricated-transition-digest.json"
        )
        trace = self.store.load_json(record["validation_receipt"]["trace_sha256"])
        authenticity = _trace_authenticity_status(record, self.store)
        replay = _replay_trace(record, trace, self.store)
        self.assertEqual(authenticity, PASS)
        self.assertTrue(replay.ok, "attack intentionally preserves mirror replay")
        self.assertEqual(_transition_execution_status(record), FAIL)
        self.assertEqual(
            _resource_derivation_status(record, trace, replay, authenticity), PASS
        )
        self.assertFalse(
            validate_path(
                ROOT / "fixtures-v0.2.1" / "fabricated-transition-digest.json",
                self.schema_path,
                ROOT,
            ).record_accepted
        )

    def test_bad_signature_is_not_a_producer_string_check(self) -> None:
        record = load_json(ROOT / "fixtures-v0.2.1" / "bad-trace-signature.json")
        trace = self.store.load_json(record["validation_receipt"]["trace_sha256"])
        self.assertEqual(trace["producer"], "pnp-glc-i0-capability-sandbox")
        self.assertEqual(_trace_authenticity_status(record, self.store), FAIL)

    def test_transitive_closure_reaches_missing_child(self) -> None:
        record = load_json(ROOT / "fixtures-v0.2.1" / "missing-transitive-ref.json")
        closure = _artifact_closure(_direct_receipt_reference_set(record), self.store)
        self.assertEqual(closure.status, FAIL)
        self.assertIn("f" * 64, closure.references)

    def test_canonical_equivalent_newline_spellings_have_one_output(self) -> None:
        short_escape = json.loads('"\\n"')
        unicode_escape = json.loads('"\\u000a"')
        self.assertEqual(short_escape, unicode_escape)
        self.assertEqual(canonical_json_bytes(short_escape), b'"\\n"')
        self.assertEqual(canonical_json_bytes(short_escape), canonical_json_bytes(unicode_escape))

    def test_schema_implications_remain_one_way(self) -> None:
        record = copy.deepcopy(load_json(ROOT / "fixtures-v0.2.1" / "legit.json"))
        record["validation_receipt"]["admission_pass"] = False
        record["validation_receipt"]["final_completion"] = False
        self.assertTrue(Draft202012Validator(self.schema).is_valid(record))

    def test_artifact_index_uses_one_pinned_snapshot(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.json"
            original = b'{"version":1}'
            path.write_bytes(original)
            index = ArtifactIndex(Path(directory))
            reference = f"sha256:{sha256_bytes(original)}"
            path.write_bytes(b'{"version":2}')
            self.assertTrue(index.contains(reference))
            self.assertEqual(index.load_json(reference), {"version": 1})

    def test_private_signing_key_is_not_published(self) -> None:
        self.assertEqual(list(ROOT.rglob("*.pem")), [])


if __name__ == "__main__":
    unittest.main()
