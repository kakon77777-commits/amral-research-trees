# 07｜BSD Certificate Globalizer

## 0. 目的

建立一個不會因為「大多數曲線已認證」就吞掉單一未認證曲線的研究控制量。

注意：它忠實於**認證狀態**，不是直接忠實於 BSD 真值。

---

# 1. Canonical enumeration

以 conductor、isogeny label 等建立：

$$
\mathcal E
=
\{E_1,E_2,\ldots\}
$$

的一個可計算枚舉。

每個 $E_i$ 代表一個 $\mathbb Q$-isogeny class。

---

# 2. Certificate target

固定目標層：

$$
\ell_\star\in\{C6,C7,C8,C9,C10\}.
$$

第 $k$ 輪後，令：

$$
H_k(\ell_\star)
=
\left\{
i:
\ell_k(E_i)<\ell_\star
\right\}.
$$

若研究只增加證書而不撤銷合法證書：

$$
H_{k+1}\subseteq H_k.
$$

---

# 3. Faithful unresolved mass

取：

$$
s>1.
$$

定義：

$$
\boxed{
\mathfrak B_k(s;\ell_\star)
=
\sum_{i\in H_k(\ell_\star)}
i^{-s}.
}
$$

任何一個固定未認證 class 都留下正質量。

因此：

$$
\mathfrak B_k=0
\iff
H_k=\varnothing
$$

在有限 benchmark 中成立。

對無限枚舉，若 certificate system monotone，則：

$$
\lim_{k\to\infty}\mathfrak B_k=0
$$

表示每個固定 class最終離開 unresolved frontier。

---

# 4. 它不是 BSD 證明

即使：

$$
\mathfrak B_k\to0,
$$

也只表示：

> 所採 certificate system逐項覆蓋了枚舉域。

要推出 BSD，還需要：

1. 每個 certificate sound；
2. target claim確實等於 BSD component；
3. 枚舉覆蓋所有 $E/\mathbb Q$；
4. certificate generation不是使用 BSD 作 oracle；
5. 對所有曲線真正達到有限 stage。

所以：

$$
\boxed{
\text{Certificate Globalizer}
\neq
\text{Truth Oracle}.
}
$$

---

# 5. 實際用途

它可以比較：

- 哪條 Agent 路線每輪減少更多 unresolved mass；
- 高 conductor曲線是否被永久遺忘；
- rank $2+$ 是否形成不下降尾部；
- 某 theorem只處理高密度子族還是逐項覆蓋；
- proof backlog是否只是轉移到另一個 component。

---

# 6. 多維版本

可分別定義：

$$
\mathfrak B^{W}_k
$$

弱 BSD backlog，

$$
\mathfrak B^{F}_k
$$

$\Sha$ finiteness backlog，

$$
\mathfrak B^{S}_k
$$

strong formula backlog。

避免一個總分掩蓋：

$$
\text{rank 已證，但 }\Sha\text{ 未閉合}.
$$
