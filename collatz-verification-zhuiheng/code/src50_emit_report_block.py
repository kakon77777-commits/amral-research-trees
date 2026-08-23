"""Emit RUN-032's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red. Every figure is held to a snapshot of what the
block actually reads by `report_block_guard` — the guard that replaced the one
shipped in src43..src45, which could not fail (RUN-028).

Usage:  python code/src50_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src50-au2d4.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src50-drill.json"
REPORT = ROOT / "reports" / "RUN-032-HARD-ZETA-AU2D4-CONGESTION-RIGIDITY.md"
FIGURES = ROOT / "data" / "gate-logs" / "src50-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src50_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    st, fm, ar = g["structure"], g["float_margin"], g["artifacts"]
    ex, sm, mt = g["exponents"], g["shipped_smoke_tests"], g["shipped_mechanical_tests"]

    out = [
        BEGIN, "",
        "**The shipped checker's own figures, recomputed in exact integers.** Read "
        "from its report, never run:",
        "",
        "| start | accelerated steps | max active depth | at time | chain plateau / strict-drop edges |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in st["rows"]:
        out.append("| `%d` | `%d` | `%d` | `%d` | `%d / %d` |"
                   % (r["start"], r["accelerated_steps_to_1"],
                      r["max_completed_active_depth"], r["depth_time"],
                      r["chain_plateau_edges"], r["chain_strict_drop_edges"]))
    out += [
        "",
        "Every field of every row agrees with the shipped report (`%d` starts "
        "compared, `%d` fields each, `%d` disagreements), and so do all `%d` of its "
        "mechanical-word rows (`%d` disagreements)."
        % (sm["starts_compared"], sm["fields_per_start"], len(sm["disagreeing"]),
           mt["sizes_compared"], len(mt["disagreeing"])),
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]

    rows = [
        ("**Theorem 3.1** — proper prefixes with a smaller-or-equal slack",
         "exact integer comparison over %d intervals on %d orbits"
         % (st["intervals"], st["orbits"]), st["prefix_violations"]),
        ("…the two independent routes disagreeing",
         "a quadratic scan against a monotone stack",
         st["two_routes_disagreements"]),
        ("**Theorem 4.1** — interval pairs that properly cross",
         "must be zero", st["laminarity_violations"]),
        ("…nested pairs / disjoint pairs",
         "both branches must be inhabited or laminarity is untested",
         "%d / %d" % (st["nested_pairs"], st["disjoint_pairs"])),
        ("**annulus identity** `A+D = D'+E` — errors",
         "as β-linear integer pairs over %d nested edges, so the residual is a "
         "pair and not a small number" % st["annulus_edges"],
         st["annulus_identity_errors"]),
        ("…the residual the bundle's own validation record reports",
         "its checker evaluates the same identity in `float`",
         ar["checker_gate_reported"]["max_annulus_identity_error"]),
        ("plateau edges / strict-drop edges",
         "the dichotomy must be exercised in both branches",
         "%d / %d" % (st["plateau_edges"], st["strict_drop_edges"])),
        ("**determinant** `Δ = rg − ph = gE + hA` — disagreements",
         "β cancels exactly; checked on every strict-drop edge",
         st["determinant_form_disagreements"]),
        ("…determinants below one", "must be zero", st["determinants_below_one"]),
        ("smallest slack gap the float comparison had to resolve",
         "%d comparisons, exactly" % fm["comparisons_the_scan_had_to_decide"],
         fm["smallest_exact_gap"]),
        ("…double spacing at that magnitude", "", fm["double_spacing_at_that_magnitude"]),
        ("…**margin, in orders of magnitude**", "the failure mode looked for",
         fm["margin_in_orders_of_magnitude"]),
        ("published exponents differing from the exact rational's nearest double",
         "of %d, largest drift %d ulps"
         % (len(ex["rows"]), ex["largest_ulp_drift"]),
         len(ex["exponents_off_by_at_least_one_ulp"])),
        ("…wrong beyond 15 significant digits", "must be zero",
         len(ex["exponents_wrong_beyond_15_digits"])),
        ("validation-record hashes verified",
         "of %d listed, over %d files in the bundle"
         % (ar["files_listed_by_the_validation_record"], ar["files_in_the_bundle"]),
         ar["verified"]),
        ("…files present but uncovered",
         "the only one is the record itself (`%s`)"
         % ar["the_only_uncovered_file_is_the_record_itself"],
         len(ar["present_but_not_covered"])),
        ("…declared upstream hashes agreeing with this tree's own records",
         "RUN-030 and RUN-031",
         sum(1 for v in ar["upstream_state"].values() if v["agrees"])),
        ("defects planted / caught by the check named for each",
         "%d of the entries is a robustness property; %d malformed"
         % (d["counts"]["robustness_properties"], d["counts"]["malformed"]),
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "The bracketed floor route used for the mechanical word agrees with exact "
        "powers of three on `0..399` (`%s`) and needed the exact fallback `%d` "
        "times at `N = %d`."
        % (g["beta_floor_route_agrees_with_exact_powers_on_0_to_399"],
           g["mechanical"]["times_the_bracket_could_not_decide_and_the_exact_power_ran"],
           g["mechanical"]["largest_N"]),
        "",
        "Every figure above is emitted by `code/src50_emit_report_block.py` from "
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
        print(json.dumps({"error": "the recheck is red", "failures": g.get("failures")},
                         indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red; a report built on checks that "
                                   "cannot fail is worse than no report",
                          "counts": d.get("counts")}, indent=2, ensure_ascii=False))
        return 2

    guard = check_against_snapshot(build, [g, d], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to; "
                                   "a figure that stopped moving with its log "
                                   "is a figure somebody typed",
                          "guard": guard}, indent=2))
        return 2

    block = build(g, d)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "no generated-block markers"}, indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src50_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src50_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
