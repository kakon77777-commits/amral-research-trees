# BSD Proof Attack 10：圓分單位校準、crystalline 矩陣與權重 trace 的零同倫

日期：2026-09-12  
狀態：完成新的單位／局部比較計算，以及一階 trace 重建的書面證明；尚未計算真實 Coleman 族的 trace jet 或 meromorphic Eichler–Shimura 常數 $C$。  
交接：使用者回報本地端重新執行近期程式及其他驗證，未見重大失誤。本輪未收到該次日誌，故不將回報擴張為本輪獨立重播。

本輪的實質新增是兩個相接的物件：

1. 一個在 $\mathbb Q$ 上明確定義的圓分單位 $1$-motive。它的 $11$-adic filtered Frobenius 係數可以精確校準，且是 unit。
2. 一個由真實 Eisenstein 族的權重 trace 一階項定義的 cochain；它給出正、反兩側擴張 cup product 的指定零同倫。這個構造有明確重建公式，但其算術 trace 輸入尚未產生。

第二項不是聲稱寫出了新的 BSD 定理。第一項的 period 是單位 motive 的 period，尚未被識別為 Attack 09 的族插值常數 $C$。

## 1. 沿用的邊界與本輪符號

沿用

$$
E:y^2+y=x^3+x^2-2x,\qquad p=11,
\qquad f_\beta=E_2(1,\chi_8)(q)-E_2(1,\chi_8)(q^{11}).
$$

Attack 09 已接受的比例為

$$
B_2=\frac{26C\lambda_8(0)}
{D_E\log_{11}(12)}\kappa^\dagger,
\qquad \lambda_8(0)\equiv5\pmod{11},\qquad D_E\ne0.
\tag{1}
$$

本輪不重跑曲線的 Kurihara、模符號或高度 producer。

記

$$
K=\mathbb Q(r),\quad r=\sqrt2,\quad
\epsilon=1+r,\quad
\xi=\chi_8\chi_{\mathrm{cyc}},\quad
T=\mathbb Q_{11}(\xi).
$$

選定 $r=\zeta_8-\zeta_8^3$，並固定相容的 Tate 基底。$X$ 是權重角色在 $12$ 的值減 $1$；$t$ 是橢圓曲線方向的 cyclotomic augmentation；$t_{\mathrm{dR}}$ 是 Fontaine period。三者不同。

以下 $L_{11}^{\mathrm{std}}(s,\chi_8)$ 明確採用通常的 Kubota–Leopoldt 規範：

$$
L_{11}^{\mathrm{std}}(1-n,\chi_8)
=(1+11^{n-1})\frac{-B_{n,\chi_8}}n,
\qquad n>0,\quad 10\mid n.
\tag{2}
$$

它不是式 (1) 的橢圓曲線扭曲函數 $\lambda_8$。即使兩者模 $11$ 都是 $5$，也沒有將其視為同一個數。

## 2. 精確單位與真正的有理幾何物件

### 命題 10.1：圓分單位與底層 norm 因子

在上述 root 規範下，

$$
u_8=
\frac{(1-\zeta_8)(1-\zeta_8^7)}
{(1-\zeta_8^3)(1-\zeta_8^5)}
=3-2r=\epsilon^{-2}.
\tag{3}
$$

圓分單位 Euler system 的底層 norm 因子是 $1-\chi_8(11)=2$；因此相應的底層單位及有理 Kummer 類為

$$
u_{\mathrm{bot}}=u_8^2=17-12r=\epsilon^{-4},
\qquad
\operatorname{Kum}(u_{\mathrm{bot}})
=-4\operatorname{Kum}(\epsilon).
\tag{4}
$$

**證明。** 分子、分母分別為 $2-r$、$2+r$，故其商是 $3-2r$。再用

$$
(3-2r)(1+r)^2=1,\qquad
(3-2r)^2=17-12r
$$

即可。兩個單位的 field norm 都是 $1$。底層 norm 規範可在 [Bertolini–Castella–Darmon–Dasgupta–Prasanna–Rotger，§1.1](https://web.math.ucsb.edu/~castella/Durham.pdf) 的圓分單位 norm 關係中核對。本例二次特徵等於其逆特徵，沒有額外的 inverse-character 差異。證畢。

取 norm-one torus

$$
\mathcal T=\operatorname{Res}^{1}_{K/\mathbb Q}\mathbb G_m.
$$

因為 $u_{\mathrm{bot}}\in\mathcal T(\mathbb Q)$，得到在 $\mathbb Q$ 上定義的 $1$-motive

$$
\boxed{
M_{\mathrm{bot}}=
[\mathbb Z\longrightarrow\mathcal T],
\qquad 1\longmapsto17-12\sqrt2.
}
\tag{5}
$$

在 $K$ 上用第一個座標 $\mathcal T_K\simeq\mathbb G_m$ 固定 cocharacter，其 Tate realization 滿足

$$
0\longrightarrow T
\longrightarrow V_{11}(M_{\mathrm{bot}})
\longrightarrow\mathbb Q_{11}
\longrightarrow0,
\tag{6}
$$

擴張類正是式 (4)。

$\epsilon$ 的 norm 是 $-1$，所以不能直接把 $1\mapsto\epsilon$ 寫成同一個 norm-one torus 的整 $1$-motive。式 (5) 避開了這個問題；在有理擴張類中除以 $-4$，便得到後文的 $\epsilon$ 規範。因為 $4$ 是 $11$-adic unit，這一步也不引入 $11$-分母。

$\epsilon^\sigma=-\epsilon^{-1}$，而 $-1$ 的有理 Kummer 類為零，因此 $\operatorname{Kum}(\epsilon)$ 確實位於 $\chi_8$ 分量。

### 同一物件的兩種 regulator

在實嵌入 $r>0$ 下，

$$
\frac{\log|u_{\mathrm{bot}}|}{r}
=-4\,\frac{\log(1+r)}r.
\tag{7}
$$

另一方面，Gauss sum 在本例是

$$
G(\chi_8)=\zeta_8-\zeta_8^3-\zeta_8^5+\zeta_8^7=2r.
$$

由展開 $-\log(1-z)=\sum_{m\ge1}z^m/m$，先在 $|z|<1$ 求和再取 Abel 極限，可直接得出

$$
L(1,\chi_8)
=-\frac{1}{2r}
\sum_{a\in\{1,3,5,7\}}\chi_8(a)\log|1-\zeta_8^a|
=\frac{\log(1+r)}r.
\tag{8}
$$

所以式 (7) 等於 $-4L(1,\chi_8)$。這確實是同一個有理單位的實數與 $11$-adic realization 可相互比較的情形；它尚不是橢圓曲線的二階 BSD regulator。

## 3. 局部 crystalline 校準完全寫出來

$2$ 在模 $11$ 非平方，故 $K_{11}/\mathbb Q_{11}$ 是非分歧二次擴張，且 Frobenius 作用於 $r$ 為 $-r$。

選 $T$ 的 Tate 基底 $e_\xi$，令

$$
d_\chi=\frac{r}{t_{\mathrm{dR}}}e_\xi.
$$

則

$$
D_{\mathrm{cris}}(T)=\mathbb Q_{11}d_\chi,
\qquad
\varphi(d_\chi)=-\frac1{11}d_\chi,
\qquad
\operatorname{Fil}^{0}D_{\mathrm{dR}}(T)=0.
\tag{9}
$$

記

$$
L_\epsilon=\frac{\log_{11}(\epsilon)}r,\qquad
L_{\mathrm{bot}}=\frac{\log_{11}(u_{\mathrm{bot}})}r=-4L_\epsilon.
\tag{10}
$$

### 命題 10.2：framed filtered Frobenius 矩陣

對式 (6) 的 crystalline realization，有唯一的 $\varphi=1$ 向量 $d_0$ 映到商的基底 $1$。在 $(d_\chi,d_0)$ 基底中，

$$
\varphi=
\begin{pmatrix}
-1/11&0\\
0&1
\end{pmatrix},
\qquad
\operatorname{Fil}^{0}D
=\mathbb Q_{11}(d_0+L_{\mathrm{bot}}d_\chi),
\tag{11}
$$

且 $\operatorname{Fil}^{-1}D=D$、$\operatorname{Fil}^{1}D=0$。

若改用 filtration 基底

$$
h_{\mathrm{bot}}=d_0+L_{\mathrm{bot}}d_\chi,
$$

則

$$
\boxed{
[\varphi]_{(d_\chi,h_{\mathrm{bot}})}
=
\begin{pmatrix}
-1/11&q_{\mathrm{bot}}\\
0&1
\end{pmatrix},
\qquad
q_{\mathrm{bot}}=-\frac{12}{11}L_{\mathrm{bot}}.
}
\tag{12}
$$

**證明與符號規範。** Kummer cocycle 採用 $g(u^{1/11^m})/u^{1/11^m}$。對局部單位，Bloch–Kato logarithm 在此規範下等於通常的單位 logarithm；非平凡 unramified twist 的對應同構可參照 [Darmon–Rotger，Example 1.6](https://www.math.mcgill.ca/darmon/pub/Articles/Research/70.DR3/DR3.pdf)。

更具體地，在分裂 $\chi_8$ 的非分歧擴張上，令 $\nu_u$ 為標準 Kummer period，滿足

$$
g\nu_u-\nu_u=\kappa_u(g)t_{\mathrm{dR}},\qquad
\varphi(\nu_u)=11\nu_u,\qquad
\theta(\nu_u)=\log_{11}(u).
$$

若 $e_1,e_2$ 為 Kummer extension 的表示基底，則

$$
v=e_2-\frac{\nu_u}{t_{\mathrm{dR}}}e_1
$$

是 $\varphi$-固定的 crystalline lift。因 $\nu_u-\log_{11}(u)$ 屬於第一階 filtration，

$$
v+\log_{11}(u)\frac{e_1}{t_{\mathrm{dR}}}
$$

生成 filtration 零次線。將 $u=u_{\mathrm{bot}}$ 取 $\chi_8$ descent，並用 $d_\chi=r e_1/t_{\mathrm{dR}}$，正好得到式 (11)。$\varphi-1$ 在 subline 上的特徵值是 $-12/11\ne0$，保證 lift 的唯一性。最後

$$
\varphi(h_{\mathrm{bot}})
=d_0-\frac{L_{\mathrm{bot}}}{11}d_\chi
=h_{\mathrm{bot}}-\frac{12}{11}L_{\mathrm{bot}}d_\chi
$$

給出式 (12)。證畢。

### 與 Dirichlet 特殊值的精確識別

Leopoldt 公式在式 (2) 的規範下，連同式 (3) 及 $G(\chi_8)=2r$，給出

$$
L_{11}^{\mathrm{std}}(1,\chi_8)
=-\frac{1+1/11}{2r}\log_{11}(u_8)
=\frac{12}{11}L_\epsilon.
\tag{13}
$$

使用的公式及 Gauss 因子見 [Bertolini 等，Theorem 1.1](https://web.math.ucsb.edu/~castella/Durham.pdf)。因此

$$
\boxed{
q_{\mathrm{bot}}=4L_{11}^{\mathrm{std}}(1,\chi_8).
}
\tag{14}
$$

這不是將兩個未知常數命名成相同值：式 (12) 是 unit extension 的 filtered Frobenius 計算，式 (13) 是已知的特殊值比較。

### 精度與實際數值

本輪直接對 $u_{\mathrm{bot}}^6$ 的 principal-unit logarithm 計算。寫 $w=u_{\mathrm{bot}}^6-1$，則

$$
u_{\mathrm{bot}}^6
=768398401-543339720r,\qquad w\in11\mathcal O_{K_{11}}.
$$

為取得模 $11^N$ 的 log，取級數至 $m=2N-1$。對所有未取項 $m\ge2N$，

$$
v_{11}(w^m/m)\ge m-v_{11}(m)\ge m/2\ge N.
\tag{15}
$$

程式先以整數處理分母中的 $11$ 冪，再反轉剩餘 unit；沒有將不可逆分母直接模除。

本輪 $N=10$，輸出如下。每個同餘均附有其自己的 modulus。

| 量 | 最小非負剩餘值 | modulus |
|---|---:|---:|
| $L_{\mathrm{bot}}$ | $8662686351$ | $11^{10}=25937424601$ |
| $L_\epsilon$ | $17287396863$ | $11^{10}$ |
| $L_\epsilon/11$ | $1571581533$ | $11^9=2357947691$ |
| $L_{11}^{\mathrm{std}}(1,\chi_8)$ | $2353344559$ | $11^9$ |
| $q_{\mathrm{bot}}$ | $2339535163$ | $11^9$ |

特別是

$$
v_{11}(L_\epsilon)=1,\qquad
L_{11}^{\mathrm{std}}(1,\chi_8)\equiv5\pmod{11},
\qquad
q_{\mathrm{bot}}\equiv9\pmod{11}.
\tag{16}
$$

為排除式 (13) 中的 sign／Gauss／Euler 規範錯誤，本輪另計算一個新的 Bernoulli 特殊值：

$$
B_{10,\chi_8}=28730410,\qquad
-\frac{B_{10,\chi_8}}{10}=-2873041\equiv5\pmod{11}.
\tag{17}
$$

由式 (2)，這是 $L_{11}^{\mathrm{std}}(-9,\chi_8)$ 模 $11$ 的值。非平凡 tame 特徵對應整係數的 Kubota–Leopoldt 測度；在固定有限角色分支，所有 $1+11\mathbb Z_{11}$ 上的冪角色模 $11$ 均為 $1$，故它與 $s=1$ 的值模 $11$ 相同。式 (17) 只核查規範與第一位數字，不是聲稱 Bernoulli 一點核對證明了全部九位數字或一般 Leopoldt 定理。

### 推論 10.3：局部整校準是可逆的

在所選 $\mathbb Z_{11}(\xi)$ lattice 下，$\operatorname{Kum}(\epsilon)$ 生成局部 $H_f^1$。

**證明。** 非分歧二次擴張中的 $11$-power Kummer cohomology，可由 multiplicative pro-$11$ completion 描述。在 $\chi_8$ 分量，valuation 部分消失，有限 residue units 的階數與 $11$ 互素。因此通常的 log 將此分量識別為

$$
(11\mathcal O_{K_{11}})^{\chi_8}=11\mathbb Z_{11}r.
$$

式 (16) 表明 $\log_{11}(\epsilon)/(11r)$ 是 unit。因擴張次數 $2$ 可逆，restriction／descent 不增加 $11$-指數。證畢。

這使下面的 Kummer normalization 在局部具有整數意義，並非任選一個可能被 $11$ 整除很多次的非零類。

## 4. 從單位纖維走向真實權重族

選用對偶的 overconvergent representation $V(\mathbf f)^*$，其 Eisenstein 纖維是

$$
0\longrightarrow T\longrightarrow V(f_\beta)^*
\longrightarrow\mathbb Q_{11}\longrightarrow0.
\tag{18}
$$

此擴張 crystalline 且非分裂。相鄰的 compact-support lattice 給出反向、非 de Rham 擴張；reducibility ideal 恰好是 $(X)$。這些是使用 [Loeffler–Rivero，§A5–A6](https://arxiv.org/html/2201.02078v2) 的實際算術輸入，不是從下一節的模型矩陣推出。

全域有限 Selmer 空間

$$
H_f^1(\mathbb Q,T)
\simeq
(\mathcal O_K^\times\otimes\mathbb Q_{11})^{\chi_8}
$$

是一維，且由 $\operatorname{Kum}(\epsilon)$ 張成。因而可以選擇式 (18) 的 graded-piece frames，使其 extension class 恰為 $\operatorname{Kum}(\epsilon)$。

**這個選擇固定了什麼？** 它固定 sub 與 quotient 的相對尺度；共同的 scalar 自同構仍存在。它尚未證明這些 frames 等於由 modular canonical differential 得出的 frames。

令 $J$ 是固定的複共軛。因為 $\xi(J)=-1$ 且 $2$ 可逆，可以在權重族中選 $J$-eigenbasis，使

$$
\rho_X(J)=
\begin{pmatrix}-1&0\\0&1\end{pmatrix}.
$$

在適當局部係數域 $L$ 上完成，寫 $R=L[[X]]$。族的矩陣可寫成

$$
\rho_X(g)=
\begin{pmatrix}
a_g(X)&b_g(X)\\
Xv_g(X)&d_g(X)
\end{pmatrix},
\qquad
a_g(0)=\xi(g),\quad d_g(0)=1.
\tag{19}
$$

設

$$
b_\epsilon(g)=b_g(0),\qquad
v(g)=v_g(0),\qquad
\beta(g)=\frac{v(g)}{\xi(g)}.
\tag{20}
$$

$J$-eigenbasis 給出 $b_\epsilon(J)=0$。對固定的 Kummer class，這個條件也排除了代表 cocycle 的 coboundary 歧義：改變 lift 所增加的 cocycle 是 $z(\xi(g)-1)$，在 $J$ 的值為 $-2z$，所以必須 $z=0$。

在 $(e_1,Xe_2)$ 的相鄰 lattice 中，矩陣變成

$$
\begin{pmatrix}
a_g(X)&Xb_g(X)\\
v_g(X)&d_g(X)
\end{pmatrix}.
$$

因此 $\beta$ 正是反向擴張的 cocycle，其係數角色為 $\xi^{-1}$。這裡有具體的 character、方向與 lattice，不是只說「應該存在某種 secondary class」。

## 5. 新的明確重建公式與零同倫

### 定理 10.4：Kummer 規範下的 trace 重建

在式 (19) 的假設下，令

$$
\mathscr T_X(g)=\operatorname{tr}\rho_X(g),\qquad
A(g)=[X]\,a_g(X),\qquad
F(g)=\frac{A(g)}{\xi(g)}.
$$

則對任意 $g,h$，

$$
a_g(X)=\frac{\mathscr T_X(g)-\mathscr T_X(Jg)}2,
\tag{21}
$$

以及

$$
\boxed{
Q(g,h):=A(gh)-\xi(g)A(h)-\xi(h)A(g)
=b_\epsilon(g)\,v(h).
}
\tag{22}
$$

故只要取 $b_\epsilon(g_*)\ne0$ 的元素 $g_*$，便有

$$
\boxed{
\beta(h)=
\frac{A(g_*h)-\xi(g_*)A(h)-\xi(h)A(g_*)}
{b_\epsilon(g_*)\,\xi(h)}.
}
\tag{23}
$$

更進一步，在通常的 inhomogeneous cochain 規範下，

$$
\boxed{
b_\epsilon\smile\beta=-\delta F.
}
\tag{24}
$$

**證明。** 因 $\rho_X(J)$ 已對角化，$\mathscr T_X(Jg)=-a_g(X)+d_g(X)$，立即得到式 (21)。

矩陣乘法的左上角給出

$$
a_{gh}(X)=a_g(X)a_h(X)+Xb_g(X)v_h(X).
$$

取 $X$ 一次係數，即得式 (22)，再除以非零 pivot 得式 (23)。

同一乘法在右上角及左下角的最低次係數分別給出

$$
b_\epsilon(gh)=b_\epsilon(g)+\xi(g)b_\epsilon(h),
$$

$$
v(gh)=v(g)\xi(h)+v(h).
$$

故

$$
\beta(gh)=\beta(g)+\xi(g)^{-1}\beta(h).
$$

用 $T\otimes T^{-1}\simeq L$ 的自然配對，cup product 的值是

$$
(b_\epsilon\smile\beta)(g,h)
=b_\epsilon(g)\xi(g)^{-1}\beta(h)
=\frac{b_\epsilon(g)v(h)}{\xi(g)\xi(h)}.
$$

另一方面，把式 (22) 除以 $\xi(g)\xi(h)$ 得

$$
F(gh)-F(g)-F(h)
=\frac{b_\epsilon(g)v(h)}{\xi(g)\xi(h)}.
$$

而對 trivial-coefficient $1$-cochain，

$$
(\delta F)(g,h)=F(h)-F(gh)+F(g).
$$

這正是式 (24)。證畢。

### 這個定理增加的資訊

式 (24) 不只說 cup product 在 $H^2$ 中是零；它指定了由權重族所選的零同倫 $-F$。兩個任意零同倫的差可以是 $1$-cocycle，而式 (21) 從固定 trace 與固定 $J$ 選出具體的 $F$。

式 (22) 也說明矩陣 $(Q(g_i,h_j))$ 的 rank 至多為一。在有實際算術輸入時，可以用另一個非零 row pivot 重建同一個 $v(h)$；這是一個有內容的相容性檢查。

由推論 10.3，取整 Kummer cocycle 並作上述 $J$ normalization 後，存在局部元素 $g_*$ 使 $b_\epsilon(g_*)$ 是 $11$-adic unit。否則其 reduction cocycle 處處為零，與局部 generator 的非零 reduction 矛盾。因此 pivot 原則上可選成不損失 $11$-adic 精度的值；本輪尚未列出此真實 Galois 元素及其 trace。

### 座標與 frame 的行為

改基底為 $(u e_1,v e_2)$ 時，

$$
b_\epsilon\longmapsto(v/u)b_\epsilon,\qquad
v(\,\cdot\,)\longmapsto(u/v)v(\,\cdot\,),
$$

所以 $Q$ 不變。固定 Kummer normalization 後，這個相對 rescaling 已被排除。

若 $X'=sX+O(X^2)$，則

$$
A'=s^{-1}A,\qquad v'=s^{-1}v,\qquad F'=s^{-1}F.
$$

所以內在物件是例如

$$
\beta\otimes\overline X
\in H^1(\mathbb Q,L(\xi^{-1}))
\otimes_L\mathfrak m/\mathfrak m^2,
\tag{25}
$$

而不是忽略權重座標的裸數字 $\beta$。

本定理使用 $V(\mathbf f)^*$ 的 trace。若從 Fourier／Hecke 資料取得的是 $V(\mathbf f)$ 的 trace，必須先用

$$
\operatorname{tr}(\rho^\vee)
=\frac{\operatorname{tr}(\rho)}{\det\rho}
$$

轉換，包含 determinant 的權重導數。不能只搬用同一串 Hecke 數字。

## 6. 新程式實際證明了哪些有限內容

**attack10_unit_tangent.py** 僅使用 Python 標準函式庫，執行三類工作：

1. 在 $\mathbb Z[\zeta_8]/(\zeta_8^4+1)$ 及 $\mathbb Z[\sqrt2]$ 中證明式 (3)–(4) 與 Gauss sum 身份。
2. 執行具有尾項界限的 $11$-adic log，計算式 (12)–(17) 的數值。
3. 用 exact dual numbers $R_1=\mathbb Q[X]/X^2$ 實作式 (21)–(24)，確認矩陣方向、cup 的角色作用與負號、不同 pivot 重建，以及 frame／座標變換。

第三類的輸入明確是自由群代數模型：

$$
\rho(a)=
\begin{pmatrix}2+7X&3+13X\\5X&1+11X\end{pmatrix},
\quad
\rho(b)=
\begin{pmatrix}3+17X&2+19X\\7X&1+23X\end{pmatrix},
\quad
\rho(J)=\begin{pmatrix}-1&0\\0&1\end{pmatrix}.
\tag{26}
$$

它們定義在 $\operatorname{Free}(a,b)*C_2(J)$。程式對 $26$ 個 reduced words 的 $676$ 對組合完成精確檢查，並輸出每對的 $Q$、cup 與 $-\delta F$，供本地端逐項檢查。

例如

$$
Q(a,a)=15,\qquad Q(a,b)=21,
$$

用 $b_\epsilon(a)=3$ 的模型 pivot 還原 $v(a)=5$、$v(b)=7$；改用 $b_\epsilon(b)=2$ 的 pivot 得到相同結果。

**模型不是 Galois 數據。** 式 (26) 的 $2,3,5,7$ 等數字沒有被宣稱是本例的 Coleman-family trace 或 Kummer cocycle 取值。書面定理對真實族的結構性應用使用第 4 節的文獻輸入；程式只對其代數公式作有限演算核查。

程式另把模型的 lower coefficients 改成 $8X,9X$。兩個模型的 $X=0$ 矩陣相同，但 $Q(a,a)$ 從 $15$ 變成 $24$。這只說明「給定殘餘單位擴張」這一項抽象資料並不包含族的一階方向；沒有聲稱同一算術 eigencurve 上存在這兩個不同方向。

## 7. 對 $C$ 的攻擊精確停在哪裡

Attack 09 的未知量來自

$$
c_{\mathbf f}(X)=X^n(C+O(X)),
\qquad
\omega_{\mathbf f}=b_{\mathbf f}^{+}/c_{\mathbf f}.
\tag{27}
$$

本輪已固定一個真正的單位 motive、其局部 filtration、Frobenius 矩陣，以及可用於指定權重族零同倫的 trace 公式。然而，式 (27) 比較的是 classical canonical differential 在族中的 meromorphic 插值。

下列兩個箭頭仍是具體缺口：

| 比較／計算步驟 | 已有內容 | 缺少的精確輸入 |
|---|---|---|
| Kummer 纖維 $\longrightarrow$ 反向擴張的一階方向 | 式 (21)–(24) 的重建與零同倫 | 真實 $\mathscr T_X(g)$、$\mathscr T_X(Jg)$ 模 $X^2$，以及一個可識別的 Kummer pivot |
| 已固定纖維／族資料 $\longrightarrow$ 式 (27) 的 leading period | 單位的 filtered Frobenius 校準與文獻給出的 meromorphic ES 存在性 | 實際 ES comparison map 的 leading jet，含 Tate shifts、Gauss sum、Serre／Ohta 配對及 quotient transport |

單純有有限個 $a_\ell'(0)$，尚不等於已取得式 (23) 所需的所有 Galois word traces $\mathscr T'_0(Jg)$、$\mathscr T'_0(Jgh)$。必須建立與算術 pseudocharacter 的相容識別。本輪程式未越過這一步。

而即使完成 trace 的一階重建，也尚未證明它決定式 (27) 的 $n$ 及 $C$；若需要更高階 ES jet，就必須實際計算或證明階數界。沒有把 $n=1$ 從 reducibility ideal $(X)$ 直接推出來。

### 本輪嘗試但沒有成立的捷徑

把式 (14) 的 unit 稱為 $C$，會跳過上表第二個比較箭頭，因此不成立。

另外，Beilinson–Flach 的 $b_{\mathbf f}^{+}$ 與 Kato 退化論文中的 $a_{\mathbf f}^{-}$ 作用在不同 crystalline 線；後者的 meromorphic 比較係數通常記作 $d_{\mathbf f}$。即使兩篇文獻的 leading constants 都使用字母 $C$，也沒有相等的推論。

相關區別及額外 adjoint simple-zero／非零導數假設，見 [Polo–Rivero，§2.3、Assumption 1.2、§5.5–5.6](https://arxiv.org/html/2501.01514v2)。本輪未驗證這些附加假設，也未取得兩個 period 的配對公式，所以沒有用「兩個常數直接相消」推進式 (1)。

這不是程式運算失敗。本輪 arithmetic 和 algebra-model 計算均成功；未完成的是上述真正的算術 trace 計算與 de Rham／族插值比較。

## 8. 下一個研究目標與狀態

下一輪最直接的工作物件是固定規範的 Eisenstein 族 trace 與 ES map 的 jet，而不是再計算一次 $\epsilon^{24}$ 或曲線的舊 certificate。

式 (23) 提供一個具體切入點：只要產出相容的算術 trace words，便能還原反向擴張與式 (24) 的指定零同倫；接著要把這個 secondary 資料與 meromorphic ES leading map 配對。是否只需一階資料，仍須證明。

本輪已有一個真正能同時談實數和 $11$-adic regulator 的有理單位 motive。下一道需要攻克的是它如何與橢圓曲線側的 Euler-system leading class 相接。沒有把有理單位的存在當作整個橢圓曲線 determinant 已經下降到 $\mathbb Q$。

| 項目 | 狀態 |
|---|---|
| 圓分單位與 norm-one $1$-motive | 精確構造完成 |
| 單位 motive 的局部 filtered Frobenius 校準 | 書面推導與有限計算完成，$q_{\mathrm{bot}}\equiv9\bmod11$ |
| 單位 motive 的實數／$11$-adic regulator 比較 | 本例已明確寫出；使用既有 Leopoldt 公式 |
| 權重 trace 重建與指定 cup 零同倫 | 書面代數證明完成，有限模型演算成功 |
| 真實 Coleman 族 trace jets | 尚未計算 |
| $n,C,B_2$ 座標及 $s_{11}$ | 尚未計算 |
| 橢圓曲線的有理 determinant／複數 leading-term 比較 | 尚未完成 |
| BSD、canonical frontier | BSD 尚未證明；canonical frontier 不更新 |

包內的 JSON 對真實 trace jets、$n$、$C$、$B_2$ 及 $s_{11}$ 均保留為 null。完整書面推導、精確數值、代數模型與未知項各自有明確標記。
