# 25｜Chebotarev Referee Audit

$$
f_2(x)=x^3+x^2+8x-16.
$$

其 discriminant：

$$
-11136=-2^7\cdot3\cdot29.
$$

irreducible + nonsquare discriminant：

$$
\operatorname{Gal}(L/\mathbf Q)=S_3.
$$

唯一 quadratic subfield：

$$
F_0=\mathbf Q(\sqrt{-174}).
$$

令：

$$
K=\mathbf Q(\zeta_{24},\sqrt{29}).
$$

$$
[K:\mathbf Q]=16.
$$

且：

$$
\sqrt{-174}=\sqrt{-6}\sqrt{29},
$$

而 $\mathbf Q(\sqrt{-6})\subset\mathbf Q(\zeta_{24})$，所以：

$$
F_0\subset K.
$$

因 $K$ abelian，$L$ 的唯一 nontrivial proper Galois subfield又只有 $F_0$：

$$
L\cap K=F_0.
$$

因此：

$$
[LK:\mathbf Q]=48.
$$

support condition：

- identity on $K$；
- 3-cycle on $L$。

3-cycle fix $F_0$，所以 compatible。

class size：

$$
2.
$$

Chebotarev：

$$
\boxed{\delta(\mathcal P)=2/48=1/24.}
$$

---

# Numerical sanity

v0.4另用完全獨立的小型 polynomial-mod-$q$ verifier掃：

$$
q<10^7.
$$

這只驗 implementation與 density trend，不替代 theorem。
