# BSD 證明攻擊 05：rank-two 首項、整高度與輔助 torsion 的接合

2026-09-12。Neo.K／EveMissLab 與 GPT 的研究工作稿。

本文繼續向前推導。目標是把 Attack 04 的 determinant 比較搬到 rank-two regulator，並保留兩個輔助素點產生的整格差。主結果是在明列既有輸入、Kato 一側界與 Selmer 對偶之下的證明稿；尚未經獨立審查。本文沒有宣稱完整 BSD 或複數主項公式已證明。

## 1. 本輪推到的等式

固定

$$
E: y^2+y=x^3+x^2-2x,
\quad E=389a1,\quad p=11,
\quad P=(0,0),\quad Q=(1,0).
$$

令

$$
O=\mathbb Z_{11},\quad k=\mathbb F_{11},\quad
M=E(\mathbb Q)\otimes O=OP\oplus OQ,
\quad \Lambda=O[[t]],\quad t=\gamma_{\rm cyc}-1,
$$

其中 $\gamma_{\rm cyc}$ 對應 $1+11=12$。使用 Néron differential

$$
\omega=\frac{dx}{2y+1},\qquad
\ell(R)=\frac{\log_\omega(R)}{11}.
$$

本文的 $h_\gamma$ 是以 $t$-係數表示、由 ordinary Selmer Bockstein 及整對偶定義的 cyclotomic 高度。記其在 $P,Q$ 基底的矩陣為 $H_\gamma$。本輪推導給出

$$
\det H_\gamma\in O^\times,
\qquad
L_{11}(E,t)=t^2U(t),\quad U(t)\in\Lambda^\times.
$$

對 primitive cyclotomic Kato 類 $z_{\rm prim,\infty}$，其第一個導出類存在且滿足

$$
\kappa_{\rm prim}
:=\left.\frac{z_{\rm prim,\infty}}{t}\right|_{t=0}
=u_0\operatorname{adj}(H_\gamma)
\begin{pmatrix}\ell(P)\\\ell(Q)\end{pmatrix},
\qquad u_0\in O^\times.
$$

右側以 $P,Q$ 作向量座標。這個式子把 Kato 的導出類接到真正的高度矩陣。$u_0$ 保留 determinant／週期正規化的 unit，沒有被擅自設成 $1$。

此外，若

$$
\Sigma=\{\infty,11,389,397,991\},\qquad T=T_{11}(E),
$$

則原先尚未確定指數的 torsion 被推到精確結論

$$
H^2(G_{\mathbb Q,\Sigma},T)\simeq O\oplus O/11O
$$

作為 $O$-模；此分裂不是 canonical。兩個輔助點的合併格指數則是 $11^2$，必須完整保留於首項比較。

以下逐段給出論證。

## 2. 沿用輸入與本輪唯一的新數值計算

沿用 v1、v2 的算術輸入：$M=OP\oplus OQ$、$\operatorname{Sha}(E/\mathbb Q)[11^\infty]=0$、殘餘 Galois 像含 $\mathrm{SL}_2(k)$、$a_{11}=-4$、$\#E(\mathbb F_{11})=16$。在 $389$ 處 Tamagawa 數為 $1$，相應 $11$-adic 局部修正為 unit。全域沒有 $11$-torsion。

兩個輔助點的局部群之 $11$-部分均為 $k$，既有局部化矩陣是

$$
\begin{pmatrix}1&2\\1&4\end{pmatrix}.
$$

Attack 04 的新計算給出 primitive ordinary 測度

$$
\overline L_{11}^{\lambda}(t)
=2t^2+2t^3+2t^4+5t^6+6t^7+10t^8+7t^9
\pmod{t^{11}},
$$

canonical 尺度相差非零 $k$-unit。因此 $\mu=0,\lambda=2$ 是沿用輸入；本文不重跑那 $110$ 項，更不重跑舊 $392040$ 項 Kurihara 求和。這時尚不能只憑 mod $11$ 資料聲稱 characteristic-zero 消失階為 $2$；第 5 節才補出該推論。

本輪新增的計算是局部 log。因 $\#E(\mathbb F_{11})=16$，$[16]R$ 對 $R=P,Q$ 都進入形式群。若 $s=-x/y$ 為形式參數，則

$$
\log_\omega(s)=s\pmod{11^2}\qquad(s\in11O).
$$

理由是 invariant differential 的形式展開具有 $O$-係數；積分後第 $n$ 項的分母至多加入 $v_{11}(n)$，而 $n-v_{11}(n)\ge2$ 對所有 $n\ge2$ 成立。因此

$$
\ell(R)\equiv\frac{s([16]R)}{16\cdot11}\pmod{11}.
$$

`local_log.py` 用有理數加法與倍點，精確得到：

| 點 | $s([16]R)\bmod121$ | $v_{11}(s([16]R))$ | $\ell(R)\bmod11$ |
|---|---:|---:|---:|
| $P$ | $99$ | $1$ | $4$ |
| $Q$ | $66$ | $1$ | $10$ |

所以

$$
\boxed{\ell:M\twoheadrightarrow O,\qquad
(\overline\ell(P),\overline\ell(Q))=(4,10).}
$$

特別地 $\ker\overline\ell=k(P+4Q)$。完整有理點座標與形式參數保存在 JSON，不使用浮點近似。

## 3. 先在基域構造完整有限條件的 Selmer 複形

本節在 $\Lambda$ 上工作。先將 Attack 04 的 relaxed 全域複形沿 tame 增廣下降到基域的 cyclotomic 塔，再對 $397,991$ 施加通常未分歧條件。這裡係數表示在輔助點未分歧，慣性不變量是自由的 $\Lambda$-模。

這一步不等於將原 $O[C_{11}^2]$-族的非自由慣性不變量先作增廣；兩個操作不能混同。

令 $C_{\rm prim,\infty}$ 為全域 cohomology 在所有 away-from-$11$ 點施加通常有限條件、在 $11$ 尚未施加有限條件的複形。它可用相應 $j_*T$ 的 étale cohomology 表示。令

$$
Q_\infty=\mathbf R\Gamma(\mathbb Q_{11},\mathbb T^-),\qquad
S_{\rm prim,\infty}
=\operatorname{Cone}(C_{\rm prim,\infty}\to Q_\infty)[-1],
$$

其中 $\mathbb T=T\otimes_O\Lambda^\iota$，$\iota$ 表示 inverse tautological action。下標 $0$ 表示導出 $t=0$ 特化。

ordinary quotient 的殘餘 Frobenius 是 $7\ne1$，局部 dual twist 也無不變量，故

$$
Q_\infty\simeq\Lambda[-1],\qquad Q_0\simeq O[-1].
$$

完整的有限條件是 self-dual；本例 non-anomalous，且壞點 Tamagawa 修正為 $11$-unit。由整 Selmer 對偶及既有 Sha 輸入，

$$
H^1(S_{\rm prim,0})=M,\qquad
H^2(S_{\rm prim,0})=M^*:=\operatorname{Hom}_O(M,O),
\qquad H^0=H^3=0.
$$

具體地，Kummer 序列把離散 Selmer 群識別為 $M\otimes_O(\mathbb Q_{11}/O)$；其 Pontryagin dual 是 $M^*$。global duality 將這個 dual 放在 compact Selmer 複形的次數 $2$。away-from-$11$ 的有限條件保留局部 $H^0$，使相關 boundary 項相消；沒有把輔助局部 torsion 當成零。所用基礎為 [Milne，Arithmetic Duality Theorems，I.6](https://www.jmilne.org/math/Books/ADTnot.pdf) 的 Selmer／局部對偶，以及 [BKS I v2，§5.1.1](https://arxiv.org/html/1910.07404v2#S5.SS1.SSS1) 所述 Selmer 複形和導出下降。

選局部商基底，使三角的邊界

$$
\delta:O=H^1(Q_0)\longrightarrow H^2(S_{\rm prim,0})=M^*
$$

滿足 $\delta(1)=\ell$。這個正規化是整的：形式對數將局部 $11$-completion 識別為 $11O$，可取形式點 $c$ 使 $\log_\omega(c)=11$，再以局部 Tate pairing 選對偶基底。邊界與 global duality 的相容性使其作用於 $R\in M$ 正是 $\ell(R)$。

第 2 節證明 $\ell$ primitive，故 $\delta$ 是 saturated injection。三角的長正合列給出

$$
H^1(C_{\rm prim,0})=M,\qquad
H^2(C_{\rm prim,0})=M^*/O\ell\simeq O.
$$

注意 primitive 複形此處沒有 $11$-torsion。這是下一步 minimal model 和首項計算所需的整格結論。

## 4. 兩個輔助素點的格修正與精確 torsion 指數

令 $S_{\rm rel,\infty}$ 為基域 cyclotomic 塔上只在 $11$ 施加有限條件、在 $397,991$ relaxed 的複形。$S_{\rm rel,0}$ 正是先前 tame 增廣後的 relaxed 複形，已有

$$
H^1(S_{\rm rel,0})=M,\qquad
H^2(S_{\rm rel,0})=:L\simeq O^2.
$$

在基域係數上，令

$$
L_\ell=\operatorname{Cone}(U_\ell\to K_\ell),\qquad
U_\ell=\mathbf R\Gamma_{\rm ur}(\mathbb Q_\ell,\mathbb T),\quad
K_\ell=\mathbf R\Gamma(\mathbb Q_\ell,\mathbb T).
$$

局部 inertia cohomology 給出 $L_\ell$ 的兩項自由模型，位於次數 $1,2$，行列式是 Euler 因子 $E_\ell(t)$ 的 unit 倍。在 $t=0$，

$$
H^1(L_{\ell,0})=0,\qquad H^2(L_{\ell,0})\simeq O/11O
\quad (\ell=397,991).
$$

這裡零的是 singular quotient 的 $H^1$；其 $H^2$ 非零，必須留下。$\#E(\mathbb F_{397})=374$、$\#E(\mathbb F_{991})=1045$ 的 $11$-部分均恰為 $11$。Euler／cohomology 的對接可見 [Kim–Lee–Ponsinet v5，Corollaries 3.4–3.5、Proposition 5.1](https://arxiv.org/pdf/1909.01764v5)。

Selmer 條件比較的真正三角為

$$
S_{\rm prim,\infty}\longrightarrow S_{\rm rel,\infty}
\longrightarrow L_{397}\oplus L_{991}\longrightarrow S_{\rm prim,\infty}[1].
$$

導出特化後取 cohomology，得到

$$
0\longrightarrow M^*\xrightarrow{J}L\longrightarrow k^2\longrightarrow0.
$$

**引理 4.1。** 若 $J:O^2\hookrightarrow O^2$ 的 cokernel 為 $k^2$，則

$$
J=11W,\qquad W\in\mathrm{GL}_2(O),\qquad v_{11}(\det J)=2.
$$

**證明。** cokernel 被 $11$ 殺掉，故 $11O^2\subseteq\operatorname{im}J$。兩者在 $O^2$ 的 index 都是 $11^2$，所以相等。選基底便得結論。證畢。

完整與 relaxed 複形到同一 $Q_0$ 的三角相容，因此 relaxed 邊界是

$$
\delta_{\rm rel}(1)=J\ell=11W\ell.
$$

$W\ell$ primitive，故此向量的兩個座標恰有共同 $11$-因子一次。在 $389$ 處，沿用的局部殘餘消失使有限／relaxed 商複形 acyclic，因此這裡 away-from-$11$ 的 relaxed 全域複形確實與 $\mathbf R\Gamma(G_{\mathbb Q,\Sigma},T)$ 識別。再由長正合列，

$$
H^2(G_{\mathbb Q,\Sigma},T)
=\operatorname{coker}(O\xrightarrow{11W\ell}L)
\simeq O\oplus O/11O.
$$

這證明 v2 未知的 torsion 指數恰為 $1$。$\operatorname{Sha}[11^\infty]$ 仍為零；此處的 torsion 來自不同局部條件的複形與邊界，不是新出現的 Sha。

在 analytic Euler 慣例，兩個輔助因子的常數乘積是

$$
\mathcal E(0)=E_{397}(0)E_{991}(0)
=\frac{374}{397}\frac{1045}{991}
=11^2\frac{3230}{393427},
$$

其中最後一個分數在 $O$ 中為 unit，mod $11$ 為 $7$。這與 $v_{11}(\det J)=2$ 一致；兩者的字面等式需沿同一 local determinant 基底搬移，本文需要的是所示格指數。

## 5. 從 μ = 0、λ = 2 推到整高度不退化

### 5.1 實際兩項模型

由第 3 節的 cohomology、perfectness 與 coefficient base change，可選 minimal free models

$$
C_{\rm prim,\infty}\simeq[\Lambda^2\xrightarrow{d(t)}\Lambda],
\qquad
S_{\rm prim,\infty}\simeq[\Lambda^2\xrightarrow{B(t)}\Lambda^2],
$$

均位於次數 $1,2$。這個 minimal model 的尺寸有整係數上的理由：先導出模 $t$，再導出模 $11$，第 3 節的自由 cohomology 給出的 residue-field 維數分別為 $(2,1)$ 和 $(2,2)$，其餘次數為零。對 bounded free model 消去含 unit 的 differential entries 後，剩下的 minimal model 模極大理想時 differential 為零，所以其各次數 rank 正是上述維數。這裡沒有以 rational rank 代替整模型。

局部映射在模型中為 row $q(t):\Lambda^2\to\Lambda$，並可按 cone 的 orientation 寫

$$
B(t)=\begin{pmatrix}d(t)\\q(t)\end{pmatrix}.
$$

因 $H^1(C_{\rm prim,0})=M$ 秩二、$H^2(C_{\rm prim,0})$ 秩一，$d(0)=0$。全域到局部 singular quotient 的映射在 $t=0$ 為零，因其像是 $\ker\delta=0$，所以 $q(0)=0$。因此

$$
d(t)=t(a_1(t),a_2(t)),\qquad
q(t)=t(b_1(t),b_2(t)),\qquad B(t)=tV(t).
$$

特別地 $\det B(t)=t^2\det V(t)$。這是整係數上的真消失階下界。

### 5.2 一側界已足以迫使 V 可逆

Kato 的 $H^1$ generic rank 一、$H^2$ torsion 與一側 characteristic-ideal 界，以及 ordinary Coleman 的整同構和互反律，給出

$$
h(t):=q(t)z_{\rm prim,\infty}
=v(t)L_{11}(E,t)^\iota,\qquad v(t)\in\Lambda^\times,
$$

和

$$
h(t)=\det B(t)\,u(t),\qquad u(t)\in\Lambda.
$$

精確來源為 [Kim–Lee–Ponsinet v5，Theorems 1.5、1.11](https://arxiv.org/pdf/1909.01764v5) 及 [Kataoka v1，Theorems 4.7、6.4 在 $K=\mathbb Q$ 的情形](https://arxiv.org/html/2008.02422v1)。good ordinary、non-anomalous、大殘餘像及整 primitive lattice 均使用前述輸入。

這個元素整除可直接在 $\Lambda$ 的每個高度一 DVR 上證明：把 $d(t)$ 作 Smith normal form，Kato 界表示 $z$ 相對 kernel 基底的 valuation 至少為 cokernel 的長度，故它被 maximal-minor 向量整除。再用正規環 $\Lambda$ 等於各高度一局部環的交集。generic 的 $\det B\ne0$ 則由 Kato 的秩結論與非零局部值 $L_{11}\ne0$ 推出。本文沒有從等式主猜想出發。

因此

$$
h(t)=t^2\det V(t)u(t).
$$

由沿用的 mod $11$ 計算，$h(t)$ 的二次係數是 unit，前面乘上的 Coleman 及 period 因子亦為 unit。比較上式的二次係數得

$$
\det V(0)u(0)\in O^\times.
$$

兩個因子都在 $O$，所以兩者都是 unit。故

$$
V(t)\in\mathrm{GL}_2(\Lambda),\qquad u(t)\in\Lambda^\times.
$$

並且

$$
\boxed{L_{11}(E,t)=t^2U(t),\qquad U(t)\in\Lambda^\times.}
$$

這一次得到的是 characteristic-zero 的確切 $t$-消失階 $2$，不是只說 mod $11$ 的 $\lambda=2$。

### 5.3 高度矩陣與整複形的形狀

在 $P,Q$ 與其 dual 基底下，$V(0)=B'(0)$ 就是 Bockstein 的矩陣，再經整 global duality 得 $H_\gamma$。兩個目標格的識別是 $O$-同構，故

$$
\boxed{\det H_\gamma\in O^\times.}
$$

這個 pairing 使用 actual ordinary Selmer complex，是 Nekovář cyclotomic 高度的 $t$-係數形式。本文採正邊界；[BKS I v2，§5.1.1](https://arxiv.org/html/1910.07404v2#S5.SS1.SSS1) 採負邊界，所以可相差整體負號。秩二 regulator 不受此符號影響。對稱性是該高度的性質。

若改用明確定義的 log normalization

$$
h_{\log}(x,y)=\log_{11}(12)h_\gamma(x,y),
$$

則

$$
v_{11}\bigl(\det(h_{\log}(P_i,P_j))\bigr)=2.
$$

這裡沒有聲稱已數值算出高度矩陣每個 entry；非退化和 determinant valuation 是從整複形與一側界推出。

還有更強的複形結論。用 $V(t)^{-1}$ 改變定義域基底，可以同時化成

$$
B(t)=tI_2,\qquad d(t)=(t,0),\qquad q(t)=(0,t).
$$

此 normal form 的基底通常不是原 $P,Q$ 基底。因此

$$
H^1(S_{\rm prim,\infty})=0,\qquad
H^2(S_{\rm prim,\infty})\simeq(\Lambda/(t))^2.
$$

這是所定義 Selmer 複形的實際模同構，強於只給出 characteristic ideal $(t^2)$。

## 6. 提取 Kato 的 rank-two 首項

對 row $d(t)=(d_1(t),d_2(t))$，其 determinant/cofactor 類為

$$
v_{\det}(t)=\begin{pmatrix}-d_2(t)\\d_1(t)\end{pmatrix}
=t\begin{pmatrix}-a_2(t)\\a_1(t)\end{pmatrix}.
$$

Kato 一側界與第 5 節的 unit 升級給出

$$
z_{\rm prim,\infty}=u(t)v_{\det}(t),\qquad u(t)\in\Lambda^\times.
$$

所以 $z_{\rm prim,\infty}/t$ 存在於真正的 global $H^1$，並非只在 fraction field 中形式相除。其特化

$$
\kappa_{\rm prim}=u(0)(-a_2(0)P+a_1(0)Q)
$$

落在 $M=H^1(S_{\rm prim,0})$。因 $V(0)$ 可逆，row $(a_1(0),a_2(0))$ primitive，故此類在 $M$ 中亦 primitive。

接著把它接到高度。寫 $\ell_P=\ell(P)$、$\ell_Q=\ell(Q)$，選

$$
\pi:M^*\twoheadrightarrow O,\qquad
\pi=(\ell_Q,-\ell_P).
$$

它的 kernel 正是 $O\ell$，所以為第 3 節 $H^2(C_{\rm prim,0})$ 的整座標。Bockstein 自然性給出

$$
(a_1(0),a_2(0))=\pi H_\gamma.
$$

若 $H_\gamma=\left(\begin{smallmatrix}a&b\\b&c\end{smallmatrix}\right)$，便有

$$
\begin{pmatrix}-a_2(0)\\a_1(0)\end{pmatrix}
=\begin{pmatrix}c\ell_P-b\ell_Q\\a\ell_Q-b\ell_P\end{pmatrix}
=\operatorname{adj}(H_\gamma)\begin{pmatrix}\ell_P\\\ell_Q\end{pmatrix}.
$$

**定理 6.1。** 在上述整基底和 orientation 下，

$$
\boxed{\kappa_{\rm prim}
=u_0\operatorname{adj}(H_\gamma)\ell,\qquad u_0\in O^\times.}
$$

對任意 $x\in M$，進而有

$$
\boxed{h_\gamma(x,\kappa_{\rm prim})
=u_0\det(H_\gamma)\ell(x).}
$$

**證明。** 前式由剛才的 contraction 計算；後式只需左乘 $x^{\rm t}H_\gamma$，使用 $H_\gamma\operatorname{adj}(H_\gamma)=\det(H_\gamma)I_2$。證畢。

它有一個不依賴 coordinate 的表述：

$$
O\kappa_{\rm prim}=(\ker\ell)^{\perp_{h_\gamma}}.
$$

因 $H_\gamma$ unimodular、$\ell$ primitive，兩邊都是相同的 saturated rank-one 子模。特別地，mod $11$ 的 derived Kato 方向是 $k(P+4Q)$ 的高度正交補。

上述公式是本例的整格、up-to-unit 版本的 Bockstein／高度比較；可對照 [BKS I v2，Theorem 5.6](https://arxiv.org/html/1910.07404v2#S5.SS2) 的 regulator contraction。本文沒有套用其含有複數 BSD 元素的猜想來定義 $\kappa$。

## 7. 把輔助 torsion 精確搬回 cofactor 首項

現在回到原 relaxed 模型，並用下標 $\rm rel$ 避免與 primitive 模型混淆：

$$
A_{\rm rel}(t)=(B_{\rm rel}(t)\ c_{\rm rel}(t)),
\qquad q_{\rm rel}=(0,0,1),\qquad B_{\rm rel}(0)=0.
$$

第 4 節的比較映射在 $H^1$ 上是 identity，在 $H^2$ 上是 $J=11W$。由 boundary／Bockstein 自然性，可選相容 sign 與基底使

$$
B_{\rm rel}'(0)=JH_\gamma,\qquad
c_{\rm rel}(0)=J\ell.
$$

若 cone sign 取相反，第二式會有負號；以下首項公式連同 determinant orientation 一起改號，unit 及 valuation 結論相同。

relaxed cofactor 是

$$
v_{\rm rel}(t)=
\begin{pmatrix}-\operatorname{adj}(B_{\rm rel}(t))c_{\rm rel}(t)\\
\det B_{\rm rel}(t)\end{pmatrix}.
$$

因二階伴隨矩陣對 entries 線性，且最後座標的消失階至少是二，

$$
v_{\rm rel}'(0)=
\begin{pmatrix}-\operatorname{adj}(JH_\gamma)J\ell\\0\end{pmatrix}.
$$

**引理 7.1（保留格指數的 contraction）。** 對交換環上的方陣 $J,H$，有

$$
\operatorname{adj}(JH)J=(\det J)\operatorname{adj}(H).
$$

**證明。** $\operatorname{adj}(JH)=\operatorname{adj}(H)\operatorname{adj}(J)$，再用 $\operatorname{adj}(J)J=(\det J)I$。這是多項式恆等式，不需要先反轉 $\det J$。證畢。

故

$$
\boxed{v_{\rm rel}'(0)=
\begin{pmatrix}-(\det J)\operatorname{adj}(H_\gamma)\ell\\0\end{pmatrix}.}
$$

因此 relaxed 的導出 Kato 類帶有 **恰兩次 $11$** 的整格因子：

$$
\kappa_{\rm rel}\in11^2M\setminus11^3M,\qquad
O\kappa_{\rm rel}=11^2O\kappa_{\rm prim}.
$$

這裡使用 Attack 04 給出的 relaxed Kato／cofactor unit 比較。亦可由已定義的 primitive Kato 類及 Euler norm 關係直接得到：在相容 convention 下

$$
z_{\rm rel,\infty}
=w(t)\mathcal E(t)z_{\rm prim,\infty},\qquad w(t)\in\Lambda^\times,
$$

而 $z_{\rm prim,\infty}(0)=0$，故取一次導數只留下 $w(0)\mathcal E(0)\kappa_{\rm prim}$。第 4 節已給出 $v_{11}(\mathcal E(0))=2$。

值得區分兩個不同數：全域 $H^2$ 的 torsion 是 $O/11O$，但完整 regulator 格比較使用 $\det J$，其 valuation 是 $2$。只把前者的長度 $1$ 當成全部修正，會少掉一個 $11$。

同一三角在 $\Lambda$ 上給出 determinant 因子

$$
\det B_{\rm rel}(t)\doteq
\mathcal E(t)\det B(t),
$$

其中 $\doteq$ 表示相差 $\Lambda$-unit。Euler 因子在兩側同時出現，因此可在整域 $\Lambda$ 中消去；不需要假裝 $\mathcal E(0)$ 是 unit。這也將 Attack 04 的 relaxed 比較接到第 5 節的完整有限條件。

## 8. 為何有限 tame 的一次項會看不見這件事

仍令 $R=O[C_{11}^2]$，$I=(X,Y)$。由 $(1+X)^{11}=(1+Y)^{11}=1$，

$$
11I\subseteq I^2.
$$

Attack 03 的有限模型滿足 $B_F\in M_2(I)$、$c_F(0)\in11O^2$。所以

$$
-\operatorname{adj}(B_F)c_F\in I^2R^2,\qquad
\det B_F\in I^2.
$$

因此其 cofactor 的線性 cochain 首項在 $I/I^2$ 中是零，雖然二次首項可以是非零的 $2XY$。這是群環中 $11$ 與增廣過濾的實際關係，不是高度必然退化。

cyclotomic 的 $t/t^2$ 則是自由 $O$-模，保留了 $11^2$ 的 valuation，允許第 7 節先追蹤格指數再抽取 primitive 首項。本稿沒有在被 $11$ 殺掉的 $I/I^2$ 裡非法除以 $11$。

## 9. 可移植的證明片段

**引理 9.1。** 設 $B(t)\in M_r(O[[t]])$，$B(0)=0$。若非零 $f(t)$ 滿足

$$
f(t)\in\det B(t)\,O[[t]],\qquad
\mu(f)=0,\qquad\lambda(f)=r,
$$

則

$$
B(t)=tV(t),\quad V(t)\in\mathrm{GL}_r(O[[t]]),
\quad f(t)=t^rU(t),\quad U(t)\in O[[t]]^\times.
$$

**證明。** 寫 $f=t^r\det(V)u$。mod $11$ 的 $t^r$ 係數非零，故 $\det V(0)$ 和 $u(0)$ 均為 unit。證畢。

所以對其他曲線與秩，若能取得相應完整整 Selmer 格與最小 $\lambda=r$，同一證法會將一側界升成 unimodular 高度及確切 $p$-adic 消失階。這個引理不保證每條曲線、每個素數都滿足最小 $\lambda$，更不自行提供複數比較。

## 10. 本輪的證明邊界與下一個主攻命題

本稿已給出具體的 cyclotomic filtered 比較：完整有限 Selmer 複形、rank-two 高度、primitive 導出 Kato 類，以及 relaxed 複形的 torsion／格指數。這是原 R318 所需比較的一個已展開切面；原 finite $F$ 的全部 filtered、canonical 規範尚不能一概標為 closed。

第 5 節的高度不退化與 primitive normal form 可以直接由 Kato 一側界及本例最小 $\lambda$ 推出。它們不必將 Attack 04 的整等變比較當成唯一支柱；Attack 04 的作用是連回原 $F$-族的 Kato／determinant 類。

仍待攻克的複數部分非常具體：構造具有獨立 rational structure 的 motivic determinant 元素，證明其 étale 首項對應本稿的 $\kappa_{\rm prim}$，而其複數 regulator 給出 $L''(E,1)/2!$。必須先給出這個 rational／motivic 比較，才能合法地把

$$
\frac{L''(E,1)}{2!\,\Omega_E^+\operatorname{Reg}_{\infty}(P,Q)}
$$

當作可放入 $\mathbb Q_{11}$ 比較的數。本文沒有先假設這個比值有理，也沒有把未確定的 $u_0$ 換成期待的 BSD 常數。

下一步的攻擊對象因此是兩種 realization 的同一個 motivic 元素，而不再是「是否存在一個不退化的 $11$-adic regulator」。後一個問題已由本稿的推導處理。

## 11. 可重播的新計算與交付

Windows PowerShell：

```powershell
py -3 .\local_log.py --output .\local_log_result_local.json
```

macOS／Linux：

```bash
python3 ./local_log.py --output ./local_log_result_local.json
```

只需 Python 3.9 以上標準函式庫。預期形式參數為 $99,66\pmod{121}$，正規化 log 向量為 $(4,10)\pmod{11}$。程式沒有計算高度矩陣，也沒有自行宣告 Selmer 對偶或 torsion 定理成立；那些結論的證明在本文。

本包列出既有輸入及來源雜湊，附上本輪新程式與實際輸出。原 UTF-8 Markdown 是 canonical source，正式數學僅使用 `$`／`$$` delimiter。本文未改寫既有 canonical frontier，也未把尚未獨立審查的稿件稱為認證結果。
