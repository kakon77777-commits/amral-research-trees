#!/usr/bin/env python3
"""Attack 10: exact circular-unit calibration and first-order trace algebra.

Python standard library only. The trace data below are labelled algebra models,
NOT arithmetic Coleman-family traces. No old certificate producer is called.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb
from pathlib import Path

def require(ok, message):
    if not ok:
        raise ArithmeticError(message)

def qm(x, y):
    return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])

def qp(x, n):
    r = (1, 0)
    while n:
        if n & 1:
            r = qm(r, x)
        x = qm(x, x)
        n //= 2
    return r

def znorm(x):
    return x[0]**2-2*x[1]**2

def zadd(x, y):
    return tuple(a+b for a, b in zip(x, y))

def zneg(x):
    return tuple(-a for a in x)

def zmul(x, y):
    out = [0]*4
    for i in range(4):
        for j in range(4):
            k = i+j
            out[k % 4] += (-1 if k >= 4 else 1)*x[i]*y[j]
    return tuple(out)

def zpow(x, n):
    r = (1, 0, 0, 0)
    while n:
        if n & 1:
            r = zmul(r, x)
        x = zmul(x, x)
        n //= 2
    return r

def unit_identity():
    one, zeta = (1, 0, 0, 0), (0, 1, 0, 0)
    root2 = zadd(zeta, zneg(zpow(zeta, 3)))
    factors = {a: zadd(one, zneg(zpow(zeta, a))) for a in (1, 3, 5, 7)}
    numerator = zmul(factors[1], factors[7])
    denominator = zmul(factors[3], factors[5])
    unit = (3, -2, 0, 2)
    require(zmul(root2, root2) == (2, 0, 0, 0), "sqrt(2) embedding")
    require(numerator == zmul(unit, denominator), "circular-unit quotient")
    gauss = tuple(sum({1:1, 3:-1, 5:-1, 7:1}[a]*zpow(zeta, a)[i]
                      for a in (1, 3, 5, 7)) for i in range(4))
    require(gauss == tuple(2*x for x in root2), "Gauss normalization")
    eps, uchi, bottom = (1, 1), (3, -2), (17, -12)
    require(qm(uchi, qp(eps, 2)) == (1, 0), "u_chi=epsilon^-2")
    require(qp(uchi, 2) == bottom, "bottom norm factor")
    require(qm(bottom, qp(eps, 4)) == (1, 0), "bottom=epsilon^-4")
    require(znorm(uchi) == znorm(bottom) == 1, "norm-one torus point")
    return {
        "cyclotomic_ring": "Z[zeta]/(zeta^4+1)",
        "root2": root2, "gauss_sum": gauss,
        "numerator": numerator, "denominator": denominator,
        "unit_quotient": unit,
        "epsilon_in_Z_sqrt2": eps, "u_chi_in_Z_sqrt2": uchi,
        "bottom_unit_in_Z_sqrt2": bottom,
        "bottom_Kummer_multiple_of_epsilon": -4,
        "norms": {"epsilon": znorm(eps), "u_chi": 1, "bottom": 1},
        "exact_identities_passed": True
    }

def vp(n, p):
    require(n != 0, "valuation of zero not represented by this helper")
    n, v = abs(n), 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def rational_mod(x, modulus):
    x = F(x)
    require(__import__("math").gcd(x.denominator, modulus) == 1, "non-unit denominator")
    return x.numerator*pow(x.denominator, -1, modulus) % modulus

def digits(n, p, count):
    out = []
    for _ in range(count):
        out.append(n % p)
        n //= p
    return out

def local_log(p, precision):
    # bottom=epsilon^-4 has order 6 in the residue norm-one torus.
    bottom = (17, -12)
    power = qp(bottom, 6)
    w = (power[0]-1, power[1])
    require(all(x % p == 0 for x in w), "principal unit entry")
    modulus = p**precision
    max_term = 2*precision-1
    term, summation, rows = (1, 0), [0, 0], []
    for m in range(1, max_term+1):
        term = qm(term, w)
        loss = vp(m, p)
        divisor = p**loss
        require(all(x % divisor == 0 for x in term), "division precision")
        unit_inverse = pow(m//divisor, -1, modulus)
        sign = 1 if m % 2 else -1
        residues = [sign*(x//divisor)*unit_inverse % modulus for x in term]
        summation = [(a+b) % modulus for a, b in zip(summation, residues)]
        rows.append({"m": m, "valuation_lower_bound": m-loss,
                     "term_residues": residues})
    log_bottom = [x*pow(6, -1, modulus) % modulus for x in summation]
    require(log_bottom[0] == 0, "norm-one logarithm must be anti-invariant")
    L_bottom = log_bottom[1]
    L_eps = (-L_bottom*pow(4, -1, modulus)) % modulus
    require(L_eps % p == 0 and L_eps % (p*p) != 0, "epsilon log has exact valuation 1")
    smaller = p**(precision-1)
    normalized = L_eps//p
    lp = ((p+1)*normalized) % smaller
    q_eps = (-lp) % smaller
    q_bottom = (4*lp) % smaller
    require((p*q_bottom+(p+1)*L_bottom) % modulus == 0, "filtered Frobenius off-diagonal")
    require(q_bottom % p != 0, "calibration is a local unit")
    return {
        "p": p, "precision_exponent_for_L": precision,
        "modulus_for_L": modulus, "bottom_power_6": power,
        "principal_unit_minus_one": w,
        "series_terms": rows,
        "first_omitted_term": 2*precision,
        "tail_proof": "For m>=2N, v_p(w^m/m)>=m-v_p(m)>=m/2>=N (p=11).",
        "log_bottom_coefficients_mod_pN": log_bottom,
        "L_bottom_mod_pN": L_bottom, "L_epsilon_mod_pN": L_eps,
        "L_epsilon_exact_valuation": 1,
        "modulus_for_normalized_quantities": smaller,
        "L_epsilon_div_p_mod": normalized,
        "L_epsilon_div_p_digits_low_to_high": digits(normalized, p, precision-1),
        "Leopoldt_Lp_1_chi_mod": lp,
        "Leopoldt_Lp_digits_low_to_high": digits(lp, p, precision-1),
        "phi_offdiag_epsilon_mod": q_eps,
        "phi_offdiag_bottom_mod": q_bottom,
        "phi_offdiag_bottom_mod_p": q_bottom % p,
        "Leopoldt_Lp_mod_p": lp % p,
        "period_C_computed": False
    }

def bernoulli_check(p):
    n = 10
    B = [F(1)]
    for m in range(1, n+1):
        B.append(-sum(F(comb(m+1, k))*B[k] for k in range(m))/F(m+1))
    chi = {1: 1, 3: -1, 5: -1, 7: 1}
    Bchi = 8**(n-1)*sum(chi[a]*sum(F(comb(n, k))*B[k]*F(a, 8)**(n-k)
                                  for k in range(n+1)) for a in chi)
    raw = -Bchi/n
    interpolated = (1+p**(n-1))*raw
    return {
        "n": n, "B_n_chi": str(Bchi), "L_complex_1_minus_n": str(raw),
        "Euler_factor": 1+p**(n-1),
        "Lp_1_minus_n_mod_p": rational_mod(interpolated, p),
        "purpose": "Independent mod-11 sign/Gauss/Euler normalization check via integral KL measure."
    }

@dataclass(frozen=True)
class Dual:
    constant: F = F(0)
    linear: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "constant", F(self.constant))
        object.__setattr__(self, "linear", F(self.linear))

    def __add__(self, other):
        other = asdual(other)
        return Dual(self.constant+other.constant, self.linear+other.linear)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.constant, -self.linear)

    def __sub__(self, other):
        return self+-asdual(other)

    def __rsub__(self, other):
        return asdual(other)+-self

    def __mul__(self, other):
        other = asdual(other)
        return Dual(self.constant*other.constant,
                    self.constant*other.linear+self.linear*other.constant)

    __rmul__ = __mul__

    def inverse(self):
        require(self.constant != 0, "dual-number inverse")
        return Dual(1/self.constant, -self.linear/self.constant**2)

    def __truediv__(self, other):
        return self*asdual(other).inverse()

def asdual(x):
    return x if isinstance(x, Dual) else Dual(x)

def matrix(rows):
    return tuple(tuple(asdual(x) for x in row) for row in rows)

IDENTITY = matrix([[1,0],[0,1]])

def mm(a, b):
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(2)), Dual())
                       for j in range(2)) for i in range(2))

def mi(a):
    det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return ((a[1][1]/det, -a[0][1]/det), (-a[1][0]/det, a[0][0]/det))

def trace(a):
    return a[0][0]+a[1][1]

def encode_matrix(m):
    return [[[str(x.constant), str(x.linear)] for x in row] for row in m]

def trace_model(lower_a=5, lower_b=7):
    mats = {
        "a": matrix([[Dual(2,7), Dual(3,13)], [Dual(0,lower_a), Dual(1,11)]]),
        "b": matrix([[Dual(3,17), Dual(2,19)], [Dual(0,lower_b), Dual(1,23)]]),
        "j": matrix([[-1,0],[0,1]])
    }
    mats["A"], mats["B"] = mi(mats["a"]), mi(mats["b"])
    require(mm(mats["j"], mats["j"]) == IDENTITY, "involution")
    cache = {"": IDENTITY}
    def rho(word):
        if word not in cache:
            cache[word] = mm(rho(word[:-1]), mats[word[-1]])
        return cache[word]
    def T(word):
        return trace(rho(word))
    def diagonal_from_trace(word):
        return (T(word)-T("j"+word))/2
    def xi(word):
        return diagonal_from_trace(word).constant
    def A(word):
        return diagonal_from_trace(word).linear
    def Q(g, h):
        return A(g+h)-xi(g)*A(h)-xi(h)*A(g)
    def b0(word):
        return rho(word)[0][1].constant
    def beta(word):
        return rho(word)[1][0].linear/xi(word)
    def Fcochain(word):
        return A(word)/xi(word)
    alphabet = ("a","A","b","B","j")
    inverse = {"a":"A","A":"a","b":"B","B":"b","j":"j"}
    words = [""]+list(alphabet)
    words += [g+h for g in alphabet for h in alphabet if h != inverse[g]]
    rows = []
    for g in words:
        require(diagonal_from_trace(g) == rho(g)[0][0], "diagonal reconstruction")
        for h in words:
            q = Q(g,h)
            direct_product = b0(g)*rho(h)[1][0].linear
            require(q == direct_product, "rank-one trace tensor")
            require(b0(g+h) == b0(g)+xi(g)*b0(h), "upper cocycle")
            require(beta(g+h) == beta(g)+beta(h)/xi(g), "opposite cocycle")
            cup = b0(g)*beta(h)/xi(g)
            coboundary = Fcochain(h)-Fcochain(g+h)+Fcochain(g)
            require(cup == -coboundary, "cup nullhomotopy")
            rows.append({"g":g or "1", "h":h or "1", "Q":str(q),
                         "cup":str(cup), "minus_delta_F":str(-coboundary)})
    reconstructed = []
    for h in words:
        v_a, v_b = Q("a",h)/b0("a"), Q("b",h)/b0("b")
        require(v_a == v_b == rho(h)[1][0].linear, "calibrated row reconstruction")
        reconstructed.append({"word":h or "1", "v_from_a":str(v_a),
                              "v_from_b":str(v_b), "beta":str(beta(h)),
                              "A_over_xi":str(Fcochain(h))})
    # A change of diagonal frame preserves trace and scales the off-diagonals inversely.
    D = matrix([[2,0],[0,3]])
    for word in words:
        changed = mm(mm(mi(D),rho(word)),D)
        require(trace(changed) == T(word), "frame invariant trace")
        require(changed[0][1].constant == F(3,2)*b0(word), "upper frame weight")
        require(changed[1][0].linear == F(2,3)*rho(word)[1][0].linear, "lower frame weight")
    # X'=5X: tangent coefficient divides by 5.
    coordinate = {}
    for name, m in mats.items():
        coordinate[name] = tuple(tuple(Dual(x.constant,x.linear/5) for x in row) for row in m)
    for g in alphabet:
        for h in alphabet:
            old = mm(mats[g],mats[h])
            new = mm(coordinate[g],coordinate[h])
            require(all(new[i][k].constant == old[i][k].constant and
                        new[i][k].linear == old[i][k].linear/5
                        for i in range(2) for k in range(2)), "coordinate tensor weight")
    return {
        "data_kind": "EXACT ALGEBRA MODEL; not arithmetic Galois or Hecke trace data",
        "coefficient_ring": "Q[X]/(X^2)",
        "group": "Free(a,b) * C2(j)",
        "matrices": {name:encode_matrix(mats[name]) for name in ("a","b","j")},
        "word_count":len(words), "pair_count":len(rows),
        "trace_tensor_rows": rows, "opposite_reconstruction": reconstructed,
        "Q_a_a":str(Q("a","a")), "Q_a_b":str(Q("a","b")),
        "frame_and_coordinate_checks": True,
        "all_pair_identities_passed": True
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("attack10_result.json"))
    parser.add_argument("--precision", type=int, default=10, choices=range(3,31))
    args = parser.parse_args()
    input_path = Path(__file__).with_name("INPUTS.json")
    inputs = json.loads(input_path.read_text(encoding="utf-8"))
    require(inputs["p"] == 11, "this certificate is specialized to p=11")
    exact = unit_identity()
    local = local_log(11,args.precision)
    bern = bernoulli_check(11)
    require(local["Leopoldt_Lp_mod_p"] == bern["Lp_1_minus_n_mod_p"], "Leopoldt / Bernoulli normalization")
    model = trace_model()
    alternative = trace_model(lower_a=8,lower_b=9)
    require(model["Q_a_a"] != alternative["Q_a_a"], "same residual extension need not fix a tangent")
    result = {
        "schema":"bsd-attack10-unit-tangent-v1", "date":"2026-09-12",
        "input_sha256":hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "accepted_inputs_recomputed":False,
        "circular_unit":exact, "local_crystalline_calibration":local,
        "new_Bernoulli_normalization_check":bern,
        "first_order_trace_algebra":model,
        "alternative_algebra_model":{
            "warning":"Illustrates insufficient abstract input only; not a second arithmetic Coleman family.",
            "same_residual_matrices":True,
            "Q_a_a":alternative["Q_a_a"], "Q_a_b":alternative["Q_a_b"],
            "all_pair_identities_passed":alternative["all_pair_identities_passed"]},
        "status":{
            "exact_arithmetic_and_model_checks_passed":True,
            "new_written_proof":"Unit calibration; local filtered-phi description; conditional trace reconstruction and explicit cup nullhomotopy.",
            "actual_Coleman_trace_jets":None,
            "meromorphic_ES_order_n":None,
            "period_C":None,
            "Beilinson_Flach_B2_coordinates":None,
            "s11":None,
            "BSD_proved":False,
            "canonical_frontier_updated":False}
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "output":str(args.output),
        "bottom_unit":"17-12*sqrt(2)=epsilon^-4",
        "Leopoldt_Lp_mod_11":local["Leopoldt_Lp_mod_p"],
        "phi_offdiag_bottom_mod_11":local["phi_offdiag_bottom_mod_p"],
        "model_pairs":model["pair_count"],
        "actual_trace_jets_computed":False,
        "C_computed":False},ensure_ascii=False))

if __name__ == "__main__":
    main()

