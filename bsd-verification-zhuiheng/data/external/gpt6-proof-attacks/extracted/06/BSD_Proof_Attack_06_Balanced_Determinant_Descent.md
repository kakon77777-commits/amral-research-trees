# BSD 證明攻擊 06：固定標量、cyclotomic 切向障礙與平衡行列式下降

2026-09-12。Neo.K／EveMissLab 與 GPT 的研究工作稿。

本稿沿用 Attack 05 的算術輸入與推導，不重播舊證書。這輪實際嘗試的是從 cyclotomic Kato 類走到複數主項。直接把整個 cyclotomic 一次變形升成通常的幾何 motive，會在 Hodge–Tate 條件失敗；本文給出該失敗的算子計算。隨後改走正、反扭曲配對與行列式下降，證明局部障礙在係數配對中消去，並構造一個不依賴生成元、Mordell–Weil 基底及週期尺度的 $11$-adic 行列式元素。

本文沒有完成這個元素的有理下降或複數互反律。已推導的命題、失敗的構造與尚待證明的橋接分別明列；這是可供外部審查的探索稿，並非完整 BSD 證明。

## 1. 固定輸入，將任意 unit 尺度改成明確規範

固定

$$
E:y^2+y=x^3+x^2-2x,
\qquad N=389,\qquad p=11,
\qquad P=(0,0),\quad Q=(1,0).
$$

令

$$
O=\mathbb Z_{11},\quad K=\mathbb Q_{11},\quad
M=E(\mathbb Q)\otimes O=OP\oplus OQ,
\quad M_{\mathbb Q}=E(\mathbb Q)\otimes\mathbb Q.
$$

沿用 $\operatorname{Sha}(E/\mathbb Q)[11^\infty]=0$、大殘餘像、ordinary 且 non-anomalous、$a_{11}=-4$、以及 $389$ 處局部修正為 unit 的輸入。令

$$
\gamma\longleftrightarrow12,\qquad t=\gamma-1,\qquad
\omega=\frac{dx}{2y+1},\qquad
\ell=\frac{\log_\omega}{11}.
$$

Attack 05 給出的新局部輸入是

$$
(\ell(P),\ell(Q))\equiv(4,10)\pmod{11}.
$$

所以 $\ell$ primitive，且 $\ell(P)$ 是 unit。沿用該稿得到的高度非退化及精確消失階：

$$
R_{11,\gamma}:=\det H\in O^\times,
\qquad L_{11}(E,t)=a_2t^2+O(t^3),\qquad a_2\in O^\times.
$$

以下 $h$ 與 $H$ 使用 Burns–Kurihara–Sano 的負 Bockstein convention。若將 Attack 05 的正 Bockstein 矩陣直接搬來，則此處 $H=-H_\gamma$；秩二 determinant 相同。這個符號調整不影響該稿的非退化與整格結論，但固定字面相等式時必須記錄。

週期也固定：取正向 rational Betti cycle $\delta^+$，令

$$
\Omega=\int_{\delta^+}\omega>0.
$$

可選 $\Omega=\int_{E(\mathbb R)}|\omega|$，對應 BSD 的實週期慣例；不同文獻若取單一實成分的 primitive period，必須把有理倍數一併搬移。本文不把這個倍數藏進未標記的 unit。

以此週期定義 primitive ordinary $p$-adic $L$ 函數，並令 $z^\dagger_\infty$ 為同一週期、已去 smoothing 與 away-from-$p$ Euler 因子的標準 Kato 類，選相容 Coleman convention 使

$$
\operatorname{Col}(z^\dagger_\infty)=L_{11}(E,t).
$$

若原群作用使用 involution，必須同時反轉所有類與 Coleman 公式。本文的 $\dagger$ 記號用來區別「已固定尺度的類」與前稿只指定到 unit 的類。這是數學規範，並不表示本輪已數值算出 canonical 模符號尺度或 Kato 座標。既有 primitive lattice 輸入保證所作尺度搬移是 $O$-unit。

令

$$
\kappa^\dagger=\left.(z^\dagger_\infty/t)\right|_{t=0}\in M.
$$

此導出類的存在與 primitivity 沿用 Attack 05。

## 2. 精確局部因子：為何出現的是 16

令 $\alpha$ 為 ordinary unit root、$\beta=11/\alpha$，所以

$$
\alpha+\beta=-4,\qquad \alpha\beta=11,\qquad
\alpha\equiv7\pmod{11}.
$$

定義

$$
e_{11}=\left(1-\alpha^{-1}\right)^2,
\qquad
c_\alpha=\left(1-\alpha^{-1}\right)
             \left(1-\beta^{-1}\right)^{-1},
\qquad \theta_\alpha=c_\alpha/11.
$$

其中 $e_{11},\theta_\alpha\in O^\times$，而 $v_{11}(c_\alpha)=1$。

**命題 2.1。** 在第 1 節的規範下，

$$
h(x,\kappa^\dagger)=\theta_\alpha^{-1}a_2\ell(x)
\qquad(x\in M).
$$

**論證。** 使用 [BKS I，Theorem 6.2 與 §6.4 的 Rubin 導數公式](https://arxiv.org/html/1910.07404v2#S6.SS2)。其局部乘數為 $c_\alpha^{-1}$，作用於 $\log_\omega(x)$ 與 $p$-adic 二次首項。代入 $\log_\omega=11\ell$ 即得上式。該定理所需的自由性、正秩及 $11$-primary Sha 有限性均包含於本例沿用輸入；away-from-$p$ 的 unit Euler 因子可在類與 $L$ 函數兩側相容消去。此處使用的是 Rubin 公式，不使用該文的 generalized Perrin-Riou 猜想。證畢。

也可直接從局部 Tate pairing 看出 $\theta_\alpha$：形式群點 $c$ 若滿足 $\log_\omega(c)=11$，其對偶座標為 $\ell$；Coleman 在 trivial branch 使用的點，其形式對數為 $c_\alpha$。兩個局部座標的倍率恰為 $c_\alpha/11$。此數值亦見 [Kataoka，Theorem 6.4 證明中的式 (6.8)–(6.10)](https://arxiv.org/html/2008.02422v1#S6)。

寫成向量形式並使用 $H$ 可逆，得到沒有任意基底 unit 的公式

$$
\kappa^\dagger
=\frac{a_2}{\theta_\alpha R_{11,\gamma}}
  \operatorname{adj}(H)\ell.
$$

定義固定基底下的 scalar

$$
\mathfrak s_{11}:=
\frac{a_2}{e_{11}R_{11,\gamma}}\in O^\times.
$$

**引理 2.2。** 有精確等式

$$
\frac{e_{11}}{\theta_\alpha}
=11\left(1-\alpha^{-1}\right)\left(1-\beta^{-1}\right)
=11+1-a_{11}=16.
$$

**證明。** 展開乘積，使用 $\alpha\beta=11$ 及 $\alpha+\beta=a_{11}$：

$$
11\left(1-\frac{\alpha+\beta}{\alpha\beta}
           +\frac1{\alpha\beta}\right)
=11-a_{11}+1.
$$

證畢。因此

$$
\boxed{\kappa^\dagger
=16\mathfrak s_{11}\operatorname{adj}(H)\ell.}
$$

這裡精確求出的是局部 multiplier $16$。$\mathfrak s_{11}$ 仍未算出，更未證明它有理。尤其不能把「局部因子是 $16$」改寫成「canonical Kato multiplier 已證為 $16$」；後者額外要求 $\mathfrak s_{11}=1$。

對一般 good ordinary、non-anomalous 素數 $p$，同一消去給出 $p+1-a_p=\#E(\mathbb F_p)$。這不是僅在某個模數下成立的近似。

## 3. 伴隨矩陣消去局部高度修正

這一段是之後做幾何下降可直接使用的代數片段。

**引理 3.1。** 設 $A$ 是任意交換環，$H$ 是對稱二階矩陣，$l$ 是二維 column。則對任意 $c\in A$，

$$
\operatorname{adj}(H+c,ll^{\mathsf T})l
=\operatorname{adj}(H)l,
$$

且

$$
\det(H+c,ll^{\mathsf T})
=\det H+c,l^{\mathsf T}\operatorname{adj}(H)l.
$$

**證明。** 寫

$$
H=\begin{pmatrix}a&b\\b&d\end{pmatrix},\qquad
l=\begin{pmatrix}x\\y\end{pmatrix}.
$$

第一個式子的左邊是

$$
\begin{pmatrix}
(d+cy^2)x-(b+cxy)y\\
-(b+cxy)x+(a+cx^2)y
\end{pmatrix}
=\begin{pmatrix}dx-by\\ay-bx\end{pmatrix}.
$$

第二式直接展開 determinant，二次 $c^2x^2y^2$ 項相消。兩式都是多項式恆等式，不必反轉 $\det H$。證畢。

**推論 3.2。** 若一項局部高度修正是經過 $\ell$ 的對稱雙線性形式，即

$$
h_c(x,y)=h(x,y)+c\ell(x)\ell(y),
$$

則 $\operatorname{adj}(H_c)\ell$ 不變。這適用於所有已知會因子化為上述形式的局部 splitting 改變；本文不以代數引理代替特定高度理論中「改變確實有此形狀」的另行證明。

更進一步，第 2 節的類滿足

$$
h_c(x,\kappa^\dagger)
=16\mathfrak s_{11}\det(H_c)\ell(x).
$$

理由是將 $\kappa^\dagger$ 的精確式子代入，並用引理 3.1。只要 $\det H_c\ne0$，比值

$$
\frac{h_c(x,\kappa^\dagger)}
{16\det(H_c)\ell(x)}=\mathfrak s_{11}
$$

與 $c$ 無關。即使某個 $H_c$ 退化，伴隨矩陣向量本身仍由多項式式子定義且不變。

這使我們可以先以伴隨矩陣 contraction 追蹤類，再處理局部高度選擇。直接只看 regulator determinant，則會保留額外的 splitting 依賴。

## 4. 直接 motivic 一次變形為何失敗

令 $\chi_{\rm cyc}$ 為 $11$-adic cyclotomic character。此節先反轉 $11$，在 $K$ 上研究 Hodge–Tate 性；所用的參數變換不被宣稱為 $O$ 上的整同構。

在恆等 character 附近，取 weight parameter

$$
w=\frac{\log(1+t)}{\log_{11}(12)}.
$$

對偶數主分支，universal character 可寫為

$$
\psi_w(g)=\exp\bigl(w\log_{11}\langle\chi_{\rm cyc}(g)\rangle\bigr).
$$

在 $A=K[\varepsilon]/(\varepsilon^2)$ 中取 $w=\varepsilon$，得到一個二維 $K$-表示 $J$：

$$
\rho_J(g)=
\begin{pmatrix}
1&\log_{11}\langle\chi_{\rm cyc}(g)\rangle\\
0&1
\end{pmatrix}.
$$

**命題 4.1。** $J$ 不是 Hodge–Tate，因此不是 de Rham。對 $V=T_{11}(E)\otimes K$，$V\otimes_KJ$ 也不是 Hodge–Tate。

**證明。** 在 cyclotomic 商的充分小開子群上，

$$
\log\rho_J(g)=
\log_{11}\chi_{\rm cyc}(g)
\begin{pmatrix}0&1\\0&0\end{pmatrix}.
$$

故其 Sen 算子為

$$
\Theta_J=\begin{pmatrix}0&1\\0&0\end{pmatrix},
\qquad \Theta_J\ne0,\qquad \Theta_J^2=0.
$$

它的 characteristic polynomial 和 minimal polynomial 均為 $X^2$，不半單。Hodge–Tate 的 Sen 判準要求算子半單且特徵值為整數；參見 [Brinon–Conrad，CMI notes，§15.1、Exercises 15.5.3–15.5.4](https://math.stanford.edu/~conrad/papers/notes.pdf#page=286)。

$V$ 本身 Hodge–Tate，Sen 算子有兩個相差一的特徵值。張量積算子為

$$
\Theta_{V\otimes J}=\Theta_V\otimes1+1\otimes\Theta_J.
$$

在 $\Theta_V$ 的每個特徵空間上，第二項留下非零 Jordan 塊，所以仍不半單。取 inverse universal character 只會改變該 nilpotent 項的符號。證畢。

因此，若要求一個通常的幾何 motive／幾何來源的混合物件，其整個 étale realization 正是這個 first jet，構造已在局部必要條件失敗。幾何 étale cohomology 的 de Rham 性不能套用到此表示上。

這不妨礙在 Iwasawa cohomology 中定義 $z^\dagger_\infty/t$，也不否認個別 geometric specialization 或廣義 Kato 類的構造。它只排除以下直接論法：

「整個 cyclotomic first jet 是通常的幾何 motive，因此可以把該 first jet 的 p-adic 比較原封不動搬到複數 realization。」

錯誤已定位在這一句的前提，而不在 Attack 05 的整除或 Bockstein 計算。

## 5. 正、反扭曲配對：局部障礙確實可消去

對任意有限階截斷 $A_m=K[[t]]/(t^m)$，令 $A_m(\psi)$ 與 $A_m(\psi^{-1})$ 為相反 universal characters 的 rank-one $A_m$-表示。

**命題 5.1。** 有 canonical $G_{\mathbb Q}$-equivariant 同構

$$
\bigl(V\otimes_K A_m(\psi)\bigr)
\otimes_{A_m}
\bigl(V\otimes_K A_m(\psi^{-1})\bigr)
\simeq (V\otimes_KV)\otimes_K A_m,
$$

其中右側 $A_m$ 的 Galois 作用平凡。

**證明。** 映射將 $(v\otimes a)\otimes(w\otimes b)$ 送到 $(v\otimes w)\otimes ab$。Galois 作用中的兩個 scalar 乘積為 $\psi(g)\psi(g)^{-1}=1$。這是所有階的恆等式，不只消去一次項。證畢。

右側係數表示是 $E\times E$ 的 Künneth motive 的 realization 加上平凡重數，因此第 4 節的 nilpotent Sen 障礙不再存在。這給出可採用的係數層級幾何路徑：先配對相反扭曲，再求 motivic 來源。

同樣地，若把 $J$ 視為二維 $K$-表示，則

$$
\det_KJ=K,\qquad
\det_K(V\otimes_KJ)=(\det_KV)^2.
$$

因此 top determinant 也看不見該 nilpotent 項。但必須區分 $\det_K$ 與 rank-one $A$-表示的 $\det_A$：後者仍是原來的 $\psi$，並沒有消失。本文沒有用前者偷換後者，更沒有從係數表示的 determinant 直接斷言全域 Selmer determinant 已有理下降。

### 5.2 配對以後，普通 cup product 又為何不夠

對本例的有限 Selmer 類 $x,y\in M\otimes_OK$，考慮 Weil pairing 收縮後的 cup product

$$
x\cup_e y\in H^2(G_{\mathbb Q,S},K(1)).
$$

**命題 5.2。** 這個普通 cup product 是零。

**證明。** 每個局部 finite 條件與其 Tate dual 互為正交；以主極化識別後，兩個 finite 類的局部 cup product 為零。在 away-from-$11$ 處，也可直接使用 rational local finite subgroup 的消失。另一方面，對 $K(1)$ 的全域 $H^2$，局部化到所有相關有限素點是單射：由 Kummer 序列，有限的 $S$-ideal class group 在反轉 $11$ 後不貢獻；剩下的是 Brauer 群的 Tate module，使用 Brauer–Hasse–Noether 的局部單射。故全域 cup product 為零。這些對偶與局部化性質可對照 [Milne，Arithmetic Duality Theorems，I.4、I.6](https://www.jmilne.org/math/Books/ADTnot.pdf)。證畢。

因此新的幾何攻擊必須保留「零 cup product 的消零資料」——即選定 null-homotopy 及其局部比較所產生的 secondary regulator。Poincaré biextension 與高度正是這類次級資料的幾何模型。只把兩個類作普通 cup product，再取 determinant，會在這一步得到零。

第 3 節說明，若局部選擇的差異經由 $\ell$ 因子化，伴隨矩陣 contraction 可以消去這個差異。這是改走 secondary pairing／determinant 的實質理由；尚未構造出 Kato 特定的 rational secondary 類。

## 6. 建立固定的 rational line 及其 p-adic 元素

定義一維 rational line

$$
\mathscr D_{\mathbb Q}
=\left(\bigwedge^2_{\mathbb Q}M_{\mathbb Q}\right)^{\otimes2}
\otimes_{\mathbb Q}H_1(E(\mathbb C),\mathbb Q)^+.
$$

它是此處固定 polarization 後的 regulator line 記帳模型；本文沒有無證明地把它等同於整個 Bloch–Kato fundamental line 的全部整結構。

寫

$$
b=(P\wedge Q)^{\otimes2}\otimes\delta^+.
$$

以 Néron–Tate pairing 的 determinant $R_\infty(P,Q)$ 定義實 realization

$$
\rho_\infty:\mathscr D_{\mathbb Q}\otimes\mathbb R\longrightarrow\mathbb R,
\qquad \rho_\infty(b)=\Omega R_\infty(P,Q).
$$

這個映射的定義只用 rational points、Betti cycle 及高度，不用 $L''(E,1)$。

**定義 6.1。** 本輪構造的 $11$-adic 行列式元素為

$$
\boxed{\eta_{11}^{\mathrm K}
=\mathfrak s_{11}b
=\frac{a_2}{e_{11}R_{11,\gamma}},b
\in\mathscr D_{\mathbb Q}\otimes K.}
$$

它亦可由已固定尺度的 derived Kato 類提取：對任意 $x$ 滿足 $\ell(x)\ne0$，

$$
\eta_{11}^{\mathrm K}
=\frac{h(x,\kappa^\dagger)}
{16R_{11,\gamma}\ell(x)},b.
$$

**命題 6.2。** $\eta_{11}^{\mathrm K}$ 不依賴以下相容改變：

1. $M_{\mathbb Q}$ 的基底；
2. $\Gamma$ 的 topological generator；
3. Betti 週期尺度與相應的 $L$ 函數／Kato 尺度；
4. 以 Kato pairing 提取公式計算時，第 3 節形式的局部高度修正，只要修正後 regulator 非零。

**證明。** 若基底變換矩陣為 $A\in\mathrm{GL}_2(\mathbb Q)$，則

$$
H'=A^{\mathsf T}HA,\quad R'_{11,\gamma}=(\det A)^2R_{11,\gamma},
\quad b'=(\det A)^2b.
$$

故比值乘上 $b$ 不變。

若 $\gamma'=\gamma^u$、$u\in\mathbb Z_{11}^\times$，則

$$
t'=ut+O(t^2),\qquad a'_2=u^{-2}a_2,
\qquad H'=u^{-1}H,
\qquad R'_{11,\gamma'}=u^{-2}R_{11,\gamma}.
$$

故仍不變。若 $\delta'^+=c\delta^+$、$c\in\mathbb Q^\times$，則 $\Omega'=c\Omega$、$L'_{11}=c^{-1}L_{11}$，所以 $a'_2=c^{-1}a_2$ 與 $b'=cb$ 抵消。最後，使用由 $\kappa^\dagger$ 提取的公式及推論 3.2。證畢。

使用修正後的高度 $H_c$ 時，第 4 點必須透過 Kato pairing 公式計算。商 $a_2/(e_{11}\det H)$ 原本固定的是 ordinary unit-root 高度；若改用 $H_c$，其 Coleman／analytic 比較也須相容改變，不能固定 $a_2/e_{11}$ 而只換分母。

這是一個真正定義出的、去除上述選擇的 $p$-adic 元素。其有理性仍是一個算術命題：

$$
\eta_{11}^{\mathrm K}\stackrel{?}{\in}\mathscr D_{\mathbb Q}.
$$

一維 rational line 的存在不等於其任意 $K$-點都有 rational 來源。尤其已知 $\mathfrak s_{11}\in O^\times$ 不會自行推出 $\mathfrak s_{11}\in\mathbb Q$。

## 7. 複數端可直接攻的 Mellin kernel

令 $f_E(z)=\sum_{n\ge1}a_ne^{2\pi inz}$ 為 $E$ 的 normalized newform，並定義

$$
\Lambda_E(s)=N^{s/2}(2\pi)^{-s}\Gamma(s)L(E,s).
$$

本例 $389$ 處 split multiplicative，故 functional equation 的 sign 為 $+1$。第 1 節的 $L_{11}(E,0)=0$，配合 trivial-character 插值及 $e_{11}\ne0$，亦給出 $L(E,1)=0$；這裡只使用已知 rational central modular-symbol value 的嵌入。偶 functional equation 於是給出 $L'(E,1)=0$。尚不藉此斷言二次導數非零。

Fricke 關係為

$$
f_E\left(\frac{i}{\sqrt N,y}\right)
=y^2f_E\left(\frac{iy}{\sqrt N}\right).
$$

將 Mellin integral 在 $1$ 處切開、對下半段作 $y\mapsto1/y$，得到

$$
\Lambda_E(1+s)
=\int_1^\infty f_E\left(\frac{iy}{\sqrt N}\right)(y^s+y^{-s})\,dy.
$$

由 cusp 衰減可逐項微分，二次係數因此是

$$
[s^2]\Lambda_E(1+s)
=\int_1^\infty f_E\left(\frac{iy}{\sqrt N}\right)(\log y)^2\,dy.
$$

因 $L(E,1)=L'(E,1)=0$，Gamma 與 conductor 因子的導數不產生額外低階項。所以有精確公式

$$
\boxed{
\frac{L''(E,1)}{2}
=\frac{2\pi}{\sqrt{389}}
\int_1^\infty
f_E\left(\frac{iy}{\sqrt{389}}\right)(\log y)^2\,dy.
}
$$

這是一個已明確給出的複數側目標，不涉及把 $11$-adic 數硬嵌入實數。也可以寫成絕對收斂級數

$$
\frac{L''(E,1)}2
=\frac{2\pi}{\sqrt{389}}
\sum_{n\ge1}a_n
\int_1^\infty e^{-2\pi ny/\sqrt{389}}(\log y)^2\,dy.
$$

本文尚未把這個 kernel 的 period 識別為某個獨立構造的 rational secondary class 的實 regulator；這正是複數端缺少的實質比較。

## 8. 本輪的新攻擊命題與精確未完成處

現在可以把候選橋接寫成一個有固定來源、固定目標的命題。

**攻擊命題 BD6（未證）。** 從原來的 Kato 幾何資料及正、反扭曲的 secondary pairing，構造一個

$$
\eta_{\mathrm{geom}}\in\mathscr D_{\mathbb Q}
$$

使其同時滿足

$$
\eta_{\mathrm{geom}}\otimes1=\eta_{11}^{\mathrm K},
$$

以及

$$
\rho_\infty(\eta_{\mathrm{geom}})
=\frac{2\pi}{\sqrt{389}}
\int_1^\infty
f_E\left(\frac{iy}{\sqrt{389}}\right)(\log y)^2\,dy.
$$

此處「構造」要求給出實際 rational cycle、biextension／secondary morphism 或相應的 determinant 比較，不能以右側 $L$ 值反向定義一個實向量後，宣稱它有 rational 來源。

**命題 8.1（若 BD6 成立的精確後果）。** 在沿用輸入下，BD6 會推出

$$
\operatorname{ord}_{s=1}L(E,s)=2,
\qquad
\frac{L''(E,1)}{2\Omega R_\infty(P,Q)}
\in\mathbb Q\cap\mathbb Z_{11}^\times.
$$

因此會得到本例 classical leading-term rationality 與 $11$-part 的正確 valuation。

**證明。** 寫 $\eta_{\mathrm{geom}}=c b$，其中 $c\in\mathbb Q$。其 $11$-adic realization 給出 $c=\mathfrak s_{11}$，因此 $c$ 非零且是 $11$-unit。再取實 regulator，得到 $L''/2=c\Omega R_\infty$。$\Omega$ 與 Néron–Tate regulator 均非零，所以 $L''\ne0$；結合前節的低階消失即得 rank equality。$11$-primary Sha、Tamagawa 與 torsion 的沿用資料，以及 $P,Q$ 是 $O$-basis，使所需的 $11$-part valuation 恰為零。證畢。

這不會單憑一個素數推出完整 BSD 常數。其他素數、全 Sha 的有限性與全域整格指數仍需各自處理。也不宣稱已把所有曲線的問題化約成一個已解引理。

BD6 的數值內容仍包含本例 rank-two $p$-adic Beilinson 比較及有理下降；僅將它寫成行列式元素不會降低其算術難度。本輪新增的是規範消去、明確的 first-jet 障礙，以及避開該障礙的平衡係數構造，並把下一個待構造物件限制到 secondary determinant。

本輪實際走到的位置如下：

| 構造步驟 | 本輪結果 |
|---|---|
| 固定 Kato／Coleman／週期規範 | 給出精確 $\kappa^\dagger=16\mathfrak s_{11}\operatorname{adj}(H)\ell$ |
| 消除經 $\ell$ 因子化的局部高度修正 | 多項式恆等式已證 |
| 整個 cyclotomic first jet 的通常 motivic 升格 | 被非半單 Sen 算子排除 |
| 正、反扭曲的係數配對 | 所有階 character 因子精確消去 |
| 使用普通 cup product 產生主項 | 得到零；必須保留 secondary 資料 |
| 提取不依賴上述選擇的行列式元素 | $\eta_{11}^{\mathrm K}$ 已定義，獨立性已證 |
| rational secondary lift 與 Mellin kernel 比較 | **尚未構造；BD6 未證** |

所以本輪沒有解出 $\mathfrak s_{11}$，也沒有把複數比較標為完成。真正的新方向是：在配對後的固定幾何係數上，構造 Kato 特定的 secondary determinant 類。第 4 節的失敗告訴我們，要求整個 cyclotomic 變形族先有通常的 motivic 來源，反而要求了不成立的性質。

## 9. 本包的新代數計算

`attack06_algebra.py` 僅用 Python 標準函式庫，進行兩類精確計算：

1. 在 $\mathbb Q[A]/(A^2+4A+11)$ 中，以有理數算術化簡 $e_{11}/\theta_\alpha$，得到 $16$；並展示 ordinary 根的 Hensel residue。
2. 對一般符號矩陣與一般 log 向量，直接化簡第 3 節的兩個多項式恆等式；另列出 first-jet Jordan 塊及正、反 character 的截斷乘積。

這些輸出展示本輪代數，不計算 $H$ 的數值 entries、$a_2$ 的 canonical 精確值、$\mathfrak s_{11}$ 或 BD6 的幾何類。Hodge–Tate 判斷依賴正文引用的 Sen 定理，不是由 Python 模擬 Galois 群。

Windows PowerShell：

```powershell
py -3 .\attack06_algebra.py --output .\attack06_result_local.json
```

macOS／Linux：

```bash
python3 ./attack06_algebra.py --output ./attack06_result_local.json
```

本文為原始 UTF-8 source。正式數學僅使用 `$` 與 `$$`。本輪未改寫既有 canonical frontier；本稿的「已證」指所列前提下的書面推導，不代表已通過獨立形式化或學者審查。
