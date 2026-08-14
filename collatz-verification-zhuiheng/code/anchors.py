"""External anchor check: this engine against published OEIS data.

數學戰士「墜衡」 / AMRAL Research Lab.

Why this file exists
--------------------
An engine checked only against another program I wrote is checked against my
own assumptions. The two record sequences below were computed by other people,
by other methods, decades apart, and are archived here as byte-exact snapshots
with digests. If this engine has a systematic error in how it iterates, counts
steps, or tracks the maximum, the comparison against them breaks.

  A006877 / A006878  record-setting starts, and their delays, for the number of
                     steps of the standard map C to reach 1
  A006884 / A006885  record-setting starts, and their values, for the highest
                     point of the C-trajectory before reaching 1

The comparison is exact and two-sided: every published record at or below the
tested bound must appear in the engine's output with the same value, and the
engine must not emit any record the published list does not have.

Usage:  python code/anchors.py [bound]
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTERNAL = ROOT / "data" / "external"
# COLLATZ_BIN lets the mutation drill point this same check at a deliberately
# broken build without editing it.
BINARY = pathlib.Path(os.environ.get("COLLATZ_BIN", ROOT / "build" / "collatz_verify.exe"))

SOURCES = {
    "A006877": "https://oeis.org/A006877/b006877.txt",
    "A006878": "https://oeis.org/A006878/b006878.txt",
    "A006884": "https://oeis.org/A006884/b006884.txt",
    "A006885": "https://oeis.org/A006885/b006885.txt",
}


def load_bfile(name: str) -> tuple[list[int], str]:
    """Return (values indexed from the b-file's own first index, sha256)."""
    path = EXTERNAL / f"b{name[1:]}.txt"
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    values: list[int] = []
    for line in raw.decode("utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"{path.name}: unparsable line {line!r}")
        values.append(int(parts[1]))
    if not values:
        raise ValueError(f"{path.name}: no data lines")
    return values, digest


def run_records(bound: int) -> dict:
    if not BINARY.exists():
        raise SystemExit(f"engine not built: {BINARY}")
    proc = subprocess.run(
        [str(BINARY), "--records", str(bound), "--threads", "16"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(proc.stdout)


def compare(kind: str, engine: list[list[int]], starts: list[int], vals: list[int],
            bound: int) -> dict:
    # The two b-files of a pair are maintained separately and are not always
    # extended in step: as snapshotted, A006884 has 98 terms and A006885 has 97.
    # Only the paired prefix is usable, and the drop is reported rather than
    # absorbed by zip().
    paired = min(len(starts), len(vals))
    published = [(s, v) for s, v in zip(starts[:paired], vals[:paired]) if s <= bound]
    produced = [(int(a), int(b)) for a, b in engine if int(a) <= bound]
    if not published:
        raise SystemExit(
            f"{kind}: no published record lies at or below bound {bound}; the "
            f"comparison would be vacuous. Raise the bound."
        )
    missing = [p for p in published if p not in produced]
    extra = [p for p in produced if p not in published]
    return {
        "kind": kind,
        "bound": bound,
        "snapshot_terms": {"starts": len(starts), "values": len(vals), "paired_used": paired},
        "published_compared": len(published),
        "engine_produced": len(produced),
        "largest_compared_start": published[-1][0],
        "missing_from_engine": missing[:20],
        "not_in_published_list": extra[:20],
        "match": not missing and not extra,
    }


def main() -> int:
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000_000

    digests = {}
    delay_starts, digests["A006877"] = load_bfile("A006877")
    delay_vals, digests["A006878"] = load_bfile("A006878")
    peak_starts, digests["A006884"] = load_bfile("A006884")
    peak_vals, digests["A006885"] = load_bfile("A006885")

    res = run_records(bound)
    if not res.get("ok"):
        raise SystemExit(f"engine run failed: {res}")

    checks = [
        compare("delay_records", res["delay_records"], delay_starts, delay_vals, bound),
        compare("peak_records", res["peak_records"], peak_starts, peak_vals, bound),
    ]
    report = {
        "tool": "anchors.py",
        "bound": bound,
        "engine_elapsed_s": res["elapsed_s"],
        "sources": SOURCES,
        "snapshot_sha256": digests,
        "checks": checks,
        "all_match": all(c["match"] for c in checks),
    }
    print(json.dumps(report, indent=2))
    return 0 if report["all_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
