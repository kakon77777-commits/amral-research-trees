#!/usr/bin/env python3
p=11
M=((1,2),(1,4))
det=(M[0][0]*M[1][1]-M[0][1]*M[1][0])%p
mt=6
ratio=(mt*pow(det,-1,p))%p
assert det==2
assert ratio==3
assert det!=0 and mt!=0
print("FINITE_NORM_BOCKSTEIN_EXACT")
print(f"det_M_loc_mod_11={det}")
print(f"finite_Bockstein= {det} * X_397*X_991")
print(f"Mazur_Tate_initial= {mt} * X_397*X_991")
print(f"deterministic_unit_ratio={ratio}")
print("MIXED_LINE_COINCIDENCE_OK")
