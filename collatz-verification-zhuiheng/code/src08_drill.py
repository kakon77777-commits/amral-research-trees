"""Mutation drill for src08_hardzeta_round02_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Same discipline as `src07_drill.py`, aimed at Round 02's additions: the
quotient-coordinate thresholds, the parity-restricted sum, `beta_k`, the
first-crossing enumeration and the Terras margin. Eight of the defects damage
Round 02's own formulas, so each asks whether the cross-round confrontation would
notice if the paper's restatement disagreed with Round 01.

Two mutations were tried and **retired as no-ops**, for the reason this tree has
now met three times: `3^u` and `2^j` are never equal, so `<` and `<=` select the
same set wherever they compare those two. They are replaced by mutations that
change the answer.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src08_drill.py
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
TOOL = CODE / "src08_hardzeta_round02_recheck.py"
ALGEBRA = CODE / "hz_chart_algebra.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_I_Round_02_bundle.zip"
ROUND02 = "Hard_Zeta_Phase_I_Round_02_Atomic_Hazard_Coefficient_Correction_v0.1.md"
MAP2 = "Hard_Zeta_ROUTE_MAP_v0.2.md"
TIMEOUT_S = 1200

ALGEBRA_DEFECTS = [
    ("A01_q_D_numerator_drops_the_factor_two",
     "SRC08_quotient_thresholds_agree_with_round_01s_caps",
     ("    return (w.m - 2 * w.r) // delta", "    return (w.m - w.r) // delta")),
    ("A02_q_U_numerator_loses_the_plus_one",
     "SRC08_quotient_thresholds_agree_with_round_01s_caps",
     ("    return (3 * w.m + 1 - 2 * w.r) // delta",
      "    return (3 * w.m - 2 * w.r) // delta")),
    # `while p * 3 < 2 ** (k + 1)` -> `<=` is a NO-OP: 3^u never equals a power
    # of two. Mutating the exponent instead actually moves beta_k.
    ("A03_beta_uses_the_wrong_exponent",
     "SRC08_beta_k_zones_agree_with_round_01s_power_zones",
     ("    while p * 3 < 2 ** (k + 1):", "    while p * 3 < 2 ** k:")),
    ("A04_zone_boundary_shifted_by_one",
     "SRC08_beta_k_zones_agree_with_round_01s_power_zones",
     ("    if u <= b - 1:", "    if u <= b:")),
    ("A05_parity_restricted_sum_ignores_the_parity_offset",
     "SRC08_parity_restricted_sums_reproduce_round_01_chart_masses",
     ("    first = A_lo if (A_lo - e) % 2 == 0 else A_lo + 1", "    first = A_lo")),
    ("A06_nu_drops_the_n_at_least_2_domain_guard",
     "SRC08_first_crossing_residue_separation_holds_on_every_word_checked",
     ('    return w.r if w.r >= 2 else w.r + 2 ** w.k', "    return w.r")),
    # `3 ** c.u < 2 ** c.k` -> `<=` is the same no-op again; widening the
    # threshold admits words that have not crossed at all.
    ("A07_first_crossing_enumeration_admits_non_crossing_words",
     "SRC08_first_crossing_depths_are_exactly_the_bit_lengths_of_powers_of_3",
     ("            if 3 ** c.u < 2 ** c.k:", "            if 3 ** c.u < 2 ** (c.k + 1):")),
    ("A08_terras_cap_off_by_one",
     "SRC08_first_crossing_hard_height_is_set_by_the_final_prefix_alone",
     ("    c = w.b // delta\n    n = nu(w)", "    c = w.b // delta + 1\n    n = nu(w)")),
]

TOOL_DEFECTS = [
    ("T01_coefficient_stopping_time_condition_inverted",
     "SRC08_coefficient_stopping_time_never_exceeds_the_classical_one",
     ("        if tau == 0 and 3 ** u < 2 ** j:", "        if tau == 0 and 3 ** u > 2 ** j:")),
    # Shifting the R-predicate on the MEASURED range is undetectable: R_k is
    # empty everywhere below 2^18, so every predicate gives mass 0 and the split
    # reduces to C_k = Z_k. The identity is instead exercised on synthetic
    # (sigma, tau) data where R is non-empty, and the mutation lands there.
    ("T02_correction_compartment_boundary_shifted",
     "SRC08_the_split_identity_is_implemented_correctly_where_R_is_nonempty",
     ("        R = {n for n in range(2, len(syn_sig)) if syn_tau[n] <= k < syn_sig[n]}",
      "        R = {n for n in range(2, len(syn_sig)) if syn_tau[n] < k < syn_sig[n]}")),
    ("T03_step_count_used_for_legality_is_off_by_one",
     "SRC08_child_legality_holds_in_the_quotient_coordinate",
     ("    for _ in range(k):\n        x = T(x)\n    return x",
      "    for _ in range(k + 1):\n        x = T(x)\n    return x")),
]

DOC_DEFECTS = [
    ("D01_loose_round02_diverges_from_the_bundled_copy",
     "SRC08_loose_files_match_the_bundled_copies", "loose"),
    ("D02_bundle_no_longer_carries_round_01",
     "SRC08_bundle_carries_round_01_alongside_round_02", "round01"),
    ("D03_route_map_v02_restates_the_weighted_general_bridge",
     "SRC08_route_map_v02_does_not_restate_the_general_bridge", "bridge"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    if kind == "loose":
        p = src / ROUND02
        p.write_text(p.read_text(encoding="utf-8").replace("Neo.K", "Neo.Q", 1),
                     encoding="utf-8")
        return
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    if kind == "round01":
        keep = {n: b for n, b in keep.items() if "Round_01" not in n}
    elif kind == "bridge":
        keep[MAP2] = (keep[MAP2].decode("utf-8")
                      + "\n\\[Q_k=\\sum\\omega_i\\to0.\\]\n").encode("utf-8")
        (src / MAP2).write_bytes(keep[MAP2])
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def main() -> int:
    rep = {
        "tool": "src08_drill.py",
        "subject": "src08_hardzeta_round02_recheck.py and Round 02's additions "
                   "to hz_chart_algebra.py",
        "defects": {}, "controls": {},
    }
    original_algebra = ALGEBRA.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, algebra_module="hz_chart_algebra") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ALGEBRA_MODULE": algebra_module}
        out = subprocess.run([sys.executable, str(tool)], capture_output=True,
                             text=True, encoding="utf-8", timeout=TIMEOUT_S, env=env)
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
        for nm in (BUNDLE, ROUND02, MAP2):
            shutil.copy2(SOURCE / nm, base / nm)

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

        for name, target, (old, new) in ALGEBRA_DEFECTS:
            if old not in original_algebra:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} absent; nothing was tested"}
                continue
            mod = f"_drill_algebra_{name}"
            f = CODE / f"{mod}.py"
            try:
                f.write_text(original_algebra.replace(old, new, 1), encoding="utf-8")
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

        mod = "_drill_algebra_null08"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original_algebra + "\n# a comment nothing reads\n",
                         encoding="utf-8")
            res = run(base, TOOL, mod)
        finally:
            f.unlink(missing_ok=True)
        rep["controls"]["N01_algebra_annotated_where_nothing_reads"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

        s = tmp / "src_null"
        shutil.copytree(base, s)
        (s / "UNREAD_SCRATCH.txt").write_text("read by nothing\n", encoding="utf-8")
        res = run(s, TOOL)
        rep["controls"]["N02_unrelated_file_beside_the_documents"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(rep["defects"]),
        "defects_caught_by_the_named_check": caught,
        "defects_in_round_02s_own_formulas": len(ALGEBRA_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
