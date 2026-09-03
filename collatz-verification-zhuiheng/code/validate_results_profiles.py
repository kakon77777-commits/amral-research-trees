"""What a consumer of a results file can actually rely on, measured per file.

數學戰士「墜衡」 / AMRAL Research Lab.

`schema_version: 1` does not identify a shape. Two files in this monorepo
declare it and share six keys; everything after that diverges, and one of them
has no `verified_claims` or `explicit_non_claims` at all. A renderer that
dispatches on the version integer will break on one of them.

Rather than renumber — which would need every line to move at once, and this
tree does not edit another line's provenance — this script measures each file
against named PROFILES and reports which ones it satisfies. Profiles are
INFERRED from content, so a file needs no change, and no other tree needs to
be touched, for its capabilities to be described correctly.

  results-envelope/1  the six keys both existing files already agree on
  results-claims/1    envelope, plus structured verified_claims and
                      explicit_non_claims — what a claim-box UI needs
  results-pairs/1     envelope, plus render_pairs: the figures this line says
                      must never be shown without the number that gives them
                      meaning. "1441 defects caught" reads identically whether
                      1441 or 2000 were planted; which of the two is
                      load-bearing is a fact about the line, not something a
                      renderer can infer.
  results-figures/1   envelope, plus headline_figures: which of this line's
                      numbers are its own headlines and under what label, so a
                      renderer need understand no line's internal structure.
                      Nothing declared here may also belong to a pair, and
                      each declares its kind: a plain number, or a range that
                      resolves to exactly two numbers shown together.

Not satisfying a profile is not an error. It tells a renderer which branch to
take: a line outside `results-claims/1` still states its boundaries, in
`global_status.statement` and its report prose, and must still be rendered
with them. The only hard failure is a file that DECLARES a profile in a
`profiles` field and then does not satisfy it.

Files are enumerated from git across every branch rather than from a list
typed here, because a list typed here is the thing that goes stale.

Usage:
  python code/validate_results_profiles.py                 # every branch
  python code/validate_results_profiles.py --paths a.json  # explicit files
"""

from __future__ import annotations

import argparse
import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
OUT = ROOT / "data" / "gate-logs" / "results-profiles.json"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout


def discover() -> list[tuple[str, str]]:
    """(ref, path) for every results.v*.json in the repository, any branch.

    Enumerated, not listed. A branch added later is picked up without editing
    this file, which is the whole point.
    """
    refs = []
    for line in _git("branch", "-a", "--format=%(refname:short)").splitlines():
        ref = line.strip()
        if ref and "HEAD" not in ref:
            refs.append(ref)
    found: set[tuple[str, str]] = set()
    for ref in refs:
        for path in _git("ls-tree", "-r", "--name-only", ref).splitlines():
            p = path.strip()
            if p.endswith(".json") and "/data/results.v" in p:
                found.add((ref, p))
    # one row per path: prefer a remote ref so the result is reproducible
    best: dict[str, str] = {}
    for ref, path in sorted(found):
        if path not in best or (not best[path].startswith("origin/")
                                and ref.startswith("origin/")):
            best[path] = ref
    return sorted((r, p) for p, r in best.items())


def _obj(doc: dict, key: str) -> dict:
    v = doc.get(key)
    return v if isinstance(v, dict) else {}


def check_envelope(doc: dict) -> list[str]:
    """Missing requirements for results-envelope/1, empty if satisfied."""
    missing = []
    if not isinstance(doc.get("schema_version"), int):
        missing.append("schema_version must be an integer")
    for key in ("research_line_id", "date"):
        if not isinstance(doc.get(key), str) or not doc.get(key):
            missing.append(f"{key} must be a non-empty string")
    if not _obj(doc, "researcher").get("display_name"):
        missing.append("researcher.display_name is required")
    if not _obj(doc, "problem").get("id"):
        missing.append("problem.id is required")
    gs = _obj(doc, "global_status")
    if not isinstance(gs.get("solved"), bool):
        missing.append("global_status.solved must be a boolean")
    if not isinstance(gs.get("statement"), str) or not gs.get("statement"):
        missing.append("global_status.statement must be a non-empty string")
    return missing


def check_claims(doc: dict) -> list[str]:
    """Missing requirements for results-claims/1, beyond the envelope."""
    missing = []
    vc = doc.get("verified_claims")
    if not isinstance(vc, list) or not vc:
        missing.append("verified_claims must be a non-empty array")
    else:
        for i, c in enumerate(vc):
            if not isinstance(c, dict) or not c.get("id") or not c.get("claim"):
                missing.append(f"verified_claims[{i}] needs both id and claim")
    nc = doc.get("explicit_non_claims")
    if not isinstance(nc, list) or not nc:
        missing.append("explicit_non_claims must be a non-empty array")
    elif not all(isinstance(s, str) and s for s in nc):
        missing.append("every explicit_non_claims entry must be a non-empty string")
    return missing


def _resolve(doc: dict, dotted: str):
    cur = doc
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def check_pairs(doc: dict) -> list[str]:
    """Missing requirements for results-pairs/1, beyond the envelope.

    A figure like "1441 defects caught" reads identically whether 1441 or 2000
    were planted. Which of two numbers is load-bearing is a fact about the
    line, not something a renderer can infer, so a line that wants that
    protection declares its pairs and a renderer refuses to show one alone.
    """
    missing = []
    pairs = doc.get("render_pairs")
    if not isinstance(pairs, list) or not pairs:
        missing.append("render_pairs must be a non-empty array")
        return missing
    for i, p in enumerate(pairs):
        if not isinstance(p, dict):
            missing.append(f"render_pairs[{i}] must be an object")
            continue
        for side in ("value", "against"):
            path = p.get(side)
            if not isinstance(path, str) or not path:
                missing.append(f"render_pairs[{i}].{side} must be a dotted path")
                continue
            got = _resolve(doc, path)
            if got is None:
                missing.append(f"render_pairs[{i}].{side} does not resolve: {path}")
            elif isinstance(got, bool) or not isinstance(got, (int, float)):
                missing.append(f"render_pairs[{i}].{side} is not a number: {path}")
        if not p.get("why"):
            missing.append(f"render_pairs[{i}] needs a why: a pair with no stated "
                           "reason cannot be reviewed")
    return missing


def check_figures(doc: dict) -> list[str]:
    """Missing requirements for results-figures/1, beyond the envelope.

    A renderer that has to guess which fields are a line's headline numbers
    ends up hardcoding one line's shape. That is not hypothetical: the
    verification sub-site knew `paper_sweep.*` and `coverage.*`, so the second
    line to arrive rendered its entire body of work as two empty section
    headings. A line says which figures are its own headlines, and a renderer
    needs to understand no line's internal structure.
    """
    missing = []
    figs = doc.get("headline_figures")
    if not isinstance(figs, list) or not figs:
        missing.append("headline_figures must be a non-empty array")
        return missing
    pairs = doc.get("render_pairs")
    claimed = set()
    if isinstance(pairs, list):
        for p in pairs:
            if isinstance(p, dict):
                claimed |= {p.get("value"), p.get("against")}
    for i, f in enumerate(figs):
        if not isinstance(f, dict):
            missing.append(f"headline_figures[{i}] must be an object")
            continue
        path = f.get("path")
        if not isinstance(path, str) or not path:
            missing.append(f"headline_figures[{i}].path must be a dotted path")
        else:
            if path in claimed:
                missing.append(
                    f"headline_figures[{i}] {path} is also part of a render "
                    "pair; showing it alone is the defect the pair prevents")
            got = _resolve(doc, path)
            kind = f.get("kind", "number")
            num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
            if got is None:
                missing.append(f"headline_figures[{i}].path does not resolve: {path}")
            elif kind == "number":
                if not num(got):
                    missing.append(f"headline_figures[{i}] is declared a number "
                                   f"and is not: {path}")
            elif kind == "range":
                if (not isinstance(got, list) or len(got) != 2
                        or not all(num(x) for x in got)):
                    missing.append(f"headline_figures[{i}] is declared a range "
                                   f"and must resolve to exactly two numbers: "
                                   f"{path}")
            else:
                missing.append(f"headline_figures[{i}] has an unknown kind "
                               f"{kind!r}; a renderer cannot guess how to draw it")
        if not f.get("label"):
            missing.append(f"headline_figures[{i}] needs a label: a bare number "
                           "under no heading is not a figure")
    return missing


PROFILES = {
    "results-envelope/1": check_envelope,
    "results-claims/1": check_claims,
    "results-pairs/1": check_pairs,
    "results-figures/1": check_figures,
}
# a profile is only reachable once its prerequisite holds
REQUIRES = {"results-claims/1": "results-envelope/1",
            "results-pairs/1": "results-envelope/1",
            "results-figures/1": "results-envelope/1"}


def why_not_archivable(rows: list[dict], explicit_paths: bool) -> str | None:
    """Reason this run must not overwrite the archived log, or None.

    Learned the expensive way, twice. Running with `--paths` to check one file
    replaced the canonical cross-branch measurement with a one-file one — and
    the second time the one file was a throwaway under a temp directory, so the
    archived gate log briefly cited `.../scratchpad/dryrun/...` as this tree's
    evidence. Neither run said anything was wrong, because nothing was: the
    measurement was accurate about the file it was given.

    An ad-hoc query and the archived measurement are different artifacts. The
    second condition is the load-bearing one: it refuses on the SHAPE of what
    was measured rather than on which flag was passed, so a future code path
    that reaches here another way is refused too.
    """
    if explicit_paths:
        return ("run with --paths: an ad-hoc query over chosen files is not "
                "the cross-branch measurement this log records")
    stray = [r["path"] for r in rows if not r.get("ref")]
    if stray:
        return (f"measured files not read from a git ref: {stray}. The archived "
                "log must cite what a consumer cloning this repository "
                "receives, never a path on one machine")
    return None


def evaluate(doc: dict) -> dict:
    satisfied, gaps = [], {}
    for name, check in PROFILES.items():
        need = REQUIRES.get(name)
        if need and need not in satisfied:
            gaps[name] = [f"requires {need}, which is not satisfied"]
            continue
        missing = check(doc)
        if missing:
            gaps[name] = missing
        else:
            satisfied.append(name)
    declared = doc.get("profiles")
    declared = declared if isinstance(declared, list) else []
    broken = [p for p in declared if p not in satisfied]
    return {
        "satisfies": satisfied,
        "gaps": gaps,
        "declared": declared,
        "declared_but_not_satisfied": broken,
        "renders_claim_box_from": ("verified_claims + explicit_non_claims"
                                   if "results-claims/1" in satisfied
                                   else "global_status.statement and report prose"),
        "headline_figures_to_render": [
            {"path": f.get("path"), "label": f.get("label"),
             "kind": f.get("kind", "number")}
            for f in (doc.get("headline_figures") or [])
            if isinstance(f, dict)
        ] if "results-figures/1" in satisfied else [],
        "figures_that_must_not_be_shown_alone": [
            {"value": p.get("value"), "against": p.get("against"),
             "label": p.get("label")}
            for p in (doc.get("render_pairs") or [])
            if isinstance(p, dict)
        ] if "results-pairs/1" in satisfied else [],
    }


def main() -> int:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    except (AttributeError, ValueError):                 # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", default=None,
                    help="explicit files instead of scanning the repository")
    args = ap.parse_args()

    rows = []
    if args.paths:
        sources = [(None, p) for p in args.paths]
    else:
        sources = discover()

    for ref, path in sources:
        try:
            raw = (pathlib.Path(path).read_text(encoding="utf-8") if ref is None
                   else _git("show", f"{ref}:{path}"))
            doc = json.loads(raw)
        except Exception as exc:                         # noqa: BLE001
            rows.append({"ref": ref, "path": path, "unreadable": str(exc)})
            continue
        row = {"ref": ref, "path": path,
               "research_line_id": doc.get("research_line_id"),
               "declared_schema_version": doc.get("schema_version")}
        row.update(evaluate(doc))
        rows.append(row)

    unreadable = [r for r in rows if "unreadable" in r]
    lying = [r for r in rows if r.get("declared_but_not_satisfied")]
    log = {
        "tool": "validate_results_profiles.py",
        "what_it_measures": (
            "which named profile each results file satisfies, inferred from "
            "content, so no file and no other line's tree needs to change"),
        "profiles": {
            "results-envelope/1": "the six keys every existing file agrees on",
            "results-claims/1": ("envelope plus structured verified_claims and "
                                 "explicit_non_claims"),
            "results-pairs/1": ("envelope plus render_pairs: the figures this "
                                "line says must never be shown without the "
                                "number that gives them meaning"),
            "results-figures/1": ("envelope plus headline_figures: which of "
                                  "this line's numbers are its own headlines, "
                                  "and under what label, so a renderer need "
                                  "understand no line's internal structure"),
        },
        "not_an_error": (
            "failing a profile a file never declared is information for a "
            "renderer, not a defect: that line states its boundaries elsewhere "
            "and must still be rendered with them"),
        "files": rows,
        "counts": {
            "files": len(rows),
            "unreadable": len(unreadable),
            "satisfying_envelope": sum(1 for r in rows
                                       if "results-envelope/1" in r.get("satisfies", [])),
            "satisfying_claims": sum(1 for r in rows
                                     if "results-claims/1" in r.get("satisfies", [])),
            "satisfying_pairs": sum(1 for r in rows
                                    if "results-pairs/1" in r.get("satisfies", [])),
            "satisfying_figures": sum(1 for r in rows
                                      if "results-figures/1" in r.get("satisfies", [])),
            "declared_but_not_satisfied": len(lying),
        },
        "ok": not unreadable and not lying,
    }
    archive_refusal = why_not_archivable(rows, bool(args.paths))
    if archive_refusal is None:
        OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8", newline="\n")
    else:
        log["not_archived"] = archive_refusal

    for r in rows:
        if "unreadable" in r:
            print(f"  UNREADABLE  {r['path']}  {r['unreadable']}")
            continue
        print(f"  {r['research_line_id']}")
        print(f"    {r['ref'] or 'working tree'}:{r['path']}")
        print(f"    declares schema_version {r['declared_schema_version']}, "
              f"satisfies {r['satisfies'] or ['(none)']}")
        for name, missing in r["gaps"].items():
            print(f"    misses {name}: {'; '.join(missing)}")
        print(f"    claim-box source: {r['renders_claim_box_from']}")
    print(json.dumps(log["counts"], indent=2))
    if archive_refusal is None:
        print(f"wrote {OUT}")
    else:
        print(f"NOT archived to {OUT.name} - {archive_refusal}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
