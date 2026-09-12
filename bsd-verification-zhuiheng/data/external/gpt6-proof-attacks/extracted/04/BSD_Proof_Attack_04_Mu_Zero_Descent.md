# BSD 證明攻擊 04：以 cyclotomic μ = 0 消除整群環分母

2026-09-12。Neo.K／EveMissLab 與 GPT 的研究工作稿。

本稿向前推導一段新的證明。核心成果是：給出 Attack 03 缺少的整群環整除之推導，並完成指定 relaxed 複形的 Kato／cofactor 類比較，精確到整群環 unit。這是建立在明列既有算術輸入及外部定理上的研究稿，尚未經另一次獨立審查。它沒有證明完整 BSD，也沒有關閉原 ledger 中範圍更廣的 R318／R319。

## 1. 本輪結論與固定輸入

固定

$$
E: y^2+y=x^3+x^2-2x,
\qquad E=389a1,\qquad p=11,
$$

$$
O=\mathbb Z_{11},\quad k=\mathbb F_{11},\quad
F=F_{397}F_{991},\quad G=\operatorname{Gal}(F/\mathbb Q)=C_{11}^2,
$$

$$
R=O[G],\quad \Lambda=O[[t]],\quad
\Omega=R[[t]],\quad
X=\gamma-1,\quad Y=\eta-1.
$$

$F_\ell$ 是 $\mathbb Q(\zeta_\ell)$ 的 $11$ 次子擴張。$t=\gamma_{\rm cyc}-1$，cyclotomic 座標取 $\gamma_{\rm cyc}=1+11$。有限 tame 生成元 $\gamma,\eta$ 與 $\gamma_{\rm cyc}$ 是不同的生成元。記 $\epsilon_G:\Omega\to\Lambda$ 為 tame 增廣，$\epsilon_t:\Omega\to R$ 為 $t=0$ 特化。

接受 v1、v2、Attack 03 的下列輸入，本文不重跑其有限證書：

1. $E(\mathbb Q)\otimes O=OP\oplus OQ$，$P=(0,0)$、$Q=(1,0)$；有限殘餘 Selmer 群為 $kP\oplus kQ$。殘餘 Galois 像含 $\mathrm{SL}_2(k)$。
2. $a_{11}=-4$，ordinary unit root $\alpha\equiv7\pmod{11}$。$389$ 處是 split multiplicative，既有局部殘餘上同調消失。
3. 真正全域 Galois 複形的殘餘維數是 $h^1=3,h^2=2,h^0=h^3=0$；在 $11$ 的 ordinary 局部商具有一維 $H^1$，全域到此商的殘餘映射滿射。
4. 對只在 $11$ 施加 Greenberg 條件、在 $397,991$ 保留 relaxed 條件的有限複形，Attack 03 的模型是 $A=(B\ c)$、$q=(0,0,1)$。固定相容基底後，令 $D=\det B$、$h=q(z_{\mathrm K})$，有

$$
\overline D=2XY\pmod{(X,Y)^3},\qquad
\overline h=\kappa XY\pmod{(X,Y)^3},\qquad \kappa\in k^\times.
$$

5. 既有模符號向量 $\lambda$ 是 canonical plus 模符號的非零 unit 倍：$\overline\lambda_{\rm can}=u_0\lambda$、$u_0\in k^\times$。已去除的 Kato smoothing 因子在整群環中是 unit。

輸入 4 保留了輔助局部 torsion，沒有把它投影掉。本文的 $z_{\det}$ 始終由實際複形與 determinant 基底定義；不是以 Kato 類反向定義。

本輪新增的精確有限計算給出

$$
\mu\bigl(L_{11}(E)\bigr)=0,\qquad
\lambda\bigl(L_{11}(E)\bigr)=2.
$$

下文由此推出

$$
h_\infty\in D_\infty\Omega,
\qquad
z_{\mathrm K,\infty}=u_\infty z_{\det,\infty},
\qquad u_\infty\in\Omega^\times.
$$

這裡的最後等式是指定複形下的結论，絕對 canonical scalar 仍未算出。

## 2. 分母消去引理

**引理 2.1。** 設 $A$ 是交換環，乘以 $p$ 單射且 $\bigcap_{n\ge0}p^nA=0$。若 $\overline d$ 是 $A/pA$ 的非零因子，則 $d$ 是 $A$ 的非零因子，且

$$
\boxed{dA[1/p]\cap A=dA.}
$$

**證明。** 若 $dx=0$，模 $p$ 得 $\overline d\,\overline x=0$，故 $x=px_1$。消去 $p$ 得 $dx_1=0$，反覆推出 $x\in\bigcap_np^nA=0$。

若 $h\in dA[1/p]\cap A$，存在 $n\ge0,a\in A$ 使 $p^nh=da$。當 $n>0$，模 $p$ 可知 $a=pa_1$。由 $A$ 無 $p$-torsion，消去一個 $p$ 得 $p^{n-1}h=da_1$。反覆 $n$ 次即得 $h\in dA$。另一個包含顯然。證畢。

這個引理處理的是有界的 $p$-分母。$O[[t]][1/p]$ 不等於允許無界係數分母的 $\mathbb Q_p[[t]]$；本稿只使用前者。

**引理 2.2。** 設 $G$ 是有限交換 $p$-群，$A=\mathbb Z_p[G][[t]]$。若

$$
\overline{\epsilon_G(d)}\ne0\quad\text{in }\mathbb F_p[[t]],
$$

則 $\overline d$ 是 $A/pA$ 的非零因子。因此引理 2.1 適用。

**證明。** 記 $J$ 為 $\mathbb F_p[G]$ 的增廣理想。它是 nilpotent。以 $J$ 過濾 $\mathbb F_p[G][[t]]$，各階商

$$
J^a/J^{a+1}\otimes_{\mathbb F_p}\mathbb F_p[[t]]
$$

都是 $\mathbb F_p[[t]]$ 的有限自由模。在這些階商上，乘以 $\overline d$ 就是乘以非零冪級數 $\overline{\epsilon_G(d)}$，故單射。任意非零元素都有最低非零 $J$-階，因 $J$ nilpotent；其乘積在該階不能為零。因此 $\overline d$ 乘法單射。證畢。

本例可直接使用

$$
\Omega/11\Omega=k[[t]][X,Y]/(X^{11},Y^{11}).
$$

**推論 2.3。** 若 $D_\infty$ 的 tame 增廣具有 $\mu=0$，則

$$
h_\infty\in D_\infty\Omega[1/11]
\quad\Longrightarrow\quad
h_\infty\in D_\infty\Omega.
$$

因此真正需要補出的新條件是 base cyclotomic 的 $\mu=0$，不是直接在非正規整群環上強行相除。Attack 03 的反例 $d=p+X$ 的增廣為 $p$，恰好不滿足本引理的假設。

## 3. 新計算：只用 conductor 121 就偵測到 μ = 0

取 ordinary unit root $\alpha$，滿足

$$
\alpha^2+4\alpha+11=0,\quad
\overline\alpha=7,\quad
\overline{\alpha^{-2}}=9,\quad
\overline{\alpha^{-3}}=6.
$$

ordinary 模符號測度採用

$$
\mu_\alpha(a+p^n\mathbb Z_p)
=\alpha^{-n}[a/p^n]^+
-\alpha^{-n-1}[a/p^{n-1}]^+.
$$

這個測度定義可見 [SageMath 官方文件，measure](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/padic_lseries.html#sage.schemes.elliptic_curves.padic_lseries.pAdicLseries.measure)。本文自行用有限域計算其 $n=2$ 推前；沒有把 Sage 的數值輸出作為證明輸入。

對 $1\le a<121$、$11\nmid a$，令

$$
\omega(a)=a^{11}\pmod{121},\qquad
a\omega(a)^{-1}=12^{j(a)}=1+11j(a)\pmod{121}.
$$

$\omega(a)$ 是 mod $121$ 的 Teichmüller lift；$0\le j(a)\le10$。把十個 Teichmüller 類推到同一 cyclotomic 類，得到

$$
c_j=\sum_{j(a)=j}
\bigl(9\lambda(a/121)-6\lambda(a/11)\bigr)\in k.
$$

`cyclotomic_mu.py` 以繼承的 Farey／Manin 慣例計算這 $110$ 項，所得群基底係數是

$$
(c_0,\ldots,c_{10})=(4,0,7,0,4,0,7,2,2,7,0).
$$

代入 $\gamma_{\rm cyc}=1+t$，在 $k[t]/(t^{11})$ 中得到

$$
\boxed{
\overline L_{11}^{\lambda}(t)
=2t^2+2t^3+2t^4+5t^6+6t^7+10t^8+7t^9
\pmod{t^{11}}.
}
$$

理由是 mod $11$ 時 $(1+t)^{11}-1=t^{11}$。因此這個有限群環投影真的決定完整測度的前 $11$ 個 mod $11$ 係數，並非浮點外插。

已知 canonical 模符號相差 $11$-adic unit，故其冪級數也相差 unit。常數及一次項為零、二次項非零，精確推出 $\mu=0,\lambda=2$。這裡 $\lambda$ 是 Iwasawa invariant，與模符號泛函的同名記號不同。係數 $2$ 屬於固定向量尺度；canonical 二次係數是 $2u_0$，沒有聲稱 $u_0=1$。不同 Artin 反向慣例可能把 $t$ 換成 $(1+t)^{-1}-1$，不改變這兩個 invariant。

這不單獨決定複數解析秩，也不單獨證明 $p$-adic 的 characteristic-zero 消失階等於 $2$。

## 4. 真實 cyclotomic 複形，不用任意矩陣 lift

令 $T=T_{11}(E)$，$\mathbb T=T\otimes_O\Omega^{\iota}$，其中 $\iota$ 表示 inverse tautological Galois action。取

$$
\Sigma=\{\infty,11,389,397,991\},\quad
C_\infty=\mathbf R\Gamma(G_{\mathbb Q,\Sigma},\mathbb T),
$$

$$
Q_\infty=\mathbf R\Gamma(\mathbb Q_{11},\mathbb T^-),\quad
\mathcal S_\infty=\operatorname{Cone}(C_\infty\to Q_\infty)[-1].
$$

無限處採奇素數下的 Tate 修正。使用連續 Galois cohomology 的 perfectness 與導出 coefficient base change。模極大理想 $(11,X,Y,t)$ 後，殘餘表示、cohomology 和局部映射正是第 1 節的輸入。最小自由模型遂給出

$$
C_\infty\simeq[\Omega^3\xrightarrow{A_\infty}\Omega^2],
\quad Q_\infty\simeq\Omega[-1].
$$

局部 $H^0,H^2$ 的殘餘消失使用 ordinary quotient 的 unramified Frobenius $7\ne1$ 及局部 Tate duality。殘餘局部映射滿射，故其自由模型係數中有 unit；消元後

$$
A_\infty=(B_\infty\ c_\infty),\qquad
q_\infty=(0,0,1),\qquad
\mathcal S_\infty\simeq[\Omega^2\xrightarrow{B_\infty}\Omega^2].
$$

此處兩項在次數 $1,2$。最小模型的基底可選為有限模型基底的 lift；$t=0$ 的導出特化回到 Attack 03 的複形與基底。這是對實際 Galois 複形作 minimal model，而非把任意 $t$-項加進有限矩陣。

Kato 的 cyclotomic norm-compatible 類給出

$$
z_{\mathrm K,\infty}\in H^1(C_\infty)=\ker A_\infty.
$$

沿用整 primitive lattice 和 smoothing 去除，該類在 $\Omega$ 上整。smoothing 因子的總增廣 mod $11$ 為 $3$，因此它在整個局部環 $\Omega$ 中可逆。其 $t=0$ 特化為既有 $z_{\mathrm K}$。

設

$$
D_\infty=\det B_\infty,\qquad
h_\infty=q_\infty(z_{\mathrm K,\infty}),\qquad
v_\infty=
\begin{pmatrix}-\operatorname{adj}(B_\infty)c_\infty\\D_\infty\end{pmatrix}.
$$

伴隨矩陣恆等式給出 $A_\infty v_\infty=0$ 和 $q_\infty(v_\infty)=D_\infty$。我們取 $z_{\det,\infty}=v_\infty$，並隨基底一起搬移 determinant line。

## 5. 把新 μ = 0 接到算術行列式

記

$$
B_0=\epsilon_G(B_\infty),\quad D_0=\det B_0,
\quad h_0=\epsilon_G(h_\infty),\quad C_0=C_\infty\otimes_\Omega^{\mathbf L}\Lambda.
$$

### 5.1 外部定理只用一側

我們使用 Kato 的 cyclotomic 一側界，方向明確為

$$
\operatorname{char}_{\Lambda}H^2(j_*T)
\ \mid\
\operatorname{char}_{\Lambda}\bigl(H^1(j_*T)/\Lambda z_{\rm prim}\bigr).
$$

同時使用其 $H^1$ 的 generic rank $1$ 和 $H^2$ torsion 結論。原始定理是 Kato 2004，Theorems 12.4、12.5；本文讀取的精確重述是 [Kim–Lee–Ponsinet v5，Theorems 1.5、1.11](https://arxiv.org/pdf/1909.01764v5)，另可對照 [Fouquet–Wan v3，Theorem 1.4 的 characteristic-ideal 版本](https://arxiv.org/pdf/2107.13726v3#page=5)。本例 $p=11\ge5$、good reduction、殘餘像含 $\mathrm{SL}_2(k)$，滿足所用大像條件。

這個界不假設 BSD 或 main-conjecture 的反向包含。

### 5.2 Euler 因子在高度一素理想 (11) 是 unit

primitive 與 $\Sigma$-開集的 $H^1$ 相同，$H^2$ 的差由 away-from-$p$ 局部 Iwasawa 模給出；其 characteristic ideals 是相應 Euler 因子。這正是 [Kim–Lee–Ponsinet v5，Proposition 5.1、Corollary 3.5](https://arxiv.org/pdf/1909.01764v5) 的 localization 比較。

採用 analytic 慣例，good 輔助點的因子可寫作

$$
E_\ell(t)=1-\frac{a_\ell}{\ell}\sigma_\ell^{-1}
+\frac1\ell\sigma_\ell^{-2},\qquad
\sigma_\ell=\gamma_{\rm cyc}^{s_\ell},\quad
s_\ell=\frac{\log_{11}\langle\ell\rangle}{\log_{11}(12)}.
$$

cohomological 慣例可能施以 $\iota$；以下 $\mu$ 結論及兩側整除均在同一慣例下，不能只反轉其中一側。

本例 $\ell\equiv1$、$a_\ell\equiv2\pmod{11}$，且

$$
s_{397}\equiv3,\qquad s_{991}\equiv2\pmod{11}.
$$

所以

$$
\overline E_\ell=(1-(1+t)^{-s_\ell})^2,\quad
\overline E_{397}=9t^2+O(t^3),\quad
\overline E_{991}=4t^2+O(t^3).
$$

兩者均為非零冪級數，因此 $\mu=0$。$389$ 處的因子常數 $1-389^{-1}\equiv9\pmod{11}$，為 $\Lambda$-unit。注意：$E_{397},E_{991}$ 不是 $\Lambda$-unit；它們只是在高度一素理想 $(11)$ 的局部化中成為 unit。保留它們對 $\lambda$ 與有限特化非常重要。

因此在 $\Lambda_{(11)}$，Kato 的 primitive 一側界可直接搬到本文的開集複形和相容的 imprimitive 類。

### 5.3 局部座標本身具有 μ = 0

在 $K=\mathbb Q$ 的 base cyclotomic 塔，non-anomalous 條件為 $a_{11}\not\equiv1\pmod{11}$，本例滿足。ordinary local duality 把 $Q_0$ 的 $H^1$ 識別為 local finite quotient；Coleman 泛函在其整格上取值於 $\Lambda$。可使用 [Kataoka v1，Theorems 4.7、6.4](https://arxiv.org/html/2008.02422v1)：前者給出整 Coleman 同構，後者給出 Kato 互反律。

這裡只在 $K=\mathbb Q$ 套用這兩個定理，沒有套用該文在 $K=F$ 的 equivariant Euler-system 界。後者有額外的 auxiliary local-torsion 假設，本例不能略過。

因本文 $q_0$ 與 Coleman 都是在同一局部自由秩一格上選基，存在 $v_0(t)\in\Lambda^\times$，使

$$
h_0=v_0(t)\left(
E_{397}E_{991}E_{389}L_{11}(E)
\right)^\iota.
$$

conductor／primitive-cycle 慣例亦僅加入已固定的 unit。smoothing 已相容去除。由第 3 節與 5.2，立即得到

$$
\mu(h_0)=0.
$$

順便得到 $\lambda(h_0)=2+2+2=6$，但後续分母消去只需要 $\mu(h_0)=0$。

### 5.4 一側界如何變成 D0 整除 h0

先在 $\operatorname{Frac}(\Lambda)$ 上：Kato 給出 $H^1(C_0)$ 秩一、$H^2(C_0)$ 秩零；且 $q_0(z_0)=h_0\ne0$。故 $q_0$ 在 generic $H^1$ 上同構，$\mathcal S_0$ generic acyclic，從而 $D_0\ne0$。

下面給出需要的局部代數，不把 characteristic ideal 當成未證的元素等式。

**引理 5.1（DVR 上的 cofactor 判準）。** 設 $V$ 是 DVR，$A:V^{r+1}\to V^r$ 的 generic rank 為 $r$。取相容 determinant 基底的 maximal-minor 向量 $v\in\ker A$。若 $z\in\ker A$ 非零且

$$
\operatorname{length}_V((\ker A)/Vz)
\ge\operatorname{length}_V(\operatorname{coker}A),
$$

則 $z\in Vv$。

**證明。** Smith normal form 將 $A$ 化為 $(\operatorname{diag}(d_1,\ldots,d_r)\ 0)$。此時 $\ker A=Ve_{r+1}$，$v$ 為 $(\prod_i d_i)e_{r+1}$ 的 unit 倍。若 $z=be_{r+1}$，給定不等式就是 $\operatorname{ord}(b)\ge\sum_i\operatorname{ord}(d_i)$，因此 $b$ 被 $\prod_i d_i$ 整除。基底搬回即可。證畢。

在 $V=\Lambda_{(11)}$ 使用 Kato 一側界與 5.2，得到 $z_0\in Vv_0^{\det}$。取第三座標：

$$
h_0\in D_0\Lambda_{(11)}.
$$

因此

$$
0\le\mu(D_0)\le\mu(h_0)=0,
\quad\text{故}\quad
\boxed{\overline D_0\ne0.}
$$

由引理 2.2，$\overline D_\infty$ 是 $\Omega/11$ 的非零因子；由引理 2.1，$D_\infty$ 也是 $\Omega$ 的非零因子。至此 Attack 03 的 regularity 假設已被推出，而不是再列為願望。

## 6. Character 分支只負責反轉 11 之後的整除

令 $A=\Omega[1/11]$。因 $|G|=121$ 可逆，$A$ 為正規一維環的有限乘積，按 character 的 Galois 軌道分解。每個分支為

$$
O_\chi[[t]][1/11],
$$

而非整群環中的 primitive idempotent 分解。

對 $\chi\in\widehat G$，$\chi$ 的 conductor prime to $11$、階為 $1$ 或 $11$，且 $\chi$ 為 even。本文 inverse tautological action 的 $\chi$-分支是 $T\otimes\chi^{-1}$；依所引文獻的 cohomological 表示約定，它對應 $f_E\otimes\chi$ 再作 weight-two Tate twist。它在 $11$ 仍有 good crystalline reduction，模 $O_\chi$ 的極大理想時 $\chi\equiv1$，所以殘餘大像條件不變。Kato 的一側界適用。

所需的 $11$-adic 大像也可直接看出：有限 abelian character 在 commutator 上平凡，而 $\mathrm{SL}_2(\mathbb Z_{11})$ 是 perfect；在 cyclotomic kernel 內再施加 $\chi=1$ 不會失去該 $\mathrm{SL}_2$ 像。

現在精確搬移 primitive 與 imprimitive 資料。若 $\chi$ 在某個輔助點有 ramification，該點的 rational inertia invariants 為零；若無 ramification，開集 $H^2$ 多出由 Euler 因子控制的局部 torsion。Kato 的 tame norm／插值關係同時把該 Euler 因子乘到 $z$ 上。相關 imprimitive 定義及係數慣例見 [Kim–Lee–Ponsinet v5，§4.2、§4.5](https://arxiv.org/pdf/1909.01764v5)。

所以在每個 character 分支的每個高度一素點，兩側長度增加相同的 Euler-factor valuation。不同 primitive period lattice 的非零代數常數在反轉 $11$ 後是 unit；smoothing 和 conductor unit 也不改變長度。使用引理 5.1，得到

$$
z_{\mathrm K,\chi}\in
O_\chi[[t]][1/11]\,v_\chi,
\qquad
h_\chi\in D_\chi O_\chi[[t]][1/11].
$$

這裡各高度一局部整除給出全環整除，是因該分支是正規一維環；亦可用其等於所有高度一局部環交集的性質。$D_\chi\ne0$ 已由第 5 節的非零因子性保證。

把有限個 character 軌道合回去：

$$
\boxed{h_\infty\in D_\infty\Omega[1/11].}
$$

有限個分支的分母有共同上界，因而這裡確實只反轉有限次方的 $11$。此步沒有從逐 character 的整性直接斷言整群環整性；缺少的 integral glue 由下一節的分母消去提供。

## 7. 整下降與 unit 比較

**定理 7.1（指定算術複形的比較）。** 在第 1 節明列的既有輸入下，結合第 3 節的新計算與第 5、6 節所引一側定理，存在 $u_\infty\in\Omega^\times$ 使

$$
\boxed{
z_{\mathrm K,\infty}
=u_\infty
\begin{pmatrix}
-\operatorname{adj}(B_\infty)c_\infty\\
D_\infty
\end{pmatrix}.
}
$$

因此 $t=0$ 特化給出 $z_{\mathrm K}=u_Fz_{\det}$，$u_F\in R^\times$。

**證明。** 第 5 節已證 $\overline D_\infty$ 是 mod $11$ 非零因子，第 6 節已證反轉 $11$ 後的整除。引理 2.1 立即給出

$$
h_\infty=D_\infty u_\infty,\qquad u_\infty\in\Omega.
$$

写 $z_{\mathrm K,\infty}=(x_\infty,h_\infty)$。由 cocycle 方程與伴隨矩陣恆等式，

$$
B_\infty\bigl(x_\infty+u_\infty\operatorname{adj}(B_\infty)c_\infty\bigr)=0.
$$

再乘 $\operatorname{adj}(B_\infty)$。$D_\infty$ 是非零因子，故括號內向量為零，得到全域類等式。

尚須證 $u_\infty$ 是 unit。先特化 $t=0$，再模 $11$ 及 $(X,Y)^3$；由第 1 節的兩個非零首項，

$$
\kappa XY
=\overline{u_F}\,(2XY)
=2\epsilon_G(\overline{u_F})XY.
$$

由 $XY$ 在該二次階商中非零，可知

$$
\epsilon_G(\overline{u_F})=\kappa/2\ne0.
$$

這正是 $u_\infty$ 在局部環 $\Omega$ 的 residue field 中的像。因此 $u_\infty\in\Omega^\times$。證畢。

主等式推導中未假設反向 main-conjecture 整除；unit 性使用的是已存在的 finite primitivity 輸入。此方法並不自動將 canonical unit 算成 $1$。

**推論 7.2。** 因 $D_\infty$ 是非零因子，$B_\infty$ 單射。因此對本文指定的複形，

$$
H^1(\mathcal S_\infty)=0,\qquad
\operatorname{Fitt}^0_\Omega H^2(\mathcal S_\infty)
=(D_\infty)=(h_\infty).
$$

這是實際整群環上的 Fitting ideal 等式。定理 7.1 的 $z_{\mathrm K,\infty}$ 生成的是 determinant line 的 cofactor image；它沒有聲稱生成整個 $H^1(C_\infty)$。

## 8. 前沿現在在哪裡

本輪在指定 $E,p,F$ 和上述 relaxed 複形上補出了 Attack 03 的三個缺口：真實 cyclotomic 模型、$D_\infty$ 的非零因子性，以及整群環整除。所得是 **Kato 與該 determinant/cofactor 類相差 unit 的證明稿**。

原 R318 還要求更大的 filtered Selmer／regulator comparison，包括有限條件、torsion、格及增廣階數的精確搬移；本文沒有把這整項改為 closed。原 R319 的複數主項比较也仍然沒有證明。尤其未建立

$$
\frac{L''(E,1)}{2!\,\Omega_E^+\operatorname{Reg}_{\infty}(P,Q)}
\in\mathbb Q,
$$

或其正確算術取值。一个 $11$-adic unit 等式，不能憑自身為任意實數比值賦予 rational 或 $\mathbb Q_{11}$ realization。

下一個可直接進攻的數學命題是：構造本文 determinant line 到具備 rational structure 的 rank-two motivic fundamental line 的比較，使 Kato 的相容插值類在複數實現下給出 $L''(E,1)/2!$，並讓算術 determinant 基底對應 Néron–Tate regulator 與局部因子。此比較必须從獨立構造得出，不能用期望的 BSD 常數定義。若此步成立，才有權把本文的整格控制接到複數主項。

也可以先推 finite filtered 版本以補足 R318；兩條路都必須保留輔助局部 torsion，不能以 ordinary inertia invariants 的非 perfect 模取代本文的全域 perfect 複形。

## 9. 文獻位置與原創性範圍

利用 $\mu=0$ 處理 equivariant singular primes 有既有文獻背景，例如 [Daoud v2，Theorem 3.14](https://arxiv.org/html/2010.16370v2#S3.SS3) 將 $\mu$ 消失與 character-wise divisibility 聯繫。本文不主張這個方向的文獻優先權，也沒有套用其需要整個擴張族假設的結論。

本輪的具體推進是：對目前卡住的標量 $D_\infty$ 給出可逐行證明的 saturation 引理，算出本曲線實際需要的 $\mu=0$，再把它接回原有 cofactor 比較。程式只證明第 3 節的有限求和；Kato 界、局部 reciprocity、perfectness 等屬於文獻與數學推導部分。

## 10. 隨稿程式

`eigenline_input.json` 固定既有 $390$ 維向量及其來源 SHA-256。`cyclotomic_mu.py` 只用 Python 標準函式庫，產生這次新的 $110$ 項 distribution、群基底係數與 $t$-基底係數。`cyclotomic_result.json` 是本輪實際執行的輸出，保留每一項供外部審查。

Windows PowerShell：

```powershell
py -3 .\cyclotomic_mu.py --output .\cyclotomic_result_local.json
```

macOS／Linux：

```bash
python3 ./cyclotomic_mu.py --output ./cyclotomic_result_local.json
```

預期新結果是 `mu: 0`、`lambda: 2`，`t_basis_coefficients` 為 `[0,0,2,2,2,0,5,6,10,7,0]`。這不是原 $392040$ 項 Kurihara 證書的又一次重播。

本文 UTF-8 Markdown 是數學原始稿；公式保留標準 LaTeX `$`／`$$` delimiters。程式及資料與本文一同交付。
