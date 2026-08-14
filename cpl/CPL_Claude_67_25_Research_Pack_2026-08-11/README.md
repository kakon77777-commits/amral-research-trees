# Critical-Line Proportion Ladder (CPL) — Claude 67.25% Research Pack

**建立日期：** 2026-08-11  
**研究狀態：** Batch 01 / Literature + Proof Reconstruction  
**主問題：** 從 Claude 2026-08-10 的無條件 $67.25\%$ 結果出發，研究 $70\%/80\%/90\%/99\%$ 的可達條件。

## 0. 語義鎖定

本專案中的百分比**不是黎曼猜想完成度**。

定義：

$$
P_q:\quad
\liminf_{T\to\infty}
\frac{N_0^s(T,2T)}{N(T,2T)}\ge q,
$$

其中 $N_0^s(T,2T)$ 是 $T<\gamma\le2T$ 中 **simple 且位於 $\Re(s)=1/2$** 的零點數，$N(T,2T)$ 按 multiplicity 計數。

即使達到：

$$
P_1,
$$

也只是 density-one simple critical zeros，仍然不等於 RH 的逐點全稱命題。

---

## 1. 本包內容

### 主論文

- `00_Claude_More_Than_Two_Thirds_Riemann_Zeta_2026-08-10.pdf`
  - Claude, *More Than Two Thirds of the Zeros of the Riemann Zeta Function Lie on the Critical Line* (2026-08-10).

### 直接前置／比較文獻

- `01_BGSTB24_Unconditional_Montgomery_Theorem.pdf`
- `02_BGSTB25_Pair_Correlation_Proportions.pdf`
- `03_GLSS25_PCC_Simple_Critical_Zeros.pdf`
- `04_GS25_Zeta_Zeros_on_Critical_Line.pdf`
- `05_GS26_Zeta_Zeros_Narrow_Vertical_Box.pdf`
- `06_CGdL20_Pair_Correlation_SDP.pdf`
- `07_CCLM17_Hilbert_Spaces_Pair_Correlation.pdf`

### 研究筆記

- `notes/01_Proof_Graph_Claude_67_25.md`
- `notes/02_CPL_Targets_70_80_90_99.md`
- `notes/03_Ceiling_Scope_67_25_vs_68_185.md`
- `notes/00_constant_check.txt`

### 程式

- `scripts/reproduce_constants.py`

它只重算論文中可由閉式公式直接得到的常數，不宣稱重現整個證明。

---

## 2. 第一輪已確認的關鍵結構

Claude 的核心證明可壓成：

$$
\boxed{
\text{Weil explicit formula}
\to
\text{finite Gabor compression}
\to
\text{zero-side inertia}
\to
\text{prime-side traces}
\to
\text{rank--trace certificate}
}
$$

基準 flat-window certificate：

$$
H(\lambda)=2-\frac1\lambda-\frac\lambda3,
$$

在 $\lambda=1$：

$$
H(1)=\frac23.
$$

最佳化 window 後：

$$
c_1^*=0.753296\ldots,
$$

$$
2-\frac1{c_1^*}=0.672500\ldots.
$$

---

## 3. 兩種「天花板」不可混淆

### A. $67.25\%$

這是論文 §7.1 在「block structure + two traces + primes up to $T$」且只改 window 的框架內，由 Montgomery–Taylor extremal kernel 達到的極值；論文說 no window does better。

### B. $68.185\%$

論文 Remark 1.1 宣稱一個更廣的 bandwidth-one、configuration-by-configuration certificate class 的上界約為：

$$
0.68185.
$$

因此不能把 $68.185\%$ 當成「只要再最佳化 window 就一定可達」。目前主論文正文給出這個 extremal-law 結論，但本 Batch 尚未找到足以獨立重建該 $0.68185$ 常數的完整推導；此項被標成 **OPEN-RECONSTRUCTION-01**。

---

## 4. 已知 target ladder

主論文對「same route」給出的 rough Fourier-support 需求：

$$
P_{70}:\ \sigma\approx1.04,
$$

$$
P_{80}:\ \sigma\approx1.26,
$$

$$
P_{90}:\ \sigma\approx1.70.
$$

對 $P_{99}$，論文**沒有**給 finite support threshold，因此本專案禁止用前三點線性外插。

另一條 conditional higher-moment route：若 $HL^*(4,\lambda)$ 對所有 $\lambda<1$ 成立，論文得到：

$$
P\ge\frac{13}{18}=0.722222\ldots.
$$

若能得到任意高階相應 moments，該 mechanism 可達 density $1$，但仍不等於 RH。

---

## 5. 下一批優先研究

1. **P0**：獨立重證 Lemma 3.2 rank--trace inequality。
2. **P1**：重建 off-line pair 的 $(1,1)$ signature 與 pull-back inertia。
3. **P2**：重建 prime-side first/second trace normalisation。
4. **P3**：獨立推導 $H(\lambda)$ 與 $2/3$。
5. **P4**：獨立解 §7.1 extremal problem，重得 $c_1^*$ 與 $67.25\%$。
6. **P5**：追查／重建 Remark 1.1 的 $0.68185$ extremal law。
7. **P6**：建立 $q(\sigma,k)$ 數值／解析研究平面，分離 support expansion 與 moment expansion。

---

## 6. Lean companion

Anthropic 官方 companion repo：

`https://github.com/anthropics/zeta-23-lean`

後續可在本地端直接 clone，對照 paper 的 Theorems A–E 與 `AUDIT.md`。本包本次以論文 PDF 與研究重建為主，未鏡像完整 repo。
