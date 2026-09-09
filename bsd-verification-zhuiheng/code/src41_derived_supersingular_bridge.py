"""Gate 41 — the derived supersingular FW bridge, assembled from what is computed.

數學戰士「墜衡」 / AMRAL Research Lab.

`11_Derived_Supersingular_FW_Bridge` opens by saying what it is:

    狀態：由現有外部定理拼接出的 derived proposition；不是原論文命名定理。

It asks for one thing and gives three. For `E/Q` and a good supersingular odd
`p`, suppose there is an `ell || N_E` with

    1. E nonsplit multiplicative at ell,
    2. p does not divide v_ell(Delta_min).

Then good supersingular local irreducibility gives FW-H1, the same
irreducibility excludes the FW-H2 forbidden shape, and nonsplit Steinberg with
residual ramification gives FW-H3 — so `E[p]` satisfies the Fouquet–Wan residual
hypotheses. With `L(E,1) != 0` the rank-zero p-part corollary applies, "惟
period normalization / Manin constant 需另外閉合".

THE SAME GCD ARGUMENT, ONE QUANTIFIER APART. `11`'s uniform form says that
`g_-(E) = 2^a` closes **all good supersingular odd primes** at once. `09`'s says
it closes **all odd p**. RUN-037 found `09`'s boxed line false at `p = 29`,
because `W_- = {29}` is a singleton and the `ell != p` clause empties it. `11`
is not false, and the reason is only the range of its quantifier: `W_-` consists
of primes of BAD reduction and `11` quantifies over primes of GOOD reduction, so
the failing prime is outside the claim. This gate checks that the two sets are
disjoint rather than observing that no counterexample turned up.

WHAT THIS ARM CANNOT CLOSE IS NAMED, NOT SKIPPED. `11` itself proposes the safe
period condition `c_E = 1` to avoid the modular-versus-Néron ambiguity. The
Manin constant is not computed anywhere in this tree — RUN-030's certificate
lists it among what stays cited, and it stays cited here.

Usage:  python code/src41_derived_supersingular_bridge.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402
import src40_fw_h2_ordinary as h2o                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src41-derived-bridge.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
SS_BOUND = 6000
TERMS = 20_000

CITED = {
    "the Fouquet–Wan theorem": "external; this arm checks its residual "
                               "hypotheses, never the theorem",
    "H1 and H2 at good supersingular p": "10_FW_H2_and_Ordinary_Obstruction's "
                                         "niveau-2 argument, cited in RUN-038",
    "the Manin constant c_E": "not computed anywhere in this tree; "
                              "24_Manin_Period_Audit and RUN-030's certificate "
                              "both list it as cited",
    "optimality of the twist": "a statement about X_0(696), cited since "
                               "RUN-031",
}


def hypotheses() -> dict:
    """`11`'s two numbered hypotheses, computed."""
    w = h3c.w_minus(BASE)
    return {"W_minus": [r["ell"] for r in w],
            "valuations": {str(r["ell"]): r["v_disc"] for r in w},
            "hypothesis_1_exists_nonsplit_multiplicative_ell": bool(w),
            "g_minus": h3c.g_minus(w),
            "g_minus_is_a_power_of_two": h3c.is_power_of_two(h3c.g_minus(w))}


def quantifier_ranges(bound: int = SS_BOUND) -> dict:
    """Why `11`'s uniform form survives what `09`'s does not.

    Both rest on `g_-(E) = 2^a`. `09` concludes for every odd `p`; `11` only for
    good supersingular odd `p`. The failing prime RUN-037 found is the member of
    `W_-` itself, and `W_-` is a set of bad primes, so it cannot be a good
    supersingular one. Disjointness is computed here, not observed.
    """
    w = [r["ell"] for r in h3c.w_minus(BASE)]
    c = h2o.classify(bound)
    ss = [r["p"] for r in c["supersingular"]]
    cert = h3c.uniform_certificate(BASE)
    failing = cert["p_where_the_criterion_FAILS"]
    return {"W_minus": w, "good_supersingular_below_bound": ss,
            "the_09_failing_set": failing,
            "W_minus_and_supersingular_are_disjoint": not set(w) & set(ss),
            "every_09_failure_is_outside_11s_range":
                all(p not in ss for p in failing),
            "why": ("W_- is defined by ell || N, so its members are primes of "
                    "bad reduction; the supersingular branch is by definition "
                    "primes of good reduction. The two cannot meet, which is "
                    "why 11's boxed line is true where 09's is false"),
            "the_difference_is_the_quantifier": ("09 says 'for all p > 2'; 11 "
                                                 "says 'all good supersingular "
                                                 "odd primes'. Same gcd, same "
                                                 "curve, different range")}


def per_prime(bound: int = SS_BOUND) -> dict:
    """The three FW residual hypotheses at each good supersingular prime."""
    w = h3c.w_minus(BASE)
    c = h2o.classify(bound)
    rows = []
    for r in c["supersingular"]:
        p = r["p"]
        v = h3c.h3(w, p)
        rows.append({"p": p, "a_p": r["a_p"],
                     "H1": {"verdict": "PASS", "source": "cited (niveau-2)"},
                     "H2": {"verdict": "PASS", "source": "cited (niveau-2)"},
                     "H3": {"verdict": "PASS" if v["pass"] else "FAIL",
                            "witness": v["witness"],
                            "source": "computed here"},
                     "all_three": v["pass"]})
    return {"bound": bound, "count": len(rows), "rows": rows,
            "every_prime_has_all_three": all(r["all_three"] for r in rows),
            "branch_is_non_empty": bool(rows),
            "computed_versus_cited": "H3 computed; H1 and H2 cited"}


def rank_zero_corollary(limit: int = TERMS) -> dict:
    """`L(E,1) != 0`, recomputed, and the caveat `11` attaches to it."""
    res = anchor.analyse("696.e1", BASE, N, limit=limit)
    return {"L_at_1": res["L_at_1"], "real_period": res["real_period"],
            "analytic_rank_is_zero": res["analytic_rank_is_zero"],
            "L_is_nonzero": bool(res["L_at_1"]) and abs(res["L_at_1"]) > 1e-6,
            "terms": limit,
            "the_caveat_verbatim": "period normalization / Manin constant "
                                   "需另外閉合",
            "closed_here": False}


def safe_period_condition() -> dict:
    """`11`'s own suggestion, and the honest verdict on it.

    The document proposes requiring `c_E = 1` outright to avoid splicing the
    modular and Néron periods. This arm computes the real period (RUN-014,
    repaired in RUN-017) and never the Manin constant, so the condition is
    stated and left open rather than assumed away.
    """
    return {"condition": "c_E = 1",
            "why_the_document_wants_it": "avoids the modular-period / "
                                         "Néron-period splicing ambiguity",
            "computed_in_this_tree": False,
            "what_this_tree_does_have": "the real period by AGM, confirmed "
                                        "against direct integration in "
                                        "RUN-017; the Manin constant is a "
                                        "different quantity",
            "status": "OPEN — the one hypothesis of the derived proposition "
                      "this arm cannot close"}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    h = hypotheses()
    q = quantifier_ranges()
    pp = per_prime()
    rz = rank_zero_corollary()
    sp = safe_period_condition()

    ok = (h["hypothesis_1_exists_nonsplit_multiplicative_ell"]
          and h["g_minus_is_a_power_of_two"]
          and q["W_minus_and_supersingular_are_disjoint"]
          and q["every_09_failure_is_outside_11s_range"]
          and bool(q["the_09_failing_set"])       # the contrast must be real
          and pp["branch_is_non_empty"] and pp["every_prime_has_all_three"]
          and rz["L_is_nonzero"] and rz["analytic_rank_is_zero"]
          and rz["closed_here"] is False
          and sp["computed_in_this_tree"] is False)

    log = {
        "gate": "src41 — the derived supersingular FW bridge, assembled",
        "source": "11_Derived_Supersingular_FW_Bridge",
        "documents_own_status": "由現有外部定理拼接出的 derived proposition；"
                                "不是原論文命名定理",
        "curve": BASE, "conductor": N,
        "hypotheses": h,
        "why_11_survives_what_09_does_not": q,
        "per_supersingular_prime": pp,
        "rank_zero_corollary": rz,
        "safe_period_condition": sp,
        "what_stays_cited": CITED,
        "headline": (f"the derived proposition's residual hypotheses hold at "
                     f"every one of the {pp['count']} good supersingular primes "
                     f"below {SS_BOUND} — H3 computed, H1 and H2 cited — and "
                     f"L(E,1) != 0 is recomputed. Its uniform form survives the "
                     f"failure RUN-037 found in 09's, and only because its "
                     f"quantifier ranges over good primes while W_- is made of "
                     f"bad ones. The period condition c_E = 1 stays OPEN"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  hypothesis 1: W_- = {h['W_minus']} {h['valuations']}  "
          f"→ {h['hypothesis_1_exists_nonsplit_multiplicative_ell']}")
    print(f"  uniform form: g_- = {h['g_minus']}, a power of two: "
          f"{h['g_minus_is_a_power_of_two']}")
    print()
    print(f"  09's boxed line fails at {q['the_09_failing_set']}; 11's range is "
          f"the good supersingular primes")
    print(f"    W_- ∩ supersingular = ∅ : "
          f"{q['W_minus_and_supersingular_are_disjoint']}")
    print(f"    every 09 failure outside 11's range: "
          f"{q['every_09_failure_is_outside_11s_range']}")
    print()
    print(f"  the {pp['count']} good supersingular primes below {SS_BOUND}")
    print(f"    {'p':>6}  {'a_p':>4}   H1      H2      H3   witness")
    for r in pp["rows"]:
        print(f"    {r['p']:>6}  {r['a_p']:>4}   {r['H1']['verdict']:<6}  "
              f"{r['H2']['verdict']:<6}  {r['H3']['verdict']:<4} "
              f"ℓ = {r['H3']['witness']}")
    print(f"    all three at every prime: {pp['every_prime_has_all_three']}   "
          f"({pp['computed_versus_cited']})")
    print()
    print(f"  L(E,1) = {rz['L_at_1']:.12f} at {rz['terms']} terms → nonzero: "
          f"{rz['L_is_nonzero']}")
    print(f"    the document's own caveat: {rz['the_caveat_verbatim']}")
    print(f"  safe period condition {sp['condition']}: {sp['status'][:44]}…")
    print()
    print("  what stays cited:")
    for k in CITED:
        print(f"    · {k}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
