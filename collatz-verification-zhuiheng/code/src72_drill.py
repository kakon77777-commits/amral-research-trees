"""RUN-053 mutation drill for `src72_primitive_unit.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing. The defect list lives
in `src72_drill_defects.py`; several of its anchors carry embedded quotes and
newlines, and a list this size audits better on its own.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" has four causes worth telling apart:
    unreachable, premise-empty, too weak, and mathematically identical to what
    it replaced;
  * from a GREEN baseline a defect must make a counter RISE. This round's
    strip is sharp at BOTH ends, so unlike A-U.2d.24's bounds -- which each
    carried a spare factor of three and needed a twenty-seventh to bite -- one
    unit is enough here;
  * a defect that changes only OBSERVATIONS is a finding about the gate;
  * seven defects aim at NON-VACUITY entries (N1-N7). Five of this round's
    findings ARE controls -- a broken window and three defused synthetic
    constructions -- and a control that stops firing proves nothing;
  * a defect that makes the gate RAISE is reported through
    `errors.<section>_raised` rather than crashing;
  * the pristine sidecar is written before anything is planted, every gate
    write retries a transient OS error, and the sidecar is removed only when
    the file is provably back.

Usage:
    python code/src72_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src72_drill_defects import DEFECTS                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src72_primitive_unit.py"
GATE_TIMEOUT_SECONDS = 900


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
