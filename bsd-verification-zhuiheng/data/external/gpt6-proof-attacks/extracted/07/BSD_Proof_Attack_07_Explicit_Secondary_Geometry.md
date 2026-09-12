# BSD 證明攻擊 07：一份實際構造出的次級幾何資料

2026-09-12。Neo.K／EveMissLab 與 GPT 的研究工作稿。原始 UTF-8 source。

**本輪主結果。** 對既有曲線與兩個有理點，我們寫出一條 genus $3$ 曲線、一個有理函數，以及三條座標曲線上的修正函數，構成有限的鏈 $\Gamma_{PQ}$，並逐項證明

$$
\boxed{\partial\Gamma_{PQ}
=4\bigl([(P,Q)]-[(P,O)]-[(O,Q)]+[(O,O)]\bigr).}
$$

這給出上一輪所尋找的「消零資料」的一個實際幾何模型。主結果只依賴曲線方程與有理點，不以 BSD、Sha 有限性或 Beilinson–Bloch 猜想為前提。數學推導及本輪新代數計算均列在本包。

這個物件尚未被識別為 Kato 導出類對應的消零資料。因此它不是 Attack 06 的 $\eta_{11}^{\mathrm K}$ 的已證有理提升，也尚未給出 $L''(E,1)$ 的 regulator 公式。本文把已完成的有限構造與尚未構造的比較映射分開。

## 1. 目標 cycle 與最小輸入

固定

$$
E:\ y^2+y=x^3+x^2-2x,\qquad
P=(0,0),\quad Q=(1,0),\qquad A=E\times E.
$$

$O$ 是無窮遠點，故

$$
-P=(0,-1),\qquad -Q=(1,-1).
$$

記

$$
D_P=[P]-[O],\qquad D_Q=[Q]-[O],
$$

以及零次數 cycle

$$
Z_{PQ}=D_P\boxtimes D_Q
=[(P,Q)]-[(P,O)]-[(O,Q)]+[(O,O)].
$$

它的 Albanese 像是零。本輪要找的不是數值上很小的 regulator，而是曲線與函數的有限組合

$$
\Gamma=\sum_i n_i(C_i,f_i),\qquad
\partial(C_i,f_i)=(\iota_i)_*\operatorname{div}_{\widetilde C_i}(f_i),
$$

使 $\partial\Gamma$ 等於 $Z_{PQ}$ 的某個非零整數倍。這裡使用曲線的正規化 $\widetilde C_i$ 計算除子，並把閉點的剩餘域次數計入 pushforward。

主定理不需要沿用先前算術證書。只有第 5 節延伸到整個 $M_{\mathbb Q}=E(\mathbb Q)\otimes\mathbb Q$ 時，才沿用 $P,Q$ 張成這個二維空間的既有輸入。與 Kato 的比較則仍沿用 Attack 06 的規範：

$$
\kappa^\dagger
=16\mathfrak s_{11}\operatorname{adj}(H)\ell,\qquad
\mathfrak s_{11}\in\mathbb Z_{11}^{\times},
$$

其中 $\mathfrak s_{11}$ 的有理性及值仍未知。

## 2. 從相同的 y 座標構造曲線

設 $f_0(x)=x^3+x^2-2x$。因為

$$
f_0(x_1)-f_0(x_2)
=(x_1-x_2)(x_1^2+x_1x_2+x_2^2+x_1+x_2-2),
$$

$A$ 中相同 $y$ 座標的 locus 除了對角線外，還有由二次曲線

$$
x_1^2+x_1x_2+x_2^2+x_1+x_2-2=0
$$

給出的分支。它經過 $(x_1,x_2)=(0,1)$，正好對應 $(P,Q)$。

用穿過 $(0,1)$ 的直線 $x_2=1+ux_1$ 參數化該二次曲線。令

$$
d=u^2+u+1,\qquad n=-3u-2,\qquad m=1-u-2u^2.
$$

則

$$
x_1=\frac{n}{d},\qquad x_2=\frac{m}{d}.
$$

把 $Y=2y+1$，所以 $Y^2=4x^3+4x^2-8x+1$。再令 $W=Yd^2$，得到曲線的光滑射影模型 $C$：

$$
C:\quad W^2=F_8(u),
$$

其中

$$
\begin{aligned}
F_6(u)&=d^3+4n^3+4n^2d-8nd^2\\
&=u^6+27u^5+106u^4+87u^3-14u^2-21u+1,\\
F_8(u)&=dF_6(u)\\
&=u^8+28u^7+134u^6+220u^5+179u^4\\
&\hspace{1em}+52u^3-34u^2-20u+1.
\end{aligned}
$$

映射為

$$
\phi:C\longrightarrow E\times E,\qquad
(u,W)\longmapsto
\left(
\left(\frac nd,\frac{W/d^2-1}{2}\right),
\left(\frac md,\frac{W/d^2-1}{2}\right)
\right).
$$

這些式子先在 $d\ne0$ 的開集定義。因 $C$ 光滑、$A$ proper，映射延伸到整條 $C$。在 $x_1\ne0$ 的開集可用 $u=(x_2-1)/x_1$ 恢復參數，再恢復 $W$，所以 $\phi$ 對其像 birational。以下 $(C,g)$ 代表像曲線的函數，透過此正規化計算；沒有省略映射次數。

**引理 2.1。** $C$ 的 genus 是 $3$，並且這個 hyperelliptic 模型在 $11$ 處有 good reduction。

**證明。** 在 $\mathbb F_{11}[u]$ 中，設

$$
S=7+7u+3u^2+u^3+9u^4+6u^5,
$$

$$
T=8+3u+u^2+10u^3+9u^4+10u^5+2u^6.
$$

直接乘開給出

$$
SF_8+TF_8'=1\pmod{11}.
$$

所以 $F_8$ 模 $11$ squarefree，從而在 $\mathbb Q[u]$ 也 squarefree。其 degree 為 $8$、首項係數為 $1$，因此光滑雙覆蓋的 genus 為 $(8-2)/2=3$。在奇特徵 $11$ 下，相同 squarefree 條件及無窮遠處的首項係數給出光滑射影模型。證畢。

這個一般策略與以 hyperelliptic curves／Kummer rational curves 產生零-cycle 關係的文獻一致；參見 [Gazaki–Love，§2.1–2.2](https://arxiv.org/html/2309.06361v3)。本例下文的整係數關係直接由有理函數除子證明，不借用代數閉包上 torsion-free 的結論。

## 3. 切線函數的完整除子

在二次曲線的點 $(0,1)$，切線為 $2x_1+3x_2-3=0$。取

$$
g=2x_1+3x_2-3
=-\frac{(3u+2)^2}{d}.
$$

**引理 3.1。** 有

$$
\phi_*\operatorname{div}_C(g)
=2[(P,Q)]+2[(-P,-Q)]-4[(O,O)].
$$

**證明：零點。** 分子唯一零點為 $u_0=-2/3$，且

$$
d(u_0)=\frac79,\qquad
W=\pm\frac{49}{81},\qquad
Y=\frac{W}{d^2}=\pm1.
$$

故兩個點分別映到 $(P,Q)$、$(-P,-Q)$。因 $W\ne0$，雙覆蓋在兩點均不分歧，$u-u_0$ 是局部參數。分子有二重零點，分母是 unit，所以每個零點的 order 都是 $2$。

**極點。** $d=0$ 定義一個剩餘域為 $\mathbb Q(\sqrt{-3})$ 的 degree-two 閉點。$F_6$ 在此不為零：模 $d$ 有 $F_6=4n^3$，而 $n$ 與 $d$ 互素。因此雙覆蓋在兩個幾何點均簡單分歧。以 $W$ 作局部參數，

$$
\operatorname{ord}(d)=2,\quad
\operatorname{ord}(W)=1,\quad
\operatorname{ord}(x_1)=\operatorname{ord}(x_2)=-2,
$$

$$
\operatorname{ord}(Y)=-3,\qquad
\operatorname{ord}(g)=-2.
$$

兩個 $E$ 座標均趨向 $O$。所以 degree-two 閉點的 pushforward 貢獻為 $-2\cdot2[(O,O)]$。這個 $2$ 是域次數，不是額外的猜測乘數。

**參數無窮遠。** 當 $u\to\infty$，$g\to-9$，在 $C$ 的兩個無窮遠點都沒有零點或極點。因此以上清單完整。證畢。

這一節的 proof 與 squarefree 證書同時排除了：切線重數漏算、正規化分支漏算、閉點 degree 漏算、以及參數無窮遠多出除子。

## 4. 四項鏈：邊界精確等於 4Z

定義三條座標曲線

$$
H_-=E\times\{-Q\},\qquad
V_P=\{P\}\times E,\qquad
V_O=\{O\}\times E.
$$

在 $H_-$ 上用第一個 $E$ 的函數 $x_1$；在兩條垂直曲線上用第二個 $E$ 的函數 $x_2-1$。它們的除子由

$$
\operatorname{div}_E(x)=[P]+[-P]-2[O],
\qquad
\operatorname{div}_E(x-1)=[Q]+[-Q]-2[O]
$$

直接得到。

| 曲線與函數 | pushforward 後的除子 |
|---|---|
| $(C,g)$ | $2[(P,Q)]+2[(-P,-Q)]-4[(O,O)]$ |
| $(H_-,x_1)$ | $[(P,-Q)]+[(-P,-Q)]-2[(O,-Q)]$ |
| $(V_P,x_2-1)$ | $[(P,Q)]+[(P,-Q)]-2[(P,O)]$ |
| $(V_O,x_2-1)$ | $[(O,Q)]+[(O,-Q)]-2[(O,O)]$ |

取

$$
\boxed{
\Gamma_{PQ}
=(C,g)-2(H_-,x_1)+2(V_P,x_2-1)-4(V_O,x_2-1).
}
$$

**定理 4.1。** 在整係數零-cycle 群中，

$$
\partial\Gamma_{PQ}=4Z_{PQ}.
$$

**證明。** 表格四列按 $1,-2,2,-4$ 相加。$(-P,-Q)$、$(P,-Q)$、$(O,-Q)$ 的係數各自相消，留下 $(P,Q),(P,O),(O,Q),(O,O)$ 的係數 $4,-4,-4,4$。證畢。

因此

$$
4[Z_{PQ}]=0\quad\text{於 }\mathrm{CH}_0(A),
\qquad
[Z_{PQ}]=0\quad\text{於 }\mathrm{CH}_0(A)_{\mathbb Q}.
$$

我們沒有聲稱 $4$ 是最小 annihilator，也沒有用這個計算決定整係數 cycle 的精確階。

**與 $p=11$ 的關係。** $4\in\mathbb Z_{11}^{\times}$，所以

$$
B_{PQ}:=\frac14\Gamma_{PQ},\qquad \partial B_{PQ}=Z_{PQ}
$$

同時給出 rational 係數及 $\mathbb Z_{11}$ 係數的鏈。這個有限除法不引入 $11$ 的分母；並不據此聲稱所有 regulator 比較或 Selmer 整條件已完成。

## 5. 兩個基底的四種配對都有消零資料

令 $\sigma:A\to A$ 交換兩個座標，取

$$
B_{QP}=\sigma_*B_{PQ}.
$$

則 $\partial B_{QP}=Z_{QP}$。

對 $R=P$ 或 $Q$，令 $a=x(R)$，並設 $\Delta:E\to A$ 為對角線。定義

$$
\begin{aligned}
\Gamma_{RR}={}&(\Delta,x-a)
-(E\times\{-R\},x_1-a)\\
&+(\{R\}\times E,x_2-a)
-2(\{O\}\times E,x_2-a).
\end{aligned}
$$

與第 4 節相同的除子相加給出

$$
\partial\Gamma_{RR}=2Z_{RR}.
$$

所以取 $B_{PP}=\Gamma_{PP}/2$、$B_{QQ}=\Gamma_{QQ}/2$，四項都有明確來源，所有分母也是 $11$-units。

**推論 5.1。** 對

$$
D=aD_P+bD_Q,\qquad D'=cD_P+dD_Q,\qquad a,b,c,d\in\mathbb Q,
$$

鏈

$$
B(D,D')=acB_{PP}+adB_{PQ}+bcB_{QP}+bdB_{QQ}
$$

滿足 $\partial B(D,D')=D\boxtimes D'$。因此在沿用 $P,Q$ 張成 $M_{\mathbb Q}$ 的輸入下，外積映射

$$
M_{\mathbb Q}\otimes M_{\mathbb Q}
\longrightarrow \mathrm{CH}_0(E\times E)_{\mathbb Q}
$$

在這些 Mordell–Weil divisor classes 上為零。

這是 rational Mordell–Weil 外積的結論，不是整個 $\mathrm{CH}_0(E\times E)$ 或所有有限擴張上 Albanese kernel 的消失定理。改用不同 divisor representatives 時要加入相應的 principal-divisor 鏈；本文的公式固定了 representatives，沒有假裝 chain 本身對所有選擇 canonical。

## 6. 我們究竟構造了哪一類 secondary 物件

在光滑曲面 $A$ 上，考慮 Gersten 複形的相關部分

$$
K_2^M(\mathbb Q(A))\otimes\mathbb Q
\xrightarrow{\partial_2}
\bigoplus_{C\subset A}\mathbb Q(C)^\times\otimes\mathbb Q
\xrightarrow{\partial_1}
Z_0(A)\otimes\mathbb Q.
$$

中間群以加法書寫：$n(C,f)$ 表示函數的 $n$ 倍類。固定 $Z=Z_{PQ}$，定義

$$
\mathcal T_Z=
\{B:\partial_1B=Z\}/\operatorname{im}(\partial_2).
$$

定理 4.1 給出 $\mathcal T_Z$ 的一個明確 rational 元素 $[B_{PQ}]$。因

$$
\ker(\partial_1)/\operatorname{im}(\partial_2)
=\mathrm{CH}^2(A,1)_{\mathbb Q},
$$

$\mathcal T_Z$ 是此 higher Chow 群的 torsor：兩個消零鏈之差是 closed higher Chow 類，反之加上 closed 類仍有相同邊界。

必須注意，$B_{PQ}$ 自己的邊界是 $Z_{PQ}$，不是零。它是 relative／secondary 鏈，**不能直接當成 $\mathrm{CH}^2(A,1)$ 的 closed 類去套絕對 regulator**。這個區分在下一步接 Kato 時不可略過。

以外積邊界構造幾何 mixed extensions 的機制，可對照 [Dogra，§3.1、Proposition 1](https://arxiv.org/html/2507.10111v3#S3.SS1)。該文在一般情形透過 Beilinson–Bloch 預期取得消零鏈；本例的特定外積已由上述四項鏈直接處理，無須假設其一般終止性。

這裡沒有聲稱找到文獻中未曾有過的普遍機制。新增的可檢查內容是本例的方程、函數、整係數邊界和基底上的四項資料。

## 7. 接高度時不可丟掉 Tate 部分

### 7.1 一個精確的係數障礙

令 $V=T_{11}(E)\otimes\mathbb Q_{11}$，$\tau(v\otimes w)=w\otimes v$。因 $2$ 可逆，

$$
V\otimes V=W_+\oplus W_-,
\qquad
W_\pm=\operatorname{im}\frac{1\pm\tau}{2},
$$

其中 $W_+=\operatorname{Sym}^2V$，$W_-=\bigwedge^2V\simeq\mathbb Q_{11}(1)$。

普通高度使用 Weil 收縮

$$
e:V\otimes V\longrightarrow\mathbb Q_{11}(1).
$$

**引理 7.1。** $e$ 無法只透過商 $(V\otimes V)/W_-$ 定義。

**證明。** 取 symplectic basis $v_1,v_2$。向量

$$
a=v_1\otimes v_2-v_2\otimes v_1
$$

在該商為零，但 $e(a)=2e(v_1,v_2)\ne0$。證畢。

文獻的部分 mixed-extension 構造把 divisor／coniveau 子空間先除去；對角線提供的 Tate 部分正在其中。因此不能只保留那個商，然後宣稱已恢復 Attack 06 使用的普通高度。失敗的 algebraic step 是 **Weil 收縮無法從該商下降**。這不是原有邊界關係失敗。

### 7.2 補出明確的 1-motive 資料

為保留普通高度所需的部分，我們另外給出 rational biextension 資料。令

$$
R=P+Q=(-2,-1),
$$

則精確的群律計算給出

$$
P+R=\left(\frac54,-\frac{13}{8}\right),\qquad
Q+R=\left(\frac19,-\frac{19}{27}\right).
$$

取

$$
D'_P=[P+R]-[R],\qquad D'_Q=[Q+R]-[R].
$$

兩個 divisors 分別代表 $P,Q$ 的 $\operatorname{Pic}^0$ 類，而且它們的 supports 與 $\{O,P,Q\}$ 都不相交。

對 $j=P,Q$，設

$$
\mathcal L_j=\mathcal O_E(D'_j).
$$

其 canonical rational section $s_j$ 在 $O,P,Q$ 非零，以在 $O$ 的值 rigidify $\mathcal L_j$。rigidified degree-zero line bundle 對應一個 extension

$$
1\longrightarrow\mathbb G_m\longrightarrow G_j
\longrightarrow E\longrightarrow0.
$$

$s_j(P)$ 和 $s_j(Q)$ 因而指定了 $P,Q$ 在這個 extension 中的 rational lifts。令

$$
G=G_P\times_E G_Q,
\qquad
\mathcal M=
\left[\mathbb Z^2\xrightarrow{u}G\right],
$$

其中兩個 lattice generators 分別送到

$$
u(e_P)=(s_P(P),s_Q(P)),\qquad
u(e_Q)=(s_P(Q),s_Q(Q)).
$$

**這是一個以明確有理除子與 rational lifts 定義的 $1$-motive。** 它的 $11$-adic realization 的 graded pieces 分別為 lattice 部分 $\mathbb Q_{11}^2$、橢圓曲線部分 $V$、以及 torus 部分 $\mathbb Q_{11}(1)^2$；Tate 部分並未被 quotient 消去。這裡 $\operatorname{Pic}^0(E)\simeq E$ 的符號依所固定的 polarization convention 搬移，不憑此指定 Kato 公式的符號。

局部 splittings 及全域高度由 biextension 評價取得，普通與 unit-root $p$-adic 規範的關係參見 [Rivera Arredondo，§2.1、§6](https://arxiv.org/pdf/2006.10362)。本輪給出幾何輸入，不把「有 rational lifts」當成已計算高度 entries，也不把這個 $1$-motive 自動識別成 Kato 的幾何來源。

### 7.3 係數層級可以怎樣黏合

對任一 quotient $\pi_W:V\otimes V\twoheadrightarrow W$，定義二步群

$$
U_W=V\times V\times W,
$$

乘法為

$$
(x,y,z)(x',y',z')
=(x+x',y+y',z+z'+\pi_W(x\otimes y')).
$$

雙線性保證結合律。兩個投影給出精確同構

$$
U_{V\otimes V}
\simeq U_{W_+}\times_{V\times V}U_{W_-}.
$$

逆映射把共享同一對 $(x,y)$ 的中央座標 $z_+,z_-$ 相加。這證明保留「商部分 + Tate 部分」在係數代數上足夠。

但若要把不同幾何模型產生的 cocycles 做這個纖維積，必須先識別它們的 Kummer cocycles、符號、局部 splittings 及邊界 trivializations。本文沒有用群同構代替這個比較。$[B_{ij}]$ 與 $\mathcal M$ 是已給出的有限幾何資料；保持 Attack 06 正規化的完整比較映射仍待構造。

## 8. 到 Kato 與複數主項，實際還缺哪一步

本輪把幾何輸入具體化為

$$
\mathcal G_{07}=\bigl(B_{PP},B_{PQ},B_{QP},B_{QQ};\mathcal M\bigr).
$$

它依賴曲線與 $P,Q$，沒有用 $p$-adic $L$ 函數首項反向定義任何 rational 數。這是本輪可交付的構造。

然而，Kato Euler system 的幾何來源在模曲線及各層 cyclotomic 資料上。**目前沒有構造出把那些資料的導出類送到 $\mathcal G_{07}$ 的 correspondence 或 chain map。** 因此「已知點的外積有幾何消零」到「這個消零就是 Kato 導數選定的消零」之間，尚無已證等式。

它不是可藉數值逼近略過的尺度問題。若只從 $\mathcal M$ 用已固定的高度與 log 組成

$$
\nu_{11}=\operatorname{adj}(H)\ell,
$$

Attack 06 所給出的仍然是

$$
\kappa^\dagger=16\mathfrak s_{11}\nu_{11},
$$

不能因為 $\mathcal G_{07}$ 定義在 $\mathbb Q$，就推出未知的 $\mathfrak s_{11}\in\mathbb Q$。要得到這一點，必須證明 Kato 端與幾何端在相同 regulator 比較中具有 rational 相對尺度。

即使這個 $11$-adic 比較完成，複數端仍要從實際幾何構造推導

$$
\rho_\infty(\eta_{\mathrm{geom}})
=\frac{L''(E,1)}2
=\frac{2\pi}{\sqrt{389}}
\int_1^\infty f_E\!\left(\frac{iy}{\sqrt{389}}\right)
(\log y)^2\,dy.
$$

後面這個 Mellin 等式沿用 Attack 06；本輪未聲稱新構造的 regulator 已等於該 integral。尤其不把一個 arbitrary $11$-adic 數以未指定方式搬到實數。

下一次應直接處理 $\mathcal G_{07}$ 的 étale／de Rham 比較及 Kato 的幾何 correspondence，或找出這個 candidate 的 regulator 投影為何不可能接上。僅重播本輪的邊界計算不能完成這一步。

## 9. 結果與界線

| 具體步驟 | 本輪結果 |
|---|---|
| $E\times E$ 上的有限曲線與函數 | 已給出 genus $3$ 模型、映射與切線函數 |
| 切線函數的零點、極點、重數及域次數 | 已逐項推導 |
| $4Z_{PQ}$ 的有理等價邊界 | 四項鏈精確成立 |
| $P,Q$ 四種配對的 rational 消零鏈 | 已構造；分母為 $2$ 或 $4$ |
| 支持普通高度的 Tate 幾何資料 | 以明確除子、extensions 及 $1$-motive 給出 |
| 只用 divisor quotient 恢復 Weil 收縮 | 不成立；引理 7.1 定位障礙 |
| 與 Kato 導出類的幾何比較 | 尚未構造 |
| $\mathfrak s_{11}$ 的有理性、值及複數主項比較 | 尚未證明 |

這輪的進展是一份有限、明確的幾何消零構造，以及接高度時所需的補充資料。它不是完整 BSD 證明，也不是 Attack 06 的 BD6 已閉合。

## 10. 可重播計算

**attack07_cycle.py** 只用 Python 標準函式庫。它精確重現：

1. 二次曲線參數化、兩個 $E$ 座標滿足相同方程、切線函數因式分解；
2. $F_8$ 模 $11$ 的 squarefree Bézout 證書；
3. 目標零點及極點的代數條件，以及四項 divisor 的係數消去；
4. diagonal／swapped 配對的邊界；
5. 平移後的有理點與 disjoint-support 條件；
6. quotient 丟失 Weil 收縮的明確反例。

除子的局部 valuation 由第 3 節的書面 proof 給出；程式檢查 proof 使用的多項式條件及最後的 cycle 等式。它不是 general-purpose Chow group prover，也不測試尚未定義的 Kato 比較映射。

Windows PowerShell：

~~~powershell
py -3 .\attack07_cycle.py --output .\attack07_result_local.json
~~~

macOS／Linux：

~~~bash
python3 ./attack07_cycle.py --output ./attack07_result_local.json
~~~

本輪執行成功：boundary residual 為空、genus 為 $3$、模型模 $11$ 光滑。$\mathfrak s_{11}$ 在結果檔刻意保留為 **null**，Kato／複數比較標示為尚未完成。

本文未重播舊證書，未更新既有 canonical frontier。「已證」指正文所列有限推導；未宣稱經過獨立學者或形式化系統審查。
