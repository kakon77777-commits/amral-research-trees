# 03 — $67.25\%$ 與 $68.185\%$：兩個天花板的作用域

## 1. 為什麼必須拆開

目前最容易誤讀的是：

$$
67.25\%<68.185\%.
$$

不能因此說「Claude 的 window 再最佳化一點就能到 $68.185\%$」。

---

## 2. $67.25\%$ 的精確作用域

Claude §7.1 最佳化 window functional，得到 Montgomery--Taylor kernel。主論文接著引用 CCLM17 Corollary 14，說明在只使用 Montgomery $F(\alpha)$ 於 $[-1,1]$ 的 one-delta extremal problem 中，該 kernel 是 extremal。

論文自己的語句把此範圍概括為：

$$
\boxed{
\text{block structure + two traces + primes up to }T
}
$$

因此：

$$
0.672500\ldots
$$

是這個 **window-optimisation / two-trace 子框架**的極值。

---

## 3. $68.185\%$ 的精確已知程度

Remark 1.1 說：只用

- mean density；
- Fourier support $(-1,1)$ 的 pair-correlation data；
- multiplicity integrality；
- 並要求 certificate 對每個 configuration 都成立；

則一個 explicit extremal law 顯示，simple-zero certificate 不可超過：

$$
0.68185.
$$

這是比 §7.1 window class 更廣的 statement。

但是在目前讀到的主論文正文中，$0.68185$ 的完整 extremal-law 推導沒有像 $c_1^*$ 一樣被顯式展開成可直接重算的閉式公式。

因此本研究包將它標記為：

$$
\boxed{\text{OPEN-RECONSTRUCTION-01}}
$$

研究任務不是懷疑數字，而是：

> 找出該 extremal law 的完整定義、變數、constraints、optimizer 與數值重現路徑。

---

## 4. §7.5 提供的另一個 cap

Proposition 7.4 給出有限維 dimension cap：若 test functions support length 對應 $\lambda$，則

$$
\operatorname{rank}P\le d\approx\lambda N.
$$

所以任何同型 finite compression 都不能 certify 超過約 $\lambda N$ 個 on-line points。

同時，只靠 first/second trace 的 certificate 在 $\lambda\le1/2$ 時甚至非正；而在 $1/2<\lambda<1$，無條件可得的 higher moments 又受 Rudnick--Sarnak range

$$
k\lambda<2
$$

限制，無法提供新的 even-moment gain。

這說明「只要一直算更多 moment」在無條件 bandwidth-one 區域也不是免費的。

---

## 5. 對 $P_{70}$ 的實際含義

目前可確認：

$$
P_{70}
$$

已在：

$$
70\%>68.185\%
$$

之外。

所以若 Remark 1.1 的 certificate class 假設完全適用，$P_{70}$ 必須至少破壞其中一個限制：

$$
\boxed{
\text{more support}
\ \lor\ 
\text{more correlation information}
\ \lor\ 
\text{richer non-configuration-wise/global structure}
}
$$

條件式 fourth-moment route正是第二類；support $>1$ route 是第一類。

---

## 6. 下一步

1. 追 bibliography / supplementary / Lean audit 是否包含 Remark 1.1 的 extremal-law formal statement；
2. 搜尋作者／Anthropic 是否另公開 numerical notebook；
3. 若無，從 bandwidth-one pair-correlation + integrality constraints 自己建立 configuration LP / moment problem，嘗試數值重現 $0.68185$；
4. 若能重現，再正式研究其 dual certificate 與 escape directions。
