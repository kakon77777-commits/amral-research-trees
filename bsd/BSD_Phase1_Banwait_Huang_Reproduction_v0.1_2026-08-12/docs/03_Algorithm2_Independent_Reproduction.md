# 03｜Algorithm 2 獨立重現

## 0. 目的

建立一個只依賴 Python 標準庫的 mirror，重播：

- squarefree；
- gcd；
- $a_p$；
- finite-field point count；
- $2$-adic valuation；
- quadratic splitting；
- cubic 2-division inertness；
- sign condition。

它不實作 Algorithm 1 的 descent / isogeny / optimality / L-value部分。

---

# 1. Finite-field point count

對一般 Weierstrass equation：

$$
y^2+a_1xy+a_3y
=
x^3+a_2x^2+a_4x+a_6,
$$

固定 $x\in\mathbb F_p$ 後，視為 $y$ 的二次方程。

對 odd $p$，其判別式為：

$$
D_x
=
(a_1x+a_3)^2
+
4(x^3+a_2x^2+a_4x+a_6).
$$

所以：

$$
\#\{y\}
=
1+\chi_p(D_x).
$$

再加上無窮遠點即可得到：

$$
\#E(\mathbb F_p).
$$

---

# 2. Ordinary test

$$
a_p(E)
=
p+1-\#E(\mathbb F_p).
$$

程式檢查：

$$
p\nmid a_p(E).
$$

---

# 3. CLZ branch

對：

$$
46a1,
$$

程式得到官方完全相同的七個 twists：

$$
1,185,265,305,745,785,905.
$$

---

# 4. Zhai branch

$2$-torsion的 $x$-coordinates滿足 cubic：

$$
4x^3+b_2x^2+2b_4x+b_6=0,
$$

其中：

$$
b_2=a_1^2+4a_2,
$$

$$
b_4=2a_4+a_1a_3,
$$

$$
b_6=a_3^2+4a_6.
$$

對 theorem 排除的 ramified primes之外，degree-$3$ polynomial modulo $p$ 無 root等價於 irreducible，因而對應 inert prime。

對：

$$
106d1,
$$

得到官方完全相同的 $21$ 個 twists。

---

# 5. 限制

此 mirror 的 inertness判定使用 cubic reduction modulo $p$。

在一般 number-field計算中，正式證書應使用：

```text
factorization of p O_F
```

或 Sage：

```python
F.ideal(p).is_prime()
```

本測試中，由 theorem 的：

$$
(d,3N)=1
$$

排除了相關 ramified bad primes，且與官方 fixture完全一致。

但 full production仍應以 Sage number-field backend為權威。

---

# 6. 重現結果

```text
46a1:
expected 7
actual   7
exact list match: PASS

106d1:
expected 21
actual   21
exact list match: PASS
```

因此：

$$
\boxed{
\text{Algorithm 2 branch logic可被獨立重播。}
}
$$
