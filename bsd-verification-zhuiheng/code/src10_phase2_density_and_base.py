"""Gate 10 — Phase 2's Theorem 1.1(1), the density 1/24, and the base curve under it.

數學戰士「墜衡」 / AMRAL Research Lab.

`29_Theorem_Note_v1.0` states a derived family theorem about quadratic twists of
696.e1. Parts (2) and (3) — L(E^(q),1) ≠ 0 and strong BSD — rest on cited
theorems of Skinner, Burungale–Skinner–Tian–Wan and Fouquet–Wan, and this arm
cannot recompute them. **Part (1) is arithmetic, and it is checkable here.**

    𝒫 = { q prime : q ≡ 1 (mod 24), (q/29) = 1, f₂ irreducible mod q },
        f₂(x) = x³ + x² + 8x − 16,     and the note claims δ(𝒫) = 1/24.

WHY THIS IS WORTH CHECKING RATHER THAN READING. Three conditions of density
1/8, 1/2 and 1/3 multiply to **1/48**. The note says 1/24. Either the note is
wrong by a factor of two, or the conditions are not independent — and which one
it is decides whether a stated density can be taken at face value anywhere else
in this corpus.

They are not independent, and the entanglement is exact:

    disc(f₂) = −11136 = −2⁷·3·29,   squarefree part **−174 = (−6)·29**.

The splitting field of f₂ is an S₃-extension whose quadratic subfield is
therefore Q(√−174). Now q ≡ 1 (mod 24) forces (−1/q) = (2/q) = (3/q) = 1, hence
(−6/q) = 1; and (29/q) = 1 is the second condition. So

    (disc(f₂)/q) = (−174/q) = (−6/q)·(29/q) = 1

for **every** q already satisfying the first two conditions. Frobenius is pinned
inside A₃, where the 3-cycles are 2 of 3 rather than 2 of 6. The third condition
therefore has conditional density 2/3, not 1/3, and

    δ(𝒫) = (1/8)·(1/2)·(2/3) = 1/24.

The note's number is right and the naive product is wrong. This gate does not
stop at reproducing the reasoning: it tests the pinning as a falsifiable
prediction — **for q ≡ 1 (mod 24) with (q/29) = 1, f₂ mod q never has exactly
one root** — and measures the density directly against both candidates, so that
1/24 is distinguished from 1/48 by counting and not only by argument.

It also recomputes the base curve's own arithmetic, since a family theorem
anchored on 696.e1 is worth no more than the anchor: the discriminant, the
minimality of the model at 2, non-semistability, and the reduction type at 3 and
29 — the note calls 29 nonsplit multiplicative and uses it as the uniform
Fouquet–Wan auxiliary prime.

Usage:  python code/src10_phase2_density_and_base.py
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src10-phase2-density.json"

AINVS = [0, 1, 0, 8, -16]                 # 696.e1 / Cremona 696b1, from the note
F2 = [-16, 8, 1, 1]                       # f₂ ascending: −16 + 8x + x² + x³
LIMIT = 20_000_000


# ------------------------------------------------------------- curve arithmetic

def invariants(ainvs: list[int]) -> dict[str, int]:
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return {"b2": b2, "b4": b4, "b6": b6, "b8": b8, "c4": c4, "disc": disc}


def valuation(v: int, p: int) -> int:
    k = 0
    while v % p == 0:
        v //= p
        k += 1
    return k


def factor_small(v: int) -> dict[int, int]:
    v, out, d = abs(v), {}, 2
    while d * d <= v:
        while v % d == 0:
            out[d] = out.get(d, 0) + 1
            v //= d
        d += 1 if d == 2 else 2
    if v > 1:
        out[v] = out.get(v, 0) + 1
    return out


def singular_point_count(ainvs: list[int], p: int) -> int:
    """#E_ns(F_p) at a prime of bad reduction: p−1 split, p+1 nonsplit, p additive."""
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    total = 1
    for x in range(p):
        d = ((a1 * x + a3) ** 2 + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % p
        if d == 0:
            total += 1
        else:
            total += 1 + (1 if pow(d, (p - 1) // 2, p) == 1 else -1)
    # subtract the singular point itself
    sing = 0
    for x in range(p):
        for y in range(p):
            f = (y * y + a1 * x * y + a3 * y
                 - (x ** 3 + a2 * x * x + a4 * x + a6)) % p
            fx = (-(3 * x * x + 2 * a2 * x + a4) + a1 * y) % p
            fy = (2 * y + a1 * x + a3) % p
            if f == 0 and fx == 0 and fy == 0:
                sing += 1
    return total - sing


# ----------------------------------------------------------- F_q[x] arithmetic

def poly_mulmod(a, b, f, q):
    """(a·b) mod f over F_q; f monic of degree 3, given ascending."""
    c = [0] * 5
    for i in range(3):
        if a[i]:
            for k in range(3):
                c[i + k] = (c[i + k] + a[i] * b[k]) % q
    for i in (4, 3):                      # x³ ≡ −(f0 + f1x + f2x²)
        if c[i]:
            t = c[i]
            c[i] = 0
            for k in range(3):
                c[i - 3 + k] = (c[i - 3 + k] - t * f[k]) % q
    return c[:3]


def x_pow_q(f, q):
    """x^q mod f over F_q."""
    result, base, e = [1, 0, 0], [0, 1, 0], q
    while e:
        if e & 1:
            result = poly_mulmod(result, base, f, q)
        base = poly_mulmod(base, base, f, q)
        e >>= 1
    return result


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def cubic_discriminant(f: list[int]) -> int:
    """Discriminant of a cubic given ascending as [d, c, b, a] for ax^3+bx^2+cx+d."""
    d, c, b, a = f
    return (18 * a * b * c * d - 4 * b ** 3 * d + b * b * c * c
            - 4 * a * c ** 3 - 27 * a * a * d * d)


def cubic_root_count(f4: list[int], q: int) -> int:
    """Number of distinct roots of the monic cubic f4 in F_q, for q ∤ disc.

    The discriminant is derived from f4 rather than pinned to a constant: a
    hard-coded −11136 would keep agreeing with itself if the polynomial were
    ever changed, which is the shape of an error a gate cannot catch.
    """
    f = [c % q for c in f4[:3]]
    xq = x_pow_q(f, q)
    if xq == [0, 1, 0]:                   # x^q ≡ x  ⇒  splits completely
        return 3
    return 0 if legendre(cubic_discriminant(f4), q) == 1 else 1


def sieve(n: int):
    flags = bytearray([1]) * (n + 1)
    flags[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if flags[i]:
            flags[i * i::i] = bytearray(len(flags[i * i::i]))
    return flags


def scan(limit: int, verbose: bool = False) -> dict:
    """Walk the primes below `limit`, testing the pinning and the density.

    The pinning is the falsifiable half: for q ≡ 1 (mod 24) with (q/29) = 1,
    Frobenius is confined to A3, so f2 mod q has 0 or 3 roots and never 1.
    """
    flags = sieve(limit)
    primes_total = cond12 = in_P = 0
    root_counts = {0: 0, 1: 0, 3: 0}
    violations = []
    checkpoints = []
    marks = [m for m in (10 ** 5, 10 ** 6, 10 ** 7) if m < limit] + [limit]
    mark_i = 0

    for q in range(2, limit + 1):
        if not flags[q]:
            continue
        primes_total += 1
        if q % 24 == 1 and q != 29 and legendre(29, q) == 1:
            cond12 += 1
            r = cubic_root_count(F2, q)
            root_counts[r] = root_counts.get(r, 0) + 1
            if r == 1 and len(violations) < 20:
                violations.append({"q": q, "roots": r})
            if r == 0:
                in_P += 1
        while mark_i < len(marks) and q >= marks[mark_i]:
            x = marks[mark_i]
            checkpoints.append({
                "x": x, "primes_up_to_x": primes_total, "in_P": in_P,
                "empirical_density": in_P / primes_total,
                "times_24": in_P / primes_total * 24,
                "times_48": in_P / primes_total * 48,
            })
            mark_i += 1
            if verbose:
                print(f"    x = {x:>12,}   |P|/pi(x) = {in_P/primes_total:.6f}"
                      f"   x24 = {in_P/primes_total*24:.4f}"
                      f"   x48 = {in_P/primes_total*48:.4f}", file=sys.stderr)
    return {"primes_total": primes_total, "cond12": cond12, "in_P": in_P,
            "root_counts": root_counts, "violations": violations,
            "checkpoints": checkpoints}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    # ---- the anchor curve ------------------------------------------------
    inv = invariants(AINVS)
    disc = inv["disc"]
    disc_fac = factor_small(disc)
    conductor_claimed = 696
    cond_fac = factor_small(conductor_claimed)
    base = {
        "a_invariants": AINVS,
        "equation": "y^2 = x^3 + x^2 + 8x - 16",
        "discriminant": disc,
        "discriminant_factored": {str(k): v for k, v in disc_fac.items()},
        "c4": inv["c4"],
        "note_claims_conductor": conductor_claimed,
        "conductor_factored": {str(k): v for k, v in cond_fac.items()},
        "conductor_is_squarefree": all(e == 1 for e in cond_fac.values()),
        "NOT_SEMISTABLE": not all(e == 1 for e in cond_fac.values()),
        "model_minimal_at_2": not (valuation(inv["c4"], 2) >= 4
                                   and valuation(disc, 2) >= 12),
        "v2": {"c4": valuation(inv["c4"], 2), "disc": valuation(disc, 2),
               "conductor": cond_fac.get(2, 0)},
        "reduction": {},
    }
    for p in sorted(disc_fac):
        vN = cond_fac.get(p, 0)
        kind = ("good" if vN == 0 else
                "multiplicative" if vN == 1 else "additive")
        entry = {"v_disc": disc_fac[p], "v_conductor": vN, "type": kind}
        if kind == "multiplicative":
            ns = singular_point_count(AINVS, p)
            entry["E_ns_point_count"] = ns
            entry["split"] = (ns == p - 1)
            entry["nonsplit"] = (ns == p + 1)
        base["reduction"][str(p)] = entry

    # ---- the cubic and the entanglement ----------------------------------
    d_f2 = -11136
    recomputed = cubic_discriminant(F2)
    sqfree, m = 1, abs(d_f2)
    for p, e in factor_small(d_f2).items():
        if e % 2:
            sqfree *= p
    sqfree = -sqfree if d_f2 < 0 else sqfree
    cubic = {
        "f2": "x^3 + x^2 + 8x - 16",
        "discriminant": d_f2,
        "discriminant_recomputed_from_the_formula": recomputed,
        "formula_agrees": recomputed == d_f2,
        "discriminant_factored": {str(k): v
                                  for k, v in factor_small(d_f2).items()},
        "squarefree_part": sqfree,
        "quadratic_subfield_of_the_splitting_field": f"Q(sqrt({sqfree}))",
        "galois_group": "S3 (disc is not a square, and f2 has no rational root)",
        "entanglement": (
            f"{sqfree} = (-6)·29, and q ≡ 1 (mod 24) forces (-6/q) = 1 while "
            "(29/q) = 1 is the second condition — so (disc/q) = 1 for every q "
            "already passing them, pinning Frobenius inside A3"),
    }
    assert cubic["formula_agrees"], "cubic discriminant formula disagrees"

    # ---- the prediction, and the density ---------------------------------
    scan_result = scan(LIMIT, verbose=True)
    primes_total = scan_result["primes_total"]
    cond12 = scan_result["cond12"]
    in_P = scan_result["in_P"]
    root_counts = scan_result["root_counts"]
    violations = scan_result["violations"]
    checkpoints = scan_result["checkpoints"]
    density = in_P / primes_total
    log = {
        "gate": "src10_phase2_density_and_base",
        "subject": ("29_Theorem_Note_v1.0, Theorem 1.1 part (1): the set P has "
                    "natural density 1/24"),
        "scope": (
            "parts (2) and (3) — L(E^(q),1) ≠ 0 and strong BSD for every q in P "
            "— rest on cited theorems this gate does not recompute and does not "
            "claim to have checked. Only part (1) is tested"),
        "base_curve": base,
        "cubic": cubic,
        "naive_independent_product": {
            "q ≡ 1 mod 24": "1/8",
            "(q/29) = 1": "1/2",
            "f2 irreducible mod q": "1/3 for an S3 cubic",
            "product": "1/48",
            "verdict": ("wrong — the three conditions are not independent, and "
                        "the note's 1/24 is the correct value"),
        },
        "prediction_tested": {
            "statement": ("for q ≡ 1 (mod 24) with (q/29) = 1, Frobenius lies in "
                          "A3, so f2 mod q has 0 or 3 roots and NEVER exactly 1"),
            "primes_satisfying_the_first_two_conditions": cond12,
            "root_count_histogram": {str(k): v
                                     for k, v in sorted(root_counts.items())},
            "VIOLATIONS_exactly_one_root": root_counts.get(1, 0),
            "violation_sample": violations,
            "conditional_density_of_irreducibility": (
                (in_P / cond12) if cond12 else None),
            "expected_conditional_density": 2 / 3,
        },
        "density_measured": {
            "limit": LIMIT,
            "primes_up_to_limit": primes_total,
            "size_of_P": in_P,
            "empirical_density": density,
            "one_over_density": (1 / density) if density else None,
            "checkpoints": checkpoints,
        },
        "ok": (root_counts.get(1, 0) == 0
               and base["NOT_SEMISTABLE"]
               and base["model_minimal_at_2"]
               and abs(density * 24 - 1) < 0.01),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print()
    print(f"  base curve 696.e1  Δ = {disc:,} = "
          + " · ".join(f"{p}^{e}" for p, e in sorted(disc_fac.items()))
          + (" (negative)" if disc < 0 else ""))
    print(f"    conductor {conductor_claimed} squarefree: "
          f"{base['conductor_is_squarefree']}   NOT SEMISTABLE: "
          f"{base['NOT_SEMISTABLE']}   model minimal at 2: "
          f"{base['model_minimal_at_2']}")
    for p, e in sorted(base["reduction"].items(), key=lambda kv: int(kv[0])):
        extra = ""
        if e["type"] == "multiplicative":
            extra = f"  #E_ns = {e['E_ns_point_count']}  " + (
                "SPLIT" if e["split"] else "NONSPLIT" if e["nonsplit"] else "?")
        print(f"    p = {p:>3}  v(Δ) = {e['v_disc']:>2}  v(N) = "
              f"{e['v_conductor']}  {e['type']}{extra}")
    print()
    print(f"  disc(f2) = {d_f2:,}  squarefree part {sqfree}  = (-6)·29")
    print(f"  primes with q ≡ 1 (24) and (q/29) = 1 : {cond12:,}")
    print(f"    of those, f2 mod q has 3 roots      : "
          f"{root_counts.get(3, 0):,}")
    print(f"    of those, f2 mod q irreducible      : "
          f"{root_counts.get(0, 0):,}")
    print(f"    EXACTLY ONE ROOT (must be zero)     : "
          f"{root_counts.get(1, 0):,}")
    print(f"    conditional density of irreducible  : "
          f"{in_P / cond12:.6f}   (predicted 2/3 = {2/3:.6f})")
    print()
    print(f"  |P ∩ [1,{LIMIT:,}]| / π(x) = {density:.8f}")
    print(f"    1/24 = {1/24:.8f}      1/48 = {1/48:.8f}")
    print(f"    measured × 24 = {density*24:.5f}   × 48 = {density*48:.5f}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
