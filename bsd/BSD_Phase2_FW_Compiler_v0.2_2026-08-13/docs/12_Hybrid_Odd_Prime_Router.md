# 12｜Hybrid Odd-Prime Router

完整 strong-BSD family不要求單一 theorem cover所有 $p$。

## P0 — $p=2$

Banwait–Huang Theorem 2.14。

## P1 — $p\mid d$

$p$ 是 base curve 的 good prime。要求 support primes：

- $p\ge5$；
- good ordinary；
- residual irreducibility；
- 有 multiplicative residual-ramification witness。

使用既有 additive-twist ordinary theorem。

## P2 — good ordinary, $p\nmid d$

- residual reducible：走 reducible/Eisenstein ordinary theorem；
- residual irreducible：走 ordinary Iwasawa theorem / direct ramified witness / BCS支援。

不使用 FW。

## P3 — fixed multiplicative $p\mid N$

有限集合。逐 prime檢：

- residual irreducibility；
- 另一個 $q\ne p$ 的 ramified multiplicative witness；
- 對應 multiplicative theorem hypotheses。

## P4 — fixed additive $p\mid N$

有限集合。使用 FW：

```text
H1 = exact residual absolute irreducibility
H2 = exact local character-ratio test
H3 = nonsplit multiplicative witness
period = Manin compatibility
```

## P5 — good supersingular

使用 derived FW bridge：

```text
H1 automatic
H2 automatic
H3 uniform from g_-(E)
```

## 結果

原本的

$$
\forall p>2
$$

被拆成：

- finite bad-prime table；
- support-prime restrictions；
- ordinary theorem；
- supersingular uniform certificate。

這才是可行的 global quantifier compression。
