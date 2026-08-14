"""Independent recheck of Operation Translation Series — Paper 09 (and Paper 05's counts).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *Finite Certificate Frontier*, Paper 09 v0.1.1.

Why this paper is the one that bites
------------------------------------
Paper 09 §2 defines the coefficient stopping time

    sigma(n) = inf{ j >= 1 : T^j(n) < n }

which is *exactly* the quantity this arm's engine already measures for every
start it verifies. §50 then identifies the frontier function

    K(N) = min{ k : F_k(N) = empty } = max_{2 <= n <= N} sigma(n)

so the engine's `max_sigma` over an interval **is** Paper 09's K(N) for that
interval. That makes this the one place where a 549-billion-start measurement
and the paper's framework meet on the same number.

Independence: the referee is direct iteration of T, assuming no theorem of the
paper. Prefix affine data is taken from the Paper 02 referee route (symbolic
composition of the branch operators), not from any closed form the paper states.

Usage:  python code/ot_paper09_recheck.py [max_k] [block_exponent]
"""

from __future__ import annotations

import itertools
import json
import pathlib
import sys
from math import comb, floor, log

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ot_paper02_recheck import compose_affine, words

MAX_K_DEFAULT = 11
BLOCK_EXP_DEFAULT = 20


def T(x: int) -> int:
    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2


def sigma(n: int, cap: int) -> int | None:
    """inf{ j >= 1 : T^j(n) < n }, or None if it exceeds cap."""
    x = n
    for j in range(1, cap + 1):
        x = T(x)
        if x < n:
            return j
    return None


def parity_word(n: int, k: int) -> str:
    out, x = [], n
    for _ in range(k):
        out.append("U" if x % 2 else "D")
        x = T(x)
    return "".join(out)


def prefix_data(w: str) -> list[tuple[int, int, int]]:
    """[(j, u_j, b_j)] for every prefix, from the Paper 02 referee route."""
    out = []
    for j in range(1, len(w) + 1):
        A, B, Dn = compose_affine(w[:j])
        assert Dn == 2 ** j
        u = w[:j].count("U")
        assert A == 3 ** u
        out.append((j, u, B))
    return out


def hard_height(w: str) -> float | int:
    """Paper 09 §10: h(w) = min over contracting prefixes of floor(b_j / Delta_j)."""
    best = None
    for j, u, b in prefix_data(w):
        delta = 2 ** j - 3 ** u
        if delta > 0:
            v = b // delta
            best = v if best is None else min(best, v)
    return float("inf") if best is None else best


def residue_of(w: str) -> int:
    """Paper 03: r_w = -b_w * 3^{-u} mod 2^k."""
    k = len(w)
    A, b, Dn = compose_affine(w)
    u = w.count("U")
    return (-b * pow(3, -u, 2 ** k)) % 2 ** k


def check(rep: dict, name: str, ok: bool, detail: str = "") -> None:
    rep["checks"][name] = {"pass": bool(ok), **({"detail": detail} if detail else {})}
    if not ok:
        rep["failures"].append(name + (f": {detail}" if detail else ""))


def main() -> int:
    max_k = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_K_DEFAULT
    block_exp = int(sys.argv[2]) if len(sys.argv) > 2 else BLOCK_EXP_DEFAULT
    rep = {
        "tool": "ot_paper09_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 09 v0.1.1 (Neo.K)",
        "scope": "exact finite arithmetic; the global conjecture is untouched, as the paper states",
        "max_word_length": max_k,
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    # --- Theorem B: hard height, and Theorem 47.1 (2) <-> hard membership ---
    thmB = expanding_free = 0, 0
    thmB = True
    expanding_free = True
    words_checked = 0
    finite_h = infinite_h = 0
    for k in range(1, max_k + 1):
        for w in words(k):
            h = hard_height(w)
            r = residue_of(w)
            if h == float("inf"):
                infinite_h += 1
            else:
                finite_h += 1
            # §8: an expanding prefix imposes no upper bound at all
            for j, u, b in prefix_data(w):
                if 2 ** j - 3 ** u < 0:
                    # T^j(n) > n must hold for every positive admissible n
                    for a in range(0, 4):
                        n = r + 2 ** k * a
                        if n <= 0:
                            continue
                        x = n
                        for _ in range(j):
                            x = T(x)
                        if not x > n:
                            expanding_free = False
            # Theorem B: H_w = Omega_w cap [1, h(w)]
            for a in range(0, 8):
                n = r + 2 ** k * a
                if n <= 0:
                    continue
                if parity_word(n, k) != w:
                    thmB = False
                is_hard = True
                x = n
                for _ in range(k):
                    x = T(x)
                    if x < n:
                        is_hard = False
                        break
                predicted = True if h == float("inf") else n <= h
                if is_hard != predicted:
                    thmB = False
            words_checked += 1
    check(rep, "P09_ThmB_hard_height_characterises_the_hard_domain", thmB)
    check(rep, "P09_S8_expanding_prefix_imposes_no_height_bound", expanding_free)
    rep["counts"]["words_checked"] = words_checked
    rep["counts"]["words_with_finite_hard_height"] = finite_h
    rep["counts"]["words_with_infinite_hard_height"] = infinite_h

    # --- Theorem D: the cylinder quotient certificate -----------------------
    thmD = True
    quotient_cases = 0
    for k in range(1, max_k + 1):
        for w in words(k):
            A, b, _ = compose_affine(w)
            u = w.count("U")
            if 2 ** k <= 3 ** u:
                continue
            r = residue_of(w)
            m_w = (3 ** u * r + b) // 2 ** k
            for a in range(0, 12):
                n = r + 2 ** k * a
                if n <= 0:
                    continue
                x = n
                for _ in range(k):
                    x = T(x)
                # §22: T^k(n) < n  iff  (2^k - 3^u) a > m_w - r
                if ((2 ** k - 3 ** u) * a > m_w - r) != (x < n):
                    thmD = False
                if x != m_w + 3 ** u * a:
                    thmD = False
                quotient_cases += 1
    check(rep, "P09_ThmD_cylinder_quotient_threshold_is_an_exact_iff", thmD)
    rep["counts"]["quotient_certificate_cases"] = quotient_cases

    # --- sigma's absolute indexing, pinned against outside values -----------
    # The frontier and K(N) checks below only ever compare sigma against
    # itself, so a uniform off-by-one in sigma would leave every one of them
    # green. This anchor is what makes the indexing falsifiable: the values come
    # from collatz_ref.py, a separate file with its own independent walk.
    SIGMA_ANCHORS = {3: 4, 7: 7, 27: 59, 703: 81, 10087: 105}
    anchors_ok = all(sigma(n, 4000) == s for n, s in SIGMA_ANCHORS.items())
    check(rep, "P09_S2_sigma_indexing_matches_independent_values", anchors_ok,
          "" if anchors_ok else
          f"got {{n: sigma(n) for n in SIGMA_ANCHORS}} = "
          f"{ {n: sigma(n, 4000) for n in SIGMA_ANCHORS} }, expected {SIGMA_ANCHORS}")

    # --- Theorem C, §50, §56: frontier extinction, K(N), monotonicity -------
    N_small = 20000
    cap = 4000
    sigmas = {}
    for n in range(2, N_small + 1):
        s = sigma(n, cap)
        if s is None:
            rep["failures"].append(f"sigma({n}) exceeded cap {cap}")
            break
        sigmas[n] = s
    KN = max(sigmas.values())
    argmax = min(n for n, s in sigmas.items() if s == KN)

    # Theorem C: the frontier is empty at depth k iff every sigma <= k.
    thmC = True
    for k in range(1, KN + 2):
        frontier = set()
        for n, s in sigmas.items():
            if s > k:
                frontier.add(parity_word(n, k))
        empty = not frontier
        if empty != all(s <= k for s in sigmas.values()):
            thmC = False
    check(rep, "P09_ThmC_frontier_extinction_iff_all_sigma_at_most_k", thmC)

    # §50: K(N) = min{k : frontier empty} = max sigma
    least_empty = min(k for k in range(1, KN + 2)
                      if all(s <= k for s in sigmas.values()))
    check(rep, "P09_S50_K_of_N_equals_max_sigma", least_empty == KN,
          f"least empty depth {least_empty} vs max sigma {KN}")

    # §56: the unproved set shrinks monotonically
    mono = all(
        {n for n, s in sigmas.items() if s > k + 1} <= {n for n, s in sigmas.items() if s > k}
        for k in range(1, KN + 1)
    )
    check(rep, "P09_S56_hard_set_is_monotone_in_depth", mono)
    rep["measured"]["K_of_20000"] = {"value": KN, "attained_at": argmax}

    # --- §44: canonical residues stabilise at n once 2^k > n ---------------
    stabilise = True
    for n in range(2, 400):
        for k in range(1, 12):
            w = parity_word(n, k)
            if 2 ** k > n and residue_of(w) != n:
                stabilise = False
    check(rep, "P09_S44_canonical_residue_stabilises_at_n_once_2k_exceeds_n", stabilise)

    # --- Paper 05 binomial counts, and §24's boundary accounting -----------
    # Paper 05 / his validation.json: at k = 16 there are 58651 contracting
    # residue classes, m = floor(k log2/log3) = 10.
    alpha = log(2) / log(3)
    p05 = True
    p05_table = {}
    for k, (m_exp, a_exp) in {8: (5, 219), 12: (7, 3302), 16: (10, 58651),
                              20: (12, 910596)}.items():
        m = floor(alpha * k)
        A = sum(comb(k, u) for u in range(m + 1))
        p05_table[k] = {"m": m, "classes": A}
        if (m, A) != (m_exp, a_exp):
            p05 = False
    check(rep, "P05_contracting_residue_class_counts", p05)
    rep["counts"]["p05_contracting_classes"] = p05_table

    # §24 claims the 938413 strict-descent certificates are explained by the
    # 58651 contracting classes "plus finite boundary corrections". That prose
    # is turned into an exact accounting here.
    K_BLOCK, N_BLOCK = 16, 2 ** block_exp
    contracting_r = set()
    for r in range(2 ** K_BLOCK):
        u = parity_word(r, K_BLOCK).count("U")
        if 3 ** u < 2 ** K_BLOCK:
            contracting_r.add(r)
    in_contracting = strict = equal = ascent_in_contracting = 0
    exceptions = []
    for n in range(1, N_BLOCK):
        x = n
        for _ in range(K_BLOCK):
            x = T(x)
        if n % 2 ** K_BLOCK in contracting_r:
            in_contracting += 1
            if x > n:
                ascent_in_contracting += 1
                exceptions.append({"n": n, "why": "ascends despite a contracting class"})
        if x < n:
            strict += 1
        elif x == n:
            equal += 1
            exceptions.append({"n": n, "why": "equality, not strict descent"})

    check(rep, "P05_class_count_matches_58651", len(contracting_r) == 58651)
    check(rep, "P09_S24_strict_descent_count_is_938413", strict == 938413)
    # every strict descent must sit in a contracting class, and the shortfall
    # from the class-based count must be fully itemised
    shortfall = in_contracting - strict
    check(rep, "P09_S24_boundary_corrections_are_fully_itemised",
          shortfall == len(exceptions),
          f"shortfall {shortfall} vs {len(exceptions)} itemised")
    rep["measured"]["p09_s24_accounting"] = {
        "k": K_BLOCK,
        "domain": f"1 <= n < 2^{block_exp}",
        "contracting_classes": len(contracting_r),
        "starts_in_a_contracting_class": in_contracting,
        "strict_descents": strict,
        "equalities": equal,
        "ascents_inside_a_contracting_class": ascent_in_contracting,
        "shortfall": shortfall,
        "itemised_exceptions": exceptions[:10],
    }

    # --- §50 at the scale this arm actually measured ------------------------
    # The engine's `max_sigma` over an interval IS Paper 09's K(N) for that
    # interval, because §2's sigma and the engine's sigma are the same
    # definition. The archived [3, 2^40] coverage log therefore already
    # contains K(2^40). Here the argmax is re-derived by a Python bigint walk,
    # a different implementation from the Rust engine that produced it.
    # COLLATZ_TREE_ROOT lets the mutation drill run a mutant from a scratch
    # directory while still pointing at the real archived coverage log. Absence
    # of the log is a failure, not a skip: a check that quietly passes when its
    # evidence is missing is not a check.
    import os

    tree_root = pathlib.Path(
        os.environ.get("COLLATZ_TREE_ROOT", pathlib.Path(__file__).resolve().parent.parent))
    cov_path = tree_root / "data/gate-logs/coverage.json"
    if cov_path.exists():
        cov = json.loads(cov_path.read_text(encoding="utf-8"))
        n_star = cov["max_sigma"]["at"]
        claimed = cov["max_sigma"]["value"]
        x, first_below = n_star, None
        for j in range(1, claimed + 50):
            x = T(x)
            if x < n_star:
                first_below = j
                break
        check(rep, "P09_S50_engine_max_sigma_reproduced_independently",
              first_below == claimed,
              f"engine said {claimed}, bigint walk said {first_below}")
        rep["measured"]["K_of_2_pow_40"] = {
            "value": claimed,
            "attained_at": n_star,
            "source": "the archived [3, 2^40] exhaustive run, coverage.json",
            "odd_starts_measured": cov["odd_starts_checked"],
            "even_starts": "sigma = 1 by definition of the map, so the max over [2, N] is this",
            "independently_reproduced_by": "Python arbitrary-precision walk in this file",
            "note": (
                "This is Paper 09 §50's frontier function evaluated at N = 2^40. "
                "It is a measurement, not a bound: it says nothing about K(N) for "
                "larger N, and the paper is explicit that no uniform K exists to be found."
            ),
        }
    else:
        check(rep, "P09_S50_engine_max_sigma_reproduced_independently", False,
              "coverage.json absent; cannot link to the measured run")

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
