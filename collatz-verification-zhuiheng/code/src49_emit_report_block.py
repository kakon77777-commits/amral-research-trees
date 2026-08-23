"""Emit RUN-031's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red. Every figure is held to a snapshot of what the
block actually reads by `report_block_guard` — the guard that replaced the one
shipped in src43..src45, which could not fail (RUN-028).

Usage:  python code/src49_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src49-archive.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src49-drill.json"
REPORT = ROOT / "reports" / "RUN-031-CONSOLIDATED-ARCHIVE-INTEGRITY.md"
FIGURES = ROOT / "data" / "gate-logs" / "src49-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src49_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    ea = g["entries_against_source"]
    cov = g["coverage"]
    ri = g["recursive_integrity"]
    sc = g["shipped_checksums"]
    mc = g["manifest_covers_what_changes"]
    vc = g["version_chain"]
    comp = g["composition"]
    ot = g["against_this_trees_archive"]

    out = [
        BEGIN, "",
        "**What the shipped manifests cover.** Each pack's own `SHA256SUMS.txt`, "
        "verified by recomputing the hashes rather than by running whatever "
        "produced the list:",
        "",
        "| pack | files | listed | verified | mismatched | uncovered |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name, p in sorted(sc["packs"].items()):
        out.append("| `%s` | `%d` | `%d` | `%d` | `%d` | `%d` |"
                   % (name.replace("CPL_Claude_", "").replace("_2026-08-11.zip", ""),
                      p["files_in_the_pack"], p["entries_listed"], p["verified"],
                      len(p["mismatched"]), len(p["present_but_not_covered"])))
    out += [
        "",
        "Both manifests share one sha256 (`%s`) — the pack was revised and the "
        "manifest was not. Between the two versions `%d` files differ (%s), and "
        "`%d` of them are covered."
        % (sorted({p["manifest_sha256"] for p in sc["packs"].values()})[0],
           mc["files_that_differ"],
           ", ".join("`%s`" % f for f in mc["files_added"] + mc["files_changed"]),
           mc["of_those_covered_by_the_manifest"]),
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]

    rows = [
        ("archive entries", "the top level of the container", ea["entries"]),
        ("…byte-identical to the standalone item the sweep verified",
         "the recorded hash **and** the file on disk",
         ea["byte_identical_to_the_standalone_item"]),
        ("…**that have drifted**", "must be zero", len(ea["differing"])),
        ("…with no standalone counterpart anywhere in the folder",
         "reachable only by opening this archive",
         len(ea["entries_with_no_standalone_counterpart"])),
        ("source items older than the archive",
         "of which present: %d" % cov["of_those_present"],
         cov["source_items_older_than_the_archive"]),
        ("…omitted", "named below if any", len(cov["of_those_missing"])),
        ("files reachable through every nesting level",
         "%d nested archives, deepest nesting %d"
         % (ri["nested_zips"], ri["max_depth"]), ri["files"]),
        ("…**that could not be opened**", "must be zero", len(ri["unreadable"])),
        ("shipped checksum entries verified",
         "of %d listed, across %d packs"
         % (sc["total_listed"], sc["packs_shipping_a_manifest"]),
         sc["total_verified"]),
        ("…**mismatched**", "must be zero", sc["total_mismatched"]),
        ("…files present but not covered by any manifest",
         "the scripts, notes and sources", sc["total_uncovered"]),
        ("version-chain depth", "each version nesting its predecessor",
         vc["chain_depth"]),
        ("…levels shipping a manifest", "of %d" % vc["chain_depth"],
         vc["levels_shipping_a_manifest"]),
        ("…files reachable only through that chain", "",
         vc["files_reachable_through_the_chain"]),
        ("share of the archive that is `%s` material" % comp["prefix"],
         "%d entries, %d of %d uncompressed bytes"
         % (comp["entries_under_prefix"], comp["bytes_under_prefix"],
            comp["uncompressed_bytes"]),
         "%s%%" % comp["share_percent"]),
        ("markdown entries byte-identical to this tree's own OT archive",
         "of %d, against %d archived files"
         % (ot["markdown_entries_in_the_consolidated_archive"],
            ot["files_in_this_trees_ot_archive"]),
         len(ot["byte_identical_in_both"])),
        ("defects planted / caught by the check named for each",
         "%d of the entries are robustness properties; %d malformed"
         % (d["counts"]["robustness_properties"], d["counts"]["malformed"]),
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out.append("")
    for m in cov["of_those_missing"]:
        out.append("**Omitted.** `%s`, written `%s` — `%d` seconds before the "
                   "archive was built."
                   % (m["name"], m["mtime_local"], m["seconds_older_than_the_archive"]))

    out += [
        "",
        "Every figure above is emitted by `code/src49_emit_report_block.py` from "
        "the gate logs. None is typed into this file.",
        "", END,
    ]
    return "\n".join(out)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (GATE_LOG, DRILL_LOG):
        if not path.exists():
            print(json.dumps({"error": "missing log", "path": str(path)}, indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))

    if not g.get("passed"):
        print(json.dumps({"error": "the recheck is red", "failures": g.get("failures")},
                         indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red; a report built on checks that "
                                   "cannot fail is worse than no report",
                          "counts": d.get("counts")}, indent=2, ensure_ascii=False))
        return 2

    guard = check_against_snapshot(build, [g, d], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to; "
                                   "a figure that stopped moving with its log "
                                   "is a figure somebody typed",
                          "guard": guard}, indent=2))
        return 2

    block = build(g, d)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "no generated-block markers"}, indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src49_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src49_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
