"""Falsifiability drill for the Operation Translation rechecks.

數學戰士「墜衡」 / AMRAL Research Lab.

The recheck passed every theorem of Paper 02. That is only worth something if
the recheck could have failed. Here each asserted formula is perturbed by one
term at a time and the run is required to report the *named* check as failing.

A mutation that leaves every check green means that check is not actually
testing the formula it is named after.

Note the asymmetry: `compose_affine` is the referee, derived from the operator
definitions alone. Perturbing it is expected to break many checks at once,
because everything is compared against it. Perturbing a single claimed formula
is expected to break exactly the check named for that formula.

Usage:  python code/ot_recheck_drill.py
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRILL_K = 8
DRILL_ODD_LIMIT = 601

# (id, description, old, new, checks expected to fail)
P02_MUTATIONS = [
    ("D01-thmC-exponent", "Theorem C closed form uses 3^(u-t+1)",
     "return sum(2 ** (jt - 1) * 3 ** (u - t) for t, jt in enumerate(positions, start=1))",
     "return sum(2 ** (jt - 1) * 3 ** (u - t + 1) for t, jt in enumerate(positions, start=1))",
     ["ThmC_closed_form_of_b"]),
    ("D02-thmE-matrix-entry", "Theorem E uses M_U = [[3,2],[0,2]]",
     "    MU = [[3, 1], [0, 2]]",
     "    MU = [[3, 2], [0, 2]]",
     ["ThmE_matrix_representation"]),
    ("D03-thmB-recurrence", "Theorem B recurrence adds 2^k instead of 2^|w|",
     "                expect = bh if last == \"D\" else 3 * bh + 2 ** (k - 1)",
     "                expect = bh if last == \"D\" else 3 * bh + 2 ** k",
     ["ThmB_correction_recurrence"]),
    ("D04-thmD-wrong-power", "Theorem D concatenation uses 2^|v| instead of 2^|w|",
     "                    if b_wv != 3 ** v.count(\"U\") * b_table[w] + 2 ** kw * b_table[v]:",
     "                    if b_wv != 3 ** v.count(\"U\") * b_table[w] + 2 ** kv * b_table[v]:",
     ["ThmD_concatenation_law"]),
    ("D05-thmF-lower-bound", "Theorem F lower bound off by one",
     "            if lo != 3 ** u - 2 ** u or hi != 2 ** (k - u) * (3 ** u - 2 ** u):",
     "            if lo != 3 ** u - 2 ** u + 1 or hi != 2 ** (k - u) * (3 ** u - 2 ** u):",
     ["ThmF_order_extremal_bounds"]),
    ("D06-width-formula", "§25 width drops the -1",
     "            if hi - lo != (2 ** (k - u) - 1) * (3 ** u - 2 ** u):",
     "            if hi - lo != (2 ** (k - u)) * (3 ** u - 2 ** u):",
     ["S25_correction_width_formula"]),
    ("D07-extremes-swapped", "§21 argmin and argmax words swapped",
     "            if b_table[\"U\" * u + \"D\" * (k - u)] != lo:",
     "            if b_table[\"D\" * (k - u) + \"U\" * u] != lo:",
     ["S21_extremes_attained_at_stated_words"]),
    ("D08-residue-sign", "residue formula uses 3^{+u} instead of 3^{-u}",
     "            r = (-b * pow(3, -u, 2 ** k)) % 2 ** k",
     "            r = (-b * pow(3, u, 2 ** k)) % 2 ** k",
     ["P03_residue_cylinder_is_the_admissible_domain"]),
    ("D09-referee-broken", "the referee itself: U injects 2*Dn instead of Dn",
     "            A, B, Dn = 3 * A, 3 * B + Dn, 2 * Dn",
     "            A, B, Dn = 3 * A, 3 * B + 2 * Dn, 2 * Dn",
     ["ThmC_closed_form_of_b", "ThmE_matrix_representation"]),
    ("NULL-01", "control: a comment is added",
     "def closed_form_b(word: str) -> int:",
     "# control mutation, no behavioural change\ndef closed_form_b(word: str) -> int:",
     []),
]

P06_MUTATIONS = [
    ("E01-thmC-exponent", "Theorem C uses 3^{m-i+1}",
     "        total += 3 ** (m - i) * 2 ** Kprev",
     "        total += 3 ** (m - i + 1) * 2 ** Kprev",
     ["P06_ThmBC_accelerated_affine_closure_on_real_orbits"]),
    ("E02-recurrence-prefix", "the recurrence adds 2^{K_j} instead of 2^{K_{j-1}}",
     "    for k in kappas:\n        B = 3 * B + 2 ** K\n        K += k",
     "    for k in kappas:\n        K += k\n        B = 3 * B + 2 ** K",
     ["P06_ThmC_recurrence_matches_closed_form"]),
    ("E03-expansion-shape", "run-length expansion emits D^kappa instead of D^{kappa-1}",
     "    return \"\".join(\"U\" + \"D\" * (k - 1) for k in kappas)",
     "    return \"\".join(\"U\" + \"D\" * k for k in kappas)",
     ["P06_ThmA_run_length_expansion_is_the_parity_word"]),
    ("E04-swap-exponent", "Theorem G uses 3^{m-i-1} in 0-indexed form",
     "                if lhs != 3 ** (m - i - 2) * 2 ** P * (2 ** a - 2 ** b):",
     "                if lhs != 3 ** (m - i - 1) * 2 ** P * (2 ** a - 2 ** b):",
     ["P06_ThmG_adjacent_valuation_swap_formula"]),
    ("E05-theta-off-by-one", "the section 19 threshold drops the +1",
     "                theta = B // (2 ** K - 3 ** m) + 1",
     "                theta = B // (2 ** K - 3 ** m)",
     ["P06_S19_descent_threshold_theta_is_exact_iff"]),
    ("E06-reverse-formula", "Theorem H divides by 3^{m-1}",
     "            if Fraction(2 ** K * states[m] - B, 3 ** m) != n0:",
     "            if Fraction(2 ** K * states[m] - B, 3 ** (m - 1)) != n0:",
     ["P06_ThmH_closed_reverse_recovery"]),
    ("E07-reverse-step", "the reverse step uses 2^kappa t + 1",
     "    return Fraction(2 ** kappa * t - 1, 3)",
     "    return Fraction(2 ** kappa * t + 1, 3)",
     ["P06_S35_S38_stepwise_reverse_legality"]),
    ("E08-density-modulus", "the valuation density is counted modulo 2^j, not 2^{j+1}",
     "        mod = 2 ** (j + 1)",
     "        mod = 2 ** j",
     ["P06_ThmF_exactly_one_odd_residue_class_per_valuation"]),
    ("E09-mean-series", "the mean-valuation closed partial sum drops the +2",
     "          s2 == 2 - Fraction(J + 2, 2 ** J))",
     "          s2 == 2 - Fraction(J, 2 ** J))",
     ["P06_ThmF_mean_valuation_partial_sum_closed_form"]),
    ("E10-referee-broken", "the referee itself: S divides by 2^{kappa-1}",
     "    return (3 * n + 1) // 2 ** k, k",
     "    return (3 * n + 1) // 2 ** max(k - 1, 1), k",
     ["P06_ThmA_run_length_expansion_is_the_parity_word",
      "P06_ThmBC_accelerated_affine_closure_on_real_orbits"]),
    ("NULL-02", "control: a comment is added",
     "def B_closed(kappas: list[int]) -> int:",
     "# control mutation, no behavioural change\ndef B_closed(kappas: list[int]) -> int:",
     []),
]

P09_MUTATIONS = [
    ("F01-hard-height-max", "hard height takes the max over contracting prefixes, not the min",
     "            best = v if best is None else min(best, v)",
     "            best = v if best is None else max(best, v)",
     ["P09_ThmB_hard_height_characterises_the_hard_domain"]),
    ("F02-hard-height-sign", "hard height also admits expanding prefixes",
     "        if delta > 0:",
     "        if delta != 0:",
     ["P09_ThmB_hard_height_characterises_the_hard_domain"]),
    ("F03-quotient-direction", "the quotient threshold uses >= instead of >",
     "                if ((2 ** k - 3 ** u) * a > m_w - r) != (x < n):",
     "                if ((2 ** k - 3 ** u) * a >= m_w - r) != (x < n):",
     ["P09_ThmD_cylinder_quotient_threshold_is_an_exact_iff"]),
    # 3^u is odd, so `<` and `<=` against 2^k are the same predicate. The
    # perturbation has to move the exponent to be a real defect at all.
    ("F04-class-threshold", "a class counts as contracting one power of two too early",
     "        if 3 ** u < 2 ** K_BLOCK:",
     "        if 3 ** u < 2 ** (K_BLOCK - 1):",
     ["P05_class_count_matches_58651"]),
    ("F05-p05-binomial", "the Paper 05 class count sums to m instead of m+1",
     "        A = sum(comb(k, u) for u in range(m + 1))",
     "        A = sum(comb(k, u) for u in range(m))",
     ["P05_contracting_residue_class_counts"]),
    ("F06-alpha", "the contraction exponent uses log3/log2 instead of log2/log3",
     "    alpha = log(2) / log(3)",
     "    alpha = log(3) / log(2)",
     ["P05_contracting_residue_class_counts"]),
    # A uniform shift of sigma leaves the frontier and K(N) checks green,
    # because those only ever compare sigma against itself. Only the anchor
    # against collatz_ref.py's independently derived values pins the indexing —
    # which is why that check exists.
    ("F07-sigma-off-by-one", "sigma counts from 0 instead of 1",
     "    for j in range(1, cap + 1):\n        x = T(x)\n        if x < n:\n            return j",
     "    for j in range(1, cap + 1):\n        x = T(x)\n        if x < n:\n            return j - 1",
     ["P09_S2_sigma_indexing_matches_independent_values"]),
    ("F08-referee-broken", "the referee itself: T halves odd values too",
     "    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2",
     "    return x // 2 if x % 2 == 0 else (3 * x + 1) // 4",
     ["P09_ThmB_hard_height_characterises_the_hard_domain",
      "P09_S24_strict_descent_count_is_938413"]),
    ("NULL-03", "control: a comment is added",
     "def hard_height(w: str) -> float | int:",
     "# control mutation, no behavioural change\ndef hard_height(w: str) -> float | int:",
     []),
]

P07_MUTATIONS = [
    ("G01-thmB-exponent", "Theorem B closed form uses m^{u-t+1}",
     "    return r * sum(2 ** (jt - 1) * m ** (u - t) for t, jt in enumerate(pos, start=1))",
     "    return r * sum(2 ** (jt - 1) * m ** (u - t + 1) for t, jt in enumerate(pos, start=1))",
     ["P07_ThmB_correction_closed_form"]),
    ("G02-recurrence", "the §5 recurrence injects r*2^k instead of r*2^{|w|}",
     "                    if (bh if w[-1] == \"D\" else m * bh + r * 2 ** (k - 1)) != B:",
     "                    if (bh if w[-1] == \"D\" else m * bh + r * 2 ** k) != B:",
     ["P07_S5_correction_recurrence"]),
    ("G03-matrix-entry", "§8 uses M_U = [[m, 2r], [0, 2]]",
     "        n00, n01, n11 = (1, 0, 2) if c == \"D\" else (m, r, 2)",
     "        n00, n01, n11 = (1, 0, 2) if c == \"D\" else (m, 2 * r, 2)",
     ["P07_S8_matrix_representation"]),
    ("G04-geometric-sum", "the §17 geometric sum starts one power of two too high",
     "                geo = sum(2 ** t * m ** (u - 1 - t) for t in range(u))  # exact, no division",
     "                geo = sum(2 ** (t + 1) * m ** (u - 1 - t) for t in range(u))",
     ["P07_S17_minimum_correction_closed_geometric_form"]),
    ("G05-r-linearity", "§33 drops the factor of r",
     "                if B != r * compose(w, m, 1)[1]:",
     "                if B != compose(w, m, 1)[1]:",
     ["P07_S33_correction_is_linear_in_r"]),
    ("G06-threshold", "the §21 threshold drops the +1",
     "                        theta = B // (2 ** k - m ** u) + 1",
     "                        theta = B // (2 ** k - m ** u)",
     ["P07_S21_contracting_threshold_is_an_exact_iff"]),
    # The residue line appears twice in the target (main loop and the §47
    # block), so the anchor carries its following line to stay unique.
    ("G07-residue-sign", "Theorem C uses m^{+u} instead of m^{-u}",
     "                rw = (-B * pow(m, -u, 2 ** k)) % 2 ** k\n"
     "                sw = Fraction(m ** u * rw + B, 2 ** k)",
     "                rw = (-B * pow(m, u, 2 ** k)) % 2 ** k\n"
     "                sw = Fraction(m ** u * rw + B, 2 ** k)",
     ["P07_S12_word_residue_bijection_survives"]),
    ("G08-order-threshold", "§47 uses the minimum correction instead of the maximum",
     "                    Theta = (r * 2 ** (k - u) * geo) // (2 ** k - m ** u) + 1",
     "                    Theta = (r * geo) // (2 ** k - m ** u) + 1",
     ["P07_S47_order_uniform_threshold_covers_every_word"]),
    ("G09-referee-broken", "the referee itself: U injects 2r instead of r",
     "            A, B, Dn = m * A, m * B + r * Dn, 2 * Dn",
     "            A, B, Dn = m * A, m * B + 2 * r * Dn, 2 * Dn",
     ["P07_ThmB_correction_closed_form", "P07_S8_matrix_representation"]),
    ("NULL-04", "control: a comment is added",
     "def b_closed(word: str, m: int, r: int) -> int:",
     "# control mutation, no behavioural change\ndef b_closed(word: str, m: int, r: int) -> int:",
     []),
]

P05KL_MUTATIONS = [
    # The relative-error check divided by D unguarded, so a mutation that made D
    # negative slipped past it. Guarded now, and this mutation re-aimed at it.
    ("H01-kl-formula", "the KL divergence divides by 2 instead of by 1/2",
     '    return a * (a / Decimal("0.5")).ln() + (1 - a) * ((1 - a) / Decimal("0.5")).ln()',
     '    return a * (a / Decimal("2")).ln() + (1 - a) * ((1 - a) / Decimal("2")).ln()',
     ["P05_published_KL_agrees_with_the_real_value_to_16_significant_digits"]),
    ("H02-u-max-exponent", "the exact class boundary is one power of two too low",
     "    while p * 3 < 2 ** k:",
     "    while p * 3 < 2 ** (k - 1):",
     ["P05_exact_class_boundary_agrees_with_the_independent_float_route"]),
    # The complementarity check used to re-derive the tail inline, so mutating
    # the tail function left it untouched. It now goes through exact_tail_count,
    # which is what this mutation perturbs.
    ("H03-tail-start", "the upper tail starts at u_max instead of u_max + 1",
     "    return sum(comb(k, u) for u in range(u_max + 1, k + 1))",
     "    return sum(comb(k, u) for u in range(u_max, k + 1))",
     ["P05_contracting_fraction_and_tail_are_exact_complements"]),
    ("H04-alpha-inverted", "alpha is computed as ln3/ln2",
     "    return Decimal(2).ln() / Decimal(3).ln()",
     "    return Decimal(3).ln() / Decimal(2).ln()",
     ["P05_published_alpha_is_the_nearest_double_to_the_real_value"]),
    ("NULL-05", "control: a comment is added",
     "def hp_kl(a: Decimal) -> Decimal:",
     "# control mutation, no behavioural change\ndef hp_kl(a: Decimal) -> Decimal:",
     []),
]

TARGETS = [
    ("code/ot_paper02_recheck.py", P02_MUTATIONS, [str(DRILL_K)]),
    ("code/ot_paper06_recheck.py", P06_MUTATIONS, [str(DRILL_ODD_LIMIT)]),
    # block_exp must stay 20: the section 24 accounting checks are about
    # 1 <= n < 2^20 specifically, and would be vacuous at any other width.
    ("code/ot_paper07_recheck.py", P07_MUTATIONS, ["6", "300"]),
    ("code/ot_paper09_recheck.py", P09_MUTATIONS, ["7", "20"]),
    ("code/ot_paper05_kl_recheck.py", P05KL_MUTATIONS, []),
]


def run(path: pathlib.Path, args: list[str]) -> dict | None:
    import os
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
               COLLATZ_TREE_ROOT=str(ROOT))
    proc = subprocess.run(
        [sys.executable, str(path), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=900, env=env,
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    results = []
    baselines = {}
    with tempfile.TemporaryDirectory(prefix="ot-drill-", ignore_cleanup_errors=True) as tmp:
        tmpdir = pathlib.Path(tmp)

        for target, mutations, args in TARGETS:
            source = ROOT / target
            original = source.read_text(encoding="utf-8")
            stem = pathlib.Path(target).stem

            # Paper 06's recheck imports the Paper 02 referee, so every mutant
            # needs that module beside it in the scratch directory.
            for dep in ("ot_paper02_recheck.py",):
                (tmpdir / dep).write_text(
                    (ROOT / "code" / dep).read_text(encoding="utf-8"), encoding="utf-8")

            base = tmpdir / f"baseline_{stem}.py"
            base.write_text(original, encoding="utf-8")
            baseline = run(base, args)
            if baseline is None or not baseline["ok"]:
                print(json.dumps({"error": f"baseline did not pass for {target}",
                                  "baseline": baseline}))
                return 2
            baselines[target] = len(baseline["checks"])
            print(f"{target}: baseline passes all {len(baseline['checks'])} checks",
                  file=sys.stderr)

            for mid, desc, old, new, expected in mutations:
                if original.count(old) != 1:
                    results.append({"id": mid, "target": target,
                                    "error": f"anchor occurs {original.count(old)} times"})
                    print(f"  {mid}: ANCHOR NOT UNIQUE", file=sys.stderr)
                    continue
                path = tmpdir / (re.sub(r"[^A-Za-z0-9_]", "_", mid) + ".py")
                path.write_text(original.replace(old, new), encoding="utf-8")
                out = run(path, args)
                if out is None:
                    failed_checks = ["<crashed>"]
                else:
                    # Only entries carrying a "pass" key are the recheck's own
                    # checks. Some rechecks also record `subject_claim_holds`
                    # entries — findings about the subject, which are meant to be
                    # false when the subject has a defect and must not be counted
                    # as the instrument failing, or every control would look
                    # disturbed.
                    failed_checks = [n for n, c in out["checks"].items()
                                     if "pass" in c and not c["pass"]]

                if expected:
                    # A mutant that cannot produce a result at all has been
                    # detected, though less informatively than by a named check.
                    crashed = failed_checks == ["<crashed>"]
                    caught = crashed or all(e in failed_checks for e in expected)
                    verdict = ("caught (crashed, not by a named check)" if crashed
                               else "caught" if caught else "SURVIVED / WRONG CHECK")
                else:
                    caught = not failed_checks
                    verdict = "clean (control)" if caught else "CONTROL DISTURBED"

                results.append({
                    "id": mid, "target": target, "description": desc,
                    "expected_failing_checks": expected,
                    "observed_failing_checks": failed_checks,
                    "as_expected": caught,
                })
                print(f"  {mid}: {verdict}  -> {failed_checks}", file=sys.stderr)

    # Defects and controls are counted separately. A single "as_expected" tally
    # across both makes the summary read as though more defects passed than were
    # planted.
    defects = [r for r in results if r.get("expected_failing_checks")]
    controls = [r for r in results if "expected_failing_checks" in r
                and not r["expected_failing_checks"]]
    report = {
        "tool": "ot_recheck_drill.py",
        "targets": {t: {"baseline_checks": baselines.get(t), "args": a}
                    for t, _, a in TARGETS},
        "drill_word_length": DRILL_K,
        "drill_odd_limit": DRILL_ODD_LIMIT,
        "mutations": results,
        "defects_planted": len(defects),
        "defects_caught_by_the_named_check": len([r for r in defects if r["as_expected"]]),
        "controls_planted": len(controls),
        "controls_undisturbed": len([r for r in controls if r["as_expected"]]),
        "anomalies": [r["id"] for r in results if not r.get("as_expected", False)],
    }
    report["ok"] = not report["anomalies"] and not any("error" in r for r in results)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
