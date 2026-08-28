"""Check that every mutation drill's anchors still match the current sources.

數學戰士「墜衡」 / AMRAL Research Lab.

A drill plants defects by exact string replacement. If the source is refactored,
an anchor stops matching and the drill silently tests *nothing* for that defect —
it reports `anchor absent`, but only when it is next run, which may be never.

On 2026-08-15 a performance change to `floor_beta` and `phase_credit` broke
**eight anchors across six drills** in one edit. Nothing failed; the drills were
simply no longer aimed at anything. This script is the standing guard, and it is
cheap enough to run after any change to a shared module.

On 2026-08-28 the guard turned out to have the disease it was written to catch.
It knew three defect-list shapes — `ACCEL_DEFECTS`, `ALGEBRA_DEFECTS` and
`TOOL_DEFECTS`, each paired with a module attribute of the same stem. Every drill
from `src22` onward declares `DEFECTS` against `GATE` instead, a four-element
tuple rather than three. So this audit read **zero anchors for 16 of 31 drills**,
the whole of the current sweep among them, and reported `ok: true` while auditing
nothing for half its subjects.

Two changes follow from that. The shapes are now discovered rather than listed,
and a drill that yields no auditable anchors and no reason why makes this script
**refuse**. A guard that cannot say how much it covered is not a guard; its own
zero was the finding, exactly as `measure-what-the-check-ignores` says.

Some defects genuinely cannot be audited here: a few early drills mutate through
a callable, or tag a file elsewhere in the tree instead of replacing a string.
Those are counted and named, not silently dropped.

Usage:  python code/audit_drill_anchors.py
Exit:   0 if every anchor matches exactly once and every drill is accounted for.
"""

from __future__ import annotations

import importlib.util
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE = ROOT / "code"
SOURCE_ATTRS = ("GATE", "TOOL", "SOURCE", "ALGEBRA", "ACCEL")


def load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sources_of(mod) -> dict[str, str]:
    """Every file this drill could be mutating, by the attribute naming it."""
    out = {}
    for attr in SOURCE_ATTRS:
        value = getattr(mod, attr, None)
        if value is None:
            continue
        try:
            path = pathlib.Path(value)
        except TypeError:
            continue
        if path.is_file():
            try:
                out[attr] = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
    return out


def anchor_of(item) -> tuple[str | None, str | None]:
    """The string a defect replaces, or why there is not one.

    Two generations of drill live in this tree:
      * `(name, old, new, expected)`         -- src22 onward, the current shape
      * `(name, target, (old, new))`         -- src07..src21
    and two kinds that do not replace a string in a source file at all.
    """
    if len(item) == 4 and all(isinstance(x, str) for x in item):
        return item[1], None
    if len(item) == 3:
        third = item[2]
        if isinstance(third, tuple) and third and isinstance(third[0], str):
            return third[0], None
        if callable(third):
            return None, "mutated_by_a_callable"
        if isinstance(third, str):
            return None, "tags_a_file_rather_than_replacing_a_string"
    return None, "unrecognised_shape"


def main() -> int:
    rep = {"tool": "audit_drill_anchors.py",
           "subject": "every src*_drill.py in this tree",
           "drills": {}, "counts": {}}
    total = stale = unauditable = unrecognised = 0
    silent: list[str] = []

    for path in sorted(CODE.glob("src*_drill.py")):
        try:
            d = load(path)
        except Exception as exc:
            rep["drills"][path.name] = {"error": f"{type(exc).__name__}: {exc}"}
            stale += 1
            continue

        texts = sources_of(d)
        lists = [a for a in dir(d) if a.endswith("DEFECTS")
                 and isinstance(getattr(d, a), list)]
        bad, counted, skipped = [], 0, {}
        for attr in lists:
            for item in getattr(d, attr):
                anchor, why = anchor_of(item)
                if anchor is None:
                    skipped[why] = skipped.get(why, 0) + 1
                    if why == "unrecognised_shape":
                        unrecognised += 1
                    else:
                        unauditable += 1
                    continue
                counted += 1
                hits = sum(text.count(anchor) for text in texts.values())
                if hits != 1:
                    bad.append({"defect": item[0], "list": attr,
                                "matches": hits,
                                "searched": sorted(texts),
                                "anchor": anchor.splitlines()[0][:70]})
        total += counted
        stale += len(bad)
        entry = {"anchors": counted, "stale": bad,
                 "sources_searched": sorted(texts)}
        if skipped:
            entry["not_a_string_replacement"] = skipped
        if counted == 0 and not skipped:
            entry["nothing_audited"] = ("no defect list of a known shape; this "
                                        "drill is not covered by the audit")
            silent.append(path.name)
        rep["drills"][path.name] = entry

    rep["counts"] = {
        "drills": len(rep["drills"]),
        "anchors_checked": total,
        "anchors_not_matching_exactly_once": stale,
        "defects_not_auditable_by_string_match": unauditable,
        "defects_of_an_unrecognised_shape": unrecognised,
        "drills_audited_by_nothing_at_all": len(silent),
    }
    rep["drills_audited_by_nothing_at_all"] = silent
    rep["ok"] = stale == 0 and unrecognised == 0 and not silent
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
