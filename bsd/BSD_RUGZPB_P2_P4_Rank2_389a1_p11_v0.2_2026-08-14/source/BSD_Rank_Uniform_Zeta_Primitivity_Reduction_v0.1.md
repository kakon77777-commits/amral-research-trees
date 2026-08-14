---
title: "BSD 的全域壓縮與高秩不可約前線：Rank-Uniform Zeta Primitivity Reduction"
subtitle: "Global Compression and the Irreducible Higher-Rank Frontier of the Birch–Swinnerton-Dyer Conjecture"
version: "v0.1"
date: "2026-08-14"
author: "Neo.K / EveMissLab"
language: "zh-TW"
status: "Theorem-style reduction paper / research handoff"
epistemic_status: "Contains proved reductions and no-go lemmas; does NOT prove or disprove BSD."
---

# BSD 的全域壓縮與高秩不可約前線  
## Rank-Uniform Zeta Primitivity Reduction

### 摘要

本文整理一條針對橢圓曲線 Birch–Swinnerton-Dyer 猜想（BSD）的全域研究路線。研究的出發點不是再次重述 BSD，而是將近年的 rank-$0/1$ Iwasawa、zeta element、$p$-part BSD、quadratic-twist family theorem 與可算法化證書工作，與既有的全域量詞壓縮、定理閉包、格點極限 no-go 與高秩 wall audit 統合。

本文首先將 BSD 拆成三個彼此不能偷換的層級：

$$
\mathrm{BSD\text{-}W}:
\operatorname{rank}E(\mathbb Q)
=
\operatorname{ord}_{s=1}L(E,s),
$$

$$
\mathrm{BSD\text{-}F}:
\#\Sha(E/\mathbb Q)<\infty,
$$

以及 leading coefficient identity

$$
\mathrm{BSD\text{-}S}:
\frac{L^{(r)}(E,1)}{r!}
=
\frac{
\#\Sha(E/\mathbb Q)\,
\Omega_E\,
\operatorname{Reg}(E/\mathbb Q)\,
\prod_p c_p
}{
\#E(\mathbb Q)_{\mathrm{tors}}^2
},
$$

其中

$$
r=
\operatorname{ord}_{s=1}L(E,s).
$$

接著證明兩個方法論 no-go。第一，任何對全體橢圓曲線的 faithful positive atomic compression 雖可把全域量詞壓成單一非負量，但「缺陷量為零」本身仍需要新的算術消失機制；量詞壓縮不是證明複雜度崩塌。第二，函數近似或格點極限不保持零點重數：即使 $f_a\to f_0$ 極好地收斂，也可能發生 $\operatorname{ord}_0 f_a=1$ 而 $\operatorname{ord}_0 f_0=2$，因此任何由離散 $L$-function/rank 直接取極限推出 BSD 的路線，必須另證 multiplicity/rank stabilization theorem。

在正向部分，本文把現有進展分成兩種不同 closure。rank-$0$ quadratic-twist families 的近期工作已顯示，原本表面上的

$$
\forall p
$$

可在適當 theorem router 下被壓成 generic-prime theorem 加 finite exceptional-prime certificates。這是一種真正有效的「prime-quantifier compression」，但它不自動延伸到 rank $2+$，因為高秩缺口不是單純的 prime enumeration，而是 analytic leading term、Mordell–Weil regulator、Selmer complex、$\Sha$ 與 integral zeta class 之間缺乏 rank-uniform global bridge。

本文因此提出一個明確但仍未證的 theorem target：**Rank-Uniform Global Zeta-Primitivity Bridge（RUGZPB）**。其目標是對任意 $E/\mathbb Q$ 與任意 analytic rank $r$，構造一個 canonical derived zeta object，使其同時具有：

1. analytic exact-order / leading-term compatibility；
2. Mordell–Weil exterior-power / regulator compatibility；
3. integral Selmer determinant-line compatibility；
4. all-prime local-to-global primitivity；
5. $\Sha$ finiteness/index recovery；
6. 對 $r=0,1,2,\ldots$ 的 rank-uniformity。

本文證明一個條件式 reduction theorem：若 RUGZPB 以本文定義的完整強度對所有 $E/\mathbb Q$ 成立，則 weak BSD、$\Sha$ finiteness 與 strong BSD leading coefficient formula 同時成立。這不是 BSD 證明；它把目前散落的高秩未知量壓縮成一個可被逐條攻擊、可形式化、可失敗的 theorem interface。

**關鍵詞：** Birch–Swinnerton-Dyer conjecture、elliptic curves、zeta elements、Selmer groups、Iwasawa theory、Tamagawa number conjecture、higher rank、global quantifier、primitivity、determinant line、Shafarevich–Tate group

---

# 0. 學術定位與非主張聲明

本文必須首先固定認識論狀態。

本文**不宣稱**：

1. 已證明 BSD；
2. 已否定 BSD；
3. 已證明任意 rank 的 Bloch–Kato / ETNC；
4. 已構造本文所需的 rank-uniform zeta object；
5. 已將 rank-$0/1$ 的 zeta-element theorem 自動延伸至 rank $2+$；
6. 已由 finite database、density-one family 或 finite-prime verification 推出全體 BSD；
7. 已證明本文提出的 RUGZPB 比既有 Bloch–Kato / ETNC formulation 更強、更弱或具有優先權意義。

本文**真正證明或整理**的是：

- BSD 的全域量詞與 component closure 必須分離；
- faithful global compression 不是 proof-producing mechanism；
- 普通 grid/function convergence 不保證 order-of-vanishing stabilization；
- rank-$0$ family 的 all-prime closure 與 arbitrary-rank BSD 屬於不同 theorem layer；
- 若一個指定的 rank-uniform integral zeta-primitivity bridge 成立，則可條件式推出完整 BSD；
- 因此高秩 frontier 可被壓成明確的 bridge obligations，而非模糊地寫成「仍缺一些高秩技術」。

---

# 1. BSD 的三層命題

令

$$
E/\mathbb Q
$$

為橢圓曲線，$L(E,s)$ 為其 Hasse–Weil $L$-function。

定義 analytic rank

$$
r_{\mathrm{an}}(E)
=
\operatorname{ord}_{s=1}L(E,s),
$$

以及 algebraic rank

$$
r_{\mathrm{alg}}(E)
=
\operatorname{rank}E(\mathbb Q).
$$

## 1.1 Weak BSD

$$
\boxed{
r_{\mathrm{alg}}(E)=r_{\mathrm{an}}(E).
}
$$

這裡只處理 rank equality。

## 1.2 Finiteness layer

$$
\boxed{
\#\Sha(E/\mathbb Q)<\infty.
}
$$

即使 rank equality 已知，也不能自動得到 $\Sha$ finite。

## 1.3 Strong leading coefficient layer

若

$$
r=r_{\mathrm{an}}(E)=r_{\mathrm{alg}}(E),
$$

則 strong BSD 預測：

$$
\boxed{
\frac{L^{(r)}(E,1)}{r!}
=
\frac{
\#\Sha(E/\mathbb Q)\,
\Omega_E\,
\operatorname{Reg}(E/\mathbb Q)\,
\prod_p c_p
}{
\#E(\mathbb Q)_{\mathrm{tors}}^2
}.
}
$$

因此全文採用：

$$
\boxed{
\mathrm{BSD}
=
\mathrm{BSD\text{-}W}
+
\mathrm{BSD\text{-}F}
+
\mathrm{BSD\text{-}S}.
}
$$

任何只證明其中一層的結果不得升格成 full BSD。

---

# 2. Certificate ladder 與禁止偷換

本文使用下列概念階梯。

- **C0**：curve identity；
- **C1**：local arithmetic；
- **C2**：numerical analytic rank；
- **C3**：rigorous analytic rank；
- **C4**：algebraic lower bound；
- **C5**：algebraic upper bound；
- **C6**：weak BSD；
- **C7**：single-prime strong BSD；
- **C8**：$\Sha$ finite / exact；
- **C9**：full strong BSD；
- **C10**：family theorem。

禁止下列推理：

$$
\text{analytic }\Sha
\not\Rightarrow
\text{proved }\Sha,
$$

$$
\operatorname{rank}()\text{ output}
\not\Rightarrow
\text{formal rank proof},
$$

$$
\operatorname{BSD}(E,p)
\not\Rightarrow
\operatorname{BSD}(E),
$$

$$
r\le1\text{ theorem}
\not\Rightarrow
r=2\text{ theorem},
$$

以及：

$$
\text{finite database verification}
\not\Rightarrow
\forall E/\mathbb Q.
$$

---

# 3. 2024–2026 的低秩 theorem closure

本節只列對本文 reduction 必要的外部輸入。

## 3.1 Zeta elements 與 rank $0/1$

Burungale–Skinner–Tian–Wan 建構橢圓曲線的 $p$-adic zeta elements，並透過 explicit reciprocity laws 與 Iwasawa main conjecture 得到多個 BSD 應用，包括 semistable elliptic curves 在 supersingular primes 的 main-conjecture 結果，以及 analytic rank $0/1$ 的 $p$-part BSD；其工作亦給出第一批 non-CM elliptic curves 的無限 strong-BSD families。

對本文最重要的訊息不是某一條 family，而是：

$$
\boxed{
\text{zeta element}
+
\text{Iwasawa/Selmer control}
+
\text{rank }0/1\text{ leading term}
}
$$

已經不是純猜想式語言，而有實際 theorem closure。

## 3.2 Banwait–Huang 的 theorem compiler

Banwait–Huang 將前述 strong-BSD twist criteria 編譯成明確算法，並對 conductor $\le500000$ 的 LMFDB elliptic curves 做系統辨識。

內部 Phase 1 reproduction 已完成：

1. theorem predicate map；
2. algorithm independent reproduction；
3. old/current semantic audit；
4. finite conductor regression；
5. removed-curve failure closure；
6. $500000$ conductor-domain exact artifact census。

因此 rank-$0$ twist-family 路線已從：

$$
\text{paper theorem}
$$

推進到：

$$
\boxed{
\text{paper theorem}
\to
\text{machine-checkable predicate router}.
}
$$

## 3.3 Fouquet–Wan 與 non-semistable odd-$p$ bridge

Fouquet–Wan 證明 modular motives 的 cyclotomic Iwasawa main conjecture，在 residual hypotheses 下允許 prime $p$ 處 arbitrary reduction type。

對 rank-$0$ twist family，這提供一個重要可能性：

$$
\text{Banwait--Huang }2\text{-part/nonvanishing}
+
\text{ordinary/multiplicative routes}
+
\text{Fouquet--Wan surgical odd-}p\text{ route}.
$$

內部 Phase 2 的正確結論不是「Fouquet–Wan 取代全部 odd-prime theorem」，而是：

$$
\boxed{
\text{FW = surgical bridge, not universal replacement}.
}
$$

---

# 4. Rank-$0$ family 的真正量詞壓縮

對某些 non-semistable rank-$0$ quadratic-twist family，內部研究已將表面上的：

$$
\forall p>2
$$

重新組織成：

$$
\boxed{
\text{generic-prime theorem}
+
\text{finite exceptional-prime audit}.
}
$$

例如 multiplicative witness valuations 可形成 gcd：

$$
g(E)
=
\gcd_{\ell\in W(E)}
v_\ell(\Delta_{\min}),
$$

其 odd prime divisors 不必直接 reject curve，而可放入 finite exception table。

因此：

$$
p\mid g(E)
$$

正確解讀為：

$$
\boxed{
p\text{ needs an exceptional route},
}
$$

而不是：

$$
\boxed{
E\text{ fails BSD}.
}
$$

這一步的結構價值很高，因為它展示：

$$
\boxed{
\forall p
}
$$

不一定要逐一 brute-force。

它可以透過 witness network、ramification reservoir、ordinary/supersingular routing 與 finite-exception compiler 壓縮。

然而，這個成功不能被偷換成 full BSD。

---

# 5. 為什麼 prime-quantifier compression 不等於高秩 closure

rank-$0$ 時：

$$
L(E,1)\ne0.
$$

regulator 層退化：

$$
\operatorname{Reg}(E/\mathbb Q)=1
$$

（依標準 rank-$0$ convention）。

因此 strong BSD 的核心可以高度 $p$-primary 化。

但當：

$$
r\ge2,
$$

問題新增：

1. exact analytic order；
2. $r$ 個 independent rational directions；
3. regulator determinant；
4. higher derived zeta / Euler-system classes；
5. high-rank Selmer structure；
6. $\Sha$ finiteness；
7. leading coefficient 的 archimedean comparison；
8. integral compatibility across all primes。

所以：

$$
\boxed{
\text{rank-0 all-prime compression}
\not\Rightarrow
\text{rank-uniform BSD}.
}
$$

rank-$0$ 的主要「無窮」之一是：

$$
\forall p.
$$

rank-$2+$ 的主要「無窮」還包含：

$$
\boxed{
\text{derived arithmetic structure of arbitrary rank}.
}
$$

---

# 6. Canonical rank-$2$ wall probe：389.a1

內部 certificate 使用：

$$
E=389.a1
$$

作為 rank-$2$ wall probe。

目前保存：

$$
r_{\mathrm{alg}}=2
$$

為 rigorous computationally certified input；

analytic rank $2$ 目前在內部 certificate 中仍要求附獨立 rigorous certificate；

numerical leading coefficient：

$$
\frac{L^{(2)}(E,1)}{2!}
\approx
0.759316500288426770\ldots
$$

regulator：

$$
\operatorname{Reg}(E)
\approx
0.15246017794314375\ldots
$$

並有：

$$
\prod_p c_p=1,
\qquad
\#E(\mathbb Q)_{\mathrm{tors}}=1.
$$

BSD-inferred analytic $\Sha$ prediction 為 $1$，但 actual

$$
\#\Sha(E/\mathbb Q)
$$

在此 certificate 中仍標記為 unknown，finiteness 亦未取得 proof。

因此此 curve 的用途不是「找反例」，而是顯示：

$$
\boxed{
\text{數值 identity 幾乎全部可見}
\not\Rightarrow
\text{rank-2 BSD theorem}.
}
$$

真正缺口是：

$$
\boxed{
\text{analytic rank/leading term}
\longleftrightarrow
\text{integral Selmer/MW/Sha structure}.
}
$$

---

# 7. Faithful Globalizer：可以壓縮全域量詞，但不能產生證明

令所有 $\mathbb Q$ 上 elliptic curves 依某 canonical coding 枚舉為：

$$
E_1,E_2,\ldots
$$

定義 failure indicator：

$$
\varepsilon_i
=
\begin{cases}
0,&\mathrm{BSD}(E_i)\text{ true},\\
1,&\mathrm{BSD}(E_i)\text{ false}.
\end{cases}
$$

取正的 summable weights：

$$
\omega_i=2^{-i}.
$$

定義：

$$
\boxed{
\mathfrak B
=
\sum_{i=1}^{\infty}
2^{-i}\varepsilon_i.
}
$$

因每個 weight strictly positive：

$$
\boxed{
\mathfrak B=0
\iff
\forall i,\ \varepsilon_i=0
\iff
\mathrm{BSD\ holds\ for\ all}\ E/\mathbb Q.
}
$$

這是 exact faithful compression。

但它沒有證明：

$$
\mathfrak B=0.
$$

## 定理 7.1（Positive atomic faithfulness）

令 $D=\{x_i\}_{i\ge1}$ 為 countable domain，$E_k$ 為單調遞減 unresolved frontier：

$$
E_{k+1}\subseteq E_k.
$$

取 $\omega_i>0$ 且：

$$
\sum_i\omega_i<\infty.
$$

令：

$$
Q_k
=
\sum_{x_i\in E_k}\omega_i.
$$

則：

$$
\lim_{k\to\infty}Q_k
=
\sum_{x_i\in\cap_kE_k}\omega_i.
$$

因此：

$$
\boxed{
\lim_kQ_k=0
\iff
\bigcap_kE_k=\varnothing.
}
$$

### 證明

因 indicator

$$
1_{E_k}(x_i)
$$

對固定 $i$ 單調下降至：

$$
1_{\cap_kE_k}(x_i),
$$

且由 summable positive weights 控制，可逐項取極限：

$$
\lim_kQ_k
=
\sum_i
\omega_i
1_{\cap_kE_k}(x_i).
$$

由每個 $\omega_i>0$，右式為零若且唯若沒有 unresolved atom。$\square$

### 方法論裁決

此 theorem 給：

$$
\boxed{
\text{global logical faithfulness}.
}
$$

但不給：

$$
\boxed{
Q_k\to0.
}
$$

要讓 BSD 真的閉合，仍需額外的 arithmetic mechanism，例如某種 contraction、coercivity、descent 或 theorem-completeness result。

---

# 8. Dynamic theorem closure 不等於 truth closure

令 $\mathcal T$ 為一組 sound BSD inference rules。

給定已證曲線集合 $S_0$，定義：

$$
S_{n+1}
=
\Phi_{\mathcal T}(S_n),
$$

其中 $\Phi_{\mathcal T}$ 加入所有可由 $\mathcal T$ 從 $S_n$ 合法推出 BSD 的 curves / families。

定義：

$$
S_\infty
=
\bigcup_{n\ge0}S_n.
$$

由 soundness：

$$
\boxed{
S_\infty
\subseteq
\{E/\mathbb Q:\mathrm{BSD}(E)\}.
}
$$

但要得到：

$$
S_\infty
=
\{E/\mathbb Q\},
$$

需要的是 theorem-system completeness，而不是 soundness。

所以：

$$
\boxed{
\text{dynamic fixed point}
\neq
\text{automatic global theorem}.
}
$$

此框架真正有用之處是把問題改寫為：

> 缺的是哪一個 closure-generating rule？

本文的答案是：目前最像 irreducible global frontier 的，是 arbitrary-rank analytic-to-integral arithmetic bridge。

---

# 9. Grid / continuum route 的 multiplicity no-go

舊有格點化思路可能試圖：

$$
L_a(E,s)\to L(E,s)
$$

並進一步聲稱：

$$
\operatorname{ord}_{s=1}L_a(E,s)
\to
\operatorname{ord}_{s=1}L(E,s).
$$

這一步一般不成立。

## 引理 9.1（Order of vanishing is not continuous under ordinary function convergence）

令：

$$
f_a(z)=z^2+az=z(z+a).
$$

當：

$$
a\ne0,
$$

在 $z=0$：

$$
\operatorname{ord}_{z=0}f_a=1.
$$

但：

$$
f_0(z)=z^2,
$$

故：

$$
\operatorname{ord}_{z=0}f_0=2.
$$

同時在任意 compact set：

$$
f_a\to f_0
$$

uniformly as $a\to0$。

所以：

$$
\boxed{
f_a\to f
\not\Rightarrow
\operatorname{ord}_{0}f_a
\to
\operatorname{ord}_{0}f.
}
$$

$\square$

## 推論 9.2

任何 grid-BSD proof 若要從：

$$
L_a(E,s)\to L(E,s)
$$

推出 analytic rank stabilization，必須另證足以控制 zero multiplicity 的 theorem，例如：

- derivative-level nondegeneracy；
- zero-separation；
- local factorization stability；
- Rouché-type multiplicity control；
- 或其他 explicit multiplicity stabilization mechanism。

普通「連續性」不夠。

類似地，若定義某種 grid rank：

$$
\operatorname{rank}_a(E),
$$

也必須另證：

$$
\operatorname{rank}_a(E)
\to
\operatorname{rank}E(\mathbb Q)
$$

的 arithmetic stabilization theorem。

因此舊 grid route 的 gap 不是 computation precision，而是 missing stabilization theorem。

---

# 10. Higher-rank literature 的正確解讀

higher-rank Euler/Kolyvagin/Stark systems 已建立強力的 algebraic machinery。當合適的 higher-rank Euler system 存在時，可以控制 Selmer modules。

另一方面，higher Gross–Zagier / bipartite Euler-system work 可在不預設 low analytic rank 的情況下提供 arbitrary-rank Selmer structure information，並把若干 Kolyvagin-system nontriviality 與 localized main conjecture 連結。

但這些結果不能被改寫為：

$$
\forall E/\mathbb Q,\quad
r_{\mathrm{an}}(E)\ge2
\Rightarrow
r_{\mathrm{alg}}(E)=r_{\mathrm{an}}(E).
$$

更不能自動得到：

$$
\#\Sha(E/\mathbb Q)<\infty
$$

以及完整 leading coefficient identity。

這說明目前缺的不是「完全沒有 higher-rank language」。

相反地，缺的是：

$$
\boxed{
\text{rank-uniform canonical class}
+
\text{analytic leading-term comparison}
+
\text{integral global primitivity}.
}
$$

---

# 11. BSD determinant-line interface

為避免把不同文獻中的 determinant/fundamental-line normalization 偷偷視為完全相同，本文使用一個**抽象 interface**。

對每條 elliptic curve $E/\mathbb Q$，設：

$$
\Delta_{\mathrm{BSD}}(E)
$$

為一個 rank-one arithmetic fundamental line interface。

它應具有：

### Archimedean realization

$$
\operatorname{per}_\infty:
\Delta_{\mathrm{BSD}}(E)\otimes\mathbb R
\longrightarrow
\mathbb R,
$$

其 evaluation 能與：

$$
\Omega_E,
\qquad
\operatorname{Reg}(E),
\qquad
\frac{L^{(r)}(E,1)}{r!}
$$

相容。

### $p$-adic realization

對每個 prime $p$：

$$
\operatorname{loc}_p:
\Delta_{\mathrm{BSD}}(E)\otimes\mathbb Q_p
\longrightarrow
\Delta_p(E),
$$

其中 integral lattice 應能記錄：

- $p$-primary Selmer defect；
- $\Sha[p^\infty]$；
- Tamagawa contribution；
- torsion contribution；
- 必要 local-condition normalization。

本文不宣稱此 abstract interface 是新構造。其目的只是把 Bloch–Kato / Tamagawa-number / Iwasawa fundamental-line philosophy轉成一個明確 proof API。

---

# 12. Rank-Uniform Global Zeta-Primitivity Bridge

## 定義 12.1（RUGZPB package）

稱 $E/\mathbb Q$ 滿足 rank-$r$ 的 **Rank-Uniform Global Zeta-Primitivity Bridge**，若存在 canonical derived zeta object：

$$
\mathfrak z_E^{(r)}
\in
\Delta_{\mathrm{BSD}}(E)\otimes\mathbb Q
$$

以及與其相容的 derived Selmer/Mordell–Weil object，使下列條件同時成立。

### R1 — Exact analytic order

$$
r
=
\operatorname{ord}_{s=1}L(E,s).
$$

且 $\mathfrak z_E^{(r)}$ 是與此 exact order 相對應的 first nonzero derived zeta object。

亦即：

$$
\mathfrak z_E^{(j)}=0
\quad (j<r),
$$

而：

$$
\mathfrak z_E^{(r)}\ne0.
$$

這裡 $\mathfrak z_E^{(j)}$ 的具體定義必須由未來選定的 zeta/Iwasawa/derived framework 給出，不能只用 formal symbol 冒充構造。

### R2 — Mordell–Weil exterior compatibility

存在 comparison：

$$
\mathfrak z_E^{(r)}
\longmapsto
\mathbf P_E^{(r)}
$$

其中：

$$
\mathbf P_E^{(r)}
\in
\bigwedge^r
\left(
E(\mathbb Q)/E(\mathbb Q)_{\mathrm{tors}}
\right)
\otimes\mathbb Q
$$

非零，且此 comparison 足以證：

$$
\boxed{
r_{\mathrm{alg}}(E)=r.
}
$$

這是 bridge 中不可刪掉的一步。只構造某個 rank-$r$ exterior class 而不排除更高 algebraic rank，不足以證 weak BSD。

### R3 — Regulator compatibility

在 archimedean height pairing 下：

$$
\mathbf P_E^{(r)}
$$

的 determinant 正確給出：

$$
\operatorname{Reg}(E/\mathbb Q)
$$

相對於 canonical Mordell–Weil lattice 的 index。

### R4 — Integral Selmer determinant compatibility

對每個 prime $p$，$\mathfrak z_E^{(r)}$ 的 localization：

$$
\mathfrak z_{E,p}^{(r)}
$$

落入 canonical integral arithmetic determinant lattice，且其 generator/index relation exactly 對應 $p$-primary Selmer complex。

這裡的「primitivity」不是：

$$
\#\Sha=1.
$$

而是：

> zeta object 在正確的 arithmetic determinant lattice 中生成 BSD/ETNC 所預測的 integral line。

因此非平凡 $\Sha$、Tamagawa factors 與 torsion 可以作為 lattice/index data 出現。

### R5 — $\Sha$ finiteness recovery

R4 必須足夠推出：

$$
\Sha(E/\mathbb Q)[p^\infty]
$$

對每個 $p$ 都 finite，並且除有限 primes 外 trivial 或由 global finite arithmetic object 控制，使：

$$
\boxed{
\#\Sha(E/\mathbb Q)<\infty.
}
$$

不能只得到「每個固定 $p$-primary piece 在某條件下有限」而缺乏 global finiteness。

### R6 — Local factor recovery

對每個 prime $p$，integral index equality 必須 recover：

$$
v_p
\left(
\frac{
\#\Sha(E/\mathbb Q)\prod_\ell c_\ell
}{
\#E(\mathbb Q)_{\mathrm{tors}}^2
}
\right),
$$

相對於所選 normalization。

### R7 — Archimedean leading-term comparison

$$
\boxed{
\operatorname{per}_\infty
\left(
\mathfrak z_E^{(r)}
\right)
=
\frac{L^{(r)}(E,1)}{r!}
}
$$

並在同一 comparison 中 recover：

$$
\Omega_E\operatorname{Reg}(E/\mathbb Q).
$$

### R8 — Rank uniformity

R1–R7 的 construction 與 theorem 對：

$$
r=0,1,2,\ldots
$$

使用同一套可兼容 architecture，不能在 $r\ge2$ 時把關鍵部分重新標為 conjectural input。

---

# 13. Conditional Global Reduction Theorem

## 定理 13.1（RUGZPB $\Rightarrow$ full BSD）

假設對每條：

$$
E/\mathbb Q
$$

令：

$$
r=
\operatorname{ord}_{s=1}L(E,s).
$$

若 $E$ 滿足 RUGZPB package R1–R8，則：

1. $r_{\mathrm{alg}}(E)=r_{\mathrm{an}}(E)$；
2. $\Sha(E/\mathbb Q)$ finite；
3. strong BSD leading coefficient formula 成立。

因此：

$$
\boxed{
\forall E/\mathbb Q,\ \mathrm{RUGZPB}(E)
\Longrightarrow
\mathrm{BSD}.
}
$$

### 證明

由 R1：

$$
r=r_{\mathrm{an}}(E).
$$

由 R2：

$$
r_{\mathrm{alg}}(E)=r.
$$

故：

$$
\boxed{
r_{\mathrm{alg}}(E)=r_{\mathrm{an}}(E).
}
$$

得到 BSD-W。

由 R4–R5，對每個 $p$ 的 Selmer determinant defect 被 canonical integral zeta generator 控制，並由 R5 的 global finiteness clause 得：

$$
\boxed{
\#\Sha(E/\mathbb Q)<\infty.
}
$$

得到 BSD-F。

R3 給 regulator compatibility；R6 對每個 prime 給 strong-BSD arithmetic quotient 的 $p$-adic valuation；R7 給 archimedean leading-term normalization。

因此所有 finite-prime valuations 與 real period/regulator normalization 共同固定：

$$
\frac{L^{(r)}(E,1)}{r!}
$$

相對於：

$$
\frac{
\#\Sha(E/\mathbb Q)\,
\Omega_E\,
\operatorname{Reg}(E/\mathbb Q)\,
\prod_p c_p
}{
\#E(\mathbb Q)_{\mathrm{tors}}^2
}.
$$

故 strong BSD leading coefficient identity 成立。$\square$

---

# 14. 此定理到底獲得了什麼？

定理 13.1 不能被宣稱為 BSD proof，因為 RUGZPB 本身尚未建立。

它真正做的是：

$$
\boxed{
\text{散落的 global BSD obligations}
\longrightarrow
\text{一個 typed rank-uniform theorem interface}.
}
$$

原本的 open obligations 看起來是：

- rank equality；
- all primes；
- $\Sha$；
- regulator；
- leading term；
- local factors；
- low/high rank；
- Selmer structure；
- zeta elements；
- integral comparison。

壓縮後變成：

$$
\boxed{
\text{construct and prove a rank-uniform integral derived zeta generator theorem}.
}
$$

這是 reduction，不是 solution。

---

# 15. 為什麼稱為「primitivity」而不是「再寫一次 BSD」？

如果 RUGZPB 只定義為：

> 「存在一個 object，使 BSD 成立」，

那只是 tautology。

因此 future work 必須要求 $\mathfrak z_E^{(r)}$ 具有**獨立可構造性**：

1. 由 Galois/Iwasawa/Euler-system machinery 構造；
2. 不把未知 $\#\Sha$ 當 construction input；
3. 不把 BSD leading coefficient identity 當 definition；
4. 可在 local $p$-adic realizations 中獨立驗證；
5. 可與已知 $r=0,1$ zeta elements specialization 比對；
6. 可在 $r=2$ concrete curves 上輸出非循環 certificate。

真正的 proof target 應是：

$$
\boxed{
\text{independently constructed zeta object}
\Rightarrow
\text{integral generator property}.
}
$$

而不是：

$$
\boxed{
\text{BSD formula}
\Rightarrow
\text{define a zeta object satisfying BSD}.
}
$$

---

# 16. 與 Bloch–Kato / ETNC 的關係

本文的方向明顯接近：

- Bloch–Kato Tamagawa number conjecture；
- equivariant Tamagawa number conjecture；
- Kato zeta elements；
- fundamental/determinant lines；
- higher-rank Euler/Kolyvagin/Stark systems；
- derived Gross–Zagier / Heegner structures。

因此 RUGZPB 不應宣稱是完全獨立的新宇宙。

其研究價值在於：

$$
\boxed{
\text{把「解 BSD」需要的高秩接口壓成工程化、可審計的 theorem schema}.
}
$$

若最終證明 RUGZPB 與某個既有 ETNC specialization 等價，這仍然是有價值的結果：它表示 BSD 的 irreducible frontier 被精確定位到該 specialization。

若 RUGZPB 比 full ETNC 更弱，則更有價值：可能得到一條只針對 elliptic-curve BSD 所需資料的 minimal theorem target。

這正是下一階段必須判定的問題。

---

# 17. Representation-level escape from explicit $\forall p$

rank-$0$ family work 顯示：

$$
\forall p
$$

有時可壓成 finite exception routing。

高秩版本可能還有另一種更強壓縮：

若存在單一 global integral determinant generator：

$$
\mathfrak z_E^{(r)}
\in
\Delta_{\mathrm{BSD}}(E),
$$

則其 integral primitivity 是一個 global representation-level statement。

理想情況：

$$
\boxed{
\text{global integral generator}
\Rightarrow
\text{all }p\text{-local generator statements}.
}
$$

此時：

$$
\forall p
$$

不再是主證明的 explicit outer loop，而是 global integrality 的 local shadows。

這是本文提出 RUGZPB 的核心結構動機。

但反向方向需要非常小心：

$$
\forall p\ \mathrm{local\ compatibility}
$$

不一定自動給 canonical global generator，除非另有 adelic/determinant gluing theorem。

因此未來必須分開：

- local primitivity；
- global integrality；
- local-to-global gluing；
- canonical normalization。

---

# 18. 最小 rank-$2$ 實驗

下一階段不應直接處理「所有 rank」。

應先在：

$$
E=389.a1
$$

或其他 arithmetic data 清楚的 rank-$2$ curve 上建立：

$$
\boxed{
\text{Rank-2 Zeta-Primitivity Certificate Prototype}.
}
$$

最低輸出：

### Z2-1 Rigorous analytic-rank certificate

證：

$$
\operatorname{ord}_{s=1}L(E,s)=2.
$$

### Z2-2 Mordell–Weil exterior certificate

給 generators：

$$
P_1,P_2\in E(\mathbb Q),
$$

並證：

$$
P_1\wedge P_2
\ne0
$$

且 rank upper bound 為 $2$。

### Z2-3 Regulator certificate

exact / rigorously bounded height-pairing determinant：

$$
\operatorname{Reg}(E)
=
\det
\left(
\langle P_i,P_j\rangle
\right)_{1\le i,j\le2}.
$$

### Z2-4 Selmer-complex certificate

對一個可管理的 prime $p$，建立：

$$
\Delta_p(E)
$$

與 derived class 的 integral index。

### Z2-5 Actual $\Sha[p^\infty]$ certificate

不得使用 BSD-inferred analytic $\Sha$。

需要 descent / Selmer / Euler-system theorem 輸出。

### Z2-6 Derived analytic comparison

把 rank-$2$ derived object 與：

$$
\frac{L^{(2)}(E,1)}{2!}
$$

建立非循環 comparison。

若 Z2-1 至 Z2-6 能對一條 curve 完成，就得到第一個真正的 high-rank bridge prototype。

---

# 19. 三條可能的 high-rank route

## Route A — Higher-rank Euler/Kolyvagin route

目標：

$$
\text{higher-rank Euler system}
\to
\text{higher Kolyvagin derivative}
\to
\text{Selmer determinant control}.
$$

優點：integral arithmetic 強。

缺口：需要 canonical arithmetic classes 與 analytic leading term comparison。

## Route B — Derived Gross–Zagier / Heegner route

目標：

$$
L^{(r)}(E,1)
\leftrightarrow
\text{derived geometric/Heegner data}
\leftrightarrow
\operatorname{Reg}.
$$

優點：analytic–geometric bridge 直觀。

缺口：arbitrary rank、sign、auxiliary quadratic field dependence、integrality、$\Sha$。

## Route C — ETNC / determinant-line route

目標：

$$
\boxed{
\text{zeta element generates the canonical fundamental line}.
}
$$

優點：最接近一次收納：

- special value；
- regulator；
- torsion；
- Tamagawa；
- Selmer；
- $\Sha$。

缺點：theorem target 可能幾乎與高秩 ETNC 本身同等困難。

因此本文不先選單一路線。

RUGZPB 是三條路線的共同 target interface。

---

# 20. 最重要的 no-go：不能把 target 當 assumption 後宣布完成

未來任何 manuscript 若包含：

> Assume the rank-uniform zeta-primitivity bridge.

接著推出 BSD，最多只能叫：

$$
\boxed{
\text{conditional reduction theorem}.
}
$$

要升格為 BSD proof，必須：

$$
\boxed{
\text{RUGZPB itself is proved from accepted inputs}.
}
$$

且其 proof 不得：

- 暗用 BSD；
- 暗用 full Bloch–Kato；
- 暗用 equivalent unproved ETNC；
- 用 numerical equality 代替 integral theorem；
- 用 positive-density family 代替 $\forall E$；
- 用 finite prime census 代替 global integrality。

---

# 21. 與「計算問題」的關係

計算在此研究中非常重要，但必須定位精確。

計算適合：

1. theorem-hypothesis compiler；
2. finite exceptional-prime enumeration；
3. Galois-image verification；
4. descent / Selmer certificates；
5. regulator / height verification；
6. local reduction/Tamagawa checks；
7. counterexample search；
8. rank-$2$ prototype audit。

但 full BSD 的高秩 frontier 目前不是：

$$
\boxed{
\text{只差把現有算法跑久一點}.
}
$$

更準確是：

$$
\boxed{
\text{需要一個目前尚未完成的 rank-uniform theorem，
其證明可能大量依賴計算，但不能由有限計算本身替代}.
}
$$

因此「計算 bottleneck」與「theorem bottleneck」必須分開記錄。

---

# 22. 目前最強 reduction map

截至本文版本，BSD 研究主圖可寫成：

$$
\boxed{
\begin{array}{c}
\text{rank }0/1\\
\text{Gross--Zagier/Kolyvagin}\\
\text{Iwasawa/zeta-element}\\
p\text{-part BSD}
\end{array}
}
$$

$$
\Downarrow
$$

$$
\boxed{
\begin{array}{c}
\text{algorithmic theorem router}\\
\text{Banwait--Huang}
\end{array}
}
$$

$$
\Downarrow
$$

$$
\boxed{
\begin{array}{c}
\text{non-semistable rank-0 extension}\\
\text{generic primes + finite exceptions}
\end{array}
}
$$

此分支已證明：

$$
\boxed{
\forall p\text{ can sometimes be finite-ized}.
}
$$

但 full BSD 的另一分支為：

$$
\boxed{
\begin{array}{c}
r\ge2\\
\text{analytic leading term}\\
\Updownarrow\ ?\\
\text{MW exterior class / regulator}\\
\Updownarrow\ ?\\
\text{integral Selmer determinant}\\
\Updownarrow\ ?\\
\Sha\text{ finiteness / exact index}
\end{array}
}
$$

因此目前最小全域 target：

$$
\boxed{
\textbf{Rank-Uniform Global Zeta-Primitivity Bridge}.
}
$$

---

# 23. Formal status table

| Component | Status | Meaning |
|---|---|---|
| BSD statement decomposition | PROVED / DEFINITIONAL | W/F/S 不可偷換 |
| positive atomic globalizer | PROVED | global quantifier faithful compression |
| globalizer decay $\mathfrak B=0$ | OPEN | 需要 arithmetic mechanism |
| grid convergence $\Rightarrow$ multiplicity stabilization | FALSE IN GENERAL | 有明確反例 |
| rank-$0/1$ zeta/Iwasawa BSD components | EXTERNAL THEOREM | 依各 theorem hypotheses |
| Banwait–Huang algorithmic family identification | EXTERNAL THEOREM / COMPUTATION | conductor $\le500000$ domain |
| internal Phase 1 reproduction | INTERNALLY CLOSED | independent reproduction/audit |
| non-semistable finite-exception router | DERIVED / RESEARCH RESULT | 仍需 publication/referee audit |
| explicit 696.e1 family | DERIVED THEOREM-STYLE CONSEQUENCE | 不先宣稱 priority |
| arbitrary-rank weak BSD | OPEN | general closure absent |
| arbitrary-rank $\Sha$ finiteness | OPEN | general closure absent |
| RUGZPB package | CANDIDATE THEOREM TARGET | 本文定義 |
| RUGZPB $\Rightarrow$ BSD | PROVED CONDITIONAL REDUCTION | 本文定理 13.1 |
| RUGZPB itself | OPEN | 下一主戰場 |

---

# 24. Next Proof Obligations

此節供下一個 BSD 專門對話直接接手。

## P1 — Minimality audit

回答：

> RUGZPB 中 R1–R8 哪些其實是重複的？哪些可由其他條件推出？

目標是把 package 壓成 minimal independent axioms。

## P2 — ETNC equivalence audit

精確比較：

$$
\mathrm{RUGZPB}(E)
$$

與 elliptic curve motive 的：

- Bloch–Kato Tamagawa number conjecture；
- Kato zeta isomorphism；
- ETNC specialization；
- leading-term formulation。

需要輸出：

$$
\boxed{
\text{equivalent / stronger / weaker / incomparable}
}
$$

而不是只說「很像」。

## P3 — Rank-$2$ derived object choice

至少比較：

1. higher Kato / Euler-system candidate；
2. derived Heegner/Gross–Zagier candidate；
3. determinant-line zeta candidate。

選一個可以在 $389.a1$ 上真正產生 certificate 的 route。

## P4 — One-prime rank-$2$ closure

先不要全 $p$。

固定一個 favorable odd prime：

$$
p
$$

完成：

$$
\boxed{
\text{rank-2 derived class}
\to
\text{integral Selmer index}
\to
\Sha[p^\infty]\text{ control}.
}
$$

若單 prime 都不能閉合，就先找 exact theorem obstruction。

## P5 — Analytic-to-regulator comparison

找現有最高 rank 的 unconditional / conditional derived Gross–Zagier-type result，判定能否提供：

$$
\frac{L^{(2)}(E,1)}{2!}
\longleftrightarrow
\det(\text{height pairing}).
$$

若不能，精確標出缺的是：

- class existence；
- nonvanishing；
- height formula；
- integrality；
- field descent；
- rank exactness。

## P6 — Global primitivity vs all-$p$ gluing

研究：

$$
\left[
\forall p,\ 
\mathfrak z_{E,p}^{(r)}\text{ locally primitive}
\right]
$$

是否在指定 determinant-line category 中推出：

$$
\mathfrak z_E^{(r)}
\text{ globally primitive}.
$$

這可能是把 explicit $\forall p$ 再次 representation-escape 的關鍵。

## P7 — Rank-$2$ wall atlas

建立至少 $10$ 條 rank-$2$ curves：

- different conductors；
- ordinary/supersingular favorable primes；
- different Tamagawa profiles；
- trivial/nontrivial predicted Sha；

測試 RUGZPB 的 obligations 是否真的是共同 frontier，而非 $389.a1$ 偶然。

---

# 25. Stop rules

下列任一情況發生時，必須停止並標為 no-go/reduction，而不是硬湊證明。

### Stop-1

發現 RUGZPB 與 full BSD 完全等價且沒有提供可獨立構造的 stronger interface。

則本文的價值降為：

$$
\text{formal repackaging}.
$$

### Stop-2

rank-$2$ candidate zeta object 的存在本身需要假設 BSD / Bloch–Kato。

則該 route circular。

### Stop-3

local primitivity 不能 glue globally，且沒有額外 theorem。

則 representation-level $\forall p$ escape 失敗。

### Stop-4

analytic leading-term comparison只在 rank $0/1$ 已知。

則不得把「higher-rank Euler system存在」寫成 BSD 高秩 bridge已閉合。

### Stop-5

數值 $389.a1$ identity 與 theorem input混淆。

則 certificate 降級，不允許使用 analytic Sha prediction 作 actual Sha。

---

# 26. 結論

近年的 BSD 進展顯示兩種完全不同但互補的壓縮。

第一種是 **prime quantifier compression**：

$$
\boxed{
\forall p
\longrightarrow
\text{generic theorem}
+
\text{finite exceptional certificates}.
}
$$

它已在 rank-$0$ quadratic-twist family 的 theorem routing 中展現實質效果。

第二種是本文提出要攻的 **rank-uniform structural compression**：

$$
\boxed{
\begin{array}{c}
\text{analytic order}\\
\text{leading term}\\
\text{MW rank}\\
\text{regulator}\\
\text{Selmer}\\
\Sha\\
\text{Tamagawa}\\
\text{torsion}\\
\forall p
\end{array}
\quad
\longrightarrow
\quad
\text{one integral derived zeta-primitivity theorem}.
}
$$

目前第一種已有大量 theorem 支撐；第二種仍 open。

因此本文的最終裁決不是：

$$
\boxed{\mathrm{BSD\ solved}.}
$$

而是：

$$
\boxed{
\text{BSD 的當前高秩全域前線，
可被壓縮為 rank-uniform analytic-to-integral zeta-primitivity bridge。}
}
$$

若未來能從 accepted arithmetic inputs 證明該 bridge，則本文定理 13.1 立即把它編譯成 full BSD。

反之，若該 bridge 被證明等價於更強的未解 ETNC/Bloch–Kato specialization，則這也構成一個正式 no-go frontier：BSD 的難度並沒有消失，只是被精確定位。

這就是下一輪應該真正死扣的位置。

---

# References

1. A. A. Burungale, C. Skinner, Y. Tian, X. Wan, **Zeta elements for elliptic curves and applications**, arXiv:2409.01350, 2024.
2. B. S. Banwait, X. Huang, **On the Identification of Elliptic Curves That Admit Infinitely Many Twists Satisfying the Birch–Swinnerton-Dyer Conjecture**, arXiv:2601.16044v3, 2026; accepted at ANTS XVII.
3. O. Fouquet, X. Wan, **The Iwasawa Main Conjecture for universal families of modular motives**, arXiv:2107.13726.
4. K. Kato, **Tamagawa number conjecture for zeta values**, arXiv:math/0304233.
5. D. Burns, R. Sakamoto, T. Sano, **On the theory of higher rank Euler, Kolyvagin and Stark systems, II**, arXiv:1805.08448.
6. C.-H. Kim, **A higher Gross-Zagier formula and the structure of Selmer groups**, arXiv:2203.12161.
7. O. Fouquet, **The Equivariant Tamagawa Number Conjectures for modular motives with coefficients in Hecke algebra**, arXiv:2501.07105, 2025.
8. Clay Mathematics Institute, **The Birch and Swinnerton-Dyer Conjecture and Related Problems: Recent Results**, CRC Workshop, Oxford, 21–25 September 2026.

---

# Internal project dependencies

The following internal artifacts should be carried into the next research conversation:

- `00_BSD_Global_Enclosure_Consensus.md`
- `01_BSD_Statement_and_Quantifier_Audit.md`
- `02_Known_Theorem_Closure_Map.md`
- `03_BSD_Certificate_Ladder.md`
- `07_BSD_Certificate_Globalizer.md`
- `16_Phase1_Closure_and_Phase2_Interface.md`
- `00_Phase2_Global_Enclosure_Consensus.md`
- `02_Fouquet_Wan_Hypothesis_Compiler.md`
- `17_696e1_All_Prime_Router.md`
- `paper(7).md`
- `paper(8).md`
- `paper(9).md`
- `28_Submission_Gate.md`
- `389a1_rank2.json`

Suggested next-chat launch line:

> Read this paper as the current BSD theorem/reduction state. Do not re-run rank-0 family reproduction. Start from P1–P7, with priority on P2 (ETNC equivalence/minimality audit) and P4 (one-prime rank-2 closure), keeping theorem / external input / heuristic / no-go strictly separated.

