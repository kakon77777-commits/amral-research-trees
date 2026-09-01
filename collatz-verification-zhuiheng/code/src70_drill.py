"""RUN-051 mutation drill for `src70_quotient_resonance.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch. RUN-050 had two anchors go
    non-unique the moment a comparison walker was added beside the real one;
  * "the mutation changes nothing" has four causes worth telling apart:
    unreachable, premise-empty, too weak, and mathematically identical to what
    it replaced (RUN-044's `2^-q` mod 3, RUN-045's modulus shrunk to a divisor,
    RUN-047's floor table, RUN-048's dropped modular inverse, RUN-050's
    `p < max` against `p <= max` where no endpoint is a power of three);
  * from a GREEN baseline a defect must make a counter RISE. Deleting a check
    whose counter already reads zero is invisible, and so is LOOSENING one --
    so a defect aimed at an inequality multiplies the side it must not reach;
  * a defect that changes only OBSERVATIONS is a finding about the gate;
  * five defects here aim at NON-VACUITY entries rather than failure counters
    (N1-N5). This round's findings are all about populations that are smaller
    than the counter reporting them, so the populations are drilled too;
  * a defect that makes the gate RAISE is reported through
    `errors.<section>_raised` rather than crashing;
  * the pristine sidecar is written before anything is planted, every gate
    write retries a transient OS error, and the sidecar is removed only when
    the file is provably back.

Usage:
    python code/src70_drill.py --bundle <dir>
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
GATE = ROOT / "code" / "src70_quotient_resonance.py"
LIMIT = "180000"
GATE_TIMEOUT_SECONDS = 900

DEFECTS = [
    # --- the defect and the quotient-affine identity ---
    ("D1_the_defect_divides_by_the_wrong_modulus",
     "    return num // m if num % m == 0 else None",
     "    return num // (m * 3) if num % (m * 3) == 0 else None",
     "resonance.defect_not_integral"),
    ("D2_the_defect_swaps_its_two_powers",
     "    num = b_of(word) + 3 ** ell * r - (1 << q) * s",
     "    num = b_of(word) + (1 << ell) * r - 3 ** q * s",
     "resonance.defect_not_integral"),
    ("D3_the_quotient_affine_identity_is_read_backwards",
     "                    if (1 << q) * n2 != 3 ** ell * n + d:",
     "                    if (1 << q) * n != 3 ** ell * n2 + d:",
     "resonance.quotient_affine_violations"),

    # --- Theorem 3.1, the parity-refined resonance ---
    ("D4_the_parity_refinement_demands_two_more_binary_digits",
     "                    if n % (1 << (q + 1)):",
     "                    if n % (1 << (q + 3)):",
     "resonance.parity_refinement_violations"),
    ("D5_the_output_form_loses_its_factor_of_two",
     "                    if n2 != 2 * 3 ** ell * v:",
     "                    if n2 != 3 ** ell * v:",
     "resonance.n_out_not_the_refined_form"),
    ("D6_the_supercriticality_test_is_reversed",
     "                    sup = (1 << q) > 3 ** ell",
     "                    sup = (1 << q) < 3 ** ell",
     "resonance.zero_defect_not_supercritical"),
    # 1.5 lies BELOW beta, so where Q > beta L already holds the two routes
    # agree and the mutation is invisible. The wrong constant has to be above
    # beta to separate them at all.
    ("D7_the_float_supercriticality_route_is_given_a_wrong_beta",
     "                    if sup != (q > bf * ell):",
     "                    if sup != (q > 10.0 * ell):",
     "resonance.float_supercritical_route_disagreeing"),

    # --- Theorem 4.1, the cross-adic transfer ---
    ("D8_the_binary_transfer_gains_where_it_must_spend",
     "                    if v2(n2) != v2(n) - q:",
     "                    if v2(n2) != v2(n) + q:",
     "resonance.cross_adic_two_violations"),
    ("D9_the_ternary_transfer_spends_where_it_must_gain",
     "                    if v3(n2) != v3(n) + ell:",
     "                    if v3(n2) != v3(n) - ell:",
     "resonance.cross_adic_three_violations"),

    # --- Theorem 5.1, the mechanical ceiling ---
    ("D10_the_mechanical_ceiling_is_one_lower_than_the_theorem",
     "    return ceil_beta(h) - ceil_beta(ell) - (h - ell)",
     "    return ceil_beta(h) - ceil_beta(ell) - (h - ell) - 1",
     "capacity.capacity_violations"),
    # dropping the leading 2 is invisible: unlike the per-position ceiling,
    # which is ATTAINED, the global H_max corollary has orders of slack. It
    # takes forty bits to reach it.
    ("D11_the_hmax_bound_is_raised_forty_bits",
     "        exact = (1 << (hmax + h)) < 2 * 3 ** h",
     "        exact = (1 << (hmax + h + 40)) < 2 * 3 ** h",
     "capacity.hmax_violations"),
    ("D12_the_float_hmax_route_is_inverted",
     "        if exact != (hmax < (bf - 1) * h + 1):",
     "        if exact != (hmax > (bf - 1) * h + 1):",
     "capacity.float_hmax_route_disagreeing"),

    # --- Theorem 6.1, the temporal delay (multiplied, never deleted) ---
    ("D13_the_lift_toll_is_charged_six_bits_too_much",
     "                    ok = (1 << m_in) * z0 > (1 << q) * m",
     "                    ok = (1 << m_in) * z0 > (1 << q) * m * 64",
     "delay.lift_toll_violations"),
    ("D14_the_float_toll_route_is_shifted_far_out",
     "                    if ok != (m_in > q + math.log2(m / z0) - 1e-12):",
     "                    if ok != (m_in > q + math.log2(m / z0) + 50):",
     "delay.float_toll_route_disagreeing"),
    ("D15_the_chained_delay_bound_is_raised_forty_bits",
     "                    if not 2 * 3 ** p * z0 > (1 << (q + p)) * m:",
     "                    if not 2 * 3 ** p * z0 > (1 << (q + p + 40)) * m:",
     "delay.chained_delay_violations"),
    ("D16_the_length_bound_is_raised_forty_bits",
     "                    lexact = 3 ** ell * m * (1 << p) < 2 * 3 ** p * z0",
     "                    lexact = 3 ** ell * m * (1 << (p + 40)) < 2 * 3 ** p * z0",
     "delay.length_bound_violations"),
    ("D17_the_float_length_route_is_made_unsatisfiable",
     "                    lf = ell < ((bf - 1) * p - math.log2(m / z0) + 1) / bf",
     "                    lf = ell < 0",
     "delay.float_length_route_disagreeing"),
    ("D18_the_capacity_side_of_the_delay_bound_is_halved",
     "                              or (1 << (cap + p)) < 2 * 3 ** p)",
     "                              or (1 << (cap + p)) < 3 ** p // 2)",
     "delay.capacity_below_the_delay_bound_violations"),

    # --- Theorem 7.1, the atomic classification ---
    ("D19_the_only_atomic_solution_is_named_wrongly",
     "            if (q, r) != (2, 1):",
     "            if (q, r) != (3, 1):",
     "atomic.solutions_other_than_q2_r1"),
    ("D20_the_atomic_transition_lands_at_the_wrong_state",
     "            if z != 1 + 6 * m * v:",
     "            if z != 1 + 5 * m * v:",
     "atomic.atomic_target_wrong"),
    ("D21_the_atomic_valuation_is_named_three",
     "            if q != 2:\n                t[\"atomic_valuation_not_two\"] += 1",
     "            if q != 3:\n                t[\"atomic_valuation_not_two\"] += 1",
     "atomic.atomic_valuation_not_two"),

    # --- Theorem 8.1, the q = 2 runs ---
    ("D22_the_run_start_loses_its_parity_bit",
     "                n0 = (1 << (2 * tt + 1)) * v",
     "                n0 = (1 << (2 * tt)) * v",
     "runs.valuation_not_two"),
    ("D23_the_run_endpoint_loses_its_factor_of_two",
     "                if nt != 2 * 3 ** tt * v:",
     "                if nt != 3 ** tt * v:",
     "runs.end_quotient_wrong"),
    ("D24_the_binary_spend_is_charged_once_per_step",
     "                if None in (a2, b2) or a2 - b2 != 2 * tt:",
     "                if None in (a2, b2) or a2 - b2 != tt:",
     "runs.two_adic_spend_wrong"),
    ("D25_the_ternary_gain_is_credited_twice_per_step",
     "                if None in (a3, b3) or b3 - a3 != tt:",
     "                if None in (a3, b3) or b3 - a3 != 2 * tt:",
     "runs.three_adic_gain_wrong"),

    # --- Theorems 15.1 and 16.1 ---
    ("D26_the_ternary_reset_lands_one_level_deep",
     "                            if v3(n2) != aa:",
     "                            if v3(n2) != aa + 1:",
     "reset.reset_violations"),
    ("D27_the_reset_converse_demands_five_more_levels",
     "                            if v3(n2) is None or v3(n2) < ell:",
     "                            if v3(n2) is None or v3(n2) < ell + 5:",
     "reset.converse_violations"),
    ("D28_the_replenishment_congruence_is_three_bits_deeper",
     "                        rhs = val % (1 << (q + bb)) == 0",
     "                        rhs = val % (1 << (q + bb + 3)) == 0",
     "reset.replenishment_forward_violations"),
    ("D29_the_replenishment_depth_is_read_three_too_high",
     "                        lhs = nu is not None and nu >= bb",
     "                        lhs = nu is not None and nu >= bb + 3",
     "reset.replenishment_converse_violations"),

    # --- their three synthetic blocks ---
    ("D30_the_telescoping_sum_is_off_by_one",
     "        telq = s2[0] + sum(ag2) - e2[-1]",
     "        telq = s2[0] + sum(ag2) - e2[-1] + 1",
     "synthetic.telescoping_Q_violations"),
    ("D31_the_synthetic_supercriticality_test_doubles_its_length",
     "        return (lq != telq, ll != tell, not lq > bf * ll,",
     "        return (lq != telq, ll != tell, not lq > bf * ll * 2,",
     "synthetic.supercriticality_violations"),
    ("D32_the_reservoir_assertion_asks_for_ten_times_the_margin",
     "            if not (lower2 / h > bf * 0.019 and lower3 / h > 0.019):",
     "            if not (lower2 / h > bf * 0.19 and lower3 / h > 0.19):",
     "synthetic.reservoir_assertion_violations"),

    # --- the published rows, the instrument, the artifacts, the ledger ---
    ("D33_the_published_parity_form_demands_one_more_bit",
     '        if n % (1 << (q + 1)) or n2 != 2 * 3 ** ell * (n // (1 << (q + 1))):',
     '        if n % (1 << (q + 2)) or n2 != 2 * 3 ** ell * (n // (1 << (q + 2))):',
     "examples.parity_refinement_violations"),
    ("D34_the_published_valuation_fields_are_read_crosswise",
     '        if (v2(n) != ex["nu2_in"] or v2(n2) != ex["nu2_out"]',
     '        if (v2(n) != ex["nu2_out"] or v2(n2) != ex["nu2_in"]',
     "examples.valuation_fields_disagreeing"),
    # their v2/v3 return 10**9 for zero, which sorts into comparisons; mine
    # returns None, which cannot. This plants their sentinel.
    ("D35_the_binary_valuation_of_zero_becomes_a_number",
     "    if n == 0:\n        return None\n    n, a = abs(n), 0\n"
     "    while n % 2 == 0:",
     "    if n == 0:\n        return 10 ** 9\n    n, a = abs(n), 0\n"
     "    while n % 2 == 0:",
     "instrument.failed"),
    ("D36_the_digest_is_taken_over_the_file_name",
     "    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()",
     "    actual = {n: hashlib.sha256(n.encode()).hexdigest()",
     "artifacts.digest_mismatches"),
    ("D37_the_ledger_coverage_heuristic_accepts_anything",
     "        return sum(1 for w in words if w[:7] in blob) >= max(1, len(words) // 2)",
     "        return True",
     "ledger.heuristic_failed_its_negative_control"),

    # --- aimed at NON-VACUITY, not at a failure counter ---
    ("N1_the_reservoir_guard_is_made_to_never_open",
     "        if r0 / h > theta + 0.02:",
     "        if r0 / h > 2:",
     "synthetic.reservoir_guard_opened"),
    ("N2_the_broken_control_input_is_made_identical_to_the_real_one",
     "            if broken:\n                q = max(1, q - 3)",
     "            if broken:\n                q = max(1, q - 0)",
     "synthetic.supercriticality_red_on_broken_input"),
    ("N3_every_nonzero_defect_is_called_low_activation",
     "                        if aa < ell:",
     "                        if aa < ell + 100:",
     "reset.high_activation_nodes"),
    ("N4_the_attained_capacity_population_is_emptied",
     "            if slack == 0:",
     "            if slack == -1:",
     "capacity.positions_attaining_the_capacity"),
    ("N5_the_atomic_solution_population_is_emptied",
     "            if r >= 1:",
     "            if r >= 2:",
     "atomic.solutions_found"),
]

CONTROLS = [
    ("C1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
    ("C2_a_blank_line_is_not_a_defect", b"\n"),
]


def write_gate(data: bytes, tries: int = 8) -> None:
    """Write the gate, retrying a transient OS error.

    RUN-048 lost a drill to `OSError: [Errno 22]` on a restore write. A restore
    that can die is a restore that can leave a planted defect behind.
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
