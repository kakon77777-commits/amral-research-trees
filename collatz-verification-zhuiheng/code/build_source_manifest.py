"""Chronological manifest of Neo.K's Collatz source folder.

數學戰士「墜衡」 / AMRAL Research Lab.

Neo.K's instruction (2026-08-14): all new material lands in one folder, and it is
to be unpacked **one at a time, in chronological order**, deciding for each item
whether it is new or continues something earlier.

Sixty-four items is more than can be tracked in prose, and "which have I already
done" is exactly the sort of thing that goes wrong silently. So the manifest is
generated, not maintained by hand: it reads the folder, hashes every file, sorts
by modification time, classifies each item by its name, and marks what the
verification tree has already processed.

It **reads only**. It does not extract anything. Unpacking is a separate,
deliberate step, one item at a time.

Usage:  python code/build_source_manifest.py [--source PATH]
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import zipfile

DEFAULT_SOURCE = r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"
ROOT = pathlib.Path(__file__).resolve().parent.parent

# What this tree has already independently rechecked, and where.
PROCESSED = {
    "Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0.zip": (
        "archived as ../collatz-ot-series-neok/ and fully rechecked; "
        "see reports/RUN-002-OT-SERIES.md"
    ),
    "collatz_operation_translation_finite_verification_prototype.zip": (
        "item 03. archived byte-exact at "
        "../collatz-ot-series-neok/early-experiments/; all 58651 certificate rows "
        "rechecked by code/src03_finite_prototype_recheck.py, scaling cross-checked "
        "against the Rust engine"
    ),
    "Collatz_OT_Series_Paper_01_v0.1_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_02_v0.2_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_03_v0.3_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_04_v0.4_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_05_v0.5_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_06_v0.6_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_07_v0.7_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_08_v0.8_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_INDEX_v0.1.md": (
        "loose series index beside the bundles; confirmed byte-identical to the "
        "bundled copy by code/src05_provenance_chain_recheck.py"
    ),
    "Collatz_OT_Series_Paper_01_Reclassification_and_Calibration_v0.1.md": (
        "loose Paper 01 beside the bundles; confirmed byte-identical to the "
        "bundled copy by code/src05_provenance_chain_recheck.py"
    ),
    "Collatz_OT_Series_Paper_02_Local_Affine_Atlas_Finite_Word_v0.1.md": (
        "loose Paper 02 beside the bundles; confirmed byte-identical to the "
        "bundled copy by code/src05_provenance_chain_recheck.py"
    ),
    "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1_bundle.zip": (
        "item 17, the Hard-Zeta origin. Rechecked by "
        "code/src06_hardzeta_origin_recheck.py: Z_k(s) measured on [2, 2^32) with "
        "two-sided bounds, the L = 1 uniform route refuted, and the ROUTE MAP's "
        "missing monotonicity hypothesis reported; see reports/RUN-004-HARD-ZETA-ORIGIN.md"
    ),
    "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1.1.md": (
        "item 18. Rechecked with item 17: byte-identical to the SSSP package's "
        "archived HZ original, and the v0.1 -> v0.1.1 -> v0.1.2 chain counted — "
        "v0.1.1 fixed one of the two unrestricted unions, the E_k^C one survived"
    ),
    "collatz_ot_v3_threshold_benchmark.csv": (
        "archived byte-exact at ../collatz-ot-series-neok/early-experiments/; "
        "all 15 (k, domain) rows rechecked by code/src04_v3_threshold_recheck.py, "
        "each cross-checked against the Rust engine; prune ratios confirmed to be "
        "Paper 05's P_k = A_k/2^k, and the non-monotonicity in k reproduced from "
        "the closed form"
    ),
    "collatz_operation_translation_v3_threshold_bundle.zip": (
        "archived byte-exact at ../collatz-ot-series-neok/early-experiments/; "
        "rechecked with the benchmark by code/src04_v3_threshold_recheck.py"
    ),
    "dimension_aware_log_physics_stress_bundle.zip": (
        "item 02. archived byte-exact at "
        "../collatz-ot-series-neok/early-experiments/; rechecked by "
        "code/src02_log_physics_recheck.py. Not a Collatz item."
    ),
    "finite_collatz_additive_coordinate_mvp_bundle.zip": (
        "item 01. archived byte-exact at "
        "../collatz-ot-series-neok/early-experiments/; rechecked by "
        "code/src01_additive_coordinate_recheck.py"
    ),
}


def classify(name: str) -> dict:
    """Sort an item into the research line it belongs to, from its name alone."""
    n = name.lower()
    if "sssp_repaired" in n:
        return {"line": "nine-paper series", "role": "final repaired package"}
    if re.search(r"papers?_01[_-]0\d_v0\.\d_bundle", n) or "paper_01_v0.1_bundle" in n:
        return {"line": "nine-paper series", "role": "incremental bundle, superseded by SSSP v1.0"}
    if re.match(r"collatz_ot_series_paper_0\d", n) or "collatz_ot_series_index" in n:
        return {"line": "nine-paper series", "role": "loose manuscript or index"}
    if "faithful_global_quantifier_compression" in n:
        return {"line": "Hard-Zeta", "role": "proof-route origin"}
    if "hard_zeta_route_map" in n:
        return {"line": "Hard-Zeta", "role": "route map"}
    if "hard_zeta" in n and "handoff" in n:
        return {"line": "Hard-Zeta", "role": "handoff"}
    if "hard_zeta" in n and "a_line_complete" in n:
        return {"line": "Hard-Zeta", "role": "Phase I A-line consolidation"}
    if "hard_zeta_phase_i_" in n:
        return {"line": "Hard-Zeta", "role": "Phase I round"}
    if "hard_zeta_phase_ii_" in n:
        return {"line": "Hard-Zeta", "role": "Phase II round"}
    if "crypto_semiotics" in n:
        return {"line": "other project", "role": "not Collatz; parked here"}
    if "collatz_ot_series_paper.zip" == n:
        return {"line": "nine-paper series", "role": "large consolidated archive"}
    if any(t in n for t in ("mvp_bundle", "stress_bundle", "prototype", "threshold")):
        return {"line": "early experiments", "role": "prototype / benchmark"}
    return {"line": "unclassified", "role": "needs a look"}


def round_key(name: str):
    """Sort key for Hard-Zeta rounds, so AU2d2 lands before AU2d10."""
    m = re.search(r"round_([a-z]*)(\d+)([a-z]*)(\d*)", name.lower())
    if not m:
        return None
    a, b, c, d = m.groups()
    return (a, int(b), c, int(d) if d else -1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    args = ap.parse_args()
    src = pathlib.Path(args.source)
    if not src.is_dir():
        raise SystemExit(f"source folder not found: {src}")

    items = []
    for p in sorted((q for q in src.rglob("*") if q.is_file()),
                    key=lambda q: q.stat().st_mtime):
        st = p.stat()
        raw = p.read_bytes()
        entry = {
            "name": p.relative_to(src).as_posix(),
            "mtime_local": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(
                timespec="seconds"),
            "bytes": st.st_size,
            "sha256": hashlib.sha256(raw).hexdigest(),
            **classify(p.name),
            "processed_by_this_tree": PROCESSED.get(p.name),
        }
        rk = round_key(p.name)
        if rk:
            entry["round_sort_key"] = list(rk)
        if p.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(p) as z:
                    infos = [i for i in z.infolist() if not i.is_dir()]
                    entry["zip_entries"] = len(infos)
                    entry["zip_uncompressed_bytes"] = sum(i.file_size for i in infos)
                    entry["zip_top_level"] = sorted({i.filename.split("/")[0] for i in infos})[:6]
            except zipfile.BadZipFile:
                entry["zip_entries"] = "UNREADABLE"
        items.append(entry)

    lines: dict[str, int] = {}
    for it in items:
        lines[it["line"]] = lines.get(it["line"], 0) + 1

    manifest = {
        "tool": "build_source_manifest.py",
        "source_folder": str(src),
        "generated_from": "file modification times and names; nothing was extracted",
        "item_count": len(items),
        "total_bytes": sum(i["bytes"] for i in items),
        "earliest": items[0]["mtime_local"] if items else None,
        "latest": items[-1]["mtime_local"] if items else None,
        "items_per_line": lines,
        "processed_count": sum(1 for i in items if i["processed_by_this_tree"]),
        "items": items,
    }
    out = ROOT / "data" / "source-manifest.v1.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"{len(items)} items, {manifest['total_bytes']/2**20:.1f} MiB, "
          f"{manifest['earliest']} .. {manifest['latest']}")
    for line, count in sorted(lines.items(), key=lambda kv: -kv[1]):
        print(f"  {count:3d}  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
