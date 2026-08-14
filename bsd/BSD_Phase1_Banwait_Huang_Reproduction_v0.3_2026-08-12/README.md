# BSD Phase 1 — Banwait–Huang Reproduction v0.3

**日期：** 2026-08-12

本版完成 v0.2 留下的主要 OPEN 問題：

$$
\boxed{
\text{舊版 25 條為何在現行版只剩 12 條？}
}
$$

答案現在已收斂到單一 commit 的 theorem-semantic change。

## 核心結果

2026-05-22 commit：

`1a0489c3c3099dd0c248624e6621df73ae8f0d43`

到 2026-06-03 commit：

`31fae20c8df3f1f0383f41112b914d4995d5809d`

中間只有一個 commit。

Algorithm 1 將舊的 dynamic isogeny set $A$ 改成：

$$
\{3,5,7\}
$$

一律檢查，並新增獨立：

$$
a_3(E)\neq\pm3.
$$

13 條 removed curves 的 first-failure 已閉合：

- $9$ 條：`P_ISOGENY_3`
- $2$ 條：`P_ISOGENY_5`
- $1$ 條：`P_ISOGENY_7`
- $1$ 條：`A3_ABS_3`

其中 `26b1` 在 strict 7-isogeny gate 後，亦有 secondary `A3_ABS_3`。

## 特殊例外：142e1

`142e1` 不是 isogeny removal。

模型：

$$
y^2+xy=x^3-x^2-2626x+52244.
$$

直接枚舉 $\mathbb F_3$：

$$
\#E(\mathbb F_3)=1,
$$

故：

$$
a_3=3+1-1=3.
$$

因此它精確撞上新的 $a_3(E)\neq\pm3$ gate。

## Algorithm 2 的新發現

舊／新 `<150` twist JSON 對 surviving 12 base curves 完全相同。

所以：

$$
\boxed{
\text{small positive fixture does not exercise the Algorithm2 semantic diff}.
}
$$

本版新增 synthetic predicate-level tests，專門捕捉：

1. `gcd(M,N)=1` → `gcd(M,3N)=1`；
2. 舊 `disc_valuation_condition` 被刪除。

## 注意

本版是 reproduction / proof-engineering closure，不是新增 BSD theorem。
