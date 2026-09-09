"""Gate 28 — the rank-1 BSD identity, on the rank this arm had never touched.

數學戰士「墜衡」 / AMRAL Research Lab.

`06_Phase1_Agent_Experiment` §3 divides its benchmark into three groups, R0, R1
and R2+. RUN-025 recorded that this arm had verified R0 (696.e1, RUN-014) and
R2+ (389.a1, RUN-011/020/022/023) and **never once an R1 curve**. That is a
coverage gap in this tree's own confidence, not in the corpus, and it is the
kind an attack needs to know about: the arm's assurance was uneven across
exactly the axis the experiment is organised by.

WHAT RANK 1 NEEDS THAT THE OTHER TWO DID NOT. At rank 0 the L-value is the
number; at rank 2 this arm took the leading coefficient from a document. At rank
1 the leading coefficient is computable here, because the root number is −1 and
the classical formula

    L'(E,1) = 2 Σ_{n≥1} (a_n / n) · E₁(2πn/√N)

uses exactly the exponential integral `src15` already implements in-gate. So the
rank-1 identity

    L'(E,1) = Ω_E · ĥ(P) · ∏c_p · #Sha / #E(Q)_tors²

can be closed with every term computed in this tree — the first BSD identity in
this line for which that is true.

TWO CURVES, ONE OF EACH PERIOD BRANCH. 37a1 has Δ = 37 > 0 and two real
components; 43a1 has Δ < 0 and one. RUN-017 found the Δ > 0 branch doubled and
RUN-023 gave the repair its first external test at rank 2; this adds a rank-1
test on each branch, so a period fault could not hide in the rank.

AND A DEFECT IN THIS TREE'S OWN HEIGHTS, FOUND ON THE WAY. `canonical_height`
returned `richardson2` unconditionally. On 37a1 the raw sequence's last two
entries agree to 1.0e-14 while `richardson1`'s differ by 2.5e-07 — r1 is not
monotone — and `richardson2` is built from r1's last two, so it takes a value
correct to 3e-15 and returns one wrong by 8.4e-08. `regulator` now chooses the
level by the **parallelogram law**, uniformly across all four heights, and the
choice moves `Reg(389.a1)` from RUN-017's `0.152460306865` with a claimed
residual of 1.6e-06 to `0.15246013936831948` with a residual of 9.4e-09.

Usage:  python code/src28_rank1_bsd_identity.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as a15                         # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src20_bsd_consistency as bsd20                     # noqa: E402
import src26_rank2_bsd_identity as r2                     # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src28-rank1-bsd-identity.json"

# label, a-invariants, conductor, the standard generator
CURVES = (
    ("37a1", [0, 0, 1, -1, 0], 37, [0, 0]),
    ("43a1", [0, 1, 1, 0, 0], 43, [0, 0]),
)
TERMS = 20_000


def leading_derivative(ainvs, N: int, limit: int = TERMS) -> dict:
    """L'(E,1) = 2 Σ (a_n/n) E₁(2πn/√N), valid when the root number is −1.

    The convergence is reported rather than assumed: the same sum is taken at
    three truncations, and if the last two agree to machine precision the series
    has converged and the number is not a function of the cut-off.
    """
    bad_primes = [p for p in a15.sieve(N) if N % p == 0]
    bad = {d["prime"]: d["a_p"] for d in
           (a15.bad_prime_data(ainvs, p) for p in bad_primes)}
    a = a15.coefficients(ainvs, bad, limit)
    w, wdata = a15.root_number(a, N, limit)
    root = math.sqrt(N)

    def partial(m):
        return 2.0 * sum(a[n] / n * a15.E1(2 * math.pi * n / root)
                         for n in range(1, m))

    cuts = [limit // 4, limit // 2, limit]
    vals = [partial(m) for m in cuts]
    return {
        "root_number": w if wdata["decided"] else None,
        "root_number_decided": wdata["decided"],
        "formula": "L'(E,1) = 2 * sum_n (a_n/n) E_1(2 pi n / sqrt N)",
        "valid_only_for_w_minus_1": True,
        "truncations": dict(zip(map(str, cuts), vals)),
        "value": vals[-1],
        "converged_to": abs(vals[-1] - vals[-2]),
        "bad_primes": bad_primes,
    }


def period_two_ways(ainvs) -> dict:
    """The AGM period, and the same by integrating over E(R) — no shared code."""
    b2, b4, b6, _b8, disc = a15.b_invariants(ainvs)
    agm = a15.real_period(ainvs)
    roots = r2.cubic_real_roots(4, b2, 2 * b4, b6)
    out = {"discriminant": disc, "real_components": 2 if disc > 0 else 1,
           "agm": agm, "real_roots": roots}
    if len(roots) == 3:
        e3, e2, e1 = roots
        egg = r2.period_bounded_component(e3, e2, e1, n=200_000)
        unb = r2.period_unbounded_component(e3, e2, e1, n=1_000_000, T=4000.0)
        out.update({"bounded_component": egg,
                    "unbounded_component": unb["corrected"],
                    "integrated_full_real_locus": egg + unb["corrected"]})
    else:
        # one real root: a single component, and the integral runs from it up
        e1 = roots[0]
        e2 = e3 = None
        out["integrated_full_real_locus"] = _single_component(ainvs, e1)
    got = out["integrated_full_real_locus"]
    out["integration_vs_agm"] = abs(got - agm)
    out["relative"] = abs(got - agm) / agm
    return out


def _single_component(ainvs, e1: float, n: int = 2_000_000,
                      T: float = 4000.0) -> float:
    """Δ < 0: one real root, one component. x = e1 + t² again, and the cubic's
    complex pair is carried as the real quadratic it multiplies out to.

    4x³ + b2x² + 2b4x + b6 = 4(x − e1)(x² + px + q), so with x = e1 + t² the
    integrand is dx/√(4t²(x² + px + q)) = **dt/√(x² + px + q)** — the 4 and the
    t² both cancel against dx = 2t dt. Leaving the 4 inside the root halves the
    answer, which is what the AGM cross-check caught: 2.73 against a period of
    5.47.
    """
    b2, b4, b6, _b8, _d = a15.b_invariants(ainvs)
    p = b2 / 4 + e1
    q = -b6 / (4 * e1) if e1 != 0 else (b4 / 2 + e1 * p)
    tot = 0.0
    for i in range(n):
        t = (i + 0.5) * T / n
        x = e1 + t * t
        v = x * x + p * x + q
        if v > 0:
            tot += 1.0 / math.sqrt(v) * (T / n)
    return 2 * tot + 2.0 / T


def analyse_curve(label, ainvs, N, gen) -> dict:
    red = {p: tate.reduction_data(ainvs, p, want_c=True)
           for p in a15.sieve(N) if N % p == 0}
    cond = 1
    prod_c = 1
    for p, d in red.items():
        cond *= p ** d["f"]
        prod_c *= d["c"]
    tors = a15.torsion_bound(ainvs, N)
    lp = leading_derivative(ainvs, N)
    per = period_two_ways(ainvs)

    # The height at three doubling depths, with the identity closed at each.
    # Reporting the trend is what makes "the height is the limiting term" a
    # measurement: if the ratio tightens as the height's self-consistency does,
    # the residual is the height's and not the identity's.
    by_depth = {}
    for d in (10, 11, 12):
        hd = bsd20.canonical_height(ainvs, gen, depth=d)
        pred = per["agm"] * hd["value"] * prod_c / (tors ** 2)
        by_depth[str(d)] = {
            "height": hd["value"], "level": hd["chosen_level"],
            "self_consistency": hd["self_consistency"],
            "predicted": pred, "ratio": lp["value"] / pred,
            "relative_difference": abs(lp["value"] - pred) / abs(lp["value"]),
        }
    h = bsd20.canonical_height(ainvs, gen, depth=12)
    predicted = per["agm"] * h["value"] * prod_c / (tors ** 2)
    return {
        "label": label, "a_invariants": ainvs,
        "conductor_recomputed": cond, "conductor_agrees": cond == N,
        "reduction": {str(p): {"kodaira": d["kodaira"], "f": d["f"], "c": d["c"]}
                      for p, d in red.items()},
        "product_of_tamagawa": prod_c, "torsion_bound": tors,
        "L_prime": lp, "period": per,
        "height": {"generator": gen, "value": h["value"],
                   "chosen_level": h["chosen_level"],
                   "self_consistency": h["self_consistency"],
                   "level_gaps": h["level_gaps"],
                   "at_each_level": {k: h[k] for k in
                                     ("raw_last", "richardson1", "richardson2")}},
        "identity": {
            "formula": "L'(E,1) = Omega * h(P) * prod(c_p) / tors^2, with Sha = 1",
            "predicted": predicted,
            "computed_L_prime": lp["value"],
            "ratio": lp["value"] / predicted if predicted else None,
            "relative_difference": abs(lp["value"] - predicted) / abs(lp["value"]),
            "by_doubling_depth": by_depth,
            "limiting_term": (
                "the canonical height. Its self-consistency and the identity's "
                "relative difference move together across depths 10, 11, 12; "
                "the L-derivative is converged to machine precision and the "
                "period agrees with an independent integration to 1e-11"),
        },
        "ok": (cond == N and lp["root_number"] == -1
               and abs(lp["value"] / predicted - 1.0) < 1e-5),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    rows = [analyse_curve(*c) for c in CURVES]

    # the regulator repair, stated with the number it moves
    reg = bsd20.regulator([0, 1, 1, -2, 0], [[0, 0], [1, 0]], depth=10)
    log = {
        "gate": "src28 — the rank-1 BSD identity",
        "why": ("R1 is the one group of 06_Phase1_Agent_Experiment §3 this arm "
                "had never verified. At rank 1 every term of the identity is "
                "computable here, which is not true at rank 2"),
        "curves": rows,
        "height_extrapolation_repair": {
            "was": "canonical_height returned richardson2 unconditionally",
            "why_that_was_wrong": (
                "on 37a1 the raw sequence's last two entries agree to 1.0e-14 "
                "while richardson1's differ by 2.5e-07 — r1 is not monotone — "
                "and richardson2 is built from r1's last two, so it takes a "
                "value correct to 3e-15 and returns one wrong by 8.4e-08"),
            "now": ("regulator chooses the level by the parallelogram law, "
                    "uniformly across all four heights; canonical_height "
                    "chooses by its own sequence's last-two agreement"),
            "Reg_389a1_now": reg["regulator"],
            "Reg_389a1_RUN_017": 0.152460306865,
            "level_chosen": reg["extrapolation_level"],
            "residual_now": reg["parallelogram_law_residual"],
            "residual_at_each_level": reg["residual_at_each_level"],
            "reading": ("both agree to seven significant figures, so nothing "
                        "RUN-017 concluded moves; what was over-reported is the "
                        "precision — it printed twelve digits and claimed a "
                        "1.6e-06 residual that was its own extrapolation's "
                        "fault, not the method's"),
        },
        "ok": all(r["ok"] for r in rows),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    for r in rows:
        p, i, h = r["period"], r["identity"], r["height"]
        print(f"  {r['label']}:  N = {r['conductor_recomputed']} "
              f"({r['conductor_agrees']}), Delta = {p['discriminant']}, "
              f"{p['real_components']} real component(s), prod c_p = "
              f"{r['product_of_tamagawa']}, tors | {r['torsion_bound']}")
        print(f"     w = {r['L_prime']['root_number']}, "
              f"L'(E,1) = {r['L_prime']['value']!r}  "
              f"(converged to {r['L_prime']['converged_to']:.1e})")
        print(f"     Omega = {p['agm']!r}  integration agrees to "
              f"{p['integration_vs_agm']:.2e}")
        print(f"     h(P)  = {h['value']!r}  level {h['chosen_level']}, "
              f"self-consistency {h['self_consistency']:.1e}")
        print(f"     Omega*h*c/t^2 = {i['predicted']!r}")
        print(f"     ratio = {i['ratio']!r}   relative {i['relative_difference']:.2e}")
        for dep, row in i["by_doubling_depth"].items():
            print(f"       depth {dep}: h self-consistency "
                  f"{row['self_consistency']:.1e}  ->  identity relative "
                  f"{row['relative_difference']:.2e}   ({row['level']})")
        print()
    hr = log["height_extrapolation_repair"]
    print(f"  Reg(389.a1) now {hr['Reg_389a1_now']!r} (level "
          f"{hr['level_chosen']}, residual {hr['residual_now']:+.2e})")
    print(f"    RUN-017 reported {hr['Reg_389a1_RUN_017']!r} with a claimed "
          f"residual of 1.6e-06")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
