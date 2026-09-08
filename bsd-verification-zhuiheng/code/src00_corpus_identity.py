"""Gate 00 — does the curated corpus match the archived original, byte for byte?

數學戰士「墜衡」 / AMRAL Research Lab.

The BSD line exists in four places and the site makes a claim about the
relationship between two of them. `amral.evemisslab.com/bsd/` closes with

    SHA-256 逐篇核驗 · 原始位元組，不重新打包
    (per-document SHA-256 verification · original bytes, not repackaged)

That is a checkable claim, and nothing downstream is worth checking until it
holds: every later round reads a curated document and reasons about it as
though it were the archived original.

WHAT THIS COMPARES.

  curated : work together/amral/public/bsd/{phase0,p5,phase1,phase2}/files/*.md
            the 85 documents the public site serves
  archived: amral-research-trees, branch agent/bsd, bsd/**/*.md
            the .md inside the 25 packages mirrored from the drop zone on
            2026-08-14, byte-exact from Neo's own research run

Matching is by CONTENT HASH, never by filename: the curated copies were renamed
with ordering prefixes (`29_Theorem_Note_v1.0.md` for
`BSD_696e1_Theorem_Note_v1.0_2026-08-13/...`), so a name comparison would report
a mismatch that is only a rename, and — worse — could report a match between two
different documents that happen to share a name across packages.

WHAT A FINDING HERE WOULD MEAN. A curated document with no archived twin is not
necessarily wrong; it may be a curation artifact (an index written for the site).
But it is a document the site presents as research whose original this arm cannot
reach, and every later round that reads it is reading an unwitnessed copy. That
distinction is reported, not smoothed over.

Usage:  python code/src00_corpus_identity.py
"""

from __future__ import annotations

import hashlib
import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
CURATED = REPO.parent / "amral" / "public" / "bsd"
SUBLINES = ("phase0", "p5", "phase1", "phase2")
ARCHIVE_REF = "origin/agent/bsd"
OUT = ROOT / "data" / "gate-logs" / "src00-corpus-identity.json"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def curated_docs() -> list[dict]:
    rows = []
    for sub in SUBLINES:
        d = CURATED / sub / "files"
        if not d.is_dir():
            raise SystemExit(f"curated corpus not found: {d}")
        for m in sorted(d.glob("*.md")):
            raw = m.read_bytes()
            rows.append({"subline": sub, "name": m.name,
                         "bytes": len(raw), "sha256": sha256_bytes(raw)})
    return rows


def archived_docs() -> list[dict]:
    """Every .md under bsd/ on the archive branch, hashed from its blob.

    Read through `git cat-file --batch` in one process rather than one `git
    show` per file: 292 subprocesses is not merely slow, it is 292 chances for
    a partial read to look like an absent document.
    """
    listing = subprocess.run(
        ["git", "ls-tree", "-r", ARCHIVE_REF, "bsd/"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8").stdout
    entries = []
    for line in listing.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t", 1)
        _mode, kind, blob = meta.split()
        if kind == "blob" and path.endswith(".md"):
            entries.append((blob, path))
    if not entries:
        raise SystemExit(
            f"no .md found on {ARCHIVE_REF}. Fetch the branch first; an empty "
            "archive side would report every curated document as unwitnessed.")

    # Encoded, because text=False: handing a str to a binary pipe does not fail
    # loudly here, it stalls — the first run of this gate hung past two minutes
    # rather than raising.
    query = ("\n".join(b for b, _ in entries) + "\n").encode("ascii")
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO,
                          input=query, capture_output=True, text=False)
    rows, buf = [], proc.stdout
    pos = 0
    for blob, path in entries:
        nl = buf.index(b"\n", pos)
        header = buf[pos:nl].decode("ascii")
        size = int(header.split()[2])
        body = buf[nl + 1:nl + 1 + size]
        pos = nl + 1 + size + 1                      # trailing newline
        rows.append({"path": path, "package": path.split("/")[1],
                     "bytes": size, "sha256": sha256_bytes(body)})
    return rows


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    cur = curated_docs()
    arc = archived_docs()

    by_hash: dict[str, list[dict]] = {}
    for a in arc:
        by_hash.setdefault(a["sha256"], []).append(a)

    matched, unwitnessed = [], []
    for c in cur:
        twins = by_hash.get(c["sha256"], [])
        if twins:
            matched.append({**c, "archived_as": [t["path"] for t in twins],
                            "renamed": all(
                                pathlib.PurePosixPath(t["path"]).name != c["name"]
                                for t in twins)})
        else:
            unwitnessed.append(c)

    curated_hashes = {c["sha256"] for c in cur}
    not_curated = [a for a in arc if a["sha256"] not in curated_hashes]

    renamed = [m for m in matched if m["renamed"]]
    log = {
        "gate": "src00_corpus_identity",
        "question": ("does every curated BSD document exist byte-identically in "
                     "the archived research packages?"),
        "matched_by": "content sha256, never filename",
        "why_not_filename": (
            "curated copies carry ordering prefixes the originals do not, so a "
            "name comparison would report renames as mismatches and could match "
            "two different documents sharing a name across packages"),
        "counts": {
            "curated_documents": len(cur),
            "archived_md": len(arc),
            "matched_byte_identical": len(matched),
            "matched_but_renamed": len(renamed),
            "curated_without_an_archived_original": len(unwitnessed),
            "archived_not_curated": len(not_curated),
        },
        "curated_without_an_archived_original": unwitnessed,
        "matched_but_renamed": [
            {"curated": m["name"], "subline": m["subline"],
             "archived_as": m["archived_as"]} for m in renamed],
        "per_subline": {
            sub: {
                "curated": sum(1 for c in cur if c["subline"] == sub),
                "witnessed": sum(1 for m in matched if m["subline"] == sub),
            } for sub in SUBLINES
        },
        "not_a_defect": (
            "an archived document that is not curated is expected: the site "
            "presents a selected reading path, and the packages also carry "
            "READMEs, handoffs and intermediate notes. Only the other direction "
            "is a finding."),
        "ok": len(unwitnessed) == 0,
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print(json.dumps(log["counts"], indent=2, ensure_ascii=False))
    print()
    for sub in SUBLINES:
        s = log["per_subline"][sub]
        print(f"  {sub:<8} {s['witnessed']:>3} of {s['curated']:>3} witnessed")
    if unwitnessed:
        print()
        print("  curated documents with no archived original:")
        for u in unwitnessed:
            print(f"    {u['subline']}/{u['name']}  ({u['bytes']} bytes)")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
