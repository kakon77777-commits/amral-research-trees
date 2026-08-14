# BSD Phase 2 — Fouquet–Wan Compiler v0.2

**日期：** 2026-08-13  
**定位：** 從 literature map 推進到 theorem-hypothesis compiler  
**狀態：** derived bridge / proof schema；尚未宣稱新的完整 BSD 定理

## 本輪核心結論

Fouquet–Wan 不應拿來取代所有 odd-prime theorem。正確角色是：

- fixed additive bad primes；
- good supersingular primes。

ordinary primes 繼續走既有 ordinary Iwasawa / BSD 路線。

這使原本看似無窮的 FW-H2 檢查縮成：

> 只有固定 additive bad primes 需要 expensive local residual check。

## H3 exact compiler

令

$$
W_-(E)=\{\ell:\ell\parallel N_E,\ E/\mathbf Q_\ell
\text{ nonsplit multiplicative}\}.
$$

則 weight-2 elliptic curve 的 FW-H3 可編譯為：

$$
\boxed{
\exists \ell\in W_-(E),\ \ell\ne p,\ 
p\nmid v_\ell(\Delta_{\min}).
}
$$

再令

$$
g_-(E)=\gcd_{\ell\in W_-(E)}v_\ell(\Delta_{\min}).
$$

若 $W_-(E)\neq\varnothing$ 且 $g_-(E)$ 是 $2$ 的冪，則每個 odd good supersingular prime都自動取得 H3 witness。

## H2 exact compiler

FW 禁型：

$$
E[p]|_{G_{\mathbf Q_p}}^{ss}
\simeq
\psi\oplus\psi\bar\chi_{\rm cyc}.
$$

因 $\det E[p]=\bar\chi_{\rm cyc}$，禁型必有：

$$
\psi^2=1.
$$

若 local semisimplification為 $\alpha\oplus\beta$，則：

$$
\boxed{
\mathrm{H2\ FAIL}
\iff
\alpha/\beta\in
\{\bar\chi_{\rm cyc},\bar\chi_{\rm cyc}^{-1}\}.
}
$$

good supersingular：H1/H2 automatic PASS。  
good ordinary：H2 failure 可化成

$$
a_p(E)^2\equiv1\pmod p,
$$

但這不提供乾淨的 finite-prime compression，因此 ordinary universe 不走 FW。

## Phase 2 v0.2 verdict

$$
\boxed{
\text{FW = surgical bridge, not universal replacement.}
}
$$

下一輪只做：

1. fixed additive primes 的 exact H1/H2 backend；
2. 找具體 non-semistable curves 的 $W_{\rm mult}$、$W_-$ 與 gcd certificates；
3. 尋找第一個所有 prime branches 都可閉合的 base curve。
