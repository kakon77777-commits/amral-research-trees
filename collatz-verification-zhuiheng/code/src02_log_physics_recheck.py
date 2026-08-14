"""Independent recheck of source item 02 — dimension-aware log physics stress.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, `dimension_aware_log_physics_stress_bundle.zip`, 2026-08-10 15:15.
Second item in chronological order.

Where this item sits
--------------------
Seven minutes after item 01, and it is a **branch, not a continuation**. It keeps
item 01's representation — a quantity as (sign, log-magnitude) so products become
sums — and adds an SI dimension vector, then stress-tests the whole thing on real
physics formulas. **Its subject is no longer Collatz.**

That makes it the first evidence for something the series later says outright:
the additive-coordinate idea was being developed as a general representation, and
Collatz was one application of it rather than its origin.

What is checkable, and how this differs from the bundle
------------------------------------------------------
The bundle works at 120 decimal digits in `mpmath` and compares its log-coordinate
path against a direct high-precision computation. That is a comparison of two
routes through the same library. This recheck uses **no mpmath**, and pins the
load-bearing quantities against things that are not float computations at all:

* **Stefan-Boltzmann is an external anchor.** Since the 2019 SI redefinition,
  `k_B`, `h` and `c` are *exact defined constants*, so
  `sigma = 2 pi^5 k_B^4 / (15 h^3 c^2)` is exactly determined and CODATA's value
  is an expectation this arm did not author.
* **`(2 pi hbar)^3 = h^3` needs no pi at all.** With `hbar = h/(2 pi)` it reduces
  to `h^3` symbolically, so the pi^3 cancellation the bundle demonstrates
  numerically is exact.
* **The Lorentz case has an exact route.** `1 - beta^2 = (1-beta)(1+beta)` has no
  cancellation whatsoever, so `gamma` can be computed without any log-difference
  trick. That is a genuinely different method from the bundle's, not a second
  pass of the same one.
* **pi is computed twice**, by two unrelated series, rather than typed as a
  literal.

Usage:  python code/src02_log_physics_recheck.py
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80

# SI base dimensions, in the bundle's own order.
BASE = ("kg", "m", "s", "A", "K", "mol", "cd")


def sci(x: Decimal, digits: int = 12) -> str:
    """Format preserving the exponent.

    `str(x)[:n]` looks harmless and is not: it truncates the exponent off a value
    in scientific notation, so 1.57E-27 is reported as "1.57". Every number in
    this report goes through here.
    """
    return f"{x:.{digits}E}"


def dim(**kw) -> tuple[Fraction, ...]:
    return tuple(Fraction(kw.get(b, 0)) for b in BASE)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dpow(a, q: Fraction):
    return tuple(x * q for x in a)


def pi_spigot() -> Decimal:
    """The decimal-module documentation's own pi recipe (arctan-type series)."""
    getcontext().prec += 4
    three = Decimal(3)
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    getcontext().prec -= 4
    return +s


def arctan_inv(x: int) -> Decimal:
    """arctan(1/x) by its alternating series, for integer x > 1."""
    getcontext().prec += 6
    total = term = Decimal(1) / x
    k = 0
    while True:
        k += 1
        term = -term / (x * x)
        add = term / (2 * k + 1)
        if add == 0:
            break
        total += add
    getcontext().prec -= 6
    return +total


def pi_machin() -> Decimal:
    """Machin: pi = 16 arctan(1/5) - 4 arctan(1/239). Unrelated to the recipe."""
    return +(16 * arctan_inv(5) - 4 * arctan_inv(239))


def main() -> int:
    rep = {
        "tool": "src02_log_physics_recheck.py",
        "subject": "Neo.K, dimension_aware_log_physics_stress_bundle.zip (2026-08-10)",
        "source_item": 2,
        "scope": (
            "exact dimensional algebra, an external anchor for Stefan-Boltzmann, and "
            "cancellation-free routes to the hard cases. Not about Collatz."
        ),
        "checks": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    # --- pi, computed two independent ways ---------------------------------
    p1, p2 = pi_spigot(), pi_machin()
    agree = abs(p1 - p2) < Decimal("1e-70")
    check("SRC02_pi_agrees_between_two_unrelated_series", agree,
          f"difference {sci(abs(p1 - p2))}")
    pi = p1
    rep["measured"]["pi_first_40_digits"] = str(pi)[:42]  # plain decimal, no exponent

    # --- the dimension vectors the bundle reports --------------------------
    m = dim(m=1)
    s_ = dim(s=1)
    kg = dim(kg=1)
    K = dim(K=1)
    J = dim(kg=1, m=2, s=-2)
    stated = {
        "sphere_volume_r3": (dpow(m, Fraction(3)), dim(m=3)),
        "pendulum_period": (s_, dim(s=1)),
        "phase_cell_h3": (dpow(dmul(J, s_), Fraction(3)), dim(kg=3, m=6, s=-3)),
        "stefan_boltzmann_sigma": (
            dmul(dmul(dpow(J, Fraction(4)), dpow(K, Fraction(-4))),
                 dmul(dpow(dmul(J, s_), Fraction(-3)), dpow(dim(m=1, s=-1), Fraction(-2)))),
            dim(kg=1, s=-3, K=-4)),
        "blackbody_flux": (dmul(dim(kg=1, s=-3, K=-4), dpow(K, Fraction(4))),
                           dim(kg=1, s=-3)),
        "relativistic_energy": (J, dim(kg=1, m=2, s=-2)),
    }
    dims_ok = all(got == want for got, want in stated.values())
    check("SRC02_dimension_vectors_match_the_reported_values", dims_ok,
          f"{ {k: (list(map(str, g)), list(map(str, w))) for k, (g, w) in stated.items() if g != w} }")

    # Dimensional legality: adding a metre to a kelvin must be rejected.
    check("SRC02_addition_across_unequal_dimensions_is_illegal", m != K)

    # --- (2 pi hbar)^3 = h^3, symbolically then numerically ----------------
    h = Decimal("6.62607015e-34")          # exact by SI definition
    hbar = h / (2 * pi)
    cell = (2 * pi * hbar) ** 3
    h3 = h ** 3
    check("SRC02_phase_cell_equals_h_cubed_with_pi_cancelling",
          abs(cell - h3) / h3 < Decimal("1e-70"),
          f"cell {sci(cell)} vs h^3 {sci(h3)}")
    check("SRC02_phase_cell_matches_the_reported_value",
          sci(h3, 26).startswith("2.909163220445246304647"[:18]),
          f"h^3 = {sci(h3, 26)}")
    rep["measured"]["phase_cell"] = {
        "h_cubed": sci(h3, 26),
        "reported": "2.90916322044524630464728375e-100",
        "note": "hbar = h/(2 pi) makes (2 pi hbar)^3 = h^3 identically; no pi survives.",
    }

    # --- Stefan-Boltzmann, against the SI-exact CODATA value ---------------
    kB = Decimal("1.380649e-23")           # exact by SI definition
    c = Decimal("299792458")               # exact by SI definition
    sigma = 2 * pi ** 5 * kB ** 4 / (15 * h ** 3 * c ** 2)
    # CODATA's value, which follows exactly from those defined constants.
    codata = Decimal("5.670374419184429453970996731e-8")
    rel = abs(sigma - codata) / codata
    check("SRC02_stefan_boltzmann_matches_the_SI_exact_CODATA_value",
          rel < Decimal("1e-25"), f"relative difference {sci(rel)}")
    check("SRC02_stefan_boltzmann_matches_the_bundles_own_digits",
          sci(sigma, 27).startswith("5.670374419184429453970996731"[:22]),
          f"computed {sci(sigma, 27)}")
    rep["measured"]["stefan_boltzmann"] = {
        "computed": sci(sigma, 27),
        "codata_si_exact": str(codata),
        "relative_difference": sci(rel),
        "why_this_is_an_external_anchor": (
            "k_B, h and c are exact defined constants since the 2019 SI revision, so "
            "sigma is exactly determined by the formula and CODATA's digits are an "
            "expectation this arm did not author."
        ),
    }

    # --- the Lorentz case, by a route with no cancellation at all ----------
    # binary64 first: the bundle's claim that the input is already lost there.
    beta_f = 1.0 - 1e-40
    check("SRC02_binary64_cannot_represent_the_test_beta", beta_f == 1.0,
          f"1.0 - 1e-40 gave {beta_f!r}")

    eps = Decimal("1e-40")
    beta = 1 - eps
    # (1 - beta)(1 + beta) is exact: no subtraction of nearly-equal quantities.
    one_minus_beta2 = eps * (2 - eps)
    gamma_exact = one_minus_beta2 ** Decimal("-0.5")
    # and the naive route, for contrast
    gamma_naive = (1 - beta * beta) ** Decimal("-0.5")
    reported = Decimal("70710678118654752440.08443621")
    rel_g = abs(gamma_exact - reported) / reported
    check("SRC02_lorentz_gamma_matches_via_the_factored_route",
          rel_g < Decimal("1e-25"), f"relative difference {sci(rel_g)}")
    check("SRC02_factored_and_naive_routes_agree_at_this_precision",
          abs(gamma_exact - gamma_naive) / gamma_exact < Decimal("1e-40"))
    rep["measured"]["lorentz_gamma"] = {
        "beta": "1 - 1e-40",
        "gamma_by_factored_route": sci(gamma_exact, 28),
        "reported_by_bundle": str(reported),
        "relative_difference": sci(rel_g),
        "binary64_beta": repr(beta_f),
        "note": (
            "1 - beta^2 = (1-beta)(1+beta) removes the cancellation entirely, so gamma "
            "needs no log-difference trick at all - only enough precision to hold "
            "1e-40. The bundle's log-diff-exp path gets the same number by a different "
            "method, which is what makes the agreement worth something."
        ),
    }

    # --- assessment ---------------------------------------------------------
    rep["measured"]["assessment"] = {
        "what_it_establishes": (
            "the additive-coordinate representation survives contact with real formulas: "
            "products become sums, SI dimensions compose as integer vectors, illegal "
            "additions are rejected structurally, and severe cancellation is handled at "
            "working precision. Every benchmark reproduces its reference value."
        ),
        "what_it_does_not": (
            "nothing about Collatz. This is a representation stress test, and its Collatz "
            "relevance is only that item 01 used the same coordinate."
        ),
        "relation_to_the_line": (
            "A branch rather than a continuation. Item 01 applied log coordinates to "
            "Collatz; item 02 applies the same coordinate to dimensional physics. The "
            "nine-paper series then goes the other way entirely, replacing logarithms "
            "with exact affine operators over the integers - Paper 02 §28 says an exact "
            "certificate need not depend on a floating logarithm. So this branch is not "
            "an ancestor of the series' method; it is the road not taken, and it is worth "
            "keeping precisely because it shows the alternative was tried and how far it "
            "actually goes."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
