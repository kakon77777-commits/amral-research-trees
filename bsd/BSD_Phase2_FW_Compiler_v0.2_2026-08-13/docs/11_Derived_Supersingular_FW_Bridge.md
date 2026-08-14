# 11｜Derived Supersingular FW Bridge

**狀態：** 由現有外部定理拼接出的 derived proposition；不是原論文命名定理。

令 $E/\mathbf Q$ 為 elliptic curve，$p>2$ 為 good supersingular prime。

假設存在：

$$
\ell\parallel N_E
$$

使：

1. $E$ 在 $\ell$ nonsplit multiplicative；
2.
   $$
   p\nmid v_\ell(\Delta_{\min}).
   $$

則：

- good supersingular local irreducibility給 FW-H1；
- 同一 irreducibility排除 FW-H2禁型；
- nonsplit Steinberg + residual ramification給 FW-H3。

因此 $E[p]$ 滿足 Fouquet–Wan residual hypotheses。

若再有：

$$
L(E,1)\ne0,
$$

則可套其 rank-zero $p$-part BSD corollary，惟 period normalization / Manin constant需另外閉合。

## Uniform form

若：

$$
g_-(E)=2^a,
$$

則所有 odd good supersingular primes一次得到 H3。

所以：

$$
\boxed{
\text{all good supersingular odd primes}
}
$$

可由一個 finite base certificate關閉。

## Safe period condition

候選 theorem 第一版建議直接要求：

$$
\boxed{c_E=1}
$$

避免 modular period / Néron period拼接 ambiguity。
