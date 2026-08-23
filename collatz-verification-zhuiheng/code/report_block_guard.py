"""A staleness guard for the report-block emitters that can actually fail.

數學戰士「墜衡」 / AMRAL Research Lab.

The guard this replaces could not fail. It perturbed one digit of the emitted
block and asserted the perturbed string differed from the original::

    missed = [i for i in digits
              if (block[:i] + ("9" if block[i] != "9" else "0") + block[i+1:]) == block]

That is true by construction for every string and every substitution, so `missed`
was empty in every possible universe. It printed `digits_guarded: N` and measured
nothing. Shipped in src43, src44 and src45 before anyone asked what would have to
break for it to go red.

What it was reaching for is a real property with a real failure mode:

    every figure in the block must come from a log, not from the emitter's own
    format strings.

So perturb the **log** and require the block to move. `discover` does that for
every value in every log and returns the ones the block actually reads;
`check_against_snapshot` compares that set against a stored one. A figure that
stops moving with its log has stopped being read, which is what a figure typed
into prose looks like.

What this does **not** claim: that no *undeclared* number in the block is typed.
An automatic version of that was tried and abandoned -- perturbing `13.4` to
`97.05` introduces a `0` that was not there, and a figure printed as `len([])`
has no digit anywhere in the log to perturb, so both came back as false
accusations. The honest scope is: every declared figure is load-bearing, and the
declaration is derived from a run.
"""

from __future__ import annotations

import copy
import json
import pathlib


def perturb(value):
    """Change a value into a different value of a comparable kind.

    Digit-clean on purpose. A first version appended "~" to strings and added
    1.0 to floats, which left `2605.13886` and `0.024674` carrying every original
    digit, so a perturbed figure looked untouched.
    """
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value * 10 + 7
    if isinstance(value, float):
        return value * 7.0 + 3.25
    if isinstance(value, str):
        shifted = "".join(str((int(c) + 5) % 10) if c.isdigit() else c for c in value)
        return shifted if shifted != value else value + "~"
    if isinstance(value, list):
        return [perturb(v) for v in value] if value else ["~"]
    if isinstance(value, dict):
        return dict(value, **{"~": "~"})
    if value is None:
        return "~"
    raise TypeError("no perturbation for %r" % type(value))


def _get(obj, path):
    for key in path:
        obj = obj[key]
    return obj


def _set(obj, path, value):
    for key in path[:-1]:
        obj = obj[key]
    obj[path[-1]] = value


def _moves(build, logs, baseline, index, path):
    mutated = [copy.deepcopy(log) for log in logs]
    _set(mutated[index], path, perturb(_get(mutated[index], path)))
    try:
        return build(*mutated) != baseline
    except Exception:
        return True                 # a value the build cannot run without is read


def _candidates(obj, index, path=()):
    """Every value a build could read: scalars, flat lists, and numeric dict keys.

    Keys matter -- src43 tabulates `record_updates_against_log2N` by its keys, so
    a sweep blind to keys would miss that whole column.
    """
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            yield from _candidates(obj[key], index, path + (key,))
    elif isinstance(obj, list):
        if any(isinstance(v, (dict, list)) for v in obj):
            for i, value in enumerate(obj):
                yield from _candidates(value, index, path + (i,))
        elif path:
            yield index, path
    elif path:
        yield index, path


def discover(build, logs):
    """Return the (index, path) pairs the block actually reads. Run once."""
    logs = list(logs)
    baseline = build(*logs)
    return [(i, p) for i, p in
            (c for log_i, log in enumerate(logs) for c in _candidates(log, log_i))
            if _moves(build, logs, baseline, i, p)]


def label(sourced):
    return sorted("%d:%s" % (i, "/".join(str(k) for k in p)) for i, p in sourced)


def check_against_snapshot(build, logs, snapshot_path, *, refresh=False):
    """Compare what the block reads now against a stored snapshot of what it read.

    The snapshot lives beside the gate logs rather than in the source, because
    fifty-odd paths inlined into an emitter is noise nobody rereads. `removed` is
    the regression that matters: a figure that stopped being load-bearing is a
    figure somebody typed into prose. `added` goes red too, so a refresh is a
    deliberate act with a diff, not a silent drift.
    """
    found = label(discover(build, logs))
    snapshot_path = pathlib.Path(snapshot_path)
    if refresh or not snapshot_path.exists():
        snapshot_path.write_text(json.dumps(found, indent=2) + "\n", encoding="utf-8")
        return {"figures_read": len(found), "snapshot": "written",
                "figures_no_longer_read": [], "figures_newly_read": [], "ok": True}
    stored = json.loads(snapshot_path.read_text(encoding="utf-8"))
    removed = sorted(set(stored) - set(found))
    added = sorted(set(found) - set(stored))
    return {
        "figures_read": len(found),
        "snapshot": snapshot_path.name,
        "figures_no_longer_read": removed,
        "figures_newly_read": added,
        "ok": not removed and not added,
    }


def _self_test() -> int:
    """Show the guard failing, so nobody has to take the gate on faith."""
    import tempfile

    log = {"counts": {"planted": 12}}
    reads = lambda g: "planted `%d`" % g["counts"]["planted"]       # noqa: E731
    types = lambda g: "planted `12`"                                # noqa: E731

    found = discover(reads, [log])
    blind = discover(types, [log])

    snap = pathlib.Path(tempfile.gettempdir()) / "report_block_guard_selftest.json"
    if snap.exists():
        snap.unlink()
    first = check_against_snapshot(reads, [log], snap)       # writes it
    unchanged = check_against_snapshot(reads, [log], snap)   # still reading it
    regressed = check_against_snapshot(types, [log], snap)   # somebody typed it
    snap.unlink()

    ok = (found == [(0, ("counts", "planted"))]
          and blind == []
          and first["ok"] and unchanged["ok"]
          and not regressed["ok"]
          and regressed["figures_no_longer_read"] == ["0:counts/planted"])
    print(json.dumps({"tool": "report_block_guard.py", "mode": "self-test",
                      "discover_finds_a_figure_read_from_the_log": found == [(0, ("counts", "planted"))],
                      "discover_finds_nothing_when_it_is_typed": blind == [],
                      "an_unchanged_emitter_stays_green": unchanged,
                      "a_figure_that_stopped_being_read_goes_red": regressed,
                      "the_guard_can_fail": ok, "ok": ok}, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(_self_test())
