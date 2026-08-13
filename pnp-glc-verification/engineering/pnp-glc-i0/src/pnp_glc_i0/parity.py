"""Uniform streaming PARITY and the deliberately nonuniform table family."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence


def normalize_bits(bits: Iterable[int | bool]) -> tuple[int, ...]:
    normalized = tuple(int(bit) for bit in bits)
    if any(bit not in (0, 1) for bit in normalized):
        raise ValueError("PARITY input must contain only 0/1 values")
    return normalized


@dataclass(frozen=True)
class ParityStep:
    index: int
    input_bit: int
    parity_before: int
    parity_after: int


@dataclass(frozen=True)
class StreamingParityResult:
    answer: int
    steps: tuple[ParityStep, ...]


def stream_parity(bits: Iterable[int | bool]) -> StreamingParityResult:
    """One fixed program with state (i, b) and b <- b XOR x_i."""

    normalized = normalize_bits(bits)
    parity = 0
    trace: list[ParityStep] = []
    for index, bit in enumerate(normalized, start=1):
        before = parity
        parity ^= bit
        trace.append(ParityStep(index, bit, before, parity))
    return StreamingParityResult(answer=parity, steps=tuple(trace))


def verify_prefix_invariant(
    bits: Iterable[int | bool], result: StreamingParityResult
) -> bool:
    normalized = normalize_bits(bits)
    if len(normalized) != len(result.steps):
        return False
    expected = 0
    for index, (bit, step) in enumerate(zip(normalized, result.steps), start=1):
        before = expected
        expected ^= bit
        if step != ParityStep(index, bit, before, expected):
            return False
    return result.answer == expected


@dataclass(frozen=True)
class TruthTableFamily:
    """One materialized table per input length: forall n exists A_n."""

    n: int
    answers: bytes

    @classmethod
    def build(cls, n: int, *, materialization_limit: int = 20) -> "TruthTableFamily":
        if n < 0:
            raise ValueError("n must be non-negative")
        if n > materialization_limit:
            raise ValueError(
                f"refusing to materialize 2^{n} entries; limit={materialization_limit}"
            )
        values = bytearray()
        for bits in product((0, 1), repeat=n):
            values.append(sum(bits) & 1)
        return cls(n=n, answers=bytes(values))

    @property
    def advice_bytes(self) -> int:
        return len(self.answers)

    def decide(self, bits: Sequence[int | bool]) -> int:
        normalized = normalize_bits(bits)
        if len(normalized) != self.n:
            raise ValueError(f"expected {self.n} bits, received {len(normalized)}")
        index = 0
        for bit in normalized:
            index = (index << 1) | bit
        return self.answers[index]


def pointwise_table_envelope(
    max_n: int, *, materialization_limit: int = 20
) -> list[dict[str, int]]:
    """Expose exponential construction/advice beside per-query linear decode."""

    if max_n < 0:
        raise ValueError("max_n must be non-negative")
    if max_n > materialization_limit:
        raise ValueError(
            f"refusing envelope through 2^{max_n} entries; limit={materialization_limit}"
        )
    rows: list[dict[str, int]] = []
    for n in range(max_n + 1):
        table = TruthTableFamily.build(n, materialization_limit=materialization_limit)
        rows.append(
            {
                "n": n,
                "programs_for_length": 1,
                "table_entries": 1 << n,
                "advice_bytes": table.advice_bytes,
                "decode_bit_reads_upper_bound": n,
            }
        )
    return rows
