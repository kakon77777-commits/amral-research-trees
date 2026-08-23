"""Can the item-50 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src50_congestion_rigidity.py` reports that Theorem 3.1 and laminarity hold on
real accelerated orbits with zero violations, that the annulus identity is
exactly `(0, 0)` in beta-linear integers over 229 nested edges, that the shipped
checker's own smoke-test figures reproduce field for field, and that the bundle's
declared input state closes against this tree's RUN-030 and RUN-031 records.

Two of its checks were wrong on the first pass and both were caught by comparing
against the artifact rather than by inspection: a comparison that silently
answered one direction turned Theorem 3.1 into 2757 violations, and orbit-wide
edge counts were published under the shipped report's `chain_*` field names,
which count something else. Defects D1 and D8 replant exactly those.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), a failed defect may be a robustness property (45), a
pre-flight that names malformed mutations (46), byte-exact restore that restores
bytes (47), and a failure for every locator that comes back empty (48).

Usage:  python code/src50_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src50_congestion_rigidity.py"
STARTS = "27,703,6171"          # the fourth orbit costs time and adds no branch
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the exact comparison everything rests on ---
    ("D1_the_slack_comparison_answers_only_one_direction",
     "    d = u - s\n"
     "    dk = K[u] - K[s]\n"
     "    return Fraction(3) ** d < Fraction(2) ** dk",
     "    d = u - s\n"
     "    dk = K[u] - K[s]\n"
     "    if dk < 0:\n"
     "        return False\n"
     "    return Fraction(3) ** d < Fraction(2) ** dk",
     "contradicting Theorem 3.1"),
    # D2 was labelled with Theorem 3.1, but reversing the comparison reverses it
    # for the prefix check too, so that check stays self-consistently green. What
    # catches it is the comparison against the shipped report -- which is the
    # point of having an external reference at all.
    ("D2_the_slack_comparison_is_reversed",
     "    return Fraction(3) ** d < Fraction(2) ** dk",
     "    return Fraction(3) ** d > Fraction(2) ** dk",
     "orbit figures do not reproduce"),
    ("D3_the_monotone_stack_pops_on_the_wrong_condition",
     "        while stack and slack_is_smaller(K, u, stack[-1]):",
     "        while stack and slack_is_smaller(K, stack[-1], u):",
     "disagree on the next-smaller slack"),
    # --- laminarity ---
    ("D4_the_intervals_are_stretched_past_their_crossing",
     "        intervals = [(s, e) for s, e in enumerate(e_scan) if e is not None]",
     "        intervals = [(s, e + 1) for s, e in enumerate(e_scan) if e is not None]",
     "properly cross, contradicting Theorem 4.1"),
    ("D5_nested_and_disjoint_are_never_distinguished",
     "                if b <= c or d <= a:\n"
     "                    disjoint += 1",
     "                if True:\n"
     "                    disjoint += 1",
     "laminarity was not exercised"),
    # --- the annulus identity, in beta-linear integers ---
    ("D6_the_annulus_residual_adds_where_it_should_subtract",
     "            residual = lin_sub(lin_add(A, D_i), lin_add(D_j, E))",
     "            residual = lin_add(lin_add(A, D_i), lin_add(D_j, E))",
     "annulus identity does not hold exactly"),
    ("D7_the_slack_form_has_the_wrong_sign_on_K",
     "def delta(K: list[int], m: int) -> tuple[int, int]:\n"
     '    """delta_m = beta*m - K_m."""\n'
     "    return (m, -K[m])",
     "def delta(K: list[int], m: int) -> tuple[int, int]:\n"
     '    """delta_m = beta*m - K_m."""\n'
     "    return (m, K[m])",
     "annulus identity does not hold exactly"),
    ("D8_the_determinant_combines_its_wings_with_the_wrong_sign",
     "                det = r_i * g_i - p_i * h_i",
     "                det = r_i * g_i + p_i * h_i",
     "determinant identity or its lower bound fails"),
    # --- the comparison against the shipped report ---
    ("D9_chain_edges_are_classified_by_origin_instead_of_endpoint",
     "            if b1 == b2:",
     "            if a1 == a2:",
     "orbit figures do not reproduce"),
    # D10 first changed the `--starts` default, which the drill always overrides
    # on the command line, so nothing moved. Aimed at the comparison instead.
    ("D10_only_one_shipped_smoke_test_is_compared",
     '    theirs = {r["start"]: r for r in shipped["accelerated_collatz_smoke_tests"]}',
     '    theirs = {r["start"]: r for r in shipped["accelerated_collatz_smoke_tests"][:1]}',
     "too few shipped smoke tests"),
    # D11 used to aim at an incremental power of three. That loop is gone -- it
    # was quadratic and timed the drill out -- so the defect now aims at what
    # replaced it: the bracket that makes the fast route exact.
    ("D11_the_floor_bracket_is_taken_from_the_first_convergents",
     "    (p1, q1), (p2, q2) = conv[-2], conv[-1]",
     "    (p1, q1), (p2, q2) = conv[0], conv[1]",
     "the floor bracket could not decide"),
    ("D18_the_sweep_processes_starts_before_ends",
     "        events = sorted([(a, 1) for a, _ in intervals] + [(b, -1) for _, b in intervals],\n"
     "                        key=lambda ev: (ev[0], ev[1]))",
     "        events = sorted([(a, 1) for a, _ in intervals] + [(b, -1) for _, b in intervals],\n"
     "                        key=lambda ev: (ev[0], -ev[1]))",
     "mechanical figures do not reproduce"),
    # --- the exponents ---
    ("D12_an_exponent_is_derived_from_the_wrong_expression",
     '        "chain_outer_log_denominator_power": 1 / rho,',
     '        "chain_outer_log_denominator_power": 1 / (rho + 1),',
     "wrong beyond float precision"),
    # --- the bundle's own records ---
    ("D13_the_validation_record_is_verified_with_the_wrong_hash",
     "        if hashlib.sha256(raw).hexdigest() == rec[\"sha256\"] and len(raw) == rec[\"bytes\"]:",
     "        if hashlib.sha1(raw).hexdigest() == rec[\"sha256\"] and len(raw) == rec[\"bytes\"]:",
     "validation record does not match its files"),
    ("D14_the_upstream_chain_is_closed_against_the_wrong_record",
     '    "handoff_zip": "799fad5e0614c598157b4748e0b1033585f11194d80824051ac12e3a5730acdd",',
     '    "handoff_zip": "0000000000000000000000000000000000000000000000000000000000000000",',
     "declared input state disagrees"),
    ("D15_the_markdown_dollar_count_is_read_from_the_record",
     '            "dollar_count_agrees": text.count("$") == rec["dollar_count"],',
     '            "dollar_count_agrees": rec["dollar_count"] == rec["dollar_count"],',
     "__robustness: the byte and delimiter checks still compare__"),
    # --- the float-margin measurement ---
    # D16 needs a guard that scales: 199 comparisons for 199 intervals passed a
    # flat threshold of 100 while looking at one step of each interval instead of
    # all of them. The guard now asks for several comparisons PER interval.
    ("D16_the_float_margin_looks_at_one_step_of_each_interval",
     "                for u in range(s + 1, end + 1):",
     "                for u in range(s + 1, min(s + 2, end + 1)):",
     "float-margin measurement decided almost nothing"),
    # --- the round's own refusals ---
    ("D17_a_scope_refusal_pattern_can_no_longer_match",
     '            bool(re.search(r"\\*\\*not\\*\\* a proof of Collatz, Terras CST, CASP", paper)),',
     '            bool(re.search(r"\\*\\*not\\*\\* a proof of Collatz, Terras CST, CASPX", paper)),',
     "scope refusals are missing"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D15_the_markdown_dollar_count_is_read_from_the_record": None,
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle), "--starts", STARTS],
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

    # A drill that is killed from outside cannot run its `finally`, and what is
    # left on disk is a planted defect wearing the gate's name. That happened
    # here: a ten-minute tool timeout killed this drill mid-run and D1's mutation
    # stayed live until the next run reported 2757 violations of a theorem that
    # holds. The subprocess timeout each drill has carried since item 42 protects
    # against a hanging GATE, not against the drill itself being killed.
    #
    # So the original is written to a sidecar before anything is planted, and a
    # sidecar found at startup means the last run did not finish: restore from it
    # and say so, rather than drilling a file that is already mutated.
    backup = GATE.with_suffix(GATE.suffix + ".pristine")
    interrupted = False
    if backup.exists():
        GATE.write_bytes(backup.read_bytes())
        interrupted = True
    snapshot = GATE.read_bytes()
    backup.write_bytes(snapshot)

    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name, "starts": STARTS,
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
        backup.unlink()                                  # clean exit: no sidecar
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
