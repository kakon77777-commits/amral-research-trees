"""Recompute the frozen 1500-case ledger and compare exact report bytes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    from pnp_glc_i0.experiment_v026 import _two_sat_crosscheck

    report = json.loads(
        (root / "i0-run-report.v0.2.6-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    frozen = report["two_sat"]["deterministic_crosscheck"]
    replay = _two_sat_crosscheck(
        seed=frozen["seed"],
        variable_counts=frozen["variable_counts"],
        cases_per_variable_count=frozen["cases_per_variable_count"],
    )
    checks = {
        "exact_crosscheck_object": replay == frozen,
        "frozen_total_cases_is_1500": frozen["total_cases"] == 1500,
        "six_by_250_ledger": (
            len(frozen["strata"]) == 6
            and all(item["cases"] == 250 for item in frozen["strata"])
        ),
        "frozen_seed_is_explicit": frozen["seed"] == 20260809,
        "frozen_result_passes": frozen["all_pass"] is True,
        "generation_command_is_explicit": (
            "--two-sat-crosscheck-seed 20260809"
            in report["frozen_evidence_scope"]["generation_command"]
        ),
        "evidence_location_is_explicit": (
            report["frozen_evidence_scope"]["two_sat_crosscheck_json_pointer"]
            == "/two_sat/deterministic_crosscheck"
        ),
    }
    unexpected = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "all_conformant": not unexpected,
                "checks": checks,
                "classification": "Experiment replay / frozen evidence scope",
                "p_np_claim": False,
                "total_cases_replayed": replay["total_cases"],
                "unexpected": unexpected,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
