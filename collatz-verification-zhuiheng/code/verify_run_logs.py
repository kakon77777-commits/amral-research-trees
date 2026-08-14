"""Aggregate the chunk logs into one claim — and refuse to if they do not tile.

數學戰士「墜衡」 / AMRAL Research Lab.

The engine verifies intervals. A statement about [3, N] exists only if the
archived chunk logs cover [3, N] with no gap and no overlap, every chunk exited
clean, and the per-chunk counts add up to the number of odd starts that
interval actually contains. This script is what turns a directory of logs into
that statement, and it is meant to be the thing that says no.

It reads only the archived logs. It does not re-run the engine, so it cannot
launder a missing chunk into a covered one.

Usage:  python code/verify_run_logs.py [--tag t40] [--expect-to N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "raw-logs"


def odd_starts_in(lo: int, hi: int) -> int:
    """Count of odd n with max(lo, 3) <= n <= hi."""
    lo = max(lo, 3)
    if hi < lo:
        return 0
    return (hi + 1) // 2 - lo // 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="t40")
    ap.add_argument("--expect-to", type=int, default=None)
    args = ap.parse_args()

    problems: list[str] = []
    chunks = []
    for path in sorted(LOGS.glob(f"{args.tag}_chunk*.out.log")):
        raw = path.read_bytes()
        text = raw.decode("utf-8").strip()
        if not text:
            problems.append(f"{path.name}: empty; the chunk did not produce a result")
            continue
        try:
            rec = json.loads(text)
        except json.JSONDecodeError as exc:
            problems.append(f"{path.name}: unparsable ({exc})")
            continue
        err_path = path.with_name(path.name.replace(".out.log", ".err.log"))
        stderr_bytes = err_path.stat().st_size if err_path.exists() else 0
        rec["_file"] = path.name
        rec["_sha256"] = hashlib.sha256(raw).hexdigest()
        rec["_stderr_bytes"] = stderr_bytes
        chunks.append(rec)
        if stderr_bytes:
            problems.append(f"{path.name}: companion stderr log is non-empty")

    if not chunks:
        print(json.dumps({"ok": False, "error": f"no chunk logs matched tag {args.tag!r}"}))
        return 1

    for c in chunks:
        if not c.get("ok"):
            problems.append(f"{c['_file']}: run reported ok=false")
        if c.get("failures"):
            problems.append(f"{c['_file']}: failures {c['failures']}")
        if c["resolved_by_one_k_step_jump"] + c["needed_iteration"] != c["odd_starts_checked"]:
            problems.append(f"{c['_file']}: sieve/iteration split does not sum to the total")
        want = odd_starts_in(c["from"], c["to"])
        if c["odd_starts_checked"] != want:
            problems.append(
                f"{c['_file']}: checked {c['odd_starts_checked']} odd starts, "
                f"but [{c['from']}, {c['to']}] contains {want}"
            )

    chunks.sort(key=lambda c: c["from"])
    if chunks[0]["from"] != 3:
        problems.append(f"coverage starts at {chunks[0]['from']}, not 3")
    for a, b in zip(chunks, chunks[1:]):
        if b["from"] != a["to"] + 1:
            gap = "gap" if b["from"] > a["to"] + 1 else "overlap"
            problems.append(
                f"{gap} between {a['_file']} (to {a['to']}) and {b['_file']} (from {b['from']})"
            )

    covered_to = chunks[-1]["to"]
    if args.expect_to is not None and covered_to != args.expect_to:
        problems.append(f"coverage ends at {covered_to}, expected {args.expect_to}")

    total_checked = sum(c["odd_starts_checked"] for c in chunks)
    want_total = odd_starts_in(3, covered_to)
    if total_checked != want_total:
        problems.append(f"total odd starts {total_checked} != {want_total} for [3, {covered_to}]")

    ks = sorted({c["sieve_k"] for c in chunks})
    best_sigma = max(chunks, key=lambda c: (c["max_sigma"], -c["max_sigma_at"]))
    # exact rational comparison; peak and n both run past the range where float
    # division would still be telling the truth
    best_exp = max(chunks, key=lambda c: Fraction(c["max_expansion_peak"], c["max_expansion_at"]))

    report = {
        "tool": "verify_run_logs.py",
        "tag": args.tag,
        "chunks": len(chunks),
        "covered_interval": [3, covered_to],
        "tiles_without_gap_or_overlap": not any(
            "gap" in p or "overlap" in p or "coverage starts" in p for p in problems
        ),
        "odd_starts_checked": total_checked,
        "odd_starts_expected": want_total,
        "resolved_by_one_k_step_jump": sum(c["resolved_by_one_k_step_jump"] for c in chunks),
        "needed_iteration": sum(c["needed_iteration"] for c in chunks),
        "sieve_k_values_used": ks,
        "total_engine_seconds": round(sum(c["elapsed_s"] for c in chunks), 3),
        "max_sigma": {"value": best_sigma["max_sigma"], "at": best_sigma["max_sigma_at"]},
        "max_expansion": {
            "peak": best_exp["max_expansion_peak"],
            "at": best_exp["max_expansion_at"],
            "ratio_approx": float(
                Fraction(best_exp["max_expansion_peak"], best_exp["max_expansion_at"])
            ),
        },
        "log_sha256": {c["_file"]: c["_sha256"] for c in chunks},
        "problems": problems,
        "ok": not problems,
    }
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
