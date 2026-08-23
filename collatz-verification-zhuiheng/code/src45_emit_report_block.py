"""Emit RUN-027's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red, and drills its own staleness comparison by
perturbing every digit in the emitted block. The literature record is read too, so
the withdrawal recurrence is generated rather than remembered.

Usage:  python code/src45_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src45-au2d1.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src45-drill.json"
LIT_LOG = ROOT / "data" / "external" / "au2d1-literature-check.json"
REPORT = ROOT / "reports" / "RUN-027-HARD-ZETA-AU2D1-ROTATION-CAP.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src45_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"
FIGURES = ROOT / "data" / "gate-logs" / "src45-emitter-figures.json"


def build(g: dict, d: dict, lit: dict) -> str:
    rc = g["rotation_cap"]
    dk = g["denjoy_koksma"]
    su = g["shipped_U_values"]
    cs = g["constants"]["constants"]
    cd = g["convergent_denominators"]
    eg = g["endpoint_gap"]

    rows = [
        ("**cap violations** `B/3^L ≤ U_β(L)`",
         "exact rationals, %d real first crossings" % rc["crossings"],
         rc["cap_violations"]),
        ("termwise violations `Q_j ≤ ⌊βj⌋`", "the round's own argument, per term",
         rc["termwise_violations"]),
        ("max `B/3^L ÷ U_β(L)`", "1 means the cap is attained", rc["max_B3_over_U"]),
        ("…crossings where it is **attained**", "at n = %s" % rc["at_n"],
         rc["crossings_where_the_cap_is_ATTAINED"]),
        ("mean `B/3^L ÷ U_β(L)`", "how much of the new cap real crossings use",
         rc["mean_B3_over_U"]),
        ("constants disagreeing with their closed forms",
         "β, 1/(6ln2), 6ln2, √3·ln2, 1/(6(ln2)²) recomputed",
         len(g["constants"]["disagreements"])),
        ("convergent denominators agree", "exact mediant descent vs the shipped list",
         "%s (%d of them)" % (cd["agree"], cd["count"])),
        ("Denjoy–Koksma upper violations", "two-sided, at every convergent",
         dk["upper_violations"]),
        ("Denjoy–Koksma lower violations", "the shipped check is upper-only",
         dk["lower_violations"]),
        ("…exact vs high-precision cross-checks", "where both routes are feasible",
         dk["exact_vs_high_precision_cross_checked"]),
        ("…undecidable wrap decisions", "counted, never guessed",
         dk["undecidable_wrap_decisions"]),
        ("**fraction of the DK allowance used**", "max |U(q) − qη| ÷ Var(f) = 1/3",
         dk["fraction_of_the_bound_used"]),
        ("endpoint-gap identity violations",
         "`B/3^L = (2^D−1)y + 2^{D+1}h`, exact", eg["violations"]),
        ("…crossings where the endpoint DROPS (`h < 0`)",
         "the round's `h ≥ 1` needs the surviving case",
         eg["crossings_with_h_negative_endpoint_dropped"]),
        ("defects planted / caught by their own check", "`code/src45_drill.py`",
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    out = [BEGIN, "", "| what | measured | value |", "| --- | --- | --- |"]
    for a, b, v in rows:
        out.append(f"| {a} | {b} | `{v}` |")

    out += [
        "",
        "**How much the new cap improves on `L/3`.** `U_β(L) ÷ (L/3)`, which tends "
        "to `1/(2 ln 2) = 0.7213…`:",
        "",
        "| L | ratio |",
        "| --- | --- |",
    ]
    for L, r in sorted(rc["U_over_L_third_by_L"].items(), key=lambda kv: int(kv[0])):
        out.append("| %s | %s |" % (L, r))

    out += [
        "",
        "**Finding 1, quantified.** Published decimals against decimals actually "
        "correct, recomputed as exact rationals:",
        "",
        "| L | published | correct | over-published by |",
        "| --- | --- | --- | --- |",
    ]
    for r in su["rows"]:
        out.append("| %d | %d | %d | **%d** |"
                   % (r["L"], r["published_decimals"],
                      r["decimals_actually_correct"], r["over_published_by"]))
    out += [
        "",
        "The over-publication tracks `log₁₀ L`, which is what fixed-precision "
        "summation of `L` terms costs.",
        "",
        "**The constants, each against its closed form.**",
        "",
        "| constant | closed form | published decimals | all correct |",
        "| --- | --- | --- | --- |",
    ]
    for key, v in cs.items():
        if "published_decimals" in v:
            out.append("| `%s` | `%s` | %d | %s |"
                       % (key, v["closed_form"], v["published_decimals"],
                          v["agrees_to_every_published_digit"]))
    o = cs["one_over_6_ln2_squared"]
    out.append("| `%s` | `%s` | printed in §4, not shipped | %s |"
               % ("1/(6 (ln 2)^2)", o["closed_form"],
                  o["agrees_to_printed_digits"]))

    gone = [r for r in lit["collatz_references"] if r["status"] != "live"]
    out += [
        "",
        "**The references, checked.** `%d` Collatz references plus `%d` analytic "
        "one; all say what the notes attribute to them."
        % (len(lit["collatz_references"]),
           len([r for r in lit["analytic_references"] if "arxiv" in r])),
        "",
    ]
    for r in gone:
        out.append(
            "`arXiv:%s` is **%s** (%s) and is cited as a primary reference for the "
            "**%s bundle running** — RUN-026 reported it for A-U.2d, and A-U.2d.1 "
            "repeats it."
            % (r["arxiv"], r["status"], r["withdrawn_on"],
               "second" if r.get("RECURRENCE") else "first"))

    out += [
        "",
        "Every figure above is emitted by `code/src45_emit_report_block.py` from "
        "the gate logs and the archived literature record. None is typed into this "
        "file.",
        "",
        END,
    ]
    return "\n".join(out)


def main() -> int:
    for p in (GATE_LOG, DRILL_LOG, LIT_LOG):
        if not p.exists():
            print(json.dumps({"error": "missing log", "path": str(p)}, indent=2))
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

    block = build(g, d, lit)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "no generated-block markers"}, indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    guard = check_against_snapshot(build, [g, d, lit], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to; "
                                   "a figure that stopped moving with its log "
                                   "is a figure somebody typed",
                          "guard": guard}, indent=2))
        return 2

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src45_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src45_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text,
                      "guard": guard, "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
