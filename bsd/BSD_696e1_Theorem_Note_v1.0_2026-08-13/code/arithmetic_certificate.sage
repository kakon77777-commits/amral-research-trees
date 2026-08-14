# SageMath certificate for the finite arithmetic inputs of the theorem note.
# Run with: sage arithmetic_certificate.sage

E = EllipticCurve([0,1,0,8,-16])

assert E.conductor() == 696
assert E.discriminant() == -178176
assert E.rank() == 0
assert E.torsion_order() == 1
assert E.lseries().L_ratio() == 1

# Isogeny class should be singleton.
C = E.isogeny_class()
assert len(C.curves) == 1

# Two-division cubic (scalar multiples define the same field).
R.<x> = PolynomialRing(QQ)
f2 = x^3 + x^2 + 8*x - 16
assert f2.is_irreducible()
assert f2.discriminant() == -11136

# Local discriminant valuations.
assert E.discriminant().valuation(3) == 1
assert E.discriminant().valuation(29) == 1

print("Base arithmetic certificate: PASS")
print("L(E,1)/Omega_E =", E.lseries().L_ratio())
print("disc(f2) =", f2.discriminant())
