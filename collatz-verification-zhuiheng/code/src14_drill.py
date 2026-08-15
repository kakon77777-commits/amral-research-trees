"""Mutation drill for src14_hardzeta_bline_aline_closure_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Two documents are being graded here and they fail differently. The B-line
handoff is mathematics — its slack algebra is damaged a line at a time. The
A-line closure is a claim about *scope*, so the defects that matter to it are
edits that make it claim more than it has, or that quietly drop the one open
item. Both kinds are planted, plus damage to this run's own measurements and to
the archived record of its external citation.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src14_drill.py
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE = ROOT / "code"
TOOL = CODE / "src14_hardzeta_bline_aline_closure_recheck.py"
ALGEBRA = CODE / "hz_chart_algebra.py"
ACCEL = CODE / "hz_accel_code.py"
EXTERNAL = ROOT / "data" / "external"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
HANDOFF = "Hard_Zeta_B_Line_Handoff_v0.1.md"
BUNDLE = "Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip"
A5 = "Hard_Zeta_Phase_I_Round_03A5_Exceptional_Occupancy_Rigidity_v0.1.md"
CLOSURE = "Hard_Zeta_A_Line_Closure_v1.0.md"
ROUTEMAP = "Hard_Zeta_ROUTE_MAP_v0.8_A_CLOSED.md"
TIMEOUT_S = 1200

ALGEBRA_DEFECTS = [
    ("G01_correction_slack_drops_the_residue",
     "SRC14_the_slack_trichotomy_is_exactly_descent_on_the_least_member",
     ("    return delta_of(w.k, w.u) * nu(w) - w.b",
      "    return delta_of(w.k, w.u) - w.b")),
    ("G02_correction_slack_sign_inverted",
     "SRC14_the_ratio_and_the_integer_slack_classify_identically",
     ("    return delta_of(w.k, w.u) * nu(w) - w.b",
      "    return w.b - delta_of(w.k, w.u) * nu(w)")),
    ("G03_normalized_ratio_forgets_the_drift_gap",
     "SRC14_the_ratio_and_the_integer_slack_classify_identically",
     ("    return Fraction(w.b, delta_of(w.k, w.u) * nu(w))",
      "    return Fraction(w.b, nu(w))")),
    ("G04_b_min_closed_form_wrong",
     "SRC14_b_extremals_match_their_closed_forms",
     ('"b_min_closed": 3 ** u - 2 ** u', '"b_min_closed": 3 ** u - 2 ** (u - 1)')),
    ("G05_b_max_closed_form_loses_its_power_of_two",
     "SRC14_b_extremals_match_their_closed_forms",
     ('"b_max_closed": 2 ** (k - u) * (3 ** u - 2 ** u)',
      '"b_max_closed": 2 ** (k - u - 1) * (3 ** u - 2 ** u)')),
    ("G06_b_extremal_words_swapped",
     "SRC14_b_extremals_match_their_closed_forms",
     ('    lo, hi = word_chart("U" * u + "D" * (k - u)), word_chart("D" * (k - u) + "U" * u)',
      '    lo, hi = word_chart("D" * (k - u) + "U" * u), word_chart("U" * u + "D" * (k - u))')),
    # This prune drops words whose remaining length is exactly the remaining
    # U-count, i.e. every word ending in a run of U — including D^{k-u} U^u, the
    # claimed b-maximiser. So it is the *enumeration* that breaks, and the check
    # that owns the enumeration is the closed-form one. Targeting the witness
    # check instead was wrong: witnesses survive among the words that remain.
    ("G07_words_of_shape_prunes_the_all_up_tail",
     "SRC14_b_extremals_match_their_closed_forms",
     ("        if w.u > u or (u - w.u) > (k - w.k):",
      "        if w.u > u or (u - w.u) >= (k - w.k):")),
    ("G08_nu_takes_the_residue_even_when_it_is_too_small",
     "SRC14_no_member_of_a_first_crossing_cylinder_descends_early",
     ('    return w.r if w.r >= 2 else w.r + 2 ** w.k', '    return w.r')),
]

ACCEL_DEFECTS = [
    ("A01_all_ones_source_off_by_one_power",
     "SRC14_the_all_one_family_has_the_claimed_source_and_offset",
     ("    return 2 ** (m + 1) - 1", "    return 2 ** m - 1")),
    ("A02_all_ones_offset_wrong_base",
     "SRC14_the_all_one_family_has_the_claimed_source_and_offset",
     ("    return 3 ** m - 2 ** m", "    return 3 ** m - 2 ** (m + 1)")),
    ("A03_code_lifts_use_the_wrong_modulus",
     "SRC14_every_finite_code_is_realized_by_infinitely_many_positive_integers",
     ("    r, step = source_residue(kappa), 1 << (cumulative(kappa)[-1] + 1)",
      "    r, step = source_residue(kappa), 1 << cumulative(kappa)[-1]")),
    ("A04_occupancy_counts_the_wrong_side_of_the_threshold",
     "SRC14_arbitrarily_long_zero_occupancy_prefixes_exist",
     ("    return sum(1 for q in orbit_valuations(n, m) if q >= r)",
      "    return sum(1 for q in orbit_valuations(n, m) if q >= r - 1)")),
    ("A05_excess_forgets_to_subtract_the_step_count",
     "SRC14_the_saturation_shortfall_is_exactly_the_budget_minus_the_deficit",
     ("    return cumulative(accel_code(n, m))[-1] - m",
      "    return cumulative(accel_code(n, m))[-1]")),
    ("A06_truncated_occupancy_clips_at_the_wrong_level",
     "SRC14_the_occupancy_tail_split_is_an_exact_identity",
     ("    return Fraction(sum(min(q - 1, R - 1) for q in orbit_valuations(n, m)), m)",
      "    return Fraction(sum(min(q - 1, R) for q in orbit_valuations(n, m)), m)")),
    ("A07_tail_leakage_measures_from_the_wrong_level",
     "SRC14_the_occupancy_tail_split_is_an_exact_identity",
     ("    return Fraction(sum(max(q - R, 0) for q in orbit_valuations(n, m)), m)",
      "    return Fraction(sum(max(q - R - 1, 0) for q in orbit_valuations(n, m)), m)")),
    ("A08_tail_leakage_saturates_and_hides_the_top",
     "SRC14_the_tail_leakage_observable_is_nonempty_only_below_the_top_valuation",
     ("    return Fraction(sum(max(q - R, 0) for q in orbit_valuations(n, m)), m)",
      "    return Fraction(0, m)")),
    ("A09_shortcut_parity_labels_the_odd_branch_D",
     "SRC14_the_accelerated_endpoint_carries_exactly_m_up_steps",
     ('            out.append("U")\n            x = (3 * x + 1) // 2',
      '            out.append("D")\n            x = (3 * x + 1) // 2')),
    ("A10_shortcut_parity_uses_the_unshortcut_step",
     "SRC14_the_parity_ratio_bottoms_out_at_block_ends",
     ("            x = (3 * x + 1) // 2", "            x = 3 * x + 1")),
    ("A11_u_count_reads_one_symbol_too_many",
     "SRC14_the_accelerated_endpoint_carries_exactly_m_up_steps",
     ('    return word[:ell].count("U")', '    return word[:ell + 1].count("U")')),
]

TOOL_DEFECTS = [
    ("T01_run_006s_recorded_value_transcribed_wrong",
     "SRC14_the_slack_form_reproduces_run_006s_measured_binding_ratio",
     ('got == Fraction(19, 39)', 'got == Fraction(19, 38)')),
    # Loosening the threshold here is a NO-OP, for the same reason `<` vs `<=` has
    # been five times in this arm: the real data clears `top_k <= 8` and the
    # tenfold gap with room to spare, so widening either bound changes no verdict.
    # Retired in favour of damaging the aggregation that produces the per-length
    # maxima, which moves the argmax and therefore the answer.
    ("T02_per_length_maxima_accumulate_instead_of_maximising",
     "SRC14_the_ratio_supremum_is_attained_at_a_short_word",
     ("per[w.k] = max(per.get(w.k, Fraction(0)), r)",
      "per[w.k] = per.get(w.k, Fraction(0)) + r")),
    ("T03_the_witness_search_starts_above_the_cheapest_start",
     "SRC14_the_finite_local_witness_is_exponentially_far_from_the_minimal_one",
     ("for n in range(3, 200000, 2)", "for n in range(3, 5, 2)")),
    # §11's warning has a check of its own, so it needs a defect of its own: make
    # the slack-minimiser be the b-maximiser by construction, and the witness set
    # empties out.
    ("T05_the_witness_search_picks_the_b_extremal_by_construction",
     "SRC14_b_extremal_is_not_slack_extremal",
     ("                s = min(fam, key=C.correction_slack).word",
      "                s = max(fam, key=lambda w: w.b).word")),
    ("T04_the_reduction_map_loses_an_entry",
     "SRC14_every_completed_reduction_maps_to_a_report_in_this_tree",
     ('"unique zero-lift spine": "RUN-010-HARD-ZETA-ROUND-03A3.md",',
      '"unique zero-lift spinal": "RUN-010-HARD-ZETA-ROUND-03A3.md",')),
]

# Damage to the archived record of the external citation: the check must not
# pass just because a file with the right name is present.
EXTERNAL_DEFECTS = [
    ("E01_archived_abstract_no_longer_states_the_equality",
     "SRC14_the_lopez_stoll_citation_resolves_to_the_claimed_statement",
     "abstract"),
    ("E02_archived_record_drops_the_liminf_symbol",
     "SRC14_the_lopez_stoll_citation_resolves_to_the_claimed_statement",
     "liminf"),
]

# Scope defects: edits that make the closure claim more than it has.
DOC_DEFECTS = [
    ("D01_closure_drops_its_disclaimer",
     "SRC14_the_closure_declines_to_claim_a_proof", "disclaimer"),
    ("D02_closure_promotes_the_incorrect_statement_to_correct",
     "SRC14_the_closure_declines_to_claim_a_proof", "promote"),
    ("D03_a5_ledger_loses_its_open_item",
     "SRC14_the_closure_ledger_lists_casp_as_the_single_open_item", "open"),
    ("D04_a5_drops_a_completed_reduction",
     "SRC14_every_completed_reduction_maps_to_a_report_in_this_tree", "reduction"),
    ("D05_route_map_and_closure_disagree",
     "SRC14_the_route_map_and_the_closure_state_the_same_obstruction", "routemap"),
    ("D08_complete_bundle_edits_a_reshipped_round",
     "SRC14_the_complete_bundle_reships_the_rounds_unedited", "reship"),
    ("D06_handoff_loses_its_no_gos",
     "SRC14_the_handoff_states_its_own_no_gos", "nogo"),
    ("D07_handoff_loses_its_settled_list",
     "SRC14_the_handoff_lists_what_must_not_be_reasked", "settled"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    if kind in ("nogo", "settled"):
        p = src / HANDOFF
        t = p.read_text(encoding="utf-8")
        if kind == "nogo":
            t = t.replace("No-Go", "Note")
        else:
            t = t.replace("不應再重問的問題", "附錄", 1)
        p.write_text(t, encoding="utf-8")
        return
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"disclaimer": CLOSURE, "promote": CLOSURE, "open": A5,
           "reduction": A5, "routemap": ROUTEMAP,
           "reship": "Hard_Zeta_Phase_I_Round_03A4_Spine_Valuation_Rigidity_v0.1.md"}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    if kind == "disclaimer":
        t = t.replace("**未宣稱：**", "**備註：**", 1)
    elif kind == "promote":
        t = t.replace("Incorrect statement", "Also correct", 1)
    elif kind == "open":
        t = t.replace("\\text{CASP exclusion}", "\\text{nothing further}", 1)
    elif kind == "reduction":
        t = t.replace("- unique zero-lift spine；", "", 1)
    elif kind == "routemap":
        t = t.replace("finite forbidden-pattern", "finite pattern", 1)
    elif kind == "reship":
        # a silent edit to a round this arm already verified in its own bundle
        t = t + "\n<!-- edited inside the COMPLETE bundle -->\n"
    keep[name] = t.encode("utf-8")
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def mutate_external(dst: pathlib.Path, kind: str) -> None:
    p = dst / "lopez-stoll-arxiv-2101.12747.json"
    rec = json.loads(p.read_text(encoding="utf-8"))
    if kind == "abstract":
        rec["abstract_sentence_supporting_it"] = (
            "We study the 3x+1 map on the 2-adic integers.")
    elif kind == "liminf":
        rec["abstract_sentence_supporting_it"] = rec[
            "abstract_sentence_supporting_it"].replace("\\lim", "sum")
    p.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    rep = {
        "tool": "src14_drill.py",
        "subject": "src14_hardzeta_bline_aline_closure_recheck.py, the B-line slack "
                   "layer of hz_chart_algebra.py, the A.5 occupancy layer of "
                   "hz_accel_code.py, and the archived López–Stoll record",
        "defects": {}, "controls": {},
    }
    original = {ALGEBRA: ALGEBRA.read_text(encoding="utf-8"),
                ACCEL: ACCEL.read_text(encoding="utf-8")}
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, *, algebra="hz_chart_algebra", accel="hz_accel_code",
            external=EXTERNAL) -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ALGEBRA_MODULE": algebra, "HZ_ACCEL_MODULE": accel,
               "HZ_EXTERNAL_DIR": str(external)}
        try:
            out = subprocess.run([sys.executable, str(tool)], capture_output=True,
                                 text=True, encoding="utf-8", timeout=TIMEOUT_S,
                                 env=env)
        except subprocess.TimeoutExpired:
            return {"ok": False, "checks": {}, "_crash": "timed out"}
        try:
            return json.loads(out.stdout)
        except json.JSONDecodeError:
            return {"ok": False, "checks": {},
                    "_crash": (out.stdout + out.stderr)[-400:]}

    def record(name, target, res):
        checks = res.get("checks", {})
        rep["defects"][name] = {
            "target_check": target,
            "caught_by_the_named_check": target in checks and not checks[target]["pass"],
            "run_went_red": not res.get("ok", True),
            "other_checks_that_also_fired": sorted(
                k for k, v in checks.items() if not v["pass"] and k != target),
            **({"crash": res["_crash"]} if "_crash" in res else {}),
        }

    def absent(name, target, anchor):
        rep["defects"][name] = {
            "target_check": target, "caught_by_the_named_check": False,
            "run_went_red": False, "other_checks_that_also_fired": [],
            "crash": f"anchor {anchor!r} absent; nothing was tested"}

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        base = tmp / "source"
        base.mkdir()
        shutil.copy2(SOURCE / BUNDLE, base / BUNDLE)
        shutil.copy2(SOURCE / HANDOFF, base / HANDOFF)
        # the faithfulness check compares the COMPLETE bundle against these
        for p in sorted(SOURCE.glob("Hard_Zeta_Phase_I_Round_*_bundle.zip")):
            shutil.copy2(p, base / p.name)

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

        for path, defects, prefix in ((ALGEBRA, ALGEBRA_DEFECTS, "algebra"),
                                      (ACCEL, ACCEL_DEFECTS, "accel")):
            for name, target, (old, new) in defects:
                if old not in original[path]:
                    absent(name, target, old)
                    continue
                mod = f"_drill_{prefix}_{name}"
                f = CODE / f"{mod}.py"
                try:
                    f.write_text(original[path].replace(old, new, 1), encoding="utf-8")
                    kw = ({"algebra": mod} if prefix == "algebra" else {"accel": mod})
                    record(name, target, run(base, TOOL, **kw))
                finally:
                    f.unlink(missing_ok=True)

        for name, target, (old, new) in TOOL_DEFECTS:
            if old not in original_tool:
                absent(name, target, old)
                continue
            f = CODE / f"_drill_mutant_{name}.py"
            try:
                f.write_text(original_tool.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, f))
            finally:
                f.unlink(missing_ok=True)

        for name, target, kind in EXTERNAL_DEFECTS:
            d = tmp / f"ext_{name}"
            shutil.copytree(EXTERNAL, d)
            mutate_external(d, kind)
            record(name, target, run(base, TOOL, external=d))
            shutil.rmtree(d, ignore_errors=True)

        for name, target, kind in DOC_DEFECTS:
            s = tmp / f"src_{name}"
            shutil.copytree(base, s)
            mutate_docs(s, kind)
            record(name, target, run(s, TOOL))
            shutil.rmtree(s, ignore_errors=True)

        mod = "_drill_accel_null14"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original[ACCEL] + "\n# a comment nothing reads\n",
                         encoding="utf-8")
            res = run(base, TOOL, accel=mod)
        finally:
            f.unlink(missing_ok=True)
        rep["controls"]["N01_accel_module_annotated_where_nothing_reads"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

        s = tmp / "src_null"
        shutil.copytree(base, s)
        (s / "UNREAD.txt").write_text("read by nothing\n", encoding="utf-8")
        res = run(s, TOOL)
        rep["controls"]["N02_unrelated_file_beside_the_sources"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

        d = tmp / "ext_null"
        shutil.copytree(EXTERNAL, d)
        (d / "unrelated.json").write_text("{}\n", encoding="utf-8")
        res = run(base, TOOL, external=d)
        rep["controls"]["N03_unrelated_file_beside_the_citation_record"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(rep["defects"]),
        "defects_caught_by_the_named_check": caught,
        "defects_in_the_b_line_slack_layer": len(ALGEBRA_DEFECTS),
        "defects_in_the_a5_occupancy_layer": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_measurement": len(TOOL_DEFECTS),
        "defects_in_the_archived_citation": len(EXTERNAL_DEFECTS),
        "scope_defects_in_the_documents": len(DOC_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
