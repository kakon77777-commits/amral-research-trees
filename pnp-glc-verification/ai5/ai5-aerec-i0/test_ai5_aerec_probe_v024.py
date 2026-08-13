from __future__ import annotations

import unittest
from pathlib import Path

import ai5_aerec_probe_v024 as probe


class ProbeV024UnitTests(unittest.TestCase):
    def test_profile_pins_v024_validator_and_manifest(self) -> None:
        self.assertEqual(probe.PROFILE["candidate_version"], "0.2.4")
        self.assertEqual(
            probe.PINNED_CORE[probe.PROFILE["validator_relative"]],
            "B744C9C20C510FE39F132E0DFB4AAC50E6E3E573B48B7F1AE19494F5D5195FED",
        )
        self.assertIn("SHA256SUMS-v0.2.4-candidate.txt", probe.PINNED_MANIFEST_SHA256)

    def test_smoke_prefix_contains_positive_and_new_negative_controls(self) -> None:
        self.assertEqual(probe.SMOKE_PREFIX[0], "legit")
        self.assertIn("2sat-sat", probe.SMOKE_PREFIX)
        self.assertEqual(len(probe.ORACLE_DECLARATION_NEGATIVES), 9)
        self.assertIn(
            "parity-with-2sat-oracle-obligations-only",
            probe.ORACLE_DECLARATION_NEGATIVES,
        )

    def test_configure_engine_is_version_profile_only(self) -> None:
        probe.configure_engine()
        self.assertEqual(probe.engine.CANDIDATE_VERSION, "0.2.4")
        self.assertEqual(
            probe.engine.FIXTURE_DIRECTORY,
            "fixtures-v0.2.4",
        )
        self.assertIs(
            probe.engine.explicit_regression_probes,
            probe.explicit_regression_probes_v024,
        )

    def test_local_profile_does_not_claim_independent_acceptance(self) -> None:
        source = Path(probe.engine.__file__).read_text(encoding="utf-8")
        self.assertIn('"independent_acceptance_observed": False', source)
        self.assertIn('"promotion_allowed": False', source)

    def test_scope_audit_requires_normative_symbol_closure(self) -> None:
        source = Path(probe.__file__).read_text(encoding="utf-8")
        self.assertIn('"CLOSURE-JUDGMENT-COMPLETENESS-01"', source)
        self.assertIn(
            '"generic-envelope-judgment-defined": "GenericEnvelopeShape" in judgments',
            source,
        )

    def test_late_advice_blocker_forces_no_change(self) -> None:
        blocker = probe.EXTERNAL_DISPOSITION_BLOCKERS[0]
        self.assertEqual(blocker["id"], "ADVICE-DECL-LEDGER-01")
        self.assertEqual(blocker["disposition"], "FAIL")
        self.assertFalse(blocker["frozen_manifest_fixture_present"])


if __name__ == "__main__":
    unittest.main()
