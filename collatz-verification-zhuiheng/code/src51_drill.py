"""Can the item-51 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src51_annular_residue.py` reports that section 4's exact-code arithmetic holds
in both directions, that section 6's `y = 3 (mod 4)` holds on every real source
with `L >= 2`, that the renewal identity and both determinants are exact in
beta-linear integers, and that section 6's depth cap is vacuous on real orbits
because none satisfies its corridor premise.

Two of its checks were wrong on the first pass, and both were the same mistake in
opposite directions: **imposing a conclusion without its premise** (the depth cap,
which flagged 10214 of 10214 — a rate that is a statement about the check), and
**reading a record in a shape it does not have** (item 51's validation record is a
list where item 50's was a dict, so the reader saw zero files and would have
called that clean). D13 and D14 replant exactly those.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), a failed defect may be a robustness property (45), a
pre-flight that names malformed mutations (46), byte-exact restore (47), a
failure for every locator that comes back empty (48), and a pristine sidecar so a
killed drill cannot leave its defect behind (50).

Usage:  python code/src51_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src51_annular_residue.py"
LIMIT = "1501"
CODES = "150"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- section 4, the exact code arithmetic ---
    ("D1_B_w_uses_the_wrong_power_of_three",
     "        b += 3 ** (k - 1 - j) * (1 << partial)",
     "        b += 3 ** j * (1 << partial)",
     "affine identity 2^Q z = 3^k x + B_w fails"),
    ("D2_B_w_accumulates_the_partial_sum_too_early",
     "        b += 3 ** (k - 1 - j) * (1 << partial)\n        partial += code[j]",
     "        partial += code[j]\n        b += 3 ** (k - 1 - j) * (1 << partial)",
     "affine identity 2^Q z = 3^k x + B_w fails"),
    ("D3_the_source_class_drops_the_extra_factor_of_two",
     "        modulus = 1 << (q + 1)\n        want = (pow(3, -kk, modulus) * ((1 << q) - b)) % modulus",
     "        modulus = 1 << q\n        want = (pow(3, -kk, modulus) * ((1 << q) - b)) % modulus",
     "does not realize the code"),
    ("D4_the_endpoint_class_inverts_the_wrong_way",
     "        if z % mod3 != (pow(2, -q, mod3) * b) % mod3:",
     "        if z % mod3 != (pow(2, q, mod3) * b) % mod3:",
     "residue class is wrong"),
    ("D5_the_class_is_never_checked_in_reverse",
     "        for step in range(1, 4):",
     "        for step in range(1, 1):",
     "not exercised in both directions"),
    # --- bi-exact separation ---
    ("D6_the_endpoint_separation_drops_its_factor_of_two",
     "        if (z2 - z) != 2 * 3 ** kk * m:",
     "        if (z2 - z) != 3 ** kk * m:",
     "bi-exact separation fails"),
    ("D7_no_repeated_code_pair_is_ever_formed",
     "        if code2 != code:\n            continue",
     "        if True:\n            continue",
     "too few repeated-code pairs"),
    # --- the shipped examples ---
    ("D8_only_one_shipped_example_is_checked",
     '    for ex in report.get("sample_bi_exact_examples", []):',
     '    for ex in report.get("sample_bi_exact_examples", [])[:1]:',
     "too few shipped examples"),
    ("D9_the_code_is_replayed_for_the_wrong_number_of_steps",
     "        c1, z1 = run_code(ex[\"source_1\"], k)",
     "        c1, z1 = run_code(ex[\"source_1\"], k + 1)",
     "a shipped example does not recompute"),
    # --- section 6 ---
    ("D10_the_residue_corollary_tests_the_wrong_class",
     "            if values[s] % 4 != 3:",
     "            if values[s] % 4 != 1:",
     "a source with L >= 2 is not 3 mod 4"),
    ("D11_the_forced_first_exponent_is_read_as_two",
     "            if word[s] != 1:",
     "            if word[s] != 2:",
     "a source with L >= 2 is not 3 mod 4"),
    # --- the determinants ---
    ("D12_the_plateau_determinant_pairs_its_wings_the_wrong_way",
     "                combo = lin((g_i * D_j[0], g_i * D_j[1]), (L_j * A[0], L_j * A[1]))",
     "                combo = lin((g_i * A[0], g_i * A[1]), (L_j * D_j[0], L_j * D_j[1]))",
     "determinant is not a positive integer"),
    # --- the corridor premise, which the first pass omitted ---
    ("D13_the_corridor_premise_admits_every_chain",
     "            if ys[-1] - ys[0] < u_beta(L):",
     "            if ys[-1] - ys[0] < u_beta(L) * 10 ** 9:",
     "chain cap or 4-gap fails on its own premise"),
    # --- the validation record, whose shape changed between bundles ---
    ("D14_the_list_shaped_validation_record_is_no_longer_recognised",
     '    elif isinstance(validation.get("files"), list):',
     '    elif isinstance(validation.get("files"), dict):',
     "shape this run does not know"),
    ("D15_the_validation_hashes_are_computed_with_the_wrong_function",
     '        if hashlib.sha256(raw).hexdigest() == rec["sha256"] and len(raw) == rec["bytes"]:',
     '        if hashlib.sha1(raw).hexdigest() == rec["sha256"] and len(raw) == rec["bytes"]:',
     "validation record does not match its files"),
    # --- the checker's own claims ---
    ("D16_every_claim_of_the_checker_is_marked_unconfirmed",
     '    checked = {c: mapping[c] for c in stated if c in mapping}',
     '    checked = {c: False for c in stated if c in mapping}',
     "contradicted here"),
    # --- non-vacuity of laminarity ---
    ("D17_laminarity_is_never_sampled",
     "        if start <= 999:                     # laminarity is quadratic; sample it",
     "        if start <= 0:                       # laminarity is quadratic; sample it",
     "not exercised in both branches"),
    # --- robustness ---
    # D18 first renamed a key in the comparison table, which raises rather
    # than changing a result -- a malformed robustness defect. Changing a
    # VALUE keeps the code valid and removes one cross-bundle difference,
    # which is the thing the property is actually about.
    ("D18_item_50_is_recorded_as_agreeing_with_item_51",
     '    "sigma_star": 0.8365051337388005,',
     '    "sigma_star": 0.8365051337388006,',
     "__robustness: the exact-rational check still stands alone__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D18_item_50_is_recorded_as_agreeing_with_item_51": None,
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle),
             "--limit", LIMIT, "--codes", CODES],
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

    # a killed drill cannot run its `finally` (item 50)
    backup = GATE.with_suffix(GATE.suffix + ".pristine")
    interrupted = False
    if backup.exists():
        GATE.write_bytes(backup.read_bytes())
        interrupted = True
    snapshot = GATE.read_bytes()
    backup.write_bytes(snapshot)

    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name, "limit": LIMIT, "codes": CODES,
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
        backup.unlink()
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
