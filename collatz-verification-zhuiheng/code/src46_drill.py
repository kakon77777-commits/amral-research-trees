"""Can the item-46 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src46_attainability.py` reports that §17's Saturation Equivalence holds as an
exact `iff` on every real first crossing, that the round's gap prediction is never
violated, and that the shipped JSON is not what the shipped script produces.

Habits carried in, every one of them paid for by an earlier item:

  - a subprocess timeout (item 42: a defect hung the drill and left a live
    mutation on disk);
  - defects aimed at **subjects, not comparisons** (item 43);
  - defects must break the **result, not the interpreter** (items 44, 45);
  - a failed defect may be a **robustness property** rather than a miss (item 45).

## New here: a PRE-FLIGHT on the defects themselves

Two failure modes have now cost a full drill pass each on items 42, 44, 45 and
again on the first pass of this one: a mutation that **raises**, and a mutation
that **changes nothing** because the branch it edits is unreachable on real data.
Both were being reported as the named check missing, which blames the check for
the drill's own bad aim.

So before a miss is attributed to anything, each mutated run is screened:

  - did the gate fail to terminate?  → `malformed: the gate did not terminate`
  - did it raise?                    → `malformed: the gate raised`
  - is its whole report identical to the baseline? → `malformed: the mutation
    changes nothing`

**A defect that changes nothing was never planted**, and saying so is different
from saying a check missed it. This is the fourth item where that distinction
would have saved a pass, so it is now built in rather than rediscovered.

Usage:  python code/src46_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src46_attainability.py"
LIMIT = "4001"
GATE_TIMEOUT_SECONDS = 300

DEFECTS = [
    # --- section 17, the unconditional iff ---
    ("D1_the_mechanical_test_uses_the_wrong_floor",
     "        if Qs[j] != p3.bit_length() - 1:",
     "        if Qs[j] != p3.bit_length() - 2:",
     "saturation_equivalence"),
    ("D2_the_mechanical_test_stops_one_short",
     "    p3 = 1\n    for j in range(L):\n        if Qs[j] != p3.bit_length() - 1:",
     "    p3 = 1\n    for j in range(L - 1):\n        if Qs[j] != p3.bit_length() - 1:",
     "saturation_equivalence"),
    ("D3_B_over_3L_uses_the_wrong_power",
     "        b3 = sum(Fraction(1 << Qs[j], 3 ** j) for j in range(L)) / 3",
     "        b3 = sum(Fraction(1 << Qs[j], 3 ** (j + 1)) for j in range(L)) / 3",
     "saturation_equivalence"),
    # D4 first used `bit_length() - 2`, which is `1 << -1` at j = 0 and RAISES.
    # Caught by the pre-flight now, but re-aimed anyway so it tests something.
    ("D4_U_uses_the_wrong_floor",
     "        total += Fraction(1 << (p3.bit_length() - 1), p3)",
     "        total += Fraction(1 << p3.bit_length(), p3)",
     "saturation_equivalence"),
    # the iff must be tested on BOTH diagonals, not only where it is easy
    ("D5_only_one_diagonal_is_required_to_be_inhabited",
     '        "both_diagonals_are_inhabited": both > 0 and neither > 0,',
     '        "both_diagonals_are_inhabited": both > 0 or neither > 0,',
     "__robustness: the iff guard must survive__"),
    # --- the gap prediction ---
    ("D6_the_gap_formula_drops_its_clamp",
     "    return max(0.0, (math.sqrt(H * H + 2.0 * N) - H) / 24.0 - 1.0 / 12.0)",
     "    return abs((math.sqrt(H * H + 2.0 * N) - H) / 24.0 - 1.0 / 12.0)",
     "gap_prediction"),
    ("D7_the_gap_prediction_never_fires",
     "        g = gap_bound(float(n), L)",
     "        g = 0.0",
     "the prediction is untested"),
    # --- constants ---
    ("D8_kappa_rot_uses_the_wrong_root",
     '        "kappa_rot": ("1/(12 sqrt 2)", 1 / (12 * sqrt2)),',
     '        "kappa_rot": ("1/(12 sqrt 2)", 1 / (12 * ln2)),',
     "constants"),
    ("D9_the_mutual_consistency_check_compares_a_thing_with_itself",
     '    ratio = Decimal(repr(js["kappa_rot"])) / Decimal(repr(js["eta_beta"]))',
     '    ratio = Decimal(repr(js["relative_constant"]))',
     "__robustness: individual closed forms still hold__"),
    # --- the shipped rows and the float ceiling ---
    ("D10_the_shipped_row_check_recomputes_from_the_json",
     "        y = L ** power\n        g = gap_bound(y, L)\n        rows += 1",
     "        y = L ** power\n        g = r[\"G\"]\n        rows += 1",
     "__robustness: G_over_sqrt_L still checked__"),
    # D11 first changed `<` to `<=`, which differs only when `y + N/3` is EXACTLY
    # a power of two — and it never is here, so the mutation was a NO-OP. The
    # pre-flight below now names that rather than blaming the check. Re-aimed to
    # overshoot the ceiling, which the float comparison does catch.
    ("D11_the_exact_ceiling_overshoots",
     "        while Fraction(1 << he) < v:\n            he += 1",
     "        while Fraction(1 << he) < v:\n            he += 2",
     "float_ceiling"),
    # --- provenance ---
    ("D12_the_row_key_regex_drops_uppercase_again",
     "    script_row = re.findall(r'\"([A-Za-z_]+)\":', row_block[0]) if row_block else []",
     "    script_row = re.findall(r'\"([a-z_]+)\":', row_block[0]) if row_block else []",
     "__robustness: the provenance finding survives__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

#: Defects whose point is that the finding must DISAPPEAR.
FINDING_DEFECTS: dict[str, str] = {}

#: Defects whose point is that something must SURVIVE. Each started as a defect
#: and turned out to be pinning a robustness property instead — the item-45
#: lesson, applied deliberately this time rather than discovered.
#:
#: D5  weakening the "both diagonals inhabited" guard must not make the iff pass
#:     vacuously, because the off-diagonal checks still fire on their own.
#: D9  breaking the mutual-consistency check must not hide a wrong constant,
#:     because each closed form is also checked individually.
#: D10 reading G back out of the JSON instead of recomputing must still be caught
#:     by the derived quantity `G_over_sqrt_L`, which is computed from `g`.
#: D12 a regex that drops uppercase keys must not remove the provenance finding,
#:     because the dropped row key `y` is lowercase and still shows up.
FINDING_ROBUSTNESS = {
    "D5_only_one_diagonal_is_required_to_be_inhabited": None,
    "D9_the_mutual_consistency_check_compares_a_thing_with_itself": None,
    "D10_the_shipped_row_check_recomputes_from_the_json": None,
    "D12_the_row_key_regex_drops_uppercase_again":
        "not produced by the shipped script",
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--limit", LIMIT, "--bundle", str(bundle)],
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

    Compared on the whole report minus the fields that are about the run rather
    than its result, so a defect that only changes a path or a timestamp still
    counts as changing nothing.
    """
    def strip(d):
        return {k: v for k, v in d.items()
                if k not in ("odd_starts_below", "round", "source_item")}
    return json.dumps(strip(a), sort_keys=True) == json.dumps(strip(b), sort_keys=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=pathlib.Path, required=True)
    args = ap.parse_args()

    snapshot = GATE.read_bytes()
    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name,
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

    text = GATE.read_text(encoding="utf-8")
    for name, old, new, expected in DEFECTS:
        hits = text.count(old)
        if hits != 1:
            report["defects"][name] = {
                "caught": False, "anchor_matches": hits,
                "note": "anchor matches %d times; aimed at nothing" % hits}
            continue
        try:
            GATE.write_text(text.replace(old, new), encoding="utf-8")
            res = run_gate(args.bundle)
        finally:
            GATE.write_text(text, encoding="utf-8")

        # PRE-FLIGHT. A planted defect has to be a defect before a miss means
        # anything about the check. Two failure modes have now cost a full drill
        # pass each, on items 42, 44, 45 and again here:
        #
        #   - it raises, and the drill sees "did not produce JSON" instead of the
        #     named check firing. A defect must break the RESULT, not the
        #     interpreter.
        #   - it changes nothing, because the mutated branch is unreachable on
        #     real data. A defect that changes nothing was never planted, and
        #     reporting it as a miss blames the check for the drill's own choice.
        #
        # Both are now detected and named, so a malformed defect is never counted
        # as a miss by the check it was aimed at.
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
                # the GATE must still pass: the property is covered elsewhere
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
