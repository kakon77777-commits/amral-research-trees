"""Emit RUN-029's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red. Every figure is checked by
`report_block_guard`, which perturbs the log and requires the block to move --
the guard that replaced the one shipped in src43..src45, which could not fail
(RUN-028). The literature record is read too, so the withdrawal recurrence and
the citation finding are generated rather than remembered.

Usage:  python code/src47_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src47-au2d3.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src47-drill.json"
LIT_LOG = ROOT / "data" / "external" / "au2d3-literature-check.json"
REPORT = ROOT / "reports" / "RUN-029-HARD-ZETA-AU2D3-SURVIVAL-CLOSURE.md"
FIGURES = ROOT / "data" / "gate-logs" / "src47-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src47_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"

ORDINAL = {1: "st", 2: "nd", 3: "rd"}


def build(g: dict, d: dict, lit: dict) -> str:
    ec = g["exponent_chain"]
    tc = g["transcendental_constants"]
    cf = g["continued_fraction"]
    tax = g["cf_tax"]
    filt = g["upper_convergent_filter"]
    sr = g["shipped_rows"]
    xc = g["expansion_coefficients"]
    ineq = g["elementary_inequalities"]
    rg = g["renewal_geometry"]
    ap = g["artifact_provenance"]

    out = [
        BEGIN, "",
        "**The exponent chain, exactly.** `rho_star` is a terminating decimal, so "
        "every exponent the round derives from it is a rational number and the "
        "published digits can be compared with an exact expansion rather than with "
        "a better approximation:",
        "",
        "| | exact value | 100 published digits |",
        "| --- | --- | --- |",
    ]
    for key, label in (("theta_star", "`θ★ = 1/(ρ★+1)`"),
                       ("sigma_star", "`σ★ = 1/(1+θ★)`"),
                       ("congestion_exponent", "`1 − σ★`")):
        exact = ec["%s_exact" % ("congestion" if key == "congestion_exponent" else key)]
        verdict = ec["published_digits"][key]["verdict"]
        out.append("| %s | `%s` | %s |" % (label, exact, verdict))

    out += [
        "",
        "`ρ★ = %s` exceeds the `%s` the round cites by `%s`, so \"conservatively\" "
        "holds — a larger exponent is the weaker assumption. Checked as exact "
        "rationals, not as floats."
        % (ec["rho_star_as_an_exact_rational"], ec["cited_exponent"],
           ec["rho_star_minus_cited"]),
        "",
        "**The two second-order coefficients.** The scaled residual must vanish for "
        "the round's value and must *not* vanish for a neighbouring one — otherwise "
        "the probe confirms rather than tests.",
        "",
        "| | `1e4` | `1e12` | falls ≥1000× | a 1%-wrong value still vanishes |",
        "| --- | --- | --- | --- | --- |",
    ]
    s9, s16 = xc["section_9_scaled_residuals"], xc["section_16_scaled_residuals"]
    out += [
        "| §9, `c₁ = ln2·κ_rot/η_β²` | `%s` | `%s` | `%s` | `%s` |"
        % (s9[0]["residual_with_the_round_s_c1"],
           s9[-1]["residual_with_the_round_s_c1"],
           xc["section_9_residual_falls_by_at_least_1000x_from_1e4_to_1e12"],
           not xc["section_9_wrong_coefficient_does_not_vanish"]),
        "| §16, `κ_rot/η_β^{3/2}` | `%s` | `%s` | `%s` | `%s` |"
        % (s16[0]["residual_with_the_round_s_coefficient"],
           s16[-1]["residual_with_the_round_s_coefficient"],
           xc["section_16_residual_falls_by_at_least_1000x_from_1e4_to_1e12"],
           not xc["section_16_wrong_coefficient_does_not_vanish"]),
        "",
        "The 1%%-perturbed residuals go to `%s` and `%s` instead of to zero."
        % (s9[-1]["residual_with_c1_wrong_by_1pct"],
           s16[-1]["residual_with_it_wrong_by_1pct"]),
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]

    rows = [
        ("partial quotients of `log₂3` certified by integer comparison alone",
         "`2^A` vs `3^B`; no logarithm evaluated",
         cf["terms_certified_by_integer_comparison"]),
        ("…largest denominator so certified", "where the integers stop being cheap",
         cf["largest_denominator_certified"]),
        ("…integer comparisons actually performed",
         "so the independence is measured, not claimed",
         cf["integer_comparisons_performed"]),
        ("shipped rows disagreeing with the recomputed convergents",
         "%d integer-certified, %d cross-checked at 400 dps"
         % (cf["rows_integer_certified"], cf["rows_cross_checked_only"]),
         len(cf["disagreements"])),
        ("continued-fraction tax violations `1/(q+q⁺) < p−βq < 1/q⁺`",
         "%d rows decided by exact rationals, the rest at 400 dps"
         % tax["rows_decided_exactly"],
         len(tax["violations"]) + len(tax["violations_at_400_dps_over_every_row"])),
        ("upper convergents missing from the JSON / wrongly present",
         "the filter checked in **both** directions, by parity",
         "%d / %d" % (len(filt["above_beta_but_missing_from_the_JSON"]),
                      len(filt["below_beta_but_present_in_the_JSON"]))),
        ("…parity confirmed independently by the exact bracket on",
         "indices where the bracket is tight enough to judge",
         filt["parity_confirmed_by_the_exact_bracket_on"]),
        ("transcendental constants over-published",
         "of %d, against their closed forms at 400 dps"
         % len(tc["published_digits"]), len(tc["over_published"])),
        ("constants disagreeing beyond rounding",
         "a different number, not a rounding complaint",
         len(tc["disagreeing_beyond_rounding"])),
        ("shipped row values that are **wrong**",
         "as opposed to over-published", len(sr["rows_with_a_wrong_value"])),
        ("fewest significant digits correct in any row field",
         "`p − βq` at the largest convergent",
         sr["fewest_significant_digits_correct"]),
        ("rows where the cancellation model mispredicts that",
         "`log10(β·q·q⁺)`, required conservative and within 4 digits",
         len(sr["rows_where_the_cancellation_model_mispredicts"])),
        ("elementary-inequality violations",
         "`2^D−1 ≥ (ln2)D`, `2^{gd}−1 ≥ g(2^d−1)`, `Qα−L = αD`, `D < 1`",
         ineq["violations"]),
        ("renewal sum-bound failures",
         "`Σ(2j+1)^θ` against its integral, R up to 3000",
         rg["sum_bound_failures"]),
        ("interval-colouring trials using more colours than the max overlap",
         "%d trials, %d distinct overlap counts, %d with a genuine overlap"
         % (rg["colouring_trials"], rg["distinct_max_overlaps_seen"],
            rg["trials_with_a_genuine_overlap"]),
         rg["trials_where_colours_used_exceeded_max_overlap"]),
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
        "**Provenance — and this time it holds.** Top-level keys in the script but "
        "not the JSON: `%s`. Row keys in the JSON but not the script: `%s`. The "
        "shipped JSON **is** what the shipped script produces (`%s`), so the item-35 "
        "class does not recur at its fourth look."
        % (", ".join(ap["top_level_keys_in_script_but_not_json"]) or "none",
           ", ".join(ap["row_keys_in_json_but_not_script"]) or "none",
           ap["json_was_produced_by_this_script"]),
        "",
    ]

    for ref in sorted(lit["references"],
                      key=lambda r: 0 if r.get("status") == "WITHDRAWN" else 1):
        if ref.get("status") == "WITHDRAWN":
            out.append(
                "**Literature.** `arXiv:%s` has been withdrawn since %s and is cited "
                "for the **%d%s bundle running**, alongside the paper its withdrawal "
                "notice defers to."
                % (ref["arxiv"], ref["withdrawn_on"], ref["OCCURRENCE"],
                   ORDINAL.get(ref["OCCURRENCE"], "th")))
            out.append("")
        if ref.get("crossref_says_title"):
            out.append(
                "The round's one load-bearing citation gives the title as "
                "`log_2 3`; Crossref gives `%s`, by %s. Volume, pages, year and DOI "
                "match exactly."
                % (ref["crossref_says_title"], " and ".join(ref["crossref_says_authors"])))

    out += [
        "",
        "Every figure above is emitted by `code/src47_emit_report_block.py` from the "
        "gate logs and the archived literature record. None is typed into this file, "
        "and `report_block_guard` holds that to a snapshot of what the block "
        "actually reads.",
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
        print(json.dumps({"tool": "src47_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src47_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
