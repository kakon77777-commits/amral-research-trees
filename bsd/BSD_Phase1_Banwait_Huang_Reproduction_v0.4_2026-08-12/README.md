# BSD Phase 1 — Banwait–Huang Reproduction v0.4

**日期：** 2026-08-12  
**主題：** 500K one-commit global impact + delta-only verifier

## 核心結果

最新版論文直接報告：

$$
36{,}687
$$

條 base curves 通過 current Algorithm 1。

2026-05-22 → 2026-06-03 只有一個 commit。

`ec_labels_500k.txt` 的 Git diff：

```text
+2 / -4064
```

Algorithm 1 的輸出 writer 未改，predicate 只做單調收緊：

1. dynamic isogeny set → strict `{3,5,7}`;
2. 新增 `a3 != +/-3`.

因此兩個新增 diff 行對應被改寫的 metadata，而曲線列精確少：

$$
4062.
$$

故舊版接受數可重建為：

$$
36{,}687+4{,}062
=
40{,}749.
$$

新版保留舊 accepted set 的：

$$
90.031657\%.
$$

即這一個 theorem-semantic commit移除了舊 accepted set 約：

$$
9.968343\%.
$$

## 另一個全量訊號

`twists_of_ec_labels_500k.json`：

```text
+1899 / -53404
```

這不可能由「只刪 base-curve JSON blocks」完整解釋。

因此 Algorithm2 的語義改動在 500K 域有實際輸出效應；但 small `<150` positive fixture 的 12 條 surviving curves，舊新 twist lists又完全相同。

所以新增：

$$
\boxed{
\text{large-domain semantic coverage}
}
$$

作為 regression gate。

## Delta-only verifier

完整 Sage/descent重跑前，可先只對舊版約四萬條 accepted rows取得：

```text
a3
isogeny_degrees
```

然後用 `src/incremental_algorithm1_delta.py` 精確套用唯一 commit 的新 predicate。

若結果不是精確：

$$
36{,}687,
$$

就不必浪費時間重跑全部 descent。

## 限制

本 runtime仍未物化兩個 500K 巨型 output file，所以：

- current 36,687 是論文直接值；
- 4,062 / old 40,749 是由 commit diff + monotone predicate diff + writer invariance重建；
- twist entry-level新增/刪除數尚未解析，只能確認 global output effect。

上一版 v0.3 已封存在 `prior/`。
