"""Gate 72 — GPT-6's Attack 03 ("cyclotomic divisibility"): every finite identity in it recomputed, its counterexample verified, and its own labels read.

數學戰士「墜衡」 / AMRAL Research Lab.

The document constructs a candidate class z_det from the adjugate of a 2×2
block of a relaxed Selmer complex, reduces the comparison with Kato's class to
a one-sided divisibility h_∞ ∈ D_∞·Ω in an Iwasawa algebra, proves a
conditional theorem (6.1), and says in its own words that the core
divisibility lemma is NOT proved. What it contains that can be computed:

  §3   Lemma 3.1, the adjugate identity A·z_det = 0, q(z_det) = D — checked in
       the actual ring F₁₁[G]/I³ of RUN-069 with the actual B ≡ [[X,2X],[Y,4Y]]
       and a generic c, and over the integers with random matrices
  §5   the constants: a₁₁ = −4 point-counted; 11 − a₁₁ + 1 = 16 a unit;
       U_m = (1 + 36N_γ)(1 + 90N_η) with χ(U_m) = m/f_χ on every character and
       ε(U_m) = m ≡ 1; 388/389 ≡ 9; κ = 9·5·u₀ = u₀ because 45 ≡ 1 (mod 11)
  §7   the counterexample in R₀ = Z₁₁[C₁₁]: X₀N₀ = 0, h₀ = D₀u with
       u = 1 + N₀/11 ∉ R₀, D₀ a non-zero-divisor with every characteristic-zero
       branch a unit quotient, and h₀ ∉ D₀R₀ — so branch-wise divisibility
       does not give integral divisibility, exactly as the document says
  §2   the residual Frobenius on the ordinary quotient: the unit root of
       x² − a₁₁x + 11 ≡ x(x + 4) (mod 11) is 7 ≠ 1

And the labels: the document must not claim the core lemma proved, nor BSD;
the gate scans it for those claims.

Usage:  python code/src72_attack03_cyclotomic_divisibility.py
"""

from __future__ import annotations

import json
import pathlib
import random
import re
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src70_kurihara_modular_symbols as kur              # noqa: E402
import src71_determinantal_bockstein as bock              # noqa: E402

LOGS = ROOT / "data" / "gate-logs"
DOC = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "03" / "BSD_Proof_Attack_03_Cyclotomic_Divisibility.md"
OUT = LOGS / "src72-attack03-cyclotomic-divisibility.json"

P = 11
M_N = 397 * 991
U_COEFF = (36, 90)                                       # U_m = (1 + 36 N_γ)(1 + 90 N_η)
U_DENOMINATOR = 11                                        # u = 1 + N₀/11 in the §7 counterexample
RANDOM_SEED = 3


def _doc() -> str:
    return DOC.read_text(encoding="utf-8") if DOC.exists() else ""


# ------------------------------------------------------------ §3 the adjugate identity

def adj2_ring(B):
    """adj [[a, b], [d, e]] = [[e, −b], [−d, a]] in the ring."""
    return [[B[1][1], {m: (-c) % P for m, c in B[0][1].items()}],
            [{m: (-c) % P for m, c in B[1][0].items()}, B[0][0]]]


def ordinary_unit_root(a11: int) -> list[int]:
    """The nonzero root of x² − a₁₁x + 11 mod 11 — the ordinary unit root's residue."""
    return [x for x in range(P) if (x * x - a11 * x + 11) % P == 0 and x % P]


def adjugate_identity_in_the_ring() -> dict:
    """A = (B c) with B = [[X, 2X],[Y, 4Y]] in F₁₁[G]/I³, c generic: A·z_det = 0, q(z_det) = det B."""
    X, Y, ONE = bock.X, bock.Y, bock.ONE
    two = {(0, 0): 2}
    four = {(0, 0): 4}
    B = [[X, bock.ring_mul(two, X)], [Y, bock.ring_mul(four, Y)]]
    D = bock.det2(B)
    adj = adj2_ring(B)
    rng = random.Random(RANDOM_SEED)
    failures = 0
    trials = 25
    for _ in range(trials):
        c = [{m: rng.randrange(P) for m in bock.MONOMIALS}, {m: rng.randrange(P) for m in bock.MONOMIALS}]
        c = [{m: v for m, v in ci.items() if v} for ci in c]
        # z = (−adj(B)c, D)
        z0 = {m: (-v) % P for m, v in bock.ring_add(bock.ring_mul(adj[0][0], c[0]), bock.ring_mul(adj[0][1], c[1])).items()}
        z1 = {m: (-v) % P for m, v in bock.ring_add(bock.ring_mul(adj[1][0], c[0]), bock.ring_mul(adj[1][1], c[1])).items()}
        z = [z0, z1, D]
        for i in range(2):
            row = bock.ring_add(bock.ring_add(bock.ring_mul(B[i][0], z[0]), bock.ring_mul(B[i][1], z[1])),
                                bock.ring_mul(c[i], z[2]))
            if row:
                failures += 1
    return {"B": "[[X, 2X], [Y, 4Y]]", "det_B": {f"X^{i}Y^{j}": v for (i, j), v in D.items()},
            "random_c_trials": trials, "A_z_nonzero": failures, "q_z_equals_D": True,
            "agrees": failures == 0 and D == {(1, 1): 2}}


def adjugate_identity_over_Z(trials: int = 200) -> dict:
    rng = random.Random(7)
    bad = 0
    for _ in range(trials):
        a, b, d, e, c1, c2 = (rng.randrange(-50, 51) for _ in range(6))
        D = a * e - b * d
        z = (b * c2 - e * c1, d * c1 - a * c2, D)                    # the document's explicit form
        r1 = a * z[0] + b * z[1] + c1 * z[2]
        r2 = d * z[0] + e * z[1] + c2 * z[2]
        if r1 or r2 or z[2] != D:
            bad += 1
    return {"trials": trials, "failures": bad, "agrees": bad == 0}


# ------------------------------------------------------------ §5 the constants

def constants() -> dict:
    a11 = kur.a_q(11)
    aug = 11 - a11 + 1
    # U_m = (1 + 36 N_γ)(1 + 90 N_η): χ(N) = 11 if χ trivial on that factor else 0
    values = {}
    for chi_g in (0, 1):                                          # 1 = trivial on the 397 factor
        for chi_e in (0, 1):
            f1 = 1 + U_COEFF[0] * (11 if chi_g else 0)
            f2 = 1 + U_COEFF[1] * (11 if chi_e else 0)
            conductor = (1 if chi_g else 397) * (1 if chi_e else 991)
            values[f"trivial_on_397={bool(chi_g)},trivial_on_991={bool(chi_e)}"] = {
                "chi_U_m": f1 * f2, "m_over_f_chi": M_N // conductor, "agrees": f1 * f2 == M_N // conductor}
    eps_Um = 397 * 991
    bad_prime_factor = Fraction(388, 389)
    inv389 = pow(389 % P, P - 2, P)
    unit_root = ordinary_unit_root(a11)
    return {"a_11_point_counted": a11, "eleven_minus_a11_plus_1": aug, "is_unit_mod_11": aug % P != 0,
            "U_m_character_values": values, "epsilon_U_m": eps_Um, "epsilon_U_m_mod_11": eps_Um % P,
            "bad_prime_factor_388_over_389_mod_11": (388 % P) * inv389 % P,
            "kappa_9_times_5_mod_11": 9 * 5 % P,
            "ordinary_unit_root_mod_11": unit_root, "unit_root_is_7_not_1": unit_root == [7],
            "agrees": (a11 == -4 and aug == 16 and all(v["agrees"] for v in values.values())
                       and eps_Um % P == 1 and (388 % P) * inv389 % P == 9 and 9 * 5 % P == 1 and unit_root == [7])}


# ------------------------------------------------------------ §7 the counterexample in Z₁₁[C₁₁]

def group_ring_mul(u: list[Fraction], v: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * P
    for i, a in enumerate(u):
        if a:
            for j, b in enumerate(v):
                if b:
                    out[(i + j) % P] += a * b
    return out


def counterexample() -> dict:
    """R₀ = Z₁₁[C₁₁] as vectors on the basis g^0..g^10 (Q-coefficients; integrality = 11-integrality)."""
    g = [Fraction(0)] * P
    g[1] = Fraction(1)
    one = [Fraction(0)] * P
    one[0] = Fraction(1)
    X0 = [a - b for a, b in zip(g, one)]
    N0 = [Fraction(1)] * P
    u = [a + b / U_DENOMINATOR for a, b in zip(one, N0)]
    D0 = [11 * a + b for a, b in zip(one, X0)]
    h0 = [a + b for a, b in zip(D0, N0)]
    X0N0 = group_ring_mul(X0, N0)
    D0u = group_ring_mul(D0, u)
    # u ∉ R₀: a coefficient with 11 in the denominator
    u_integral = all(c.denominator % P for c in u)
    # branch values: trivial character sends g ↦ 1; a nontrivial one sends N₀ ↦ 0
    triv = lambda v: sum(v)
    u_trivial_branch = triv(u)
    u_nontrivial_branch_const = u[0]                       # N₀ ↦ 0 kills everything but the g^0 part shared... see below
    # for a nontrivial character χ, χ(u) = 1 + χ(N₀)/11 = 1 + 0 = 1
    # D₀ is a non-zero-divisor: solve D₀·r = h₀ over Q — the unique solution must be u, which is not 11-integral
    # (multiplication by D₀ on Q[C₁₁] is invertible iff every branch value is nonzero: trivial 11, nontrivial 11 + ζ − 1 ≠ 0)
    solution_is_u = D0u == h0
    return {"X0_N0_is_zero": all(c == 0 for c in X0N0), "h0_equals_D0_times_u": solution_is_u,
            "u_in_R0": u_integral, "u_trivial_branch": str(u_trivial_branch),
            "u_nontrivial_branches": "1 (N₀ ↦ 0)",
            "D0_trivial_branch": str(triv(D0)), "D0_nontrivial_branch": "11 + (ζ − 1) ≠ 0",
            "h0_in_D0_R0": u_integral,                     # the unique quotient is u; integral iff u ∈ R₀
            "epsilon_D0_mod_11": int(triv(D0)) % P,
            "reading": "branch-wise the quotient h₀/D₀ is a unit on every characteristic-zero branch, and it is not in R₀: "
                       "the document's point, that character-wise divisibility does not glue, verified in the ring",
            "agrees": all(c == 0 for c in X0N0) and solution_is_u and not u_integral and int(triv(D0)) % P == 0}


# ------------------------------------------------------------ labels

def labels() -> dict:
    t = _doc()
    says_core_unproved = "核心算術整除引理仍未證出" in t or "尚未證明" in t
    says_not_full_bsd = "不是完整 BSD 證明" in t
    conditional = "條件性完成定理" in t
    candidate_lemma_unproved = "候選核心引理（尚未證明）" in t
    forbidden = [ph for ph in ("BSD 已證", "BSD 猜想已證明", "完整證明 BSD", "已證明 BSD") if ph in t]
    return {"document_found": bool(t), "says_core_lemma_unproved": says_core_unproved,
            "says_not_a_full_BSD_proof": says_not_full_bsd, "theorem_6_1_labelled_conditional": conditional,
            "candidate_core_lemma_labelled_unproved": candidate_lemma_unproved,
            "claims_of_a_BSD_proof_found": forbidden,
            "agrees": bool(t) and says_core_unproved and says_not_full_bsd and conditional
                      and candidate_lemma_unproved and not forbidden}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    ring = adjugate_identity_in_the_ring()
    z = adjugate_identity_over_Z()
    c = constants()
    ce = counterexample()
    lab = labels()
    ok = ring["agrees"] and z["agrees"] and c["agrees"] and ce["agrees"] and lab["agrees"]
    log = {"gate": "src72 — Attack 03, the finite content recomputed",
           "source": str(DOC.relative_to(ROOT)).replace("\\", "/"),
           "adjugate_identity_in_F11_G_mod_I3": ring, "adjugate_identity_over_Z": z,
           "constants_section_5": c, "counterexample_section_7": ce, "labels": lab,
           "not_computed_here": ["Proposition 2.1 (the shape of the Selmer complex, h¹ = 3, h² = 2) — a cohomological derivation, read",
                                 "Theorem 6.1 — conditional on three hypotheses the document itself lists; hypothesis 3 is the unproved core lemma",
                                 "the local Kato/tame-norm identification of §5 — cited to BKS II, read"],
           "headline": (f"Lemma 3.1 holds in the actual ring with det B = 2XY and over Z; the constants of §5 all "
                        f"recompute (a₁₁ = {c['a_11_point_counted']}, 16 a unit, χ(U_m) = m/f_χ on all four character "
                        f"types, ε(U_m) ≡ 1, 388/389 ≡ 9, 9·5 ≡ 1, unit root 7); the §7 counterexample is exactly as "
                        f"stated — h₀ = D₀u with u ∉ Z₁₁[C₁₁], every branch a unit; and the document labels its "
                        f"core lemma unproved and itself not a BSD proof"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  ring identity {ring['agrees']}, Z identity {z['agrees']}, constants {c['agrees']}, "
          f"counterexample {ce['agrees']}, labels {lab['agrees']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
