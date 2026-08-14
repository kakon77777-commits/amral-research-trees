# 05｜Neo.K 舊「格點秩收斂」路線審計

## 0. 舊稿內容

內部舊稿曾提出：

1. 格點化橢圓曲線；
2. 計算格點 $L$-函數；
3. 定義格點秩；
4. 定義格點零點階數；
5. 主張某種格點 BSD 關係；
6. 取：
   $$
   a\to0;
   $$
7. 以「連續性保證等式成立」。

這條線目前不能進主證明。

---

# 1. 第一個循環：格點 BSD 關係

如果每個尺度已假設：

$$
\operatorname{rank}_a(E)
\le
\operatorname{ord}_{s=1}L_a(E,s),
$$

甚至最終要求極限 equality，那麼必須說明該 inequality從何而來。

若其證明已使用 classical BSD 型連結，則是循環。

---

# 2. Rank 不是普通連續量

$$
\operatorname{rank}E(\mathbb Q)
$$

是整數值、全域算術不變量。

數值格點上的「近似點數」「矩陣秩」「離散同調 rank」不會因：

$$
a\to0
$$

自動收斂成 Mordell–Weil rank。

必須建立：

$$
\boxed{
\text{grid certificate}
\Longleftrightarrow
\text{rational-point independence / Selmer bound}.
}
$$

---

# 3. 零點階數也不由普通函數收斂保存

即使：

$$
L_a(E,s)\to L(E,s)
$$

在某區域收斂，也不自動推出：

$$
\operatorname{ord}_{s=1}L_a(E,s)
\to
\operatorname{ord}_{s=1}L(E,s).
$$

消失階對微小 perturbation 非連續。

需要至少：

- 在 $s=1$ 鄰域的解析控制；
- 導數 uniform convergence；
- lower derivatives exact vanishing；
- 首個非零導數與 error margin；
- 沒有 spurious grid zeros。

---

# 4. 「兩邊都收斂」不推出「極限相等」

由：

$$
A_a\to A
$$

與：

$$
B_a\to B
$$

不能推出：

$$
A=B.
$$

除非每個 $a$ 有合法關係：

$$
A_a=B_a
$$

並且所有極限與定義相容。

但若 $A_a=B_a$ 正是格點 BSD，難題已被搬入格點層。

---

# 5. 如果要挽救，需要四個獨立定理

## GR-1：Faithful discretisation

格點對象必須保留：

- rational points；
- group law；
- torsion；
- height；
- local reduction。

## GR-2：Rank certificate equivalence

格點 rank 必須等價於：

$$
\operatorname{rank}E(\mathbb Q),
$$

而不是視覺／數值 rank。

## GR-3：Analytic-order stability

格點 $L$-函數的 zero order必須被 rigorous analytic certificate保存。

## GR-4：Non-circular bridge

GR-2 與 GR-3 之間的 equality不能預設 BSD。

目前四項皆未完成。

---

# 6. 裁決

$$
\boxed{
\text{Archive as exploratory analogy;}
\quad
\text{do not use as Phase 1 proof route.}
}
$$

可以保留的只有工程思想：

- 多尺度檢查；
- representation consistency；
- exact certificate；
- limit audit。

不能保留「連續性保證 BSD equality」的 theorem claim。
