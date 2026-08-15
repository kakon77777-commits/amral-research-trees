"""Check that every mutation drill's anchors still match the current sources.

數學戰士「墜衡」 / AMRAL Research Lab.

A drill plants defects by exact string replacement. If the source is refactored,
an anchor stops matching and the drill silently tests *nothing* for that defect —
it reports `anchor absent`, but only when it is next run, which may be never.

On 2026-08-15 a performance change to `floor_beta` and `phase_credit` broke
**eight anchors across six drills** in one edit. Nothing failed; the drills were
simply no longer aimed at anything. This script is the standing guard, and it is
cheap enough to run after any change to a shared module.

It also reports, per drill, which of its target checks no longer exist — the
other half of the same rot.

Usage:  python code/audit_drill_anchors.py
Exit:   0 if every anchor matches exactly once, 1 otherwise.
"""

from __future__ import annotations

import importlib.util
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE = ROOT / "code"


def load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    rep = {"tool": "audit_drill_anchors.py",
           "subject": "every src*_drill.py in this tree",
           "drills": {}, "counts": {}}
    total = stale = 0

    for path in sorted(CODE.glob("src*_drill.py")):
        try:
            d = load(path)
        except Exception as exc:
            rep["drills"][path.name] = {"error": f"{type(exc).__name__}: {exc}"}
            stale += 1
            continue

        sources = {}
        for attr, src_attr in (("ACCEL_DEFECTS", "ACCEL"),
                               ("ALGEBRA_DEFECTS", "ALGEBRA"),
                               ("TOOL_DEFECTS", "TOOL")):
            holder = getattr(d, src_attr, None)
            if holder is not None and pathlib.Path(holder).exists():
                sources[attr] = pathlib.Path(holder).read_text(encoding="utf-8")

        bad, counted = [], 0
        for attr, text in sources.items():
            for name, target, (old, _new) in getattr(d, attr, []):
                counted += 1
                hits = text.count(old)
                if hits != 1:
                    bad.append({"defect": name, "target": target,
                                "matches": hits,
                                "anchor": old.splitlines()[0][:70]})
        total += counted
        stale += len(bad)
        rep["drills"][path.name] = {"anchors": counted, "stale": bad}

    rep["counts"] = {"drills": len(rep["drills"]), "anchors_checked": total,
                     "anchors_not_matching_exactly_once": stale}
    rep["ok"] = stale == 0
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
