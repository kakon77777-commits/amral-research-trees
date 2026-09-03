"""Verify coverage and aggregate claims encoded in the archived run logs."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path


TREE_ROOT = Path(__file__).resolve().parent.parent
LOGS = TREE_ROOT / "data" / "raw-logs"


def read(name: str) -> str:
    raw = (LOGS / name).read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    return raw.decode("utf-8", errors="replace")


def value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}=(.+?)\s*$", text)
    if not match:
        raise AssertionError(f"missing {key}")
    return match.group(1)


def integer(text: str, key: str) -> int:
    return int(value(text, key).replace(",", ""))


def pair(text: str, key: str) -> tuple[int, int]:
    match = re.fullmatch(r"\[(\d+),(\d+)\]", value(text, key))
    if not match:
        raise AssertionError(f"malformed {key}")
    return int(match.group(1)), int(match.group(2))


def verify_log_hashes() -> int:
    manifest = (LOGS / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected: dict[str, str] = {}
    for line in manifest:
        digest, name = line.split(" *", 1)
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert name not in expected
        expected[name] = digest
    actual_names = {path.name for path in LOGS.glob("*.log")}
    assert set(expected) == actual_names
    for name, digest in expected.items():
        observed = hashlib.sha256((LOGS / name).read_bytes()).hexdigest()
        assert observed == digest, name
    return len(expected)


def verify_direct_k64() -> dict[str, int]:
    specs = [
        ("q3000.log", (1, 3000)),
        ("q3001_4243.out.log", (3001, 4243)),
        ("q4244_5196_v2.out.log", (4244, 5196)),
        ("q5197_6000_v2.log", (5197, 6000)),
    ]
    totals = {
        "anchors": 0,
        "eligible_fibers": 0,
        "fiber_entries": 0,
        "retained_differences": 0,
        "quad_support_updates": 0,
    }
    covered: set[int] = set()
    for name, (lo, hi) in specs:
        text = read(name)
        assert "STATUS=NO_K64" in text
        for q in range(lo, hi + 1):
            assert q not in covered
            covered.add(q)
        for key in totals:
            totals[key] += integer(text, key)
    assert covered == set(range(1, 6001))
    assert totals == {
        "anchors": 18_003_000,
        "eligible_fibers": 14_040_082,
        "fiber_entries": 209_917_507,
        "retained_differences": 465_004,
        "quad_support_updates": 767_726,
    }
    return totals


def signed_log_names() -> list[str]:
    return [
        "signed_scaled_p1_12_c1_100.out.log",
        "signed_scaled_p13_24_c1_100.out.log",
        "signed_scaled_p25_36_c1_100.out.log",
        "signed_scaled_p37_48_c1_100.out.log",
        "signed_scaled_p49_60_c1_100.out.log",
        "signed_scaled_p61_71_c1_100.out.log",
        "signed_scaled_p1_9_c101_1000.out.log",
        "signed_scaled_p10_18_c101_1000.out.log",
        "signed_scaled_p19_27_c101_1000.out.log",
        "signed_scaled_p28_36_c101_1000.out.log",
        "signed_scaled_p37_45_c101_1000.out.log",
        "signed_scaled_p46_54_c101_1000.out.log",
        "signed_scaled_p55_63_c101_1000.out.log",
        *[f"signed_scaled_packet{i}_c101_1000.out.log" for i in range(64, 72)],
    ]


def verify_signed_scaling() -> dict[str, int]:
    totals = {
        "packet_multiplier_pairs": 0,
        "factor_divisors_enumerated": 0,
        "signed_closure_entries": 0,
        "expected_inherited_entries": 0,
    }
    covered: set[tuple[int, int]] = set()
    for name in signed_log_names():
        text = read(name)
        assert "STATUS=NO_SIGNED_SCALAR_INDUCED_ERDOS885_K5_IN_RANGE" in text
        p0, p1 = pair(text, "packet_range")
        c0, c1 = pair(text, "scale_range")
        for packet in range(p0, p1 + 1):
            for scale in range(c0, c1 + 1):
                key = packet, scale
                assert key not in covered
                covered.add(key)
        for key in totals:
            totals[key] += integer(text, key)
    assert covered == {(packet, scale) for packet in range(1, 72) for scale in range(1, 1001)}
    assert totals == {
        "packet_multiplier_pairs": 71_000,
        "factor_divisors_enumerated": 847_896_082,
        "signed_closure_entries": 284_000,
        "expected_inherited_entries": 284_000,
    }

    extension = read("signed_scaled_packet2_c1001_10000.out.log")
    assert "STATUS=NO_SIGNED_SCALAR_INDUCED_ERDOS885_K5_IN_RANGE" in extension
    assert pair(extension, "packet_range") == (2, 2)
    assert pair(extension, "scale_range") == (1001, 10000)
    assert integer(extension, "packet_multiplier_pairs") == 9_000
    assert integer(extension, "signed_closure_entries") == 36_000
    assert integer(extension, "expected_inherited_entries") == 36_000
    return totals


def verify_choudhry_box() -> dict[str, int | str]:
    text = read("choudhry_b6.out.log")
    assert "STATUS=NO_5x5_CANDIDATE_IN_PARAMETER_BOX" in text
    result: dict[str, int | str] = {
        "total_parameter_tuples": integer(text, "total_parameter_tuples"),
        "valid_packets": integer(text, "valid_packets"),
        "unique_normalized_packets": integer(text, "unique_normalized_packets"),
        "best_positive_shift_closure": integer(text, "best_positive_shift_closure"),
        "normalized_packet_digest_sha256": value(text, "normalized_packet_digest_sha256"),
    }
    assert result == {
        "total_parameter_tuples": 279_936,
        "valid_packets": 116_720,
        "unique_normalized_packets": 10_777,
        "best_positive_shift_closure": 2,
        "normalized_packet_digest_sha256": "a608ddd86568bcdfd303a2c1497935444a740b142446d641da6fc5729d9a0ae3",
    }
    return result


def main() -> None:
    summary = {
        "status": "PASS",
        "raw_log_sha256_files": verify_log_hashes(),
        "direct_k6_4_q_le_6000": verify_direct_k64(),
        "signed_scaling_all_71_c_le_1000": verify_signed_scaling(),
        "choudhry_positive_box_1_to_6": verify_choudhry_box(),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
