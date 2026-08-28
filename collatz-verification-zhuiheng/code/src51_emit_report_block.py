"""Emit RUN-033's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src51_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src51-au2d5.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src51-drill.json"
REPORT = ROOT / "reports" / "RUN-033-HARD-ZETA-AU2D5-ANNULAR-RESIDUE.md"
FIGURES = ROOT / "data" / "gate-logs" / "src51-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src51_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    ec, sep, se = g["exact_codes"], g["separation"], g["shipped_examples"]
    st, cs, ar = g["orbit_structure"], g["constants"], g["artifacts"]
    tc = g["their_claims"]

    out = [
        BEGIN, "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("**§4** affine identity `2^Q z = 3^k x + B_w` violations",
         "exact integers, %d random codes" % ec["trials"],
         ec["affine_identity_violations"]),
        ("…source class mod `2^(Q+1)` violations", "forward direction",
         ec["source_class_violations"]),
        ("…endpoint class mod `3^k` violations", "forward direction",
         ec["endpoint_class_violations"]),
        ("…**class members that fail to realize the code**",
         "the reverse direction, %d members drawn from the class itself"
         % ec["class_members_checked_in_reverse"],
         ec["class_members_failing_to_realize_the_code"]),
        ("**§4.3** repeated-code pairs formed", "the separation theorem's domain",
         sep["repeated_code_pairs"]),
        ("…source gap not a multiple of `2^(Q+1)`", "must be zero",
         sep["source_gap_not_a_multiple_of_2^(Q+1)"]),
        ("…endpoint gap not `2·3^k·m`", "must be zero",
         sep["endpoint_gap_not_2*3^k*m"]),
        ("…smallest source gap seen, in units of `2^(Q+1)`",
         "1 means the bound is attained",
         sep["smallest_source_gap_in_units_of_2^(Q+1)"]),
        ("shipped sample pairs recomputed from the code alone",
         "%d disagreements" % len(se["disagreeing"]), se["examples_checked"]),
        ("**§6** real sources with `L ≥ 2`",
         "of %d first-crossing sources on %d orbits"
         % (st["sources"], st["orbits"]), st["L_at_least_2"]),
        ("…**`q_(s+1) ≠ 1`**", "must be zero", st["q_next_not_one"]),
        ("…**`y ≢ 3 (mod 4)`**", "must be zero", st["source_not_3_mod_4"]),
        ("chains with distinct increasing sources",
         "§6's own premise", st["chains_with_increasing_sources"]),
        ("…**of those, inside the source corridor `y_r − y₁ < U_β(L)`**",
         "the premise the depth cap needs",
         st["chains_inside_the_source_corridor"]),
        ("…depth-cap violations among those", "vacuously zero",
         st["depth_cap_violations"]),
        ("renewal identity errors", "β-linear integer pairs over %d edges"
         % st["renewal_edges"], st["renewal_identity_errors"]),
        ("…the residual the shipped checker reports", "it evaluates in `float`",
         g["shipped_max_float_residual"]),
        ("plateau / strict-drop edges", "both branches must be inhabited",
         "%d / %d" % (st["plateau_edges"], st["drop_edges"])),
        ("determinants that are not positive integers", "must be zero",
         st["plateau_determinant_not_a_positive_integer"]
         + st["drop_determinant_not_a_positive_integer"]),
        ("laminarity violations", "%d nested, %d disjoint pairs sampled"
         % (st["nested_pairs"], st["disjoint_pairs"]),
         st["laminarity_violations"]),
        ("the checker's own claims independently confirmed",
         "of %d it states; %d not covered here"
         % (tc["claims_the_checker_states"], len(tc["not_covered_by_this_run"])),
         tc["independently_confirmed"]),
        ("validation-record files verified",
         "record shape: %s" % ar["validation_record_shape"], ar["verified"]),
        ("…uncovered files", "the record itself (`%s`)"
         % ar["the_only_uncovered_file_is_the_record_itself"],
         len(ar["present_but_not_covered"])),
        ("constants differing from the exact rational's nearest double",
         "of %d checked" % len(cs["rows"]),
         len(cs["exponents_off_by_at_least_one_ulp"])),
        ("…**that moved between item 50 and item 51**",
         "same quantity, two bundles",
         len(cs["quantities_that_moved_between_the_two_bundles"])),
        ("defects planted / caught by the check named for each",
         "%d robustness property; %d malformed"
         % (d["counts"]["robustness_properties"], d["counts"]["malformed"]),
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    moved = cs["quantities_that_moved_between_the_two_bundles"]
    if moved:
        out += ["", "**Between the bundles.** " + "; ".join(
            "`%s`: item 50 `%s` (%d ulp), item 51 `%s` (%d ulp)"
            % (k, cs["against_item_50"][k]["item_50"],
               cs["against_item_50"][k]["item_50_ulps"],
               cs["against_item_50"][k]["item_51"],
               cs["against_item_50"][k]["item_51_ulps"]) for k in moved) + "."]

    out += [
        "",
        "Every figure above is emitted by `code/src51_emit_report_block.py` from "
        "the gate logs. None is typed into this file.",
        "", END,
    ]
    return "\n".join(out)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (GATE_LOG, DRILL_LOG):
        if not path.exists():
            print(json.dumps({"error": "missing log", "path": str(path)}, indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    if not g.get("passed"):
        print(json.dumps({"error": "the recheck is red",
                          "failures": g.get("failures")}, indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red", "counts": d.get("counts")},
                         indent=2, ensure_ascii=False))
        return 2

    guard = check_against_snapshot(build, [g, d], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to",
                          "guard": guard}, indent=2))
        return 2

    block = build(g, d)
    text = REPORT.read_text(encoding="utf-8")
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail
    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src51_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src51_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
