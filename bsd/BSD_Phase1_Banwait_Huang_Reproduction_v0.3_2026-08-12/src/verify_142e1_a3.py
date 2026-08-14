#!/usr/bin/env python3
def count_points(p,a1,a2,a3,a4,a6):
    affine=[]
    for x in range(p):
        for y in range(p):
            lhs=(y*y+a1*x*y+a3*y)%p
            rhs=(x**3+a2*x*x+a4*x+a6)%p
            if lhs==rhs:
                affine.append((x,y))
    return 1+len(affine), affine

# Cremona 142E1:
# y^2 + x y = x^3 - x^2 - 2626 x + 52244
p=3
n, affine = count_points(p,1,-1,0,-2626,52244)
a_p = p + 1 - n
print("affine points mod 3:", affine)
print("#E(F_3) =", n)
print("a_3 =", a_p)
assert affine == []
assert n == 1
assert a_p == 3
