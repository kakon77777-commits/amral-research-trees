# 06｜Witness-Network v0.3 Integration

fixed odd additive prime \(p\) 的 certificate更新為：

```text
FW_PROFILE
    default = FW17_EXACT

GLOBAL_H1
    E[p] absolutely irreducible over G_Q

LOCAL_H2
    if potentially multiplicative:
        FAIL

    elif local E[p] irreducible over F_p:
        PASS

    else:
        construct local p-isogeny phi
        construct dual phihat

        kernel(phi) Qp-linear root?
        kernel(phihat) Qp-linear root?

        either YES -> FAIL
        both NO    -> PASS

H3
    nonsplit multiplicative witness ell != p
    p ∤ v_ell(Delta)

PERIOD
    modular/Neron p-adic compatibility

FINAL
    all PASS -> fixed additive p certified by Fouquet-Wan
```

## Global consequence

odd additive primes依然只產生有限 table：

\[
\mathcal A_{\rm odd}(E).
\]

因此：

\[
\forall p
\]

沒有重新膨脹。

v0.3 的真正改善是：

\[
\boxed{
\text{A2 H2 UNKNOWN}
\to
\text{exact finite local isogeny test}.
}
\]
