"""Gate 73 — GPT-6's Attack 04: the mod-11 ordinary p-adic L-function of 389.a1 at conductor 121, recomputed from this tree's own modular symbols; μ = 0 and λ = 2 checked; the Euler-factor arithmetic checked; the theorem read.

數學戰士「墜衡」 / AMRAL Research Lab.

Attack 04's one new computation: with α the ordinary unit root of
x² − a₁₁x + 11 (α ≡ 7 mod 11), the measure
μ_α(a + 11²Z₁₁) = α⁻²[a/121]⁺ − α⁻³[a/11]⁺ is pushed to the cyclotomic
quotient (Z/121)^× → 1 + 11Z/121 ≅ Z/11 via a·ω(a)⁻¹ = 12^{j(a)}, giving
c_j = Σ_{j(a)=j} (9[a/121]⁺ − 6[a/11]⁺) in F₁₁, and then
L̄(t) = Σ_j c_j (1+t)^j in F₁₁[t]/(t¹¹). The document reports
c = (4,0,7,0,4,0,7,2,2,7,0), L̄ = 2t² + 2t³ + 2t⁴ + 5t⁶ + 6t⁷ + 10t⁸ + 7t⁹,
hence μ = 0, λ = 2. Its modular symbols are the stress-test package's
eigenline; this gate uses RUN-068's — the same functional at the same scale,
λ(1,5) = 1, reached by a third implementation — with its own paths,
Teichmüller lifts and logarithms, and compares all 110 summands to the
document's own per-summand table.

Also recomputed: α ≡ 7, α⁻² ≡ 9, α⁻³ ≡ 6; s₃₉₇ ≡ 3 and s₉₉₁ ≡ 2 (the
cyclotomic exponents of 397 and 991); the mod-11 Euler factors
(1 − (1+t)^{−s})² = 9t² + …, 4t² + …; 1 − 389⁻¹ ≡ 9; and that the
counterexample of Attack 03 (D₀ = 11 + X₀) has augmentation ≡ 0, which is why
Attack 04's Lemma 2.2 does not apply to it. Theorem 7.1 is read, not checked:
it rests on Kato's one-sided bound and Kataoka's Coleman map as cited.

Usage:  python code/src73_attack04_padic_l_mod11.py
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src70_kurihara_modular_symbols as kur              # noqa: E402

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "04"
DOC = EXT / "BSD_Proof_Attack_04_Mu_Zero_Descent.md"
THEIR_RESULT = EXT / "cyclotomic_result.json"
OUT = LOGS / "src73-attack04-padic-l-mod11.json"

P = 11
P2 = 121
GAMMA = 12                                                # 1 + 11, the document's topological generator
STATED = {"group_basis": [4, 0, 7, 0, 4, 0, 7, 2, 2, 7, 0],
          "t_basis": [0, 0, 2, 2, 2, 0, 5, 6, 10, 7, 0], "mu": 0, "lambda": 2,
          "alpha": 7, "alpha_inv2": 9, "alpha_inv3": 6, "s_397": 3, "s_991": 2}


def unit_root() -> dict:
    a11 = kur.a_q(11)
    roots = [x for x in range(P) if (x * x - a11 * x + 11) % P == 0]
    alpha = [x for x in roots if x % P][0]
    inv = pow(alpha, P - 2, P)
    return {"a_11": a11, "roots_of_x2_minus_a11x_plus_11_mod_11": roots, "alpha": alpha,
            "alpha_inv2": inv * inv % P, "alpha_inv3": inv ** 3 % P,
            "agrees": alpha == STATED["alpha"] and inv * inv % P == STATED["alpha_inv2"] and inv ** 3 % P == STATED["alpha_inv3"]}


def teichmuller(a: int) -> int:
    return pow(a, P, P2)                                  # a^11 is the 10th root of unity ≡ a (mod 11)


def gamma_exponent(a: int) -> int:
    """j with a·ω(a)⁻¹ ≡ 12^j (mod 121)."""
    w = teichmuller(a)
    target = a * pow(w, -1, P2) % P2
    for j in range(P):
        if pow(GAMMA, j, P2) == target:
            return j
    return None                                           # not in the 1 + 11Z direction: the lift is wrong, and the gate must go red, not raise


def symbol(lam: list[int], a: int, n: int) -> int:
    return sum(lam[i] for i in kur.path_indices(a, n)) % P


def symbol_at_level_p(lam: list[int], a: int) -> int:
    """[a/11]⁺ for the class of a mod 11 — the symbol is 1-periodic, so reducing a first is a convention."""
    return symbol(lam, a % P, P)


def cyclotomic_exponent(ell: int) -> int:
    """s_ℓ ≡ log⟨ℓ⟩/log 12 (mod 11): the exponent of ℓ mod 121 in the 1 + 11Z direction."""
    return gamma_exponent(ell % P2)


def measure(lam: list[int]) -> dict:
    ur = unit_root()
    c2, c3 = ur["alpha_inv2"], ur["alpha_inv3"]
    coeff = [0] * P
    summands = []
    unclassified = 0
    for a in range(1, P2):
        if a % P == 0:
            continue
        j = gamma_exponent(a)
        if j is None:
            unclassified += 1
            continue
        s2 = symbol(lam, a, P2)
        s1 = symbol_at_level_p(lam, a)
        mass = (c2 * s2 - c3 * s1) % P
        coeff[j] = (coeff[j] + mass) % P
        summands.append({"a": a, "gamma_exponent": j, "symbol_p2": s2, "symbol_p": s1, "mass": mass})
    # L̄(t) = Σ_j c_j (1+t)^j mod (11, t^11)
    t = [0] * P
    for j, cj in enumerate(coeff):
        if cj:
            # binomial expansion of (1+t)^j
            for k in range(j + 1):
                t[k] = (t[k] + cj * _binom(j, k)) % P
    nonzero = [k for k, v in enumerate(t) if v]
    mu = 0 if nonzero else None
    lam_inv = nonzero[0] if nonzero else None
    return {"summands": summands, "summand_count": len(summands), "unclassified_units": unclassified,
            "group_basis_coefficients": coeff,
            "t_basis_coefficients": t, "mu": mu, "lambda": lam_inv,
            "constant_term_zero": t[0] == 0, "linear_term_zero": t[1] == 0}


def _binom(n: int, k: int) -> int:
    from math import comb
    return comb(n, k) % P


def compare_with_theirs(mine: dict) -> dict:
    if not THEIR_RESULT.exists():
        return {"present": False}
    theirs = json.loads(THEIR_RESULT.read_text(encoding="utf-8"))
    t_by_a = {s["a"]: s for s in theirs.get("summands", [])}
    m_by_a = {s["a"]: s for s in mine["summands"]}
    diffs = []
    for a, s in m_by_a.items():
        u = t_by_a.get(a)
        if u is None or any(u[k] != s[k] for k in ("gamma_exponent", "symbol_p2", "symbol_p", "mass")):
            diffs.append(a)
    return {"present": True, "their_summands": len(t_by_a), "compared": len(m_by_a),
            "summands_that_differ": diffs,
            "their_group_basis": theirs.get("group_basis_coefficients"), "their_t_basis": theirs.get("t_basis_coefficients"),
            "their_mu": theirs.get("mu"), "their_lambda": theirs.get("lambda"),
            "agrees": (not diffs and len(t_by_a) == len(m_by_a)
                       and theirs.get("group_basis_coefficients") == mine["group_basis_coefficients"]
                       and theirs.get("t_basis_coefficients") == mine["t_basis_coefficients"])}


# ------------------------------------------------------------ Euler factors

def series_pow_1_plus_t(exp: int, terms: int = 5) -> list[int]:
    """(1+t)^exp mod 11 to O(t^terms), exp may be negative (mod 11 it is a unit power series)."""
    from math import comb
    if exp >= 0:
        return [comb(exp, k) % P for k in range(terms)]
    # (1+t)^{-e} = Σ_k C(-e, k) t^k with C(-e,k) = (-1)^k C(e+k-1, k)
    e = -exp
    return [((-1) ** k * comb(e + k - 1, k)) % P for k in range(terms)]


def series_mul(u: list[int], v: list[int]) -> list[int]:
    n = len(u)
    out = [0] * n
    for i, a in enumerate(u):
        for j, b in enumerate(v):
            if i + j < n:
                out[i + j] = (out[i + j] + a * b) % P
    return out


def euler_factors() -> dict:
    res = {}
    for ell, a_ell in ((397, kur.a_q(397)), (991, kur.a_q(991))):
        s = cyclotomic_exponent(ell)
        if s is None:
            s = 0
        # E_ℓ(t) = 1 − (a_ℓ/ℓ)σ⁻¹ + (1/ℓ)σ⁻², σ = (1+t)^s, all mod 11 with ℓ ≡ 1
        inv_ell = pow(ell % P, P - 2, P)
        sig_inv = series_pow_1_plus_t(-s)
        sig_inv2 = series_mul(sig_inv, sig_inv)
        E = [(1 if k == 0 else 0) for k in range(5)]
        E = [(E[k] - a_ell * inv_ell * sig_inv[k] + inv_ell * sig_inv2[k]) % P for k in range(5)]
        one_minus = [(1 if k == 0 else 0) - sig_inv[k] for k in range(5)]
        sq = series_mul([x % P for x in one_minus], [x % P for x in one_minus])
        res[str(ell)] = {"a_ell": a_ell, "a_ell_mod_11": a_ell % P, "s_ell": s, "E_ell_mod_11_to_t4": E,
                         "equals_(1-sigma_inv)^2": E == sq, "leading_coefficient": E[2],
                         "predicted_s_squared": s * s % P, "mu_zero": any(E)}
    res["389_factor_1_minus_389_inverse_mod_11"] = (1 - pow(389 % P, P - 2, P)) % P
    res["lambda_of_h0_as_2_plus_2_plus_2"] = 6
    res["attack03_counterexample_augmentation_of_11_plus_X0"] = 11 % P
    res["agrees"] = (res["397"]["s_ell"] == STATED["s_397"] and res["991"]["s_ell"] == STATED["s_991"]
                     and res["397"]["leading_coefficient"] == 9 and res["991"]["leading_coefficient"] == 4
                     and res["397"]["equals_(1-sigma_inv)^2"] and res["991"]["equals_(1-sigma_inv)^2"]
                     and res["389_factor_1_minus_389_inverse_mod_11"] == 9)
    return res


def labels() -> dict:
    t = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    return {"document_found": bool(t),
            "says_not_full_BSD": "沒有證明完整 BSD" in t,
            "says_R318_R319_open": "R318" in t and "R319" in t and "仍未關閉" in t,
            "says_unreviewed": "尚未經" in t,
            "theorem_7_1_rests_on_cited_theorems": "Kim–Lee–Ponsinet" in t and "Kataoka" in t,
            "agrees": bool(t) and "沒有證明完整 BSD" in t and "尚未經" in t}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    ur = unit_root()
    e = kur.eigenline()
    lam = e["lambda"]
    m = measure(lam)
    cmp_ = compare_with_theirs(m)
    ef = euler_factors()
    lab = labels()
    stated_ok = (m["group_basis_coefficients"] == STATED["group_basis"] and m["t_basis_coefficients"] == STATED["t_basis"]
                 and m["mu"] == 0 and m["lambda"] == 2 and m["unclassified_units"] == 0 and m["summand_count"] == 110)
    ok = ur["agrees"] and e["agrees"] and stated_ok and cmp_.get("agrees", False) and ef["agrees"] and lab["agrees"]
    log = {"gate": "src73 — Attack 04's mod-11 p-adic L-function, from this tree's modular symbols",
           "source": str(DOC.relative_to(ROOT)).replace("\\", "/"),
           "eigenline_scale": "λ(1,5) = 1, RUN-068's functional (first nonzero at index %s)" % e["first_nonzero_index"],
           "unit_root": ur,
           "measure": {k: v for k, v in m.items() if k != "summands"},
           "summands": m["summands"],
           "comparison_with_the_documents_table": cmp_,
           "euler_factors": ef, "labels": lab, "stated": STATED,
           "not_computed_here": ["Theorem 7.1 (Kato/cofactor comparison up to a unit) — conditional on Kato's bound and Kataoka's theorems as cited",
                                 "Lemmas 2.1–2.2 — algebra, read; the counterexample's augmentation checked",
                                 "the characteristic-zero order of vanishing — the document itself says mod-11 data does not give it"],
           "headline": (f"110 summands, group-basis coefficients {m['group_basis_coefficients']}, "
                        f"L̄(t) coefficients {m['t_basis_coefficients']}, μ = {m['mu']}, λ = {m['lambda']} — the document's "
                        f"figures to the summand ({len(cmp_.get('summands_that_differ', []))} of 110 differ); "
                        f"s₃₉₇ = {ef['397']['s_ell']}, s₉₉₁ = {ef['991']['s_ell']}, Euler leading terms "
                        f"{ef['397']['leading_coefficient']}t², {ef['991']['leading_coefficient']}t², 1 − 389⁻¹ ≡ "
                        f"{ef['389_factor_1_minus_389_inverse_mod_11']}"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  α = {ur['alpha']}, α⁻² = {ur['alpha_inv2']}, α⁻³ = {ur['alpha_inv3']}")
    print(f"  c_j = {m['group_basis_coefficients']} (stated {STATED['group_basis']})")
    print(f"  L̄(t) = {m['t_basis_coefficients']} (stated {STATED['t_basis']}); μ = {m['mu']}, λ = {m['lambda']}")
    print(f"  per-summand vs the document: {cmp_.get('compared')} compared, differ {cmp_.get('summands_that_differ')}")
    print(f"  s_397 = {ef['397']['s_ell']}, s_991 = {ef['991']['s_ell']}; E_397 = {ef['397']['E_ell_mod_11_to_t4']}, "
          f"E_991 = {ef['991']['E_ell_mod_11_to_t4']}; 1 − 389⁻¹ ≡ {ef['389_factor_1_minus_389_inverse_mod_11']}")
    print(f"  labels {lab['agrees']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
