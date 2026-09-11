"""Build the complete handoff bundle of the BSD verification line.

    python handoff/build_handoff.py            # builds handoff/build/<name>/ and handoff/<name>.zip

What goes in, and from where (nothing is retyped — every figure in the
manifest is read from a log, every file is copied byte for byte):

  amral-research-trees/bsd-verification-zhuiheng/   the tree at git HEAD (tracked files only, via `git ls-files`)
  amral/public/bsd/{phase0,p5,phase1,phase2}/files/  the 85 curated documents, from the site's public directory
  amral/public/bsd/stress-test/files/               the Witness line's stress-test audit incl. its Kurihara package
  census/<package>/                                 the Phase 1 census package the gates read (via code/census_pkg.py)
  research-packages/                                the 25 archived research packages + the RUGZPB v0.1 note, from amral/drops/BSD
  git/bsd-verification-zhuiheng.bundle              `git bundle create` of the branch
  HANDOFF.md                                        handoff/HANDOFF.md with the README's round table appended
  MANIFEST.json                                     commit, branch, date, counts, drill and sweep totals, SHA-256 of every file

Then a smoke test runs INSIDE the built copy with BSD_CENSUS_PKG pointed at
the bundle's own census — every one of the drill's checks must be green there
— and its logs are restored from the source tree before hashing, so the
manifest describes exactly what was copied.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
TREE = HERE.parent                                             # bsd-verification-zhuiheng
REPO = TREE.parent                                             # amral-research-trees
WORK = REPO.parent                                             # work together
AMRAL = WORK / "amral"
CENSUS_NAME = "BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12"
CENSUS_SRC = pathlib.Path("D:/我的研究/學術討論/論文/數學/BSD") / CENSUS_NAME
DROPS = AMRAL / "drops" / "BSD"
BRANCH = "agent/bsd-verification-zhuiheng"
TODAY = datetime.date.today().isoformat()
NAME = f"BSD-verification-handoff-{TODAY}"
BUILD = HERE / "build"
OUT = BUILD / NAME
ZIP = HERE / f"{NAME}.zip"


def sh(*cmd: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=True).stdout


def copy_tree_at_head() -> int:
    files = [f for f in sh("git", "ls-files", cwd=TREE).split("\n") if f]
    dst = OUT / "amral-research-trees" / "bsd-verification-zhuiheng"
    for rel in files:
        src = TREE / rel
        if not src.exists():
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    return len(files)


def copy_dir(src: pathlib.Path, dst: pathlib.Path, pattern: str | None = None) -> int:
    n = 0
    for p in sorted(src.rglob("*")):
        if p.is_dir():
            continue
        if pattern and not p.match(pattern):
            continue
        rel = p.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        n += 1
    return n


def git_bundle() -> pathlib.Path:
    (OUT / "git").mkdir(parents=True, exist_ok=True)
    b = OUT / "git" / "bsd-verification-zhuiheng.bundle"
    subprocess.run(["git", "bundle", "create", str(b), BRANCH], cwd=REPO, check=True,
                   capture_output=True)
    subprocess.run(["git", "bundle", "verify", str(b)], cwd=REPO, check=True, capture_output=True)
    return b


def smoke_test() -> dict:
    """Every drill check green, inside the copy, with the bundle's own census."""
    tree = OUT / "amral-research-trees" / "bsd-verification-zhuiheng"
    env = dict(os.environ, BSD_CENSUS_PKG=str(OUT / "census" / CENSUS_NAME), PYTHONIOENCODING="utf-8")
    code = ("import sys, time; sys.path.insert(0, 'code'); import src11_gate_drill as d; "
            "import census_pkg as c; t = time.time(); red = [n for n, fn in d.CHECKS.items() if not fn()]; "
            "print(__import__('json').dumps({'checks': len(d.CHECKS), 'red': red, "
            "'seconds': round(time.time() - t, 1), 'census_resolved_to': str(c.PKG)}))")
    out = subprocess.run([sys.executable, "-X", "utf8", "-c", code], cwd=tree, env=env,
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit("smoke test failed to run:\n" + out.stderr[-2000:])
    result = json.loads(out.stdout.strip().splitlines()[-1])
    sweep = subprocess.run([sys.executable, "-X", "utf8", "code/src29_sweep_coverage.py"], cwd=tree, env=env,
                           capture_output=True, text=True, encoding="utf-8")
    result["sweep_exit"] = sweep.returncode
    # restore the logs the smoke test rewrote, so the manifest hashes the source tree's bytes
    for rel in ("data/gate-logs/src29-sweep-coverage.json",):
        shutil.copy2(TREE / rel, tree / rel)
    shutil.rmtree(tree / "data" / "cache", ignore_errors=True)      # a derivable a_p cache, gitignored in the source
    return result


def manifest(counts: dict, smoke: dict) -> dict:
    drill = json.loads((TREE / "data" / "gate-logs" / "src11-gate-drill.json").read_text(encoding="utf-8"))
    sweep = json.loads((TREE / "data" / "gate-logs" / "src29-sweep-coverage.json").read_text(encoding="utf-8"))
    t = drill["totals"]
    files = {}
    total = 0
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            b = p.read_bytes()
            files[p.relative_to(OUT).as_posix()] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
            total += len(b)
    return {
        "bundle": NAME, "built": datetime.datetime.now().isoformat(timespec="seconds"),
        "line": "bsd-verification-zhuiheng", "arm": "數學戰士「墜衡」 / AMRAL Research Lab",
        "git": {"repository": "kakon77777-commits/amral-research-trees", "branch": BRANCH,
                "commit": sh("git", "rev-parse", "HEAD", cwd=TREE).strip(),
                "commit_subject": sh("git", "log", "-1", "--format=%s", cwd=TREE).strip(),
                "commits_on_branch": int(sh("git", "rev-list", "--count", BRANCH, cwd=REPO).strip())},
        "rounds": {"first": "RUN-001", "last": "RUN-069", "reports": counts["reports"], "gates": counts["gates"]},
        "drill": {"checks": len(drill["baseline_all_green"]), "defects": t["defects"],
                  "caught_by_named_check": t["defects"] - len(t["UNCAUGHT_BY_ANY_CHECK"]) - len(t["CAUGHT_BY_THE_WRONG_CHECK"]),
                  "uncaught": len(t["UNCAUGHT_BY_ANY_CHECK"]), "caught_by_wrong_check": len(t["CAUGHT_BY_THE_WRONG_CHECK"]),
                  "controls": t["controls"], "controls_disturbed": len(t["controls_that_disturbed_a_check"])},
        "sweep": {"documents": len(sweep["documents"]), "buckets": sweep["counts"], "per_subline": sweep["per_subline"]},
        "contents": counts,
        "smoke_test_inside_the_bundle": smoke,
        "python_used_to_build": sys.version.split()[0],
        "layout_note": "gates find the corpus at ../../amral/public/bsd relative to the tree and the census package via code/census_pkg.py (BSD_CENSUS_PKG, else the original path, else <bundle>/census/<package>)",
        "total_bytes": total, "file_count": len(files), "files": files,
    }


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    counts = {}
    counts["tree_files"] = copy_tree_at_head()
    counts["reports"] = len(list((TREE / "reports").glob("RUN-*.md")))
    counts["gates"] = len(list((TREE / "code").glob("src*.py")))
    n = 0
    for sub in ("phase0", "p5", "phase1", "phase2"):
        n += copy_dir(AMRAL / "public" / "bsd" / sub / "files", OUT / "amral" / "public" / "bsd" / sub / "files", "*.md")
    counts["corpus_documents"] = n
    counts["stress_test_files"] = copy_dir(AMRAL / "public" / "bsd" / "stress-test" / "files",
                                           OUT / "amral" / "public" / "bsd" / "stress-test" / "files")
    counts["census_files"] = copy_dir(CENSUS_SRC, OUT / "census" / CENSUS_NAME)
    counts["research_packages"] = copy_dir(DROPS, OUT / "research-packages")
    git_bundle()
    # HANDOFF.md + the README's round table
    readme = (TREE / "README.md").read_text(encoding="utf-8")
    i = readme.index("## Rounds")
    j = readme.index("## Layout", i)
    table = readme[i:j].replace("](./reports/", "](amral-research-trees/bsd-verification-zhuiheng/reports/")
    handoff = (HERE / "HANDOFF.md").read_text(encoding="utf-8")
    (OUT / "HANDOFF.md").write_text(handoff.rstrip("\n") + "\n\n" + table.rstrip("\n") + "\n", encoding="utf-8")
    smoke = smoke_test()
    if smoke["red"] or smoke["sweep_exit"] != 0:
        raise SystemExit(f"smoke test inside the bundle is not green: {smoke}")
    m = manifest(counts, smoke)
    (OUT / "MANIFEST.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                z.write(p, (pathlib.Path(NAME) / p.relative_to(OUT)).as_posix())
    print(json.dumps({k: v for k, v in m.items() if k != "files"}, indent=2, ensure_ascii=False))
    print(f"\nzip: {ZIP} ({ZIP.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
