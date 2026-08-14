# 14｜Candidate Sieve：為什麼 696.e1 冒出來？

## Cheap gates first

本輪改用：

```text
rank/optimal/Manin
→ 2-part Lalg valuation
→ base BSD(E,2)
→ odd multiplicative reservoirs
→ fixed additive primes
→ residual images
→ only then local Iwasawa/FW
```

而不是先對每條 curve做昂貴 local Galois analysis。

---

# 696.e1

$$
E=[0,1,0,8,-16].
$$

### Base

- rank $0$；
- torsion trivial；
- optimal；
- Manin $1$；
- conductor $696<5000$；
- $\Sha_{\rm an}=1$；
- Tamagawa product $1$。

所以：

$$
L^{alg}(E,1)=1,
\qquad
v_2(L^{alg})=0.
$$

它正好進 Theorem 2.14：

```text
no rational 2-torsion
negative discriminant
```

branch。

### Odd local structure

```text
2  additive II*                 vDelta=11
3  split multiplicative I1     vDelta=1
29 nonsplit multiplicative I1  vDelta=1
```

因此：

$$
W_{\rm mult}^{odd}=\{3,29\},
$$

$$
W_-=\{29\}.
$$

而所有 relevant gcd都是 $1$。

### Residual images

LMFDB記錄 maximal image for all primes。

所以：

- support prime residual irreducibility；
- fixed multiplicative residual irreducibility；
- no rational isogeny；
- twist irreducibility preservation；

全部極度乾淨。

---

# Control: 116.b1

`116.b1` 同樣：

- rank0；
- cheap 2-part anchor漂亮；
- nonsplit multiplicative $29$。

但 odd bad structure只有：

```text
2 additive
29 nonsplit multiplicative
```

所以在 fixed multiplicative：

$$
p=29
$$

時沒有另一個：

$$
q\neq29,\quad q\parallel N
$$

作 residual-ramification witness。

因此它目前被：

```text
FAIL_FIXED_MULTIPLICATIVE_WITNESS
```

淘汰。

這說明 `696.e1` 的關鍵不是單純「有 nonsplit prime」，而是：

$$
\boxed{
\text{至少兩個 odd multiplicative reservoirs，
其中至少一個 nonsplit。}
}
$$
