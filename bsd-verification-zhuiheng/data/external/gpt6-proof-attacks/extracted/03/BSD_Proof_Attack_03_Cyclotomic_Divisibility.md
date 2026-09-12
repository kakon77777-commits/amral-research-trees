# BSD 證明攻擊 03：用 cyclotomic 整除跨過 Kato／行列式缺口

2026-09-12。Neo.K／EveMissLab 與 GPT 的研究工作稿。

本文直接提出並推演候選證明。本文完成的是以下代數引理和條件性推導；核心算術整除引理仍未證出。它不是完整 BSD 證明，也不主張文獻優先權。原始 UTF-8 本文是 canonical source。

## 1. 這次要跨過的等式

目標是由獨立定義的算術複形構造 $z_{\det}$，再證明真正的 Kato 類滿足

$$
z_{\mathrm K}=u z_{\det},\qquad u\in R^\times.
$$

候選類不能用這個等式反過來定義。本稿用伴隨矩陣構造它，接著把所需等式縮減為 cyclotomic 族中的一側整除。

固定 $E=389a1$、$p=11$、$O=\mathbb Z_{11}$、$k=\mathbb F_{11}$，並沿用

$$
F=F_{397}F_{991},\quad G=C_{11}^2,\quad R=O[G],\quad
I=(X,Y),\quad X=\gamma-1,\quad Y=\eta-1.
$$

$T=T_{11}(E)$，$V=T/11T$，$M=T\otimes_O R$。既有輸入是 $E(\mathbb Q)\otimes O=OP\oplus OQ$、有限 Selmer 群 $kP\oplus kQ$、輔助局部化矩陣 $\left(\begin{smallmatrix}1&2\\1&4\end{smallmatrix}\right)$，以及完整全域 Bockstein 的一阶矩陣。本文接受這些輸入，不重跑其計算。

## 2. 新的算術矩陣正規形

令 $\Sigma=\{\infty,11,389,397,991\}$，採奇素數下的無限處 Tate 修正。考慮

$$
C=\mathbf R\Gamma(G_{\mathbb Q,\Sigma},M),\qquad
Q_{11}=\mathbf R\Gamma(\mathbb Q_{11},M^-),
$$

以及真正的局部商映射 $q:C\to Q_{11}$。只在 $11$ 施加 Greenberg 條件，保留兩個輔助素點的 relaxed 條件：

$$
\mathcal S=\operatorname{Cone}(q)[-1].
$$

這個選擇保留通常未分歧條件與 relaxed 條件之間的差異；沒有把非 perfect 的輔助局部商刪掉後又宣稱得到原來的有限 Selmer 複形。

**命題 2.1（在上述既有算術輸入下）。** 可以選取有限自由模型和基底，使

$$
C\simeq [R^3\xrightarrow{A}R^2],\qquad
A=(B\ c),\qquad q=(0,0,1),
$$

其中兩項在次數 $1,2$，$B\in M_2(R)$、$c\in R^2$，並且

$$
\mathcal S\simeq[R^2\xrightarrow{B}R^2],\qquad
B\in M_2(I),\qquad
\overline B\equiv
\begin{pmatrix}X&2X\\Y&4Y\end{pmatrix}\pmod{\overline I^2}.
$$

最後一式在 $\overline R=k[G]$ 中，$\overline I=(X,Y)$。

**推導。** 既有的有限全域對偶計算給出 $h^2_\Sigma(V)=2$，全域 Euler characteristic 給出 $h^1_\Sigma(V)=3$。$H^0_\Sigma(V)=H^3_\Sigma(V)=0$。全域 Galois 複形的 perfectness、導出 base change 及局部環上的 minimal free model，給出秩 $3\to2$ 的模型。這裡使用的是環境 Galois 複形的性質，不需要輔助未分歧條件的慣性不變量自由。

在 $11$，ordinary quotient 的殘餘 Frobenius 是 $7\ne1$；局部殘餘上同調維數為 $(0,1,0)$。因此 $Q_{11}\simeq R[-1]$。

還需證明 $q$ 在自由模型中有 unit 係數。令 $\mathcal F$ 為通常的有限殘餘 Selmer 條件，$\mathcal R$ 為只放鬆兩個輔助素點的條件。$\mathcal R^*$ 在兩個輔助素點採 strict 條件，其 Selmer 群為零，因為既有的局部化矩陣可逆。Poitou–Tate 比較序列中

$$
\bigoplus_{\ell=397,991}H^1(\mathbb Q_\ell,V)/H_f^1(\mathbb Q_\ell,V)
\longrightarrow \operatorname{Sel}_{\mathcal F}(V)^\vee
$$

是該可逆局部化的對偶，所以也是同構。因此 $\operatorname{Sel}_{\mathcal R}(V)=\operatorname{Sel}_{\mathcal F}(V)$ 為二維。它恰是三維 $H^1_\Sigma(V)$ 到一維 $H^1(\mathbb Q_{11},V^-)$ 的核。在 $389$，殘餘局部 $H^1$ 為零，沒有額外條件。故此局部商映射滿射。

於是可在 $R$ 上消元令 $q=(0,0,1)$。對 $\operatorname{Cone}(q)[-1]$ 消去這個同構對，得到 $[R^2\xrightarrow B R^2]$。

增廣到 $O$ 後，其 $H^1$ 是 $E(\mathbb Q)\otimes O$：在輔助素點，整 Tate module 的 relaxed 與有限 $H^1$ 相同，且既有 Sha 輸入消除額外 Tate module。故 $\ker B(0)$ 在 $O^2$ 中有秩二。$O$ 是整域，因而 $B(0)=0$。可以使兩個增廣基向量對應 $P,Q$。

原模型是 minimal，故 $c(0)\in11O^2$。所以 $H^2(\mathcal S\otimes_R^{\mathbf L}k)$ 到 $H^2(C\otimes_R^{\mathbf L}k)$ 的自然映射是同構；此處亦可直接由矩陣在 $R\to k$ 下的特化看出。Bockstein 的自然性遂將既有一階矩陣搬到 $B$。證畢。

上段最後的 base change 均指係數環經 $R\to O\to k$ 的導出特化；不是把 $M$ 當作不變的 $O$-表示只對 $11$ 取商。

令

$$
D=\det B.
$$

於是 $D\in I^2$，且

$$
\overline D=2XY\pmod{\overline I^3}.
$$

這一步將一階局部關係接到一個真正 perfect 的、在 $11$ 有有限條件的全域複形之行列式。它依然帶有輔助 relaxed 條件，並非完整 BSD 高度公式。

## 3. 直接構造全域候選類

**引理 3.1（任意交換環上的恆等式）。** 對 $A=(B\ c)$，定義

$$
z_{\det}:=
\begin{pmatrix}-\operatorname{adj}(B)c\\D\end{pmatrix}\in R^3.
$$

則

$$
Az_{\det}=0,\qquad q(z_{\det})=D.
$$

**證明。** $B\operatorname{adj}(B)=D\operatorname{id}$，所以 $Az_{\det}=-Dc+cD=0$；最後一個座標就是 $D$。證畢。

因此 $z_{\det}$ 已由算術複形構造為 $H^1(C)$ 中的元素。它是固定自由模型與 determinant 基底下的 cofactor 類；基底改變時須連同 determinant line 一起搬移，不能把座標向量叫做絕對 canonical 的類。

若 $B=\left(\begin{smallmatrix}a&b\\d&e\end{smallmatrix}\right)$、$c=(c_1,c_2)^{\mathrm t}$，則完全明示為

$$
z_{\det}=(bc_2-ec_1,\ dc_1-ac_2,\ ae-bd)^{\mathrm t}.
$$

這個構造的意義是：原始 Kato 類在 $11$ 處有非零像，並不妨礙 determinant 比較。候選 $z_{\det}$ 本來也有非零的局部像。應比较這兩個全域類，而非要求原始 Kato 類先進入有限 Selmer 群。

## 4. 有限層為何不能直接相除

記 $H=\ker A$、$K=\ker B$，並令

$$
J=\{h\in R:hc\in BR^2\}
=\operatorname{Ann}_R([c]\in\operatorname{coker}B).
$$

第三座標給出正合列

$$
0\longrightarrow K\longrightarrow H\xrightarrow q J\longrightarrow0.
$$

真正的 Kato 類寫為 $z_{\mathrm K}=(x,h)$；其 cocycle 方程只給出

$$
Bx=-ch,\qquad h\in J.
$$

而 $z_{\det}$ 給出的是 $DR\subseteq J$。這個包含不自動是等號。

進一步，直接對上述正合列取商得到

$$
\operatorname{Ann}_R(D)\longrightarrow K\longrightarrow
H/Rz_{\det}\longrightarrow J/DR\longrightarrow0,
$$

第一個映射為 $a\mapsto-a\operatorname{adj}(B)c$。這把有限層的缺口分成兩個實際模：整除障礙 $J/DR$，以及整除後可能剩下的 $K$ 分量。由 $h$ 和 $D$ 有相同的消失階，不能直接把兩個模判為零。

## 5. Kato 的局部標量與 tame norm 的新連接

選取 $11$ 處局部商的基底，使局部線性泛函由 formal-group 點 $c_F$ 與 Tate pairing 給出。具體地，$a_{11}=-4$，而

$$
\left(1-\frac{a_{11}}{11}\operatorname{Fr}_{11}
+\frac1{11}\operatorname{Fr}_{11}^2\right)\log_\omega(c_F)
=\operatorname{Tr}_{\mathbb Q(\zeta_m)/F}(\zeta_m),\qquad m=397\cdot991.
$$

右側給出 $O_F\otimes\mathbb Z_{11}$ 的群環 normal basis；左側在 formal-group lattice 上可逆，因相應整算子的增廣是 $11-a_{11}+1=16$，為 unit。這是 [BKS II，式 (19) 與 Proposition 5.1](https://arxiv.org/html/2103.11535v1#S5.SS1) 的局部點建構與互反律；其這一局部推导不需令兩個輔助素點的 $11$-torsion 消失。本文不套用該文刪除所有輔助局部商的後續定理。

在相容的週期、smoothing 去除、Shapiro／Artin 慣例下，局部座標為

$$
h=q(z_{\mathrm K})=\theta_{F,S},\qquad S=\{397,991,389\}.
$$

若改變局部基底，只會同時乘上一個 $R$-unit。$S$ 在這一插值記號中不含 $11$；$11$ 的 Euler 算子已在局部點正規化中處理。

現在可直接寫出 conductor 修正，而不只逐 character 比較：

$$
N_\gamma=\sum_{i=0}^{10}\gamma^i,\quad
N_\eta=\sum_{i=0}^{10}\eta^i,\qquad
U_m=(1+36N_\gamma)(1+90N_\eta).
$$

**引理 5.1。** $U_m\in R^\times$，且對每個 character $\chi$，

$$
\chi(U_m)=m/f_\chi.
$$

**證明。** 若 $\chi$ 在一個輔助因子上非平凡，該因子的 norm 和為零；若平凡，norm 和為 $11$，對應因子分別成為 $397$ 或 $991$。兩因子相乘恰給出 $m/f_\chi$。此外 $\epsilon(U_m)=m\equiv1\pmod{11}$，所以在局部環 $R$ 中為 unit。證畢。

這兩個因子正是 tame 複形中的 norm 算子。它們同時控制局部 cochain 與 modular-element 的 conductor 修正。

若 $\theta_{F,m}$ 是相容尺度的原 modular element，則插值公式給出

$$
h=U_m^{-1}\left(1-389^{-1}\operatorname{Fr}_{389}^{-1}\right)\theta_{F,m}.
$$

壞素點因子的增廣是 $388/389\equiv9\pmod{11}$，也為 unit。故既有首項非零性直接給出

$$
\overline h=\kappa XY\pmod{\overline I^3},\qquad\kappa\in k^\times.
$$

這裡沒有算出所有整係數，也沒有用期望的 BSD 常數定義 $h$。若先前 canonical 尺度是 $5u_0XY$，上述相容正規化給出 $\kappa=9\cdot5u_0=u_0$。

## 6. 真正的新攻擊：先升到 cyclotomic 族，再下降

令 $\mathbb Q_\infty/\mathbb Q$ 為 cyclotomic $\mathbb Z_{11}$-擴張。它與 $F$ 相交於 $\mathbb Q$，設

$$
\Gamma=\operatorname{Gal}(\mathbb Q_\infty/\mathbb Q),\qquad
\Omega=O[G][[\Gamma]]\simeq R[[t]].
$$

對 $F\mathbb Q_\infty$ 的真正 Iwasawa cochain 與局部商作相同建構，得到候選相容模型

$$
A_\infty=(B_\infty\ c_\infty),\quad
q_\infty=(0,0,1),\quad D_\infty=\det B_\infty,
$$

以及 Kato 的 norm-compatible 類 $z_{\mathrm K,\infty}$。這裡必須使用真實 Galois 族；不能任意給有限矩陣加上 $t$，再宣稱已構造 Iwasawa 複形。以下定理明示假設這些模型及 $t=0$ 特化已相容。

**定理 6.1（條件性完成定理；證明如下）。** 假設：

1. 上述相容模型存在，$z_{\mathrm K,\infty}\in\ker A_\infty$，其局部座標 $h_\infty=q_\infty(z_{\mathrm K,\infty})$ 在 $t=0$ 特化為第 5 節的 $h$。
2. $D_\infty$ 是 $\Omega$ 的非零因子。
3. 下述一側整除在整群環中成立：

$$
\boxed{h_\infty\in D_\infty\Omega.}
$$

則存在 $u_\infty\in\Omega^\times$ 使

$$
z_{\mathrm K,\infty}=u_\infty
\begin{pmatrix}-\operatorname{adj}(B_\infty)c_\infty\\D_\infty\end{pmatrix}.
$$

特化後得到 $z_{\mathrm K}=u_Fz_{\det}$，其中 $u_F\in R^\times$。

**證明。** 由整除假設寫 $h_\infty=u_\infty D_\infty$，此時尚不知 $u_\infty$ 是 unit。寫 $z_{\mathrm K,\infty}=(x_\infty,h_\infty)$，則

$$
B_\infty x_\infty=-c_\infty h_\infty.
$$

與伴隨矩陣恆等式相減，得

$$
B_\infty\left(x_\infty+
u_\infty\operatorname{adj}(B_\infty)c_\infty\right)=0.
$$

再左乘 $\operatorname{adj}(B_\infty)$，得到 $D_\infty$ 乘上括號內的向量為零。$D_\infty$ 是非零因子，故括號為零，得到所需全域類等式。

將第三座標特化到 $t=0$，再模 $11$ 與 $\overline I^3$，得

$$
\kappa XY=2\overline\epsilon(u_F)XY.
$$

$XY$ 在 $\overline I^2/\overline I^3$ 非零，且 $\kappa\ne0$，所以

$$
\overline\epsilon(u_F)=\kappa/2\ne0.
$$

這正是 $u_\infty$ 在 $\Omega$ 的極大理想 $(11,X,Y,t)$ 之外的條件，故 $u_\infty$ 及 $u_F$ 都是 unit。證畢。

這個推導有兩個實際作用。第一，原本有限層的 $\ker B$ 歧義，在 $D_\infty$ 正則的族中被消去；下降時得到的是 norm-compatible 族所選定的類。第二，只需一側整除，再由已知首項的 primitivity 升級成 unit 比較，不需先假设完整的雙側主猜想。

非零因子假設可以朝兩個方向處理：證明相應 Selmer 複形在每個 characteristic-zero 分支 generically acyclic；或先證明 $h_\infty$ 是非零因子，此時整除式本身就迫使 $D_\infty$ 為非零因子。後者可嘗試由 twisted $L$ 值非消失與互反律處理。本稿沒有把所有分支的這一算術輸入標為完成；有限層的 $100$ 個混合 characters 也不涵蓋所有分支。

## 7. 我實際嘗試了哪一個證法，卡在哪裡

最直接的證法是先在 characteristic-zero characters 上使用 Euler-system bound，得到每一分支的整除，再把商黏回 $\Omega$。它的精確缺口是

$$
u_\infty=h_\infty/D_\infty\in\widetilde\Omega
\quad\not\Longrightarrow\quad u_\infty\in\Omega,
$$

其中 $\widetilde\Omega$ 表示 normalization。群 $G$ 的階被 $11$ 整除；整群環的分支之間帶有同餘黏合條件。character-wise 的 unit 也不能取代這些條件。

這不只是抽象疑慮。取簡單的整環

$$
R_0=O[C_{11}],\quad X_0=g-1,\quad
N_0=\sum_{i=0}^{10}g^i,\quad
u=1+N_0/11.
$$

在 $R_0\otimes\mathbb Q_{11}$ 中，$u$ 的 trivial 分支是 $2$，所有非平凡分支是 $1$，每一分支都是 unit，但 $u\notin R_0$。若令

$$
D_0=11+X_0,\qquad h_0=D_0+N_0,
$$

則 $X_0N_0=0$，故 $h_0=D_0u$。$D_0$ 在每一 characteristic-zero 分支非零，所以是非零因子。各分支的商都是 integral unit，然而 $h_0\notin D_0R_0$。同一反例亦可放入 $R_0[[t]]$。這證明逐分支整除的證法缺了一個真正的步驟。

因此下一個應投入數學創造力的命題是：

**候選核心引理（尚未證明）。** 對本文保留輔助局部條件資訊的 Iwasawa 複形，Kato 的整 Euler-system norm 關係迫使 $h_\infty$ 落在 $D_\infty\Omega$，包含 $11$ 上不同 characteristic-zero 分支之間的全部整同餘。

我傾向直接攻這個引理的理由是：它要求的是一側整除，定理 6.1 已說明其餘 unit 與全域類比較如何推出。具體入口是將 Kato 的 norm 關係搬到 determinant model，證明商在 $\widetilde\Omega/\Omega$ 中的類為零。必須保留第 5 節的 $U_m$ 與輔助局部項；只使用 characteristic ideals 或把 torsion 商去掉，會遺失正要證明的同餘。

這個引理含有實質的等變主猜想內容。我目前沒有證出它，也不把「Euler system 應該可以」當作證明。[BKS I，Proposition 3.3](https://arxiv.org/html/1910.07404v2#S3.SS1) 的直接版本要求所有相關局部 $p$-torsion 消失，本例兩個輔助素點不滿足，不能直接引用結束。

## 8. 對更高秩及完整 BSD 的作用範圍

伴隨矩陣推導對任意 $r\times r$ 矩陣 $B$、一欄 $c$ 都成立。若真正的 rank-$r$ 算術問題能建立 $A=(B\ c)$、一維局部商以及非零的 degree-$r$ 首項，定理 6.1 的 unit 升級原封不動。因此這裡抽取的是可移植的證明機制，$389a1$ 是當前具體試驗場。

不過，即使完成上述 unit 比較，也仍只得到指定整格下的 $p$-進 determinant／Kato 關係。從它到完整 BSD，還需要與複數首項和 Néron–Tate regulator 的精確正規化比較；一個未確定的 $p$-進 unit 不等於已得到 BSD 的精確常數。其他曲線、其他素數與所有秩亦須另行涵蓋。

本稿把數學主攻點固定為第 7 節的整等變整除，不以更多舊證書重播替代它。前文代數證明是本輪推導；核心算術引理及其 Iwasawa 全分支輸入保持候選狀態，未據此改寫已證 frontier。

## 參照

- Burns–Kurihara–Sano，[On derivatives of Kato's Euler system for elliptic curves](https://arxiv.org/html/1910.07404v2)：環境複形、導出下降與局部 torsion 的問題。
- Burns–Kurihara–Sano，[On derivatives of Kato's Euler system and the Mazur–Tate conjecture](https://arxiv.org/html/2103.11535v1)：第 2 節的 modular-element normalization、第 5.1 節的局部 pairing 身分。本文另外保留不符合其整體假設的輔助項。
- Milne，[Arithmetic Duality Theorems](https://www.jmilne.org/math/Books/ADTnot.pdf)：有限全域對偶與 Selmer 條件比較所用的基礎。

來源驗證只涵蓋上述實際使用的外部結果；本文沒有宣称已讀完 Kato 原始論文，也沒有把符號推導稱為 proof-assistant 驗證。
