"""Gate 15 — the Phase 2 anchor: r_an = 0 for 696.e1, and the BSD quantities under it.

數學戰士「墜衡」 / AMRAL Research Lab.

Phase 2's family theorem rests on one base curve satisfying full BSD, and
`21_Base_BSD_Anchor_Repair` records how that was fixed:

    v0.3 used Banwait–Huang's historical remark that Miller verified full BSD
    for **most** rank 0/1 curves below conductor 5000 — from which 696 < 5000
    does not follow. The repair cites Creutz–Miller Theorem 1.1 instead:
    N < 5000 and r_an ≤ 1 ⟹ full BSD. For 696.e1, N = 696 and r_an = 0.

That is a careful repair, and it moves the weight onto two arithmetic facts:
**N = 696** and **r_an = 0**. Both are computable, and RUN-009 checked neither —
it verified the discriminant, the reduction types and the non-semistability, but
took the conductor from the note and never touched the analytic rank.

WHAT THIS GATE COMPUTES, AND HOW IT AVOIDS ASSUMING WHAT IT IS CHECKING.

  a_n — from point counts over F_p by Legendre symbols, with a_p at bad primes
  taken from the reduction type (+1 split multiplicative, −1 non-split, 0
  additive) and the Hecke recursion for prime powers.

  **the root number w** — not assumed. The naive formula L(E,1) = 2Σ(a_n/n)e^{−2πn/√N}
  is only valid for w = +1, and 37a1 shows why that matters: it has rank 1, so
  L(E,1) = 0, yet that sum is 0.19. The sign is instead *measured*, by evaluating
  the smoothed functional-equation formula for Λ(2) with both w = ±1 and keeping
  whichever matches the Dirichlet series Σ a_n n^{−2}, which converges absolutely
  there and needs no functional equation at all.

  **the conductor** — also measured, by the same comparison. The functional
  equation only closes with the right N, so running the match over candidate
  conductors selects one. This verifies N = 696 without Tate's algorithm.

  Ω, the real period — by AGM on the 2-division cubic, both components when
  Δ > 0.

  #E(Q)_tors — by the gcd of #E(F_p) over good primes, which bounds it.

  c_p at the multiplicative primes — v_p(Δ) when split, gcd(2, v_p(Δ)) when not.

THE SELF-CHECK IS THE POINT. Every piece is validated on curves whose answers are
fixed outside this gate before 696.e1 is touched: 11a1 (w = +1, Ω = 1.26920930…,
torsion Z/5, c_11 = 5, Ш = 1, so L/Ω must be exactly 1/5), 37a1 (rank 1, w = −1),
389a1 (rank 2, w = +1, so L(E,1) = 0 despite w = +1 — the case that separates
"the sum vanishes" from "the sign kills it").

WHAT IS NOT COMPUTED HERE: c_2. The reduction at 2 is additive, and its Tamagawa
number needs Tate's algorithm, which this gate does not implement. So the round
reports c_2·#Ш as one quantity and says which factorisations of it are possible,
rather than asserting either factor.

Usage:  python code/src15_phase2_anchor.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src07_isogeny_reducibility_sieve as red7            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src15-phase2-anchor.json"

ANCHOR = ("696.e1 / 696b1", [0, 1, 0, 8, -16], 696)
EULER_GAMMA = 0.5772156649015328606
TERMS = 20_000
CONDUCTOR_CANDIDATES = (174, 348, 696, 1044, 1392, 2088, 4176)


# ----------------------------------------------------------------- special fns

def E1(x: float) -> float:
    """Exponential integral E₁(x) for x > 0 — series below 2, Lentz above."""
    if x < 2.0:
        s, term = -EULER_GAMMA - math.log(x), 1.0
        for k in range(1, 60):
            term *= -x / k
            s -= term / k
        return s
    tiny = 1e-300
    b, c, d = x + 1.0, 1e300, 1.0 / (x + 1.0)
    h = d
    for i in range(1, 300):
        a = -i * i
        b += 2.0
        d = 1.0 / (a * d + b) if abs(a * d + b) > tiny else 1.0 / tiny
        c = b + a / c if abs(b + a / c) > tiny else tiny
        delta = c * d
        h *= delta
        if abs(delta - 1.0) < 1e-17:
            break
    return h * math.exp(-x)


def agm(x: float, y: float) -> float:
    for _ in range(100):
        x, y = (x + y) / 2.0, math.sqrt(x * y)
        if abs(x - y) <= 1e-17 * abs(x):
            break
    return x


# ------------------------------------------------------------- curve arithmetic

def b_invariants(ainvs):
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return b2, b4, b6, b8, disc


def real_cubic_roots(b2, b4, b6):
    """Roots of 4x³ + b₂x² + 2b₄x + b₆, largest first."""
    b, c, d = b2 / 4.0, b4 / 2.0, b6 / 4.0
    p = c - b * b / 3.0
    q = 2 * b ** 3 / 27.0 - b * c / 3.0 + d
    if -(4 * p ** 3 + 27 * q * q) > 0:
        r = math.sqrt(-p / 3.0)
        th = math.acos(3 * q / (2 * p * r)) / 3.0
        return sorted((2 * r * math.cos(th - 2 * math.pi * k / 3.0) - b / 3.0
                       for k in range(3)), reverse=True)
    u = math.copysign(1.0, -q) * (abs(q) / 2 + math.sqrt(q * q / 4
                                                         + p ** 3 / 27)) ** (1 / 3.0)
    return [u - p / (3 * u) - b / 3.0]


def real_period(ainvs) -> float:
    """∫ over E(R) of the Néron differential — both components when Δ > 0.

    The Δ > 0 branch carried a spurious factor of 2 until RUN-017. Its value had
    only ever been checked against itself: RUN-014's drill froze Ω(37a1) as a
    regression baseline taken from this function, so the branch was never
    compared with anything outside it. Numerical integration over E(R) — added
    to the drill at the same time — puts the two conventions apart at once.

    Everything RUN-014 and RUN-015 concluded is on curves with Δ < 0, where the
    two agree exactly, so none of it moves.
    """
    b2, b4, b6, _b8, disc = b_invariants(ainvs)
    roots = real_cubic_roots(b2, b4, b6)
    if disc > 0:
        e1, e2, e3 = roots
        return 2 * math.pi / agm(math.sqrt(e1 - e3), math.sqrt(e1 - e2))
    e1 = roots[0]
    p_ = b2 / 4.0 + e1
    q_ = b4 / 2.0 + e1 * p_
    r = math.sqrt(e1 * e1 + p_ * e1 + q_)
    return 2 * math.pi / agm(2 * math.sqrt(r), math.sqrt(2 * r + 2 * e1 + p_))


def sieve(n: int) -> list[int]:
    f = bytearray([1]) * (n + 1)
    f[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if f[i]:
            f[i * i::i] = bytearray(len(f[i * i::i]))
    return [i for i in range(n + 1) if f[i]]


def point_count(ainvs, p: int) -> int:
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    t = 1
    for x in range(p):
        t += 1 + red7.legendre(((a1 * x + a3) ** 2
                                + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % p, p)
    return t


def bad_prime_data(ainvs, p: int) -> dict:
    """Reduction type at a bad prime, by counting singular and smooth points."""
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    total, singular = 1, 0
    for x in range(p):
        for y in range(p):
            if (y * y + a1 * x * y + a3 * y
                    - (x ** 3 + a2 * x * x + a4 * x + a6)) % p:
                continue
            total += 1
            if ((a1 * y - (3 * x * x + 2 * a2 * x + a4)) % p == 0
                    and (2 * y + a1 * x + a3) % p == 0):
                singular += 1
    smooth = total - singular
    kind = ("split multiplicative" if smooth == p - 1 else
            "non-split multiplicative" if smooth == p + 1 else "additive")
    return {"prime": p, "smooth_points": smooth, "type": kind,
            "a_p": 1 if kind.startswith("split") else
                   (-1 if kind.startswith("non-split") else 0)}


def coefficients(ainvs, bad: dict[int, int], limit: int) -> list[int]:
    primes = sieve(limit)
    ap = {p: (bad[p] if p in bad else point_count_ap(ainvs, p)) for p in primes}
    a = [0] * (limit + 1)
    a[1] = 1
    for p in primes:
        pk, prev2, prev1 = p, 1, ap[p]
        while pk <= limit:
            a[pk] = prev1
            prev2, prev1 = prev1, ap[p] * prev1 - (0 if p in bad else p * prev2)
            pk *= p
    for n in range(2, limit + 1):
        if a[n]:
            continue
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                q, m = 1, n
                while m % p == 0:
                    m //= p
                    q *= p
                a[n] = a[q] * a[m]
                break
    return a


def point_count_ap(ainvs, p: int) -> int:
    return p + 1 - point_count(ainvs, p)


# ----------------------------------------------------------------- the L-series

def smoothed_and_direct(a, N: int, limit: int):
    """Λ(2)-based L(E,2) for w = ±1, and the Dirichlet series it is matched to."""
    rN = math.sqrt(N)
    head = tail = 0.0
    for n in range(1, limit + 1):
        if not a[n]:
            continue
        x = 2 * math.pi * n / rN
        if x > 700:
            break
        head += a[n] * (1 + x) * math.exp(-x) / (x * x)
        tail += a[n] * E1(x)
    pref = 4 * math.pi ** 2 / N
    direct = sum(a[n] / (n * n) for n in range(1, limit + 1))
    return {1: pref * (head + tail), -1: pref * (head - tail)}, direct


def root_number(a, N: int, limit: int):
    """The sign, with an error estimate the series makes about itself.

    The residual |smoothed − direct| is NOT an error estimate: it can be small
    by accident, and on 795b1 it was 2.1e-4 against a candidate gap of 8.6e-3,
    which reads as a confident answer for no reason. What the comparison is
    actually limited by is how far the Dirichlet series still has to move, so
    that is measured directly — the sum is evaluated at limit, limit/2 and
    limit/4, and the spread between them is the error. A sign is only reported
    as decided when the gap between the two candidates clears it.
    """
    cand, direct = smoothed_and_direct(a, N, limit)
    partials = [sum(a[n] / (n * n) for n in range(1, m + 1))
                for m in (limit // 4, limit // 2, limit)]
    drift = max(abs(partials[i] - partials[-1]) for i in range(2))
    w = min(cand, key=lambda k: abs(cand[k] - direct))
    gap = abs(cand[-w] - direct) - abs(cand[w] - direct)
    return w, {"candidates": cand, "dirichlet_series": direct,
               "residual": abs(cand[w] - direct),
               "gap_to_the_other_sign": abs(cand[-w] - direct),
               "separation": gap,
               "series_drift": drift,
               "decided": gap > 20 * max(drift, 1e-15),
               "partial_sums": partials}


def truncation_scale(N: int, terms: int) -> float:
    """exp(−2π·M/√N) — the size of the first dropped term of the L(1) sum."""
    return math.exp(-2 * math.pi * terms / math.sqrt(N))


def l_value_at_one(a, N: int, w: int, limit: int | None = None):
    """L(E,1) for w = +1, or None when the available terms do not converge.

    The number of terms needed grows like √N, so a fixed limit silently
    under-converges once the conductor is large: at N ≈ 1.2 × 10⁶ a 600-term
    sum drops a first term of size 0.03. The guard is on the quantity that
    actually matters — the size of the first dropped term — and returns None
    rather than a number when it is not small.
    """
    if w != 1:
        return 0.0
    M = (len(a) - 1) if limit is None else min(limit, len(a) - 1)
    if truncation_scale(N, M) > 1e-14:
        return None
    rN = math.sqrt(N)
    return 2.0 * sum(a[n] / n * math.exp(-2 * math.pi * n / rN)
                     for n in range(1, M + 1) if a[n])


def torsion_bound(ainvs, N: int) -> int:
    g = 0
    for p in sieve(120):
        if p > 2 and N % p:
            g = math.gcd(g, point_count(ainvs, p))
    return g


def analyse(label: str, ainvs, N: int, limit: int = TERMS) -> dict:
    bad_primes = [p for p in sieve(N) if N % p == 0]
    bad = {d["prime"]: d["a_p"] for d in
           (bad_prime_data(ainvs, p) for p in bad_primes)}
    details = [bad_prime_data(ainvs, p) for p in bad_primes]
    a = coefficients(ainvs, bad, limit)
    w, wdata = root_number(a, N, limit)
    omega = real_period(ainvs)
    L1 = l_value_at_one(a, N, w) if wdata["decided"] else None
    tail = truncation_scale(N, limit)
    tors = torsion_bound(ainvs, N)
    _b2, _b4, _b6, _b8, disc = b_invariants(ainvs)
    tamagawa = {}
    for d in details:
        p, v = d["prime"], 0
        m = abs(disc)
        while m % p == 0:
            m //= p
            v += 1
        if d["type"] == "split multiplicative":
            tamagawa[str(p)] = {"c_p": v, "from": "v_p(Δ), split"}
        elif d["type"] == "non-split multiplicative":
            tamagawa[str(p)] = {"c_p": 1 if v % 2 else 2,
                                "from": "gcd(2, v_p(Δ)), non-split"}
        else:
            tamagawa[str(p)] = {"c_p": None,
                                "from": "additive — needs Tate's algorithm"}
    known = [t["c_p"] for t in tamagawa.values() if t["c_p"] is not None]
    prod_known = 1
    for c in known:
        prod_known *= c
    ratio = (L1 / omega) if (omega and L1 is not None) else None
    return {
        "label": label, "a_invariants": ainvs, "conductor_used": N,
        "discriminant": disc,
        "bad_primes": details,
        "root_number": w if wdata["decided"] else None,
        "root_number_undecided": not wdata["decided"],
        "root_number_evidence": wdata,
        "real_period": omega,
        "L_at_1": L1,
        "terms_used": limit,
        "first_dropped_term_scale": tail,
        "L_at_1_converged": L1 is not None,
        "analytic_rank_is_zero": (wdata["decided"] and w == 1
                                  and L1 is not None and abs(L1) > 1e-9),
        "torsion_bound_gcd": tors,
        "tamagawa": tamagawa,
        "product_of_known_tamagawa": prod_known,
        "L_over_Omega": ratio,
        "residual_unknown_factor": (
            None if ratio is None or not tors
            else ratio * tors * tors / prod_known),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    # ---- self-check on curves fixed outside this gate ---------------------
    checks = []
    for label, inv, N, want_w, want_ratio in (
            ("11a1", [0, -1, 1, -10, -20], 11, +1, 0.2),
            ("37a1", [0, 0, 1, -1, 0], 37, -1, 0.0),
            ("389a1", [0, 1, 1, -2, 0], 389, +1, 0.0)):
        r = analyse(label, inv, N)
        ok_w = r["root_number"] == want_w
        ok_ratio = abs((r["L_over_Omega"] or 0.0) - want_ratio) < 1e-9
        checks.append({"curve": label, "expected_w": want_w,
                       "got_w": r["root_number"], "w_ok": ok_w,
                       "expected_L_over_Omega": want_ratio,
                       "got_L_over_Omega": r["L_over_Omega"],
                       "ratio_ok": ok_ratio,
                       "real_period": r["real_period"],
                       "torsion_bound": r["torsion_bound_gcd"]})
        if not (ok_w and ok_ratio):
            raise SystemExit(
                f"SELF-CHECK FAILED on {label}: w={r['root_number']} "
                f"(want {want_w}), L/Ω={r['L_over_Omega']} (want {want_ratio}). "
                "Refusing to run on the anchor.")
    print(f"  self-check: {len(checks)} curves reproduced, 0 wrong")

    # ---- the conductor, selected rather than assumed ----------------------
    label, inv, N = ANCHOR
    bad_primes = [p for p in sieve(N) if N % p == 0]
    bad = {d["prime"]: d["a_p"] for d in
           (bad_prime_data(inv, p) for p in bad_primes)}
    a = coefficients(inv, bad, TERMS)
    conductor_scan = []
    for cand in CONDUCTOR_CANDIDATES:
        cands, direct = smoothed_and_direct(a, cand, TERMS)
        w = min(cands, key=lambda k: abs(cands[k] - direct))
        conductor_scan.append({"N": cand, "best_w": w,
                               "residual": abs(cands[w] - direct)})
    picked = min(conductor_scan, key=lambda e: e["residual"])
    runner_up = min((e for e in conductor_scan if e["N"] != picked["N"]),
                    key=lambda e: e["residual"])

    # ---- the anchor -------------------------------------------------------
    r = analyse(label, inv, N)

    log = {
        "gate": "src15_phase2_anchor",
        "subject": ("21_Base_BSD_Anchor_Repair — the repair moves the weight of "
                    "the Phase 2 family theorem onto N = 696 and r_an = 0 for "
                    "696.e1, both of which are computable"),
        "why_the_root_number_is_measured_not_assumed": (
            "L(E,1) = 2Σ(a_n/n)e^{−2πn/√N} holds only for w = +1. 37a1 has rank "
            "1, so L(E,1) = 0, and that same sum is 0.19 — a nonzero sum is no "
            "evidence of a nonzero L-value. The sign is instead read off by "
            "matching the smoothed Λ(2) against Σ a_n n^{−2}, which converges "
            "absolutely and uses no functional equation"),
        "self_check": checks,
        "conductor_selected_by_the_functional_equation": {
            "candidates": conductor_scan,
            "selected": picked,
            "runner_up": runner_up,
            "separation": (runner_up["residual"] / picked["residual"]
                           if picked["residual"] else None),
            "meaning": ("the functional equation only closes with the right "
                        "conductor, so this verifies N = 696 without Tate's "
                        "algorithm"),
        },
        "anchor": r,
        "bsd_at_rank_zero": {
            "formula": "L(E,1)/Ω = #Ш · ∏c_p / #E(Q)_tors²  when the rank is 0",
            "L_over_Omega": r["L_over_Omega"],
            "torsion": r["torsion_bound_gcd"],
            "c_3_times_c_29": r["product_of_known_tamagawa"],
            "c_2_times_Sha": r["residual_unknown_factor"],
            "reading": ("with trivial torsion and c_3 = c_29 = 1, the measured "
                        "ratio forces c_2 · #Ш = 1; both are positive integers, "
                        "so c_2 = 1 and Ш is trivial. This is a consistency "
                        "reading under the BSD formula that Creutz–Miller "
                        "supplies for this curve, not an independent proof of "
                        "either factor"),
        },
        "not_computed_here": {
            "c_2": ("the reduction at 2 is additive and its Tamagawa number "
                    "needs Tate's algorithm, which this gate does not "
                    "implement"),
            "Sha": "not computed; only the product c_2·#Ш is measured",
        },
        "ok": (r["analytic_rank_is_zero"]
               and picked["N"] == 696 and picked["best_w"] == 1
               and abs((r["L_over_Omega"] or 0) - 1.0) < 1e-8),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    for c in checks:
        print(f"    {c['curve']:6s} w = {c['got_w']:+d} (want "
              f"{c['expected_w']:+d})   L/Ω = {c['got_L_over_Omega']:.12f} "
              f"(want {c['expected_L_over_Omega']})   Ω = {c['real_period']:.10f}")
    print()
    print("  conductor selected by the functional equation:")
    for e in conductor_scan:
        mark = "  <== selected" if e["N"] == picked["N"] else ""
        print(f"    N = {e['N']:>5}   w = {e['best_w']:+d}   residual "
              f"{e['residual']:.3e}{mark}")
    print(f"    separation from the runner-up: "
          f"{log['conductor_selected_by_the_functional_equation']['separation']:.0f}×")
    print()
    print(f"  {label}")
    for d in r["bad_primes"]:
        print(f"    p = {d['prime']:>3}   {d['type']:<26} a_p = {d['a_p']:+d}")
    print(f"    root number w        = {r['root_number']:+d}")
    print(f"    real period Ω        = {r['real_period']:.12f}")
    print(f"    L(E,1)               = {r['L_at_1']:.12f}")
    print(f"    r_an = 0             : {r['analytic_rank_is_zero']}")
    print(f"    #E(Q)_tors           = {r['torsion_bound_gcd']}")
    print(f"    c_3 · c_29           = {r['product_of_known_tamagawa']}")
    print(f"    L/Ω                  = {r['L_over_Omega']:.12f}")
    print(f"    c_2 · #Ш             = {r['residual_unknown_factor']:.12f}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
