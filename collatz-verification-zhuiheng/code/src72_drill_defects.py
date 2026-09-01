"""The defect list for RUN-053's drill, kept beside the harness.

數學戰士「墜衡」 / AMRAL Research Lab.

Split out because several anchors carry embedded quotes and newlines, and a
list this size is easier to audit on its own than wedged into the runner.
"""

from __future__ import annotations

DEFECTS = [
    # --- the edge and its defect ---
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
    ("D3_the_binary_depth_is_defined_with_its_sign_reversed",
     "    c2, c3 = q + ap - a, 1 + b - bp",
     "    c2, c3 = q + a - ap, 1 + b - bp",
     "gates.zero_defect_depths_not_zero"),

    # --- Theorem 3.1, which is sharp at BOTH ends, so one unit is enough ---
    ("D4_the_strip_upper_end_is_pulled_below_its_attained_value",
     "        if not d < 3:",
     "        if not d < 2:",
     "strip.strip_upper_violations"),
    ("D5_the_strip_lower_end_is_pulled_in_two_bits",
     "        if not -(1 << q) < d:",
     "        if not -(1 << max(0, q - 2)) < d:",
     "strip.strip_lower_violations"),
    ("D6_a_positive_defect_is_allowed_only_the_value_one",
     "            if d not in (1, 2):",
     "            if d not in (1,):",
     "strip.positive_defect_not_one_or_two"),
    ("D7_the_inherited_block_bound_is_tightened",
     "        if not abs(d) < (1 << q) * 3:",
     "        if not abs(d) < (1 << q) // 4:",
     "strip.block_bound_from_the_previous_round_violations"),

    # --- Theorem 4.1, the atomic ternary-exclusive reset ---
    ("D8_the_atomic_reset_defect_is_named_one",
     '            if d != 2:\n                t["te_defect_not_two"] += 1',
     '            if d != 1:\n                t["te_defect_not_two"] += 1',
     "gates.te_defect_not_two"),
    ("D9_the_atomic_reset_valuation_is_named_two",
     "            if q != 1:",
     "            if q != 2:",
     "gates.te_valuation_not_one"),
    ("D10_the_atomic_reset_output_depths_are_demanded_positive",
     "            if not (ap == 0 and bp == 0):",
     "            if not (ap == 1 and bp == 1):",
     "gates.te_depths_wrong"),

    # --- Theorem 4.2, the binary-exclusive pump ---
    ("D11_the_binary_exclusive_defect_is_demanded_positive",
     "            if not d < 0:",
     "            if not d > 0:",
     "gates.be_defect_not_negative"),
    ("D12_the_binary_exclusive_valuation_floor_is_raised",
     "            if q < 2:",
     "            if q < 6:",
     "gates.be_valuation_below_two"),
    ("D13_the_binary_exclusive_ternary_depth_is_demanded_deeper",
     "            if bp < b + 1:",
     "            if bp < b + 4:",
     "gates.be_ternary_not_deeper"),
    ("D14_the_reservoir_bound_is_charged_four_extra_ternary_levels",
     "            exact = (1 << a) * 3 ** (b + 1) < (1 << q)",
     "            exact = (1 << a) * 3 ** (b + 5) < (1 << q)",
     "gates.be_reservoir_bound_violations"),
    ("D15_the_float_reservoir_route_is_shifted_far_out",
     "            if exact != (a + bf * (b + 1) < q + 1e-12):",
     "            if exact != (a + bf * (b + 1) < q - 40):",
     "gates.float_reservoir_route_disagreeing"),

    # --- Theorem 4.3, the synchronized normal form ---
    # the synthetic block repeats this line four spaces deeper, so the short
    # anchor matches it as a substring
    ("D16_the_synchronized_cylinder_swaps_its_two_units",
     "            if (1 << c2) * up != 3 ** c3 * u + om:\n"
     '                t["sync_cylinder_violations"] += 1',
     "            if (1 << c2) * u != 3 ** c3 * up + om:\n"
     '                t["sync_cylinder_violations"] += 1',
     "gates.sync_cylinder_violations"),
    ("D17_the_positive_normal_form_demands_the_other_parity",
     "                if not (d in (1, 2) and bp == 0 and om == 1\n"
     "                        and a == (0 if d == 1 else 1)):",
     "                if not (d in (1, 2) and bp == 0 and om == 1\n"
     "                        and a == (1 if d == 1 else 0)):",
     "gates.sync_positive_normal_form_violations"),
    ("D18_the_negative_reservoir_bound_is_charged_four_extra_levels",
     "                exact = (1 << a) * 3 ** bp < (1 << q)",
     "                exact = (1 << a) * 3 ** (bp + 4) < (1 << q)",
     "gates.sync_negative_reservoir_violations"),

    # --- Theorem 5.1 and its corollaries ---
    ("D19_the_transport_law_inverts_its_relative_defect_factor",
     "        rhs *= Fraction(3 * n + d, 3 * n)",
     "        rhs *= Fraction(3 * n, 3 * n + d)",
     "transport.transport_violations"),
    ("D20_the_transport_law_reads_its_ternary_depth_as_the_binary_one",
     "        rhs = (Fraction(3 ** c3) if c3 >= 0 else Fraction(1, 3 ** -c3))",
     "        rhs = (Fraction(3 ** c2) if c2 >= 0 else Fraction(1, 3 ** -c2))",
     "transport.transport_violations"),
    ("D21_the_seesaw_is_read_in_the_wrong_direction",
     '            if r["typ"] == "TE" and not up > u:',
     '            if r["typ"] == "TE" and not up < u:',
     "transport.exclusive_seesaw_violations"),

    # --- Theorem 6.1 and the window products ---
    ("D22_the_correction_product_swaps_its_two_powers",
     "        if Fraction(n1, n0) != Fraction(3 ** ell, 1 << q) * prod:",
     "        if Fraction(n1, n0) != Fraction(3 ** q, 1 << ell) * prod:",
     "windows.correction_product_violations"),
    ("D23_the_window_unit_transport_is_shifted_by_one",
     '        if Fraction(rows[-1]["up"], rows[0]["u"]) != uprod:',
     '        if Fraction(rows[-1]["up"], rows[0]["u"]) != uprod + 1:',
     "windows.unit_window_transport_violations"),
    ("D24_the_triangle_bound_is_asserted_with_its_terms_swapped",
     "            if one_du + abs(e) + 1e-12 < one_imb:",
     "            if one_du - abs(e) - 1e-12 < one_imb:",
     "windows.triangle_terms_with_negative_slack"),

    # --- their three synthetic blocks ---
    ("D25_the_synthetic_sync_equation_is_read_backwards",
     "                if (1 << c2) * up != 3 ** c3 * u + om:",
     "                if (1 << c2) * up != 3 ** c3 * u - om:",
     "synthetic.sync_equation_violations"),
    ("D26_the_synthetic_TE_formula_loses_its_offset",
     "        up = (1 << (a - 1)) * 3 ** (b + 1) * u + 1",
     "        up = u - 1",
     "synthetic.te_not_increasing"),
    ("D27_the_synthetic_BE_pump_loses_its_multiplier",
     "        ub = xi + (1 << c2b) * 3 ** g * upb",
     "        ub = xi",
     "synthetic.be_not_decreasing"),

    # --- the published rows, the instrument, the artifacts, the ledger ---
    ("D28_the_published_depths_are_recomputed_with_reversed_signs",
     '            if q + ex["Ap"] - ex["A"] != ex["c2"] or \\',
     '            if q + ex["A"] - ex["Ap"] != ex["c2"] or \\',
     "examples.depth_fields_disagreeing"),
    ("D29_the_published_strip_is_pulled_below_its_attained_value",
     "            if not -(1 << q) < d < 3:",
     "            if not -(1 << q) < d < 2:",
     "examples.strip_violations"),
    ("D30_the_valuation_of_zero_becomes_a_number",
     "    if n == 0:\n        return None\n    n, c = abs(n), 0",
     "    if n == 0:\n        return 10 ** 9\n    n, c = abs(n), 0",
     "instrument.failed"),
    ("D31_the_digest_is_taken_over_the_file_name",
     "    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()",
     "    actual = {n: hashlib.sha256(n.encode()).hexdigest()",
     "artifacts.digest_mismatches"),
    ("D32_the_ledger_coverage_heuristic_accepts_anything",
     "        return sum(1 for w in words if w[:7] in blob) "
     ">= max(1, len(words) // 2)",
     "        return True",
     "ledger.heuristic_failed_its_negative_control"),

    # --- aimed at NON-VACUITY, not at a failure counter. Five of this
    #     round's findings ARE controls, and a control that stops firing
    #     proves nothing, so each is drilled like a check.
    ("N1_the_attained_upper_end_population_is_emptied",
     '        if d == 2:\n            t["upper_end_attained"] += 1',
     '        if d == 5:\n            t["upper_end_attained"] += 1',
     "strip.upper_end_attained"),
    ("N2_the_broken_window_control_is_made_whole_again",
     "        cut = rows[:1] + rows[2:]",
     "        cut = rows[:]",
     "windows.broken_correction_product_failures"),
    ("N3_the_synthetic_sync_control_is_given_the_divisibility_back",
     "        up2 = num // (1 << c2)\n"
     "        if num > 0 and (1 << c2) * up2 != num:",
     "        up2 = num // (1 << c2)\n"
     "        if num > 0 and num % (1 << c2) == 0 "
     "and (1 << c2) * up2 != num:",
     "synthetic.sync_equation_violations_when_the_divisibility_is_dropped"),
    ("N4_the_synthetic_TE_control_is_given_its_multiplier_back",
     "        if not (0 * u + 1) > u:",
     "        if not (2 * u + 1) > u:",
     "synthetic.te_not_increasing_when_the_offset_is_removed"),
    ("N5_the_synthetic_BE_control_is_given_its_pump_back",
     "        if not xi > upb:",
     "        if not xi + (1 << c2b) * 3 ** g * upb > upb:",
     "synthetic.be_not_decreasing_when_the_pump_is_removed"),
    # `reservoir_tests` is incremented from BOTH the binary-exclusive and the
    # negative-synchronized branch, so zeroing one site leaves it populated.
    # A non-vacuity defect has to aim at a counter with a single increment.
    ("N6_the_positive_synchronized_population_is_emptied",
     '                t["sync_positive"] += 1',
     '                t["sync_positive"] += 0',
     "gates.sync_positive"),
    ("N7_the_ternary_exclusive_class_is_emptied",
     '    elif c3 > 0:\n        typ = "TE"',
     '    elif c3 > 10 ** 6:\n        typ = "TE"',
     "gates.ternary_exclusive"),
]
