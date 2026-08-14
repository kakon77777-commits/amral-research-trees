# 11｜500K One-Commit Global Impact

## 1. Current benchmark

論文報告：

$$
3{,}064{,}705
$$

條 conductor $<500{,}000$ 曲線中：

$$
1{,}170{,}876
$$

解析秩 $0$；

再縮到 semistable、optimal、conductor 至少兩個 prime factors後：

$$
178{,}364.
$$

Current Algorithm 1 接受：

$$
36{,}687.
$$

所以：

$$
\frac{36{,}687}{178{,}364}
\approx20.5686\%.
$$

---

## 2. One-commit effect

Git compare：

```text
ec_labels_500k.txt  +2 / -4064
```

同一個 commit 的 Algorithm1 predicate change是單調收緊。

輸出 writer 未改，與 `<150` 文件相同，兩個變動 metadata行是 timestamp/runtime 類資訊。

因此：

$$
4064-2=4062
$$

條 curve rows被移除。

重建舊 accepted count：

$$
40{,}749.
$$

---

## 3. Impact scale

舊 accepted set 中被移除比例：

$$
\frac{4062}{40749}
\approx9.9683\%.
$$

新版保留：

$$
\frac{36687}{40749}
\approx90.0317\%.
$$

在 pre-candidate pool 中：

$$
22.8460\%
\to
20.5686\%.
$$

下降約：

$$
2.2774
$$

個百分點。

對全部 $3{,}064{,}705$ curves：

$$
1.3296\%
\to
1.1971\%.
$$

這一個 semantic correction本身相當於全資料域約：

$$
0.1325
$$

個百分點。

---

## 4. Global cause union

因為 Algorithm1 在此 commit只有兩個 theorem-level變化：

1. strict $3/5/7$ rational-isogeny exclusion；
2. independent $a_3\ne\pm3$；

所以每一條 $4062$ removed curve必定落入：

$$
\boxed{
\text{new strict isogeny failure}
\;\cup\;
\{|a_3|=3\}.
}
$$

這是全量原因的**集合級閉合**。

但各 gate的精確 histogram仍未知，不能把 `<150` 的 $9/2/1/1$ 比例外推到 500K。

---

## 5. 研究解讀

這不是新 BSD theorem。

它證明的是：

> theorem predicate的一個看似很小的修正，可以改變約 $10\%$ 的舊 accepted base-curve universe。

所以對 Agent 系統：

$$
\boxed{
\text{semantic versioning不是附加工程，而是數學 soundness的一部分。}
}
$$
