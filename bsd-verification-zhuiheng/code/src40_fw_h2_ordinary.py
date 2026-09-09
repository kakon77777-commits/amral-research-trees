"""Gate 40 — the FW-H2 compiler, and the obstruction that keeps ordinary out of FW.

數學戰士「墜衡」 / AMRAL Research Lab.

`10_FW_H2_and_Ordinary_Obstruction` states three things and boxes all of them.

    good supersingular      the residual local representation is governed by the
                            niveau-2 fundamental characters, hence irreducible,
                            so FW-H1 = FW-H2 = PASS and only H3 remains

    good ordinary           rho-bar^ss = alpha-bar + chi_cyc alpha-bar^{-1} with
                            alpha-bar unramified and Frobenius value a_p mod p,
                            so H2 fails exactly when alpha-bar^2 = 1:

                                a_p(E)^2 = 1 (mod p)

    potentially             the local semisimplification is already a quadratic
    multiplicative          Tate twist psi + psi chi_cyc, which is the FW-H2
                            forbidden shape

and concludes: ordinary primes keep the ordinary theorem, FW is left to additive
and supersingular.

THE MIDDLE ONE IS A CHEAP EXACT CRITERION AND IT IS RUN HERE. By Hasse,
|a_p| <= 2 sqrt p, so for p >= 7 the congruence a_p^2 = 1 (mod p) forces
a_p = +1 or -1 outright — which is measured rather than assumed, since the
inequality is tight only above a small bound and p = 5 is inside it.

THE DOCUMENT'S REASON FOR NOT ROUTING ORDINARY TO FW IS THAT NO CLEAN
FINITE-EXCEPTION THEOREM IS AVAILABLE. That is a statement about a set, and a
set can be measured: this gate counts the ordinary primes where H2 fails, in
successive ranges, and reports whether they stop. An empty or bounded failure
set would have made the routing decision unnecessary; a set that keeps
producing members is what makes it right.

Usage:  python code/src40_fw_h2_ordinary.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src40-fw-h2-ordinary.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
P_BOUND = 6000


def classify(bound: int = P_BOUND) -> dict:
    """Every good odd prime, split into supersingular and ordinary, with `10`'s
    exact H2 criterion applied to the ordinary ones."""
    _, _, _, _, disc = anchor.b_invariants(BASE)
    rows, ss, fail = [], [], []
    for p in anchor.sieve(bound):
        if p < 5 or disc % p == 0:
            continue
        a = anchor.point_count_ap(BASE, p)
        if a % p == 0:
            ss.append({"p": p, "a_p": a})
            rows.append({"p": p, "a_p": a, "branch": "good supersingular",
                         "H2": "PASS (niveau-2, cited)"})
            continue
        bad = (a * a - 1) % p == 0
        rows.append({"p": p, "a_p": a, "branch": "good ordinary",
                     "H2": "FAIL" if bad else "PASS"})
        if bad:
            fail.append({"p": p, "a_p": a})
    return {"bound": bound, "good_odd_primes": len(rows), "rows": rows,
            "supersingular": ss, "ordinary_H2_failures": fail}


def hasse_refinement(c: dict) -> dict:
    """For p >= 7 the congruence forces a_p = +-1 exactly. Measured.

    |a_p| <= 2 sqrt p, so a_p = 1 (mod p) with |a_p| < p leaves a_p = 1 unless
    1 - p is also inside the Hasse interval, which needs p - 1 <= 2 sqrt p and
    so p <= 5. Reporting the refinement without checking the small case would be
    quoting an inequality at the one place it does not hold.
    """
    rows = [{"p": r["p"], "a_p": r["a_p"], "is_plus_or_minus_one":
             r["a_p"] in (1, -1)} for r in c["ordinary_H2_failures"]]
    small = [r for r in rows if r["p"] < 7]
    return {"failures": rows,
            "all_are_plus_or_minus_one": all(r["is_plus_or_minus_one"]
                                             for r in rows),
            "failures_below_7": [r["p"] for r in small],
            "the_bound_where_it_becomes_forced": 7,
            "why": ("p - 1 <= 2 sqrt p holds only for p <= 5, so below 7 the "
                    "congruence could also be met by a_p = 1 - p; above it the "
                    "Hasse interval is too narrow and a_p = +-1 exactly")}


def no_finite_exception(c: dict, blocks: int = 4) -> dict:
    """`10`'s reason for the routing, measured as a set that does not stop.

    The failures are bucketed into successive ranges. A set that dried up would
    make the ordinary branch coverable by FW after a finite exception list,
    which is exactly what the document says is unavailable.
    """
    b = c["bound"]
    edges = [b * (i + 1) // blocks for i in range(blocks)]
    lo, buckets = 0, []
    for hi in edges:
        got = [r["p"] for r in c["ordinary_H2_failures"] if lo < r["p"] <= hi]
        buckets.append({"range": f"({lo}, {hi}]", "failures": got,
                        "count": len(got)})
        lo = hi
    nonempty = [x for x in buckets if x["count"]]
    return {"buckets": buckets,
            "ranges_with_at_least_one_failure": len(nonempty),
            "of": blocks,
            "keeps_producing": len(nonempty) >= blocks - 1,
            "total": len(c["ordinary_H2_failures"]),
            "reading": ("the failure set is not a finite list that a theorem "
                        "could except away below this bound, which is the "
                        "document's stated reason for keeping ordinary primes "
                        "on the ordinary theorem")}


def supersingular_branch(c: dict) -> dict:
    """The branch FW is actually left, and its interlock with gate 39.

    `10` gives H1 and H2 free there, so FW needs only H3 — and RUN-037's
    compiler settles H3 for every odd `p` except the one where `W_-` is a
    singleton containing `p` itself. Every supersingular prime is a prime of
    GOOD reduction, so none of them is 29, and the exception cannot reach this
    branch. That is checked rather than argued.
    """
    w = h3c.w_minus(BASE)
    rows = []
    for r in c["supersingular"]:
        v = h3c.h3(w, r["p"])
        rows.append({"p": r["p"], "a_p": r["a_p"], "H1": "PASS (cited)",
                     "H2": "PASS (cited)", "H3": v["pass"],
                     "H3_witness": v["witness"]})
    return {"count": len(rows), "primes": [r["p"] for r in rows], "rows": rows,
            "branch_is_non_empty": bool(rows),
            "H3_passes_at_every_one": all(r["H3"] for r in rows),
            "the_H3_exception_cannot_reach_here":
                all(r["p"] not in [x["ell"] for x in w] for r in rows),
            "why": ("gate 39 found FW-H3's boxed certificate false at the one "
                    "p inside W_-, and W_- consists of bad primes while this "
                    "branch consists of good ones, so the two never meet")}


def potentially_multiplicative_branch() -> dict:
    """`10`'s third box, cross-checked against RUN-034's measurement.

    A potentially multiplicative prime lands in the FW-H2 forbidden shape, so
    that branch does not go to FW either. RUN-034 measured the same statement
    from `05`'s side and found the additive primes of this family all
    potentially good. Here the check is over the whole bad-prime set.
    """
    md = gcd35.multiplicative_data(BASE)
    rows = []
    for r in md["rows"]:
        p = r["p"]
        rows.append({"p": p, "reduction": r["type"],
                     "potential": tate.potential_reduction(BASE, p)})
    pm = [r["p"] for r in rows
          if r["potential"] == "potentially multiplicative"]
    additive_pm = [r["p"] for r in rows if r["reduction"] == "additive"
                   and r["potential"] == "potentially multiplicative"]
    return {"bad_primes": rows, "potentially_multiplicative": pm,
            "additive_and_potentially_multiplicative": additive_pm,
            "branch_is_empty_for_this_curve": not additive_pm,
            "agrees_with_RUN_034": not additive_pm,
            "note": ("3 and 29 are potentially multiplicative because they ARE "
                     "multiplicative; the branch `10` and `05` both exclude is "
                     "the additive one, and it is empty here")}


def routing(c: dict, blocks: int = 4) -> dict:
    """`10`'s boxed conclusion, checked against what was measured.

    `blocks` is passed through rather than fixed: the bucket count only makes
    sense against the bound it is applied to, and a caller running at a smaller
    bound must be able to say so instead of inheriting a split that leaves empty
    ranges for a reason that has nothing to do with the curve.
    """
    ss = supersingular_branch(c)
    ne = no_finite_exception(c, blocks=blocks)
    return {"boxed": "ordinary primes keep the ordinary theorem; FW is left to "
                     "additive + supersingular",
            "ordinary_cannot_go_to_FW_because":
                f"{ne['total']} ordinary primes below {c['bound']} fail H2, "
                f"spread over {ne['ranges_with_at_least_one_failure']} of "
                f"{ne['of']} ranges",
            "FW_branch_is_not_vacuous": ss["branch_is_non_empty"],
            "supersingular_primes": ss["primes"],
            "supported_by_measurement": (ne["keeps_producing"]
                                         and ss["branch_is_non_empty"])}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    c = classify()
    hr = hasse_refinement(c)
    ne = no_finite_exception(c)
    ss = supersingular_branch(c)
    pm = potentially_multiplicative_branch()
    rt = routing(c)

    ok = (hr["all_are_plus_or_minus_one"] and ne["keeps_producing"]
          and ss["branch_is_non_empty"] and ss["H3_passes_at_every_one"]
          and ss["the_H3_exception_cannot_reach_here"]
          and pm["branch_is_empty_for_this_curve"]
          and rt["supported_by_measurement"]
          and bool(c["ordinary_H2_failures"]))

    log = {
        "gate": "src40 — the FW-H2 compiler and the ordinary obstruction",
        "source": "10_FW_H2_and_Ordinary_Obstruction",
        "curve": BASE, "conductor": N,
        "classification": {k: v for k, v in c.items() if k != "rows"},
        "hasse_refinement": hr,
        "no_finite_exception": ne,
        "supersingular_branch": ss,
        "potentially_multiplicative_branch": pm,
        "routing": rt,
        "headline": ("`10`'s exact ordinary criterion a_p² ≡ 1 (mod p) is run: "
                     f"{len(c['ordinary_H2_failures'])} ordinary primes below "
                     f"{c['bound']} fail FW-H2, every one with a_p = ±1, and "
                     f"they keep appearing across the range. That is the "
                     f"document's reason for keeping ordinary primes off FW, "
                     f"measured. The branch FW is left — "
                     f"{ss['count']} supersingular primes — is non-empty and "
                     f"clears H3 at every one"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  696.e1, {c['good_odd_primes']} good odd primes below {c['bound']}")
    print()
    print(f"  good ordinary, FW-H2 FAILS at a_p² ≡ 1 (mod p):")
    print(f"    {[(r['p'], r['a_p']) for r in c['ordinary_H2_failures']]}")
    print(f"    every one has a_p = ±1: {hr['all_are_plus_or_minus_one']}   "
          f"(forced by Hasse for p ≥ {hr['the_bound_where_it_becomes_forced']}, "
          f"and the small cases are listed: {hr['failures_below_7']})")
    for b in ne["buckets"]:
        print(f"    {b['range']:>16}  {b['count']}  {b['failures']}")
    print(f"    keeps producing across {ne['ranges_with_at_least_one_failure']} "
          f"of {ne['of']} ranges: {ne['keeps_producing']}")
    print()
    print(f"  good supersingular — the branch FW is left: {ss['primes']}")
    print(f"    H1, H2 free (cited); H3 passes at every one: "
          f"{ss['H3_passes_at_every_one']}")
    print(f"    gate 39's H3 exception cannot reach here: "
          f"{ss['the_H3_exception_cannot_reach_here']}")
    print()
    print(f"  potentially multiplicative: {pm['potentially_multiplicative']}, "
          f"of which additive: {pm['additive_and_potentially_multiplicative']}")
    print(f"    the branch 10 and 05 both exclude is empty here: "
          f"{pm['branch_is_empty_for_this_curve']}")
    print()
    print(f"  routing supported by measurement: {rt['supported_by_measurement']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
