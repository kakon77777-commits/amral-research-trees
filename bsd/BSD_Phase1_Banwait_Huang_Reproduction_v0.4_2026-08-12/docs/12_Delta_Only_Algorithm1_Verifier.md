# 12｜Delta-Only Algorithm1 Verifier

## 目的

不要一開始重跑：

- L-value merge；
- 2-descent；
- $E'$ descent；
- $\mathcal S$；
- 全部舊 filters。

因為舊 output中的每一條 curve已經通過 old Algorithm1。

對 old accepted set：

$$
\mathcal C_{\rm old},
$$

current set只需計算：

$$
\mathcal C_{\rm new}
=
\left\{
E\in\mathcal C_{\rm old}:
\{3,5,7\}\cap I(E)=\varnothing,\;
|a_3(E)|\ne3
\right\},
$$

其中：

$$
I(E)
$$

是 rational prime-degree isogeny degrees。

這是一個**增量證明重播**。

---

## 為什麼它是 exact？

old → current 只有一個 commit。

Algorithm1 的 theorem predicate差分沒有其他 loosen/tighten gate。

因此對已知 old PASS rows：

$$
\boxed{
\text{new membership}
=
\text{strict-isogeny gate}
\land
a_3\text{ gate}.
}
$$

不需要重做 unchanged proof obligations。

---

## 輸入最小化

每條只需：

```json
{
  "cremona_label": "...",
  "a3": 0,
  "isogeny_degrees": [1,2,3,6]
}
```

如果本地 LMFDB已連接，這兩個欄位非常便宜：

- `a3`：class `aplist` 的 $p=3$ 項；
- `isogeny_degrees`：curve table metadata。

---

## 成功 Gate

輸入舊版：

$$
40{,}749
$$

條。

預期：

$$
\text{PASS}=36{,}687,
$$

$$
\text{FAIL}=4{,}062.
$$

並輸出全量 failure histogram：

```text
P_ISOGENY_3
P_ISOGENY_5
P_ISOGENY_7
A3_ABS_3
multi-failure
```

這會是第一份 500K semantic-cause census。

---

## 失敗意義

若 delta-only verifier不能得到 current官方集合，則至少一件事成立：

1. 我們漏掉 semantic diff；
2. LMFDB release不同；
3. old/current output不是同資料快照；
4. metadata mapping錯；
5. implementation有未記錄 side effect。

此時應停，不應直接進 full replay。
