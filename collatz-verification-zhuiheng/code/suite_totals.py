"""Suite-wide drill totals, computed from the archived gate logs.

數學戰士「墜衡」 / AMRAL Research Lab.

The README and the charter quote figures like "N planted defects, all caught by
the check named for each". Typed into prose, such a figure is checked by nothing
and drifts every time a drill is added — the charter said "fourteen drills, 304
defects" while the logs held considerably more.

So the figure is emitted by this script instead, and the prose cites the script.

The one thing it must not do is undercount silently. Drill logs come in two
shapes: the `src*` family puts its tallies under `counts`, while the older
`mutation-drill` and `ot-recheck-drill` put them at the top level. A reader that
knows only one shape returns 0 for the other and the total still looks plausible.
So every log is classified explicitly, and anything this script cannot interpret
is listed under `uninterpreted` and makes it exit non-zero rather than quietly
contributing nothing.

Usage:  python code/suite_totals.py
"""

from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"

# logs that are drills but carry no defect tally of their own
NOT_A_DEFECT_TALLY = {
    "drill-anchor-audit.json": "an audit of the drills, not a drill",
    "coverage-refusal-drill.json": "a refusal drill; it asserts the suite REFUSES "
                                   "to emit, and plants no defects",
}


# Every (planted, caught) key pair a drill log has ever used, and the run that
# introduced it. Enumerated rather than guessed: an unlisted pair is refused, so
# the next rename shows up as a refusal instead of as a smaller total.
#
# It has already shown up that way and been ignored. src22 renamed `caught` and
# src41 renamed both, and from then on this script exited non-zero on every run
# while the archived summary kept saying `drills: 20, uninterpreted: [], ok:
# true`. Seven drills sat outside the published figure for seven rounds. The
# refusal worked; nobody read it. Adding a shape is therefore a deliberate act
# with a name attached, and the shape each log used is reported per row so the
# drift is visible in the output rather than only in an exit code.
TALLY_KEYS = [
    ("defects_planted", "defects_caught_by_the_named_check"),   # src05..src21
    ("defects_planted", "defects_caught"),                      # early variants
    ("defects_planted", "caught"),                              # src22
    ("planted", "caught_by_their_own_check"),                   # src41..src46
]


def tallies(doc: dict) -> dict | None:
    """Read a drill log's tallies from any known shape, or None if none fits."""
    for src in (doc.get("counts", {}), doc):
        for planted_key, caught_key in TALLY_KEYS:
            planted = src.get(planted_key)
            caught = src.get(caught_key)
            if not (isinstance(planted, int) and isinstance(caught, int)):
                continue
            shape = "%s/%s" % (planted_key, caught_key)
            controls = src.get("controls", src.get("controls_planted"))
            if isinstance(controls, list):
                controls = len(controls)
            if isinstance(controls, dict):
                controls = len(controls)
            if not isinstance(controls, int):
                continue
            # three shapes have been used for the control outcome: a count of the
            # undisturbed ones, or a LIST of the disturbed ones. Reading only the
            # first turns a clean drill into a phantom failure, so read both and
            # refuse anything that is neither rather than assuming zero.
            quiet = src.get("controls_undisturbed")
            disturbed = src.get("controls_disturbed")
            if isinstance(quiet, int):
                pass
            elif isinstance(disturbed, list):
                quiet = controls - len(disturbed)
            else:
                continue
            if planted > 0:
                return {"planted": planted, "caught": caught,
                        "controls": controls, "controls_undisturbed": quiet,
                        "shape": shape}
    return None


def main() -> int:
    rows, skipped, uninterpreted = [], [], []
    for p in sorted(LOGS.glob("*drill*.json")):
        if p.name in NOT_A_DEFECT_TALLY:
            skipped.append({"log": p.name, "why": NOT_A_DEFECT_TALLY[p.name]})
            continue
        try:
            doc = json.load(io.open(p, encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            # an empty or half-written log is exactly the case that must refuse
            # rather than contribute zero — a shell redirect truncates its target
            # before the producing process writes a byte
            uninterpreted.append(p.name)
            continue
        t = tallies(doc)
        if t is None:
            uninterpreted.append(p.name)
            continue
        rows.append({"log": p.name, "ok": doc.get("ok"), **t})

    rep = {
        "tool": "suite_totals.py",
        "purpose": "the figure the README and CHARTER cite, emitted rather than "
                   "typed",
        "drills": len(rows),
        "defects_planted": sum(r["planted"] for r in rows),
        "defects_caught_by_the_named_check": sum(r["caught"] for r in rows),
        "controls": sum(r["controls"] for r in rows),
        "controls_undisturbed": sum(r["controls_undisturbed"] for r in rows),
        "per_drill": rows,
        "not_a_defect_tally": skipped,
        "uninterpreted": uninterpreted,
    }
    rep["ok"] = (
        not uninterpreted
        and rep["defects_planted"] == rep["defects_caught_by_the_named_check"]
        and rep["controls"] == rep["controls_undisturbed"]
        and all(r["ok"] for r in rows)
    )
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
