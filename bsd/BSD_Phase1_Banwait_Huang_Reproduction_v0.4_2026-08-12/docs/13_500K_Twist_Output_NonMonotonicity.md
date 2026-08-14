# 13｜500K Twist Output Non-Monotonicity

## 觀測

同一 commit：

```text
twists_of_ec_labels_500k.json
+1899 / -53404
```

而 Algorithm1 base-curve set只會縮小。

如果 twist JSON只因 base curve被刪除而改變：

$$
\text{diff additions}
$$

應最多來自極少數 punctuation / context change，而不會有 $1899$ 個新增行。

所以全量輸出表明：

$$
\boxed{
\text{Algorithm2 semantic change is active somewhere in the large domain.}
}
$$

---

## 兩個相反方向的 predicate change

### Shrink

$$
\gcd(M,N)=1
\to
\gcd(M,3N)=1.
$$

這會移除舊版允許的 $3\mid M$ candidates（當 $3\nmid N$）。

### Expand

刪除舊：

```text
disc_valuation_condition
```

可能讓某些以前被 ramification-style gate擋掉的 $M$ 新增進來。

因此：

$$
\boxed{
\text{twist output need not be monotone}.
}
$$

---

## 為什麼不能直接說「新增 1899 個 twists」？

Git diff統計的是**行**，而 JSON 中同時包含：

- key lines；
- bracket/comma structural lines；
- twist integer lines；
- 整個被刪除 base block。

因此：

$$
1899
$$

是 added diff lines，不是已證明的 unique new twist count。

完整 entry-level census需要物化 old/current JSON後 parse set difference。

---

## Small fixture coverage failure

對 current surviving `<150` 的 12 條曲線：

$$
T_{\rm old}(E)=T_{\rm new}(E)
$$

逐條成立。

因此 small positive fixture對 Algorithm2 這次 semantic diff 的 branch coverage：

$$
\boxed{
0\text{ observed output deltas}.
}
$$

這就是為什麼 v0.3 加 synthetic semantic tests，而 v0.4 要求 full-file entry census。
