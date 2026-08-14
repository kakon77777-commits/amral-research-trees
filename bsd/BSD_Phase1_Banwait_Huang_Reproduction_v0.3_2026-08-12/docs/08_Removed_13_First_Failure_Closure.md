# 08｜Removed 13 First-Failure Closure

v0.2 對 13 條 removed curves 保守標成：

```text
VERSION_REGRESSION_REMOVED
reason = OPEN
```

v0.3 已利用：

1. exact one-commit diff；
2. 官方 old/current fixture mapping；
3. LMFDB / Cremona primary curve/isogeny data；
4. 一個 exact finite-field count；

完成 first-failure closure。

## Histogram

$$
9\times P\_ISOGENY\_3,
$$

$$
2\times P\_ISOGENY\_5,
$$

$$
1\times P\_ISOGENY\_7,
$$

$$
1\times A3\_ABS\_3.
$$

## 完整表

| Curve | LMFDB | First failure |
|---|---|---|
| 14a1 | 14.a6 | P_ISOGENY_3 |
| 34a1 | 34.a4 | P_ISOGENY_3 |
| 66c1 | 66.c3 | P_ISOGENY_5 |
| 26a1 | 26.a2 | P_ISOGENY_3 |
| 26b1 | 26.b2 | P_ISOGENY_7 |
| 35a1 | 35.a3 | P_ISOGENY_3 |
| 38a1 | 38.a3 | P_ISOGENY_3 |
| 38b1 | 38.b2 | P_ISOGENY_5 |
| 106a1 | 106.c2 | P_ISOGENY_3 |
| 110c1 | 110.a1 | P_ISOGENY_3 |
| 110b1 | 110.c1 | P_ISOGENY_3 |
| 142e1 | 142.c1 | A3_ABS_3 |
| 142d1 | 142.e2 | P_ISOGENY_3 |

`26b1` 還有 secondary：

$$
a_3=-3.
$$

但 production pipeline先執行 strict isogeny gate，因此 first failure是 `P_ISOGENY_7`。

## 關鍵結論

小樣本的 25→12 不再是黑箱版本漂移：

$$
\boxed{
\text{13 removed curves are fully explained by the new Algorithm1 predicates.}
}
$$
