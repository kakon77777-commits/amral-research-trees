# 07｜One-Commit Semantic Autopsy

## Commit distance

舊 fixture commit：

`1a0489c3c3099dd0c248624e6621df73ae8f0d43`

現行 commit：

`31fae20c8df3f1f0383f41112b914d4995d5809d`

兩者相差恰好一個 commit。

## Algorithm 1

舊版本不是一律排除 $3,5,7$-isogeny，而是建立動態集合：

$$
A_{\mathrm{old}}
=
\{3: 3\mid N\text{ or }|a_3|=3\}
\cup
\{5:5\mid N\}
\cup
\{7:7\mid N\}.
$$

只排除：

$$
p\in A_{\mathrm{old}}
$$

的 rational $p$-isogeny。

新版本改成：

$$
A_{\mathrm{new}}=\{3,5,7\},
$$

並另外新增：

$$
a_3(E)\neq\pm3.
$$

這是 theorem predicate 的實質收緊，不是效能重構。

## Algorithm 2

同 commit：

$$
\gcd(M,N)=1
\quad\longrightarrow\quad
\gcd(M,3N)=1,
$$

但同時移除了舊 twist-side `disc_valuation_condition`。

所以 Algorithm 2 同時存在：

- shrink mechanism；
- expand mechanism。

不能用「新版比較嚴」一個方向概括。
