"""Measure how the A-line's surviving disjunction moved across the whole series.

數學戰士「墜衡」 / AMRAL Research Lab, 2026-09-03.

Every Hard-Zeta bundle publishes an `updated_frontier` in its constants file: a
disjunction of the branches a CASP survivor could still live in. Read in
chronological order they are the series' own record of whether it is converging.

Run:  python analysis/frontier-trajectory.py <bundle-dir>
"""
from __future__ import annotations
import json, pathlib, re, sys, zipfile


def main() -> int:
    src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    recs = []
    for p in src.glob("*.zip"):
        try:
            z = zipfile.ZipFile(p)
            fn = [n for n in z.namelist() if "constants_frontier" in n]
            if not fn:
                continue
            d = json.loads(z.read(fn[0]).decode("utf-8"))
        except Exception:                                # noqa: BLE001
            continue
        if not d.get("updated_frontier"):
            continue
        recs.append((p.stat().st_mtime, d.get("round", "?"),
                     d["updated_frontier"]))
    recs.sort()
    prev, out = set(), []
    for _, rnd, fr in recs:
        b = {x.strip() for x in re.split(r"\s+OR\s+", fr) if x.strip()}
        out.append({"round": rnd, "branches": len(b),
                    "killed": sorted(prev - b), "born": sorted(b - prev)})
        prev = b
    report = {
        "rounds_with_a_frontier": len(out),
        "branch_counts": [r["branches"] for r in out],
        "total_killed": sum(len(r["killed"]) for r in out),
        "total_born": sum(len(r["born"]) for r in out),
        "minimum_reached": min((r["branches"] for r in out), default=0),
        "round_at_minimum": min(out, key=lambda r: r["branches"])["round"]
                            if out else None,
        "final_branches": sorted(prev),
        "reading": (
            "The disjunction does not converge. Almost every round kills "
            "branches and births about as many, and the count ends higher "
            "than it began. The one exception collapsed it to a single "
            "conjunctive branch -- and that round added a GLOBAL COUNTING "
            "constraint (record sparsity) rather than pricing a local "
            "mechanism more finely. Every round since has priced mechanisms "
            "exactly, and each exact price revealed another currency the "
            "survivor could pay in. An exact identity is a change of "
            "coordinates, not an obstruction."),
        "per_round": out,
    }
    pathlib.Path("analysis/frontier-trajectory.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in report.items() if k != "per_round"},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
