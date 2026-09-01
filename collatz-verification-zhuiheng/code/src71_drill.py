"""RUN-052 mutation drill for `src71_compensation.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch. Two lines in this gate differ only
    by indentation, so a short anchor matches the wrong one as a substring;
  * "the mutation changes nothing" has four causes worth telling apart:
    unreachable, premise-empty, too weak, and mathematically identical to what
    it replaced. RUN-051 supplied two more of the third kind -- 1.5 lies below
    beta, and a corollary's `+1` was not load-bearing;
  * from a GREEN baseline a defect must make a counter RISE. Deleting a check
    whose counter reads zero is invisible, and so is LOOSENING one -- so a
    defect aimed at an inequality multiplies the side it must not reach, and
    both bounds here carry a spare factor of three, so it takes more than one;
  * six defects aim at NON-VACUITY entries rather than failure counters
    (N1-N6). Two of this round's findings ARE controls -- a broken partition
    and a free quadrant -- and a control that stops firing proves nothing;
  * a defect that makes the gate RAISE is reported through
    `errors.<section>_raised` rather than crashing;
  * the pristine sidecar is written before anything is planted, every gate
    write retries a transient OS error, and the sidecar is removed only when
    the file is provably back.

Usage:
    python code/src71_drill.py --bundle <dir>
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
GATE = ROOT / "code" / "src71_compensation.py"
GATE_TIMEOUT_SECONDS = 900

DEFECTS = [
    # --- the segment, the defect, the two depths ---
    ("D1_the_defect_adds_where_it_must_subtract",
     "    num = bc + 3 ** ell * r - (1 << q) * s",
     "    num = bc + 3 ** ell * r + (1 << q) * s",
     "population.malformed_segments"),
    ("D2_the_affine_identity_is_read_backwards",
     "    if (1 << q) * z != 3 ** ell * x + bc:",
     "    if (1 << q) * x != 3 ** ell * z + bc:",
     "population.malformed_segments"),
    ("D3_the_binary_depth_is_defined_with_its_sign_reversed",
     '            "c2": q + ap - a, "c3": ell + bt - bp, "word": word, "M": m}',
     '            "c2": q + a - ap, "c3": ell + bt - bp, "word": word, "M": m}',
     "equivalence.equivalence_violations"),
    ("D4_the_ternary_depth_is_defined_with_its_sign_reversed",
     '            "c2": q + ap - a, "c3": ell + bt - bp, "word": word, "M": m}',
     '            "c2": q + ap - a, "c3": ell + bp - bt, "word": word, "M": m}',
     "equivalence.equivalence_violations"),

    # --- Theorem 4.1 and Theorem 5.1 ---
    ("D5_the_affine_upper_bound_is_halved",
     "        tight = (1 << (q - ell)) * (3 ** ell - (1 << ell))\n"
     "        if not bc > 0:\n"
     '            t["affine_lower_bound_violations"] += 1',
     "        tight = (1 << (q - ell)) * (3 ** ell - (1 << ell)) // 2\n"
     "        if not bc > 0:\n"
     '            t["affine_lower_bound_violations"] += 1',
     "bounds.affine_upper_bound_violations"),
    ("D6_the_affine_lower_bound_is_inverted",
     "        if not bc > 0:\n"
     '            t["affine_lower_bound_violations"] += 1',
     "        if not bc < 0:\n"
     '            t["affine_lower_bound_violations"] += 1',
     "bounds.affine_lower_bound_violations"),
    # the barrier is loose by exactly three, so a halving is invisible
    ("D7_the_defect_barrier_is_tightened_past_its_spare_factor",
     "        if not abs(d) < (1 << q) * 3 ** ell:\n"
     '            t["barrier_violations"] += 1',
     "        if not abs(d) < (1 << q) * 3 ** ell // 27:\n"
     '            t["barrier_violations"] += 1',
     "bounds.barrier_violations"),
    ("D8_the_sharpened_barrier_is_tightened_nine_fold",
     "        sharp = (1 << q) * 3 ** (ell - 1)",
     "        sharp = (1 << q) * 3 ** (ell - 1) // 9",
     "bounds.sharpened_barrier_violations"),

    # --- Theorem 6.1 and Corollary 6.2 ---
    ("D9_zero_compensation_needs_only_one_depth_to_vanish",
     "        zero_comp = (c2 == 0 and c3 == 0)",
     "        zero_comp = (c2 == 0 or c3 == 0)",
     "equivalence.equivalence_violations"),
    ("D10_the_no_double_deficit_test_demands_both_depths",
     "        if not (c2 > 0 or c3 > 0):",
     "        if not (c2 > 0 and c3 > 0):",
     "equivalence.double_deficit_violations"),

    # --- Theorems 7.1 and 7.2, which their report never counts ---
    ("D11_the_binary_alignment_valuation_is_one_too_deep",
     "            elif vp(d, 2) != a:",
     "            elif vp(d, 2) != a + 1:",
     "alignment.binary_valuation_violations"),
    ("D12_the_binary_alignment_congruence_loses_its_sign",
     "            if ((d >> a) + 3 ** ell * (n >> a)) % (1 << c2):",
     "            if ((d >> a) - 3 ** ell * (n >> a)) % (1 << c2):",
     "alignment.binary_congruence_violations"),
    ("D13_the_ternary_alignment_valuation_is_one_too_deep",
     "            elif vp(d, 3) != bp:",
     "            elif vp(d, 3) != bp + 1:",
     "alignment.ternary_valuation_violations"),
    ("D14_the_ternary_alignment_congruence_loses_its_sign",
     "            if ((d // 3 ** bp) - (1 << q) * (n2 // 3 ** bp)) % (3 ** c3):",
     "            if ((d // 3 ** bp) + (1 << q) * (n2 // 3 ** bp)) % (3 ** c3):",
     "alignment.ternary_congruence_violations"),

    # --- Theorems 8.1 and 9.1 ---
    ("D15_the_cylinder_equation_swaps_its_two_units",
     "        if (1 << c2) * up != 3 ** c3 * u + om:",
     "        if (1 << c2) * u != 3 ** c3 * up + om:",
     "primitive.cylinder_equation_violations"),
    ("D16_the_primitive_omega_is_divided_by_the_wrong_ternary_power",
     "        om = d // ((1 << a) * 3 ** bp)",
     "        om = d // ((1 << a) * 3 ** bt)",
     "primitive.omega_not_coprime_to_six"),
    ("D17_the_primitive_unit_keeps_its_ternary_part",
     "        u = n // ((1 << a) * 3 ** bt)",
     "        u = n // (1 << a)",
     "primitive.u_not_coprime_to_six"),
    ("D18_the_crt_window_is_tightened_past_its_spare_factor",
     "        if not lhs < dmod:",
     "        if not lhs * 81 < dmod:",
     "primitive.crt_window_violations"),
    ("D19_the_sharpened_window_is_tightened_three_fold",
     "        if not 3 * lhs <= dmod:",
     "        if not 9 * lhs <= dmod:",
     "primitive.sharpened_window_violations"),

    # --- Theorem 11.1, and the two predicates that restate their hypotheses ---
    ("D20_the_ternary_overdrain_demands_five_more_levels",
     "            if not bp >= bt + ell:",
     "            if not bp >= bt + ell + 5:",
     "trichotomy.ternary_overdrain_violations"),
    ("D21_the_binary_overdrain_demands_five_more_levels",
     "            if not a - ap >= q:",
     "            if not a - ap >= q + 5:",
     "trichotomy.binary_overdrain_violations"),
    ("D22_the_ternary_predicate_comparison_is_shifted_by_one",
     "        if (c3 <= 0) != (bp >= bt + ell):",
     "        if (c3 <= 0) != (bp >= bt + ell + 1):",
     "trichotomy.c3_nonpositive_disagreeing_with_B_prime_bound"),
    ("D23_the_binary_predicate_comparison_is_shifted_by_one",
     "        if (c2 <= 0) != (a - ap >= q):",
     "        if (c2 <= 0) != (a - ap >= q + 1):",
     "trichotomy.c2_nonpositive_disagreeing_with_A_bound"),

    # --- Theorem 12.1 ---
    ("D24_the_binary_telescoping_adds_where_it_must_subtract",
     '        if sum(x["c2"] for x in rows) != q + rows[-1]["Ap"] - rows[0]["A"]:',
     '        if sum(x["c2"] for x in rows) != q + rows[-1]["Ap"] + rows[0]["A"]:',
     "telescoping.binary_telescoping_violations"),
    ("D25_the_ternary_telescoping_adds_where_it_must_subtract",
     '        if sum(x["c3"] for x in rows) != ell + rows[0]["Bt"] - rows[-1]["Bp"]:',
     '        if sum(x["c3"] for x in rows) != ell + rows[0]["Bt"] + rows[-1]["Bp"]:',
     "telescoping.ternary_telescoping_violations"),

    # --- their two synthetic blocks ---
    ("D26_the_random_word_bound_is_halved",
     "        tight = (1 << (q - ell)) * (3 ** ell - (1 << ell))\n"
     "        if not bc > 0:\n"
     '            t["word_lower_bound_violations"] += 1',
     "        tight = (1 << (q - ell)) * (3 ** ell - (1 << ell)) // 2\n"
     "        if not bc > 0:\n"
     '            t["word_lower_bound_violations"] += 1',
     "synthetic.word_upper_bound_violations"),
    ("D27_the_quadrant_divisibility_modulus_gains_a_seven",
     "        return d % mod == 0, (d == 0 or abs(d) >= mod), d == 0",
     "        return d % (mod * 7) == 0, (d == 0 or abs(d) >= mod), d == 0",
     "synthetic.quadrant_divisibility_violations"),

    # --- the published rows, the instrument, the artifacts, the ledger ---
    ("D28_the_published_depths_are_recomputed_with_reversed_signs",
     '            if q + ap - a != ex["c2"] or ell + bt - bp != ex["c3"]:',
     '            if q + a - ap != ex["c2"] or ell + bp - bt != ex["c3"]:',
     "examples.depth_fields_disagreeing"),
    ("D29_the_published_barrier_is_tightened_past_its_spare_factor",
     "            if not abs(d) < (1 << q) * 3 ** ell:\n"
     '                t["barrier_violations"] += 1',
     "            if not abs(d) < (1 << q) * 3 ** ell // 27:\n"
     '                t["barrier_violations"] += 1',
     "examples.barrier_violations"),
    ("D30_the_valuation_of_zero_becomes_a_number",
     "    if n == 0:\n        return None\n    n, c = abs(n), 0",
     "    if n == 0:\n        return 10 ** 9\n    n, c = abs(n), 0",
     "instrument.failed"),
    ("D31_the_digest_is_taken_over_the_file_name",
     "    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()",
     "    actual = {n: hashlib.sha256(n.encode()).hexdigest()",
     "artifacts.digest_mismatches"),
    ("D32_the_ledger_coverage_heuristic_accepts_anything",
     "        return sum(1 for w in words if w[:7] in blob) >= max(1, len(words) // 2)",
     "        return True",
     "ledger.heuristic_failed_its_negative_control"),

    # --- aimed at NON-VACUITY, not at a failure counter ---
    ("N1_the_attained_affine_bound_population_is_emptied",
     "        if bc == tight:\n"
     '            t["affine_upper_bound_attained"] += 1',
     "        if bc == tight + 1:\n"
     '            t["affine_upper_bound_attained"] += 1',
     "bounds.affine_upper_bound_attained"),
    ("N2_the_attained_sharpened_barrier_population_is_emptied",
     "        if abs(d) == sharp:",
     "        if abs(d) == sharp + 1:",
     "bounds.sharpened_barrier_attained"),
    # the telescoping control: restore consecutiveness and it stops firing
    # dropping only the `+ 1` is not enough: the `if v > u + 1` filter still
    # removes single-step blocks, and a missing block breaks the chain just as
    # a shifted one does. The control has to be restored whole.
    ("N3_the_broken_partition_control_is_made_consecutive_again",
     "        shifted = [segment(st, qs, u + 1, v, m)\n"
     "                   for u, v in zip(pts, pts[1:]) if v > u + 1]",
     "        shifted = [segment(st, qs, u, v, m)\n"
     "                   for u, v in zip(pts, pts[1:])]",
     "telescoping.broken_binary_telescoping_failures"),
    # the quadrant control: put the constraint back and it stops firing
    ("N4_the_free_quadrant_control_is_given_the_constraint_back",
     "            a = rng2.randint(0, q + ap + 8)\n"
     "            bp = rng2.randint(0, bt + ell + 8)",
     "            a = rng2.randint(q + ap, q + ap + 8)\n"
     "            bp = rng2.randint(bt + ell, bt + ell + 8)",
     "synthetic.free_quadrant_divisibility_failures"),
    ("N5_the_binary_exclusive_class_is_emptied",
     "        if c2 > 0 and c3 <= 0:",
     "        if c2 > 0 and c3 <= -100:",
     "trichotomy.binary_exclusive"),
    ("N6_the_binary_alignment_population_is_emptied",
     "        if c2 > 0:\n"
     '            t["binary_alignment_population"] += 1',
     "        if c2 > 10 ** 6:\n"
     '            t["binary_alignment_population"] += 1',
     "alignment.binary_alignment_population"),
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
            [sys.executable, str(GATE), "--bundle", str(bundle)],
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
        "gate": GATE.name,
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
