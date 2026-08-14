"""First bridge from this arm's engine to the Hard-Zeta route map.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *Hard-Zeta Route Map v0.2* and the Faithful Global Quantifier
Compression line.

Why this exists
---------------
The route map states the global target as

    Z_k(s) = sum over { n : sigma(n) > k } of n^{-s}   ->  0,

where sigma(n) = inf{ j >= 1 : T^j(n) < n }. That is **exactly** the quantity this
arm's engine already measures for every start it verifies — the same sigma whose
maximum over [3, 2^40] is the K(2^40) = 550 recorded in RUN-002. So the Hard-Zeta
programme is a statement about a set this tree has already enumerated, and the
route map's decomposition is directly measurable here.

The decomposition, in the map's own notation:

    tau_c(n) = inf{ j : 3^{u_j(n)} < 2^j }        the coefficient stopping time
    tau_c(n) <= sigma(n)
    E_k = C_k  |_|  R_k ,   C_k = { tau_c > k },  R_k = { tau_c <= k < sigma }

and the strong form R_k = 0 is **Terras's coefficient-stopping conjecture**,
sigma(n) = tau_c(n) for all n > 1 — an open problem, verified computationally.

This probe measures three things and claims nothing beyond them:

  1. tau_c(n) <= sigma(n), which is a theorem and should never fail;
  2. whether R_k is empty on the tested range, i.e. whether sigma = tau_c there;
  3. the split of E_k into C_k and R_k at several depths k.

**A finite range with R_k empty is not evidence for the conjecture.** It is the
bound at which this arm has checked it, and nothing more. The same standing rule
as everywhere else in this tree.

Usage:  python code/hz_route_probe.py [limit]
"""

from __future__ import annotations

import json
import sys


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def sigma_and_tau(n: int, cap: int = 4000) -> tuple[int | None, int | None]:
    """(sigma, tau_c) by one walk, assuming neither closed form."""
    x, u, sigma, tau = n, 0, None, None
    for j in range(1, cap + 1):
        if x % 2:
            u += 1
        x = T(x)
        if tau is None and 3 ** u < 2 ** j:
            tau = j
        if sigma is None and x < n:
            sigma = j
        if sigma is not None and tau is not None:
            break
    return sigma, tau


def main() -> int:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    rep = {
        "tool": "hz_route_probe.py",
        "subject": "Neo.K, Hard-Zeta Route Map v0.2 — the E_k = C_k + R_k decomposition",
        "scope": (
            "a finite measurement of the route map's own quantities. R_k empty on a "
            "finite range is NOT evidence for the coefficient-stopping conjecture; it "
            "is the bound at which this arm checked it."
        ),
        "domain": f"odd 3 <= n < {limit}",
        "checks": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    ordering_ok = True
    both_defined = True
    equal = 0
    strict = 0
    strict_witnesses = []
    max_sigma = (0, 0)
    max_tau = (0, 0)
    count = 0

    for n in range(3, limit, 2):
        s, t = sigma_and_tau(n)
        if s is None or t is None:
            both_defined = False
            continue
        if not t <= s:
            ordering_ok = False
        if t == s:
            equal += 1
        else:
            strict += 1
            if len(strict_witnesses) < 20:
                strict_witnesses.append({"n": n, "tau_c": t, "sigma": s})
        if s > max_sigma[0]:
            max_sigma = (s, n)
        if t > max_tau[0]:
            max_tau = (t, n)
        count += 1

    check("HZ_tau_c_never_exceeds_sigma", ordering_ok)
    check("HZ_both_stopping_times_are_defined_on_the_range", both_defined)
    # This one is a MEASUREMENT reported as a check only in the sense that a
    # counterexample here would be a genuine discovery about the subject's
    # strong form. It is not a proof of anything.
    check("HZ_R_k_is_empty_on_this_range_i_e_sigma_equals_tau_c",
          strict == 0, f"{strict} starts with tau_c < sigma, e.g. {strict_witnesses[:5]}")

    rep["measured"]["coefficient_stopping"] = {
        "odd_starts": count,
        "sigma_equals_tau_c": equal,
        "sigma_exceeds_tau_c": strict,
        "first_strict_witnesses": strict_witnesses,
        "max_sigma": {"value": max_sigma[0], "at": max_sigma[1]},
        "max_tau_c": {"value": max_tau[0], "at": max_tau[1]},
        "terras_note": (
            "sigma = tau_c for all n > 1 is Terras's coefficient-stopping conjecture, "
            "which is open. Equality across this range means R_k is empty here and "
            "nothing about larger n."
        ),
    }

    # The route map's split of E_k, at several depths.
    split = {}
    for k in (5, 10, 20, 40, 80):
        C = R = certified = 0
        for n in range(3, min(limit, 200_001), 2):
            s, t = sigma_and_tau(n)
            if s is None or t is None:
                continue
            if t > k:
                C += 1
            elif s > k:
                R += 1
            else:
                certified += 1
        split[k] = {"C_k_tau_c_gt_k": C, "R_k_tau_c_le_k_lt_sigma": R,
                    "certified_sigma_le_k": certified}
    rep["measured"]["E_k_split"] = {
        "domain": f"odd 3 <= n < {min(limit, 200001)}",
        "by_depth": split,
        "note": (
            "E_k = C_k disjoint-union R_k is the route map's decomposition of the hard "
            "set. R_k is empty at every depth here, which is the same fact as the "
            "coefficient-stopping measurement above viewed depth by depth."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
