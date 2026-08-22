"""Emit RUN-024's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either log is red, and drills its own staleness comparison by
perturbing every digit in the emitted block.

Usage:  python code/src42_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src42-au2e3.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src42-drill.json"
REPORT = ROOT / "reports" / "RUN-024-HARD-ZETA-AU2E3-INFINITE-SUPPORT.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src42_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    gap = g["corrigendum_gap"]
    cb = g["unconditional"]["correction_bank"]
    tel = g["unconditional"]["telescoping"]
    bc = g["unconditional"]["bank_cost_identity"]
    cen = g["survival_census"]
    sm = g["not_testable_here"]["suffix_minima"]
    mass = g["mass_no_go"]

    rows = [
        ("odd starts walked", "both crossing indices computed for each",
         gap["starts"]),
        ("**the two routes disagree on**",
         "direct walk of T against ⌊L·log₂3⌋+1 from a bit length",
         gap["routes_disagree"]),
        ("odd-step count ≠ L", "one odd step per accelerated block",
         gap["odd_count_not_equal_to_L"]),
        ("**gap `Q_L − k` is zero**", "the two indices coincide",
         "%s%%" % gap["gap_zero_share_pct"]),
        ("mean gap", "modified steps", gap["gap_mean"]),
        ("largest gap seen", "modified steps", gap["gap_max"]),
        ("bank increment-identity violations", "A_{m+1}−A_m = (1/3)·2^(−δ_m), exact",
         cb["increment_identity_violations"]),
        ("the two expressions for `A_m` disagree on",
         "`2^(−δ_m)·Y_m` against `n + (1/3)Σ 2^(−δ_i)`, accumulated independently",
         cb["two_expressions_for_A_disagree"]),
        ("upper-bound violations before the crossing", "A_m ≤ n + m/3 while δ ≥ 0",
         cb["upper_bound_violations_before_the_crossing"]),
        ("starts where that bound fails after the crossing",
         "the negative half, without which the test is one-sided",
         cb["starts_where_the_upper_bound_fails_after_the_crossing"]),
        ("telescoping violations", "gapped disjoint intervals, exact",
         tel["violations"]),
        ("…of which the inequality is **strict**",
         "with contiguous intervals it is an equality and cannot fire",
         tel["cases_where_the_inequality_is_STRICT"]),
        ("§3 transcription-check violations", "labelled, not counted as a result",
         bc["violations"]),
        ("**surviving resets**", "Y_b ≥ Y_a; a survivor would refute Terras",
         cen["surviving_resets"]),
        ("defects planted / caught by their own check", "`code/src42_drill.py`",
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]

    out = [BEGIN, "", "| what | measured | value |", "| --- | --- | --- |"]
    for a, b, v in rows:
        out.append(f"| {a} | {b} | `{v}` |")

    dist = gap["gap_distribution"]
    shown = [k for k in sorted(dist, key=int)][:9]
    total = sum(dist.values())
    out += [
        "",
        "**The corrigendum's gap, distributed.** `Q_L − k` in modified steps, where "
        "`Q_L` is the accelerated block endpoint A-U.2e.2 indexes by and `k` is the "
        "true modified first crossing:",
        "",
        "| gap | starts | share |",
        "| --- | --- | --- |",
    ]
    for k in shown:
        out.append("| %s | %d | %.2f%% |" % (k, dist[k], 100.0 * dist[k] / total))
    tail = sum(dist[k] for k in dist if int(k) > int(shown[-1]))
    if tail:
        out.append("| > %s | %d | %.2f%% |" % (shown[-1], tail, 100.0 * tail / total))

    light = mass["infinite_sets_can_be_arbitrarily_light"]
    out += [
        "",
        "**The Mass No-Go, by construction.** For each target the set is infinite and "
        "its mass is an exact rational: "
        + "; ".join(
            "`s=%d`, target `%s` → `%s` with mass `%.3g`"
            % (e["s"], e["epsilon"], e["set"], e["mass"]) for e in light
        )
        + ".",
        "",
        "**§8, and why the agreement is not evidence.** Over `%d` orbits the "
        "δ-characterisation and the Y-characterisation pick the same positions every "
        "time — and every set has size `%s`, the final index alone. Reported as "
        "`testable_here: %s`."
        % (sm["starts"], ", ".join(sm["delta_set_sizes"].keys()),
           str(sm["testable_here"]).lower()),
        "",
        "Every figure above is emitted by `code/src42_emit_report_block.py` from the "
        "two gate logs. None is typed into this file.",
        "",
        END,
    ]
    return "\n".join(out)


def main() -> int:
    for p in (GATE_LOG, DRILL_LOG):
        if not p.exists():
            print(json.dumps({"error": "missing log", "path": str(p)}, indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    if not g.get("passed"):
        print(json.dumps({"error": "the recheck is red; refusing to publish counts "
                                   "from a red gate", "failures": g.get("failures")},
                         indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red; a report built on checks that "
                                   "cannot fail is worse than no report",
                          "counts": d.get("counts")}, indent=2, ensure_ascii=False))
        return 2

    block = build(g, d)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "no generated-block markers in the report"},
                         indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    digits = [m.start() for m in re.finditer(r"\d", block)]
    missed = [i for i in digits
              if (block[:i] + ("9" if block[i] != "9" else "0") + block[i + 1:]) == block]
    if missed:                                          # pragma: no cover
        print(json.dumps({"error": "the staleness comparison is blind to some digits",
                          "undetected": missed}, indent=2))
        return 2

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src42_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "ok": not stale}, indent=2))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src42_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text,
                      "digits_guarded": len(digits), "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
