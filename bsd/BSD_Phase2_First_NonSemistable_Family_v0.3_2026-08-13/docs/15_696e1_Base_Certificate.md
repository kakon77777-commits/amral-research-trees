# 15｜696.e1 Base Certificate

## Curve

$$
E:\ y^2=x^3+x^2+8x-16.
$$

$$
N=696=2^3\cdot3\cdot29.
$$

$$
\Delta_{\min}=-2^{11}\cdot3\cdot29<0.
$$

$$
E(\mathbb Q)_{\rm tors}=0.
$$

analytic / algebraic rank：

$$
0.
$$

optimal，Manin constant：

$$
1.
$$

---

# Base BSD(E,2)

Banwait–Huang 的 introduction回顧：

> full BSD 已驗證到 conductor $5000$ 的 analytic rank $0/1$ elliptic curves。

因此本 curve：

$$
696<5000,\qquad r_{\rm an}=0
$$

有：

$$
\boxed{\operatorname{BSD}(E)}
$$

的既有 rigorous verification。

特別：

$$
\boxed{\operatorname{BSD}(E,2)}.
$$

這裡不使用：

```text
analytic Sha = 1 => actual Sha = 1
```

這種 circular inference。

---

# Lalg gate

LMFDB：

$$
\Sha_{\rm an}=1,
\qquad
\prod c_p=1,
\qquad
|E(\mathbb Q)_{\rm tors}|=1,
\qquad
Reg=1.
$$

按 analytic Sha定義：

$$
\frac{L(E,1)}{\Omega_E}=1.
$$

所以：

$$
\boxed{
v_2(L^{alg}(E,1))=0.
}
$$

---

# 2-division cubic

因 $a_1=a_3=0$：

$$
f_2(x)
=
x^3+x^2+8x-16.
$$

無 rational root，因此 irreducible over $\mathbb Q$。

其 discriminant：

$$
\operatorname{disc}(f_2)
=
-11136
=
-2^7\cdot3\cdot29.
$$

不是平方。

故 Galois closure：

$$
S_3.
$$

quadratic resolvent：

$$
\mathbb Q(\sqrt{-174}).
$$
