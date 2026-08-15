"""Mutation drill for src18_hardzeta_au2b1_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The subject publishes a constant to 80 digits and a script that produced it. So
the defects that matter are the ones that would let a *wrong* constant reproduce:
damage to the entropy, to the root-finder, to the variational ratio, and to the
digit-by-digit comparison itself.

Every check must have at least one defect naming it; `audit()` enforces that
before the mutation loop runs. No defect loosens a comparison — that shape has
been a no-op ten times in this arm.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src18_drill.py
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
TOOL = CODE / "src18_hardzeta_au2b1_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b1_bundle.zip"
AU2B1 = "Hard_Zeta_Phase_II_Round_AU2b1_Sharp_Packing_Entropy_Threshold_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.2_AU2b1.md"
CONSTANTS = "Hard_Zeta_AU2b1_packing_entropy_constants.json"
SCRIPT = "verify_Hard_Zeta_AU2b1_packing_entropy.py"
PRED = "Hard_Zeta_Phase_II_Round_AU2b_Sparse_Lift_Rigidity_v0.1.md"
COMPANIONS = ["Hard_Zeta_Phase_II_Round_AU1_bundle.zip",
              "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip",
              "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip"]
TIMEOUT_S = 1500

ACCEL_DEFECTS = [
    ("A01_entropy_adds_where_it_subtracts",
     "SRC18_the_entropy_root_is_bracketed_by_gamma_and_one",
     ("    return ((1 + z) * (1 + z).ln() - z * z.ln()) / ln2",
      "    return ((1 + z) * (1 + z).ln() + z * z.ln()) / ln2")),
    ("A02_entropy_derivative_drops_the_one",
     "SRC18_the_entropy_derivative_is_log_of_one_plus_reciprocal",
     ("    return (1 + 1 / z).ln() / Decimal(2).ln()",
      "    return (1 / z).ln() / Decimal(2).ln()")),
    ("A03_the_root_bisection_moves_the_wrong_end",
     "SRC18_the_bundled_constants_reproduce_under_a_different_method",
     ("        if packing_entropy(mid) < beta:\n            lo = mid\n        else:\n            hi = mid",
      "        if packing_entropy(mid) < beta:\n            hi = mid\n        else:\n            lo = mid")),
    ("A04_the_packing_constant_divides_by_gamma",
     "SRC18_the_variational_supremum_equals_the_published_constant",
     ("    return (entropy_root(digits) - (beta - 1)) / beta",
      "    return (entropy_root(digits) - (beta - 1)) / (beta - 1)")),
    ("A05_the_variational_ratio_is_inverted",
     "SRC18_the_variational_ratio_is_strictly_increasing",
     ("    return x / packing_entropy(beta - 1 + x)",
      "    return packing_entropy(beta - 1 + x) / x")),
    ("A06_the_excess_window_is_one_too_narrow",
     "SRC18_the_block_excess_stays_inside_its_range",
     ("    return max(0, lo_g - D), lo_g + 1 + D",
      "    return max(0, lo_g - D), lo_g + D")),
    ("A07_block_count_A_stops_one_excess_short",
     "SRC18_the_packing_sums_match_a_direct_enumeration",
     ("    return sum(comb(r + E - 1, E) for E in range(lo, hi + 1))",
      "    return sum(comb(r + E - 1, E) for E in range(lo, hi))")),
    # Retargeted: the packing inequality has so much slack at computable sizes
    # that a mis-weighted B still clears it. What it does break is the count.
    ("A08_block_count_B_weights_by_the_wrong_power",
     "SRC18_the_packing_sums_match_a_direct_enumeration",
     ("    return sum(Fraction(comb(r + E - 1, E), 2 ** E) for E in range(lo, hi + 1))",
      "    return sum(Fraction(comb(r + E - 1, E), 2 ** (2 * E)) for E in range(lo, hi + 1))")),
    ("A09_occurrence_counts_keys_on_the_position",
     "SRC18_no_block_recurs_more_often_than_packing_allows",
     ("        blk = q[i:i + r]\n        out[blk] = out.get(blk, 0) + 1",
      "        blk = q[i:i + r] + (i,)\n        out[blk] = out.get(blk, 0) + 1")),
    # Retargeted: with a wrong floor_beta, 2^{floor} != 3^r is still true, so the
    # non-integrality check survives it. The excess window does not.
    ("A10_floor_beta_uses_the_wrong_base",
     "SRC18_the_block_excess_stays_inside_its_range",
     ("        _POW3.append(_POW3[-1] * 3)", "        _POW3.append(_POW3[-1] * 2)")),
    # A defect on block_excess() would be DEAD here — this tool computes the
    # excess from `cumulative` directly and never calls that function. Replaced
    # by one that empties the multi-occurrence term, which the strengthened
    # non-degeneracy guard now sees.
    ("A11_block_count_B_contributes_nothing",
     "SRC18_the_multi_occurrence_packing_inequality_holds",
     ("    return sum(Fraction(comb(r + E - 1, E), 2 ** E) for E in range(lo, hi + 1))",
      "    return Fraction(0) * sum(Fraction(comb(r + E - 1, E), 2 ** E)\n"
      "                             for E in range(lo, hi + 1))")),
    ("A12_deficit_uses_the_wrong_floor",
     "SRC18_the_block_excess_identity_holds",
     ("    return floor_beta(m) - cumulative(accel_code(n, m))[-1]",
      "    return floor_beta(m + 1) - cumulative(accel_code(n, m))[-1]")),
]

TOOL_DEFECTS = [
    # Dropping the digit threshold was a no-op — the eleventh loosening in this
    # arm. Scaling the recomputed constant moves the answer instead.
    ("T01_the_recomputed_constant_is_scaled",
     "SRC18_the_bundled_constants_reproduce_under_a_different_method",
     ('("c_pack", c)):', '("c_pack", c * 2)):')),
    ("T09_the_non_integrality_test_compares_a_thing_to_itself",
     "SRC18_gamma_times_r_is_never_an_integer",
     ("        bad = [r for r in range(1, 200) if 2 ** A.floor_beta(r) == 3 ** r]",
      "        bad = [r for r in range(1, 200) if 3 ** r == 3 ** r]")),
    ("T02_the_entropy_identity_tolerance_is_widened_past_the_claim",
     "SRC18_the_entropy_minus_z_times_its_derivative_is_log_of_one_plus_z",
     ("            rhs = (1 + z).ln() / LN2",
      "            rhs = (1 + z).ln() / LN2 + Decimal(1) / Decimal(10 ** 10)")),
    ("T03_the_bracket_sign_check_reads_the_same_end_twice",
     "SRC18_the_published_root_bracket_really_straddles_the_root",
     ("        s_hi = A.packing_entropy(GAMMA_D + hi) - BETA_D",
      "        s_hi = A.packing_entropy(GAMMA_D + lo) - BETA_D")),
    ("T04_the_safe_witness_reads_the_wrong_exponent",
     "SRC18_the_explicit_safe_constant_satisfies_both_criteria",
     ('        x = Decimal(consts["safe_x"])',
      '        x = Decimal(consts["safe_x"]) * 2')),
    ("T05_the_optimality_probe_stays_inside_the_feasible_side",
     "SRC18_both_sides_of_the_optimality_boundary_really_fail",
     ('        above = x_star * Decimal("1.01")',
      '        above = x_star * Decimal("0.99")')),
    ("T06_the_comparison_uses_the_published_constant_as_the_ceiling",
     "SRC18_the_new_argument_passes_the_previous_schemes_measured_ceiling",
     ('AU2B_SCHEME_CEILING = Decimal("0.015018214488925716")',
      'AU2B_SCHEME_CEILING = Decimal("0.05")')),
    ("T07_the_unproved_list_is_read_from_the_proved_section",
     "SRC18_the_paper_lists_casp_terras_and_collatz_as_unproved",
     ('        tail = au2b1[au2b1.find("## 未證"):] if "## 未證" in au2b1 else ""',
      '        tail = au2b1[au2b1.find("## 已證"):au2b1.find("## 未證")] if "## 未證" in au2b1 else ""')),
    # Reading the JSON instead of the script was a no-op: the JSON carries the
    # same field NAMES, so every key is still found. The route map carries none.
    ("T08_the_script_field_check_reads_the_route_map",
     "SRC18_the_bundled_script_and_json_describe_the_same_quantities",
     ('        src = raw.get(SCRIPT, b"").decode("utf-8")',
      '        src = raw.get(ROUTEMAP, b"").decode("utf-8")')),
]

DOC_DEFECTS = [
    ("D01_route_map_changes_the_published_constant",
     "SRC18_the_route_map_carries_the_same_constant", "constant"),
    ("D02_route_map_loses_its_method_boundary",
     "SRC18_the_paper_states_the_method_boundary", "boundary"),
    ("D03_bundle_edits_the_reshipped_predecessor",
     "SRC18_the_bundle_reships_its_predecessors_unedited", "reship"),
    ("D04_the_constants_json_is_perturbed_in_its_fortieth_digit",
     "SRC18_the_bundled_constants_reproduce_under_a_different_method", "digit"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"constant": ROUTEMAP, "boundary": ROUTEMAP, "reship": PRED,
           "digit": CONSTANTS}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    if kind == "constant":
        t = t.replace("0.03585676003404866", "0.03585676003404867")
    elif kind == "boundary":
        t = t.replace("Method boundary", "Method note", 1)
    elif kind == "reship":
        t = t + "\n<!-- edited inside the AU2b1 bundle -->\n"
    elif kind == "digit":
        # a single digit deep inside c_pack — far past anything a float would see
        rec = json.loads(t)
        c = rec["c_pack"]
        rec["c_pack"] = c[:41] + ("8" if c[41] != "8" else "7") + c[42:]
        t = json.dumps(rec, ensure_ascii=False, indent=2)
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
        "tool": "src18_drill.py",
        "subject": "src18_hardzeta_au2b1_recheck.py and the A-U.2b.1 layer of "
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

        mod = "_drill_accel_null18"
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
        "defects_in_the_au2b1_layer": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_measurement": len(TOOL_DEFECTS),
        "scope_defects_in_the_artifact": len(DOC_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
        "checks_without_a_defect_naming_them": 0,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
