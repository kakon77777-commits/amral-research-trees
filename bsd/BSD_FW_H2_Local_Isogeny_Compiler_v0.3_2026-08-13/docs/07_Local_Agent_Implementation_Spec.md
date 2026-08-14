# 07｜Local Agent Implementation Spec

## Goal

實作：

```text
certify_fw_h2(E, p, profile="FW17_EXACT")
```

輸出必須可 replay，不可只回 boolean。

---

## Required outputs

```json
{
  "curve": "...",
  "p": 5,
  "profile": "FW17_EXACT",
  "global_abs_irreducible": "PASS",
  "potential_reduction": "...",
  "potentially_multiplicative": false,
  "local_reducibility_Fp": "REDUCIBLE",
  "phi": {
    "defined_over_Qp": true,
    "kernel_polynomial": "...",
    "kernel_linear_factor_Qp": false
  },
  "dual_phi": {
    "kernel_polynomial": "...",
    "kernel_linear_factor_Qp": false
  },
  "fw17_h2": "PASS",
  "evidence": []
}
```

---

## Backend rules

### Rule 1

優先使用 Sage/Magma 已有的 certified local isogeny / local factorization machinery。

不要用浮點 approximation決定：

```text
Q_p root
```

### Rule 2

若 backend只能判：

```text
local p-isogeny exists
```

但不能產 kernel character evidence，不能把它當 H2 verdict。

### Rule 3

kernel polynomial linear factor必須是 exact \(p\)-adic factorization /
Hensel certificate。

### Rule 4

若 representation local irreducible證書本身只是 heuristic：

```text
UNKNOWN
```

不可升 PASS。

---

## Regression fixtures

至少加入：

### Fixture A — \(p=3\) reducible
expected:
```text
FAIL
```

### Fixture B — potentially multiplicative additive
expected:
```text
FAIL
```

### Fixture C — reducible, phi kernel rational-x
expected:
```text
FAIL
```

### Fixture D — reducible, dual kernel rational-x
expected:
```text
FAIL
```

### Fixture E — reducible, both kernel polynomials no Qp-linear root
expected:
```text
PASS
```

### Fixture F — local irreducible
expected:
```text
PASS
```

---

## Do not infer

```text
Kodaira type alone -> PASS
no Qp rational p-torsion -> PASS
potentially supersingular -> PASS
global irreducible -> local irreducible
```

這四個都是禁止 shortcut。
