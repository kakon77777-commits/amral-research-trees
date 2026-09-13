# PC-002：相對 regulator 的有限展開與 cup 校準

日期：2026-09-13。研究方向由 Neo.K 指定；目前發話身份 `unresolved`。本輪接續 PC-001，輸入是固定規範的 389.a1 與 19.a1 模符號。程式沒有執行前一驗證線的 producer。

## 本輪結果

定義兩條曲線的 ordinary 函數 \(L_i(t)=L_p(E_i,\sigma_t)\)，以及
\(\lambda_i(t)=L_p(E_i\otimes\chi_8,x^{-1}\sigma_t)\)，其中
\(\sigma_t(12)=1+t\) 且有限角色平凡。令

\[
Q(t)=\frac{L_E(t)\lambda_E(t)}{L_0(t)\lambda_0(t)}.
\tag{1}
\]

已算出 \(Q\bmod(11,t^{121})\)，其前十一個係數為

\[
\boxed{Q(t)=7t^2+10t^3+9t^4+7t^5+6t^6+7t^9+t^{10}
\pmod{(11,t^{11})}.}
\tag{2}
\]

再從 Farey 三角形 cochain 計算 cup pairing，得到固定特徵線的
\(J_E\equiv1\)、\(J_0\equiv3\pmod{11}\)。因此

\[
Q_\cup(t):=\frac{J_0}{J_E}Q(t)
\]

在四條正負特徵線各自作 unit rescaling 下不變；其前十一項是

\[
\boxed{Q_\cup(t)=10t^2+8t^3+5t^4+10t^5+7t^6+10t^9+3t^{10}
\pmod{(11,t^{11})}.}
\tag{3}
\]

完整的 121 個係數、產生各 measure 的 cusp 值與加總項、下一層檢查，以及完整 cup 矩陣，都在本輪 JSON 中。式 (2)–(3) 是具體的解析比較目標；不是由原始 BF 類座標測量出的 regulator。

## 1. 共同 Eisenstein period 在函數層消去

在共同輔助族及同一 \(b_{\mathbf f}^{+}\) frame 中，記 full mixed Perrin–Riou regulator 為 \(R_i(X,t)\)。LR C1.9–C1.11 給出

\[
R_i(X,t)=c_{\mathbf f}(X)\,\mathscr S_i(X,t)\,\mathcal L_i(X,t).
\]

兩個 partner 均固定於權重 2、trivial nebentype，且使用同一 smoothing 整數 5。原文式 (8) 顯示 \(\mathscr S_E=\mathscr S_0\) 是函數恆等，而非僅在中心相等。輔助 tame level 8 與 389、19 分別互質，C1.6 的 Artin 分解在此不需另加共同升級 level 所產生的 tame 因子。故消去共同因子後的 germ 滿足

\[
\left.\frac{D_E}{D_0}\frac{R_E}{R_0}\right|_{X=0}=Q(t),
\qquad D_i=L_p(\operatorname{Ad}\mathbf g_i)(0).
\tag{4}
\]

這裡先在局部分式域相消，再延拓至 X=0；沒有將兩個零值直接相除。PC-001 的非零輸入保證校準分母在中心為 unit（在係數域意義下）。這個純量比值不使用 generic Eisenstein 商映射，所以不重犯 PC-001 指出的提前投影問題。[LR：B3.1、式 (8)、C1.6–C1.11](https://arxiv.org/html/2201.02078v2)

式 (4) 使用文獻定理，而本輪直接計算的是右端。\(D_E/D_0\) 的完整規範尚未與下文的 \(\Gamma_0\) cup 數字接合，因此本稿不將 Q 或 \(Q_\cup\) 稱為已測得的 \(R_E/R_0\)。

## 2. 有限層為何足以證明所列係數

**有限層引理。** 設 \(\mu\) 是 \(\mathbf Z_{11}^{\times}\) 上的整、有界測度，
\(e(x)=\log\langle x\rangle/\log(12)\in\mathbf Z_{11}\)。對 \(m\ge1\)，
\[
\int x^{a}(1+t)^{e(x)}d\mu(x)
\equiv
\sum_{u\in(\mathbf Z/11^{m+1})^\times}
u^a\mu(u+11^{m+1}\mathbf Z_{11})(1+t)^{e_u}
\pmod{(11,t^{11^m})},
\tag{5}
\]
其中 \(a=0\) 或 \(-1\)，且 \(e_u\) 是 \(e(u)\bmod11^m\) 的最小非負代表。

**證明。** 同一 residue ball 中 \(e(x)\) 模 \(11^m\) 固定，而 \(x^a\) 模 11 固定。指數改變 \(11^m z\) 所引入的因子，在特徵 11 中為 \((1+t^{11^m})^z\)，在所列截斷範圍等於 1。由測度加性對所有小球求和即得。指數 0 與 \(11^m\) 在低次項無法區別，卻在 \(t^{11^m}\) 首次分離，因此精度界不能多聲稱一項。證畢。

ordinary 測度採用
\[
\mu_i(a+11^n\mathbf Z_{11})=
\alpha_i^{-n}\Phi_i^+(a/11^n)
-\alpha_i^{-n-1}\Phi_i^+(a/11^{n-1}).
\]
扭曲測度用負號線，先算
\(\Phi_{i,\chi_8}(r)=\sum_{b=1,3,5,7}\chi_8(b)\Phi_i^-(r+b/8)\)，
再使用 \(\alpha_{i,\chi_8}=-\alpha_i\)。\(x^{-1}\) 是完整角色，沒有改成平凡分支或複數中心值。

本輪以 \(11^3=1331\) 層產生 121 個係數，並用 \(11^4\) 層重新計算所有 coarse balls 的和。兩條曲線各有 1210 個 coarse unit balls，每格均同時核對 ordinary 與 twisted measure；另外核對 \(11^2\to11^3\) 的 110 格。所有差異為零。這些有限核對檢查實作；式 (5) 才是它們代表整個有界測度截斷的理由。

## 3. 實際解析資料

係數順序均為 \(t^0,t^1,\ldots,t^{10}\)：

| 函數 | 前十一個係數，mod 11 |
|---|---|
| \(L_E\) | `[0,0,2,2,2,0,5,6,10,7,0]` |
| \(\lambda_E\) | `[5,9,10,6,6,2,0,8,8,9,10]` |
| \(L_0\) | `[9,3,10,3,1,6,9,6,2,0,6]` |
| \(\lambda_0\) | `[4,3,10,9,4,10,2,7,3,8,3]` |

第一列與先前 Attack 04 的結果完全一致，其餘展開及比值為本輪計算。分母常數為 \(9\cdot4=3\pmod{11}\)，故除法不損失上述精度。首項為 \((2\cdot5)/(9\cdot4)=7\)。在明列的整 period 規範下，完整 Q 的 Iwasawa invariants 因而是 \(\mu=0,\lambda=2\)。

**這裡的 2 是 reduction 的最低非零次數／Weierstrass degree。** 單憑 mod 11 展開，不能推出 characteristic-zero 的常數及一次項恰為零；它們可能只是被 11 整除。本稿沒有從有限數據另行證明解析零點階數。

## 4. 命題：Farey cup 校準消去四個特徵線尺度

對 prime level N，以 \(i\in\mathbf P^1(\mathbf F_N)\) 標記 Farey darts；令
\(S(c,d)=(d,-c)\)、\(R(c,d)=(d,-c-d)\)。設 u、v 為 edge-value cochains，滿足
\[
u_i+u_{Si}=0,\quad u_i+u_{Ri}+u_{R^2i}=0,
\]
v 也同樣成立。這裡使用標準的 [Manin presentation](https://wstein.org/books/modform/modform/modular_symbols.html)，並把其對偶看成閉 edge cochains。固定同一個曲面方向，定義
\[
J_N(u,v)=\frac16\sum_i(u_i v_{Ri}-v_i u_{Ri}).
\tag{6}
\]
則式 (6) 給出 compactified modular curve 的 cup pairing，至多差一個所有 level 共同的方向符號；它對 cusp-potential coboundary 為零。

**證明。** 先在 torsion-free cover
\(\Gamma'=\Gamma_0(N)\cap\overline{\Gamma(3)}\) 上做 Farey triangulation。其 degree d 整除 12，所以在 \(\mathbf Z[1/6]\) 及 \(\mathbf F_{11}\) 中可逆。對單一有向三角形，閉 cochains 的相鄰 edge 值設為 \((a,b,-a-b)\)、\((A,B,-A-B)\)。antisymmetrized cup 的貢獻是 \((aB-bA)/2\)。三個 cyclic determinant 值相等，故改成 dart sum 得係數 1/6。若 R 的順序與所選邊界方向相反，只改變全域符號。

cover 把每個 base dart 重複 d 次，pullback 也把 compact-surface cup evaluation 乘 d；兩側除以 d，得到 base 公式。這避開 elliptic stabilizer 的假自由作用。cusps 在 compactification 中為 vertices，cusp-potential 的差是 coboundary；其 cup evaluation 為零。證畢。

u、v 在此是 cochain 值，不是任意的 primal homology 座標。對本輪資料，完整有限矩陣檢查為

| level | genus | Manin cocycle 維數 | cup rank | radical 維數 | 指定正負 eigenlines 的 J |
|---:|---:|---:|---:|---:|---:|
| 389 | 32 | 65 | 64 | 1 | 1 mod 11 |
| 19 | 1 | 3 | 2 | 1 | 3 mod 11 |

兩個 radical 都由 cusp gauge `[-1,0,...,0,1]` 張成。程式先檢查正負輸入及 gauge 確為 cocycles，再作此判定，避免把不屬於 cocycle 空間的向量錯認成 radical 元素。

把四條特徵線各自乘 \(a,b,c,d\in\mathbf Z_{11}^{\times}\)，則
\[
Q\mapsto\frac{ab}{cd}Q,\qquad
J_E\mapsto abJ_E,\quad J_0\mapsto cdJ_0.
\]
所以 \(Q_\cup=(J_0/J_E)Q\) 不變，證明式 (3) 的尺度不變性。這是四個 eigenline frame rescaling 的不變性；**不是任意更換 cochain 代表時所有解析函數都不變**。加 cusp gauge 通常破壞 Hecke eigenproperty；本例 T2 的 cuspidal 特徵值分別為 −2、0，與 gauge 的 3 分離，指定了相應 Hecke lift。

## 5. 與 BSD 目標的距離和下一個具體比較

本輪實際產出一個 C-free 的解析展開，以及進一步消去四個 eigenline unit 尺度的 cup-normalized 展開。數學依據是共同 period 消去、有限層引理及式 (6) 的曲面 cup 計算；不是因程式顯示 PASS 就認定 cohomology 類已構造。

下一個純量比較可明確寫成：以 LR B2.3 的 Petersson/period 規範，識別 \(D_i\) 與 ordinary Euler multiplier、\(J_i\) 之間的 \(\Gamma_0/\Gamma_1\) 及積分常數。當前這項識別尚未完成，不能直接把 \(3/1\) 當成 \(D_0/D_E\)。

再往後仍需真正的 BF leading class、或一個與它同規範的非零 global height pairing，才能用 PC-001 的公式求 \(s_{11}\)。本輪的 cyclotomic t 展開也不是 Attack 10 尚缺的 Coleman-family **權重 X** trace jet。這些不同輸入在輸出 JSON 中保持明列。

## 6. 重跑與核驗

```powershell
python -B code/relative_regulator.py --output data/pc002-relative-regulator.json
python -B code/cup_normalization.py --output data/pc002-cup-normalization.json
```

Python 3.11+，僅用標準函式庫。所有前輪特徵向量及來源 hashes 已凍結在 `data/pc002-inputs.json`；不依賴原始 checkout 的未提交資料。結果包含 1331 層的每一個新 summand 及底層 cusp 值。14641 層作為 refinement 檢查，保留 measure digest 與逐格一致性結果，可由程式重算。

第二上下文核對了 smoothing/tame 因子、有限層精度界及 torsion-free cover 的 cup 證明，並指出兩個已修正的實作／表述缺口：cup 輸入必須先證明為 cocycles；尺度不變性不能擴張為任意 gauge 變更。它沒有宣稱獨立執行所有程式。
