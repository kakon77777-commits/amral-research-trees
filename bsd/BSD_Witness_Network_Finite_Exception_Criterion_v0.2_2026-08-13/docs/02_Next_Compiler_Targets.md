# 02 | Next Compiler Targets

Priority order after v0.2:

## 1. Additive FW-H2 compiler

Input:
```text
p
Kodaira type
potential reduction type
local residual representation
```

Output:
```text
FW_H2_PASS / FAIL / UNKNOWN
```

No database scaling until this is exact.

## 2. Period compiler

Input:
```text
p
Kodaira type
optimality
modular degree / Manin evidence
```

Output:
```text
PERIOD_SAFE / UNKNOWN
```

## 3. Ordinary finite exception compiler

For
\[
p\mid g_{\rm mult},
\]
try:
- BCS Corollary 1.3.1;
- reducible ordinary theorem;
- direct Skinner witness if another local source exists.

## 4. Only then census

The first database output should count:
```text
GENERIC_PASS
FINITE_EXCEPTION_PASS
ADDITIVE_LOCAL_UNKNOWN
PERIOD_UNKNOWN
TRUE_REJECT
```

The UNKNOWN rows must remain visible.
