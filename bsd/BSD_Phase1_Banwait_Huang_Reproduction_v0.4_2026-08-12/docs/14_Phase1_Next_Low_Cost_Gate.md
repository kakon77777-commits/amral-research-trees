# 14｜Phase 1 下一個最低成本 Gate

## 不要直接全量重跑 Algorithm1

先做：

### Gate A — Delta-only base verifier

輸入 old accepted list + `a3/isogeny_degrees`。

目標：

$$
40{,}749
\to
36{,}687.
$$

### Gate B — Twist JSON parser diff

直接物化：

```text
old twists_of_ec_labels_500k.json
current twists_of_ec_labels_500k.json
```

計算：

1. removed base keys；
2. stable base keys；
3. stable curves with twist changes；
4. twists removed only by gcd(3N)；
5. twists added after deleting old disc gate；
6. both-effect curves。

### Gate C — Only then full Sage replay

若 A、B 都和 repository current outputs一致，再重跑所有 expensive descent。

---

# 為什麼？

完整 Algorithm1 current paper runtime約十幾分鐘本身其實不算昂貴。

真正昂貴的是**研究語義錯誤的返工**。

Delta-first 可以先確認：

$$
\boxed{
\text{我們理解的是同一個 theorem version。}
}
$$

再投入 full proof-engineering。
