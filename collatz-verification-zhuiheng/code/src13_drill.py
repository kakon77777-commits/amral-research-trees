"""Mutation drill for src13_hardzeta_round03a4_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 03-A.4 is a ledger: a Sturmian credit budget, an excess-valuation spend, and
a deficit that turns out to be the orbit's growth rate. Eleven defects damage that
ledger a line at a time; three more damage this run's own measurements, including
the continued-fraction machinery that the Legendre gate rests on.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src13_drill.py
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
TOOL = CODE / "src13_hardzeta_round03a4_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_I_Round_03A4_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A4_Spine_Valuation_Rigidity_v0.1.md"
TIMEOUT_S = 900

ACCEL_DEFECTS = [
    # A constant offset cancels inside b_m = credit(m) - credit(m-1), so the
    # recurrence cannot see it; the telescoped ledger can.
    ("A01_sturmian_credit_off_by_one",
     "SRC13_the_credit_ledger_telescopes_and_is_never_overspent",
     ("    return floor_beta(m) - m", "    return floor_beta(m) - m + 1")),
    ("A02_deficit_uses_the_wrong_floor",
     "SRC13_subcritical_is_exactly_a_nonnegative_deficit",
     ("    return floor_beta(m) - cumulative(accel_code(n, m))[-1]",
      "    return floor_beta(m + 1) - cumulative(accel_code(n, m))[-1]")),
    ("A03_credit_spent_forgets_the_minus_one",
     "SRC13_the_credit_ledger_telescopes_and_is_never_overspent",
     ("    return sum(q - 1 for q in orbit_valuations(n, m))",
      "    return sum(q for q in orbit_valuations(n, m))")),
    ("A04_cylinder_residue_drops_the_inverse",
     "SRC13_high_valuation_is_exactly_membership_of_one_residue_class",
     ("    return (-pow(3, -1, 1 << r)) % (1 << r)",
      "    return (-pow(3, 1, 1 << r)) % (1 << r)")),
    ("A05_cylinder_visits_scans_one_element_too_many",
     "SRC13_cylinder_occupancy_stays_inside_the_sturmian_budget",
     ("    return sum(1 for y in orbit_endpoints(n, m)[:m] if y % mod == eta)",
      "    return sum(1 for y in orbit_endpoints(n, m) if y % mod == eta)")),
    ("A06_excursion_check_drops_a_term",
     "SRC13_the_spine_excursion_identity_holds_in_exact_integers",
     ("    rhs = 3 ** m * n + sum(3 ** (m - 1 - i) * 2 ** K[i] for i in range(m))",
      "    rhs = 3 ** m * n + sum(3 ** (m - 1 - i) * 2 ** K[i] for i in range(m - 1))")),
    ("A07_orbit_endpoints_starts_after_the_first_step",
     "SRC13_high_valuation_is_exactly_membership_of_one_residue_class",
     ("    out, x = [n], n", "    out, x = [], n")),
    ("A08_legendre_gate_comparison_inverted",
     "SRC13_where_the_gate_opens_the_ratio_really_is_a_convergent",
     ("    return 3 ** (2 * m * m) < 2 ** (2 * m * K + m)",
      "    return 3 ** (2 * m * m) > 2 ** (2 * m * K + m)")),
    ("A09_legendre_gate_loses_its_half",
     "SRC13_the_legendre_gate_is_open_only_rarely",
     ("    return 3 ** (2 * m * m) < 2 ** (2 * m * K + m)",
      "    return 3 ** (2 * m * m) < 2 ** (2 * m * K + 4 * m)")),
    # `<=` vs `<` is a NO-OP for the FIFTH time in this arm: acc*P == Q would
    # need an exact power relation between the rationals, which log2(3) being
    # irrational forbids. Mutating the recursion step instead really moves the
    # expansion.
    ("A10_continued_fraction_tail_recursion_not_inverted",
     "SRC13_beta_continued_fraction_matches_its_known_expansion",
     ("        P, Q = rem, P", "        P, Q = P, rem")),
    ("A11_convergent_recursion_roles_swapped",
     "SRC13_beta_convergents_contain_the_named_equal_temperaments",
     ("    p_prev, q_prev, p, q = 0, 1, 1, 0", "    p_prev, q_prev, p, q = 1, 0, 0, 1")),
]

TOOL_DEFECTS = [
    ("T01_the_known_expansion_is_transcribed_wrong",
     "SRC13_beta_continued_fraction_matches_its_known_expansion",
     ("KNOWN_CF = [1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2]",
      "KNOWN_CF = [1, 1, 1, 2, 2, 3, 1, 5, 2, 24, 2, 2]")),
    ("T02_the_haar_gap_check_compares_against_nothing",
     "SRC13_the_haar_gap_is_real_and_not_an_artefact_of_the_bound",
     ("        gamma = math.log2(3) - 1", "        gamma = 0.0")),
    ("T03_the_bounded_deficit_bracket_uses_the_wrong_maximum",
     "SRC13_the_bounded_deficit_bounds_bracket_the_endpoint",
     ("            D = max(ds)", "            D = min(ds)")),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_ledger",
     "SRC13_paper_keeps_an_explicit_proved_and_unproved_ledger", "ledger"),
    ("D02_paper_loses_its_method_no_gos",
     "SRC13_paper_states_its_own_method_no_gos", "nogo"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    txt = keep[PAPER].decode("utf-8")
    if kind == "ledger":
        txt = txt.replace("## 未證", "## 附註", 1)
    elif kind == "nogo":
        txt = txt.replace("Method No-Go", "Method Note", 1)
    keep[PAPER] = txt.encode("utf-8")
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def main() -> int:
    rep = {
        "tool": "src13_drill.py",
        "subject": "src13_hardzeta_round03a4_recheck.py and the deficit-queue "
                   "layer of hz_accel_code.py",
        "defects": {}, "controls": {},
    }
    original_accel = ACCEL.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, accel_module="hz_accel_code") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ACCEL_MODULE": accel_module}
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

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        base = tmp / "source"
        base.mkdir()
        shutil.copy2(SOURCE / BUNDLE, base / BUNDLE)

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

        for name, target, (old, new) in ACCEL_DEFECTS:
            if old not in original_accel:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} absent; nothing was tested"}
                continue
            mod = f"_drill_accel_{name}"
            f = CODE / f"{mod}.py"
            try:
                f.write_text(original_accel.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, TOOL, mod))
            finally:
                f.unlink(missing_ok=True)

        for name, target, (old, new) in TOOL_DEFECTS:
            if old not in original_tool:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} absent; nothing was tested"}
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

        mod = "_drill_accel_null13"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original_accel + "\n# a comment nothing reads\n",
                         encoding="utf-8")
            res = run(base, TOOL, mod)
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
        "defects_in_the_ledger_layer": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_measurement": len(TOOL_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
