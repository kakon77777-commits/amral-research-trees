# Exact/local replay gate for P5-BOC-NZ11.
# Run under SageMath and preserve the complete stdout.

E = EllipticCurve('389a1')
p = 11
prec = 30

assert E.conductor() == 389
assert E.rank() == 2
assert E.has_good_reduction(p)
assert E.ap(p) % p != 0

R = E.padic_regulator(p, prec)
print("curve =", E.cremona_label())
print("p =", p)
print("precision =", prec)
print("p-adic regulator =", R)
print("valuation =", R.valuation())
assert R != 0
print("P5_BOC_NZ11_REPLAY_PASS")
