"""RUN-050 mutation drill for `src69_defect_tree.py`.

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
    whose counter already reads zero is invisible, and so is LOOSENING one --
    so a defect aimed at an inequality multiplies the side it must not reach
    rather than deleting the comparison;
  * a defect that changes only OBSERVATIONS is a finding about the gate:
    RUN-048 had four such, all pointing at a section whose only failure
    counter compared against a vacuous bound;
  * two defects here aim at a NON-VACUITY entry rather than a failure counter
    (D31, D32). RUN-049's headline was a law whose second half was only an
    observation, so the populations that make a law non-degenerate are drilled
    like the law itself;
  * a defect that makes the gate RAISE is reported through
    `errors.<section>_raised` rather than crashing;
  * the pristine sidecar is written before anything is planted, every gate
    write retries a transient OS error, and the sidecar is removed only when
    the file is provably back.

Usage:
    python code/src69_drill.py --bundle <dir>
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
GATE = ROOT / "code" / "src69_defect_tree.py"
LIMIT = "220000"
GATE_TIMEOUT_SECONDS = 900

DEFECTS = [
    # --- the general path defect ---
    ("D1_the_defect_divides_by_the_wrong_modulus",
     "    return num // m if num % m == 0 else None",
     "    return num // (m * 3) if num % (m * 3) == 0 else None",
     "calculus.defect_not_integral"),
    ("D2_the_defect_swaps_its_two_powers",
     "    num = b_of(word) + 3 ** ell * r - (1 << q) * s",
     "    num = b_of(word) + (1 << ell) * r - 3 ** q * s",
     "calculus.defect_not_integral"),
    ("D3_the_defect_adds_where_it_must_subtract",
     "    num = b_of(word) + 3 ** ell * r - (1 << q) * s",
     "    num = b_of(word) + 3 ** ell * r + (1 << q) * s",
     "calculus.defect_not_integral"),

    # --- the quotient-affine product ---
    ("D4_the_product_attaches_each_coefficient_to_the_other_operand",
     "    return (a2 * a1, a2 * d1 + e1 * d2, e2 * e1)",
     "    return (a2 * a1, a1 * d2 + e2 * d1, e2 * e1)",
     "calculus.composition_theorem_4_1_violations"),
    ("D5_the_product_adds_its_diagonal",
     "    return (a2 * a1, a2 * d1 + e1 * d2, e2 * e1)",
     "    return (a2 * a1, a2 * d1 + e1 * d2, e2 + e1)",
     "calculus.diagonal_not_multiplicative"),

    # --- the eraser: the one line the round turns on ---
    # aimed at sibling disjointness, NOT at laminarity. Measured: the other
    # retention rule leaves the family laminar and contiguous (0 crossings, 0
    # non-contiguous, 0 misanchored) on all 18,603 levels, and Theorem 6.1
    # still reconstructs -- what it destroys is disjointness, 130,140 pairs
    # sharing a left endpoint where the paper's rule has none.
    ("D6_the_eraser_retains_the_first_occurrence_as_AU2d21_did",
     "            stack_t[p] = i",
     "            pass",
     "tree.intervals_sharing_a_left_endpoint"),
    # the comparison walker repeats this line verbatim, so the anchor has to
    # reach as far as `stack_t[p] = i` to name only the paper's rule
    ("D7_the_interval_starts_one_step_after_its_residue",
     "            out.append((stack_t[p], i, v))\n"
     "            for old in stack_v[p + 1:]:\n"
     "                pos.pop(old, None)\n"
     "            stack_v = stack_v[:p + 1]\n"
     "            stack_t = stack_t[:p + 1]\n"
     "            stack_t[p] = i",
     "            out.append((stack_t[p] + 1, i, v))\n"
     "            for old in stack_v[p + 1:]:\n"
     "                pos.pop(old, None)\n"
     "            stack_v = stack_v[:p + 1]\n"
     "            stack_t = stack_t[:p + 1]\n"
     "            stack_t[p] = i",
     "tree.interval_endpoints_not_congruent"),

    # --- Theorems 5.1 and 6.1, the tree ---
    ("D8_the_parent_is_the_outermost_enclosing_interval",
     "                if best is None or d - c < best_len:",
     "                if best is None or d - c > best_len:",
     "tree.tree_matrix_disagreeing_with_the_direct_one"),
    ("D9_the_tree_composes_its_children_in_reverse",
     "        acc = cmat if acc is None else mat_comp(acc, cmat)",
     "        acc = cmat if acc is None else mat_comp(cmat, acc)",
     "tree.tree_matrix_disagreeing_with_the_direct_one"),
    # reversing the endpoints makes the span defect non-integral before it can
    # disagree with anything, so the honest counter is the integrality one --
    # and before the None guard was added this crashed the section instead.
    ("D10_the_gap_before_a_child_reads_its_endpoints_backwards",
     "            mat = matrix_of(word[cur:ca], states[cur] % m, states[ca] % m, m)",
     "            mat = matrix_of(word[cur:ca], states[ca] % m, states[cur] % m, m)",
     "tree.node_span_defect_not_integral"),

    # --- Theorem 7.1, the root ---
    # `p < max` instead of `p <= max` is premise-empty here: it differs only
    # when an endpoint is an exact power of three, and 0 of 7,845 bridges have
    # one. The mutation that bites takes the modulus a full power too small.
    ("D11_the_canonical_modulus_stops_a_full_power_early",
     "    while p <= max(x, z):",
     "    while p <= max(x, z) // 3:",
     "root.canonical_modulus_not_above_both_endpoints"),
    ("D12_the_root_defect_reads_its_endpoints_backwards",
     "        if path_defect(w, X, Z, m) != 0:",
     "        if path_defect(w, Z, X, m) != 0:",
     "root.root_defect_not_zero"),

    # --- Theorem 7.2 and Corollary 7.3 ---
    ("D13_the_weighted_expansion_drops_its_two_power",
     "                terms.append(3 ** (h - b) * (1 << prefix_q) * d)",
     "                terms.append(3 ** (h - b) * d)",
     "root.expansion_theorem_7_2_violations"),
    ("D14_the_weighted_expansion_counts_its_three_power_forwards",
     "                terms.append(3 ** (h - b) * (1 << prefix_q) * d)",
     "                terms.append(3 ** b * (1 << prefix_q) * d)",
     "root.expansion_theorem_7_2_violations"),
    ("D15_the_ultrametric_pairing_looks_at_the_deepest_block",
     "                lo = min(nz)",
     "                lo = max(nz)",
     "root.ultrametric_minimum_not_paired"),

    # --- Theorem 12.1, the coboundary ---
    ("D16_the_prefix_coboundary_drops_its_power",
     "            if dp != (1 << qp) * n:",
     "            if dp != n:",
     "root.prefix_defect_not_the_coboundary"),
    ("D17_the_suffix_coboundary_loses_its_sign",
     "            if ds != -(3 ** ls) * n:",
     "            if ds != (3 ** ls) * n:",
     "root.suffix_defect_not_the_coboundary"),

    # --- Theorem 8.1, the activation depth ---
    ("D18_the_depth_equivalence_excludes_its_own_valuation",
     "                    if lifts != (extra <= nu):",
     "                    if lifts != (extra < nu):",
     "depth.depth_equivalence_violations"),
    ("D19_the_depth_probe_never_deepens_its_modulus",
     "                    mod2 = m * 3 ** extra",
     "                    mod2 = m * 3",
     "depth.depth_equivalence_violations"),

    # --- Theorem 9.1, the sign law ---
    ("D20_the_sign_law_reverses_its_supercriticality_test",
     "                sub_critical = (1 << q) <= 3 ** ell          # Q <= beta L",
     "                sub_critical = (1 << q) >= 3 ** ell          # Q <= beta L",
     "sign.sign_law_violations"),
    ("D21_the_float_route_is_given_a_wrong_beta",
     "                if sub_critical != (q <= beta_f * ell):",
     "                if sub_critical != (q <= 1.5 * ell):",
     "sign.float_sign_route_disagreeing_with_the_exact_one"),

    # --- Theorem 10.1, the resonance ---
    ("D22_the_resonance_divides_each_side_by_the_other_power",
     "                u1, u2 = n // (1 << q), n2 // (3 ** ell)",
     "                u1, u2 = n // (3 ** ell), n2 // (1 << q)",
     "sign.resonance_parameters_disagreeing"),
    ("D23_the_resonance_divisibility_test_is_swapped",
     "                if n % (1 << q) or n2 % (3 ** ell):",
     "                if n % (3 ** ell) or n2 % (1 << q):",
     "sign.resonance_n_not_a_multiple"),

    # --- Theorem 11.1, the lift toll (multiplied, never deleted) ---
    ("D24_the_inbound_toll_is_charged_six_bits_too_much",
     "                ok_in = (1 << (m_in + 1)) * z0 > (1 << q) * m",
     "                ok_in = (1 << (m_in + 1)) * z0 > (1 << q) * m * 64",
     "sign.lift_toll_in_violations"),
    ("D25_the_outbound_toll_is_charged_six_bits_too_much",
     "                ok_out = (1 << (m_out + 1)) * z0 > 3 ** ell * m",
     "                ok_out = (1 << (m_out + 1)) * z0 > 3 ** ell * m * 64",
     "sign.lift_toll_out_violations"),

    # --- Theorem 13.1, the quotient floor ---
    ("D26_the_quotient_floor_is_raised_three_bits",
     "            lhs = (n + 1) * m",
     "            lhs = (n + 1) * m // 8",
     "quotient_floor.quotient_floor_violations"),
    ("D27_the_float_floor_route_is_reversed",
     "            f = n > ((1 << (ms[ell] - 1)) * Z - m) / m - 1e-12",
     "            f = n < ((1 << (ms[ell] - 1)) * Z - m) / m - 1e-12",
     "quotient_floor.float_route_disagreeing_with_the_exact_one"),

    # --- Corollary 13.2, the claim with no counter of their own ---
    ("D28_the_corollary_parameter_window_is_left_unsatisfiable",
     "\n    gamma, eta = 0.20, 0.45",
     "\n    gamma, eta = 0.60, 0.45",
     "corollary.parameter_window_empty"),
    ("D29_the_retained_vertex_floor_is_raised_six_bits",
     "            if not (n + 1) * m_low > (1 << (ms[ell] - 1)) * Z:",
     "            if not (n + 1) * m_low > (1 << (ms[ell] - 1)) * Z * 64:",
     "corollary.retained_high_lift_vertex_below_the_floor"),

    # --- the published rows, the instrument, the artifacts, the ledger ---
    ("D30_the_published_lift_identity_is_read_backwards",
     '        if (1 << ex["Q"]) * n2 != 3 ** ex["length"] * n:',
     '        if (1 << ex["Q"]) * n != 3 ** ex["length"] * n2:',
     "examples.zero_node_lift_identity_violations"),
    # the sentinel this gate exists to avoid: a zero valuation would sort into
    # the ultrametric minimum and win it. Written as a RETURN change, never as
    # a guard change -- moving the guard sends v3(0) into a loop that never
    # divides down, and a hung gate is a malformed defect, not a catch.
    ("D33_the_valuation_of_zero_becomes_a_number",
     "    if x == 0:\n        return None",
     "    if x == 0:\n        return 0",
     "instrument.failed"),
    ("D34_the_digest_is_taken_over_the_file_name",
     "    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()",
     "    actual = {n: hashlib.sha256(n.encode()).hexdigest()",
     "artifacts.digest_mismatches"),
    ("D35_the_ledger_coverage_heuristic_accepts_anything",
     "        return hit >= max(1, len(words) // 2)",
     "        return True",
     "ledger.heuristic_failed_its_negative_control"),

    # --- aimed at NON-VACUITY, not at a failure counter ---
    ("D31_the_order_sensitive_population_is_emptied",
     "                if mat_comp(right, left) == comp:",
     "                if True:",
     "calculus.order_sensitive_compositions"),
    # the retention comparison is only evidence while the two rules actually
    # differ; make them identical and the whole of Finding 2 says nothing.
    ("D36_the_comparison_rule_is_made_identical_to_the_paper_rule",
     "            stack_t = stack_t[:p + 1]\n    return out",
     "            stack_t = stack_t[:p + 1]\n            stack_t[p] = i\n"
     "    return out",
     "retention.levels_where_the_two_rules_differ"),
    ("D32_the_nesting_population_is_emptied",
     "                    elif (c <= a and b <= d) or (a <= c and d <= b):\n"
     '                        t["nested_pairs"] += 1',
     "                    elif False:\n"
     '                        t["nested_pairs"] += 1',
     "tree.nested_pairs"),
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
