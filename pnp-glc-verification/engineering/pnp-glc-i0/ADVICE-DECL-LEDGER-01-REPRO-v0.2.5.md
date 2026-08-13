# ADVICE-DECL-LEDGER-01：v0.2.4 反例與 v0.2.5 回歸

分類：accepted-record declaration/ledger consistency Counterexample；不是實際 truth-table resource hiding、correctness、signature/closure bypass或 P/NP 結果。

## Frozen v0.2.4 反例

合法 PARITY streaming record只把 required `admissibility.advice` 改成 `one truth table per n`，其餘仍為 single uniform program、null generator、declared/observed access none、advice/generated-table bytes為0且 generation time/space/output為0；同步 projection/trace/map並有效簽章後仍可 accepted。原因是該欄雖位於 admissibility且 required，卻只是 unconstrained string，所有 gate與ledger derivation都不讀它。

AI-1 addendum SHA-256：`4F9FD695377D6B891C6B7D62B86F2F81D82FCD15DC3AABAE067820B58EDA2D8B`。AI-3 formal/interface report SHA-256：`EC42899B9CC5E375CF756A76EE34F970D7E52B2BEF755D8BFC9136B9BE39CE00`。

## v0.2.5 修補

- 移除 free-text `advice`，改為 typed `advice_mode`。
- schema對 mode→generator／uniformity／quantifier／access／ledger做 fail-closed conditional。
- external `ExpectedAdviceDecl(family, mechanism)`與 `_advice_declaration_matches`再做 family/mechanism映射及跨欄相等檢查。
- trace observation與 receipt observation仍由既有 authenticity／answer-access checks交叉核對。

## Executable regression

```powershell
$env:PYTHONUTF8='1'
python scripts/reproduce_advice_decl_ledger_v025.py .
```

本地觀察：exit 0；4 negative probes、3合法 none-advice positive controls、1 table-binding control、unexpected `[]`。

兩個直接矛盾負例由 schema拒絕：table mode + null generator/none access/zero ledger；none mode + table generator/positive ledger。兩個 schema-valid反向負例由 external validator拒絕並產生 `advice-declaration-ledger-binding`：stream mechanism搭配完整 table declaration，以及 table mechanism搭配完整 none declaration。所有負例都不被 accepted。reproducer SHA-256：`A414C1A5BAD1F99AA6B34705EFC1C8D5C21BFD40D86D2EEABFB9A447F76C72BA`。

以上只建立 bounded I0 advice declaration一致性；不是實際任意 advice machine或 nonuniform complexity framework 的一般定理。
