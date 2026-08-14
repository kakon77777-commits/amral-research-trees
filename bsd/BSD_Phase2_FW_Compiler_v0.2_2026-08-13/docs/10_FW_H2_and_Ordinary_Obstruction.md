# 10｜FW-H2 Compiler 與 Ordinary Obstruction

## Good supersingular

good supersingular的 residual local representation由 niveau-2 fundamental characters控制，local residual type irreducible。

所以：

$$
\boxed{
\mathrm{FW\text{-}H1=PASS,\qquad
FW\text{-}H2=PASS.
}
$$

FW 只剩 H3。

## Good ordinary

標準 ordinary semisimplification：

$$
\bar\rho^{ss}
\simeq
\bar\alpha
\oplus
\bar\chi_{\rm cyc}\bar\alpha^{-1},
$$

其中 $\bar\alpha$ unramified，Frobenius value對應 $a_p\bmod p$。

H2 failure iff

$$
\bar\alpha^2=1,
$$

故：

$$
\boxed{
a_p(E)^2\equiv1\pmod p.
}
$$

這是 cheap exact criterion。

## 為什麼 ordinary 不應走 FW？

要用 FW cover所有 ordinary primes，必須排除所有滿足：

$$
a_p^2\equiv1\pmod p
$$

的 prime。

一般沒有乾淨的 finite-exception theorem可供使用。

所以：

$$
\boxed{
\text{ordinary primes繼續用 ordinary theorem；
FW留給 additive + supersingular。}
}
$$

## Potentially multiplicative

local semisimplification本來就呈 quadratic Tate twist：

$$
\psi\oplus\psi\bar\chi_{\rm cyc},
$$

因此落入 FW-H2 禁型。

這一 branch 也不走 FW。
