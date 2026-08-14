# 27｜Revised Derived Theorem Candidate

令：

$$
E:\ y^2=x^3+x^2+8x-16.
$$

令：

$$
\mathcal P
=
\left\{
q\text{ prime}:
q\equiv1\pmod{24},\
\left(\frac q{29}\right)=1,\
x^3+x^2+8x-16
\text{ irreducible mod }q
\right\}.
$$

則：

$$
\delta(\mathcal P)=\frac1{24}.
$$

**Derived theorem candidate：**

$$
\boxed{
\forall q\in\mathcal P,\quad
\operatorname{BSD}(E^{(q)})
}
$$

其中 $E^{(q)}$ 表示 quadratic twist by $q$。

## Proof router

### p=2

Banwait–Huang Theorem 2.14 + Creutz–Miller base full BSD。

### p=q

BSTW Theorem 9.21(c) 的 quadratic-twist clause + rank-zero descent，
ramK witness $29$。

### odd good ordinary p

Skinner Theorem C，witness $29$。

### p=3

Skinner Theorem C，witness $29$。

### p=29

Skinner Theorem C，witness $3$。

### odd good supersingular p

Fouquet–Wan Theorem 1.7 + Corollary 1.10，nonsplit Steinberg witness $29$。

所有 primes exhaustive。

## Claim label

目前：

```text
DERIVED THEOREM CANDIDATE
```

若 novelty/citation referee再通過，可進：

```text
PREPRINT CANDIDATE
```

是否稱「new theorem」必須由 novelty audit另外決定。
