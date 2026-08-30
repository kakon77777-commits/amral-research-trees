"""Show, on the real logs, that a figure typed into a report is caught.

數學戰士「墜衡」 / AMRAL Research Lab.

`report_block_guard` replaced a guard that could not fail. Asserting that the
replacement can fail is not the same as showing it, so this freezes one figure in
each report emitter -- exactly what a copy-paste does, the number
stops tracking its log -- and requires the emitter to go red. Five emitters now.

Two screens keep the demo from being the thing it is testing:

  * **the unchanged emitter must be green**, or "red" proves nothing;
  * **the freeze must be a real mutation**, checked by running the frozen build
    against a perturbed log and requiring the output to differ.

The second screen earned its place immediately. The first version of this demo
replaced ``` `9999` ``` with the same literal, but two of the emitters print
that figure without backticks, so the substring never occurred, nothing was
planted, and the guard passed for the wrong reason -- the same malformed-defect
class that `srcNN_drill.py` screens for.

Usage:  python code/emitter_guard_demo.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot, perturb   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent

# One figure per emitter: something central enough that freezing it would be a
# real defect in the published report.
CASES = [
    ("src43", (0, ("determinant", "positive_on_real_brackets", "pairs"))),
    ("src44", (0, ("horizons", "starts"))),
    ("src45", (0, ("rotation_cap", "crossings"))),
    ("src46", (0, ("saturation_equivalence", "crossings"))),
    ("src47", (0, ("continued_fraction", "largest_denominator_certified"))),
    ("src48", (0, ("cross_bundle_identity", "distinct_documents"))),
    ("src49", (0, ("recursive_integrity", "files"))),
    ("src50", (0, ("structure", "annulus_edges"))),
    ("src51", (0, ("orbit_structure", "renewal_edges"))),
    ("src52", (0, ("capacity", "pairs_enumerated"))),
    ("src53", (0, ("slope_quantization", "edges"))),
    ("src54", (0, ("segments", "segments"))),
    ("src55", (0, ("sieve", "odd_integers_mapped"))),
    ("src57", (0, ("reciprocal_flow", "edges"))),
    ("src58", (0, ("certificates", "inequalities_checked"))),
    ("src59", (0, ("results", "orbits", "sliding_block_identities_checked"))),
    ("src60", (0, ("results", "orbits", "first_crossing_intervals"))),
    ("src61", (0, ("results", "suffix", "suffix_minima"))),
    ("src62", (0, ("results", "q1", "pairs_from_a_suffix_minimum"))),
    ("src63", (0, ("results", "bank", "steps"))),
]


def load(stem):
    path = ROOT / ("%s_emit_report_block.py" % stem)
    spec = importlib.util.spec_from_file_location(stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[stem] = module
    spec.loader.exec_module(module)
    logs = [module.GATE_LOG, module.DRILL_LOG]
    if hasattr(module, "LIT_LOG"):
        logs.append(module.LIT_LOG)
    return module, [json.loads(p.read_text(encoding="utf-8")) for p in logs]


def _at(logs, where):
    value = logs[where[0]]
    for key in where[1]:
        value = value[key]
    return value


def freeze(module, logs, where):
    """A build whose figure is stuck at today's value, however the log moves."""
    literal = str(_at(logs, where))

    def frozen(*args):
        return module.build(*args).replace(str(_at(args, where)), literal)

    return frozen, literal


def main() -> int:
    cases, all_ok = [], True
    for stem, where in CASES:
        module, logs = load(stem)
        honest = check_against_snapshot(module.build, logs, module.FIGURES)

        frozen, literal = freeze(module, logs, where)

        bumped = [copy.deepcopy(log) for log in logs]
        holder = bumped[where[0]]
        for key in where[1][:-1]:
            holder = holder[key]
        holder[where[1][-1]] = perturb(holder[where[1][-1]])
        planted = frozen(*bumped) != module.build(*bumped)

        caught = check_against_snapshot(frozen, logs, module.FIGURES)
        ok = honest["ok"] and planted and not caught["ok"]
        all_ok = all_ok and ok
        cases.append({
            "emitter": "%s_emit_report_block.py" % stem,
            "figure_frozen": "%d:%s" % (where[0], "/".join(where[1])),
            "value_frozen_at": literal,
            "the_freeze_is_a_real_mutation": planted,
            "the_unchanged_emitter_is_green": honest["ok"],
            "figures_the_unchanged_emitter_reads": honest["figures_read"],
            "the_frozen_emitter_goes_red": not caught["ok"],
            "reported_as_no_longer_read": caught["figures_no_longer_read"],
            "ok": ok,
        })

    print(json.dumps({
        "tool": "emitter_guard_demo.py",
        "claim": "a figure typed into a report stops tracking its log, and the "
                 "guard says so -- shown on the real gate logs, not asserted",
        "cases": cases,
        "ok": all_ok,
    }, indent=2))
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
