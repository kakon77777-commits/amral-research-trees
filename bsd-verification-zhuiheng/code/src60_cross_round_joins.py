"""Gate 60 — cross-round joins: every prime set in every log, intersected with every other.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-057 found that member 3529 of the family is also an ordinary H2-obstruction
prime of the base — a fact whose two halves had sat in RUN-038's log and
RUN-047's log for many rounds, unjoined. That is the failure mode of a line
that reads one document per round: it never asks whether a set computed in one
round meets a set computed in another.

This gate asks that question mechanically. It walks every archived gate log,
collects every list of integers that looks like a set of primes, intersects
each pair drawn from different logs, and reports every non-empty intersection
together with whether any report already names it. The output is a table for a
reader, not a verdict: an intersection is a candidate for a finding, and most
candidates are noise — the bad primes {2, 3, 29} recur everywhere, Mazur's
twelve recur everywhere, small-prime scaffolding recurs everywhere. The gate
filters the obvious noise and leaves the judgement in the report.

What it asserts is narrow: that the 3529 join IS in the table — a joins gate
that could not find the one join already known would be measuring nothing —
and that the table is written.

Usage:  python code/src60_cross_round_joins.py
"""

from __future__ import annotations

import collections
import itertools
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
OUT = LOGS / "src60-cross-round-joins.json"

MIN_ELEMENT = 50          # sets living entirely below this are scaffolding
MIN_SIZE = 2
MAX_SIZE = 5000
PRIME_FRACTION = 0.8      # a "prime set" is mostly primes
NOISE_IF_SEEN_IN = 4      # an identical set appearing in this many logs is a constant

_PRIMES = set(anchor.sieve(200_000))


def _is_prime(n: int) -> bool:
    if n < 200_000:
        return n in _PRIMES
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def _walk(o, path: str, out: list) -> None:
    if isinstance(o, dict):
        for k, v in o.items():
            _walk(v, f"{path}.{k}" if path else k, out)
    elif isinstance(o, list):
        if (MIN_SIZE <= len(o) <= MAX_SIZE
                and all(isinstance(x, int) and not isinstance(x, bool) for x in o)):
            out.append((path, o))
        else:
            for i, v in enumerate(o):
                _walk(v, f"{path}[{i}]", out)


def prime_sets() -> list[dict]:
    """Every list of integers in every log that is mostly primes and not
    entirely small."""
    sets = []
    for f in sorted(LOGS.glob("src*.json")):
        if f.name.startswith("src60-"):
            continue                          # never join this gate to itself
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:                                # pragma: no cover
            continue
        found: list = []
        _walk(d, "", found)
        for path, lst in found:
            s = sorted(set(lst))
            if max(s) < MIN_ELEMENT:
                continue
            if sum(_is_prime(x) for x in s) < PRIME_FRACTION * len(s):
                continue
            sets.append({"log": f.name, "path": path, "set": s, "size": len(s)})
    return sets


def drop_constants(sets: list[dict]) -> tuple[list[dict], list[dict]]:
    """A set that appears identically in many logs is scaffolding, not a
    finding — Mazur's degrees, the bad primes, the certified surjectivity list
    re-read by later gates."""
    by_content: dict[tuple, set] = collections.defaultdict(set)
    for s in sets:
        by_content[tuple(s["set"])].add(s["log"])
    keep, dropped = [], []
    for s in sets:
        if len(by_content[tuple(s["set"])]) >= NOISE_IF_SEEN_IN:
            dropped.append(s)
        else:
            keep.append(s)
    return keep, dropped


SCAFFOLDING = {2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163, 29}   # Mazur + 29


def _is_prime_segment(s: list[int]) -> bool:
    """All primes in [min, max] — a sieve's `primes_tested`, not a finding."""
    lo, hi = min(s), max(s)
    seg = [q for q in anchor.sieve(hi) if q >= lo]
    return len(s) >= 5 and seg == s


def joins(sets: list[dict]) -> list[dict]:
    """Every non-empty intersection between prime sets from different logs,
    minus the two shapes that are never findings: an intersection inside the
    scaffolding every gate tests (Mazur's twelve and 29), and a join against a
    plain initial segment of primes, which says only that a bound is large."""
    out = []
    for a, b in itertools.combinations(sets, 2):
        if a["log"] == b["log"]:
            continue
        inter = sorted(set(a["set"]) & set(b["set"]))
        if not inter:
            continue
        if set(inter) <= SCAFFOLDING:
            continue
        if _is_prime_segment(a["set"]) or _is_prime_segment(b["set"]):
            continue
        # a set contained in another is a re-read, not a join
        if set(a["set"]) <= set(b["set"]) or set(b["set"]) <= set(a["set"]):
            continue
        out.append({"a": f"{a['log']} :: {a['path']}",
                    "b": f"{b['log']} :: {b['path']}",
                    "size_a": a["size"], "size_b": b["size"],
                    "intersection": inter[:40], "size": len(inter)})
    return out


_ROUND_OF: dict[str, str] = {}


def round_of(log_name: str) -> str | None:
    """Which RUN-NNN report lists this log's gate under **Tools:**."""
    if not _ROUND_OF:
        for f in sorted(REPORTS.glob("RUN-*.md")):
            head = f.read_text(encoding="utf-8")[:3000]
            for m in re.finditer(r"src(\d\d)_\w+\.py", head):
                _ROUND_OF.setdefault(m.group(0)[:5], f.name[:7])
    return _ROUND_OF.get(log_name[:5])


def mentioned_in_reports(join: dict) -> dict:
    """Has the JOIN been made — not merely the numbers written down?

    A number can sit in a report as a member of one round's list without that
    report ever meeting the other round. RUN-038's report names 3529 as an
    obstruction prime and RUN-047's names it as a member; neither joins them.
    So the test is: some single report names every number of the intersection
    AND references both source rounds (its own round counts as a reference).
    """
    nums = join["intersection"]
    if len(nums) > 12:
        return {"checked": False, "why": "too many numbers to require in one "
                                         "report"}
    ra = round_of(join["a"].split(" :: ")[0])
    rb = round_of(join["b"].split(" :: ")[0])
    hits, numbers_only = [], []
    for f in sorted(REPORTS.glob("RUN-*.md")):
        t = f.read_text(encoding="utf-8")
        if not all(re.search(rf"(?<!\d){n}(?!\d)", t) for n in nums):
            continue
        me = f.name[:7]
        refs_a = ra is None or ra == me or ra in t
        refs_b = rb is None or rb == me or rb in t
        (hits if (refs_a and refs_b) else numbers_only).append(me)
    return {"checked": True, "round_a": ra, "round_b": rb,
            "reports_making_the_join": hits,
            "reports_naming_numbers_only": numbers_only[:6],
            "join_made": bool(hits)}


def the_known_join(all_joins: list[dict]) -> dict:
    """The join RUN-057 made by hand must be in the table — and specifically
    the one between RUN-038's obstruction list (src40) and a MEMBERSHIP list of
    𝒫 (src49's three definitions, or src16's member list). A row that merely
    contains 3529 and touches src40 is not enough: src59 re-reads src40's list,
    so a containment row would survive filters that had dropped every real
    join. The first version of this test accepted that, and a planted
    inverted-containment defect went uncaught because of it."""
    rows = [j for j in all_joins if 3529 in j["intersection"]]
    src40 = [j for j in rows if "src40" in j["a"] or "src40" in j["b"]]
    def other(j):
        return j["b"] if "src40" in j["a"] else j["a"]
    against_membership = [j for j in src40
                          if other(j).startswith(("src49", "src16"))]
    return {"joins_containing_3529": len(rows),
            "of_which_touch_RUN_038s_log": len(src40),
            "of_which_meet_a_membership_list": len(against_membership),
            "found": bool(against_membership),
            "examples": [{"a": j["a"], "b": j["b"], "inter": j["intersection"][:6]}
                         for j in against_membership[:4]]}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    sets = prime_sets()
    kept, dropped = drop_constants(sets)
    all_joins = joins(kept)
    for j in all_joins:
        j["mentioned"] = mentioned_in_reports(j)
    unmentioned = [j for j in all_joins
                   if j["mentioned"].get("checked") and not j["mentioned"]["join_made"]]
    unmentioned.sort(key=lambda j: (-j["size"], j["a"]))
    known = the_known_join(all_joins)

    ok = (len(sets) >= 20 and known["found"] and len(all_joins) >= 1)

    log = {
        "gate": "src60 — cross-round joins",
        "parameters": {"min_element": MIN_ELEMENT, "prime_fraction": PRIME_FRACTION,
                       "noise_if_seen_in": NOISE_IF_SEEN_IN},
        "prime_sets_found": len(sets),
        "dropped_as_constants": len(dropped),
        "constants": sorted({f"{s['log']} :: {s['path']}" for s in dropped})[:30],
        "sets_joined": len(kept),
        "joins": len(all_joins),
        "joins_made": sum(1 for j in all_joins
                          if j["mentioned"].get("checked") and j["mentioned"]["join_made"]),
        "joins_unchecked_too_many_numbers": sum(
            1 for j in all_joins if not j["mentioned"].get("checked")),
        "joins_not_named_in_any_report": len(unmentioned),
        "table_unmentioned": unmentioned[:60],
        "table_all": all_joins[:200],
        "the_known_join_3529": known,
        "reading": ("a row is a CANDIDATE. Most are two gates reading the same "
                    "upstream fact — the same witness primes, the same member "
                    "list — and mean nothing. The ones worth a round are where "
                    "two different COMPUTATIONS meet at a number neither round "
                    "expected, the way RUN-038's obstruction list met RUN-047's "
                    "membership list at 3529"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  {len(sets)} prime sets across the logs; {len(dropped)} dropped as "
          f"constants (identical in ≥ {NOISE_IF_SEEN_IN} logs); {len(kept)} joined")
    print(f"  {len(all_joins)} non-empty cross-log intersections; "
          f"{len(unmentioned)} not named together in any report")
    print(f"  the 3529 join is in the table: {known['found']} "
          f"({known['joins_containing_3529']} rows contain 3529, "
          f"{known['of_which_touch_RUN_038s_log']} touch src40)")
    print()
    print("  unmentioned joins, largest first:")
    for j in unmentioned[:18]:
        print(f"    {j['size']:3d}  {j['intersection'][:6]}{'…' if j['size'] > 6 else ''}")
        print(f"          {j['a'][:70]}")
        print(f"          {j['b'][:70]}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
