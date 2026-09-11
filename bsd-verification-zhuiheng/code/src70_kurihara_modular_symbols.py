"""Gate 70 — the RUGZPB P4 certificate's proof-critical computation, done a third time from scratch: mod-11 modular symbols for Γ₀(389), the 389.a1 plus-eigenline, and the Kurihara number δ_{397·991}.

數學戰士「墜衡」 / AMRAL Research Lab.

`BSD_RUGZPB_P2_P4_389a1_p11_v0.2` rests its theorem — Ш(389.a1/ℚ)[11^∞] = 0,
via Kim's Theorem 1.8 — on one exact finite computation: the mod-11 Kurihara
number at n = 397·991 is nonzero. The document reports δ = 6 in a
"deterministic normalization" it does not disclose. The Witness line's
stress-test package (`stress-test/files/kurihara`) rebuilt the computation
with a disclosed normalization, λ(1,5) = 1 in the ordering (1,0), (1,1), …,
(1,388), (0,1), and found δ = 5, recording the manuscript's 6 as literally
unreproduced.

This gate is a third implementation, this line's own, sharing no code with
either: Manin symbols on P¹(F₃₈₉) with the S and R relations, Hecke operators
by Merel's determinant-q matrices (a > b ≥ 0, d > c ≥ 0) acting on the
bottom row, the plus condition λ(c,d) = λ(−c,d), a sparse elimination over
F₁₁ in three stages (relations → 65, Hecke at 2, 3, 5 → 2, plus → 1), the
eigenvalues at 7, 13, 17, 19 as a check the operators are right, and the
path {∞, a/n} by continued fractions. Every a_q is point-counted here.

Beyond δ it computes the whole of θ̄_n modulo I³ — the constant, X, Y, X²,
Y² and XY coefficients — which is the object P5 v1.1 §1 writes as
6·X₃₉₇X₉₉₁: ord_I(θ̄_n) = 2 is the vanishing of the first three, and the
X² and Y² coefficients vanishing is what the norm relations predict. The
rank-1 Kurihara numbers at 397 and 991 alone are computed too; Kim's theorem
says they vanish when the Selmer corank is 2.

Usage:  python code/src70_kurihara_modular_symbols.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "p5" / "files"
DOC = "BSD_RUGZPB_P2_P4_389a1_p11_v0.2.md"
OUT = LOGS / "src70-kurihara-modular-symbols.json"

AINVS = [0, 1, 1, -2, 0]                  # 389.a1
N = 389
P = 11
ELLS = (397, 991)
ROOTS = {397: 5, 991: 6}
HECKE_ISOLATE = (2, 3, 5)
HECKE_CHECK = (7, 13, 17, 19)
NORMALISE_AT = 5                          # λ(1,5) = 1 — the stress-test package's disclosed scale
PLUS_SIGN = 1                             # λ(c,d) = PLUS_SIGN · λ(−c,d): +1 is the real-part functional; −1 would be Stein's star
STATED = {"dimension_after_relations": 65, "dimension_after_hecke": 2, "dimension_after_plus": 1,
          "relation_rank": 325, "eigenvalues_check": (-5, -3, -6, 5),
          "delta_manuscript": 6, "delta_stress_test_at_lambda_1_5": 5,
          "stress_test_raw_product_sum": 43605160}
BLOCKS = 40


# ------------------------------------------------------------ the curve

def count_points_general(a: list[int], q: int) -> int:
    a1, a2, a3, a4, a6 = (c % q for c in a)
    n = 1
    for x in range(q):
        rhs = (x ** 3 + a2 * x * x + a4 * x + a6) % q
        for y in range(q):
            if (y * y + a1 * x * y + a3 * y - rhs) % q == 0:
                n += 1
    return n


def a_q(q: int) -> int:
    return q + 1 - count_points_general(AINVS, q)


# ------------------------------------------------------------ P¹(F_N)

def inv_mod(x: int, m: int) -> int:
    return pow(x % m, m - 2, m)


def p1_index(c: int, d: int) -> int:
    """(c : d) ↦ d·c⁻¹ if c ≢ 0, else N. Generators are (1,t), t < N, and (0,1)."""
    c %= N
    d %= N
    if c:
        return d * inv_mod(c, N) % N
    if d == 0:
        raise ValueError("(0:0) is not a point of P¹")
    return N


def rep(i: int) -> tuple[int, int]:
    return (1, i) if i < N else (0, 1)


# ------------------------------------------------------------ relations and Hecke

def relation_rows() -> list[dict[int, int]]:
    rows = []
    for i in range(N + 1):
        c, d = rep(i)
        s: dict[int, int] = {}
        for j in (i, p1_index(d, -c)):
            s[j] = s.get(j, 0) + 1
        rows.append(s)
        r: dict[int, int] = {}
        for j in (i, p1_index(d, -c - d), p1_index(-c - d, c)):
            r[j] = r.get(j, 0) + 1
        rows.append(r)
    return rows


def merel_matrices(q: int) -> list[tuple[int, int, int, int]]:
    """[[a,b],[c,d]] with ad − bc = q, a > b ≥ 0, d > c ≥ 0 (Merel, 1994)."""
    out = []
    for a in range(1, q + 1):
        for b in range(0, a):
            for c in range(0, q + 1):
                num = q + b * c
                if num % a:
                    continue
                d = num // a
                if d > c:
                    out.append((a, b, c, d))
    return out


def hecke_rows(q: int) -> list[dict[int, int]]:
    """Row i holds T_q m_i in the generators: Σ_h m((c,d)·h), h over Merel's set."""
    ms = merel_matrices(q)
    rows = []
    for i in range(N + 1):
        c, d = rep(i)
        r: dict[int, int] = {}
        for a, b, cc, dd in ms:
            j = p1_index(c * a + d * cc, c * b + d * dd)
            r[j] = r.get(j, 0) + 1
        rows.append(r)
    return rows


def iota_index(i: int) -> int:
    c, d = rep(i)
    return p1_index(-c, d)


# ------------------------------------------------------------ sparse linear algebra over F_P

def rref_sparse(rows: list[dict[int, int]]) -> dict[int, dict[int, int]]:
    """Reduced row echelon form; returns {pivot column: row} with each row normalised."""
    pivots: dict[int, dict[int, int]] = {}
    for row in rows:
        r = {c: v % P for c, v in row.items() if v % P}
        while r:
            hit = [c for c in r if c in pivots]
            if not hit:
                break
            c = hit[0]
            f = r[c]
            for cc, vv in pivots[c].items():
                nv = (r.get(cc, 0) - f * vv) % P
                if nv:
                    r[cc] = nv
                else:
                    r.pop(cc, None)
        if not r:
            continue
        c = min(r)
        inv = inv_mod(r[c], P)
        r = {cc: vv * inv % P for cc, vv in r.items()}
        # keep the form reduced: clear column c from every existing pivot row
        for pc, pr in pivots.items():
            if c in pr:
                f = pr[c]
                for cc, vv in r.items():
                    nv = (pr.get(cc, 0) - f * vv) % P
                    if nv:
                        pr[cc] = nv
                    else:
                        pr.pop(cc, None)
        pivots[c] = r
    return pivots


def nullspace(rows: list[dict[int, int]], ncols: int) -> list[list[int]]:
    piv = rref_sparse(rows)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [0] * ncols
        v[f] = 1
        for pc, pr in piv.items():
            if f in pr:
                v[pc] = (-pr[f]) % P
        basis.append(v)
    return basis


def apply_rows(rows: list[dict[int, int]], v: list[int]) -> list[int]:
    return [sum(coef * v[j] for j, coef in r.items()) % P for r in rows]


# ------------------------------------------------------------ the eigenline

def genus_x0_prime(N: int) -> int:
    """g(X₀(N)) for prime N: 1 + (N+1)/12 − ε₂/4 − ε₃/3 − 1, with ε₂ = 1 + (−1|N), ε₃ = 1 + (−3|N)."""
    e2 = 1 + (1 if N % 4 == 1 else -1)
    e3 = 1 + (1 if N % 3 == 1 else -1)
    twelve_g = 12 + (N + 1) - 3 * e2 - 4 * e3 - 12
    assert twelve_g % 12 == 0
    return twelve_g // 12


def eigenline() -> dict:
    t0 = time.time()
    rel = relation_rows()
    K = nullspace(rel, N + 1)                       # basis of the Manin quotient's dual: λ with λ(rel) = 0
    dim_rel = len(K)
    aq = {q: a_q(q) for q in HECKE_ISOLATE + HECKE_CHECK}
    # Hecke constraints, restricted to span(K): (H_q − a_q I) K μ = 0
    cons: list[dict[int, int]] = []
    for q in HECKE_ISOLATE:
        H = hecke_rows(q)
        images = [apply_rows(H, k) for k in K]        # H k for each basis vector k
        for i in range(N + 1):
            row = {}
            for b, (k, hk) in enumerate(zip(K, images)):
                val = (hk[i] - aq[q] * k[i]) % P
                if val:
                    row[b] = val
            if row:
                cons.append(row)
    M = nullspace(cons, dim_rel)                    # coordinates μ in the K-basis
    hecke_vectors = [[sum(m[b] * K[b][i] for b in range(dim_rel)) % P for i in range(N + 1)] for m in M]
    dim_hecke = len(hecke_vectors)
    # plus: λ_i = λ_{ι(i)}
    plus_cons: list[dict[int, int]] = []
    for i in range(N + 1):
        j = iota_index(i)
        if j == i:
            continue
        row = {}
        for b, v in enumerate(hecke_vectors):
            val = (v[i] - PLUS_SIGN * v[j]) % P
            if val:
                row[b] = val
        if row:
            plus_cons.append(row)
    Pl = nullspace(plus_cons, dim_hecke)
    plus_vectors = [[sum(m[b] * hecke_vectors[b][i] for b in range(dim_hecke)) % P for i in range(N + 1)] for m in Pl]
    dim_plus = len(plus_vectors)
    lam = plus_vectors[0] if dim_plus == 1 else None
    first_nonzero = next((i for i, v in enumerate(lam) if v), None) if lam else None
    if lam is not None and first_nonzero is not None:
        s = inv_mod(lam[first_nonzero], P)
        lam = [v * s % P for v in lam]
    # the check the operators are right: eigenvalues at four more primes
    evs = {}
    if lam is not None:
        for q in HECKE_CHECK:
            H = hecke_rows(q)
            hl = apply_rows(H, lam)
            ratio = None
            for i in range(N + 1):
                if lam[i]:
                    ratio = hl[i] * inv_mod(lam[i], P) % P
                    break
            evs[q] = {"a_q_point_counted": aq[q], "a_q_mod_11": aq[q] % P,
                      "eigenvalue_of_lambda": ratio,
                      "is_eigenvector": all((hl[i] - aq[q] * lam[i]) % P == 0 for i in range(N + 1)),
                      "agrees": ratio == aq[q] % P}
    g = genus_x0_prime(N)
    return {"seconds": round(time.time() - t0, 2),
            "generators": N + 1, "relation_rows": len(rel),
            "dimension_after_relations": dim_rel, "relation_rank": (N + 1) - dim_rel,
            "genus_of_X0_389": g, "two_g_plus_cusps_minus_1": 2 * g + 1,
            "dimension_equals_2g_plus_1": dim_rel == 2 * g + 1,
            "a_q_point_counted": {str(q): aq[q] for q in aq},
            "hecke_isolation_primes": list(HECKE_ISOLATE),
            "dimension_after_hecke": dim_hecke, "dimension_after_plus": dim_plus,
            "first_nonzero_index": first_nonzero, "normalised_at": NORMALISE_AT,
            "lambda": lam, "eigenvalue_checks": {str(q): v for q, v in evs.items()},
            "merel_set_sizes": {str(q): len(merel_matrices(q)) for q in HECKE_ISOLATE + HECKE_CHECK},
            "agrees": (dim_rel == STATED["dimension_after_relations"] and dim_rel == 2 * g + 1
                       and dim_hecke == STATED["dimension_after_hecke"]
                       and dim_plus == STATED["dimension_after_plus"]
                       and first_nonzero == NORMALISE_AT
                       and all(v["agrees"] and v["is_eigenvector"] for v in evs.values())
                       and tuple(aq[q] for q in HECKE_CHECK) == STATED["eigenvalues_check"])}


# ------------------------------------------------------------ paths and the sum

def path_indices(a: int, n: int) -> list[int]:
    """{∞, a/n} as Manin-symbol generator indices: m(q_i, (−1)^{i−1} q_{i−1}) over the convergents."""
    out = [p1_index(1, 0)]                          # {∞, a_0} = {∞, 0} = m(1, 0)
    num, den = a, n
    a0 = num // den
    num -= a0 * den
    p_prev2, q_prev2 = 1, 0
    p_prev, q_prev = a0, 1
    i = 1
    while num:
        k, r = divmod(den, num)
        p_new, q_new = k * p_prev + p_prev2, k * q_prev + q_prev2
        out.append(p1_index(q_new, (1 if (i - 1) % 2 == 0 else -1) * q_prev))
        p_prev2, q_prev2, p_prev, q_prev = p_prev, q_prev, p_new, q_new
        den, num = num, r
        i += 1
    if (p_prev, q_prev) != (a // math.gcd(a, n), n // math.gcd(a, n)):
        raise ValueError("continued fraction did not return to a/n")
    return out


def log_table(ell: int, g: int) -> list[int]:
    """log_g(x) mod (ell − 1) for x = 1..ell−1, reduced mod P. Refuses a non-primitive g."""
    tab = [-1] * ell
    x = 1
    for k in range(ell - 1):
        if tab[x] != -1:
            raise ValueError(f"{g} is not a primitive root mod {ell}: orbit closes at {k}")
        tab[x] = k % P
        x = x * g % ell
    if x != 1 or any(v == -1 for v in tab[1:]):
        raise ValueError(f"{g} is not a primitive root mod {ell}")
    return tab


def kurihara_sum(lam: list[int], blocks: int = BLOCKS, block_ids=None) -> dict:
    n = ELLS[0] * ELLS[1]
    logs = {ell: log_table(ell, ROOTS[ell]) for ell in ELLS}
    lo, hi = logs[ELLS[0]], logs[ELLS[1]]
    size = (n + blocks - 1) // blocks
    per_block = []
    tot = {"const": 0, "X": 0, "Y": 0, "X2": 0, "Y2": 0, "XY": 0}
    raw = 0
    terms = 0
    for b in range(blocks):
        if block_ids is not None and b not in block_ids:
            continue
        s = {"const": 0, "X": 0, "Y": 0, "X2": 0, "Y2": 0, "XY": 0}
        braw = 0
        bterms = 0
        for a in range(max(1, b * size), min(n, (b + 1) * size)):
            if a % ELLS[0] == 0 or a % ELLS[1] == 0:
                continue
            v = sum(lam[i] for i in path_indices(a, n)) % P
            bterms += 1
            if not v:
                continue
            i, j = lo[a % ELLS[0]], hi[a % ELLS[1]]
            s["const"] += v
            s["X"] += v * i
            s["Y"] += v * j
            s["X2"] += v * (i * (i - 1) // 2)
            s["Y2"] += v * (j * (j - 1) // 2)
            s["XY"] += v * i * j
            braw += v * i * j
        per_block.append({"block": b, "terms": bterms, "raw_product_sum": braw,
                          "mod_11": {k: val % P for k, val in s.items()}})
        for k in s:
            tot[k] += s[k]
        raw += braw
        terms += bterms
    return {"n": n, "blocks": blocks, "terms": terms, "phi_n": (ELLS[0] - 1) * (ELLS[1] - 1),
            "primitive_roots_verified": {str(e): ROOTS[e] for e in ELLS},
            "theta_bar_mod_I3": {k: v % P for k, v in tot.items()},
            "delta_n_XY_coefficient": tot["XY"] % P,
            "raw_product_sum": raw, "per_block": per_block}


def rank_one_sums(lam: list[int]) -> dict:
    out = {}
    for ell in ELLS:
        tab = log_table(ell, ROOTS[ell])
        s = 0
        for a in range(1, ell):
            v = sum(lam[i] for i in path_indices(a, ell)) % P
            s += v * tab[a]
        out[str(ell)] = s % P
    return out


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    doc = (DOCS / DOC).exists()
    e = eigenline()
    print(f"  eigenline: {e['dimension_after_relations']} → {e['dimension_after_hecke']} → "
          f"{e['dimension_after_plus']} in {e['seconds']}s; first nonzero at {e['first_nonzero_index']}; "
          f"a_q {e['a_q_point_counted']}; checks "
          f"{ {q: v['agrees'] for q, v in e['eigenvalue_checks'].items()} }")
    if e["lambda"] is None:
        print("  no eigenline; stopping")
        return 1
    t0 = time.time()
    k = kurihara_sum(e["lambda"])
    r1 = rank_one_sums(e["lambda"])
    secs = round(time.time() - t0, 1)
    th = k["theta_bar_mod_I3"]
    delta = k["delta_n_XY_coefficient"]
    ok = (doc and e["agrees"] and delta != 0
          and th["const"] == 0 and th["X"] == 0 and th["Y"] == 0 and th["X2"] == 0 and th["Y2"] == 0
          and k["terms"] == k["phi_n"]
          and delta == STATED["delta_stress_test_at_lambda_1_5"]
          and k["raw_product_sum"] == STATED["stress_test_raw_product_sum"]
          and all(v == 0 for v in r1.values()))
    log = {"gate": "src70 — Kurihara number of 389.a1 at 397·991 mod 11, from modular symbols built here",
           "source": DOC, "document_found": doc,
           "conventions": {"manin_symbol": "m(c,d) = g{0,∞}, g ∈ SL₂(ℤ) with bottom row ≡ (c,d) mod 389",
                           "generators": "(1,0), (1,1), …, (1,388), (0,1); index t for (1,t), 389 for (0,1)",
                           "relations": "m(c,d) + m(d,−c) = 0; m(c,d) + m(d,−c−d) + m(−c−d,c) = 0",
                           "hecke": "Merel matrices ad − bc = q, a > b ≥ 0, d > c ≥ 0, acting on the bottom row",
                           "plus": "λ(c,d) = λ(−c,d) — the real-part functional; not Stein's star",
                           "path": "{∞, a/n} = Σ m(q_i, (−1)^{i−1} q_{i−1}) over the convergents of a/n",
                           "logs": "primitive roots 5 mod 397 and 6 mod 991, logs reduced mod 11",
                           "scale": "λ(1,5) = 1 — the first nonzero coordinate in the ordering"},
           "eigenline": {k_: v for k_, v in e.items() if k_ != "lambda"},
           "lambda_nonzero_coordinates": sum(1 for v in e["lambda"] if v),
           "lambda_first_twelve": e["lambda"][:12],
           "lambda": e["lambda"],
           "kurihara": {k_: v for k_, v in k.items() if k_ != "per_block"},
           "kurihara_blocks": k["per_block"],
           "rank_one_kurihara_numbers": r1,
           "seconds_for_the_sum": secs,
           "stated": STATED,
           "reading": ("δ_n^(λ) = 5 ≠ 0 under the disclosed scale λ(1,5) = 1 — the stress-test package's "
                       "figure, reached here by a third implementation with the same integer raw sum; the "
                       "manuscript's 6 is a different, undisclosed scale, and stays literally unreproduced. "
                       "θ̄_n ≡ 5·X₃₉₇X₉₉₁ (mod I³): the constant, X, Y, X² and Y² coefficients all vanish, "
                       "so ord_I(θ̄_n) = 2 exactly as P5 v1.1 §1 states, and the rank-1 Kurihara numbers at "
                       "397 and 991 are 0, as Kim's theorem requires when the Selmer corank is 2"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  θ̄_n mod I³: {th}; δ = {delta}; raw product sum {k['raw_product_sum']:,} "
          f"(stress-test {STATED['stress_test_raw_product_sum']:,}); terms {k['terms']:,} = φ(n) {k['phi_n']:,}; "
          f"rank-1 numbers {r1}; {secs}s")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
