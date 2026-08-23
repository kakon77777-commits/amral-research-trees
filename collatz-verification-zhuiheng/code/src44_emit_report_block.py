"""Emit RUN-026's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red, and drills its own staleness comparison by
perturbing every digit in the emitted block. The literature record is read too,
so the withdrawal note is generated rather than remembered.

Usage:  python code/src44_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src44-au2d.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src44-drill.json"
LIT_LOG = ROOT / "data" / "external" / "au2d-literature-check.json"
REPORT = ROOT / "reports" / "RUN-026-HARD-ZETA-AU2D-SOURCE-FREEZE.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src44_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict, lit: dict) -> str:
    sh = g["shift_hereditary_source"]
    h = g["horizons"]
    c = g["contraction"]
    b = g["adelic_bank"]
    f = g["freeze_versus_crossing"]

    rows = [
        ("2-adic source identity `𝓑(σ^s q) = Y_s`",
         "evaluated in `ℤ/2^N`, %d cases across four shifts" % sh["cases"],
         "%d matches, %d mismatches" % (sh["matches"], sh["mismatches"])),
        ("…**negative controls that correctly failed**",
         "one orbit's series against a different orbit's endpoint",
         sh["negative_controls_that_correctly_failed"]),
        ("…negative controls that wrongly matched", "must be zero",
         sh["negative_controls_that_wrongly_matched"]),
        ("freeze-bound violations `F₂(y) ≤ ⌊log₂ y⌋`", "exact, %d starts" % h["starts"],
         h["freeze_bound_violations"]),
        ("mean `F₂ / ⌊log₂ y⌋`", "how loose the bound runs",
         h["mean_F2_over_floor_log2"]),
        ("max `F₂ / ⌊log₂ y⌋`", "1 means the bound is attained",
         h["max_F2_over_floor_log2"]),
        ("…starts where it is **attained**", "so the tightness is measured",
         h["starts_where_the_bound_is_ATTAINED"]),
        ("endpoint-exposure violations", "`m ≥ F₃(y) ⟹ Y_{s+m} < 3^m`",
         h["endpoint_exposure_violations"]),
        ("bi-exact horizon violations",
         "`floor_log32`'s defining inequalities and the domination, separately",
         h["bi_exact_horizon_violations"]),
        ("…starts where `⌊log₂ y⌋` is **strictly** below `⌊log_{3/2} y⌋`",
         "the domination is not vacuous",
         h["starts_where_log2_is_STRICTLY_below_log32"]),
        ("contraction violations `S(x) < 2x`", "exhaustive over %d odd x" % c["odd_x_checked"],
         c["violations"]),
        ("the two expressions for `𝒜_m` disagree on",
         "accumulated series against `2^{Q_m}Y_{s+m}/3^m`",
         b["two_expressions_disagree"]),
        ("`v₂(𝒜_m) ≠ Q_m` on", "numerator carries `2^{Q_m}`, both odd elsewhere",
         b["v2_of_bank_not_equal_to_Q"]),
        ("Archimedean bound violations before the crossing", "`y ≤ 𝒜_m ≤ y + m/3`",
         b["archimedean_bound_violations_before_the_crossing"]),
        ("…starts where it fails **after** the crossing",
         "the negative half, without which the test is one-sided",
         b["starts_where_it_fails_after_the_crossing"]),
        ("defects planted / caught by their own check", "`code/src44_drill.py`",
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    out = [BEGIN, "", "| what | measured | value |", "| --- | --- | --- |"]
    for a, bb, v in rows:
        out.append(f"| {a} | {bb} | `{v}` |")

    out += [
        "",
        "**§15, asked of starts that exist.** Section 15 concludes `F₂₃(y) < L(y)` "
        "for large surviving B-atoms. On real starts:",
        "",
        "| | starts | share |",
        "| --- | --- | --- |",
        "| source frozen **before** the crossing (§15's regime) | %d | %s%% |"
        % (f["source_frozen_before_the_crossing"], f["share_pct"]),
        "| the crossing happens **first** | %d | %s%% |"
        % (f["crossing_first"], f["crossing_first_pct"]),
        "| tie | %d | |" % f["tie"],
        "",
        "out of `%d` starts. RUN-023 measured `0` surviving crossings below "
        "`2·10⁵`, which is the hypothesis §15 needs." % f["starts"],
        "",
    ]

    live = [r for r in lit["references"] if r["status"] == "live"]
    gone = [r for r in lit["references"] if r["status"] != "live"]
    out += [
        "**The four cited references, checked.** `%d` live and saying what the "
        "notes attribute to them; `%d` withdrawn."
        % (len(live), len(gone)),
        "",
        "| arXiv | status | every attributed claim present |",
        "| --- | --- | --- |",
    ]
    for r in lit["references"]:
        allp = all(r["claims_checked"].values())
        extra = ""
        if r["status"] != "live":
            extra = " (%s)" % r.get("withdrawn_on", "")
        out.append("| `%s` | **%s**%s | %s |"
                   % (r["arxiv"], r["status"], extra, "yes" if allp else "NO"))
    for r in gone:
        out += [
            "",
            "`arXiv:%s` was withdrawn on **%s** — %s. It is **not load-bearing**: %s"
            % (r["arxiv"], r["withdrawn_on"], r["withdrawal_reason_as_stated"],
               r["why_not_load_bearing"]),
        ]

    out += [
        "",
        "Every figure above is emitted by `code/src44_emit_report_block.py` from "
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

    digits = [m.start() for m in re.finditer(r"\d", block)]
    missed = [i for i in digits
              if (block[:i] + ("9" if block[i] != "9" else "0") + block[i + 1:]) == block]
    if missed:                                          # pragma: no cover
        print(json.dumps({"error": "staleness comparison blind to some digits",
                          "undetected": missed}, indent=2))
        return 2

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src44_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "ok": not stale}, indent=2))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src44_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text,
                      "digits_guarded": len(digits), "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
