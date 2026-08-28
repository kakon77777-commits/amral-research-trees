"""Can the item-52 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src52_farey_entropy.py` reports that section 3's binary bridge and concatenation
law are exact, that section 5's rational-Catalan capacity agrees with brute-force
enumeration on 34 coprime pairs up to 3876 members, that section 6's B-to-B class
modulo `2^(p+2)` holds in both directions, and that the published continued
fractions are what `theta = beta - 1` requires.

D15 replants this run's own near-miss: I expected `theta` to be `1/beta` and its
published expansion looked one term short. The round defines `theta = beta - 1`
at section 9, so the expansion was right and the expectation was wrong. Reading
the definition is the only reason that did not become a finding against correct
arithmetic, and the defect keeps that check honest.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), robustness properties (45), a pre-flight naming
malformed mutations (46), byte-exact restore (47), a failure for every empty
locator (48), a pristine sidecar against a killed drill (50), and premise before
conclusion (51).

Usage:  python code/src52_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src52_farey_entropy.py"
LIMIT = "1201"
TRIALS = "300"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- section 3, the binary bridge ---
    ("D1_the_functional_counts_the_ones_on_the_wrong_side",
     "            ones_right -= 1\n            total += (1 << (i - 1)) * 3 ** ones_right",
     "            total += (1 << (i - 1)) * 3 ** ones_right\n            ones_right -= 1",
     "binary bridge C(d(w)) = B_w fails"),
    ("D2_the_binary_word_places_its_ones_one_step_late",
     "    for a in code:\n        word[partial] = 1\n        partial += a",
     "    for a in code:\n        partial += a\n        word[partial - 1 if partial else 0] = 1",
     "binary bridge C(d(w)) = B_w fails"),
    ("D3_the_affine_numerator_uses_the_wrong_power_of_three",
     "        b += 3 ** (g - 1 - j) * (1 << partial)",
     "        b += 3 ** j * (1 << partial)",
     "binary bridge C(d(w)) = B_w fails"),
    ("D4_the_concatenation_law_uses_the_left_length",
     "        if buv != 3 ** h * b + (1 << p) * bv:",
     "        if buv != 3 ** g * b + (1 << p) * bv:",
     "concatenation identity fails"),
    ("D5_the_normalized_correction_is_divided_twice",
     "    return total / 3",
     "    return total / 9",
     "normalized correction c(w) = B_w/3^g fails"),
    # --- section 5, the capacity count ---
    ("D6_the_prefix_constraint_is_dropped_from_the_enumeration",
     "            if j + 1 < g and nxt * g > (j + 1) * p:\n                break",
     "            if False:\n                break",
     "capacity formula disagrees with enumeration"),
    ("D7_the_closed_form_divides_by_the_wrong_index",
     "            f1, f2 = a // g, b // p",
     "            f1, f2 = a // g, b // g",
     "two closed forms of the capacity disagree"),
    ("D8_the_capacity_window_is_shrunk_back",
     "    for g in range(2, 14):\n        for p in range(g + 1, 23):",
     "    for g in range(2, 5):\n        for p in range(g + 1, 8):",
     "capacity enumeration was too small"),
    ("D9_the_shipped_capacity_examples_are_checked_against_the_wrong_form",
     "        want = math.comb(p, g) // p",
     "        want = math.comb(p, g) // g",
     "shipped capacity example does not recompute"),
    # --- section 6, the extra bit ---
    ("D10_the_B_to_B_modulus_falls_back_to_item_51's",
     "        modulus = 1 << (p + 2)\n        want = (pow(3, -g, modulus) * (3 * (1 << p) - b)) % modulus",
     "        modulus = 1 << (p + 1)\n        want = (pow(3, -g, modulus) * (3 * (1 << p) - b)) % modulus",
     "B-to-B source class modulo 2^(p+2) fails"),
    ("D11_the_B_to_B_class_drops_its_factor_of_three",
     "        want = (pow(3, -g, modulus) * (3 * (1 << p) - b)) % modulus",
     "        want = (pow(3, -g, modulus) * ((1 << p) - b)) % modulus",
     "B-to-B source class modulo 2^(p+2) fails"),
    ("D12_the_B_to_B_class_is_never_checked_in_reverse",
     "        for step in (1, 2, 3):",
     "        for step in ():",
     "not checked in both directions"),
    ("D13_the_destination_separation_is_asked_for_too_much",
     "            if abs(z2 - z) < 4 * 3 ** g or (z2 - z) % (4 * 3 ** g):",
     "            if abs(z2 - z) < 8 * 3 ** g or (z2 - z) % (8 * 3 ** g):",
     "B-to-B separation fails"),
    # --- the continued fractions ---
    ("D14_the_certified_terms_are_altered",
     "CERTIFIED_BETA_CF = (1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1)",
     "CERTIFIED_BETA_CF = (1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 2)",
     "disagrees with the terms RUN-029 certified"),
    # This is the mistake this run nearly published: expecting theta = 1/beta.
    ("D15_theta_is_expected_to_be_one_over_beta_again",
     "    expected_theta = [0] + beta_cf[1:len(theta_cf)] if beta_cf else []",
     "    expected_theta = [0] + beta_cf[:len(theta_cf) - 1] if beta_cf else []",
     "not beta's shifted"),
    # --- the carried-over result section 6 rests on ---
    ("D16_the_carried_over_residue_result_tests_the_wrong_class",
     "            if values[s] % 4 != 3:\n                violations += 1",
     "            if values[s] % 4 != 1:\n                violations += 1",
     "3 mod 4 result, which section 6 assumes, fails"),
    # --- the artifacts ---
    ("D17_the_validation_hashes_use_the_wrong_function",
     '        if hashlib.sha256(raw).hexdigest() == rec["sha256"] and len(raw) == rec["bytes"]:',
     '        if hashlib.sha1(raw).hexdigest() == rec["sha256"] and len(raw) == rec["bytes"]:',
     "validation record does not match its files"),
    ("D18_the_list_shaped_record_is_no_longer_recognised",
     '    elif isinstance(validation.get("files"), list):',
     '    elif isinstance(validation.get("files"), tuple):',
     "unknown shape"),
    # --- robustness ---
    ("D19_the_rho_star_echo_is_dropped",
     '    return {"rows": rows, "off_by_at_least_one_ulp": drifted,\n            "rho_star_agrees": published.get("rho_star") == 4.1164}',
     '    return {"rows": rows, "off_by_at_least_one_ulp": drifted,\n            "rho_star_agrees": True}',
     "__robustness: the ulp comparison stands on its own__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D19_the_rho_star_echo_is_dropped": None,
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle),
             "--limit", LIMIT, "--trials", TRIALS],
            capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
            env={**__import__("os").environ, "PYTHONUTF8": "1"},
        )
    except subprocess.TimeoutExpired:
        return {"passed": False, "failures": ["__the gate did not terminate__"],
                "findings": [], "hung": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "failures": ["__the gate did not produce JSON__"],
                "findings": [], "stderr_tail": (proc.stderr or "")[-400:]}


def _same_verdict(a: dict, b: dict) -> bool:
    def strip(d):
        return {k: v for k, v in d.items() if k not in ("round", "source_item")}
    return json.dumps(strip(a), sort_keys=True) == json.dumps(strip(b), sort_keys=True)


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
        GATE.write_bytes(backup.read_bytes())
        interrupted = True
    snapshot = GATE.read_bytes()
    backup.write_bytes(snapshot)

    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name, "limit": LIMIT, "trials": TRIALS,
        "a_previous_run_was_interrupted_and_the_gate_was_restored": interrupted,
        "baseline": {"passed": base.get("passed"), "failures": base.get("failures"),
                     "findings": base.get("findings")},
        "defects": {}, "controls": {},
    }
    if not base.get("passed"):
        report["ok"] = False
        report["note"] = "the gate is not green before anything was planted"
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 2
    baseline_findings = base.get("findings", [])

    raw_text = snapshot.decode("utf-8")
    for name, old, new, expected in DEFECTS:
        hits = raw_text.count(old)
        if hits != 1:
            report["defects"][name] = {
                "caught": False, "anchor_matches": hits,
                "note": "anchor matches %d times; aimed at nothing" % hits}
            continue
        try:
            GATE.write_bytes(raw_text.replace(old, new).encode("utf-8"))
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(snapshot)

        if name not in FINDING_ROBUSTNESS:
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
                    "caught": False, "malformed": "the mutation changes nothing",
                    "note": "the branch is unreachable on real data, so this was "
                            "never planted; it is not the check missing it"}
                continue

        if name in FINDING_ROBUSTNESS:
            needle = FINDING_ROBUSTNESS[name]
            if needle is None:
                report["defects"][name] = {
                    "caught": bool(res.get("passed")),
                    "kind": "robustness: the gate must stay green",
                    "gate_still_green": bool(res.get("passed")),
                    "failures_seen": res.get("failures", [])[:3]}
            else:
                was = any(needle in f for f in baseline_findings)
                now = any(needle in f for f in res.get("findings", []))
                report["defects"][name] = {
                    "caught": was and now,
                    "kind": "robustness: the finding must SURVIVE",
                    "finding_present_at_baseline": was, "finding_survived": now}
            continue

        failures = res.get("failures", [])
        by_own = any(expected in f for f in failures)
        report["defects"][name] = {
            "caught": by_own, "expected_failure_named": expected,
            "reported": failures[:4],
            "caught_by_something_else_only": bool(failures) and not by_own,
            "hung": bool(res.get("hung"))}

    for name, suffix in CONTROLS:
        try:
            GATE.write_bytes(snapshot + suffix)
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(snapshot)
        report["controls"][name] = {"undisturbed": bool(res.get("passed"))}
    report["controls"]["N2_the_gate_is_restored_byte_exactly"] = {
        "undisturbed": GATE.read_bytes() == snapshot}

    caught = sum(1 for v in report["defects"].values() if v.get("caught"))
    report["counts"] = {
        "planted": len(DEFECTS), "caught_by_their_own_check": caught,
        "missed": len(DEFECTS) - caught,
        "robustness_properties": len(FINDING_ROBUSTNESS),
        "malformed": sum(1 for v in report["defects"].values() if v.get("malformed")),
        "hung": sum(1 for v in report["defects"].values() if v.get("hung")),
        "controls": len(report["controls"]),
        "controls_undisturbed": sum(1 for c in report["controls"].values()
                                    if c["undisturbed"])}
    report["ok"] = (caught == len(DEFECTS)
                    and all(c["undisturbed"] for c in report["controls"].values()))
    if GATE.read_bytes() == snapshot:
        backup.unlink()
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
