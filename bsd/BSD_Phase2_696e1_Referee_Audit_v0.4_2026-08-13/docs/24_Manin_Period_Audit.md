# 24｜Manin / Period Audit

FW Corollary 1.10公式使用 modular-form period，並提醒 elliptic curve的 Néron period相差 Manin constant。

現代結果給：

> optimal parametrization的 Manin constant只可能由 additive reduction primes支撐。

對 $E_q$：

- additive primes是 $2$ 與 twist prime $q$；
- FW只用在 **good supersingular $p$**。

所以：

$$
p\notin\{2,q\}
$$

且：

$$
\boxed{p\nmid c_{E_q}.}
$$

因此 modular/Néron period在 $p$-adic valuation上相同。

## Optimality

base `696.e1` mod-$\ell$ images maximal for all $\ell$。

quadratic twisting保持 residual irreducibility，因此 $E_q$ 沒有 rational prime-degree isogeny。

故其 Q-isogeny class沒有另一條 nonisomorphic curve，$E_q$ 本身就是 optimal representative。

所以此 period argument不依賴任意挑選 isogenous model。
