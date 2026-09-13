"""PC-002: the relative analytic regulator in F_11[t]/(t^121).

Accept pinned modular-symbol vectors; build all new measures from cusp paths.
No predecessor producer is imported or executed. The relation to mixed BF
regulators is conditional on the explicitly cited reciprocity conventions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
P = 11


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value,separators=(",",":"),sort_keys=True).encode()).hexdigest()


def p1(c: int, d: int, level: int) -> int:
    c, d = c % level, d % level
    if c:
        return d*pow(c,-1,level) % level
    if not d:
        raise ValueError("zero projective point")
    return level


def cusp(value: Fraction, vector: list[int], level: int) -> int:
    # Euclidean continued fractions; the column sign puts every edge in SL2(Z).
    numerator, denominator = value.numerator, value.denominator
    pm2,pm1,qm2,qm1 = 0,1,1,0
    previous = (1,0)
    answer = 0
    while denominator:
        a,rem = divmod(numerator,denominator)
        pn,qn = a*pm1+pm2,a*qm1+qm2
        det = previous[0]*qn-pn*previous[1]
        if det not in (-1,1):
            raise ArithmeticError("non-unimodular path edge")
        answer += vector[p1(qn,-det*previous[1],level)]
        previous = pn,qn
        pm2,pm1,qm2,qm1 = pm1,pn,qm1,qn
        numerator,denominator = denominator,rem
    return answer % P


def manin_checks(curve: dict) -> dict[str,bool]:
    level=curve["level"]
    result={}
    for name,sign in (("plus",1),("minus",-1)):
        v=curve[name]
        if len(v)!=level+1:
            raise ValueError("wrong vector length")
        checks=[]
        for i in range(level+1):
            c,d=(1,i) if i<level else (0,1)
            checks.extend(((v[i]+v[p1(d,-c,level)])%P == 0,
                           (v[i]+v[p1(d,-c-d,level)]+v[p1(-c-d,c,level)])%P == 0,
                           (v[i]-sign*v[p1(-c,d,level)])%P == 0))
        checks.append(v[curve["normalization"][name+"_index"]] == 1)
        result[name]=all(checks)
    a1,a2,a3,a4,a6=curve["ainvs"]
    points=1+sum((y*y+a1*x*y+a3*y-x**3-a2*x*x-a4*x-a6)%P == 0
                 for x in range(P) for y in range(P))
    result["a11"]=P+1-points == curve["a11"]
    result["ordinary"]=curve["a11"]%P != 0
    return result


def gamma_exponents(level: int) -> dict[int,int]:
    """Principal units modulo p^level, enumerated by the fixed generator 12."""
    modulus=P**level
    expected=P**(level-1)
    result={}
    value=1
    for exponent in range(expected):
        if value in result:
            raise ArithmeticError("cyclotomic generator order too small")
        result[value]=exponent
        value=value*(1+P)%modulus
    if value!=1:
        raise ArithmeticError("wrong cyclotomic generator order")
    return result


def exponent(a: int, level: int, lookup: dict[int,int]) -> int:
    modulus=P**level
    omega=pow(a,P**(level-1),modulus)
    if pow(omega,P-1,modulus)!=1 or omega%P!=a%P:
        raise ArithmeticError("bad Teichmuller lift")
    principal=a*pow(omega,-1,modulus)%modulus
    return lookup[principal]


def binomial_rows(width: int) -> list[list[int]]:
    return [[comb(e,j)%P if j<=e else 0 for j in range(width)] for e in range(width)]


def from_groups(groups: list[int]) -> list[int]:
    width=len(groups)
    rows=binomial_rows(width)
    return [sum(groups[e]*rows[e][j] for e in range(width))%P for j in range(width)]


def measure_layer(curve: dict, level: int, width: int, keep_terms: bool) -> dict:
    modulus=P**level
    if width>P**(level-1) or width not in (P,P*P):
        raise ValueError("unsupported or uncertified series width")
    lookup=gamma_exponents(level)
    alpha=curve["a11"]%P
    twist_alpha=(-alpha)%P  # chi_8(11) = -1
    ordinary_power=pow(alpha,-level,P)
    ordinary_previous=pow(alpha,-level-1,P)
    twisted_power=pow(twist_alpha,-level,P)
    twisted_previous=pow(twist_alpha,-level-1,P)
    groups_L=[0]*width
    groups_lambda=[0]*width
    terms=[]
    raw={}
    plus,minus,N=curve["plus"],curve["minus"],curve["level"]
    for a in range(1,modulus):
        if a%P==0:
            continue
        x=Fraction(a,modulus)
        prev=Fraction(a,modulus//P)
        plus_n=cusp(x,plus,N)
        plus_prev=cusp(prev,plus,N)
        minus_n=[cusp(x+Fraction(b,8),minus,N) for b in (1,3,5,7)]
        minus_prev=[cusp(prev+Fraction(b,8),minus,N) for b in (1,3,5,7)]
        sn=(minus_n[0]-minus_n[1]-minus_n[2]+minus_n[3])%P
        sp=(minus_prev[0]-minus_prev[1]-minus_prev[2]+minus_prev[3])%P
        mu=(ordinary_power*plus_n-ordinary_previous*plus_prev)%P
        twisted_mu=(twisted_power*sn-twisted_previous*sp)%P
        e=exponent(a,level,lookup)%width
        weighted=pow(a,-1,P)*twisted_mu%P
        groups_L[e]=(groups_L[e]+mu)%P
        groups_lambda[e]=(groups_lambda[e]+weighted)%P
        raw[a]=[mu,twisted_mu]
        # Every summand at the production layer, plus its individual cusp values.
        if keep_terms:
            terms.append([a,e,plus_n,plus_prev,minus_n,minus_prev,mu,twisted_mu,weighted])
    result={"level":level,"modulus":modulus,"certified_width":width,
            "units":len(raw),"L_group_coefficients":groups_L,
            "lambda_group_coefficients":groups_lambda,
            "L_coefficients":from_groups(groups_L),
            "lambda_coefficients":from_groups(groups_lambda),
            "raw_measure_sha256":digest(raw),"raw":raw}
    if keep_terms:
        result["summand_fields"]=["a","gamma_exponent","plus_at_a_modulus","plus_at_a_parent",
                                  "minus_cusps_at_a_modulus_b_1_3_5_7","minus_cusps_at_a_parent_b_1_3_5_7",
                                  "ordinary_measure","twisted_measure","x_inverse_weighted_twisted_measure"]
        result["summands"]=terms
    return result


def multiply(a: list[int], b: list[int]) -> list[int]:
    width=min(len(a),len(b))
    return [sum(a[j]*b[n-j] for j in range(n+1))%P for n in range(width)]


def divide(numerator: list[int], denominator: list[int]) -> list[int]:
    if denominator[0]%P==0:
        raise ZeroDivisionError("the calibrated denominator is not a unit")
    inverse=pow(denominator[0],-1,P)
    answer=[]
    for n,value in enumerate(numerator):
        answer.append((value-sum(denominator[j]*answer[n-j] for j in range(1,n+1)))*inverse%P)
    return answer


def distribution_check(coarse: dict, fine: dict) -> dict:
    modulus=coarse["modulus"]
    failures=[]
    for a,pair in coarse["raw"].items():
        sums=[sum(fine["raw"][a+modulus*b][i] for b in range(P))%P for i in (0,1)]
        if sums!=pair:
            failures.append(a)
    width=coarse["certified_width"]
    return {"coarse_level":coarse["level"],"fine_level":fine["level"],
            "measure_cells_compared":len(coarse["raw"]),
            "failed_cells":failures,
            "series_agree":all(coarse[key]==fine[key][:width] for key in ("L_coefficients","lambda_coefficients"))}


def public_layer(layer: dict) -> dict:
    return {key:value for key,value in layer.items() if key!="raw"}


def run(inputs: dict) -> dict:
    if inputs["p"]!=P or inputs["gamma"]!=12:
        raise ValueError("wrong prime/coordinate contract")
    width=P*P
    production={}
    checks={}
    first_layers={}
    for label in ("target","calibrator"):
        curve=inputs[label]
        structural=manin_checks(curve)
        if not all(structural.values()):
            raise ArithmeticError((label,structural))
        coarse=measure_layer(curve,2,P,False)
        main=measure_layer(curve,3,width,True)
        fine=measure_layer(curve,4,width,False)
        transitions=[distribution_check(coarse,main),distribution_check(main,fine)]
        if any(t["failed_cells"] or not t["series_agree"] for t in transitions):
            raise ArithmeticError((label,transitions))
        first_layers[label]=public_layer(coarse)
        production[label]=public_layer(main)
        checks[label]={"input_checks":structural,"refinement":transitions,
                       "verification_level4_measure_sha256":fine["raw_measure_sha256"]}
    target,cal=production["target"],production["calibrator"]
    numerator=multiply(target["L_coefficients"],target["lambda_coefficients"])
    denominator=multiply(cal["L_coefficients"],cal["lambda_coefficients"])
    quotient=divide(numerator,denominator)
    if multiply(quotient,denominator)!=numerator:
        raise ArithmeticError("quotient identity failed")
    old_check=target["L_coefficients"][:P]==inputs["target"]["expected_mod11_t11"]
    if not old_check:
        raise ArithmeticError("target series disagrees with the accepted earlier computation")
    # Falsifying witnesses operate on the named precision/coordinate contracts.
    coarse_width=P
    finer_exponent=P
    old_polynomial=[comb(0,j)%P if j==0 else 0 for j in range(P+1)]
    alias_polynomial=[comb(finer_exponent,j)%P for j in range(P+1)]
    precision_alias=(old_polynomial[:P]==alias_polynomial[:P] and old_polynomial[P]!=alias_polynomial[P])
    wrong_unweighted=from_groups([sum(row[7] for row in target["summands"] if row[1]==e)%P for e in range(width)])
    bad_input=json.loads(json.dumps(inputs["target"]))
    bad_input["minus"][0]=(bad_input["minus"][0]+1)%P
    negative_checks={
        "one_fewer_layer_cannot_certify_next_coefficient":precision_alias,
        "omitted_x_inverse_weight_changes_twisted_series":wrong_unweighted!=target["lambda_coefficients"],
        "modified_input_rejected_by_Manin_checks":not all(manin_checks(bad_input).values()),
    }
    try:
        divide(numerator,[0]+denominator[1:])
        negative_checks["zero_denominator_rejected"]=False
    except ZeroDivisionError:
        negative_checks["zero_denominator_rejected"]=True
    if not all(negative_checks.values()):
        raise ArithmeticError(negative_checks)
    valuation=next((i for i,c in enumerate(quotient) if c),None)
    return {"round":"PC-002","status":"PASS", "ring":"F_11[t]/(t^121)",
            "inputs_sha256":digest(inputs),"first_layers":first_layers,
            "production_layers":production,"checks":checks,
            "target_earlier_series_matched":old_check,
            "numerator_coefficients":numerator,"denominator_coefficients":denominator,
            "quotient_coefficients":quotient,"quotient_mod11_t_order":valuation,
            "quotient_leading_coefficient":quotient[valuation] if valuation is not None else None,
            "quotient_times_denominator_equals_numerator":True,
            "negative_checks":negative_checks,
            "claims":{"computed":"Analytic target germ in pinned modular-symbol periods",
                      "mu_in_these_periods":0 if valuation is not None else None,
                      "lambda_in_these_periods":valuation,
                      "actual_BF_regulator_measured":False,"BF_class_coordinates_computed":False,
                      "Coleman_weight_trace_jet_computed":False,"adjoint_period_ratio_computed":False,
                      "C_computed":False,"s11_computed":False,"BSD_proved":False}}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--inputs",type=Path,default=ROOT/"data"/"pc002-inputs.json")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=run(json.loads(args.inputs.read_text(encoding="utf-8")))
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
    summary={key:result[key] for key in ("round","status","ring","checks","quotient_mod11_t_order",
                                      "quotient_leading_coefficient","negative_checks","claims")}
    summary["first_eleven_coefficients"]={
        "target_L":result["production_layers"]["target"]["L_coefficients"][:P],
        "target_lambda":result["production_layers"]["target"]["lambda_coefficients"][:P],
        "calibrator_L":result["production_layers"]["calibrator"]["L_coefficients"][:P],
        "calibrator_lambda":result["production_layers"]["calibrator"]["lambda_coefficients"][:P],
        "quotient":result["quotient_coefficients"][:P]}
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
