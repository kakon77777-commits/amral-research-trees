"""Gate 86 — BSD Symbolic Rounds 010–012 (the web GPT's proof-obligation DAG, reciprocity-kernel dichotomy, adelic descent): the architecture document read against itself and against this line's logs, its one scalar identity evaluated on 389.a1 with the tree's own numbers; every boxed statement of the reciprocity round instantiated exactly on lines, two-dimensional spaces, binary forms and two-variable formal families, including the leading-term theorem and its directional failure; every boxed statement of the adelic round instantiated on explicit ideles of Q with rational components, and its rational-reconstruction mechanism run on a real object of this line — the formal parameter of [16]P on 389.a1 — with the explicit precision threshold.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 010 is a synthesis. What can be checked: the chain (5.1) parsed
from the document is A0 → … → A10 with the S/C/T alphabet and its only
two pure-T arrows are the two the text singles out (T1 at A3 → A4, T6 at
A8 → A9); the proof-obligation matrix (§31) is consistent with its own
typing (T ⟺ "no", C ⟺ "yes", S ⟺ "yes, already symbolic"), its six T rows
are T1–T6 of §25 in order, and the four cuts of (27.1) partition
{T1, …, T6}; the "symbolically closed" invariants S1–S8 are things this
line has instantiated (RUN-079, 082, 083 — read from those gate logs, the
named checks green), S9–S10 belong to Rounds 008–009 which were not in the
folder; and (24.1), L''(E,1)/2 = Ω_E·Reg(E)·q_fin, holds on 389.a1 with
the tree's own Ω (RUN-017), the regulator and L''/2 of RUN-026/073, with
q_fin = 1 (Tamagawa 1, torsion 1, Ш taken as 1), to 10⁻¹².

Round 011 (rank-2 transverse quotient Q = H/L is a line): the kernel
dichotomy (3.1–3.2), tensor nonannihilation (4.1), the order theorem
ord ℒ = e + m in the 𝔪-adic two-variable sense (5.1), one witness (7.1),
the lifted functional kills exactly L (8.2), the adapted-basis scalar
c' = uc (9.1), a nonzero annihilator vector gives a nonzero functional
under a perfect pairing (10.1), the 2×2 determinant criterion in a
non-adapted basis (11.3–11.5) and its corollary (12.1), nonannihilation ≠
directional criticality — a binary form with a rational root direction
(14.1), the directional order theorem along a path (15.1–15.2), the
one-variable case (17.1), cross-curve transport (19.2) and the calibrator
witness (20.1), the minimal leading-term theorem with its leading
coefficient U(0)·E_e(ξ)·λ(τ_m(ξ)) (23.1–23.2), the dim Q = 2 countermodel
(§25) and the determinant criterion for d = 2 (§26), the consistency
triangle (§30) — all on exact random instances.

Round 012 (ideles of Q): local lattice classes are valuations (2.1);
finite-support valuation vectors classify Q^×/{±1} with the positive
representative Π p^{d_p} (3.1–3.2, 13.1, 23.1); the split a = q₀·u with u
a unit idele (6.4); principal ⟺ every normalised component is one sign ε
(7.1–7.3), checked in both directions on diagonal and non-diagonal ideles;
the residual unit obstruction (8.1); ‖a‖ = |a_∞|/q₀ (9.3), ‖a‖ = 1 for
principal ideles (9.2), and the no-go (9.4) by an explicit idele of norm 1
with every valuation 0 that is not principal; lattice ≠ element descent
(10.1, 24.1); a² = Π p^{2d_p} (12.1, 32.1); S-unit reconstruction (14.1);
the finitely-many-exact-checks no-go (18.1); the restricted
principalisation theorem (19.1); the three-part ledger (20.3) and the
sign-compatibility it needs; and §21's rational reconstruction made
explicit — from a residue mod 11^k a fraction m/n with |m| ≤ M, 1 ≤ n ≤ N
is recovered by the extended Euclidean algorithm when 11^k > 2MN
(exhaustively unique at 11³ for M = N = 25; a collision at 11²), and the
same mechanism recovers the exact formal parameter z = −x/y of [16]P and
[16]Q on 389.a1 (RUN-072's points; z has 39- and 54-digit numerators and
denominators) from their residues mod 11^k once k passes the threshold —
and z mod 121 comes back as RUN-072's 99 and 66. One slip found: Theorem
19.1 lets the diagonal sign be ε = −1 while its hypothesis fixes u_p = 1
outside S; that idele is not principal by the round's own Theorem 7.1, so
the "if" direction holds only with ε = +1 (counterexample recorded).

Not verified: everything the documents list as T-type — actual descent,
support, reciprocity, complex comparison — and BSD.

Usage:  python code/src86_symbolic010_012_architecture_reciprocity_adelic.py
"""

from __future__ import annotations

import json
import math
import pathlib
import random
import re
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src15_phase2_anchor as anchor15                    # noqa: E402  real_period
import src26_rank2_bsd_identity as r2bsd                  # noqa: E402  DOC_REG, DOC_L2, DOC_TAMAGAWA, DOC_TORSION, AINVS

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt-symbolic-rounds"
DOCS = {"010": EXT / "BSD_Symbolic_Round_010_Four_Bridge_Closure_Diagram_and_Minimal_Missing_Theorems.md",
        "011": EXT / "BSD_Symbolic_Round_011_Reciprocity_Kernel_Nonannihilation_and_Minimal_Leading_Term_Theorem.md",
        "012": EXT / "BSD_Symbolic_Round_012_Adelic_Descent_Principal_Idele_Obstruction_and_Rational_Reconstruction.md"}
OUT = LOGS / "src86-symbolic010-012-architecture-reciprocity-adelic.json"

P = 11
RANDOM_SEED = 12
TRIALS = 40
DEG = 6                                                    # two-variable families truncated at this total degree
PRIMES = (2, 3, 5, 7, 11, 13)                              # the finite places an explicit idele carries; 1 elsewhere
AINVS = (0, 1, 1, -2, 0)                                   # 389.a1, y² + y = x³ + x² − 2x
GENERATORS = ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)))   # P, Q
REDUCTION_ORDER = 16                                       # #Ẽ(F₁₁), so [16]P, [16]Q lie in the formal group (RUN-072)

# --- the arithmetic the drill may disturb ---------------------------------------
Q_FIN = 1                                                  # Ш-factor in (24.1) for 389.a1: q_fin = Tamagawa · this / torsion²
ORDER_THEOREM_OFFSET = 0                                   # ord ℒ = e + m + this (5.1, 17.1, 23.1, 24.1 of Round 011)
KERNEL_DICHOTOMY_DIMENSION = 1                             # dim Q for which "λ ≠ 0 ⇒ ker λ = 0" is asserted (§25: fails at 2)
LEADING_TERM_INCLUDES_UNIT = True                          # (23.2): the leading coefficient carries U(0)
QUOTIENT_ENTRY = "d"                                       # (11.3): the induced quotient map of [[a, b], [0, d]] is d
PRINCIPAL_SIGN_SET = (1, -1)                               # the diagonal units of Q^× (7.1)
PADIC_ABS_EXPONENT_SIGN = -1                               # |x|_p = p^{sign · v_p(x)} (9.1)
RECONSTRUCTION_FACTOR = 2                                  # uniqueness of m/n mod p^k when p^k > FACTOR · M · N (§21)

# --- the closed invariants of Round 010 §29, and where this line instantiated them ----
CLOSED_INVARIANTS = {
    "S1": ("common scalar cancellation", "src81-symbolic001-cross-rank-calibration.json",
           [("symbolic_identities", "passed", "theorem_4_4"), ("symbolic_identities", "all_pass")]),
    "S2": ("rank-2 determinant gauge weight 2", "src84-symbolic002-004-determinant-jets.json",
           [("round_002", "checks", "5.2"), ("round_002", "checks", "9.1")]),
    "S3": ("paired regulator gauge weight 4", "src84-symbolic002-004-determinant-jets.json",
           [("round_002", "checks", "11.1"), ("round_004", "checks", "10.1")]),
    "S4": ("jet order does not change the determinant weight", "src84-symbolic002-004-determinant-jets.json",
           [("round_004", "checks", "9.1"), ("round_004", "checks", "23.1")]),
    "S5": ("projective jet unit invariance", "src84-symbolic002-004-determinant-jets.json",
           [("round_003", "checks", "4.2"), ("round_004", "checks", "6.3")]),
    "S6": ("Bockstein quotient sufficiency", "src84-symbolic002-004-determinant-jets.json",
           [("round_003", "checks", "14.2"), ("round_004", "checks", "17.2")]),
    "S7": ("lattice index n gives n² on the regulator", "src85-symbolic005-007-lattice-torsor-euler.json",
           [("round_005", "checks", "8.1"), ("round_005", "checks", "9.1")]),
    "S8": ("derived Euler additivity on cones and triangles", "src85-symbolic005-007-lattice-torsor-euler.json",
           [("round_007", "checks", "14.2"), ("round_007", "checks", "15.1"), ("round_007", "checks", "18.1")]),
    "N1": ("the Q_11-not-Q no-go, sqrt 3 to 11^12", "src85-symbolic005-007-lattice-torsor-euler.json",
           [("round_006", "checks", "4.1")]),
}
NOT_IN_FOLDER = {"S9": "regulator multiplicity one on the primal-dual line — Round 008",
                 "S10": "e + m ≤ r_an under the factorisation — Round 009; its equality case is Round 011 (5.1), checked here"}


def rnd(rng: random.Random, nonzero: bool = False) -> Fraction:
    while True:
        v = Fraction(rng.randint(-5, 5), rng.randint(1, 3))
        if v or not nonzero:
            return v


# ------------------------------------------------------------ Round 010

def dag_from_document(text: str) -> dict:
    """The chain (5.1) as the document writes it, and the two structural facts the text states about it."""
    i = text.index("tag{5.1}")
    block = text[text.rindex("boxed{", 0, i):i]
    nodes, arrows = [], []
    for node, arrow in re.findall(r"A(\d+)|xrightarrow\{([^}]+)\}", block):
        if node:
            nodes.append(int(node))
        else:
            arrows.append(arrow)
    chain = nodes == list(range(11)) and len(arrows) == 10
    alphabet = all(a in ("S", "C", "T", "S/C", "T/C", "C/T") for a in arrows)
    pure_t = [k for k, a in enumerate(arrows) if a == "T"]           # arrow k is A_k → A_{k+1}
    return {"nodes": nodes, "arrows": arrows, "is_chain": chain, "alphabet_ok": alphabet,
            "pure_theorem_arrows": pure_t,
            "pure_theorem_arrows_are_T1_and_T6": pure_t == [3, 8],       # §11: A3 → A4 is T1; §22: A8 → A9 is T6
            "agrees": chain and alphabet and pure_t == [3, 8]}


def obligation_matrix(text: str) -> dict:
    """§31 read against its own typing, §25's list and the cuts of (27.1)."""
    s31 = text[text.index("# 31."):text.index("# 32.")]
    rows = [[c.strip() for c in ln.strip("|").split("|")] for ln in s31.splitlines() if ln.startswith("|")][2:]
    expected = {"S": lambda ans: ans.startswith("yes"), "C": lambda ans: ans == "yes", "T": lambda ans: ans == "no",
                "C/T": lambda ans: ans in ("partially", "often yes"), "S/C": lambda ans: ans.startswith("yes")}
    typed = all(expected[r[1]](r[2]) for r in rows)
    t_rows = [r[0] for r in rows if r[1] == "T"]
    s25 = text[text.index("# 25."):text.index("# 26.")]
    t_list = re.findall(r"## T(\d)\. ([^\n]+)", s25)
    keys = ["descent", "support", "complex identification", "fundamental-line", "reciprocity", "complex-to"]
    order_ok = (len(t_rows) == 6 and [int(n) for n, _ in t_list] == [1, 2, 3, 4, 5, 6]
                and all(k in r for k, r in zip(keys, t_rows)) and all(k in n.lower() for k, (_, n) in zip(keys, t_list)))
    s27 = text[text.index("# 27."):text.index("# 28.")]
    cuts = [sorted(int(x) for x in set(re.findall(r"T(\d)", blk.split("代表", 1)[1]))) for blk in s27.split("## Cut")[1:]]
    flat = [t for c in cuts for t in c]
    partition = len(cuts) == 4 and sorted(flat) == [1, 2, 3, 4, 5, 6] and len(flat) == 6
    return {"rows": len(rows), "typing_consistent": typed, "theorem_rows": t_rows, "theorem_list_25": t_list,
            "theorem_rows_are_T1_to_T6": order_ok, "cuts_27_1": cuts, "cuts_partition_T1_T6": partition,
            "agrees": typed and order_ok and partition}


def closed_invariants() -> dict:
    """S1–S8 (and no-go N1) read from this line's own gate logs: the named checks are green there."""
    out, ok = {}, True
    cache = {}
    for key, (what, log, paths) in CLOSED_INVARIANTS.items():
        if log not in cache:
            cache[log] = json.loads((LOGS / log).read_text(encoding="utf-8"))
        vals = []
        for path in paths:
            v = cache[log]
            for step in path:
                v = v[step]
            vals.append(v)
        green = all(v is True or (isinstance(v, int) and not isinstance(v, bool) and v > 0) for v in vals)
        out[key] = {"what": what, "log": log, "values": vals, "green": green}
        ok &= green
    return {"instantiated_here": out, "not_in_folder": NOT_IN_FOLDER, "agrees": ok}


def instance_24_1() -> dict:
    """(24.1) on 389.a1 with the tree's own Ω, the regulator and L''/2, q_fin = Tamagawa·Ш/torsion²."""
    omega = anchor15.real_period(r2bsd.AINVS)
    reg, L2 = r2bsd.DOC_REG, r2bsd.DOC_L2
    q_fin = Fraction(r2bsd.DOC_TAMAGAWA * Q_FIN, r2bsd.DOC_TORSION ** 2)
    predicted = omega * reg * float(q_fin)
    ratio = L2 / predicted
    return {"curve": "389.a1", "omega": omega, "regulator": reg, "q_fin": str(q_fin), "L2_over_2": L2,
            "omega_reg_qfin": predicted, "ratio": ratio, "agrees": abs(ratio - 1.0) < 1e-12}


def round_010() -> dict:
    text = DOCS["010"].read_text(encoding="utf-8")
    dag, mat, closed, inst = dag_from_document(text), obligation_matrix(text), closed_invariants(), instance_24_1()
    return {"dag": dag, "matrix": mat, "closed_invariants": closed, "instance_24_1": inst,
            "agrees": dag["agrees"] and mat["agrees"] and closed["agrees"] and inst["agrees"]}


# ------------------------------------------------------------ two-variable formal algebra (Round 011)

def p2_mul(a: dict, b: dict) -> dict:
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            if i + j + k + l <= DEG:
                out[(i + k, j + l)] = out.get((i + k, j + l), Fraction(0)) + x * y
    return {k: v for k, v in out.items() if v}


def p2_scale(a: dict, c: Fraction) -> dict:
    return {k: c * v for k, v in a.items() if c * v}


def p2_order(a: dict):
    return min((i + j for (i, j), v in a.items() if v), default=None)


def p2_path(a: dict, xi) -> list:
    """(X, t) = (ξ₀s, ξ₁s): the coefficients in s."""
    out = [Fraction(0)] * (DEG + 1)
    for (i, j), v in a.items():
        out[i + j] += v * xi[0] ** i * xi[1] ** j
    return out


def s_order(coeffs: list):
    return next((k for k, v in enumerate(coeffs) if v), None)


def p2_random(rng: random.Random, low: int, high: int = DEG) -> dict:
    out = {}
    for i in range(high + 1):
        for j in range(high + 1 - i):
            if i + j >= low:
                out[(i, j)] = rnd(rng)
    if not any(v for (i, j), v in out.items() if i + j == low):
        out[(low, 0)] = Fraction(1)
    return {k: v for k, v in out.items() if v}


def form_with_root(rng: random.Random, m: int, r: Fraction) -> dict:
    """A binary form of degree m divisible by (X − r·t): zero on the direction (r, 1)."""
    g = {(i, m - 1 - i): rnd(rng) for i in range(m)}
    if not any(g.values()):
        g[(0, m - 1)] = Fraction(1)
    f = {}
    for (i, j), v in g.items():
        f[(i + 1, j)] = f.get((i + 1, j), Fraction(0)) + v
        f[(i, j + 1)] = f.get((i, j + 1), Fraction(0)) - r * v
    return {k: v for k, v in f.items() if v}


def form_eval(f: dict, xi) -> Fraction:
    return sum((v * xi[0] ** i * xi[1] ** j for (i, j), v in f.items()), Fraction(0))


def det2(M) -> Fraction:
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def mat_vec(A, v):
    return [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]


def inv2(M):
    d = det2(M)
    return [[M[1][1] / d, -M[0][1] / d], [-M[1][0] / d, M[0][0] / d]]


def random_invertible(rng: random.Random):
    while True:
        M = [[rnd(rng), rnd(rng)], [rnd(rng), rnd(rng)]]
        if det2(M):
            return M


def dichotomy_holds(rng: random.Random, dim: int, samples: int = 20) -> bool:
    """'every nonzero linear map K^dim → K has zero kernel' — true for dim = 1, false for dim = 2 (§25)."""
    for _ in range(samples):
        f = [rnd(rng) for _ in range(dim)]
        if not any(f):
            continue
        if dim == 1:
            kernel_vector = None
        else:                                                    # a nonzero vector in ker f, explicitly
            i = next(k for k, x in enumerate(f) if x)
            j = (i + 1) % dim
            kernel_vector = [Fraction(0)] * dim
            kernel_vector[i], kernel_vector[j] = -f[j], f[i]
            if not any(kernel_vector):
                kernel_vector = None
        if kernel_vector is not None and sum(a * b for a, b in zip(f, kernel_vector)) == 0:
            return False
    return True


# ------------------------------------------------------------ Round 011

def round_011(rng: random.Random) -> dict:
    keys = ("3.1", "3.2", "4.1", "5.1", "7.1", "8.2", "9.1", "10.1", "11.3", "12.1", "14.1", "15.1", "15.2",
            "17.1", "19.2", "20.1", "23.1", "23.2", "25", "26", "30")
    ok = {k: True for k in keys}
    n_zero = 0
    for trial in range(TRIALS):
        c = Fraction(0) if trial % 4 == 3 else rnd(rng, True)          # the reciprocity scalar λ: Q → A; a quarter are zero
        n_zero += c == 0
        sample_q = [Fraction(1), Fraction(-3, 2), Fraction(7), rnd(rng, True)]
        # (3.1)–(3.2): ker λ = Q ⟺ λ = 0; λ ≠ 0 ⇒ ker λ = 0
        killed = [q for q in sample_q if c * q == 0]
        ok["3.1"] &= (len(killed) == len(sample_q)) == (c == 0)
        ok["3.2"] &= (c == 0) or not killed
        # (4.1): id_V ⊗ λ on V ⊗ Q ≅ V^{m+1}: τ ↦ cτ
        m = rng.randint(1, 3)
        tau = [rnd(rng) for _ in range(m + 1)]
        if not any(tau):
            tau[0] = Fraction(1)
        ok["4.1"] &= (any(c * x for x in tau)) == (c != 0)
        # the two-variable factorisation ℒ = U·E·λ(Z_tr): U a unit, ord E = e, Z_tr with first form τ_m of degree m
        e = rng.randint(0, 2)
        U = p2_random(rng, 0)
        if not U.get((0, 0)):
            U[(0, 0)] = Fraction(1)
        E = p2_random(rng, e)
        r_root = rnd(rng)
        tau_m = form_with_root(rng, m, r_root)                            # zero on ξ_crit = (r, 1)
        Z = dict(tau_m)
        Z.update(p2_random(rng, m + 1))
        Z = {k: v for k, v in Z.items() if v}
        L = p2_mul(p2_mul(U, E), p2_scale(Z, c))
        # (5.1): 𝔪-adic order e + m when λ ≠ 0; ℒ ≡ 0 when λ = 0 (the channel-zero case of §31)
        if c:
            ok["5.1"] &= p2_order(L) == e + m + ORDER_THEOREM_OFFSET
        else:
            ok["5.1"] &= p2_order(L) is None
        # (7.1): one witness decides
        q = rnd(rng, True)
        ok["7.1"] &= (c * q != 0) == (c != 0)
        # (8.2): λ̃ = λ∘π on H = K², κ = (1, 0), π(x) = x₁: ker λ̃ = L ⟺ λ ≠ 0, = H ⟺ λ = 0
        vectors = [[rnd(rng), rnd(rng)] for _ in range(8)] + [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
        in_ker = [c * x[1] == 0 for x in vectors]
        in_L = [x[1] == 0 for x in vectors]
        ok["8.2"] &= (in_ker == in_L) if c else all(in_ker)
        # (9.1): in the basis (κ, q) with λ̃(q) = c, the lift q' = uq + aκ gives c' = uc
        qv = [rnd(rng), rnd(rng, True)]
        u, a = rnd(rng, True), rnd(rng)
        lam_tilde = lambda x, _q=qv: c * x[1] / _q[1]                  # noqa: E731  λ̃(κ) = 0, λ̃(q) = c
        q_prime = [u * qv[0] + a, u * qv[1]]
        ok["9.1"] &= lam_tilde(q_prime) == u * c and lam_tilde([Fraction(1), Fraction(0)]) == 0
        # (10.1): perfect pairing β(x, η) = xᵀBη; η spanning L^⊥; λ_η descends and is nonzero
        B = random_invertible(rng)
        eta = [-B[0][1], B[0][0]]                                         # β(κ, η) = B₀₀η₀ + B₀₁η₁ = 0
        beta = lambda x, y, _B=B: sum(x[i] * _B[i][j] * y[j] for i in range(2) for j in range(2))   # noqa: E731
        ok["10.1"] &= any(eta) and beta([Fraction(1), Fraction(0)], eta) == 0 and beta([Fraction(0), Fraction(1)], eta) != 0
        # (11.3)–(11.5), (12.1): Φ: H → W with Φ(L) ⊂ L_W, Φ|_L ≠ 0, in a non-adapted basis
        aa, bb, dd = rnd(rng, True), rnd(rng), (Fraction(0) if trial % 5 == 4 else rnd(rng, True))
        Pm, Pw = random_invertible(rng), random_invertible(rng)
        Phi = mat_mul(Pw, mat_mul([[aa, bb], [Fraction(0), dd]], inv2(Pm)))
        kappa, qH = mat_vec(Pm, [Fraction(1), Fraction(0)]), mat_vec(Pm, [Fraction(0), Fraction(1)])
        kappa_w, q_w = mat_vec(Pw, [Fraction(1), Fraction(0)]), mat_vec(Pw, [Fraction(0), Fraction(1)])
        img_kappa, img_q = mat_vec(Phi, kappa), mat_vec(Phi, qH)
        coords = lambda v, _Pw=Pw: mat_vec(inv2(_Pw), v)                # noqa: E731  coordinates in (κ_W, q_W)
        ck, cq = coords(img_kappa), coords(img_q)
        respects = ck[1] == 0 and ck[0] == aa                             # Φ(κ) = aκ_W ∈ L_W, Φ|_L ≠ 0
        induced = cq[1] if QUOTIENT_ENTRY == "d" else cq[0]              # the induced map H/L → W/L_W on the class of q
        ok["11.3"] &= respects and (det2(Phi) != 0) == (induced != 0) == (dd != 0)
        mu = rnd(rng, True)
        ok["12.1"] &= ((det2(Phi) != 0 and mu != 0) == (mu * induced != 0))
        # (14.1): (id ⊗ λ)(τ_m) = c·τ_m ≠ 0 while τ_m(ξ_crit) = 0 — nonannihilation is not directional noncriticality
        xi_crit = [r_root, Fraction(1)]
        while True:
            xi_gen = [rnd(rng, True), rnd(rng, True)]
            if form_eval(tau_m, xi_gen) != 0:
                break
        ok["14.1"] &= (form_eval(tau_m, xi_crit) == 0) and (any(v for v in p2_scale(tau_m, c).values()) == (c != 0))
        # (15.1)–(15.2), (23.1)–(23.2): along the paths sξ_gen and sξ_crit
        if c:
            path_gen, path_E = p2_path(L, xi_gen), p2_path(E, xi_gen)
            e_xi = s_order(path_E)
            r_xi = s_order(path_gen)
            ok["15.1"] &= r_xi == e_xi + m + ORDER_THEOREM_OFFSET
            ok["23.1"] &= r_xi == e_xi + m + ORDER_THEOREM_OFFSET
            lead = (U[(0, 0)] if LEADING_TERM_INCLUDES_UNIT else Fraction(1)) * path_E[e_xi] * c * form_eval(tau_m, xi_gen)
            ok["23.2"] &= path_gen[r_xi] == lead
            r_crit = s_order(p2_path(L, xi_crit))
            e_crit = s_order(p2_path(E, xi_crit))
            ok["15.2"] &= (r_crit is None) or (e_crit is None) or (r_crit > e_crit + m)
        # (17.1): one variable — Z(t) = t^m·(unit): ord ℒ = e + m exactly, no direction to choose
        if c:
            Z1 = {(0, j): rnd(rng) for j in range(m, DEG + 1)}
            Z1[(0, m)] = rnd(rng, True)
            E1 = {(0, j): rnd(rng) for j in range(e, DEG + 1)}
            E1[(0, e)] = rnd(rng, True)
            U1 = {(0, j): rnd(rng) for j in range(0, DEG + 1)}
            U1[(0, 0)] = rnd(rng, True)
            ok["17.1"] &= p2_order(p2_mul(p2_mul(U1, E1), p2_scale(Z1, c))) == e + m + ORDER_THEOREM_OFFSET
        # (19.2), (20.1): ψ_i λ_i = u_i λ_* φ_i with φ, ψ, u invertible; a calibrator witness b₀ = λ₀(q₀) ≠ 0
        lam_star = c
        lam_partners = []
        for _i in range(3):
            phi, psi, ui = rnd(rng, True), rnd(rng, True), rnd(rng, True)
            lam_i = ui * lam_star * phi / psi
            ok["19.2"] &= psi * lam_i == ui * lam_star * phi and ((lam_i == 0) == (lam_star == 0))
            lam_partners.append(lam_i)
        q0 = rnd(rng, True)
        b0 = lam_partners[0] * q0
        ok["20.1"] &= (b0 != 0) == all(l != 0 for l in lam_partners)
        # §25: the dichotomy is asserted for dim Q = KERNEL_DICHOTOMY_DIMENSION; §26: det Λ ≠ 0 ⇒ injective for d = 2
        ok["25"] &= dichotomy_holds(rng, KERNEL_DICHOTOMY_DIMENSION) and not dichotomy_holds(rng, 2)
        Lam = random_invertible(rng)
        tau2 = [rnd(rng), rnd(rng)]
        if not any(tau2):
            tau2[0] = Fraction(1)
        ok["26"] &= any(mat_vec(Lam, tau2))
        # §30: the consistency triangle — order equality and τ_m(ξ) ≠ 0 force λ ≠ 0 (contrapositive on the zero trials)
        if not c:
            ok["30"] &= s_order(p2_path(L, xi_gen)) is None
    return {"trials": TRIALS, "zero_channel_trials": n_zero, "checks": ok, "agrees": all(ok.values())}


# ------------------------------------------------------------ Round 012

def valuation(x: Fraction, ell: int) -> int:
    v, num, den = 0, abs(x.numerator), x.denominator
    if num == 0:
        raise ZeroDivisionError("valuation of 0")
    while num % ell == 0:
        num //= ell
        v += 1
    while den % ell == 0:
        den //= ell
        v -= 1
    return v


def prime_factors(n: int) -> set:
    out, m, q = set(), abs(n), 2
    while q * q <= m:
        while m % q == 0:
            out.add(q)
            m //= q
        q += 1
    if m > 1:
        out.add(m)
    return out


def positive_representative(a: Fraction) -> Fraction:
    """(3.2): Π p^{v_p(a)} over the support of a."""
    out = Fraction(1)
    for p_ in prime_factors(a.numerator) | prime_factors(a.denominator):
        out *= Fraction(p_) ** valuation(a, p_)
    return out


def split(a: dict) -> tuple:
    """(6.1)–(6.4): d_p, q₀ = Π p^{d_p}, and the unit idele u = a/q₀."""
    d = {p_: valuation(a[p_], p_) for p_ in PRIMES}
    q0 = Fraction(1)
    for p_ in PRIMES:
        q0 *= Fraction(p_) ** d[p_]
    u = {v: a[v] / q0 for v in a}
    return d, q0, u


def is_principal(a: dict) -> bool:
    """An idele with rational components is the diagonal image of q ∈ Q^× iff every component equals q."""
    return len(set(a.values())) == 1


def criterion_7_1(u: dict) -> bool:
    return any(all(u[v] == eps for v in u) for eps in PRINCIPAL_SIGN_SET)


def idele_norm(a: dict) -> Fraction:
    n = abs(a["inf"])
    for p_ in PRIMES:
        n *= Fraction(p_) ** (PADIC_ABS_EXPONENT_SIGN * valuation(a[p_], p_))
    return n


def random_rational(rng: random.Random) -> Fraction:
    """A random element of Q^× supported on PRIMES — the ideles here carry components only there, 1 elsewhere."""
    a = Fraction(rng.choice([-1, 1]))
    for p_ in PRIMES:
        a *= Fraction(p_) ** rng.randint(-2, 2)
    return a


def random_unit_at(rng: random.Random, p_: int) -> Fraction:
    while True:
        u = Fraction(rng.randint(1, 30), rng.randint(1, 30))
        if valuation(u, p_) == 0 and u != 1:
            return u


def rational_reconstruct(r: int, mod: int, M: int, N: int):
    """m/n ≡ r (mod `mod`) with |m| ≤ M, 1 ≤ n ≤ N by the extended Euclidean algorithm (Wang); None if none found."""
    r %= mod
    r0, r1 = mod, r
    s0, s1 = 0, 1
    while r1 > M:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    n = abs(s1)
    m = r1 if s1 > 0 else -r1
    if n == 0 or n > N or math.gcd(abs(m), n) != 1 or (m - n * r) % mod:
        return None
    return Fraction(m, n)


def exhaustive_uniqueness(mod: int, M: int, N: int):
    """All admissible m/n (|m| ≤ M, 1 ≤ n ≤ N, gcd 1, p ∤ n) have distinct residues mod `mod`, or the first collision."""
    seen = {}
    for m_ in range(-M, M + 1):
        for n_ in range(1, N + 1):
            if n_ % P == 0 or math.gcd(abs(m_), n_) != 1:
                continue
            r = m_ * pow(n_, -1, mod) % mod
            if r in seen:
                return False, (str(seen[r]), f"{m_}/{n_}", r)
            seen[r] = Fraction(m_, n_)
    return True, None


def reconstruction_threshold(M: int, N: int) -> int:
    k = 1
    while P ** k <= RECONSTRUCTION_FACTOR * M * N:
        k += 1
    return k


# --- the real object: [16]P and [16]Q on 389.a1, their formal parameters z = −x/y (RUN-072's objects) ---

def ec_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    a1, a2, a3, a4, a6 = AINVS
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        if y1 + y2 + a1 * x2 + a3 == 0:
            return None
        lam = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) / (2 * y1 + a1 * x1 + a3)
        nu = (-x1 ** 3 + a4 * x1 + 2 * a6 - a3 * y1) / (2 * y1 + a1 * x1 + a3)
    else:
        lam = (y2 - y1) / (x2 - x1)
        nu = (y1 * x2 - y2 * x1) / (x2 - x1)
    x3 = lam * lam + a1 * lam - a2 - x1 - x2
    return (x3, -(lam + a1) * x3 - nu - a3)


def ec_mul(k: int, pt):
    result, addend = None, pt
    while k:
        if k & 1:
            result = ec_add(result, addend)
        addend = ec_add(addend, addend)
        k >>= 1
    return result


def on_curve(pt) -> bool:
    a1, a2, a3, a4, a6 = AINVS
    x, y = pt
    return y * y + a1 * x * y + a3 * y == x ** 3 + a2 * x * x + a4 * x + a6


def reconstruct_formal_parameter(label: str, pt) -> dict:
    """z([16]pt) = −x/y exactly, then back from its residue mod 11^k at the threshold, and at a third of it."""
    R = ec_mul(REDUCTION_ORDER, pt)
    if R is None or not on_curve(R):
        return {"point": label, "agrees": False}
    z = -R[0] / R[1]
    if z.denominator % P == 0:
        return {"point": label, "agrees": False, "why": "z not 11-integral"}
    digits_m, digits_n = len(str(abs(z.numerator))), len(str(z.denominator))
    M, N = 10 ** digits_m, 10 ** digits_n
    k = reconstruction_threshold(M, N)
    mod = P ** k
    r = z.numerator * pow(z.denominator, -1, mod) % mod
    got = rational_reconstruct(r, mod, M, N)
    k_low = max(1, k // 3)
    mod_low = P ** k_low
    got_low = rational_reconstruct(z.numerator * pow(z.denominator, -1, mod_low) % mod_low, mod_low, M, N)
    return {"point": label, "v11_of_z": valuation(z, P), "z_mod_121": z.numerator * pow(z.denominator, -1, 121) % 121,
            "numerator_digits": digits_m, "denominator_digits": digits_n, "height_bound_log10_MN": digits_m + digits_n,
            "threshold_k": k, "recovered_exactly": got == z,
            "below_threshold": {"k": k_low, "recovered": got_low == z, "result": None if got_low is None else str(got_low)},
            "agrees": got == z}


def round_012(rng: random.Random) -> dict:
    keys = ("2.1", "3.2", "3.1-injective", "6.4", "7.1", "7.3", "8.1", "9.2", "9.3", "9.4", "10.1", "12.1", "14.1",
            "18.1", "19.1", "19.1-literal-fails-at-minus-one", "20.3", "23.1", "21")
    ok = {k: True for k in keys}
    literal_19_1_counterexample = None
    for trial in range(TRIALS):
        a = random_rational(rng)
        # (2.1): the local lattice class is the valuation; a p-unit factor is invisible
        for ell in (2, 3, 5):
            ok["2.1"] &= valuation(random_unit_at(rng, ell) * a, ell) == valuation(a, ell)
        # (3.1)–(3.2), (13.1): the positive representative from the valuation vector; injective mod sign
        a0 = positive_representative(a)
        ok["3.2"] &= a0 == abs(a) and a0 > 0
        b = -a if trial % 3 == 0 else random_rational(rng)
        vec = lambda x: tuple(valuation(x, p_) for p_ in sorted(prime_factors(a.numerator) | prime_factors(a.denominator)   # noqa: E731
                                                                | prime_factors(b.numerator) | prime_factors(b.denominator)))
        ok["3.1-injective"] &= (vec(a) == vec(b)) == (abs(a) == abs(b))
        # the diagonal idele of a, and (6.4), (7.1)–(7.3), (9.2)
        diag = {p_: a for p_ in PRIMES}
        diag["inf"] = a
        d, q0, u = split(diag)
        ok["6.4"] &= all(valuation(u[p_], p_) == 0 for p_ in PRIMES) and q0 == a0
        ok["7.1"] &= is_principal(diag) and criterion_7_1(u)
        eps = 1 if a > 0 else -1
        ok["7.3"] &= all(diag[v] == eps * q0 for v in diag)
        ok["9.2"] &= idele_norm(diag) == 1
        # a non-diagonal idele: random components — the criterion agrees with principality in both directions
        nd = {p_: random_rational(rng) for p_ in PRIMES}
        nd["inf"] = random_rational(rng)
        if trial % 2:
            nd[13] = nd[2]                                                # occasionally repeat a component
        _, _, u_nd = split(nd)
        ok["7.1"] &= is_principal(nd) == criterion_7_1(u_nd)
        # (9.1), (9.3): ‖a‖ = |a_∞|·Π|a_p|_p = |a_∞|/q₀ on the random idele
        d_nd, q0_nd, _ = split(nd)
        ok["9.3"] &= idele_norm(nd) == abs(nd["inf"]) / q0_nd
        # (8.1), (9.4), (10.1), (24.1): units at every finite place, a_∞ = q₀ — norm 1, every valuation that of q₀, not principal
        pert = {p_: random_unit_at(rng, p_) * a0 for p_ in PRIMES}
        pert["inf"] = a0
        d_pert, q0_pert, u_pert = split(pert)
        ok["8.1"] &= d_pert == d and not criterion_7_1(u_pert) and all(valuation(u_pert[p_], p_) == 0 for p_ in PRIMES)
        ok["9.4"] &= idele_norm(pert) == 1 and not is_principal(pert)
        ok["10.1"] &= q0_pert == q0 and not is_principal(pert)            # same lattice class everywhere, no global element
        # (12.1), (32.1): a² from the valuations alone
        ok["12.1"] &= a * a == a0 * a0
        # (14.1): an S-unit is its valuations on S, up to sign
        S = sorted(rng.sample(PRIMES, rng.randint(1, 4)))
        s_unit = Fraction(rng.choice([-1, 1]))
        for ell in S:
            s_unit *= Fraction(ell) ** rng.randint(-3, 3)
        rebuilt = Fraction(1)
        for ell in S:
            rebuilt *= Fraction(ell) ** valuation(s_unit, ell)
        ok["14.1"] &= abs(s_unit) == rebuilt and all(valuation(s_unit, p_) == 0 for p_ in PRIMES if p_ not in S)
        # (18.1): exact equalities on S = {2, 3, 5, ∞} and every valuation cannot see a unit change at 13
        alt = dict(diag)
        alt[13] = random_unit_at(rng, 13) * a
        ok["18.1"] &= (all(alt[v] == diag[v] for v in (2, 3, 5, "inf")) and split(alt)[0] == d
                      and not is_principal(alt))
        # (19.1): u_p = 1 outside S (hypothesis 2); the finite check on S and at ∞ decides principality.
        # As written, the theorem allows ε = −1; with u_p = 1 outside S that idele is not principal (7.1), so the
        # literal "if" fails at ε = −1 and the correct finite check is u_ℓ = 1 on S, u_∞ = 1. Both are recorded.
        S19 = (2, 3, 5)
        kind = trial % 4
        restricted = {p_: q0 for p_ in PRIMES}
        if kind == 0:                                                     # the diagonal image of q₀
            restricted["inf"] = q0
        elif kind == 1:                                                   # random units on S, a sign at ∞
            for ell in S19:
                restricted[ell] = random_unit_at(rng, ell) * q0
            restricted["inf"] = rng.choice([1, -1]) * q0
        elif kind == 2:                                                   # ε = −1 on S and at ∞, +1 outside: the literal counterexample
            for ell in S19:
                restricted[ell] = -q0
            restricted["inf"] = -q0
        else:                                                             # +1 on S, −1 at ∞
            restricted["inf"] = -q0
        _, _, u_r = split(restricted)
        literal = any(all(u_r[ell] == e_ for ell in S19) and u_r["inf"] == e_ for e_ in (1, -1))
        corrected = all(u_r[ell] == 1 for ell in S19) and u_r["inf"] == 1
        ok["19.1"] &= corrected == is_principal(restricted)
        if kind == 2:
            literal_19_1_counterexample = {"u_on_S": {ell: str(u_r[ell]) for ell in S19}, "u_inf": str(u_r["inf"]),
                                           "u_outside_S": {p_: str(u_r[p_]) for p_ in PRIMES if p_ not in S19},
                                           "literal_19_1_says_principal": literal, "principal": is_principal(restricted)}
            ok["19.1-literal-fails-at-minus-one"] &= literal and not is_principal(restricted)
        # (20.1)–(20.3): the ledger; a_∞ = −q₀ with u_p = +1 has 𝔫 = 1, 𝔲 = 1 and is not principal — the sign condition
        n_def = abs(diag["inf"]) / q0
        u_def_trivial = any(all(u[p_] == e_ for p_ in PRIMES) for e_ in (1, -1))
        ok["20.3"] &= n_def == 1 and u_def_trivial
        mixed = {p_: q0 for p_ in PRIMES}
        mixed["inf"] = -q0
        _, _, u_m = split(mixed)
        ok["20.3"] &= (abs(mixed["inf"]) / q0 == 1) and all(u_m[p_] == 1 for p_ in PRIMES) and not is_principal(mixed)
        # (23.1): compatible local lattices p^{d_p}Z_p reconstruct a₀ with v_p(a₀) = d_p at every p, zero outside
        dvec = {p_: (rng.randint(-2, 2) if rng.random() < 0.5 else 0) for p_ in PRIMES}
        a_lat = Fraction(1)
        for p_ in PRIMES:
            a_lat *= Fraction(p_) ** dvec[p_]
        ok["23.1"] &= all(valuation(a_lat, p_) == dvec[p_] for p_ in PRIMES) and all(
            valuation(a_lat, ell) == 0 for ell in (17, 19, 23, 29) if ell not in PRIMES)
    # §21: rational reconstruction — exhaustive uniqueness at 11³ for the largest M = N under the threshold,
    # the extended Euclid recovering each, and a collision at 11²
    mod3 = P ** 3
    Mmax = 1
    while RECONSTRUCTION_FACTOR * (Mmax + 1) ** 2 < mod3:
        Mmax += 1
    unique3, coll3 = exhaustive_uniqueness(mod3, Mmax, Mmax)
    recovered = all(rational_reconstruct(m_ * pow(n_, -1, mod3) % mod3, mod3, Mmax, Mmax) == Fraction(m_, n_)
                    for m_ in range(-Mmax, Mmax + 1) for n_ in range(1, Mmax + 1)
                    if n_ % P and math.gcd(abs(m_), n_) == 1)
    unique2, coll2 = exhaustive_uniqueness(P ** 2, Mmax, Mmax)
    # and at 11⁶ with M = N = 40, random fractions
    mod6, M6 = P ** 6, 40
    unique6 = mod6 > RECONSTRUCTION_FACTOR * M6 * M6
    for _ in range(TRIALS):
        m_, n_ = rng.randint(-M6, M6), rng.randint(1, M6)
        if n_ % P == 0:
            continue
        g = math.gcd(abs(m_), n_)
        m_, n_ = m_ // g, n_ // g
        unique6 &= rational_reconstruct(m_ * pow(n_, -1, mod6) % mod6, mod6, M6, M6) == Fraction(m_, n_)
    ok["21"] &= unique3 and recovered and (not unique2) and unique6
    real = [reconstruct_formal_parameter("[16]P", GENERATORS[0]), reconstruct_formal_parameter("[16]Q", GENERATORS[1])]
    ok["21"] &= all(r["agrees"] for r in real)
    return {"trials": TRIALS, "checks": ok,
            "reconstruction": {"modulus_11_3": mod3, "largest_M_equal_N_under_threshold": Mmax,
                               "exhaustively_unique_at_11_3": unique3, "collision_at_11_3": coll3,
                               "all_recovered_at_11_3": recovered, "unique_at_11_2": unique2, "collision_at_11_2": coll2,
                               "random_at_11_6_M_N_40": unique6},
            "theorem_19_1_literal_counterexample": literal_19_1_counterexample,
            "formal_parameters_of_16P_16Q": real, "agrees": all(ok.values())}


# ------------------------------------------------------------ labels

def labels() -> dict:
    out = {}
    t10 = DOCS["010"].read_text(encoding="utf-8")
    out["010"] = {"no_bsd_claim": "未主張 BSD 已證明" in t10, "not_proof_closure": "這不等於 BSD proof closure" in t10,
                  "no_go_list_N1_N6": all(f"### N{i}" in t10 for i in range(1, 7))}
    t11 = DOCS["011"].read_text(encoding="utf-8")
    i = t11.index("# 34. 本輪沒有證明")
    out["011"] = {"no_bsd_claim": "未主張 BSD 已證明" in t11, "unproved_list": True,
                  "bsd_last_unproved": "10. BSD。" in t11[i:t11.index("# 35.", i)]}
    t12 = DOCS["012"].read_text(encoding="utf-8")
    i = t12.index("# 37. Not proved")
    out["012"] = {"no_bsd_claim": "no claim that BSD is proved" in t12, "unproved_list": True,
                  "bsd_last_unproved": "10. BSD." in t12[i:t12.index("# 38.", i)]}
    return {"documents": out, "agrees": all(all(v.values()) for v in out.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    rng = random.Random(RANDOM_SEED)
    r10 = round_010()
    inst = r10["instance_24_1"]
    print(f"  Round 010: chain {r10['dag']['is_chain']}, arrows {r10['dag']['arrows']}, pure-T arrows {r10['dag']['pure_theorem_arrows']}; "
          f"matrix rows {r10['matrix']['rows']} typed {r10['matrix']['typing_consistent']}, T rows = T1..T6 {r10['matrix']['theorem_rows_are_T1_to_T6']}, "
          f"cuts {r10['matrix']['cuts_27_1']} partition {r10['matrix']['cuts_partition_T1_T6']}")
    print(f"  Round 010: closed invariants green here: {[k for k, v in r10['closed_invariants']['instantiated_here'].items() if v['green']]}; "
          f"not in folder: {list(r10['closed_invariants']['not_in_folder'])}")
    print(f"  Round 010 (24.1) on 389.a1: Omega {inst['omega']:.12f} x Reg {inst['regulator']} x q_fin {inst['q_fin']} = "
          f"{inst['omega_reg_qfin']:.13f} vs L''/2 {inst['L2_over_2']} (ratio {inst['ratio']:.15f})")
    r11 = round_011(rng)
    print(f"  Round 011: {r11['checks']} ({r11['zero_channel_trials']} zero-channel trials of {TRIALS})")
    r12 = round_012(rng)
    print(f"  Round 012: {r12['checks']}")
    print(f"  Round 012 reconstruction: {r12['reconstruction']}")
    for r in r12["formal_parameters_of_16P_16Q"]:
        print(f"  Round 012 {r['point']}: v11(z) = {r.get('v11_of_z')}, z mod 121 = {r.get('z_mod_121')}, digits {r.get('numerator_digits')}/{r.get('denominator_digits')}, "
              f"threshold k = {r.get('threshold_k')}, recovered {r.get('recovered_exactly')}, below threshold {r.get('below_threshold')}")
    lab = labels()
    ok = r10["agrees"] and r11["agrees"] and r12["agrees"] and lab["agrees"]
    out = {"gate": "src86", "round": "RUN-084", "round_010": r10, "round_011": r11, "round_012": r12, "labels": lab, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  labels: {lab['documents']}")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
