from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pnp_glc_i0.oracles import (  # noqa: E402
    assignment_satisfies_2sat,
    exhaustive_2sat,
    verify_unsat_certificate,
)
from pnp_glc_i0.two_sat import solve_2sat  # noqa: E402


class TwoSatTests(unittest.TestCase):
    def test_sat_assignment_oracle(self) -> None:
        clauses = [(1, 2), (-1, 2), (-2, 3)]
        result = solve_2sat(3, clauses)
        self.assertEqual(result.status, "sat")
        self.assertIsNotNone(result.assignment)
        self.assertTrue(assignment_satisfies_2sat(clauses, result.assignment or {}))

    def test_unsat_path_certificate(self) -> None:
        clauses = [(1, 1), (-1, -1)]
        result = solve_2sat(1, clauses)
        self.assertEqual(result.status, "unsat")
        self.assertTrue(
            verify_unsat_certificate(
                clauses,
                result.unsat_variable or 0,
                result.positive_to_negative,
                result.negative_to_positive,
            )
        )

    def test_random_small_instances_match_exhaustive_oracle(self) -> None:
        rng = random.Random(20260809)
        for variable_count in range(1, 7):
            literals = [
                literal
                for variable in range(1, variable_count + 1)
                for literal in (variable, -variable)
            ]
            for _ in range(250):
                clauses = [
                    (rng.choice(literals), rng.choice(literals))
                    for _ in range(rng.randrange(0, 3 * variable_count + 1))
                ]
                result = solve_2sat(variable_count, clauses)
                exhaustive = exhaustive_2sat(variable_count, clauses)
                self.assertEqual(result.status == "sat", exhaustive is not None)

    def test_invalid_literal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            solve_2sat(2, [(0, 1)])
        with self.assertRaises(ValueError):
            solve_2sat(2, [(1, 3)])


if __name__ == "__main__":
    unittest.main()
