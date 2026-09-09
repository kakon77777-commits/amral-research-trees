"""Gate 33 — Mazur's twelve isogeny degrees, closed for 696.e1 and its family.

數學戰士「墜衡」 / AMRAL Research Lab.

Since RUN-018 this arm has carried the same limitation, and named it in every
round that touched the anchor: RUN-007's `X₀(n)` method decides **four** of the
twelve prime degrees Mazur's theorem allows — 2, 3, 5 and 7 — and the other
eight are named rather than checked. RUN-030's certificate lists it among what
stays cited. `24_Manin_Period_Audit` rests its optimality argument on the same
claim:

    quadratic twisting preserves residual irreducibility, so E_q has no rational
    prime-degree isogeny; hence its Q-isogeny class has no other nonisomorphic
    curve and E_q is itself the optimal representative

so the gap is not decorative — it is a premise of the period argument.

THE TOOL WAS ALREADY HERE. If `E` admits a rational `n`-isogeny then `ρ̄_n` is
reducible, so for every prime `ℓ` of good reduction with `ℓ ≠ n` the
characteristic polynomial of Frobenius splits over `F_n`:

    x² − a_ℓ x + ℓ  factors mod n   ⟺   a_ℓ² − 4ℓ is a square mod n.

**One `ℓ` where it is a non-residue refutes the isogeny outright.** That is
RUN-007's reducibility sieve, one-sided and exact, and it needs no
parametrisation, no list of `j`-invariants, and nothing recalled — which after
RUN-030 is the point.

WHERE IT CANNOT WORK, AND WHY THAT IS NOT A SEARCH PROBLEM. At `n = 2` every
element of `F₂` is a square, so the condition is satisfied by every `ℓ` and the
sieve is **structurally vacuous** — not "no witness below the search bound".
Degree 2 is settled by `X₀(2)` in RUN-007, which decides rather than refutes.

AND THE REFUTATION TRANSFERS TO THE TWISTS. For a quadratic twist,
`a_ℓ(E^{(d)}) = χ_d(ℓ)·a_ℓ(E)` with `χ_d(ℓ) = ±1`, so `a_ℓ² − 4ℓ` is **identical**
— the sign is squared away. A witness for the base is therefore a witness for
every twist at that `ℓ`, provided `ℓ` stays good, which is measured here rather
than asserted.

Usage:  python code/src33_mazur_degrees_closed.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src07_isogeny_reducibility_sieve as sieve          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src33-mazur-degrees.json"

ANCHOR = [0, 1, 0, 8, -16]                # 696.e1
MAZUR = (2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163)
DECIDED_BY_X0N = (2, 3, 5, 7)             # RUN-007's complete method
SEARCH = 600
TWIST_DISCRIMINANTS = (241, 313, 409)     # members RUN-015 and RUN-016 worked


def small_primes(limit: int) -> list[int]:
    flags = bytearray([1]) * limit
    flags[:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if flags[i]:
            flags[i * i::i] = bytearray(len(flags[i * i::i]))
    return [i for i, v in enumerate(flags) if v]


def quadratic_twist(ainvs: list[int], d: int) -> list[int]:
    """E^{(d)} in the form y² = x³ + b2 d x² + 8 b4 d² x + 16 b6 d³."""
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    return [0, b2 * d, 0, 8 * b4 * d * d, 16 * b6 * d ** 3]


def witness(ainvs: list[int], n: int, primes: list[int]) -> dict | None:
    """The first good ℓ ≠ n at which a_ℓ² − 4ℓ is a non-residue mod n."""
    for ell in primes:
        if ell == n or sieve.divides_discriminant(ainvs, ell):
            continue
        a = sieve.a_p(ainvs, ell)
        if a is None:
            continue
        disc = (a * a - 4 * ell) % n
        if not sieve.is_square_mod(disc, n):
            return {"ell": ell, "a_ell": a, "a_squared_minus_4ell_mod_n": disc,
                    "reads": f"x^2 - {a}x + {ell} is irreducible mod {n}"}
    return None


def vacuity_at_2() -> dict:
    """Every element of F₂ is a square, so the sieve cannot refute at n = 2."""
    squares = sorted({(x * x) % 2 for x in range(2)})
    return {"squares_mod_2": squares, "all_of_F2": squares == [0, 1],
            "so_the_sieve_is": "structurally vacuous at n = 2",
            "not": "a search that did not go far enough",
            "settled_instead_by": ("RUN-007's X_0(2), which decides rather than "
                                   "refutes: 696.e1 has no rational 2-isogeny")}


def twist_invariance(primes: list[int]) -> dict:
    """a_ℓ² − 4ℓ is the same for E and every quadratic twist at good ℓ."""
    rows = []
    for d in TWIST_DISCRIMINANTS:
        T = quadratic_twist(ANCHOR, d)
        compared, identical, sign_flips = 0, 0, 0
        for ell in primes[:30]:
            if (sieve.divides_discriminant(ANCHOR, ell)
                    or sieve.divides_discriminant(T, ell)):
                continue
            a, at = sieve.a_p(ANCHOR, ell), sieve.a_p(T, ell)
            if a is None or at is None:
                continue
            compared += 1
            if a * a - 4 * ell == at * at - 4 * ell:
                identical += 1
            if a != at:
                sign_flips += 1
        rows.append({"twist_discriminant": d, "good_primes_compared": compared,
                     "discriminant_identical": identical,
                     "a_ell_sign_flips": sign_flips,
                     "all_identical": compared == identical})
    return {"rows": rows,
            "all_identical": all(r["all_identical"] for r in rows),
            "why": ("a_l(E^(d)) = chi_d(l) a_l(E) with chi_d(l) = +-1, so the "
                    "sign is squared away and a_l^2 - 4l is unchanged"),
            "sign_flips_observed": sum(r["a_ell_sign_flips"] for r in rows),
            "caveat": ("a witness transfers only while l stays good for the "
                       "twist, i.e. l does not divide the twisting "
                       "discriminant")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    primes = [p for p in small_primes(SEARCH)]
    results = {}
    for n in MAZUR:
        w = witness(ANCHOR, n, primes)
        results[n] = {
            "degree": n,
            "refuted_by_the_sieve": w is not None,
            "witness": w,
            "also_decided_by_X0n_in_RUN_007": n in DECIDED_BY_X0N,
        }
    vac = vacuity_at_2()
    tw = twist_invariance(primes)

    refuted = [n for n in MAZUR if results[n]["refuted_by_the_sieve"]]
    covered = [n for n in MAZUR
               if results[n]["refuted_by_the_sieve"] or n in DECIDED_BY_X0N]
    doubly = [n for n in MAZUR
              if results[n]["refuted_by_the_sieve"] and n in DECIDED_BY_X0N]

    log = {
        "gate": "src33 — Mazur's twelve degrees for 696.e1",
        "curve": {"label": "696.e1", "a_invariants": ANCHOR},
        "criterion": ("a rational n-isogeny makes rho-bar_n reducible, so "
                      "x^2 - a_l x + l splits over F_n at every good l != n. "
                      "One non-residue refutes it"),
        "search_bound_for_witnesses": SEARCH,
        "per_degree": {str(n): results[n] for n in MAZUR},
        "refuted_by_the_sieve": refuted,
        "covered_by_one_method_or_the_other": covered,
        "covered_all_twelve": sorted(covered) == sorted(MAZUR),
        "degrees_with_two_independent_proofs": doubly,
        "vacuity_at_2": vac,
        "twist_invariance": tw,
        "closes": ("the '4 of Mazur's 12' limitation this arm has carried since "
                   "RUN-018 and listed in RUN-030's certificate, and the "
                   "premise 24_Manin_Period_Audit's optimality argument rests "
                   "on"),
        "ok": (sorted(covered) == sorted(MAZUR) and vac["all_of_F2"]
               and tw["all_identical"] and len(refuted) == 11),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  696.e1, Mazur's twelve prime degrees, witnesses below {SEARCH}")
    for n in MAZUR:
        r = results[n]
        if r["witness"]:
            w = r["witness"]
            extra = "  (also X_0(n) in RUN-007)" if r["also_decided_by_X0n_in_RUN_007"] else ""
            print(f"    n = {n:3d}  refuted: l = {w['ell']:3d}, a_l = "
                  f"{w['a_ell']:4d}, a^2-4l = {w['a_squared_minus_4ell_mod_n']} "
                  f"is a non-residue{extra}")
        else:
            print(f"    n = {n:3d}  sieve {vac['so_the_sieve_is']} — "
                  f"{vac['settled_instead_by']}")
    print()
    print(f"  refuted by the sieve: {len(refuted)} of 12; "
          f"covered by one method or the other: "
          f"{len(covered)} of 12 → all twelve: {log['covered_all_twelve']}")
    print(f"  two independent proofs at: {doubly}")
    print()
    print("  twist invariance of a^2 - 4l:")
    for r in tw["rows"]:
        print(f"    d = {r['twist_discriminant']:4d}: "
              f"{r['discriminant_identical']}/{r['good_primes_compared']} "
              f"identical, {r['a_ell_sign_flips']} sign flips in a_l")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
