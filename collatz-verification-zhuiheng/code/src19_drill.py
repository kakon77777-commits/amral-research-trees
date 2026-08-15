"""Mutation drill for src19_hardzeta_au2b2_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The load-bearing object here is a dynamic program, so the defects that matter
most damage the DP a line at a time — the corridor, the credit word, the
direction of accumulation — and the second-order constants that the Stirling
prefactor buys.

Every check must have at least one defect naming it; `audit()` enforces that
before the mutation loop runs. No defect loosens a comparison: that shape has
been a no-op eleven times in this arm.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src19_drill.py
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
TOOL = CODE / "src19_hardzeta_au2b2_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b2_bundle.zip"
AU2B2 = "Hard_Zeta_Phase_II_Round_AU2b2_Queue_Entropy_Second_Order_Barrier_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.3_AU2b2.md"
CONSTANTS = "Hard_Zeta_AU2b2_constants_and_queue.json"
SCRIPT = "verify_Hard_Zeta_AU2b2_queue_second_order.py"
PRED = "Hard_Zeta_Phase_II_Round_AU2b1_Sharp_Packing_Entropy_Threshold_v0.1.md"
COMPANIONS = ["Hard_Zeta_Phase_II_Round_AU1_bundle.zip",
              "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip",
              "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip",
              "Hard_Zeta_Phase_II_Round_AU2b1_bundle.zip"]
TIMEOUT_S = 1800

ACCEL_DEFECTS = [
    ("A01_the_credit_is_taken_across_two_steps",
     "SRC19_the_phase_resolved_credit_is_always_a_single_bit",
     ("    return fl(phase + j) - fl(phase + j - 1)",
      "    return fl(phase + j) - fl(phase + j - 2)")),
    ("A02_the_credit_floor_uses_beta_not_gamma",
     "SRC19_the_credit_prefix_stays_within_one_of_gamma_s",
     ("        return floor_beta(k) - k if k else 0",
      "        return floor_beta(k) if k else 0")),
    ("A03_the_dp_accumulates_in_the_wrong_direction",
     "SRC19_the_queue_dp_matches_a_direct_enumeration",
     ("        vec = [total - pref[max(0, t - b)] for t in range(D + 1)]",
      "        vec = [pref[max(0, t - b)] for t in range(D + 1)]")),
    ("A04_the_dp_ignores_the_credit",
     "SRC19_every_published_queue_row_reproduces_under_an_independent_dp",
     ("        vec = [total - pref[max(0, t - b)] for t in range(D + 1)]",
      "        vec = [total - pref[t] for t in range(D + 1)]")),
    ("A05_the_dp_corridor_is_one_too_wide",
     "SRC19_the_queue_dp_matches_a_direct_enumeration",
     ("    vec = [1] * (D + 1)\n    for j in range(1, r + 1):\n        b = phase_credit(j, phase)",
      "    vec = [1] * (D + 2)\n    for j in range(1, r + 1):\n        b = phase_credit(j, phase)")),
    # Widening the guard to -1 is a NO-OP: the e-loop stops at d+b, so nd is
    # never negative and the guard has nothing to catch. The two are redundant
    # with each other. Excluding e = 0 removes real paths instead.
    ("A06_the_bruteforce_forbids_a_zero_excess",
     "SRC19_the_queue_dp_matches_a_direct_enumeration",
     ("        for e in range(0, d + b + 1):",
      "        for e in range(1, d + b + 1):")),
    ("A07_floor_beta_uses_the_wrong_base",
     "SRC19_the_subjects_float_floor_agrees_with_exact_arithmetic",
     ("    return (3 ** j).bit_length() - 1", "    return (4 ** j).bit_length() - 1")),
    ("A08_the_entropy_derivative_drops_the_one",
     "SRC19_the_second_order_constants_reproduce_independently",
     ("    _HPRIME_CACHE[digits] = (1 + 1 / z).ln() / Decimal(2).ln()",
      "    _HPRIME_CACHE[digits] = (1 / z).ln() / Decimal(2).ln()")),
    ("A09_the_second_order_constant_forgets_its_half",
     "SRC19_the_block_scale_optimum_sits_at_the_published_constant",
     ("    return 1 / (2 * entropy_derivative_at_root(digits))",
      "    return 1 / entropy_derivative_at_root(digits)")),
    ("A10_the_first_block_scale_exponent_loses_its_drift",
     "SRC19_each_block_scale_exponent_binds_on_its_own_side",
     ("    p1 = h * d + s * (beta - h * x) - Decimal(\"0.5\")",
      "    p1 = h * d - Decimal(\"0.5\")")),
    ("A11_the_second_block_scale_exponent_loses_its_drift",
     "SRC19_each_block_scale_exponent_binds_on_its_own_side",
     ("    p2 = h * (d - x * s) - Decimal(\"0.5\")",
      "    p2 = h * d - Decimal(\"0.5\")")),
    ("A12_the_entropy_root_bisects_the_wrong_way",
     "SRC19_the_safe_second_order_constant_clears_its_criterion",
     ("        if packing_entropy(mid) < beta:\n            lo = mid\n        else:\n            hi = mid",
      "        if packing_entropy(mid) < beta:\n            hi = mid\n        else:\n            lo = mid")),
]

TOOL_DEFECTS = [
    ("T01_the_table_tolerance_is_read_from_the_wrong_column",
     "SRC19_every_published_queue_row_reproduces_under_an_independent_dp",
     ('            rate = lg / r', '            rate = lg / (r + 1)')),
    ("T02_the_corridor_rule_uses_the_wrong_constant",
     "SRC19_each_published_row_uses_the_corridor_its_length_implies",
     ("        x = float(A.entropy_root(DIGITS) - GAMMA_D)",
      "        x = float(A.entropy_root(DIGITS))")),
    ("T03_the_excess_identity_drops_the_starting_deficit",
     "SRC19_the_block_excess_equals_the_credit_prefix_plus_the_queue_drop",
     ("                    if E != B + D - d:", "                    if E != B - d:")),
    ("T04_the_saturation_check_reads_the_gaps_backwards",
     "SRC19_the_queue_entropy_rate_climbs_toward_beta",
     ("        gaps = [beta_f - r[\"rate\"] for r in rows]",
      "        gaps = [r[\"rate\"] - beta_f for r in rows]")),
    ("T05_the_ratio_check_uses_a_range_where_it_is_false",
     "SRC19_the_composition_ratios_are_below_one_in_the_relevant_range",
     ("            for E in (int(0.6 * r), int(0.64 * r)):",
      "            for E in (int(6 * r), int(6.4 * r)):")),
    # Reading d_pack as the safe constant is a NEAR-TIE, not a defect: h * d_pack
    # comes out 0.4999999999999999999999 by rounding, so it clears `< 0.5`. A
    # value genuinely above the threshold moves the answer.
    ("T06_the_safe_constant_is_read_above_its_threshold",
     "SRC19_the_safe_second_order_constant_clears_its_criterion",
     ('        safe = Decimal(consts["safe_second_order_constant"])',
      '        safe = Decimal("0.4")')),
    ("T07_the_optimum_scan_only_looks_at_positive_shifts",
     "SRC19_the_block_scale_optimum_sits_at_the_published_constant",
     ('        s = Decimal("-0.5")\n        step = Decimal("0.002")',
      '        s = Decimal("0.1")\n        step = Decimal("0.002")')),
    ("T08_the_pairing_check_reads_the_wrong_marker",
     "SRC19_the_json_covers_everything_the_script_would_emit",
     ('            if "for r in [" in line:', '            if "for q in [" in line:')),
    ("T09_the_unproved_list_is_read_from_the_proved_section",
     "SRC19_the_paper_lists_casp_terras_and_collatz_as_unproved",
     ('        tail = au2b2[au2b2.find("## 未證"):] if "## 未證" in au2b2 else ""',
      '        tail = au2b2[au2b2.find("## 已證"):au2b2.find("## 未證")] if "## 未證" in au2b2 else ""')),
    ("T10_the_lever_measurement_reads_the_first_row",
     "SRC19_the_queue_lever_gave_no_first_order_gain",
     ('        return (rows and abs(rows[-1]["rate"] - float(BETA_D)) < 0.01',
      '        return (rows and abs(rows[0]["rate"] - float(BETA_D)) < 0.01')),
]

DOC_DEFECTS = [
    ("D01_route_map_loses_the_second_order_constant",
     "SRC19_the_route_map_carries_both_constants", "constant"),
    ("D02_route_map_and_paper_lose_the_no_gain_statement",
     "SRC19_the_paper_records_the_first_order_no_gain", "nogain"),
    ("D03_bundle_edits_the_reshipped_predecessor",
     "SRC19_the_bundle_reships_its_predecessors_unedited", "reship"),
    ("D04_the_constants_json_is_perturbed_deep_inside_d_pack",
     "SRC19_the_second_order_constants_reproduce_independently", "digit"),
    ("D05_the_json_drops_a_row_the_script_emits",
     "SRC19_the_json_covers_everything_the_script_would_emit", "droprow"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"constant": ROUTEMAP, "nogain": ROUTEMAP, "reship": PRED,
           "digit": CONSTANTS, "droprow": CONSTANTS}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    if kind == "constant":
        t = t.replace("0.3689789787331466", "0.3689789787331467")
    elif kind == "nogain":
        t = t.replace("does not improve the first-order packing constant",
                      "changes the first-order packing constant", 1)
    elif kind == "reship":
        t = t + "\n<!-- edited inside the AU2b2 bundle -->\n"
    elif kind == "digit":
        rec = json.loads(t)
        d = rec["d_pack"]
        rec["d_pack"] = d[:41] + ("8" if d[41] != "8" else "7") + d[42:]
        t = json.dumps(rec, ensure_ascii=False, indent=2)
    elif kind == "droprow":
        rec = json.loads(t)
        rec["queue_dp"] = [r for r in rec["queue_dp"] if r["r"] != 2000]
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
        "tool": "src19_drill.py",
        "subject": "src19_hardzeta_au2b2_recheck.py and the A-U.2b.2 layer of "
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

        mod = "_drill_accel_null19"
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
        "defects_in_the_au2b2_layer": len(ACCEL_DEFECTS),
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
