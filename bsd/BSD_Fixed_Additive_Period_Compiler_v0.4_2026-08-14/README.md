# BSD Phase 2 — Fixed Additive Period Compiler v0.4

**日期：** 2026-08-14  
**定位：** fixed odd additive prime 的 modular-period / Néron-period compiler  
**狀態：** certificate hierarchy CLOSED；small/excluded additive primes 的 family-uniform period control仍 OPEN。

## 核心修正

Fouquet–Wan Corollary 1.10 的 rank-zero公式使用 modular-form period \(\Omega_f\)。
elliptic-curve BSD 使用 Néron period，兩者差 Manin constant \(c_E\)。

因此：

\[
\boxed{\mathrm{FW\ H1+H2+H3\ PASS}\not\Rightarrow\mathrm{BSD}(E,p)}
\]

除非另外證明：

\[
p\nmid c_E.
\]

本輪把 period gate拆成 **family-uniform** 與 **per-twist** 兩種 certificate。

---

## 1. Family-uniform branch：Edixhoven safe class

Česnavičius–Neururer–Saha 回顧 Edixhoven [Edi91, Thm. 3]：

若 \(p\ge11\) 是 additive prime，且 reduction **不是** additive potentially ordinary
Kodaira type II, III, IV，則：

\[
\boxed{p\nmid c_\phi.}
\]

若 admissible twist使 fixed bad prime \(p\) 在 \(\mathbf Q(\sqrt d)\) split，
則 quadratic character在 \(G_{\mathbf Q_p}\) 上 trivial，故 local reduction type不變。

因此：

```text
p >= 11
not (potentially ordinary and Kodaira II/III/IV)
twist locally trivial at p
optimality convention closed
```

可直接輸出：

```text
PERIOD_PASS_UNIFORM_FAMILY
```

這是真正能用在：

\[
\forall d\in\mathcal D(E)
\]

的 period certificate。

---

## 2. Per-twist branch：CNS modular degree

Česnavičius–Neururer–Saha Theorem 1.2 給：

\[
c_\phi\mid6\deg\phi,
\]

而對每個 \(p\ge5\) 更精確：

\[
v_p(c_\phi)\le v_p(\deg\phi).
\]

所以對**一條具體 curve/twist**：

\[
\boxed{
p\ge5,\quad p\nmid\deg\phi
\Longrightarrow
p\nmid c_\phi.
}
\]

這是 exact certificate。

但是：

\[
\deg(\phi_{E^{(d)}})
\]

會隨 \(d\) 改變，所以：

```text
base modular degree coprime to p
```

不能推出：

```text
all twists period safe at p.
```

因此 CNS modular-degree branch預設只能輸出：

```text
PERIOD_PASS_THIS_CURVE
```

除非另有 family-uniform modular-degree theorem。

---

## 3. \(p=3\) 精確例外

CNS Theorem 1.2 的 \(3\)-adic bound只有在：

\[
v_3(N)\ge3
\]

且**不存在**

\[
p'\mid N,\qquad p'\equiv2\pmod3
\]

時可能多一個 \(+1\)。

所以若：

\[
v_3(N)\le2
\]

或存在上述 \(p'\)，則仍有：

\[
v_3(c_\phi)\le v_3(\deg\phi).
\]

因此這些情形配：

\[
3\nmid\deg\phi
\]

可輸出 `PERIOD_PASS_THIS_CURVE`。

若 exceptional geometry存在，單靠 \(3\nmid\deg\phi\) 不足以關閉 Manin gate。

---

## 4. Direct Manin certificate

若 certified source直接給 \(c_E\)，則：

\[
v_p(c_E)=0
\]

直接 PASS。

CNS 亦回顧 Cremona 對 conductor \(N\le500000\) 的 optimal curves
完成 Manin conjecture computational verification。

但這仍然是：

```text
THIS_CURVE
```

不是 infinite-family uniform theorem。

---

## 5. Certificate hierarchy

### P0 — UNIFORM_EDIXHOVEN

輸出：

```text
PERIOD_PASS_UNIFORM_FAMILY
```

### P1 — DIRECT_MANIN

輸出：

```text
PERIOD_PASS_THIS_CURVE
```

### P2 — CNS_MODULAR_DEGREE

輸出：

```text
PERIOD_PASS_THIS_CURVE
```

### P3 — VERIFIED_DATABASE_RANGE

輸出：

```text
PERIOD_PASS_THIS_CURVE
```

### P4 — UNKNOWN

對 \(3,5,7\) 或 Edixhoven excluded local types，若沒有額外 theorem/certificate：

```text
PERIOD_UNKNOWN
```

不能把 FW residual PASS 升成 elliptic BSD \(p\)-part。

---

## 6. Global-enclosure correction

上一版說「odd additive prime只產生有限 certificate」需要精確化。

正確的是：

- H1/H2/H3：base/local finite；
- period：可能是 **family-uniform global gate**。

因此：

\[
\boxed{
\text{per-twist decidable}\neq
\text{infinite family proved}.
}
\]

這是本輪最重要的量詞修正。

---

## 7. Rigorous widened theorem class

目前可直接加入 full infinite-family theorem 的 fixed odd additive primes：

\[
\boxed{
p\ge11
}
\]

且不屬於：

\[
\boxed{
\text{additive potentially ordinary Kodaira II, III, IV}.
}
\]

再配：

- FW17-H1；
- FW17-H2 local-isogeny compiler；
- nonsplit H3 witness；
- twist optimality / period convention closed。

這已嚴格擴張 earlier：

```text
only additive prime is 2
```

的 family criterion。

---

## 8. Remaining frontier

真正剩下的 uniform period wall是：

\[
p\in\{3,5,7\}
\]

以及：

\[
p\ge11
\]

但屬於 Edixhoven excluded potentially ordinary types II/III/IV。

下一步只值得攻三條路：

1. twist-family Manin \(p\)-adic invariance；
2. family-uniform modular-degree nondivisibility / congruence-prime theorem；
3. 若連續幾輪不改 Gate，凍結這堵牆，將一般 theorem限定在 Edixhoven-safe class。
