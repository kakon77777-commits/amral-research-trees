# Independent canonical/eclib replay for E=389a1, p=11, n=397*991.
# This follows the public Ghitza-Kim reference convention.
from sage.libs.eclib.newforms import ECModularSymbol

E = EllipticCurve('389a1')
p = 11
ells = [397, 991]
roots = {397: 5, 991: 6}
n = prod(ells)
L = GF(p)
f = ECModularSymbol(E, sign=1)

# Reference-code normalization: eclib's normalization differs by scale 2
# only when the discriminant is negative. Here Disc(E)=389>0.
scale = 1 if E.discriminant() > 0 else 2

LOGS = {}
for ell in ells:
    K = GF(ell)
    g = K(roots[ell])
    assert g.multiplicative_order() == ell - 1
    tbl = {}
    for a in K:
        if a != 0:
            tbl[a] = L(a.log(g))
    LOGS[ell] = tbl

S = L(0)
for a in xsrange(1, n):
    if gcd(a, n) == 1:
        mult = L(f(a/n))
        for ell in ells:
            mult *= LOGS[ell][GF(ell)(a)]
        S += mult

res = S / scale
print('curve=', E.label())
print('p=', p)
print('n=', n)
print('delta_mod_11=', res)
print('nonzero=', bool(res != 0))
assert res != 0
