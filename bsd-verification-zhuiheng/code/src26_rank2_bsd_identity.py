"""Gate 26 — the rank-2 BSD identity at 389.a1, and the real period that carries it.

數學戰士「墜衡」 / AMRAL Research Lab.

`BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1` §6 uses 389.a1 as its
canonical rank-2 wall probe and records three numbers:

    L''(E,1)/2! ≈ 0.759316500288426770...
    Reg(E)      ≈ 0.15246017794314375...
    prod c_p = 1,   #E(Q)_tors = 1,   BSD-inferred analytic Sha = 1.

With those Tamagawa and torsion values the rank-2 BSD formula collapses to

    L''(E,1)/2!  =  Omega_E * Reg(E),

so the three numbers determine a real period, and **this arm can supply that
period independently**. It is the sharpest available test of RUN-017's finding.

WHY THIS CURVE AND THIS ROUND. RUN-017 found that this tree's real period was
wrong by a factor of two on the Delta > 0 branch, for three rounds, and nothing
caught it because RUN-014's drill had frozen Omega(37a1) taken from the same
function. Everything already reported survived, because the anchor and every
twist have Delta < 0 — so the fix was never tested against an independent number
on a curve that actually uses the repaired branch. **389.a1 has Delta = 389 > 0**,
E(R) has two components, and the rank-2 identity above is an external number
that closes or does not.

THE PERIOD IS COMPUTED THREE WAYS, sharing no code between them: the AGM in
src15, a Chebyshev-substituted integral over the bounded (egg) component, and a
t = e1 + u^2 substituted integral over the unbounded one whose tail is corrected
by its own closed form 2/T. If the three agree, the convention question — whether
BSD's Omega here is one component or the whole real locus — is answered by
measurement rather than by convention.

Usage:  python code/src26_rank2_bsd_identity.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as a15                         # noqa: E402
import src20_bsd_consistency as bsd20                     # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src26-rank2-bsd-identity.json"

AINVS = [0, 1, 1, -2, 0]                  # 389.a1
GENS = [[0, 0], [1, 0]]                   # P, Q — the basis v1.2 fixes

# §6 of the rank-uniform document, quoted
DOC_L2 = 0.759316500288426770
DOC_REG = 0.15246017794314375
DOC_TAMAGAWA = 1
DOC_TORSION = 1


# --------------------------------------------------------------------------
# the real locus
# --------------------------------------------------------------------------

def cubic_real_roots(a3, a2, a1, a0, iters: int = 800):
    """Real roots of a cubic by Durand–Kerner, sorted. No library, no src15."""
    zs = [complex(0.4, 0.9) ** k for k in (1, 2, 3)]
    f = lambda z: ((a3 * z + a2) * z + a1) * z + a0     # noqa: E731
    for _ in range(iters):
        nxt = []
        for i, z in enumerate(zs):
            den = a3
            for j, w in enumerate(zs):
                if i != j:
                    den *= (z - w)
            nxt.append(z - f(z) / den)
        zs = nxt
    return sorted(z.real for z in zs if abs(z.imag) < 1e-9)


def period_bounded_component(e3, e2, e1, n: int = 400_000) -> float:
    """2·∫ over the egg [e3, e2] of dx/√(4(x−e1)(x−e2)(x−e3)).

    The substitution x = midpoint + halfwidth·cos θ turns the inverse-square-root
    endpoint singularities into the Jacobian's sin θ, which cancels them exactly.
    """
    lo, hi = e3, e2
    mid, half = (lo + hi) / 2, (hi - lo) / 2
    tot = 0.0
    for i in range(n):
        th = (i + 0.5) * math.pi / n
        x = mid + half * math.cos(th)
        v = 4 * (x - e1) * (x - e2) * (x - e3)
        if v > 0:
            tot += half * math.sin(th) / math.sqrt(v) * (math.pi / n)
    return 2 * tot


def period_unbounded_component(e3, e2, e1, n: int = 2_000_000,
                               T: float = 4000.0) -> dict:
    """2·∫ over [e1, ∞) of dx/√(4(x−e1)(x−e2)(x−e3)), with its tail in closed form.

    Putting x = e1 + t² gives dx/√(4·t²·(x−e2)(x−e3)) = dt/√((x−e2)(x−e3)); the
    endpoint singularity cancels identically rather than numerically. The tail
    beyond T behaves like ∫ dt/t² = 1/T, doubled for the two signs of y, so the
    truncation is corrected by exactly 2/T — and that the correction lands the
    answer on the bounded component's value is itself a check on the
    substitution.
    """
    tot = 0.0
    for i in range(n):
        t = (i + 0.5) * T / n
        x = e1 + t * t
        tot += 1.0 / math.sqrt((x - e2) * (x - e3)) * (T / n)
    truncated = 2 * tot
    return {"truncated_at_T": truncated, "T": T,
            "analytic_tail_2_over_T": 2.0 / T,
            "corrected": truncated + 2.0 / T}


def analyse() -> dict:
    b2, b4, b6, b8, disc = a15.b_invariants(AINVS)
    # y² + a1xy + a3y = … ⟺ (2y + a1x + a3)² = 4x³ + b2x² + 2b4x + b6
    roots = cubic_real_roots(4, b2, 2 * b4, b6)
    e3, e2, e1 = roots
    egg = period_bounded_component(e3, e2, e1)
    unb = period_unbounded_component(e3, e2, e1)
    agm = a15.real_period(AINVS)
    full = egg + unb["corrected"]

    reg10 = bsd20.regulator(AINVS, GENS, depth=10)
    reg = reg10["regulator"]

    def identity(omega, regulator):
        pred = omega * regulator * DOC_TAMAGAWA / (DOC_TORSION ** 2)
        return {"omega": omega, "regulator": regulator, "predicted_L2": pred,
                "document_L2": DOC_L2, "ratio": DOC_L2 / pred,
                "relative_difference": abs(DOC_L2 - pred) / DOC_L2}

    with_doc_reg = identity(agm, DOC_REG)
    with_our_reg = identity(agm, reg)
    with_integrated = identity(full, DOC_REG)

    return {
        "gate": "src26 — the rank-2 BSD identity at 389.a1",
        "curve": {"a_invariants": AINVS, "discriminant": disc,
                  "discriminant_positive": disc > 0,
                  "real_components": 2 if disc > 0 else 1,
                  "note": ("Delta > 0 is the branch RUN-017 found doubled. Every "
                           "result this arm had already published used Delta < 0, "
                           "so the repair had never been tested against an "
                           "external number on a curve that uses it")},
        "real_locus": {
            "cubic_real_roots": roots,
            "bounded_egg_component": egg,
            "unbounded_component": unb,
            "the_two_components_agree_to": abs(egg - unb["corrected"]),
            "full_real_locus": full,
            "agm_from_src15": agm,
            "integration_vs_agm": abs(full - agm),
            "relative": abs(full - agm) / agm,
            "one_component_over_agm": egg / agm,
            "which_convention_the_identity_needs": (
                "the FULL real locus. One component is exactly half the AGM "
                "value, so a gate that integrated the identity component alone "
                "would be out by the same factor of two RUN-017 removed"),
        },
        "regulator": {
            "ours_depth_10": reg,
            "parallelogram_residual": reg10.get("parallelogram_residual"),
            "document": DOC_REG,
            "difference": abs(reg - DOC_REG),
            "inside_our_own_residual": abs(reg - DOC_REG) < 2e-6,
        },
        "rank_2_bsd_identity": {
            "formula": "L''(E,1)/2! = Omega * Reg * prod(c_p) / #tors^2, with Sha = 1",
            "with_the_documents_regulator": with_doc_reg,
            "with_our_regulator": with_our_reg,
            "with_the_integrated_period": with_integrated,
            "limiting_term": ("our regulator, not our period: substituting the "
                              "document's regulator closes the identity to "
                              "machine precision while substituting ours moves "
                              "it by about 1e-6, which is the depth-10 "
                              "regulator's own accuracy"),
        },
        "what_this_does_not_settle": {
            "independence": ("whether the document's three numbers were computed "
                             "independently of each other cannot be read off the "
                             "document. What is established here is that THIS "
                             "arm's period, computed from the curve and sharing "
                             "no code with the source, satisfies the identity "
                             "their L'' and Reg define"),
            "analytic_rank": ("no second derivative of L is computed here. The "
                              "document itself marks analytic rank 2 as still "
                              "requiring an independent rigorous certificate"),
            "sha": ("Sha = 1 is BSD-inferred in the document and assumed here to "
                    "state the identity. Nothing below computes Sha"),
        },
        "ok": (abs(full - agm) / agm < 1e-3
               and abs(egg / agm - 0.5) < 1e-6
               and with_doc_reg["relative_difference"] < 1e-12
               and abs(reg - DOC_REG) < 2e-6),
    }


def main() -> int:
    log = analyse()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    rl = log["real_locus"]
    print(f"  Delta = {log['curve']['discriminant']} > 0 — "
          f"{log['curve']['real_components']} real components")
    print(f"  real roots {[round(r, 10) for r in rl['cubic_real_roots']]}")
    print(f"  egg component        {rl['bounded_egg_component']!r}")
    print(f"  unbounded component  {rl['unbounded_component']['corrected']!r}  "
          f"(truncated at T = {rl['unbounded_component']['T']:.0f}, tail "
          f"{rl['unbounded_component']['analytic_tail_2_over_T']:.1e} added in "
          f"closed form)")
    print(f"    the two agree to   {rl['the_two_components_agree_to']:.3e}")
    print(f"  full real locus      {rl['full_real_locus']!r}")
    print(f"  AGM (src15)          {rl['agm_from_src15']!r}")
    print(f"    integration vs AGM {rl['integration_vs_agm']:.3e} "
          f"(relative {rl['relative']:.1e});  one component / AGM = "
          f"{rl['one_component_over_agm']:.10f}")
    print()
    rg = log["regulator"]
    print(f"  Reg ours (depth 10)  {rg['ours_depth_10']!r}")
    print(f"  Reg document         {rg['document']!r}   differ by "
          f"{rg['difference']:.3e}, inside our residual: "
          f"{rg['inside_our_own_residual']}")
    print()
    idn = log["rank_2_bsd_identity"]
    for key in ("with_the_documents_regulator", "with_our_regulator",
                "with_the_integrated_period"):
        d = idn[key]
        print(f"  {key:32s} ratio {d['ratio']!r}  "
              f"(rel {d['relative_difference']:.2e})")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
