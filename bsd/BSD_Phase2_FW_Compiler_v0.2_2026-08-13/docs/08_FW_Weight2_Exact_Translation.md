# 08｜Fouquet–Wan Theorem 1.7：Weight-2 Exact Translation

## H1

$$
\bar\rho_{E,p}\text{ absolutely irreducible}.
$$

## H2

不存在 character $\psi:G_{\mathbf Q_p}\to\mathbf F_p^\times$ 使

$$
\bar\rho_{E,p}|_{G_{\mathbf Q_p}}^{ss}
\simeq
\psi\oplus\psi\bar\chi_{\rm cyc}.
$$

由

$$
\det E[p]=\bar\chi_{\rm cyc}
$$

可得禁型必滿足

$$
\psi^2=1.
$$

因此 H2 failure 是：

> local residual semisimplification為一個 quadratic character與其 cyclotomic twist的直和。

若

$$
V^{ss}=\alpha\oplus\beta,
$$

則等價 ratio test：

$$
\boxed{
\mathrm{H2\ FAIL}
\iff
\alpha\beta^{-1}
\in\{\bar\chi_{\rm cyc},\bar\chi_{\rm cyc}^{-1}\}.
}
$$

這是 production compiler 應使用的 representation-level predicate。

## H3

對 weight $2$ elliptic curve，FW 的 auxiliary Steinberg prime可 specialised 為：

- $\ell\parallel N$；
- nonsplit multiplicative reduction；
- $\bar\rho_{E,p}$ 在 $\ell$ ramified。

而 multiplicative prime的 residual ramification由：

$$
p\nmid v_\ell(\Delta_{\min})
$$

判定。

所以：

$$
\boxed{
\mathrm{FW\text{-}H3}(E,p)
\iff
\exists\ell\parallel N:
\begin{cases}
E \text{ nonsplit multiplicative at }\ell,\\
\ell\ne p,\\
p\nmid v_\ell(\Delta_{\min}).
\end{cases}
}
$$
