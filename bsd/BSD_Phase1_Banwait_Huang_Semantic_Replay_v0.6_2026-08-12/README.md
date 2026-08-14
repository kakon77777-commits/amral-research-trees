# BSD Phase 1 — Banwait–Huang Semantic Replay v0.6

**日期：** 2026-08-12

## 一句話

v0.5 是 `Exact Artifact Census`。

v0.6 將 generator → OLD → CURRENT 的 Algorithm2 source diff 套回已 materialize 的真實 twist pairs，完成：

**Exact Semantic Replay（stable domain）**

## 最重要結果

在 generator archived JSON 的全部 39,394 curves / 293,482 twist pairs 上：

- OLD 新增的 `disc_valuation_condition` 失敗 pair：**0**
- 因而該 gate 對全部已 materialize generator output 都是資料上冗餘的。

在 36,687 stable base curves 上：

- generator twist pairs：268,697
- OLD-source replay pairs：268,697
- CURRENT pairs：247,391
- new `gcd(M,3N)=1` 刪除：21,306
- 刪除 `disc_valuation_condition` 所新增：0
- hidden interaction：0
- CURRENT predicted-vs-actual mismatch：0

Curve classes：

- UNCHANGED = 31,250
- SHRINK_ONLY = 5,437
- EXPAND_ONLY = 0
- MIXED = 0

而且所有 21,306 個 removals 全部在 `Zha16_no_2_tors` 分支；CLZ20 為 0。

## 作用域

這個 replay 對 stable 36,687 curves 是 exact。

另有 1,355 條 OLD base curves 是 generator JSON 生成後才加入，因此沒有 generator twist entry。v0.6 不虛構它們的 historical OLD-source outputs。

## 下一步

Reproduction line 至此已足夠收斂。除非要做完整歷史重建，否則不建議再投入大量時間補那 1,355 條，因為它們已被 CURRENT Algorithm1 排除，不影響當前 theorem-qualified universe。

建議下一階段回到 BSD 數學本身：
- High-rank wall atlas，或
- current strong-BSD family coverage / theorem applicability 的新數學擴張。
