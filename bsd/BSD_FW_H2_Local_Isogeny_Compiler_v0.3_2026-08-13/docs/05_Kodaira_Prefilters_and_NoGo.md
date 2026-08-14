# 05｜Kodaira Prefilters and No-Go Results

## Exact no-go: potentially multiplicative

potentially multiplicative curve由 quadratic character \(\psi\) twist後成 Tate curve。

Tate residual semisimplification：

\[
1\oplus\omega.
\]

twist回去：

\[
\psi\oplus\psi\omega.
\]

因：

\[
\psi^2=1,
\]

它正好是 FW Theorem 1.7 forbidden form。

所以：

```text
ADDITIVE + POTENTIALLY_MULTIPLICATIVE
=> FW17_H2_FAIL
```

不用 local backend。

---

## \(p=3\)

\[
\mathbf F_3^\times
=
\{\pm1\}.
\]

所以任何 local \(1\)-dimensional constituent都是 quadratic/trivial。

因此：

```text
p=3 + LOCAL_REDUCIBLE
=> FW17_H2_FAIL

p=3 + LOCAL_IRREDUCIBLE
=> FW17_H2_PASS
```

---

## rational local \(p\)-torsion

若：

\[
E(\mathbf Q_p)[p]\neq0,
\]

trivial line存在：

```text
=> FW17_H2_FAIL
```

Pannekoek可協助 cheap-detect additive local p-torsion。

但：

```text
NO rational p-torsion
!= H2 PASS
```

因 kernel character仍可能是 nontrivial quadratic。

---

## 正式拒絕 Kodaira-only table

以下推論不得使用：

```text
potentially supersingular => PASS
potentially good ordinary => FAIL/PASS
Kodaira X => automatic H2
```

除非另外有 residual-character theorem。

Kodaira / potential-reduction只作優先排序，
final decision必須落到：

```text
local residual irreducibility
or
local p-isogeny character/kernel certificate.
```
