"""Emit RUN-034's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src52_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src52-au2d6.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src52-drill.json"
REPORT = ROOT / "reports" / "RUN-034-HARD-ZETA-AU2D6-FAREY-ENTROPY.md"
FIGURES = ROOT / "data" / "gate-logs" / "src52-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src52_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    eb, cap, b2b = g["exact_bridge"], g["capacity"], g["b_to_b"]
    cf, oc, cs = g["continued_fractions"], g["orbit_carryover"], g["constants"]
    ar, tc = g["artifacts"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The capacity count, formula against enumeration.** A sample of the "
        "coprime pairs enumerated exhaustively:",
        "",
        "| `p` | `g` | enumerated | `binom(p,g)/p` |",
        "| --- | --- | --- | --- |",
    ]
    for r in cap["rows"][:8]:
        out.append("| `%d` | `%d` | `%d` | `%d` |"
                   % (r["p"], r["g"], r["enumerated"], r["formula"]))
    out += [
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("coprime pairs enumerated exhaustively",
         "largest `%s`, with `%d` members"
         % (cap["largest_pair"], cap["largest_count"]), cap["pairs_enumerated"]),
        ("…**enumeration disagreeing with the closed form**", "must be zero",
         len(cap["enumeration_disagreements"])),
        ("…the two closed forms disagreeing with each other",
         "`binom(p−1,g−1)/g` against `binom(p,g)/p`",
         len(cap["formula_disagreements_between_the_two_forms"])),
        ("shipped capacity examples recomputed",
         "%d disagreements, including the 129-digit one"
         % len(cap["shipped_examples_disagreeing"]),
         cap["shipped_examples_checked"]),
        ("**§3** binary-bridge violations `C(d(w)) = B_w`",
         "exact integers, %d random codes" % eb["trials"],
         eb["bridge_violations_C_of_d_equals_B"]),
        ("…normalized-correction violations",
         "`c(w) = (1/3)Σ2^(P_j)/3^j` as exact Fractions",
         eb["normalized_correction_violations"]),
        ("…concatenation violations on `B` / on `c`", "must be zero",
         "%d / %d" % (eb["concatenation_violations_on_B"],
                      eb["concatenation_violations_on_c"])),
        ("**§6** codes with a `3 (mod 4)` destination",
         "the theorem's own hypothesis", b2b["codes_with_a_B_destination"]),
        ("…class violations mod `2^(p+2)`", "forward direction",
         b2b["class_violations"]),
        ("…**class members failing the code or the residue**",
         "the reverse direction, %d members drawn from the class itself"
         % b2b["class_members_checked_in_reverse"],
         b2b["class_members_failing_the_code_or_the_residue"]),
        ("…source gaps below `2^(p+2)` / destination gaps not `4·3^g`",
         "%d repeated-code pairs" % b2b["repeated_code_pairs"],
         "%d / %d" % (b2b["source_gap_below_2^(p+2)"],
                      b2b["destination_gap_not_a_multiple_of_4*3^g"])),
        ("…pairs where the modulus is exactly twice item 51's",
         "the extra bit, counted", b2b["pairs_where_the_modulus_is_exactly_twice_item_51's"]),
        ("**item 51 carryover** real sources with `L ≥ 2`",
         "re-verified, not assumed", oc["sources_with_L_at_least_2"]),
        ("…**not `≡ 3 (mod 4)`**", "must be zero", oc["not_3_mod_4"]),
        ("published `β` partial quotients", "of which the first 16 match the "
         "terms RUN-029 certified by integer comparison: `%s`"
         % cf["beta_first_16_match_the_certified_terms"], cf["beta_terms_published"]),
        ("`θ` expansion equals `[0] + β`'s shifted",
         "which is what `θ = β − 1` requires; and `θ ≠ 1/β` is `%s`"
         % cf["theta_is_not_one_over_beta"],
         cf["theta_cf_equals_zero_then_beta_cf_shifted"]),
        ("inherited exponents off the exact rational's nearest double",
         "of %d checked" % len(cs["rows"]), len(cs["off_by_at_least_one_ulp"])),
        ("validation-record files verified",
         "shape: %s; uncovered: %d" % (ar["validation_record_shape"],
                                       len(ar["present_but_not_covered"])),
         ar["verified"]),
        ("the checker's stated claims independently confirmed",
         "of %d; %d named as not covered here"
         % (tc["claims_the_checker_states"], len(tc["not_covered_by_this_run"])),
         tc["independently_confirmed"]),
        ("defects planted / caught by the check named for each",
         "%d robustness property; %d malformed; first-pass"
         % (d["counts"]["robustness_properties"], d["counts"]["malformed"]),
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**The two transcripts.** `checker_stdout.txt` is byte-identical to the "
        "checker report: `%s`. It is the report plus `%r`."
        % (ar["report_and_stdout_byte_identical"], ar["stdout_is_the_report_plus"]),
        "",
        "**Not covered here**, named rather than implied: "
        + "; ".join("*%s*" % c for c in tc["not_covered_by_this_run"]) + ".",
        "",
        "Every figure above is emitted by `code/src52_emit_report_block.py` from "
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
        print(json.dumps({"tool": "src52_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src52_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
