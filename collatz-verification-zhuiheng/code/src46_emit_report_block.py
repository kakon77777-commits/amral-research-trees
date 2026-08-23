"""Emit RUN-028's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red. Every figure below is checked by
`report_block_guard`, which perturbs the log and requires the block to move --
unlike the digit guard shipped in src43..src45, which could not fail. The literature record is read too, so the withdrawal recurrence is
generated rather than remembered.

Usage:  python code/src46_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src46-au2d2.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src46-drill.json"
LIT_LOG = ROOT / "data" / "external" / "au2d2-literature-check.json"
REPORT = ROOT / "reports" / "RUN-028-HARD-ZETA-AU2D2-ATTAINABILITY.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src46_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"
FIGURES = ROOT / "data" / "gate-logs" / "src46-emitter-figures.json"

ORDINAL = {1: "st", 2: "nd", 3: "rd"}



def build(g: dict, d: dict, lit: dict) -> str:
    se = g["saturation_equivalence"]
    gp = g["gap_prediction"]
    fc = g["float_ceiling"]
    cs = g["constants"]
    sr = g["shipped_rows"]
    ap = g["artifact_provenance"]

    out = [
        BEGIN, "",
        "**The Saturation Equivalence, all four cells.** `B/3^L = U_β(L)` against "
        "`Q_j = ⌊βj⌋ ∀ j<L`, both sides exact, on `%d` real first crossings:"
        % se["crossings"],
        "",
        "| | mechanical prefix | not mechanical |",
        "| --- | --- | --- |",
        "| **envelope attained** | `%d` | **`%d`** |"
        % (se["saturated_and_mechanical"], se["saturated_but_NOT_mechanical"]),
        "| **not attained** | **`%d`** | `%d` |"
        % (se["mechanical_but_NOT_saturated"], se["neither"]),
        "",
        "Both off-diagonals are empty, and both diagonals are inhabited (`%s`) — so "
        "the equivalence is exercised in both directions, not only where it is easy."
        % se["both_diagonals_are_inhabited"],
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]

    rows = [
        ("largest `L` at which the envelope is attained",
         "exact rationals", se["largest_L_at_which_the_envelope_is_attained"]),
        ("crossings where the round's gap `G > 0`",
         "the prediction's whole domain", gp["crossings_with_positive_gap"]),
        ("**…of those, attained anyway**",
         "the round predicts zero", gp["attained_despite_a_positive_gap"]),
        ("smallest `L` with `G > 0` among real crossings",
         "for comparison with the line above", gp["smallest_L_with_a_positive_gap"]),
        ("constants disagreeing with their closed forms",
         "η=1/(6ln2), κ_rot=1/(12√2), ln2/(2√2), and κ/η = the relative constant",
         len(cs["disagreements"])),
        ("shipped `G` rows disagreeing",
         "recomputed from the round's own formula, %d rows" % sr["rows"],
         sr["disagreements"]),
        ("float-vs-exact ceiling mismatches",
         "`ceil(log2(y+N/3))` against an integer route, %d rows" % fc["rows_checked"],
         fc["float_vs_exact_mismatches"]),
        ("…closest approach to a power of two",
         "in `log₂`, across those rows", fc["closest_approach_to_a_power_of_two"]),
        ("…margin over float `log2` error",
         "orders of magnitude", fc["margin_in_orders_of_magnitude"]),
        ("defects planted / caught by the check named for each",
         "%d of the entries are robustness properties, not defects"
         % d["counts"]["robustness_properties"],
         "%d / %d" % (d["counts"]["planted"], d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**Provenance.** Row keys the script writes that the JSON lacks: `%s`. Row "
        "keys the JSON has that the script never writes: `%s`. Top-level keys match: "
        "`%s`."
        % (", ".join(ap["row_keys_in_script_but_not_json"]) or "none",
           ", ".join(ap["row_keys_in_json_but_not_script"]) or "none",
           ap["script_top_level_keys"] == ap["json_top_level_keys"]),
        "",
    ]

    for ref in lit["references"]:
        if ref["status"] == "WITHDRAWN":
            out.append(
                "**Literature.** `arXiv:%s` has been withdrawn since %s and is cited "
                "for the **%d%s bundle running**." %
                (ref["arxiv"], ref["withdrawn_on"], ref["OCCURRENCE"],
                 ORDINAL.get(ref["OCCURRENCE"], "th")))

    out += [
        "",
        "Every figure above is emitted by `code/src46_emit_report_block.py` from the "
        "gate logs and the archived literature record. None is typed into this file, "
        "and that is checked rather than claimed: see the guard report below.",
        "", END,
    ]
    return "\n".join(out)


def main() -> int:
    for path in (GATE_LOG, DRILL_LOG, LIT_LOG):
        if not path.exists():
            print(json.dumps({"error": "missing log", "path": str(path)}, indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    lit = json.loads(LIT_LOG.read_text(encoding="utf-8"))

    if not g.get("passed"):
        print(json.dumps({"error": "the recheck is red", "failures": g.get("failures")},
                         indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red; a report built on checks that "
                                   "cannot fail is worse than no report",
                          "counts": d.get("counts")}, indent=2, ensure_ascii=False))
        return 2

    guard = check_against_snapshot(build, [g, d, lit], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to; "
                                   "a figure that stopped moving with its log "
                                   "is a figure somebody typed",
                          "guard": guard}, indent=2))
        return 2

    block = build(g, d, lit)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "no generated-block markers"}, indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src46_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src46_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
