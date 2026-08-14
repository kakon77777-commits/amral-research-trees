#!/usr/bin/env python3
import json
from pathlib import Path

p = 11
M = [[1,2],[1,4]]

def det2(M):
    return (M[0][0]*M[1][1]-M[0][1]*M[1][0]) % p

def row_kernel(row):
    # Return a nonzero vector (-b,a) for row (a,b).
    a,b=row
    return ((-b)%p, a%p)

def dot(row,v):
    return sum(x*y for x,y in zip(row,v)) % p

assert det2(M) == 2
k397 = row_kernel(M[0])  # (-2,1)
k991 = row_kernel(M[1])  # (-4,1)
assert k397 == (9,1)
assert k991 == (7,1)
assert dot(M[0], k397) == 0
assert dot(M[1], k991) == 0
assert dot(M[1], k397) != 0
assert dot(M[0], k991) != 0
# Columns k397,k991 relative to (P,Q).
K = [[k397[0], k991[0]],[k397[1], k991[1]]]
kwedge = det2(K)
assert kwedge == 2

result = {
    "schema_version":"1.2",
    "curve":"389.a1",
    "p":11,
    "dependency":"Sha[11]=0 and v1.1 localization matrix",
    "selmer_dimension":2,
    "localization_matrix":M,
    "localization_determinant_mod11":2,
    "norm_selmer": {
        "empty": {"dimension":2, "basis":["P","Q"]},
        "397": {"dimension":1, "basis_vector_coordinates_P_Q":[-2,1], "basis":"Q-2P"},
        "991": {"dimension":1, "basis_vector_coordinates_P_Q":[-4,1], "basis":"Q-4P"},
        "397_991": {"dimension":0, "basis":[]}
    },
    "transversality": {
        "intersection_single_norm_lines_dimension":0,
        "sum_single_norm_lines_dimension":2,
        "wedge_coefficient_mod11":kwedge,
        "status":"PRIMITIVE_TRANSVERSE"
    },
    "exact_sequence": "0 -> Sel_11(E/Q) -> L_397 (+) L_991 -> 0 via localization isomorphism",
    "gate_status": {
        "P5_NORM_COREVERTEX_11_rank2":"CLOSED_EXACT_UNDER_INHERITED_SHA11_ZERO",
        "P5_ANOM_BocCOMP_11_rank2":"OPEN"
    }
}
out=Path(__file__).resolve().parents[1]/"results"/"norm_selmer_core_vertex_certificate.json"
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("NORM_SELMER_CORE_VERTEX_EXACT")
print("dims = 2, 1, 1, 0")
print("K_397 = <Q-2P>")
print("K_991 = <Q-4P>")
print("wedge coefficient mod 11 =",kwedge)
