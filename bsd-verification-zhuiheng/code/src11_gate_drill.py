"""Drill for gates 08, 09 and 10 — plant a defect, demand the named check catch it.

數學戰士「墜衡」 / AMRAL Research Lab.

This tree's README has stated since RUN-001 that

    Every gate gets a mutation drill, and a planted defect must be caught by the
    check *named for it* — not merely by some check. A gate that has only ever
    been green is indistinguishable from a comment.

and until now the BSD line had none. Ten gates, zero drills, and a method section
saying otherwise. This closes that for the three gates carrying the substantive
claims — the X₀(n) engine under RUN-007 and RUN-008, the kept-curve checks, and
the Phase 2 density.

TWO KINDS OF DEFECT, because the gates make two kinds of claim.

  `code` — break the gate's own arithmetic and demand a check notice. A wrong
  parametrisation constant, a search window too narrow to reach a real root, a
  candidate cap that returns "none found" instead of "not finished".

  `data` — hand a check the bad input it exists to reject. A discriminant
  valuation that does not rebuild the discriminant, a partition with an overlap.
  A validator that has only ever seen good data has not been tested either.

AND A POSITIVE CONTROL ON THE DRILL ITSELF. Gate 10 reports zero Frobenius-pinning
violations over 79,204 primes. That number means nothing unless the check can
report a violation at all, so one defect replaces f₂ with x³ + x + 1, whose
quadratic resolvent Q(√−31) is *not* inside Q(ζ₂₄, √29) — the pinning genuinely
does not hold there, and violations must appear. A check that cannot go red has
not passed anything.

CONTROLS are perturbations that must leave every check green: a wider search
window, a larger candidate budget, a different random seed for the randomised
factorisation, the same valuations in a different key order. Without them the
drill only shows that the checks are sensitive to *something*.

WHAT THE FIRST RUN FOUND, which is the reason to write drills rather than assume
them. Three defects were caught by nothing at all — an off-by-one in `nth_root`,
a primality test stubbed to always say "prime", and `x^q` computed without its
squaring step. None of them changed a single verdict on any fixture curve. The
first two live on the no-factoring fallback, a path the census never needed
because every denominator factored; the third is invisible to the pinning check,
whose branch is decided by a Legendre symbol and never consults the polynomial
arithmetic. Three checks were added for them — `uv-pairs-agree`, `factorisation`
and `density-1-over-24` — and each now catches its own. The gates were not
wrong; the checks did not cover them, and nothing but a planted defect was going
to say so.

Usage:  python code/src11_gate_drill.py
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src09_kept_curves_removal_gate as kept             # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src11-gate-drill.json"

# Curves whose verdicts are fixed independently of any run of these gates:
# the six of gate 08's own self-check plus the hard tail of the census, where
# 183430x1's 3-isogeny was established by hand in RUN-006 (ψ₃(163100) = 0).
HARD = [
    ("458626a1", [1, -1, 0, -3322098119425, 2330590303502505277],
     {2: False, 3: False, 5: False, 7: False}),            # den 35 digits
    ("183430x1", [1, 0, 1, -35912323909, 2502914884498672],
     {2: False, 3: True, 5: False, 7: False}),             # den 33 digits
    ("105830f1", [1, 0, 1, -3787689128, -21214699861002],
     {2: False, 3: True, 5: False, 7: False}),             # den 31 digits
    ("38b1", [1, 1, 1, 0, 1], {2: False, 3: False, 5: True, 7: False}),
    ("26b1", [1, -1, 1, -3, 3], {2: False, 3: False, 5: False, 7: True}),
]

GOOD_RECORD = {
    "curve_label": "14a1",
    "ainvs": [1, 0, 1, 4, -6],
    "discriminant_valuations": {"2": 6, "7": 3},           # −21952 = −2⁶·7³
}


# ------------------------------------------------------------------- the checks

def check_x0n_self_check() -> bool:
    """Gate 08 refuses to run unless it reproduces answers known outside it."""
    try:
        x0n.self_check()
    except SystemExit:
        return False
    except Exception:
        return False
    return True


def check_x0n_hard_fixture() -> bool:
    """The same engine on the tail of the census, where the searches are hard."""
    for _label, ainvs, want in HARD:
        j = x0n.j_invariant(ainvs)
        if j is None:
            return False
        fac = {} if j.denominator == 1 else x0n.factorise(j.denominator)
        for n, expected in want.items():
            pts = x0n.rational_points(j, n, fac)
            if pts is None or bool(pts) is not expected:
                return False
    return True


def check_disc_valuations(record=None) -> bool:
    """Gate 09 rebuilds ∏p^v and compares it to the Δ it computes itself."""
    agrees, _rebuilt, primes = kept.verify_discriminant_valuations(
        record or GOOD_RECORD)
    return agrees and bool(primes)


def check_partition(triple=None) -> bool:
    """kept ⊔ removed = the old base, recomputed rather than read."""
    k, r, o = triple or ({"a", "b"}, {"c"}, {"a", "b", "c"})
    return kept.verify_partition(k, r, o)["ok"]


def check_cubic_discriminant() -> bool:
    """disc(f₂) recomputed from the formula must be −11136."""
    return ph2.cubic_discriminant(ph2.F2) == -11136


def check_frobenius_pinning() -> bool:
    """For q ≡ 1 (24) with (q/29) = 1, f₂ mod q never has exactly one root."""
    r = ph2.scan(60_000)
    return not r["violations"] and r["cond12"] > 0


def check_reduction_type() -> bool:
    """29 is nonsplit multiplicative on 696.e1: #E_ns(F₂₉) = 30 = 29 + 1."""
    return (ph2.singular_point_count(ph2.AINVS, 29) == 30
            and ph2.singular_point_count(ph2.AINVS, 3) == 2)


def _prime_by_trial(v: int) -> bool:
    """Deterministic, and deliberately not the routine under test."""
    if v < 2:
        return False
    d = 2
    while d * d <= v:
        if v % d == 0:
            return False
        d += 1
    return True


def check_factorisation() -> bool:
    """factorise() must return actual primes whose product is the input.

    Added because the first run of this drill showed that stubbing the
    primality test to always say "prime" changed no fixture verdict — the
    corrupted factorisations only ever dropped candidates that were not roots.
    A gate can be wrong in a way its own outputs never reveal.
    """
    v = 32 * 3 * 1000003 * 1000033
    fac = x0n.factorise(v)
    if fac is None:
        return False
    prod = 1
    for q, e in fac.items():
        prod *= q ** e
    return prod == v and all(_prime_by_trial(q) for q in fac)


def check_uv_pairs_agree() -> bool:
    """The factoring and no-factoring routes to (u', v') must give one answer.

    The no-factoring route is the one the census never needed — every
    denominator factored — so nothing in RUN-007 or RUN-008 exercised it. It is
    still in the gate, so it is still a claim.
    """
    for dn in (32, 243, 1024, 7776, 15625, 100_000, 371_293):
        for D, m in ((3, 1), (1, 5), (1, 7), (1, 2)):
            a = x0n.uv_pairs(dn, x0n.factorise(dn), D, m)
            b = x0n.uv_pairs(dn, None, D, m)
            if a is None or b is None or sorted(a) != sorted(b):
                return False
    return True


def check_density_one_over_24() -> bool:
    """The measured density must land on 1/24 and not on 1/48.

    Separate from the pinning check, because the pinning branch is decided by a
    Legendre symbol and never consults the polynomial arithmetic — so "zero
    violations" cannot detect a broken x^q. The density can: it is what
    distinguishes 0 roots from 3.
    """
    r = ph2.scan(300_000)
    if not r["primes_total"]:
        return False
    d = r["in_P"] / r["primes_total"]
    return abs(d - 1 / 24) < abs(d - 1 / 48) and abs(d * 24 - 1) < 0.05


CHECKS = {
    "x0n-self-check": check_x0n_self_check,
    "x0n-hard-fixture": check_x0n_hard_fixture,
    "disc-valuations": check_disc_valuations,
    "partition": check_partition,
    "cubic-discriminant": check_cubic_discriminant,
    "frobenius-pinning": check_frobenius_pinning,
    "reduction-type": check_reduction_type,
    "factorisation": check_factorisation,
    "uv-pairs-agree": check_uv_pairs_agree,
    "density-1-over-24": check_density_one_over_24,
}


# ------------------------------------------------------------------ the patches

def patch(mod, attr, value):
    old = getattr(mod, attr)
    setattr(mod, attr, value)
    return lambda: setattr(mod, attr, old)


def patch_param(n, coeffs=None, m=None):
    old = copy.deepcopy(x0n.PARAM)
    c, mm = x0n.PARAM[n]
    x0n.PARAM[n] = (coeffs if coeffs is not None else c,
                    m if m is not None else mm)
    return lambda: x0n.PARAM.update(old)


def _bad_j(ainvs):                       # b₈ sign flipped on one term
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 + a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    from fractions import Fraction
    return None if disc == 0 else Fraction(c4 ** 3, disc)


def _partial_factorise(v):               # trial division only, no rho
    fac, d = {}, 2
    while d * d <= v and d < 1_000_000:
        while v % d == 0:
            fac[d] = fac.get(d, 0) + 1
            v //= d
        d += 1 if d == 2 else 2
    return fac                           # silently drops any large cofactor


def _no_singular_subtraction(ainvs, p):
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    total = 1
    for x in range(p):
        d = ((a1 * x + a3) ** 2 + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % p
        total += 1 if d == 0 else 1 + (1 if pow(d, (p - 1) // 2, p) == 1 else -1)
    return total


DEFECTS = [
    # ---- gate 08: the X₀(n) parametrisations ---------------------------------
    ("X0(3) constant 27 becomes 26", "code", "x0n-self-check",
     lambda: patch_param(3, x0n.polymul([26, 1], x0n.polypow([3, 1], 3)))),
    ("X0(3) cube becomes a square", "code", "x0n-self-check",
     lambda: patch_param(3, x0n.polymul([27, 1], x0n.polypow([3, 1], 2)))),
    ("X0(3) pole order 1 becomes 2", "code", "x0n-self-check",
     lambda: patch_param(3, None, 2)),
    ("X0(5) coefficient 250 becomes 205", "code", "x0n-self-check",
     lambda: patch_param(5, x0n.polypow([3125, 205, 1], 3))),
    ("X0(5) constant 3125 becomes 3120", "code", "x0n-self-check",
     lambda: patch_param(5, x0n.polypow([3120, 250, 1], 3))),
    ("X0(5) pole order 5 becomes 4", "code", "x0n-self-check",
     lambda: patch_param(5, None, 4)),
    ("X0(7) coefficient 13 becomes 31", "code", "x0n-self-check",
     lambda: patch_param(7, x0n.polymul([49, 31, 1],
                                        x0n.polypow([2401, 245, 1], 3)))),
    ("X0(7) constant 2401 becomes 2400", "code", "x0n-self-check",
     lambda: patch_param(7, x0n.polymul([49, 13, 1],
                                        x0n.polypow([2400, 245, 1], 3)))),
    ("X0(2) constant 256 becomes 255", "code", "x0n-self-check",
     lambda: patch_param(2, x0n.polypow([255, 1], 3))),
    ("X0(2) pole order 2 becomes 3", "code", "x0n-self-check",
     lambda: patch_param(2, None, 3)),

    # ---- gate 08: the surrounding arithmetic ---------------------------------
    ("j-invariant: a1a3a4 term in b8 flips sign", "code", "x0n-self-check",
     lambda: patch(x0n, "j_invariant", _bad_j)),
    ("search window narrowed below what a real root needs", "code",
     "x0n-self-check", lambda: patch(x0n, "GAMMA_PAD", -40)),
    ("candidate budget cut to zero: 'none found' replaces 'not finished'",
     "code", "x0n-hard-fixture", lambda: patch(x0n, "MAX_CANDIDATES", 1)),
    ("factorisation drops its large cofactor instead of returning None",
     "code", "x0n-hard-fixture",
     lambda: patch(x0n, "factorise", _partial_factorise)),
    ("nth_root off by one, so the no-factoring fallback misses", "code",
     "uv-pairs-agree",
     lambda: patch(x0n, "nth_root", lambda x, k: max(0, _true_nth_root(x, k) - 1))),
    ("primality test always says prime, corrupting every factorisation",
     "code", "factorisation",
     lambda: patch(x0n, "_is_probable_prime", lambda v: True)),

    # ---- gate 09: the checks that guard supplied data ------------------------
    ("valuation exponent wrong by one", "data", "disc-valuations",
     lambda: _record_patch({"2": 5, "7": 3})),
    ("a prime of the discriminant omitted", "data", "disc-valuations",
     lambda: _record_patch({"2": 6})),
    ("a prime that does not divide the discriminant added", "data",
     "disc-valuations", lambda: _record_patch({"2": 6, "7": 3, "11": 1})),
    ("valuations absent entirely", "data", "disc-valuations",
     lambda: _record_patch({})),
    ("kept and removed overlap", "data", "partition",
     lambda: _partition_patch(({"a", "b"}, {"b", "c"}, {"a", "b", "c"}))),
    ("a base curve in neither kept nor removed", "data", "partition",
     lambda: _partition_patch(({"a"}, {"c"}, {"a", "b", "c"}))),
    ("a kept label absent from the base", "data", "partition",
     lambda: _partition_patch(({"a", "z"}, {"c"}, {"a", "c"}))),

    # ---- gate 10 -------------------------------------------------------------
    ("cubic discriminant formula: 18abcd term dropped", "code",
     "cubic-discriminant",
     lambda: patch(ph2, "cubic_discriminant",
                   lambda f: (-4 * f[2] ** 3 * f[0] + f[2] ** 2 * f[1] ** 2
                              - 4 * f[3] * f[1] ** 3
                              - 27 * f[3] ** 2 * f[0] ** 2))),
    ("f2 replaced by x^3+x+1, whose resolvent escapes Q(zeta24, sqrt29)",
     "code", "frobenius-pinning", lambda: patch(ph2, "F2", [1, 1, 0, 1])),
    ("x^q computed without the squaring step", "code", "density-1-over-24",
     lambda: patch(ph2, "x_pow_q", _bad_x_pow_q)),
    ("singular point never subtracted from the point count", "code",
     "reduction-type",
     lambda: patch(ph2, "singular_point_count", _no_singular_subtraction)),
]

CONTROLS = [
    ("search window widened", lambda: patch(x0n, "GAMMA_PAD", 12)),
    ("candidate budget raised", lambda: patch(x0n, "MAX_CANDIDATES", 400_000)),
    ("different random seed for the factorisation",
     lambda: _reseed(987654321)),
    ("rho budget raised", lambda: patch(x0n, "RHO_BUDGET", 800)),
    ("label-file header length re-read as the same value",
     lambda: patch(kept, "LABEL_HEADER_LINES", 6)),
    ("valuations given in a different key order", lambda: _record_patch(
        {"7": 3, "2": 6})),
    ("partition sets given as different objects with the same members",
     lambda: _partition_patch((set(["a", "b"]), set(["c"]),
                               set(["c", "b", "a"])))),
    ("no change at all", lambda: (lambda: None)),
]


_true_nth_root = x0n.nth_root
_RECORD_OVERRIDE: dict | None = None
_PARTITION_OVERRIDE: tuple | None = None


def _record_patch(vals):
    global _RECORD_OVERRIDE
    rec = dict(GOOD_RECORD)
    rec["discriminant_valuations"] = vals
    _RECORD_OVERRIDE = rec

    def restore():
        global _RECORD_OVERRIDE
        _RECORD_OVERRIDE = None
    return restore


def _partition_patch(triple):
    global _PARTITION_OVERRIDE
    _PARTITION_OVERRIDE = triple

    def restore():
        global _PARTITION_OVERRIDE
        _PARTITION_OVERRIDE = None
    return restore


def _reseed(seed):
    import random
    random.seed(seed)
    return lambda: random.seed(20260908)


def _bad_x_pow_q(f, q):
    result, base, e = [1, 0, 0], [0, 1, 0], q
    while e:
        if e & 1:
            result = ph2.poly_mulmod(result, base, f, q)
        e >>= 1                          # base never squared
    return result


def run_checks() -> dict[str, bool]:
    out = {}
    for name, fn in CHECKS.items():
        try:
            if name == "disc-valuations":
                out[name] = fn(_RECORD_OVERRIDE)
            elif name == "partition":
                out[name] = fn(_PARTITION_OVERRIDE)
            else:
                out[name] = fn()
        except Exception:
            out[name] = False            # a crash is a red check, not a pass
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    baseline = run_checks()
    if not all(baseline.values()):
        raise SystemExit(f"the undisturbed gates are not green: {baseline}")
    print(f"  baseline: all {len(baseline)} checks green")

    results, uncaught, wrong_catcher = [], [], []
    for name, kind, expected, make in DEFECTS:
        restore = make()
        try:
            got = run_checks()
        finally:
            restore()
        red = [k for k, v in got.items() if not v]
        entry = {"defect": name, "kind": kind, "named_check": expected,
                 "checks_that_went_red": red,
                 "caught_by_the_named_check": expected in red}
        results.append(entry)
        if not red:
            uncaught.append(name)
        elif expected not in red:
            wrong_catcher.append({"defect": name, "expected": expected,
                                  "actually_caught_by": red})
        flag = ("OK " if expected in red else
                "MISSED " if not red else "WRONG-CHECK ")
        print(f"    {flag:12s} [{kind}] {name}")
        print(f"                 red: {', '.join(red) if red else '(none)'}")

    print()
    ctrl_results, disturbed = [], []
    for name, make in CONTROLS:
        restore = make()
        try:
            got = run_checks()
        finally:
            restore()
        red = [k for k, v in got.items() if not v]
        ctrl_results.append({"control": name, "checks_that_went_red": red,
                             "undisturbed": not red})
        if red:
            disturbed.append({"control": name, "red": red})
        print(f"    {'OK ' if not red else 'DISTURBED '}control: {name}"
              + (f"   red: {', '.join(red)}" if red else ""))

    after = run_checks()
    log = {
        "gate": "src11_gate_drill",
        "covers": ["src08_modular_curve_confirmation",
                   "src09_kept_curves_removal_gate",
                   "src10_phase2_density_and_base"],
        "rule": ("a planted defect must be caught by the check NAMED for it, "
                 "not merely by some check; and controls must disturb nothing"),
        "two_kinds": {
            "code": "break the gate's own arithmetic, demand a check notice",
            "data": ("hand a validating check the bad input it exists to "
                     "reject — a validator that has only seen good data has "
                     "not been tested either"),
        },
        "positive_control_on_the_drill": (
            "replacing f2 with x^3+x+1, whose quadratic resolvent Q(sqrt-31) is "
            "NOT inside Q(zeta24, sqrt29), must make the pinning check go red — "
            "otherwise gate 10's 'zero violations over 79,204 primes' would be "
            "indistinguishable from a check that cannot fire"),
        "baseline_all_green": baseline,
        "defects": results,
        "controls": ctrl_results,
        "totals": {
            "defects": len(DEFECTS),
            "caught_by_the_named_check": sum(
                1 for r in results if r["caught_by_the_named_check"]),
            "UNCAUGHT_BY_ANY_CHECK": uncaught,
            "CAUGHT_BY_THE_WRONG_CHECK": wrong_catcher,
            "controls": len(CONTROLS),
            "controls_that_disturbed_a_check": disturbed,
        },
        "state_restored_afterwards": all(after.values()),
        "ok": (not uncaught and not wrong_catcher and not disturbed
               and all(after.values())),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    t = log["totals"]
    print()
    print(f"  {t['defects']} defects, {t['caught_by_the_named_check']} caught "
          f"by the check named for them")
    print(f"  uncaught by any check      : "
          f"{len(uncaught)}{'  ' + ', '.join(uncaught) if uncaught else ''}")
    print(f"  caught by the wrong check  : {len(wrong_catcher)}")
    print(f"  {t['controls']} controls, "
          f"{len(disturbed)} disturbed a check")
    print(f"  state restored afterwards  : {log['state_restored_afterwards']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
