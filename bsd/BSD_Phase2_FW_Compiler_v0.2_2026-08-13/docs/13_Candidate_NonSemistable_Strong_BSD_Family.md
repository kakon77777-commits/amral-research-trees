# 13｜Candidate Non-Semistable Strong-BSD Family Schema v0.2

**狀態：研究候選；尚未宣稱正式新定理。**

令 $E/\mathbf Q$ 為 optimal、analytic-rank-$0$ elliptic curve，不要求 semistable。

目標：找一個可有限判定的 base certificate，使某個 Banwait-style infinite twist family
$\mathcal D(E)$ 滿足：

$$
\forall d\in\mathcal D(E),\quad
\operatorname{BSD}(E_d).
$$

## B0 — 2-part anchor

- Banwait–Huang Theorem 2.14 branch；
- $\operatorname{BSD}(E,2)$；
- twist local/splitting條件；
- 建議 $c_E=1$。

## B1 — ordinary ramification reservoir

令

$$
W_{\rm mult}^{odd}(E)=
\{q\text{ odd}:q\parallel N_E\}.
$$

要求非空且：

$$
g_{\rm mult}^{odd}(E)
=
\gcd_{q\in W_{\rm mult}^{odd}(E)}
v_q(\Delta_{\min})
$$

為 $2$ 的冪。

## B2 — FW nonsplit reservoir

$$
W_-(E)\ne\varnothing,
$$

且：

$$
g_-(E)
=
\gcd_{q\in W_-(E)}
v_q(\Delta_{\min})
$$

為 $2$ 的冪。

## B3 — fixed additive odd primes

逐個 exact verify：

```text
FW-H1
FW-H2
period / Manin
```

H3由 B2提供。

## B4 — fixed multiplicative odd primes

逐個 finite check對應 multiplicative theorem hypotheses與 distinct ramified witness。

## B5 — twist support

$p\mid d$ 的 primes要求：

- 避開 3；
- good ordinary；
- 避開 finite residual-reducibility/image exceptions；
- 保持 Theorem 2.14 所需 splitting / inertness條件。

## 尚未完成的 obligations

1. fixed additive primes 的 exact H1 backend；
2. fixed additive primes 的 exact H2 local residual backend；
3. fixed multiplicative branch正式 theorem table；
4. Manin-period compatibility；
5. 所有 support restrictions 的 Chebotarev / CRT simultaneous compatibility；
6. final all-prime cover proof。

六項完成前，不升級為 theorem。
