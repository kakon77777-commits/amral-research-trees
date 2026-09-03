"""Drill: do the sweep-input guards in build_results.py actually refuse?

數學戰士「墜衡」 / AMRAL Research Lab.

`build_results.py` gained three refusals when the paper sweep was folded into
data/results.v1.json. On the real archived inputs all three are silent, and a
guard that has only ever been silent is indistinguishable from a comment — the
exact shape this tree spent seventy-three rounds cataloguing in other people's
checkers. So each one is driven here with an input crafted to trip it.

The bar is the same one the rest of the suite uses: a planted defect must be
caught by the check NAMED for it, not merely by some check. A refusal carrying
the wrong message would pass a weaker test and is counted as a survivor here.

Usage:  python code/build_results_guard_drill.py
"""

from __future__ import annotations

import copy
import io
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

import build_results  # noqa: E402


def real_inputs() -> tuple[dict, dict]:
    """The archived totals and manifest, exactly as the builder reads them."""
    totals = json.loads((ROOT / "data" / "gate-logs" / "suite-totals.json")
                        .read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "data" / "source-manifest.v1.json")
                          .read_text(encoding="utf-8"))
    return totals, manifest


def run(totals: dict, manifest: dict) -> str | None:
    """Return the refusal message, or None if the guard let the input through."""
    try:
        build_results.check_sweep_inputs(totals, manifest)
    except build_results.SweepInputError as exc:
        return str(exc)
    return None


def main() -> int:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    except (AttributeError, ValueError):                 # pragma: no cover
        pass

    totals, manifest = real_inputs()
    defects: dict[str, dict] = {}

    # D1 - a red aggregation must stop the build, not be summarised.
    t = copy.deepcopy(totals)
    t["ok"] = False
    msg = run(t, manifest)
    defects["D1_totals_report_themselves_red"] = {
        "why": "suite_totals.py exiting non-zero must not become a published figure",
        "refused": msg is not None,
        "named_check": bool(msg and "red" in msg),
        "message": msg,
    }

    # D2 - a drill log the aggregator could not classify means the count is a
    # floor, not a total. Publishing it as a total is the silent undercount.
    t = copy.deepcopy(totals)
    t["uninterpreted"] = ["src99-drill.json"]
    msg = run(t, manifest)
    defects["D2_a_drill_log_was_not_interpreted"] = {
        "why": "an unclassified drill contributes zero; the total would look plausible",
        "refused": msg is not None,
        "named_check": bool(msg and "undercount" in msg),
        "message": msg,
    }

    # D3 - a source item with no recheck and no owning line is a gap in the
    # sweep, and the sweep must not be reported as complete over it.
    m = copy.deepcopy(manifest)
    m["unprocessed"] = ["Some_Round_That_Was_Never_Touched_bundle.zip"]
    msg = run(totals, m)
    defects["D3_a_source_item_was_never_processed"] = {
        "why": "the figure this tree cites as 73/73 must not survive a real gap",
        "refused": msg is not None,
        "named_check": bool(msg and "complete" in msg),
        "message": msg,
    }

    # D4 - a half-written log has no `ok` at all. Absent must be treated as red,
    # never as pass-by-default.
    t = copy.deepcopy(totals)
    del t["ok"]
    msg = run(t, manifest)
    defects["D4_the_ok_field_is_missing_entirely"] = {
        "why": "a truncated gate log must refuse, not read as unset-therefore-fine",
        "refused": msg is not None,
        "named_check": bool(msg and "red" in msg),
        "message": msg,
    }

    # D5 - the README asserts the sweep's completeness in its own sentence, from
    # its own counter. That claim must also break when an item goes unhandled.
    # Only sweep_counts() is called: emit_readme_counts.main() rewrites the real
    # README, so it is never invoked against a crafted manifest.
    import emit_readme_counts                            # noqa: PLC0415

    real = json.loads((ROOT / "data" / "source-manifest.v1.json")
                      .read_text(encoding="utf-8"))
    kept = emit_readme_counts.MANIFEST
    with tempfile.TemporaryDirectory() as td:
        # deliberately not under data/gate-logs/: suite_totals.py globs that
        # directory, and a stray crafted file there would land in the totals
        crafted = pathlib.Path(td) / "crafted-manifest.json"
        crafted.write_text(json.dumps(
            {"item_count": real["item_count"],
             "processed_count": real["processed_count"] - 1,
             "belongs_to_another_line": real["belongs_to_another_line"]}),
            encoding="utf-8")
        try:
            emit_readme_counts.MANIFEST = crafted
            total, done = emit_readme_counts.sweep_counts()
        finally:
            emit_readme_counts.MANIFEST = kept
    defects["D5_the_readme_counter_over_an_unhandled_item"] = {
        "why": "'Across N source items' must stop being N when one is unaccounted for",
        "refused": total != done,
        "named_check": total != done and done == total - 1,
        "message": f"item_count={total}, dispositioned={done}",
    }

    # Controls: inputs that must NOT be refused. If a control trips, the guard
    # is over-eager and the drill above proves nothing about discrimination.
    controls: dict[str, dict] = {}

    total, done = emit_readme_counts.sweep_counts()
    controls["C3_the_readme_counter_on_the_real_manifest"] = {
        "why": "the tree's actual state must read as complete",
        "undisturbed": total == done,
        "message": f"item_count={total}, dispositioned={done}",
    }

    msg = run(copy.deepcopy(totals), copy.deepcopy(manifest))
    controls["C1_the_real_archived_inputs"] = {
        "why": "the state the tree is actually in must build",
        "undisturbed": msg is None,
        "message": msg,
    }

    t = copy.deepcopy(totals)
    m = copy.deepcopy(manifest)
    t["some_field_added_later"] = {"a": 1}
    m["unprocessed"] = []
    m["another_new_field"] = 7
    msg = run(t, m)
    controls["C2_unrelated_new_fields_and_an_empty_gap_list"] = {
        "why": "an empty `unprocessed` is the healthy state, not a missing key",
        "undisturbed": msg is None,
        "message": msg,
    }

    planted = len(defects)
    caught = sum(1 for d in defects.values() if d["refused"] and d["named_check"])
    refused_at_all = sum(1 for d in defects.values() if d["refused"])
    undisturbed = sum(1 for c in controls.values() if c["undisturbed"])

    log = {
        "tool": "build_results_guard_drill.py",
        "subject": ("code/build_results.py check_sweep_inputs() and "
                    "code/emit_readme_counts.py sweep_counts()"),
        "note": ("each defect must be refused by the check named for it; a refusal "
                 "with the wrong message counts as a survivor"),
        "defects": defects,
        "controls": controls,
        "counts": {
            "defects_planted": planted,
            "defects_caught_by_the_named_check": caught,
            "defects_refused_by_any_check": refused_at_all,
            "controls": len(controls),
            "controls_undisturbed": undisturbed,
        },
        "ok": caught == planted and undisturbed == len(controls),
    }

    out = ROOT / "data" / "gate-logs" / "build-results-guard-drill.json"
    out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"counts": log["counts"], "ok": log["ok"]},
                     indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
