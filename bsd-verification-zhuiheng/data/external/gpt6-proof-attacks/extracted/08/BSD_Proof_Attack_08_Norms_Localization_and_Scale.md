# BSD Proof Attack 08：精確範數、定位邊界與尺度歧義

日期：2026-09-12  
狀態：書面推導與精確代數計算完成；尚未經獨立形式化或學術審查。  
範圍：推進 Attack 07 的幾何鏈與 Attack 06 的 Kato 尺度問題；不重播先前算術 certificates，不更新 canonical frontier。

本輪得到三項具體結果：算完上一輪鏈沿三個自然映射的推送；構造在座標正規化後仍能消除常數的封閉修正；用定位序列寫出確實落入橢圓曲線點類的懸吊。最後一項修正了直接推送的次數問題，但沒有建立幾何邊界與 cyclotomic 導出類的比較。

## 1. 接受的輸入與本輪問題

全篇在 $\mathbb Q$ 上工作；寫 higher Chow 群時使用有理係數，除非特別指出某條鏈具有整數係數。

$$
E:\quad y^2+y=x^3+x^2-2x,\qquad
P=(0,0),\quad Q=(1,0),\quad R=P+Q=(-2,-1).
$$

令 $O$ 為無窮遠點，$A=E\times E$，並置

$$
Z_{PQ}=[(P,Q)]-[(P,O)]-[(O,Q)]+[(O,O)].
$$

Attack 07 提供曲線 $C$：它是以下非對角分量的光滑完備正規化：

$$
y_1=y_2=y,\qquad
x_1^2+x_1x_2+x_2^2+x_1+x_2-2=0.
$$

映射 $\phi:C\to A$ 取兩個有序點。函數及輔助曲線為

$$
g=2x_1+3x_2-3,\qquad
H_-=E\times\{-Q\},\quad
V_P=\{P\}\times E,\quad V_O=\{O\}\times E.
$$

接受上一輪已建立的整數鏈等式

$$
\Gamma=(C,g)-2(H_-,x_1)
+2(V_P,x_2-1)-4(V_O,x_2-1),
\qquad
\partial\Gamma=4Z_{PQ}.
\tag{1}
$$

這裡 $(C,g)$ 簡記經 $\phi$ 推入 $A$ 的函數鏈。$\Gamma$ 有非零鏈邊界；不能把它直接寫成 $CH^2(A,1)$ 的封閉類。

本輪研究

$$
\pi_1,\pi_2:A\to E,\qquad m:A\to E,\quad m(S,T)=S+T.
$$

對函數鏈 $B=\sum n_i(C_i,f_i)$，定義其乘法記號的推送

$$
F_h(B)=
\prod_{\dim h(C_i)=1}
N_{\mathbb Q(C_i)/\mathbb Q(E)}(f_i)^{n_i}.
\tag{2}
$$

式中使用支撐曲線的正規化。被收縮的曲線不貢獻函數項；其主除子的零次數使邊界推送也為零。整數鏈時式 (2) 是有理函數；有理係數鏈時解讀於 $\mathbb Q(E)^\times\otimes_{\mathbb Z}\mathbb Q$。範數與除子相容給出

$$
\operatorname{div}F_h(B)=h_*(\partial B).
\tag{3}
$$

## 2. 三個範數全部算清楚

### 命題 08.1

沿 $C$ 的三個二次映射，範數恰為

$$
\boxed{
N_{\pi_1\phi}(g)=7x^2,\qquad
N_{\pi_2\phi}(g)=7(x-1)^2,\qquad
N_{m\phi}(g)=7(x+2)^2.
}
\tag{4}
$$

**證明。** 在固定的共同 $y$ 上，三個橫座標是

$$
X^3+X^2-2X-y^2-y
$$

的根。固定其中一根 $x$，另兩根 $r,s$ 滿足

$$
r+s=-1-x,\qquad rs=x^2+x-2.
\tag{5}
$$

因此

$$
N(a+br)=a^2+ab(-1-x)+b^2(x^2+x-2).
\tag{6}
$$

第一、第二個投影分別取

$$
(a,b)=(2x-3,3),\qquad (a,b)=(3x-3,2),
$$

展開便得到前兩式。

三個同高點共線，故群律給出 $p_1+p_2+p_3=O$；加法映射的輸出是 $-p_3$，其橫座標仍為第三根 $x$。此時

$$
g=2r+3s-3=-5-2x+s.
$$

代入 $(a,b)=(-5-2x,1)$ 得第三式。負點改變縱座標為 $-y-1$，但不改變 $y^2+y$。這些是函數域恆等式，不是有限精度近似。證畢。

### 命題 08.2

完整鏈的三個推送是

$$
\boxed{
F_{\pi_1}(\Gamma)=7,\qquad
F_{\pi_2}(\Gamma)=7,\qquad
F_m(\Gamma)=7M^4,\quad M=\frac{x+2}{y}.
}
\tag{7}
$$

**證明。** 第一投影保留 $(C,g)$ 與水平鏈，故

$$
F_{\pi_1}(\Gamma)=7x^2x^{-2}=7.
$$

第二投影保留 $(C,g)$ 與兩條垂直鏈，故

$$
F_{\pi_2}(\Gamma)=7(x-1)^2(x-1)^2(x-1)^{-4}=7.
$$

計算加法推送時，以 $T=(x,y)$ 為目標點。水平鏈的原座標是 $T+Q$，$V_P$ 的第二座標是 $T-P$。群律給出

$$
A(T):=x(T+Q)=\frac{x^2+x-2-y}{(x-1)^2},
$$

$$
B(T):=x(T-P)-1=\frac{y+1-x^2-2x}{x^2}.
\tag{8}
$$

其中第一式由斜率 $y/(x-1)$ 得到；第二式用 $-P=(0,-1)$ 及斜率 $(y+1)/x$ 得到。利用曲線方程可得含符號的恆等式

$$
\frac BA=-\frac{(x+2)(x-1)^2}{y^2}.
\tag{9}
$$

例如交叉相乘後要證明的分子為

$$
y^2(y+1-x^2-2x)+x^2(x+2)(x^2+x-2-y)=0;
$$

代入 $y^2=x^3+x^2-2x-y$ 後恰為零。因此

$$
\begin{aligned}
F_m(\Gamma)
&=7(x+2)^2A^{-2}B^2(x-1)^{-4}\\
&=7\frac{(x+2)^4}{y^4}=7M^4.
\end{aligned}
$$

有理函數等式先在分母不為零的稠密開集成立，故在整個函數域成立，不需要逐點排除所有零點。證畢。

除子也能直接辨認：

$$
\operatorname{div}(x+2)=[R]+[-R]-2[O],
$$

$$
\operatorname{div}(y)=[P]+[Q]+[-R]-3[O],
$$

因而

$$
\boxed{
\operatorname{div}M=[R]-[P]-[Q]+[O]=m_*Z_{PQ}.
}
\tag{10}
$$

式 (7) 與式 (1) 的加法邊界精確相容。

## 3. 更強的結果：座標正規化仍不能固定常數

令 $H_0=E\times\{O\}$，取封閉常數鏈

$$
\Xi_7=(H_0,7)+(V_O,7),\qquad \partial\Xi_7=0,
$$

並設 $\Gamma^0=\Gamma-\Xi_7$。立即得到

$$
\partial\Gamma^0=4Z_{PQ},
$$

$$
\boxed{
F_{\pi_1}(\Gamma^0)=F_{\pi_2}(\Gamma^0)=1,\qquad
F_m(\Gamma^0)=M^4/7.
}
\tag{11}
$$

這已顯示 $7$ 取決於封閉部分。但尚可更進一步。

### 命題 08.3

令 $\Delta=\{(T,T):T\in E\}$。對 $c\in\mathbb Q^\times$，

$$
\Theta_c=(\Delta,c)-(H_0,c)-(V_O,c)
\tag{12}
$$

是封閉鏈，且

$$
\boxed{
F_{\pi_1}(\Theta_c)=F_{\pi_2}(\Theta_c)=1,\qquad
F_m(\Theta_c)=c^2.
}
\tag{13}
$$

**證明。** 常數函數的除子為零。三條支撐曲線上的映射次數如下；被收縮者記為 $0$：

| 支撐 | $\pi_1$ | $\pi_2$ | $m$ |
|---|---:|---:|---:|
| $\Delta$ | $1$ | $1$ | $4$ |
| $H_0$ | $1$ | $0$ | $1$ |
| $V_O$ | $0$ | $1$ | $1$ |

最後一欄的 $4$ 來自 $m|_\Delta=[2]$，在特徵零橢圓曲線上次數為 $4$。常數的範數是常數的映射次數次方，所以式 (13) 的指數是

$$
(1,1,4)-(1,0,1)-(0,1,1)=(0,0,2).
$$

證畢。

特別地，在有理係數鏈群取

$$
\Gamma^1=\Gamma^0+\frac12\Theta_7.
$$

則

$$
\boxed{
\partial\Gamma^1=4Z_{PQ},\qquad
F_{\pi_1}(\Gamma^1)=F_{\pi_2}(\Gamma^1)=1,\qquad
F_m(\Gamma^1)=M^4.
}
\tag{14}
$$

此式不需添加 $\sqrt7$：有理係數群中 $\tfrac12[7^2]=[7]$。式 (14) 的推送以乘法記號表示其在 $\mathbb Q(E)^\times\otimes\mathbb Q$ 中的值。

更一般地，加入 $\tfrac12\Theta_c$ 保持邊界及兩個座標正規化，卻把加法投影乘以任意 $c\in\mathbb Q^\times$。這個歧義是真正的 higher Chow 歧義：例如 $\Theta_7$ 的加法推送是 $[49]\ne0$ 於

$$
CH^1(E,1)_{\mathbb Q}=\mathbb Q^\times\otimes\mathbb Q.
$$

它不可能已是 tame-symbol 邊界。

因此，**只給定式 (1) 的邊界，以及兩個座標投影等於 $1$，仍不足以從加法投影選出唯一常數。** 不能把這裡出現的 $7$ 指認為 Attack 06 的 $s_{11}$。

此結論針對函數鏈與其單位投影。沒有據此宣稱正規化後的全域高度會隨意改變；全域高度含有局部配對與乘積公式，必須另外比較。

## 4. 直接接 Kato 的精確失敗位置

### 命題 08.4：直接推送的目標群不對

對真正封閉的類，這些 proper pushforward 的型別是

$$
CH^2(E^2,1)_{\mathbb Q}
=H_{\mathcal M}^3(E^2,\mathbb Q(2))
\longrightarrow
CH^1(E,1)_{\mathbb Q}
=H_{\mathcal M}^1(E,\mathbb Q(1)).
\tag{15}
$$

因為 $E$ 是幾何連通的完備曲線，右端是 $\mathbb Q^\times\otimes\mathbb Q$。

反之，橢圓曲線有理點所對應的除子類位於

$$
E(\mathbb Q)\otimes\mathbb Q
\simeq \operatorname{Pic}^0(E)_{\mathbb Q}
\subset CH^1(E,0)_{\mathbb Q}
=H_{\mathcal M}^2(E,\mathbb Q(1)).
\tag{16}
$$

第一個目標的單位 regulator 屬於 Tate 的

$$
H^1(\mathbb Q,\mathbb Q_{11}(1));
$$

第二個目標的度零部分才經 Kummer 映射進入

$$
H^1(\mathbb Q,V),\qquad V=T_{11}E\otimes\mathbb Q_{11}.
$$

普通代數 correspondence 的 pullback、與普通 cycle 相交、proper pushforward 都保留 higher Chow 指標 $q$。式 (15) 仍有 $q=1$，式 (16) 卻是 $q=0$。這是次數及 regulator 目標的失配。

對非封閉的 $\Gamma$，更不能跳過此問題：取 $F_m(\Gamma)$ 的除子只得到主除子 $4\operatorname{div}M$，在 $\operatorname{Pic}(E)$ 的類為零。

**失敗步驟已定位為：從鏈的普通推送／單位 regulator，直接認作橢圓曲線 Selmer 類。** 加高數值精度、取得更多模素數值，或把單位重命名，都不會更改目標群。

本命題不排除帶有定位邊界、退化、相對 regulator、譜序列邊界等額外操作的構造；這些操作正是可能改變次數的地方。

## 5. 可以完成的修正：明確定位懸吊

取新的幾何參數 $\tau$，令

$$
X=E\times\mathbb A^1_\tau,\quad
U=E\times\mathbb G_{m,\tau},\quad
i:E_0\hookrightarrow X,\quad j:U\hookrightarrow X.
$$

這裡的 $\tau$ 尚未、也不自動等於 Iwasawa 參數 $t=\gamma-1$。

使用 higher Chow 定位序列

$$
CH^2(U,1)_{\mathbb Q}
\xrightarrow{\partial_0}
CH^1(E,0)_{\mathbb Q}.
\tag{17}
$$

採用除子在 $\tau=0$ 有正號的邊界慣例。定位序列的次數、與乘積及 proper pushforward 的相容性，可參照 [del Ángel 等，Specialization of cycles and the K-theory elevator，§3.1](https://arxiv.org/html/1704.04779v2#S3.SS1)。

### 命題 08.5

以下是 $U$ 上的封閉 higher Chow cycles：

$$
\mathcal S_P=(\{P\}\times\mathbb G_m,\tau)
-(\{O\}\times\mathbb G_m,\tau),
$$

$$
\mathcal S_Q=(\{Q\}\times\mathbb G_m,\tau)
-(\{O\}\times\mathbb G_m,\tau).
\tag{18}
$$

其定位邊界為

$$
\boxed{
\partial_0\mathcal S_P=[P]-[O],\qquad
\partial_0\mathcal S_Q=[Q]-[O].
}
\tag{19}
$$

**證明。** $\tau$ 在 $\mathbb G_m$ 上可逆，故式 (18) 在 $U$ 內沒有除子邊界。將每條支撐曲線閉包到 $X$，有

$$
\operatorname{div}_{\mathbb A^1}(\tau)=[0].
$$

因此閉包邊界分別為 $[(P,0)]-[(O,0)]$ 與 $[(Q,0)]-[(O,0)]$。透過 $E_0\simeq E$ 即得式 (19)。證畢。

先前接受的 $P,Q$ 非扭性保證右端是非零的有理 Picard 類。對度零除子施行 étale cycle class，再取橢圓曲線的 Kummer 分量，確實得到 $P,Q$ 的 Kummer 類。這裡只是定位／Kummer 的自然性，不涉及 Kato 類的認同。

這是可用的次數修正：式 (17) 確實把 $q=1$ 降到 $q=0$。

## 6. 常值乘法群模型的完整分類

### 命題 08.6

在此模型中有分裂短正合列

$$
0\longrightarrow CH^2(E,1)_{\mathbb Q}
\xrightarrow{\operatorname{pr}^*}
CH^2(E\times\mathbb G_m,1)_{\mathbb Q}
\xrightarrow{\partial_0}
\operatorname{Pic}(E)_{\mathbb Q}
\longrightarrow0,
\tag{20}
$$

其一個顯式截面是

$$
s_\tau(D)=D\times\{\tau\},\qquad
\partial_0s_\tau(D)=D.
\tag{21}
$$

因此

$$
\boxed{
CH^2(E\times\mathbb G_m,1)_{\mathbb Q}
\simeq
CH^2(E,1)_{\mathbb Q}\oplus\operatorname{Pic}(E)_{\mathbb Q}.
}
\tag{22}
$$

**證明。** 定位長正合列的相關片段為

$$
CH^1(E,1)_{\mathbb Q}
\xrightarrow{i_*}CH^2(X,1)_{\mathbb Q}
\xrightarrow{j^*}CH^2(U,1)_{\mathbb Q}
\xrightarrow{\partial_0}CH^1(E,0)_{\mathbb Q}
\xrightarrow{i_*}CH^2(X,0)_{\mathbb Q}.
$$

同倫不變性使 $X\to E$ 的拉回為同構，零截面的 $i^*$ 是其逆。零截面的法叢平凡，自交公式給出

$$
i^*i_*(a)=c_1(\mathcal O_E)\cdot a=0.
$$

由 $i^*$ 為同構，兩個相應的 $i_*$ 均為零。因此得到短正合列。乘積 $D\times\{\tau\}$ 定義在 Chow 類上，式 (19) 的同一計算對任意除子 $D$ 給出截面。證畢。

具體而言，每個 $\mathcal Z\in CH^2(U,1)_{\mathbb Q}$ 唯一分解成

$$
\mathcal Z=\operatorname{pr}^*\xi+s_\tau(D),\qquad
D=\partial_0\mathcal Z,\quad \xi\in CH^2(E,1)_{\mathbb Q},
\tag{23}
$$

其中唯一性相對於已選定的截面 $s_\tau$。

這個分類有兩項直接推論：

1. 常值模型中的非零點邊界，是懸吊時所放入的除子類。加入此模型本身，沒有由 $\Gamma$ 自動選出一個新 Kato 類。
2. 邊界不決定可延伸的封閉部分。例子是加入 $\operatorname{pr}^*(O,7)$：它在 $X$ 上已定義，故邊界為零；它在 $U$ 上卻不為零，因為沿 $U\to\mathbb G_m$ 推送得到非零單位 $7$。

改參數 $\tau\mapsto c\tau$ 時也有精確公式

$$
s_{c\tau}(D)-s_\tau(D)
=\operatorname{pr}^*(D\cdot\{c\}).
\tag{24}
$$

右端是可延伸類，故不改變邊界。式 (24) 沒有斷言對每個度零 $D$ 與每個 $c$，其右端必非零；非零歧義已有上一段獨立例子。

還須區分兩種不同操作：文獻的 specialization 是

$$
\operatorname{Sp}_\tau(z)=\partial_0(\{\tau\}\cdot z),
$$

它保留 $q$；式 (17) 的定位邊界本身才降低 $q$。不能以同一個「特殊化」名稱混用兩者。此定義見同一文獻 [§3.1，式 (3.1)](https://arxiv.org/html/1704.04779v2#S3.SS1)。

## 7. 接下來必須解的比較問題

Attack 06 的固定正規化輸入是

$$
\kappa^\dagger
=16s_{11}\operatorname{adj}(H)\ell,\qquad
s_{11}=\frac{a_2}{e_{11}\det H},
\tag{25}
$$

其中 $L_p(t)=a_2t^2+\cdots$，$\ell=\log_\omega/11$，$H$ 是先前固定符號與尺度的高度矩陣，$e_{11}=(1-\alpha^{-1})^2$。$s_{11}$ 的值與所需的有理下降仍未證明。

本輪式 (19) 的成功不足以推出式 (25) 的幾何解釋。至少仍缺以下實際資料：

1. 一個與 Kato／Euler-system 類相容的族或相對 cycle 構造，且其 Euler、Hecke、period 正規化全部固定。
2. 一個可檢查的比較，使幾何邊界的 étale realization 對應到所需的 cyclotomic leading-term 操作；不能只作變數代換 $\tau=t$。
3. 對式 (23) 的封閉部分，以及 Attack 07 的相對高度／局部 splitting，給出能消除式 (12) 歧義的條件。

次數還要再分清：Iwasawa 一階係數擴張的 Bockstein 在上同調中是

$$
\beta:H^1(\mathbb Q,V)\longrightarrow
H^2(\mathbb Q,V)\otimes I/I^2,\qquad I=(t),
$$

而已可除以 $t$ 的 Iwasawa 類所取的 $(z_\infty/t)\bmod t$ 仍是 $H^1$ 的 leading term。這兩者也不是同一映射。要將它們接到式 (17)，必須提出真正的導出層級比較與其次數位移。

**下一個具體突破口是帶正規化的 Euler-system 退化比較。** Loeffler–Rivero 的 [Eisenstein degeneration of Euler systems，Proposition C1.12、Theorem C1.13 與 Remark C1.14](https://arxiv.org/html/2201.02078v2) 在其假設下，已把 Eisenstein 退化所得 leading class 與 Kato 類比較，公式仍含 $C=c_{\mathbf f}^*(r)\in L^\times$；證明使用 regulator 比較及相關 Selmer 消失。這提供可研究的比較機制，沒有直接給出我們的有理尺度。

本輪沒有選出滿足該文全部假設的輔助族，也沒有把文中 $C$ 算成本文的 $7$ 或 $s_{11}$。下一步的明確目標是：在具體可用的族中辨認這個 leading period 因子，並比較到固定 determinant line。只得到「相差一個非零 $L$ 元素」仍不足以完成有理下降。

最後，所需的有理性應放在正確的物件上。即使 $s_{11}\in\mathbb Q$，式 (25) 的 $\operatorname{adj}(H)\ell$ 仍含 $11$-adic 高度與對數，因此不能要求 $\kappa^\dagger$ 本身必是一個有理係數 Mordell–Weil 點。先前的目標是 determinant 元素

$$
\eta_{11}=s_{11}b,\qquad
b=(P\wedge Q)^{\otimes2}\otimes\delta_+,
$$

的有理提升，以及同一提升的無窮遠 regulator 與 $L''(E,1)/2$ 的比較。這兩步本輪皆未建立。

## 8. 計算證據與交接邊界

**attack08_correspondence.py** 僅使用 Python 標準函式庫，在

$$
\mathbb Q[x,y]/(y^2+y-x^3-x^2+2x)
$$

中以 $a(x)+b(x)y$ 表示元素，交叉相乘檢查有理函數恆等式。沒有使用浮點近似。

本輪執行得到：

| 項目 | 結果 | 證據層級 |
|---|---|---|
| 三個新範數 | $7x^2,\ 7(x-1)^2,\ 7(x+2)^2$ | 整數多項式精確展開 |
| 平移比值的負號 | 式 (9) 成立 | 函數域殘差為零 |
| 完整加法推送 | $7M^4$ | 函數域殘差為零 |
| 封閉修正的指數 | $(0,0,2)$ | 使用 $[2]$ 次數 $4$ 的精確記帳 |
| 消除常數後 | $(1,1,M^4)$ | 有理係數精確記帳 |
| 懸吊邊界 | $P-O,\ Q-O$ | 有限除子記帳＋第 5 節書面推導 |
| 完整分裂與次數障礙 | 式 (15)–(24) | 標準理論下的書面證明，非程式證明 |
| Kato／cyclotomic 比較 | 尚未構造 | 明確未完成 |
| $s_{11}$、複數 leading term | 尚未確定／比較 | 明確未完成 |

程式中的除子支撐與映射次數由本稿的群律及幾何論證提供；通過精確記帳並不等於程式自行證明了 higher Chow 理論、所有 regulator 相容性或 BSD。

交接時可獨立核查的新節點是式 (8)–(9) 的符號、$\Theta_c$ 的映射次數、有理係數的使用、定位邊界的符號，以及式 (20) 中的自交與同倫不變性。無須為檢查本輪代數而重跑先前 Kurihara、模符號或高度 certificates。

**本輪完成自然推送及其尺度歧義的計算，並完成常值模型的次數修正。缺口已收斂為帶 period 與封閉部分正規化的 Euler-system／相對 regulator 比較。BSD 尚未證明，canonical frontier 保持原狀。**
