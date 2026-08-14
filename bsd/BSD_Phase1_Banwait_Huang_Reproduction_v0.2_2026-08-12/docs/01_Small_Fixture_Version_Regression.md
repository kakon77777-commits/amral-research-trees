# 01｜小樣本版本回歸：25 → 12

## Old fixture

日期：$2026$-$05$-$22$。

總數：$25$，其中 $10$ 條 CLZ20、$15$ 條 Zha16。

## Current fixture

日期：$2026$-$06$-$03$。

總數：$12$，其中 $7$ 條 CLZ20、$5$ 條 Zha16。

## Exact diff

保留 $12$，移除 $13$，新增 $0$。

移除清單：

```text
106a1, 110b1, 110c1, 142d1, 142e1, 14a1, 26a1, 26b1, 34a1, 35a1, 38a1, 38b1, 66c1
```

## 不能過度解讀

這份 diff 只能說某曲線由舊版 `PASS` 變成現行非 `PASS`。

沒有逐 filter replay 前，一律標：

```text
VERSION_REGRESSION_REMOVED
reason = OPEN
```

不能從 commit message、branch 分布或直覺補完數學理由。
