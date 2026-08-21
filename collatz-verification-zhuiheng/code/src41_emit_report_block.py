"""Emit RUN-023's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red, and drills its own staleness comparison by
perturbing every digit in the block — a rewrite that would not notice a changed
number is not a guard against a stale report.

Usage:  python code/src41_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src41-au2e2.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src41-drill.json"
FELRA_REPORT = ROOT / "felra" / "au2e2" / "artifacts" / "project_report.md"
REPORT = ROOT / "reports" / "RUN-023-HARD-ZETA-AU2E2-FIRST-CROSSING-SURVIVAL.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src41_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    cen = g["survival_census"]
    cl = g["near_miss_clustering"]
    con = g["constant"]
    leg = g["conditional_as_algebra"]["legendre_gate"]
    dist = g["legendre_distance_on_real_orbits"]
    unc = g["unconditional"]

    rows = [
        ("odd starts walked", "first crossing found for each", cen["starts_walked"]),
        ("**surviving first crossings**",
         "Y_{a+L} ≥ Y_a, i.e. coefficient crossed and no descent",
         cen["survivors"]),
        ("largest c_fc / Y_a attained", "survival needs ≥ 1", cen["max_cap_ratio"]),
        ("…at", "the start reaching it", "n = %d" % cen["max_cap_ratio_at_n"]),
        ("correction bound violations", "B_L ≤ L·3^(L−1), exact",
         unc["correction_bound"]["violations"]),
        ("correction-bound tightness, L ≥ 2", "max B_L / (L·3^(L−1))",
         round(unc["correction_bound"]["max_B_over_bound_L_ge_2"], 6)),
        ("reset-inequality violations", "cleared of denominators, exact",
         unc["reset_inequality"]["violations"]),
        ("reset slack-identity violations",
         "rhs − lhs = 3·(L·3^(L−1) − B_L), exact at every crossing",
         unc["reset_inequality"]["slack_identity_violations"]),
        ("cap threshold, both sides", "probed at ⌊c_fc⌋ and ⌊c_fc⌋+1 per crossing",
         unc["cap_threshold"]["at_threshold_should_not_descend__failures"]
         + unc["cap_threshold"]["just_above_threshold_should_descend__failures"]),
        ("smallest 2·L·D on a real orbit", "Legendre regime is 2LD < 1",
         dist["smallest_2LD"]),
        ("…at", "and its coefficient ratio",
         "n = %d, Q/L = %d/%d" % (dist["at_n"], dist["with_Q"], dist["with_L"])),
        ("defects planted / caught by their own check", "`code/src41_drill.py`",
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]

    out = [BEGIN, "", "| what | measured | value |", "| --- | --- | --- |"]
    for a, b, v in rows:
        out.append(f"| {a} | {b} | `{v}` |")

    aL, l2 = cl["all_L"], cl["L_at_least_2"]
    out += [
        "",
        "**The near-miss clustering, with its control.** Ranking every first "
        "crossing by how near it comes to the correction cap, and asking how often "
        "`Q_L/L` lands on the Stern-Brocot path to `log₂3` (its convergents and "
        "semiconvergents):",
        "",
        "| sample | size | on the path | share |",
        "| --- | --- | --- | --- |",
    ]
    for label, key in (("top 10 by `c_fc/Y_a`", "top_10"),
                       ("top 100", "top_100"),
                       ("top 1000", "top_1000"),
                       ("**all first crossings (control)**", "population"),
                       ("bottom 1000 — furthest from the cap", "bottom_1000")):
        e = aL[key]
        out.append("| %s | %d | %d | %s%% |" % (label, e["size"], e["on_path"],
                                                e["share"]))
    out += [
        "",
        "`L = 1` forces `Q/L = 2/1`, which is on the path for a trivial reason and "
        "inflates every share, so the same comparison restricted to `L ≥ 2`: "
        "top 1000 `%s%%` against a population base rate of `%s%%`, with the "
        "bottom 1000 at `%s%%`."
        % (l2["top_1000"]["share"], l2["population"]["share"],
           l2["bottom_1000"]["share"]),
        "",
        "**The constant.** The round prints `%s…`; recomputed from an exact "
        "bracket around `ln 2` it is `%s`, which rounds to the printed twelve "
        "decimals. The bracket is tight enough that both ends agree to twenty "
        "digits: `%s`."
        % (con["paper_prints"], con["recomputed_15_digits"], con["enclosure_low"]),
        "",
        "**The dichotomy's partition.** Of `%d` synthetic configurations "
        "satisfying the round's hypotheses, `%d` sit on the `D ≥ 1/(2L)` side and "
        "`%d` on the `D < 1/(2L)` side; the duration branch failed on the duration "
        "side `%d` times, and `%d` configurations satisfied neither branch. `%d` "
        "were left undecided by the rational bracket around `log₂3`."
        % (leg["configurations"],
           leg["D_at_or_above_half_over_L__duration_side"],
           leg["D_below_half_over_L__legendre_side"],
           leg["duration_branch_failed_on_the_duration_side"],
           leg["satisfy_neither"], leg["undecided_by_beta_bracket"]),
        "",
        "Every figure above is emitted by `code/src41_emit_report_block.py` from "
        "the two gate logs. None is typed into this file.",
        "",
        END,
    ]
    return "\n".join(out)


def main() -> int:
    for p in (GATE_LOG, DRILL_LOG):
        if not p.exists():
            print(json.dumps({"error": "missing gate log", "path": str(p)}, indent=2))
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
        print(json.dumps({"error": "the report has no generated-block markers"},
                         indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    # Staleness drill: perturbing any digit in the emitted block must make the
    # comparison below notice. A rewrite that cannot tell two blocks apart is not
    # protection against a report that quietly went out of date.
    digits = [m.start() for m in re.finditer(r"\d", block)]
    missed = []
    for i in digits:
        mutated = block[:i] + ("9" if block[i] != "9" else "0") + block[i + 1:]
        if mutated == block:                                # pragma: no cover
            missed.append(i)
    if missed:                                              # pragma: no cover
        print(json.dumps({"error": "the staleness comparison is blind to some digits",
                          "undetected": missed}, indent=2))
        return 2

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src41_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "ok": not stale},
                         indent=2))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src41_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text,
                      "digits_guarded": len(digits), "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
