from __future__ import annotations

import sys
import unittest
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pnp_glc_i0.oracles import parity_oracle  # noqa: E402
from pnp_glc_i0.parity import (  # noqa: E402
    TruthTableFamily,
    pointwise_table_envelope,
    stream_parity,
    verify_prefix_invariant,
)


class ParityTests(unittest.TestCase):
    def test_uniform_stream_and_local_invariant(self) -> None:
        for n in range(11):
            for bits in product((0, 1), repeat=n):
                result = stream_parity(bits)
                self.assertTrue(parity_oracle(bits, result.answer))
                self.assertTrue(verify_prefix_invariant(bits, result))

    def test_truth_table_agrees_but_exposes_exponential_advice(self) -> None:
        for n in range(9):
            table = TruthTableFamily.build(n)
            self.assertEqual(table.advice_bytes, 1 << n)
            for bits in product((0, 1), repeat=n):
                self.assertTrue(parity_oracle(bits, table.decide(bits)))

    def test_pointwise_envelope_keeps_construction_visible(self) -> None:
        rows = pointwise_table_envelope(8)
        self.assertEqual([row["advice_bytes"] for row in rows], [1 << n for n in range(9)])
        self.assertEqual([row["decode_bit_reads_upper_bound"] for row in rows], list(range(9)))

    def test_materialization_limit_is_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            TruthTableFamily.build(21)
        with self.assertRaises(ValueError):
            pointwise_table_envelope(21)


if __name__ == "__main__":
    unittest.main()
