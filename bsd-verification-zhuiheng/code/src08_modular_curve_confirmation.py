"""Gate 08 — decide the isogeny columns in BOTH directions, through X₀(n).

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-006 settled the n=3 column exactly. RUN-007's reducibility sieve refuted
every curve the package calls False for n = 3, 5, 7 — and left every curve it
calls True surviving-but-unproved, because a sieve can refute and never confirm.
This gate is the first method in the line that is COMPLETE: it returns yes or
no, so it decides the positive claims and re-derives the negative ones by a
route independent of both earlier gates.

THE CRITERION. A quadratic twist carries a curve's rational subgroups with it,
so whether E/Q admits a rational n-isogeny depends only on j(E). X₀(3), X₀(5)
and X₀(7) have genus 0 with a rational point, hence a rational parametrisation
of the j-line:

    X₀(3):  j = (t+27)(t+3)³ / t
    X₀(5):  j = (t²+250t+3125)³ / t⁵
    X₀(7):  j = (t²+13t+49)(t²+245t+2401)³ / t⁷

so **E has a rational n-isogeny ⟺ j(E) = f_n(t) for some rational t ≠ 0**.

WHY THIS IS SEARCHABLE, given that j's denominator reaches 26 digits here.
Write f_n = N(t)/t^m with N monic of degree d, D = d − m, and N(0) = c₀ a pure
power of n (729 = 3⁶, 3125³ = 5¹⁵, 49·2401³ = 7¹⁴ — this is not a coincidence,
it is the cusp structure). Put t = u/v in lowest terms and clear denominators:

    j = A / (v^D · u^m),   A = Σ cᵢ uⁱ v^{d−i}.

A ≡ u^d (mod v) so gcd(A, v) = 1, and A ≡ c₀v^d (mod u) so every prime of
gcd(A, u) divides n. Feeding that back through j = num/den in lowest terms:

    **den = v^D · |u′|^m · n^w,     u′ = the n-free part of u.**

So the n-free part of den factors as v′^D · |u′|^m and NOTHING else — u and v are
pinned to a handful of possibilities, and the only freedom left is a power of n,
which the archimedean size of j bounds. |u′| ≤ den^{1/m} is 10^5.2 for n=5 at 26
digits and 270 for n=7, so those two need no factorisation at all. Every test is
integer: den·Σ cᵢ Uⁱ V^{d−i} = num·U^m·V^{D}.

THE METHOD IS VALIDATED BEFORE IT IS TRUSTED. `self_check()` runs curves whose
answer is known independently — 11a1 (two 5-isogenies), 49a1 (7, and j an
integer so den = 1), 26b1 (7), 14a1 and 26a1 (3), 37a1 (trivial isogeny class,
so all three must come back NO) — and refuses to run the census if any of them
comes out wrong. A gate that has not reproduced a known answer is not evidence.

n = 3 IS A CONTROL, not a result: RUN-006 decided all 4,062 curves exactly by
rational roots of ψ₃. Disagreement anywhere would indict one of the two gates
and be the finding, ahead of either verdict.

j = 0 and j = 1728 are set aside rather than answered — extra automorphisms make
the twist argument need care there — and reported as a carve-out.

Usage:  python code/src08_modular_curve_confirmation.py
"""

from __future__ import annotations

import csv
import json
import math
import pathlib
import random
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = (pathlib.Path("D:/我的研究/學術討論/論文/數學/BSD")
       / "BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12")
CENSUS = PKG / "results" / "algorithm1_removed_census.csv"
ARITH = PKG / "inputs" / "metadata" / "old_base_curve_arithmetic.json"
PRIOR6 = ROOT / "data" / "gate-logs" / "src06-three-isogeny-sieve.json"
OUT = ROOT / "data" / "gate-logs" / "src08-modular-curve.json"

NS = (3, 5, 7)
GAMMA_PAD = 5
MAX_CANDIDATES = 200_000
RHO_BUDGET = 400


# ---------------------------------------------------------------- polynomials

def polymul(a: list[int], b: list[int]) -> list[int]:
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            c[i + k] += x * y
    return c


def polypow(a: list[int], k: int) -> list[int]:
    out = [1]
    for _ in range(k):
        out = polymul(out, a)
    return out


# N(t) ascending, and m = the pole order at t = 0. N(0) is a pure power of n in
# every row — 2²⁴, 3⁶, 5¹⁵, 7¹⁴ — which is what makes the denominator bound work.
#
# n = 2 is here for the base's own selection criterion rather than the census's
# removal gate. It is sound for the same reason: E[2] is unchanged by a quadratic
# twist (χ_d lands in {±1}, and −1 = +1 in F₂), so a rational 2-isogeny — which
# for order 2 is exactly a rational 2-torsion point — again depends only on j.
PARAM: dict[int, tuple[list[int], int]] = {
    2: (polypow([256, 1], 3), 2),
    3: (polymul([27, 1], polypow([3, 1], 3)), 1),
    5: (polypow([3125, 250, 1], 3), 5),
    7: (polymul([49, 13, 1], polypow([2401, 245, 1], 3)), 7),
}


def j_invariant(ainvs: list[int]) -> Fraction | None:
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return None if disc == 0 else Fraction(c4 ** 3, disc)


# ------------------------------------------------------------- integer helpers

def log2_int(v: int) -> float:
    b = v.bit_length()
    return (b - 53) + math.log2(v >> (b - 53)) if b > 53 else math.log2(v)


def logn_frac(num: int, den: int, n: int) -> float:
    return (log2_int(abs(num)) - log2_int(den)) / math.log2(n)


def nth_root(x: int, k: int) -> int:
    """floor(x ** (1/k)) for x >= 0, exactly."""
    if x < 2:
        return x
    r = 1 << ((x.bit_length() + k - 1) // k)
    while True:
        nxt = ((k - 1) * r + x // r ** (k - 1)) // k
        if nxt >= r:
            return r
        r = nxt


def _is_probable_prime(v: int) -> bool:
    if v < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if v % p == 0:
            return v == p
    d, s = v - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, v)
        if x in (1, v - 1):
            continue
        for _ in range(s - 1):
            x = x * x % v
            if x == v - 1:
                break
        else:
            return False
    return True


def _rho(v: int) -> int | None:
    if v % 2 == 0:
        return 2
    for _ in range(24):
        x = random.randrange(2, v)
        y, c, d = x, random.randrange(1, v), 1
        steps = 0
        while d == 1 and steps < 2_000_000:
            x = (x * x + c) % v
            y = (y * y + c) % v
            y = (y * y + c) % v
            d = math.gcd(abs(x - y), v)
            steps += 1
        if 1 < d < v:
            return d
    return None


def factorise_over(v: int, primes) -> dict[int, int] | None:
    """Factorisation of v > 0 over a supplied prime set, or None if v does not
    factor completely over it.

    den(j) divides the discriminant, and for a minimal model the primes of the
    discriminant are known — so a 48-digit denominator needs no search at all,
    provided the supplied set is checked rather than trusted. None on any
    leftover cofactor: a partial answer here would silently shrink the candidate
    set and turn an unfinished search into a false 'no rational point'.
    """
    fac: dict[int, int] = {}
    for p in primes:
        while v % p == 0:
            fac[p] = fac.get(p, 0) + 1
            v //= p
    return fac if v == 1 else None


def factorise(v: int) -> dict[int, int] | None:
    """Full factorisation of v > 0, or None if it could not be completed.

    None rather than a partial answer: an incomplete factorisation yields an
    incomplete candidate set, which would silently turn an unfinished search
    into a false 'no rational point'.
    """
    fac: dict[int, int] = {}
    d = 2
    while d * d <= v and d < 1_000_000:
        while v % d == 0:
            fac[d] = fac.get(d, 0) + 1
            v //= d
        d += 1 if d == 2 else 2
    stack = [v] if v > 1 else []
    tries = 0
    while stack:
        w = stack.pop()
        if w == 1:
            continue
        if _is_probable_prime(w):
            fac[w] = fac.get(w, 0) + 1
            continue
        tries += 1
        if tries > RHO_BUDGET:
            return None
        f = _rho(w)
        if f is None:
            return None
        stack += [f, w // f]
    return fac


# --------------------------------------------------------------- the decision

def uv_pairs(dn: int, fac: dict[int, int] | None, D: int, m: int
             ) -> list[tuple[int, int]] | None:
    """All (|u'|, v') > 0 with v'^D · |u'|^m == dn, or None if not enumerable."""
    if dn == 1:
        return [(1, 1)]
    if fac is not None:
        pairs = [(1, 1)]
        for p, e in fac.items():
            grown = []
            for b in range(e // D + 1):
                rest = e - D * b
                if rest % m:
                    continue
                a = rest // m
                for ua, vb in pairs:
                    grown.append((ua * p ** a, vb * p ** b))
            pairs = grown
            if not pairs or len(pairs) > 4096:
                return pairs or []
        return pairs
    # No factorisation: enumerate the smaller side directly. |u'| <= dn^(1/m)
    # and v' <= dn^(1/D), so whichever exponent is larger gives a short loop.
    if m >= D:
        bound = nth_root(dn, m)
        if bound > 5_000_000:
            return None
        return [(k, dn // k ** m) for k in range(1, bound + 1)
                if dn % k ** m == 0]
    bound = nth_root(dn, D)
    if bound > 5_000_000:
        return None
    return [(dn // k ** D, k) for k in range(1, bound + 1) if dn % k ** D == 0]


def rational_points(j: Fraction, n: int, fac: dict[int, int] | None
                    ) -> list[Fraction] | None:
    """Every rational t ≠ 0 with f_n(t) == j, or None if the search was cut."""
    coeffs, m = PARAM[n]
    d = len(coeffs) - 1
    D = d - m
    num, den = j.numerator, j.denominator

    dn = den
    while dn % n == 0:
        dn //= n
    # The n-part must come out of the factorisation too, not just out of dn:
    # u' is by definition n-free, and leaving n in would ask uv_pairs to solve
    # D·b + m·a = v_n(den), which for other (D, m) can have no solution at all
    # and would return an empty candidate set — a false negative rather than a
    # slower search. (With D = 1 or m = 1, as here, it is always solvable, so
    # this changes no result in RUN-007; it removes the hazard, not a defect.)
    fac_n_free = None if fac is None else {p: e for p, e in fac.items() if p != n}
    pairs = uv_pairs(dn, fac_n_free, D, m)
    if pairs is None:
        return None

    # Archimedean bounds on |t|, so the remaining power of n is a finite range.
    tail = sum(abs(c) for c in coeffs[:-1])
    head = sum(abs(c) for c in coeffs[1:])
    hi_plain = math.log(max(2.0, 2.0 * tail), n)
    lo_plain = math.log(coeffs[0] / (2.0 * head), n)
    lj = logn_frac(num, den, n)
    hi = max(hi_plain, (math.log(2, n) + lj) / D)
    lo = min(lo_plain, (math.log(coeffs[0], n) - math.log(2, n) - lj) / m)

    found, tried = [], 0
    for ua, vb in pairs:
        offset = math.log(ua, n) - math.log(vb, n)
        g0 = math.floor(lo - offset) - GAMMA_PAD
        g1 = math.ceil(hi - offset) + GAMMA_PAD
        tried += 2 * (g1 - g0 + 1)
        if tried > MAX_CANDIDATES:
            return None
        for g in range(g0, g1 + 1):
            u, v = (ua * n ** g, vb) if g >= 0 else (ua, vb * n ** -g)
            for su in (u, -u):
                lhs = den * sum(c * su ** i * v ** (d - i)
                                for i, c in enumerate(coeffs))
                if lhs == num * su ** m * v ** D:
                    found.append(Fraction(su, v))
    return sorted(set(found))


# ---------------------------------------------------------- known-answer check

KNOWN: list[tuple[str, list[int], dict[int, bool]]] = [
    # label, a-invariants, the answer that is known independently of this gate.
    #
    # The n = 2 column is a rational 2-torsion point, checked by hand against the
    # 2-division polynomial 4x³ + b₂x² + 2b₄x + b₆ rather than assumed from the
    # shape of the isogeny class. 49a1 is why: it was entered here as False, the
    # gate said True, and the gate was right — 4x³ − 3x² − 8x − 4 vanishes at
    # x = 2, giving the rational point (2, −1). The expectation was corrected
    # after computing it, not after seeing the gate's answer.
    ("11a1", [0, -1, 1, -10, -20], {2: False, 3: False, 5: True, 7: False}),
    ("14a1", [1, 0, 1, 4, -6], {2: True, 3: True, 5: False, 7: False}),
    ("15a1", [1, 1, 1, -10, -10], {2: True, 3: False, 5: False, 7: False}),
    ("26a1", [1, 0, 1, -5, -8], {2: False, 3: True, 5: False, 7: False}),
    ("26b1", [1, -1, 1, -3, 3], {2: False, 3: False, 5: False, 7: True}),
    ("49a1", [1, -1, 0, -2, -1], {2: True, 3: False, 5: False, 7: True}),
    ("37a1", [0, 0, 1, -1, 0], {2: False, 3: False, 5: False, 7: False}),
]


def self_check() -> list[dict]:
    """Reproduce answers known independently. Raise rather than run on failure."""
    report = []
    for label, inv, expect in KNOWN:
        j = j_invariant(inv)
        assert j is not None, label
        fac = factorise(j.denominator) if j.denominator > 1 else {}
        for n, want in expect.items():
            pts = rational_points(j, n, fac)
            got = None if pts is None else bool(pts)
            report.append({"curve": label, "n": n, "expected": want,
                           "got": got,
                           "t": [] if not pts else [str(x) for x in pts[:4]]})
            if got is not want:
                raise SystemExit(
                    f"SELF-CHECK FAILED: {label} n={n} expected {want}, got "
                    f"{got}. The method is not validated; refusing to run it "
                    f"on the census.")
    return report


# ----------------------------------------------------------------------- main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    random.seed(20260908)
    for path in (CENSUS, ARITH):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")

    checks = self_check()
    print(f"  self-check: {len(checks)} known answers reproduced, 0 wrong")

    ainvs = {r["curve_label"]: r["ainvs"]
             for r in json.loads(ARITH.read_text(encoding="utf-8"))["records"]}
    rows = list(csv.DictReader(CENSUS.open(encoding="utf-8")))

    res = {n: {"agree_true": [], "agree_false": [], "disagree": [],
               "undecided": [], "special_j": []} for n in NS}
    unfactored = 0

    for idx, r in enumerate(rows):
        if idx and idx % 500 == 0:
            print(f"    … {idx:,}/{len(rows):,}", file=sys.stderr)
        label = r["curve_label"]
        inv = ainvs.get(label)
        if inv is None:
            continue
        j = j_invariant(inv)
        if j is None:
            continue
        fac = {} if j.denominator == 1 else factorise(j.denominator)
        if fac is None:
            unfactored += 1
        for n in NS:
            claim = r[f"has_isogeny_{n}"].strip().lower() == "true"
            if j in (Fraction(0), Fraction(1728)):
                res[n]["special_j"].append({"label": label, "j": str(j),
                                            "package_says": claim})
                continue
            pts = rational_points(j, n, fac)
            if pts is None:
                res[n]["undecided"].append({"label": label,
                                            "package_says": claim})
            elif bool(pts) == claim:
                key = "agree_true" if claim else "agree_false"
                entry = {"label": label, "t": [str(x) for x in pts[:4]]}
                res[n][key].append(entry if claim else label)
            else:
                res[n]["disagree"].append(
                    {"label": label, "package_says": claim,
                     "gate_says": bool(pts), "j": str(j),
                     "t": [str(x) for x in pts[:4]]})

    # Control: RUN-006 decided n=3 exactly by rational roots of ψ₃.
    control = {"ran": False}
    if PRIOR6.exists():
        prior = json.loads(PRIOR6.read_text(encoding="utf-8"))
        c6 = prior.get("counts", {})
        clean6 = (c6.get("EXACT_disagrees_with_the_package") == 0
                  and c6.get("REFUTED_package_says_true_but_no_rational_root") == 0)
        if clean6:
            decided3 = (len(res[3]["agree_true"]) + len(res[3]["agree_false"])
                        + len(res[3]["disagree"]))
            control = {
                "ran": True,
                "RUN006_verdict": "all 4,062 agree with the package, 0 refuted",
                "this_gate_decided": decided3,
                "this_gate_disagreements_with_package": len(res[3]["disagree"]),
                "consistent_with_RUN006": len(res[3]["disagree"]) == 0,
                "meaning": (
                    "RUN-006 and this gate share no arithmetic — one finds "
                    "rational roots of ψ₃, the other rational points on X₀(3). "
                    "Both agreeing with the package on every curve they decide "
                    "is a genuine cross-check; either disagreeing would indict "
                    "a gate before it indicted the census."),
            }

    counts = {}
    for n in NS:
        claims_true = sum(1 for r in rows
                          if r[f"has_isogeny_{n}"].strip().lower() == "true")
        counts[f"n={n}"] = {
            "package_says_true": claims_true,
            "CONFIRMED_true_rational_point_found": len(res[n]["agree_true"]),
            "CONFIRMED_false_no_rational_point": len(res[n]["agree_false"]),
            "DISAGREES_with_the_package": len(res[n]["disagree"]),
            "undecided_search_cut": len(res[n]["undecided"]),
            "set_aside_j_is_0_or_1728": len(res[n]["special_j"]),
        }

    log = {
        "gate": "src08_modular_curve_confirmation",
        "what_is_new": (
            "first complete method in this line — it decides yes AND no, so it "
            "closes the positive claims RUN-006 and RUN-007 could only leave "
            "unresolved, and re-derives the negative ones independently"),
        "criterion": (
            "a rational n-isogeny survives quadratic twist, so it depends only "
            "on j(E); X₀(3), X₀(5), X₀(7) are genus 0 with a rational point, so "
            "E has a rational n-isogeny iff j(E) = f_n(t) for some rational "
            "t ≠ 0"),
        "parametrisations": {
            "X0(3)": "j = (t+27)(t+3)^3 / t",
            "X0(5)": "j = (t^2+250t+3125)^3 / t^5",
            "X0(7)": "j = (t^2+13t+49)(t^2+245t+2401)^3 / t^7",
        },
        "why_a_26_digit_denominator_is_searchable": (
            "writing t = u/v in lowest terms gives j = A/(v^D u^m) with "
            "gcd(A,v) = 1 and every prime of gcd(A,u) dividing N(0), which is a "
            "pure power of n. Hence den(j) = v^D · |u'|^m · n^w with u' the "
            "n-free part of u — the n-free part of the denominator factors as "
            "v'^D·|u'|^m and nothing else, and the leftover power of n is "
            "bounded by the archimedean size of j"),
        "self_check": {
            "policy": ("the gate reproduces answers known independently before "
                       "it is allowed to run on the census, and exits rather "
                       "than report if any is wrong"),
            "results": checks,
        },
        "counts": counts,
        "control_n3_against_RUN006": control,
        "disagreements": {f"n={n}": res[n]["disagree"][:20] for n in NS},
        "undecided": {f"n={n}": res[n]["undecided"][:20] for n in NS},
        "set_aside": {f"n={n}": res[n]["special_j"][:20] for n in NS},
        "confirmed_sample": {f"n={n}": res[n]["agree_true"][:3] for n in NS},
        "denominators_not_factored": unfactored,
        "ok": all(not res[n]["disagree"] for n in NS),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print()
    for n in NS:
        c = counts[f"n={n}"]
        print(f"  n = {n}   package says true: {c['package_says_true']:>6,}")
        print(f"      CONFIRMED true  (rational point on X0({n}))  : "
              f"{c['CONFIRMED_true_rational_point_found']:>6,}")
        print(f"      CONFIRMED false (no rational point)         : "
              f"{c['CONFIRMED_false_no_rational_point']:>6,}")
        print(f"      DISAGREES with the package                  : "
              f"{c['DISAGREES_with_the_package']:>6,}")
        print(f"      undecided / set aside                       : "
              f"{c['undecided_search_cut']:>6,} / "
              f"{c['set_aside_j_is_0_or_1728']:,}")
    print()
    print(f"  control against RUN-006 (n=3) ran: {control['ran']}   "
          f"consistent: {control.get('consistent_with_RUN006')}")
    print(f"  denominators that would not factor: {unfactored:,}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
