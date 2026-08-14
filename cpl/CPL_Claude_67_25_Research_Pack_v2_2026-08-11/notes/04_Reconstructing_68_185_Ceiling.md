# 04 — 重建 Bandwidth-One 的 $68.185\%$ Ceiling
## 從一句 Remark 到對抗性配置律、LP 對偶與資訊不可辨識性

**狀態：** 第一輪結構重建  
**日期：** 2026-08-11  
**目標：** 找出 Claude 論文中 bandwidth-one configuration-wise certificate ceiling 的實際數學機制，並定位通往 $70\%$ 必須突破的假設。

---

## 1. 這個 ceiling 不是只存在於論文敘述

Anthropic 官方 Lean companion repository 的 `Zeta23/PairCeiling/` 專門形式化這個 optimality remark。公開 README 明確說：它包含 stability inequality，以及一個 explicit $N=256$ periodic law；對適當 bandwidth-one certificate，這個 law 給出

$$
v\le 0.6818287+2.55\times10^{-6}\left(|r'(1)|+\int_0^1|r''(x)|\,dx\right).
$$

`LawN256.lean` 更記錄了 exact-rational simple-point fraction：

$$
p_0=\frac{10909258999421303588095230195816054408197}{16000000000000000000000000000000000000000}=0.681828687463832\ldots,
$$

即

$$
\boxed{68.182868746383\%}.
$$

這已非常接近論文 Remark 1.1 使用的 $0.68185$。

---

## 2. Certificate 的觀測域

令 configuration 在 grid $j/N$ 上的 form-factor masses 為

$$
s_j=\frac{S(j)}{N},\qquad j=1,\dots,N.
$$

定義

$$
C(x)=\sum_{j/N\le x}s_j,
$$

$$
D(x)=C(x)-\frac{x^2}{2},
$$

$$
E(x)=\int_0^xD(t)\,dt.
$$

certificate $(c_0,r)$ 對一個 simple-point fraction 為 $p$ 的 configuration 有效，若

$$
c_0+\sum_{j=1}^Ns_jr(j/N)\le p.
$$

而它對理想 bandwidth-one CUE datum 的值為

$$
v(c_0,r)=c_0+\int_0^1r(x)x\,dx.
$$

所以真正的問題是：**只知道 bandwidth-one form-factor rows 時，$v$ 能被 configuration-wise validity 推到多高？**

---

## 3. Stability identity

`Stability.lean` 的核心是 Abel summation 加兩次 integration by parts：

$$
\sum_js_jr(j/N)-\int_0^1r(x)x\,dx
=
r(1)D(1)-r'(1)E(1)+\int_0^1r''(x)E(x)\,dx.
$$

因此

$$
\left|\sum_js_jr(j/N)-\int_0^1r(x)x\,dx\right|
\le
|r(1)||D(1)|+|r'(1)||E(1)|+\sup|E|\int_0^1|r''|.
$$

這就是把「離散近 CUE rows」提升到「連續 certificate value」的 QCI bridge。

---

## 4. Near-CUE law

若

$$
|NS(j)-j|\le\tau\qquad(0<j<N),
$$

`NearCUE.lean` 證明

$$
\boxed{\sup_{x\in[0,1]}|E(x)|\le\frac1{6N^2}+\frac{\tau}{2N}}.
$$

對官方 law：

$$
N=256,\qquad \tau=3\times10^{-40},
$$

故

$$
\epsilon_{256}=2.543131510416667e-06\ldots<2.5431316\times10^{-6}.
$$

---

## 5. Signed ceiling

若

$$
r(1)\ge0,\qquad D(1)\ge0,
$$

則 signed integration-by-parts 版本中 edge term 對上界有利，可以刪除。於是

$$
\boxed{
v\le p_0+2.5431316\times10^{-6}\left(|r'(1)|+\int_0^1|r''(x)|\,dx\right).
}
$$

這是目前公開 Lean repo 中可直接讀到的 finite-$N$ obstruction。

論文的 $0.68185$ 與 exact law 的差為

$$
0.68185-p_0=2.13125361684385e-05.
$$

若 roughness

$$
R(r)=|r'(1)|+\int_0^1|r''(x)|\,dx
$$

約不超過

$$
R(r)\lesssim 8.380430,
$$

則這個 $N=256$ signed witness 已經把 certificate 壓到 $0.68185$ 附近。

**注意：** $p_0$ 是 explicit finite-$N$ law 的 exact fraction；$0.68185$ 是論文對較廣 certificate class 的 ceiling 表述。兩者不能偷換成同一個 exact theorem constant。

---

## 6. 對抗性 law 的本質

`LawN256.lean` 說這個 law 是 finitely-supported probability law over $256$-periodic marked configurations。

每個 configuration 有 rational positions

$$
x_{c,i}\in[0,256),
$$

marks

$$
m_{c,i}\in\{1,2\},
$$

且

$$
\sum_im_{c,i}=256.
$$

平均 form factor 為

$$
S(j)=\frac1{256}\sum_cw_c\left|\sum_im_{c,i}e^{2\pi ijx_{c,i}/256}\right|^2,
$$

其中

$$
w_c\ge0,\qquad\sum_cw_c=1.
$$

Lean source 稱它是「an exact-rational linear programme over 256-periodic marked configurations」的 optimal law。

因此它的直觀是：

> 構造一個平均 pair-correlation rows 幾乎完美模仿 CUE，但平均 simple-point fraction 只有約 $68.18\%$ 的世界。

只要 certificate 必須對每個 configuration 都有效，那它對這個 probability mixture 取平均後也必須有效。

於是：

$$
\boxed{
\text{bandwidth-one pair observables 幾乎相同}
\not\Rightarrow
\text{simple fraction}>68.2\%.
}
$$

這其實是一個 information-indistinguishability obstruction。

---

## 7. Primal / Dual 重建

從公開 source 可重建其概念型 primal：

$$
\min_{w_c}\sum_cw_cp_c
$$

subject to

$$
w_c\ge0,\qquad\sum_cw_c=1,
$$

以及

$$
\sum_cw_cS_c(j)\approx\frac{j}{N},\qquad j=1,\dots,N-1.
$$

最終 law 將 row error 壓到 $3\times10^{-40}$。

對偶側就是 certificate：用 observables $S(j)$ 的線性/函數泛函去 lower-bound $p_c$。

因此 ceiling 是一個典型 minimax / LP-duality 現象：

```text
Primal: 找低 simple fraction、但 bandwidth-one 看起來像 CUE 的 adversarial law。
Dual:   找只憑 bandwidth-one observables 就能證高 simple fraction 的 certificate。
```

primal law 一旦把 $p$ 壓在 $0.68183$，dual certificate 就不能無條件跳到 $0.70$。

---

## 8. 第一個缺失 artifact

官方 source 指定外部 certificate：

```text
cert_N256_blk_b128m.json
```

SHA-256：

```text
cc3de9917db4d14d844630a4e97dda8387fd6e257e52b6967f430b8914584eb8
```

README / Lean source 都說它「available from the authors」，但目前 public repo 並未包含該 JSON。

因此現在我們能重建：

- analytic stability；
- grid-to-continuum bridge；
- Near-CUE error；
- exact $p_0$；
- kernel-checked row enclosures；
- signed ceiling。

但暫時不能完整重跑：

$$
\text{configuration generation}\to\text{exact rational LP solve}\to\text{external JSON certificate}.
$$

---

## 9. 通往 $70\%$ 的 Escape Classes

因為

$$
\Delta_{70}=0.70-p_0\approx 0.018171312536,
$$

要越過 $70\%$，至少要破壞 ceiling 的某個假設：

### A. Support escape

增加 Fourier support，例如 Claude 論文估計

$$
1\to1.04.
$$

### B. Moment escape

加入 higher moments / higher correlations，例如 fourth-moment conditional route 可達

$$
\frac{13}{18}=72.22\ldots\%.
$$

### C. Structural escape

加入不被 pair form factor 捕捉的配置資訊。

### D. Certificate-class escape

放棄 configuration-by-configuration、只讀 bandwidth-one observables 的 certificate class。

### E. Zeta-specific realizability escape

證明這個 abstract extremal marked-configuration law 不可能由真正的 zeta zeros 實現。

最後這一條尤其重要：ceiling law 是 abstract admissible configuration law，不是「存在真實 zeta zeros 具有這個配置」的證明。

---

## 10. 新命題：Bandwidth-One Escape Problem（BOEP）

令 $\mathfrak C_1$ 為所有只依賴 bandwidth-one pair-correlation observables、且 configuration-wise valid 的 certificate class。尋找最小額外資訊 $\mathcal I$，使

$$
\sup_{C\in\mathfrak C_1+\mathcal I}\operatorname{Cert}(C)>0.68185.
$$

第一個實際門檻：

$$
\boxed{P_{70}:\operatorname{Cert}\ge0.70.}
$$

這將「比例主義」轉成一個真正可研究的問題：

$$
\boxed{
\text{需要加入哪一種最小新資訊，才能排除現在的 extremal law？}
}
$$

---

## 11. 下一步

1. 建 small-$N$ marked-configuration toy LP，重現 primal/dual obstruction。
2. 研究 $p_N$ 隨 $N$ 的下降與是否趨近約 $0.68185$。
3. 對比 support escape 與 moment escape 的「新增資訊成本」。
4. 尋找 zeta-specific realizability constraints，判斷 abstract law 是否受到額外算術／拓樸限制。
5. 若取得官方 JSON，完整重跑 $N=256$ exact-rational LP。
