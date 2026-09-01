"""RUN-048 mutation drill for `src67_return_loops.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" has four causes worth telling apart:
    unreachable, premise-empty, too weak, and mathematically identical to what
    it replaced (RUN-044's `2^-q` mod 3, RUN-045's modulus shrunk to a divisor,
    RUN-047's ceiling table replaced by the floor table);
  * from a GREEN baseline a defect must make a counter RISE. Deleting a check
    whose counter already reads zero is invisible, and so is LOOSENING one;
  * a defect that makes the gate RAISE is malformed too, and the fix belongs in
    the gate. Every section reports through an `errors.<section>_raised`
    counter;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back.

Usage:
    python code/src67_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src67_return_loops.py"
LIMIT = "200000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the order and the residue map ---
    ("D1_the_order_of_two_is_read_one_power_high",
     "    return 2 * 3 ** (k - 1)",
     "    return 2 * 3 ** k",
     "instrument.failed"),
    ("D2_the_residue_map_drops_its_affine_shift",
     "    return (3 * r + 1) * pow(pow(2, q, m), -1, m) % m",
     "    return (3 * r) * pow(pow(2, q, m), -1, m) % m",
     "instrument.failed"),
    ("D3_the_residue_map_advances_by_four_not_two",
     "    return (3 * r + 1) * pow(pow(2, q, m), -1, m) % m",
     "    return (3 * r + 1) * pow(pow(4, q, m), -1, m) % m",
     "instrument.failed"),

    # --- Theorem 3.1, boundary locality ---
    ("D4_the_truncated_sum_runs_one_term_short",
     "            trunc = sum(3 ** (j - 1) * pow(pow(2, Qs[j], mod), -1, mod)\n                        for j in range(1, k + 1)) % mod",
     "            trunc = sum(3 ** (j - 1) * pow(pow(2, Qs[j], mod), -1, mod)\n                        for j in range(1, k)) % mod",
     "locality.truncated_sum_violations"),
    ("D5_the_truncated_sum_shifts_its_power_of_three",
     "            trunc = sum(3 ** (j - 1) * pow(pow(2, Qs[j], mod), -1, mod)\n                        for j in range(1, k + 1)) % mod",
     "            trunc = sum(3 ** j * pow(pow(2, Qs[j], mod), -1, mod)\n                        for j in range(1, k + 1)) % mod",
     "locality.truncated_sum_violations"),
    ("D6_the_full_sum_drops_the_modular_inverse",
     "            full = sum(3 ** (j - 1) * pow(pow(2, Qs[j], mod), -1, mod)\n                       for j in range(1, h + 1)) % mod",
     "            full = sum(3 ** (j - 1) * pow(pow(2, Qs[j], mod), 1, mod)\n                       for j in range(1, h + 1)) % mod",
     "locality.full_sum_violations"),
    ("D7_the_tail_term_divisibility_is_read_at_the_wrong_level",
     "                if 3 ** (j - 1) % mod:",
     "                if 3 ** (j - 2) % mod:",
     "locality.tail_term_not_divisible_by_the_modulus"),
    ("D8_the_suffix_representative_uses_the_whole_word",
     "            suf = w[h - k:]",
     "            suf = w[h - k - 1:]",
     "locality.suffix_representative_violations"),

    # --- Theorem 4.1, the source budget ---
    ("D9_the_middle_term_is_read_at_the_wrong_suffix",
     "            mid = ceil_beta(h) - ceil_beta(h - r)",
     "            mid = ceil_beta(h) - ceil_beta(h - r + 1)",
     "source_budget.left_inequality_violations"),
    ("D10_the_left_inequality_is_made_strict",
     "            if pr > mid:",
     "            if pr >= mid:",
     "source_budget.left_inequality_violations"),
    ("D11_the_right_inequality_is_halved",
     "            if mid > 2 * r:",
     "            if mid > r:",
     "source_budget.right_inequality_violations"),
    ("D12_a_single_valuation_is_bounded_by_r_not_two_r",
     "            if max(w[:r]) > 2 * r:",
     "            if max(w[:r]) > r // 2:",
     "source_budget.single_valuation_above_two_r"),

    # --- Theorem 5.1 and Corollary 5.2 ---
    ("D13_the_period_is_compared_to_the_wrong_fraction_of_m",
     "        if s != 2 * m // 3:",
     "        if s != m // 3:",
     "labels.period_disagreeing_with_two_thirds_m"),
    ("D14_the_label_uniqueness_scan_runs_past_the_period",
     "            for q in range(1, s):",
     "            for q in range(1, s + 2):",
     "labels.label_collisions_below_the_period"),
    ("D15_the_period_collision_is_looked_for_one_step_early",
     "            if forward_target(r, s, m) != forward_target(r, 0, m):\n                t[\"no_collision_at_the_period\"] += 1",
     "            if forward_target(r, s - 1, m) != forward_target(r, 0, m):\n                t[\"no_collision_at_the_period\"] += 1",
     "labels.no_collision_at_the_period"),
    ("D16_the_sheet_bound_is_lowered_to_two",
     "            if top > 3:",
     "            if top > 2:",
     "labels.more_than_three_sheets"),
    ("D17_the_sheet_scan_stops_at_the_period",
     "            for q in range(1, 2 * m):",
     "            for q in range(1, s):",
     "labels.three_sheets_never_attained"),

    # --- Theorem 6.1 ---
    ("D18_the_alias_budget_counts_the_wrong_edges",
     "            b = sum(1 for q in w if q >= s)",
     "            b = sum(1 for q in w if q >= 1)",
     "alias.budget_theorem_6_1_violations"),
    ("D19_the_large_edge_budget_uses_the_period_not_twice_the_modulus",
     "            b2 = sum(1 for q in w if q >= 2 * m)",
     "            b2 = sum(1 for q in w if q >= 1)",
     "alias.large_edge_budget_violations"),
    ("D20_the_total_valuation_is_compared_to_the_wrong_ceiling",
     "        if q_total != ceil_beta(h):",
     "        if q_total != ceil_beta(h) + 1:",
     "alias.total_valuation_not_the_ceiling"),

    # --- the return loops and their certificate ---
    ("D21_the_loop_walker_keeps_the_erased_interior_on_the_stack",
     "            for old in stack[p + 1:]:\n                pos.pop(states[old] % m, None)\n            stack = stack[:p + 1]",
     "            for old in stack[p + 1:]:\n                pass\n            stack = stack[:p + 1]",
     "errors.loops_raised"),
    ("D22_the_loop_records_the_wrong_cycle_length",
     "            out.append((stack[p], j, len(stack) - p))",
     "            out.append((stack[p], j, len(stack) + p))",
     "loops.erased_cycle_longer_than_the_period"),
    ("D23_the_loop_endpoint_congruence_is_read_at_the_source",
     "                if states[j] % m != rc:",
     "                if states[i] % m != rc + 1:",
     "loops.loop_endpoints_not_congruent"),
    ("D24_the_segment_affine_identity_drops_its_correction",
     "                if (1 << qc) * states[j] != 3 ** lc * states[i] + bc:",
     "                if (1 << qc) * states[j] != 3 ** lc * states[i]:",
     "loops.segment_affine_identity_violations"),
    ("D25_the_certificate_adds_where_it_must_subtract",
     "                if ((1 << qc) - 3 ** lc) * rc % m != bc % m:",
     "                if ((1 << qc) + 3 ** lc) * rc % m != bc % m:",
     "loops.certificate_theorem_11_1_violations"),
    ("D26_the_certificate_uses_the_wrong_return_residue",
     "                rc = states[i] % m",
     "                rc = states[i] % (m * 3)",
     "loops.loop_endpoints_not_congruent"),
    ("D27_the_certificate_correction_spans_the_wrong_edges",
     "                bc = b_of(tuple(w[i:j]))",
     "                bc = b_of(tuple(w[i:j + 1])) if j < len(w) else b_of(tuple(w[i:j]))",
     "loops.certificate_theorem_11_1_violations"),
    ("D28_the_cycle_bound_uses_twice_the_modulus",
     "                if cyc > s:",
     "                if cyc > 1:",
     "loops.erased_cycle_longer_than_the_period"),

    # --- Theorem 9.1's finite bound ---
    ("D29_the_low_vertex_lift_is_read_forwards",
     "    low = [ms[h - j] < thr for j in range(h + 1)]",
     "    low = [ms[j] < thr for j in range(h + 1)]",
     "clean_mass.low_lift_vertex_inside_a_clean_run"),
    ("D30_the_bad_edge_test_forgets_one_endpoint",
     "    bad = [word[j] >= qthr or low[j] or low[j + 1] for j in range(h)]",
     "    bad = [word[j] >= qthr or low[j] for j in range(h)]",
     "clean_mass.low_lift_vertex_inside_a_clean_run"),
    ("D31_the_erasure_counts_stack_depth_from_the_bottom",
     "            erased += len(stack) - p",
     "            erased += len(stack) + p",
     "clean_mass.erasure_accounting_violations"),
    ("D32_the_finite_lower_bound_demands_every_edge",
     "            lower = h + 1 - (b + 2 * low_count + 1) * s",
     "            lower = h + 1",
     "clean_mass.mass_below_the_finite_bound"),
    ("D33_the_clean_run_admits_a_large_edge",
     "    bad = [word[j] >= qthr or low[j] or low[j + 1] for j in range(h)]",
     "    bad = [low[j] or low[j + 1] for j in range(h)]",
     "clean_mass.large_edge_inside_a_clean_run"),
    ("D34_the_unit_residue_test_admits_multiples_of_three",
     "                if any(r % 3 == 0 for r in res):",
     "                if any(r % 3 == 1 for r in res):",
     "clean_mass.non_unit_residue_in_a_clean_run"),
    ("D35_the_residual_path_bound_is_lowered_to_one",
     "                if rest > s:",
     "                if rest > 1:",
     "clean_mass.residual_path_longer_than_the_period"),
    ("D36_the_integer_depth_multiplies_by_the_wrong_base",
     "        while p * 3 <= max(h, 3):",
     "        while p * 2 <= max(h, 3):",
     "clean_mass.float_depth_disagreeing_with_the_integer_one"),

    # --- their two synthetic blocks ---
    ("D37_the_arranged_inequality_is_reported_the_wrong_way",
     "        if not gamma < eta:",
     "        if gamma < eta:",
     "their_algebra.high_lift_gamma_not_below_eta"),
    ("D38_the_two_assertions_are_compared_against_a_third_thing",
     "        if (1 - eta + gamma < 1) != (gamma < eta):",
     "        if (1 - eta + gamma < 1) != (gamma > eta):",
     "their_algebra.high_lift_second_assertion_differing_from_the_first"),
    ("D39_the_loop_invariant_constant_is_recomputed_differently",
     "        if 1 - math.log2(3) / 3 != c_loop:",
     "        if 1 - math.log2(3) / 4 != c_loop:",
     "their_algebra.high_lift_constant_varying_across_the_loop"),
    ("D40_the_repaired_left_side_is_reported_as_still_failing",
     "        if not lhs > 0:",
     "        if lhs > 0:",
     "their_algebra.alias_assertion_failed_after_the_repair"),

    # --- their near-full rows ---
    ("D41_the_near_full_modulus_bracket_is_tightened",
     "        if not m <= target < 3 * m:",
     "        if not m <= target < m:",
     "near_full.modulus_bracket_violations"),
    ("D42_the_alias_bound_divides_by_the_modulus_not_the_period",
     "        b = q // ord_two(k)",
     "        b = q // (3 ** k)",
     "near_full.alias_bound_disagreeing"),
    ("D43_the_near_full_depth_uses_the_wrong_base",
     "        k = max(1, math.floor(math.log(target, 3)))",
     "        k = max(1, math.floor(math.log(target, 2)))",
     "near_full.k_disagreeing"),

    # --- published examples ---
    ("D44_the_example_lower_bound_forgets_the_low_vertices",
     "        lower = max(0, h + 1 - (big + 2 * low + 1) * ord_two(k))",
     "        lower = max(0, h + 1 - (big + 1) * ord_two(k))",
     "examples.lower_bound_disagreeing"),
    ("D45_the_example_low_vertex_count_reads_the_forward_lift",
     "        low = sum(1 for x in ms if x < thr)",
     "        low = sum(1 for x in ms if x > thr)",
     "examples.low_vertex_count_disagreeing"),
    ("D46_the_example_large_edge_threshold_is_the_period",
     "        big = sum(1 for q in w if q >= 2 * m)",
     "        big = sum(1 for q in w if q >= 1)",
     "examples.large_edge_count_disagreeing"),
    ("D47_the_example_lookup_forgets_the_endpoint_again",
     "        by_key.setdefault((rec[0], rec[2]), rec)",
     "        by_key.setdefault((rec[0], rec[0]), rec)",
     "examples.example_not_found_in_my_population"),

    # --- the artifact and ledger layers ---
    ("D48_the_checksum_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D49_the_ledger_coverage_heuristic_accepts_anything",
     "        return hit >= max(1, len(words) // 2)",
     "        return hit >= 0",
     "ledger.heuristic_failed_its_negative_control"),
    ("D50_the_ledger_coverage_heuristic_accepts_nothing",
     "        hit = sum(1 for w in words if w[:7] in blob)",
     "        hit = sum(1 for w in words if w[:7] == blob)",
     "ledger.heuristic_failed_its_positive_control"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
    ("N2_a_blank_line_is_not_a_defect", b"\n"),
]


def write_gate(data: bytes, tries: int = 8) -> None:
    """Write the gate, retrying a transient OS error.

    Windows returned `OSError: [Errno 22] Invalid argument` on one restore in
    the middle of a run -- an indexer or the just-finished `py_compile` holding
    the handle for a moment. The pristine sidecar recovered it and the file was
    provably unchanged, but a restore that can die is a restore that can leave
    a planted defect behind, so it retries and then raises loudly rather than
    silently continuing with a mutated gate.
    """
    last = None
    for attempt in range(tries):
        try:
            GATE.write_bytes(data)
            return
        except OSError as exc:                          # pragma: no cover
            last = exc
            time.sleep(0.05 * (attempt + 1))
    raise RuntimeError("could not restore %s after %d tries: %r"
                       % (GATE.name, tries, last))


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle),
             "--limit", LIMIT],
            capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
    except subprocess.TimeoutExpired:
        return {"passed": False,
                "failures": ["__the gate did not terminate__"], "hung": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False,
                "failures": ["__the gate did not produce JSON__"],
                "stderr_tail": (proc.stderr or "")[-400:]}


def _complaints(res: dict) -> list[str]:
    return (list(res.get("failures", []))
            + list(res.get("empty_populations", []))
            + list(res.get("counters_not_in_the_failure_or_population_lists",
                           [])))


def _same_verdict(a: dict, b: dict) -> bool:
    def strip(d: dict) -> dict:
        return {k: v for k, v in d.items() if k not in ("bundle",)}
    return (json.dumps(strip(a), sort_keys=True, default=str)
            == json.dumps(strip(b), sort_keys=True, default=str))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=pathlib.Path, required=True)
    args = ap.parse_args()

    backup = GATE.with_suffix(GATE.suffix + ".pristine")
    interrupted = False
    if backup.exists():
        write_gate(backup.read_bytes())
        interrupted = True
    snapshot = GATE.read_bytes()
    backup.write_bytes(snapshot)

    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name, "limit": LIMIT,
        "a_previous_run_was_interrupted_and_the_gate_was_restored": interrupted,
        "baseline": {"passed": base.get("passed"),
                     "failures": base.get("failures"),
                     "empty_populations": base.get("empty_populations")},
        "defects": {}, "controls": {},
    }
    if not base.get("passed"):
        report["ok"] = False
        report["note"] = "the gate is not green before anything was planted"
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 2

    raw = snapshot.decode("utf-8")
    aim = {name: raw.count(old) for name, old, _n, _e in DEFECTS}
    report["anchors_matching_once"] = sum(1 for v in aim.values() if v == 1)
    report["anchors_not_unique"] = {k: v for k, v in aim.items() if v != 1}

    for name, old, new, expected in DEFECTS:
        if aim[name] != 1:
            report["defects"][name] = {
                "caught": False, "anchor_matches": aim[name],
                "malformed": "the anchor names %d places, so nothing was "
                             "planted" % aim[name]}
            continue
        try:
            write_gate(raw.replace(old, new).encode("utf-8"))
            res = run_gate(args.bundle)
        finally:
            write_gate(snapshot)

        if res.get("hung"):
            report["defects"][name] = {
                "caught": False, "malformed": "the gate did not terminate"}
            continue
        if "__the gate did not produce JSON__" in res.get("failures", []):
            report["defects"][name] = {
                "caught": False, "malformed": "the gate raised",
                "stderr_tail": res.get("stderr_tail", "")[-200:]}
            continue
        if _same_verdict(base, res):
            report["defects"][name] = {
                "caught": False,
                "malformed": "the mutation changes nothing",
                "note": "unreachable, premise-empty, too weak, or "
                        "mathematically identical -- and from green, deleting "
                        "or LOOSENING a check whose counter reads zero is "
                        "invisible too"}
            continue
        said = _complaints(res)
        report["defects"][name] = {
            "caught": any(expected in c for c in said),
            "expected_named": expected,
            "reported": said[:4],
            "caught_by_something_else_only": (bool(said) and
                                              not any(expected in c
                                                      for c in said)),
        }

    for name, addition in CONTROLS:
        try:
            write_gate(snapshot + addition)
            res = run_gate(args.bundle)
        finally:
            write_gate(snapshot)
        report["controls"][name] = {
            "undisturbed": bool(res.get("passed")) and not _complaints(res),
            "reported": _complaints(res)[:4],
        }

    caught = sum(1 for v in report["defects"].values() if v.get("caught"))
    malformed = sum(1 for v in report["defects"].values() if v.get("malformed"))
    report["totals"] = {
        "defects": len(DEFECTS), "caught": caught, "malformed": malformed,
        "missed": len(DEFECTS) - caught - malformed,
        "caught_but_by_another_counter": sum(
            1 for v in report["defects"].values()
            if v.get("caught_by_something_else_only")),
        "controls": len(report["controls"]),
        "controls_undisturbed": sum(1 for c in report["controls"].values()
                                    if c["undisturbed"]),
    }
    tot = report["totals"]
    report["counts"] = {
        "planted": tot["defects"],
        "caught_by_their_own_check": tot["caught"],
        "missed": tot["missed"], "malformed": tot["malformed"],
        "controls": tot["controls"],
        "controls_undisturbed": tot["controls_undisturbed"],
    }
    report["ok"] = (caught == len(DEFECTS)
                    and all(c["undisturbed"]
                            for c in report["controls"].values()))
    if GATE.read_bytes() == snapshot:
        backup.unlink()
    else:
        report["ok"] = False
        report["note"] = "the gate did not come back byte-identical"
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
