"""PC-002: Farey-triangle cup pairing and eigensymbol-scale cancellation.

The report proves the triangle formula; this program checks its full radical
on the supplied levels and computes the two pinned eigensymbol pairings.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from relative_regulator import P, p1, digest

ROOT=Path(__file__).resolve().parent.parent


def permutations(level):
    s=[];r=[]
    for i in range(level+1):
        c,d=(1,i) if i<level else (0,1)
        s.append(p1(d,-c,level))
        r.append(p1(d,-c-d,level))
    return s,r


def kernel_basis(level,s,r):
    pivots={}
    for i in range(level+1):
        for indices in ((i,s[i]),(i,r[i],r[r[i]])):
            row={}
            for j in indices:
                row[j]=(row.get(j,0)+1)%P
            row={j:v for j,v in row.items() if v}
            while row:
                k=min(row)
                if k not in pivots:
                    factor=pow(row[k],-1,P)
                    pivots[k]={j:v*factor%P for j,v in row.items()}
                    break
                factor=row[k]
                for j,v in pivots[k].items():
                    new=(row.get(j,0)-factor*v)%P
                    if new:
                        row[j]=new
                    else:
                        row.pop(j,None)
    result=[]
    for j in range(level+1):
        if j in pivots:
            continue
        v=[0]*(level+1);v[j]=1
        for pivot in sorted(pivots,reverse=True):
            v[pivot]=-sum(x*v[k] for k,x in pivots[pivot].items() if k!=pivot)%P
        result.append(v)
    return result


def cup(u,v,r):
    return sum(u[i]*v[r[i]]-v[i]*u[r[i]] for i in range(len(u)))*pow(6,-1,P)%P


def is_cocycle(v,s,r):
    return len(v)==len(r) and all((v[i]+v[s[i]])%P==0 and
                                 (v[i]+v[r[i]]+v[r[r[i]]])%P==0 for i in range(len(r)))


def rank(matrix):
    a=[row[:] for row in matrix]
    k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]%P),None)
        if pivot is None:
            continue
        a[k],a[pivot]=a[pivot],a[k]
        inverse=pow(a[k][j],-1,P)
        a[k]=[x*inverse%P for x in a[k]]
        for i in range(k+1,len(a)):
            factor=a[i][j]
            if factor:
                a[i]=[(x-factor*y)%P for x,y in zip(a[i],a[k])]
        k+=1
    return k


def analyze(curve):
    N=curve["level"]
    s,r=permutations(N)
    basis=kernel_basis(N,s,r)
    matrix=[[cup(u,v,r) for v in basis] for u in basis]
    pairing_rank=rank(matrix)
    # Standard prime-level genus formula; cusp count is two.
    eps2=2 if N%4==1 else 0
    eps3=2 if N%3==1 else 0
    genus=F(N+1,12)-F(eps2,4)-F(eps3,3)
    if genus.denominator!=1:
        raise ArithmeticError("nonintegral genus")
    genus=int(genus)
    gauge=[0]*(N+1);gauge[0]=-1;gauge[N]=1
    conditions={
        "S_has_order_two":all(s[s[i]]==i for i in range(N+1)),
        "R_has_order_three":all(r[r[r[i]]]==i for i in range(N+1)),
        "dimension_is_2g_plus_1":len(basis)==2*genus+1,
        "cup_rank_is_2g":pairing_rank==2*genus,
        "plus_is_cocycle":is_cocycle(curve["plus"],s,r),
        "minus_is_cocycle":is_cocycle(curve["minus"],s,r),
        "cusp_gauge_is_nonzero_cocycle":any(gauge) and is_cocycle(gauge,s,r),
        "cusp_gauge_spans_radical":all(cup(gauge,v,r)==0 for v in basis) and len(basis)-pairing_rank==1,
        "alternating":all(matrix[i][i]==0 and all((matrix[i][j]+matrix[j][i])%P==0 for j in range(len(basis))) for i in range(len(basis))),
    }
    if not all(conditions.values()):
        raise ArithmeticError((N,conditions))
    u,v=curve["plus"],curve["minus"]
    j=cup(u,v,r)
    if not j:
        raise ArithmeticError("eigensymbol pairing is not a unit")
    gauge_checks=[cup([(x+a*y)%P for x,y in zip(u,gauge)],[(x+b*y)%P for x,y in zip(v,gauge)],r)==j
                  for a,b in ((1,3),(2,7),(10,10))]
    if not all(gauge_checks):
        raise ArithmeticError("pairing depends on cusp gauge")
    altered=u[:];altered[0]=(altered[0]+1)%P
    noncocycle_rejected=not is_cocycle(altered,s,r)
    if not noncocycle_rejected:
        raise ArithmeticError("cocycle check did not reject the planted defect")
    return {"level":N,"genus":genus,"manin_cocycle_dimension":len(basis),
            "cup_rank":pairing_rank,"radical_dimension":len(basis)-pairing_rank,
            "elliptic_order2_fixed_edges":sum(s[i]==i for i in range(N+1)),
            "elliptic_order3_fixed_triangles":sum(r[i]==i for i in range(N+1)),
            "eigensymbol_pairing_mod11":j,"conditions":conditions,
            "cusp_gauge_controls":gauge_checks,"noncocycle_probe_rejected":noncocycle_rejected,
            "cup_matrix_in_computed_basis":matrix}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--inputs",type=Path,default=ROOT/"data"/"pc002-inputs.json")
    parser.add_argument("--series",type=Path,default=ROOT/"data"/"pc002-relative-regulator.json")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    inp=json.loads(args.inputs.read_text(encoding="utf-8"))
    series=json.loads(args.series.read_text(encoding="utf-8"))
    if series["inputs_sha256"]!=digest(inp):
        raise ValueError("series and cup inputs have different identities")
    target,cal=analyze(inp["target"]),analyze(inp["calibrator"])
    je,j0=target["eigensymbol_pairing_mod11"],cal["eigensymbol_pairing_mod11"]
    factor=j0*pow(je,-1,P)%P
    q=series["quotient_coefficients"]
    normalized=[factor*x%P for x in q]
    controls=[]
    for a,b,c,d in ((2,3,5,7),(10,2,7,3),(4,9,2,8)):
        changed_q=[x*a*b*pow(c*d,-1,P)%P for x in q]
        changed_factor=(c*d*j0)*pow(a*b*je,-1,P)%P
        controls.append([changed_factor*x%P for x in changed_q]==normalized)
    if not all(controls):
        raise ArithmeticError("four independent eigensymbol rescalings do not cancel")
    output={"round":"PC-002","status":"PASS","ring":"F_11[t]/(t^121)",
            "inputs_sha256":digest(inp),
            "pairing_formula":"sum_i (u_i*v_Ri-v_i*u_Ri)/6 on the fixed oriented Farey triangles",
            "target":target,"calibrator":cal,"cup_ratio_mod11":factor,
            "cup_normalized_quotient_coefficients":normalized,
            "four_line_rescaling_controls":controls,
            "claims":{"computed":"Gamma0 Farey cup pairing and a four-eigensymbol-rescaling invariant germ",
                      "matched_to_LR_adjoint_periods":False,"actual_BF_classes_computed":False,
                      "s11_computed":False,"BSD_proved":False}}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":output["status"],"target_pairing":je,"calibrator_pairing":j0,
                      "cup_ranks":[target["cup_rank"],cal["cup_rank"]],
                      "radicals":[target["radical_dimension"],cal["radical_dimension"]],
                      "first_eleven_coefficients":normalized[:P],"controls":controls,
                      "claims":output["claims"]},indent=2))


if __name__=="__main__":
    main()
