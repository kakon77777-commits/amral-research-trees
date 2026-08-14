# 09｜FW-H3 Exact Elliptic-Curve Compiler

定義

$$
W_-(E)=
\{\ell:\ell\parallel N_E,\ E\text{ nonsplit multiplicative at }\ell\}.
$$

對 odd $p$：

$$
\mathrm{FW\text{-}H3}(E,p)
\iff
\exists\ell\in W_-(E),\ 
\ell\ne p,\ 
p\nmid v_\ell(\Delta_{\min}).
$$

## Uniform certificate

令

$$
g_-(E)=
\gcd_{\ell\in W_-(E)}
v_\ell(\Delta_{\min}).
$$

若：

$$
W_-(E)\ne\varnothing
$$

且

$$
g_-(E)=2^a,
$$

則沒有 odd prime同時整除所有 witness valuations。

因此在 good supersingular / fixed additive branch 中：

$$
\boxed{
\forall p>2,\quad
\mathrm{FW\text{-}H3}(E,p)=PASS
}
$$

只需一個有限 base certificate。

## Twist-family preservation

若 Banwait-style twist family要求每個 $\ell\mid N$ 在
$\mathbf Q(\sqrt d)$ 中 split，則 quadratic twist character在
$G_{\mathbf Q_\ell}$ 上 trivial，因此同一 H3 witness沿 family保存。
