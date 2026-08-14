# 16｜696.e1 Chebotarev Support Family

## Prime family

定義：

$$
\mathcal P
=
\left\{
q\text{ prime}:
q\equiv1\pmod{24},
\left(\frac q{29}\right)=1,
f_2\bmod q\text{ irreducible}
\right\}.
$$

---

# Why the splitting conditions work

若：

$$
q\equiv1\pmod{24},
$$

則：

$$
q\equiv1\pmod8,
\qquad
q\equiv1\pmod3.
$$

因此在：

$$
\mathbb Q(\sqrt q)
$$

中：

- $2$ split；
- $3$ split。

再加：

$$
\left(\frac q{29}\right)=1,
$$

得 $29$ split。

所以 conductor所有 primes：

$$
2,3,29
$$

都 split。

---

# Chebotarev compatibility

令 $L$ 為 $f_2$ Galois closure。

$$
\mathrm{Gal}(L/\mathbb Q)=S_3.
$$

quadratic resolvent：

$$
F_0=\mathbb Q(\sqrt{-174}).
$$

令：

$$
K=\mathbb Q(\zeta_{24},\sqrt{29}).
$$

$K$ abelian，而 $S_3$ extension唯一 nontrivial normal abelian subfield是 $F_0$。

又：

$$
\sqrt{-174}=\sqrt{-6}\sqrt{29},
$$

且：

$$
\mathbb Q(\sqrt{-6})\subset\mathbb Q(\zeta_{24}).
$$

所以：

$$
L\cap K=F_0.
$$

因此：

$$
[LK:\mathbb Q]=48.
$$

取：

$$
(\sigma,1),
$$

其中 $\sigma$ 是 $S_3$ 的 3-cycle。

3-cycle在 $F_0$ 上 trivial，所以這是 fiber-product Galois group中的合法 element。

其 conjugacy class大小：

$$
2.
$$

故 Chebotarev density：

$$
\boxed{
\frac2{48}=\frac1{24}.
}
$$

---

# Automatic ordinary

$q$ inert in cubic field：

$$
\Longleftrightarrow
\mathrm{Frob}_q
\text{ 在 }GL_2(\mathbb F_2)\simeq S_3
\text{ 是 order-3 element}.
$$

order-3 element characteristic polynomial：

$$
X^2+X+1,
$$

所以 trace：

$$
1\pmod2.
$$

故：

$$
a_q(E)\equiv1\pmod2.
$$

即 $a_q$ odd。

$q\ge5$ 時若 supersingular：

$$
q\mid a_q
$$

加 Hasse bound會迫使：

$$
a_q=0,
$$

矛盾。

因此：

$$
\boxed{
q\in\mathcal P\Rightarrow q\text{ good ordinary for }E.
}
$$

---

# First explicit prime

$$
q=241.
$$

檢查：

$$
241\equiv1\pmod{24},
$$

$$
241\bmod29=9
$$

為 quadratic residue，

$f_2$ mod $241$ 無 root，故 irreducible。

直接 point count：

$$
a_{241}(E)=-7.
$$

所以第一個 explicit twist parameter可以取：

$$
\boxed{d=241}.
$$
