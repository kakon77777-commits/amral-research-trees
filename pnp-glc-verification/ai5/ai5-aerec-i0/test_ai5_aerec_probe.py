from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import ai5_aerec_probe as probe


class ProbeUnitTests(unittest.TestCase):
    def test_compare_expected_checks_only_manifest_fields(self) -> None:
        observed = {"a": 1, "nested": {"b": 2, "extra": 3}, "extra": True}
        self.assertEqual(probe.compare_expected(observed, {"a": 1, "nested": {"b": 2}}), [])
        mismatch = probe.compare_expected(observed, {"nested": {"b": 4}})
        self.assertEqual(mismatch[0]["path"], "$.nested.b")

    def test_smoke_prefix_mixes_positive_and_attack_controls(self) -> None:
        names = {
            "legit",
            "fabricated-states-999",
            "fabricated-transition-digest",
            "2sat-sat",
            "other",
        }
        order = probe.adaptive_fixture_order(names)
        self.assertEqual(order[:4], [
            "legit",
            "fabricated-states-999",
            "fabricated-transition-digest",
            "2sat-sat",
        ])

    def test_history_prioritizes_observed_mismatch_after_smoke_prefix(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
