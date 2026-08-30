"""Emit RUN-039's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src58_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src58-au2d11.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src58-drill.json"
REPORT = ROOT / "reports" / "RUN-039-HARD-ZETA-AU2D11-MULTISTEP-TRANSPORT.md"
FIGURES = ROOT / "data" / "gate-logs" / "src58-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src58_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    ce, tr, ch = g["certificates"], g["transport"], g["channel"]
    mp, hi, cs = g["mass_and_product"], g["hierarchy"], g["constants"]
    led, ar, tc = g["ledger"], g["artifacts"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The three dual certificates, checked exactly.** A level-`h` "
        "certificate must satisfy `−3a_r + 2^k a_{T(r,k)} + μ_{r,k} ≥ 1` for "
        "every unit `r` mod `3^h` and every `k ≥ 1`. The tail is not assumed: "
        "past `K` with `2^K a_min − 3a_max ≥ 1` the inequality holds from the "
        "transport term alone, and `K` is computed.",
        "",
        "| level | modulus | units | multipliers | declared `tail_k` | computed | inequalities | violations | `α_h` |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in ce["rows"]:
        out.append("| `%d` | `%d` | `%d` | `%d` | `%d` | `%d` | `%d` | `%d` | `%s` |"
                   % (r["level"], r["modulus"], r["units"], r["multipliers"],
                      r["declared_tail_k"], r["tail_settles_from_k"],
                      r["inequalities"], r["violations"], r["alpha"]))
    out += [
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("certificate inequalities checked", "across %d levels" % ce["levels"],
         ce["inequalities_checked"]),
        ("…**violations**", "exact rationals, must be zero",
         ce["certificate_inequality_violations"]),
        ("potentials not positive / multipliers negative",
         "Definition 5.1 requires both",
         "%d / %d" % (ce["potentials_not_positive"], ce["multipliers_negative"])),
        ("units with no potential listed", "the certificate must be total",
         ce["residues_with_no_potential"]),
        ("…**transitions leaving the unit group**",
         "`T(r,k)` must stay coprime to 3, or the transport is not closed",
         ce["transitions_leaving_the_unit_group"]),
        ("multipliers beyond the declared tail", "must be zero",
         ce["multipliers_beyond_the_declared_tail"]),
        ("levels whose computed tail exceeds the declared one",
         "the declared `tail_k` must actually suffice",
         ce["levels_where_the_computed_tail_exceeds_the_declared_one"]),
        ("…**`α` disagreeing with Corollary 5.3**",
         "`α_h = (1/3)Σ μ_{r,k}/(3^h 2^{k+1})`, exactly",
         ce["alpha_disagreeing_with_corollary_5_3"]),
        ("…`A` not three times `α`", "must be zero", ce["A_not_three_times_alpha"]),
        ("…checker report disagreeing with the certificate file",
         "modulus, tail, `A` and `α` compared field by field",
         ce["report_disagreeing_with_the_certificate_file"]),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))
    out += [
        "",
        "The strongest certified exponent is `%s`, which the checker report "
        "agrees with (`%s`), and the exponents decrease with level (`%s`). The "
        "gain over A-U.2d.10 recomputes as `η11 = 4/45 − α = %s`, matching the "
        "reported float (`%s`)."
        % (ce["strongest_certified_alpha"], ce["the_report_agrees_on_the_strongest"],
           ce["the_certified_exponents_decrease_with_level"],
           ce["eta11_recomputed"], ce["eta11_matches_the_reported_float"]),
        "",
        "**Section 3's transport identity and section 4's channel, on real "
        "orbits.**",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("segments from %d orbits" % tr["orbits"],
         "longest `L` = %d" % tr["max_L"], tr["segments"]),
        ("residue transport identities checked",
         "one per unit residue mod 27 per segment",
         tr["residue_identities_checked"]),
        ("…**violations of Theorem 3.1**", "exact Fractions, must be zero",
         tr["transport_identity_violations"]),
        ("…states outside the unit group",
         "A-U.2d.9's sieve, re-verified here",
         tr["states_outside_the_unit_group"]),
        ("…**meeting `z > y`**, the premise Theorem 5.2 needs",
         "a first-crossing endpoint is where the slack drops",
         tr["segments_meeting_the_endpoint_premise_z_above_y"]),
        ("channels checked", "`q(n)=k` and `n≡r (mod 3^h)` by CRT",
         ch["channels_checked"]),
        ("…**not selecting exactly one class mod `3^h 2^{k+1}`**",
         "must be zero", ch["channels_not_selecting_exactly_one_class"]),
        ("…modulus disagreeing with `3^h 2^{k+1}`", "must be zero",
         ch["modulus_disagreeing_with_3h_2k1"]),
        ("…capacity windows / violations of `H_{h,k}`",
         "sorted members of one class, all at least `y`",
         "%d / %d" % (ch["capacity_windows"], ch["capacity_violations"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))
    out += [
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("Theorem 5.2 applied / violated", "premise-gated on `z > y`",
         "%d / %d" % (mp["theorem_5_2_checked"], mp["theorem_5_2_violations"])),
        ("low-source segments `7 ≤ y ≤ L`", "of %d" % mp["segments"],
         mp["low_source_segments_7_le_y_le_L"]),
        ("…**violations of the uniform mod-27 envelope**",
         "`𝒫 < C₁₁(L/y)^{1373/25856}`", mp["uniform_envelope_violations"]),
        ("hierarchy rows read", "section 12's floating diagnostics",
         hi["rows_checked"]),
        ("…where the exponent is not the coefficient over three", "must be zero",
         hi["rows_where_the_exponent_is_not_the_coefficient_over_three"]),
        ("…not decreasing in `h`", "must be zero", hi["rows_not_decreasing_in_h"]),
        ("…**certified levels disagreeing with the diagnostic**",
         "`h = 1, 2, 3` appear in both and must agree",
         hi["certified_levels_disagreeing_with_the_diagnostic"]),
        ("the report labels the floating hierarchy diagnostic-only",
         "its own scope warning", hi["the_report_labels_them_diagnostics_only"]),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**Constants, against their closed forms.**",
        "",
        "| constant | published | closed form | ulps |",
        "| --- | --- | --- | --- |",
    ]
    for name, row in cs["rows"].items():
        out.append("| `%s` | `%s` | `%s` | `%s` |"
                   % (name, row["published"], row["closed_form"],
                      row.get("ulps", "undecided")))
    chain = cs["the_derivation_chain_in_float64"]
    ex = cs["exact_rational_strings_reproduce"]
    out += [
        "",
        "The three exact rational strings the frontier ships reproduce: "
        + ", ".join("`%s` %s" % (k, v) for k, v in ex.items()) + ".",
        "",
        "The chain is shorter this round — the root `C₁₁` is the exact nearest "
        "double and so is `C₁₁/6` — but the last two links still drift, and "
        "reproduce in float64 from the already-rounded parent: `C₁₁/6` gives the "
        "published depth constant (`%s`), that to the `−25856/24483` gives `c₁₁` "
        "(`%s`), and the float64 `θ★` and `α` through `μ11`'s formula give "
        "`μ11` (`%s`)."
        % (chain["C11_depth_is_the_published_C11_over_six_as_doubles"],
           chain["c11_is_the_published_C11_depth_to_the_minus_25856_over_24483"],
           chain["mu11_is_the_float64_theta_and_alpha_put_through_the_formula"]),
        "",
        "| the paper prints | verdict |",
        "| --- | --- |",
    ]
    for name, row in cs["inline_decimals_in_the_paper"].items():
        out.append("| `%s` = `%s…` | %s |" % (name, row["published"],
                                              row["verdict"]))

    out += [
        "",
        "**The manifests.**",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    tail = [
        ("files in the bundle",
         "`CHECKSUMS.sha256` lists %d, the validation record %d"
         % (ar["listed_in_CHECKSUMS"], ar["listed_in_the_validation_record"]),
         ar["files_in_the_bundle"]),
        ("…digests that do not reproduce", "must be zero",
         len(ar["CHECKSUMS_mismatches"]) + len(ar["validation_record_mismatches"])),
        ("**validation records carrying a digest at all**",
         "its fields are %s" % ", ".join("`%s`" % f
                                         for f in ar["validation_record_fields"]),
         ar["validation_records_carrying_a_digest"]),
        ("…listed in the validation record but not in `CHECKSUMS`",
         ", ".join(ar["in_the_validation_record_but_not_CHECKSUMS"]) or "none",
         len(ar["in_the_validation_record_but_not_CHECKSUMS"])),
        ("…**files with no digest anywhere**",
         ", ".join(ar["files_with_no_digest_anywhere"]) or "none",
         len(ar["files_with_no_digest_anywhere"])),
        ("the artifact builder is shipped / has a digest",
         "it generated every other artifact in the bundle",
         "%s / %s" % (ar["the_builder_is_shipped"], ar["the_builder_has_a_digest"])),
        ("the checker's named checks independently confirmed",
         "of %d; %d named as not covered here"
         % (tc["checks_the_report_names"], len(tc["not_covered_by_this_run"])),
         tc["independently_confirmed"]),
        ("this run's own bracket self-checks",
         "%d failed" % len(g["instrument_selfcheck"]["failed"]),
         g["instrument_selfcheck"]["checks"]),
        ("defects planted / caught by the check named for each",
         "%d robustness property; %d malformed; %d controls, %d undisturbed"
         % (d["counts"]["robustness_properties"], d["counts"]["malformed"],
            d["counts"]["controls"], d["counts"]["controls_undisturbed"]),
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in tail:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**The ledger against the paper's own section 17.**",
        "",
        "| the paper says | the JSON ledger says | shortfall |",
        "| --- | --- | --- |",
    ]
    for row in led["table"]:
        out.append("| §%s: `%d` | `%s`: `%s` | `%s` |"
                   % (row["paper_section"], row["paper_items"],
                      row["ledger_key"], row["ledger_items"], row["shortfall"]))
    out += [
        "",
        "The paper carries `%d` `NO-GO` headings (`%s`)."
        % (led["paper_no_go_headings"],
           ", ".join(led["no_go_headings_in_the_paper"])),
        "",
        "**Not covered here**, named rather than implied: "
        + "; ".join("*%s*" % c for c in tc["not_covered_by_this_run"]) + ".",
        "",
        "Every figure above is emitted by `code/src58_emit_report_block.py` from "
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
                          "failures": g.get("failures"),
                          "guards": g.get("non_vacuity_guards")},
                         indent=2, ensure_ascii=False))
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
        print(json.dumps({"tool": "src58_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src58_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
