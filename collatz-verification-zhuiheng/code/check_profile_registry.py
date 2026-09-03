"""Refuse if the profiles this tree implements and the registry disagree.

數學戰士「墜衡」 / AMRAL Research Lab.

The profile registry now lives in SEDB, at
`../../SEDB/projects/amral-results-profiles/`, because it governs every AMRAL
research line and had been living inside this one. What did NOT move is the
logic: whether a file satisfies a profile is decided by executable checks in
`validate_results_profiles.py`.

So there are two artifacts, and the only thing that keeps them one truth rather
than two copies is this check. Without it, a profile could be renamed in the
registry, or added in code, and nothing would notice — which is the second-truth
failure the move was meant to end, reintroduced by the move itself.

Three states, and the third is the one usually got wrong:

  agree     - the implemented set and the registered set match exactly
  disagree  - they do not; this exits non-zero and names the difference
  unmeasured - the registry is not reachable from here

`unmeasured` is NOT a pass. A check that cannot run has no verdict, and
reporting one would be worse than not checking at all. The mirror under
`data/external/` exists so the common case is measurable without SEDB
installed, and the mirror itself is compared against the live registry whenever
SEDB IS present.

Usage:  python code/check_profile_registry.py
"""

from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

import validate_results_profiles as V  # noqa: E402

MIRROR = ROOT / "data" / "external" / "results-profiles-registry.v1.json"
LIVE = (ROOT.parent.parent / "SEDB" / "projects" / "amral-results-profiles"
        / "results-profiles-registry.v1.json")
OUT = ROOT / "data" / "gate-logs" / "profile-registry-agreement.json"
MEASUREMENT = ROOT / "data" / "gate-logs" / "results-profiles.json"


def load(path: pathlib.Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:                             # noqa: BLE001
        return {"__unreadable__": str(exc)}


def compare(registry: dict) -> dict:
    """Differences between the registered profiles and the implemented ones."""
    registered = {p["key"] for p in registry.get("profiles", [])}
    implemented = set(V.PROFILES)
    return {
        "registered_not_implemented": sorted(registered - implemented),
        "implemented_not_registered": sorted(implemented - registered),
        "agree": registered == implemented,
        "count": len(registered),
    }


def compare_measurement(registry: dict, log: dict | None = None) -> dict:
    """Does the registry's satisfaction match this tree's own measurement?

    The registry is BUILT from that log, so drift means one of the two was
    regenerated without the other — a stale registry describing a state that
    no longer holds.

    `log` is a parameter so the drill can hand it a crafted one; it defaults to
    the archived measurement, which is what the real run compares against.
    """
    if log is None:
        log = load(MEASUREMENT)
    if not isinstance(log, dict) or "files" not in log:
        return {"comparable": False,
                "why": "no archived cross-branch measurement to compare against"}
    mine = {r["research_line_id"]: sorted(r["satisfies"])
            for r in log["files"] if r.get("research_line_id")}
    theirs = {l["research_line_id"]: sorted(l["satisfies"])
              for l in registry.get("lines", [])}
    drift = sorted(k for k in set(mine) | set(theirs) if mine.get(k) != theirs.get(k))
    return {"comparable": True, "lines_measured": sorted(mine),
            "lines_in_registry": sorted(theirs), "drifted": drift,
            "agree": not drift}


def main() -> int:
    try:
        # reconfigure, not a fresh TextIOWrapper: wrapping sys.stdout.buffer a
        # second time in one process closes the first wrapper and takes the
        # underlying buffer with it, so main() could not be called twice.
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):                 # pragma: no cover
        pass

    mirror, live = load(MIRROR), load(LIVE)
    result: dict = {
        "tool": "check_profile_registry.py",
        "registry_home": ("SEDB/projects/amral-results-profiles - the registry "
                          "governs every AMRAL line, so it does not live in "
                          "one line's tree"),
        "mirror_present": mirror is not None,
        "live_registry_present": live is not None,
    }

    source = live if isinstance(live, dict) and "profiles" in live else mirror
    if not isinstance(source, dict) or "profiles" not in source:
        result["state"] = "unmeasured"
        result["why"] = ("no readable registry: neither the mirror at "
                         f"{MIRROR.relative_to(ROOT)} nor the live export at "
                         f"{LIVE}. A check that cannot run has no verdict, so "
                         "this is not reported as agreement.")
        result["ok"] = False
    else:
        result["read_from"] = "live" if source is live else "mirror"
        result["profiles"] = compare(source)
        result["measurement"] = compare_measurement(source)
        # When both exist they must be identical: a mirror that has drifted
        # from the registry is a second truth wearing the word "mirror".
        if isinstance(live, dict) and isinstance(mirror, dict):
            result["mirror_matches_live"] = (live == mirror)
        else:
            result["mirror_matches_live"] = None
        result["state"] = "agree" if (
            result["profiles"]["agree"]
            and result["measurement"].get("agree", False)
            and result["mirror_matches_live"] is not False
        ) else "disagree"
        result["ok"] = result["state"] == "agree"

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("registry_home", "why")},
                     indent=2, ensure_ascii=False))
    if result.get("why"):
        print(result["why"])
    print(f"wrote {OUT.name}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
