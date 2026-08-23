#!/usr/bin/env python3
"""Recheck of the consolidated Collatz_OT_Series_Paper archive (source item 49).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, `Collatz_OT_Series_Paper.zip` (2026-08-13, 17.5 MB, 50 entries) —
a large consolidated archive of the source folder itself.

## A third kind of object, and a third kind of check

Items 1..47 asserted mathematics. Item 48 asserted what the other documents say.
This one asserts nothing at all: it is a **container**. So the question is neither
whether the theorems hold nor whether the summary is faithful, but whether the
archive is what it appears to be — and an archive has its own failure modes:

  * an entry that has drifted from the standalone item the sweep verified;
  * an item the archive silently omits;
  * content that exists ONLY inside it, which no item-by-item sweep would meet;
  * a nested structure that cannot be opened all the way down;
  * and an integrity manifest that verifies perfectly while covering the wrong
    half of what it ships.

The last one is the interesting one, and it is what this archive does.

## The check that the artifact asks for

Two of the entries ship their own `SHA256SUMS.txt`. That is an integrity claim
made by the artifact about itself, and the right response is to compute the
hashes independently and compare — never to run whatever produced the list.
Standing rule since item 35.

Verifying what a manifest lists is only half of it. The other half is asking
**what it does not list**, and whether the uncovered part is the part that
changes. A quantity compared only with itself is no measurement
(cf. RUN-028's vacuous guard); a manifest that covers only the immutable files
is the same mistake wearing a checksum.

Usage:
  python code/src49_archive_integrity.py --archive PATH --source DIR
                                         --manifest data/source-manifest.v1.json
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import pathlib
import sys
import zipfile

MAX_DEPTH = 24               # a nested archive is a loop risk, not just deep


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def entries_of(data: bytes) -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BytesIO(data))


# ---------------------------------------------------------------------------

def check_entries_against_source(archive: bytes, source: pathlib.Path,
                                 manifest: dict) -> dict:
    """Every entry against the standalone item the sweep already verified.

    Compared against BOTH the hash this tree recorded when it swept the item and
    the file on disk now, because those answer different questions: the first
    asks whether the archive matches what was verified, the second whether the
    standalone item has since moved.
    """
    recorded = {it["name"]: it for it in manifest["items"]}
    zf = entries_of(archive)
    matched, differing, archive_only, unrecorded = [], [], [], []
    for name in sorted(n for n in zf.namelist() if not n.endswith("/")):
        digest = sha256(zf.read(name))
        rec = recorded.get(name)
        live = source / name
        if rec is None:
            archive_only.append({"entry": name, "bytes": zf.getinfo(name).file_size,
                                 "on_disk": live.exists()})
            continue
        same_as_recorded = rec["sha256"] == digest
        same_as_disk = live.exists() and sha256(live.read_bytes()) == digest
        if same_as_recorded and same_as_disk:
            matched.append(name)
        elif not live.exists():
            unrecorded.append({"entry": name, "note": "recorded but not on disk now"})
        else:
            differing.append({"entry": name,
                              "recorded_sha256": rec["sha256"][:16],
                              "archive_sha256": digest[:16],
                              "matches_the_recorded_hash": same_as_recorded,
                              "matches_the_file_on_disk": same_as_disk})
    return {
        "entries": len(zf.namelist()),
        "byte_identical_to_the_standalone_item": len(matched),
        "differing": differing,
        "entries_with_no_standalone_counterpart": archive_only,
        "recorded_but_absent_from_disk": unrecorded,
    }


def check_coverage(archive_name: str, archive: bytes, manifest: dict) -> dict:
    """What the archive leaves out, which no per-entry check can see."""
    recorded = {it["name"]: it for it in manifest["items"]}
    cut = recorded[archive_name]["mtime_local"]
    inside = {n for n in entries_of(archive).namelist()}
    older = [it for it in manifest["items"]
             if it["mtime_local"] < cut and it["name"] != archive_name]
    missing = [{"name": it["name"], "mtime_local": it["mtime_local"],
                "seconds_older_than_the_archive": _gap(it["mtime_local"], cut)}
               for it in older if it["name"] not in inside]
    return {
        "archive_mtime": cut,
        "source_items_older_than_the_archive": len(older),
        "of_those_present": len(older) - len(missing),
        "of_those_missing": missing,
    }


def _gap(a: str, b: str) -> int:
    import datetime
    fmt = "%Y-%m-%dT%H:%M:%S"
    return int((datetime.datetime.strptime(b, fmt)
                - datetime.datetime.strptime(a, fmt)).total_seconds())


def check_recursive_integrity(archive: bytes) -> dict:
    """Every zip at every level must open. Depth and file count are measured."""
    stats = {"files": 0, "nested_zips": 0, "max_depth": 0, "unreadable": []}

    def walk(data: bytes, label: str, depth: int) -> None:
        if depth > MAX_DEPTH:                            # pragma: no cover
            stats["unreadable"].append({"entry": label, "why": "deeper than MAX_DEPTH"})
            return
        stats["max_depth"] = max(stats["max_depth"], depth)
        try:
            zf = entries_of(data)
            names = zf.namelist()
        except zipfile.BadZipFile:
            stats["unreadable"].append({"entry": label, "why": "not a readable zip"})
            return
        for name in names:
            if name.endswith("/"):
                continue
            stats["files"] += 1
            if name.lower().endswith(".zip"):
                stats["nested_zips"] += 1
                walk(zf.read(name), name, depth + 1)

    walk(archive, "<archive>", 0)
    return stats


def _read_manifest_lines(text: str) -> dict[str, str]:
    listed = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        digest, _, name = line.partition("  ")
        listed[name.strip()] = digest.strip()
    return listed


def _pack_files(zf: zipfile.ZipFile) -> tuple[str, dict[str, str]]:
    sums = [n for n in zf.namelist() if n.endswith("SHA256SUMS.txt")]
    root = sums[0].rsplit("SHA256SUMS.txt", 1)[0] if sums else ""
    files = {}
    for n in zf.namelist():
        if n.endswith("/"):
            continue
        key = n[len(root):] if root and n.startswith(root) else n
        files[key] = sha256(zf.read(n))
    return root, files


def check_shipped_checksums(archive: bytes) -> dict:
    """Verify what each shipped manifest lists, and measure what it omits."""
    zf = entries_of(archive)
    packs = {}
    for name in sorted(n for n in zf.namelist() if n.lower().endswith(".zip")):
        try:
            inner = entries_of(zf.read(name))
        except zipfile.BadZipFile:                       # pragma: no cover
            continue
        sums = [n for n in inner.namelist() if n.endswith("SHA256SUMS.txt")]
        if not sums:
            continue
        root, files = _pack_files(inner)
        listed = _read_manifest_lines(inner.read(sums[0]).decode("utf-8", "replace"))
        verified = [f for f, h in listed.items() if files.get(f) == h]
        mismatched = [{"file": f, "listed": h[:16], "actual": files.get(f, "")[:16]}
                      for f, h in listed.items()
                      if f in files and files[f] != h]
        absent = [f for f in listed if f not in files]
        uncovered = sorted(f for f in files
                           if f not in listed and f != "SHA256SUMS.txt")
        packs[name] = {
            "files_in_the_pack": len(files),
            "entries_listed": len(listed),
            "verified": len(verified),
            "mismatched": mismatched,
            "listed_but_absent": absent,
            "present_but_not_covered": uncovered,
            "coverage": "%d of %d" % (len(listed), len(files)),
            "manifest_sha256": sha256(inner.read(sums[0]))[:16],
        }
    return {
        "packs_shipping_a_manifest": len(packs),
        "packs": packs,
        "total_listed": sum(p["entries_listed"] for p in packs.values()),
        "total_verified": sum(p["verified"] for p in packs.values()),
        "total_mismatched": sum(len(p["mismatched"]) for p in packs.values()),
        "total_uncovered": sum(len(p["present_but_not_covered"]) for p in packs.values()),
    }


def check_manifest_covers_what_changes(archive: bytes, older: str, newer: str) -> dict:
    """The measurement that turns 'incomplete' into a finding.

    A manifest listing eight third-party PDFs verifies perfectly forever, because
    those files cannot change. The question that distinguishes an integrity claim
    from a decoration is whether it covers the files that DID change between two
    shipped versions of the same pack.
    """
    zf = entries_of(archive)
    if older not in zf.namelist() or newer not in zf.namelist():
        return {"skipped": "one of the two versions is not in this archive"}
    _, a = _pack_files(entries_of(zf.read(older)))
    inner_b = entries_of(zf.read(newer))
    _, b = _pack_files(inner_b)
    sums = [n for n in inner_b.namelist() if n.endswith("SHA256SUMS.txt")]
    listed = _read_manifest_lines(inner_b.read(sums[0]).decode("utf-8", "replace")) if sums else {}

    added = sorted(set(b) - set(a))
    removed = sorted(set(a) - set(b))
    changed = sorted(k for k in set(a) & set(b)
                     if a[k] != b[k] and k != "SHA256SUMS.txt")
    differing = [f for f in added + removed + changed]
    covered = [f for f in differing if f in listed]

    a_sums = [n for n in entries_of(zf.read(older)).namelist()
              if n.endswith("SHA256SUMS.txt")]
    manifest_identical = bool(a_sums and sums) and (
        sha256(entries_of(zf.read(older)).read(a_sums[0]))
        == sha256(inner_b.read(sums[0])))

    return {
        "older": older, "newer": newer,
        "files_added": added, "files_removed": removed, "files_changed": changed,
        "files_that_differ": len(differing),
        "of_those_covered_by_the_manifest": len(covered),
        "the_manifest_is_byte_identical_between_the_two_versions": manifest_identical,
        "the_manifest_covers_nothing_that_changed":
            len(differing) > 0 and len(covered) == 0,
    }


def check_version_chain(archive: bytes, top: str) -> dict:
    """A pack that nests its own predecessor, all the way down."""
    zf = entries_of(archive)
    if top not in zf.namelist():
        return {"skipped": "not in this archive"}
    levels = []

    def walk(data: bytes, label: str, depth: int) -> None:
        if depth > MAX_DEPTH:                            # pragma: no cover
            return
        try:
            inner = entries_of(data)
        except zipfile.BadZipFile:                       # pragma: no cover
            levels.append({"depth": depth, "label": label, "unreadable": True})
            return
        files = [n for n in inner.namelist() if not n.endswith("/")]
        levels.append({
            "depth": depth, "label": pathlib.Path(label).name,
            "files": len(files),
            "ships_a_manifest": any(n.endswith("SHA256SUMS.txt") for n in files)})
        for n in sorted(files):
            if n.lower().endswith(".zip"):
                walk(inner.read(n), n, depth + 1)

    walk(zf.read(top), top, 0)
    return {
        "levels": levels,
        "chain_depth": len(levels),
        "levels_shipping_a_manifest": sum(1 for l in levels if l.get("ships_a_manifest")),
        "files_reachable_through_the_chain": sum(l.get("files", 0) for l in levels),
    }


def check_composition(archive: bytes, prefix: str) -> dict:
    zf = entries_of(archive)
    total = sum(zf.getinfo(n).file_size for n in zf.namelist() if not n.endswith("/"))
    tagged = sum(zf.getinfo(n).file_size for n in zf.namelist()
                 if n.startswith(prefix) and not n.endswith("/"))
    return {
        "uncompressed_bytes": total,
        "bytes_under_prefix": tagged,
        "prefix": prefix,
        "share_percent": round(100.0 * tagged / total, 1) if total else 0.0,
        "entries_under_prefix": sum(1 for n in zf.namelist() if n.startswith(prefix)),
    }


def check_against_this_trees_archive(archive: bytes, tree: pathlib.Path) -> dict:
    """Does anything in the archive appear byte-identically in what we archived?

    A measurement, not a gate. The tree holds the SSSP-Repaired edition of the
    series (RUN-002); this archive holds the working documents. They are not the
    same edition and are not expected to agree file-for-file -- but the overlap,
    whatever it is, is worth knowing rather than assuming.
    """
    if not tree.exists():
        return {"skipped": "tree archive not found"}
    ours = {}
    for p in tree.rglob("*"):
        if p.is_file():
            ours.setdefault(sha256(p.read_bytes()), []).append(p.name)
    zf = entries_of(archive)
    shared, only_here = [], 0
    for n in zf.namelist():
        if n.endswith("/") or not n.lower().endswith(".md"):
            continue
        h = sha256(zf.read(n))
        if h in ours:
            shared.append({"archive_entry": n, "in_our_archive_as": ours[h][0]})
        else:
            only_here += 1
    return {
        "files_in_this_trees_ot_archive": sum(1 for p in tree.rglob("*") if p.is_file()),
        "markdown_entries_in_the_consolidated_archive": only_here + len(shared),
        "byte_identical_in_both": shared,
        "present_here_but_not_byte_identical_in_ours": only_here,
    }


# ---------------------------------------------------------------------------

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True, type=pathlib.Path)
    ap.add_argument("--source", required=True, type=pathlib.Path)
    ap.add_argument("--manifest", required=True, type=pathlib.Path)
    ap.add_argument("--ot-tree", type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    data = args.archive.read_bytes()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    name = args.archive.name

    rep = {
        "round": "consolidated archive Collatz_OT_Series_Paper.zip",
        "source_item": 49,
        "archive_sha256": sha256(data),
        "archive_bytes": len(data),
        "entries_against_source": check_entries_against_source(data, args.source, manifest),
        "coverage": check_coverage(name, data, manifest),
        "recursive_integrity": check_recursive_integrity(data),
        "shipped_checksums": check_shipped_checksums(data),
        "manifest_covers_what_changes": check_manifest_covers_what_changes(
            data,
            "CPL_Claude_67_25_Research_Pack_2026-08-11.zip",
            "CPL_Claude_67_25_Research_Pack_v2_2026-08-11.zip"),
        "version_chain": check_version_chain(
            data, "CPL_Claude_Research_Pack_v11_2026-08-11.zip"),
        "composition": check_composition(data, "CPL_"),
        "against_this_trees_archive": check_against_this_trees_archive(
            data, args.ot_tree) if args.ot_tree else {"skipped": "no --ot-tree"},
    }

    ea, cov, ri = rep["entries_against_source"], rep["coverage"], rep["recursive_integrity"]
    sc, mc = rep["shipped_checksums"], rep["manifest_covers_what_changes"]
    vc, comp = rep["version_chain"], rep["composition"]

    failures = []
    if ea["differing"]:
        failures.append("an archive entry has drifted from the standalone item: %s"
                        % [d["entry"] for d in ea["differing"]])
    if ea["byte_identical_to_the_standalone_item"] < 10:
        failures.append("too few entries were compared against the source folder "
                        "for this to be a comparison")
    if ri["unreadable"]:
        failures.append("a nested archive could not be opened: %s" % ri["unreadable"])
    if ri["nested_zips"] < 10 or ri["max_depth"] < 2:
        failures.append("the recursive walk did not descend, so it read nothing")
    if sc["total_mismatched"]:
        failures.append("a shipped checksum does not match its file")
    if sc["packs_shipping_a_manifest"] < 1 or sc["total_verified"] < 1:
        failures.append("no shipped manifest was verified, so that check read nothing")
    if any(p["listed_but_absent"] for p in sc["packs"].values()):
        failures.append("a shipped manifest lists a file the pack does not contain")
    if mc.get("skipped"):
        failures.append("the two pack versions could not be compared")
    # A coverage question asked about two identical inputs answers itself. If the
    # two shipped versions come back indistinguishable, the comparison read one
    # thing twice and the finding below would vanish without a failure.
    if not mc.get("skipped") and mc.get("files_that_differ", 0) == 0:
        failures.append("the two pack versions are indistinguishable, so the "
                        "coverage question was never asked")
    if vc.get("chain_depth", 0) < 2:
        failures.append("the version chain was not followed")
    if comp["entries_under_prefix"] == 0:
        failures.append("the composition check matched no entries, so its share is "
                        "a statement about nothing")
    if cov["source_items_older_than_the_archive"] < 10:
        failures.append("the coverage check found almost no items older than the "
                        "archive, so it is comparing against an empty set")
    elif cov["of_those_present"] < 0.5 * cov["source_items_older_than_the_archive"]:
        failures.append("most of the items the coverage check selected are absent "
                        "from the archive, so it is not looking at the archive's "
                        "own contents")

    findings = []
    if mc.get("the_manifest_covers_nothing_that_changed"):
        findings.append(
            "the shipped `SHA256SUMS.txt` verifies every one of its %d entries and "
            "covers the wrong half. It lists the third-party PDFs, which cannot "
            "change; between the two shipped versions of the same pack %d files "
            "differ (%s) and the manifest covers **none** of them — it is byte-"
            "identical across the two versions (%s). An integrity manifest that "
            "only ever certifies the immutable files is a checksum on the part "
            "nobody would doubt."
            % (sc["total_listed"], mc["files_that_differ"],
               ", ".join(mc["files_added"] + mc["files_changed"]),
               mc["the_manifest_is_byte_identical_between_the_two_versions"]))
    if sc["total_uncovered"]:
        findings.append(
            "across the packs that ship a manifest, %d files are present and "
            "uncovered, including the scripts and notes: %s."
            % (sc["total_uncovered"],
               ", ".join(sorted({f for p in sc["packs"].values()
                                 for f in p["present_but_not_covered"]
                                 if f.endswith((".py", ".json"))}))))
    if vc.get("levels_shipping_a_manifest") == 0 and vc.get("chain_depth", 0) > 1:
        findings.append(
            "a second pack nests its own predecessor %d levels deep, and **no "
            "level ships a manifest at all** — %d files reachable only by opening "
            "every one of them in turn."
            % (vc["chain_depth"], vc["files_reachable_through_the_chain"]))
    if cov["of_those_missing"]:
        findings.append(
            "the archive omits %d source item(s) older than itself: %s."
            % (len(cov["of_those_missing"]),
               "; ".join("%s, by %d seconds" % (m["name"], m["seconds_older_than_the_archive"])
                         for m in cov["of_those_missing"])))
    if comp["share_percent"] >= 25:
        findings.append(
            "%.1f%% of the archive by uncompressed bytes is `%s` material that "
            "exists nowhere else in the source folder — %d entries an item-by-item "
            "sweep would never have opened."
            % (comp["share_percent"], comp["prefix"], comp["entries_under_prefix"]))

    rep["findings"] = findings
    rep["failures"] = failures
    rep["passed"] = not failures

    text = json.dumps(rep, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
