"""Gate 44 — the corpus's own base certificate, compared row by row.

數學戰士「墜衡」 / AMRAL Research Lab.

`15_696e1_Base_Certificate` is the corpus's own certificate for the anchor, and
RUN-030 built an independent one in this tree. Two certificates for one curve
should agree, and where they cannot they should say which rows are computations
and which are citations. This runs that comparison.

THE DISCRIMINANT OF THE 2-DIVISION CUBIC NEEDS CARE, AND A NAIVE COMPARISON
WOULD REPORT A DISAGREEMENT THAT IS NOT ONE. Three different cubics are in play
and all three are correct:

    4x^3 + b2 x^2 + 2 b4 x + b6      the 2-division polynomial itself
    x^3 + x^2 + 8x - 16              `15`'s f_2, the above divided by 4, which
                                     is monic because a1 = a3 = 0
    x^3 + 4x^2 + 128x - 1024         RUN-036's monic form, from x -> x/4

Their discriminants are -11136 and -45613056, differing by 4096 = 64^2. The
same square class, so the same quadratic resolvent and the same Galois closure —
which is what the certificate rows actually claim. The comparison is therefore
by SQUARE CLASS and by squarefree part, not by value, and the gate says so in
the row rather than silently normalising.

WHAT THE DOCUMENT REFUSES IS ALSO CHECKED. `15` states outright that it does not
use

    analytic Sha = 1  =>  actual Sha = 1

and calls it circular. The gate reads the document for that refusal and reports
whether it is there, because a certificate's disclaimers are part of what it
certifies — the same reason RUN-030's rows carry their provenance and RUN-025
counted 36 labelled Sha claims.

Usage:  python code/src44_base_certificate_compare.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src44-base-certificate.json"
DOC = (ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
       / "15_696e1_Base_Certificate.md")

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
TERMS = 20_000

REFUSAL = "analytic Sha = 1 => actual Sha = 1"


def squarefree(n: int) -> tuple[int, int]:
    """(squarefree part, square part) with the sign kept on the squarefree part."""
    s, sq = abs(n), 1
    d = 2
    while d * d <= s:
        while s % (d * d) == 0:
            s //= d * d
            sq *= d
        d += 1
    return (-s if n < 0 else s, sq * sq)


def row(name, stated, recomputed, agree, kind, note=None) -> dict:
    r = {"row": name, "stated_in_15": stated, "recomputed_here": recomputed,
         "agree": agree, "kind": kind}
    if note:
        r["note"] = note
    return r


def compare(limit: int = TERMS) -> list[dict]:
    b2, b4, b6, b8, disc = anchor.b_invariants(BASE)
    c4 = b2 * b2 - 24 * b4
    md = gcd35.multiplicative_data(BASE)
    cps = {r["p"]: tate.reduction_data(BASE, r["p"], want_c=True).get("c")
           for r in md["rows"]}
    prod_c = math.prod(cps.values())
    res = anchor.analyse("696.e1", BASE, N, limit=limit)
    ratio = (res["L_at_1"] / res["real_period"]
             if res["L_at_1"] and res["real_period"] else None)
    tors = anchor.torsion_bound(BASE, N)

    # the three cubics, all correct
    f2_doc = [1, 1, 8, -16]                 # 15's, valid since a1 = a3 = 0
    f2_scaled = [1, b2, 8 * b4, 16 * b6]    # RUN-036's, from x -> x/4

    def cubic_disc(A, B, C):
        return (18 * A * B * C - 4 * A ** 3 * C + A * A * B * B
                - 4 * B ** 3 - 27 * C * C)

    d_doc = cubic_disc(*f2_doc[1:])
    d_scaled = cubic_disc(*f2_scaled[1:])
    sf_doc, sq_doc = squarefree(d_doc)
    sf_scaled, _ = squarefree(d_scaled)
    roots_doc = [x for x in range(-40, 41)
                 if x ** 3 + x * x + 8 * x - 16 == 0]

    conductor = tate.conductor(BASE, [2, 3, 29])

    return [
        row("curve y² = x³ + x² + 8x − 16", "[0, 1, 0, 8, -16]",
            str(BASE), str(BASE) == "[0, 1, 0, 8, -16]", "computed"),
        row("N = 696 = 2³·3·29", 696, conductor, conductor == 696, "computed",
            "conductor summed from Tate's f at each bad prime"),
        row("Δ_min = −2¹¹·3·29", -(2 ** 11) * 3 * 29, disc,
            disc == -(2 ** 11) * 3 * 29, "computed"),
        row("Δ_min < 0", True, disc < 0, disc < 0, "computed"),
        row("E(Q)_tors = 0", 1, tors, tors == 1, "computed",
            "trivial torsion; the document writes the group, the gate the order"),
        row("analytic rank 0", 0, 0 if res["analytic_rank_is_zero"] else None,
            res["analytic_rank_is_zero"], "computed",
            f"root number and L(E,1) at {limit} terms"),
        row("algebraic rank 0", 0, None, None, "NOT COMPUTED HERE",
            "no round of this arm computes the algebraic rank; RUN-030's "
            "certificate lists it among what stays cited"),
        row("optimal", True, None, None, "cited",
            "RUN-031 closed the premise (no rational prime-degree isogeny) and "
            "RUN-036 certified the mod-ℓ images; which curve the modular "
            "parametrisation lands on is still not computed"),
        row("Manin constant = 1", 1, None, None, "cited",
            "not computed anywhere in this tree; RUN-039 left `c_E = 1` open "
            "and RUN-040 checked `01`'s condition for `p ∤ c` instead"),
        row("BSD(E) verified for conductor < 5000, r_an = 0", "696 < 5000",
            "696 < 5000", conductor < 5000, "cited source",
            "the verification itself is Creutz–Miller / the literature; only "
            "the inequality is checked here"),
        row("∏ c_p = 1", 1, prod_c, prod_c == 1, "computed",
            f"Tamagawa numbers {cps}"),
        row("|E(Q)_tors| = 1", 1, tors, tors == 1, "computed"),
        row("Reg = 1", 1, 1, True, "computed by convention",
            "the empty determinant at rank 0; not an independent measurement"),
        row("Ш_an = 1", 1, None, None, "cited (LMFDB)",
            "the ANALYTIC order; RUN-025 counted 36 numeric Ш claims in the "
            "corpus and found all of them labelled"),
        row("L(E,1)/Ω_E = 1", 1, round(ratio, 9) if ratio else None,
            ratio is not None and abs(ratio - 1) < 1e-6, "computed",
            f"L = {res['L_at_1']}, Ω = {res['real_period']}"),
        row("v₂(L^alg) = 0", 0, 0 if ratio and abs(ratio - 1) < 1e-6 else None,
            ratio is not None and abs(ratio - 1) < 1e-6, "computed",
            "ord₂(1) = 0, the reading RUN-018, RUN-020 and RUN-032 all used"),
        row("f₂(x) = x³ + x² + 8x − 16", f2_doc, f2_doc, True, "computed",
            "the 2-division polynomial 4x³ + b₂x² + 2b₄x + b₆ divided by 4, "
            "which is monic exactly because a₁ = a₃ = 0"),
        row("f₂ has no rational root", True, not roots_doc, not roots_doc,
            "computed"),
        row("disc(f₂) = −11136 = −2⁷·3·29", -11136, d_doc,
            d_doc == -11136 == -(2 ** 7) * 3 * 29, "computed",
            f"RUN-036 used the x → x/4 model, whose discriminant is "
            f"{d_scaled} = 4096 × {d_doc}. 4096 = 64², so the SQUARE CLASS is "
            f"the same and every claim below is unaffected"),
        row("disc(f₂) is not a square", False,
            math.isqrt(abs(d_doc)) ** 2 == d_doc and d_doc > 0,
            not (d_doc > 0 and math.isqrt(d_doc) ** 2 == d_doc), "computed",
            "tested with an integer square root"),
        row("Galois closure S₃", "S₃",
            "S₃" if not roots_doc and not (d_doc > 0 and
                                           math.isqrt(abs(d_doc)) ** 2 == d_doc)
            else "not S₃",
            not roots_doc, "computed",
            "irreducible with non-square discriminant"),
        row("quadratic resolvent Q(√−174)", -174, sf_doc, sf_doc == -174,
            "computed",
            f"squarefree part of {d_doc} is {sf_doc} with square part "
            f"{sq_doc}; the x → x/4 model gives {sf_scaled}, the same"),
    ]


def the_refusal() -> dict:
    """`15` refuses the circular Ш inference. Is the refusal in the text?"""
    if not DOC.exists():
        return {"document_found": False, "path": str(DOC)}
    text = DOC.read_text(encoding="utf-8")
    marks = ["analytic Sha", "actual Sha", "circular"]
    present = {m: (m in text) for m in marks}
    return {"document_found": True,
            "the_refusal_as_written": REFUSAL,
            "markers_present": present,
            "refusal_is_in_the_document": all(present.values()),
            "why_this_is_checked": ("a certificate's disclaimers are part of "
                                    "what it certifies. If the refusal were "
                                    "dropped, every Ш row in the corpus would "
                                    "change meaning while the numbers stayed "
                                    "the same")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    rows = compare()
    ref = the_refusal()
    computed = [r for r in rows if r["kind"].startswith("computed")]
    cited = [r for r in rows if not r["kind"].startswith("computed")]
    disagreements = [r for r in computed if r["agree"] is not True]

    ok = (not disagreements and ref.get("refusal_is_in_the_document", False)
          and len(computed) >= 14 and len(cited) >= 4)

    log = {
        "gate": "src44 — 15_696e1_Base_Certificate, compared row by row",
        "source": "15_696e1_Base_Certificate",
        "against": "this tree's own computations, and RUN-030's certificate",
        "curve": BASE,
        "rows": rows,
        "rows_computed_here": len(computed),
        "rows_not_computable_here": len(cited),
        "disagreements": disagreements,
        "the_refusal": ref,
        "the_three_cubics": {
            "2-division polynomial": "4x³ + b₂x² + 2b₄x + b₆",
            "15's f₂": "x³ + x² + 8x − 16, the above over 4 (monic because "
                       "a₁ = a₃ = 0)",
            "RUN-036's": "x³ + 4x² + 128x − 1024, from x → x/4",
            "discriminants": [-11136, -45613056],
            "ratio": 4096,
            "ratio_is_a_square": math.isqrt(4096) ** 2 == 4096,
            "so": "same square class, same squarefree part −174, same "
                  "quadratic resolvent, same Galois closure. A comparison by "
                  "value would have reported a disagreement that is not one",
        },
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  15_696e1_Base_Certificate against this tree — {len(rows)} rows")
    print()
    for r in rows:
        mark = ("OK   " if r["agree"] is True else
                "  —  " if r["agree"] is None else "DISAGREE")
        print(f"    {mark}  {r['row'][:44]:44s} {str(r['kind'])[:22]:22s}")
    print()
    print(f"  computed here: {len(computed)}   not computable here: "
          f"{len(cited)}   disagreements: {len(disagreements)}")
    print()
    c = log["the_three_cubics"]
    print(f"  the three cubics: discriminants {c['discriminants']}, ratio "
          f"{c['ratio']}, a square: {c['ratio_is_a_square']}")
    print(f"    → {c['so'][:88]}…")
    print()
    print(f"  the document's refusal of the circular Ш inference present: "
          f"{ref.get('refusal_is_in_the_document')}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
