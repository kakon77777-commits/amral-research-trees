"""Can the item-49 archive-integrity check actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src49_archive_integrity.py` reports that 47 of 50 entries are byte-identical to
the standalone items this sweep already verified, that all 964 files open at every
one of nine nesting levels, that both shipped `SHA256SUMS.txt` manifests verify
perfectly — and that they cover the wrong half of what they ship.

An archive check has a shape that makes drilling awkward: **almost every branch
that would report a defect is one no real input reaches.** Nothing differs, so
`differing` is always empty; nothing is unreadable, so `unreadable` is always
empty. Weakening a branch that never fires is invisible, which is the item-43
lesson. So the defects here break the **subject** — the hash, the lookup, the
recursion — and make the empty branch fill, rather than loosening a comparison
that has nothing to compare.

The other half is the non-vacuity guards. A check that reads nothing reports a
clean archive, so the gate fails when the recursive walk does not descend, when
no manifest is verified, when the two pack versions come back indistinguishable,
when the composition prefix matches nothing, and when the coverage set is empty.
Six of the defects below aim at exactly those.

Usage:  python code/src49_drill.py --archive PATH --source DIR --manifest PATH
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src49_archive_integrity.py"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the entry comparison: make the empty branch fill ---
    ("D1_entries_are_matched_against_the_wrong_recorded_item",
     '        rec = recorded.get(name)',
     '        rec = recorded.get(name) if name.startswith("Hard") else '
     'list(recorded.values())[0]',
     "has drifted from the standalone item"),
    ("D2_the_on_disk_comparison_is_dropped",
     '        same_as_disk = live.exists() and sha256(live.read_bytes()) == digest',
     '        same_as_disk = True',
     "__robustness: the recorded hash is still compared__"),
    # --- the recursive walk ---
    ("D3_the_walk_never_descends",
     '            if name.lower().endswith(".zip"):\n'
     '                stats["nested_zips"] += 1\n'
     '                walk(zf.read(name), name, depth + 1)',
     '            if name.lower().endswith(".zip") and False:\n'
     '                stats["nested_zips"] += 1\n'
     '                walk(zf.read(name), name, depth + 1)',
     "recursive walk did not descend"),
    ("D4_every_nested_archive_looks_unreadable",
     '        try:\n'
     '            zf = entries_of(data)\n'
     '            names = zf.namelist()\n'
     '        except zipfile.BadZipFile:',
     '        try:\n'
     '            zf = entries_of(data)\n'
     '            names = zf.namelist()\n'
     '            raise zipfile.BadZipFile("planted")\n'
     '        except zipfile.BadZipFile:',
     "could not be opened"),
    ("D5_the_depth_limit_stops_the_walk_immediately",
     "MAX_DEPTH = 24               # a nested archive is a loop risk, not just deep",
     "MAX_DEPTH = 1                # a nested archive is a loop risk, not just deep",
     "could not be opened"),
    # --- the shipped checksums ---
    ("D6_the_verification_hashes_with_the_wrong_function",
     "def sha256(data: bytes) -> str:\n"
     "    return hashlib.sha256(data).hexdigest()",
     "def sha256(data: bytes) -> str:\n"
     "    return hashlib.sha1(data).hexdigest()",
     "does not match its file"),
    # D7 first parsed on a single space instead of two. That is a no-op here:
    # the extra space lands at the front of the filename and `.strip()` removes
    # it, so the parse produces exactly the same table. The pre-flight named it.
    # Swapping the two fields is the same slip with a consequence.
    ("D7_the_manifest_columns_are_read_in_the_wrong_order",
     '        digest, _, name = line.partition("  ")',
     '        name, _, digest = line.partition("  ")',
     "lists a file the pack does not contain"),
    ("D8_no_pack_manifest_is_read_at_all",
     '        if not sums:\n'
     '            continue\n'
     '        root, files = _pack_files(inner)',
     '        if True:\n'
     '            continue\n'
     '        root, files = _pack_files(inner)',
     "no shipped manifest was verified"),
    # --- the coverage question that produces the main finding ---
    ("D9_the_two_pack_versions_are_the_same_pack",
     '    _, a = _pack_files(entries_of(zf.read(older)))',
     '    _, a = _pack_files(entries_of(zf.read(newer)))',
     "indistinguishable, so the coverage question"),
    # --- the version chain ---
    ("D10_the_version_chain_is_not_followed",
     '        for n in sorted(files):\n'
     '            if n.lower().endswith(".zip"):\n'
     '                walk(inner.read(n), n, depth + 1)',
     '        for n in sorted(files):\n'
     '            if n.lower().endswith(".zip") and False:\n'
     '                walk(inner.read(n), n, depth + 1)',
     "version chain was not followed"),
    # --- the non-vacuity guards on the measurements ---
    ("D11_the_composition_prefix_matches_nothing",
     '        "against_this_trees_archive": check_against_this_trees_archive(',
     '        "composition_unused": None,\n'
     '        "against_this_trees_archive": check_against_this_trees_archive(',
     "__robustness: an added report key changes no verdict__"),
    ("D12_the_composition_prefix_is_never_matched",
     '        "composition": check_composition(data, "CPL_"),',
     '        "composition": check_composition(data, "NOTHING_MATCHES_THIS_"),',
     "matched no entries"),
    # D13's flip yields 24 items rather than 48 -- still plenty for a size
    # threshold, which is why the guard now asks whether the archive CONTAINS
    # the set it selected rather than how big that set is.
    ("D13_the_coverage_set_is_built_from_the_wrong_side",
     '    older = [it for it in manifest["items"]\n'
     '             if it["mtime_local"] < cut and it["name"] != archive_name]',
     '    older = [it for it in manifest["items"]\n'
     '             if it["mtime_local"] > cut and it["name"] != archive_name]',
     "not looking at the archive's own contents"),
    ("D14_too_few_entries_are_compared_to_be_a_comparison",
     '    for name in sorted(n for n in zf.namelist() if not n.endswith("/")):',
     '    for name in sorted(n for n in zf.namelist() if not n.endswith("/"))[:3]:',
     "too few entries were compared"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D2_the_on_disk_comparison_is_dropped": None,
    "D11_the_composition_prefix_matches_nothing": None,
}


def run_gate(args) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--archive", str(args.archive),
             "--source", str(args.source), "--manifest", str(args.manifest)],
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
    ap.add_argument("--archive", type=pathlib.Path, required=True)
    ap.add_argument("--source", type=pathlib.Path, required=True)
    ap.add_argument("--manifest", type=pathlib.Path, required=True)
    args = ap.parse_args()

    snapshot = GATE.read_bytes()
    base = run_gate(args)
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
            res = run_gate(args)
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
            res = run_gate(args)
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
