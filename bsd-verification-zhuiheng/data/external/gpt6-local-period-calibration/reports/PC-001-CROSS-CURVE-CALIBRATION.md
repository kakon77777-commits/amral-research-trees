# PC-001：用秩零曲線校準 rank-2 BSD 退化公式

日期：2026-09-13。研究方向由 Neo.K 指定；目前發話身份 `unresolved`。

本輪有兩個結果：在共同規範下，推出消去 Eisenstein 比較常數的跨曲線公式；並從有理模符號構造出滿足所需非零條件的校準曲線 `19.a1`。這是對 Attack 09–10 的額外研究路線。以下稱「命題」者有列明假設及證明；不主張文獻新穎性，也沒有得到 BSD 的完整證明。

## 1. 要消去的是共同常數

設目標曲線為 `389.a1`，`p=11`，輔助形式仍為 `E_2(1,chi_8)` 的 critical refinement。固定同一條輔助族、權重座標 X、Eisenstein 商映射及 period frame。令

\[
L=\log_{11}(12),\qquad j(t)=\frac{\log(1+t)}{L}.
\]

X 是輔助權重方向，t 是 cyclotomic 方向。對普通 partner i，先取 X-leading class，再以同一個輔助商映射投影，記為 \(\widehat B_i(t)\)。採相容的 Kato、Coleman、Gauss 與 adjoint 規範，退化關係寫成

\[
\widehat B_i(t)=C_\pi A_i(t)j(t)z_i(t),
\quad
A_i(t)=\frac{\mathscr S_5(t)\lambda_i(t)}{D_i}.
\tag{1}
\]

使用的文獻事實是 Loeffler–Rivero C1.9–C1.13 的退化比較及 C1.11 的唯一性：固定輔助 frame 後，meromorphic ES 映射由輔助族決定。將同一個輔助 quotient transport 用於各 partner，便得到式 (1) 的共同 \(C_\pi\)。這裡特意沒有把它直接等同於任意原始座標下的 \([X^n]c_{\mathbf f}\)。[原始文獻](https://arxiv.org/html/2201.02078v2#S21.SS8)

## 2. 命題：跨曲線的 leading-ratio 校準

假設式 (1) 在自由的 \(L[[t]]\)-模及其相容線性 Coleman 映射中成立，且

\[
z_E(t)=t\kappa_E+O(t^2),\quad \kappa_E\ne0,
\qquad
\ell_0:=\operatorname{Col}_0(z_0)(0)\ne0,
\]

\(A_E(0)A_0(0)C_\pi\ne0\)。定義

\[
B_{E,2}=[t^2]\widehat B_E(t),\qquad
r_{0,1}=[t]\operatorname{Col}_0(\widehat B_0(t)).
\]

則 \(r_{0,1}\ne0\)，而且

\[
\boxed{\displaystyle
\kappa_E=
\frac{A_0(0)\ell_0}{A_E(0)}
\frac{B_{E,2}}{r_{0,1}}.}
\tag{2}
\]

**證明。** \(j(t)=t/L+O(t^2)\)，所以直接取係數得

\[
B_{E,2}=\frac{C_\pi A_E(0)}L\kappa_E,
\qquad
r_{0,1}=\frac{C_\pi A_0(0)}L\ell_0.
\]

第二式的右端非零。將兩式相除並整理得式 (2)。分子是目標曲線的類，分母是係數域中的純量，沒有把不同曲線的 cohomology 向量直接相除。證畢。

同一個 quotient scalar、共同 frame 變更，以及 \(X'=sX+O(X^2)\) 所造成的 leading 因子 \(s^{-n}\)，在式 (2) 中一同消去。這不要求把 n 假設為 1。若只把其中一條曲線另行乘一個未知尺度，消去便不成立；共同規範是必要假設。

沿用 Attack 06 的 \(\kappa_E=16s_{11}\operatorname{adj}(H)\ell\)，在 \(\det H\ne0\)、\(\ell(x)\ne0\) 時，也得到

\[
s_{11}=\frac{A_0(0)\ell_0}{16A_E(0)}
\frac{h(x,B_{E,2})}{r_{0,1}\det(H)\ell(x)}.
\tag{3}
\]

式 (2)–(3) 消去獨立求 C 的需要；它們仍要求真正構造 \(B_{E,2}\) 與 \(r_{0,1}\)。本輪沒有以式 (1) 反向定義這兩個輸入，再把恆等式當成新證據。

## 3. 實際校準曲線與新有限計算

選

\[
E_0:\ y^2+y=x^3+x^2-769x-8470,
\]

即 LMFDB `19.a1`（Cremona `19a2`）。導子 19、秩零及標籤對照取自 [LMFDB](https://www.lmfdb.org/EllipticCurve/Q/19/a/1)；本輪另外直接數點得到 \(a_{11}=3\)，所以在 11 普通。曾考慮的 level-17 partner 有 \(a_{11}=0\)，沒有作為 ordinary 校準曲線使用。

`calibrator.py` 從 \(\mathbf P^1(\mathbf F_{19})\) 的 20 個生成元建立 S、R 的 Manin 關係，在 **Q** 上消去後得到維數 3。X_0(19) 的 genus 是 1；T2 的 cusp 特徵值 0 與 Eisenstein 特徵值 3 分離。正負 involution 各得到一條有理特徵線。這個結構識別了 level-19 的 cusp form；另在 3、5、7、11、13 檢查 Hecke 作用與直接點數一致。

period 規範完全留在輸出：正號 primitive vector 的第 0 座標是 2，除以 2 後該座標為 1；負號 primitive vector 第 4 座標為 1。先建立 characteristic-zero 向量再 reduction，避免僅有模 11 eigenline 卻未識別提升的問題。這不是對某一 isogenous curve 的 Neron period 數值作未聲明的換算。

第一層 ordinary measure 與 \(\chi_8\)-twisted、\(x^{-1}\) moment 的結果如下（數字均由 [實際輸出](../data/calibrator-19a1.json) 產生）：

| 量 | mod 11 |
|---|---:|
| ordinary unit root \(\alpha_0\) | 3 |
| twisted unit root \(\chi_8(11)\alpha_0\) | 8 |
| \(L_p(E_0,\mathbf 1)\)，\(\mathbf 1\) 指平凡乘法角色 | 9 |
| \(L_p(E_0\otimes\chi_8,x^{-1})\) | 4 |
| smoothing \(26\) | 4 |
| 三個非零因子的乘積 | 1 |
| ordinary adjoint Euler multiplier | 7 |

完整的十項 twisted cusp sums 為

\[
(4,4,0,2,9,2,9,0,7,7),
\quad \sum a^{-1}S_a=10\pmod{11},
\quad 8^{-1}\cdot10=4\pmod{11}.
\]

正號 ordinary 值同時滿足

\[
\sum_a\mu(a+11\mathbf Z_{11})
=(1-3^{-1})^2\Phi^+(0)=9\pmod{11}.
\]

因此校準所需的兩個 L-value 不會在這個中心引入零點。adjoint 的 Euler factor 非零；其完整 period 比值 \(D_0\) 沒有在本輪算出。把這些有限結果用於式 (2) 前，Kato/Coleman/adjoint 規範必須與這兩條模符號 period 對齊；不能將表格稱為完整 \(A_0(0)\ell_0\) 的數值。

ordinary 測度相容性由 Hecke 關係與 \(\alpha^2-a_{11}\alpha+11=0\) 推出；有理 eigenline 的取值與 ordinary 根均有整提升，故模 11 非零給出所選 period 下的真正非零性。程式另在分母 121 的下一層逐項核對 distribution relation。

## 4. 提前校準的版本還差一個 transport

在 full mixed Perrin–Riou regulator 中，C1.9 給出 \(R_i(X,t)=c_{\mathbf f}(X)U_i(X,t)\)。秩零校準可令 \(U_0(0,0)\ne0\)，所以 \(R_0(X,0)\) 與 \(c_{\mathbf f}(X)\) 有相同 X 消失階數。這是可用來探測未知 n 的 observable。

但 C1.7 的 \(b_{\mathbf f}^+(0)=c_r\eta_f\) 還帶有固定商 transport。若記為 \(q_{\mathbf f}\)，則按定義可寫

\[
R_i^{\mathrm{lead}}=
q_{\mathbf f}\,\operatorname{Col}_i(\widehat B_i)/j,
\qquad C_\pi=c_{\mathrm{lead}}/q_{\mathbf f}.
\]

所以單用原始 \(R_0\) 去除 full BF family 的零點，尚不能默認 \(q_{\mathbf f}=1\)。式 (2) 在兩個已同樣投影的類之間取比，會自動消去此因子。這是獨立上下文審查指出、並納入本稿的實質限制。

另外，generic 輔助 Galois representation 不提供 Eisenstein 的一維商；順序必須是先處理權重首項，再特殊化、投影。沒有把 generic 類直接投向不存在的 \(\psi=1\) 商，也沒有沿 X=t 替代這些操作。

Polo–Rivero–Wu 的另一條 Kato-to-units 路線使用不同 period 與額外假設；本稿不需要以那條路線來令兩個字母同為 C 的常數相等。[v3 原文](https://arxiv.org/html/2501.01514v3)

## 5. 核驗及下一個可交付物

有限算術包含正负有理 eigenline、額外 Hecke 檢查、兩種測度的下一層相容性、獨立 period rescaling 控制及四個具名錯誤檢查。形式程式以精確分數驗證 288 組共同常數／階數／權重規範，另檢查錯誤比例、factorial、quotient transport 與對角線污染。一般式 (2) 的依據仍是第二節的證明。

下一個真正的算術輸入是：共同 Eisenstein 商下、由原始 Beilinson–Flach 構造取得的校準係數 \(r_{0,1}\) 與目標向量 \(B_{E,2}\)。若能產出兩者，式 (2) 就給出相對校準的 Kato leading class。從該類進一步識別有理 determinant 及無窮遠 regulator 仍是獨立工作；本輪的局部非零數字沒有取代這個比較。

本輪已交付消元公式與可用校準 partner。真實 BF 類、C 的數值、s11 及完整 BSD 結論仍未產出。
