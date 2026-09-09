"""Gate 38 — "mod-ℓ images maximal for all ℓ", certified where it can be.

數學戰士「墜衡」 / AMRAL Research Lab.

`24_Manin_Period_Audit` rests its optimality argument on one asserted sentence:

    base 696.e1 mod-ℓ images maximal for all ℓ.

Nothing in the corpus computes it, and RUN-031 closed only the reducible case —
a rational `n`-isogeny — at Mazur's twelve degrees. Reducibility is one of four
ways `ρ̄_ℓ` can miss `GL₂(F_ℓ)`.

THE OTHER THREE ARE REFUTABLE BY THE SAME KIND OF WITNESS. For a subgroup of
`GL₂(F_ℓ)` with surjective determinant — and `det ρ̄_ℓ` is the cyclotomic
character, which is surjective — being proper means being contained in a Borel,
in the normaliser of a split Cartan, in the normaliser of a nonsplit Cartan, or
having projective image `A₄`, `S₄` or `A₅`. Each is a statement about **every**
Frobenius, so **one** good prime `ℓ'` can refute it:

    Borel                       a² − 4ℓ' is a non-residue mod ℓ
    N(split Cartan)             a ≢ 0 and a² − 4ℓ' a non-residue
    N(nonsplit Cartan)          a ≢ 0 and a² − 4ℓ' a nonzero residue
    projective A₄ / S₄ / A₅     the projective order of Frob_ℓ' is outside
                                {1,2,3} / {1,2,3,4} / {1,2,3,5}

where the projective order is read off `u = a²/ℓ' mod ℓ`: `u = 4, 0, 1, 2` give
orders 1, 2, 4… — precisely, `u = 4 → 1`, `u = 0 → 2`, `u = 1 → 3`, `u = 2 → 4`,
`u² − 5u + 5 ≡ 0 → 5`, anything else `> 5`.

Refuting all six for a given `ℓ` certifies `ρ̄_ℓ` surjective. The certificate is
**one-sided**: a class with no witness below the search bound is undecided, not
established, and the gate says which.

`ℓ = 2` IS DONE DIFFERENTLY AND `ℓ = 3` IS BLOCKED TWICE OVER. At `ℓ = 2`,
`GL₂(F₂) ≅ S₃` and surjectivity is the 2-division cubic being irreducible with
non-square discriminant — computed here directly. At `ℓ = 3` two obstructions
are structural rather than a short search: `PGL₂(F₃) ≅ S₄`, so "projective image
`S₄`" *is* surjectivity and cannot be refuted; and the nonsplit-Cartan test is
**vacuous mod 3**, since a nonzero trace forces `a² ≡ 1` and `4 ≡ 1`, making
`a² − 4ℓ' ≡ 1 − ℓ'`, which is the nonzero square 1 only when `3 | ℓ'`. Four
residue cases, exhausted — the same shape RUN-031 had to give `n = 2`. The Borel,
the split Cartan normaliser, `A₄` and `A₅` are all refuted there, so `ℓ = 3` is
reported **partially certified**, never counted as certified.

Usage:  python code/src38_mod_ell_surjectivity.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src07_isogeny_reducibility_sieve as red7           # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src38-mod-ell-surjectivity.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
ELL_BOUND = 170                           # covers Mazur's largest, 163
SEARCH = 600                              # good primes used as witnesses
MAZUR = (2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163)

EXCEPTIONAL = {"A4": (1, 2, 3), "S4": (1, 2, 3, 4), "A5": (1, 2, 3, 5)}


def good_primes(limit: int) -> list[int]:
    """Primes of good reduction for the base, found from the discriminant."""
    _, _, _, _, disc = anchor.b_invariants(BASE)
    return [p for p in mz.small_primes(limit) if disc % p]


def projective_order(a: int, ellp: int, ell: int) -> int:
    """The order of Frob_{ell'} in PGL₂(F_ell), read off u = a²/ell' mod ell.

    Returns 6 for "greater than 5", which is all the exceptional tests need.
    """
    inv = pow(ellp % ell, ell - 2, ell)
    u = (a * a % ell) * inv % ell
    if u == 4 % ell:
        return 1
    if u == 0:
        return 2
    if u == 1 % ell:
        return 3
    if u == 2 % ell:
        return 4
    if (u * u - 5 * u + 5) % ell == 0:
        return 5
    return 6


def certify(ell: int, primes: list[int]) -> dict:
    """Refute each maximal class for one ell, or report it undecided."""
    found: dict[str, dict | None] = {k: None for k in
                                     ("borel", "split_cartan_normalizer",
                                      "nonsplit_cartan_normalizer",
                                      "A4", "S4", "A5")}
    for ellp in primes:
        if ellp == ell:
            continue
        a = anchor.point_count_ap(BASE, ellp)
        disc = (a * a - 4 * ellp) % ell
        sq = red7.is_square_mod(disc, ell)
        if found["borel"] is None and not sq:
            found["borel"] = {"ell_prime": ellp, "a": a,
                              "a2_minus_4l_mod_ell": disc,
                              "reason": "a² − 4ℓ' is a non-residue, so the "
                                        "characteristic polynomial is "
                                        "irreducible mod ℓ"}
        if (found["split_cartan_normalizer"] is None
                and a % ell and not sq):
            found["split_cartan_normalizer"] = {
                "ell_prime": ellp, "a": a, "a2_minus_4l_mod_ell": disc,
                "reason": "trace ≢ 0 puts Frob in the Cartan itself, and a "
                          "split Cartan needs a² − 4ℓ' to be a residue"}
        if (found["nonsplit_cartan_normalizer"] is None
                and a % ell and disc % ell and sq):
            found["nonsplit_cartan_normalizer"] = {
                "ell_prime": ellp, "a": a, "a2_minus_4l_mod_ell": disc,
                "reason": "trace ≢ 0 and a² − 4ℓ' a nonzero residue: Frob is "
                          "in a split Cartan, which a nonsplit one excludes"}
        o = projective_order(a, ellp, ell)
        for name, allowed in EXCEPTIONAL.items():
            if found[name] is None and o not in allowed:
                found[name] = {"ell_prime": ellp, "a": a,
                               "projective_order": o,
                               "reason": f"projective order {o} is outside "
                                         f"{list(allowed)}"}
        if all(v is not None for v in found.values()):
            break
    undecided = [k for k, v in found.items() if v is None]
    return {"ell": ell, "witnesses": found, "undecided": undecided,
            "surjective": not undecided}


def ell_two() -> dict:
    """GL₂(F₂) ≅ S₃: surjective iff the 2-division cubic is irreducible with
    non-square discriminant. Computed rather than cited."""
    b2, b4, b6, b8, _ = anchor.b_invariants(BASE)
    # 4x³ + b2x² + 2b4x + b6, scaled to the monic cubic x³ + b2x² + 8b4x + 16b6
    # by x -> x/4; rational roots of the monic form are integers dividing 16b6
    A, B, C = b2, 8 * b4, 16 * b6
    n = abs(C) or 1
    divisors = [d for d in range(1, n + 1) if n % d == 0]
    roots = [r for d in divisors for r in (d, -d)
             if r ** 3 + A * r * r + B * r + C == 0]
    irreducible = not roots
    # disc(x³+Ax²+Bx+C) = 18ABC − 4A³C + A²B² − 4B³ − 27C²
    dcubic = (18 * A * B * C - 4 * A ** 3 * C + A * A * B * B
              - 4 * B ** 3 - 27 * C * C)
    # integer square root: a float sqrt is not a proof for large discriminants
    square = dcubic > 0 and math.isqrt(dcubic) ** 2 == dcubic
    sf, sq = abs(dcubic), 1
    for q in range(2, 400):
        while sf % (q * q) == 0:
            sf //= q * q
            sq *= q
    return {"ell": 2, "cubic": [1, A, B, C], "rational_roots": roots,
            "irreducible": irreducible, "discriminant": dcubic,
            "discriminant_is_a_square": square,
            "squarefree_part": -sf if dcubic < 0 else sf,
            "square_part": sq * sq,
            "surjective": irreducible and not square,
            "why": "GL₂(F₂) ≅ S₃; the image is all of S₃ exactly when the "
                   "2-division cubic is irreducible and its discriminant is "
                   "not a square"}


def vacuity_at_3() -> dict:
    """At ell = 3 the nonsplit-Cartan test cannot fire, and that is a proof.

    The refutation needs a good `ell'` with `a not= 0` and `a^2 - 4 ell'` a
    nonzero square mod 3. But mod 3 a nonzero trace forces `a^2 = 1`, and
    `4 = 1`, so `a^2 - 4 ell' = 1 - ell'`; asking that to be the nonzero square
    1 forces `ell' = 0 mod 3`, i.e. `ell' = 3`, which the test excludes. Four
    residue cases, exhausted, and the outcome is the same as RUN-031's `n = 2`:
    a criterion that no search length reaches, reported as vacuous rather than
    undecided.
    """
    rows = []
    for a in (1, 2):
        for lp in (1, 2):
            v = (a * a - 4 * lp) % 3
            rows.append({"a mod 3": a, "ell' mod 3": lp,
                         "a^2 - 4 ell' mod 3": v,
                         "nonzero square mod 3": v == 1})
    return {"cases": rows,
            "any_case_refutes": any(r["nonzero square mod 3"] for r in rows),
            "structurally_vacuous": not any(r["nonzero square mod 3"]
                                            for r in rows),
            "why": ("a nonzero trace forces a^2 = 1 mod 3 and 4 = 1, so "
                    "a^2 - 4 ell' = 1 - ell'; that is the nonzero square 1 "
                    "only when 3 divides ell', which the test excludes")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    primes = good_primes(SEARCH)
    two = ell_two()
    rows = [certify(ell, primes) for ell in mz.small_primes(ELL_BOUND)
            if ell > 3]
    three = certify(3, primes)
    three["S4_is_the_whole_group"] = True
    three["nonsplit_cartan_vacuity"] = vacuity_at_3()
    three["scope"] = ("two structural obstructions, not a short search: "
                      "PGL₂(F₃) ≅ S₄, so 'projective image S₄' IS "
                      "surjectivity and cannot be refuted; and the "
                      "nonsplit-Cartan test is vacuous mod 3, proved by "
                      "exhausting the four residue cases. A₄, A₅, the Borel "
                      "and the split Cartan normaliser are all refuted. This "
                      "ℓ is reported partially certified, not certified")
    three["surjective"] = False
    three["partially_certified"] = [k for k, v in three["witnesses"].items()
                                    if v is not None]

    certified = [r["ell"] for r in rows if r["surjective"]]
    undecided = {r["ell"]: r["undecided"] for r in rows if not r["surjective"]}
    mazur_covered = [n for n in MAZUR if n in certified or n == 2 and
                     two["surjective"]]

    ok = (two["surjective"] and not undecided and len(certified) == len(rows)
          and rows and three["surjective"] is False
          and three["nonsplit_cartan_vacuity"]["structurally_vacuous"])

    log = {
        "gate": "src38 — mod-ℓ surjectivity, certified where it can be",
        "source": "24_Manin_Period_Audit: 'base 696.e1 mod-ℓ images maximal "
                  "for all ℓ'",
        "curve": BASE,
        "method": ("refute every maximal class that a proper subgroup with "
                   "surjective determinant could lie in; one Frobenius "
                   "suffices per class, and the certificate is one-sided"),
        "good_primes_searched": len(primes), "search_bound": SEARCH,
        "ell_2": two,
        "ell_3": three,
        "ell_5_to_100": rows,
        "certified_surjective": [2] + certified if two["surjective"] else certified,
        "not_certified": {"3": three["scope"], **{str(k): v for k, v
                                                  in undecided.items()}},
        "mazur_degrees_certified": mazur_covered,
        "what_stays_cited": ("'for all ℓ' is Serre's theorem for a non-CM "
                             "curve — all but finitely many ℓ have surjective "
                             "ρ̄_ℓ — and that theorem is cited, not proved. "
                             "This gate certifies a finite range and says "
                             "which ℓ it did not reach"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  696.e1, {len(primes)} good primes below {SEARCH} as witnesses")
    print()
    print(f"  ℓ = 2   cubic {two['cubic']}  irreducible={two['irreducible']}  "
          f"disc={two['discriminant']} (squarefree part "
          f"{two['squarefree_part']}) square={two['discriminant_is_a_square']}"
          f"  → surjective: {two['surjective']}")
    print(f"  ℓ = 3   partially certified: {three['partially_certified']}")
    print(f"          {three['scope'][:74]}…")
    print(f"          nonsplit-Cartan test vacuous mod 3 over all "
          f"{len(three['nonsplit_cartan_vacuity']['cases'])} residue cases: "
          f"{three['nonsplit_cartan_vacuity']['structurally_vacuous']}")
    print()
    print(f"  {'ℓ':>4}  {'Borel':>7} {'N(spl)':>7} {'N(non)':>7} "
          f"{'A4':>5} {'S4':>5} {'A5':>5}   surjective")
    for r in rows:
        w = r["witnesses"]
        cells = [str(w[k]["ell_prime"]) if w[k] else "—"
                 for k in ("borel", "split_cartan_normalizer",
                           "nonsplit_cartan_normalizer", "A4", "S4", "A5")]
        print(f"  {r['ell']:>4}  {cells[0]:>7} {cells[1]:>7} {cells[2]:>7} "
              f"{cells[3]:>5} {cells[4]:>5} {cells[5]:>5}   {r['surjective']}")
    print()
    print(f"  certified surjective: ℓ = 2 and {len(certified)} primes "
          f"5 ≤ ℓ ≤ {ELL_BOUND}")
    print(f"  not certified: ℓ = 3 (S₄ is the whole projective group)"
          + (f", and {sorted(undecided)}" if undecided else ""))
    print(f"  of Mazur's twelve: {mazur_covered}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
