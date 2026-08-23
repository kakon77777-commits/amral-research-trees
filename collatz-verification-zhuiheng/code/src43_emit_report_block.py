"""Emit RUN-025's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either log is red, and drills its own staleness comparison by
perturbing every digit in the emitted block.

Usage:  python code/src43_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src43-au2e4.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src43-drill.json"
REPORT = ROOT / "reports" / "RUN-025-HARD-ZETA-AU2E4-RENEWAL-RIGIDITY.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src43_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"
FIGURES = ROOT / "data" / "gate-logs" / "src43-emitter-figures.json"


def build(g: dict, d: dict) -> str:
    det = g["determinant"]["positive_on_real_brackets"]
    idn = g["determinant"]["identity_is_algebra_in_beta"]
    cb = g["cross_error_barrier"]
    fl = g["farey_lock"]
    ss = g["scale_separation"]
    tax = g["cf_tax"]
    rc = g["recycling_no_go"]
    g5 = g["section_5_growth"]
    rho = g["rho_constants"]

    rows = [
        ("bracketing pairs formed", "every lower approximant against every upper",
         det["pairs"]),
        ("…with `Δ = 1` (Farey-locked)", "", det["delta_equals_1"]),
        ("…with `Δ > 1`", "so the positivity check is not tested only where it is automatic",
         det["delta_above_1"]),
        ("largest `Δ` seen", "", det["largest_delta"]),
        ("`Δ ≥ 1` violations", "exact integer comparison", det["violations"]),
        ("identity violations at arbitrary `β`",
         "%d pairs × %d substitutions; it is algebra, not arithmetic about log₂3"
         % (idn["pairs"], idn["beta_substitutions_each"]), idn["violations"]),
        ("cross-error barrier violations", "`max(d₋,d₊) ≥ 1/(q₋+q₊)`, β bracketed",
         cb["violations"]),
        ("…undecided by the β bracket", "reported, never rounded",
         cb["undecided_by_beta_bracket"]),
        ("…pairs within a factor 2 of the barrier", "so the bound is approached",
         cb["pairs_within_a_factor_two_of_the_barrier"]),
        ("consecutive brackets **not** Farey-locked", "must be zero",
         fl["consecutive_pairs_not_locked"]),
        ("locked pairs violating `s ≥ q₋+q₊`", "and the mediant attains it",
         fl["locked_pairs_violating_the_bound"]),
        ("unlocked pairs admitting a cheaper interior",
         "the negative half — %d checked" % fl["unlocked_pairs_checked"],
         fl["unlocked_pairs_admitting_a_cheaper_interior"]),
        ("continued-fraction tax violations", "`1/(q+q′) < |qβ−p| < 1/q′`",
         tax["violations"]),
        ("recycling monotonicity violations",
         "`g/(2^{gd}−1)` strictly decreasing over %d samples" % rc["samples"],
         rc["monotonicity_violations"]),
        ("defects planted / caught by their own check", "`code/src43_drill.py`",
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    out = [BEGIN, "", "| what | measured | value |", "| --- | --- | --- |"]
    for a, b, v in rows:
        out.append(f"| {a} | {b} | `{v}` |")

    out += [
        "",
        "**§5, premise against conclusion.** The premise is checked at every step of "
        "the descent; the inference is then tested directly.",
        "",
        "| | |",
        "| --- | --- |",
        "| premise `q_new = q₋+q₊` violations | `%d` |"
        % g5["premise_next_denominator_is_q_minus_plus_q_plus__violations"],
        "| steps failing `q_k ≥ q_{k−1}+q_{k−2}` | **`%d` of `%d`** |"
        % (g5["steps_failing_q_k_ge_q_k1_plus_q_k2"], g5["steps"]),
        "| longest same-side run | **`%d`** |" % g5["longest_same_side_run"],
        "| denominators across it | `%s` |"
        % ", ".join(str(x) for x in g5["denominators_in_that_run"]),
        "| consecutive differences | `%s` — constant: `%s` |"
        % (", ".join(str(x) for x in g5["consecutive_differences_there"]),
           str(g5["difference_is_constant"]).lower()),
        "| **convergents** failing the recursion | `%d` |"
        % g5["convergents_failing_the_fibonacci_recursion"],
        "",
        "Record updates against `log₂N`, which would be bounded if the count were "
        "`O(log N)`:",
        "",
        "| N | updates | log₂N | ratio |",
        "| --- | --- | --- | --- |",
    ]
    for N, e in sorted(g5["record_updates_against_log2N"].items(), key=lambda kv: int(kv[0])):
        out.append("| %s | %d | %s | **%s** |"
                   % (N, e["record_updates"], e["log2_N"], e["ratio"]))

    out += [
        "",
        "**The two constants, exactly.** `c = 2/5` gives `1 − 4c² = %s`, a perfect "
        "rational square, so `ρ = %s` — a rational, no square root evaluated. "
        "`c = 1/4` gives `1 − 4c² = %s`, so `ρ = %s`, recomputed as `%s` against the "
        "round's printed `%s`."
        % (rho["c_2_5"]["one_minus_4c2"], rho["c_2_5"]["rho_exact"],
           rho["c_1_4"]["one_minus_4c2"], rho["c_1_4"]["closed_form"],
           rho["c_1_4"]["recomputed"], rho["c_1_4"]["paper_says"]),
        "",
        "**Scale separation, and where its hypothesis is inhabited at all.** "
        + "; ".join(
            "`%s`: %d qualifying pairs, %d violations%s"
            % (k.replace("c_", "c = ").replace("_", "/"),
               v["pairs_satisfying_the_hypothesis"], v["violations"],
               (", smallest scale ratio `%s`" % v["min_scale_ratio_seen"])
               if v["min_scale_ratio_seen"] else "")
            for k, v in sorted(ss.items()) if k.startswith("c_"))
        + ". A `c` with no qualifying pair is reported as uninhabited rather than "
          "as a pass — requiring every `c` to be inhabited would be asking the "
          "sample to contain the very configuration the theorem constrains.",
        "",
        "Every figure above is emitted by `code/src43_emit_report_block.py` from the "
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
        print(json.dumps({"error": "the recheck is red", "failures": g.get("failures")},
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
        print(json.dumps({"error": "no generated-block markers"}, indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    guard = check_against_snapshot(build, [g, d], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to; "
                                   "a figure that stopped moving with its log "
                                   "is a figure somebody typed",
                          "guard": guard}, indent=2))
        return 2

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src43_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src43_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text,
                      "guard": guard, "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
