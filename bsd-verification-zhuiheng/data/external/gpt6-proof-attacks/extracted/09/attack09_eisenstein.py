#!/usr/bin/env python3
"""New Eisenstein and twisted-moment calculations for BSD Attack 09.

Python 3.9+, standard library only. Reads the ACCEPTED mod-11 Hecke
eigenspace in INPUTS.json; never rebuilds the old Kurihara certificate.
No floating-point arithmetic and no claim to compute the Coleman family,
its leading period, a Beilinson-Flach cohomology class, or s11.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def chi8(n):
    return {1: 1, 3: -1, 5: -1, 7: 1}.get(n % 8, 0)


def eisenstein_coefficient(n):
    return sum(chi8(d)*d for d in range(1, n+1) if n % d == 0)


def critical_coefficient(n):
    return eisenstein_coefficient(n) - (eisenstein_coefficient(n//11) if n % 11 == 0 else 0)


def quad_mul(x, y):
    """Exact multiplication in Z[sqrt(2)]."""
    return x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def quad_pow(x, n):
    out = (1, 0)
    while n:
        if n & 1:
            out = quad_mul(out, x)
        x = quad_mul(x, x)
        n //= 2
    return out


def projective_index(c, d, level):
    c, d = c % level, d % level
    if c:
        return d*pow(c, -1, level) % level
    check(d != 0, "Invalid projective bottom row")
    return level


def minus_line(basis, level, p):
    """Take the negative involution eigenspace in an accepted 2D space."""
    check(len(basis) == level+1 and all(len(row) == 2 for row in basis),
          "Accepted basis must have 390 rows and two columns")
    rows = []
    for i in range(level+1):
        c, d = (1, i) if i < level else (0, 1)
        j = projective_index(-c, d, level)
        rows.append([(basis[i][k]+basis[j][k]) % p for k in range(2)])
    first_row = next((row for row in rows if any(row)), None)
    check(first_row is not None, "Minus constraints unexpectedly have rank zero")
    coeff = [first_row[1] % p, -first_row[0] % p]
    check(all(sum(a*b for a, b in zip(row, coeff)) % p == 0 for row in rows),
          "Minus constraint rank exceeds one")
    vector = [sum(a*b for a, b in zip(row, coeff)) % p for row in basis]
    first = next((i for i, value in enumerate(vector) if value), None)
    check(first is not None, "Minus kernel gave zero functional")
    scale = pow(vector[first], -1, p)
    coeff = [a*scale % p for a in coeff]
    vector = [a*scale % p for a in vector]
    for i in range(level+1):
        c, d = (1, i) if i < level else (0, 1)
        check((vector[i]+vector[projective_index(-c, d, level)]) % p == 0,
              "Negative involution identity failed")
    return vector, coeff, first


def cusp_value(a, b, vector, level, p):
    """Evaluate {infinity,a/b} by unimodular continued-fraction edges.

    The endpoint/row convention is inherited from the accepted input.
    Returns the path as well as its value, making the 40 new paths inspectable.
    """
    if b == 0:
        return 0, []
    if b < 0:
        a, b = -a, -b
    numerator_old, denominator_old = 0, 1
    numerator_previous, denominator_previous = 1, 0
    path = []
    while b:
        digit, remainder = divmod(a, b)
        numerator_next = digit*numerator_previous+numerator_old
        denominator_next = digit*denominator_previous+denominator_old
        determinant = numerator_next*denominator_previous-numerator_previous*denominator_next
        check(determinant in (-1, 1), "Non-unimodular continued-fraction edge")
        index = projective_index(determinant*denominator_next, denominator_previous, level)
        path.append(index)
        numerator_old, denominator_old = numerator_previous, denominator_previous
        numerator_previous, denominator_previous = numerator_next, denominator_next
        a, b = b, remainder
    return sum(vector[i] for i in path) % p, path


# Small sparse polynomial arithmetic over Q. Each monomial is a sorted
# tuple of formal variable names. This checks the NEW leading coefficients
# componentwise without pretending to know their arithmetic values.
def poly_const(c):
    c = Fraction(c)
    return {(): c} if c else {}


def poly_var(name):
    return {(name,): Fraction(1)}


def poly_add(a, b):
    out = dict(a)
    for monomial, value in b.items():
        out[monomial] = out.get(monomial, Fraction(0))+value
        if not out[monomial]:
            del out[monomial]
    return out


def poly_mul(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            monomial = tuple(sorted(m+n))
            out[monomial] = out.get(monomial, Fraction(0))+c*d
    return {m: c for m, c in out.items() if c}


def poly_scale(a, c):
    return poly_mul(a, poly_const(c))


def series_mul(a, b, precision):
    out = [{} for _ in range(precision)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i+j < precision:
                out[i+j] = poly_add(out[i+j], poly_mul(x, y))
    return out


def serial_poly(a):
    return [{"coefficient": str(c), "monomial": list(m)}
            for m, c in sorted(a.items())]


def leading_series_calculation():
    precision = 5
    C = poly_var("C")
    A0, A1, A2 = [poly_var(name) for name in ("A0", "A1", "A2")]
    k0, k1, k2 = [poly_var(name) for name in ("kappa0", "kappa1", "kappa2")]
    a2, a3 = [poly_var(name) for name in ("a2", "a3")]
    log_series = [{}]+[poly_const(Fraction((-1)**(n+1), n)) for n in range(1, precision)]
    z = [{}, k0, k1, k2]
    col_z = [{}, {}, a2, a3]
    factor = series_mul([C], [A0, A1, A2], precision)
    scaled_B = series_mul(factor, series_mul(log_series, z, precision), precision)
    scaled_col_B = series_mul(factor, series_mul(log_series, col_z, precision), precision)
    expected_B2 = poly_mul(poly_mul(C, A0), k0)
    expected_B3 = poly_mul(C, poly_add(poly_mul(A0, k1),
                              poly_mul(poly_add(A1, poly_scale(A0, Fraction(-1, 2))), k0)))
    expected_col_B3 = poly_mul(poly_mul(C, A0), a2)
    check(scaled_B[0] == scaled_B[1] == {}, "Unexpected lower class coefficient")
    check(scaled_B[2] == expected_B2 and scaled_B[3] == expected_B3,
          "Formal class leading coefficients failed")
    check(all(scaled_col_B[i] == {} for i in range(3)), "Unexpected lower regulator coefficient")
    check(scaled_col_B[3] == expected_col_B3, "Formal regulator leading coefficient failed")
    return {
        "normalization": "scaled_B=log_11(12)*B_hat=C*A(t)*log(1+t)*z(t)",
        "class_first_coefficient_degree": 2,
        "class_degree_2": serial_poly(scaled_B[2]),
        "class_degree_3": serial_poly(scaled_B[3]),
        "regulator_first_coefficient_degree": 3,
        "regulator_degree_3": serial_poly(scaled_col_B[3]),
        "arithmetic_C_A0_kappa_a2_computed": False
    }


def compute(inputs):
    p, level = inputs["p"], inputs["level"]
    check((p, level) == (11, 389), "This finite calculation is specialized to (389,11)")
    basis = inputs["accepted_manin_eigenspace"]["basis_mod_11"]
    vector, coeff, first = minus_line(basis, level, p)

    # NEW conductor 8 twist, not the old Kurihara sum.
    twisted_zero = sum(chi8(b)*cusp_value(b, 8, vector, level, p)[0]
                       for b in (1, 3, 5, 7)) % p
    alpha_twist = chi8(p)*inputs["ordinary_root_mod_p"] % p
    alpha_inverse = pow(alpha_twist, -1, p)
    terms = []
    for a in range(1, p):
        summands = []
        for b in (1, 3, 5, 7):
            numerator, denominator = 8*a+p*b, 8*p
            value, path = cusp_value(numerator, denominator, vector, level, p)
            summands.append({"b": b, "chi8_b": chi8(b), "numerator": numerator,
                             "denominator": denominator, "path_indices": path,
                             "minus_symbol": value})
        twisted_symbol = sum(item["chi8_b"]*item["minus_symbol"] for item in summands) % p
        measure = alpha_inverse*(twisted_symbol-alpha_inverse*twisted_zero) % p
        inverse_a = pow(a, -1, p)
        terms.append({"a": a, "summands": summands, "twisted_symbol": twisted_symbol,
                      "measure_on_residue": measure, "inverse_a": inverse_a,
                      "weighted_measure": inverse_a*measure % p})
    moment = sum(item["weighted_measure"] for item in terms) % p
    raw_sum = sum(item["inverse_a"]*item["twisted_symbol"] for item in terms) % p
    check(twisted_zero == 0, "An even twist of the minus symbol must vanish at zero")
    check(all((terms[a-1]["measure_on_residue"]+terms[p-a-1]["measure_on_residue"]) % p == 0
              for a in range(1, p)), "Twisted minus measure parity failed")
    check(moment != 0, "New shifted twisted p-adic L-value may vanish; stop the unit argument")

    # Exact auxiliary Eisenstein data.
    B2chi = sum(8*chi8(a)*(Fraction(a, 8)**2-Fraction(a, 8)+Fraction(1, 6))
                for a in range(1, 9))
    constant = -B2chi/4
    qcoeffs = [critical_coefficient(n) for n in range(1, 33)]
    up_residuals = [critical_coefficient(11*n)+11*critical_coefficient(n)
                    for n in range(1, 13)]
    check(B2chi == 2 and constant == Fraction(-1, 2), "Eisenstein constant term failed")
    check(not any(up_residuals), "Critical U11 refinement identity failed")
    check(chi8(-1) == 1 and chi8(11) == -1 and chi8(5) == -1, "Auxiliary character checks failed")

    # Nonzero local Kummer image of epsilon=1+sqrt(2).
    epsilon24 = quad_pow((1, 1), 24)
    mod121 = tuple(c % 121 for c in epsilon24)
    check(mod121[0] == 1 and mod121[1] % 11 == 0, "Principal-unit expansion failed")
    log_mod121 = ((mod121[0]-1)*pow(24, -1, 121) % 121,
                  mod121[1]*pow(24, -1, 121) % 121)
    check(log_mod121[0] == 0 and log_mod121[1] % 11 == 0, "Logarithm anti-invariant part failed")
    regulator_residue = log_mod121[1]//11 % 11
    check(regulator_residue != 0, "Auxiliary Kummer localization vanishes at this precision")
    check(pow(2, 5, 11) == 10, "The quadratic extension should be unramified and nonsplit at 11")

    smoothing = 25-chi8(5)
    adj_euler_residue = (1-pow(inputs["ordinary_root_mod_p"]**2 % p, -1, p)) % p
    check(smoothing % p != 0 and adj_euler_residue != 0, "A proposed invertible factor vanished")
    # A0=C5(0)*lambda8(0)/D_E. This normalized product is computable
    # without knowing the adjoint period D_E.
    A0_times_D_mod11 = smoothing*moment % p

    return {
        "task": "BSD Proof Attack 09: a usable Eisenstein degeneration",
        "prior_certificates_replayed": False,
        "eisenstein": {
            "form": "E_2(1,chi_8)", "tame_level": 8,
            "chi8_11": chi8(11), "chi8_5": chi8(5), "B2_chi8": str(B2chi),
            "constant_term": str(constant), "critical_U11": -11,
            "critical_q_coefficients_n_1_to_32": qcoeffs,
            "U11_residuals_n_1_to_12": up_residuals,
            "p_decent_arithmetic_conditions": True,
            "noncriticality_basis": "Nonzero localization of the chi8 Kummer unit; literature theorem required."
        },
        "unit_anchor": {
            "epsilon": "1+sqrt(2)", "norm": -1, "epsilon_power": 24,
            "epsilon_power_exact": list(epsilon24),
            "epsilon_power_mod_121": list(mod121),
            "log_epsilon_mod_121": list(log_mod121),
            "log_epsilon_over_11_sqrt2_mod_11": regulator_residue,
            "scope": "Uses log(epsilon)=log(epsilon^24)/24 and a proved valuation bound for the discarded log terms.",
            "is_the_unknown_Eichler_Shimura_period": False
        },
        "new_minus_line": {
            "dimension": 1, "coefficients_in_accepted_2D_basis": coeff,
            "normalization_index": first, "normalization_value": 1,
            "vector_mod_11": vector,
            "old_Hecke_eigenspace_accepted_without_replay": True
        },
        "shifted_twisted_moment": {
            "character": "x -> x^(-1), including the odd Teichmuller component",
            "period_convention": "Phi_chi(r)=sum_b chi8(b)*Phi_E^-(r+b/8); Omega_chi=Omega_minus/G(chi8).",
            "alpha_twist_mod11": alpha_twist, "twisted_symbol_at_zero": twisted_zero,
            "new_cusp_path_count": 40, "residue_terms": terms,
            "weighted_unstabilized_sum_mod11": raw_sum,
            "lambda8_at_zero_mod11": moment,
            "nonzero": moment != 0,
            "scope": "An integral ordinary measure moment at a noncritical character; not the central complex L-value."
        },
        "invertible_factors": {
            "C5_at_zero": smoothing, "C5_at_zero_mod11": smoothing % p,
            "adjoint_Euler_factor_mod11": adj_euler_residue,
            "A0_times_D_E_mod11": A0_times_D_mod11,
            "D_E_value": None, "A0_value": None,
            "formal_t_order_A": 0,
            "D_E_nonzero_reason": "Adjoint interpolation: nonzero Petersson ratio and nonzero Euler factors."
        },
        "formal_leading_calculation": leading_series_calculation(),
        "period_and_parameter_bookkeeping": {
            "Eisenstein_uniformizer": "X, distinct from cyclotomic t=gamma-1 and Fontaine t_dR",
            "period_order_n": None, "leading_period_C": None,
            "change_X_to_vX": "Both leading period and leading class coordinates multiply by v(0)^(-n).",
            "common_frame_change": "Both line coordinates change by the same unit; their tensor quotient is unchanged.",
            "rationality_consequence": "None without a rational realization comparison."
        },
        "derived_comparison": {
            "definition": "B2=[t^2] B_hat after the Eisenstein leading-term operation",
            "formula": "kappa_dagger=log_11(12)*D_E/(26*C*lambda8(0))*B2",
            "s11_formula": "s11=log_11(12)*D_E/(416*C*lambda8(0))*h(x,B2)/(det(H)*ell(x))",
            "basis": "Loeffler-Rivero C1.13 plus accepted Attack 06 inputs, compatible periods and the NEW nonzero moment.",
            "actual_B2_computed": False
        },
        "open": {
            "C_value": None, "n_value": None, "B2_coordinates": None, "s11": None,
            "comparison_with_Attack07_relative_cycle": "not constructed",
            "rational_determinant_descent": "not proved",
            "archimedean_leading_term_comparison": "not proved",
            "BSD_proved": False, "canonical_frontier_updated": False
        }
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).with_name("INPUTS.json"))
    parser.add_argument("--output", type=Path, default=Path("attack09_result_local.json"))
    args = parser.parse_args()
    raw = args.inputs.read_bytes()
    inputs = json.loads(raw.decode("utf-8"))
    result = compute(inputs)
    result["inputs_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "lambda8_at_zero_mod11": result["shifted_twisted_moment"]["lambda8_at_zero_mod11"],
        "unit_log_normalized_mod11": result["unit_anchor"]["log_epsilon_over_11_sqrt2_mod_11"],
        "C5_at_zero": result["invertible_factors"]["C5_at_zero"],
        "class_t_order": 2, "regulator_t_order": 3,
        "C_computed": False, "s11_computed": False, "output": str(args.output)
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
