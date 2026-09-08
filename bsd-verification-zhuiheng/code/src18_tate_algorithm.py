"""Gate 18 — Tate's algorithm: 40,749 conductors from scratch, and the c_2 two rounds owed.

數學戰士「墜衡」 / AMRAL Research Lab.

Three debts come due together.

**RUN-014 and RUN-015 both carved out c_2.** The anchor 696.e1 has additive
reduction at 2, and its Tamagawa number needs Tate's algorithm. Both rounds
reported c_2·#Ш as one quantity and said so rather than splitting it.

**The census's conductor column has never been checked.** RUN-004 recomputed
40,749 discriminants and 135,787 valuations; RUN-008 verified the factorisations
*of the discriminant*. Nothing has recomputed a conductor. RUN-014 verified one —
N = 696, by which conductor makes the functional equation close — and that is a
completely different route from this one, which is why both are worth having.

**Phase 2 routes on Kodaira types.** `01_Odd_Additive_Period_Barrier` names a
Manin-constant condition that excludes "additive potentially ordinary of Kodaira
type II, III, or IV", and `05_Kodaira_Prefilters_and_NoGo` states an exact no-go
for additive **potentially multiplicative** reduction while formally refusing any
Kodaira-only inference. Neither is checkable without the types.

TWO PLACES WHERE THIS IMPLEMENTATION SEARCHES INSTEAD OF QUOTING A FORMULA, and
both are deliberate. Step 2 moves the singular point of the reduction to the
origin; for p = 2 and 3 that point is found by scanning the nine or four points
of the reduced curve rather than by a closed form, because those are exactly the
cases whose closed forms are easy to misremember — and a first version of this
gate did misremember one, returning f = 4 for 696.e1 at p = 2 where the answer is
3. Step 7 needs a model with p|a₁, p²|a₂, p³|a₃, p⁴|a₄, p⁶|a₆; the transformation
achieving it is found by searching a bounded box of (r, s, t). A search that
succeeds is exact, and one that fails says so instead of returning a number.

THE VALIDATION IS THE POINT. The conductor is ∏ p^{f_p}, and the base carries
40,749 of them. Recomputing every one is at once the largest test this
implementation can be given and a verification of a column nothing has touched.

Usage:  python code/src18_tate_algorithm.py
"""

from __future__ import annotations

import collections
import itertools
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src18-tate.json"

COMPONENTS = {"I0": 1, "II": 1, "III": 2, "IV": 3, "I0*": 5,
              "IV*": 7, "III*": 8, "II*": 9}


def valuation(n: int, p: int) -> int:
    if n == 0:
        return 10 ** 9
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def invariants(a1, a2, a3, a4, a6):
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return b2, b4, b6, b8, c4, c6, disc


def translate(a, r, s, t):
    """(x, y) → (x + r, y + s·x + t)."""
    a1, a2, a3, a4, a6 = a
    return [a1 + 2 * s,
            a2 - s * a1 + 3 * r - s * s,
            a3 + r * a1 + 2 * t,
            a4 - s * a3 + 2 * r * a2 - (t + r * s) * a1 + 3 * r * r - 2 * s * t,
            a6 + r * a4 + r * r * a2 + r ** 3 - t * a3 - t * t - r * t * a1]


def quad_roots(A, B, C, p):
    """Roots of A·x² + B·x + C over F_p, as a list (A may be 0)."""
    return [x for x in range(p) if (A * x * x + B * x + C) % p == 0]


def cubic_roots(b, c, d, p):
    """Roots of T³ + bT² + cT + d over F_p."""
    return [x for x in range(p)
            if (x ** 3 + b * x * x + c * x + d) % p == 0]


def singular_point(a, p):
    """The singular point of the reduction mod p, found rather than derived."""
    a1, a2, a3, a4, a6 = (v % p for v in a)
    for x in range(p):
        for y in range(p):
            if (y * y + a1 * x * y + a3 * y
                    - (x ** 3 + a2 * x * x + a4 * x + a6)) % p:
                continue
            if ((a1 * y - (3 * x * x + 2 * a2 * x + a4)) % p == 0
                    and (2 * y + a1 * x + a3) % p == 0):
                return x, y
    return None


# What step 7 actually needs: its cubic is T³ + (a₂/p)T² + (a₄/p²)T + (a₆/p³),
# and the branches below it read a₃/p², a₄/p³, a₆/p⁴. A first version demanded
# p²|a₂, p³|a₃, p⁴|a₄, p⁶|a₆ — a normalisation that does not exist for 696.e1 at
# p = 2, which is how the requirement was found to be wrong rather than the search.
WANT = (1, 1, 2, 3, 4)


def normalise_for_step7(a, p):
    """A model with p|a1, p|a2, p²|a3, p³|a4, p⁴|a6, or None if none exists.

    The conditions are triangular — a1' depends only on s, a2' on (r, s), a3' on
    (r, s, t) — so the search is three nested loops with a prune after each
    rather than a product over all three. A simultaneous digit-by-digit lift was
    the first version and it branched p³ per digit, which at p = 3 is 19,683
    and at p = 29 is hopeless; nothing needed that, because p ≥ 5 never reaches
    here (see reduction_data).

    r runs to p⁴ because a6' contains r³ and (r + p³k)³ ≡ r³ only modulo p³.

    The conditions are exactly what makes step 7's cubic integral — p|a2 for its
    T² coefficient, p²|a4 for its T coefficient, p³|a6 for its constant — and no
    more. A stronger normalisation (p³|a4, p⁴|a6) was tried first and is a trap:
    it forces the last two coefficients to vanish mod p, so the cubic becomes
    T²(T + b) and **type I0* can never be returned**. Thirteen hand-picked
    curves and two thousand census conductors all passed anyway, because none of
    them was I0* at 2 or 3.
    """
    a1, a2, a3, a4, a6 = a
    for s in range(p * p):
        if (a1 + 2 * s) % p:
            continue
        b = translate(a, 0, s, 0)
        for r in range(p ** 4):
            if (b[1] + 3 * r) % p:
                continue
            c = translate(b, r, 0, 0)
            if c[0] % p or c[1] % p:
                continue
            for t in range(p ** 3):
                d = translate(c, 0, 0, t)
                if (d[2] % p ** 2 == 0 and d[3] % p ** 2 == 0
                        and d[4] % p ** 3 == 0):
                    return d
    return None


def tate(ainvs, p: int) -> dict:
    """Kodaira type, conductor exponent, Tamagawa number and minimality at p."""
    a = [int(v) for v in ainvs]
    scalings = 0
    while True:
        b2, b4, b6, b8, c4, c6, disc = invariants(*a)
        n = valuation(disc, p)
        if n == 0:
            return {"kodaira": "I0", "f": 0, "c": 1, "v_disc": 0,
                    "scalings": scalings}

        sing = singular_point(a, p)
        if sing is None:
            raise RuntimeError(f"no singular point mod {p} for {ainvs}")
        a = translate(a, sing[0], 0, sing[1])
        b2, b4, b6, b8, c4, c6, disc = invariants(*a)

        # ---- step 3: multiplicative -------------------------------------
        if c4 % p != 0:
            split = bool(quad_roots(1, a[0] % p, (-a[1]) % p, p))
            c = n if split else (2 if n % 2 == 0 else 1)
            return {"kodaira": f"I{n}", "f": 1, "c": c, "v_disc": n,
                    "split_multiplicative": split, "scalings": scalings}

        # ---- steps 4, 5, 6 ------------------------------------------------
        if a[4] % (p * p) != 0:
            return {"kodaira": "II", "f": n, "c": 1, "v_disc": n,
                    "scalings": scalings}
        if b8 % (p ** 3) != 0:
            return {"kodaira": "III", "f": n - 1, "c": 2, "v_disc": n,
                    "scalings": scalings}
        if b6 % (p ** 3) != 0:
            c = 3 if quad_roots(1, a[2] // p, -(a[4] // (p * p)), p) else 1
            return {"kodaira": "IV", "f": n - 2, "c": c, "v_disc": n,
                    "scalings": scalings}

        # ---- step 7 --------------------------------------------------------
        nz = normalise_for_step7(a, p)
        if nz is None:
            raise RuntimeError(f"step-7 normalisation not found for {ainvs} "
                               f"at p={p}")
        a = nz
        b = a[1] // p
        cc = a[3] // (p * p)
        d = a[4] // (p ** 3)
        w = (27 * d * d - b * b * cc * cc + 4 * b ** 3 * d
             - 18 * b * cc * d + 4 * cc ** 3)
        x = 3 * cc - b * b

        if w % p != 0:                       # three distinct roots
            return {"kodaira": "I0*", "f": n - 4,
                    "c": 1 + len(cubic_roots(b, cc, d, p)),
                    "v_disc": n, "scalings": scalings}

        if x % p != 0:                       # one double root → I_m*
            return _i_m_star(a, p, n, b, cc, d, scalings)

        # triple root
        rt = cubic_roots(b, cc, d, p)
        a = translate(a, p * (rt[0] if rt else 0), 0, 0)
        res = _after_triple(a, p, n, scalings)
        if res != "NON_MINIMAL":
            return res
        a = [a[0] // p, a[1] // p ** 2, a[2] // p ** 3,
             a[3] // p ** 4, a[4] // p ** 6]
        scalings += 1


def _i_m_star(a, p, n, b, cc, d, scalings):
    """The double-root branch: types I_m*."""
    if p == 2:
        r = cc % 2
    elif p == 3:
        r = (b * cc) % 3
    else:
        r = ((b * cc - 9 * d) * pow(2 * (3 * cc - b * b), -1, p)) % p
    a = translate(a, r * p, 0, 0)
    m, mx, my = 1, p * p, p * p
    while m < 400:
        a3t = a[2] // my
        a6t = a[4] // (mx * my)
        if (a3t * a3t + 4 * a6t) % p != 0:
            c = 4 if quad_roots(1, a3t, -a6t, p) else 2
            return {"kodaira": f"I{m}*", "f": n - m - 4, "c": c,
                    "v_disc": n, "scalings": scalings}
        if p == 2:
            t = my * (a6t % 2)
        else:
            t = my * ((-a3t * pow(2, -1, p)) % p)
        a = translate(a, 0, 0, t)
        my *= p
        m += 1
        a2t = a[1] // p
        a3t = a[2] // my
        a4t = a[3] // (p * mx)
        a6t = a[4] // (mx * my)
        if (a4t * a4t - 4 * a2t * a6t) % p != 0:
            c = 4 if quad_roots(a2t, a4t, a6t, p) else 2
            return {"kodaira": f"I{m}*", "f": n - m - 4, "c": c,
                    "v_disc": n, "scalings": scalings}
        if p == 2:
            r = mx * ((a6t * (a2t if a2t % 2 else 1)) % 2)
        else:
            r = mx * ((-a4t * pow(2 * a2t, -1, p)) % p)
        a = translate(a, r, 0, 0)
        mx *= p
        m += 1
    raise RuntimeError("I_m* chain did not terminate")


def _after_triple(a, p, n, scalings):
    """Types IV*, III*, II*, or a non-minimal model."""
    a3t = a[2] // (p * p)
    a6t = a[4] // (p ** 4)
    if (a3t * a3t + 4 * a6t) % p != 0:
        c = 3 if quad_roots(1, a3t, -a6t, p) else 1
        return {"kodaira": "IV*", "f": n - 6, "c": c, "v_disc": n,
                "scalings": scalings}
    if p == 2:
        t = -(a6t % 2) * p * p
    else:
        t = -p * p * ((a3t * pow(2, -1, p)) % p)
    a = translate(a, 0, 0, t)
    if a[3] % (p ** 4) != 0:
        return {"kodaira": "III*", "f": n - 7, "c": 2, "v_disc": n,
                "scalings": scalings}
    if a[4] % (p ** 6) != 0:
        return {"kodaira": "II*", "f": n - 8, "c": 1, "v_disc": n,
                "scalings": scalings}
    return "NON_MINIMAL"


def kodaira_from_valuations(vc4, vc6, vd):
    """Kodaira type for p ≥ 5, from (v(c4), v(c6), v(Δ)) alone.

    Away from 2 and 3 the type is a function of those three valuations, and the
    conductor exponent of every additive type is 2 — there is no wild
    ramification. That makes the whole step-7 machinery unnecessary for p ≥ 5,
    which matters: its search branches p³ per p-adic digit, so at p = 29 it is
    24,389 branches deep and the conductor never needed it.
    """
    if vd == 0:
        return "I0", 0
    if vc4 == 0:
        return f"I{vd}", 1
    if vd == 2:
        return "II", 2
    if vd == 3:
        return "III", 2
    if vd == 4:
        return "IV", 2
    if vd == 6 and vc4 >= 2 and vc6 >= 3:
        return "I0*", 2
    if vd == 8:
        return "IV*", 2
    if vd == 9:
        return "III*", 2
    if vd == 10:
        return "II*", 2
    if vc4 == 2 and vc6 == 3:
        return f"I{vd - 6}*", 2
    return "additive", 2


def normalise_odd(a, p, prec=4):
    """Step-7 normalisation for p ≥ 5, solved rather than searched.

    Away from 2 and 3 the three conditions are linear and 2, 3 are invertible,
    so s, r and t are determined outright: s kills a1, r kills a2, t kills a3,
    each to p^prec.
    """
    M = p ** prec
    inv2, inv3 = pow(2, -1, M), pow(3, -1, M)
    b = translate(a, 0, (-a[0] * inv2) % M, 0)
    c = translate(b, (-b[1] * inv3) % M, 0, 0)
    return translate(c, 0, 0, (-c[2] * inv2) % M)


def tamagawa_additive_odd(ainvs, p, kodaira):
    """c_p for an additive type at p ≥ 5.

    II, III, II* and III* have a fixed component group and are settled before
    step 7 ever runs, so they must not be routed through its normalisation:
    49a1 at p = 7 is type III and no such normalisation exists for it. Only
    I0* needs the cubic.
    """
    if kodaira in ("II", "II*"):
        return 1
    if kodaira in ("III", "III*"):
        return 2
    a = [int(v) for v in ainvs]
    sing = singular_point(a, p)
    if sing is None:
        return None
    a = normalise_odd(translate(a, sing[0], 0, sing[1]), p)
    if any(a[i] % p ** e for i, e in ((0, 1), (1, 1), (2, 2), (3, 2), (4, 3))):
        return None
    b, cc, d = (a[1] // p) % p, (a[3] // (p * p)) % p, (a[4] // p ** 3) % p
    if kodaira == "I0*":
        return 1 + len(cubic_roots(b, cc, d, p))
    return None


def reduction_data(ainvs, p: int, want_c: bool = False) -> dict:
    """Type, conductor exponent and (where computed) c_p, by the cheap route.

    p = 2 and p = 3 go through the full algorithm because they are the only
    primes where the conductor exponent is not determined by the reduction type.
    """
    if p in (2, 3):
        return tate(ainvs, p)
    _b2, _b4, _b6, _b8, c4, c6, disc = invariants(*ainvs)
    vd = valuation(disc, p)
    if vd == 0:
        return {"kodaira": "I0", "f": 0, "c": 1, "v_disc": 0}
    if c4 % p != 0:
        # Split iff -c6 is a square mod p. The alternative — move the singular
        # point to the origin and read the tangent slopes — needs to FIND that
        # point, and the only implementation here scans p x p pairs. At a
        # conductor prime near 500,000 that is 2.5e11 operations for a fact one
        # Legendre symbol settles, and it is what made a first run of this gate
        # take longer than the whole census had taken to check.
        split = pow((-c6) % p, (p - 1) // 2, p) == 1
        return {"kodaira": f"I{vd}", "f": 1,
                "c": vd if split else (2 if vd % 2 == 0 else 1),
                "v_disc": vd, "split_multiplicative": split}
    kod, f = kodaira_from_valuations(valuation(c4, p), valuation(c6, p), vd)
    # c is computed only on request: the normalisation works modulo p⁴, and at
    # a conductor prime near 500,000 that is a 23-digit modulus to invert for a
    # number the conductor never needs.
    return {"kodaira": kod, "f": f,
            "c": tamagawa_additive_odd(ainvs, p, kod) if want_c else None,
            "v_disc": vd}


def conductor(ainvs, primes) -> int:
    N = 1
    for p in primes:
        N *= p ** reduction_data(ainvs, p)["f"]
    return N


def potential_reduction(ainvs, p: int) -> str:
    """v_p(j) < 0 is potentially multiplicative; otherwise potentially good."""
    j = x0n.j_invariant(ainvs)
    if j is None:
        return "singular"
    vj = ((valuation(j.numerator, p) if j.numerator else 10 ** 9)
          - valuation(j.denominator, p))
    return "potentially multiplicative" if vj < 0 else "potentially good"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    print("gate 18 is a library; RUN-016 drives it from src19")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
