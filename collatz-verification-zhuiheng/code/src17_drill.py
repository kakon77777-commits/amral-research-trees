"""Mutation drill for src17_hardzeta_au2b_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

A-U.2b is the first positive round of Phase II, so the defects that matter most
are the ones that would let a *wrong* constant through: the entropy base, the
admissible interval, and the two explicit inequalities behind the published
`0.01`. Those clear by margins of 1e-4 and 6e-4, so each is drilled by a
perturbation smaller than the claim it supports.

Every check must have at least one defect naming it; `audit()` enforces that
before the mutation loop runs. No defect here loosens a comparison — that shape
has been a no-op nine times in this arm and is not used again.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src17_drill.py
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
TOOL = CODE / "src17_hardzeta_au2b_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip"
AU2B = "Hard_Zeta_Phase_II_Round_AU2b_Sparse_Lift_Rigidity_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.1_AU2b.md"
PRED = "Hard_Zeta_Phase_II_Round_AU2a_Lift_Occupation_Coupling_v0.1.md"
COMPANIONS = ["Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip",
              "Hard_Zeta_Phase_II_Round_AU1_bundle.zip",
              "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip"]
TIMEOUT_S = 1500

ACCEL_DEFECTS = [
    ("A01_orbit_endpoints_starts_after_the_first_step",
     "SRC17_a_repeated_exponent_block_forces_a_congruence",
     ("    out, x = [n], n", "    out, x = [], n")),
    # Retargeted: min instead of max leaves the tradeoff intact, because its
    # right-hand side is negative at small r. It breaks the barrier contrast.
    ("A02_record_deficit_takes_the_minimum",
     "SRC17_real_starts_clear_the_barrier_and_only_the_countermodel_does_not",
     ("    return max(deficit(n, m) for m in range(1, N + 1))",
      "    return min(deficit(n, m) for m in range(1, N + 1))")),
    ("A03_factor_complexity_counts_positions_not_factors",
     "SRC17_the_mechanical_code_has_sturmian_complexity",
     ("    return len({word[j:j + r] for j in range(len(word) - r + 1)})",
      "    return len([word[j:j + r] for j in range(len(word) - r + 1)])")),
    ("A04_block_excess_forgets_the_minus_one",
     "SRC17_the_block_excess_ledger_telescopes",
     ("    return sum(x - 1 for x in q[i:i + r])",
      "    return sum(x for x in q[i:i + r])")),
    ("A05_composition_count_uses_the_wrong_binomial",
     "SRC17_the_composition_count_matches_a_direct_enumeration",
     ("    return comb(r + E - 1, E)", "    return comb(r + E, E)")),
    ("A06_entropy_base_drops_the_denominator",
     "SRC17_the_entropy_constant_matches_and_is_below_three",
     ("    return ((1 + g) * (1 + g).ln() - g * g.ln()).exp()",
      "    return ((1 + g) * (1 + g).ln()).exp()")),
    # Retargeted: the interval check uses the tool's own BETA_D; gamma_decimal()
    # is read only by the entropy constant.
    ("A07_gamma_decimal_is_not_shifted",
     "SRC17_the_entropy_constant_matches_and_is_below_three",
     ("    return Decimal(3).ln() / Decimal(2).ln() - 1",
      "    return Decimal(3).ln() / Decimal(2).ln()")),
    ("A08_periodic_tail_source_inverts_its_denominator",
     "SRC17_an_ultimately_periodic_subcritical_tail_has_a_negative_source",
     ("    return Fraction(offset(v), 2 ** Q - 3 ** pp)",
      "    return Fraction(offset(v), 3 ** pp - 2 ** Q)")),
    ("A09_cycle_test_compares_the_wrong_way",
     "SRC17_a_positive_cycle_requires_a_supercritical_period",
     ("    return 2 ** cumulative(v)[-1] > 3 ** len(v)",
      "    return 2 ** cumulative(v)[-1] < 3 ** len(v)")),
    ("A10_deficit_uses_the_wrong_floor",
     "SRC17_the_deficit_recurrence_holds",
     ("    return floor_beta(m) - cumulative(accel_code(n, m))[-1]",
      "    return floor_beta(m + 1) - cumulative(accel_code(n, m))[-1]")),
    ("A11_mechanical_code_shifts_its_index",
     "SRC17_the_mechanical_code_has_identically_zero_deficit",
     ("    return tuple(floor_beta(j) - floor_beta(j - 1) for j in range(1, m + 1))",
      "    return tuple(floor_beta(j + 1) - floor_beta(j) for j in range(1, m + 1))")),
    ("A12_floor_beta_uses_the_wrong_base",
     "SRC17_return_separation_operates_at_base_three",
     ("    return (3 ** j).bit_length() - 1", "    return (4 ** j).bit_length() - 1")),
    ("A13_anchor_cocycle_reports_no_lifts",
     "SRC17_two_independent_routes_agree_the_mechanical_code_is_unanchored",
     ("    return [lift_digit(kappa[:j]) for j in range(1, len(kappa) + 1)]",
      "    return [0 for j in range(1, len(kappa) + 1)]")),
    # Retargeted: a shorter lifetime gives shorter orbits and therefore FEWER
    # repeats, so the no-repeat check survives it.
    ("A14_subcritical_lifetime_stops_one_step_early",
     "SRC17_the_complexity_peak_law_holds_on_real_spines",
     ("def subcritical_lifetime(n: int, limit: int = 400) -> int:",
      "def subcritical_lifetime(n: int, limit: int = 3) -> int:")),
    # Retargeted: the excursion bound reads the deficit and the endpoints, never
    # the valuation list.
    ("A15_orbit_valuations_shifts_by_one",
     "SRC17_the_block_excess_ledger_telescopes",
     ("    return list(accel_code(n, m))", "    return [x + 1 for x in accel_code(n, m)]")),
    ("A16_orbit_endpoints_never_advances",
     "SRC17_no_state_repeats_on_a_subcritical_spine",
     ("        x = y >> ((y & -y).bit_length() - 1)\n        out.append(x)\n    return out",
      "        x = y >> ((y & -y).bit_length() - 1)\n        out.append(n)\n    return out")),
]

TOOL_DEFECTS = [
    # each constant is perturbed by LESS than the margin it is claimed to clear,
    # so the check must be reading the real value rather than a rounded one
    ("T01_the_first_inequality_bound_is_transcribed_high",
     "SRC17_the_first_explicit_inequality_clears",
     ('return (val > Decimal("0.0022")), {',
      'return (val > Decimal("0.0024")), {')),
    ("T02_the_second_inequality_bound_is_transcribed_low",
     "SRC17_the_second_explicit_inequality_clears",
     ('return (val < Decimal("0.986")), {',
      'return (val < Decimal("0.9851")), {')),
    ("T03_the_c_used_in_the_inequalities_drifts",
     "SRC17_the_first_explicit_inequality_clears",
     ('        c, eps = Decimal("0.645"), Decimal("0.01")\n        val = BETA_D * c - 1 - 2 * eps',
      '        c, eps = Decimal("0.6300"), Decimal("0.01")\n        val = BETA_D * c - 1 - 2 * eps')),
    ("T04_the_entropy_prefix_is_transcribed_wrong",
     "SRC17_the_entropy_constant_matches_and_is_below_three",
     ('claimed = "2.8395137304"', 'claimed = "2.8395137305"')),
    ("T05_the_separation_check_compares_the_wrong_pair",
     "SRC17_repeated_blocks_force_the_states_to_separate",
     ("                        if abs(Y[a] - Y[b]) < 2 ** (Q + 1):",
      "                        if abs(Y[a] - Y[a]) < 2 ** (Q + 1):")),
    # Reading the WHOLE orbit was a no-op — max(Y) >= max(Y[:N]) makes the
    # failure condition harder, not easier. Shrinking the window moves it.
    ("T06_the_peak_law_reads_only_the_first_state",
     "SRC17_the_complexity_peak_law_holds_on_real_spines",
     ("                if max(Y[:N]) < 2 ** (r + 1):",
      "                if max(Y[:1]) < 2 ** (r + 1):")),
    ("T11_the_tradeoff_sign_is_transcribed_wrong",
     "SRC17_the_complexity_deficit_tradeoff_holds",
     ("                rhs = r - math.log2(n + N / 3)",
      "                rhs = r + math.log2(n + N / 3)")),
    # Retargeted: flipping the sign makes log2(Lambda) SMALLER (0.6006 instead of
    # 1.5057), so the interval's upper end moves out to 1.665 and c = 0.645 is
    # still inside — the interval widens rather than emptying. What it does move
    # is the ceiling search.
    ("T12_the_entropy_logarithm_adds_where_it_subtracts",
     "SRC17_the_published_constant_is_below_this_schemes_ceiling",
     ("    return ((1 + g) * (1 + g).ln() - g * g.ln()) / LN2",
      "    return ((1 + g) * (1 + g).ln() + g * g.ln()) / LN2")),
    ("T14_the_interval_lower_end_uses_gamma_instead_of_beta",
     "SRC17_the_admissible_c_interval_is_nonempty",
     ("        lo = 1 / BETA_D", "        lo = 1 / GAMMA_D")),
    ("T13_the_excursion_bound_is_tightened_past_the_truth",
     "SRC17_the_exact_excursion_upper_bound_holds",
     ("                if not (Y[m] < 2 ** (d + 1) * (n + Fraction(m, 3))):",
      "                if not (Y[m] < 2 ** (d - 1) * (n + Fraction(m, 3))):")),
    ("T07_the_thin_range_uses_the_wrong_record",
     "SRC17_thin_deficit_blocks_stay_in_their_range",
     ("            D = A.record_deficit(n, life)\n            g = math.log2(3) - 1",
      "            D = 0\n            g = math.log2(3) - 1")),
    ("T08_the_ceiling_search_scans_the_wrong_window",
     "SRC17_the_published_constant_is_below_this_schemes_ceiling",
     ('        c = Decimal("0.60")\n        while c < Decimal("0.70"):',
      '        c = Decimal("0.10")\n        while c < Decimal("0.20"):')),
    ("T09_the_contrast_reads_a_real_start_as_the_countermodel",
     "SRC17_real_starts_clear_the_barrier_and_only_the_countermodel_does_not",
     ("        mech = A.mechanical_code(400)\n        mech_D = max(",
      "        mech = A.accel_code(27, 30)\n        mech_D = max(")),
    ("T10_the_limits_section_stops_requiring_the_conjecture",
     "SRC17_the_paper_states_what_it_does_not_prove",
     ('        tail = au2b[au2b.find("# 36."):] if "# 36." in au2b else ""',
      '        tail = au2b[au2b.find("# 35."):au2b.find("# 36.")] if "# 36." in au2b else ""')),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_limits_section",
     "SRC17_the_paper_states_what_it_does_not_prove", "limits"),
    ("D02_route_map_loses_an_eliminated_class",
     "SRC17_the_route_map_and_the_paper_agree_on_the_eliminated_classes", "classes"),
    ("D03_route_map_changes_the_published_constant",
     "SRC17_the_route_map_and_the_paper_agree_on_the_eliminated_classes", "constant"),
    ("D04_bundle_edits_the_reshipped_predecessor",
     "SRC17_the_bundle_reships_its_predecessors_unedited", "reship"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"limits": AU2B, "classes": ROUTEMAP, "constant": ROUTEMAP,
           "reship": PRED}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    if kind == "limits":
        head, _, tail = t.partition("# 36.")
        t = head + "# 36." + tail.replace("Collatz", "後續", 1)
    elif kind == "classes":
        t = t.replace("mechanical critical code", "mechanical critical note")
    elif kind == "constant":
        t = t.replace("0.01", "0.02")
    elif kind == "reship":
        t = t + "\n<!-- edited inside the AU2b bundle -->\n"
    keep[name] = t.encode("utf-8")
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def audit(baseline: dict) -> list[str]:
    targeted = ({t for _, t, _ in ACCEL_DEFECTS} | {t for _, t, _ in TOOL_DEFECTS}
                | {t for _, t, _ in DOC_DEFECTS})
    names = set(baseline.get("checks", {}))
    return sorted([f"unguarded check: {c}" for c in names - targeted]
                  + [f"defect names a check that does not exist: {t}"
                     for t in targeted - names])


def main() -> int:
    rep = {
        "tool": "src17_drill.py",
        "subject": "src17_hardzeta_au2b_recheck.py and the A-U.2b layer of "
                   "hz_accel_code.py",
        "defects": {}, "controls": {}, "audit": [],
    }
    original_accel = ACCEL.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, accel="hz_accel_code") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ACCEL_MODULE": accel}
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
        c = res.get("checks", {})
        rep["defects"][name] = {
            "target_check": target,
            "caught_by_the_named_check": target in c and not c[target]["pass"],
            "run_went_red": not res.get("ok", True),
            "other_checks_that_also_fired": sorted(
                k for k, v in c.items() if not v["pass"] and k != target),
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
        for c in COMPANIONS:
            shutil.copy2(SOURCE / c, base / c)

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2
        rep["audit"] = audit(baseline)
        if rep["audit"]:
            print(json.dumps({"error": "coverage audit failed before the drill ran",
                              "audit": rep["audit"]}, indent=2, ensure_ascii=False))
            return 3

        for name, target, (old, new) in ACCEL_DEFECTS:
            if old not in original_accel:
                absent(name, target, old)
                continue
            mod = f"_drill_accel_{name}"
            f = CODE / f"{mod}.py"
            try:
                f.write_text(original_accel.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, TOOL, accel=mod))
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

        for name, target, kind in DOC_DEFECTS:
            s = tmp / f"src_{name}"
            shutil.copytree(base, s)
            mutate_docs(s, kind)
            record(name, target, run(s, TOOL))
            shutil.rmtree(s, ignore_errors=True)

        mod = "_drill_accel_null17"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original_accel + "\n# a comment nothing reads\n",
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
        rep["controls"]["N02_unrelated_file_beside_the_bundle"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(rep["defects"]),
        "defects_caught_by_the_named_check": caught,
        "defects_in_the_au2b_layer": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_measurement": len(TOOL_DEFECTS),
        "scope_defects_in_the_documents": len(DOC_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
        "checks_without_a_defect_naming_them": 0,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
