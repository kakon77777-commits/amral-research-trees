"""RUN-049 mutation drill for `src68_loop_defect.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" has four causes worth telling apart:
    unreachable, premise-empty, too weak, and mathematically identical to what
    it replaced (RUN-044's `2^-q` mod 3, RUN-045's modulus shrunk to a divisor,
    RUN-047's floor table, RUN-048's dropped modular inverse);
  * from a GREEN baseline a defect must make a counter RISE. Deleting a check
    whose counter already reads zero is invisible, and so is LOOSENING one;
  * a defect that changes only OBSERVATIONS is a finding about the gate:
    RUN-048 had four such, all pointing at a section whose only failure
    counter compared against a vacuous bound;
  * a defect that makes the gate RAISE is reported through
    `errors.<section>_raised` rather than crashing;
  * the pristine sidecar is written before anything is planted, every gate
    write retries a transient OS error, and the sidecar is removed only when
    the file is provably back.

Usage:
    python code/src68_drill.py --bundle <dir>
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
GATE = ROOT / "code" / "src68_loop_defect.py"
LIMIT = "220000"
GATE_TIMEOUT_SECONDS = 900

DEFECTS = [
    # --- the defect and the eraser ---
    ("D1_the_defect_divides_by_the_wrong_modulus",
     "    return num // m if num % m == 0 else None",
     "    return num // (m * 3) if num % (m * 3) == 0 else None",
     "defects.defect_not_integral"),
    ("D2_the_defect_adds_where_it_must_subtract",
     "    num = b_of(word) - ((1 << q) - 3 ** ell) * r",
     "    num = b_of(word) + ((1 << q) - 3 ** ell) * r",
     "defects.defect_not_integral"),
    ("D3_the_defect_swaps_its_two_powers",
     "    num = b_of(word) - ((1 << q) - 3 ** ell) * r",
     "    num = b_of(word) - (3 ** q - (1 << ell)) * r",
     "defects.defect_not_integral"),
    ("D4_contiguity_is_declared_for_every_cycle",
     "            contiguous = all(b == a + 1 for a, b in zip(idxs, idxs[1:]))",
     "            contiguous = True",
     "defects.quotient_lift_violations_on_contiguous_cycles"),
    ("D5_contiguity_is_read_two_steps_apart",
     "            contiguous = all(b == a + 1 for a, b in zip(idxs, idxs[1:]))",
     "            contiguous = all(b == a + 2 for a, b in zip(idxs, idxs[1:]))",
     "instrument.failed"),
    ("D6_the_cycle_word_keeps_the_erased_labels",
     "            stack_e = stack_e[:p]",
     "            stack_e = stack_e[:p + 1]",
     "defects.cycle_does_not_return_to_its_residue"),
    ("D7_the_cycle_starts_at_the_wrong_stack_vertex",
     "            out.append((stack_v[p], cyc, stack_i[p], idx, contiguous))",
     "            out.append((stack_v[p], cyc, stack_i[p] + 1, idx, contiguous))",
     "defects.endpoints_not_congruent_to_the_residue"),

    # --- Theorem 3.1, the surplus budget ---
    ("D8_the_surplus_identity_forgets_its_baseline",
     "        if sum(q - 1 for q in w) != surplus or q_total != ceil_beta(h):",
     "        if sum(q for q in w) != surplus or q_total != ceil_beta(h):",
     "surplus.surplus_identity_violations"),
    ("D9_the_surplus_is_read_against_the_wrong_ceiling",
     "        surplus = q_total - h",
     "        surplus = q_total - h + 1",
     "surplus.surplus_identity_violations"),
    ("D10_the_alias_budget_charges_the_full_period",
     "            if a_k * max(1, s - 1) > surplus:",
     "            if a_k * max(1, s + 3) > surplus:",
     "surplus.budget_theorem_3_1_violations"),
    ("D11_the_alias_set_is_taken_below_the_period",
     "            a_k = sum(1 for q in w if q >= s)",
     "            a_k = sum(1 for q in w if q >= 1)",
     "surplus.budget_theorem_3_1_violations"),

    # --- Theorem 4.1, the faithful core ---
    ("D12_the_deletion_threshold_is_twice_the_modulus_again",
     "            bad = [q >= s for q in w]",
     "            bad = [q >= 2 * m for q in w]",
     "faithful_core.retained_edge_at_or_above_the_period"),
    ("D13_every_retained_edge_is_called_alias_large",
     "                        if q >= s:",
     "                        if q >= 1:",
     "faithful_core.retained_edge_at_or_above_the_period"),
    ("D14_the_uniqueness_scan_runs_past_the_period",
     "                            if [p for p in range(1, s)",
     "                            if [p for p in range(1, s + 2)",
     "faithful_core.label_not_unique_in_the_faithful_range"),
    ("D15_the_finite_bound_forgets_the_deleted_edges",
     "            lower = h + 1 - (a_k + 1) * s",
     "            lower = h + 1",
     "faithful_core.mass_below_the_finite_bound"),
    ("D16_the_high_lift_bound_forgets_the_low_vertices",
     "            if mass2 < max(0, h + 1 - (a_k + 2 * n_low + 1) * s):",
     "            if mass2 < max(0, h + 1):",
     "faithful_core.high_lift_mass_below_its_bound"),
    ("D17_the_cycle_length_bound_is_lowered_to_one",
     "                    if len(cyc) > s:",
     "                    if len(cyc) > 1:",
     "faithful_core.cycle_longer_than_the_period"),

    # --- Theorem 9.1 and the quotient lift ---
    ("D18_the_certificate_drops_its_affine_correction",
     "                if (((1 << q_c) - 3 ** l_c) * r - b_of(cyc)) % m:",
     "                if (((1 << q_c) - 3 ** l_c) * r) % m:",
     "defects.certificate_theorem_9_1_violations"),
    ("D19_the_certificate_reads_the_wrong_residue",
     "                if (((1 << q_c) - 3 ** l_c) * r - b_of(cyc)) % m:",
     "                if (((1 << q_c) - 3 ** l_c) * (r + 1) - b_of(cyc)) % m:",
     "defects.certificate_theorem_9_1_violations"),
    ("D20_the_quotient_digits_are_read_one_block_high",
     "                n, n2 = (x - r) // m, (z - r) // m",
     "                n, n2 = (x - r) // m + 1, (z - r) // m",
     "defects.quotient_lift_violations_on_contiguous_cycles"),
    ("D21_the_quotient_lift_swaps_its_two_powers",
     "                holds = (1 << q_c) * n2 == 3 ** l_c * n + dm",
     "                holds = 3 ** l_c * n2 == (1 << q_c) * n + dm",
     "defects.quotient_lift_violations_on_contiguous_cycles"),
    ("D22_the_quotient_lift_drops_the_defect",
     "                holds = (1 << q_c) * n2 == 3 ** l_c * n + dm",
     "                holds = (1 << q_c) * n2 == 3 ** l_c * n",
     "defects.quotient_lift_violations_on_contiguous_cycles"),
    ("D23_every_cycle_is_called_a_non_return",
     "                if cur != r:\n                    t[\"cycle_does_not_return_to_its_residue\"] += 1",
     "                if cur == r:\n                    t[\"cycle_does_not_return_to_its_residue\"] += 1",
     "defects.cycle_does_not_return_to_its_residue"),

    # --- Theorem 11.1, the semigroup law ---
    ("D24_the_true_law_swaps_its_coefficients",
     "        true_rhs = 3 ** len(d) * dc + (1 << sum(c)) * dd",
     "        true_rhs = (1 << sum(d)) * dc + 3 ** len(c) * dd",
     "semigroup.true_law_violations_on_distinct_pairs"),
    ("D25_the_true_law_reads_the_wrong_length",
     "        true_rhs = 3 ** len(d) * dc + (1 << sum(c)) * dd",
     "        true_rhs = 3 ** len(c) * dc + (1 << sum(c)) * dd",
     "semigroup.true_law_violations_on_distinct_pairs"),
    ("D26_the_swapped_law_is_made_identical_to_the_true_one",
     "        swapped = (1 << sum(d)) * dc + 3 ** len(c) * dd",
     "        swapped = 3 ** len(d) * dc + (1 << sum(c)) * dd",
     "semigroup.swapped_law_disagreeing_on_distinct_pairs"),
    ("D27_the_composition_is_taken_in_the_wrong_order",
     "        dcd = defect(tuple(c) + tuple(d), r, m)",
     "        dcd = defect(tuple(d) + tuple(c), r, m)",
     "semigroup.true_law_violations_on_distinct_pairs"),
    ("D28_the_pair_pool_admits_a_cycle_twice",
     "                if len(bucket) < 4 and cyc not in bucket:",
     "                if len(bucket) < 4:",
     "semigroup.pair_words_identical"),

    # --- Theorems 6.1 and 7.1, screening ---
    ("D29_the_endpoint_residue_forgets_its_inverse",
     "    return b_of(word) % m * pow(pow(2, sum(word), m), -1, m) % m",
     "    return b_of(word) % m * pow(2, sum(word), m) % m",
     "screening.endpoint_suffix_formula_violations"),
    ("D30_the_suffix_formula_walks_the_word_forwards",
     "        run += word[len(word) - j]",
     "        run += word[j - 1]",
     "screening.endpoint_suffix_formula_violations"),
    ("D31_the_suffix_formula_shifts_its_power_of_three",
     "        total = (total + 3 ** (j - 1) * pow(pow(2, run, m), -1, m)) % m",
     "        total = (total + 3 ** j * pow(pow(2, run, m), -1, m)) % m",
     "screening.endpoint_suffix_formula_violations"),
    ("D32_the_source_representative_drops_its_inverse",
     "    r = ((1 << q) - b_of(word)) % mod * pow(pow(3, ell, mod), -1, mod) % mod",
     "    r = ((1 << q) - b_of(word)) % mod * pow(3, ell, mod) % mod",
     "screening.source_screening_violations"),
    ("D33_the_prefix_modulus_loses_its_extra_bit",
     "            mod = 1 << (sum(pref) + 1)",
     "            mod = 1 << (sum(pref) + 4)",
     "screening.source_screening_violations"),
    ("D34_the_inside_probe_changes_nothing_at_all",
     "            inside = tuple(list(w[:-1]) + [w[-1] + 1])",
     "            inside = tuple(list(w[:-1]) + [w[-1]])",
     "screening.changes_inside_the_horizon_that_moved_nothing"),
    ("D35_the_outside_probe_changes_the_last_valuation",
     "                outside = tuple([w[0] + 2] + list(w[1:]))",
     "                outside = tuple(list(w[:-1]) + [w[-1] + 2])",
     "screening.changes_outside_the_horizon_that_moved_something"),
    ("D36_the_alternate_prefix_changes_the_suffix_too",
     "            alt = tuple([w[0] + 1] + list(w[1:]))",
     "            alt = tuple([w[0] + 1] + list(w[1:-1]) + [w[-1] + 1])",
     "screening.endpoint_screening_violations"),

    # --- their three cannot-fail blocks ---
    ("D37_the_arranged_inequality_is_reported_the_wrong_way",
     "        if not gamma < eta:",
     "        if gamma < eta:",
     "their_algebra.faithful_core_gamma_not_below_eta"),
    ("D38_the_two_assertions_are_compared_against_a_third_thing",
     "        if (1 - eta + gamma < 1) != (gamma < eta):",
     "        if (1 - eta + gamma < 1) != (gamma > eta):",
     "their_algebra.faithful_core_second_assertion_differing_from_the_first"),
    ("D39_the_loop_invariant_constant_is_recomputed_differently",
     "        if 2 - math.log2(3) != c_faith:",
     "        if 3 - math.log2(3) != c_faith:",
     "their_algebra.faithful_core_constant_varying_across_the_loop"),
    ("D40_the_horizon_margin_is_read_with_the_wrong_sign",
     "        if not val < 0:",
     "        if not val > 0:",
     "their_algebra.horizon_could_have_failed"),
    ("D41_the_near_full_ratio_is_inverted",
     "        ratio = 1 / (logh ** a)",
     "        ratio = logh ** a",
     "their_algebra.near_full_could_have_failed"),

    # --- published examples ---
    ("D42_the_example_defect_is_compared_at_the_wrong_residue",
     "        dm = defect(w, r, m)\n        if dm != ex[\"defect\"]:",
     "        dm = defect(w, r + 1, m)\n        if dm != ex[\"defect\"]:",
     "examples.defect_disagreeing"),
    ("D43_the_example_period_is_read_as_one",
     "        s = ord_two(round(math.log(m, 3)))",
     "        s = 1",
     "examples.label_at_or_above_the_period"),
    ("D44_the_example_certificate_drops_its_correction",
     "        if (((1 << sum(w)) - 3 ** len(w)) * r - b_of(w)) % m:",
     "        if (((1 << sum(w)) - 3 ** len(w)) * r) % m:",
     "examples.certificate_violations"),
    ("D45_the_example_word_is_walked_backwards",
     "        cur = r\n        for q in w:\n            cur = forward_target(cur, q, m)\n        if cur != r:\n            t[\"cycle_does_not_return\"] += 1",
     "        cur = r\n        for q in reversed(w):\n            cur = forward_target(cur, q, m)\n        if cur != r:\n            t[\"cycle_does_not_return\"] += 1",
     "examples.cycle_does_not_return"),

    # --- the instrument's own claims ---
    ("D46_the_composition_law_is_asserted_symmetric",
     "         != 3 ** len(c) * b_of(d) + (1 << sum(d)) * b_of(c))",
     "         == 3 ** len(c) * b_of(d) + (1 << sum(d)) * b_of(c))",
     "instrument.failed"),
    # `ord_two` lives in src67 and is imported, so it cannot be planted from
    # here. The instrument's own order self-test can.
    ("D47_the_order_self_test_expects_the_wrong_residue",
     "        if pow(2, s, m) != 1:\n            bad += 1",
     "        if pow(2, s, m) != 2:\n            bad += 1",
     "instrument.failed"),

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

    RUN-048 lost a drill to `OSError: [Errno 22]` on a restore write. The
    pristine sidecar recovered it, but a restore that can die is a restore that
    can leave a planted defect behind.
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
