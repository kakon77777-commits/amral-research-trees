# BSD Phase 2 — First Non-Semistable Family v0.3

**日期：** 2026-08-13  
**主角：** LMFDB `696.e1` / Cremona `696b1`  
**狀態：** `PROVISIONAL DERIVED FAMILY THEOREM` — proof router已閉合到可逐行 referee；尚未宣稱文獻新穎性。

---

# 0. 一句話

我們找到一條不在 Banwait–Huang semistable universe 裡的 curve：

$$
E:\quad y^2=x^3+x^2+8x-16,
$$

conductor：

$$
N=696=2^3\cdot3\cdot29,
$$

其唯一 non-semistable obstruction在 $2$。

它同時具有：

- rank $0$；
- trivial torsion；
- optimal；
- Manin constant $1$；
- $\Sha_{\rm an}=1$；
- $L(E,1)/\Omega_E=1$；
- split multiplicative $3$，$v_3(\Delta)=1$；
- nonsplit multiplicative $29$，$v_{29}(\Delta)=1$；
- 所有 mod-$\ell$ Galois images maximal；
- 無 rational isogenies。

這讓：

$$
3\leftrightarrow29
$$

成為 fixed multiplicative prime彼此的 residual-ramification witnesses，而 $29$ 又同時成為所有 good supersingular primes 的 Fouquet–Wan witness。

---

# 1. Explicit prime family

令：

$$
f_2(x)=x^3+x^2+8x-16.
$$

定義 $\mathcal P$ 為所有 prime $q$ 滿足：

$$
q\equiv1\pmod{24},
$$

$$
\left(\frac{q}{29}\right)=1,
$$

以及：

$$
f_2(x)\text{ 在 }\mathbb F_q[x]\text{ 不可約}.
$$

前 20 個：

```text
241, 313, 457, 673, 937, 1009, 1153, 1753, 2017, 2089,
2113, 2137, 2617, 2713, 3049, 3457, 3529, 3769, 3793, 4201
```

每一個這樣的 $q$：

- $2,3,29$ 都 split in $\mathbb Q(\sqrt q)$；
- $q$ inert in the cubic 2-division field；
- $q$ automatic ordinary for $E$。

所以它正好是 Banwait–Huang Theorem 2.14 no-rational-$2$-torsion branch的自然 support prime。

---

# 2. Automatic ordinarity trick

$q$ inert in the cubic 2-division field代表 mod-$2$ Frobenius是 $S_3\simeq GL_2(\mathbb F_2)$ 中的 $3$-cycle。

order-$3$ element的 trace：

$$
1\in\mathbb F_2.
$$

故：

$$
a_q(E)\equiv1\pmod2.
$$

因此 $a_q$ 是 odd。

對 $q\ge5$，supersingular會迫使：

$$
a_q=0
$$

（Hasse bound）。

矛盾。

所以：

$$
\boxed{
q\text{ inert in }f_2
\Longrightarrow
q\text{ ordinary}.
}
$$

這把 Algorithm2 裡原本獨立的 ordinary support condition，在這條 curve上直接吸收到 $2$-division inertness condition中。

---

# 3. Chebotarev family

$f_2$ 的 discriminant：

$$
-11136=-2^7\cdot3\cdot29.
$$

$f_2$ irreducible且 discriminant非平方，因此其 Galois closure $L/\mathbb Q$ 有：

$$
\mathrm{Gal}(L/\mathbb Q)\cong S_3.
$$

唯一 quadratic resolvent：

$$
F_0=\mathbb Q(\sqrt{-174}).
$$

令：

$$
K=\mathbb Q(\zeta_{24},\sqrt{29}).
$$

則：

$$
[K:\mathbb Q]=16,
$$

而：

$$
F_0\subset K.
$$

因 $L$ 唯一非平凡 normal abelian subfield就是 $F_0$：

$$
L\cap K=F_0.
$$

所以：

$$
[LK:\mathbb Q]=\frac{6\cdot16}{2}=48.
$$

取 $S_3$ 中任一 $3$-cycle $\sigma$，它在 $F_0$ 上作用 trivial；與
$\mathrm{Gal}(K/\mathbb Q)$ 的 identity相容。

Chebotarev因此給：

$$
\boxed{
\delta(\mathcal P)=\frac{2}{48}=\frac1{24}.
}
$$

所以 $\mathcal P$ 不只無限，而且具有正自然密度 $1/24$。

---

# 4. Candidate conclusion

對每：

$$
q\in\mathcal P,
$$

令 $E_q$ 是 quadratic twist。

目前的 derived proof router得到：

1. Banwait–Huang Theorem 2.14：
   $$
   L(E_q,1)\neq0,\qquad \operatorname{BSD}(E_q,2).
   $$
2. $p=q$ additive-twist branch：
   ordinary + residual irreducible + witness $29$。
3. good ordinary $p\nmid q$：
   direct ramified witness $3$ or $29$。
4. fixed multiplicative $p=3,29$：
   互為 distinct ramified witness。
5. good supersingular $p$：
   Fouquet–Wan, witness $29$。

因此候選結論：

$$
\boxed{
\forall q\in\mathcal P,\quad
\operatorname{BSD}(E_q).
}
$$

---

# 5. Claim discipline

這一包把上述內容標成：

```text
PROVISIONAL DERIVED FAMILY THEOREM
```

而不是：

```text
NEW THEOREM
```

原因：

1. 需要再做一輪 line-by-line external-source convention audit；
2. Fouquet–Wan / Banwait–Huang 部分依賴 preprint-level results；
3. 尚未完成真正的 novelty search；
4. 尚未讓獨立 Sage/Magma/另一個 Agent完整 replay proof certificate。

如果下一輪 referee audit不出現新 gap，才升級成：

```text
DERIVED THEOREM / PREPRINT CANDIDATE
```
