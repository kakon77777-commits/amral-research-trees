"""Gate 64 — `02`'s adversarial regression corpus, run against this line's own 8b instrument; and the ecdata pin that only reproduces as CRLF.

數學戰士「墜衡」 / AMRAL Research Lab.

`02_Official_Discrepancy_Corpus` names four curves — 62a1, 66b1, 105a1, 141c1 —
that pass semistability, isogeny exclusion, ramification, optimality, rank zero
and the BSD(E,2) gate, and are rejected by CURRENT Algorithm 1 on four counts,
one of which is that `f'(x_0)` IS A RATIONAL SQUARE. It calls the four a
"theorem-router adversarial regression corpus" and says that any version which
suddenly accepts them should be labelled REGRESSION?, not NEW BSD BREAKTHROUGH!.

RUN-055 computed exactly that condition — `f'(x_0)` non-square — on all 3,747
CLZ20 curves of the accepted base and found zero squares. A check that has only
ever seen passing data has not been tested; RUN-042 said so about Kodaira
types, RUN-053 about a hypothesis. Here are four curves the corpus says MUST
fail. They are not in the base (they were rejected before it), so the instrument
had never seen them.

THE INSTRUMENT PASSES ITS NEGATIVE CONTROL: on the a-invariants read from the
pinned ecdata shard, each of the four has exactly one rational 2-torsion point
and `f'(x_0)` is a perfect square — 64, 64, 16, 144 — 4 of 4, as `02` states.
Three of the four a-invariant lists the first draft typed from memory were
WRONG; the shard is the source, and the drill holds the gate to it.

AND THE SHARD'S PIN ONLY REPRODUCES AS CRLF. The package records
`allcurves/allcurves.00000-09999` at 2,211,088 bytes, SHA-256 8a6073c4…; the
blob at the pinned commit is 2,146,401 bytes, SHA-256 259f3846… — 64,687 bytes
short, one per line. CRLF-converted, it hashes to the package's value exactly.
So the census hashed a Windows checkout of ecdata, though its PROVENANCE.md
says the twist JSONs were pulled with `git cat-file blob` to avoid precisely
this. The content is identical modulo line endings; the arithmetic is
unaffected; the pin, as recorded, does not verify against upstream without
knowing to convert.

Usage:  python code/src64_discrepancy_corpus.py
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
SHARD = EXT / "ecdata-25cec5e-allcurves.00000-09999"
SHARD_PROV = EXT / "ecdata-25cec5e-allcurves.00000-09999.provenance.json"
OUT = LOGS / "src64-discrepancy-corpus.json"

FOUR = ("62a1", "66b1", "105a1", "141c1")
PACKAGE_SHA = "8a6073c4703da0c39242e68b4af92d9d897d7e894e618c8ff6e2b010b39d57ad"
PACKAGE_BYTES = 2211088


def shard_pin() -> dict:
    b = SHARD.read_bytes() if SHARD.exists() else b""
    lf = hashlib.sha256(b).hexdigest()
    crlf_b = b.replace(b"\n", b"\r\n")
    crlf = hashlib.sha256(crlf_b).hexdigest()
    prov = json.loads(SHARD_PROV.read_text(encoding="utf-8")) if SHARD_PROV.exists() else {}
    return {"shard_present": bool(b), "bytes_lf": len(b), "sha256_lf": lf,
            "bytes_crlf": len(crlf_b), "sha256_crlf": crlf,
            "package_bytes": PACKAGE_BYTES, "package_sha256": PACKAGE_SHA,
            "lf_matches_package": lf == PACKAGE_SHA,
            "crlf_matches_package": crlf == PACKAGE_SHA,
            "line_count": b.count(b"\n"),
            "byte_gap_equals_line_count": (PACKAGE_BYTES - len(b)) == b.count(b"\n"),
            "provenance_record": prov.get("source"),
            "reading": ("the package hashed a CRLF checkout of ecdata. The "
                        "content is the upstream blob's; the recorded pin is "
                        "not the blob's hash")}


def read_curve(label: str) -> list[int] | None:
    """`62a1` -> the a-invariants on the `62 a 1` line of the shard."""
    n = "".join(ch for ch in label if ch.isdigit() or ch == "")  # conductor digits then class+num
    # split label into conductor, class letters, number
    i = 0
    while i < len(label) and label[i].isdigit():
        i += 1
    cond, rest = label[:i], label[i:]
    j = 0
    while j < len(rest) and rest[j].isalpha():
        j += 1
    cls, num = rest[:j], rest[j:]
    prefix = f"{cond} {cls} {num} "
    for line in SHARD.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return json.loads(line.split(" ")[3])
    return None


def the_four(base: list[dict]) -> dict:
    labels = {r["curve_label"] for r in base}
    rows = []
    for lab in FOUR:
        a = read_curve(lab)
        if a is None:
            rows.append({"curve": lab, "found_in_shard": False})
            continue
        t = cmap.rational_two_torsion_x(a)
        c0, c1, c2, _ = cmap.two_division_cubic(a)
        _b2, _b4, _b6, _b8, disc = cmap.anchor.b_invariants(a)
        roots = t["exact_integer_roots"]
        r = {"curve": lab, "found_in_shard": True, "ainvs": a,
             "in_the_40749_base": lab in labels,
             "rational_two_torsion_roots": roots,
             "exactly_one_root": len(roots) == 1}
        if roots:
            X0 = roots[0]
            gp = 3 * X0 * X0 + 2 * c2 * X0 + c1          # 4·f'(x0): same square class
            r.update({"X0": X0, "four_f_prime": gp,
                      "f_prime_is_a_square": cmap.is_square(gp),
                      "minus_f_prime_is_a_square": cmap.is_square(-gp),
                      "minus_disc_is_a_square": cmap.is_square(-disc)})
        rows.append(r)
    return {"rows": rows,
            "all_found": all(r["found_in_shard"] for r in rows),
            "none_in_base": all(not r.get("in_the_40749_base", True) for r in rows),
            "all_exactly_one_root": all(r.get("exactly_one_root") for r in rows),
            "f_prime_square_count": sum(1 for r in rows if r.get("f_prime_is_a_square")),
            "02_says_f_prime_is_a_square": True,
            "instrument_agrees_with_02_on_all_four":
                all(r.get("f_prime_is_a_square") for r in rows),
            "the_other_two_nonsquare_conditions_hold":
                all(not r.get("minus_f_prime_is_a_square")
                    and not r.get("minus_disc_is_a_square") for r in rows),
            "02s_other_reasons_not_computed_here": [
                "ord_2 L^alg = -2 where CLZ20 needs -1",
                "E'(Q)[2] ≅ (2,2), not cyclic",
                "the S ≠ ∅ gate fails"],
            "regression_rule": ("02: if a version accepts these four, label it "
                                "REGRESSION?, not NEW BSD BREAKTHROUGH!. This "
                                "gate makes that a standing check on this "
                                "line's own 8b instrument")}


def negative_control_for_RUN_055() -> dict:
    r55 = json.loads((LOGS / "src57-theorem-2-18-condition-map.json")
                     .read_text(encoding="utf-8")) if (LOGS / "src57-theorem-2-18-condition-map.json").exists() else {}
    br = r55.get("branches") or {}
    return {"RUN_055_checked": br.get("8b_checked"),
            "RUN_055_f_prime_squares_found": br.get("8b_f_prime_is_a_square"),
            "so_the_instrument_had_only_seen": "passing curves",
            "now_it_has_seen": "four the corpus says must fail, and it fails them",
            "discipline": "RUN-042: a condition whose excluded set is never "
                          "exhibited has not been tested"}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    t02 = (DOCS / "02_Official_Discrepancy_Corpus.md")
    t02 = t02.read_text(encoding="utf-8") if t02.exists() else ""
    base = cmap.load_base()
    pin = shard_pin()
    four = the_four(base)
    nc = negative_control_for_RUN_055()

    ok = (bool(t02) and all(l in t02 for l in FOUR)
          and pin["shard_present"] and pin["crlf_matches_package"]
          and not pin["lf_matches_package"] and pin["byte_gap_equals_line_count"]
          and four["all_found"] and four["none_in_base"]
          and four["all_exactly_one_root"]
          and four["f_prime_square_count"] == 4
          and four["instrument_agrees_with_02_on_all_four"]
          and nc["RUN_055_f_prime_squares_found"] == 0)

    log = {"gate": "src64 — 02's adversarial corpus against this line's 8b instrument",
           "source": "02_Official_Discrepancy_Corpus", "document_found": bool(t02),
           "shard_pin": pin, "the_four": four,
           "negative_control_for_RUN_055": nc,
           "headline": (f"02's four adversarial curves, read from the pinned ecdata "
                        f"shard: none in the base, each with exactly one rational "
                        f"2-torsion point, and f'(x0) a perfect square on "
                        f"{four['f_prime_square_count']} of 4 — RUN-055's "
                        f"instrument, which found 0 squares on 3,747 accepted "
                        f"curves, fails all four as 02 says. And the shard's pin "
                        f"reproduces only as CRLF: LF sha {pin['sha256_lf'][:8]}… "
                        f"≠ package, CRLF sha = package, gap {PACKAGE_BYTES - pin['bytes_lf']:,} "
                        f"bytes = {pin['line_count']:,} lines"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

    print(f"  shard: LF {pin['bytes_lf']:,} B sha {pin['sha256_lf'][:12]}…; CRLF "
          f"{pin['bytes_crlf']:,} B sha {pin['sha256_crlf'][:12]}…; package "
          f"{PACKAGE_BYTES:,} B — LF matches {pin['lf_matches_package']}, CRLF "
          f"matches {pin['crlf_matches_package']}, gap = lines "
          f"{pin['byte_gap_equals_line_count']}")
    print()
    for r in four["rows"]:
        print(f"  {r['curve']:6s} {r.get('ainvs')}  in base {r.get('in_the_40749_base')}  "
              f"X0 {r.get('X0')}  4f' {r.get('four_f_prime')}  square {r.get('f_prime_is_a_square')}  "
              f"-f' sq {r.get('minus_f_prime_is_a_square')}  -Δ sq {r.get('minus_disc_is_a_square')}")
    print(f"  f'(x0) square on {four['f_prime_square_count']} of 4; RUN-055 found "
          f"{nc['RUN_055_f_prime_squares_found']} among {nc['RUN_055_checked']:,} accepted")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
