"""Can the item-48 handoff-fidelity check actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src48_handoff_fidelity.py` reports that every number in the handoff traces to a
round document, that no reshipped document has drifted across 27 bundles, that
the handoff's status disclaimers are intact — and that its occupancy lemma is the
round's lemma times sqrt 2, contradicting the constant the handoff itself prints
three lines later.

A fidelity check has a failure mode a mathematical check does not: **its locators
can stop finding anything, and a locator that finds nothing reports the subject as
clean.** Two of this file's checks did exactly that on the first pass — one search
normalised whitespace on the haystack but not the needle, and one treated an
arXiv identifier as a constant. So several defects here break the *locator*
rather than the comparison, and the gate grew a failure for every locator that
comes back empty.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), a failed defect may be a robustness property (45), a
pre-flight that names malformed mutations (46), and byte-exact restore that
actually restores bytes (47).

Usage:  python code/src48_drill.py --bundle DIR --corpus DIR --source DIR
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src48_handoff_fidelity.py"
LITERATURE = ROOT / "data" / "external" / "handoff-v1-literature-check.json"
GATE_TIMEOUT_SECONDS = 300

DEFECTS = [
    # --- the locators, which is where a fidelity check fails quietly ---
    ("D1_arXiv_identifiers_are_treated_as_constants_again",
     "    ids = set(arxiv_ids(text))\n"
     "    return sorted(set(m.group(0) for m in re.finditer(r\"\\d+\\.\\d{%d,}\" % DECIMALS, text)\n"
     "                      if m.group(0) not in ids))",
     "    ids = set()\n"
     "    return sorted(set(m.group(0) for m in re.finditer(r\"\\d+\\.\\d{%d,}\" % DECIMALS, text)\n"
     "                      if m.group(0) not in ids))",
     "numbers found in no round document"),
    # D2 first replaced the whole squeeze with the identity -- which changes
    # nothing, because the handoff happens to write this lemma in exactly the
    # canonical spacing, so both sides matched unsqueezed. The pre-flight named
    # it. The real bug was normalising ONE side, so that is what is planted now.
    ("D2_the_squeeze_normalises_the_haystack_only",
     '    handoff_states_sqrt_L = squeeze(r"\\mathcal O_L\\gtrsim\\sqrt L") in flat_handoff',
     '    handoff_states_sqrt_L = r"\\mathcal O_L\\gtrsim\\sqrt L" in flat_handoff',
     "cannot find the handoff's own lemma"),
    ("D16_the_divisor_line_locator_normalises_one_side_only",
     '    handoff_states_twelfth = squeeze(r"\\Lambda_L\\ge\\mathcal O_L/12") in flat_handoff',
     '    handoff_states_twelfth = r"\\Lambda_L\\ge\\mathcal O_L/12" in flat_handoff',
     "half its arithmetic is unread"),
    ("D3_the_reference_list_section_is_mislocated",
     '    section = handoff.split("# 25.")[-1].split("# 26.")[0]',
     '    section = handoff.split("# 26.")[-1].split("# 27.")[0]',
     "standing reference list could not be located"),
    ("D4_the_file_manifest_section_is_mislocated",
     '    section = handoff.split("# 24.")[-1].split("# 25.")[0]',
     '    section = handoff.split("# 2.")[-1].split("# 3.")[0]',
     "file manifest could not be located"),
    ("D5_the_corpus_trace_looks_at_one_document_only",
     "    verbatim = sorted(n for n, t in corpus.items() if value in t)",
     "    verbatim = sorted(n for n, t in list(corpus.items())[:1] if value in t)",
     "numbers found in no round document"),
    # --- the constants ---
    ("D6_kappa_rot_closed_form_uses_the_wrong_root",
     '    "kappa_rot = 1/(12 sqrt 2)": (lambda: 1 / (12 * mp.sqrt(2)), "0.05892556510"),',
     '    "kappa_rot = 1/(12 sqrt 2)": (lambda: 1 / (12 * mp.sqrt(3)), "0.05892556510"),',
     "disagrees with its closed form"),
    ("D7_sigma_star_is_the_wrong_rational",
     '    "sigma_star = 1/(1+theta)": (Fraction(12791, 15291), "0.836505133739"),',
     '    "sigma_star = 1/(1+theta)": (Fraction(12791, 15292), "0.836505133739"),',
     "disagrees with its closed form"),
    ("D8_a_constant_the_check_claims_to_read_is_not_in_the_handoff",
     '    "beta = log2 3": (lambda: mp.log(3, 2), "1.5849625007"),',
     '    "beta = log2 3": (lambda: mp.log(3, 2), "1.58496250072"),',
     "not in the handoff"),
    # --- the status disclaimers ---
    ("D9_a_required_statement_pattern_can_no_longer_match",
     '        r"不宣稱已證\\s*Collatz\\s*/\\s*Terras\\s*/\\s*CASP",',
     '        r"不宣稱已證\\s*Collatz\\s*/\\s*Terras\\s*/\\s*CASPX",',
     "drops required statements"),
    ("D10_an_absence_check_is_made_vacuous",
     '        (r"CASP\\s*(已證明|已被證明|is proved|已證$)", "CASP 已證明"),',
     '        (r"CASP\\s*(絕不可能出現的字串)", "CASP 已證明"),',
     "absence check is vacuous"),
    # --- cross-bundle identity ---
    ("D11_every_reshipped_document_looks_divergent",
     "            hashes.setdefault(base, set()).add(\n"
     "                hashlib.sha256(zf.read(name)).hexdigest())",
     "            hashes.setdefault(base, set()).add(\n"
     "                hashlib.sha256(zf.read(name) + zpath.name.encode()).hexdigest())",
     "reshipped document differs between bundles"),
    ("D12_only_one_bundle_is_examined",
     '    for zpath in sorted(source.glob("Hard_Zeta*.zip")):',
     '    for zpath in sorted(source.glob("Hard_Zeta*.zip"))[:1]:',
     "did not exercise anything"),
    # --- the occupancy comparison itself ---
    ("D13_the_occupancy_bound_is_evaluated_at_the_wrong_horizon",
     "            H = mp.mpf(0)                     # the o(sqrt L) limit the round takes",
     "            H = mp.sqrt(N)                   # the o(sqrt L) limit the round takes",
     "does not tend to sqrt(L)/sqrt(2)"),
    # --- references the handoff introduces ---
    ("D14_an_introduced_reference_is_no_longer_checked",
     "    verified = {r.get(\"arxiv\"): r for r in lit.get(\"references\", [])}",
     "    verified = {}",
     "did not check them"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

#: Defects whose point is that the gate must STAY GREEN because another check
#: already covers the property. `None` means "the gate must still pass".
FINDING_ROBUSTNESS: dict[str, str | None] = {
    # The parenthetical in the reference finding counts how many entries carry a
    # caveat. Miscounting that changes the sentence and must NOT change whether
    # the finding is made -- the finding rests on the withdrawn entry itself.
    "D15_the_caveat_count_is_inflated": "withdrawn 2026-05-20, is listed in the standing",
}
DEFECTS.append(
    ("D15_the_caveat_count_is_inflated",
     '    with_caveat = [e for e in entries if "caveat" in e or "保留" in e]',
     '    with_caveat = list(entries)',
     "__robustness: the finding rests on the withdrawn entry, not the count__"))


def run_gate(bundle, corpus, source) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle),
             "--corpus", str(corpus), "--source", str(source),
             "--literature", str(LITERATURE)],
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
    ap.add_argument("--corpus", type=pathlib.Path, required=True)
    ap.add_argument("--source", type=pathlib.Path, required=True)
    args = ap.parse_args()

    snapshot = GATE.read_bytes()
    base = run_gate(args.bundle, args.corpus, args.source)
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
            res = run_gate(args.bundle, args.corpus, args.source)
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
                    "gate_still_green": bool(res.get("passed"))}
            else:
                was = any(needle in f for f in baseline_findings)
                now = any(needle in f for f in res.get("findings", []))
                report["defects"][name] = {
                    "caught": was and now,
                    "kind": "robustness: the finding must SURVIVE",
                    "finding_present_at_baseline": was,
                    "finding_survived": now}
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
            res = run_gate(args.bundle, args.corpus, args.source)
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
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
