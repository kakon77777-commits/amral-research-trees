# 15｜Fresh Semantic Replay：Algorithm2 OLD → CURRENT

## 1. Source chronology

三個語義節點：

$$
G=\text{generator commit }7286794,
$$

$$
O=\text{OLD commit }1a0489,
$$

$$
C=\text{CURRENT commit }31fae2.
$$

`G -> O` 的 Algorithm2 theorem predicate 新增：

$$
D(E,d)=\texttt{disc\_valuation\_condition}.
$$

`O -> C`：

1. 刪除 $D(E,d)$；
2. 把
   $$
   \gcd(d,N)=1
   $$
   收緊成
   $$
   \gcd(d,3N)=1.
   $$

其餘 relevant admissibility predicates 不變。

---

## 2. 為什麼可以不用 Sage 重建 OLD stable output？

generator archived twist JSON 已經是 generator Algorithm2 對實際曲線的輸出。

所以 OLD source在相同 generator-domain curve上只需再施加：

$$
D(E,d).
$$

v0.5 同時提供每條曲線：

- conductor primes；
- minimal discriminant；
- $v_q(\Delta_E)$。

因此 $D(E,d)$ 可直接 exact replay，不需要重新計算：

- $a_p$；
- 2-division field；
- Kronecker conditions；
- squarefreeness；

因為 generator output已通過這些 unchanged gates。

---

## 3. 全 materialized generator domain

Generator archived JSON：

$$
39{,}394\text{ curves},
$$

$$
293{,}482\text{ twist pairs}.
$$

逐 pair套用 OLD 新增：

$$
D(E,d)
$$

得到：

$$
\boxed{
0\text{ failures}.
}
$$

因此在全部已 materialize generator output上：

$$
\boxed{
T_O(E)=T_G(E).
}
$$

注意：這是資料域 statement，不宣稱 $D$ 作為抽象 theorem condition 永遠冗餘。

---

## 4. Stable 36,687 curves 的兩 gate 分割

在 generator twist pairs 上定義：

$$
D=1
$$

表示通過 OLD disc gate；

$$
G_3=1
$$

表示通過 CURRENT：

$$
\gcd(d,3N)=1.
$$

精確四格：

| Cell | Count | 意義 |
|---|---:|---|
| $D=1,G_3=1$ | 247,391 | OLD/CURRENT 共通 |
| $D=1,G_3=0$ | 21,306 | OLD-only；被新 gcd gate 刪除 |
| $D=0,G_3=1$ | 0 | CURRENT-only；本可由刪 disc gate新增 |
| $D=0,G_3=0$ | 0 | 兩 gate interaction 隱藏區 |

因此：

$$
|T_O|=268{,}697,
$$

$$
|T_C|=247{,}391.
$$

而：

$$
T_C
=
\{(E,d)\in T_O:\gcd(d,3N_E)=1\}.
$$

逐 curve 比較 mismatch：

$$
\boxed{0}.
$$

---

## 5. Semantic attribution

因此 stable domain 的 OLD→CURRENT delta 可以**完全歸因**：

$$
\boxed{
21{,}306\text{ removals}
=
\text{new factor-3 coprimality gate}.
}
$$

而：

$$
\boxed{
0\text{ additions}
=
\text{disc gate deletion produced no observable gain}.
}
$$

不存在 mixed interaction。

---

## 6. Branch structure

### CLZ20

generator stable pairs：

$$
5{,}849.
$$

全部：

$$
D=1,G_3=1.
$$

所以：

$$
\Delta_{\rm CLZ}=0.
$$

這與 CLZ twist prime condition要求：

$$
p\equiv1\pmod4
$$

相容；$p=3$ 本來就不能成為 twist prime。

### Zha16

generator stable pairs：

$$
262{,}848.
$$

其中：

$$
241{,}542
$$

保留，

$$
21{,}306
$$

因 factor $3$ 被刪除。

所以整個 observable Algorithm2 semantic delta都落在 Zha16 branch。

---

## 7. Curve-level census

$$
31{,}250
$$

條 stable curves完全 unchanged。

$$
5{,}437
$$

條只有 removals。

$$
0
$$

條 only additions。

$$
0
$$

條 mixed。

因此：

$$
\boxed{
\text{CURRENT semantic update在 stable domain 是純單調縮減。}
}
$$

先前從 source diff推測可能有 shrink + expand 兩方向，現在 exact replay證明：

> expand mechanism 在這個實際資料域沒有啟動。

---

## 8. Epistemic boundary

還有：

$$
1{,}355
$$

條 OLD base curves是在 generator twist JSON生成後才加入 OLD base file。

它們沒有 generator twist entries，因此本 replay不能在不重新執行 Algorithm2 common gates 的情況下重建其 OLD-source output。

但這 1,355 curves全部已被 CURRENT Algorithm1 strict isogeny gate排除。

所以對**當前 theorem-qualified universe**：

$$
\boxed{
\text{stable semantic replay已閉合。}
}
$$

補那 1,355 條只具有歷史重建價值，不是 current BSD research 的必要依賴。

---

## 9. 停止規則

此 reproduction line 已從：

$$
\text{artifact diff}
\to
\text{exact census}
\to
\text{source semantic replay}
$$

完成三層閉合。

若沒有新的 theorem discrepancy，繼續做：

- 更細 Git archaeology；
- 1,355 條歷史曲線重建；
- 更多 formatting replay；

應標：

`ENGINEERING / HISTORICAL ONLY`

而不是 BSD 數學進展。

因此建議在 v0.6 封頂 Phase 1 reproduction。
