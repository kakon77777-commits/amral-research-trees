"""Gate 31 — §Q9's twist accounting, measured from the artefacts rather than derived.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-028 checked `V0_5_EXACT_CENSUS_REPORT` §Q9's global accounting identity and
found it correct as arithmetic, with **four of its six independent inputs**
already computed by this tree in RUN-012. It named the two that were not —
`old_total_twist_pairs = 293482` and `upstream_removed = 24785` — as the
cheapest open item in Phase 1, since the identity ties them and one measurement
would close both.

This gate does better than that. Both twist artefacts are on the archive branch,
so **every term is measured directly** and none is inferred from the identity:

    old_total_twist_pairs   new_total_twist_pairs
    upstream_removed        stable_removed
    stable_added            newbase_added

An identity whose terms are all measured is a real check; one with two terms
back-solved from it is a tautology in those two. That difference is the round.

THE COUNTING RULE IS CALIBRATED, NOT ASSUMED. The artefact maps each label to a
list of twist discriminants including the trivial `d = 1`, so "twist pairs"
could mean the sum of list lengths or that minus one per label. The rule is
fixed by a value this tree has already verified: RUN-012 rebuilt **247,391**
pairs, and the d = 1-inclusive sum over the NEW artefact is 247,391 while the
exclusive one is 210,704. So the document counts the trivial twist, and the same
rule then applies to the old artefact rather than being chosen to fit it.

Usage:  python code/src31_q9_census_closure.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
ARCHIVE = "origin/agent/bsd"
BASE = ("bsd/BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12/inputs")
OUT = ROOT / "data" / "gate-logs" / "src31-q9-census-closure.json"

# §Q9 and §Q4 as the report prints them, plus the base count the twist artefact
# is a subset of.
STATED = {"old_total_twist_pairs": 293482, "new_total_twist_pairs": 247391,
          "lhs": 46091, "upstream_removed": 24785, "stable_removed": 21306,
          "stable_added": 0, "newbase_added": 0, "rhs": 46091}
BASE_CURVES = 40749          # RUN-004's census, recomputed there
KEPT_CURVES = 36687          # RUN-008's kept set, closed both ways there


def _blob(path: str) -> tuple[str, bytes]:
    """The archive branch's blob at `path`, with its object id for provenance."""
    oid = subprocess.run(["git", "rev-parse", f"{ARCHIVE}:{path}"], cwd=REPO,
                         capture_output=True, text=True)
    if oid.returncode != 0:
        raise SystemExit(f"not on {ARCHIVE}: {path}")
    data = subprocess.run(["git", "cat-file", "-p", oid.stdout.strip()],
                          cwd=REPO, capture_output=True)
    if data.returncode != 0:
        raise SystemExit(f"could not read blob for {path}")
    return oid.stdout.strip(), data.stdout


def load(which: str) -> tuple[str, dict]:
    oid, raw = _blob(f"{BASE}/{which}/twists_of_ec_labels_500k.json")
    return oid, json.loads(raw.decode("utf-8"))


def calibrate(new: dict) -> dict:
    """Which counting rule the document uses, decided by a verified number."""
    inclusive = sum(len(v) for v in new.values())
    exclusive = sum(sum(1 for d in v if d != 1) for v in new.values())
    return {
        "pairs_counting_trivial_twist": inclusive,
        "pairs_excluding_trivial_twist": exclusive,
        "verified_value_from_RUN_012": STATED["new_total_twist_pairs"],
        "rule": ("inclusive" if inclusive == STATED["new_total_twist_pairs"]
                 else "exclusive" if exclusive == STATED["new_total_twist_pairs"]
                 else "neither"),
        "calibrated": inclusive == STATED["new_total_twist_pairs"],
        "note": ("the rule is fixed by a number this tree already verified, not "
                 "chosen to make the old count come out right"),
    }


def decompose(old: dict, new: dict) -> dict:
    """Every term of §Q9, measured. Nothing here is back-solved."""
    O, N = set(old), set(new)
    dropped, added, common = O - N, N - O, O & N
    upstream_removed = sum(len(old[l]) for l in dropped)
    newbase_added = sum(len(new[l]) for l in added)
    stable_removed = stable_added = 0
    for l in common:
        a, b = set(old[l]), set(new[l])
        stable_removed += len(a - b)
        stable_added += len(b - a)
    old_total = sum(len(v) for v in old.values())
    new_total = sum(len(v) for v in new.values())
    measured = {"old_total_twist_pairs": old_total,
                "new_total_twist_pairs": new_total,
                "lhs": old_total - new_total,
                "upstream_removed": upstream_removed,
                "stable_removed": stable_removed,
                "stable_added": stable_added,
                "newbase_added": newbase_added,
                "rhs": upstream_removed + stable_removed
                       - stable_added - newbase_added}
    return {
        "labels": {"old": len(O), "new": len(N), "dropped": len(dropped),
                   "added": len(added), "common": len(common)},
        "measured": measured,
        "stated": STATED,
        "agreement": {k: measured[k] == STATED[k] for k in STATED},
        "all_agree": all(measured[k] == STATED[k] for k in STATED),
        "identity_holds": measured["lhs"] == measured["rhs"],
        "every_term_measured": True,
        "reading": ("RUN-028 could check the identity's arithmetic and four of "
                    "its six inputs. All six are measured here, so the identity "
                    "is a check rather than a definition of its last two terms"),
    }


def base_without_twists(old: dict) -> dict:
    """The 1,355 RUN-028 could not place.

    RUN-028's absent list carried `1355`, from a replay document saying a set of
    that size could not be rebuilt without re-running Algorithm 2. It is the
    base curves that have no entry in the twist artefact at all:
    40,749 − 39,394.
    """
    n = BASE_CURVES - len(old)
    return {"base_curves_RUN_004": BASE_CURVES,
            "labels_in_the_old_twist_artefact": len(old),
            "difference": n,
            "matches_the_1355_RUN_028_could_not_place": n == 1355,
            "reading": ("the twist artefact does not cover the whole census: "
                        f"{n:,} base labels have no twist entry, which is the "
                        "figure the replay document reports and RUN-028 listed "
                        "as having no counterpart here")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    old_oid, old = load("old")
    new_oid, new = load("new")
    cal = calibrate(new)
    dec = decompose(old, new)
    extra = base_without_twists(old)

    log = {
        "gate": "src31 — §Q9's twist accounting, measured from the artefacts",
        "provenance": {"branch": ARCHIVE, "old_blob": old_oid,
                       "new_blob": new_oid, "path": BASE},
        "calibration": cal,
        "decomposition": dec,
        "base_curves_without_twist_entries": extra,
        "closes": ["old_total_twist_pairs", "upstream_removed",
                   "the 1355 of RUN-028's absent list"],
        "ok": (cal["calibrated"] and dec["all_agree"] and dec["identity_holds"]
               and extra["matches_the_1355_RUN_028_could_not_place"]
               and dec["labels"]["new"] == KEPT_CURVES),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  artefacts from {ARCHIVE}")
    print(f"    old blob {old_oid[:12]}   new blob {new_oid[:12]}")
    print(f"  counting rule: inclusive gives {cal['pairs_counting_trivial_twist']:,}, "
          f"exclusive {cal['pairs_excluding_trivial_twist']:,}; RUN-012 verified "
          f"{cal['verified_value_from_RUN_012']:,} → {cal['rule']}")
    lb = dec["labels"]
    print(f"  labels: old {lb['old']:,}  new {lb['new']:,}  dropped "
          f"{lb['dropped']:,}  added {lb['added']:,}")
    print()
    for k in ("old_total_twist_pairs", "new_total_twist_pairs", "lhs",
              "upstream_removed", "stable_removed", "stable_added",
              "newbase_added", "rhs"):
        m, s = dec["measured"][k], STATED[k]
        print(f"    {k:22s} measured {m:>8,}   stated {s:>8,}   "
              f"{'agree' if m == s else 'DIFFERS'}")
    print(f"\n  identity holds: {dec['identity_holds']}   "
          f"every term measured: {dec['every_term_measured']}")
    print(f"  base labels with no twist entry: {extra['difference']:,} "
          f"({BASE_CURVES:,} − {lb['old']:,}) — matches RUN-028's unplaced "
          f"1,355: {extra['matches_the_1355_RUN_028_could_not_place']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
