"""Gate 71 — P5 v1.3, "Determinantal Kurihara–Semilocal Closure": the finite Bockstein determinant computed in the truncated group ring, the scalar 3 shown to take every value in F₁₁^× under the changes the document permits, and Kim's hypotheses checked where they are checkable.

數學戰士「墜衡」 / AMRAL Research Lab.

v1.3 defines A = F₁₁[G], G ≅ C₁₁ × C₁₁, X = γ₃₉₇ − 1, Y = γ₉₉₁ − 1, the
operator B_N with matrix [[X, 2X], [Y, 4Y]], and states
det(B_N)(P∧Q) = 2·(e₃₉₇∧e₉₉₁) ⊗ XY — a one-line determinant in A/I³ — then
that [θ̄_n]₂ = 6·XY and 2·XY generate the same line, with ratio 6/2 = 3 "not
promoted to a canonical invariant". It also aligns the v1.2 isomorphism with
Chan-Ho Kim's semi-local theorem "under the standard residual-surjectivity,
Manin-constant, local-p-torsion, and Tamagawa hypotheses".

What this gate computes:

  §2–§3  A/I³ as the ring F₁₁[X, Y]/(X, Y)³ with the relation (1+X)^11 = 1
         automatic there; det(B_N) by the ring's own multiplication; the
         claim that ord_I(θ̄_n) = 2 and the line are invariant under generator
         changes γ ↦ γ^a, and that the XY coefficient is not
  §4     the ratio: with δ = 5 at the disclosed scale (RUN-068), the ratio
         5/2 = 8 there and 6/2 = 3 in the manuscript's; under changes of
         primitive root alone the ratio takes all ten values of F₁₁^× — a
         computed set, from the identity log_{g'} = log_{g'}(g)·log_g, checked
         on the actual 392,040-term sum for two other root pairs
  §1     Kim's hypotheses: p ≥ 5; good ordinary (a₁₁ = −4); ρ̄_{E,11}
         surjective, certified by Frobenius witnesses refuting every maximal
         subgroup class; E(ℚ₁₁)[11] = 0 from 11 ∤ #E(F₁₁) = 16 and e = 1 < 10;
         c₃₈₉ = 1 from v₃₈₉(Δ) = 1; trivial torsion from a gcd of point
         counts. The Manin constant is an external input and is not computed
  §5–§7  the labels: three closed, two open, and no report of this line
         closing either open one

Usage:  python code/src71_determinantal_bockstein.py
"""

from __future__ import annotations

import itertools
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src70_kurihara_modular_symbols as kur              # noqa: E402

LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "p5" / "files"
DOC = "BSD_P5_Determinantal_Kurihara_Semilocal_389a1_p11_v1.3.md"
OUT = LOGS / "src71-determinantal-bockstein.json"

P = 11
AINVS = [0, 1, 1, -2, 0]
M_LOC = ((1, 2), (1, 4))
THETA_MANUSCRIPT = 6
STATED = {"det_coefficient": 2, "ratio_manuscript": 3, "closed_labels": 3, "open_labels": 2}
SEARCH = 300                              # good primes searched for Frobenius witnesses
TORSION_BOUND = 60                        # good primes whose point counts are gcd-ed


def _doc() -> str:
    p = DOCS / DOC
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ------------------------------------------------------------ A / I³

MONOMIALS = ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2))


def ring_mul(u: dict, v: dict) -> dict:
    out: dict = {}
    for (i, j), a in u.items():
        for (k, l), b in v.items():
            if i + k + j + l <= 2:
                m = (i + k, j + l)
                out[m] = (out.get(m, 0) + a * b) % P
    return {m: c for m, c in out.items() if c}


def ring_add(u: dict, v: dict, sign: int = 1) -> dict:
    out = dict(u)
    for m, c in v.items():
        out[m] = (out.get(m, 0) + sign * c) % P
    return {m: c for m, c in out.items() if c}


def ring_pow(u: dict, e: int) -> dict:
    out = {(0, 0): 1}
    for _ in range(e):
        out = ring_mul(out, u)
    return out


X = {(1, 0): 1}
Y = {(0, 1): 1}
ONE = {(0, 0): 1}


def det2(m: list[list[dict]]) -> dict:
    return ring_add(ring_mul(m[0][0], m[1][1]), ring_mul(m[0][1], m[1][0]), -1)


def bockstein_determinant(mloc=M_LOC) -> dict:
    """B_N in the bases P, Q and e₃₉₇, e₉₉₁: row ℓ is λ_ℓ(·) ⊗ X_ℓ."""
    (a, b), (c, d) = mloc
    B = [[{(1, 0): a % P}, {(1, 0): b % P}], [{(0, 1): c % P}, {(0, 1): d % P}]]
    det = det2(B)
    scalar = (a * d - b * c) % P
    eleven_power = ring_pow(ring_add(ONE, X), P)         # (1 + X)^11 in A/I³
    return {"matrix": [[str(x) for x in row] for row in B], "det_in_A_mod_I3": {f"X^{i}Y^{j}": c for (i, j), c in det.items()},
            "det_is_scalar_times_XY": set(det) == {(1, 1)} and det[(1, 1)] == scalar,
            "scalar": det.get((1, 1), 0), "scalar_stated": STATED["det_coefficient"],
            "det_M_loc_mod_11": scalar,
            "one_plus_X_to_the_11_mod_I3": {f"X^{i}Y^{j}": c for (i, j), c in eleven_power.items()},
            "relation_gamma_to_the_11_is_automatic_mod_I3": eleven_power == ONE,
            "agrees": det.get((1, 1), 0) == STATED["det_coefficient"] and set(det) == {(1, 1)}}


def generator_change_invariance() -> dict:
    """γ₃₉₇ ↦ γ₃₉₇^a, γ₉₉₁ ↦ γ₉₉₁^b: X' = (1+X)^a − 1. The line F₁₁·XY and ord_I are
    invariant; the coefficient of XY scales by a·b, so every unit occurs."""
    coefficients = set()
    order_preserved = True
    line_preserved = True
    for a in range(1, P):
        for b in range(1, P):
            Xa = ring_add(ring_pow(ring_add(ONE, X), a), ONE, -1)
            Yb = ring_add(ring_pow(ring_add(ONE, Y), b), ONE, -1)
            elt = ring_mul(Xa, Yb)                       # X'Y' in terms of X, Y
            elt = {m: c * STATED["det_coefficient"] % P for m, c in elt.items()}
            elt = {m: c for m, c in elt.items() if c}
            if any(i + j < 2 for (i, j) in elt):
                order_preserved = False
            if set(elt) != {(1, 1)}:
                line_preserved = False
            coefficients.add(elt.get((1, 1), 0))
    return {"pairs_tested": (P - 1) ** 2, "ord_I_2_preserved": order_preserved,
            "line_F11_XY_preserved": line_preserved,
            "XY_coefficients_reached": sorted(coefficients),
            "every_unit_reached": coefficients == set(range(1, P))}


# ------------------------------------------------------------ the ratio

def ratio_under_primitive_roots(delta_at_5_6: int, check_pairs=((7, 11), (13, 7))) -> dict:
    """δ_{g',h'} = δ_{5,6} · log_{g'}(5) · log_{h'}(6) (mod 11) — checked on the
    actual sum for `check_pairs`, then used to list every ratio reachable."""
    lam = kur.eigenline()["lambda"]
    checks = []
    for g, h in check_pairs:
        # the predicted scale
        s397 = kur.log_table(397, g)[5]
        s991 = kur.log_table(991, h)[6]
        predicted = delta_at_5_6 * s397 * s991 % P
        old = dict(kur.ROOTS)
        kur.ROOTS[397], kur.ROOTS[991] = g, h
        try:
            actual = kur.kurihara_sum(lam)["delta_n_XY_coefficient"]
        finally:
            kur.ROOTS.update(old)
        checks.append({"roots": (g, h), "log_scale_397": s397, "log_scale_991": s991,
                       "predicted": predicted, "computed": actual, "agrees": predicted == actual})
    # every primitive root of 397 gives log_{g'}(5) ranging over all units mod 11
    scales397 = sorted({kur.log_table(397, g)[5] for g in range(2, 397) if _is_primitive(g, 397)})
    scales991 = sorted({kur.log_table(991, h)[6] for h in range(2, 991) if _is_primitive(h, 991)})
    ratios = sorted({delta_at_5_6 * a * b * pow(STATED["det_coefficient"], P - 2, P) % P
                     for a in scales397 for b in scales991})
    return {"delta_at_roots_5_6": delta_at_5_6, "det_coefficient": STATED["det_coefficient"],
            "ratio_at_disclosed_scale": delta_at_5_6 * pow(STATED["det_coefficient"], P - 2, P) % P,
            "ratio_manuscript_6_over_2": THETA_MANUSCRIPT * pow(STATED["det_coefficient"], P - 2, P) % P,
            "primitive_roots_mod_397": len([g for g in range(2, 397) if _is_primitive(g, 397)]),
            "primitive_roots_mod_991": len([h for h in range(2, 991) if _is_primitive(h, 991)]),
            "log_scales_reached_mod_11_at_397": scales397, "log_scales_reached_mod_11_at_991": scales991,
            "ratios_reachable_by_primitive_root_choice": ratios,
            "every_unit_is_a_reachable_ratio": ratios == list(range(1, P)),
            "identity_checked_on_the_full_sum": checks,
            "agrees": all(c["agrees"] for c in checks) and ratios == list(range(1, P))}


def _is_primitive(g: int, ell: int) -> bool:
    order = ell - 1
    for q in _prime_factors(order):
        if pow(g, order // q, ell) == 1:
            return False
    return True


def _prime_factors(n: int) -> list[int]:
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


# ------------------------------------------------------------ Kim's hypotheses

def _primes(limit: int) -> list[int]:
    s = bytearray([1]) * (limit + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(limit) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(limit + 1) if s[i]]


def _is_square_mod(a: int, ell: int) -> bool:
    a %= ell
    return a == 0 or pow(a, (ell - 1) // 2, ell) == 1


def _projective_order(a: int, ellp: int, ell: int) -> int:
    u = (a * a % ell) * pow(ellp % ell, ell - 2, ell) % ell
    if u == 4 % ell:
        return 1
    if u == 0:
        return 2
    if u == 1:
        return 3
    if u == 2:
        return 4
    if (u * u - 5 * u + 5) % ell == 0:
        return 5
    return 6


def residual_surjectivity(ell: int = P, search: int | None = None) -> dict:
    """ρ̄_{E,ell} surjective: refute Borel, both Cartan normalisers and the three
    exceptional projective images, each by one good Frobenius — RUN-036's method,
    reimplemented for 389.a1."""
    search = SEARCH if search is None else search
    found = {k: None for k in ("borel", "split_cartan_normalizer", "nonsplit_cartan_normalizer", "A4", "S4", "A5")}
    allowed = {"A4": (1, 2, 3), "S4": (1, 2, 3, 4), "A5": (1, 2, 3, 5)}
    for q in _primes(search):
        if q in (ell, 389):
            continue
        a = kur.a_q(q)
        disc = (a * a - 4 * q) % ell
        sq = _is_square_mod(disc, ell)
        if found["borel"] is None and not sq:
            found["borel"] = {"witness": q, "a": a}
        if found["split_cartan_normalizer"] is None and a % ell and not sq:
            found["split_cartan_normalizer"] = {"witness": q, "a": a}
        if found["nonsplit_cartan_normalizer"] is None and a % ell and disc and sq:
            found["nonsplit_cartan_normalizer"] = {"witness": q, "a": a}
        o = _projective_order(a, q, ell)
        for name, ok in allowed.items():
            if found[name] is None and o not in ok:
                found[name] = {"witness": q, "a": a, "projective_order": o}
        if all(v is not None for v in found.values()):
            break
    return {"ell": ell, "witnesses": found, "surjective": all(v is not None for v in found.values())}


def local_p_torsion(n11: int) -> dict:
    """E(ℚ₁₁)[11] ↪ Ẽ(F₁₁)[11] because E₁(ℚ₁₁) has no 11-torsion at e = 1 < p − 1."""
    return {"count_F11": n11, "eleven_divides_count": n11 % P == 0,
            "formal_group_torsion_free": "e = 1 < p − 1 = 10, so E₁(ℚ₁₁) has no 11-torsion",
            "E_Q11_11_is_zero": n11 % P != 0}


def kims_hypotheses() -> dict:
    n11 = kur.count_points_general(AINVS, P)
    a11 = P + 1 - n11
    lt = local_p_torsion(n11)
    surj = residual_surjectivity()
    gcd_counts = 0
    for q in _primes(TORSION_BOUND):
        if q != 389:
            gcd_counts = math.gcd(gcd_counts, kur.count_points_general(AINVS, q))
    inv = _b_c(AINVS)
    return {"p_at_least_5": P >= 5,
            "good_at_p": 389 % P != 0,
            "ordinary": {"count_mod_11": n11, "a_11": a11, "holds": a11 % P != 0},
            "residual_surjectivity": surj,
            "local_p_torsion": lt,
            "tamagawa": {"v_389_of_discriminant": _v(inv["disc"], 389), "c_389": 1 if _v(inv["disc"], 389) == 1 else None,
                         "holds": _v(inv["disc"], 389) == 1},
            "torsion": {"gcd_of_point_counts_good_p_below_60": gcd_counts, "trivial": gcd_counts == 1},
            "manin_constant": {"status": "EXTERNAL — LMFDB/Cremona record c = 1; not computed here"},
            "agrees": (a11 % P != 0 and surj["surjective"] and lt["E_Q11_11_is_zero"]
                       and _v(inv["disc"], 389) == 1 and gcd_counts == 1)}


def _b_c(a: list[int]) -> dict:
    a1, a2, a3, a4, a6 = a
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return {"disc": -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6}


def _v(n: int, p: int) -> int:
    v = 0
    while n and n % p == 0:
        n //= p
        v += 1
    return v


# ------------------------------------------------------------ labels

def labels(reports: dict[str, str]) -> dict:
    t = _doc()
    closed = t.count("\\mathrm{CLOSED}") + t.count("\\mathrm{CLOSED\\_EXACT}") + t.count("\\mathrm{CLOSED\\_UP\\_TO\\_UNITS}")
    opens = t.count("\\mathbf{OPEN}")
    open_names = ("CANON", "CPLX")
    offenders = [rn for rn, txt in reports.items()
                 if any(re.search(name + r"[^\n]{0,60}\b(closed|CLOSED|proved|PROVED)\b", txt) for name in open_names)]
    return {"closed_labels": closed, "closed_stated": STATED["closed_labels"],
            "open_labels": opens, "open_stated": STATED["open_labels"],
            "open_gates": ["P5-CANON-BocID", "P5-CPLX-GPR"],
            "reports_closing_an_open_gate": offenders,
            "section_8_instruction": "Do not recompute the finite group law or Kurihara sum — this line did both anyway: a certificate that has never been recomputed is a claim",
            "agrees": closed == 3 and opens == 2 and not offenders}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    doc = bool(_doc())
    bd = bockstein_determinant()
    gi = generator_change_invariance()
    log70 = kur.OUT
    delta = json.loads(log70.read_text(encoding="utf-8"))["kurihara"]["delta_n_XY_coefficient"] if log70.exists() else None
    ratio = ratio_under_primitive_roots(delta) if delta is not None else {"agrees": False}
    kim = kims_hypotheses()
    reports = {f.name[:7]: f.read_text(encoding="utf-8") for f in sorted(REPORTS.glob("RUN-*.md"))}
    lab = labels(reports)
    ok = (doc and bd["agrees"] and gi["ord_I_2_preserved"] and gi["line_F11_XY_preserved"]
          and gi["every_unit_reached"] and ratio["agrees"] and kim["agrees"] and lab["agrees"])
    log = {"gate": "src71 — P5 v1.3, the finite Bockstein determinant, the non-canonical ratio, Kim's hypotheses",
           "source": DOC, "document_found": doc,
           "bockstein_determinant": bd, "generator_change": gi, "ratio": ratio,
           "kims_hypotheses": kim, "labels": lab,
           "headline": (f"det(B_N) = {bd['scalar']}·XY in F₁₁[G]/I³ by the ring's own multiplication; under the "
                        f"{gi['pairs_tested']} generator changes the line and ord_I = 2 are invariant and the "
                        f"coefficient reaches every unit; the ratio θ/det is {ratio.get('ratio_at_disclosed_scale')} "
                        f"at the disclosed scale and 3 in the manuscript's, and primitive-root choice alone "
                        f"reaches all ten units — the document is right not to promote it; Kim's hypotheses hold "
                        f"where computable, ρ̄_11 surjective by witnesses, the Manin constant external; "
                        f"{lab['closed_labels']} closed labels, {lab['open_labels']} open, none closed by this line"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  det(B_N) = {bd['det_in_A_mod_I3']} ({bd['agrees']}); (1+X)^11 ≡ 1: {bd['relation_gamma_to_the_11_is_automatic_mod_I3']}")
    print(f"  generator changes: ord preserved {gi['ord_I_2_preserved']}, line preserved {gi['line_F11_XY_preserved']}, "
          f"coefficients {gi['XY_coefficients_reached']}")
    print(f"  ratio: disclosed {ratio.get('ratio_at_disclosed_scale')}, manuscript {ratio.get('ratio_manuscript_6_over_2')}, "
          f"reachable {ratio.get('ratios_reachable_by_primitive_root_choice')}; full-sum checks "
          f"{[c['agrees'] for c in ratio.get('identity_checked_on_the_full_sum', [])]}")
    print(f"  Kim: ordinary {kim['ordinary']['holds']}, surjective {kim['residual_surjectivity']['surjective']}, "
          f"E(Q_11)[11]=0 {kim['local_p_torsion']['E_Q11_11_is_zero']}, c_389 {kim['tamagawa']['c_389']}, "
          f"torsion trivial {kim['torsion']['trivial']}")
    print(f"  labels: closed {lab['closed_labels']}, open {lab['open_labels']}, offenders {lab['reports_closing_an_open_gate'] or 'none'}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
