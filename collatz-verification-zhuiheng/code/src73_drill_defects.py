"""The defect list for RUN-054's drill, kept beside the harness.

數學戰士「墜衡」 / AMRAL Research Lab.

Split out for the same reason as RUN-053's: several anchors carry embedded
quotes and newlines, and a list this size audits better on its own.
"""

from __future__ import annotations

DEFECTS = [
    # --- the edge ---
    ("D1_the_edge_defect_adds_where_it_must_subtract",
     "    num = 1 + 3 * r - (1 << q) * s",
     "    num = 1 + 3 * r + (1 << q) * s",
     "population.malformed_edges"),
    # the published-row check repeats this comparison, so the anchor has to
    # reach the line only `edge()` has
    ("D2_the_quotient_identity_is_read_backwards",
     "    if (1 << q) * n2 != 3 * n + d:\n"
     '        return "quotient identity failed"',
     "    if (1 << q) * n != 3 * n2 + d:\n"
     '        return "quotient identity failed"',
     "population.malformed_edges"),
    ("D3_the_ternary_depth_is_defined_with_its_sign_reversed",
     "    c2, c3 = q + ap - a, 1 + b - bp",
     "    c2, c3 = q + ap - a, 1 + bp - b",
     "sync_toll.reservoir_depth_disagreeing_with_a_nonneg_valuation"),

    # --- Theorem 3.1, the transport identity, exact ---
    ("D4_the_transport_law_inverts_its_relative_defect_factor",
     "        rhs *= Fraction(3 * n + d, 3 * n)",
     "        rhs *= Fraction(3 * n, 3 * n + d)",
     "transport.exact_transport_violations"),
    ("D5_the_transport_law_reads_its_ternary_depth_as_the_binary_one",
     "        rhs = (Fraction(3 ** c3) if c3 >= 0 else Fraction(1, 3 ** -c3))",
     "        rhs = (Fraction(3 ** c2) if c2 >= 0 else Fraction(1, 3 ** -c2))",
     "transport.exact_transport_violations"),
    ("D6_their_float_tolerance_is_tightened_past_the_error_it_covers",
     "        if not err < 2e-11:",
     "        if not err < 1e-18:",
     "transport.float_transport_violations_at_their_tolerance"),

    # --- their synchronized reservoir toll, three definitional clauses ---
    ("D7_the_depth_clause_demands_two_more_levels",
     "        if not b >= c3 - 1:",
     "        if not b >= c3 + 1:",
     "sync_toll.reservoir_depth_violations"),
    ("D8_the_quotient_floor_is_raised_two_powers",
     "        if not n >= 3 ** (c3 - 1):",
     "        if not n >= 3 ** (c3 + 1):",
     "sync_toll.quotient_floor_violations"),
    ("D9_the_c3_floor_is_raised",
     "        if not c3 >= 1:",
     "        if not c3 >= 3:",
     "sync_toll.c3_below_one"),
    ("D10_the_depth_comparison_is_shifted_by_one",
     "        if (b >= c3 - 1) != (bp >= 0):",
     "        if (b >= c3 - 1) != (bp >= 1):",
     "sync_toll.reservoir_depth_disagreeing_with_a_nonneg_valuation"),
    ("D11_the_branch_comparison_is_shifted_by_one",
     "        if (c3 >= 1) != (c3 > 0):",
     "        if (c3 >= 1) != (c3 > 1):",
     "sync_toll.c3_at_least_one_disagreeing_with_the_branch"),

    # --- the variation-transfer bound ---
    ("D12_the_per_term_reverse_triangle_is_asserted_the_wrong_way",
     "        if abs(du - imb) > e + 1e-12:",
     "        if abs(du - imb) > e / 1000 - 1e-12:",
     "variation.terms_with_negative_slack"),
    ("D13_the_window_bound_is_tightened_far_past_its_slack",
     "        if not abs(tv - j) <= e + 2e-10:",
     "        if not abs(tv - j) <= e / 1000:",
     "variation.window_violations"),

    # --- Lemma 7.1, in exact rationals ---
    ("D14_the_separation_is_compared_against_the_wrong_side",
     "        if not num * q_local * b > den:",
     "        if not num * q_local * b > den * 100:",
     "cf.separation_violations"),
    ("D15_the_local_partial_quotient_maximum_is_taken_too_small",
     "    q_local = mb + 2",
     "    q_local = 1",
     "cf.separation_violations"),
    ("D16_the_nearest_integer_is_rounded_from_the_wrong_end",
     "        a_hi = (2 * ph * b + qh) // (2 * qh)",
     "        a_hi = (2 * ph * b + qh) // (2 * qh) + 1",
     "cf.b_values_the_bracket_could_not_decide"),
    # appending the disputed `a_lo` is invisible, and that is not a gap in the
    # instrument: when the bracket cannot decide a term, `a_lo` may still be
    # the CORRECT one, so the convergent stays a best approximation.
    # Uncertified is not the same as wrong. Only a term that is actually wrong
    # breaks the best-approximation property the instrument tests.
    ("D17_the_certified_prefix_accepts_a_term_that_is_actually_wrong",
     "        if a_lo != a_hi:\n            break",
     "        if a_lo != a_hi:\n            out.append(a_lo + 5)\n            break",
     "instrument.failed"),

    # --- Theorems 8.1 and 9.1 ---
    ("D18_the_gate_count_master_is_raised_a_hundredfold",
     "            if not j * q_local * s + Fraction(1, 10 ** 9) >= n * n:",
     "            if not j * q_local * s + Fraction(1, 10 ** 9) >= n * n * 100:",
     "masters.gate_count_master_violations"),
    ("D19_the_workload_depth_master_is_raised_a_hundredfold",
     "            if not j * q_local * d * d + Fraction(1, 10 ** 9) >= s:",
     "            if not j * q_local * d * d + Fraction(1, 10 ** 9) >= s * 100:",
     "masters.workload_depth_master_violations"),
    ("D20_the_monotone_run_bound_drops_its_run_count",
     "        if not tv <= runs * h + 1e-10:",
     "        if not tv <= h + 1e-10:",
     "masters.monotone_run_violations"),
    ("D21_the_coarea_identity_is_tightened_past_float_noise",
     "        if not abs(integ - tv) < 1e-8:",
     "        if not abs(integ - tv) < 1e-30:",
     "masters.coarea_identity_violations"),
    ("D22_the_coarea_crossing_bound_drops_its_maximum",
     "        if not mx * h + 1e-10 >= tv:",
     "        if not h + 1e-10 >= tv:",
     "masters.coarea_max_crossing_violations"),

    # --- their exponent block ---
    ("D23_the_exponent_half_space_is_asserted_above_its_own_threshold",
     "            if not lhs >= 1 - 1e-12:",
     "            if not lhs >= 2 - 1e-12:",
     "exponent.half_space_violations"),
    ("D24_the_guard_implication_is_read_the_wrong_way",
     "        if lhs < 1 - 1e-12 and lhs < 1 + 1e-12:",
     "        if lhs > 1 - 1e-12 and lhs < 1 + 1e-12:",
     "exponent.assert_not_implied"),

    # --- the published rows, artifacts, ledger, instrument ---
    # A and A' coincide on every published row, so reversing that difference
    # is invisible; shifting the compared value is not
    ("D25_the_published_depths_are_recomputed_one_off",
     '            if (q + ex["Ap"] - ex["A"] != ex["c2"]',
     '            if (q + ex["Ap"] - ex["A"] != ex["c2"] + 1',
     "examples.depth_fields_disagreeing"),
    ("D26_the_published_rows_are_required_to_be_unsynchronized",
     '            if not (ex["c2"] > 0 and ex["c3"] > 0):',
     '            if not (ex["c2"] < 0 and ex["c3"] < 0):',
     "examples.class_not_synchronized"),
    ("D27_the_published_quotient_identity_is_read_backwards",
     "            if (1 << q) * n2 != 3 * n + d:",
     "            if (1 << q) * n != 3 * n2 + d:",
     "examples.quotient_identity_violations"),
    ("D28_the_digest_is_taken_over_the_file_name",
     "    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()",
     "    actual = {n: hashlib.sha256(n.encode()).hexdigest()",
     "artifacts.digest_mismatches"),
    ("D29_the_ledger_coverage_heuristic_accepts_anything",
     "        return sum(1 for w in words if w[:7] in blob) "
     ">= max(1, len(words) // 2)",
     "        return True",
     "ledger.heuristic_failed_its_negative_control"),
    ("D30_the_valuation_of_zero_becomes_a_number",
     "    if n == 0:\n        return None\n    n, c = abs(n), 0",
     "    if n == 0:\n        return 10 ** 9\n    n, c = abs(n), 0",
     "instrument.failed"),

    # --- aimed at NON-VACUITY, not at a failure counter ---
    ("N1_the_certified_prefix_is_cut_to_nothing",
     "def certified_cf(cap: int = 80):",
     "def certified_cf(cap: int = 0):",
     "cf.certified_partial_quotients"),
    ("N2_the_broken_window_control_is_left_unbroken",
     "        tv2 = tv - abs(math.log2(rows[1][\"up\"] / rows[1][\"u\"])) + 40.0",
     "        tv2 = tv",
     "variation.broken_window_failures"),
    ("N3_the_exponent_assert_is_never_reached",
     "        if feasible:",
     "        if feasible or True:",
     "exponent.reached_the_assert"),
    ("N4_the_monotone_run_guard_never_opens",
     "        if h <= 1e-14:",
     "        if h <= 1e14:",
     "masters.run_guard_opened"),
    ("N5_the_synchronized_population_is_emptied",
     '        if r["typ"] != "sync":',
     '        if r["typ"] != "SYNC":',
     "sync_toll.sync_edges"),
    ("N6_the_provenance_note_is_looked_for_under_the_wrong_name",
     '    t["provenance_note_present"] = int((bundle / PROVENANCE).exists())',
     '    t["provenance_note_present"] = int((bundle / "nope.md").exists())',
     "constants.provenance_note_present"),

    # --- aimed at the artifact-defect field, which is neither a failure
    #     counter nor a population. This one already reports a real defect, so
    #     the defect that tests it must make it report MORE, not less: a
    #     mutation that empties it would be a vanishing, and from a known state
    #     only a rise is visible.
    ("A1_the_validation_record_check_reports_every_file_it_names",
     '    t["validation_names_a_file_not_in_the_bundle"] = sorted(\n'
     "        n for n in named if n not in actual)",
     '    t["validation_names_a_file_not_in_the_bundle"] = sorted(\n'
     "        n for n in named if n in actual)",
     "artifacts.validation_names_a_file_not_in_the_bundle"),
]
