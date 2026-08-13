from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import ai5_aerec_probe_v023 as probe


class ProbeV023UnitTests(unittest.TestCase):
    def test_compare_expected_checks_only_manifest_fields(self) -> None:
        observed = {"a": 1, "nested": {"b": 2, "extra": 3}, "extra": True}
        self.assertEqual(
            probe.compare_expected(observed, {"a": 1, "nested": {"b": 2}}),
            [],
        )
        mismatch = probe.compare_expected(observed, {"nested": {"b": 4}})
        self.assertEqual(mismatch[0]["path"], "$.nested.b")

    def test_manifest_parser_accepts_exact_format(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SHA256SUMS.txt"
            digest = hashlib.sha256(b"x").hexdigest().upper()
            path.write_text(f"{digest}  item.txt\n", encoding="utf-8")
            self.assertEqual(probe.parse_checksum_manifest(path), [("item.txt", digest)])

    def test_manifest_parser_rejects_ambiguous_spacing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SHA256SUMS.txt"
            digest = hashlib.sha256(b"x").hexdigest().upper()
            path.write_text(f"{digest} item.txt\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                probe.parse_checksum_manifest(path)

    def test_smoke_prefix_has_accept_and_reject_controls(self) -> None:
        names = set(probe.SMOKE_PREFIX)
        order = probe.adaptive_fixture_order(names)
        self.assertEqual(order, probe.SMOKE_PREFIX)
        self.assertIn("legit", order)
        self.assertIn("receipt-ref-substitution", order)
        self.assertIn("malformed-unsupported-envelope", order)

    def test_history_prioritizes_observed_mismatch_after_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            history = Path(directory) / "history.json"
            history.write_text(json.dumps({
                "fixtures": {
                    "alpha": {
                        "matches_expectation": True,
                        "timing_ns": {"median": 100},
                    },
                    "omega": {
                        "matches_expectation": False,
                        "timing_ns": {"median": 100},
                    },
                }
            }), encoding="utf-8")
            order = probe.adaptive_fixture_order({"alpha", "omega"}, [history])
            self.assertEqual(order, ["omega", "alpha"])

    def test_nearest_rank_percentile(self) -> None:
        self.assertEqual(probe.percentile_nearest_rank([1, 2, 3, 4, 5], 0.95), 5)

    def test_v023_frozen_blocker_is_not_misreported_as_acceptance_bypass(self) -> None:
        blocker = probe.KNOWN_FROZEN_BLOCKER
        self.assertEqual(blocker["id"], "CLOSURE-EDGE-SCOPE-01")
        self.assertEqual(blocker["disposition"], "FAIL")
        self.assertFalse(blocker["implementation_acceptance_bypass"])
        self.assertFalse(blocker["p_np_implication"])


if __name__ == "__main__":
    unittest.main()
