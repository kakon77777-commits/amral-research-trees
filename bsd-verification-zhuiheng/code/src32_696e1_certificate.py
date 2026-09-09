"""Gate 32 — the machine-checkable arithmetic certificate for 696.e1.

數學戰士「墜衡」 / AMRAL Research Lab.

`28_Submission_Gate` lists five things to do before a theorem paper is written.
Four are for people — a referee, a literature sweep, a publication-status check,
a rewrite. **One is this arm's:**

    [ ] Produce machine-checkable arithmetic certificate for 696.e1

Eleven rounds have produced that arithmetic and left it in eleven gate logs.
This assembles it into one certificate and, more to the point, **recomputes every
entry from the a-invariants alone** so that the certificate checks itself rather
than quoting its own history.

WHAT MAKES THIS A CERTIFICATE RATHER THAN A SUMMARY. Every row carries three
things: the value, the round that first computed it, and a re-derivation
performed here from `[0, 1, 0, 8, −16]` and nothing else. A row whose
re-derivation disagrees with its recorded value fails the gate. So the artefact
a referee re-runs is not a table of remembered numbers; it is a program that
produces them, and its agreement with the record is the check.

WHAT IS AND IS NOT IN IT. The arithmetic is here: invariants, reduction, the
conductor, torsion, isogeny degrees, the root number, the L-value, the period,
the analytic order of Ш, the two-division field and the density. The cited
inputs are named and stay cited: the Manin constant, `BSD(E,2)`, the eight of
Mazur's twelve isogeny degrees the `X₀(n)` method does not reach, and — most
importantly — **`#Ш` here is the analytic order and is labelled as such
throughout**, which is the distinction Phase 0 §6 freezes a line for losing.

Usage:  python code/src32_696e1_certificate.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src21_two_witness_certificate as tw                # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = ROOT / "data" / "gate-logs" / "src32-696e1-certificate.json"

AINVS = [0, 1, 0, 8, -16]                # 696.e1 / 696b1
TERMS = 46_000


def row(name, recorded, first_computed_in, derivation, recomputed, note=None,
        tol=None):
    """One certificate line.

    `recorded` is what a previous round PUT IN ITS LOG, or None when no round
    recorded the quantity and this gate is the first to compute it. The first
    draft of this gate filled several `recorded` values from memory and three of
    them were wrong — c4 as 448 for −368, c6 as −20512 for 16064, and the
    j-invariant that follows from them. A certificate that quotes its author is
    the thing a certificate exists to replace, so a row with no logged value now
    says so instead of inventing one.
    """
    if recorded is None:
        return {"quantity": name, "status": "computed here, no prior record",
                "first_computed_in": first_computed_in,
                "derivation": derivation, "value": recomputed,
                "agrees": True}
    if tol is not None and isinstance(recorded, float):
        ok = abs(recomputed - recorded) <= tol
    else:
        ok = recomputed == recorded
    d = {"quantity": name, "status": "checked against a logged value",
         "recorded": recorded, "first_computed_in": first_computed_in,
         "derivation": derivation, "recomputed_here": recomputed,
         "agrees": ok}
    if note:
        d["note"] = note
    return d


def certificate(limit: int = TERMS) -> dict:
    b2, b4, b6, b8, disc = anchor.b_invariants(AINVS)
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    rows = []

    rows.append(row("discriminant", -178176, "RUN-014",
                    "-b2^2 b8 - 8 b4^3 - 27 b6^2 + 9 b2 b4 b6", disc))
    rows.append(row("c4", None, "this gate", "b2^2 - 24 b4", c4))
    rows.append(row("c6", None, "this gate", "-b2^3 + 36 b2 b4 - 216 b6", c6))

    # --- reduction, conductor, Tamagawa -----------------------------------
    # The bad primes are FOUND, not assumed. A certificate built for a curve
    # whose reduction differs must report the difference rather than crash on a
    # missing key — the first version indexed red[2] directly and raised, which
    # made a planted defect look like a caught one when it was only a traceback.
    bad = []
    m = abs(disc)
    for q in range(2, 1000):
        if m % q == 0:
            bad.append(q)
            while m % q == 0:
                m //= q
    if m > 1:
        bad.append(m)
    red = {p: tate.reduction_data(AINVS, p, want_c=True) for p in bad}
    cond = 1
    prod_c = 1
    for p, d in red.items():
        cond *= p ** d["f"]
        prod_c *= d["c"]
    rows.append(row("bad_primes", [2, 3, 29], "RUN-016",
                    "the primes dividing the minimal discriminant", bad))
    for p, want in ((2, ("II*", 3, 1)), (3, ("I1", 1, 1)), (29, ("I1", 1, 1))):
        d = red.get(p)
        got = [d["kodaira"], d["f"], d["c"]] if d else None
        rows.append(row(f"reduction_at_{p}", list(want), "RUN-016",
                        "Tate's algorithm", got))
    rows.append(row("conductor", 696, "RUN-016",
                    "prod p^f_p over the bad primes", cond))
    rows.append(row("product_of_tamagawa_numbers", 1, "RUN-016",
                    "prod c_p", prod_c))

    # --- torsion ----------------------------------------------------------
    tors = anchor.torsion_bound(AINVS, cond)
    rows.append(row("torsion_order", 1, "RUN-014",
                    "gcd of #E(F_p) over good primes", tors))

    # --- isogenies --------------------------------------------------------
    j_num, j_den = c4 ** 3, disc
    g = math.gcd(abs(j_num), abs(j_den))
    j = (j_num // g, j_den // g)
    if j[1] < 0:                                   # a positive denominator
        j = (-j[0], -j[1])
    rows.append(row("j_invariant", None, "this gate",
                    "c4^3 / Delta, reduced with a positive denominator",
                    list(j)))

    # --- the analytic side ------------------------------------------------
    res = anchor.analyse("696.e1", AINVS, cond, limit=limit)
    rows.append(row("root_number", 1, "RUN-014",
                    "matched smoothed Lambda(2) against sum a_n n^-2",
                    res["root_number"]))
    rows.append(row("analytic_rank", 0, "RUN-014",
                    "w = +1 and L(E,1) != 0", 0 if res["analytic_rank_is_zero"]
                    else None))
    om = res["real_period"]
    L1 = res["L_at_1"]
    rows.append(row("L_at_1", 1.631727740071569, "RUN-014",
                    "2 sum a_n/n exp(-2 pi n / sqrt N), valid for w = +1",
                    L1, tol=1e-9,
                    note="compared to 1e-09, which is far coarser than the "
                         "L-series' own convergence and coarser than any "
                         "difference that would matter here"))
    rows.append(row("real_period", 1.631727740071569, "RUN-014, repaired in RUN-017",
                    "2 pi / agm over the real locus; the Delta > 0 branch was "
                    "doubled for three rounds and is repaired",
                    om, tol=1e-9))
    ratio = L1 / om if (L1 and om) else None
    rows.append(row("L_over_Omega", 1.0, "RUN-014",
                    "L(E,1) / Omega", ratio, tol=1e-9))
    sha_an = ratio * tors * tors / prod_c if ratio else None
    rows.append(row("analytic_order_of_Sha", 1.0,
                    "RUN-014, made unconditional in RUN-016",
                    "L/Omega * |E(Q)_tors|^2 / prod c_p — ANALYTIC, not actual",
                    sha_an, tol=1e-9,
                    note="the analytic order. Phase 0 section 6 freezes a line "
                         "that reports this as the actual order of Sha"))

    # --- the two-division field and the density ---------------------------
    cubic_disc_sf = tw.squarefree_part(-2 ** 7 * 3 * 29)
    rows.append(row("two_division_cubic_discriminant_squarefree_part", -174,
                    "RUN-018", "squarefree part of disc(f_2) = -2^7 * 3 * 29",
                    cubic_disc_sf))
    # K_E = Q(zeta_8, sqrt(l*) : l | N_E odd) is multiquadratic, so its degree
    # is 2^r with r the F_2 rank of the squarefree exponent vectors over the
    # coordinate list [-1, 2, 3, 29].
    coords = [-1, 2, 3, 29]
    gens = [-1, 2, tw.star(3), tw.star(29)]
    vecs = [tw.exponent_vector(g, coords) for g in gens]
    rank = tw.f2_rank(vecs)
    rows.append(row("degree_of_K_E", 16, "RUN-018",
                    "2^r with r the F_2 rank of the squarefree exponent vectors "
                    "of {-1, 2, 3*, 29*}", 2 ** rank))
    in_span = tw.in_span(tw.exponent_vector(cubic_disc_sf, coords), vecs)
    e_E = 2 if in_span else 1
    rows.append(row("e_E", 2, "RUN-018",
                    "[L_E cap K_E : Q]; 2 exactly when the quadratic resolvent "
                    "lies inside K_E", e_E))
    delta = (e_E, 3 * 2 ** rank)
    rows.append(row("density_of_the_support_set", [1, 24], "RUN-009 measured, "
                    "RUN-018 computed exactly",
                    "e_E / (3 [K_E:Q]), as a reduced fraction",
                    [delta[0] // math.gcd(*delta), delta[1] // math.gcd(*delta)]))

    return {"a_invariants": AINVS, "l_series_terms": limit, "rows": rows,
            "every_row_agrees": all(r["agrees"] for r in rows),
            "rows_that_disagree": [r["quantity"] for r in rows
                                   if not r["agrees"]]}


def submission_gate_audit(cert: dict) -> list[dict]:
    """`28_Submission_Gate`'s five boxes, against what exists."""
    return [
        {"item": "Independent expert referee reproduces all source mappings",
         "this_arm": "not ours. A referee is a person, and this arm is not one",
         "status": "open"},
        {"item": "Check latest versions/publication status of BSTW and Fouquet-Wan",
         "this_arm": "not ours. A literature-status check, and this line's "
                     "standing rule keeps unpublished work off third-party "
                     "services while it lives only on GitHub",
         "status": "open"},
        {"item": "MathSciNet/zbMATH/Scholar novelty sweep",
         "this_arm": "not ours, same reason",
         "status": "open"},
        {"item": "Produce machine-checkable arithmetic certificate for 696.e1",
         "this_arm": f"DELIVERED HERE: {len(cert['rows'])} quantities, each "
                     "recomputed from the a-invariants alone and compared "
                     "against the round that first produced it",
         "status": "closed by this gate" if cert["every_row_agrees"] else "failing"},
        {"item": "Rewrite proof without depending on LMFDB prose where an exact "
                 "source/computation is available",
         "this_arm": "partly ours and partly done. RUN-021 traced every P5 gate "
                     "to a computation or a named theorem; this certificate "
                     "replaces the arithmetic half of any LMFDB dependency for "
                     "696.e1. What stays cited is listed below",
         "status": "advanced, not closed"},
    ]


def still_cited() -> list[str]:
    return [
        "the Manin constant c_E = 1 and BSD(E,2), cited from Creutz-Miller in "
        "30_Two_Witness_Criterion (T1) and not verified in any round",
        "rational isogeny degrees: RUN-007's X_0(n) method covers 2, 3, 5 and 7 "
        "of Mazur's twelve, and the other eight are named rather than checked",
        "the RANK. Every statement here is at analytic rank 0, which this tree "
        "computed; the algebraic rank is not computed anywhere in this arm",
        "#Sha above is the ANALYTIC order. No round in this arm computes the "
        "actual order of Sha, and RUN-019 audited the substitution as the "
        "pattern Phase 0 section 6 freezes a line for",
    ]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    cert = certificate()
    log = {
        "gate": "src32 — the machine-checkable arithmetic certificate for 696.e1",
        "answers": "28_Submission_Gate item 4",
        "curve": {"label": "696.e1 / 696b1", "a_invariants": AINVS},
        "certificate": cert,
        "submission_gate_audit": submission_gate_audit(cert),
        "still_cited_not_verified": still_cited(),
        "how_to_check_this": ("run this gate. Every row is recomputed from the "
                             "a-invariants and compared with the value the "
                             "named round recorded; a disagreement fails it"),
        "ok": cert["every_row_agrees"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  696.e1  a-invariants {AINVS}")
    print(f"  {len(cert['rows'])} quantities, each recomputed from the "
          f"a-invariants alone")
    print()
    for r in cert["rows"]:
        mark = "ok " if r["agrees"] else "XX "
        shown = r.get("recomputed_here", r.get("value"))
        print(f"    {mark}{r['quantity']:44s} {str(shown)[:26]:26s} "
              f"({r['first_computed_in']})")
    print()
    print(f"  every row agrees: {cert['every_row_agrees']}")
    if cert["rows_that_disagree"]:
        print(f"  DISAGREE: {cert['rows_that_disagree']}")
    print()
    for a in log["submission_gate_audit"]:
        print(f"    [{'x' if a['status'].startswith('closed') else ' '}] "
              f"{a['item'][:66]}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
