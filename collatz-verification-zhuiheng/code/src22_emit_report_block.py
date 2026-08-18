"""Emit RUN-022's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red, and drills its own staleness comparison by
perturbing every digit in the block.

Usage:  python code/src22_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = HERE / "data" / "gate-logs" / "src22-au2e1.json"
DRILL_LOG = HERE / "data" / "gate-logs" / "src22-drill.json"
REPORT = HERE / "reports" / "RUN-022-HARD-ZETA-AU2E1-RESET-BLOCK.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src22_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    o, rs = g["orbits"], g["relative_survival"]
    thm = rs["theorem_form_at_the_weakest_admissible_h"]
    route = rs["theorem_form_at_h_equals_delta_b_which_is_the_route_map_form"]
    pk = g["disjoint_reset_packing"]
    rows = [
        ("orbits walked", "accelerated starts", o["starts"]),
        ("", "steps per start", o["steps"]),
        ("", "reset blocks found", o["reset_blocks_found"]),
        ("", "distinct accelerated valuations seen",
         len(o["distinct_valuations_seen"])),
        ("", "steps with q ≥ 3", o["steps_with_q_ge_3"]),
        ("renormalized anchor", "violations, in exact rational arithmetic",
         g["anchor_identity"]["violations"]),
        ("relative survival", "blocks checked at the weakest admissible h",
         thm["checked"]),
        ("", "violations there", thm["violations"]),
        ("", "blocks checked at h = δ_b (the route map's form)", route["checked"]),
        ("", "violations there", route["violations"]),
        ("depth–duration", "blocks checked", g["depth_duration"]["checked"]),
        ("", "violations", g["depth_duration"]["violations"]),
        ("disjoint packing", "families checked", pk["families_checked"]),
        ("", "violations", pk["violations"]),
        ("the checks themselves", "defects planted",
         d["counts"]["defects_planted"]),
        ("", "caught, each for the reason named", d["counts"]["caught"]),
        ("", "null controls undisturbed", d["counts"]["controls_undisturbed"]),
        ("", "controls requiring the comparison to be able to reject",
         len(g["controls"])),
    ]
    out = [BEGIN, "", "| what | measured | value |", "| --- | --- | --- |"]
    for a, b, v in rows:
        out.append(f"| {a} | {b} | `{v}` |")

    br = g["mod8_bridge"]["q_classes_by_odd_residue_capped_at_3"]
    we = g["worked_example"]
    out += [
        "",
        "**The mod-8 bridge, exhaustively.** Capping the accelerated valuation at "
        "`3`, the four odd residues give: "
        + ", ".join(f"`Y ≡ {r} (mod 8)` → `q ∈ {br[r]}`" for r in ("1", "3", "5", "7"))
        + f". So `q ≥ 3` holds for residue `5` and for no other, which is the "
          f"biconditional the round needs. It is not vacuous on real orbits either: "
          f"`{o['steps_with_q_ge_3']}` of the steps walked here have `q ≥ 3`, and "
          f"the valuations seen span `{o['distinct_valuations_seen']}`.",
        "",
        f"**The round's worked example recomputes.** With `D = {we['D']}` and "
        f"`ρ = {we['rho']}`, `ρ − 2^-D = {we['rho_minus_2_pow_minus_D']}` and the "
        f"duration coefficient is `{we['L_coefficient']}` — the round states "
        f"`{we['package_states']}` and `{we['package_states_coefficient']}`.",
        "",
        "Every figure above is emitted by `code/src22_emit_report_block.py` from "
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
    for name, rep in (("src22_au2e1_reset_block", g), ("src22_drill", d)):
        if not rep.get("ok"):
            print(json.dumps({"error": "%s is not green; refusing to publish "
                                       "counts from a red gate" % name,
                              "problems": rep.get("problems")},
                             indent=2, ensure_ascii=False))
            return 2

    block = build(g, d)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "report has no generated block markers"},
                         indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = head + block + tail

    digits = [i for i, ch in enumerate(block) if ch.isdigit()]
    missed = [i for i in digits
              if (head + block[:i] + str((int(block[i]) + 1) % 10)
                  + block[i + 1:] + tail) == text]
    if not digits or missed:
        print(json.dumps({"error": "the staleness comparison failed its own "
                                   "control", "digits": len(digits),
                          "undetected": missed}, indent=2))
        return 2

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src22_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "ok": not stale},
                         indent=2))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src22_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text,
                      "digits_guarded": len(digits), "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
