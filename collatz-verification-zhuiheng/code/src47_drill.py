"""Can the item-47 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src47_survival_closure.py` reports that the round's exponent chain is exactly
rational and correct to every published digit, that the continued fraction of
`log_2 3` recomputed by integer comparisons alone agrees with the artifact, that
both second-order expansion coefficients are right, and that the shipped JSON is
what the shipped script produces.

Habits carried in, every one paid for by an earlier item:

  - a subprocess timeout (item 42: a defect hung the drill and left a live
    mutation on disk);
  - defects aimed at **subjects, not comparisons** (item 43);
  - defects must break the **result, not the interpreter** (items 44, 45);
  - a failed defect may be a **robustness property** rather than a miss (45);
  - a **pre-flight** on every mutation, so a malformed defect is named rather
    than scored as a check that missed (item 46).

## What is new here: a defect that changes no number at all

D6 swaps the integer-certified continued fraction for the high-precision one.
Every partial quotient it produces is identical, so every field in the report
agrees and the two-methods-agree check confirms a comparison of a thing with
itself. Nothing in the previous design could see it. The gate now counts the
integer comparisons it actually performed, which is the only field that moves --
so the independence claim became measurable specifically because this drill had
to be able to break it.

Usage:  python code/src47_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src47_survival_closure.py"
CF_BUDGET = "4"                 # 14 certified terms in about 7 seconds
GATE_TIMEOUT_SECONDS = 300

DEFECTS = [
    # --- the exponent chain, which is exactly rational ---
    # D1 first read rho_star through a float. That is a real defect, but it
    # breaks `mu_star == rho_star + 1` first, so the identity check fired and the
    # digit check was never reached. Re-aimed so exactly one check can see it.
    ("D1_a_published_figure_is_checked_against_the_wrong_exact_value",
     '        "theta_star": (data["theta_star"], theta),',
     '        "theta_star": (data["theta_star"], sigma),',
     "published exponent digits are wrong"),
    ("D20_rho_star_is_no_longer_conservative_against_the_cited_exponent",
     'CITED_EXPONENT = "4.11633052"',
     'CITED_EXPONENT = "4.2"',
     "not conservative against the exponent the round cites"),
    ("D2_sigma_is_built_from_the_wrong_reciprocal",
     "    sigma = 1 / (1 + theta)\n    congestion = 1 - sigma",
     "    sigma = 1 / (1 - theta)\n    congestion = 1 - sigma",
     "does not satisfy its own identities"),
    # --- the transcendental constants and the relations between them ---
    ("D3_kappa_rot_uses_the_wrong_root",
     '            "kappa_rot": (kappa, "1/(12 sqrt 2)"),',
     '            "kappa_rot": (kappa, "1/(12 sqrt 3)"),',
     "__robustness: the closed form itself is unchanged__"),
    # D4 was labelled "the constants contradict each other", but this entry
    # feeds the DIGIT comparison, not the relations between the constants. The
    # check that owns it is the one that fired. Two defects now, one per check.
    ("D4_the_leading_cf_constant_gets_the_wrong_power",
     '            "cf_leading_constant": (6 * ln2 ** 2, "6 (ln 2)^2 = ln2/eta"),',
     '            "cf_leading_constant": (6 * ln2 ** 3, "6 (ln 2)^2 = ln2/eta"),',
     "disagrees with its closed form far beyond rounding"),
    ("D19_a_relation_between_the_constants_is_stated_wrongly",
     '            "cf_second/cf_leading == kappa/eta":\n'
     '                abs((3 * ln2 ** 3 / mp.sqrt(2)) / (6 * ln2 ** 2) - kappa / eta),',
     '            "cf_second/cf_leading == kappa/eta":\n'
     '                abs((3 * ln2 ** 3 / mp.sqrt(2)) / (6 * ln2 ** 2) - eta / kappa),',
     "the constants contradict each other"),
    # --- the integer-certified continued fraction ---
    ("D5_the_integer_comparison_has_a_branch_backwards",
     "    if a2 <= 0 and a3 <= 0:\n        return 0 if (a2 == 0 and a3 == 0) else -1",
     "    if a2 <= 0 and a3 <= 0:\n        return 0 if (a2 == 0 and a3 == 0) else 1",
     "integer comparison primitive is wrong"),
    # The one that motivated counting comparisons at all: identical output.
    ("D6_the_certified_route_is_silently_the_high_precision_one",
     "    terms, started, stopped = [], time.time(), None\n    for _ in range(max_terms):",
     "    terms, started, stopped = [], time.time(), None\n"
     "    terms.extend(mpmath_continued_fraction(max_terms))\n"
     "    for _ in range(0):",
     "did not perform integer comparisons"),
    # D7 first passed `want=2`, which selects the same last two convergents --
    # the filter `>= want` then `[-2:]` makes the argument almost inert. The
    # pre-flight named it "changes nothing" instead of blaming the check.
    # D7 took two tries. `want=2` selects the same last two convergents, and so
    # does slicing the filtered list from the front when that list has exactly
    # two entries -- the `want` argument cannot widen this bracket at all. Both
    # attempts were named "changes nothing" by the pre-flight rather than scored
    # against the check, which is the entire point of having one.
    ("D7_the_bracket_is_taken_from_far_too_early_a_convergent",
     "    pick = [c for c in conv if c[0] >= want][-2:] or conv[-2:]",
     "    pick = conv[:2]",
     "decided too few rows"),
    # --- the upper-convergent filter, in both directions ---
    ("D8_the_parity_rule_is_inverted",
     '        if (side == "above") != (i % 2 == 1):',
     '        if (side == "above") == (i % 2 == 1):',
     "filter is wrong in one direction"),
    ("D9_a_shipped_row_goes_missing_before_the_filter_sees_it",
     '    kept = {row["index"] for row in data["upper_convergent_diagnostics"]}\n    conv = convergents_from_terms(terms)',
     '    kept = {row["index"] for row in data["upper_convergent_diagnostics"]} - {5}\n    conv = convergents_from_terms(terms)',
     "filter is wrong in one direction"),
    # --- the continued-fraction tax ---
    ("D10_the_tax_lower_bound_is_raised_to_meet_the_upper_one",
     "        lower, upper = Fraction(1, q + qn), Fraction(1, qn)",
     "        lower, upper = Fraction(1, qn), Fraction(1, qn)",
     "continued-fraction tax inequality is violated"),
    # --- the two second-order expansion coefficients ---
    ("D11_the_section_9_residual_is_scaled_by_the_wrong_power",
     '            return (exact - claimed) * q ** mp.mpf("1.5")',
     '            return (exact - claimed) * q ** mp.mpf("1.0")',
     "section-9 residual does not discriminate its coefficient asymptotically"),
    ("D12_the_section_16_coefficient_uses_the_wrong_exponent",
     '        coeff16 = kappa / eta ** mp.mpf("1.5")',
     '        coeff16 = kappa / eta ** mp.mpf("2.0")',
     "section-16 residual does not discriminate"),
    # D13 first flipped the sign of the root used only by the `root_ok` check --
    # and BOTH roots solve the quadratic, so nothing moved and the pre-flight
    # named it. Re-aimed at the root the expansion actually uses.
    ("D13_the_expansion_uses_the_other_root",
     "            A = mp.mpf(A)\n"
     "            x = (kappa + mp.sqrt(kappa ** 2 + 4 * eta * A)) / (2 * eta)\n"
     "            return (x ** 2 - A / eta - second * mp.sqrt(A)) / mp.sqrt(A)",
     "            A = mp.mpf(A)\n"
     "            x = (kappa - mp.sqrt(kappa ** 2 + 4 * eta * A)) / (2 * eta)\n"
     "            return (x ** 2 - A / eta - second * mp.sqrt(A)) / mp.sqrt(A)",
     "section-16 residual does not discriminate"),
    ("D18_the_root_check_is_asked_the_wrong_equation",
     "        root_ok = abs(eta * x ** 2 - kappa * x - A) < mp.mpf(10) ** (-WORKING_DPS + 30)",
     "        root_ok = abs(eta * x ** 2 - kappa * x + A) < mp.mpf(10) ** (-WORKING_DPS + 30)",
     "quadratic root is wrong"),
    # --- the renewal geometry ---
    ("D14_the_colouring_never_reuses_a_colour",
     "            col = next((c for c in range(used + 1) if c not in taken), used)",
     "            col = used",
     "renewal geometry does not hold as stated"),
    # D15 first shrank the intervals to width 1 at random starts -- which still
    # collides often enough to keep three distinct overlap counts, so the guard
    # was right not to fire. Made disjoint by construction instead.
    ("D15_the_colouring_sample_can_no_longer_overlap",
     "        for _ in range(n):\n"
     "            s = rng.randint(0, 200)\n"
     "            ivs.append((s, s + rng.randint(1, 60)))",
     "        for _k in range(n):\n"
     "            s = _k * 500\n"
     "            ivs.append((s, s + 1))",
     "colouring sample never exercised a real overlap"),
    # --- the cancellation model behind the over-publication finding ---
    ("D16_the_cancellation_model_forgets_the_next_denominator",
     "            predicted = shown - float(mp.log(beta * q * qn, 10)) if q_i * qn_i > 1 else shown",
     "            predicted = shown - float(mp.log(beta * q, 10)) if q_i * qn_i > 1 else shown",
     "cancellation model does not predict"),
    # --- the elementary inequalities ---
    ("D17_the_superadditivity_hypothesis_drops_g_being_an_integer",
     "            g = rng.randint(1, 40)",
     "            g = mp.mpf(rng.random())",
     "elementary inequality the derivation uses fails"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

#: Defects whose point is that the gate must STAY GREEN, because another check
#: already covers the property. `None` means "the gate must still pass".
FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D3_kappa_rot_uses_the_wrong_root": None,
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle),
             "--cf-budget", CF_BUDGET],
            capture_output=True, text=True, cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {"passed": False, "failures": ["__the gate did not terminate__"],
                "findings": [], "hung": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "failures": ["__the gate did not produce JSON__"],
                "findings": [], "stderr_tail": proc.stderr[-400:]}


def _same_verdict(a: dict, b: dict) -> bool:
    """Did the mutation move ANY number the gate reports?

    Compared on the whole report minus the fields that describe the run rather
    than its result -- the certification is wall-clock bounded, so its timing and
    the term count it happens to reach vary between runs and are not evidence
    that a mutation did anything.
    """
    def strip(d):
        out = {k: v for k, v in d.items() if k not in ("round", "source_item")}
        cf = dict(out.get("continued_fraction", {}))
        for k in ("certification_seconds",):
            cf.pop(k, None)
        if cf:
            out["continued_fraction"] = cf
        return out
    return json.dumps(strip(a), sort_keys=True) == json.dumps(strip(b), sort_keys=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=pathlib.Path, required=True)
    args = ap.parse_args()

    snapshot = GATE.read_bytes()
    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name,
        "cf_budget_seconds": float(CF_BUDGET),
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

    # Bytes, not text. `read_text` then `write_text` translates LF to CRLF on
    # Windows, so the round trip silently rewrote every line of the file the
    # drill had just promised to restore -- caught by the byte-exact control,
    # which is the entire reason that control exists.
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

        # PRE-FLIGHT, carried from item 46. A planted defect has to be a defect
        # before a miss says anything about the check that was aimed at it.
        if name not in FINDING_ROBUSTNESS:
            if res.get("hung"):
                report["defects"][name] = {
                    "caught": False, "malformed": "the gate did not terminate",
                    "note": "a defect must break the result, not the interpreter"}
                continue
            if "__the gate did not produce JSON__" in res.get("failures", []):
                report["defects"][name] = {
                    "caught": False, "malformed": "the gate raised",
                    "note": "a defect must break the result, not the interpreter",
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
                    "kind": "robustness: the gate must stay green because another "
                            "check covers this",
                    "gate_still_green": bool(res.get("passed")),
                    "failures_seen": res.get("failures", [])[:3],
                }
            else:
                was = any(needle in f for f in baseline_findings)
                now = any(needle in f for f in res.get("findings", []))
                report["defects"][name] = {
                    "caught": was and now,
                    "kind": "robustness: the finding must SURVIVE",
                    "finding_present_at_baseline": was,
                    "finding_survived": now,
                }
            continue

        failures = res.get("failures", [])
        by_own = any(expected in f for f in failures)
        report["defects"][name] = {
            "caught": by_own, "expected_failure_named": expected,
            "reported": failures[:4],
            "caught_by_something_else_only": bool(failures) and not by_own,
            "hung": bool(res.get("hung")),
        }

    for name, suffix in CONTROLS:
        raw = GATE.read_bytes()
        try:
            GATE.write_bytes(raw + suffix)
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(raw)
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
                                    if c["undisturbed"]),
    }
    report["ok"] = (caught == len(DEFECTS)
                    and all(c["undisturbed"] for c in report["controls"].values()))
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
